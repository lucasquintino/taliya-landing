from __future__ import annotations

# ruff: noqa: E402

import asyncio
import json
import sys
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_ROOT = ROOT / "services" / "taliya-agent-runtime"
if str(RUNTIME_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_ROOT))

from app.core.taliya_commercial.conductor import ConductorProviderRequest
from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import InMemoryMemoryStore, RuntimeState

FEATURE = "011-taliya-commercial-agent-core-reset"
TASK = "T011-097"
FEATURE_DIR = ROOT / "specs" / FEATURE
FIXTURE_PATH = FEATURE_DIR / "manual-review-samples" / "shadow-mode-comparison-samples.json"
REPORT_DIR = FEATURE_DIR / "eval-reports"
REPORT_JSON = REPORT_DIR / "agent-runtime-spec011-shadow-compare.json"
REPORT_MD = REPORT_DIR / "agent-runtime-spec011-shadow-compare.md"
TASKS_PATH = FEATURE_DIR / "tasks.md"

STATIC_CHECK_FILES = (
    "services/taliya-agent-runtime/app/core/taliya_commercial/runtime_adapter.py",
    "services/taliya-agent-runtime/app/main.py",
)
PRODUCT_VARIABLE_NAMES = {
    "agent_name",
    "official_demo_link",
    "plan_name",
    "plan_price_summary",
    "product_fact_summary",
    "recommended_plan_or_range",
}
PRODUCT_SOURCES = {"official_product_knowledge", "spec_006_product_contract"}
UNVERIFIED_IDENTITY_SOURCES = {"channel_provided", "inferred", "unverified"}


class FixtureConductorProvider:
    def __init__(self, sample: dict[str, Any]) -> None:
        self.sample = sample
        self.calls: list[ConductorProviderRequest] = []

    def __call__(self, request: ConductorProviderRequest) -> dict[str, Any]:
        self.calls.append(request)
        context = request.context
        decision = deepcopy(self.sample["decision"])
        decision.update(
            {
                "turn_id": context.turn_id,
                "conversation_id": context.conversation_id,
                "channel": context.channel,
                "agent_key": context.agent_key,
            }
        )
        for item in decision.get("template_plan", {}).get("items", []):
            if isinstance(item, dict):
                item.setdefault("channel", context.channel)
        return {
            "decision": decision,
            "model_usage": deepcopy(self.sample["model_usage"]),
        }


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _request_from_sample(sample: dict[str, Any]) -> AgentRunRequest:
    metadata = {
        "spec011_core_contract": "taliya_commercial_core_reset_v1",
        "spec011_shadow_mode": {
            "enabled": True,
            "reason": f"t011_097_shadow_compare:{sample['id']}",
        },
        "provider": sample["channel"],
        **dict(sample.get("metadata") or {}),
    }
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": sample["channel"],
            "conversation": sample["conversation"],
            "message": sample["message"],
            "sender": sample.get("sender") or {},
            "metadata": metadata,
        }
    )


async def _seed_initial_state(
    memory_store: InMemoryMemoryStore,
    request: AgentRunRequest,
    sample: dict[str, Any],
) -> dict[str, Any] | None:
    state_payload = sample.get("initial_state")
    if not isinstance(state_payload, dict):
        return None
    state = RuntimeState(
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        **state_payload,
    )
    await memory_store.save_state(state)
    loaded = await memory_store.load_state(
        request.conversation.conversation_id,
        request.agent_key,
    )
    return loaded.model_dump(mode="json") if loaded is not None else None


