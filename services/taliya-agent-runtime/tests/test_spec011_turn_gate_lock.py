from __future__ import annotations

from dataclasses import asdict, fields
from datetime import UTC, datetime, timedelta

import pytest

from app.core.taliya_commercial.turn_gate import ConversationLockManager, TurnLockResult


class FakeClock:
    def __init__(self) -> None:
        self.current = datetime(2026, 5, 30, 12, 0, tzinfo=UTC)

    def now(self) -> datetime:
        return self.current

    def advance(self, *, seconds: int) -> None:
        self.current += timedelta(seconds=seconds)


def test_conversation_lock_allows_one_active_turn_per_conversation() -> None:
    clock = FakeClock()
    manager = ConversationLockManager(now=clock.now, ttl_seconds=30)

    first = manager.acquire(conversation_id="conv_1", owner_id="turn_a")
    second = manager.acquire(conversation_id="conv_1", owner_id="turn_b")

    assert first.status == "acquired"
    assert first.owner_id == "turn_a"
    assert first.expires_at == clock.now() + timedelta(seconds=30)
    assert second.status == "busy"
    assert second.active_owner_id == "turn_a"
    assert second.retry_after_seconds == 30.0

    released = manager.release(conversation_id="conv_1", owner_id="turn_a")
    reacquired = manager.acquire(conversation_id="conv_1", owner_id="turn_b")

    assert released.status == "released"
    assert reacquired.status == "acquired"
    assert reacquired.owner_id == "turn_b"


def test_conversation_lock_is_scoped_by_conversation() -> None:
    clock = FakeClock()
    manager = ConversationLockManager(now=clock.now, ttl_seconds=30)

    first = manager.acquire(conversation_id="conv_1", owner_id="turn_a")
    second = manager.acquire(conversation_id="conv_2", owner_id="turn_b")

    assert first.status == "acquired"
    assert second.status == "acquired"
    assert second.conversation_id == "conv_2"
    assert second.owner_id == "turn_b"


def test_release_requires_lock_owner_and_preserves_active_lock() -> None:
    clock = FakeClock()
    manager = ConversationLockManager(now=clock.now, ttl_seconds=30)
    manager.acquire(conversation_id="conv_1", owner_id="turn_a")

    wrong_owner = manager.release(conversation_id="conv_1", owner_id="turn_b")
    still_busy = manager.acquire(conversation_id="conv_1", owner_id="turn_c")

    assert wrong_owner.status == "not_owner"
    assert wrong_owner.active_owner_id == "turn_a"
    assert still_busy.status == "busy"
    assert still_busy.active_owner_id == "turn_a"


def test_expired_lock_can_be_reacquired_without_commercial_logic() -> None:
    clock = FakeClock()
    manager = ConversationLockManager(now=clock.now, ttl_seconds=30)
    manager.acquire(conversation_id="conv_1", owner_id="turn_a")

    clock.advance(seconds=31)
    reacquired = manager.acquire(conversation_id="conv_1", owner_id="turn_b")

    assert reacquired.status == "acquired"
    assert reacquired.owner_id == "turn_b"
    assert reacquired.active_owner_id is None


def test_lock_rejects_empty_operational_keys() -> None:
    manager = ConversationLockManager()

    with pytest.raises(ValueError, match="conversation_id"):
        manager.acquire(conversation_id=" ", owner_id="turn_a")

    with pytest.raises(ValueError, match="owner_id"):
        manager.release(conversation_id="conv_1", owner_id="")


def test_lock_result_has_only_operational_fields() -> None:
    result_field_names = {field.name for field in fields(TurnLockResult)}
    forbidden_decision_fields = {
        "route",
        "intent",
        "template_id",
        "diagnostic_action",
        "price",
        "demo",
        "message_text",
    }

    result = TurnLockResult(status="acquired", conversation_id="conv_1", owner_id="turn_a")

    assert forbidden_decision_fields.isdisjoint(result_field_names)
    assert forbidden_decision_fields.isdisjoint(asdict(result))
