from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
BASE_EVAL = ROOT / "scripts" / "eval-agent-runtime-real-openai.py"
SPEC011_FIXTURE = ROOT / "scripts" / "fixtures" / "agent-runtime" / "spec-011-real-openai-p0.json"


def _load_eval_module():
    spec = importlib.util.spec_from_file_location("agent_runtime_real_openai_eval", BASE_EVAL)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_spec011_fixture_cases_link_to_regression_ids_and_checks_are_known():
    module = _load_eval_module()
    scenarios = json.loads(SPEC011_FIXTURE.read_text(encoding="utf-8"))

    assert scenarios
    covered = {
        regression_id
        for scenario in scenarios
        for regression_id in scenario.get("regression_case_ids", [])
    }
    assert {
        "RC-011-001",
        "RC-011-002",
        "RC-011-003",
        "RC-011-004",
        "RC-011-005",
        "RC-011-006",
        "RC-011-007",
        "RC-011-008",
        "RC-011-009",
        "RC-011-012",
        "RC-011-013",
        "RC-011-014",
    }.issubset(covered)

    for scenario in scenarios:
        assert scenario.get("id", "").startswith("spec011-")
        assert scenario.get("regression_case_ids"), scenario["id"]
        assert scenario.get("checks"), scenario["id"]
        failures = module._check_scenario(
            {**scenario, "checks": [*scenario["checks"], "__unknown_check_for_contract_test__"]},
            [
                {
                    "http_status": 200,
                    "payload": {
                        "output": {
                            "messages": [{"text": "ok"}],
                            "decision": {},
                            "usage": {"model": "unit-test", "input_tokens": 1},
                        }
                    },
                }
            ],
        )
        assert any("unknown eval check" in failure for failure in failures)


def test_real_openai_eval_does_not_run_behavior_checks_on_budget_incomplete_scenario():
    module = _load_eval_module()
    scenario = {
        "id": "budgeted-multiturn",
        "messages": ["quero contratar", "Studio Viva", "quanto custa o Completo?"],
        "checks": ["route:product", "mentions_complete_price_only"],
    }
    turns = [
        {
            "http_status": 200,
            "payload": {"output": {"decision": {"route": "waitlist"}, "messages": []}},
            "cost_gate": {
                "status": "stopped",
                "running_cost_usd": 0.12,
                "max_cost_usd": 0.10,
            },
        }
    ]

    failures = module._evaluate_scenario_failures(
        scenario,
        turns,
        running_cost=0.12,
        max_cost_usd=0.10,
    )

    assert failures == [
        "eval stopped by max cost before scenario completion; "
        "behavior checks were skipped for this incomplete transcript; "
        "eval exceeded max cost: US$0.120000 > US$0.100000"
    ]
    assert module._budget_status_for_scenario(
        scenario,
        turns,
        0.12,
        0.10,
    ) == "stopped_before_completion"


def test_real_openai_eval_keeps_behavior_checks_when_budget_exceeds_after_completion():
    module = _load_eval_module()
    scenario = {
        "id": "budgeted-complete",
        "messages": ["quanto custa?"],
        "checks": ["route:product"],
    }
    turns = [
        {
            "http_status": 200,
            "payload": {"output": {"decision": {"route": "waitlist"}, "messages": []}},
            "cost_gate": {
                "status": "stopped",
                "running_cost_usd": 0.12,
                "max_cost_usd": 0.10,
            },
        }
    ]

    failures = module._evaluate_scenario_failures(
        scenario,
        turns,
        running_cost=0.12,
        max_cost_usd=0.10,
    )

    assert "expected decision.route=product, got waitlist" in failures
    assert "eval exceeded max cost: US$0.120000 > US$0.100000" in failures
    assert module._budget_status_for_scenario(
        scenario,
        turns,
        0.12,
        0.10,
    ) == "exceeded_after_completion"


def test_real_openai_eval_refuses_uncapped_real_runs():
    module = _load_eval_module()

    with pytest.raises(SystemExit, match="--max-model-calls must be set"):
        module._validate_real_eval_budget_caps(
            estimated_calls=1,
            max_model_calls=0,
            max_cost_usd=0.10,
        )

    with pytest.raises(SystemExit, match="--max-cost-usd must be set"):
        module._validate_real_eval_budget_caps(
            estimated_calls=1,
            max_model_calls=1,
            max_cost_usd=0,
        )


def test_real_openai_eval_refuses_more_estimated_calls_than_cap():
    module = _load_eval_module()

    with pytest.raises(SystemExit, match="estimated model calls 3 exceed --max-model-calls=2"):
        module._validate_real_eval_budget_caps(
            estimated_calls=3,
            max_model_calls=2,
            max_cost_usd=0.10,
        )


def test_real_openai_eval_accepts_explicit_positive_caps():
    module = _load_eval_module()

    module._validate_real_eval_budget_caps(
        estimated_calls=2,
        max_model_calls=2,
        max_cost_usd=0.10,
    )