async def _run_sample(sample: dict[str, Any]) -> dict[str, Any]:
    request = _request_from_sample(sample)
    memory_store = InMemoryMemoryStore()
    before_state = await _seed_initial_state(memory_store, request, sample)
    provider = FixtureConductorProvider(sample)

    response = await run_spec011_agent_turn(
        request,
        memory_store=memory_store,
        provider="mock",
        model=sample["model_usage"]["model"],
        conductor_provider=provider,
    )

    after_state = await memory_store.load_state(
        request.conversation.conversation_id,
        request.agent_key,
    )
    events = await memory_store.list_events(request.conversation.conversation_id)
    usage_records = await memory_store.list_model_usage(request.conversation.conversation_id)
    shadow_events = [
        event
        for event in events
        if event.content == "spec011_shadow_turn_completed"
    ]
    event = shadow_events[0] if shadow_events else None
    trace = event.metadata.get("trace") if event is not None else None
    if not isinstance(trace, dict):
        trace = {}

    assertions: list[dict[str, Any]] = []
    _compare_shadow_envelope(
        assertions=assertions,
        sample=sample,
        response=response.model_dump(mode="json"),
        provider_call_count=len(provider.calls),
    )
    _compare_trace_artifacts(assertions=assertions, sample=sample, trace=trace)
    _compare_sales_inbox(assertions=assertions, sample=sample, trace=trace)
    _compare_persistence(
        assertions=assertions,
        sample=sample,
        trace=trace,
        events=[event.model_dump(mode="json") for event in events],
        usage_records=usage_records,
        before_state=before_state,
        after_state=after_state.model_dump(mode="json") if after_state is not None else None,
    )
    _compare_static_quarantine(assertions)

    failed = [item for item in assertions if not item["ok"]]
    decision = _trace_value(trace, "decision", {})
    rendered_messages = _trace_value(trace, "rendered_messages", [])
    runtime_state = _trace_value(trace, "runtime_state_diff", {})
    sales_inbox_projection = _trace_value(trace, "sales_inbox_projection", {})
    delivery_events = _trace_value(trace, "delivery_events", [])

    return {
        "scenario_id": sample["id"],
        "title": sample["title"],
        "status": "PASS" if not failed else "FAIL",
        "severity": "P0",
        "channel": sample["channel"],
        "review_cases": sample.get("review_cases", []),
        "input_messages": [request.message.model_dump(mode="json")],
        "public_messages": response.output.messages,
        "rendered_messages": rendered_messages,
        "decision_json": decision,
        "validator_results": [_trace_value(trace, "validator_result", {})],
        "repair_attempts": [_trace_value(trace, "repair_result", {})],
        "model_usage": _trace_value(trace, "model_usage", {}),
        "runtime_state": runtime_state,
        "sales_inbox_projection": sales_inbox_projection,
        "delivery_events": delivery_events,
        "trace_complete": _trace_value(trace, "trace_complete", False),
        "schema_version": _trace_value(trace, "input", {}).get("schema_version"),
        "golden_transcript_diff": _golden_diff(sample, trace, failed),
        "assertions": assertions,
        "failure_reason": ", ".join(item["id"] for item in failed) if failed else None,
        "artifact_paths": [
            _relative(FIXTURE_PATH),
            _relative(REPORT_JSON),
            _relative(REPORT_MD),
        ],
    }


def _compare_shadow_envelope(
    *,
    assertions: list[dict[str, Any]],
    sample: dict[str, Any],
    response: dict[str, Any],
    provider_call_count: int,
) -> None:
    delivery_control = response.get("delivery_control") or {}
    output = response.get("output") or {}
    _assert_equal(
        assertions,
        f"{sample['id']}:provider_called_once",
        1,
        provider_call_count,
    )
    _assert_equal(
        assertions,
        f"{sample['id']}:shadow_mode_true",
        True,
        delivery_control.get("shadow_mode"),
    )
    _assert_equal(
        assertions,
        f"{sample['id']}:delivery_suppressed_true",
        True,
        delivery_control.get("delivery_suppressed"),
    )
    _assert_equal(
        assertions,
        f"{sample['id']}:public_messages_empty",
        [],
        output.get("messages"),
    )
    _assert_truthy(
        assertions,
        f"{sample['id']}:response_model_usage_present",
        (output.get("usage") or {}).get("input_tokens"),
    )


