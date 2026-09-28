"""T012-031 (isolated core): the action-first turn runner and conversation loop.

Chains the v2 pipeline end to end, isolated from the public endpoint:

    state snapshot -> Turn Situation Builder -> starting agent (deterministic)
    -> Agents SDK run (board preamble + transcript + inbound)
    -> ConductorActionDecision -> Decision Compiler -> validators/renderer
    -> commit-after-validation state evolution

Paid calls stay behind `require_paid_approval`; an injected SDK `Model`
instance runs the same pipeline as a no-cost dry-run. Tracing stays
local-only. One repair operation with precise validator feedback.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from time import perf_counter
from typing import Any

from app.core.taliya_commercial.product_knowledge import (
    build_official_product_knowledge_refs,
)
from app.core.taliya_commercial.renderer import render_validated_template_plan
from app.core.taliya_commercial.schemas import (
    RenderPlan,
    RenderPlanItem,
    TemplateVariableValue,
    ValidatorResult,
)
from app.core.taliya_commercial_sdk.action_agents import (
    build_action_first_agents,
    starting_agent_name_for,
)
from app.core.taliya_commercial_sdk.action_safety import classify_safety_boundary
from app.core.taliya_commercial_sdk.action_trace import (
    build_action_turn_trace,
    build_safety_trace,
)
from app.core.taliya_commercial_sdk.action_validators import (
    ANSWERING_ACTIONS,
    ActionTurnValidation,
    build_action_sales_inbox_projection,
    validate_compiled_turn,
)
from app.core.taliya_commercial_sdk.conductor_decision import ConductorActionDecision
from app.core.taliya_commercial_sdk.decision_compiler import (
    CompiledTurn,
    compile_action_decision,
)
from app.core.taliya_commercial_sdk.isolation import (
    assert_public_cutover_disabled,
    require_paid_approval,
)
from app.core.taliya_commercial_sdk.paid_spike_harness import (
    DRY_RUN_MODEL_NAME,
    MODEL_PRICING_USD_PER_MILLION,
    SpikePreconditionError,
    estimate_cost_usd,
)
from app.core.taliya_commercial_sdk.turn_situation import (
    TurnSituation,
    build_turn_situation,
)
from app.settings import get_settings

try:
    from agents import RunConfig, Runner, set_tracing_disabled
except Exception:  # pragma: no cover - import fallback for static/no-sdk environments
    RunConfig = None
    Runner = None
    set_tracing_disabled = None

_REPAIR_INSTRUCTION = (
    "Your ConductorActionDecision failed deterministic validation. Fix ONLY "
    "what the errors below require and return a corrected, complete decision "
    "in the same schema. If an error says a direct question was not answered "
    "first, select the answering action. If a composition variable is "
    "missing or parrots the lead, write a practical reading grounded in "
    "their meaning, not a recap of their words. If the error is "
    "conductor_action_not_in_allowed_menu, "
    "choose one of the allowed actions shown in the error; in post_diagnostic "
    "mode, use answer_product_question_with_saved_context for product/how-it-"
    "works follow-up questions instead of generic product actions. If the "
    "error is post_diagnostic_waitlist_intent_requires_waitlist_action, choose "
    "offer_or_join_waitlist_if_eligible with waitlist_context_summary. If the "
    "error is price_question_missing_price_answer, "
    "price_question_missing_diagnostic_hook, or "
    "price_question_missing_diagnostic_offer, answer the price with an "
    "answering price/product action, include product_fact_keys_used=['prices'], "
    "keep direct_question set to the current price question, and do not "
    "clarify. If the error is demo_direct_question_flags_missing, keep "
    "send_demo, set direct_question to the current demo request, add a direct "
    "answer obligation with evidence, and keep demo_intent='requested' plus "
    "product_fact_keys_used=['demo_link']. If the error is "
    "price_plus_context_requires_context_hook, "
    "keep the price-answering action and add a plan_fit_context composition "
    "grounded in the lead's concrete pain/context so the runtime can use the "
    "contextual price hook. If the error is "
    "price_context_missing_specific_pain_anchor, rewrite plan_fit_context to "
    "mention a concrete anchor from the current lead message, such as their "
    "agenda, reposicao, WhatsApp, follow-up, or other stated pain. If the "
    "error is pain_context_missing_specific_anchor, keep "
    "offer_diagnostic_from_pain and rewrite pain_context_human to preserve a "
    "concrete channel, process, or object from the lead's message without "
    "copying their sentence. If the error is "
    "instagram_source_action_required or "
    "instagram_source_opening_template_missing, choose "
    "answer_source_opening and do not add a product fact key for a broad "
    "source opening. If the "
    "error is compile_completion_with_missing_keys:<key>, keep "
    "complete_diagnostic only when the current inbound or transcript answers "
    "that final key, and add the missing captured_slots entry with evidence; "
    "otherwise capture the pending answer and continue. If the "
    "error says join_waitlist is not in the "
    "allowed menu, and the lead is not already in an active waitlist details "
    "flow, choose offer_or_join_waitlist_if_eligible with a grounded "
    "waitlist_context_summary instead. If the error is "
    "compile_repeated_pending_question_without_capture, do not repeat the "
    "same diagnostic question: either capture the lead's answer for the "
    "pending key and continue, or choose clarify_ambiguous_diagnostic_answer "
    "with a concrete clarification_question.\nValidator errors:\n{errors}"
)


def resolve_official_facts(
    needed: Sequence[str],
    *,
    overrides: Mapping[str, Any] | None = None,
    product_fact_keys: Sequence[str] = (),
) -> dict[str, Any]:
    """Deterministic official-fact resolution for compiler-owned variables.

    Formats values straight from the official product knowledge source -
    formatting official content is compiler territory; no prose is invented.
    """

    facts: dict[str, Any] = dict(overrides or {})
    wanted = [name for name in needed if name not in facts]
    if not wanted:
        return facts
    refs = {ref.key: ref for ref in build_official_product_knowledge_refs(None) if not ref.missing}

    if "plan_price_summary" in wanted and "plans" in refs:
        plans = refs["plans"].value or []
        parts = [
            f"{plan.get('name')}: {plan.get('price_label')}"
            for plan in plans
            if isinstance(plan, Mapping) and plan.get("price_label")
        ]
        if parts:
            facts["plan_price_summary"] = {
                "kind": "long_text",
                "value": ". ".join(parts) + ".",
                "source": "official_product_knowledge",
                "evidence": ["product_knowledge.plans"],
                "max_length": 360,
            }
    if "recommended_plan_or_range" in wanted and "plans" in refs:
        plans = refs["plans"].value or []
        plan = next(
            (
                item
                for item in plans
                if isinstance(item, Mapping) and item.get("name") == "Essencial"
            ),
            None,
        )
        if isinstance(plan, Mapping) and plan.get("price_label"):
            facts["recommended_plan_or_range"] = {
                "kind": "short_text",
                "value": f"Essencial ({plan['price_label']})",
                "source": "official_product_knowledge",
                "evidence": ["product_knowledge.plans.essencial"],
            }
    if "indicated_agents" in wanted and "routine_areas" in refs:
        routine_areas = refs["routine_areas"].value or {}
        if isinstance(routine_areas, Mapping):
            facts["indicated_agents"] = [
                {
                    "agent_name": "Atendimento e vendas",
                    "agent_pain_resolved": str(
                        routine_areas.get(
                            "vendas_interessados",
                            "Interessados e follow-up ficam organizados.",
                        )
                    ),
                    "agent_practical_action": str(
                        routine_areas.get(
                            "gestao_prioridades",
                            "A equipe enxerga o que precisa resolver primeiro.",
                        )
                    ),
                }
            ]
    if "official_demo_link" in wanted and "links" in refs:
        links = refs["links"].value or {}
        demo_link = None
        if isinstance(links, Mapping):
            demo_link = links.get("demonstration") or links.get("demo") or links.get("demo_full")
        if demo_link:
            facts["official_demo_link"] = {
                "kind": "url",
                "value": str(demo_link),
                "source": "official_product_knowledge",
                "evidence": ["product_knowledge.links.demo"],
            }
    if "product_fact_summary" in wanted:
        summary_key = next(
            (
                key
                for key in product_fact_keys
                if key
                in {
                    "whatsapp_scope",
                    "availability_and_onboarding",
                    "comparison_spreadsheet",
                    "comparison_management_system",
                    "security_and_data",
                    "out_of_profile",
                    "how_it_works",
                    "routine_areas",
                    "integration_scope",
                }
                and key in refs
            ),
            "whatsapp_scope" if "whatsapp_scope" in refs else None,
        )
        raw_scope = refs[summary_key].value if summary_key else ""
        if isinstance(raw_scope, Mapping):
            scope = " ".join(f"{key}: {value}" for key, value in raw_scope.items() if value)
        else:
            scope = str(raw_scope or "")
        if summary_key and scope:
            facts["product_fact_summary"] = {
                "kind": "long_text",
                "value": scope[:320],
                "source": "official_product_knowledge",
                "evidence": [f"product_knowledge.{summary_key}"],
                "max_length": 320,
            }
    return facts


@dataclass
class ActionModelUsage:
    model_operations: int = 0
    input_tokens: int = 0
    cached_input_tokens: int = 0
    cache_write_input_tokens: int = 0
    output_tokens: int = 0
    reasoning_tokens: int = 0


@dataclass
class ActionTurnReport:
    user_text: str
    mode: str
    starting_agent: str | None
    llm_called: bool
    status: str
    selected_action: str | None = None
    template_ids: tuple[str, ...] = ()
    rendered_messages: tuple[str, ...] = ()
    issues: tuple[str, ...] = ()
    issue_details: tuple[str, ...] = ()
    repairs: int = 0
    model_operations: int = 0
    input_tokens: int = 0
    cached_input_tokens: int = 0
    cache_write_input_tokens: int = 0
    output_tokens: int = 0
    reasoning_tokens: int = 0
    latency_ms: float = 0.0
    cost_usd: float = 0.0
    next_state: str | None = None
    sales_inbox_projection: dict[str, Any] = field(default_factory=dict)
    trace: dict[str, Any] = field(default_factory=dict)


@dataclass
class ActionConversationReport:
    turns: list[ActionTurnReport] = field(default_factory=list)
    final_state: dict[str, Any] = field(default_factory=dict)
    transcript: list[dict[str, str]] = field(default_factory=list)
    total_model_operations: int = 0
    total_cost_usd: float = 0.0
    cost_cap_usd: float | None = None
    cost_cap_exceeded: bool = False

    @property
    def turns_passed(self) -> int:
        return sum(1 for turn in self.turns if turn.status == "delivered")


def _usage_of(run_result: Any) -> ActionModelUsage:
    usage = getattr(getattr(run_result, "context_wrapper", None), "usage", None)
    if usage is None:
        return ActionModelUsage()
    input_details = getattr(usage, "input_tokens_details", None)
    output_details = getattr(usage, "output_tokens_details", None)
    return ActionModelUsage(
        model_operations=int(getattr(usage, "requests", 0) or 0),
        input_tokens=int(getattr(usage, "input_tokens", 0) or 0),
        cached_input_tokens=int(getattr(input_details, "cached_tokens", 0) or 0),
        cache_write_input_tokens=int(getattr(input_details, "cache_write_tokens", 0) or 0),
        output_tokens=int(getattr(usage, "output_tokens", 0) or 0),
        reasoning_tokens=int(getattr(output_details, "reasoning_tokens", 0) or 0),
    )


def _add_usage(report: ActionTurnReport, usage: ActionModelUsage) -> None:
    report.model_operations += usage.model_operations
    report.input_tokens += usage.input_tokens
    report.cached_input_tokens += usage.cached_input_tokens
    report.cache_write_input_tokens += usage.cache_write_input_tokens
    report.output_tokens += usage.output_tokens
    report.reasoning_tokens += usage.reasoning_tokens


def _commit(
    state: dict[str, Any],
    compiled: CompiledTurn,
    decision: ConductorActionDecision,
) -> None:
    """Commit-after-validation state evolution (runtime rule)."""

    state["canonical_state"] = compiled.next_state
    if compiled.ledger_updates:
        diagnostic = state.setdefault("diagnostic", {"status": "in_progress"})
        ledger = diagnostic.setdefault("ledger", {})
        for update in compiled.ledger_updates:
            ledger[update["question_key"]] = {
                "status": update["status"],
                "answer_value": update.get("answer_value"),
            }
        diagnostic["status"] = (
            "delivered" if compiled.selected_action == "complete_diagnostic" else "in_progress"
        )
        if compiled.selected_action == "complete_diagnostic":
            final_fields = _diagnostic_final_fields(compiled)
            if final_fields:
                diagnostic["final_fields"] = final_fields
    for key, patch in compiled.state_patch.items():
        if key == "handoff":
            state["human_status"] = patch.get("status", "requested")
        else:
            state[key] = {**(state.get(key) or {}), **patch}
    if compiled.selected_action == "complete_diagnostic":
        state.setdefault("diagnostic", {})["status"] = "delivered"
    question = decision.direct_question
    if question and compiled.selected_action in ANSWERING_ACTIONS:
        answered = list(state.get("answered_obligations") or [])
        answered.append(question)
        state["answered_obligations"] = answered


def _diagnostic_final_fields(compiled: CompiledTurn) -> dict[str, Any]:
    final_fields: dict[str, Any] = {}
    plan = compiled.variables.get("recommended_plan_or_range")
    if isinstance(plan, dict) and plan.get("value"):
        final_fields["final_plan_or_range"] = plan["value"]
    if "diagnostic.deliver_demo_not_offered" in compiled.template_ids:
        final_fields["final_demo_line"] = (
            "Temos algumas demonstracoes que mostram o funcionamento na pratica. "
            "Quer que eu te mande?"
        )
    elif "diagnostic.deliver_demo_already_offered" in compiled.template_ids:
        final_fields["final_demo_line"] = "Chegou a olhar as demonstracoes? O que voce achou?"
    return final_fields


def _has_prior_conversation_context(
    transcript: list[dict[str, str]],
    situation: TurnSituation,
) -> bool:
    if transcript:
        return True
    snapshot = dict(situation.state_snapshot)
    return (
        situation.channel == "widget"
        and snapshot.get("client_has_prior_assistant_messages") is True
    )


async def run_action_turn(
    *,
    state: dict[str, Any],
    transcript: list[dict[str, str]],
    user_text: str,
    agents_by_name: Mapping[str, Any],
    model_name: str,
    official_facts_overrides: Mapping[str, Any] | None = None,
    channel: str = "whatsapp",
    message_type: str = "text",
    unsupported_media_kind: str | None = None,
) -> ActionTurnReport:
    safety = classify_safety_boundary(
        user_text=user_text,
        message_type=message_type,
        unsupported_media_kind=unsupported_media_kind,
    )
    if safety is not None:
        state.update(safety.state_patch)
        items = [
            RenderPlanItem(
                template_id=safety.template_id,
                channel="whatsapp",
                variables={
                    name: TemplateVariableValue.model_validate(payload)
                    for name, payload in safety.variables.items()
                },
            )
        ]
        rendered = render_validated_template_plan(
            RenderPlan(items=items, chunk_policy="whatsapp_max_3"),
            ValidatorResult(
                decision_id=f"safety_{safety.code}",
                status="passed",
                final_disposition="accepted",
            ),
            channel="whatsapp",
        )
        transcript.append({"role": "user", "content": user_text})
        transcript.extend({"role": "assistant", "content": message.text} for message in rendered)
        rendered_messages = tuple(message.text for message in rendered)
        return ActionTurnReport(
            user_text=user_text,
            mode="safety",
            starting_agent=None,
            llm_called=False,
            status="safety_blocked",
            template_ids=(safety.template_id,),
            rendered_messages=rendered_messages,
            issues=(safety.code,),
            next_state="safety_blocked",
            trace=build_safety_trace(
                user_text=user_text,
                message_type=message_type,
                safety_code=safety.code,
                template_id=safety.template_id,
                rendered_messages=rendered_messages,
            ),
        )

    situation = build_turn_situation(state_snapshot=state, channel=channel)
    starting_agent = starting_agent_name_for(situation)
    report = ActionTurnReport(
        user_text=user_text,
        mode=situation.mode,
        starting_agent=starting_agent,
        llm_called=starting_agent is not None,
        status="pending",
    )
    if starting_agent is None:
        report.status = "deferred" if situation.mode == "delivery_deferred" else "suppressed"
        return report

    run_config = RunConfig(tracing_disabled=True, workflow_name="spec012_action_first_turn")
    input_items = [{"role": "system", "content": situation.to_preamble()}]
    input_items.extend(transcript)
    input_items.append({"role": "user", "content": user_text})

    max_turns = 2 if starting_agent == "taliya_triage_agent" else 1
    run_started_at = perf_counter()
    run_result = await Runner.run(
        agents_by_name[starting_agent],
        input_items,
        max_turns=max_turns,
        run_config=run_config,
    )
    usage = _usage_of(run_result)
    _add_usage(report, usage)
    report.latency_ms = round((perf_counter() - run_started_at) * 1_000, 3)
    report.cost_usd = estimate_cost_usd(
        model_name,
        input_tokens=usage.input_tokens,
        cached_input_tokens=usage.cached_input_tokens,
        cache_write_input_tokens=usage.cache_write_input_tokens,
        output_tokens=usage.output_tokens,
    )

    decision = run_result.final_output
    if not isinstance(decision, ConductorActionDecision):
        report.status = "failed"
        report.issues = ("action_output_not_structured",)
        report.trace = build_action_turn_trace(
            user_text=user_text,
            situation=situation,
            starting_agent=starting_agent,
            run_result=run_result,
            decision=None,
            compiled=None,
            validation=None,
            rendered_messages=(),
            sales_inbox_projection=None,
            status=report.status,
            repairs=report.repairs,
            model_operations=report.model_operations,
            input_tokens=report.input_tokens,
            cached_input_tokens=report.cached_input_tokens,
            cache_write_input_tokens=report.cache_write_input_tokens,
            output_tokens=report.output_tokens,
            reasoning_tokens=report.reasoning_tokens,
            latency_ms=report.latency_ms,
            cost_usd=report.cost_usd,
        )
        return report

    compiled, validation = _compile_and_validate(
        decision, situation, user_text, transcript, official_facts_overrides
    )

    repair_validator_errors: tuple[Any, ...] = ()
    repair_run_result: Any | None = None
    if not validation.ok:
        # One repair operation with precise feedback (design-lock budget).
        repair_validator_errors = tuple(validation.validator_result.errors)
        error_lines = "\n".join(
            f"- {issue.code}: {issue.message}" for issue in validation.validator_result.errors
        )
        repair_input = list(run_result.to_input_list()) + [
            {"role": "user", "content": _REPAIR_INSTRUCTION.format(errors=error_lines)}
        ]
        repair_result = await Runner.run(
            run_result.last_agent,
            repair_input,
            max_turns=1,
            run_config=run_config,
        )
        repair_run_result = repair_result
        repair_usage = _usage_of(repair_result)
        _add_usage(report, repair_usage)
        report.latency_ms = round((perf_counter() - run_started_at) * 1_000, 3)
        report.cost_usd += estimate_cost_usd(
            model_name,
            input_tokens=repair_usage.input_tokens,
            cached_input_tokens=repair_usage.cached_input_tokens,
            cache_write_input_tokens=repair_usage.cache_write_input_tokens,
            output_tokens=repair_usage.output_tokens,
        )
        report.repairs = 1
        repaired = repair_result.final_output
        if isinstance(repaired, ConductorActionDecision):
            # Repair preserves first-pass extractions: the lead's answer was
            # already captured; a regenerated decision must not lose it.
            if decision.captured_slots and not repaired.captured_slots:
                repaired = repaired.model_copy(update={"captured_slots": decision.captured_slots})
            if decision.composition_variables:
                merged = {variable.name: variable for variable in decision.composition_variables}
                merged.update(
                    {variable.name: variable for variable in repaired.composition_variables}
                )
                repaired = repaired.model_copy(
                    update={"composition_variables": list(merged.values())}
                )
            compiled_retry, validation_retry = _compile_and_validate(
                repaired, situation, user_text, transcript, official_facts_overrides
            )
            if validation_retry.ok:
                decision, compiled, validation = repaired, compiled_retry, validation_retry

    report.selected_action = compiled.selected_action
    report.template_ids = compiled.template_ids
    report.issues = tuple(issue.code for issue in validation.validator_result.errors)
    report.issue_details = tuple(
        f"{issue.code}: {issue.message[:200]}" for issue in validation.validator_result.errors
    )
    if validation.ok:
        report.status = "delivered"
        report.rendered_messages = tuple(message.text for message in validation.rendered_preview)
        projection = build_action_sales_inbox_projection(
            compiled=compiled,
            decision=decision,
            situation=situation,
            current_user_text=user_text,
            has_history=_has_prior_conversation_context(transcript, situation),
            validator_result=validation.validator_result,
        )
        report.sales_inbox_projection = projection.model_dump(mode="json")
        report.next_state = compiled.next_state
        _commit(state, compiled, decision)
        transcript.append({"role": "user", "content": user_text})
        transcript.extend(
            {"role": "assistant", "content": text} for text in report.rendered_messages
        )
    else:
        report.status = "failed"
    report.trace = build_action_turn_trace(
        user_text=user_text,
        situation=situation,
        starting_agent=starting_agent,
        run_result=run_result,
        decision=decision,
        compiled=compiled,
        validation=validation,
        rendered_messages=report.rendered_messages,
        sales_inbox_projection=report.sales_inbox_projection or None,
        status=report.status,
        repairs=report.repairs,
        model_operations=report.model_operations,
        input_tokens=report.input_tokens,
        cached_input_tokens=report.cached_input_tokens,
        cache_write_input_tokens=report.cache_write_input_tokens,
        output_tokens=report.output_tokens,
        reasoning_tokens=report.reasoning_tokens,
        latency_ms=report.latency_ms,
        cost_usd=report.cost_usd,
        repair_validator_errors=repair_validator_errors,
        repair_run_result=repair_run_result,
    )
    return report


def _compile_and_validate(
    decision: ConductorActionDecision,
    situation: TurnSituation,
    user_text: str,
    transcript: list[dict[str, str]],
    official_facts_overrides: Mapping[str, Any] | None,
) -> tuple[CompiledTurn, ActionTurnValidation]:
    needed = ["plan_price_summary", "official_demo_link", "product_fact_summary"]
    if decision.selected_action == "complete_diagnostic":
        needed.extend(("indicated_agents", "recommended_plan_or_range"))
    facts = resolve_official_facts(
        needed,
        overrides=official_facts_overrides,
        product_fact_keys=decision.product_fact_keys_used,
    )
    compiled = compile_action_decision(decision, situation, official_facts=facts)
    validation = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text=user_text,
        has_history=_has_prior_conversation_context(transcript, situation),
    )
    return compiled, validation


async def run_action_conversation(
    user_messages: Sequence[str],
    *,
    model: Any | None = None,
    paid_openai_approved: bool = False,
    initial_state: Mapping[str, Any] | None = None,
    official_facts_overrides: Mapping[str, Any] | None = None,
    max_total_cost_usd: float | None = 0.30,
) -> ActionConversationReport:
    """Run a multi-turn conversation through the action-first pipeline."""

    assert_public_cutover_disabled()
    if Runner is None or RunConfig is None:
        raise SpikePreconditionError("openai-agents SDK is required")
    injected = model is not None and not isinstance(model, str)
    if injected:
        model_name = getattr(model, "spike_model_name", DRY_RUN_MODEL_NAME)
        agent_model: Any = model
    else:
        require_paid_approval(approved=paid_openai_approved)
        model_name = model or get_settings().model
        if model_name not in MODEL_PRICING_USD_PER_MILLION:
            raise SpikePreconditionError(f"Model '{model_name}' has no recorded pricing.")
        agent_model = model_name
    set_tracing_disabled(True)

    agents_by_name = build_action_first_agents(model=agent_model)
    state: dict[str, Any] = dict(initial_state or {})
    channel = str(state.get("channel") or "whatsapp")
    transcript: list[dict[str, str]] = []
    conversation = ActionConversationReport(cost_cap_usd=max_total_cost_usd)

    for user_text in user_messages:
        if max_total_cost_usd is not None and conversation.total_cost_usd >= max_total_cost_usd:
            conversation.cost_cap_exceeded = True
            conversation.turns.append(
                ActionTurnReport(
                    user_text=user_text,
                    mode="cost_cap",
                    starting_agent=None,
                    llm_called=False,
                    status="deferred",
                    issues=("cost_budget_exceeded",),
                    next_state="cost_cap_deferred",
                )
            )
            break
        turn = await run_action_turn(
            state=state,
            transcript=transcript,
            user_text=user_text,
            agents_by_name=agents_by_name,
            model_name=model_name,
            official_facts_overrides=official_facts_overrides,
            channel=channel,
        )
        conversation.turns.append(turn)
        conversation.total_model_operations += turn.model_operations
        conversation.total_cost_usd += turn.cost_usd
        if turn.status == "failed":
            break

    conversation.final_state = state
    conversation.transcript = list(transcript)
    return conversation
