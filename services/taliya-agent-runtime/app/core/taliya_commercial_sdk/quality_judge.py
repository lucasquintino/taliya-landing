"""T012-039: quality-judge gate harness for action-first evals.

The final Layer 3 judge is an LLM/manual-review gate from Spec 010. This
module deliberately does not pretend local heuristics are the judge. It accepts
judge scores/rationales from a provider (mocked in no-cost tests, real later),
then applies the release thresholds and proof-mode rules.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

QUALITY_DIMENSIONS: tuple[str, ...] = (
    "directness",
    "naturalness",
    "usefulness",
    "commercial_clarity",
    "evidence_use",
    "diagnostic_quality",
    "waitlist_timing",
    "safety_and_honesty",
    "brevity_and_channel_fit",
    "no_robotic_phrasing",
)

ProofMode = Literal["mocked", "real_model", "manual_review"]
GateStatus = Literal["passed", "failed", "blocked_pending_real_judge"]


@dataclass(frozen=True)
class QualityJudgeScenario:
    scenario_id: str
    transcript: tuple[str, ...]
    blocking_failures: tuple[str, ...] = ()
    mapped_p1: bool = True


@dataclass(frozen=True)
class QualityJudgeScore:
    scenario_id: str
    dimensions: dict[str, float]
    rationale: str
    proof_mode: ProofMode

    @property
    def average(self) -> float:
        return round(
            sum(self.dimensions.values()) / max(len(self.dimensions), 1),
            2,
        )

    @property
    def minimum(self) -> float:
        return min(self.dimensions.values()) if self.dimensions else 0.0


@dataclass(frozen=True)
class QualityJudgeReport:
    status: GateStatus
    proof_mode: ProofMode
    scenario_count: int
    mapped_p1_count: int
    average: float
    minimum: float
    required_average: float
    required_minimum: float
    release_eligible: bool
    blocking_failures: tuple[str, ...] = ()
    failed_scenarios: tuple[str, ...] = ()
    scores: tuple[QualityJudgeScore, ...] = field(default_factory=tuple)
    scenarios: tuple[QualityJudgeScenario, ...] = field(default_factory=tuple)


def build_quality_judge_report(
    *,
    scenarios: list[QualityJudgeScenario],
    scores: list[QualityJudgeScore],
    proof_mode: ProofMode,
    required_average: float = 4.2,
    required_minimum: float = 4.0,
) -> QualityJudgeReport:
    """Apply Spec 010 Layer 3 thresholds to supplied judge scores."""

    scores_by_id = {score.scenario_id: score for score in scores}
    mapped = [scenario for scenario in scenarios if scenario.mapped_p1]
    missing_scores = [
        scenario.scenario_id
        for scenario in mapped
        if scenario.scenario_id not in scores_by_id
    ]
    blocking_failures = [
        f"{scenario.scenario_id}:{failure}"
        for scenario in scenarios
        for failure in scenario.blocking_failures
    ]
    score_mode_mismatches = [
        score.scenario_id
        for score in scores
        if score.proof_mode != proof_mode
    ]
    invalid_scores = [
        score.scenario_id
        for score in scores
        if set(score.dimensions) != set(QUALITY_DIMENSIONS)
        or any(value < 1 or value > 5 for value in score.dimensions.values())
    ]
    considered = [
        scores_by_id[scenario.scenario_id]
        for scenario in mapped
        if scenario.scenario_id in scores_by_id
    ]
    average = round(
        sum(score.average for score in considered) / max(len(considered), 1),
        2,
    )
    minimum = min((score.minimum for score in considered), default=0.0)
    below_minimum = [
        score.scenario_id for score in considered if score.minimum < required_minimum
    ]
    failed_scenarios = tuple(
        sorted(
            {
                *missing_scores,
                *score_mode_mismatches,
                *invalid_scores,
                *below_minimum,
            }
        )
    )

    status: GateStatus
    if (
        blocking_failures
        or failed_scenarios
        or not considered
        or average < required_average
    ):
        status = "failed"
    elif proof_mode != "real_model":
        status = "blocked_pending_real_judge"
    else:
        status = "passed"

    return QualityJudgeReport(
        status=status,
        proof_mode=proof_mode,
        scenario_count=len(scenarios),
        mapped_p1_count=len(mapped),
        average=average,
        minimum=round(minimum, 2),
        required_average=required_average,
        required_minimum=required_minimum,
        release_eligible=status == "passed" and proof_mode == "real_model",
        blocking_failures=tuple(blocking_failures),
        failed_scenarios=failed_scenarios,
        scores=tuple(scores),
        scenarios=tuple(scenarios),
    )


def export_quality_judge_evidence_package(
    report: QualityJudgeReport,
    *,
    run_id: str,
    agent_key: str = "taliya_commercial",
    model_usage: dict[str, Any] | None = None,
    product_source_versions: dict[str, Any] | None = None,
    deterministic_invariant_results: dict[str, Any] | None = None,
    skipped_scenarios: list[str] | None = None,
) -> dict[str, Any]:
    """Build the local Layer 3 evidence package required by Spec 010.

    This packages supplied judge scores and transcript metadata only. It never
    calls a judge model and never promotes mocked proof mode to approval.
    """

    scores_by_id = {score.scenario_id: score for score in report.scores}
    scenario_payloads = []
    for scenario in report.scenarios:
        score = scores_by_id.get(scenario.scenario_id)
        scenario_payloads.append(
            {
                "scenario_id": scenario.scenario_id,
                "mapped_p1": scenario.mapped_p1,
                "transcript": list(scenario.transcript),
                "structured_outputs": [],
                "tool_calls": [],
                "handoffs": [],
                "guardrails": [],
                "blocking_failures": list(scenario.blocking_failures),
                "judge_score": _score_payload(score) if score else None,
            }
        )

    return {
        "schema": "012.quality_judge_evidence.v1",
        "run_id": run_id,
        "agent_key": agent_key,
        "proof_mode": report.proof_mode,
        "scenario_ids": [scenario.scenario_id for scenario in report.scenarios],
        "scenario_count": report.scenario_count,
        "mapped_p1_count": report.mapped_p1_count,
        "required_average": report.required_average,
        "required_minimum": report.required_minimum,
        "average": report.average,
        "minimum": report.minimum,
        "status": report.status,
        "release_eligible": report.release_eligible,
        "final_pass": report.status == "passed" and report.release_eligible,
        "blocking_failures": list(report.blocking_failures),
        "failed_scenarios": list(report.failed_scenarios),
        "skipped_scenarios": list(skipped_scenarios or []),
        "deterministic_invariant_results": deterministic_invariant_results or {},
        "model_usage": model_usage or {"model_operations": 0, "cost_usd": 0.0},
        "product_source_versions": product_source_versions or {},
        "judge_scores": [_score_payload(score) for score in report.scores],
        "scenarios": scenario_payloads,
    }


def _score_payload(score: QualityJudgeScore | None) -> dict[str, Any] | None:
    if score is None:
        return None
    return {
        "scenario_id": score.scenario_id,
        "dimensions": dict(score.dimensions),
        "average": score.average,
        "minimum": score.minimum,
        "rationale": score.rationale,
        "proof_mode": score.proof_mode,
    }
