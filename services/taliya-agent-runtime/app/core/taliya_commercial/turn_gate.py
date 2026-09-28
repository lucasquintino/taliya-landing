from __future__ import annotations

from collections.abc import Callable
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from threading import RLock
from typing import Literal

Channel = Literal["widget", "whatsapp"]
TurnLockStatus = Literal["acquired", "busy", "released", "not_owner", "not_found"]
InboundIdempotencyStatus = Literal["new", "duplicate"]
InboundSequenceStatus = Literal["assigned", "duplicate"]
HumanPauseAction = Literal["continue", "suppress_ai_reply"]

BLOCKING_HUMAN_STATUSES = frozenset(
    {
        "active",
        "human_active",
        "human_handoff",
        "paused_by_human",
    }
)
OPEN_HUMAN_STATUSES = frozenset({"none", "resumed"})


@dataclass(frozen=True, slots=True)
class InboundIdempotencyInput:
    channel: Channel
    conversation_id: str
    channel_conversation_id: str | None = None
    channel_message_id: str | None = None
    provided_idempotency_key: str | None = None


@dataclass(frozen=True, slots=True)
class InboundIdempotencyRecord:
    idempotency_key: str
    conversation_id: str
    turn_id: str
    claimed_at: datetime


@dataclass(frozen=True, slots=True)
class InboundIdempotencyResult:
    status: InboundIdempotencyStatus
    idempotency_key: str
    conversation_id: str
    accepted_turn_id: str | None = None
    duplicate_of_turn_id: str | None = None
    claimed_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class InboundSequenceInput:
    conversation_id: str
    idempotency_key: str


@dataclass(frozen=True, slots=True)
class InboundSequenceRecord:
    conversation_id: str
    idempotency_key: str
    sequence_number: int
    turn_id: str
    assigned_at: datetime


@dataclass(frozen=True, slots=True)
class InboundSequenceResult:
    status: InboundSequenceStatus
    conversation_id: str
    idempotency_key: str
    sequence_number: int
    accepted_turn_id: str | None = None
    duplicate_of_turn_id: str | None = None
    assigned_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class HumanPauseState:
    conversation_id: str
    status: str = "none"
    reason: str | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class HumanPauseDecision:
    action: HumanPauseAction
    conversation_id: str
    human_status: str
    ai_reply_allowed: bool
    persist_inbound: bool = True
    requires_explicit_resume: bool = False
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class TurnLockLease:
    conversation_id: str
    owner_id: str
    acquired_at: datetime
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class TurnLockResult:
    status: TurnLockStatus
    conversation_id: str
    owner_id: str | None = None
    active_owner_id: str | None = None
    expires_at: datetime | None = None
    retry_after_seconds: float | None = None


class InMemoryConversationLockStore:
    """Local lock store for tests/dev; production wiring must use shared persistence."""

    def __init__(self) -> None:
        self._locks: dict[str, TurnLockLease] = {}
        self._lock = RLock()

    @contextmanager
    def transaction(self):
        with self._lock:
            yield

    def get(self, conversation_id: str) -> TurnLockLease | None:
        return self._locks.get(conversation_id)

    def set(self, lease: TurnLockLease) -> None:
        self._locks[lease.conversation_id] = lease

    def delete(self, conversation_id: str) -> None:
        self._locks.pop(conversation_id, None)


class InMemoryInboundIdempotencyStore:
    """Local idempotency store for tests/dev; production wiring must be durable."""

    def __init__(self) -> None:
        self._records: dict[str, InboundIdempotencyRecord] = {}
        self._lock = RLock()

    @contextmanager
    def transaction(self):
        with self._lock:
            yield

    def get(self, idempotency_key: str) -> InboundIdempotencyRecord | None:
        return self._records.get(idempotency_key)

    def set(self, record: InboundIdempotencyRecord) -> None:
        self._records[record.idempotency_key] = record


class InMemoryInboundSequenceStore:
    """Local sequence store for tests/dev; production wiring must be durable."""

    def __init__(self) -> None:
        self._records: dict[tuple[str, str], InboundSequenceRecord] = {}
        self._last_sequence_by_conversation: dict[str, int] = {}
        self._lock = RLock()

    @contextmanager
    def transaction(self):
        with self._lock:
            yield

    def get(self, *, conversation_id: str, idempotency_key: str) -> InboundSequenceRecord | None:
        return self._records.get((conversation_id, idempotency_key))

    def next_sequence_number(self, conversation_id: str) -> int:
        return self._last_sequence_by_conversation.get(conversation_id, 0) + 1

    def set(self, record: InboundSequenceRecord) -> None:
        key = (record.conversation_id, record.idempotency_key)
        self._records[key] = record
        current = self._last_sequence_by_conversation.get(record.conversation_id, 0)
        self._last_sequence_by_conversation[record.conversation_id] = max(
            current,
            record.sequence_number,
        )


