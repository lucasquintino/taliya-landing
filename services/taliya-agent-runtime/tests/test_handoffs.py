import pytest

from app.runtime.runner import run_agent_turn
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import InMemoryMemoryStore

pytestmark = pytest.mark.legacy_runner_reference


@pytest.mark.asyncio
async def test_taliya_commercial_handoff_agent_sets_pause_output_and_event():
    store = InMemoryMemoryStore()
    request = AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {"conversation_id": "conv_handoff", "source": "taliya_whatsapp"},
            "message": {
                "idempotency_key": "wa:conv_handoff:1",
                "type": "text",
                "text": "quero falar com uma pessoa",
            },
            "sender": {},
            "metadata": {},
        }
    )

    response = await run_agent_turn(request, memory_store=store, provider="mock", model="gpt-5.2")
    events = await store.list_events("conv_handoff")
    state = await store.load_state("conv_handoff", "taliya_commercial")

    assert response.status == "human_paused"
    assert response.current_agent == "taliya_commercial_handoff_agent"
    assert response.output.handoff is not None
    assert response.output.handoff.status == "requested"
    assert any(
        event.type == "handoff"
        and event.metadata["target_agent"] == "taliya_commercial_handoff_agent"
        for event in events
    )
    assert state is not None
    assert state.human_status == "active"
