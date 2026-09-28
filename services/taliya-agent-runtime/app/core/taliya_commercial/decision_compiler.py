from __future__ import annotations

from typing import Any

from app.core.taliya_commercial.schemas import (
    CapturedSlot,
    ConductorActionDecision,
    ConductorDecision,
    DiagnosticLedgerItem,
    LanguagePolicyDecision,
    PolicyChecks,
    RenderPlan,
    RenderPlanItem,
    TemplateVariableValue,
    TurnContext,
    TurnFact,
)
from app.core.taliya_commercial.turn_situation import (
    DiagnosticQuestionKey,
    TurnSituation,
)

_DIAGNOSTIC_TEMPLATE_BY_KEY: dict[str, str] = {
    "active_students_or_size": "diagnostic.ask_active_students",
    "main_pain": "diagnostic.ask_main_pain",
    "pain_detail": "diagnostic.ask_pain_detail",
    "current_process": "diagnostic.ask_current_process",
    "priority": "diagnostic.ask_priority",
    "urgency": "diagnostic.ask_urgency",
}
_COMPLETE_DIAGNOSTIC_KEYS = (
    "active_students_or_size",
    "main_pain",
    "pain_detail",
    "current_process",
    "priority",
    "urgency",
)


class DecisionCompilerError(Exception):
    """Raised when an action decision cannot be safely compiled."""


def compile_action_decision(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
    turn_situation: TurnSituation,
) -> ConductorDecision:
    _validate_context_alignment(action_decision, context, turn_situation)

    if action_decision.selected_action in {
        "answer_direct_product_question",
        "answer_price",
    }:
        return _compile_price_answer(action_decision, context=context)

    if action_decision.selected_action == "answer_general_interest":
        return _compile_entry_opening(
            action_decision,
            context=context,
            template_id="opening.general_interest",
        )

    if action_decision.selected_action == "answer_source_opening":
        template_id = (
            "opening.instagram_source"
            if "source_from_instagram" in action_decision.interpreted_intents
            else "opening.site_cta"
        )
        return _compile_entry_opening(
            action_decision,
            context=context,
            template_id=template_id,
        )

    if action_decision.selected_action == "offer_diagnostic_from_pain":
        return _compile_diagnostic_offer_from_pain(
            action_decision,
            context=context,
            turn_situation=turn_situation,
        )

    if action_decision.selected_action == "start_requested_diagnostic":
        return _compile_start_requested_diagnostic(
            action_decision,
            context=context,
            turn_situation=turn_situation,
        )

    if action_decision.selected_action == "handoff_requested":
        return _compile_handoff_requested(action_decision, context=context)

    if action_decision.selected_action == "clarify_ambiguous_opening":
        return _compile_clarification(
            action_decision,
            context=context,
            role="entry",
            route="entry",
            current_state="entry_clarification",
            next_state="entry",
        )

    if action_decision.selected_action == "capture_pending_diagnostic_answer":
        return _compile_pending_diagnostic_capture(
            action_decision,
            context=context,
            turn_situation=turn_situation,
        )

    if action_decision.selected_action == "answer_direct_question_then_continue_diagnostic":
        return _compile_direct_question_then_continue_diagnostic(
            action_decision,
            context=context,
            turn_situation=turn_situation,
        )

    if action_decision.selected_action == "ask_next_diagnostic_question":
        return _compile_ask_next_diagnostic_question(
            action_decision,
            context=context,
            turn_situation=turn_situation,
        )

    if action_decision.selected_action == "complete_diagnostic":
        return _compile_completed_diagnostic_without_new_slot(
            action_decision,
            context=context,
        )

    if action_decision.selected_action == "clarify_ambiguous_diagnostic_answer":
        return _compile_ambiguous_diagnostic_answer(
            action_decision,
            context=context,
            turn_situation=turn_situation,
        )

    if action_decision.selected_action == "respect_diagnostic_refusal":
        return _compile_diagnostic_refusal(action_decision, context=context)

    if action_decision.selected_action == "send_demo":
        return _compile_send_demo(action_decision, context=context)

    if action_decision.selected_action == "answer_product_question_with_saved_context":
        return _compile_post_diagnostic_how_it_works(action_decision, context=context)

    if action_decision.selected_action == "answer_price_objection_with_context":
        return _compile_price_objection_with_context(
            action_decision,
            context=context,
            diagnostic_offer=False,
        )

    if action_decision.selected_action == "offer_or_join_waitlist_if_eligible":
        return _compile_waitlist_offer_with_context(action_decision, context=context)

    if action_decision.selected_action == "ask_demo_reaction":
        return _compile_ask_demo_reaction(action_decision, context=context)

    if action_decision.selected_action == "clarify_ambiguous_followup":
        return _compile_clarification(
            action_decision,
            context=context,
            role="product",
            route="product",
            current_state="followup_clarification",
            next_state="post_diagnostic",
        )

    if action_decision.selected_action == "answer_plan_fit_with_diagnostic_offer":
        return _compile_plan_fit_with_diagnostic_offer(action_decision, context=context)

    if action_decision.selected_action == "answer_how_it_works":
        return _compile_post_diagnostic_how_it_works(action_decision, context=context)

    if action_decision.selected_action == "answer_whatsapp_scope":
        return _compile_whatsapp_scope(action_decision, context=context)

    if action_decision.selected_action == "answer_integration_scope_safely":
        return _compile_integration_scope(action_decision, context=context)

    if action_decision.selected_action == "answer_price_objection":
        return _compile_price_objection_with_context(
            action_decision,
            context=context,
            diagnostic_offer=True,
        )

    if action_decision.selected_action == "offer_diagnostic_after_answer":
        return _compile_diagnostic_offer_after_answer(action_decision, context=context)

    if action_decision.selected_action == "clarify_product_question":
        return _compile_clarification(
            action_decision,
            context=context,
            role="product",
            route="product",
            current_state="product_clarification",
            next_state="product_question",
        )

    if action_decision.selected_action == "offer_waitlist":
        return _compile_waitlist_offer_with_context(action_decision, context=context)

    if action_decision.selected_action == "collect_waitlist_missing_detail":
        return _compile_collect_waitlist_missing_detail(
            action_decision,
            context=context,
        )

    if action_decision.selected_action == "join_waitlist":
        return _compile_join_waitlist(action_decision, context=context)

    if action_decision.selected_action == "decline_waitlist":
        return _compile_decline_waitlist(action_decision, context=context)

    if action_decision.selected_action == "answer_question_then_continue_waitlist":
        return _compile_answer_question_then_continue_waitlist(
            action_decision,
            context=context,
        )

    raise DecisionCompilerError(
        f"unsupported selected_action for compiler: {action_decision.selected_action}"
    )


