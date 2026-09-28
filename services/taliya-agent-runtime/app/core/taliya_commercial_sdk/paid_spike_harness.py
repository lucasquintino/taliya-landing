from __future__ import annotations

import json
import os
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.core.taliya_commercial_sdk.agents import TRIAGE_AGENT, build_sdk_agents
from app.core.taliya_commercial_sdk.isolation import (
    assert_public_cutover_disabled,
    require_paid_approval,
)
from app.core.taliya_commercial_sdk.output_adapter import (
    SdkOutputAdapterError,
    adapt_sdk_run_result_to_turn_proposal,
)
from app.core.taliya_commercial_sdk.spike_scenarios import (
    FrozenSpikeScenario,
    load_frozen_spike_scenarios,
)
from app.core.taliya_commercial_sdk.validators_adapter import (
    scrub_stale_direct_question,
    validate_and_render_spike_output,
)
from app.settings import get_settings

try:
    from agents import RunConfig, Runner, set_tracing_disabled
    from agents.exceptions import MaxTurnsExceeded, ModelBehaviorError
except Exception:  # pragma: no cover - import fallback for static/no-sdk environments
    RunConfig = None
    Runner = None
    set_tracing_disabled = None

    class MaxTurnsExceeded(Exception):  # type: ignore[no-redef]
        pass

    class ModelBehaviorError(Exception):  # type: ignore[no-redef]
        pass

DRY_RUN_MODEL_NAME = "mocked-sdk-dry-run"

# Pricing checked against the OpenAI model pages. A paid run with an unpriced
# model must stop instead of estimating from another model.
MODEL_PRICING_USD_PER_MILLION: dict[str, dict[str, float]] = {
    "gpt-5.4-mini": {
        "input": 0.75,
        "cached_input": 0.075,
        "cache_write_input": 0.75,
        "output": 4.50,
    },
    "gpt-5.6-luna": {
        "input": 1.00,
        "cached_input": 0.10,
        "cache_write_input": 1.25,
        "output": 6.00,
    },
    DRY_RUN_MODEL_NAME: {
        "input": 0.0,
        "cached_input": 0.0,
        "cache_write_input": 0.0,
        "output": 0.0,
    },
}

# Worst-case per model operation, from the approval packet budget assumptions.
WORST_CASE_INPUT_TOKENS_PER_OPERATION = 8_000
WORST_CASE_OUTPUT_TOKENS_PER_OPERATION = 1_500


class SpikePreconditionError(RuntimeError):
    """Raised when a T012-027 execution precondition is not met."""


@dataclass(frozen=True)
class SpikeBudget:
    max_total_model_operations: int = 45
    max_total_cost_usd: float = 1.00
    max_model_operations_per_scenario: int = 3


@dataclass
class ScenarioUsage:
    model: str
    model_operations: int = 0
    input_tokens: int = 0
    cached_input_tokens: int = 0
    cache_write_input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    handoffs: int = 0
    repairs: int = 0
    recorded: bool = True

    def as_proposal_usage(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "model_operations": self.model_operations,
            "input_tokens": self.input_tokens,
            "cached_input_tokens": self.cached_input_tokens,
            "cache_write_input_tokens": self.cache_write_input_tokens,
            "output_tokens": self.output_tokens,
            "cost_usd": round(self.cost_usd, 6),
            "handoffs": self.handoffs,
            "repairs": self.repairs,
        }