class InMemoryHumanPauseStore:
    """Local human-pause store for tests/dev; production wiring must be durable."""

    def __init__(self) -> None:
        self._states: dict[str, HumanPauseState] = {}
        self._lock = RLock()

    @contextmanager
    def transaction(self):
        with self._lock:
            yield

    def get(self, conversation_id: str) -> HumanPauseState | None:
        return self._states.get(conversation_id)

    def set(self, state: HumanPauseState) -> None:
        self._states[state.conversation_id] = state


class InboundIdempotencyManager:
    def __init__(
        self,
        *,
        store: InMemoryInboundIdempotencyStore | None = None,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self._store = store or InMemoryInboundIdempotencyStore()
        self._now = now or _utc_now

    def claim(self, inbound: InboundIdempotencyInput, *, turn_id: str) -> InboundIdempotencyResult:
        _validate_lock_key("turn_id", turn_id)
        key = stable_inbound_idempotency_key(inbound)

        with self._store.transaction():
            existing = self._store.get(key)
            if existing is not None:
                return InboundIdempotencyResult(
                    status="duplicate",
                    idempotency_key=key,
                    conversation_id=existing.conversation_id,
                    duplicate_of_turn_id=existing.turn_id,
                    claimed_at=existing.claimed_at,
                )

            record = InboundIdempotencyRecord(
                idempotency_key=key,
                conversation_id=inbound.conversation_id,
                turn_id=turn_id,
                claimed_at=self._now(),
            )
            self._store.set(record)
            return InboundIdempotencyResult(
                status="new",
                idempotency_key=key,
                conversation_id=inbound.conversation_id,
                accepted_turn_id=turn_id,
                claimed_at=record.claimed_at,
            )


class InboundSequenceManager:
    def __init__(
        self,
        *,
        store: InMemoryInboundSequenceStore | None = None,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self._store = store or InMemoryInboundSequenceStore()
        self._now = now or _utc_now

    def assign(
        self,
        inbound: InboundSequenceInput,
        *,
        turn_id: str,
    ) -> InboundSequenceResult:
        _validate_lock_key("conversation_id", inbound.conversation_id)
        _validate_lock_key("idempotency_key", inbound.idempotency_key)
        _validate_lock_key("turn_id", turn_id)

        with self._store.transaction():
            existing = self._store.get(
                conversation_id=inbound.conversation_id,
                idempotency_key=inbound.idempotency_key,
            )
            if existing is not None:
                return InboundSequenceResult(
                    status="duplicate",
                    conversation_id=inbound.conversation_id,
                    idempotency_key=inbound.idempotency_key,
                    sequence_number=existing.sequence_number,
                    duplicate_of_turn_id=existing.turn_id,
                    assigned_at=existing.assigned_at,
                )

            record = InboundSequenceRecord(
                conversation_id=inbound.conversation_id,
                idempotency_key=inbound.idempotency_key,
                sequence_number=self._store.next_sequence_number(inbound.conversation_id),
                turn_id=turn_id,
                assigned_at=self._now(),
            )
            self._store.set(record)
            return InboundSequenceResult(
                status="assigned",
                conversation_id=inbound.conversation_id,
                idempotency_key=inbound.idempotency_key,
                sequence_number=record.sequence_number,
                accepted_turn_id=turn_id,
                assigned_at=record.assigned_at,
            )


class HumanPauseManager:
    def __init__(
        self,
        *,
        store: InMemoryHumanPauseStore | None = None,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self._store = store or InMemoryHumanPauseStore()
        self._now = now or _utc_now

    def pause(
        self,
        *,
        conversation_id: str,
        reason: str | None = None,
        status: str = "paused_by_human",
    ) -> HumanPauseState:
        _validate_lock_key("conversation_id", conversation_id)
        normalized_status = _normalized_required("human_status", status)
        if normalized_status not in BLOCKING_HUMAN_STATUSES:
            raise ValueError("pause status must block AI replies")

        state = HumanPauseState(
            conversation_id=conversation_id,
            status=normalized_status,
            reason=reason,
            updated_at=self._now(),
        )
        with self._store.transaction():
            self._store.set(state)
        return state

    def resume(self, *, conversation_id: str) -> HumanPauseState:
        _validate_lock_key("conversation_id", conversation_id)
        state = HumanPauseState(
            conversation_id=conversation_id,
            status="resumed",
            reason=None,
            updated_at=self._now(),
        )
        with self._store.transaction():
            self._store.set(state)
        return state

    def evaluate(self, *, conversation_id: str) -> HumanPauseDecision:
        _validate_lock_key("conversation_id", conversation_id)
        with self._store.transaction():
            state = self._store.get(conversation_id)

        if state is None:
            state = HumanPauseState(conversation_id=conversation_id)

        status = state.status.strip().lower()
        if status in OPEN_HUMAN_STATUSES:
            return HumanPauseDecision(
                action="continue",
                conversation_id=conversation_id,
                human_status=status,
                ai_reply_allowed=True,
            )

        if status in BLOCKING_HUMAN_STATUSES:
            return HumanPauseDecision(
                action="suppress_ai_reply",
                conversation_id=conversation_id,
                human_status=status,
                ai_reply_allowed=False,
                requires_explicit_resume=True,
                reason=state.reason,
            )

        return HumanPauseDecision(
            action="suppress_ai_reply",
            conversation_id=conversation_id,
            human_status=status,
            ai_reply_allowed=False,
            requires_explicit_resume=True,
            reason=f"unsupported_human_status:{status}",
        )


class ConversationLockManager:
    def __init__(
        self,
        *,
        store: InMemoryConversationLockStore | None = None,
        ttl_seconds: int = 120,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be greater than zero")

        self._store = store or InMemoryConversationLockStore()
        self._ttl = timedelta(seconds=ttl_seconds)
        self._now = now or _utc_now

    def acquire(self, *, conversation_id: str, owner_id: str) -> TurnLockResult:
        _validate_lock_key("conversation_id", conversation_id)
        _validate_lock_key("owner_id", owner_id)

        with self._store.transaction():
            now = self._now()
            active = self._store.get(conversation_id)

            if active is not None and active.expires_at > now:
                return TurnLockResult(
                    status="busy",
                    conversation_id=conversation_id,
                    active_owner_id=active.owner_id,
                    expires_at=active.expires_at,
                    retry_after_seconds=max(0.0, (active.expires_at - now).total_seconds()),
                )

            lease = TurnLockLease(
                conversation_id=conversation_id,
                owner_id=owner_id,
                acquired_at=now,
                expires_at=now + self._ttl,
            )
            self._store.set(lease)

            return TurnLockResult(
                status="acquired",
                conversation_id=conversation_id,
                owner_id=owner_id,
                expires_at=lease.expires_at,
            )

    def release(self, *, conversation_id: str, owner_id: str) -> TurnLockResult:
        _validate_lock_key("conversation_id", conversation_id)
        _validate_lock_key("owner_id", owner_id)

        with self._store.transaction():
            active = self._store.get(conversation_id)

            if active is None:
                return TurnLockResult(status="not_found", conversation_id=conversation_id)

            if active.owner_id != owner_id:
                return TurnLockResult(
                    status="not_owner",
                    conversation_id=conversation_id,
                    active_owner_id=active.owner_id,
                    expires_at=active.expires_at,
                )

            self._store.delete(conversation_id)
            return TurnLockResult(
                status="released",
                conversation_id=conversation_id,
                owner_id=owner_id,
            )


def _utc_now() -> datetime:
    return datetime.now(UTC)


def stable_inbound_idempotency_key(inbound: InboundIdempotencyInput) -> str:
    channel = _normalized_required("channel", inbound.channel)
    if channel not in {"widget", "whatsapp"}:
        raise ValueError("channel must be widget or whatsapp")
    conversation_scope = _normalized_required(
        "conversation_id",
        inbound.channel_conversation_id or inbound.conversation_id,
    )
    source_name, source_value = _stable_inbound_source(inbound)
    material = "\x1f".join(("011", channel, conversation_scope, source_name, source_value))
    digest = sha256(material.encode("utf-8")).hexdigest()
    return f"inbound:v1:{channel}:{source_name}:{digest}"


def _stable_inbound_source(inbound: InboundIdempotencyInput) -> tuple[str, str]:
    if inbound.channel_message_id and inbound.channel_message_id.strip():
        return "channel_message_id", inbound.channel_message_id.strip()
    if inbound.provided_idempotency_key and inbound.provided_idempotency_key.strip():
        return "provided_idempotency_key", inbound.provided_idempotency_key.strip()
    raise ValueError("stable inbound identifier is required")


def _normalized_required(field_name: str, value: str) -> str:
    normalized = value.strip().lower()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _validate_lock_key(field_name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty")
