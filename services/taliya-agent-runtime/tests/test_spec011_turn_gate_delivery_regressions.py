from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, datetime

from app.core.taliya_commercial.outbox import DeferredInboundInput, OutboxManager
from app.core.taliya_commercial.turn_gate import (
    InboundIdempotencyInput,
    InboundIdempotencyManager,
    InboundSequenceInput,
    InboundSequenceManager,
)


def _runtime_parts():
    def now() -> datetime:
        return datetime(2026, 5, 30, 12, 0, tzinfo=UTC)

    return (
        InboundIdempotencyManager(now=now),
        InboundSequenceManager(now=now),
        OutboxManager(now=now),
    )


def _claim_and_sequence(
    idempotency: InboundIdempotencyManager,
    sequence: InboundSequenceManager,
    *,
    conversation_id: str,
    turn_id: str,
    channel_message_id: str,
):
    claim = idempotency.claim(
        InboundIdempotencyInput(
            channel="whatsapp",
            conversation_id=conversation_id,
            channel_conversation_id="wa_thread_1",
            channel_message_id=channel_message_id,
            provided_idempotency_key=f"adapter:{turn_id}",
        ),
        turn_id=turn_id,
    )
    assigned = sequence.assign(
        InboundSequenceInput(
            conversation_id=conversation_id,
            idempotency_key=claim.idempotency_key,
        ),
        turn_id=turn_id,
    )
    return claim, assigned


def test_rc_011_010_second_inbound_during_chunks_waits_for_current_outbox() -> None:
    idempotency, sequence, outbox = _runtime_parts()
    _, first_sequence = _claim_and_sequence(
        idempotency,
        sequence,
        conversation_id="conv_1",
        turn_id="turn_1",
        channel_message_id="wamid_1",
    )
    outbox.reserve_delivery(
        conversation_id="conv_1",
        outbox_id="outbox_1",
        owner_turn_id="turn_1",
        inbound_sequence_number=first_sequence.sequence_number,
        chunk_count=3,
    )
    second_claim, second_sequence = _claim_and_sequence(
        idempotency,
        sequence,
        conversation_id="conv_1",
        turn_id="turn_2",
        channel_message_id="wamid_2",
    )

    during_delivery = outbox.evaluate_inbound(
        DeferredInboundInput(
            conversation_id="conv_1",
            idempotency_key=second_claim.idempotency_key,
            sequence_number=second_sequence.sequence_number,
            turn_id="turn_2",
        )
    )
    completed = outbox.complete_delivery(
        conversation_id="conv_1",
        outbox_id="outbox_1",
        owner_turn_id="turn_1",
    )
    next_turn = outbox.pop_next_deferred(conversation_id="conv_1")

    assert during_delivery.status == "deferred"
    assert during_delivery.action == "defer_until_outbox_complete"
    assert during_delivery.persist_inbound is True
    assert during_delivery.start_parallel_response is False
    assert completed.status == "completed"
    assert completed.deferred_count == 1
    assert next_turn is not None
    assert next_turn.turn_id == "turn_2"
    assert next_turn.sequence_number == 2


def test_rc_011_010_retry_of_deferred_inbound_does_not_duplicate_queue() -> None:
    idempotency, sequence, outbox = _runtime_parts()
    _, first_sequence = _claim_and_sequence(
        idempotency,
        sequence,
        conversation_id="conv_1",
        turn_id="turn_1",
        channel_message_id="wamid_1",
    )
    outbox.reserve_delivery(
        conversation_id="conv_1",
        outbox_id="outbox_1",
        owner_turn_id="turn_1",
        inbound_sequence_number=first_sequence.sequence_number,
        chunk_count=3,
    )
    second_claim, second_sequence = _claim_and_sequence(
        idempotency,
        sequence,
        conversation_id="conv_1",
        turn_id="turn_2",
        channel_message_id="wamid_2",
    )

    first_defer = outbox.evaluate_inbound(
        DeferredInboundInput(
            conversation_id="conv_1",
            idempotency_key=second_claim.idempotency_key,
            sequence_number=second_sequence.sequence_number,
            turn_id="turn_2",
        )
    )
    retry_claim, retry_sequence = _claim_and_sequence(
        idempotency,
        sequence,
        conversation_id="conv_1",
        turn_id="turn_retry",
        channel_message_id="wamid_2",
    )
    retry_defer = outbox.evaluate_inbound(
        DeferredInboundInput(
            conversation_id="conv_1",
            idempotency_key=retry_claim.idempotency_key,
            sequence_number=retry_sequence.sequence_number,
            turn_id="turn_retry",
        )
    )
    completed = outbox.complete_delivery(
        conversation_id="conv_1",
        outbox_id="outbox_1",
        owner_turn_id="turn_1",
    )
    next_turn = outbox.pop_next_deferred(conversation_id="conv_1")
    empty = outbox.pop_next_deferred(conversation_id="conv_1")

    assert retry_claim.status == "duplicate"
    assert retry_sequence.status == "duplicate"
    assert retry_sequence.sequence_number == second_sequence.sequence_number
    assert first_defer.status == "deferred"
    assert retry_defer.status == "duplicate_deferred"
    assert retry_defer.duplicate_of_turn_id == "turn_2"
    assert completed.deferred_count == 1
    assert next_turn is not None
    assert next_turn.turn_id == "turn_2"
    assert empty is None


def test_rc_011_011_social_ack_during_chunks_is_deferred_without_semantic_handling() -> None:
    lead_message_sent_during_chunks = "tudo bem"
    idempotency, sequence, outbox = _runtime_parts()
    _, first_sequence = _claim_and_sequence(
        idempotency,
        sequence,
        conversation_id="conv_1",
        turn_id="turn_1",
        channel_message_id="wamid_1",
    )
    outbox.reserve_delivery(
        conversation_id="conv_1",
        outbox_id="outbox_1",
        owner_turn_id="turn_1",
        inbound_sequence_number=first_sequence.sequence_number,
        chunk_count=3,
    )
    ack_claim, ack_sequence = _claim_and_sequence(
        idempotency,
        sequence,
        conversation_id="conv_1",
        turn_id="turn_2",
        channel_message_id="wamid_tudo_bem",
    )

    during_delivery = outbox.evaluate_inbound(
        DeferredInboundInput(
            conversation_id="conv_1",
            idempotency_key=ack_claim.idempotency_key,
            sequence_number=ack_sequence.sequence_number,
            turn_id="turn_2",
        )
    )
    outbox.complete_delivery(
        conversation_id="conv_1",
        outbox_id="outbox_1",
        owner_turn_id="turn_1",
    )
    next_turn = outbox.pop_next_deferred(conversation_id="conv_1")

    assert lead_message_sent_during_chunks == "tudo bem"
    assert "tudo bem" not in str(asdict(during_delivery))
    assert during_delivery.status == "deferred"
    assert during_delivery.start_parallel_response is False
    assert during_delivery.action == "defer_until_outbox_complete"
    assert next_turn is not None
    assert next_turn.turn_id == "turn_2"
