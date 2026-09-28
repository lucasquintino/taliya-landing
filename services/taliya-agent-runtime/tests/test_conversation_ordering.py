import pytest

from app.shared.memory.postgres import InMemoryMemoryStore, RuntimeState


@pytest.mark.asyncio
async def test_conversation_state_preserves_message_order():
    store = InMemoryMemoryStore()
    state = RuntimeState(
        conversation_id="conv_order",
        agent_key="taliya_commercial",
        current_agent_name="taliya_commercial_entry_agent",
        input_items=[
            {"id": "msg_1", "role": "user", "content": "oi"},
            {"id": "msg_2", "role": "user", "content": "quanto custa?"},
        ],
    )

    await store.save_state(state)
    loaded = await store.load_state("conv_order", "taliya_commercial")

    assert loaded is not None
    assert [item["id"] for item in loaded.input_items] == ["msg_1", "msg_2"]
