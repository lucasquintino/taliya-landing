from __future__ import annotations

from app.core.taliya_commercial.cost_report import validate_cost_optimization_report


def _scenario(
    scenario_id: str,
    *,
    before_cost: float = 0.03,
    after_cost: float = 0.02,
    after_input_tokens: int = 800,
    after_output_tokens: int = 160,
    behavior_gate_before: str = "pass",
    behavior_gate_after: str = "pass",
    golden_diff_approved: bool = True,
) -> dict[str, object]:
    return {
        "scenario_id": scenario_id,
        "runtime_usage_before": {
            "model": "gpt-5.4-mini",
            "input_tokens": 1200,
            "output_tokens": 220,
            "cost_usd": before_cost,
        },
        "runtime_usage_after": {
            "model": "gpt-5.4-mini",
            "input_tokens": after_input_tokens,
            "output_tokens": after_output_tokens,
            "cost_usd": after_cost,
        },
        "eval_only_usage": [
            {
                "model": "gpt-5.4-mini",
                "input_tokens": 300,
                "output_tokens": 80,
                "cost_usd": 0.005,
                "label": "judge_eval_only",
            }
        ],
        "behavior_gate_before": behavior_gate_before,
        "behavior_gate_after": behavior_gate_after,
        "golden_transcript_diff_approved": golden_diff_approved,
    }


def _payload(*scenarios: dict[str, object]) -> dict[str, object]:
    return {
        "report_id": "cost_011_089_001",
        "created_at": "2026-05-30T12:00:00Z",
        "optimization_summary": "Reduced context tokens without removing LLM call.",
        "scenarios": list(scenarios),
    }


def test_cost_report_accepts_lower_cost_with_model_usage_and_passing_behavior() -> None:
    result = validate_cost_optimization_report(
        _payload(_scenario("price_direct"), _scenario("diagnostic_final"))
    )

    assert result.status == "passed"
    assert result.final_disposition == "accepted"
    assert result.errors == []
    assert result.warnings == []


def test_cost_report_blocks_zero_runtime_model_usage() -> None:
    result = validate_cost_optimization_report(
        _payload(
            _scenario(
                "price_direct",
                after_input_tokens=0,
                after_output_tokens=0,
                after_cost=0,
            )
        )
    )

    assert result.status == "blocked"
    assert {error.code for error in result.errors} == {
        "cost_report_runtime_model_usage_missing"
    }


def test_cost_report_blocks_cost_savings_with_behavior_regression() -> None:
    result = validate_cost_optimization_report(
        _payload(
            _scenario(
                "diagnostic_final",
                behavior_gate_after="fail",
                golden_diff_approved=False,
            )
        )
    )

    assert result.status == "blocked"
    assert {error.code for error in result.errors} == {
        "cost_report_behavior_regressed",
        "cost_report_golden_diff_unapproved",
    }
