from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_ROOT = REPO_ROOT / "services" / "taliya-agent-runtime"
if str(RUNTIME_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_ROOT))

from app.core.taliya_commercial_sdk.action_turn_runner import (  # noqa: E402
    ActionConversationReport,
    run_action_conversation,
)
from app.core.taliya_commercial_sdk.paid_spike_harness import (  # noqa: E402
    MODEL_PRICING_USD_PER_MILLION,
)
from app.settings import get_settings  # noqa: E402

FIXTURE_PATH = (
    REPO_ROOT
    / "scripts"
    / "fixtures"
    / "agent-runtime"
    / "spec-011-golden-transcripts.json"
)
DEFAULT_EVIDENCE_DIR = (
    REPO_ROOT
    / "specs"
    / "012-taliya-commercial-agent-agents-sdk-migration"
    / "evidence"
    / "t012-043-real-model-golden-transcripts"
)
DEFAULT_ENV_FILE = REPO_ROOT / ".env.local"
_REQUIRED_DIAGNOSTIC_KEYS = {
    "active_students_or_size",
    "main_pain",
    "pain_detail",
    "current_process",
    "priority",
    "urgency",
}
_COMPLETE_DIAGNOSTIC_STATUSES = {
    "answered",
    "inferred_from_prior_message",
    "not_applicable",
}


@dataclass
class GoldenScenarioResult:
    scenario_id: str
    title: str
    status: str
    messages: list[str]
    transcript: list[dict[str, str]] = field(default_factory=list)
    turns: list[dict[str, Any]] = field(default_factory=list)
    final_state: dict[str, Any] = field(default_factory=dict)
    checks: list[str] = field(default_factory=list)
    check_results: list[dict[str, Any]] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)
    total_model_operations: int = 0
    total_cost_usd: float = 0.0
    cost_cap_exceeded: bool = False


def _load_fixtures(
    fixture_path: Path,
    scenario_id: str | None = None,
) -> list[dict[str, Any]]:
    fixtures = json.loads(fixture_path.read_text(encoding="utf-8"))
    if scenario_id is None:
        return fixtures
    return [fixture for fixture in fixtures if fixture["id"] == scenario_id]


def _fixture_preflight_issues(fixtures: list[dict[str, Any]]) -> list[str]:
    issues: list[str] = []
    for fixture in fixtures:
        fixture_id = str(fixture.get("id") or "missing_id")
        messages = fixture.get("messages")
        if (
            not isinstance(messages, list)
            or not messages
            or not all(
                isinstance(message, str) and message.strip() for message in messages
            )
        ):
            issues.append(f"{fixture_id}:messages_missing_or_invalid")

        initial_state = fixture.get("initial_state") or {}
        diagnostic = initial_state.get("diagnostic") or {}
        status = str(diagnostic.get("status") or "").casefold()
        canonical_state = str(initial_state.get("canonical_state") or "").casefold()
        completed = status in {"complete", "completed", "delivered"} or (
            canonical_state == "diagnostic_delivered"
        )
        if not completed:
            continue

        ledger = diagnostic.get("ledger") or {}
        complete_keys = {
            key
            for key, entry in ledger.items()
            if isinstance(entry, dict)
            and str(entry.get("status") or "").casefold()
            in _COMPLETE_DIAGNOSTIC_STATUSES
        }
        missing_keys = sorted(_REQUIRED_DIAGNOSTIC_KEYS - complete_keys)
        if missing_keys:
            issues.append(
                f"{fixture_id}:completed_diagnostic_missing_ledger_keys:"
                + ",".join(missing_keys)
            )

        final_fields = diagnostic.get("final_fields") or {}
        missing_final_fields = [
            key
            for key in ("final_plan_or_range", "final_demo_line")
            if not str(final_fields.get(key) or "").strip()
        ]
        if missing_final_fields:
            issues.append(
                f"{fixture_id}:completed_diagnostic_missing_final_fields:"
                + ",".join(missing_final_fields)
            )
    return issues


def _display_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(REPO_ROOT))
    except ValueError:
        return str(resolved)


def _load_openai_key_from_env_file(path: Path) -> bool:
    if os.environ.get("OPENAI_API_KEY") or not path.exists():
        return bool(os.environ.get("OPENAI_API_KEY"))
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        if name.strip() != "OPENAI_API_KEY":
            continue
        secret = value.strip().strip('"').strip("'")
        if secret:
            os.environ["OPENAI_API_KEY"] = secret
            return True
    return False


