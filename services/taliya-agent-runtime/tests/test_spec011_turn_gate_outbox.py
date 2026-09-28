from __future__ import annotations

from dataclasses import asdict, fields
from datetime import UTC, datetime

import pytest

from app.core.taliya_commercial.outbox import (
    DeferredInboundDecision,
    DeferredInboundInput,
    InMemoryOutboxStore,
    OutboxManager,
    OutboxReservationResult,
)


def test_active_outbox_defers_new_inbound_without_parallel_response() -> None:
    manager = OutboxManager(now=lambda: datetime(2026, 5, 30, 12, 0, tzinfo=UTC))
    reservation = manager.reserve_delivery(
        conversation_id="conv_1",
        outbox_id="outbox_1",
        owner_turn_id="turn_1",
        inbound_sequence_number=1,
        chunk_count=3,
    )

    decision = manager.evaluate_inbound(
        DeferredInboundInput(
            conversation_id="conv_1",
            idempotency_key="inbound:b",
            sequence_number=2,
            turn_id="turn_2",
        )
    )

    assert reservation.status == "reserved"
    assert decision.status == "deferred"
    assert decision.action == "defer_until_outbox_complete"
    assert decision.persist_inbound is True
    assert decision.start_parallel_response is False
    assert decision.active_outbox_id == "outbox_1"
    assert decision.process_after_outbox_id == "outbox_1"


def test_duplicate_deferred_inbound_keeps_one_queue_entry() -> None:
    manager = OutboxManager(now=lambda: datetime(2026, 5, 30, 12, 0, tzinfo=UTC))
    manager.reserve_delivery(
        conversation_id="conv_1",
        outbox_id="outbox_1",
        owner_turn_id="turn_1",
        inbound_sequence_number=1,
        chunk_count=2,
    )

    first = manager.evaluate_inbound(
        DeferredInboundInput(
            conversation_id="conv_1",
            idempotency_key="inbound:b",
            sequence_number=2,
            turn_id="turn_2",
        )
    )
    duplicate = manager.evaluate_inbound(
        DeferredInboundInput(
            conversation_id="conv_1",
            idempotency_key="inbound:b",
            sequence_number=2,
            turn_id="turn_retry",
        )
    )

    completed = manager.complete_delivery(
        conversation_id="conv_1",
        outbox_id="outbox_1",
        owner_turn_id="turn_1",
    )
    next_deferred = manager.pop_next_deferred(conversation_id="conv_1")
    empty = manager.pop_next_deferred(conversation_id="conv_1")

    assert first.status == "deferred"
    assert duplicate.status == "duplicate_deferred"
    assert duplicate.duplicate_of_turn_id == "turn_2"
    assert completed.status == "completed"
    assert completed.deferred_count == 1
    assert next_deferred is not None
    assert next_deferred.sequence_number == 2
    assert next_deferred.turn_id == "turn_2"
    assert empty is None


def test_deferred_inbounds_are_released_in_sequence_order_after_delivery_finishes() -> None:
    manager = OutboxManager(now=lambda: datetime(2026, 5, 30, 12, 0, tzinfo=UTC))
    manager.reserve_delivery(
        conversation_id="conv_1",
        outbox_id="outbox_1",
        owner_turn_id="turn_1",
        inbound_sequence_number=1,
        chunk_count=2,
    )

    manager.evaluate_inbound(
        DeferredInboundInput(
            conversation_id="conv_1",
            idempotency_key="inbound:c",
            sequence_number=3,
            turn_id="turn_3",
        )
    )
    manager.evaluate_inbound(
        DeferredInboundInput(
            conversation_id="conv_1",
            idempotency_key="inbound:b",
            sequence_number=2,
            turn_id="turn_2",
        )
    )
    manager.complete_delivery(
        conversation_id="conv_1",
        outbox_id="outbox_1",
        owner_turn_id="turn_1",
    )

    first = manager.pop_next_deferred(conversation_id="conv_1")
    second = manager.pop_next_deferred(conversation_id="conv_1")

    assert first is not None
    assert first.sequence_number == 2
    assert second is not None
    assert second.sequence_number == 3


def test_inbound_after_delivery_completion_can_process_now() -> None:
    manager = OutboxManager(now=lambda: datetime(2026, 5, 30, 12, 0, tzinfo=UTC))
    manager.reserve_delivery(
        conversation_id="conv_1",
        outbox_id="outbox_1",
        owner_turn_id="turn_1",
        inbound_sequence_number=1,
        chunk_count=1,
    )
    manager.complete_delivery(
        conversation_id="conv_1",
        outbox_id="outbox_1",
        owner_turn_id="turn_1",
    )

    decision = manager.evaluate_inbound(
        DeferredInboundInput(
            conversation_id="conv_1",
            idempotency_key="inbound:b",
            sequence_number=2,
            turn_id="turn_2",
        )
    )

    assert decision.status == "not_deferred"
    assert decision.action == "process_now"
    assert decision.persist_inbound is True
    assert decision.start_parallel_response is False


def test_outbox_reservation_is_owned_and_scoped_by_conversation() -> None:
    store = InMemoryOutboxStore()
    manager = OutboxManager(
        store=store,
        now=lambda: datetime(2026, 5, 30, 12, 0, tzinfo=UTC),
    )
    first = manager.reserve_delivery(
        conversation_id="conv_1",
        outbox_id="outbox_1",
        owner_turn_id="turn_1",
        inbound_sequence_number=1,
        chunk_count=1,
    )
    busy = manager.reserve_delivery(
        conversation_id="conv_1",
        outbox_id="outbox_2",
        owner_turn_id="turn_2",
        inbound_sequence_number=2,
        chunk_count=1,
    )
    other_conversation = manager.reserve_delivery(
        conversation_id="conv_2",
        outbox_id="outbox_3",
        owner_turn_id="turn_3",
        inbound_sequence_number=1,
        chunk_count=1,
    )
    wrong_owner = manager.complete_delivery(
        conversation_id="conv_1",
        outbox_id="outbox_1",
        owner_turn_id="turn_2",
    )

    assert first.status == "reserved"
    assert busy.status == "busy"
    assert busy.active_outbox_id == "outbox_1"
    assert other_conversation.status == "reserved"
    assert wrong_owner.status == "not_owner"
    assert manager.active_delivery(conversation_id="conv_1") is not None


def test_outbox_rejects_invalid_operational_keys() -> None:
    manager = OutboxManager()

    with pytest.raises(ValueError, match="conversation_id"):
        manager.reserve_delivery(
            conversation_id=" ",
            outbox_id="outbox_1",
            owner_turn_id="turn_1",
            inbound_sequence_number=1,
            chunk_count=1,
        )

    with pytest.raises(ValueError, match="chunk_count"):
        manager.reserve_delivery(
            conversation_id="conv_1",
            outbox_id="outbox_1",
            owner_turn_id="turn_1",
            inbound_sequence_number=1,
            chunk_count=0,
        )


def test_outbox_results_have_only_operational_fields() -> None:
    deferred_field_names = {field.name for field in fields(DeferredInboundDecision)}
    reservation_field_names = {field.name for field in fields(OutboxReservationResult)}
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
    result = DeferredInboundDecision(
        status="not_deferred",
        action="process_now",
        conversation_id="conv_1",
        idempotency_key="inbound:a",
        sequence_number=1,
    )

    assert forbidden_decision_fields.isdisjoint(deferred_field_names)
    assert forbidden_decision_fields.isdisjoint(reservation_field_names)
    assert forbidden_decision_fields.isdisjoint(asdict(result))
