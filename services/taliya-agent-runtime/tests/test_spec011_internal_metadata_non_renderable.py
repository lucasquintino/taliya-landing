from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.schemas import ProductKnowledgeRef, TurnFact
from app.runtime.events import RuntimeEvent
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState


def _request_with_internal_labels() -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_internal_1",
                "lead_id": "lead_internal_1",
                "channel_conversation_id": "wa_internal_1",
                "source": "lead came from the site",
                "entry_intent": "Reliable profile first name",
            },
            "message": {
                "idempotency_key": "wa:conv_internal_1:1",
                "channel_message_id": "wamid_internal_1",
                "type": "text",
                "text": "Oi",
            },
            "sender": {
                "name": "Reliable profile first name: Ana",
                "whatsapp_phone": "+5511999999999",
            },
            "metadata": {
                "page_path": "/pilates",
                "utm_source": "instagram",
                "runtime_control": {
                    "debug_label": "lead came from the site",
                    "profile_label": "Reliable profile first name",
                },
            },
        }
    )


def _state_with_runtime_debug_memory() -> RuntimeState:
    return RuntimeState(
        conversation_id="conv_internal_1",
        agent_key="taliya_commercial",
        current_agent_name="taliya_commercial_product_agent",
        summary="Lead abriu conversa pelo WhatsApp da Taliya.",
        input_items=[{"role": "user", "content": "Oi", "id": "m1"}],
        lead_facts=[
            {
                "key": "main_pain",
                "value": "agenda baguncada",
                "confidence": "high",
                "evidence": ["m1"],
            }
        ],
        diagnostic={"status": "not_started", "ledger": []},
        waitlist={"status": "none"},
        demo={"status": "not_offered"},
        human_status="none",
    )


def test_channel_source_metadata_is_context_only_and_non_renderable() -> None:
    context = build_turn_context(
        turn_id="turn_internal_1",
        request=_request_with_internal_labels(),
        state=_state_with_runtime_debug_memory(),
        recent_events=[],
    )

    channel_facts = [fact for fact in context.facts if fact.source == "channel_metadata"]

    assert channel_facts
    assert all(fact.renderable is False for fact in channel_facts)
    assert {
        fact.value
        for fact in channel_facts
        if fact.value in {"lead came from the site", "Reliable profile first name"}
    } == {"lead came from the site", "Reliable profile first name"}

    with pytest.raises(ValidationError):
        TurnFact.model_validate(
            {
                "key": "profile_name",
                "value": "Reliable profile first name: Ana",
                "source": "channel_metadata",
                "reliability": "channel_provided",
                "renderable": True,
                "evidence": ["sender.name"],
            }
        )


def test_runtime_control_and_debug_event_metadata_do_not_enter_customer_context() -> None:
    context = build_turn_context(
        turn_id="turn_internal_2",
        request=_request_with_internal_labels(),
        state=_state_with_runtime_debug_memory(),
        recent_events=[
            RuntimeEvent(
                run_id="run_internal_1",
                conversation_id="conv_internal_1",
                agent_key="taliya_commercial",
                type="message",
                agent="taliya_commercial",
                content="Mensagem enviada pela Taliya",
                metadata={
                    "role": "assistant",
                    "template_id": "opening.cold_greeting",
                    "internal_debug": "lead came from the site",
                    "profile_label": "Reliable profile first name",
                },
                timestamp_ms=100,
            )
        ],
    )

    assert "runtime_control" not in context.sales_inbox_inputs
    assert all("runtime_control" not in fact.evidence for fact in context.facts)
    assert all("internal_debug" not in item for item in context.recent_transcript)
    assert all("profile_label" not in item for item in context.recent_transcript)
    assert context.recent_transcript[-1]["template_id"] == "opening.cold_greeting"


def test_product_knowledge_refs_are_source_material_not_renderable_variables() -> None:
    context = build_turn_context(
        turn_id="turn_internal_3",
        request=_request_with_internal_labels(),
        state=_state_with_runtime_debug_memory(),
        recent_events=[],
        product_knowledge_keys=["prices"],
        spec006_contract_keys=["product_positioning"],
    )

    assert context.product_knowledge
    assert all(ref.renderable is False for ref in context.product_knowledge)

    with pytest.raises(ValidationError):
        ProductKnowledgeRef.model_validate(
            {
                "key": "prices",
                "source": "official_product_knowledge",
                "version": "pk-test",
                "value": {"base": 497},
                "excerpt": "base: 497",
                "renderable": True,
                "evidence": ["product_knowledge.prices"],
            }
        )