def _now_slug() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def _normalize(value: str) -> str:
    table = str.maketrans(
        {
            "á": "a",
            "à": "a",
            "ã": "a",
            "â": "a",
            "é": "e",
            "ê": "e",
            "í": "i",
            "ó": "o",
            "ô": "o",
            "õ": "o",
            "ú": "u",
            "ç": "c",
            "Á": "a",
            "À": "a",
            "Ã": "a",
            "Â": "a",
            "É": "e",
            "Ê": "e",
            "Í": "i",
            "Ó": "o",
            "Ô": "o",
            "Õ": "o",
            "Ú": "u",
            "Ç": "c",
        }
    )
    return value.translate(table).lower()


def _all_rendered_text(conversation: ActionConversationReport) -> str:
    return "\n".join(
        item.get("content", "")
        for item in conversation.transcript
        if item.get("role") == "assistant"
    )


def _turns_to_json(conversation: ActionConversationReport) -> list[dict[str, Any]]:
    turns: list[dict[str, Any]] = []
    for index, turn in enumerate(conversation.turns, start=1):
        turns.append(
            {
                "turn": index,
                "user_text": turn.user_text,
                "mode": turn.mode,
                "starting_agent": turn.starting_agent,
                "llm_called": turn.llm_called,
                "status": turn.status,
                "selected_action": turn.selected_action,
                "template_ids": list(turn.template_ids),
                "rendered_messages": list(turn.rendered_messages),
                "issues": list(turn.issues),
                "issue_details": list(turn.issue_details),
                "repairs": turn.repairs,
                "model_operations": turn.model_operations,
                "cost_usd": round(turn.cost_usd, 6),
                "next_state": turn.next_state,
                "sales_inbox_projection": turn.sales_inbox_projection,
                "trace": turn.trace,
            }
        )
    return turns


def _expected_template_ids(fixture: dict[str, Any]) -> list[str]:
    expected = fixture.get("expected") or {}
    decision = expected.get("decision") or {}
    return list(decision.get("template_ids") or [])


def _evaluate_fixture(
    fixture: dict[str, Any],
    conversation: ActionConversationReport,
) -> tuple[list[dict[str, Any]], list[str], str]:
    rendered_text = _all_rendered_text(conversation)
    rendered_norm = _normalize(rendered_text)
    check_results: list[dict[str, Any]] = []
    issues: list[str] = []

    def add(name: str, passed: bool, detail: str = "") -> None:
        check_results.append(
            {"check": name, "passed": passed, "detail": "" if passed else detail}
        )
        if not passed:
            issues.append(f"{name}: {detail}".rstrip(": "))

    all_turns_acceptable = all(
        turn.status in {"delivered", "suppressed", "safety_blocked"}
        for turn in conversation.turns
    )
    add("turn_statuses_acceptable", all_turns_acceptable)

    expected = fixture.get("expected") or {}
    for expected_text in expected.get("rendered_text_must_include") or []:
        add(
            f"includes:{expected_text}",
            _normalize(expected_text) in rendered_norm,
            "missing expected rendered text",
        )
    for banned_text in expected.get("rendered_text_must_not_include") or []:
        add(
            f"excludes:{banned_text}",
            _normalize(banned_text) not in rendered_norm,
            "banned rendered text present",
        )

    for template_id in _expected_template_ids(fixture):
        present = any(template_id in turn.template_ids for turn in conversation.turns)
        add(f"template_present:{template_id}", present, "template was not selected")

    if expected.get("second_turn_must_be_silent"):
        second = conversation.turns[1] if len(conversation.turns) > 1 else None
        add(
            "second_turn_silent",
            bool(
                second
                and not second.rendered_messages
                and second.status == "suppressed"
            ),
            "second turn rendered a message or was not suppressed",
        )

    terminal_failures = [
        issue
        for turn in conversation.turns
        if turn.status == "failed"
        for issue in turn.issues
    ]
    add("no_failed_turns", not terminal_failures, ", ".join(terminal_failures))

    status = "passed" if not issues else "failed"
    return check_results, issues, status