def _validate_context_alignment(
    action_decision: ConductorActionDecision,
    context: TurnContext,
    turn_situation: TurnSituation,
) -> None:
    mismatches = []
    for field_name in ("turn_id", "conversation_id", "channel", "agent_key"):
        if getattr(action_decision, field_name) != getattr(context, field_name):
            mismatches.append(field_name)
    if action_decision.turn_id != turn_situation.turn_id:
        mismatches.append("turn_situation.turn_id")
    if action_decision.selected_action not in turn_situation.allowed_actions:
        mismatches.append("selected_action")
    if mismatches:
        raise DecisionCompilerError(
            "action decision does not match compiler context: "
            + ", ".join(sorted(set(mismatches)))
        )


def _compile_price_answer(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
) -> ConductorDecision:
    plan_price_summary = _official_price_summary(context)
    diagnostic_hook_item = _diagnostic_hook_item_for_price(action_decision)
    items = [
        RenderPlanItem(
            template_id="product.price_direct",
            variables={
                "plan_price_summary": _template_value(
                    "long_text",
                    plan_price_summary,
                    source="official_product_knowledge",
                    evidence=["product_knowledge.prices"],
                    max_length=360,
                )
            },
        ),
        diagnostic_hook_item,
    ]
    return _base_decision(
        action_decision,
        context=context,
        role="product",
        route="product",
        previous_state="entry",
        current_state="product_question",
        next_state="product_question_answered",
        template_plan=RenderPlan(items=items),
        direct_question_present=True,
        direct_question_answered_first=True,
        diagnostic_action="offer",
    )


def _compile_entry_opening(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
    template_id: str,
) -> ConductorDecision:
    return _base_decision(
        action_decision,
        context=context,
        role="entry",
        route="entry",
        previous_state="entry",
        current_state="entry_opening",
        next_state="diagnostic_offered",
        template_plan=RenderPlan(items=[RenderPlanItem(template_id=template_id)]),
        diagnostic_action="offer",
    )


def _compile_diagnostic_offer_from_pain(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
    turn_situation: TurnSituation,
) -> ConductorDecision:
    items = [
        RenderPlanItem(template_id="opening.cold_greeting"),
        RenderPlanItem(
            template_id="diagnostic.offer_soft",
            variables={
                "pain_context_human": _template_value(
                    "long_text",
                    _required_diagnostic_text(
                        action_decision,
                        "pain_context_human",
                    ),
                    source="user_message",
                    evidence=list(action_decision.evidence),
                    max_length=420,
                )
            },
        )
    ]
    asks_first_question = "active_students_or_size" in turn_situation.missing_diagnostic_keys
    if asks_first_question:
        items.append(RenderPlanItem(template_id="diagnostic.ask_active_students"))
    return _base_decision(
        action_decision,
        context=context,
        role="diagnostic",
        route="diagnostic",
        previous_state="entry",
        current_state="diagnostic_offered",
        next_state="diagnostic_in_progress",
        template_plan=RenderPlan(items=items),
        diagnostic_action="start" if asks_first_question else "offer",
        next_question_key=(
            "active_students_or_size" if asks_first_question else None
        ),
    )


def _compile_start_requested_diagnostic(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
    turn_situation: TurnSituation,
) -> ConductorDecision:
    next_question = turn_situation.pending_question_key or "active_students_or_size"
    return _base_decision(
        action_decision,
        context=context,
        role="diagnostic",
        route="diagnostic",
        previous_state="entry",
        current_state="diagnostic_start",
        next_state="diagnostic_in_progress",
        template_plan=RenderPlan(
            items=[
                RenderPlanItem(template_id="opening.diagnostic_cta"),
                RenderPlanItem(template_id=_DIAGNOSTIC_TEMPLATE_BY_KEY[next_question]),
            ]
        ),
        diagnostic_action="start",
        next_question_key=next_question,
    )


def _compile_handoff_requested(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
) -> ConductorDecision:
    return _base_decision(
        action_decision,
        context=context,
        role="handoff",
        route="handoff",
        previous_state="commercial_conversation",
        current_state="human_handoff",
        next_state="paused_by_human",
        template_plan=RenderPlan(items=[RenderPlanItem(template_id="handoff.acknowledge")]),
        handoff_status="requested",
        handoff_reason=_handoff_reason(action_decision),
    )


