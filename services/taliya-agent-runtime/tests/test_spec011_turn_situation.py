from __future__ import annotations

from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.turn_situation import (
    TurnSituation,
    build_turn_situation,
)
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState


def _request(text: str = "quero resolver agora") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {
                "conversation_id": "conv_turn_situation",
                "lead_id": "lead_turn_situation",
                "channel_conversation_id": "widget_thread_1",
                "source": "pilates_landing",
                "entry_intent": "site_cta",
            },
            "message": {
                "idempotency_key": f"widget:conv_turn_situation:{hash(text)}",
                "channel_message_id": f"msg:{hash(text)}",
                "type": "text",
                "text": text,
                "timestamp": "2026-06-04T12:00:00Z",
            },
            "sender": {"name": "Ana"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _diagnostic_state(
    *,
    status: str = "in_progress",
    answered_keys: tuple[str, ...] = (
        "active_students_or_size",
        "main_pain",
        "pain_detail",
        "current_process",
        "priority",
    ),
) -> RuntimeState:
    ledger = [
        {
            "question_key": question_key,
            "status": "answered",
            "answer_value": f"answer:{question_key}",
            "evidence": [f"evidence:{question_key}"],
            "confidence": "high",
            "may_ask_again": False,
        }
        for question_key in answered_keys
    ]
    return RuntimeState(
        conversation_id="conv_turn_situation",
        agent_key="taliya_commercial",
        current_agent_name="taliya_commercial_spec011_diagnostic_agent",
        diagnostic={"status": status, "ledger": ledger},
        waitlist={"status": "none"},
        demo={"status": "not_offered"},
        human_status="none",
    )


def _context(text: str, state: RuntimeState | None = None):
    return build_turn_context(
        turn_id="turn_situation_1",
        request=_request(text),
        state=state,
        recent_events=[],
        product_knowledge_keys=["prices", "links", "how_it_works"],
        spec006_contract_keys=["product_positioning"],
    )


def _signature(situation: TurnSituation) -> tuple[object, ...]:
    return (
        situation.mode,
        situation.pending_question_key,
        tuple(situation.completed_diagnostic_keys),
        tuple(situation.missing_diagnostic_keys),
        tuple(situation.allowed_actions),
        tuple(situation.required_obligations),
        tuple(situation.eligible_template_groups),
        tuple(situation.forbidden_actions_now),
    )


def test_turn_situation_builds_pending_diagnostic_board_from_state() -> None:
    situation = build_turn_situation(
        _context("quero resolver agora", _diagnostic_state())
    )

    assert situation.schema_version == "011.turn_situation.v1"
    assert situation.mode == "diagnostic"
    assert situation.pending_question_key == "urgency"
    assert situation.completed_diagnostic_keys == [
        "active_students_or_size",
        "main_pain",
        "pain_detail",
        "current_process",
        "priority",
    ]
    assert situation.missing_diagnostic_keys == ["urgency"]
    assert "capture_pending_diagnostic_answer" in situation.allowed_actions
    assert "complete_diagnostic_if_pending_answer_is_captured" in (
        situation.required_obligations
    )
    assert "diagnostic_completion" in situation.eligible_template_groups
    assert "prices" in situation.official_fact_keys_available


def test_turn_situation_does_not_change_commercial_action_menu_from_raw_text_keywords() -> None:
    state = _diagnostic_state()
    baseline = build_turn_situation(_context("quero resolver agora", state))

    for text in (
        "me manda demo",
        "achei caro",
        "quero comecar, me coloca na lista",
        "como funciona mesmo?",
        "vim pelo Instagram e quero preco",
    ):
        situation = build_turn_situation(_context(text, state))
        assert _signature(situation) == _signature(baseline)


def test_completed_diagnostic_enters_post_diagnostic_mode_without_reopening_questions() -> None:
    state = _diagnostic_state(
        status="completed",
        answered_keys=(
            "active_students_or_size",
            "main_pain",
            "pain_detail",
            "current_process",
            "priority",
            "urgency",
        ),
    )

    situation = build_turn_situation(_context("como funciona mesmo?", state))

    assert situation.mode == "post_diagnostic"
    assert situation.pending_question_key is None
    assert situation.missing_diagnostic_keys == []
    assert "answer_product_question_with_saved_context" in situation.allowed_actions
    assert "preserve_completed_diagnostic_context" in situation.required_obligations
    assert "completed_diagnostic_must_not_be_reopened_without_llm_reason" in (
        situation.state_constraints
    )


def test_handoff_active_allows_only_handoff_mode_actions() -> None:
    state = _diagnostic_state()
    state.human_status = "active"
    state.human_reason = "operator took over"

    situation = build_turn_situation(_context("ainda estou aqui", state))

    assert situation.mode == "handoff"
    assert situation.allowed_actions == [
        "pause_for_human",
        "resume_only_with_explicit_resume_event",
        "suppress_ai_reply_while_human_active",
    ]
    assert "human_active_blocks_ai_commercial_reply" in situation.required_obligations
    assert "answer_price" in situation.forbidden_actions_now


def test_entry_mode_still_keeps_llm_available_for_commercial_interpretation() -> None:
    situation = build_turn_situation(_context("quanto custa?", None))

    assert situation.mode == "entry"
    assert "answer_direct_product_question" in situation.allowed_actions
    assert "offer_diagnostic_from_pain" in situation.allowed_actions
    assert "llm_must_interpret_latest_inbound" in situation.required_obligations
    assert "join_waitlist" in situation.forbidden_actions_now
