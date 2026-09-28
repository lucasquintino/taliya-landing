"""T012-030B tests: deterministic Turn Situation Builder."""

from __future__ import annotations

import inspect

from app.core.taliya_commercial_sdk.conductor_decision import ACTION_MENU_BY_MODE
from app.core.taliya_commercial_sdk.turn_situation import (
    TurnSituation,
    build_turn_situation,
)


def test_builder_signature_has_no_lead_text_parameter() -> None:
    """Structural anti-drift proof: the board is built from state only.

    Interpreting raw lead text here is the forbidden pattern from
    011/action-contract.md; the builder cannot do it because it never
    receives the message.
    """

    parameters = inspect.signature(build_turn_situation).parameters
    forbidden_names = {"text", "user_text", "message", "inbound", "lead_text"}
    assert not (forbidden_names & set(parameters))


def test_empty_state_is_entry_mode_first_contact() -> None:
    situation = build_turn_situation(state_snapshot={}, channel="whatsapp")

    assert situation.mode == "entry"
    assert situation.allowed_actions == ACTION_MENU_BY_MODE["entry"]
    assert situation.pending_question_key is None
    assert situation.missing_diagnostic_keys == (
        "active_students_or_size",
        "main_pain",
        "pain_detail",
        "current_process",
        "priority",
        "urgency",
    )
    assert situation.llm_turn_allowed is True
    assert "first contact" in situation.to_preamble()


def test_diagnostic_in_progress_pending_key_and_completion_gate() -> None:
    snapshot = {
        "diagnostic": {
            "status": "in_progress",
            "ledger": {
                "active_students_or_size": {"status": "answered", "answer_value": "120"},
                "main_pain": {"status": "answered", "answer_value": "perde leads"},
            },
        },
    }
    situation = build_turn_situation(state_snapshot=snapshot, channel="whatsapp")

    assert situation.mode == "diagnostic"
    assert situation.pending_question_key == "pain_detail"
    assert situation.completed_diagnostic_keys == (
        "active_students_or_size",
        "main_pain",
    )
    # More than one key missing: completion is structurally off the menu.
    assert "complete_diagnostic" not in situation.allowed_actions
    assert "complete_diagnostic" in situation.forbidden_actions_now
    assert any("resume the pending" in item for item in situation.required_obligations)
    assert "pending diagnostic question: pain_detail" in situation.to_preamble()


def test_diagnostic_last_key_pending_allows_completion() -> None:
    ledger = {
        key: {"status": "answered", "answer_value": "x"}
        for key in (
            "active_students_or_size",
            "main_pain",
            "pain_detail",
            "current_process",
            "priority",
        )
    }
    snapshot = {"diagnostic": {"status": "in_progress", "ledger": ledger}}
    situation = build_turn_situation(state_snapshot=snapshot, channel="whatsapp")

    assert situation.pending_question_key == "urgency"
    assert "complete_diagnostic" in situation.allowed_actions


def test_operational_precedence_over_canonical_state() -> None:
    # Human handoff outranks everything commercial.
    handoff = build_turn_situation(
        state_snapshot={
            "canonical_state": "diagnostic_in_progress",
            "human_status": "active",
        },
        channel="whatsapp",
    )
    assert handoff.mode == "handoff"
    assert handoff.allowed_actions == ACTION_MENU_BY_MODE["handoff"]
    assert handoff.llm_turn_allowed is False

    # Delivery in flight: defer, no LLM turn at all.
    deferred = build_turn_situation(
        state_snapshot={
            "canonical_state": "price_question",
            "delivery": {"status": "delivering", "chunks_remaining": 2},
        },
        channel="whatsapp",
    )
    assert deferred.mode == "delivery_deferred"
    assert deferred.allowed_actions == ()
    assert deferred.llm_turn_allowed is False

    safety = build_turn_situation(
        state_snapshot={"safety_blocked": True}, channel="widget"
    )
    assert safety.mode == "safety"
    assert safety.llm_turn_allowed is False


def test_completed_diagnostic_operational_state_overrides_stale_entry_state() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "diagnostic_offered",
            "diagnostic": {
                "status": "delivered",
                "ledger": {
                    "active_students_or_size": {"status": "answered"},
                    "main_pain": {"status": "answered"},
                    "pain_detail": {"status": "answered"},
                    "current_process": {"status": "answered"},
                    "priority": {"status": "answered"},
                    "urgency": {"status": "answered"},
                },
            },
        },
        channel="whatsapp",
    )

    assert situation.mode == "post_diagnostic"
    assert "offer_or_join_waitlist_if_eligible" in situation.allowed_actions
    assert "start_requested_diagnostic" not in situation.allowed_actions
    assert any("never restart" in item for item in situation.state_constraints)