def _compare_trace_artifacts(
    *,
    assertions: list[dict[str, Any]],
    sample: dict[str, Any],
    trace: dict[str, Any],
) -> None:
    expected = sample["expected"]
    decision = _trace_value(trace, "decision", {})
    diagnostic = decision.get("diagnostic") or {}
    waitlist = decision.get("waitlist") or {}
    demo = decision.get("demo") or {}
    handoff = decision.get("handoff") or {}
    render_plan = decision.get("template_plan") or {}
    render_items = render_plan.get("items") or []
    rendered_messages = _trace_value(trace, "rendered_messages", [])
    rendered_text = _joined_rendered_text(rendered_messages)

    _assert_equal(assertions, f"{sample['id']}:trace_complete", True, trace.get("trace_complete"))
    for key in ("role", "route", "current_state", "next_state"):
        _assert_equal(
            assertions,
            f"{sample['id']}:decision_{key}",
            expected[key],
            decision.get(key),
        )
    _assert_equal(
        assertions,
        f"{sample['id']}:detected_intents",
        expected["detected_intents"],
        decision.get("detected_intents"),
    )
    _assert_equal(
        assertions,
        f"{sample['id']}:direct_question_answered_first",
        expected["direct_question_answered_first"],
        decision.get("direct_question_answered_first"),
    )
    _assert_equal(
        assertions,
        f"{sample['id']}:diagnostic_action",
        expected["diagnostic_action"],
        diagnostic.get("action", "none"),
    )
    if "next_question_key" in expected:
        _assert_equal(
            assertions,
            f"{sample['id']}:diagnostic_next_question",
            expected["next_question_key"],
            diagnostic.get("next_question_key"),
        )
    if "ledger_updates" in expected:
        _assert_subset_dicts(
            assertions,
            f"{sample['id']}:diagnostic_ledger_updates",
            expected["ledger_updates"],
            diagnostic.get("ledger_updates") or [],
        )
    _assert_equal(
        assertions,
        f"{sample['id']}:waitlist_status",
        expected["waitlist_status"],
        waitlist.get("status", "none"),
    )
    _assert_equal(
        assertions,
        f"{sample['id']}:demo_status",
        expected["demo_status"],
        demo.get("status", "not_offered"),
    )
    _assert_equal(
        assertions,
        f"{sample['id']}:handoff_status",
        expected["handoff_status"],
        handoff.get("status", "none"),
    )
    _assert_subset_dicts(
        assertions,
        f"{sample['id']}:numeric_interpretations",
        expected.get("numeric_interpretations", []),
        decision.get("numeric_interpretations") or [],
    )
    _assert_equal(
        assertions,
        f"{sample['id']}:render_plan_template_ids",
        expected["template_ids"],
        [item.get("template_id") for item in render_items],
    )
    _assert_equal(
        assertions,
        f"{sample['id']}:rendered_trace_template_ids",
        expected["template_ids"],
        _unique_ordered(message.get("template_id") for message in rendered_messages),
    )
    _assert_truthy(
        assertions,
        f"{sample['id']}:rendered_trace_messages_present",
        rendered_messages,
    )
    for snippet in expected.get("rendered_text_must_include", []):
        _assert_contains(
            assertions,
            f"{sample['id']}:rendered_contains:{snippet}",
            rendered_text,
            snippet,
        )
    for snippet in expected.get("rendered_text_must_not_include", []):
        _assert_not_contains(
            assertions,
            f"{sample['id']}:rendered_excludes:{snippet}",
            rendered_text,
            snippet,
        )
    _assert_product_variable_sources(assertions, sample, render_items)
    validator = _trace_value(trace, "validator_result", {})
    repair = _trace_value(trace, "repair_result", {})
    _assert_equal(assertions, f"{sample['id']}:validator_passed", "passed", validator.get("status"))
    _assert_equal(
        assertions,
        f"{sample['id']}:validator_accepted",
        "accepted",
        validator.get("final_disposition"),
    )
    _assert_equal(
        assertions,
        f"{sample['id']}:repair_not_needed",
        "not_needed",
        repair.get("status"),
    )
    usage = _trace_value(trace, "model_usage", {})
    _assert_truthy(assertions, f"{sample['id']}:trace_model_usage_model", usage.get("model"))
    _assert_number_gt(assertions, f"{sample['id']}:trace_model_usage_input", usage.get("input_tokens"), 0)
    _assert_number_gt(assertions, f"{sample['id']}:trace_model_usage_output", usage.get("output_tokens"), 0)