def _scenario_result_from_conversation(
    fixture: dict[str, Any],
    conversation: ActionConversationReport,
) -> GoldenScenarioResult:
    check_results, issues, status = _evaluate_fixture(fixture, conversation)
    return GoldenScenarioResult(
        scenario_id=fixture["id"],
        title=fixture.get("title", fixture["id"]),
        status=status,
        messages=list(fixture["messages"]),
        transcript=list(conversation.transcript),
        turns=_turns_to_json(conversation),
        final_state=conversation.final_state,
        checks=list(fixture.get("checks") or []),
        check_results=check_results,
        issues=issues,
        total_model_operations=conversation.total_model_operations,
        total_cost_usd=round(conversation.total_cost_usd, 6),
        cost_cap_exceeded=conversation.cost_cap_exceeded,
    )


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines: list[str] = [
        f"# {payload['task']} real-model transcripts",
        "",
        f"- Schema: `{payload['schema']}`",
        f"- Started at: `{payload['started_at']}`",
        f"- Finished at: `{payload['finished_at']}`",
        f"- Model: `{payload['model']}`",
        f"- Paid approval: `{payload['paid_approval']}`",
        f"- Paid call status: `{payload['paid_call_status']}`",
        f"- Budget cap: `${payload['budget']['max_total_cost_usd']:.2f}`",
        f"- Total cost: `${payload['summary']['total_cost_usd']:.6f}`",
        f"- Total model operations: `{payload['summary']['total_model_operations']}`",
        "- Passed scenarios: "
        f"`{payload['summary']['passed_scenarios']}/"
        f"{payload['summary']['scenario_count']}`",
        f"- Aborted: `{payload['aborted']}`",
    ]
    if payload.get("abort_reason"):
        lines.append(f"- Abort reason: `{payload['abort_reason']}`")
    lines.extend(["", "## Scenario Summary", ""])
    for scenario in payload["scenarios"]:
        lines.append(
            f"- `{scenario['scenario_id']}`: {scenario['status']} "
            f"({scenario['total_model_operations']} ops, "
            f"${scenario['total_cost_usd']:.6f})"
        )
        if scenario["issues"]:
            lines.append(f"  Issues: {'; '.join(scenario['issues'])}")
    lines.extend(["", "## Full Message Exchanges", ""])
    for scenario in payload["scenarios"]:
        lines.extend(
            [
                f"### {scenario['scenario_id']}",
                "",
                f"Status: `{scenario['status']}`",
                "",
            ]
        )
        turns = scenario.get("turns") or []
        transcript = scenario.get("transcript") or []
        if not turns and not transcript:
            lines.append("_No rendered exchange was recorded._")
            lines.append("")
            continue
        if turns:
            for turn in turns:
                lines.append(f"**user:** {turn.get('user_text', '')}")
                lines.append("")
                rendered_messages = turn.get("rendered_messages") or []
                for message in rendered_messages:
                    lines.append(f"**assistant:** {message}")
                    lines.append("")
                if not rendered_messages:
                    status = turn.get("status", "unknown")
                    issues = ", ".join(turn.get("issues") or [])
                    detail = f"; issues: {issues}" if issues else ""
                    lines.append(
                        f"_No assistant message delivered (status: {status}{detail})._"
                    )
                    lines.append("")
        else:
            for item in transcript:
                role = item.get("role", "unknown")
                content = item.get("content", "")
                lines.append(f"**{role}:** {content}")
                lines.append("")
        lines.append("Checks:")
        for check in scenario["check_results"]:
            marker = "PASS" if check["passed"] else "FAIL"
            detail = f" - {check['detail']}" if check.get("detail") else ""
            lines.append(f"- `{marker}` {check['check']}{detail}")
        lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


