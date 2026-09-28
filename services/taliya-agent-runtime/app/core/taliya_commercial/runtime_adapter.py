from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from openai import AsyncOpenAI

from app.core.taliya_commercial.conductor import (
    ActionConductorProvider,
    ActionConductorProviderRequest,
    ActionConductorTurnResult,
    ConductorDecisionValidationError,
    ConductorProvider,
    ConductorProviderRequest,
    build_action_conductor_model_input_payload,
    build_conductor_model_input_payload,
    build_model_turn_context_payload,
    conduct_action_turn,
    conduct_turn,
)
from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.context_profile import build_runtime_context_profile
from app.core.taliya_commercial.decision_compiler import compile_action_decision
from app.core.taliya_commercial.renderer import render_validated_template_plan
from app.core.taliya_commercial.repair import RepairProvider, repair_conductor_decision
from app.core.taliya_commercial.runtime_state import (
    build_runtime_state_diff,
    canonical_diagnostic_ledger,
    merge_diagnostic_ledger,
)
from app.core.taliya_commercial.sales_inbox_projection import build_sales_inbox_projection
from app.core.taliya_commercial.schemas import (
    ConductorDecision,
    DeliveryEvent,
    ModelUsage,
    RenderedMessage,
    RepairResult,
    TraceRecord,
    TurnContext,
)
from app.core.taliya_commercial.trace_store import build_turn_trace
from app.core.taliya_commercial.turn_gate import BLOCKING_HUMAN_STATUSES
from app.core.taliya_commercial.turn_situation import build_turn_situation
from app.core.taliya_commercial.validators import validate_conductor_result
from app.domains.taliya_commercial.behavior_policy import assess_profile_name
from app.runtime.events import RuntimeEvent
from app.runtime.schemas import (
    AgentMessage,
    AgentOutput,
    AgentRunRequest,
    AgentRunResponse,
    DeliveryControl,
    DiagnosticOutput,
    HandoffOutput,
    LeadFact,
    RuntimeDecision,
    SourceRef,
    ToolResult,
    Usage,
    WaitlistAction,
)
from app.runtime.usage import estimate_cost_usd
from app.shared.memory.postgres import InMemoryMemoryStore, RuntimeState


class Spec011RuntimeAdapterError(RuntimeError):
    pass


@dataclass(frozen=True)
class ShadowModeControl:
    enabled: bool = False
    reason: str | None = None


@dataclass(frozen=True)
class ActionTurnRuntimeResult:
    result: ActionConductorTurnResult
    repair_attempt_count: int = 0