@dataclass
class ScenarioReport:
    number: int
    scenario_id: str
    channel: str
    required_proof: str
    input_transcript: list[dict[str, str]] = field(default_factory=list)
    starting_agent: str = TRIAGE_AGENT
    agent_path: list[dict[str, Any]] = field(default_factory=list)
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    sdk_final_output: dict[str, Any] | None = None
    turn_proposal: dict[str, Any] | None = None
    validator_result: dict[str, Any] | None = None
    rendered_preview: list[dict[str, Any]] = field(default_factory=list)
    proposed_state_diff: dict[str, Any] = field(default_factory=dict)
    proposed_sales_inbox_projection: dict[str, Any] = field(default_factory=dict)
    usage: dict[str, Any] = field(default_factory=dict)
    status: str = "not_run"
    pass_fail_reason: str = ""
    comparison_notes: str = (
        "Compare manually against the local Spec 011 path evidence; "
        "no new paid Spec 011 calls are allowed for this comparison."
    )

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "number": self.number,
            "scenario_id": self.scenario_id,
            "channel": self.channel,
            "required_proof": self.required_proof,
            "input_transcript": self.input_transcript,
            "starting_agent": self.starting_agent,
            "agent_path": self.agent_path,
            "tool_calls": self.tool_calls,
            "sdk_final_output": self.sdk_final_output,
            "turn_proposal": self.turn_proposal,
            "validator_result": self.validator_result,
            "rendered_preview": self.rendered_preview,
            "proposed_state_diff": self.proposed_state_diff,
            "proposed_sales_inbox_projection": self.proposed_sales_inbox_projection,
            "usage": self.usage,
            "status": self.status,
            "pass_fail_reason": self.pass_fail_reason,
            "comparison_notes": self.comparison_notes,
        }


@dataclass
class SpikeRunReport:
    proof_type: str
    model: str
    tracing_disabled: bool
    public_cutover: bool
    paid_call_status: str
    started_at: str
    budget: SpikeBudget
    total_model_operations: int = 0
    total_cost_usd: float = 0.0
    aborted: bool = False
    abort_reason: str | None = None
    scenario_reports: list[ScenarioReport] = field(default_factory=list)

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "proof_type": self.proof_type,
            "model": self.model,
            "tracing_disabled": self.tracing_disabled,
            "public_cutover": self.public_cutover,
            "paid_call_status": self.paid_call_status,
            "started_at": self.started_at,
            "budget": {
                "max_total_model_operations": self.budget.max_total_model_operations,
                "max_total_cost_usd": self.budget.max_total_cost_usd,
                "max_model_operations_per_scenario": (
                    self.budget.max_model_operations_per_scenario
                ),
            },
            "total_model_operations": self.total_model_operations,
            "total_cost_usd": round(self.total_cost_usd, 6),
            "aborted": self.aborted,
            "abort_reason": self.abort_reason,
            "scenarios": [report.to_json_dict() for report in self.scenario_reports],
        }


def estimate_cost_usd(
    model_name: str,
    *,
    input_tokens: int,
    cached_input_tokens: int,
    output_tokens: int,
    cache_write_input_tokens: int = 0,
) -> float:
    pricing = MODEL_PRICING_USD_PER_MILLION.get(model_name)
    if pricing is None:
        raise SpikePreconditionError(
            f"No recorded pricing for model '{model_name}'. The paid spike must "
            "stop and return for approval instead of guessing cost."
        )
    cached = min(max(cached_input_tokens, 0), max(input_tokens, 0))
    cache_write = min(
        max(cache_write_input_tokens, 0),
        max(input_tokens - cached, 0),
    )
    uncached_input = max(input_tokens - cached - cache_write, 0)
    return (
        uncached_input * pricing["input"]
        + cached * pricing["cached_input"]
        + cache_write * pricing["cache_write_input"]
        + output_tokens * pricing["output"]
    ) / 1_000_000


def worst_case_scenario_cost_usd(model_name: str, budget: SpikeBudget) -> float:
    operations = budget.max_model_operations_per_scenario
    return estimate_cost_usd(
        model_name,
        input_tokens=WORST_CASE_INPUT_TOKENS_PER_OPERATION * operations,
        cached_input_tokens=0,
        cache_write_input_tokens=0,
        output_tokens=WORST_CASE_OUTPUT_TOKENS_PER_OPERATION * operations,
    )


def _worst_case_usage(model_name: str, budget: SpikeBudget) -> ScenarioUsage:
    operations = budget.max_model_operations_per_scenario
    usage = ScenarioUsage(
        model=model_name,
        model_operations=operations,
        input_tokens=WORST_CASE_INPUT_TOKENS_PER_OPERATION * operations,
        output_tokens=WORST_CASE_OUTPUT_TOKENS_PER_OPERATION * operations,
        recorded=False,
    )
    usage.cost_usd = estimate_cost_usd(
        model_name,
        input_tokens=usage.input_tokens,
        cached_input_tokens=0,
        cache_write_input_tokens=0,
        output_tokens=usage.output_tokens,
    )
    return usage


