from __future__ import annotations

import asyncio
import json
import runpy
from argparse import Namespace
from pathlib import Path
from types import SimpleNamespace

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
RUNNER_PATH = REPO_ROOT / "scripts" / "eval-agent-runtime-spec012-real-model-golden.py"
TARGETED_FIXTURE_PATH = (
    REPO_ROOT / "scripts" / "fixtures" / "agent-runtime" / "spec-012-luna-targeted.json"
)


def _runner_namespace() -> dict:
    return runpy.run_path(str(RUNNER_PATH))


def test_paid_fixture_preflight_blocks_incomplete_completed_diagnostic() -> None:
    validate = _runner_namespace()["_fixture_preflight_issues"]

    issues = validate(
        [
            {
                "id": "invalid-completed-diagnostic",
                "messages": ["quero comecar"],
                "initial_state": {
                    "canonical_state": "diagnostic_delivered",
                    "diagnostic": {"status": "delivered"},
                },
            }
        ]
    )

    assert any("completed_diagnostic_missing_ledger_keys" in issue for issue in issues)
    assert any("completed_diagnostic_missing_final_fields" in issue for issue in issues)


def test_luna_targeted_fixtures_pass_paid_preflight() -> None:
    namespace = _runner_namespace()
    fixtures = namespace["_load_fixtures"](TARGETED_FIXTURE_PATH)

    assert namespace["_fixture_preflight_issues"](fixtures) == []


def test_markdown_writer_accepts_preflight_scenarios_without_turns(tmp_path: Path) -> None:
    write_markdown = _runner_namespace()["_write_markdown"]
    report_path = tmp_path / "preflight.md"

    write_markdown(
        report_path,
        {
            "task": "T012-057",
            "schema": "012.preflight.test",
            "started_at": "2026-08-05T00:00:00Z",
            "finished_at": "2026-08-05T00:00:00Z",
            "model": "gpt-5.6-luna",
            "paid_approval": "not used in preflight",
            "paid_call_status": "not_attempted_preflight_only",
            "budget": {"max_total_cost_usd": 0.08},
            "summary": {
                "scenario_count": 1,
                "passed_scenarios": 0,
                "total_cost_usd": 0.0,
                "total_model_operations": 0,
            },
            "aborted": False,
            "scenarios": [
                {
                    "scenario_id": "preflight-only",
                    "status": "preflight_only",
                    "transcript": [],
                    "check_results": [],
                    "issues": [],
                    "total_model_operations": 0,
                    "total_cost_usd": 0.0,
                }
            ],
        },
    )

    assert "No rendered exchange was recorded" in report_path.read_text(encoding="utf-8")


def test_paid_runner_stops_after_first_failed_scenario(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    namespace = _runner_namespace()
    run_paid = namespace["_run_paid"]
    result_type = namespace["GoldenScenarioResult"]
    fixture_path = tmp_path / "fixtures.json"
    fixture_path.write_text(
        json.dumps(
            [
                {"id": "first", "title": "First", "messages": ["one"]},
                {"id": "second", "title": "Second", "messages": ["two"]},
            ]
        ),
        encoding="utf-8",
    )
    calls: list[str] = []

    async def fake_run_action_conversation(*_args, initial_state, **_kwargs):
        calls.append(initial_state["conversation_id"])
        return SimpleNamespace(
            total_cost_usd=0.001,
            total_model_operations=1,
            cost_cap_exceeded=False,
        )

    def failed_result(fixture, _conversation):
        return result_type(
            scenario_id=fixture["id"],
            title=fixture["title"],
            status="failed",
            messages=fixture["messages"],
            issues=["expected failure"],
            total_model_operations=1,
            total_cost_usd=0.001,
        )

    monkeypatch.setenv("OPENAI_API_KEY", "test-only-key")
    monkeypatch.setitem(
        run_paid.__globals__,
        "run_action_conversation",
        fake_run_action_conversation,
    )
    monkeypatch.setitem(
        run_paid.__globals__,
        "_scenario_result_from_conversation",
        failed_result,
    )

    payload = asyncio.run(
        run_paid(
            Namespace(
                fixture=fixture_path,
                scenario_id=None,
                model="gpt-5.6-luna",
                evidence_dir=tmp_path / "evidence",
                max_total_cost_usd=0.05,
                approval_note="test-only approval",
                task_id="T012-057-test",
                env_file=None,
            )
        )
    )

    assert calls == ["t012-043-first"]
    assert payload["aborted"] is True
    assert payload["abort_reason"] == "failed_scenario_first"
    assert payload["summary"]["executed_scenarios"] == 1