async def run_spec011_agent_turn(
    request: AgentRunRequest,
    *,
    memory_store: InMemoryMemoryStore,
    provider: str,
    model: str,
    conductor_provider: ConductorProvider | None = None,
    action_conductor_provider: ActionConductorProvider | None = None,
    repair_provider: RepairProvider | None = None,
) -> AgentRunResponse:
    run_id = f"run_spec011_{uuid4().hex}"
    turn_id = _stable_turn_id(request)
    shadow_control = _shadow_mode_control(request)
    state = await memory_store.load_state(
        request.conversation.conversation_id,
        request.agent_key,
    )
    recent_events = await memory_store.list_events(request.conversation.conversation_id)
    context_profile = build_runtime_context_profile(request=request, state=state)
    context = build_turn_context(
        turn_id=turn_id,
        request=request,
        state=state,
        recent_events=recent_events,
        max_recent_transcript_items=context_profile.max_recent_transcript_items,
        product_knowledge_keys=list(context_profile.product_knowledge_keys),
        spec006_contract_keys=list(context_profile.spec006_contract_keys),
    )
    if _state_blocks_ai_reply(state):
        return await _human_pause_suppressed_response(
            request=request,
            memory_store=memory_store,
            state=state,
            run_id=run_id,
            turn_id=turn_id,
            context=context,
        )

    if conductor_provider is not None:
        conductor_result = await conduct_turn(context, provider=conductor_provider)
        decision = conductor_result.decision
        model_usage = conductor_result.model_usage
        turn_situation_payload: dict[str, Any] = {}
        action_decision_payload: dict[str, Any] = {}
        action_repair_attempt_count = 0
    else:
        action_conductor = action_conductor_provider or _action_conductor_provider_for(
            provider=provider,
            model=model,
        )
        action_runtime_result = await _conduct_action_turn_with_single_repair(
            context,
            provider=action_conductor,
        )
        action_result = action_runtime_result.result
        turn_situation = build_turn_situation(context)
        turn_situation_payload = turn_situation.model_dump(mode="json")
        action_decision_payload = action_result.decision.model_dump(mode="json")
        action_repair_attempt_count = action_runtime_result.repair_attempt_count
        decision = compile_action_decision(
            action_result.decision,
            context=context,
            turn_situation=turn_situation,
        )
        model_usage = action_result.model_usage
    validator_result = validate_conductor_result(decision, context)
    repair_result = RepairResult()
    active_repair_provider = repair_provider or _repair_provider_for(
        provider=provider,
        model=model,
    )

    if validator_result.status != "passed" and active_repair_provider is not None:
        repair_result = await repair_conductor_decision(
            decision,
            context,
            validator_result,
            provider=active_repair_provider,
        )
        if repair_result.status == "repaired" and repair_result.repaired_decision is not None:
            decision = repair_result.repaired_decision
            validator_result = validate_conductor_result(decision, context).model_copy(
                update={
                    "repair_attempt_count": repair_result.attempt_count,
                    "final_disposition": "repaired",
                }
            )
            if repair_result.model_usage is not None:
                model_usage = _combine_usage(model_usage, repair_result.model_usage)

    if validator_result.status != "passed":
        codes = ",".join(issue.code for issue in validator_result.errors)
        details = json.dumps(
            [issue.model_dump(mode="json") for issue in validator_result.errors[:12]],
            ensure_ascii=True,
            separators=(",", ":"),
        )
        raise Spec011RuntimeAdapterError(
            f"spec011_validation_failed:{codes}:{details}"
        )

    rendered_messages = render_validated_template_plan(
        decision.template_plan,
        validator_result,
        channel=request.channel,
    )
    runtime_state_diff = build_runtime_state_diff(
        decision,
        validator_result,
        repair_result=repair_result if validator_result.final_disposition == "repaired" else None,
    )
    delivery_events = _delivery_events_for_turn(
        request=request,
        context=context,
        decision=decision,
        rendered_messages=rendered_messages,
        shadow_control=shadow_control,
    )
    sales_inbox_projection = build_sales_inbox_projection(
        context=context,
        decision=decision,
        validator_result=validator_result,
        runtime_state_diff=runtime_state_diff,
        delivery_events=delivery_events,
    )
    trace = build_turn_trace(
        context=context,
        decision=decision,
        validator_result=validator_result,
        repair_result=repair_result,
        render_plan=decision.template_plan,
        rendered_messages=rendered_messages,
        model_usage=model_usage,
        runtime_state_diff=runtime_state_diff,
        delivery_events=delivery_events,
        sales_inbox_projection=sales_inbox_projection,
        turn_situation=turn_situation_payload,
        action_decision=action_decision_payload,
        action_repair_attempt_count=action_repair_attempt_count,
    )

    if shadow_control.enabled:
        await _persist_shadow_turn(
            memory_store=memory_store,
            request=request,
            run_id=run_id,
            context=context,
            decision=decision,
            rendered_messages=rendered_messages,
            runtime_state_diff=runtime_state_diff,
            model_usage=model_usage,
            trace=trace,
            shadow_control=shadow_control,
        )
    else:
        await _persist_turn(
            memory_store=memory_store,
            request=request,
            state=state,
            run_id=run_id,
            context=context,
            decision=decision,
            rendered_messages=rendered_messages,
            runtime_state_diff=runtime_state_diff,
            model_usage=model_usage,
            trace=trace,
        )

    return _agent_run_response(
        request=request,
        run_id=run_id,
        decision=decision,
        rendered_messages=rendered_messages,
        model_usage=model_usage,
        trace=trace,
        context=context,
        shadow_control=shadow_control,
    )


def _delivery_events_for_turn(
    *,
    request: AgentRunRequest,
    context: TurnContext,
    decision: ConductorDecision,
    rendered_messages: list[RenderedMessage],
    shadow_control: ShadowModeControl,
) -> list[DeliveryEvent]:
    events = [
        DeliveryEvent(
            event="delivery_suppressed" if shadow_control.enabled else "rendered",
            idempotency_key=request.message.idempotency_key,
            status="suppressed" if shadow_control.enabled else "planned",
            metadata={
                "message_count": len(rendered_messages),
                "shadow_mode": shadow_control.enabled,
                "delivery_suppressed": shadow_control.enabled,
                "suppression_reason": shadow_control.reason,
            },
        )
    ]
    if decision.waitlist.status == "joined":
        events.append(
            DeliveryEvent(
                event="waitlist_joined",
                idempotency_key=(
                    f"waitlist:{request.conversation.conversation_id}:"
                    f"{request.message.idempotency_key}"
                ),
                status="recorded",
                metadata={"joined_at": context.inbound.timestamp or _utc_now_iso()},
            )
        )
    return events


def _utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _conductor_provider_for(*, provider: str, model: str) -> ConductorProvider:
    if provider == "openai":
        return OpenAIConductorProvider(model=model)
    raise Spec011RuntimeAdapterError("spec011_conductor_provider_required")


def _action_conductor_provider_for(
    *,
    provider: str,
    model: str,
) -> ActionConductorProvider:
    if provider == "openai":
        return OpenAIActionConductorProvider(model=model)
    raise Spec011RuntimeAdapterError("spec011_action_conductor_provider_required")