def _extract_scenario_usage(run_result: Any, model_name: str) -> ScenarioUsage:
    usage_obj = getattr(getattr(run_result, "context_wrapper", None), "usage", None)
    if usage_obj is None:
        return ScenarioUsage(model=model_name, recorded=False)
    cached = 0
    cache_write = 0
    details = getattr(usage_obj, "input_tokens_details", None)
    if details is not None and getattr(details, "cached_tokens", None):
        cached = details.cached_tokens
    if details is not None and getattr(details, "cache_write_tokens", None):
        cache_write = details.cache_write_tokens
    handoffs = sum(
        1
        for item in getattr(run_result, "new_items", [])
        if "handoff_output" in str(getattr(item, "type", ""))
    )
    usage = ScenarioUsage(
        model=model_name,
        model_operations=usage_obj.requests,
        input_tokens=usage_obj.input_tokens,
        cached_input_tokens=cached,
        cache_write_input_tokens=cache_write,
        output_tokens=usage_obj.output_tokens,
        handoffs=handoffs,
    )
    usage.cost_usd = estimate_cost_usd(
        model_name,
        input_tokens=usage.input_tokens,
        cached_input_tokens=usage.cached_input_tokens,
        cache_write_input_tokens=usage.cache_write_input_tokens,
        output_tokens=usage.output_tokens,
    )
    return usage


def _serialize_tool_calls(run_result: Any) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    for item in getattr(run_result, "new_items", []):
        item_type = str(getattr(item, "type", ""))
        raw = getattr(item, "raw_item", None)
        if item_type == "tool_call_item":
            calls.append(
                {
                    "event": "tool_call",
                    "name": getattr(raw, "name", None),
                    "arguments": getattr(raw, "arguments", None),
                }
            )
        elif item_type == "tool_call_output_item":
            output = getattr(item, "output", None)
            calls.append(
                {
                    "event": "tool_output",
                    "output": output if isinstance(output, (dict, str)) else str(output),
                }
            )
        elif item_type == "handoff_output_item":
            calls.append(
                {
                    "event": "handoff",
                    "from_agent": getattr(
                        getattr(item, "source_agent", None), "name", None
                    ),
                    "to_agent": getattr(
                        getattr(item, "target_agent", None), "name", None
                    ),
                }
            )
    return calls


_REPAIR_INSTRUCTION = (
    "Your structured output failed Taliya's validators. Fix ONLY what the "
    "errors below require and return the corrected, complete structured "
    "output in the same schema. Keep your commercial understanding; if an "
    "error says a direct question was not answered first, change the template "
    "plan so it actually answers the question before steering. A "
    "source_not_allowed error means the variable's declared source must be "
    "one of its allowed sources from your instructions, reflecting where the "
    "underlying facts came from (ledger facts -> diagnostic_ledger, official "
    "facts -> official_product_knowledge); relabel it, do not invent new "
    "content. A value_too_long error means rewrite that value comfortably "
    "under its max_length. Do not call tools.\nValidator errors:\n{errors}"
)


async def _attempt_single_repair(
    run_result: Any,
    *,
    context: Any,
    run_config: Any,
    errors: Sequence[Any],
) -> Any | None:
    last_agent = getattr(run_result, "last_agent", None)
    to_input_list = getattr(run_result, "to_input_list", None)
    if last_agent is None or to_input_list is None:
        return None
    error_lines = "\n".join(f"- {issue.code}: {issue.message}" for issue in errors)
    repair_input = list(to_input_list()) + [
        {"role": "user", "content": _REPAIR_INSTRUCTION.format(errors=error_lines)}
    ]
    try:
        return await Runner.run(
            last_agent,
            repair_input,
            context=context,
            max_turns=1,
            run_config=run_config,
        )
    except (MaxTurnsExceeded, ModelBehaviorError):
        return None


