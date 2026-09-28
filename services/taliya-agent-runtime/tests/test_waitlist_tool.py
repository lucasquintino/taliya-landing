import pytest

from app.domains.taliya_commercial.guardrails import validate_waitlist_no_checkout
from app.runtime.runner import run_agent_turn
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import InMemoryMemoryStore

pytestmark = pytest.mark.legacy_runner_reference


def _request(conversation_id: str, text: str, index: int = 1) -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {"conversation_id": conversation_id, "source": "pilates_landing"},
            "message": {
                "idempotency_key": f"widget:{conversation_id}:{index}",
                "type": "text",
                "text": text,
            },
            "sender": {},
            "metadata": {},
        }
    )


@pytest.mark.asyncio
async def test_cold_greeting_does_not_offer_waitlist():
    store = InMemoryMemoryStore()
    response = await run_agent_turn(
        _request("conv_wait_cold", "oi"), memory_store=store, provider="mock", model="gpt-5.2"
    )

    assert response.output.waitlist_action is None
    assert "lista de espera" not in response.output.messages[0].text.lower()


@pytest.mark.asyncio
async def test_buying_intent_offers_waitlist_without_checkout():
    store = InMemoryMemoryStore()
    response = await run_agent_turn(
        _request("conv_wait_buy", "Quero assinar agora"),
        memory_store=store,
        provider="mock",
        model="gpt-5.2",
    )
    waitlist = await store.get_waitlist("conv_wait_buy")

    assert response.current_agent == "taliya_commercial_waitlist_agent"
    assert response.output.waitlist_action is not None
    assert response.output.waitlist_action.status == "offered"
    assert waitlist is not None
    assert waitlist["status"] == "offered"
    assert "checkout" not in response.output.messages[0].text.lower()


@pytest.mark.asyncio
async def test_waitlist_acceptance_without_details_stays_pending_details():
    store = InMemoryMemoryStore()
    await run_agent_turn(
        _request("conv_wait_join", "Quero assinar agora", 1),
        memory_store=store,
        provider="mock",
        model="gpt-5.2",
    )
    response = await run_agent_turn(
        _request("conv_wait_join", "Pode colocar meu studio", 2),
        memory_store=store,
        provider="mock",
        model="gpt-5.2",
    )
    waitlist = await store.get_waitlist("conv_wait_join")

    assert response.output.waitlist_action is not None
    assert response.output.waitlist_action.status == "pending_details"
    assert waitlist is not None
    assert waitlist["status"] == "pending_details"
    assert waitlist["missing_fields"] == ["studio_name", "city_state"]


@pytest.mark.asyncio
async def test_waitlist_join_after_offer_with_contact_and_context_is_idempotent():
    store = InMemoryMemoryStore()
    await run_agent_turn(
        _request("conv_wait_ready", "Quero assinar agora", 1),
        memory_store=store,
        provider="mock",
        model="gpt-5.2",
    )
    ready_request = _request("conv_wait_ready", "Pode colocar o Studio Viva em Vitoria", 2)
    ready_request.sender.email = "ana@example.com"
    response = await run_agent_turn(
        ready_request,
        memory_store=store,
        provider="mock",
        model="gpt-5.2",
    )
    waitlist = await store.get_waitlist("conv_wait_ready")

    assert response.output.waitlist_action is not None
    assert response.output.waitlist_action.status == "joined"
    assert waitlist is not None
    assert waitlist["status"] == "joined"


def test_waitlist_no_checkout_guardrail_blocks_checkout_language():
    result = validate_waitlist_no_checkout(
        "Posso te colocar na lista, sem link de checkout por enquanto."
    )
    assert result.passed is False
