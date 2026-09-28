from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.schemas import TurnFact
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState


def _request_with_channel_identity() -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_identity_1",
                "lead_id": "lead_identity_1",
                "channel_conversation_id": "wa_identity_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_identity_1:1",
                "channel_message_id": "wamid_identity_1",
                "type": "text",
                "text": "Oi",
            },
            "sender": {
                "name": "Reliable profile first name: Ana",
                "whatsapp_phone": "+5511999999999",
                "email": "perfil@canal.example",
            },
            "metadata": {"page_path": "/pilates"},
        }
    )


def _state_with_identity_sources() -> RuntimeState:
    return RuntimeState(
        conversation_id="conv_identity_1",
        agent_key="taliya_commercial",
        current_agent_name="taliya_commercial_product_agent",
        lead_facts=[
            {
                "key": "first_name",
                "value": "Ana",
                "source": "memory",
                "reliability": "customer_provided",
                "confidence": "high",
                "evidence": ["message:m2"],
            },
            {
                "key": "email",
                "value": "ana@studio.com",
                "source": "operator",
                "reliability": "operator_provided",
                "confidence": "high",
                "evidence": ["operator:manual_update"],
            },
            {
                "key": "first_name",
                "value": "Reliable profile first name: Ana",
                "source": "sales_inbox_projection",
                "reliability": "inferred",
                "confidence": "low",
                "evidence": ["sales_inbox:profile_name_guess"],
            },
            {
                "key": "whatsapp_phone",
                "value": "+5511888888888",
                "source": "sales_inbox_projection",
                "reliability": "unverified",
                "confidence": "low",
                "evidence": ["sales_inbox:last_seen_phone"],
            },
        ],
        diagnostic={"status": "not_started", "ledger": []},
        waitlist={"status": "none"},
        demo={"status": "not_offered"},
    )


def _facts_by_key_and_value(context_facts: list[TurnFact]) -> dict[tuple[str, str], TurnFact]:
    return {(fact.key, str(fact.value)): fact for fact in context_facts}


def test_identity_and_contact_facts_keep_reliability_source_labels() -> None:
    context = build_turn_context(
        turn_id="turn_identity_1",
        request=_request_with_channel_identity(),
        state=_state_with_identity_sources(),
        recent_events=[],
    )

    facts = _facts_by_key_and_value(context.facts)

    channel_profile = facts[("profile_name", "Reliable profile first name: Ana")]
    assert channel_profile.source == "channel_metadata"
    assert channel_profile.reliability == "channel_provided"
    assert channel_profile.renderable is False

    customer_name = facts[("first_name", "Ana")]
    assert customer_name.source == "memory"
    assert customer_name.reliability == "customer_provided"
    assert customer_name.confidence == "high"
    assert customer_name.evidence == ["message:m2"]

    operator_email = facts[("email", "ana@studio.com")]
    assert operator_email.source == "operator"
    assert operator_email.reliability == "operator_provided"
    assert operator_email.evidence == ["operator:manual_update"]

    inferred_profile_name = facts[("first_name", "Reliable profile first name: Ana")]
    assert inferred_profile_name.source == "sales_inbox_projection"
    assert inferred_profile_name.reliability == "inferred"
    assert inferred_profile_name.confidence == "low"

    unverified_phone = facts[("whatsapp_phone", "+5511888888888")]
    assert unverified_phone.source == "sales_inbox_projection"
    assert unverified_phone.reliability == "unverified"

    assert not any(
        fact.value == "Reliable profile first name: Ana"
        and fact.reliability == "customer_provided"
        for fact in context.facts
    )


def test_identity_memory_fact_without_evidence_is_not_confirmed_customer_identity() -> None:
    state = RuntimeState(
        conversation_id="conv_identity_1",
        agent_key="taliya_commercial",
        current_agent_name="taliya_commercial_product_agent",
        lead_facts=[
            {
                "key": "first_name",
                "value": "Ana",
                "source": "memory",
                "reliability": "customer_provided",
                "confidence": "medium",
                "evidence": [],
            }
        ],
    )

    context = build_turn_context(
        turn_id="turn_identity_2",
        request=_request_with_channel_identity(),
        state=state,
        recent_events=[],
    )

    facts = _facts_by_key_and_value(context.facts)
    first_name = facts[("first_name", "Ana")]

    assert first_name.source == "memory"
    assert first_name.reliability == "unverified"
    assert first_name.renderable is False


def test_identity_contact_schema_rejects_invalid_reliable_source_pairs() -> None:
    with pytest.raises(ValidationError):
        TurnFact.model_validate(
            {
                "key": "first_name",
                "value": "Ana",
                "source": "channel_metadata",
                "reliability": "customer_provided",
                "renderable": False,
                "evidence": ["sender.name"],
            }
        )

    with pytest.raises(ValidationError):
        TurnFact.model_validate(
            {
                "key": "email",
                "value": "ana@studio.com",
                "source": "operator",
                "reliability": "customer_provided",
                "renderable": False,
                "evidence": ["operator:manual_update"],
            }
        )

    with pytest.raises(ValidationError):
        TurnFact.model_validate(
            {
                "key": "first_name",
                "value": "Ana",
                "source": "memory",
                "reliability": "customer_provided",
                "renderable": False,
                "evidence": [],
            }
        )

    with pytest.raises(ValidationError):
        TurnFact.model_validate(
            {
                "key": "whatsapp_phone",
                "value": "+5511888888888",
                "source": "sales_inbox_projection",
                "reliability": "customer_provided",
                "renderable": False,
                "evidence": ["sales_inbox:last_seen_phone"],
            }
        )