async def _run_single_scenario(
    scenario: FrozenSpikeScenario,
    agents_by_name: dict[str, Any],
    *,
    model_name: str,
    run_config: Any,
    budget: SpikeBudget,
) -> ScenarioReport:
    # Design-lock starting policy: if the persisted current agent is known,
    # start there (state-based operational selection, not raw-text routing).
    starting_agent = TRIAGE_AGENT
    persisted_agent = dict(scenario.state_snapshot).get("current_sdk_agent")
    if isinstance(persisted_agent, str) and persisted_agent in agents_by_name:
        starting_agent = persisted_agent

    report = ScenarioReport(
        number=scenario.number,
        scenario_id=scenario.scenario_id,
        channel=scenario.channel,
        required_proof=scenario.required_proof,
        input_transcript=scenario.to_input_items(),
        starting_agent=starting_agent,
    )
    context = scenario.to_run_context()

    try:
        run_result = await Runner.run(
            agents_by_name[starting_agent],
            scenario.to_input_items(),
            context=context,
            max_turns=budget.max_model_operations_per_scenario,
            run_config=run_config,
        )
    except MaxTurnsExceeded as exc:
        run_data = getattr(exc, "run_data", None)
        partial_usage = (
            _extract_scenario_usage(run_data, model_name) if run_data is not None else None
        )
        if partial_usage is not None and partial_usage.recorded:
            report.usage = partial_usage.as_proposal_usage()
        else:
            report.usage = _worst_case_usage(model_name, budget).as_proposal_usage()
        if run_data is not None:
            report.tool_calls = _serialize_tool_calls(run_data)
        report.status = "failed"
        report.pass_fail_reason = (
            "max_turns_exceeded: scenario needed more than the approved "
            f"{budget.max_model_operations_per_scenario} model operations; "
            "partial run items recorded for diagnosis."
        )
        return report
    except ModelBehaviorError as exc:
        report.usage = _worst_case_usage(model_name, budget).as_proposal_usage()
        report.status = "aborted"
        report.pass_fail_reason = (
            "sdk_output_not_structured: the model did not return the strict "
            f"structured output ({exc}); the approval packet requires aborting "
            "when SDK output cannot adapt to TaliyaTurnProposal."
        )
        return report
    except Exception as exc:  # provider/API failures must not lose the report
        report.usage = ScenarioUsage(model=model_name, recorded=False).as_proposal_usage()
        report.status = "aborted"
        report.pass_fail_reason = (
            f"provider_error: {type(exc).__name__}: {str(exc)[:200]} - run "
            "aborted; no usage was recorded for this scenario."
        )
        return report

    usage = _extract_scenario_usage(run_result, model_name)
    report.usage = usage.as_proposal_usage()
    report.tool_calls = _serialize_tool_calls(run_result)
    if not usage.recorded:
        report.status = "aborted"
        report.pass_fail_reason = (
            "usage_unrecorded: the runner did not report usage; the approval "
            "packet requires aborting when usage/cost cannot be recorded."
        )
        return report

    try:
        proposal = adapt_sdk_run_result_to_turn_proposal(
            run_result,
            turn_id=context.turn_id,
            conversation_id=context.conversation_id,
            channel=scenario.channel,
            starting_agent=starting_agent,
            usage=usage.as_proposal_usage(),
        )
    except SdkOutputAdapterError as exc:
        report.status = "failed"
        report.pass_fail_reason = f"output_adapter_rejected: {exc}"
        final_output = getattr(run_result, "final_output", None)
        if hasattr(final_output, "model_dump"):
            report.sdk_final_output = final_output.model_dump(mode="json")
        return report

    proposal = scrub_stale_direct_question(proposal, scenario.user_text)
    validated = validate_and_render_spike_output(
        proposal,
        state_snapshot=scenario.state_snapshot,
        current_user_text=scenario.user_text,
    )

    # Design-lock repair: at most one extra model operation, only when it fits
    # inside the approved per-scenario operation cap.
    if (
        validated.validator_result.status != "passed"
        and usage.model_operations + 1 <= budget.max_model_operations_per_scenario
    ):
        repair_run = await _attempt_single_repair(
            run_result,
            context=context,
            run_config=run_config,
            errors=validated.validator_result.errors,
        )
        if repair_run is not None:
            repair_usage = _extract_scenario_usage(repair_run, model_name)
            if repair_usage.recorded:
                usage.model_operations += repair_usage.model_operations
                usage.input_tokens += repair_usage.input_tokens
                usage.cached_input_tokens += repair_usage.cached_input_tokens
                usage.cache_write_input_tokens += (
                    repair_usage.cache_write_input_tokens
                )
                usage.output_tokens += repair_usage.output_tokens
                usage.repairs = 1
                usage.cost_usd = estimate_cost_usd(
                    model_name,
                    input_tokens=usage.input_tokens,
                    cached_input_tokens=usage.cached_input_tokens,
                    cache_write_input_tokens=usage.cache_write_input_tokens,
                    output_tokens=usage.output_tokens,
                )
                report.usage = usage.as_proposal_usage()
            try:
                repaired_proposal = adapt_sdk_run_result_to_turn_proposal(
                    repair_run,
                    turn_id=context.turn_id,
                    conversation_id=context.conversation_id,
                    channel=scenario.channel,
                    starting_agent=starting_agent,
                    usage=usage.as_proposal_usage(),
                )
            except SdkOutputAdapterError:
                repaired_proposal = None
            if repaired_proposal is not None:
                repaired_proposal = scrub_stale_direct_question(
                    repaired_proposal, scenario.user_text
                )
                repaired_validated = validate_and_render_spike_output(
                    repaired_proposal,
                    state_snapshot=scenario.state_snapshot,
                    current_user_text=scenario.user_text,
                )
                if repaired_validated.validator_result.status == "passed":
                    run_result = repair_run
                    proposal = repaired_proposal
                    validated = repaired_validated

    final_output = getattr(run_result, "final_output", None)
    if hasattr(final_output, "model_dump"):
        report.sdk_final_output = final_output.model_dump(mode="json")
    report.agent_path = [item.model_dump(mode="json") for item in proposal.agent_path]
    report.turn_proposal = proposal.model_dump(mode="json")
    report.proposed_state_diff = dict(proposal.state_patch_proposal)
    report.proposed_sales_inbox_projection = dict(
        proposal.sales_inbox_projection_proposal
    )
    report.validator_result = validated.validator_result.model_dump(mode="json")
    report.rendered_preview = [
        message.model_dump(mode="json") for message in validated.rendered_preview
    ]

    if validated.validator_result.status == "passed" and validated.rendered_preview:
        report.status = "passed_structural"
        report.pass_fail_reason = (
            "Structured proposal validated and approved templates rendered. "
            "Conversational-quality pass/fail still requires the manual review "
            "described in the approval packet."
        )
    else:
        report.status = "failed"
        issue_codes = [issue.code for issue in validated.validator_result.errors]
        report.pass_fail_reason = f"validator_blocked: {', '.join(issue_codes)}"
    return report