async def _conduct_action_turn_with_single_repair(
    context: TurnContext,
    *,
    provider: ActionConductorProvider,
) -> ActionTurnRuntimeResult:
    try:
        return ActionTurnRuntimeResult(
            result=await conduct_action_turn(context, provider=provider)
        )
    except ConductorDecisionValidationError as first_error:
        return ActionTurnRuntimeResult(
            result=await conduct_action_turn(
                context,
                provider=_ActionRepairProvider(provider, first_error),
            ),
            repair_attempt_count=1,
        )


class _ActionRepairProvider:
    def __init__(
        self,
        provider: ActionConductorProvider,
        first_error: ConductorDecisionValidationError,
    ) -> None:
        self.provider = provider
        self.first_error = first_error

    async def __call__(self, request: ActionConductorProviderRequest) -> Any:
        repaired_request = request.model_copy(
            update={
                "instructions": [
                    *request.instructions,
                    "Previous ConductorActionDecision was rejected before "
                    f"compilation: {self.first_error}. Return a corrected "
                    "ConductorActionDecision only.",
                    "You must choose selected_action from "
                    "turn_situation.allowed_actions and use only official fact keys "
                    "present in turn_situation.official_fact_keys_available.",
                ],
                "provider_requirements": [
                    *request.provider_requirements,
                    "This is the single action-level repair attempt. Do not add "
                    "route, state, template_plan, render_plan, or customer-facing text.",
                ],
            }
        )
        result = self.provider(repaired_request)
        if hasattr(result, "__await__"):
            return await result
        return result


def _repair_provider_for(*, provider: str, model: str) -> RepairProvider | None:
    if provider == "openai":
        return OpenAIRepairProvider(model=model)
    return None


class OpenAIActionConductorProvider:
    def __init__(self, *, model: str) -> None:
        self.model = model
        self.client = AsyncOpenAI()

    async def __call__(self, request: ActionConductorProviderRequest) -> dict[str, Any]:
        response = await self.client.responses.create(
            model=self.model,
            instructions="\n".join(request.instructions),
            input=json.dumps(
                build_action_conductor_model_input_payload(request),
                ensure_ascii=True,
                separators=(",", ":"),
            ),
            text={
                "format": {
                    "type": "json_schema",
                    "name": "taliya_spec011_action_conductor_decision",
                    "schema": request.response_schema,
                    "strict": False,
                }
            },
        )
        usage = getattr(response, "usage", None)
        decision_payload = json.loads(response.output_text)
        input_tokens = int(getattr(usage, "input_tokens", 0) or 0)
        output_tokens = int(getattr(usage, "output_tokens", 0) or 0)
        return {
            "decision": decision_payload,
            "model_usage": {
                "model": self.model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost_usd": estimate_cost_usd(
                    self.model,
                    input_tokens,
                    output_tokens,
                ),
            },
        }


class OpenAIConductorProvider:
    def __init__(self, *, model: str) -> None:
        self.model = model
        self.client = AsyncOpenAI()

    async def __call__(self, request: ConductorProviderRequest) -> dict[str, Any]:
        response = await self.client.responses.create(
            model=self.model,
            instructions="\n".join(request.instructions),
            input=json.dumps(
                build_conductor_model_input_payload(request),
                ensure_ascii=True,
                separators=(",", ":"),
            ),
            text={
                "format": {
                    "type": "json_schema",
                    "name": "taliya_spec011_conductor_decision",
                    "schema": request.response_schema,
                    # The ConductorDecision contract includes validator-checked maps
                    # for template variables and final diagnostic fields. OpenAI
                    # strict schema mode rejects those map shapes; Pydantic plus
                    # Spec 011 validators remain the hard boundary after JSON output.
                    "strict": False,
                }
            },
        )
        usage = getattr(response, "usage", None)
        decision_payload = json.loads(response.output_text)
        input_tokens = int(getattr(usage, "input_tokens", 0) or 0)
        output_tokens = int(getattr(usage, "output_tokens", 0) or 0)
        return {
            "decision": decision_payload,
            "model_usage": {
                "model": self.model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost_usd": estimate_cost_usd(
                    self.model,
                    input_tokens,
                    output_tokens,
                ),
            },
        }


class OpenAIRepairProvider:
    def __init__(self, *, model: str) -> None:
        self.model = model
        self.client = AsyncOpenAI()

    async def __call__(self, request: Any) -> dict[str, Any]:
        response = await self.client.responses.create(
            model=self.model,
            instructions="\n".join(request.instructions),
            input=json.dumps(
                {
                    "provider_requirements": request.provider_requirements,
                    "original_decision": request.original_decision.model_dump(mode="json"),
                    "validator_errors": [
                        error.model_dump(mode="json")
                        for error in request.validator_errors
                    ],
                    "context": build_model_turn_context_payload(request.context),
                },
                ensure_ascii=True,
                separators=(",", ":"),
            ),
            text={
                "format": {
                    "type": "json_schema",
                    "name": "taliya_spec011_repaired_conductor_decision",
                    "schema": request.response_schema,
                    "strict": False,
                }
            },
        )
        usage = getattr(response, "usage", None)
        decision_payload = json.loads(response.output_text)
        input_tokens = int(getattr(usage, "input_tokens", 0) or 0)
        output_tokens = int(getattr(usage, "output_tokens", 0) or 0)
        return {
            "decision": decision_payload,
            "model_usage": {
                "model": self.model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost_usd": estimate_cost_usd(
                    self.model,
                    input_tokens,
                    output_tokens,
                ),
            },
        }