def _compare_sales_inbox(
    *,
    assertions: list[dict[str, Any]],
    sample: dict[str, Any],
    trace: dict[str, Any],
) -> None:
    expected = sample["expected"]["sales_inbox"]
    projection = _trace_value(trace, "sales_inbox_projection", {})
    fields = projection.get("fields") or {}

    for key in ("commercial_stage", "diagnostic_status", "waitlist_status", "handoff_status"):
        _assert_equal(
            assertions,
            f"{sample['id']}:sales_inbox_{key}",
            expected[key],
            projection.get(key),
        )
    _assert_equal(
        assertions,
        f"{sample['id']}:sales_inbox_lead_id",
        sample["conversation"]["lead_id"],
        projection.get("lead_id"),
    )
    _assert_equal(
        assertions,
        f"{sample['id']}:sales_inbox_template_ids",
        sample["expected"]["template_ids"],
        fields.get("template_ids"),
    )
    _assert_equal(
        assertions,
        f"{sample['id']}:sales_inbox_operator_next_action",
        expected["operator_next_action"],
        fields.get("operator_next_action"),
    )
    _assert_equal(
        assertions,
        f"{sample['id']}:sales_inbox_source_labels",
        expected["source_labels"],
        fields.get("source_labels"),
    )
    unverified_marked_verified = [
        identity
        for identity in projection.get("identity") or []
        if identity.get("source") in UNVERIFIED_IDENTITY_SOURCES and identity.get("verified") is True
    ]
    _assert_equal(
        assertions,
        f"{sample['id']}:sales_inbox_unverified_identity_not_promoted",
        [],
        unverified_marked_verified,
    )


def _compare_persistence(
    *,
    assertions: list[dict[str, Any]],
    sample: dict[str, Any],
    trace: dict[str, Any],
    events: list[dict[str, Any]],
    usage_records: list[dict[str, Any]],
    before_state: dict[str, Any] | None,
    after_state: dict[str, Any] | None,
) -> None:
    runtime_state = _trace_value(trace, "runtime_state_diff", {})
    delivery_events = _trace_value(trace, "delivery_events", [])

    _assert_equal(
        assertions,
        f"{sample['id']}:runtime_state_source",
        "accepted_decision",
        runtime_state.get("source"),
    )
    _assert_equal(
        assertions,
        f"{sample['id']}:runtime_state_current_state",
        sample["expected"]["next_state"],
        (runtime_state.get("set") or {}).get("current_state"),
    )
    _assert_equal(
        assertions,
        f"{sample['id']}:runtime_state_template_ids",
        sample["expected"]["template_ids"],
        (runtime_state.get("set") or {}).get("last_selected_template_ids"),
    )
    _assert_equal(
        assertions,
        f"{sample['id']}:shadow_state_not_mutated",
        before_state,
        after_state,
    )
    _assert_equal(
        assertions,
        f"{sample['id']}:one_shadow_event",
        1,
        len([event for event in events if event.get("content") == "spec011_shadow_turn_completed"]),
    )
    _assert_equal(
        assertions,
        f"{sample['id']}:model_usage_recorded_once",
        1,
        len(usage_records),
    )
    if usage_records:
        _assert_equal(
            assertions,
            f"{sample['id']}:model_usage_marked_shadow",
            True,
            usage_records[0].get("shadow_mode"),
        )
    _assert_equal(
        assertions,
        f"{sample['id']}:delivery_events_suppressed_only",
        ["delivery_suppressed"],
        [event.get("event") for event in delivery_events],
    )
    _assert_equal(
        assertions,
        f"{sample['id']}:delivery_events_status_suppressed",
        ["suppressed"],
        [event.get("status") for event in delivery_events],
    )


def _compare_static_quarantine(assertions: list[dict[str, Any]]) -> None:
    hits: list[dict[str, Any]] = []
    for relative_path in STATIC_CHECK_FILES:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if "app.runtime.runner" in line or "run_agent_turn(" in line:
                hits.append(
                    {
                        "path": relative_path,
                        "line": line_number,
                        "text": line.strip(),
                    }
                )
    _assert_equal(
        assertions,
        "static:old_python_runner_not_called",
        [],
        hits,
    )


def _assert_product_variable_sources(
    assertions: list[dict[str, Any]],
    sample: dict[str, Any],
    render_items: list[dict[str, Any]],
) -> None:
    bad_variables: list[dict[str, Any]] = []
    for item in render_items:
        variables = item.get("variables") or {}
        for name, variable in variables.items():
            if name not in PRODUCT_VARIABLE_NAMES:
                continue
            if variable.get("source") not in PRODUCT_SOURCES:
                bad_variables.append(
                    {
                        "template_id": item.get("template_id"),
                        "variable": name,
                        "source": variable.get("source"),
                    }
                )
    _assert_equal(
        assertions,
        f"{sample['id']}:product_variables_use_official_sources",
        [],
        bad_variables,
    )