def _compile_clarification(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
    role: str,
    route: str,
    current_state: str,
    next_state: str,
) -> ConductorDecision:
    return _base_decision(
        action_decision,
        context=context,
        role=role,
        route=route,
        previous_state="commercial_conversation",
        current_state=current_state,
        next_state=next_state,
        template_plan=RenderPlan(
            items=[
                RenderPlanItem(
                    template_id="fallback.unmapped_adaptive",
                    variables={
                        "clarification_question": _template_value(
                            "short_text",
                            _clarification_question(action_decision),
                            source="model_decision",
                            evidence=list(action_decision.evidence),
                            max_length=140,
                        )
                    },
                )
            ]
        ),
    )


def _diagnostic_hook_item_for_price(
    action_decision: ConductorActionDecision,
) -> RenderPlanItem:
    plan_fit_context = action_decision.diagnostic_intent.details.get("plan_fit_context")
    if isinstance(plan_fit_context, str) and plan_fit_context.strip():
        return RenderPlanItem(
            template_id="diagnostic.price_hook_with_context",
            variables={
                "plan_fit_context": _template_value(
                    "short_text",
                    plan_fit_context.strip(),
                    source="user_message",
                    evidence=list(action_decision.evidence),
                    max_length=180,
                )
            },
        )
    return RenderPlanItem(template_id="diagnostic.price_hook")


def _compile_pending_diagnostic_capture(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
    turn_situation: TurnSituation,
) -> ConductorDecision:
    pending_key = turn_situation.pending_question_key
    if pending_key is None:
        raise DecisionCompilerError("pending diagnostic capture requires pending_question_key")
    slot = _slot_for_key(action_decision.captured_slots, pending_key)
    if slot is None:
        raise DecisionCompilerError(
            f"pending diagnostic capture requires captured slot: {pending_key}"
        )

    ledger_update = _ledger_update_from_slot(slot, pending_key)
    completed_keys = set(turn_situation.completed_diagnostic_keys)
    completed_keys.add(pending_key)
    if all(key in completed_keys for key in _COMPLETE_DIAGNOSTIC_KEYS):
        return _compile_completed_diagnostic(
            action_decision,
            context=context,
            ledger_update=ledger_update,
        )

    next_question = next(
        key for key in _COMPLETE_DIAGNOSTIC_KEYS if key not in completed_keys
    )
    return _base_decision(
        action_decision,
        context=context,
        role="diagnostic",
        route="diagnostic",
        previous_state="diagnostic_in_progress",
        current_state="diagnostic_in_progress",
        next_state="diagnostic_in_progress",
        template_plan=RenderPlan(
            items=[
                RenderPlanItem(
                    template_id=_DIAGNOSTIC_TEMPLATE_BY_KEY[next_question],
                    variables={
                        "answer_feedback": _template_value(
                            "short_text",
                            _feedback_for_slot(slot),
                            source="diagnostic_ledger",
                            evidence=list(slot.evidence),
                            max_length=180,
                        )
                    },
                )
            ]
        ),
        diagnostic_action="ask_next",
        ledger_updates=[ledger_update],
        next_question_key=next_question,
    )


def _compile_ask_next_diagnostic_question(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
    turn_situation: TurnSituation,
) -> ConductorDecision:
    next_question = turn_situation.pending_question_key
    if next_question is None:
        raise DecisionCompilerError("ask_next diagnostic requires pending_question_key")
    return _base_decision(
        action_decision,
        context=context,
        role="diagnostic",
        route="diagnostic",
        previous_state="diagnostic_in_progress",
        current_state="diagnostic_in_progress",
        next_state="diagnostic_in_progress",
        template_plan=RenderPlan(
            items=[RenderPlanItem(template_id=_DIAGNOSTIC_TEMPLATE_BY_KEY[next_question])]
        ),
        diagnostic_action="ask_next",
        next_question_key=next_question,
    )


def _compile_direct_question_then_continue_diagnostic(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
    turn_situation: TurnSituation,
) -> ConductorDecision:
    next_question = turn_situation.pending_question_key
    if next_question is None:
        raise DecisionCompilerError("diagnostic continuation requires pending_question_key")
    return _base_decision(
        action_decision,
        context=context,
        role="diagnostic",
        route="diagnostic",
        previous_state="diagnostic_in_progress",
        current_state="diagnostic_product_answer",
        next_state="diagnostic_in_progress",
        template_plan=RenderPlan(
            items=[
                RenderPlanItem(
                    template_id="product.how_it_works_direct",
                    variables={
                        "contextual_next_step": _template_value(
                            "enum",
                            "continue_diagnostic",
                            source="model_decision",
                            evidence=list(action_decision.evidence),
                        )
                    },
                ),
                RenderPlanItem(template_id=_DIAGNOSTIC_TEMPLATE_BY_KEY[next_question]),
            ]
        ),
        direct_question_present=True,
        direct_question_answered_first=True,
        diagnostic_action="ask_next",
        next_question_key=next_question,
    )


def _compile_completed_diagnostic_without_new_slot(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
) -> ConductorDecision:
    return _compile_completed_diagnostic(
        action_decision,
        context=context,
        ledger_update=None,
    )


def _compile_ambiguous_diagnostic_answer(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
    turn_situation: TurnSituation,
) -> ConductorDecision:
    pending_key = turn_situation.pending_question_key
    question = (
        "Pode me responder esse ponto de um jeito mais direto?"
        if pending_key is None
        else _clarification_for_diagnostic_key(pending_key)
    )
    return _base_decision(
        action_decision,
        context=context,
        role="diagnostic",
        route="diagnostic",
        previous_state="diagnostic_in_progress",
        current_state="diagnostic_insufficient_evidence",
        next_state="diagnostic_in_progress",
        template_plan=RenderPlan(
            items=[
                RenderPlanItem(
                    template_id="diagnostic.insufficient_evidence",
                    variables={
                        "clarification_question": _template_value(
                            "short_text",
                            question,
                            source="model_decision",
                            evidence=list(action_decision.evidence),
                            max_length=140,
                        )
                    },
                )
            ]
        ),
        diagnostic_action="insufficient_evidence",
        next_question_key=pending_key,
    )