def _agent_run_response(
    *,
    request: AgentRunRequest,
    run_id: str,
    decision: ConductorDecision,
    rendered_messages: list[RenderedMessage],
    model_usage: ModelUsage,
    trace: TraceRecord,
    context: TurnContext,
    shadow_control: ShadowModeControl,
) -> AgentRunResponse:
    delivery_control = DeliveryControl(
        shadow_mode=shadow_control.enabled,
        delivery_suppressed=shadow_control.enabled,
        suppression_reason=shadow_control.reason if shadow_control.enabled else None,
        rendered_message_count=len(rendered_messages),
        trace_contains_rendered_messages=bool(rendered_messages),
    )
    response_messages = [] if shadow_control.enabled else rendered_messages
    safety_flags = ["shadow_mode", "delivery_suppressed"] if shadow_control.enabled else []
    tool_results = (
        [
            ToolResult(
                name="shadow_mode",
                status="ok",
                summary=f"delivery_suppressed:{shadow_control.reason or 'spec011_shadow_mode'}",
            )
        ]
        if shadow_control.enabled
        else []
    )
    eval_trace_artifacts = _eval_trace_artifacts(request, trace)
    return AgentRunResponse(
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        lead_id=request.conversation.lead_id,
        agent_key=request.agent_key,
        agent_family=request.agent_family,
        owner_scope=request.owner_scope,
        tenant_id=request.tenant_id,
        current_agent=_current_agent_name(decision),
        status="human_paused" if _handoff_pauses_automation(decision) else "succeeded",
        trace_id=trace.trace_id,
        output=AgentOutput(
            decision=_runtime_decision(decision, context=context),
            messages=[
                AgentMessage(
                    text=message.text,
                    channel_hint=request.channel,
                    kind="text",
                    template_id=message.template_id,
                    requires_product_source=_message_requires_product_source(message),
                )
                for message in response_messages
            ],
            lead_facts=[
                LeadFact(
                    key=fact.key,
                    value=str(fact.value),
                    confidence=fact.confidence,
                    evidence=fact.evidence,
                )
                for fact in decision.facts
                if fact.source == "user_message"
            ],
            diagnostic=_diagnostic_output(
                decision,
                context=context,
                sales_inbox_projection=trace.sales_inbox_projection,
            ),
            waitlist_action=WaitlistAction(
                status=decision.waitlist.status,
                missing_fields=decision.waitlist.missing_details,
            ),
            handoff=HandoffOutput(
                status=decision.handoff.status,
                reason=decision.handoff.reason,
            ),
            sources=_source_refs(context),
            safety_flags=safety_flags,
            tool_results=tool_results,
            usage=Usage(
                model=model_usage.model,
                input_tokens=model_usage.input_tokens,
                output_tokens=model_usage.output_tokens,
                cost_usd=model_usage.cost_usd,
            ),
            confidence=decision.confidence,
            **eval_trace_artifacts,
        ),
        delivery_control=delivery_control,
    )


def _eval_trace_artifacts(
    request: AgentRunRequest,
    trace: TraceRecord,
) -> dict[str, Any]:
    if request.metadata.get("spec011_eval_trace") is not True:
        return {}
    return {
        "context_snapshot": trace.input.model_dump(mode="json"),
        "turn_situation": dict(trace.turn_situation),
        "action_decision": dict(trace.action_decision),
        "action_repair_attempt_count": trace.action_repair_attempt_count,
        "conductor_json": trace.decision.model_dump(mode="json"),
        "validator_results": [trace.validator_result.model_dump(mode="json")],
        "repair_attempts": [trace.repair_result.model_dump(mode="json")],
        "runtime_state": dict(trace.runtime_state_diff),
        "sales_inbox_projection": trace.sales_inbox_projection.model_dump(mode="json"),
        "delivery_events": [
            event.model_dump(mode="json", exclude_none=True)
            for event in trace.delivery_events
        ],
        "trace_complete": trace.trace_complete,
    }


