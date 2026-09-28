"""Isolated Spec 012 Agents SDK spike package.

This package is intentionally not imported by the public runtime endpoint until
the later feature-flagged integration tasks approve a cutover path.
"""

from app.core.taliya_commercial_sdk.agents import (
    DIAGNOSTIC_AGENT,
    ENTRY_AGENT,
    HANDOFF_AGENT,
    PRODUCT_AGENT,
    TRIAGE_AGENT,
    WAITLIST_AGENT,
    TaliyaSdkAgentSpec,
    build_sdk_agent_specs,
    build_sdk_agents,
    get_sdk_agent_manifest,
)
from app.core.taliya_commercial_sdk.conductor_decision import (
    ACTION_MENU_BY_MODE,
    ConductorActionDecision,
    composition_variable_names,
    validate_action_decision,
)
from app.core.taliya_commercial_sdk.isolation import (
    PAID_OPENAI_CALLS_APPROVED,
    PUBLIC_CUTOVER_ENABLED,
    SdkSpikeCutoverBlocked,
    SdkSpikePaidCallBlocked,
    assert_public_cutover_disabled,
    require_paid_approval,
)
from app.core.taliya_commercial_sdk.output_adapter import (
    SdkOutputAdapterError,
    adapt_sdk_output_to_turn_proposal,
    adapt_sdk_run_result_to_turn_proposal,
)
from app.core.taliya_commercial_sdk.output_schema import (
    FORBIDDEN_DIRECT_OUTPUT_FIELDS,
    TaliyaTurnProposal,
)
from app.core.taliya_commercial_sdk.paid_spike_harness import (
    DRY_RUN_MODEL_NAME,
    MODEL_PRICING_USD_PER_MILLION,
    ScenarioReport,
    SpikeBudget,
    SpikePreconditionError,
    SpikeRunReport,
    estimate_cost_usd,
    run_spike_scenarios,
    worst_case_scenario_cost_usd,
    write_spike_report,
)
from app.core.taliya_commercial_sdk.run_context import TaliyaSpikeContext, TranscriptItem
from app.core.taliya_commercial_sdk.sdk_output_model import (
    TaliyaSdkTurnOutput,
    sdk_turn_output_to_proposal_fields,
)
from app.core.taliya_commercial_sdk.spike_runner import (
    IsolatedSdkSpikeInput,
    IsolatedSdkSpikeResult,
    run_isolated_sdk_spike,
)
from app.core.taliya_commercial_sdk.spike_scenarios import (
    FROZEN_SCENARIO_IDS,
    FrozenSpikeScenario,
    frozen_scenario_ids,
    get_frozen_scenario,
    load_frozen_spike_scenarios,
)
from app.core.taliya_commercial_sdk.tools import (
    COMMIT_TOOL_NAMES,
    PROPOSAL_ONLY_TOOL_NAMES,
    READ_ONLY_TOOL_NAMES,
    get_sdk_tool_names,
    get_sdk_tools,
)
from app.core.taliya_commercial_sdk.turn_situation import (
    TurnSituation,
    build_turn_situation,
)
from app.core.taliya_commercial_sdk.validators_adapter import (
    SdkSpikeValidatedOutput,
    validate_and_render_spike_output,
)

__all__ = [
    "ACTION_MENU_BY_MODE",
    "ConductorActionDecision",
    "composition_variable_names",
    "validate_action_decision",
    "DIAGNOSTIC_AGENT",
    "ENTRY_AGENT",
    "HANDOFF_AGENT",
    "IsolatedSdkSpikeInput",
    "IsolatedSdkSpikeResult",
    "PAID_OPENAI_CALLS_APPROVED",
    "PRODUCT_AGENT",
    "PROPOSAL_ONLY_TOOL_NAMES",
    "PUBLIC_CUTOVER_ENABLED",
    "READ_ONLY_TOOL_NAMES",
    "SdkSpikeCutoverBlocked",
    "SdkOutputAdapterError",
    "SdkSpikeValidatedOutput",
    "SdkSpikePaidCallBlocked",
    "TaliyaTurnProposal",
    "TRIAGE_AGENT",
    "TaliyaSdkAgentSpec",
    "WAITLIST_AGENT",
    "assert_public_cutover_disabled",
    "build_sdk_agent_specs",
    "build_sdk_agents",
    "get_sdk_agent_manifest",
    "get_sdk_tool_names",
    "get_sdk_tools",
    "require_paid_approval",
    "run_isolated_sdk_spike",
    "COMMIT_TOOL_NAMES",
    "DRY_RUN_MODEL_NAME",
    "FORBIDDEN_DIRECT_OUTPUT_FIELDS",
    "FROZEN_SCENARIO_IDS",
    "FrozenSpikeScenario",
    "MODEL_PRICING_USD_PER_MILLION",
    "ScenarioReport",
    "SpikeBudget",
    "SpikePreconditionError",
    "SpikeRunReport",
    "TaliyaSdkTurnOutput",
    "TaliyaSpikeContext",
    "TurnSituation",
    "build_turn_situation",
    "TranscriptItem",
    "adapt_sdk_output_to_turn_proposal",
    "adapt_sdk_run_result_to_turn_proposal",
    "estimate_cost_usd",
    "frozen_scenario_ids",
    "get_frozen_scenario",
    "load_frozen_spike_scenarios",
    "run_spike_scenarios",
    "sdk_turn_output_to_proposal_fields",
    "validate_and_render_spike_output",
    "worst_case_scenario_cost_usd",
    "write_spike_report",
]
