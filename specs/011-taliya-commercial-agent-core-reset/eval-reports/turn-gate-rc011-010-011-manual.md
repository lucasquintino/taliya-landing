# Turn Gate Manual Validation - RC-011-010 / RC-011-011

Date: 2026-05-30

Scope: isolated Spec 011 Turn Gate core. This does not claim public runtime/adapter cutover; that remains Phase 9.

Regression cases:

- `RC-011-010`: duplicate chunks / second inbound while previous response chunks are scheduled.
- `RC-011-011`: `"tudo bem"` during chunk delivery must be persisted/deferred and must not be processed in parallel as a new commercial intent.

Manual simulation command:

```powershell
@'
from datetime import UTC, datetime

from app.core.taliya_commercial.outbox import DeferredInboundInput, OutboxManager
from app.core.taliya_commercial.turn_gate import (
    InboundIdempotencyInput,
    InboundIdempotencyManager,
    InboundSequenceInput,
    InboundSequenceManager,
)

def now() -> datetime:
    return datetime(2026, 5, 30, 12, 0, tzinfo=UTC)

idempotency = InboundIdempotencyManager(now=now)
sequence = InboundSequenceManager(now=now)
outbox = OutboxManager(now=now)

def claim_and_sequence(turn_id: str, channel_message_id: str):
    claim = idempotency.claim(
        InboundIdempotencyInput(
            channel="whatsapp",
            conversation_id="conv_manual",
            channel_conversation_id="wa_manual",
            channel_message_id=channel_message_id,
            provided_idempotency_key=f"adapter:{turn_id}",
        ),
        turn_id=turn_id,
    )
    assigned = sequence.assign(
        InboundSequenceInput(
            conversation_id="conv_manual",
            idempotency_key=claim.idempotency_key,
        ),
        turn_id=turn_id,
    )
    return claim, assigned

_, first_seq = claim_and_sequence("turn_1", "wamid_1")
reservation = outbox.reserve_delivery(
    conversation_id="conv_manual",
    outbox_id="outbox_current",
    owner_turn_id="turn_1",
    inbound_sequence_number=first_seq.sequence_number,
    chunk_count=3,
)
print(f"1 reserve_current: status={reservation.status}; chunks=3")

lead_text = "tudo bem"
ack_claim, ack_seq = claim_and_sequence("turn_2", "wamid_2")
ack_decision = outbox.evaluate_inbound(
    DeferredInboundInput(
        conversation_id="conv_manual",
        idempotency_key=ack_claim.idempotency_key,
        sequence_number=ack_seq.sequence_number,
        turn_id="turn_2",
    )
)
print(
    "2 inbound_during_chunks: "
    f"lead_text={lead_text!r}; status={ack_decision.status}; "
    f"action={ack_decision.action}; parallel={ack_decision.start_parallel_response}; "
    f"persist={ack_decision.persist_inbound}"
)

retry_claim, retry_seq = claim_and_sequence("turn_retry", "wamid_2")
retry_decision = outbox.evaluate_inbound(
    DeferredInboundInput(
        conversation_id="conv_manual",
        idempotency_key=retry_claim.idempotency_key,
        sequence_number=retry_seq.sequence_number,
        turn_id="turn_retry",
    )
)
print(
    "3 retry_same_inbound: "
    f"idempotency={retry_claim.status}; sequence={retry_seq.status}; "
    f"defer={retry_decision.status}; duplicate_of={retry_decision.duplicate_of_turn_id}"
)

completed = outbox.complete_delivery(
    conversation_id="conv_manual",
    outbox_id="outbox_current",
    owner_turn_id="turn_1",
)
next_turn = outbox.pop_next_deferred(conversation_id="conv_manual")
print(
    "4 finish_current_then_next: "
    f"completion={completed.status}; queued={completed.deferred_count}; "
    f"next_turn={next_turn.turn_id if next_turn else None}; "
    f"next_sequence={next_turn.sequence_number if next_turn else None}"
)
'@ | python -
```

Observed output:

```text
1 reserve_current: status=reserved; chunks=3
2 inbound_during_chunks: lead_text='tudo bem'; status=deferred; action=defer_until_outbox_complete; parallel=False; persist=True
3 retry_same_inbound: idempotency=duplicate; sequence=duplicate; defer=duplicate_deferred; duplicate_of=turn_2
4 finish_current_then_next: completion=completed; queued=1; next_turn=turn_2; next_sequence=2
```

Manual conclusion:

- The active outbound delivery is reserved before chunk delivery.
- A new inbound received during active delivery is persisted/deferred.
- No parallel response is started.
- Provider retry of the same inbound remains duplicate at idempotency, sequence, and deferred-queue layers.
- The current outbound completes first.
- The deferred inbound becomes the next clean turn after completion.
- The string `"tudo bem"` is not passed into the Turn Gate as a semantic signal; the gate uses only operational ids and sequence.
