from __future__ import annotations

from collections.abc import Callable
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from threading import RLock
from typing import Literal

OutboxReservationStatus = Literal["reserved", "busy", "completed", "not_owner", "not_found"]
DeferredInboundStatus = Literal["deferred", "duplicate_deferred", "not_deferred"]
DeferredInboundAction = Literal["defer_until_outbox_complete", "process_now"]


@dataclass(frozen=True, slots=True)
class OutboxReservation:
    conversation_id: str
    outbox_id: str
    owner_turn_id: str
    inbound_sequence_number: int
    chunk_count: int
    reserved_at: datetime
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class OutboxReservationResult:
    status: OutboxReservationStatus
    conversation_id: str
    outbox_id: str | None = None
    owner_turn_id: str | None = None
    active_outbox_id: str | None = None
    active_owner_turn_id: str | None = None
    expires_at: datetime | None = None
    retry_after_seconds: float | None = None
    deferred_count: int = 0
    next_deferred_sequence_number: int | None = None


@dataclass(frozen=True, slots=True)
class DeferredInboundInput:
    conversation_id: str
    idempotency_key: str
    sequence_number: int
    turn_id: str


@dataclass(frozen=True, slots=True)
class DeferredInboundRecord:
    conversation_id: str
    idempotency_key: str
    sequence_number: int
    turn_id: str
    active_outbox_id: str
    deferred_at: datetime


@dataclass(frozen=True, slots=True)
class DeferredInboundDecision:
    status: DeferredInboundStatus
    action: DeferredInboundAction
    conversation_id: str
    idempotency_key: str
    sequence_number: int
    persist_inbound: bool = True
    start_parallel_response: bool = False
    active_outbox_id: str | None = None
    process_after_outbox_id: str | None = None
    accepted_turn_id: str | None = None
    duplicate_of_turn_id: str | None = None
    deferred_count: int = 0


class InMemoryOutboxStore:
    """Local outbox store for tests/dev; production wiring must use shared persistence."""

    def __init__(self) -> None:
        self._active_by_conversation: dict[str, OutboxReservation] = {}
        self._deferred_by_key: dict[tuple[str, str], DeferredInboundRecord] = {}
        self._lock = RLock()

    @contextmanager
    def transaction(self):
        with self._lock:
            yield

    def active(self, conversation_id: str) -> OutboxReservation | None:
        return self._active_by_conversation.get(conversation_id)

    def set_active(self, reservation: OutboxReservation) -> None:
        self._active_by_conversation[reservation.conversation_id] = reservation

    def clear_active(self, conversation_id: str) -> None:
        self._active_by_conversation.pop(conversation_id, None)

    def get_deferred(
        self,
        *,
        conversation_id: str,
        idempotency_key: str,
    ) -> DeferredInboundRecord | None:
        return self._deferred_by_key.get((conversation_id, idempotency_key))

    def add_deferred(self, record: DeferredInboundRecord) -> None:
        self._deferred_by_key[(record.conversation_id, record.idempotency_key)] = record

    def list_deferred(self, conversation_id: str) -> list[DeferredInboundRecord]:
        records = [
            record
            for (stored_conversation_id, _), record in self._deferred_by_key.items()
            if stored_conversation_id == conversation_id
        ]
        return sorted(records, key=lambda record: record.sequence_number)

    def pop_next_deferred(self, conversation_id: str) -> DeferredInboundRecord | None:
        records = self.list_deferred(conversation_id)
        if not records:
            return None
        record = records[0]
        self._deferred_by_key.pop((record.conversation_id, record.idempotency_key), None)
        return record

    def deferred_count(self, conversation_id: str) -> int:
        return len(self.list_deferred(conversation_id))


