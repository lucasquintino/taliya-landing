"""Manual transcript review package for Spec 012 action-first evidence."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

MANUAL_REVIEW_CHECKLIST: tuple[dict[str, str], ...] = (
    {
        "id": "answers_direct_questions_first",
        "label": "Direct questions are answered before steering",
    },
    {
        "id": "studio_owner_language",
        "label": "Language sounds natural for a Pilates studio owner",
    },
    {
        "id": "official_facts_only",
        "label": "Prices, demo link, availability, and product claims use official facts",
    },
    {
        "id": "diagnostic_flow_quality",
        "label": "Diagnostic questions progress naturally without repeats",
    },
    {
        "id": "final_diagnostic_quality",
        "label": "Final diagnostic is complete, practical, and not truncated",
    },
    {
        "id": "handoff_and_suppression",
        "label": "Human handoff pauses AI replies after acknowledgement",
    },
    {
        "id": "no_unsafe_promises",
        "label": "No checkout, discount, VIP, date, or integration promises are invented",
    },
)


def export_manual_transcript_review_package(
    conversation: Any,
    *,
    scenario_id: str,
    proof_mode: str = "mocked_no_cost",
    reviewer: str = "product_owner",
) -> dict[str, Any]:
    """Build a local package for human transcript review."""

    turns = list(getattr(conversation, "turns", []) or [])
    transcript = list(getattr(conversation, "transcript", []) or [])
    return {
        "schema": "012.manual_transcript_review.v1",
        "scenario_id": scenario_id,
        "proof_mode": proof_mode,
        "review_status": "pending_manual_review",
        "reviewer": reviewer,
        "checklist": [
            {**item, "status": "pending", "notes": ""}
            for item in MANUAL_REVIEW_CHECKLIST
        ],
        "summary": {
            "turn_count": len(turns),
            "delivered_turn_count": sum(
                1 for turn in turns if getattr(turn, "status", None) == "delivered"
            ),
            "suppressed_turn_count": sum(
                1 for turn in turns if getattr(turn, "status", None) == "suppressed"
            ),
            "total_model_operations": getattr(
                conversation, "total_model_operations", 0
            ),
            "total_cost_usd": getattr(conversation, "total_cost_usd", 0.0),
        },
        "transcript": _dump(transcript),
        "turns": [_turn_review_payload(index, turn) for index, turn in enumerate(turns)],
        "final_state": _dump(getattr(conversation, "final_state", {})),
        "manual_review_notes": "",
        "manual_decision": "pending",
    }


def write_manual_transcript_review_package(
    package: Mapping[str, Any],
    report_dir: Path | str,
) -> Path:
    """Write local JSON and Markdown files for manual transcript review."""

    output_dir = Path(report_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "manual-transcript-review-package.json"
    json_path.write_text(
        json.dumps(_dump(package), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "manual-transcript-review-package.md").write_text(
        _manual_review_markdown(package),
        encoding="utf-8",
    )
    return json_path


def _turn_review_payload(index: int, turn: Any) -> dict[str, Any]:
    trace = _dump(getattr(turn, "trace", {}) or {})
    projection = _dump(getattr(turn, "sales_inbox_projection", {}) or {})
    return {
        "index": index,
        "status": getattr(turn, "status", None),
        "mode": getattr(turn, "mode", None),
        "selected_action": getattr(turn, "selected_action", None),
        "template_ids": list(getattr(turn, "template_ids", ()) or ()),
        "rendered_messages": list(getattr(turn, "rendered_messages", ()) or ()),
        "issues": list(getattr(turn, "issues", ()) or ()),
        "repairs": getattr(turn, "repairs", 0),
        "model_operations": getattr(turn, "model_operations", 0),
        "cost_usd": getattr(turn, "cost_usd", 0.0),
        "trace_present": bool(trace),
        "trace_complete": trace.get("trace_complete")
        if isinstance(trace, Mapping)
        else None,
        "sales_inbox_projection_present": bool(projection),
        "projection_lead_id": projection.get("lead_id")
        if isinstance(projection, Mapping)
        else None,
    }


def _manual_review_markdown(package: Mapping[str, Any]) -> str:
    summary = package.get("summary", {})
    lines = [
        "# Spec 012 Manual Transcript Review Package",
        "",
        f"- Schema: {package.get('schema')}",
        f"- Scenario: {package.get('scenario_id')}",
        f"- Proof mode: {package.get('proof_mode')}",
        f"- Review status: {package.get('review_status')}",
        f"- Manual decision: {package.get('manual_decision')}",
        f"- Turn count: {summary.get('turn_count', 0)}",
        f"- Delivered turns: {summary.get('delivered_turn_count', 0)}",
        f"- Suppressed turns: {summary.get('suppressed_turn_count', 0)}",
        f"- Total model operations: {summary.get('total_model_operations', 0)}",
        f"- Total cost USD: {summary.get('total_cost_usd', 0.0)}",
        "",
        "## Checklist",
        "",
    ]
    checklist = package.get("checklist", [])
    if isinstance(checklist, Sequence):
        for item in checklist:
            if isinstance(item, Mapping):
                lines.append(
                    f"- [ ] {item.get('id')}: {item.get('label')} "
                    f"(status: {item.get('status')})"
                )
    lines.extend(["", "## Transcript", ""])
    transcript = package.get("transcript", [])
    if isinstance(transcript, Sequence):
        for item in transcript:
            if not isinstance(item, Mapping):
                continue
            role = str(item.get("role") or "").upper()
            content = item.get("content") or item.get("text") or ""
            lines.append(f"**{role}:** {content}")
            lines.append("")
    lines.extend(["## Turn Summary", ""])
    turns = package.get("turns", [])
    if isinstance(turns, Sequence):
        for turn in turns:
            if not isinstance(turn, Mapping):
                continue
            templates = ", ".join(str(item) for item in turn.get("template_ids", []))
            lines.append(
                f"- Turn {turn.get('index')}: {turn.get('status')} / "
                f"{turn.get('mode')} / {turn.get('selected_action') or ''} / "
                f"{templates} / trace={turn.get('trace_present')} / "
                f"projection={turn.get('sales_inbox_projection_present')}"
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
