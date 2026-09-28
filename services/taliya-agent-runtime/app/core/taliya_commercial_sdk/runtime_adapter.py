"""T012-031 runtime adapter for the action-first SDK path.

This module is the narrow bridge between the public FastAPI runtime contract
and the isolated action-first runner. It does not authorize paid calls or
public cutover by itself; `app.main` owns the feature flag and idempotency
boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from app.core.taliya_commercial_sdk.action_turn_runner import run_action_conversation
from app.runtime.events import RuntimeEvent
from app.runtime.schemas import (
    AgentMessage,
    AgentOutput,
    AgentRunRequest,
    AgentRunResponse,
    DeliveryControl,
    HandoffOutput,
    RuntimeDecision,
    RuntimeInputSnapshot,
    SourceRef,
    ToolResult,
    Usage,
)
from app.shared.memory.postgres import InMemoryMemoryStore, RuntimeState
from app.shared.product_knowledge.source import get_product_knowledge_source

ACTION_FIRST_AGENT_KEY = "taliya_commercial"
ACTION_FIRST_BLOCKED_CODE = "spec012_action_first_paid_call_blocked"
ACTION_FIRST_MOCK_MODEL_REQUIRED_CODE = "spec012_action_first_mock_model_required"


@dataclass(frozen=True)
class ActionFirstShadowControl:
    enabled: bool = False
    reason: str | None = None


class ActionFirstRuntimeBlocked(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def _state_snapshot(
    payload: AgentRunRequest,
    previous_state: RuntimeState | None,
) -> dict[str, Any]:
    has_prior_assistant = _client_has_prior_assistant_messages(payload)
    if previous_state is None:
        snapshot: dict[str, Any] = {
            "conversation_id": payload.conversation.conversation_id,
            "lead_id": payload.conversation.lead_id,
            "source": payload.conversation.source,
            "channel": payload.channel,
        }
        if has_prior_assistant:
            snapshot["client_has_prior_assistant_messages"] = True
        return snapshot
    snapshot = previous_state.model_dump(mode="json")
    snapshot["conversation_id"] = payload.conversation.conversation_id
    snapshot["lead_id"] = payload.conversation.lead_id
    snapshot["source"] = payload.conversation.source
    snapshot["channel"] = payload.channel
    if has_prior_assistant:
        snapshot["client_has_prior_assistant_messages"] = True
    if previous_state.last_decision:
        next_state = previous_state.last_decision.get("next_state")
        if isinstance(next_state, str) and next_state:
            snapshot["canonical_state"] = next_state
    return snapshot


def _client_has_prior_assistant_messages(payload: AgentRunRequest) -> bool:
    if payload.metadata.get("client_has_prior_assistant_messages") is True:
        return True
    recent_messages = payload.metadata.get("recent_client_messages")
    if not isinstance(recent_messages, list):
        return False
    return any(
        isinstance(message, dict) and message.get("role") == "assistant"
        for message in recent_messages
    )


def _runtime_decision_from_trace(trace: dict[str, Any]) -> RuntimeDecision:
    decision = trace.get("compiler") or {}
    if not isinstance(decision, dict):
        decision = {}
    return RuntimeDecision(
        previous_state=str(decision.get("previous_state") or "new_lead"),
        current_state=str(decision.get("current_state") or "new_lead"),
        next_state=str(decision.get("next_state") or "new_lead"),
        route=str(decision.get("route") or "entry"),  # type: ignore[arg-type]
        detected_intents=list(decision.get("intents") or []),
        direct_question_present=bool(decision.get("direct_question_present") or False),
        direct_question_answered_first=True,
        template_ids=list(decision.get("template_ids") or []),
        render_plan=list(decision.get("render_plan") or []),
    )


def _trace_section_as_list(trace: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = trace.get(key)
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        return [value]
    return []


def _shadow_mode_control(request: AgentRunRequest) -> ActionFirstShadowControl:
    raw = request.metadata.get("spec012_shadow_mode")
    if raw is True:
        return ActionFirstShadowControl(enabled=True, reason="spec012_shadow_mode")
    if isinstance(raw, dict) and raw.get("enabled") is True:
        reason = raw.get("reason")
        return ActionFirstShadowControl(
            enabled=True,
            reason=str(reason) if reason else "spec012_shadow_mode",
        )
    return ActionFirstShadowControl()


def _runtime_trace_summary(trace: dict[str, Any], *, trace_id: str) -> dict[str, Any]:
    """Build a local event trace summary without raw inbound/rendered text."""

    return {
        "schema": "012.runtime_action_trace_summary.v1",
        "trace_id": trace_id,
        "trace_complete": bool(trace.get("trace_complete")),
        "sdk_start": trace.get("sdk_start") or {},
        "sdk_run_items": trace.get("sdk_run_items") or [],
        "context_snapshot": trace.get("context_snapshot") or {},
        "turn_situation": trace.get("turn_situation") or {},
        "action_decision": trace.get("action_decision") or {},
        "compiler": trace.get("compiler") or {},
        "validators": trace.get("validators") or {},
        "repair_or_escalation": trace.get("repair_or_escalation") or {},
        "render_plan": trace.get("render_plan") or {},
        "state_diff": trace.get("state_diff") or {},
        "sales_inbox_projection": trace.get("sales_inbox_projection") or {},
        "delivery": trace.get("delivery") or {},
        "usage_cost": trace.get("usage_cost") or {},
    }


async def _cost_capped_response(
    payload: AgentRunRequest,
    *,
    memory_store: InMemoryMemoryStore,
    previous_state: RuntimeState,
    model: str,
    cost_cap_usd: float,
) -> AgentRunResponse:
    run_id = f"run_{uuid4().hex}"
    trace_id = f"trace_{uuid4().hex}"
    current_agent = (
        previous_state.current_agent_name or "taliya_commercial_action_first_agent"
    )
    output = AgentOutput(
        decision=RuntimeDecision(
            previous_state=previous_state.last_decision.get("next_state", "new_lead")
            if previous_state.last_decision
            else "new_lead",
            current_state="cost_cap_reached",
            next_state="cost_cap_deferred",
            route="safe_fallback",
        ),
        messages=[],
        usage=Usage(model=model, input_tokens=0, output_tokens=0, cost_usd=0),
        confidence="high",
        handoff=HandoffOutput(
            status="active",
            reason="cost_cap_reached",
        ),
        safety_flags=["cost_cap_reached", "human_follow_up_required"],
        runtime_state=previous_state.model_dump(mode="json"),
        delivery_events=[
            {
                "type": "cost_cap_suppressed",
                "message_count": 0,
                "cost_cap_usd": cost_cap_usd,
                "prior_cost_usd": previous_state.cost_usd,
            }
        ],
        trace_complete=True,
    )
    await memory_store.record_guardrail_event(
        payload.conversation.conversation_id,
        {
            "run_id": run_id,
            "agent_key": payload.agent_key,
            "name": "spec012_action_first_cost_cap",
            "phase": "turn_gate",
            "status": "blocked",
            "reason": "cost_cap_reached",
            "blocked": True,
            "cost_cap_usd": cost_cap_usd,
            "prior_cost_usd": previous_state.cost_usd,
        },
    )
    await memory_store.record_event(
        RuntimeEvent(
            run_id=run_id,
            conversation_id=payload.conversation.conversation_id,
            agent_key=payload.agent_key,
            type="guardrail",
            agent=current_agent,
            metadata={
                "spec012_action_first": True,
                "status": "cost_capped",
                "reason": "cost_cap_reached",
                "cost_cap_usd": cost_cap_usd,
                "prior_cost_usd": previous_state.cost_usd,
            },
        )
    )
    return AgentRunResponse(
        run_id=run_id,
        conversation_id=payload.conversation.conversation_id,
        lead_id=payload.conversation.lead_id,
        agent_key=payload.agent_key,
        current_agent=current_agent,
        status="cost_capped",
        output=output,
        trace_id=trace_id,
    )


def _runtime_state_from_report(
    payload: AgentRunRequest,
    previous_state: RuntimeState | None,
    *,
    current_agent: str,
    final_state: dict[str, Any],
    decision: RuntimeDecision,
    cost_usd: float,
) -> RuntimeState:
    input_items = list(previous_state.input_items if previous_state else [])
    input_items.append(
        {
            "role": "user",
            "content": payload.message.text or "",
            "id": payload.message.idempotency_key,
        }
    )
    answered_direct_questions = list(
        final_state.get("answered_direct_questions")
        or final_state.get("answered_obligations")
        or (previous_state.answered_direct_questions if previous_state else [])
    )
    return RuntimeState(
        conversation_id=payload.conversation.conversation_id,
        agent_key=payload.agent_key,
        current_agent_name=current_agent,
        lead_id=payload.conversation.lead_id,
        channel=payload.channel,
        channel_conversation_id=payload.conversation.channel_conversation_id,
        source=payload.conversation.source,
        entry_intent=payload.conversation.entry_intent,
        input_items=input_items,
        summary=previous_state.summary if previous_state else None,
        lead_facts=final_state.get("lead_facts")
        or (previous_state.lead_facts if previous_state else []),
        diagnostic=final_state.get("diagnostic")
        or (previous_state.diagnostic if previous_state else None),
        demo=final_state.get("demo") or (previous_state.demo if previous_state else None),
        waitlist=final_state.get("waitlist")
        or (previous_state.waitlist if previous_state else None),
        human_status=str(
            final_state.get("human_status")
            or (previous_state.human_status if previous_state else "none")
        ),
        human_reason=previous_state.human_reason if previous_state else None,
        last_decision=decision.model_dump(mode="json"),
        last_route=decision.route,
        last_opening_type=decision.opening_type,
        asked_questions=final_state.get("asked_questions")
        or (previous_state.asked_questions if previous_state else []),
        answered_direct_questions=answered_direct_questions,
        profile_name_status=final_state.get("profile_name_status")
        or (previous_state.profile_name_status if previous_state else None),
        product_source_version=final_state.get("product_source_version")
        or (previous_state.product_source_version if previous_state else None),
        cost_usd=(previous_state.cost_usd if previous_state else 0) + cost_usd,
    )


async def run_action_first_agent_turn(
    payload: AgentRunRequest,
    *,
    memory_store: InMemoryMemoryStore,
    provider: str,
    model: str,
    cost_cap_usd: float = 0.15,
    sdk_model: Any | None = None,
) -> AgentRunResponse:
    """Run one public-runtime turn through the action-first SDK path.

    Mock mode requires an injected no-cost SDK model. A real provider uses the
    configured model through the action-first runner and remains guarded by the
    public feature/production routing, cost cap, validation, and rollback
    boundaries.
    """

    previous_state = await memory_store.load_state(
        payload.conversation.conversation_id,
        payload.agent_key,
    )
    shadow_control = _shadow_mode_control(payload)
    if previous_state is not None and previous_state.cost_usd >= cost_cap_usd:
        return await _cost_capped_response(
            payload,
            memory_store=memory_store,
            previous_state=previous_state,
            model=model,
            cost_cap_usd=cost_cap_usd,
        )

    if provider == "mock" and sdk_model is None:
        raise ActionFirstRuntimeBlocked(
            ACTION_FIRST_MOCK_MODEL_REQUIRED_CODE,
            "Spec 012 action-first runtime path requires an injected no-cost SDK "
            "model in mock mode.",
        )

    report = await run_action_conversation(
        [payload.message.text or ""],
        model=sdk_model if provider == "mock" else model,
        paid_openai_approved=provider != "mock",
        initial_state=_state_snapshot(payload, previous_state),
        max_total_cost_usd=cost_cap_usd,
    )
    turn = report.turns[-1]
    run_id = f"run_{uuid4().hex}"
    trace_id = f"trace_{uuid4().hex}"
    decision = _runtime_decision_from_trace(turn.trace)
    current_agent = turn.starting_agent or "taliya_commercial_action_first_agent"
    messages = [
        AgentMessage(text=text, channel_hint=payload.channel)
        for text in turn.rendered_messages
    ]
    response_messages = [] if shadow_control.enabled else messages
    product_source = get_product_knowledge_source()
    source_keys = _structured_product_source_keys(turn.trace)
    output = AgentOutput(
        decision=decision,
        messages=response_messages,
        sources=[
            SourceRef(
                type="product_knowledge",
                version=product_source.version,
                keys=source_keys,
            )
        ]
        if source_keys
        else [],
        usage=Usage(
            model=model,
            model_operations=turn.model_operations,
            input_tokens=turn.input_tokens,
            cached_input_tokens=turn.cached_input_tokens,
            cache_write_input_tokens=turn.cache_write_input_tokens,
            output_tokens=turn.output_tokens,
            reasoning_tokens=turn.reasoning_tokens,
            repairs=turn.repairs,
            latency_ms=turn.latency_ms,
            cost_usd=turn.cost_usd,
        ),
        confidence="high" if turn.status == "delivered" else "medium",
        safety_flags=["shadow_mode", "delivery_suppressed"]
        if shadow_control.enabled
        else [],
        tool_results=[
            ToolResult(
                name="shadow_mode",
                status="ok",
                summary=(
                    f"delivery_suppressed:{shadow_control.reason or 'spec012_shadow_mode'}"
                ),
            )
        ]
        if shadow_control.enabled
        else [],
        context_snapshot=turn.trace.get("context_snapshot") or {},
        turn_situation=turn.trace.get("turn_situation") or {},
        action_decision=turn.trace.get("action_decision") or {},
        validator_results=_trace_section_as_list(turn.trace, "validators"),
        repair_attempts=_trace_section_as_list(turn.trace, "repair_or_escalation"),
        runtime_state=report.final_state,
        sales_inbox_projection=turn.sales_inbox_projection,
        delivery_events=[
            {
                "type": "delivery_suppressed"
                if shadow_control.enabled
                else "local_preview",
                "message_count": len(turn.rendered_messages),
                "shadow_mode": shadow_control.enabled,
                "suppression_reason": shadow_control.reason
                if shadow_control.enabled
                else None,
                "trace_delivery": turn.trace.get("delivery") or {},
            }
        ],
        trace_complete=bool(turn.trace),
    )
    if not shadow_control.enabled:
        state = _runtime_state_from_report(
            payload,
            previous_state,
            current_agent=current_agent,
            final_state=report.final_state,
            decision=decision,
            cost_usd=turn.cost_usd,
        )
        try:
            await memory_store.save_state(state)
        except Exception as exc:  # pragma: no cover - production persistence boundary
            output.safety_flags.append("persistence_degraded")
            output.tool_results.append(
                ToolResult(
                    name="save_runtime_state",
                    status="error",
                    summary=f"state persistence failed: {type(exc).__name__}",
                )
            )
        output.runtime_state = report.final_state
    else:
        output.runtime_state = previous_state.model_dump(mode="json") if previous_state else {}
    try:
        await memory_store.record_model_usage(
            payload.conversation.conversation_id,
            {
                "run_id": run_id,
                "agent_key": payload.agent_key,
                "model": model,
                "model_operations": turn.model_operations,
                "input_tokens": turn.input_tokens,
                "cached_input_tokens": turn.cached_input_tokens,
                "cache_write_input_tokens": turn.cache_write_input_tokens,
                "output_tokens": turn.output_tokens,
                "reasoning_tokens": turn.reasoning_tokens,
                "repairs": turn.repairs,
                "latency_ms": turn.latency_ms,
                "cost_usd": turn.cost_usd,
                "shadow_mode": shadow_control.enabled,
                "provider": provider,
                "status": "succeeded" if turn.status == "delivered" else "failed",
            },
        )
    except Exception as exc:  # pragma: no cover - production observability boundary
        output.safety_flags.append("observability_degraded")
        output.tool_results.append(
            ToolResult(
                name="record_model_usage",
                status="error",
                summary=f"model usage persistence failed: {type(exc).__name__}",
            )
        )
    try:
        await memory_store.record_event(
            RuntimeEvent(
                run_id=run_id,
                conversation_id=payload.conversation.conversation_id,
                agent_key=payload.agent_key,
                type="context_update" if shadow_control.enabled else "message",
                agent=current_agent,
                content="spec012_shadow_turn_completed"
                if shadow_control.enabled
                else (messages[0].text if messages else ""),
                metadata={
                    "spec012_action_first": True,
                    "status": turn.status,
                    "shadow_mode": shadow_control.enabled,
                    "delivery_suppressed": shadow_control.enabled,
                    "suppression_reason": shadow_control.reason
                    if shadow_control.enabled
                    else None,
                    "rendered_message_count": len(turn.rendered_messages),
                    "trace_summary": _runtime_trace_summary(turn.trace, trace_id=trace_id),
                    "sales_inbox_projection": turn.sales_inbox_projection,
                },
            )
        )
    except Exception as exc:  # pragma: no cover - production observability boundary
        output.safety_flags.append("observability_degraded")
        output.tool_results.append(
            ToolResult(
                name="record_runtime_event",
                status="error",
                summary=f"runtime event persistence failed: {type(exc).__name__}",
            )
        )
    status = "succeeded" if turn.status == "delivered" else "failed"
    return AgentRunResponse(
        run_id=run_id,
        conversation_id=payload.conversation.conversation_id,
        lead_id=payload.conversation.lead_id,
        agent_key=payload.agent_key,
        current_agent=current_agent,
        status=status,
        output=output,
        trace_id=trace_id,
        input_snapshot=RuntimeInputSnapshot(
            channel=payload.channel,
            conversation_id=payload.conversation.conversation_id,
            lead_id=payload.conversation.lead_id,
            channel_conversation_id=payload.conversation.channel_conversation_id,
            source=payload.conversation.source,
            entry_intent=payload.conversation.entry_intent,
            message_id=payload.message.idempotency_key,
            channel_message_id=payload.message.channel_message_id,
            message_type=payload.message.type,
            message_timestamp=payload.message.timestamp,
            page_path=str(payload.metadata.get("page_path") or "") or None,
            source_section=str(payload.metadata.get("source_section") or "") or None,
            campaign_stage=str(payload.metadata.get("campaign_stage") or "") or None,
        ),
        delivery_control=DeliveryControl(
            shadow_mode=shadow_control.enabled,
            delivery_suppressed=shadow_control.enabled,
            suppression_reason=shadow_control.reason if shadow_control.enabled else None,
            rendered_message_count=len(turn.rendered_messages),
            trace_contains_rendered_messages=True,
        ),
    )


def _structured_product_source_keys(trace: dict[str, Any]) -> list[str]:
    action_decision = trace.get("action_decision") or {}
    if not isinstance(action_decision, dict):
        return []
    raw_keys = action_decision.get("product_fact_keys_used") or []
    if not isinstance(raw_keys, list):
        return []
    return sorted({str(key).strip() for key in raw_keys if str(key).strip()})
