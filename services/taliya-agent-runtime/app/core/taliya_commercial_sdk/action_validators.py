"""T012-032 (core slice): validators for compiled action-first turns.

Action-level direct-question adequacy (deterministic: a direct question in
the current inbound requires an answering action, not a steering one),
anti-parrot and banned-voice rules from the 010 contracts, and rendering of
the compiled plan through the existing approved renderer.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.core.taliya_commercial.product_knowledge import (
    build_official_product_knowledge_refs,
)
from app.core.taliya_commercial.renderer import RenderError, render_validated_template_plan
from app.core.taliya_commercial.runtime_state import build_runtime_state_diff
from app.core.taliya_commercial.sales_inbox_projection import (
    build_sales_inbox_projection,
)
from app.core.taliya_commercial.schemas import (
    ConductorDecision as LegacyConductorDecision,
)
from app.core.taliya_commercial.schemas import (
    DeliveryEvent,
    InboundTurn,
    LanguagePolicyDecision,
    RenderedMessage,
    RenderPlan,
    RenderPlanItem,
    SalesInboxProjection,
    TemplateVariableValue,
    TurnContext,
    ValidationIssue,
    ValidatorResult,
)
from app.core.taliya_commercial.schemas import (
    NumericInterpretation as LegacyNumericInterpretation,
)
from app.core.taliya_commercial.validators import validate_conductor_result
from app.core.taliya_commercial_sdk.conductor_decision import ConductorActionDecision
from app.core.taliya_commercial_sdk.decision_compiler import CompiledTurn
from app.core.taliya_commercial_sdk.turn_situation import TurnSituation
from app.core.taliya_commercial_sdk.validators_adapter import (
    DIAGNOSTIC_ASK_TEMPLATE_BY_KEY,
    _normalized_tokens,
    _question_is_from_current_inbound,
)

# Actions that legitimately respond to a direct question this turn. Anything
# else is steering and fails "direct question answered first".
ANSWERING_ACTIONS = frozenset(
    {
        "answer_general_interest",
        "answer_source_opening",
        "answer_direct_product_question",
        "answer_direct_question_then_continue_diagnostic",
        "answer_product_question_with_saved_context",
        "answer_question_then_continue_waitlist",
        "answer_price",
        "answer_plan_fit_with_diagnostic_offer",
        "answer_how_it_works",
        "answer_whatsapp_scope",
        "answer_integration_scope_safely",
        "answer_comparison_current_tool",
        "answer_security_and_data",
        "answer_availability_and_onboarding",
        "answer_out_of_profile",
        "answer_price_objection",
        "answer_price_objection_with_context",
        "send_demo",
        "respect_diagnostic_refusal",
        "handoff_requested",
        "pause_for_human",
    }
)

CLARIFYING_ACTIONS = frozenset(
    {
        "clarify_ambiguous_opening",
        "clarify_ambiguous_diagnostic_answer",
        "clarify_ambiguous_followup",
        "clarify_product_question",
    }
)

# Voice rules from behavior-contract.md (Voice And Style) and the rejected
# final-diagnostic formats. Checked on rendered text, lowercase.
BANNED_RENDERED_PHRASES: tuple[str, ...] = (
    "que bom te ver por aqui",
    "incrivel",
    "maravilha",
    "amei",
    "para eu te ajudar corretamente",
    "qual seu nome?",
    "com quem eu falo?",
    "gargalo principal",
    "para plano, eu compararia",
    "isso faz sentido para o momento do seu studio?",
)

CUSTOMER_VISIBLE_INTERNAL_MARKERS: tuple[str, ...] = (
    "nao prometa",
    "nao diga",
    "não prometa",
    "não diga",
    "chat comercial",
    "product_knowledge",
    "source_label",
    "utm_source",
    "runtime_state",
    "diagnostic_ledger",
    "guardrail",
    "validator",
    "template_id",
    "resumo interno",
    "a pessoa achou",
    "o lead",
    "a lead",
    "lead came",
    "never promise",
    "must ",
    "should use",
    "undefined",
    "null",
    "none",
)
CUSTOMER_VISIBLE_ENCODING_MARKERS: tuple[str, ...] = ("Ã", "Â", "â€")
CUSTOMER_VISIBLE_BAD_PUNCTUATION: tuple[str, ...] = (
    "..",
    " ,",
    " .",
    ": .",
)

_GREETING_MARKERS = ("oi, tudo bem", "ola, tudo bem", "bom dia", "boa tarde")
_CONTEXT_ANCHOR_STOPWORDS = frozenset(
    {
        "tenho",
        "queria",
        "saber",
        "preco",
        "preço",
        "quanto",
        "custa",
        "valor",
        "plano",
        "planos",
        "diagnostico",
        "diagnóstico",
        "perco",
        "muitos",
        "interessados",
        "porque",
        "equipe",
        "demora",
        "responder",
    }
)
_THIN_CONTEXT_EVIDENCE_PHRASES = (
    "pelo que voce contou",
    "pelo que você contou",
)

_CONTEXTUAL_PRICE_INTENT_MARKERS = (
    "pain",
    "dor",
    "context",
    "rotina",
    "agenda",
    "reposi",
    "whatsapp",
    "follow",
    "atendimento",
    "vendas",
    "operational",
)

# Approved template bodies prefix some replies with a greeting chunk (live
# Spec 011 copy, untouched). Mid-conversation, that chunk violates the
# repeated-greeting voice rule, so the action-first delivery DROPS pure
# greeting chunks when history exists - deterministic channel formatting.
_PURE_GREETING_CHUNKS = frozenset(
    {"oi, tudo bem?", "ola, tudo bem?", "oi, tudo bem", "ola, tudo bem"}
)


@dataclass(frozen=True)
class ActionTurnValidation:
    validator_result: ValidatorResult
    rendered_preview: list[RenderedMessage] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.validator_result.status == "passed"


def _issue(code: str, message: str, path: str | None = None) -> ValidationIssue:
    return ValidationIssue(code=code, severity="P0", message=message, path=path)


def _route_for(compiled: CompiledTurn, situation: TurnSituation) -> str:
    if compiled.selected_action in {"handoff_requested", "pause_for_human"}:
        return "handoff"
    if compiled.selected_action.startswith("answer_question_then_continue_waitlist"):
        return "waitlist"
    if compiled.selected_action in {
        "offer_waitlist",
        "offer_or_join_waitlist_if_eligible",
        "collect_waitlist_missing_detail",
        "join_waitlist",
        "decline_waitlist",
        "pause_waitlist_decision",
    }:
        return "waitlist"
    if compiled.selected_action in {
        "offer_diagnostic_from_pain",
        "start_requested_diagnostic",
        "capture_pending_diagnostic_answer",
        "answer_direct_question_then_continue_diagnostic",
        "ask_next_diagnostic_question",
        "complete_diagnostic",
        "clarify_ambiguous_diagnostic_answer",
    }:
        return "diagnostic"
    if any(template_id.startswith("opening.") for template_id in compiled.template_ids):
        return "entry"
    if situation.mode == "safety":
        return "safe_fallback"
    return "product"


def _legacy_numeric_interpretations(
    decision: ConductorActionDecision,
) -> list[LegacyNumericInterpretation]:
    values: list[LegacyNumericInterpretation] = []
    for item in decision.numeric_interpretations:
        raw_value = item.value_text
        kind = item.kind
        parsed: int | float | str = raw_value
        numeric = _numeric_value_or_none(raw_value)
        if numeric is not None:
            parsed = numeric
        elif kind == "plan_price":
            kind = "unknown_number"
        values.append(
            LegacyNumericInterpretation(
                raw_text=item.raw_text,
                kind=kind,
                value=parsed,
                currency="BRL" if kind == "plan_price" else None,
                evidence=list(item.evidence),
            )
        )
    return values


def _numeric_value_or_none(raw_value: str) -> int | float | None:
    normalized = (
        raw_value.strip().removeprefix("R$").replace(" ", "").replace(".", "").replace(",", ".")
    )
    if not normalized:
        return None
    try:
        parsed = float(normalized)
    except ValueError:
        return None
    if parsed.is_integer():
        return int(parsed)
    return parsed


def _legacy_waitlist(
    decision: ConductorActionDecision,
    compiled: CompiledTurn,
    situation: TurnSituation,
) -> dict:
    waitlist_status = (compiled.state_patch.get("waitlist") or {}).get("status")
    snapshot_status = (
        (compiled.sales_inbox_projection.get("waitlist_status") or "none")
        if compiled.sales_inbox_projection
        else "none"
    )
    status = waitlist_status or snapshot_status or "none"
    if status == "pending_data":
        status = "pending_details"
    snapshot_waitlist = dict(situation.state_snapshot).get("waitlist") or {}
    state_snapshot_status = str(snapshot_waitlist.get("status") or "none")
    missing_details = (
        []
        if compiled.selected_action == "join_waitlist"
        else list(snapshot_waitlist.get("missing_details") or [])
    )
    eligibility = "unknown"
    if decision.waitlist_intent in {"contract_intent", "accepts", "provides_detail"}:
        eligibility = "eligible"
    if compiled.selected_action == "join_waitlist":
        eligibility = "eligible"
    if state_snapshot_status in {
        "offered",
        "pending_data",
        "pending_details",
        "joined",
    }:
        eligibility = "eligible"
    return {
        "eligibility": eligibility,
        "status": status,
        "missing_details": missing_details,
    }


def _legacy_demo(decision: ConductorActionDecision, compiled: CompiledTurn) -> dict:
    if compiled.selected_action == "send_demo":
        return {"status": "offered", "next_step": "offer_demo"}
    if decision.demo_intent in {"requested", "curiosity"}:
        return {"status": "viewed_or_asked", "next_step": "ask_demo_reaction"}
    if decision.demo_intent == "reaction_positive":
        return {
            "status": "reacted_positive",
            "next_step": "follow_positive_demo_interest",
        }
    return {"status": "not_offered", "next_step": "none"}


def _legacy_diagnostic(decision: ConductorActionDecision, compiled: CompiledTurn) -> dict:
    action = "none"
    if compiled.selected_action in {
        "answer_price_objection",
        "offer_diagnostic_from_pain",
        "offer_diagnostic_after_answer",
    }:
        action = "offer"
    elif {
        "diagnostic.price_hook",
        "diagnostic.price_hook_with_context",
    }.intersection(compiled.template_ids):
        action = "offer"
    elif {
        "opening.instagram_source",
        "opening.site_cta",
        "opening.general_interest",
    }.intersection(compiled.template_ids):
        action = "offer"
    elif compiled.selected_action == "start_requested_diagnostic":
        action = "start"
    elif compiled.selected_action in {
        "capture_pending_diagnostic_answer",
        "answer_direct_question_then_continue_diagnostic",
        "ask_next_diagnostic_question",
    }:
        action = "ask_next"
    elif compiled.selected_action == "complete_diagnostic":
        action = "complete"
    ledger_updates = [
        {
            "question_key": update["question_key"],
            "status": update["status"],
            "answer_value": update.get("answer_value"),
            "evidence": list(update.get("evidence") or ["compiled.ledger_update"]),
            "confidence": "high",
        }
        for update in compiled.ledger_updates
    ]
    question_by_template = {
        template_id: key for key, template_id in DIAGNOSTIC_ASK_TEMPLATE_BY_KEY.items()
    }
    next_question_key = next(
        (
            question_by_template[template_id]
            for template_id in compiled.template_ids
            if template_id in question_by_template
        ),
        None,
    )
    return {
        "action": action,
        "ledger_updates": ledger_updates,
        "next_question_key": next_question_key,
    }


def _legacy_context(
    *,
    situation: TurnSituation,
    current_user_text: str,
    has_history: bool,
) -> TurnContext:
    snapshot = dict(situation.state_snapshot)
    diagnostic = snapshot.get("diagnostic") or {}
    waitlist = snapshot.get("waitlist") or {}
    demo = snapshot.get("demo") or {}
    handoff = snapshot.get("handoff") or {}
    ledger = diagnostic.get("ledger") or {}
    diagnostic_ledger = [
        {"question_key": key, **value} for key, value in ledger.items() if isinstance(value, dict)
    ]
    compact_memory = []
    if has_history or snapshot.get("canonical_state"):
        current_state = snapshot.get("canonical_state") or "new_lead"
        compact_memory.append(
            {
                "kind": "summary",
                "value": str(snapshot.get("summary") or f"Estado comercial: {current_state}"),
                "current_state": current_state,
            }
        )
    lead_id = snapshot.get("lead_id") or snapshot.get("leadId")
    channel_metadata = snapshot.get("channel_metadata") or {}
    diagnostic_status = diagnostic.get("status") if isinstance(diagnostic, dict) else None
    if diagnostic_status == "delivered":
        diagnostic_status = "completed"
    sales_inbox_inputs = {
        "lead_id": lead_id,
        "source": snapshot.get("source"),
        "entry_intent": snapshot.get("entry_intent"),
        "channel_conversation_id": snapshot.get("channel_conversation_id")
        or (
            channel_metadata.get("channel_conversation_id")
            if isinstance(channel_metadata, dict)
            else None
        ),
        "diagnostic_status": diagnostic_status,
        "diagnostic_final_fields": diagnostic.get("final_fields")
        if isinstance(diagnostic, dict)
        else None,
        "waitlist_status": waitlist.get("status") if isinstance(waitlist, dict) else None,
        "waitlist_idempotency_key": waitlist.get("idempotency_key")
        if isinstance(waitlist, dict)
        else None,
        "waitlist_joined_at": waitlist.get("joined_at") if isinstance(waitlist, dict) else None,
        "handoff_status": snapshot.get("human_status")
        or (handoff.get("status") if isinstance(handoff, dict) else None),
        "demo_status": demo.get("status") if isinstance(demo, dict) else None,
    }
    return TurnContext(
        turn_id="spec012_action_turn",
        conversation_id=str(snapshot.get("conversation_id") or "spec012_action_conv"),
        agent_key="taliya_commercial",
        channel=situation.channel,
        inbound=InboundTurn(
            message_id="spec012_action_inbound",
            idempotency_key="spec012_action_inbound",
            text=current_user_text,
        ),
        product_knowledge=build_official_product_knowledge_refs(None),
        compact_memory=compact_memory,
        recent_transcript=[{"role": "assistant", "content": "..."}] if has_history else [],
        diagnostic_ledger=diagnostic_ledger,
        waitlist_state=dict(waitlist) if isinstance(waitlist, dict) else {},
        demo_state=dict(demo) if isinstance(demo, dict) else {},
        handoff_state=dict(handoff) if isinstance(handoff, dict) else {},
        sales_inbox_inputs={
            key: value
            for key, value in sales_inbox_inputs.items()
            if value is not None and value != ""
        },
    )


def _legacy_decision(
    *,
    compiled: CompiledTurn,
    decision: ConductorActionDecision,
    situation: TurnSituation,
    context: TurnContext,
    items: list[RenderPlanItem],
) -> LegacyConductorDecision:
    route = _route_for(compiled, situation)
    direct_present = bool(decision.direct_question)
    interpreted_intents = list(decision.interpreted_intents)
    product_fact_intents = list(decision.product_fact_keys_used)
    if compiled.selected_action == "answer_source_opening":
        source = str(dict(situation.state_snapshot).get("source") or "")
        if source == "instagram" and "source_from_instagram" not in interpreted_intents:
            interpreted_intents.append("source_from_instagram")
        # The approved source-opening template already contains the broad
        # product overview. Product fact keys must not make the legacy bridge
        # demand a second, redundant how-it-works template.
        product_fact_intents = []
    if compiled.selected_action in {
        "offer_or_join_waitlist_if_eligible",
        "offer_waitlist",
        "join_waitlist",
        "collect_waitlist_missing_detail",
    }:
        interpreted_intents = [
            intent
            for intent in interpreted_intents
            if "price_objection" not in intent.casefold()
            and "objection_price" not in intent.casefold()
        ]
    return LegacyConductorDecision(
        schema_version="011.0",
        decision_id=f"action_{compiled.selected_action}",
        turn_id=context.turn_id,
        conversation_id=context.conversation_id,
        channel=situation.channel,
        agent_key="taliya_commercial",
        role="safety" if route == "safe_fallback" else route,
        route=route,
        previous_state=compiled.previous_state,
        current_state=compiled.current_state,
        next_state=compiled.next_state,
        detected_intents=[
            *interpreted_intents,
            compiled.selected_action,
            *product_fact_intents,
        ],
        direct_question_present=direct_present,
        direct_question_answered_first=(
            not direct_present or compiled.selected_action in ANSWERING_ACTIONS
        ),
        numeric_interpretations=_legacy_numeric_interpretations(decision),
        diagnostic=_legacy_diagnostic(decision, compiled),
        demo=_legacy_demo(decision, compiled),
        waitlist=_legacy_waitlist(decision, compiled, situation),
        handoff={
            "status": "requested"
            if compiled.selected_action in {"handoff_requested", "pause_for_human"}
            else "none",
            "reason": (
                str(compiled.variables.get("handoff_reason", {}).get("value") or "") or None
            ),
        },
        language_policy=LanguagePolicyDecision(
            register="studio_owner_practical",
            crm_term_policy="avoid_by_default",
        ),
        template_plan=RenderPlan(items=items, chunk_policy=compiled.chunk_policy),
        policy_checks={
            "direct_question_answered_first": (
                not direct_present or compiled.selected_action in ANSWERING_ACTIONS
            ),
            "diagnostic_timing_ok": True,
            "waitlist_timing_ok": True,
            "official_facts_only": True,
            "no_internal_text_leak": True,
            "no_early_contact_capture": True,
            "no_human_overlap": True,
        },
        confidence=decision.confidence,
        repair_hints=list(decision.repair_hints),
    )


def _render_plan_items(compiled: CompiledTurn, situation: TurnSituation) -> list[RenderPlanItem]:
    from app.core.taliya_commercial.template_registry import TEMPLATE_REGISTRY

    items: list[RenderPlanItem] = []
    for template_id in compiled.template_ids:
        template = TEMPLATE_REGISTRY.get(template_id)
        accepted = (
            set(template.required_variables) | set(template.optional_variables)
            if template is not None
            else set()
        )
        items.append(
            RenderPlanItem(
                template_id=template_id,
                channel=situation.channel,
                variables={
                    name: TemplateVariableValue.model_validate(payload)
                    for name, payload in compiled.variables.items()
                    if isinstance(payload, dict) and name in accepted
                },
            )
        )
    return items


def build_action_sales_inbox_projection(
    *,
    compiled: CompiledTurn,
    decision: ConductorActionDecision,
    situation: TurnSituation,
    current_user_text: str,
    has_history: bool,
    validator_result: ValidatorResult,
) -> SalesInboxProjection:
    """Build the Sales Inbox projection from validated action-first state.

    This is an adapter around the preserved Spec 011 projection builder:
    action-first output is first mapped to the validated legacy contract, then
    runtime-state diff and projection are derived from that accepted source.
    """

    items = _render_plan_items(compiled, situation)
    legacy_context = _legacy_context(
        situation=situation,
        current_user_text=current_user_text,
        has_history=has_history,
    )
    legacy_decision = _legacy_decision(
        compiled=compiled,
        decision=decision,
        situation=situation,
        context=legacy_context,
        items=items,
    )
    runtime_state_diff = build_runtime_state_diff(
        legacy_decision,
        ValidatorResult(
            decision_id=legacy_decision.decision_id,
            status=validator_result.status,
            errors=list(validator_result.errors),
            warnings=list(validator_result.warnings),
            repair_attempt_count=validator_result.repair_attempt_count,
            final_disposition=validator_result.final_disposition,
        ),
    )
    return build_sales_inbox_projection(
        context=legacy_context,
        decision=legacy_decision,
        validator_result=ValidatorResult(
            decision_id=legacy_decision.decision_id,
            status=validator_result.status,
            errors=list(validator_result.errors),
            warnings=list(validator_result.warnings),
            repair_attempt_count=validator_result.repair_attempt_count,
            final_disposition=validator_result.final_disposition,
        ),
        runtime_state_diff=runtime_state_diff,
        delivery_events=_projection_delivery_events(compiled),
    )


def _projection_delivery_events(compiled: CompiledTurn) -> list[DeliveryEvent]:
    if compiled.selected_action == "join_waitlist":
        return [
            DeliveryEvent(
                event="waitlist_joined",
                idempotency_key=f"waitlist:{compiled.next_state}:1",
                status="recorded",
                metadata={"joined_at": "mocked"},
            )
        ]
    if compiled.selected_action in {"handoff_requested", "pause_for_human"}:
        return [DeliveryEvent(event="handoff_requested", status="recorded")]
    return [DeliveryEvent(event="reserved", status="planned")]


def _has_rich_diagnostic_context(situation: TurnSituation, compiled: CompiledTurn) -> bool:
    completed = set(situation.completed_diagnostic_keys)
    captured = {
        str(update.get("question_key"))
        for update in compiled.ledger_updates
        if update.get("question_key")
        and update.get("status") in {"answered", "inferred_from_prior_message"}
    }
    return len(completed | captured) >= 3


def _validate_action_voice_contract(
    *,
    compiled: CompiledTurn,
    decision: ConductorActionDecision,
    situation: TurnSituation,
    current_user_text: str,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    source = str(dict(situation.state_snapshot).get("source") or "")
    declared_intents = " ".join(decision.interpreted_intents).casefold()
    if (
        situation.mode == "entry"
        and source == "instagram"
        and "instagram" in declared_intents
        and compiled.selected_action == "answer_general_interest"
    ):
        issues.append(
            _issue(
                "instagram_source_action_required",
                "The LLM declared an Instagram-source opening, so the turn "
                "must use answer_source_opening instead of the generic "
                "interest action.",
                path="selected_action",
            )
        )
    if (
        "product.price_direct" in compiled.template_ids
        and "diagnostic.price_hook" in compiled.template_ids
        and _decision_declares_price_with_context(decision)
    ):
        issues.append(
            _issue(
                "price_plus_context_requires_context_hook",
                "When the LLM declares price plus pain/context in the same "
                "turn, the price answer must include plan_fit_context so the "
                "runtime renders diagnostic.price_hook_with_context.",
                path="composition_variables.plan_fit_context",
            )
        )
    if (
        situation.mode == "post_diagnostic"
        and compiled.selected_action != "offer_or_join_waitlist_if_eligible"
        and _decision_declares_waitlist_start(decision)
    ):
        issues.append(
            _issue(
                "post_diagnostic_waitlist_intent_requires_waitlist_action",
                "When the LLM declares post-diagnostic start/list intent, the "
                "turn must use offer_or_join_waitlist_if_eligible instead of "
                "continuing an objection/product answer.",
                path="selected_action",
            )
        )
    lead_used_crm = "crm" in current_user_text.casefold()
    rich_diagnostic_context = _has_rich_diagnostic_context(situation, compiled)
    pain_context = compiled.variables.get("pain_context_human")
    pain_context_value = (
        str(pain_context.get("value") or "") if isinstance(pain_context, dict) else ""
    )
    if (
        compiled.selected_action == "offer_diagnostic_from_pain"
        and isinstance(pain_context, dict)
        and not any(
            marker in pain_context_value.casefold() for marker in CUSTOMER_VISIBLE_INTERNAL_MARKERS
        )
        and not _has_current_turn_context_anchor(
            current_user_text=current_user_text,
            value=pain_context_value,
        )
    ):
        issues.append(
            _issue(
                "pain_context_missing_specific_anchor",
                "Pain-first acknowledgement must preserve a concrete channel, "
                "process, or object from the lead's message while paraphrasing "
                "the situation naturally.",
                path="composition_variables.pain_context_human",
            )
        )
    for variable in decision.composition_variables:
        if variable.name == "waitlist_context_summary" and any(
            marker in str(variable.value).casefold()
            for marker in ("checkout", "desconto", "vip", "condicao especial")
        ):
            issues.append(
                _issue(
                    "waitlist_context_summary_promises_blocked",
                    "Waitlist context must not contain checkout, discount, VIP, "
                    "or special-condition promises.",
                    path="composition_variables.waitlist_context_summary",
                )
            )
    for name, payload in compiled.variables.items():
        value = str(payload.get("value") or "")
        lowered = value.casefold()
        if "crm" in lowered and not lead_used_crm:
            issues.append(
                _issue(
                    "voice_crm_jargon_for_lay_lead",
                    "CRM jargon is not customer-facing default language; use "
                    "studio-owner practical wording unless the lead used it.",
                    path=f"variables.{name}",
                )
            )
        if (
            any(phrase in lowered for phrase in _THIN_CONTEXT_EVIDENCE_PHRASES)
            and not rich_diagnostic_context
        ):
            issues.append(
                _issue(
                    "voice_thin_context_evidence_framing",
                    "'pelo que voce contou' requires rich diagnostic evidence; "
                    "thin-context turns must use lighter wording.",
                    path=f"variables.{name}",
                )
            )
    return issues


def _decision_declares_price_with_context(decision: ConductorActionDecision) -> bool:
    if decision.selected_action not in {
        "answer_price",
        "answer_direct_product_question",
    }:
        return False
    if not (
        "prices" in decision.product_fact_keys_used
        or any("price" in intent.casefold() for intent in decision.interpreted_intents)
    ):
        return False
    contextual_slots = {
        "main_pain",
        "pain_detail",
        "current_process",
        "priority",
    }
    if any(
        slot.key in contextual_slots and slot.status != "ambiguous"
        for slot in decision.captured_slots
    ):
        return True
    intent_text = " ".join(decision.interpreted_intents).casefold()
    if any(marker in intent_text for marker in _CONTEXTUAL_PRICE_INTENT_MARKERS):
        return True
    return False


def _decision_declares_answerable_product_fact(
    decision: ConductorActionDecision,
) -> bool:
    return any(
        fact_key in {"prices", "plans", "demo_link"} for fact_key in decision.product_fact_keys_used
    )


def _decision_declares_price_question(decision: ConductorActionDecision) -> bool:
    return any("price" in intent.casefold() for intent in decision.interpreted_intents)


def _decision_declares_waitlist_start(decision: ConductorActionDecision) -> bool:
    if decision.waitlist_intent in {"contract_intent", "accepts"}:
        return True
    if any(
        variable.name == "waitlist_context_summary" for variable in decision.composition_variables
    ):
        return True
    intent_text = " ".join(decision.interpreted_intents).casefold()
    return any(marker in intent_text for marker in ("waitlist", "lista", "start"))


def _has_current_turn_context_anchor(*, current_user_text: str, value: str) -> bool:
    if "crm" in current_user_text.casefold() and "crm" in value.casefold():
        return True
    inbound_tokens = {
        token
        for token in _normalized_tokens(current_user_text)
        if (len(token) >= 6 or token == "crm") and token not in _CONTEXT_ANCHOR_STOPWORDS
    }
    if not inbound_tokens:
        return True
    value_tokens = set(_normalized_tokens(value))
    return bool(inbound_tokens & value_tokens)


def _validate_customer_visible_messages(
    rendered: list[RenderedMessage],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for index, message in enumerate(rendered):
        text = message.text
        lowered = text.casefold()
        for marker in CUSTOMER_VISIBLE_INTERNAL_MARKERS:
            if marker in lowered:
                issues.append(
                    _issue(
                        "customer_visible_internal_text_leak",
                        f"customer-visible message contains internal marker: {marker!r}",
                        path=f"rendered_messages[{index}]",
                    )
                )
                break
        if any(marker in text for marker in CUSTOMER_VISIBLE_ENCODING_MARKERS):
            issues.append(
                _issue(
                    "customer_visible_encoding_artifact",
                    "customer-visible message contains mojibake/encoding artifact.",
                    path=f"rendered_messages[{index}]",
                )
            )
        if "{" in text or "}" in text:
            issues.append(
                _issue(
                    "customer_visible_placeholder_leak",
                    "customer-visible message contains an unresolved placeholder.",
                    path=f"rendered_messages[{index}]",
                )
            )
        if any(marker in text for marker in CUSTOMER_VISIBLE_BAD_PUNCTUATION):
            issues.append(
                _issue(
                    "customer_visible_text_quality",
                    "customer-visible message contains broken punctuation.",
                    path=f"rendered_messages[{index}]",
                )
            )
    return issues


def validate_compiled_turn(
    compiled: CompiledTurn,
    *,
    decision: ConductorActionDecision,
    situation: TurnSituation,
    current_user_text: str,
    has_history: bool,
) -> ActionTurnValidation:
    issues: list[ValidationIssue] = []

    for code in compiled.issues:
        message = f"compiler blocked the turn: {code}"
        if code == "conductor_action_not_in_allowed_menu":
            message += "; allowed actions this turn: " + ", ".join(situation.allowed_actions)
        elif code == "compile_capture_completed_use_complete_diagnostic":
            message += (
                "; the captured answer completes the last mandatory key: "
                "choose complete_diagnostic and include the compositions "
                "pain_context_human, crm_base_recommendation, and "
                "operational_first_step grounded in the ledger (in Brazilian "
                "Portuguese), keeping the same captured_slots."
            )
        issues.append(_issue(code, message))

    # Direct-question adequacy at the ACTION level (deterministic).
    question = decision.direct_question
    if question and _question_is_from_current_inbound(question, current_user_text):
        if compiled.selected_action in CLARIFYING_ACTIONS:
            direct_answer_missing = (
                not decision.needs_clarification
                or _decision_declares_answerable_product_fact(decision)
                or _decision_declares_price_question(decision)
            )
        else:
            direct_answer_missing = compiled.selected_action not in ANSWERING_ACTIONS
        if direct_answer_missing and situation.mode != "delivery_deferred":
            issues.append(
                _issue(
                    "action_direct_question_not_answered_first",
                    f"Direct question '{question}' requires an answering "
                    f"action; '{compiled.selected_action}' is steering. Pick "
                    "the action that answers it first.",
                    path="selected_action",
                )
            )
    elif question:
        issues.append(
            _issue(
                "action_stale_direct_question",
                f"direct_question '{question}' is not asked in the current "
                "inbound message; clear it.",
                path="direct_question",
            )
        )

    # Anti-parrot: compositions must reuse meaning, not the lead's sentence.
    inbound_tokens = _normalized_tokens(current_user_text)
    for name, payload in compiled.variables.items():
        value = str(payload.get("value") or "")
        value_tokens = _normalized_tokens(value)
        if (
            len(value_tokens) >= 4
            and inbound_tokens
            and len(value_tokens & inbound_tokens) / len(value_tokens) > 0.8
        ):
            issues.append(
                _issue(
                    "voice_literal_parroting",
                    f"variable {name} repeats the lead's sentence almost "
                    "literally; rephrase the meaning naturally.",
                    path=f"variables.{name}",
                )
            )

    issues.extend(
        _validate_action_voice_contract(
            compiled=compiled,
            decision=decision,
            situation=situation,
            current_user_text=current_user_text,
        )
    )

    validator_result = ValidatorResult(
        decision_id=f"action_{compiled.selected_action}",
        status="passed" if not issues else "failed",
        errors=issues,
        final_disposition="accepted" if not issues else "blocked",
    )
    if issues:
        return ActionTurnValidation(validator_result=validator_result)

    # Port the full Spec 011 validator set onto the action-first compiled
    # shape. The LLM still returns only ConductorActionDecision; this adapter is
    # a validation bridge, not a second conversation brain.
    items = _render_plan_items(compiled, situation)
    legacy_context = _legacy_context(
        situation=situation,
        current_user_text=current_user_text,
        has_history=has_history,
    )
    legacy_result = validate_conductor_result(
        _legacy_decision(
            compiled=compiled,
            decision=decision,
            situation=situation,
            context=legacy_context,
            items=items,
        ),
        legacy_context,
    )
    if legacy_result.status != "passed":
        return ActionTurnValidation(
            validator_result=ValidatorResult(
                decision_id=legacy_result.decision_id,
                status="failed",
                errors=list(legacy_result.errors),
                final_disposition="blocked",
            )
        )

    # The legacy validator receives the same shape for contract checks and may
    # normalize nested plan items. Rebuild from the compiled action output so
    # the approved renderer gets the compiler-owned variables intact.
    items = _render_plan_items(compiled, situation)
    try:
        rendered = render_validated_template_plan(
            RenderPlan(items=items, chunk_policy=compiled.chunk_policy),
            validator_result,
            channel=situation.channel,
        )
    except (RenderError, ValueError) as exc:
        return ActionTurnValidation(
            validator_result=ValidatorResult(
                decision_id=validator_result.decision_id,
                status="failed",
                errors=[_issue("action_render_failed", str(exc)[:300])],
                final_disposition="blocked",
            )
        )

    # Mid-conversation: drop approved-body greeting chunks (delivery shaping).
    if has_history:
        rendered = [
            message
            for message in rendered
            if message.text.strip().lower() not in _PURE_GREETING_CHUNKS
        ]

    # Voice rules on the final rendered text.
    voice_issues: list[ValidationIssue] = []
    rendered_text = " ".join(message.text for message in rendered).lower()
    for phrase in BANNED_RENDERED_PHRASES:
        if phrase in rendered_text:
            voice_issues.append(
                _issue(
                    "voice_banned_phrase",
                    f"banned phrase rendered: '{phrase}'",
                )
            )
    if has_history and any(marker in rendered_text for marker in _GREETING_MARKERS):
        voice_issues.append(
            _issue(
                "voice_repeated_greeting",
                "greeting rendered mid-conversation; greetings are for the first contact only.",
            )
        )
    voice_issues.extend(_validate_customer_visible_messages(list(rendered)))
    if voice_issues:
        return ActionTurnValidation(
            validator_result=ValidatorResult(
                decision_id=validator_result.decision_id,
                status="failed",
                errors=voice_issues,
                final_disposition="blocked",
            )
        )

    return ActionTurnValidation(validator_result=validator_result, rendered_preview=list(rendered))
