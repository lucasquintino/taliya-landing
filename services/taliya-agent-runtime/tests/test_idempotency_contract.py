import pytest

from app.shared.memory.postgres import InMemoryMemoryStore


@pytest.mark.asyncio
async def test_idempotent_tool_executes_once_for_same_key():
    store = InMemoryMemoryStore()
    calls = 0

    async def action():
        nonlocal calls
        calls += 1
        return {"ok": True}

    first = await store.run_idempotent_tool("tool:1", action)
    second = await store.run_idempotent_tool("tool:1", action)

    assert first == second
    assert calls == 1
    assert await store.count_tool_calls("tool:1") == 1
