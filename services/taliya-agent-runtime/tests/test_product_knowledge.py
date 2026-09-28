import pytest

from app.runtime.runner import run_agent_turn
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import InMemoryMemoryStore
from app.shared.product_knowledge.source import get_product_knowledge_source

pytestmark = pytest.mark.legacy_runner_reference


def test_product_knowledge_contains_official_prices_and_links():
    source = get_product_knowledge_source()

    prices = {plan.id: plan.monthly_price_brl for plan in source.plans}

    assert source.scope == "taliya_commercial"
    assert prices["base"] == 197
    assert prices["one_agent"] == 497
    assert prices["three_agents"] == 897
    assert prices["seven_agents"] == 1497
    assert source.links["plans"] == "https://www.taliya.com.br/pilates/planos"
    assert source.links["demonstration"] == "https://www.taliya.com.br/pilates/planos/demonstracao"


def test_product_knowledge_keeps_checkout_unavailable_until_configured():
    source = get_product_knowledge_source()

    assert source.checkout_status == "unavailable"
    assert "checkout" in source.unsupported_claims


def test_product_knowledge_query_returns_missing_facts_explicitly():
    source = get_product_knowledge_source()
    result = source.query(["prices", "integration_calendar"])

    assert result["source_version"] == source.version
    assert "prices" in result["facts"]
    assert "integration_calendar" in result["missing_facts"]


def test_product_followup_delta_knowledge_keys_exist_and_are_selective():
    source = get_product_knowledge_source()
    requested = [
        "how_it_works",
        "routine_areas",
        "whatsapp_scope",
        "integration_scope",
        "comparison_spreadsheet",
        "comparison_management_system",
        "security_and_data",
        "availability_and_onboarding",
        "out_of_profile",
    ]

    result = source.query(requested)

    assert result["missing_facts"] == []
    assert set(requested).issubset(result["facts"])
    assert "WhatsApp Business" in result["facts"]["whatsapp_scope"]
    assert "Instagram integration" in result["facts"]["integration_scope"]
    assert "CPF" in result["facts"]["security_and_data"]
    default_result = source.query()
    assert "how_it_works" not in default_result["facts"]


@pytest.mark.asyncio
async def test_price_answer_persists_product_source_version():
    store = InMemoryMemoryStore()
    request = AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {"conversation_id": "conv_product", "source": "pilates_landing"},
            "message": {
                "idempotency_key": "widget:conv_product:1",
                "type": "text",
                "text": "quanto custa?",
            },
            "sender": {},
            "metadata": {},
        }
    )

    response = await run_agent_turn(request, memory_store=store, provider="mock", model="gpt-5.2")
    state = await store.load_state("conv_product", "taliya_commercial")

    assert response.output.sources[0].version == "taliya-commercial-2026-05-22"
    assert state is not None
    assert state.product_source_version == "taliya-commercial-2026-05-22"


@pytest.mark.asyncio
async def test_price_first_answers_and_hooks_diagnostic_with_greeting():
    store = InMemoryMemoryStore()
    request = AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {"conversation_id": "conv_price_hook", "source": "pilates_landing"},
            "message": {
                "idempotency_key": "widget:conv_price_hook:1",
                "type": "text",
                "text": "quanto custa?",
            },
            "sender": {"name": "Ana Paula"},
            "metadata": {},
        }
    )

    response = await run_agent_turn(request, memory_store=store, provider="mock", model="gpt-5.2")
    texts = [message.text for message in response.output.messages]

    assert texts[0].startswith("Oi, Ana, tudo bem? Hoje os planos são")
    assert any("diagnóstico gratuito" in text for text in texts)
    assert any("algum dos nossos planos te atenderia" in text for text in texts)


@pytest.mark.asyncio
async def test_plan_fit_uses_owner_copy_without_repeated_diagnostic_question():
    store = InMemoryMemoryStore()
    request = AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {"conversation_id": "conv_plan_fit", "source": "pilates_landing"},
            "message": {
                "idempotency_key": "widget:conv_plan_fit:1",
                "type": "text",
                "text": "qual plano voce recomenda pra mim?",
            },
            "sender": {},
            "metadata": {},
        }
    )

    response = await run_agent_turn(request, memory_store=store, provider="mock", model="gpt-5.2")
    text = "\n".join(message.text for message in response.output.messages)

    assert "Oi, tudo bem? Para comparar plano sem chutar" in text
    assert "quais agentes fariam sentido" in text
    assert "O que você acha?" in text
    assert "Quer que eu faça esse diagnóstico?" not in text


@pytest.mark.asyncio
async def test_price_plus_pain_preserves_context_in_diagnostic_hook():
    store = InMemoryMemoryStore()
    request = AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {"conversation_id": "conv_price_pain", "source": "taliya_whatsapp"},
            "message": {
                "idempotency_key": "wa:conv_price_pain:1",
                "type": "text",
                "text": "tenho agenda e reposicoes meio perdidas, mas tambem queria saber preco",
            },
            "sender": {"whatsapp_phone": "+5511999999999"},
            "metadata": {},
        }
    )

    response = await run_agent_turn(request, memory_store=store, provider="mock", model="gpt-5.2")
    text = "\n".join(message.text for message in response.output.messages).lower()

    assert "r$ 197" in text
    assert "agenda" in text
    assert "reposi" in text
    assert "diagnóstico gratuito" in text


@pytest.mark.asyncio
async def test_post_waitlist_complete_price_does_not_repeat_status_or_all_plans():
    store = InMemoryMemoryStore()
    first = AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_post_wait_price",
                "source": "taliya_whatsapp",
            },
            "message": {
                "idempotency_key": "wa:conv_post_wait_price:1",
                "type": "text",
                "text": "quero contratar, como faco para entrar?",
            },
            "sender": {"whatsapp_phone": "+5511999999999"},
            "metadata": {},
        }
    )
    second = AgentRunRequest.model_validate(
        {
            **first.model_dump(),
            "message": {
                "idempotency_key": "wa:conv_post_wait_price:2",
                "type": "text",
                "text": "pode colocar o Studio Viva em Vitoria ES",
            },
        }
    )
    third = AgentRunRequest.model_validate(
        {
            **first.model_dump(),
            "message": {
                "idempotency_key": "wa:conv_post_wait_price:3",
                "type": "text",
                "text": "quanto custa o Completo?",
            },
        }
    )

    await run_agent_turn(first, memory_store=store, provider="mock", model="gpt-5.2")
    await run_agent_turn(second, memory_store=store, provider="mock", model="gpt-5.2")
    response = await run_agent_turn(third, memory_store=store, provider="mock", model="gpt-5.2")
    text = "\n".join(message.text for message in response.output.messages)

    assert "O Completo fica em R$ 1.497/mês." in text
    assert "Base R$ 197" not in text
    assert "continua registrado" not in text