def _compile_diagnostic_refusal(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
) -> ConductorDecision:
    return _base_decision(
        action_decision,
        context=context,
        role="product",
        route="product",
        previous_state="diagnostic_offered",
        current_state="diagnostic_refused",
        next_state="product_question",
        template_plan=RenderPlan(items=[RenderPlanItem(template_id="product.overview_short")]),
        official_facts_only=False,
    )


def _compile_completed_diagnostic(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
    ledger_update: DiagnosticLedgerItem | None,
) -> ConductorDecision:
    diagnostic_evidence = _diagnostic_evidence(
        context,
        extra=(
            list(ledger_update.evidence)
            if ledger_update is not None
            else list(action_decision.evidence)
        ),
    )
    items = [
        RenderPlanItem(template_id="diagnostic.deliver_hold"),
        RenderPlanItem(
            template_id="diagnostic.deliver_context",
            variables={
                "pain_context_human": _template_value(
                    "long_text",
                    _diagnostic_text(
                        action_decision,
                        "pain_context_human",
                        "Pelo que voce contou, o studio precisa organizar melhor os "
                        "pontos que mais pesam na rotina antes de escolher um plano.",
                    ),
                    source="diagnostic_ledger",
                    evidence=diagnostic_evidence,
                    max_length=420,
                )
            },
        ),
        RenderPlanItem(
            template_id="diagnostic.deliver_crm_base",
            variables={
                "crm_base_recommendation": _template_value(
                    "long_text",
                    _diagnostic_text(
                        action_decision,
                        "crm_base_recommendation",
                        "Eu comecaria deixando conversas, alunos, pendencias e "
                        "proximos passos em uma base organizada para a equipe "
                        "enxergar prioridade.",
                    ),
                    source="diagnostic_ledger",
                    evidence=diagnostic_evidence,
                    max_length=260,
                )
            },
        ),
        RenderPlanItem(
            template_id="diagnostic.deliver_operational_step",
            variables={
                "operational_first_step": _template_value(
                    "long_text",
                    _diagnostic_text(
                        action_decision,
                        "operational_first_step",
                        "O primeiro passo pratico seria separar o que precisa de "
                        "retorno hoje e o que pode virar rotina acompanhada.",
                    ),
                    source="diagnostic_ledger",
                    evidence=diagnostic_evidence,
                    max_length=240,
                )
            },
        ),
        RenderPlanItem(
            template_id="diagnostic.deliver_agent_recommendation",
            variables={
                "agent_name": _template_value(
                    "short_text",
                    _recommended_agent_name(context),
                    source="official_product_knowledge",
                    evidence=["product_knowledge.plans"],
                    max_length=60,
                ),
                "agent_pain_resolved": _template_value(
                    "long_text",
                    _diagnostic_text(
                        action_decision,
                        "agent_pain_resolved",
                        "rotinas importantes ficando sem acompanhamento claro",
                    ),
                    source="diagnostic_ledger",
                    evidence=diagnostic_evidence,
                    max_length=180,
                ),
                "agent_practical_action": _template_value(
                    "long_text",
                    _diagnostic_text(
                        action_decision,
                        "agent_practical_action",
                        "ajuda a organizar retornos, proximos passos e pontos que precisam de acao",
                    ),
                    source="diagnostic_ledger",
                    evidence=diagnostic_evidence,
                    max_length=280,
                ),
            },
        ),
        RenderPlanItem(
            template_id="diagnostic.deliver_plan_recommendation",
            variables={
                "recommended_plan_or_range": _template_value(
                    "short_text",
                    _recommended_plan_or_range(context),
                    source="official_product_knowledge",
                    evidence=["product_knowledge.plans"],
                    max_length=90,
                )
            },
        ),
        RenderPlanItem(
            template_id="diagnostic.deliver_demo_not_offered",
            variables={
                "demo_status": _template_value(
                    "enum",
                    "not_offered",
                    source="runtime_state",
                    evidence=["runtime_state.demo.status"],
                )
            },
        ),
    ]
    return _base_decision(
        action_decision,
        context=context,
        role="diagnostic",
        route="diagnostic",
        previous_state="diagnostic_in_progress",
        current_state="diagnostic_ready",
        next_state="diagnostic_delivered",
        template_plan=RenderPlan(items=items, chunk_policy="staged_diagnostic"),
        diagnostic_action="complete",
        ledger_updates=[ledger_update] if ledger_update is not None else [],
        final_fields={"recommended_plan_or_range": _recommended_plan_or_range(context)},
    )


def _compile_send_demo(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
) -> ConductorDecision:
    return _base_decision(
        action_decision,
        context=context,
        role="product",
        route="product",
        previous_state="post_diagnostic",
        current_state="demo_requested",
        next_state="demo_offered",
        template_plan=RenderPlan(
            items=[
                RenderPlanItem(
                    template_id="product.demo_direct",
                    variables={
                        "official_demo_link": _template_value(
                            "url",
                            _official_demo_link(context),
                            source="official_product_knowledge",
                            evidence=["product_knowledge.links"],
                        )
                    },
                )
            ]
        ),
        direct_question_present=True,
        direct_question_answered_first=True,
        demo_status="offered",
        demo_next_step="offer_demo",
    )


