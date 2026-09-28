"""T012-034: local trace assembly for the action-first SDK path.

SDK trace export remains disabled. This module builds a JSON-friendly local
trace record from pipeline artifacts so evals/debugging can prove what the LLM
selected and what deterministic compiler/validators/rendering did with it.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

TRACE_EXPORT_REQUIRED_SECTIONS: tuple[str, ...] = (
    "inbound",
    "turn_gate",
    "context_snapshot",
    "turn_situation",
    "sdk_start",
    "sdk_run_items",
    "sdk_final_output",
    "taliya_proposal",
    "action_decision",
    "compiler",
    "validators",
    "repair_or_escalation",
    "render_plan",
    "rendered_messages",
    "state_diff",
    "sales_inbox_projection",
    "delivery",
    "usage_cost",
)

TRACE_REQUIRED_STATUSES: frozenset[str] = frozenset(
    {"delivered", "failed", "safety_blocked"}
)


def summarize_sdk_run_items(run_result: Any | None) -> list[dict[str, Any]]:
    """Return structural SDK run-item summaries without raw provider payloads."""

    if run_result is None:
        return []
    candidates = (
        getattr(run_result, "new_items", None)
        or getattr(run_result, "items", None)
        or []
    )
    summaries: list[dict[str, Any]] = []
    for item in candidates:
        raw_item = getattr(item, "raw_item", None)
        agent = getattr(item, "agent", None)
        summaries.append(
            {
                "item_type": type(item).__name__,
                "raw_item_type": type(raw_item).__name__ if raw_item is not None else None,
                "agent_name": getattr(agent, "name", None),
                "tool_name": getattr(raw_item, "name", None),
                "handoff_target": getattr(item, "target_agent", None)
                and getattr(item.target_agent, "name", None),
            }
        )
    return summaries


def build_safety_trace(
    *,
    user_text: str,
    message_type: str,
    safety_code: str,
    template_id: str,
    rendered_messages: Sequence[str],
) -> dict[str, Any]:
    return {
        "trace_schema": "012.action_turn_trace.v1",
        "trace_complete": True,
        "inbound": {"text": user_text, "message_type": message_type},
        "turn_gate": {"status": "accepted"},
        "context_snapshot": {
            "state_snapshot": {"safety_blocked": True, "safety_reason": safety_code},
            "compact_memory": None,
            "official_fact_keys_available": [],
        },
        "turn_situation": {"mode": "safety", "llm_turn_allowed": False},
        "sdk_start": {"starting_agent": None, "llm_called": False},
        "sdk_run_items": [],
        "sdk_final_output": None,
        "taliya_proposal": {
            "boundary": "action_first",
            "superseded_schema": "TaliyaTurnProposal",
            "action_decision": None,
            "direct_sdk_delivery_allowed": False,
        },
        "action_decision": None,
        "compiler": {
            "selected_action": None,
            "template_ids": [template_id],
            "state_patch": {"safety_blocked": True, "safety_reason": safety_code},
        },
        "validators": {
            "status": "passed",
            "errors": [],
            "final_disposition": "accepted",
        },
        "repair_or_escalation": {"repair_attempt_count": 0},
        "render_plan": {"template_ids": [template_id]},
        "rendered_messages": list(rendered_messages),
        "state_diff": {"next_state": "safety_blocked"},
        "sales_inbox_projection": None,
        "delivery": {
            "public_delivery": False,
            "outbox_reserved": False,
            "rendered_count": len(rendered_messages),
            "chunk_policy": "whatsapp_max_3",
        },
        "usage_cost": {"model_operations": 0, "cost_usd": 0.0},
        "failure_labels": [safety_code],
    }


def build_action_turn_trace(
    *,
    user_text: str,
    situation: Any,
    starting_agent: str | None,
    run_result: Any | None,
    decision: Any | None,
    compiled: Any | None,
    validation: Any | None,
    rendered_messages: Sequence[str],
    sales_inbox_projection: Mapping[str, Any] | None,
    status: str,
    repairs: int,
    model_operations: int,
    input_tokens: int,
    cached_input_tokens: int,
    cache_write_input_tokens: int,
    output_tokens: int,
    reasoning_tokens: int,
    latency_ms: float,
    cost_usd: float,
    repair_validator_errors: Sequence[Any] = (),
    repair_run_result: Any | None = None,
) -> dict[str, Any]:
    validator_result = getattr(validation, "validator_result", None)
    return {
        "trace_schema": "012.action_turn_trace.v1",
        "trace_complete": status in {"delivered", "failed"},
        "inbound": {"text": user_text, "message_type": "text"},
        "turn_gate": {"status": "accepted"},
        "context_snapshot": _context_snapshot_payload(situation),
        "turn_situation": _turn_situation_payload(situation),
        "sdk_start": {
            "starting_agent": starting_agent,
            "llm_called": starting_agent is not None,
        },
        "sdk_run_items": summarize_sdk_run_items(run_result),
        "sdk_final_output": _dump(decision),
        "taliya_proposal": _action_first_proposal_payload(decision),
        "action_decision": _dump(decision),
        "compiler": _compiled_payload(compiled),
        "validators": _validator_payload(validator_result),
        "repair_or_escalation": {
            "repair_attempt_count": repairs,
            "validator_feedback": [
                _issue_payload(issue) for issue in repair_validator_errors
            ],
            "repair_sdk_run_items": summarize_sdk_run_items(repair_run_result),
        },
        "render_plan": {
            "template_ids": list(getattr(compiled, "template_ids", ()) or ()),
            "variables": _dump(getattr(compiled, "variables", {}) or {}),
            "chunk_policy": getattr(compiled, "chunk_policy", None),
        },
        "rendered_messages": list(rendered_messages),
        "state_diff": {
            "next_state": getattr(compiled, "next_state", None),
            "state_patch": _dump(getattr(compiled, "state_patch", {}) or {}),
            "ledger_updates": _dump(getattr(compiled, "ledger_updates", ()) or ()),
        },
        "sales_inbox_projection": _dump(sales_inbox_projection),
        "delivery": {
            "public_delivery": False,
            "outbox_reserved": False,
            "rendered_count": len(rendered_messages),
            "chunk_policy": getattr(compiled, "chunk_policy", None),
        },
        "usage_cost": {
            "model_operations": model_operations,
            "input_tokens": input_tokens,
            "cached_input_tokens": cached_input_tokens,
            "cache_write_input_tokens": cache_write_input_tokens,
            "output_tokens": output_tokens,
            "reasoning_tokens": reasoning_tokens,
            "latency_ms": latency_ms,
            "cost_usd": cost_usd,
        },
        "failure_labels": _failure_labels(validator_result),
    }


def export_action_conversation_trace_package(
    conversation: Any,
    *,
    scenario_id: str,
    model_name: str | None = None,
    proof_mode: str = "mocked_no_cost",
) -> dict[str, Any]:
    """Build a local-only trace evidence package for one conversation.

    The export is an in-memory JSON-friendly package for eval evidence. It
    deliberately does not enable SDK/provider trace export or write to any
    external store.
    """

    turns = list(getattr(conversation, "turns", []) or [])
    packaged_turns = [_trace_turn_payload(index, turn) for index, turn in enumerate(turns)]
    missing_required_sections = {
        str(turn["index"]): turn["missing_required_sections"]
        for turn in packaged_turns
        if turn["trace_required"] and turn["missing_required_sections"]
    }
    missing_trace_turn_indexes = [
        turn["index"]
        for turn in packaged_turns
        if turn["trace_required"] and not turn["trace_present"]
    ]
    incomplete_trace_turn_indexes = [
        turn["index"]
        for turn in packaged_turns
        if turn["trace_required"] and turn["trace_complete"] is not True
    ]

    return {
        "schema": "012.action_trace_export.v1",
        "scenario_id": scenario_id,
        "proof_mode": proof_mode,
        "model_name": model_name,
        "external_trace_export": {
            "enabled": False,
            "reason": "blocked_by_d_012_007_and_d_012_009",
        },
        "required_sections": list(TRACE_EXPORT_REQUIRED_SECTIONS),
        "trace_count": sum(1 for turn in packaged_turns if turn["trace_present"]),
        "turn_count": len(packaged_turns),
        "trace_complete": not (
            missing_required_sections
            or missing_trace_turn_indexes
            or incomplete_trace_turn_indexes
        ),
        "missing_required_sections": missing_required_sections,
        "missing_trace_turn_indexes": missing_trace_turn_indexes,
        "incomplete_trace_turn_indexes": incomplete_trace_turn_indexes,
        "conversation_summary": {
            "turns_passed": getattr(conversation, "turns_passed", None),
            "final_state": _dump(getattr(conversation, "final_state", {})),
            "transcript": _dump(getattr(conversation, "transcript", [])),
            "total_model_operations": getattr(
                conversation, "total_model_operations", 0
            ),
            "total_cost_usd": getattr(conversation, "total_cost_usd", 0.0),
        },
        "turns": packaged_turns,
    }


def write_action_trace_evidence_package(
    package: Mapping[str, Any],
    report_dir: Path | str,
) -> Path:
    """Write a local-only trace package and markdown summary."""

    output_dir = Path(report_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "mandatory-trace-package.json"
    json_path.write_text(
        json.dumps(_dump(package), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "mandatory-trace-package.md").write_text(
        _trace_package_markdown(package),
        encoding="utf-8",
    )
    return json_path


def _trace_turn_payload(index: int, turn: Any) -> dict[str, Any]:
    trace = _dump(getattr(turn, "trace", {}) or {})
    status = getattr(turn, "status", None)
    trace_required = status in TRACE_REQUIRED_STATUSES
    missing = _missing_required_sections(trace) if trace_required else []
    return {
        "index": index,
        "status": status,
        "mode": getattr(turn, "mode", None),
        "selected_action": getattr(turn, "selected_action", None),
        "template_ids": list(getattr(turn, "template_ids", ()) or ()),
        "trace_required": trace_required,
        "trace_present": bool(trace),
        "trace_complete": trace.get("trace_complete") if isinstance(trace, Mapping) else None,
        "missing_required_sections": missing,
        "sales_inbox_projection_present": bool(
            getattr(turn, "sales_inbox_projection", None)
        ),
        "usage_cost": {
            "model_operations": getattr(turn, "model_operations", 0),
            "cost_usd": getattr(turn, "cost_usd", 0.0),
        },
        "trace": trace,
    }


def _trace_package_markdown(package: Mapping[str, Any]) -> str:
    summary = package.get("conversation_summary", {})
    turns = package.get("turns", [])
    lines = [
        "# Spec 012 Mandatory Trace Package",
        "",
        f"- Schema: {package.get('schema')}",
        f"- Scenario: {package.get('scenario_id')}",
        f"- Proof mode: {package.get('proof_mode')}",
        f"- Trace complete: {package.get('trace_complete')}",
        f"- External trace export enabled: {_external_trace_enabled(package)}",
        f"- Turn count: {package.get('turn_count')}",
        f"- Trace count: {package.get('trace_count')}",
        f"- Total model operations: {summary.get('total_model_operations', 0)}",
        f"- Total cost USD: {summary.get('total_cost_usd', 0.0)}",
        "",
        "| Turn | Status | Mode | Action | Templates | Trace required | Trace present |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    if isinstance(turns, Sequence):
        for turn in turns:
            if not isinstance(turn, Mapping):
                continue
            templates = ", ".join(str(item) for item in turn.get("template_ids", []))
            lines.append(
                f"| {turn.get('index')} | {turn.get('status')} | "
                f"{turn.get('mode')} | {turn.get('selected_action') or ''} | "
                f"{templates} | {turn.get('trace_required')} | "
                f"{turn.get('trace_present')} |"
            )
    return "\n".join(lines) + "\n"


def _external_trace_enabled(package: Mapping[str, Any]) -> bool:
    external = package.get("external_trace_export", {})
    return bool(isinstance(external, Mapping) and external.get("enabled"))


def _missing_required_sections(trace: Any) -> list[str]:
    if not isinstance(trace, Mapping) or not trace:
        return list(TRACE_EXPORT_REQUIRED_SECTIONS)
    return [
        section
        for section in TRACE_EXPORT_REQUIRED_SECTIONS
        if section not in trace
    ]


def _turn_situation_payload(situation: Any) -> dict[str, Any]:
    return {
        "mode": getattr(situation, "mode", None),
        "pending_question_key": getattr(situation, "pending_question_key", None),
        "allowed_actions": list(getattr(situation, "allowed_actions", ()) or ()),
        "eligible_template_groups": list(
            getattr(situation, "eligible_template_groups", ()) or ()
        ),
        "forbidden_actions_now": list(
            getattr(situation, "forbidden_actions_now", ()) or ()
        ),
        "required_obligations": list(
            getattr(situation, "required_obligations", ()) or ()
        ),
        "llm_turn_allowed": getattr(situation, "llm_turn_allowed", None),
        "post_diagnostic_context": _dump(
            getattr(situation, "post_diagnostic_context", None)
        ),
        "profile_name_context": _dump(getattr(situation, "profile_name_context", None)),
    }


def _context_snapshot_payload(situation: Any) -> dict[str, Any]:
    snapshot = _dump(getattr(situation, "state_snapshot", {}) or {})
    return {
        "state_snapshot": snapshot,
        "compact_memory": snapshot.get("summary")
        if isinstance(snapshot, Mapping)
        else None,
        "official_fact_keys_available": list(
            getattr(situation, "official_fact_keys_available", ()) or ()
        ),
        "post_diagnostic_context": _dump(
            getattr(situation, "post_diagnostic_context", None)
        ),
        "profile_name_context": _dump(getattr(situation, "profile_name_context", None)),
    }


def _action_first_proposal_payload(decision: Any | None) -> dict[str, Any]:
    return {
        "boundary": "action_first",
        "superseded_schema": "TaliyaTurnProposal",
        "action_decision": _dump(decision),
        "direct_sdk_delivery_allowed": False,
    }


def _compiled_payload(compiled: Any | None) -> dict[str, Any] | None:
    if compiled is None:
        return None
    return {
        "selected_action": getattr(compiled, "selected_action", None),
        "previous_state": getattr(compiled, "previous_state", None),
        "current_state": getattr(compiled, "current_state", None),
        "next_state": getattr(compiled, "next_state", None),
        "template_ids": list(getattr(compiled, "template_ids", ()) or ()),
        "issues": list(getattr(compiled, "issues", ()) or ()),
    }


def _validator_payload(validator_result: Any | None) -> dict[str, Any] | None:
    if validator_result is None:
        return None
    return {
        "decision_id": getattr(validator_result, "decision_id", None),
        "status": getattr(validator_result, "status", None),
        "errors": [_issue_payload(issue) for issue in getattr(validator_result, "errors", [])],
        "warnings": [
            _issue_payload(issue) for issue in getattr(validator_result, "warnings", [])
        ],
        "repair_attempt_count": getattr(validator_result, "repair_attempt_count", 0),
        "final_disposition": getattr(validator_result, "final_disposition", None),
    }


def _issue_payload(issue: Any) -> dict[str, Any]:
    return {
        "code": getattr(issue, "code", None),
        "message": getattr(issue, "message", None),
    }


def _failure_labels(validator_result: Any | None) -> list[str]:
    if validator_result is None:
        return []
    return [
        str(getattr(issue, "code", "unknown"))
        for issue in getattr(validator_result, "errors", [])
    ]


def _dump(value: Any) -> Any:
    if value is None or isinstance(value, str | int | float | bool):
        return value
    if isinstance(value, Mapping):
        return {str(key): _dump(item) for key, item in value.items()}
    if isinstance(value, tuple | list | set):
        return [_dump(item) for item in value]
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if is_dataclass(value):
        return _dump(asdict(value))
    return str(value)