async def _run_paid(args: argparse.Namespace) -> dict[str, Any]:
    fixtures = _load_fixtures(args.fixture, args.scenario_id)
    model = args.model or get_settings().model
    started_at = datetime.now(UTC).isoformat()
    run_dir = args.evidence_dir / _now_slug()
    results: list[GoldenScenarioResult] = []
    total_cost = 0.0
    total_ops = 0
    aborted = False
    abort_reason: str | None = None
    if not args.approval_note:
        return _write_blocked_paid_report(
            run_dir=run_dir,
            fixtures=fixtures,
            model=model,
            started_at=started_at,
            args=args,
            abort_reason="A current paid-run approval note is required.",
        )
    if args.scenario_id and not fixtures:
        return _write_blocked_paid_report(
            run_dir=run_dir,
            fixtures=[],
            model=model,
            started_at=started_at,
            args=args,
            abort_reason=f"Scenario '{args.scenario_id}' was not found.",
        )

    fixture_issues = _fixture_preflight_issues(fixtures)
    if fixture_issues:
        return _write_blocked_paid_report(
            run_dir=run_dir,
            fixtures=fixtures,
            model=model,
            started_at=started_at,
            args=args,
            abort_reason="fixture_preflight_failed:" + ";".join(fixture_issues),
        )

    if model not in MODEL_PRICING_USD_PER_MILLION:
        return _write_blocked_paid_report(
            run_dir=run_dir,
            fixtures=fixtures,
            model=model,
            started_at=started_at,
            args=args,
            abort_reason=f"Model '{model}' has no recorded pricing.",
        )
    if not os.environ.get("OPENAI_API_KEY") and not get_settings().openai_api_key:
        return _write_blocked_paid_report(
            run_dir=run_dir,
            fixtures=fixtures,
            model=model,
            started_at=started_at,
            args=args,
            abort_reason=(
                "OPENAI_API_KEY is not available in the environment or runtime .env."
            ),
        )

    for fixture in fixtures:
        remaining = args.max_total_cost_usd - total_cost
        if remaining <= 0:
            aborted = True
            abort_reason = "budget_cap_reached_before_next_scenario"
            break
        try:
            fixture_initial_state = dict(fixture.get("initial_state") or {})
            fixture_initial_state.update(
                {
                    "conversation_id": f"t012-043-{fixture['id']}",
                    "lead_id": f"t012-043-{fixture['id']}",
                    "source": fixture.get("source"),
                    "channel": fixture.get("channel", "whatsapp"),
                }
            )
            conversation = await run_action_conversation(
                fixture["messages"],
                model=model,
                paid_openai_approved=True,
                initial_state=fixture_initial_state,
                max_total_cost_usd=remaining,
            )
            result = _scenario_result_from_conversation(fixture, conversation)
        except Exception as exc:
            result = GoldenScenarioResult(
                scenario_id=fixture["id"],
                title=fixture.get("title", fixture["id"]),
                status="runtime_error",
                messages=list(fixture["messages"]),
                checks=list(fixture.get("checks") or []),
                issues=[f"{type(exc).__name__}: {exc}"],
            )
            aborted = True
            abort_reason = f"runtime_error_in_{fixture['id']}"
            results.append(result)
            _write_json(run_dir / f"{fixture['id']}.json", asdict(result))
            break
        results.append(result)
        total_cost += conversation.total_cost_usd
        total_ops += conversation.total_model_operations
        _write_json(run_dir / f"{fixture['id']}.json", asdict(result))
        if result.status != "passed":
            aborted = True
            abort_reason = f"failed_scenario_{fixture['id']}"
            break
        if conversation.cost_cap_exceeded or total_cost >= args.max_total_cost_usd:
            aborted = True
            abort_reason = "budget_cap_reached"
            break

    finished_at = datetime.now(UTC).isoformat()
    payload = {
        "schema": "012.real_model_golden_transcripts.v1",
        "task": args.task_id,
        "fixture_path": _display_path(args.fixture),
        "started_at": started_at,
        "finished_at": finished_at,
        "model": model,
        "paid_approval": args.approval_note,
        "paid_call_status": "attempted_real_openai",
        "env_file_used": str(args.env_file) if args.env_file else None,
        "budget": {
            "max_total_cost_usd": args.max_total_cost_usd,
            "cap_policy": "conservative local hard cap for this approved run",
        },
        "summary": {
            "scenario_count": len(fixtures),
            "executed_scenarios": len(results),
            "passed_scenarios": sum(
                1 for result in results if result.status == "passed"
            ),
            "failed_scenarios": sum(
                1 for result in results if result.status == "failed"
            ),
            "total_model_operations": total_ops,
            "total_cost_usd": round(total_cost, 6),
        },
        "aborted": aborted,
        "abort_reason": abort_reason,
        "scenarios": [asdict(result) for result in results],
    }
    _write_json(run_dir / "report.json", payload)
    _write_markdown(run_dir / "report.md", payload)
    return payload


def _write_blocked_paid_report(
    *,
    run_dir: Path,
    fixtures: list[dict[str, Any]],
    model: str,
    started_at: str,
    args: argparse.Namespace,
    abort_reason: str,
) -> dict[str, Any]:
    finished_at = datetime.now(UTC).isoformat()
    payload = {
        "schema": "012.real_model_golden_transcripts.v1",
        "task": args.task_id,
        "fixture_path": _display_path(args.fixture),
        "started_at": started_at,
        "finished_at": finished_at,
        "model": model,
        "paid_approval": args.approval_note or "missing_current_approval",
        "paid_call_status": "blocked_before_openai_call",
        "env_file_used": str(args.env_file) if args.env_file else None,
        "budget": {
            "max_total_cost_usd": args.max_total_cost_usd,
            "cap_policy": "conservative local hard cap for this approved run",
        },
        "summary": {
            "scenario_count": len(fixtures),
            "executed_scenarios": 0,
            "passed_scenarios": 0,
            "failed_scenarios": 0,
            "total_model_operations": 0,
            "total_cost_usd": 0.0,
        },
        "aborted": True,
        "abort_reason": abort_reason,
        "scenarios": [
            {
                "scenario_id": fixture["id"],
                "title": fixture.get("title", fixture["id"]),
                "status": "blocked_before_openai_call",
                "messages": fixture["messages"],
                "transcript": [],
                "turns": [],
                "final_state": {},
                "checks": fixture.get("checks") or [],
                "check_results": [],
                "issues": [abort_reason],
                "total_model_operations": 0,
                "total_cost_usd": 0.0,
                "cost_cap_exceeded": False,
            }
            for fixture in fixtures
        ],
    }
    _write_json(run_dir / "report.json", payload)
    _write_markdown(run_dir / "report.md", payload)
    return payload