async def run_spike_scenarios(
    *,
    paid_openai_approved: bool = False,
    model: Any | None = None,
    scenarios: Sequence[FrozenSpikeScenario] | None = None,
    budget: SpikeBudget | None = None,
    report_dir: Path | str | None = None,
) -> SpikeRunReport:
    """Run the frozen spike scenarios through the real Agents SDK runner.

    Paid execution requires `paid_openai_approved=True` plus the packet's
    explicit user approval recorded beforehand. Passing an injected SDK
    `Model` instance (not a string) runs the same harness as a no-cost
    dry-run, which is the T012-026B gate before any paid call.
    """

    assert_public_cutover_disabled()
    if Runner is None or RunConfig is None or set_tracing_disabled is None:
        raise SpikePreconditionError(
            "openai-agents SDK is required to run the spike harness."
        )

    active_budget = budget or SpikeBudget()
    injected_model = model is not None and not isinstance(model, str)
    if injected_model:
        model_name = getattr(model, "spike_model_name", DRY_RUN_MODEL_NAME)
        proof_type = "mocked_dry_run"
        paid_call_status = "not_run"
        agent_model: Any = model
    else:
        require_paid_approval(approved=paid_openai_approved)
        model_name = model or get_settings().model
        if model_name not in MODEL_PRICING_USD_PER_MILLION:
            raise SpikePreconditionError(
                f"Model '{model_name}' has no recorded pricing in the approval "
                "packet; stop and return for approval."
            )
        if not os.environ.get("OPENAI_API_KEY"):
            raise SpikePreconditionError(
                "OPENAI_API_KEY is not available; the paid spike cannot start."
            )
        proof_type = "isolated_spike_paid"
        paid_call_status = "run"
        agent_model = model_name

    # D-012-007: traces stay local-only. Disable SDK trace export globally and
    # per run before any model call.
    set_tracing_disabled(True)
    run_config = RunConfig(
        tracing_disabled=True,
        trace_include_sensitive_data=False,
        workflow_name="spec012_t012_027_sdk_spike",
    )

    agents_by_name = build_sdk_agents(model=agent_model)
    selected_scenarios = (
        tuple(scenarios) if scenarios is not None else load_frozen_spike_scenarios()
    )

    run_report = SpikeRunReport(
        proof_type=proof_type,
        model=model_name,
        tracing_disabled=True,
        public_cutover=False,
        paid_call_status=paid_call_status,
        started_at=datetime.now(UTC).isoformat(),
        budget=active_budget,
    )

    worst_case_next = worst_case_scenario_cost_usd(model_name, active_budget)
    for scenario in selected_scenarios:
        remaining_operations = (
            active_budget.max_total_model_operations - run_report.total_model_operations
        )
        if remaining_operations < active_budget.max_model_operations_per_scenario:
            run_report.aborted = True
            run_report.abort_reason = (
                "model_operation_ceiling: continuing could exceed the approved "
                f"{active_budget.max_total_model_operations} operations."
            )
            break
        if (
            run_report.total_cost_usd + worst_case_next
            > active_budget.max_total_cost_usd
        ):
            run_report.aborted = True
            run_report.abort_reason = (
                "cost_ceiling: continuing could exceed the approved "
                f"${active_budget.max_total_cost_usd:.2f} estimated cost."
            )
            break

        scenario_report = await _run_single_scenario(
            scenario,
            agents_by_name,
            model_name=model_name,
            run_config=run_config,
            budget=active_budget,
        )
        run_report.scenario_reports.append(scenario_report)
        run_report.total_model_operations += scenario_report.usage.get(
            "model_operations", 0
        )
        run_report.total_cost_usd += scenario_report.usage.get("cost_usd", 0.0)

        if scenario_report.status == "aborted":
            run_report.aborted = True
            run_report.abort_reason = scenario_report.pass_fail_reason
            break

    if report_dir is not None:
        write_spike_report(run_report, Path(report_dir))
    return run_report


