from __future__ import annotations

import inspect
import os

import pytest

from app.core.taliya_commercial_sdk import (
    IsolatedSdkSpikeInput,
    SdkSpikePaidCallBlocked,
    run_isolated_sdk_spike,
)


def test_spec012_sdk_spike_package_is_not_public_endpoint_cutover() -> None:
    import app.main as runtime_main

    route_paths = {getattr(route, "path", None) for route in runtime_main.app.routes}
    assert "/v1/taliya-commercial/turn" in route_paths
    assert "/v1/taliya-commercial/sdk-spike" not in route_paths

    main_source = inspect.getsource(runtime_main)
    assert "run_action_first_agent_turn" in main_source
    assert "spec012_action_first_enabled" not in main_source
    assert "run_isolated_sdk_spike" not in main_source
    assert "run_spec011_agent_turn" not in main_source


@pytest.mark.asyncio
async def test_spec012_sdk_spike_blocks_paid_calls_without_approval() -> None:
    spike_input = IsolatedSdkSpikeInput(
        conversation_id="conv_t012_020",
        turn_id="turn_t012_020",
        channel="widget",
        user_text="quanto custa?",
    )

    with pytest.raises(SdkSpikePaidCallBlocked):
        await run_isolated_sdk_spike(spike_input)


@pytest.mark.asyncio
async def test_spec012_sdk_spike_runs_with_mocked_no_cost_runner() -> None:
    api_key_env = "OPENAI" + "_API_KEY"
    os.environ.pop(api_key_env, None)
    spike_input = IsolatedSdkSpikeInput(
        conversation_id="conv_t012_020",
        turn_id="turn_t012_020",
        channel="widget",
        user_text="perco leads no WhatsApp e quero saber o preco",
        metadata={"spec_task": "T012-020"},
    )
    calls: list[IsolatedSdkSpikeInput] = []

    async def mocked_runner(received: IsolatedSdkSpikeInput) -> dict[str, object]:
        calls.append(received)
        return {
            "agent_path": ["mock_taliya_triage_agent"],
            "structured_output_pending_task": "T012-023",
            "commercial_understanding_source": "mocked_fixture",
        }

    result = await run_isolated_sdk_spike(spike_input, sdk_runner=mocked_runner)

    assert calls == [spike_input]
    assert result.proof_type == "mocked"
    assert result.paid_call_status == "not_run"
    assert result.public_cutover is False
    assert result.sdk_output["structured_output_pending_task"] == "T012-023"