def _compile_post_diagnostic_how_it_works(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
) -> ConductorDecision:
    return _base_decision(
        action_decision,
        context=context,
        role="product",
        route="product",
        previous_state="post_diagnostic",
        current_state="product_followup",
        next_state="post_diagnostic",
        template_plan=RenderPlan(
            items=[
                RenderPlanItem(
                    template_id="product.how_it_works_direct",
                    variables={
                        "contextual_next_step": _template_value(
                            "enum",
                            "diagnostic_offer_generic",
                            source="model_decision",
                            evidence=list(action_decision.evidence),
                        )
                    },
                )
            ]
        ),
        direct_question_present=True,
        direct_question_answered_first=True,
    )


def _compile_price_objection_with_context(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
    diagnostic_offer: bool,
) -> ConductorDecision:
    return _base_decision(
        action_decision,
        context=context,
        role="product",
        route="product",
        previous_state="post_diagnostic",
        current_state="price_objection",
        next_state="post_diagnostic",
        template_plan=RenderPlan(items=[RenderPlanItem(template_id="product.price_objection_value")]),
        direct_question_present=True,
        direct_question_answered_first=True,
        diagnostic_action="offer" if diagnostic_offer else "none",
        official_facts_only=False,
    )


def _compile_ask_demo_reaction(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
) -> ConductorDecision:
    return _base_decision(
        action_decision,
        context=context,
        role="product",
        route="product",
        previous_state="post_diagnostic",
        current_state="demo_followup",
        next_state="post_diagnostic",
        template_plan=RenderPlan(
            items=[
                RenderPlanItem(
                    template_id="diagnostic.deliver_demo_already_offered",
                    variables={
                        "demo_status": _template_value(
                            "enum",
                            _demo_status_for_reaction(context),
                            source="runtime_state",
                            evidence=["runtime_state.demo.status"],
                        )
                    },
                )
            ]
        ),
        demo_status=_demo_status_for_reaction(context),
        demo_next_step="ask_demo_reaction",
    )


def _compile_plan_fit_with_diagnostic_offer(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
) -> ConductorDecision:
    return _base_decision(
        action_decision,
        context=context,
        role="product",
        route="product",
        previous_state="entry",
        current_state="plan_fit_question",
        next_state="diagnostic_offered",
        template_plan=RenderPlan(
            items=[
                RenderPlanItem(
                    template_id="product.plan_fit_with_diagnostic",
                    variables={
                        "plan_fit_context": _template_value(
                            "short_text",
                            _plan_fit_context(action_decision),
                            source="user_message",
                            evidence=list(action_decision.evidence),
                            max_length=180,
                        )
                    },
                )
            ]
        ),
        direct_question_present=True,
        direct_question_answered_first=True,
        diagnostic_action="offer",
        official_facts_only=False,
    )


def _compile_whatsapp_scope(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
) -> ConductorDecision:
    return _base_decision(
        action_decision,
        context=context,
        role="product",
        route="product",
        previous_state="entry",
        current_state="product_question",
        next_state="product_question_answered",
        template_plan=RenderPlan(
            items=[
                RenderPlanItem(
                    template_id="product.whatsapp_direct",
                    variables={
                        "product_fact_summary": _template_value(
                            "long_text",
                            _product_fact_summary(context, "whatsapp_scope"),
                            source="official_product_knowledge",
                            evidence=["product_knowledge.whatsapp_scope"],
                            max_length=320,
                        ),
                        "official_demo_link": _template_value(
                            "url",
                            _official_demo_link(context),
                            source="official_product_knowledge",
                            evidence=["product_knowledge.links"],
                        ),
                    },
                )
            ]
        ),
        direct_question_present=True,
        direct_question_answered_first=True,
    )


def _compile_integration_scope(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
) -> ConductorDecision:
    return _base_decision(
        action_decision,
        context=context,
        role="product",
        route="product",
        previous_state="entry",
        current_state="integration_scope_question",
        next_state="product_question_answered",
        template_plan=RenderPlan(
            items=[
                RenderPlanItem(
                    template_id="product.integration_scope_direct",
                    variables={
                        "integration_topic": _template_value(
                            "short_text",
                            _integration_topic(action_decision),
                            source="user_message",
                            evidence=list(action_decision.evidence),
                            max_length=100,
                        )
                    },
                )
            ]
        ),
        direct_question_present=True,
        direct_question_answered_first=True,
    )


def _compile_diagnostic_offer_after_answer(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
) -> ConductorDecision:
    return _base_decision(
        action_decision,
        context=context,
        role="product",
        route="product",
        previous_state="product_question",
        current_state="product_answered_diagnostic_offer",
        next_state="diagnostic_offered",
        template_plan=RenderPlan(items=[RenderPlanItem(template_id="diagnostic.offer_soft")]),
        direct_question_present=True,
        direct_question_answered_first=True,
        diagnostic_action="offer",
        official_facts_only=False,
    )


def _compile_waitlist_offer_with_context(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
) -> ConductorDecision:
    return _base_decision(
        action_decision,
        context=context,
        role="waitlist",
        route="waitlist",
        previous_state="post_diagnostic",
        current_state="waitlist_offer",
        next_state="waitlist_offered",
        template_plan=RenderPlan(
            items=[
                RenderPlanItem(
                    template_id="waitlist.offer_after_contract_intent",
                    variables={
                        "waitlist_context_summary": _template_value(
                            "long_text",
                            _waitlist_context_summary(action_decision),
                            source="diagnostic_ledger",
                            evidence=_diagnostic_evidence(
                                context,
                                extra=list(action_decision.evidence),
                            ),
                            max_length=220,
                        )
                    },
                )
            ]
        ),
        waitlist_status="offered",
        waitlist_eligibility="eligible",
    )