def write_spike_report(run_report: SpikeRunReport, report_dir: Path) -> Path:
    """Write local-only evidence files for the spike run."""

    report_dir.mkdir(parents=True, exist_ok=True)
    summary_path = report_dir / "spike-run-report.json"
    summary_path.write_text(
        json.dumps(run_report.to_json_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    for scenario_report in run_report.scenario_reports:
        scenario_path = (
            report_dir
            / f"scenario-{scenario_report.number:02d}-{scenario_report.scenario_id}.json"
        )
        scenario_path.write_text(
            json.dumps(scenario_report.to_json_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    lines = [
        "# Spec 012 SDK Spike Run Report",
        "",
        f"- Proof type: {run_report.proof_type}",
        f"- Model: {run_report.model}",
        f"- Tracing disabled: {run_report.tracing_disabled}",
        f"- Paid call status: {run_report.paid_call_status}",
        f"- Total model operations: {run_report.total_model_operations}",
        f"- Total estimated cost USD: {run_report.total_cost_usd:.6f}",
        f"- Aborted: {run_report.aborted}",
        f"- Abort reason: {run_report.abort_reason or 'none'}",
        "",
        "| # | Scenario | Status | Ops | Cost USD | Reason |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for scenario_report in run_report.scenario_reports:
        lines.append(
            f"| {scenario_report.number} | {scenario_report.scenario_id} | "
            f"{scenario_report.status} | "
            f"{scenario_report.usage.get('model_operations', 0)} | "
            f"{scenario_report.usage.get('cost_usd', 0.0):.6f} | "
            f"{scenario_report.pass_fail_reason} |"
        )
    (report_dir / "spike-run-report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    return summary_path
