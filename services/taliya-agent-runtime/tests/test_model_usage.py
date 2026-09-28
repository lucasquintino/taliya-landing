import pytest

from app.runtime.runner import run_agent_turn
from app.runtime.schemas import AgentRunRequest
from app.runtime.usage import (
    build_usage_record,
    cap_status_for_cost,
    estimate_cost_usd,
    usage_from_tokens,
)
from app.settings import get_settings
from app.shared.memory.postgres import InMemoryMemoryStore, RuntimeState

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


def test_usage_record_tracks_budget_and_cap_status():
    usage = usage_from_tokens("gpt-5.2", 1000, 200)
    record = build_usage_record(
        run_id="run_usage",
        conversation_id="conv_usage",
        agent_key="taliya_commercial",
        operation="runner",
        usage=usage,
        budget_before=0.048,
        review_cost_usd=0.05,
        hard_cost_cap_usd=0.15,
    )

    assert record.budget_after > record.budget_before
    assert record.cap_status == "review"
    assert (
        cap_status_for_cost(0.151, review_cost_usd=0.05, hard_cost_cap_usd=0.15)
        == "hard_cap_blocked"
    )


def test_current_gpt_54_mini_pricing_table_is_used():
    usage = usage_from_tokens("gpt-5.4-mini", 1_000_000, 1_000_000)

    assert usage.cost_usd == 5.25


def test_luna_pricing_table_is_cache_aware():
    assert estimate_cost_usd(
        "gpt-5.6-luna",
        1_000_000,
        1_000_000,
        cached_input_tokens=500_000,
    ) == pytest.approx(6.55)


def test_luna_pricing_includes_billed_cache_writes():
    assert estimate_cost_usd(
        "gpt-5.6-luna",
        1_000_000,
        1_000_000,
        cached_input_tokens=250_000,
        cache_write_input_tokens=500_000,
    ) == pytest.approx(6.9)


def test_unknown_model_pricing_fails_closed():
    with pytest.raises(ValueError, match="No recorded pricing"):
        estimate_cost_usd("gpt-unpriced-model", 1_000, 200)


@pytest.mark.asyncio
async def test_runner_records_model_usage_and_tool_summaries():
    store = InMemoryMemoryStore()
    response = await run_agent_turn(
        _request("conv_usage_runtime", "quanto custa?"),
        memory_store=store,
        provider="mock",
        model="gpt-5.2",
    )

    usage_records = await store.list_model_usage("conv_usage_runtime")
    tool_summaries = await store.list_tool_summaries("conv_usage_runtime")

    assert response.output.usage.cost_usd > 0
    assert usage_records
    assert usage_records[0]["operation"] == "runner"
    assert tool_summaries
    assert tool_summaries[0]["tool_name"] == "get_product_knowledge"


@pytest.mark.asyncio
async def test_runner_hard_cost_cap_suppresses_automatic_reply(monkeypatch):
    monkeypatch.setenv("TALIYA_AGENT_HARD_COST_CAP_USD", "0.01")
    get_settings.cache_clear()
    store = InMemoryMemoryStore()
    await store.save_state(
        RuntimeState(
            conversation_id="conv_cost_cap",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_entry_agent",
            cost_usd=0.02,
        )
    )

    response = await run_agent_turn(
        _request("conv_cost_cap", "quanto custa?"),
        memory_store=store,
        provider="mock",
        model="gpt-5.2",
    )
    guardrails = await store.list_guardrail_events("conv_cost_cap")

    assert response.status == "cost_capped"
    assert response.output.messages == []
    assert response.output.handoff is not None
    assert response.output.handoff.status == "active"
    assert response.output.safety_flags == ["cost_cap_reached", "human_follow_up_required"]
    assert guardrails
    get_settings.cache_clear()