def _compile_collect_waitlist_missing_detail(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
) -> ConductorDecision:
    missing_details = _waitlist_missing_details(action_decision, context)
    template_id = _waitlist_missing_template(missing_details[0])
    return _base_decision(
        action_decision,
        context=context,
        role="waitlist",
        route="waitlist",
        previous_state="waitlist_offered",
        current_state="waitlist_pending_details",
        next_state="waitlist_pending_details",
        template_plan=RenderPlan(items=[RenderPlanItem(template_id=template_id)]),
        waitlist_status="pending_details",
        waitlist_eligibility="eligible",
        waitlist_missing_details=missing_details,
    )


def _compile_join_waitlist(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
) -> ConductorDecision:
    variables: dict[str, TemplateVariableValue] = {}
    studio_name = _slot_value(action_decision, "studio_name") or _state_value(
        context.waitlist_state,
        "studio_name",
    )
    city_state = _slot_value(action_decision, "city_state") or _state_value(
        context.waitlist_state,
        "city_state",
    )
    if studio_name:
        variables["studio_name"] = _template_value(
            "short_text",
            studio_name,
            source="user_message",
            evidence=_slot_evidence(action_decision, "studio_name"),
            max_length=80,
        )
    if city_state:
        variables["city_state"] = _template_value(
            "short_text",
            city_state,
            source="user_message",
            evidence=_slot_evidence(action_decision, "city_state"),
            max_length=80,
        )
    return _base_decision(
        action_decision,
        context=context,
        role="waitlist",
        route="waitlist",
        previous_state="waitlist_pending_details",
        current_state="waitlist_joined",
        next_state="waitlist_joined",
        template_plan=RenderPlan(
            items=[RenderPlanItem(template_id="waitlist.joined", variables=variables)]
        ),
        waitlist_status="joined",
        waitlist_eligibility="eligible",
    )


def _compile_decline_waitlist(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
) -> ConductorDecision:
    return _base_decision(
        action_decision,
        context=context,
        role="waitlist",
        route="waitlist",
        previous_state="waitlist_offered",
        current_state="waitlist_declined",
        next_state="post_diagnostic",
        template_plan=RenderPlan(items=[RenderPlanItem(template_id="waitlist.status_preserved")]),
        waitlist_status="declined",
        waitlist_eligibility="eligible",
    )


def _compile_answer_question_then_continue_waitlist(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
) -> ConductorDecision:
    missing_details = _waitlist_missing_details(action_decision, context)
    return _base_decision(
        action_decision,
        context=context,
        role="waitlist",
        route="waitlist",
        previous_state="waitlist_pending_details",
        current_state="waitlist_question_answered",
        next_state="waitlist_pending_details",
        template_plan=RenderPlan(
            items=[
                RenderPlanItem(
                    template_id="product.how_it_works_direct",
                    variables={
                        "contextual_next_step": _template_value(
                            "enum",
                            "no_cta",
                            source="model_decision",
                            evidence=list(action_decision.evidence),
                        )
                    },
                ),
                RenderPlanItem(template_id=_waitlist_missing_template(missing_details[0])),
            ]
        ),
        direct_question_present=True,
        direct_question_answered_first=True,
        waitlist_status="pending_details",
        waitlist_eligibility="eligible",
        waitlist_missing_details=missing_details,
    )


def _base_decision(
    action_decision: ConductorActionDecision,
    *,
    context: TurnContext,
    role: str,
    route: str,
    previous_state: str,
    current_state: str,
    next_state: str,
    template_plan: RenderPlan,
    direct_question_present: bool | None = None,
    direct_question_answered_first: bool | None = None,
    diagnostic_action: str = "none",
    ledger_updates: list[DiagnosticLedgerItem] | None = None,
    next_question_key: str | None = None,
    final_fields: dict[str, Any] | None = None,
    demo_status: str = "none",
    demo_next_step: str = "none",
    waitlist_status: str = "none",
    waitlist_eligibility: str = "unknown",
    waitlist_missing_details: list[str] | None = None,
    handoff_status: str = "none",
    handoff_reason: str | None = None,
    official_facts_only: bool = True,
) -> ConductorDecision:
    return ConductorDecision(
        schema_version="011.0",
        turn_id=context.turn_id,
        conversation_id=context.conversation_id,
        channel=context.channel,
        agent_key=context.agent_key,
        role=role,  # type: ignore[arg-type]
        route=route,  # type: ignore[arg-type]
        previous_state=previous_state,
        current_state=current_state,
        next_state=next_state,
        detected_intents=list(action_decision.interpreted_intents),
        direct_question_present=(
            action_decision.direct_question.present
            if direct_question_present is None
            else direct_question_present
        ),
        direct_question_answered_first=(
            action_decision.direct_question.answered_first
            if direct_question_answered_first is None
            else direct_question_answered_first
        ),
        facts=_facts_from_slots(action_decision.captured_slots),
        numeric_interpretations=list(action_decision.numeric_interpretations),
        diagnostic={
            "action": diagnostic_action,
            "ledger_updates": ledger_updates or [],
            "next_question_key": next_question_key,
            "final_fields": final_fields or {},
        },
        demo={"status": demo_status, "next_step": demo_next_step}
        if demo_status != "none"
        else (
            {"status": action_decision.demo_intent.status}
            if action_decision.demo_intent.status
            in {"offered", "viewed_or_asked", "reacted_positive"}
            else {}
        ),
        waitlist={
            "eligibility": waitlist_eligibility,
            "status": waitlist_status,
            "missing_details": waitlist_missing_details or [],
        }
        if waitlist_status != "none"
        else (
            {"status": action_decision.waitlist_intent.status}
            if action_decision.waitlist_intent.status
            in {
                "offered",
                "pending_details",
                "joined",
                "declined",
            }
            else {}
        ),
        handoff={
            "status": handoff_status,
            "reason": handoff_reason,
        }
        if handoff_status != "none"
        else (
            {
                "status": "requested",
                "reason": _handoff_reason(action_decision),
            }
            if action_decision.handoff_intent.status == "requested"
            else {}
        ),
        language_policy=LanguagePolicyDecision(
            register="studio_owner_practical",
            crm_term_policy="avoid_by_default",
        ),
        template_plan=template_plan,
        policy_checks=PolicyChecks(
            direct_question_answered_first=True,
            diagnostic_timing_ok=True,
            waitlist_timing_ok=True,
            official_facts_only=official_facts_only,
            no_internal_text_leak=True,
            no_early_contact_capture=True,
            no_human_overlap=True,
        ),
        confidence=action_decision.confidence,
        repair_hints=list(action_decision.repair_hints),
    )


