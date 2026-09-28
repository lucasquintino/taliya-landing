import pytest

from app.domains.taliya_commercial.context import TaliyaCommercialContext
from app.domains.taliya_commercial.tools import pause_for_human, resume_from_human
from app.runtime.runner import run_agent_turn
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import InMemoryMemoryStore

pytestmark = pytest.mark.legacy_runner_reference


def _request(
    conversation_id: str, text: str, index: int = 1, metadata: dict | None = None
) -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": conversation_id,
                "lead_id": f"lead_{conversation_id}",
                "source": "taliya_whatsapp",
            },
            "message": {
                "idempotency_key": f"wa:{conversation_id}:{index}",
                "type": "text",
                "text": text,
            },
            "sender": {},
            "metadata": metadata or {},
        }
    )


@pytest.mark.asyncio
async def test_pause_and_resume_tools_persist_handoff_status_idempotently():
    store = InMemoryMemoryStore()
    context = TaliyaCommercialContext(
        conversation_id="conv_tool_handoff", lead_id="lead_1", memory_store=store
    )

    first = await pause_for_human(
        context,
        idempotency_key="handoff:conv_tool_handoff:pause",
        reason="operator_pause",
    )
    second = await pause_for_human(
        context,
        idempotency_key="handoff:conv_tool_handoff:pause",
        reason="different_reason",
    )
    resumed = await resume_from_human(
        context,
        idempotency_key="handoff:conv_tool_handoff:resume",
    )

    handoffs = await store.list_handoffs("conv_tool_handoff")
    assert first == second
    assert first["status"] == "active"
    assert resumed["status"] == "resumed"
    assert [handoff["status"] for handoff in handoffs] == ["active", "resumed"]
    assert (await store.count_tool_calls("handoff:conv_tool_handoff:pause")) == 1


@pytest.mark.asyncio
async def test_lead_human_request_pauses_subsequent_automation_without_reply():
    store = InMemoryMemoryStore()
    first = await run_agent_turn(
        _request("conv_handoff_runtime", "quero falar com uma pessoa", 1),
        memory_store=store,
        provider="mock",
        model="gpt-5.2",
    )
    second = await run_agent_turn(
        _request("conv_handoff_runtime", "oi, ainda estou aqui", 2),
        memory_store=store,
        provider="mock",
        model="gpt-5.2",
    )

    state = await store.load_state("conv_handoff_runtime", "taliya_commercial")
    events = await store.list_events("conv_handoff_runtime")

    assert first.status == "human_paused"
    assert first.output.messages
    assert second.status == "human_paused"
    assert second.output.messages == []
    assert second.output.handoff is not None
    assert second.output.handoff.status == "active"
    assert state is not None
    assert state.human_status == "active"
    assert any(
        event.type == "guardrail" and event.agent == "taliya_commercial_handoff_agent"
        for event in events
    )


@pytest.mark.asyncio
async def test_operator_runtime_control_can_resume_after_pause():
    store = InMemoryMemoryStore()
    await run_agent_turn(
        _request("conv_operator_resume", "quero humano", 1),
        memory_store=store,
        provider="mock",
        model="gpt-5.2",
    )
    resumed = await run_agent_turn(
        _request(
            "conv_operator_resume",
            "operator resume",
            2,
            {"runtime_control": {"action": "resume_human", "reason": "operator_resume"}},
        ),
        memory_store=store,
        provider="mock",
        model="gpt-5.2",
    )
    next_turn = await run_agent_turn(
        _request("conv_operator_resume", "quanto custa?", 3),
        memory_store=store,
        provider="mock",
        model="gpt-5.2",
    )

    assert resumed.output.handoff is not None
    assert resumed.output.handoff.status == "resumed"
    assert next_turn.status == "succeeded"
    assert next_turn.output.messages
    assert next_turn.current_agent == "taliya_commercial_product_agent"
