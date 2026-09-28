"""T012-030A tests: ConductorActionDecision schema and per-mode action menus."""

from __future__ import annotations

import typing

import pytest
from agents import AgentOutputSchema
from pydantic import ValidationError

from app.core.taliya_commercial_sdk.conductor_decision import (
    ACTION_MENU_BY_MODE,
    ConductorActionDecision,
    TurnAction,
    composition_variable_names,
    validate_action_decision,
)


def _decision(**overrides) -> ConductorActionDecision:
    payload = {
        "selected_action": "answer_price",
        "interpreted_intents": ["price"],
        "direct_question": "quanto custa?",
        "evidence": ["inbound.text"],
        **overrides,
    }
    return ConductorActionDecision.model_validate(payload)


def test_conductor_decision_is_strict_sdk_output_compatible() -> None:
    AgentOutputSchema(ConductorActionDecision)


def test_conductor_decision_rejects_superseded_boundary_fields() -> None:
    # The pre-T011-105 boundary (model emitting template plans, states, or
    # final text) must be unrepresentable.
    for forbidden in (
        {"template_plan": {"template_ids": ["product.price_direct"]}},
        {"template_ids": ["product.price_direct"]},
        {"current_state": "price_question"},
        {"next_state": "diagnostic_offered"},
        {"final_text": "Oi!"},
        {"assistant_reply": "Oi!"},
        {"state_patch_proposal": {}},
    ):
        with pytest.raises(ValidationError):
            _decision(**forbidden)


def test_conductor_decision_rejects_invented_actions_and_slot_keys() -> None:
    with pytest.raises(ValidationError):
        _decision(selected_action="send_checkout_link")
    with pytest.raises(ValidationError):
        _decision(captured_slots=[{"key": "diagnostic_cta", "value_text": "x", "evidence": ["e"]}])
    with pytest.raises(ValidationError):
        _decision(product_fact_keys_used=["how_it_works_direct"])


def test_action_menus_preserve_011_contract_with_012_delta_actions() -> None:
    assert ACTION_MENU_BY_MODE["entry"] == (
        "answer_general_interest",
        "answer_source_opening",
        "offer_diagnostic_from_pain",
        "answer_direct_product_question",
        "start_requested_diagnostic",
        "handoff_requested",
        "clarify_ambiguous_opening",
    )
    assert ACTION_MENU_BY_MODE["diagnostic"] == (
        "capture_pending_diagnostic_answer",
        "answer_direct_question_then_continue_diagnostic",
        "ask_next_diagnostic_question",
        "complete_diagnostic",
        "clarify_ambiguous_diagnostic_answer",
        "respect_diagnostic_refusal",
        "handoff_requested",
    )
    assert ACTION_MENU_BY_MODE["post_diagnostic"] == (
        "answer_product_question_with_saved_context",
        "send_demo",
        "answer_price_objection_with_context",
        "offer_or_join_waitlist_if_eligible",
        "handoff_requested",
        "ask_demo_reaction",
        "clarify_ambiguous_followup",
    )
    for mode in ("product", "price", "demo"):
        assert ACTION_MENU_BY_MODE[mode] == (
            "answer_price",
            "answer_plan_fit_with_diagnostic_offer",
            "answer_how_it_works",
            "answer_whatsapp_scope",
            "answer_integration_scope_safely",
            "answer_comparison_current_tool",
            "answer_security_and_data",
            "answer_availability_and_onboarding",
            "answer_out_of_profile",
            "send_demo",
            "answer_price_objection",
            "offer_diagnostic_after_answer",
            "clarify_product_question",
            "handoff_requested",
        )
    assert ACTION_MENU_BY_MODE["waitlist"] == (
        "offer_waitlist",
        "collect_waitlist_missing_detail",
        "join_waitlist",
        "decline_waitlist",
        "pause_waitlist_decision",
        "answer_question_then_continue_waitlist",
        "handoff_requested",
    )
    assert ACTION_MENU_BY_MODE["handoff"] == (
        "pause_for_human",
        "resume_only_with_explicit_resume_event",
        "suppress_ai_reply_while_human_active",
    )
    # Operational modes never call the LLM (allowed determinism).
    assert ACTION_MENU_BY_MODE["safety"] == ()
    assert ACTION_MENU_BY_MODE["delivery_deferred"] == ()


def test_turn_action_literal_and_menus_are_consistent() -> None:
    literal_actions = set(typing.get_args(TurnAction))
    menu_actions = {action for menu in ACTION_MENU_BY_MODE.values() for action in menu}
    assert menu_actions == literal_actions


def test_composition_set_excludes_official_only_variables() -> None:
    composable = composition_variable_names()
    # Model composes prose grounded in lead context / ledger.
    assert "answer_feedback" in composable
    assert "pain_context_human" in composable
    assert "crm_base_recommendation" in composable  # diagnostic_ledger allowed
    # Official-only variables are compiler-owned, never model-composed.
    assert "recommended_plan_or_range" not in composable
    assert "official_demo_link" not in composable


def test_validate_action_decision_form_checks() -> None:
    decision = _decision()
    assert validate_action_decision(decision, allowed_actions=ACTION_MENU_BY_MODE["price"]) == []

    wrong_menu = validate_action_decision(decision, allowed_actions=ACTION_MENU_BY_MODE["handoff"])
    assert "conductor_action_not_in_allowed_menu" in wrong_menu

    bad_composition = _decision(
        composition_variables=[
            {"name": "recommended_plan_or_range", "value": "Essencial", "evidence": ["x"]},
            {"name": "answer_feedback", "value": "Entendi.", "evidence": []},
        ]
    )
    issues = validate_action_decision(bad_composition, allowed_actions=ACTION_MENU_BY_MODE["price"])
    assert any(
        issue.startswith("conductor_composition_variable_not_composable") for issue in issues
    )
    assert any(
        issue.startswith("conductor_composition_variable_missing_evidence") for issue in issues
    )

    confused = _decision(needs_clarification=True)
    issues2 = validate_action_decision(confused, allowed_actions=ACTION_MENU_BY_MODE["price"])
    assert "conductor_clarification_flag_without_clarify_action" in issues2