def _write_preflight(args: argparse.Namespace) -> dict[str, Any]:
    fixtures = _load_fixtures(args.fixture, args.scenario_id)
    fixture_issues = _fixture_preflight_issues(fixtures)
    model = args.model or get_settings().model
    run_dir = args.evidence_dir / f"preflight-{_now_slug()}"
    payload = {
        "schema": "012.real_model_golden_transcripts_preflight.v1",
        "task": args.task_id,
        "created_at": datetime.now(UTC).isoformat(),
        "model": model,
        "fixture_path": _display_path(args.fixture),
        "scenario_count": len(fixtures),
        "scenario_ids": [fixture["id"] for fixture in fixtures],
        "messages_by_scenario": {
            fixture["id"]: fixture["messages"] for fixture in fixtures
        },
        "openai_api_key_available": bool(
            os.environ.get("OPENAI_API_KEY") or get_settings().openai_api_key
        ),
        "env_file_checked": str(args.env_file) if args.env_file else None,
        "model_has_recorded_pricing": model in MODEL_PRICING_USD_PER_MILLION,
        "fixture_validation_status": "passed" if not fixture_issues else "failed",
        "fixture_validation_issues": fixture_issues,
        "max_total_cost_usd": args.max_total_cost_usd,
        "paid_call_status": "not_attempted_preflight_only",
    }
    _write_json(run_dir / "preflight.json", payload)
    _write_markdown(
        run_dir / "preflight.md",
        {
            **payload,
            "started_at": payload["created_at"],
            "finished_at": payload["created_at"],
            "paid_approval": "not used in preflight",
            "paid_call_status": "not_attempted_preflight_only",
            "budget": {"max_total_cost_usd": args.max_total_cost_usd},
            "summary": {
                "scenario_count": len(fixtures),
                "passed_scenarios": 0,
                "total_cost_usd": 0.0,
                "total_model_operations": 0,
            },
            "aborted": False,
            "scenarios": [
                {
                    "scenario_id": fixture["id"],
                    "status": "preflight_only",
                    "messages": fixture["messages"],
                    "transcript": [],
                    "check_results": [],
                    "issues": [],
                    "total_model_operations": 0,
                    "total_cost_usd": 0.0,
                }
                for fixture in fixtures
            ],
        },
    )
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Spec 012 T012-043 real-model golden transcripts."
    )
    parser.add_argument("--model", default=None)
    parser.add_argument(
        "--task-id",
        default="T012-043",
        help="Spec task identifier recorded in generated evidence.",
    )
    parser.add_argument(
        "--fixture",
        type=Path,
        default=FIXTURE_PATH,
        help="Fixture JSON containing the conversations to run.",
    )
    parser.add_argument(
        "--evidence-dir",
        type=Path,
        default=DEFAULT_EVIDENCE_DIR,
        help="Directory where the complete JSON and Markdown evidence is saved.",
    )
    parser.add_argument(
        "--scenario-id",
        default=None,
        help="Optional single golden scenario id to run, e.g. final-price-first.",
    )
    parser.add_argument("--max-total-cost-usd", type=float, default=1.0)
    parser.add_argument(
        "--approval-note",
        default=None,
        help=(
            "Required for a paid run. Records the current user approval and "
            "approved budget in the evidence."
        ),
    )
    parser.add_argument(
        "--env-file",
        type=Path,
        default=DEFAULT_ENV_FILE,
        help="Local env file used only to load OPENAI_API_KEY without printing it.",
    )
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="Load fixtures and write evidence without calling OpenAI.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.env_file:
        _load_openai_key_from_env_file(args.env_file)
    if args.preflight_only:
        payload = _write_preflight(args)
    else:
        payload = asyncio.run(_run_paid(args))
    print(json.dumps(payload, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