def test_waitlist_operational_state_overrides_completed_diagnostic_state() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "diagnostic_delivered",
            "diagnostic": {"status": "delivered", "ledger": {}},
            "waitlist": {"status": "offered"},
        },
        channel="whatsapp",
    )

    assert situation.mode == "waitlist"
    assert situation.allowed_actions == ACTION_MENU_BY_MODE["waitlist"]


def test_canonical_states_map_to_modes() -> None:
    for canonical, expected_mode in (
        ("price_question", "price"),
        ("product_question", "product"),
        ("demo_question", "demo"),
        ("diagnostic_delivered", "post_diagnostic"),
        ("buying_intent_detected", "waitlist"),
        ("waitlist_offered", "waitlist"),
        ("greeting_only", "entry"),
    ):
        situation = build_turn_situation(
            state_snapshot={"canonical_state": canonical}, channel="whatsapp"
        )
        assert situation.mode == expected_mode, canonical
        assert situation.allowed_actions == ACTION_MENU_BY_MODE[expected_mode]


def test_post_diagnostic_with_joined_waitlist_blocks_reoffer() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "waitlist_joined",
            "waitlist": {"status": "joined"},
            "diagnostic": {"status": "complete", "ledger": {}},
        },
        channel="whatsapp",
    )

    assert situation.mode == "post_diagnostic"
    assert "offer_or_join_waitlist_if_eligible" not in situation.allowed_actions
    assert "offer_or_join_waitlist_if_eligible" in situation.forbidden_actions_now
    assert any("never restart" in item for item in situation.state_constraints)


def test_post_diagnostic_preamble_carries_compact_delta_context() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "diagnostic_delivered",
            "diagnostic": {
                "status": "completed",
                "pain_context_human": "interessados ficam sem retorno claro",
                "likely_cause": "controle manual sem fila de proximas acoes",
                "first_recommended_step": "organizar atendimento e follow-up",
                "indicated_agents": ["Atendimento", "Vendas"],
                "recommended_plan_or_range": "Essencial",
                "unknowns": ["volume de reposicoes"],
            },
            "demo": {"status": "offered"},
            "waitlist": {"status": "none"},
        },
        channel="whatsapp",
    )

    preamble = situation.to_preamble()

    assert situation.mode == "post_diagnostic"
    assert situation.post_diagnostic_context == {
        "pain_context_human": "interessados ficam sem retorno claro",
        "likely_cause": "controle manual sem fila de proximas acoes",
        "first_recommended_step": "organizar atendimento e follow-up",
        "recommended_area": "organizar atendimento e follow-up",
        "indicated_agents": ["Atendimento", "Vendas"],
        "recommended_plan_or_range": "Essencial",
        "demo_status": "offered",
        "waitlist_status": "none",
        "unknowns": ["volume de reposicoes"],
    }
    assert "post_diagnostic_context:" in preamble
    assert "interessados ficam sem retorno claro" in preamble
    assert "Essencial" in preamble


def test_profile_name_context_marks_reliable_and_unreliable_names() -> None:
    reliable = build_turn_situation(
        state_snapshot={
            "canonical_state": "new_lead",
            "channel_metadata": {"profile_name": "Lucas Alves"},
        },
        channel="whatsapp",
    )
    unreliable = build_turn_situation(
        state_snapshot={
            "canonical_state": "new_lead",
            "channel_metadata": {"profile_name": "Studio Vida Pilates"},
        },
        channel="whatsapp",
    )

    assert reliable.profile_name_context == {
        "usage": "used_reliable_name",
        "first_name": "Lucas",
    }
    assert unreliable.profile_name_context["usage"] == "ignored_unreliable_name"
    assert "profile_name_policy:" in reliable.to_preamble()
    assert "Studio Vida Pilates" not in unreliable.to_preamble()


def test_preamble_carries_compact_memory() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "diagnostic_in_progress",
            "summary": "Lead com studio de 120 alunos, perde leads no WhatsApp.",
            "answered_obligations": ["quanto custa?"],
            "diagnostic": {
                "status": "in_progress",
                "ledger": {
                    "active_students_or_size": {
                        "status": "answered",
                        "answer_value": "120",
                    }
                },
            },
        },
        channel="whatsapp",
    )
    preamble = situation.to_preamble()

    assert "mode: diagnostic" in preamble
    assert "120 alunos" in preamble
    assert "quanto custa?" in preamble
    assert "allowed actions:" in preamble
    assert isinstance(situation, TurnSituation)
