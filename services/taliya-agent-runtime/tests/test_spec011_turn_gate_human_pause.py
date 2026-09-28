from __future__ import annotations

from dataclasses import asdict, fields
from datetime import UTC, datetime

from app.core.taliya_commercial.turn_gate import (
    HumanPauseDecision,
    HumanPauseManager,
    HumanPauseState,
    InMemoryHumanPauseStore,
)


def test_human_pause_suppresses_ai_reply_but_preserves_inbound_persistence() -> None:
    manager = HumanPauseManager(now=lambda: datetime(2026, 5, 30, 12, 0, tzinfo=UTC))

    state = manager.pause(conversation_id="conv_1", reason="operator took over")
    decision = manager.evaluate(conversation_id="conv_1")

    assert state.status == "paused_by_human"
    assert decision.action == "suppress_ai_reply"
    assert decision.ai_reply_allowed is False
    assert decision.persist_inbound is True
    assert decision.requires_explicit_resume is True
    assert decision.reason == "operator took over"


def test_human_handoff_and_active_statuses_are_blocking() -> None:
    store = InMemoryHumanPauseStore()
    manager = HumanPauseManager(store=store)

    for status in ("active", "human_active", "human_handoff", "paused_by_human"):
        store.set(
            HumanPauseState(
                conversation_id=f"conv_{status}",
                status=status,
                reason=f"{status} reason",
            )
        )

        decision = manager.evaluate(conversation_id=f"conv_{status}")

        assert decision.action == "suppress_ai_reply"
        assert decision.ai_reply_allowed is False
        assert decision.persist_inbound is True
        assert decision.requires_explicit_resume is True


def test_resume_releases_pause_only_after_explicit_operator_action() -> None:
    manager = HumanPauseManager(now=lambda: datetime(2026, 5, 30, 12, 0, tzinfo=UTC))
    manager.pause(conversation_id="conv_1", reason="operator took over")

    paused = manager.evaluate(conversation_id="conv_1")
    resumed_state = manager.resume(conversation_id="conv_1")
    resumed = manager.evaluate(conversation_id="conv_1")

    assert paused.action == "suppress_ai_reply"
    assert resumed_state.status == "resumed"
    assert resumed.action == "continue"
    assert resumed.ai_reply_allowed is True
    assert resumed.persist_inbound is True
    assert resumed.requires_explicit_resume is False


def test_default_state_allows_turn_to_continue() -> None:
    manager = HumanPauseManager()

    decision = manager.evaluate(conversation_id="conv_1")

    assert decision.action == "continue"
    assert decision.ai_reply_allowed is True
    assert decision.persist_inbound is True


def test_unknown_human_status_fails_closed_without_ai_reply() -> None:
    store = InMemoryHumanPauseStore()
    store.set(HumanPauseState(conversation_id="conv_1", status="mystery"))
    manager = HumanPauseManager(store=store)

    decision = manager.evaluate(conversation_id="conv_1")

    assert decision.action == "suppress_ai_reply"
    assert decision.ai_reply_allowed is False
    assert decision.persist_inbound is True
    assert decision.requires_explicit_resume is True
    assert decision.reason == "unsupported_human_status:mystery"


def test_human_pause_result_has_only_operational_fields() -> None:
    state_field_names = {field.name for field in fields(HumanPauseState)}
    decision_field_names = {field.name for field in fields(HumanPauseDecision)}
    forbidden_decision_fields = {
        "route",
        "intent",
        "template_id",
        "diagnostic_action",
        "price",
        "demo",
        "message_text",
        "user_text",
        "text",
    }
    decision = HumanPauseDecision(
        action="continue",
        conversation_id="conv_1",
        human_status="none",
        ai_reply_allowed=True,
    )

    assert forbidden_decision_fields.isdisjoint(state_field_names)
    assert forbidden_decision_fields.isdisjoint(decision_field_names)
    assert forbidden_decision_fields.isdisjoint(asdict(decision))
