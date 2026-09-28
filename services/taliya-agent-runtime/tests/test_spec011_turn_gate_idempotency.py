from __future__ import annotations

from dataclasses import asdict, fields
from datetime import UTC, datetime

import pytest

from app.core.taliya_commercial.turn_gate import (
    InboundIdempotencyInput,
    InboundIdempotencyManager,
    InboundIdempotencyResult,
    stable_inbound_idempotency_key,
)


def _inbound(**overrides: str | None) -> InboundIdempotencyInput:
    values = {
        "channel": "whatsapp",
        "conversation_id": "conv_1",
        "channel_conversation_id": "wa_thread_1",
        "channel_message_id": "wamid_123",
        "provided_idempotency_key": "adapter_request_a",
    }
    values.update(overrides)
    return InboundIdempotencyInput(**values)


def test_stable_key_prefers_channel_message_id_over_request_id() -> None:
    first_delivery = _inbound(provided_idempotency_key="adapter_request_a")
    provider_retry = _inbound(provided_idempotency_key="adapter_request_b")

    first_key = stable_inbound_idempotency_key(first_delivery)
    retry_key = stable_inbound_idempotency_key(provider_retry)

    assert first_key == retry_key
    assert first_key.startswith("inbound:v1:whatsapp:channel_message_id:")
    assert "wamid_123" not in first_key
    assert "wa_thread_1" not in first_key


def test_stable_key_uses_adapter_key_only_when_provider_message_id_is_missing() -> None:
    first_key = stable_inbound_idempotency_key(
        _inbound(
            channel="widget",
            conversation_id="widget_conv_1",
            channel_conversation_id="widget_session_1",
            channel_message_id=None,
            provided_idempotency_key="widget_message_1",
        )
    )
    retry_key = stable_inbound_idempotency_key(
        _inbound(
            channel="widget",
            conversation_id="widget_conv_1",
            channel_conversation_id="widget_session_1",
            channel_message_id=None,
            provided_idempotency_key="widget_message_1",
        )
    )
    different_adapter_message = stable_inbound_idempotency_key(
        _inbound(
            channel="widget",
            conversation_id="widget_conv_1",
            channel_conversation_id="widget_session_1",
            channel_message_id=None,
            provided_idempotency_key="widget_message_2",
        )
    )

    assert first_key == retry_key
    assert first_key.startswith("inbound:v1:widget:provided_idempotency_key:")
    assert first_key != different_adapter_message


def test_stable_key_separates_channel_conversations() -> None:
    first_key = stable_inbound_idempotency_key(_inbound(channel_conversation_id="wa_thread_1"))
    second_key = stable_inbound_idempotency_key(_inbound(channel_conversation_id="wa_thread_2"))

    assert first_key != second_key


def test_stable_key_requires_a_stable_message_identifier() -> None:
    with pytest.raises(ValueError, match="stable inbound identifier"):
        stable_inbound_idempotency_key(
            _inbound(channel_message_id=None, provided_idempotency_key=None)
        )


def test_stable_key_rejects_channel_outside_scope() -> None:
    with pytest.raises(ValueError, match="channel"):
        stable_inbound_idempotency_key(_inbound(channel="email"))


def test_idempotency_claim_returns_duplicate_reference_without_reclaiming() -> None:
    manager = InboundIdempotencyManager(now=lambda: datetime(2026, 5, 30, 12, 0, tzinfo=UTC))
    first_delivery = _inbound(provided_idempotency_key="adapter_request_a")
    provider_retry = _inbound(provided_idempotency_key="adapter_request_b")

    first = manager.claim(first_delivery, turn_id="turn_1")
    duplicate = manager.claim(provider_retry, turn_id="turn_retry")

    assert first.status == "new"
    assert first.accepted_turn_id == "turn_1"
    assert first.duplicate_of_turn_id is None
    assert duplicate.status == "duplicate"
    assert duplicate.accepted_turn_id is None
    assert duplicate.duplicate_of_turn_id == "turn_1"
    assert duplicate.idempotency_key == first.idempotency_key


def test_idempotency_result_has_only_operational_fields() -> None:
    input_field_names = {field.name for field in fields(InboundIdempotencyInput)}
    result_field_names = {field.name for field in fields(InboundIdempotencyResult)}
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
    result = InboundIdempotencyResult(
        status="new",
        idempotency_key="inbound:v1:whatsapp:channel_message_id:abc",
        conversation_id="conv_1",
        accepted_turn_id="turn_1",
    )

    assert forbidden_decision_fields.isdisjoint(input_field_names)
    assert forbidden_decision_fields.isdisjoint(result_field_names)
    assert forbidden_decision_fields.isdisjoint(asdict(result))
