import pytest

from app.runtime.runner import run_agent_turn
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import InMemoryMemoryStore

pytestmark = pytest.mark.legacy_runner_reference


@pytest.mark.asyncio
async def test_runner_persists_tool_handoff_message_and_usage_events():
    store = InMemoryMemoryStore()
    request = AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {"conversation_id": "conv_events", "source": "pilates_landing"},
            "message": {
                "idempotency_key": "widget:conv_events:1",
                "type": "text",
                "text": "quanto custa e qual plano faz sentido?",
            },
            "sender": {},
            "metadata": {},
        }
    )

    response = await run_agent_turn(request, memory_store=store, provider="mock", model="gpt-5.2")
    events = await store.list_events("conv_events")
    event_types = [event.type for event in events]

    assert response.current_agent == "taliya_commercial_product_agent"
    assert "handoff" in event_types
    assert "tool_call" in event_types
    assert "message" in event_types
    assert "usage" in event_types
    assert any(event.content == "get_product_knowledge" for event in events)


@pytest.mark.asyncio
async def test_runner_updates_current_agent_and_input_history():
    store = InMemoryMemoryStore()
    request = AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {"conversation_id": "conv_state", "source": "taliya_whatsapp"},
            "message": {
                "idempotency_key": "wa:conv_state:1",
                "type": "text",
                "text": "tenho muita falta e reposicao baguncada",
            },
            "sender": {},
            "metadata": {},
        }
    )

    response = await run_agent_turn(request, memory_store=store, provider="mock", model="gpt-5.2")
    state = await store.load_state("conv_state", "taliya_commercial")

    assert response.current_agent == "taliya_commercial_diagnostic_agent"
    assert state is not None
    assert state.current_agent_name == "taliya_commercial_diagnostic_agent"
    assert state.input_items[-1]["content"] == "tenho muita falta e reposicao baguncada"