def _slot_for_key(slots: list[CapturedSlot], key: str) -> CapturedSlot | None:
    return next((slot for slot in slots if slot.key == key), None)


def _ledger_update_from_slot(
    slot: CapturedSlot,
    question_key: DiagnosticQuestionKey,
) -> DiagnosticLedgerItem:
    return DiagnosticLedgerItem(
        question_key=question_key,
        status="answered",
        answer_value=str(slot.value),
        evidence=list(slot.evidence),
        confidence=slot.confidence,
    )


def _facts_from_slots(slots: list[CapturedSlot]) -> list[TurnFact]:
    return [
        TurnFact(
            key=slot.key,
            value=slot.value,
            source="user_message",
            reliability="customer_provided",
            renderable=False,
            confidence=slot.confidence,
            evidence=list(slot.evidence),
        )
        for slot in slots
    ]


def _template_value(
    kind: str,
    value: Any,
    *,
    source: str,
    evidence: list[str],
    max_length: int | None = None,
) -> TemplateVariableValue:
    return TemplateVariableValue(
        kind=kind,  # type: ignore[arg-type]
        value=value,
        source=source,  # type: ignore[arg-type]
        evidence=evidence,
        max_length=max_length,
    )


def _official_price_summary(context: TurnContext) -> str:
    ref = _product_ref(context, "prices")
    if ref is None or ref.value is None:
        raise DecisionCompilerError("price answer requires official prices in context")
    prices = ref.value
    if not isinstance(prices, dict):
        return str(ref.excerpt or prices)
    labels = [str(label) for label in prices.values()]
    return "Planos atuais: " + "; ".join(labels) + "."


def _recommended_plan_or_range(context: TurnContext) -> str:
    ref = _product_ref(context, "plans")
    if ref is None or ref.value is None:
        return "Essencial, Avance ou Completo"
    plans = ref.value
    if not isinstance(plans, list):
        return "Essencial, Avance ou Completo"
    names = [str(plan.get("name")) for plan in plans if isinstance(plan, dict)]
    active_names = [name for name in names if name in {"Essencial", "Avance", "Completo"}]
    return ", ".join(active_names) if active_names else "Essencial, Avance ou Completo"


def _recommended_agent_name(context: TurnContext) -> str:
    ref = _product_ref(context, "plans")
    if ref is None or ref.value is None:
        return "Atendimento"
    plans = ref.value
    if not isinstance(plans, list):
        return "Atendimento"
    for plan in plans:
        if not isinstance(plan, dict):
            continue
        included = plan.get("included_agents")
        if isinstance(included, list) and included:
            return str(included[0])
    return "Atendimento"


def _official_demo_link(context: TurnContext) -> str:
    ref = _product_ref(context, "links")
    if ref is None or ref.value is None:
        raise DecisionCompilerError("demo answer requires official links in context")
    links = ref.value
    if not isinstance(links, dict):
        raise DecisionCompilerError("demo answer requires structured official links")
    demo_link = str(links.get("demonstration") or "").strip()
    if not demo_link:
        raise DecisionCompilerError("demo answer requires official demonstration link")
    return demo_link


def _product_fact_summary(context: TurnContext, key: str) -> str:
    ref = _product_ref(context, key)
    if ref is None or ref.value is None:
        raise DecisionCompilerError(f"product answer requires official {key} in context")
    if key == "whatsapp_scope":
        return (
            "Quando o WhatsApp Business do studio esta conectado, os agentes "
            "podem apoiar conversas e a Taliya atualiza o painel com contexto "
            "da operacao. Os alunos nao precisam baixar aplicativo nem criar "
            "senha: eles seguem falando pelo WhatsApp. Quando algo precisa de "
            "acao ou confirmacao, a Taliya avisa o responsavel."
        )
    return str(ref.excerpt or ref.value)


def _integration_topic(action_decision: ConductorActionDecision) -> str:
    value = action_decision.direct_question.answer_obligations
    detail = action_decision.product_fact_keys_used
    candidate = action_decision.diagnostic_intent.details.get("integration_topic")
    if isinstance(candidate, str) and candidate.strip():
        return candidate.strip()
    candidate = action_decision.direct_question.answer_obligations[0] if value else None
    if candidate:
        return str(candidate)[:100]
    candidate = detail[0] if detail else None
    if candidate:
        return str(candidate)[:100]
    return "essa integracao"


