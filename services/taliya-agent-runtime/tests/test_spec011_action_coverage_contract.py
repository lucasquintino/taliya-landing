from __future__ import annotations

from typing import get_args

from app.core.taliya_commercial.turn_situation import TurnAction

COMPILED_ACTIONS = {
    "answer_general_interest",
    "answer_source_opening",
    "offer_diagnostic_from_pain",
    "answer_direct_product_question",
    "start_requested_diagnostic",
    "handoff_requested",
    "clarify_ambiguous_opening",
    "answer_price",
    "capture_pending_diagnostic_answer",
    "answer_direct_question_then_continue_diagnostic",
    "ask_next_diagnostic_question",
    "complete_diagnostic",
    "clarify_ambiguous_diagnostic_answer",
    "respect_diagnostic_refusal",
    "send_demo",
    "answer_product_question_with_saved_context",
    "answer_price_objection_with_context",
    "offer_or_join_waitlist_if_eligible",
    "ask_demo_reaction",
    "clarify_ambiguous_followup",
    "answer_plan_fit_with_diagnostic_offer",
    "answer_how_it_works",
    "answer_whatsapp_scope",
    "answer_integration_scope_safely",
    "answer_price_objection",
    "offer_diagnostic_after_answer",
    "clarify_product_question",
    "offer_waitlist",
    "collect_waitlist_missing_detail",
    "join_waitlist",
    "decline_waitlist",
    "answer_question_then_continue_waitlist",
}

OPERATIONALLY_HANDLED_ACTIONS = {
    "pause_for_human",
    "resume_only_with_explicit_resume_event",
    "suppress_ai_reply_while_human_active",
}


def test_every_allowed_action_has_an_explicit_coverage_classification() -> None:
    allowed_actions = set(get_args(TurnAction))
    classified_actions = COMPILED_ACTIONS | OPERATIONALLY_HANDLED_ACTIONS

    assert classified_actions == allowed_actions


def test_paid_readiness_is_blocked_until_no_compiler_actions_are_pending() -> None:
    assert COMPILED_ACTIONS.isdisjoint(OPERATIONALLY_HANDLED_ACTIONS)