def _golden_diff(
    sample: dict[str, Any],
    trace: dict[str, Any],
    failed: list[dict[str, Any]],
) -> dict[str, Any]:
    decision = _trace_value(trace, "decision", {})
    rendered_text = _joined_rendered_text(_trace_value(trace, "rendered_messages", []))
    projection = _trace_value(trace, "sales_inbox_projection", {})
    return {
        "basis": "manual_review_sample_until_t011_019_t011_019a_complete",
        "versioned_golden_transcripts_complete": False,
        "phase_10_golden_gate_satisfied": False,
        "status": "matched_manual_sample" if not failed else "drift_from_manual_sample",
        "expected": sample["expected"],
        "observed": {
            "route": decision.get("route"),
            "role": decision.get("role"),
            "detected_intents": decision.get("detected_intents"),
            "template_ids": [
                item.get("template_id")
                for item in (decision.get("template_plan") or {}).get("items", [])
            ],
            "rendered_text_excerpt": rendered_text[:500],
            "sales_inbox": {
                "commercial_stage": projection.get("commercial_stage"),
                "diagnostic_status": projection.get("diagnostic_status"),
                "waitlist_status": projection.get("waitlist_status"),
                "handoff_status": projection.get("handoff_status"),
                "source_labels": (projection.get("fields") or {}).get("source_labels"),
            },
        },
    }


def _assert_equal(
    assertions: list[dict[str, Any]],
    assertion_id: str,
    expected: Any,
    actual: Any,
) -> None:
    assertions.append(
        {
            "id": assertion_id,
            "ok": actual == expected,
            "expected": expected,
            "actual": actual,
        }
    )


def _assert_truthy(
    assertions: list[dict[str, Any]],
    assertion_id: str,
    actual: Any,
) -> None:
    assertions.append(
        {
            "id": assertion_id,
            "ok": bool(actual),
            "expected": "truthy",
            "actual": actual,
        }
    )


def _assert_number_gt(
    assertions: list[dict[str, Any]],
    assertion_id: str,
    actual: Any,
    threshold: float,
) -> None:
    try:
        numeric = float(actual)
    except (TypeError, ValueError):
        numeric = float("-inf")
    assertions.append(
        {
            "id": assertion_id,
            "ok": numeric > threshold,
            "expected": f">{threshold}",
            "actual": actual,
        }
    )


def _assert_contains(
    assertions: list[dict[str, Any]],
    assertion_id: str,
    text: str,
    snippet: str,
) -> None:
    assertions.append(
        {
            "id": assertion_id,
            "ok": snippet.casefold() in text.casefold(),
            "expected": f"contains:{snippet}",
            "actual": text,
        }
    )


def _assert_not_contains(
    assertions: list[dict[str, Any]],
    assertion_id: str,
    text: str,
    snippet: str,
) -> None:
    assertions.append(
        {
            "id": assertion_id,
            "ok": snippet.casefold() not in text.casefold(),
            "expected": f"excludes:{snippet}",
            "actual": text,
        }
    )


def _assert_subset_dicts(
    assertions: list[dict[str, Any]],
    assertion_id: str,
    expected: list[dict[str, Any]],
    actual: list[dict[str, Any]],
) -> None:
    missing = []
    for expected_item in expected:
        if not any(_dict_contains(actual_item, expected_item) for actual_item in actual):
            missing.append(expected_item)
    assertions.append(
        {
            "id": assertion_id,
            "ok": not missing,
            "expected": expected,
            "actual": actual,
            "missing": missing,
        }
    )


def _dict_contains(actual: Any, expected: dict[str, Any]) -> bool:
    if not isinstance(actual, dict):
        return False
    return all(actual.get(key) == value for key, value in expected.items())


def _trace_value(trace: dict[str, Any], key: str, default: Any) -> Any:
    value = trace.get(key)
    return value if value is not None else default


def _joined_rendered_text(rendered_messages: list[dict[str, Any]]) -> str:
    return "\n".join(
        str(message.get("text") or "")
        for message in rendered_messages
        if isinstance(message, dict)
    )