def _runtime_decision(
    decision: ConductorDecision,
    *,
    context: TurnContext,
) -> RuntimeDecision:
    return RuntimeDecision(
        previous_state=decision.previous_state,
        current_state=decision.current_state,
        next_state=decision.next_state,
        route=decision.route,
        opening_type=_runtime_opening_type(decision),
        detected_intents=decision.detected_intents,
        direct_question_present=decision.direct_question_present,
        direct_question_answered_first=decision.direct_question_answered_first,
        diagnostic_action=decision.diagnostic.action,
        diagnostic_allowed_now=decision.diagnostic.action != "none",
        waitlist_allowed_now=decision.waitlist.status != "none",
        demo_status=decision.demo.status,
        demo_next_step=decision.demo.next_step,
        profile_name_usage=_runtime_profile_name_usage(decision, context),
        facts_used=_fact_evidence(decision),
        facts_missing=decision.repair_hints,
        template_ids=[item.template_id for item in decision.template_plan.items],
        template_variables={
            item.template_id: {
                key: variable.model_dump(mode="json")
                for key, variable in item.variables.items()
            }
            for item in decision.template_plan.items
        },
        render_plan=[item.model_dump(mode="json") for item in decision.template_plan.items],
        diagnostic_ledger_status=_diagnostic_ledger_status(decision),
        next_question_kind=_runtime_next_question_kind(
            decision.diagnostic.next_question_key
        ),
    )


def _runtime_opening_type(decision: ConductorDecision) -> str:
    template_ids = {
        item.template_id.split("#", 1)[0] for item in decision.template_plan.items
    }
    if template_ids.intersection(
        {"opening.cold_greeting", "opening.cold_greeting_named"}
    ):
        return "cold_greeting_only"
    if "opening.widget_empty_diagnostic" in template_ids:
        return "widget_opening"
    if template_ids.intersection({"opening.site_cta", "opening.general_interest"}):
        return "site_forced_message"
    if "opening.instagram_source" in template_ids:
        return "social_source_opening"
    if "opening.diagnostic_cta" in template_ids:
        return "diagnostic_cta_opening"
    if decision.direct_question_present and decision.route == "product":
        return "direct_question_opening"
    return "none"


def _runtime_profile_name_usage(
    decision: ConductorDecision,
    context: TurnContext,
) -> str:
    if any("first_name" in item.variables for item in decision.template_plan.items):
        return "used_reliable_name"
    return _runtime_profile_name_usage_from_context(context)


def _runtime_profile_name_usage_from_context(context: TurnContext) -> str:
    profile_name = _channel_profile_name(context)
    if profile_name is None:
        return "not_available"

    if assess_profile_name(profile_name).status == "unreliable":
        return "ignored_unreliable_name"
    return "not_needed"


def _channel_profile_name(context: TurnContext) -> str | None:
    for fact in context.facts:
        if fact.key == "profile_name" and fact.source == "channel_metadata":
            value = str(fact.value or "").strip()
            return value or None
    return None


def _runtime_next_question_kind(next_question_key: str | None) -> str:
    """Translate Spec 011 diagnostic keys to the legacy RuntimeDecision enum."""
    if not next_question_key:
        return "none"
    return {
        "active_students_or_size": "plan_fit",
        "main_pain": "pain",
        "pain_detail": "pain",
        "current_process": "current_process",
        "priority": "priority",
        "urgency": "urgency",
    }.get(next_question_key, "clarification")


def _state_blocks_ai_reply(state: RuntimeState | None) -> bool:
    if state is None:
        return False
    return str(state.human_status or "").strip().lower() in BLOCKING_HUMAN_STATUSES


def _handoff_pauses_automation(decision: ConductorDecision) -> bool:
    return decision.handoff.status in {"requested", "active"}


def _diagnostic_output(
    decision: ConductorDecision,
    *,
    context: TurnContext,
    sales_inbox_projection: Any,
) -> DiagnosticOutput | None:
    if (
        decision.diagnostic.action == "none"
        and not decision.diagnostic.ledger_updates
        and not decision.diagnostic.final_fields
    ):
        if getattr(sales_inbox_projection, "diagnostic_status", None) == "completed":
            return _completed_diagnostic_output_from_context(
                decision=decision,
                context=context,
                sales_inbox_projection=sales_inbox_projection,
            )
        return None

    final_fields = decision.diagnostic.final_fields
    return DiagnosticOutput(
        status=_diagnostic_status(decision),
        ledger=[item.model_dump(mode="json") for item in decision.diagnostic.ledger_updates],
        facts_used=_fact_evidence(decision),
        main_bottleneck=_optional_string(final_fields.get("main_bottleneck")),
        crm_base_recommendation=_optional_string(final_fields.get("crm_base_recommendation")),
        first_recommended_step=_optional_string(final_fields.get("first_recommended_step")),
        indicated_agents=list(final_fields.get("indicated_agents") or []),
        plan_or_range_to_compare=_optional_string(final_fields.get("final_plan_or_range")),
        final_plan_line=_optional_string(final_fields.get("final_plan_line")),
        final_demo_line=_optional_string(final_fields.get("final_demo_line")),
        final_demo_next_step_question=_optional_string(final_fields.get("final_demo_next_step_question")),
        evidence=_fact_evidence(decision),
        confidence=decision.confidence,
        next_question=decision.diagnostic.next_question_key,
    )


