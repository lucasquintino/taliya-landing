from __future__ import annotations

from app.core.taliya_commercial_sdk.quality_judge import (
    QUALITY_DIMENSIONS,
    QualityJudgeScenario,
    QualityJudgeScore,
    build_quality_judge_report,
    export_quality_judge_evidence_package,
)


def _score(
    scenario_id: str,
    value: float,
    *,
    proof_mode: str = "mocked",
    overrides: dict[str, float] | None = None,
) -> QualityJudgeScore:
    dimensions = {dimension: value for dimension in QUALITY_DIMENSIONS}
    dimensions.update(overrides or {})
    return QualityJudgeScore(
        scenario_id=scenario_id,
        dimensions=dimensions,
        rationale="Mocked judge rationale for harness validation.",
        proof_mode=proof_mode,  # type: ignore[arg-type]
    )


def test_t012_039_mocked_quality_judge_cannot_release() -> None:
    report = build_quality_judge_report(
        scenarios=[
            QualityJudgeScenario("price_first", ("lead: quanto custa?",)),
            QualityJudgeScenario("diagnostic_final", ("lead: quero diagnostico",)),
        ],
        scores=[_score("price_first", 4.5), _score("diagnostic_final", 4.6)],
        proof_mode="mocked",
    )

    assert report.status == "blocked_pending_real_judge"
    assert report.release_eligible is False
    assert report.average == 4.55
    assert report.minimum == 4.5


def test_t012_039_real_quality_judge_passes_when_thresholds_hold() -> None:
    report = build_quality_judge_report(
        scenarios=[QualityJudgeScenario("long_conversation", ("lead: quero seguir",))],
        scores=[_score("long_conversation", 4.4, proof_mode="real_model")],
        proof_mode="real_model",
    )

    assert report.status == "passed"
    assert report.release_eligible is True


def test_t012_039_quality_judge_blocks_average_below_gate() -> None:
    report = build_quality_judge_report(
        scenarios=[
            QualityJudgeScenario("one", ("lead",)),
            QualityJudgeScenario("two", ("lead",)),
        ],
        scores=[_score("one", 4.1), _score("two", 4.2)],
        proof_mode="real_model",
    )

    assert report.status == "failed"
    assert report.average == 4.15
    assert report.release_eligible is False


def test_t012_039_quality_judge_blocks_any_dimension_below_four() -> None:
    report = build_quality_judge_report(
        scenarios=[QualityJudgeScenario("robotic", ("lead",))],
        scores=[
            _score(
                "robotic",
                4.6,
                proof_mode="real_model",
                overrides={"no_robotic_phrasing": 3.5},
            )
        ],
        proof_mode="real_model",
    )

    assert report.status == "failed"
    assert report.failed_scenarios == ("robotic",)
    assert report.minimum == 3.5


def test_t012_039_blocking_failures_override_judge_score() -> None:
    report = build_quality_judge_report(
        scenarios=[
            QualityJudgeScenario(
                "checkout_invented",
                ("lead",),
                blocking_failures=("invented_checkout",),
            )
        ],
        scores=[_score("checkout_invented", 5, proof_mode="real_model")],
        proof_mode="real_model",
    )

    assert report.status == "failed"
    assert report.blocking_failures == ("checkout_invented:invented_checkout",)
    assert report.release_eligible is False


def test_t012_039_quality_judge_requires_all_contract_dimensions() -> None:
    incomplete = {dimension: 4.5 for dimension in QUALITY_DIMENSIONS[:-1]}
    report = build_quality_judge_report(
        scenarios=[QualityJudgeScenario("missing_dimension", ("lead",))],
        scores=[
            QualityJudgeScore(
                scenario_id="missing_dimension",
                dimensions=incomplete,
                rationale="Missing one dimension.",
                proof_mode="real_model",
            )
        ],
        proof_mode="real_model",
    )

    assert report.status == "failed"
    assert report.failed_scenarios == ("missing_dimension",)


def test_t012_039_exports_eval_contract_evidence_package_without_release() -> None:
    scenarios = [
        QualityJudgeScenario(
            "price_first",
            (
                "lead: quanto custa?",
                "assistant: Os planos comecam em R$ 197 por mes...",
            ),
        ),
        QualityJudgeScenario(
            "waitlist_joined_resume",
            (
                "lead: como funciona mesmo?",
                "assistant: Funciona como um sistema operacional comercial...",
            ),
        ),
    ]
    report = build_quality_judge_report(
        scenarios=scenarios,
        scores=[
            _score("price_first", 4.5),
            _score("waitlist_joined_resume", 4.4),
        ],
        proof_mode="mocked",
    )

    package = export_quality_judge_evidence_package(
        report,
        run_id="t012-039-mocked-quality-package",
        model_usage={"model_operations": 0, "cost_usd": 0.0},
        product_source_versions={"product_knowledge": "mocked_local"},
        deterministic_invariant_results={"spec012_structural": "passed"},
    )

    assert package["schema"] == "012.quality_judge_evidence.v1"
    assert package["run_id"] == "t012-039-mocked-quality-package"
    assert package["agent_key"] == "taliya_commercial"
    assert package["scenario_ids"] == ["price_first", "waitlist_joined_resume"]
    assert package["status"] == "blocked_pending_real_judge"
    assert package["release_eligible"] is False
    assert package["final_pass"] is False
    assert package["average"] == 4.45
    assert package["minimum"] == 4.4
    assert package["model_usage"] == {"model_operations": 0, "cost_usd": 0.0}
    assert package["product_source_versions"] == {
        "product_knowledge": "mocked_local"
    }
    assert package["deterministic_invariant_results"] == {
        "spec012_structural": "passed"
    }
    assert len(package["judge_scores"]) == 2
    assert package["judge_scores"][0]["rationale"]
    assert package["scenarios"][0]["transcript"][0] == "lead: quanto custa?"
    assert package["scenarios"][0]["structured_outputs"] == []
    assert package["scenarios"][0]["tool_calls"] == []
    assert package["scenarios"][0]["guardrails"] == []
