"""Local Sales Inbox projection evidence for the action-first SDK path."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

REQUIRED_PROJECTION_FIELDS: tuple[str, ...] = (
    "conversation_id",
    "lead_id",
    "commercial_stage",
    "diagnostic_status",
    "fields",
)

REQUIRED_NESTED_FIELDS: tuple[str, ...] = (
    "template_ids",
    "validator_status",
    "source_labels",
)


def export_sales_inbox_projection_package(
    conversation: Any,
    *,
    scenario_id: str,
    proof_mode: str = "mocked_no_cost",
) -> dict[str, Any]:
    """Build a local JSON-friendly Sales Inbox projection evidence package."""

    turns = list(getattr(conversation, "turns", []) or [])
    packaged_turns = [
        _turn_projection_payload(index, turn) for index, turn in enumerate(turns)
    ]
    delivered_turns = [
        turn for turn in packaged_turns if turn["projection_required"]
    ]
    missing_required = {
        str(turn["index"]): turn["missing_required_fields"]
        for turn in delivered_turns
        if turn["missing_required_fields"]
    }
    missing_projection_indexes = [
        turn["index"]
        for turn in delivered_turns
        if not turn["projection_present"]
    ]

    return {
        "schema": "012.sales_inbox_projection_export.v1",
        "scenario_id": scenario_id,
        "proof_mode": proof_mode,
        "required_projection_fields": list(REQUIRED_PROJECTION_FIELDS),
        "required_nested_fields": list(REQUIRED_NESTED_FIELDS),
        "turn_count": len(packaged_turns),
        "projection_count": sum(
            1 for turn in packaged_turns if turn["projection_present"]
        ),
        "projection_complete": not (
            missing_required or missing_projection_indexes
        ),
        "missing_required_fields": missing_required,
        "missing_projection_turn_indexes": missing_projection_indexes,
        "conversation_summary": {
            "turns_passed": getattr(conversation, "turns_passed", None),
            "final_state": _dump(getattr(conversation, "final_state", {})),
            "total_model_operations": getattr(
                conversation, "total_model_operations", 0
            ),
            "total_cost_usd": getattr(conversation, "total_cost_usd", 0.0),
        },
        "turns": packaged_turns,
    }


def write_sales_inbox_projection_package(
    package: Mapping[str, Any],
    report_dir: Path | str,
) -> Path:
    """Write local-only Sales Inbox projection evidence."""

    output_dir = Path(report_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "sales-inbox-projection-package.json"
    json_path.write_text(
        json.dumps(_dump(package), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "sales-inbox-projection-package.md").write_text(
        _projection_package_markdown(package),
        encoding="utf-8",
    )
    return json_path


def _turn_projection_payload(index: int, turn: Any) -> dict[str, Any]:
    projection = _dump(getattr(turn, "sales_inbox_projection", {}) or {})
    status = getattr(turn, "status", None)
    projection_required = status == "delivered"
    return {
        "index": index,
        "status": status,
        "mode": getattr(turn, "mode", None),
        "selected_action": getattr(turn, "selected_action", None),
        "template_ids": list(getattr(turn, "template_ids", ()) or ()),
        "projection_required": projection_required,
        "projection_present": bool(projection),
        "missing_required_fields": (
            _missing_projection_fields(projection) if projection_required else []
        ),
        "projection": projection,
    }


def _missing_projection_fields(projection: Any) -> list[str]:
    if not isinstance(projection, Mapping) or not projection:
        return list(REQUIRED_PROJECTION_FIELDS)
    missing = [
        field
        for field in REQUIRED_PROJECTION_FIELDS
        if field not in projection or projection.get(field) in (None, "")
    ]
    fields = projection.get("fields")
    if not isinstance(fields, Mapping):
        missing.extend(f"fields.{field}" for field in REQUIRED_NESTED_FIELDS)
        return missing
    for field in REQUIRED_NESTED_FIELDS:
        if field not in fields or fields.get(field) in (None, "", []):
            missing.append(f"fields.{field}")
    return missing


def _projection_package_markdown(package: Mapping[str, Any]) -> str:
    summary = package.get("conversation_summary", {})
    turns = package.get("turns", [])
    lines = [
        "# Spec 012 Sales Inbox Projection Package",
        "",
        f"- Schema: {package.get('schema')}",
        f"- Scenario: {package.get('scenario_id')}",
        f"- Proof mode: {package.get('proof_mode')}",
        f"- Projection complete: {package.get('projection_complete')}",
        f"- Turn count: {package.get('turn_count')}",
        f"- Projection count: {package.get('projection_count')}",
        f"- Total model operations: {summary.get('total_model_operations', 0)}",
        f"- Total cost USD: {summary.get('total_cost_usd', 0.0)}",
        "",
        "| Turn | Status | Mode | Action | Stage | Diagnostic | Projection |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    if isinstance(turns, Sequence):
        for turn in turns:
            if not isinstance(turn, Mapping):
                continue
            projection = turn.get("projection")
            if not isinstance(projection, Mapping):
                projection = {}
            lines.append(
                f"| {turn.get('index')} | {turn.get('status')} | "
                f"{turn.get('mode')} | {turn.get('selected_action') or ''} | "
                f"{projection.get('commercial_stage') or ''} | "
                f"{projection.get('diagnostic_status') or ''} | "
                f"{turn.get('projection_present')} |"
            )
    return "\n".join(lines) + "\n"


def _dump(value: Any) -> Any:
    if value is None or isinstance(value, str | int | float | bool):
        return value
    if isinstance(value, Mapping):
        return {str(key): _dump(item) for key, item in value.items()}
    if isinstance(value, tuple | list | set):
        return [_dump(item) for item in value]
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    return str(value)