def _completed_diagnostic_output_from_context(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    sales_inbox_projection: Any,
) -> DiagnosticOutput:
    final_fields = dict(context.sales_inbox_inputs.get("diagnostic_final_fields") or {})
    projection_fields = dict(getattr(sales_inbox_projection, "fields", {}) or {})
    evidence = _diagnostic_ledger_evidence(context)
    return DiagnosticOutput(
        status="completed",
        ledger=canonical_diagnostic_ledger(context.diagnostic_ledger),
        facts_used=evidence,
        main_bottleneck=_optional_string(final_fields.get("main_bottleneck")),
        crm_base_recommendation=_optional_string(
            final_fields.get("crm_base_recommendation")
        ),
        first_recommended_step=_optional_string(
            final_fields.get("first_recommended_step")
        ),
        indicated_agents=list(final_fields.get("indicated_agents") or []),
        plan_or_range_to_compare=_optional_string(
            projection_fields.get("final_plan_or_range")
            or final_fields.get("final_plan_or_range")
        ),
        final_plan_line=_optional_string(final_fields.get("final_plan_line")),
        final_demo_line=_optional_string(
            projection_fields.get("final_demo_line")
            or final_fields.get("final_demo_line")
        ),
        final_demo_next_step_question=_optional_string(
            final_fields.get("final_demo_next_step_question")
        ),
        evidence=evidence,
        confidence=decision.confidence,
        next_question=None,
    )


def _diagnostic_ledger_evidence(context: TurnContext) -> list[str]:
    evidence: list[str] = []
    seen: set[str] = set()
    for item in context.diagnostic_ledger:
        if not isinstance(item, dict):
            continue
        for value in item.get("evidence") or []:
            text = str(value).strip()
            if text and text not in seen:
                evidence.append(text)
                seen.add(text)
    return evidence


async def _persist_turn(
    *,
    memory_store: InMemoryMemoryStore,
    request: AgentRunRequest,
    state: RuntimeState | None,
    run_id: str,
    context: TurnContext,
    decision: ConductorDecision,
    rendered_messages: list[RenderedMessage],
    runtime_state_diff: dict[str, Any],
    model_usage: ModelUsage,
    trace: TraceRecord,
) -> None:
    next_state = state.model_copy(deep=True) if state else RuntimeState(
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        current_agent_name=_current_agent_name(decision),
    )
    next_state.current_agent_name = _current_agent_name(decision)
    if request.message.text:
        next_state.input_items.append(
            {
                "id": request.message.channel_message_id or request.message.idempotency_key,
                "role": "user",
                "content": request.message.text,
                "source": request.channel,
            }
        )
    for message in rendered_messages:
        next_state.input_items.append(
            {
                "id": f"{trace.trace_id}:{message.sequence}",
                "role": "assistant",
                "content": message.text,
                "template_id": message.template_id,
            }
        )

    state_set = dict(runtime_state_diff.get("set") or {})
    state_append = dict(runtime_state_diff.get("append") or {})
    runtime_decision = _runtime_decision(decision, context=context)
    next_state.last_decision = runtime_decision.model_dump(mode="json")
    next_state.last_route = decision.route
    next_state.last_opening_type = runtime_decision.opening_type
    next_state.profile_name_status = runtime_decision.profile_name_usage
    next_state.lead_facts = _merge_fact_updates(
        next_state.lead_facts,
        list(state_append.get("fact_updates") or []),
    )
    if "diagnostic" in state_set:
        next_state.diagnostic = dict(state_set["diagnostic"])
        next_state.diagnostic["ledger"] = merge_diagnostic_ledger(
            _existing_diagnostic_ledger(state),
            list(state_append.get("diagnostic_ledger") or []),
        )
    elif isinstance(next_state.diagnostic, dict):
        ledger = next_state.diagnostic.get("ledger")
        if isinstance(ledger, list):
            next_state.diagnostic["ledger"] = canonical_diagnostic_ledger(ledger)
    if "demo" in state_set:
        next_state.demo = dict(state_set["demo"])
    if "waitlist" in state_set:
        next_state.waitlist = dict(state_set["waitlist"])
    handoff = state_set.get("handoff")
    if isinstance(handoff, dict):
        handoff_status = str(handoff.get("status") or "none")
        next_state.human_status = (
            "active" if handoff_status in {"requested", "active"} else handoff_status
        )
        next_state.human_reason = _optional_string(handoff.get("reason"))
    next_state.cost_usd = round(next_state.cost_usd + model_usage.cost_usd, 6)
    next_state.product_source_version = _product_source_version(context)

    await memory_store.save_state(next_state)
    await memory_store.record_model_usage(
        request.conversation.conversation_id,
        {
            "run_id": run_id,
            "agent_key": request.agent_key,
            **model_usage.model_dump(mode="json"),
        },
    )
    await memory_store.record_event(
        RuntimeEvent(
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="usage",
            agent=_current_agent_name(decision),
            content="spec011_core_turn_completed",
            metadata={
                "trace_id": trace.trace_id,
                "decision_id": decision.decision_id,
                "template_ids": [item.template_id for item in decision.template_plan.items],
            },
        )
    )