class OutboxManager:
    def __init__(
        self,
        *,
        store: InMemoryOutboxStore | None = None,
        ttl_seconds: int = 300,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be greater than zero")

        self._store = store or InMemoryOutboxStore()
        self._ttl = timedelta(seconds=ttl_seconds)
        self._now = now or _utc_now

    def reserve_delivery(
        self,
        *,
        conversation_id: str,
        outbox_id: str,
        owner_turn_id: str,
        inbound_sequence_number: int,
        chunk_count: int,
    ) -> OutboxReservationResult:
        _validate_key("conversation_id", conversation_id)
        _validate_key("outbox_id", outbox_id)
        _validate_key("owner_turn_id", owner_turn_id)
        _validate_positive_int("inbound_sequence_number", inbound_sequence_number)
        _validate_positive_int("chunk_count", chunk_count)

        with self._store.transaction():
            now = self._now()
            active = self._active_if_unexpired(conversation_id, now)
            if active is not None:
                return OutboxReservationResult(
                    status="busy",
                    conversation_id=conversation_id,
                    active_outbox_id=active.outbox_id,
                    active_owner_turn_id=active.owner_turn_id,
                    expires_at=active.expires_at,
                    retry_after_seconds=max(0.0, (active.expires_at - now).total_seconds()),
                    deferred_count=self._store.deferred_count(conversation_id),
                    next_deferred_sequence_number=_next_deferred_sequence(
                        self._store,
                        conversation_id,
                    ),
                )

            reservation = OutboxReservation(
                conversation_id=conversation_id,
                outbox_id=outbox_id,
                owner_turn_id=owner_turn_id,
                inbound_sequence_number=inbound_sequence_number,
                chunk_count=chunk_count,
                reserved_at=now,
                expires_at=now + self._ttl,
            )
            self._store.set_active(reservation)

            return OutboxReservationResult(
                status="reserved",
                conversation_id=conversation_id,
                outbox_id=outbox_id,
                owner_turn_id=owner_turn_id,
                expires_at=reservation.expires_at,
            )

    def evaluate_inbound(self, inbound: DeferredInboundInput) -> DeferredInboundDecision:
        _validate_key("conversation_id", inbound.conversation_id)
        _validate_key("idempotency_key", inbound.idempotency_key)
        _validate_key("turn_id", inbound.turn_id)
        _validate_positive_int("sequence_number", inbound.sequence_number)

        with self._store.transaction():
            now = self._now()
            active = self._active_if_unexpired(inbound.conversation_id, now)
            if active is None:
                return DeferredInboundDecision(
                    status="not_deferred",
                    action="process_now",
                    conversation_id=inbound.conversation_id,
                    idempotency_key=inbound.idempotency_key,
                    sequence_number=inbound.sequence_number,
                    accepted_turn_id=inbound.turn_id,
                )

            existing = self._store.get_deferred(
                conversation_id=inbound.conversation_id,
                idempotency_key=inbound.idempotency_key,
            )
            if existing is not None:
                return DeferredInboundDecision(
                    status="duplicate_deferred",
                    action="defer_until_outbox_complete",
                    conversation_id=inbound.conversation_id,
                    idempotency_key=inbound.idempotency_key,
                    sequence_number=existing.sequence_number,
                    active_outbox_id=existing.active_outbox_id,
                    process_after_outbox_id=existing.active_outbox_id,
                    duplicate_of_turn_id=existing.turn_id,
                    deferred_count=self._store.deferred_count(inbound.conversation_id),
                )

            record = DeferredInboundRecord(
                conversation_id=inbound.conversation_id,
                idempotency_key=inbound.idempotency_key,
                sequence_number=inbound.sequence_number,
                turn_id=inbound.turn_id,
                active_outbox_id=active.outbox_id,
                deferred_at=now,
            )
            self._store.add_deferred(record)

            return DeferredInboundDecision(
                status="deferred",
                action="defer_until_outbox_complete",
                conversation_id=inbound.conversation_id,
                idempotency_key=inbound.idempotency_key,
                sequence_number=inbound.sequence_number,
                active_outbox_id=active.outbox_id,
                process_after_outbox_id=active.outbox_id,
                deferred_count=self._store.deferred_count(inbound.conversation_id),
            )

    def complete_delivery(
        self,
        *,
        conversation_id: str,
        outbox_id: str,
        owner_turn_id: str,
    ) -> OutboxReservationResult:
        _validate_key("conversation_id", conversation_id)
        _validate_key("outbox_id", outbox_id)
        _validate_key("owner_turn_id", owner_turn_id)

        with self._store.transaction():
            active = self._store.active(conversation_id)
            if active is None or active.outbox_id != outbox_id:
                return OutboxReservationResult(
                    status="not_found",
                    conversation_id=conversation_id,
                    outbox_id=outbox_id,
                    deferred_count=self._store.deferred_count(conversation_id),
                    next_deferred_sequence_number=_next_deferred_sequence(
                        self._store,
                        conversation_id,
                    ),
                )

            if active.owner_turn_id != owner_turn_id:
                return OutboxReservationResult(
                    status="not_owner",
                    conversation_id=conversation_id,
                    outbox_id=outbox_id,
                    active_outbox_id=active.outbox_id,
                    active_owner_turn_id=active.owner_turn_id,
                    expires_at=active.expires_at,
                    deferred_count=self._store.deferred_count(conversation_id),
                    next_deferred_sequence_number=_next_deferred_sequence(
                        self._store,
                        conversation_id,
                    ),
                )

            self._store.clear_active(conversation_id)
            return OutboxReservationResult(
                status="completed",
                conversation_id=conversation_id,
                outbox_id=outbox_id,
                owner_turn_id=owner_turn_id,
                deferred_count=self._store.deferred_count(conversation_id),
                next_deferred_sequence_number=_next_deferred_sequence(
                    self._store,
                    conversation_id,
                ),
            )

    def pop_next_deferred(self, *, conversation_id: str) -> DeferredInboundRecord | None:
        _validate_key("conversation_id", conversation_id)
        with self._store.transaction():
            return self._store.pop_next_deferred(conversation_id)

    def active_delivery(self, *, conversation_id: str) -> OutboxReservation | None:
        _validate_key("conversation_id", conversation_id)
        with self._store.transaction():
            return self._active_if_unexpired(conversation_id, self._now())

    def _active_if_unexpired(
        self,
        conversation_id: str,
        now: datetime,
    ) -> OutboxReservation | None:
        active = self._store.active(conversation_id)
        if active is None:
            return None
        if active.expires_at <= now:
            self._store.clear_active(conversation_id)
            return None
        return active


def _next_deferred_sequence(
    store: InMemoryOutboxStore,
    conversation_id: str,
) -> int | None:
    records = store.list_deferred(conversation_id)
    return records[0].sequence_number if records else None


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _validate_key(field_name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty")


def _validate_positive_int(field_name: str, value: int) -> None:
    if value <= 0:
        raise ValueError(f"{field_name} must be greater than zero")
