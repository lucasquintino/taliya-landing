from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

from app.core.taliya_commercial_sdk.isolation import (
    assert_public_cutover_disabled,
    require_paid_approval,
)

MockedSdkRunner = Callable[["IsolatedSdkSpikeInput"], Awaitable[Mapping[str, Any]]]


@dataclass(frozen=True)
class IsolatedSdkSpikeInput:
    conversation_id: str
    turn_id: str
    channel: str
    user_text: str
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class IsolatedSdkSpikeResult:
    conversation_id: str
    turn_id: str
    proof_type: str
    paid_call_status: str
    public_cutover: bool
    sdk_output: Mapping[str, Any]


async def run_isolated_sdk_spike(
    spike_input: IsolatedSdkSpikeInput,
    *,
    sdk_runner: MockedSdkRunner | None = None,
    paid_openai_approved: bool = False,
) -> IsolatedSdkSpikeResult:
    """Run the T012-020 spike path only with an injected no-cost SDK runner.

    T012-021 and later tasks can replace the injected runner with real Agents SDK
    orchestration after mocked coverage is green and paid calls are approved.
    """

    assert_public_cutover_disabled()
    if sdk_runner is None:
        require_paid_approval(approved=paid_openai_approved)
        raise RuntimeError("A real Agents SDK runner is not implemented in T012-020.")

    raw_output = await sdk_runner(spike_input)
    return IsolatedSdkSpikeResult(
        conversation_id=spike_input.conversation_id,
        turn_id=spike_input.turn_id,
        proof_type="mocked",
        paid_call_status="not_run",
        public_cutover=False,
        sdk_output=dict(raw_output),
    )
