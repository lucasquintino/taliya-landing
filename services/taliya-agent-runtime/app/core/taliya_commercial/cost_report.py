from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, ValidationError

from app.core.taliya_commercial.schemas import (
    Severity,
    StrictModel,
    ValidationIssue,
    ValidatorResult,
)


class UsageSnapshot(StrictModel):
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    label: str | None = None


class CostScenario(StrictModel):
    scenario_id: str
    runtime_usage_before: UsageSnapshot
    runtime_usage_after: UsageSnapshot
    eval_only_usage: list[UsageSnapshot] = Field(default_factory=list)
    behavior_gate_before: Literal["pass", "fail"]
    behavior_gate_after: Literal["pass", "fail"]
    golden_transcript_diff_approved: bool = False


class CostOptimizationReport(StrictModel):
    report_id: str
    created_at: str
    optimization_summary: str
    scenarios: list[CostScenario]


def validate_cost_optimization_report(payload: Any) -> ValidatorResult:
    try:
        report = CostOptimizationReport.model_validate(payload)
    except ValidationError as error:
        return ValidatorResult(
            decision_id=_payload_report_id(payload),
            status="blocked",
            errors=[
                _issue(
                    code="cost_report_schema_invalid",
                    message=str(error),
                    path="cost_report",
                )
            ],
            final_disposition="blocked",
        )

    errors: list[ValidationIssue] = []
    warnings: list[ValidationIssue] = []
    for index, scenario in enumerate(report.scenarios):
        errors.extend(_validate_runtime_usage(scenario, index))
        errors.extend(_validate_behavior_quality(scenario, index))
        warnings.extend(_validate_cost_savings(scenario, index))

    if not report.scenarios:
        errors.append(
            _issue(
                code="cost_report_scenarios_missing",
                message="cost report requires scenarios",
                path="scenarios",
            )
        )

    return ValidatorResult(
        decision_id=report.report_id,
        status="blocked" if errors else "passed",
        errors=errors,
        warnings=warnings,
        final_disposition="blocked" if errors else "accepted",
    )


def _validate_runtime_usage(
    scenario: CostScenario,
    index: int,
) -> list[ValidationIssue]:
    after = scenario.runtime_usage_after
    if after.input_tokens > 0 and after.output_tokens > 0 and after.model.strip():
        return []
    return [
        _issue(
            code="cost_report_runtime_model_usage_missing",
            message="normal commercial turns require runtime model usage after optimization",
            path=f"scenarios[{index}].runtime_usage_after",
        )
    ]


def _validate_behavior_quality(
    scenario: CostScenario,
    index: int,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    cost_decreased = scenario.runtime_usage_after.cost_usd < (
        scenario.runtime_usage_before.cost_usd
    )
    if scenario.behavior_gate_after != "pass":
        issues.append(
            _issue(
                code="cost_report_behavior_regressed",
                message="cost optimization cannot pass with behavior gate failure",
                path=f"scenarios[{index}].behavior_gate_after",
            )
        )
    if cost_decreased and not scenario.golden_transcript_diff_approved:
        issues.append(
            _issue(
                code="cost_report_golden_diff_unapproved",
                message="cost savings require approved golden transcript diff",
                path=f"scenarios[{index}].golden_transcript_diff_approved",
            )
        )
    return issues


def _validate_cost_savings(
    scenario: CostScenario,
    index: int,
) -> list[ValidationIssue]:
    if scenario.runtime_usage_after.cost_usd < scenario.runtime_usage_before.cost_usd:
        return []
    return [
        _warning(
            code="cost_report_no_savings",
            message="scenario did not reduce runtime cost",
            path=f"scenarios[{index}].runtime_usage_after.cost_usd",
        )
    ]


def _payload_report_id(payload: Any) -> str:
    if isinstance(payload, dict):
        value = payload.get("report_id")
        if isinstance(value, str) and value.strip():
            return value
    return "cost_optimization_report"


def _issue(*, code: str, message: str, path: str) -> ValidationIssue:
    return ValidationIssue(code=code, severity=_P0, message=message, path=path)


def _warning(*, code: str, message: str, path: str) -> ValidationIssue:
    return ValidationIssue(code=code, severity=_P2, message=message, path=path)


_P0: Severity = "P0"
_P2: Severity = "P2"