def _plan_fit_context(action_decision: ConductorActionDecision) -> str:
    value = action_decision.diagnostic_intent.details.get("plan_fit_context")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return (
        "Para recomendar plano sem chute, eu preciso entender tamanho, rotina e "
        "prioridade do studio."
    )


def _clarification_question(action_decision: ConductorActionDecision) -> str:
    value = action_decision.diagnostic_intent.details.get("clarification_question")
    if isinstance(value, str) and value.strip():
        return value.strip()
    value = action_decision.waitlist_intent.details.get("clarification_question")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return "Voce quer entender a Taliya, tirar uma duvida especifica ou fazer o diagnostico?"


def _clarification_for_diagnostic_key(question_key: str) -> str:
    questions = {
        "active_students_or_size": "Hoje seu studio tem aproximadamente quantos alunos ativos?",
        "main_pain": (
            "Qual dessas areas pesa mais hoje: WhatsApp, agenda, vendas, "
            "financeiro ou acompanhamento?"
        ),
        "pain_detail": "Hoje voce consegue ver facilmente o que precisa ser resolvido no dia?",
        "current_process": "Isso fica em sistema, WhatsApp, planilha ou caderno?",
        "priority": "Qual tarefa voce mais quer deixar mais leve primeiro?",
        "urgency": "Voces querem resolver isso agora ou estao so pesquisando por enquanto?",
    }
    return questions.get(question_key, "Pode me responder esse ponto de um jeito mais direto?")


def _demo_status_for_reaction(context: TurnContext) -> str:
    status = str(context.demo_state.get("status") or "offered")
    if status in {"offered", "viewed_or_asked", "reacted_positive"}:
        return status
    return "offered"


def _waitlist_missing_details(
    action_decision: ConductorActionDecision,
    context: TurnContext,
) -> list[str]:
    details = action_decision.waitlist_intent.details.get("missing_details")
    if isinstance(details, list):
        normalized = [str(item) for item in details if str(item) in _WAITLIST_DETAIL_TEMPLATES]
        if normalized:
            return normalized
    state_details = context.waitlist_state.get("missing_details") or context.waitlist_state.get(
        "missing_fields"
    )
    if isinstance(state_details, list):
        normalized = [
            str(item) for item in state_details if str(item) in _WAITLIST_DETAIL_TEMPLATES
        ]
        if normalized:
            return normalized
    if context.channel == "whatsapp":
        return ["studio_name", "city_state"]
    return ["studio_name", "city_state", "contact_path"]


_WAITLIST_DETAIL_TEMPLATES = {
    "studio_name": "waitlist.ask_missing_studio",
    "city_state": "waitlist.ask_missing_city",
    "contact_path": "waitlist.ask_missing_contact_path",
}


def _waitlist_missing_template(detail: str) -> str:
    try:
        return _WAITLIST_DETAIL_TEMPLATES[detail]
    except KeyError as error:
        raise DecisionCompilerError(f"unsupported waitlist missing detail: {detail}") from error


def _slot_value(action_decision: ConductorActionDecision, key: str) -> str | None:
    slot = _slot_for_key(action_decision.captured_slots, key)
    if slot is None:
        return None
    value = str(slot.value).strip()
    return value or None


def _slot_evidence(action_decision: ConductorActionDecision, key: str) -> list[str]:
    slot = _slot_for_key(action_decision.captured_slots, key)
    if slot is not None and slot.evidence:
        return list(slot.evidence)
    return list(action_decision.evidence)


def _state_value(state: dict[str, Any], key: str) -> str | None:
    value = state.get(key)
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _handoff_reason(action_decision: ConductorActionDecision) -> str:
    value = action_decision.handoff_intent.details.get("reason")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return "pedido do lead para falar com uma pessoa"


def _waitlist_context_summary(action_decision: ConductorActionDecision) -> str:
    value = action_decision.waitlist_intent.details.get("context_summary")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return (
        "Como ja existe contexto comercial suficiente, o proximo passo seguro e "
        "registrar o interesse na lista de espera da Taliya."
    )


def _product_ref(context: TurnContext, key: str):
    return next(
        (
            ref
            for ref in context.product_knowledge
            if ref.key == key and not ref.missing
        ),
        None,
    )


def _diagnostic_text(
    action_decision: ConductorActionDecision,
    key: str,
    fallback: str,
) -> str:
    value = action_decision.diagnostic_intent.details.get(key)
    if isinstance(value, str) and value.strip():
        return value.strip()
    return fallback


def _required_diagnostic_text(
    action_decision: ConductorActionDecision,
    key: str,
) -> str:
    value = action_decision.diagnostic_intent.details.get(key)
    if isinstance(value, str) and value.strip():
        return value.strip()
    raise DecisionCompilerError(f"action requires diagnostic_intent.details.{key}")


def _diagnostic_evidence(context: TurnContext, *, extra: list[str]) -> list[str]:
    evidence = [
        str(value)
        for item in context.diagnostic_ledger
        if item
        for value in (item.get("evidence") or [item.get("question_key")])
    ]
    evidence.extend(extra)
    compact: list[str] = []
    for item in evidence:
        if not item or item in compact:
            continue
        compact.append(item if len(item) <= 180 else item[:180])
    return compact or ["diagnostic_ledger"]


def _feedback_for_slot(slot: CapturedSlot) -> str:
    value = str(slot.value).strip()
    if not value:
        return "Entendi esse ponto."
    return f"Entendi: {value}."
