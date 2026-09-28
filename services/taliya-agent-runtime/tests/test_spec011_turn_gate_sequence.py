from __future__ import annotations

from dataclasses import asdict, fields
from datetime import UTC, datetime

import pytest

from app.core.taliya_commercial.turn_gate import (
    InboundSequenceInput,
    InboundSequenceManager,
    InboundSequenceResult,
)


def test_unique_inbound_messages_get_monotonic_sequence_numbers_per_conversation() -> None:
    manager = InboundSequenceManager(now=lambda: datetime(2026, 5, 30, 12, 0, tzinfo=UTC))

    first = manager.assign(
        InboundSequenceInput(conversation_id="conv_1", idempotency_key="inbound:a"),
        turn_id="turn_1",
    )
    second = manager.assign(
        InboundSequenceInput(conversation_id="conv_1", idempotency_key="inbound:b"),
        turn_id="turn_2",
    )

    assert first.status == "assigned"
    assert first.sequence_number == 1
    assert first.accepted_turn_id == "turn_1"
    assert second.status == "assigned"
    assert second.sequence_number == 2
    assert second.accepted_turn_id == "turn_2"


def test_duplicate_inbound_keeps_original_sequence_and_does_not_advance_counter() -> None:
    manager = InboundSequenceManager(now=lambda: datetime(2026, 5, 30, 12, 0, tzinfo=UTC))
    first = manager.assign(
        InboundSequenceInput(conversation_id="conv_1", idempotency_key="inbound:a"),
        turn_id="turn_1",
    )

    duplicate = manager.assign(
        InboundSequenceInput(conversation_id="conv_1", idempotency_key="inbound:a"),
        turn_id="turn_retry",
    )
    next_unique = manager.assign(
        InboundSequenceInput(conversation_id="conv_1", idempotency_key="inbound:b"),
        turn_id="turn_2",
    )

    assert duplicate.status == "duplicate"
    assert duplicate.sequence_number == first.sequence_number
    assert duplicate.duplicate_of_turn_id == "turn_1"
    assert duplicate.accepted_turn_id is None
    assert next_unique.status == "assigned"
    assert next_unique.sequence_number == 2


def test_sequence_numbers_are_scoped_by_conversation() -> None:
    manager = InboundSequenceManager(now=lambda: datetime(2026, 5, 30, 12, 0, tzinfo=UTC))

    first_conversation = manager.assign(
        InboundSequenceInput(conversation_id="conv_1", idempotency_key="inbound:a"),
        turn_id="turn_1",
    )
    second_conversation = manager.assign(
        InboundSequenceInput(conversation_id="conv_2", idempotency_key="inbound:a"),
        turn_id="turn_2",
    )

    assert first_conversation.sequence_number == 1
    assert second_conversation.sequence_number == 1
    assert second_conversation.conversation_id == "conv_2"


def test_sequence_requires_stable_operational_keys() -> None:
    manager = InboundSequenceManager()

    with pytest.raises(ValueError, match="conversation_id"):
        manager.assign(
            InboundSequenceInput(conversation_id=" ", idempotency_key="inbound:a"),
            turn_id="turn_1",
        )

    with pytest.raises(ValueError, match="idempotency_key"):
        manager.assign(
            InboundSequenceInput(conversation_id="conv_1", idempotency_key=" "),
            turn_id="turn_1",
        )

    with pytest.raises(ValueError, match="turn_id"):
        manager.assign(
            InboundSequenceInput(conversation_id="conv_1", idempotency_key="inbound:a"),
            turn_id="",
        )


def test_sequence_result_has_only_operational_fields() -> None:
    input_field_names = {field.name for field in fields(InboundSequenceInput)}
    result_field_names = {field.name for field in fields(InboundSequenceResult)}
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
    result = InboundSequenceResult(
        status="assigned",
        conversation_id="conv_1",
        idempotency_key="inbound:a",
        sequence_number=1,
        accepted_turn_id="turn_1",
    )

    assert forbidden_decision_fields.isdisjoint(input_field_names)
    assert forbidden_decision_fields.isdisjoint(result_field_names)
    assert forbidden_decision_fields.isdisjoint(asdict(result))