async def _human_pause_suppressed_response(
    *,
    request: AgentRunRequest,
    memory_store: InMemoryMemoryStore,
    state: RuntimeState | None,
    run_id: str,
    turn_id: str,
    context: TurnContext,
) -> AgentRunResponse:
    trace_id = f"trace_{uuid4().hex}"
    reason = _optional_string(state.human_reason if state else None) or "human_handoff_active"
    decision = RuntimeDecision(
        previous_state=_previous_state_from_runtime_state(state),
        current_state="paused_by_human",
        next_state="paused_by_human",
        route="handoff",
        opening_type="none",
        detected_intents=[],
        direct_question_present=False,
        direct_question_answered_first=True,
        diagnostic_action="none",
        diagnostic_allowed_now=False,
        waitlist_allowed_now=False,
        profile_name_usage=_runtime_profile_name_usage_from_context(context),
        facts_used=[],
        facts_missing=[],
        template_ids=[],
        template_variables={},
        render_plan=[],
    )
    delivery_events = [
        {
            "event": "delivery_suppressed",
            "idempotency_key": request.message.idempotency_key,
            "status": "suppressed",
            "metadata": {
                "reason": "human_handoff_active",
                "turn_id": turn_id,
            },
        }
    ]
    eval_trace_artifacts = (
        {
            "context_snapshot": context.model_dump(mode="json"),
            "runtime_state": {
                "set": {"handoff": {"status": "active", "reason": reason}},
                "append": {},
            },
            "sales_inbox_projection": {
                "conversation_id": request.conversation.conversation_id,
                "lead_id": request.conversation.lead_id,
                "commercial_stage": "human_handoff",
                "handoff_status": "active",
                "fields": {
                    "handoff_reason": reason,
                    "human_active": True,
                    "ai_paused": True,
                },
            },
            "delivery_events": delivery_events,
            "trace_complete": True,
        }
        if request.metadata.get("spec011_eval_trace") is True
        else {}
    )
    output = AgentOutput(
        decision=decision,
        messages=[],
        handoff=HandoffOutput(status="active", reason=reason),
        safety_flags=["human_handoff_active", "ai_reply_suppressed"],
        tool_results=[
            ToolResult(
                name="human_handoff_pause",
                status="blocked",
                summary="ai_reply_suppressed:human_handoff_active",
            )
        ],
        usage=Usage(model=None, input_tokens=0, output_tokens=0, cost_usd=0),
        confidence="high",
        **eval_trace_artifacts,
    )
    await _persist_human_pause_suppressed_turn(
        request=request,
        memory_store=memory_store,
        state=state,
        run_id=run_id,
        trace_id=trace_id,
        decision=decision,
        reason=reason,
    )
    return AgentRunResponse(
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        lead_id=request.conversation.lead_id,
        agent_key=request.agent_key,
        agent_family=request.agent_family,
        owner_scope=request.owner_scope,
        tenant_id=request.tenant_id,
        current_agent="taliya_commercial_spec011_handoff_agent",
        status="human_paused",
        output=output,
        trace_id=trace_id,
        delivery_control=DeliveryControl(
            delivery_suppressed=True,
            suppression_reason="human_handoff_active",
            rendered_message_count=0,
            trace_contains_rendered_messages=False,
        ),
    )


async def _persist_human_pause_suppressed_turn(
    *,
    request: AgentRunRequest,
    memory_store: InMemoryMemoryStore,
    state: RuntimeState | None,
    run_id: str,
    trace_id: str,
    decision: RuntimeDecision,
    reason: str,
) -> None:
    next_state = state.model_copy(deep=True) if state else RuntimeState(
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        current_agent_name="taliya_commercial_spec011_handoff_agent",
    )
    next_state.current_agent_name = "taliya_commercial_spec011_handoff_agent"
    if request.message.text:
        next_state.input_items.append(
            {
                "id": request.message.channel_message_id or request.message.idempotency_key,
                "role": "user",
                "content": request.message.text,
                "source": request.channel,
                "delivery": "suppressed_by_human_handoff",
            }
        )
    next_state.human_status = "active"
    next_state.human_reason = reason
    next_state.last_decision = decision.model_dump(mode="json")
    next_state.last_route = decision.route
    next_state.last_opening_type = decision.opening_type
    next_state.profile_name_status = decision.profile_name_usage
    await memory_store.save_state(next_state)
    await memory_store.record_event(
        RuntimeEvent(
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="guardrail",
            agent="taliya_commercial_spec011_handoff_agent",
            content="spec011_human_pause_suppressed_ai_reply",
            metadata={
                "trace_id": trace_id,
                "reason": reason,
                "idempotency_key": request.message.idempotency_key,
            },
        )
    )


def _previous_state_from_runtime_state(state: RuntimeState | None) -> str:
    if state is None:
        return "new_lead"
    if state.last_decision:
        candidate = state.last_decision.get("next_state") or state.last_decision.get(
            "current_state"
        )
        if isinstance(candidate, str) and candidate.strip():
            return candidate
    return state.last_route or "new_lead"


