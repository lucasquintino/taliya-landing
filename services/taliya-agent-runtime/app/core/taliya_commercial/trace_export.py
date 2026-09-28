from __future__ import annotations

import json
from typing import Any

from app.core.taliya_commercial.schemas import TraceRecord
from app.core.taliya_commercial.trace_store import (
    TracePersistenceError,
    trace_record_to_json,
)

_EVAL_REPORT_SCHEMA_VERSION = "011.eval_report.v1"
_REQUIRED_RECORD_KEYS = {
    "scenario_id",
    "status",
    "severity",
    "channel",
    "input_messages",
    "rendered_messages",
    "decision_json",
    "validator_results",
    "repair_attempts",
    "model_usage",
    "runtime_state",
    "sales_inbox_projection",
    "delivery_events",
    "trace_complete",
    "schema_version",
    "golden_transcript_diff",
    "assertions",
    "failure_reason",
    "artifact_paths",
}


class TraceExportError(ValueError):
    pass


def build_trace_eval_record(
    trace: TraceRecord,
    *,
    scenario_id: str,
    status: str = "PASS",
    severity: str = "P0",
    assertions: list[str] | None = None,
    failure_reason: str | None = None,
    artifact_paths: list[str] | None = None,
    golden_transcript_diff: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _validate_trace(trace)
    record = {
        "scenario_id": scenario_id,
        "status": status,
        "severity": severity,
        "channel": trace.input.channel,
        "input_messages": [trace.input.inbound.model_dump(mode="json")],
        "rendered_messages": [
            message.model_dump(mode="json", exclude_none=True)
            for message in trace.rendered_messages
        ],
        "decision_json": trace.decision.model_dump(mode="json"),
        "validator_results": [trace.validator_result.model_dump(mode="json")],
        "repair_attempts": [trace.repair_result.model_dump(mode="json")],
        "model_usage": trace.model_usage.model_dump(mode="json"),
        "runtime_state": dict(trace.runtime_state_diff),
        "sales_inbox_projection": trace.sales_inbox_projection.model_dump(mode="json"),
        "delivery_events": [
            event.model_dump(mode="json", exclude_none=True)
            for event in trace.delivery_events
        ],
        "trace_complete": trace.trace_complete,
        "schema_version": trace.input.schema_version,
        "golden_transcript_diff": golden_transcript_diff,
        "assertions": assertions or [],
        "failure_reason": failure_reason,
        "artifact_paths": artifact_paths or [],
    }
    _validate_record(record)
    return record


def trace_eval_report_to_json(records: list[dict[str, Any]]) -> str:
    for record in records:
        _validate_record(record)
    payload = {
        "schema_version": _EVAL_REPORT_SCHEMA_VERSION,
        "summary": {
            "scenario_count": len(records),
            "passed": sum(1 for record in records if record["status"] == "PASS"),
            "failed": sum(1 for record in records if record["status"] == "FAIL"),
        },
        "scenarios": records,
    }
    return json.dumps(
        payload,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )


def trace_eval_report_to_markdown(records: list[dict[str, Any]]) -> str:
    for record in records:
        _validate_record(record)
    lines = ["# Spec 011 Trace Eval Report", ""]
    for record in records:
        lines.extend(
            [
                f"## {record['scenario_id']}",
                "",
                f"Status: {record['status']}",
                f"Severity: {record['severity']}",
                f"Channel: {record['channel']}",
                f"Trace complete: {str(record['trace_complete']).lower()}",
                f"Model usage: {record['model_usage'].get('model')}",
                "Sales Inbox stage: "
                f"{record['sales_inbox_projection'].get('commercial_stage')}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def _validate_trace(trace: TraceRecord) -> None:
    try:
        trace_record_to_json(trace)
    except (TracePersistenceError, ValueError) as error:
        raise TraceExportError(str(error)) from error


def _validate_record(record: dict[str, Any]) -> None:
    missing = sorted(_REQUIRED_RECORD_KEYS.difference(record))
    if missing:
        raise TraceExportError(
            "trace eval record missing mandatory keys: " + ", ".join(missing)
        )
    if record["trace_complete"] is not True:
        raise TraceExportError("trace eval record must be trace_complete")
    if not record["rendered_messages"]:
        raise TraceExportError("trace eval record missing rendered_messages")
    if not record["delivery_events"]:
        raise TraceExportError("trace eval record missing delivery_events")
    if not record["validator_results"]:
        raise TraceExportError("trace eval record missing validator_results")
    if not record["model_usage"]:
        raise TraceExportError("trace eval record missing model_usage")
    if not record["runtime_state"]:
        raise TraceExportError("trace eval record missing runtime_state")
    if not record["sales_inbox_projection"]:
        raise TraceExportError("trace eval record missing sales_inbox_projection")