def _unique_ordered(values: Any) -> list[Any]:
    unique = []
    for value in values:
        if value is None or value in unique:
            continue
        unique.append(value)
    return unique


def _relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def _golden_status_from_tasks(fixture: dict[str, Any]) -> dict[str, Any]:
    status = deepcopy(fixture.get("golden_transcript_status") or {})
    tasks_text = TASKS_PATH.read_text(encoding="utf-8")
    status["tasks_md_t011_019_checked"] = "- [x] T011-019 " in tasks_text
    status["tasks_md_t011_019a_checked"] = "- [x] T011-019A " in tasks_text
    status["versioned_golden_transcripts_complete"] = bool(
        status["tasks_md_t011_019_checked"]
        and status["tasks_md_t011_019a_checked"]
    )
    status["phase_10_claim"] = (
        "not_satisfied_by_this_shadow_comparison"
        if not status["versioned_golden_transcripts_complete"]
        else "golden_tasks_marked_complete_but_phase_10_still_requires_full_gate"
    )
    return status


def _write_report(report: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(
        json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# agent-runtime-spec011-shadow-compare",
        "",
        f"Generated at: {report['created_at']}",
        f"Release gate: {report['release_gate']}",
        f"Passed: {report['summary']['passed']}/{report['summary']['scenario_count']}",
        "",
        "Golden transcript status: versioned goldens are incomplete; this report "
        "uses replayable manual review samples and does not satisfy Phase 10 "
        "golden/do-not-do approval.",
        "",
    ]
    for scenario in report["scenarios"]:
        failed_assertions = [
            assertion["id"]
            for assertion in scenario["assertions"]
            if not assertion["ok"]
        ]
        lines.extend(
            [
                f"## {scenario['status']} {scenario['scenario_id']}",
                "",
                f"Channel: {scenario['channel']}",
                f"Review cases: {', '.join(scenario['review_cases'])}",
                f"Public messages delivered: {len(scenario['public_messages'])}",
                f"Rendered trace messages: {len(scenario['rendered_messages'])}",
                "Decision route: "
                f"{scenario['decision_json'].get('route')} / "
                f"{scenario['decision_json'].get('role')}",
                "Sales Inbox stage: "
                f"{scenario['sales_inbox_projection'].get('commercial_stage')}",
                "Failed assertions: "
                f"{', '.join(failed_assertions) if failed_assertions else 'none'}",
                "",
            ]
        )
    REPORT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


async def _main_async() -> int:
    fixture = _load_json(FIXTURE_PATH)
    scenarios = []
    for sample in fixture.get("samples", []):
        scenarios.append(await _run_sample(sample))

    failed = [scenario for scenario in scenarios if scenario["status"] != "PASS"]
    assertion_count = sum(len(scenario["assertions"]) for scenario in scenarios)
    failed_assertion_count = sum(
        1
        for scenario in scenarios
        for assertion in scenario["assertions"]
        if not assertion["ok"]
    )
    golden_status = _golden_status_from_tasks(fixture)
    report = {
        "schema_version": "011.shadow_compare.report.v1",
        "feature": FEATURE,
        "task": TASK,
        "created_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "release_gate": "fail" if failed else "pass_with_manual_review_samples",
        "summary": {
            "scenario_count": len(scenarios),
            "passed": len(scenarios) - len(failed),
            "failed": len(failed),
            "assertion_count": assertion_count,
            "failed_assertion_count": failed_assertion_count,
        },
        "golden_transcript_status": golden_status,
        "checked_files": [
            _relative(FIXTURE_PATH),
            *STATIC_CHECK_FILES,
        ],
        "scenarios": scenarios,
    }
    _write_report(report)
    if failed:
        print(
            "agent-runtime-spec011-shadow-compare: "
            f"{len(failed)} failure(s). Report: {_relative(REPORT_JSON)}"
        )
        return 1
    print(
        "agent-runtime-spec011-shadow-compare: "
        f"{len(scenarios)}/{len(scenarios)} passed. Report: {_relative(REPORT_JSON)}"
    )
    return 0


def main() -> int:
    return asyncio.run(_main_async())


if __name__ == "__main__":
    raise SystemExit(main())