async def _persist_shadow_turn(
    *,
    memory_store: InMemoryMemoryStore,
    request: AgentRunRequest,
    run_id: str,
    context: TurnContext,
    decision: ConductorDecision,
    rendered_messages: list[RenderedMessage],
    runtime_state_diff: dict[str, Any],
    model_usage: ModelUsage,
    trace: TraceRecord,
    shadow_control: ShadowModeControl,
) -> None:
    await memory_store.record_model_usage(
        request.conversation.conversation_id,
        {
            "run_id": run_id,
            "agent_key": request.agent_key,
            "shadow_mode": True,
            **model_usage.model_dump(mode="json"),
        },
    )
    await memory_store.record_event(
        RuntimeEvent(
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="context_update",
            agent=_current_agent_name(decision),
            content="spec011_shadow_turn_completed",
            metadata={
                "shadow_mode": True,
                "delivery_suppressed": True,
                "suppression_reason": shadow_control.reason,
                "trace_id": trace.trace_id,
                "decision_id": decision.decision_id,
                "template_ids": [item.template_id for item in decision.template_plan.items],
                "rendered_message_count": len(rendered_messages),
                "trace": trace.model_dump(mode="json"),
                "runtime_state_diff": dict(runtime_state_diff),
                "sales_inbox_projection": trace.sales_inbox_projection.model_dump(mode="json"),
            },
        )
    )


def _existing_diagnostic_ledger(state: RuntimeState | None) -> list[Any]:
    if state is None or not isinstance(state.diagnostic, dict):
        return []
    ledger = state.diagnostic.get("ledger")
    return list(ledger) if isinstance(ledger, list) else []


def _merge_fact_updates(
    existing: list[dict[str, Any]],
    updates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    merged = [dict(item) for item in existing]
    seen = {(item.get("key"), json.dumps(item.get("value"), sort_keys=True)) for item in merged}
    for item in updates:
        key = (item.get("key"), json.dumps(item.get("value"), sort_keys=True))
        if key in seen:
            continue
        merged.append(dict(item))
        seen.add(key)
    return merged


def _combine_usage(first: ModelUsage, second: ModelUsage) -> ModelUsage:
    return ModelUsage(
        model=first.model,
        input_tokens=first.input_tokens + second.input_tokens,
        output_tokens=first.output_tokens + second.output_tokens,
        cost_usd=round(first.cost_usd + second.cost_usd, 6),
    )


def _stable_turn_id(request: AgentRunRequest) -> str:
    digest = hashlib.sha256(
        json.dumps(
            {
                "channel": request.channel,
                "conversation_id": request.conversation.conversation_id,
                "idempotency_key": request.message.idempotency_key,
            },
            ensure_ascii=True,
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()
    return f"turn_{request.channel}_{digest[:16]}"


def _shadow_mode_control(request: AgentRunRequest) -> ShadowModeControl:
    raw = request.metadata.get("spec011_shadow_mode")
    if raw is True:
        return ShadowModeControl(enabled=True, reason="spec011_shadow_mode")
    if not isinstance(raw, dict) or raw.get("enabled") is not True:
        return ShadowModeControl()
    return ShadowModeControl(
        enabled=True,
        reason=_optional_string(raw.get("reason")) or "spec011_shadow_mode",
    )


def _current_agent_name(decision: ConductorDecision) -> str:
    return f"taliya_commercial_spec011_{decision.role}_agent"


def _message_requires_product_source(message: RenderedMessage) -> bool:
    return bool(message.template_id and message.template_id.startswith("product."))


def _source_refs(context: TurnContext) -> list[SourceRef]:
    refs: list[SourceRef] = []
    official_keys = [
        ref.key
        for ref in context.product_knowledge
        if ref.source == "official_product_knowledge" and not ref.missing
    ]
    version = _product_source_version(context)
    if official_keys:
        refs.append(
            SourceRef(
                type="product_knowledge",
                version=version,
                keys=official_keys,
            )
        )
    return refs


def _product_source_version(context: TurnContext) -> str | None:
    for ref in context.product_knowledge:
        if ref.source == "official_product_knowledge" and ref.version:
            return ref.version
    return None


def _diagnostic_status(decision: ConductorDecision) -> str:
    action = decision.diagnostic.action
    if action == "offer":
        return "offered"
    if action in {"start", "ask_next"}:
        return "in_progress"
    if action == "complete":
        return "completed"
    if action == "insufficient_evidence":
        return "insufficient_evidence"
    return "not_started"


def _diagnostic_ledger_status(decision: ConductorDecision) -> str:
    if decision.diagnostic.action == "complete":
        return "complete"
    if decision.diagnostic.action in {"start", "ask_next"}:
        return "in_progress"
    if decision.diagnostic.action == "insufficient_evidence":
        return "blocked"
    return "not_started"


def _fact_evidence(decision: ConductorDecision) -> list[str]:
    evidence: list[str] = []
    for fact in decision.facts:
        evidence.extend(fact.evidence)
    return evidence


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
