from __future__ import annotations

from app.core.taliya_commercial.context_builder import build_turn_context
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState
from app.shared.product_knowledge.source import get_product_knowledge_source


def _request(text: str) -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {
                "conversation_id": "conv_pk_1",
                "lead_id": "lead_pk_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "widget:conv_pk_1:1",
                "type": "text",
                "text": text,
            },
            "sender": {},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _state() -> RuntimeState:
    return RuntimeState(
        conversation_id="conv_pk_1",
        agent_key="taliya_commercial",
        current_agent_name="taliya_commercial_product_agent",
        summary="Lead quer entender a Taliya.",
        diagnostic={"status": "not_started", "ledger": []},
        waitlist={"status": "none"},
        demo={"status": "not_offered"},
    )


def test_context_builder_retrieves_official_product_knowledge_as_context() -> None:
    official_source = get_product_knowledge_source()
    context = build_turn_context(
        turn_id="turn_pk_1",
        request=_request("quanto custa?"),
        state=_state(),
        recent_events=[],
        product_knowledge_keys=["prices", "links", "checkout_status"],
    )

    refs = {ref.key: ref for ref in context.product_knowledge}

    assert refs["prices"].source == "official_product_knowledge"
    assert refs["prices"].version == official_source.version
    assert refs["prices"].value == official_source.query(["prices"])["facts"]["prices"]
    assert refs["prices"].missing is False
    assert refs["prices"].evidence == ["product_knowledge.prices"]
    assert refs["links"].value == official_source.query(["links"])["facts"]["links"]
    assert refs["checkout_status"].value == official_source.checkout_status


def test_context_builder_records_missing_product_facts_explicitly() -> None:
    context = build_turn_context(
        turn_id="turn_pk_missing",
        request=_request("integra com meu calendario?"),
        state=_state(),
        recent_events=[],
        product_knowledge_keys=["integration_calendar"],
    )

    official_refs = [
        ref for ref in context.product_knowledge if ref.source == "official_product_knowledge"
    ]

    assert len(official_refs) == 1
    missing_ref = official_refs[0]
    assert missing_ref.key == "integration_calendar"
    assert missing_ref.source == "official_product_knowledge"
    assert missing_ref.missing is True
    assert missing_ref.value is None
    assert missing_ref.excerpt is None


def test_default_product_knowledge_is_stable_context_not_commercial_routing() -> None:
    price_context = build_turn_context(
        turn_id="turn_price",
        request=_request("quanto custa?"),
        state=_state(),
        recent_events=[],
    )
    pain_context = build_turn_context(
        turn_id="turn_pain",
        request=_request("minha agenda e reposicoes estao baguncadas"),
        state=_state(),
        recent_events=[],
    )

    price_keys = [ref.key for ref in price_context.product_knowledge]
    pain_keys = [ref.key for ref in pain_context.product_knowledge]

    assert price_keys == pain_keys
    assert "prices" in price_keys
    assert "unsupported_claims" in price_keys
    assert {
        "how_it_works",
        "routine_areas",
        "whatsapp_scope",
        "integration_scope",
        "comparison_spreadsheet",
        "comparison_management_system",
        "security_and_data",
        "out_of_profile",
    }.issubset(price_keys)
    assert price_context.diagnostic_ledger == pain_context.diagnostic_ledger
    assert price_context.waitlist_state == pain_context.waitlist_state
    assert price_context.demo_state == pain_context.demo_state
    assert price_context.handoff_state == pain_context.handoff_state
    assert not any(
        hasattr(ref, "route") or hasattr(ref, "template_id")
        for ref in price_context.product_knowledge
    )
