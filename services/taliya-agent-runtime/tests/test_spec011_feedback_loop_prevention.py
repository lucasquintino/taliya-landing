from __future__ import annotations

from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.sales_inbox_projection import (
    export_projection_identity_facts_for_context,
)
from app.core.taliya_commercial.schemas import SalesInboxProjection
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState


def _request() -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_feedback_loop_1",
                "lead_id": "lead_feedback_loop_1",
                "channel_conversation_id": "wa_feedback_loop_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_feedback_loop_1:1",
                "channel_message_id": "wamid_feedback_loop_1",
                "type": "text",
                "text": "oi",
            },
            "sender": {"name": "Ana Canal"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _projection() -> SalesInboxProjection:
    return SalesInboxProjection.model_validate(
        {
            "conversation_id": "conv_feedback_loop_1",
            "lead_id": "lead_feedback_loop_1",
            "commercial_stage": "product_answered",
            "summary": "Lead identificada.",
            "diagnostic_status": "not_started",
            "waitlist_status": "none",
            "handoff_status": "none",
            "identity": [
                {
                    "key": "person_name",
                    "value": "Ana",
                    "source": "customer_provided",
                    "verified": True,
                },
                {
                    "key": "profile_name",
                    "value": "Ana Canal",
                    "source": "channel_provided",
                    "verified": False,
                },
                {
                    "key": "phone",
                    "value": "+5511999999999",
                    "source": "unverified",
                    "verified": False,
                },
            ],
            "fields": {
                "template_ids": ["product.overview_short"],
                "validator_status": "passed",
                "validator_final_disposition": "accepted",
                "source_labels": {"state_source": "accepted_decision"},
                "operator_next_action": "none",
            },
        }
    )


def test_projection_identity_reenters_context_as_unverified_projection_facts() -> None:
    projection = _projection()
    exported_facts = export_projection_identity_facts_for_context(projection)
    context = build_turn_context(
        turn_id="turn_feedback_loop_1",
        request=_request(),
        state=RuntimeState(
            conversation_id="conv_feedback_loop_1",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_product_agent",
            lead_facts=exported_facts,
        ),
        recent_events=[],
    )

    projected_facts = {
        fact.key: fact
        for fact in context.facts
        if fact.source == "sales_inbox_projection"
    }

    assert exported_facts
    assert projected_facts["person_name"].reliability == "unverified"
    assert projected_facts["profile_name"].reliability == "unverified"
    assert projected_facts["phone"].reliability == "unverified"
    assert all(fact.renderable is False for fact in projected_facts.values())
    assert all(fact.confidence == "low" for fact in projected_facts.values())
    assert all(
        fact.evidence == [f"sales_inbox_projection.identity.{fact.key}"]
        for fact in projected_facts.values()
    )
    assert all(item["source"] == "sales_inbox_projection" for item in exported_facts)
    assert all(item["reliability"] == "unverified" for item in exported_facts)
    assert all(item["confidence"] == "low" for item in exported_facts)
