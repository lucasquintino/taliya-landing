from __future__ import annotations

import hashlib
import json
from pathlib import Path

from app.core.taliya_commercial.schemas import (
    ConductorDecision,
    DeliveryEvent,
    ModelUsage,
    RenderedMessage,
    RenderPlan,
    RepairResult,
    SalesInboxProjection,
    TraceRecord,
    TurnContext,
    ValidatorResult,
)


class TracePersistenceError(ValueError):
    pass


def build_turn_trace(
    *,
    context: TurnContext,
    decision: ConductorDecision,
    validator_result: ValidatorResult,
    repair_result: RepairResult,
    render_plan: RenderPlan,
    rendered_messages: list[RenderedMessage],
    model_usage: ModelUsage,
    runtime_state_diff: dict[str, object],
    delivery_events: list[DeliveryEvent],
    sales_inbox_projection: SalesInboxProjection,
    turn_situation: dict[str, object] | None = None,
    action_decision: dict[str, object] | None = None,
    action_repair_attempt_count: int = 0,
    trace_id: str | None = None,
) -> TraceRecord:
    record = TraceRecord(
        trace_id=trace_id or _stable_trace_id(context, decision),
        turn_id=context.turn_id,
        input=context,
        turn_situation=dict(turn_situation or {}),
        action_decision=dict(action_decision or {}),
        action_repair_attempt_count=action_repair_attempt_count,
        decision=decision,
        validator_result=validator_result,
        repair_result=repair_result,
        render_plan=render_plan,
        rendered_messages=rendered_messages,
        model_usage=model_usage,
        runtime_state_diff=dict(runtime_state_diff),
        delivery_events=delivery_events,
        sales_inbox_projection=sales_inbox_projection,
        trace_complete=True,
    )
    _validate_trace_record(record)
    return record


def trace_record_to_json(record: TraceRecord) -> str:
    _validate_trace_record(record)
    return json.dumps(
        record.model_dump(mode="json"),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )


def trace_record_from_json(payload: str) -> TraceRecord:
    record = TraceRecord.model_validate_json(payload)
    _validate_trace_record(record)
    return record


class TraceFileStore:
    def __init__(self, directory: str | Path) -> None:
        self.directory = Path(directory)

    def save(self, record: TraceRecord) -> Path:
        _validate_trace_record(record)
        self.directory.mkdir(parents=True, exist_ok=True)
        path = self._path_for(record.trace_id)
        path.write_text(trace_record_to_json(record), encoding="utf-8")
        return path

    def load(self, trace_id: str) -> TraceRecord:
        return trace_record_from_json(
            self._path_for(trace_id).read_text(encoding="utf-8")
        )

    def list_for_conversation(self, conversation_id: str) -> list[TraceRecord]:
        records: list[TraceRecord] = []
        if not self.directory.exists():
            return records
        for path in sorted(self.directory.glob("*.json")):
            record = trace_record_from_json(path.read_text(encoding="utf-8"))
            if record.input.conversation_id == conversation_id:
                records.append(record)
        return records

    def _path_for(self, trace_id: str) -> Path:
        return self.directory / f"{_safe_trace_id(trace_id)}.json"


def _validate_trace_record(record: TraceRecord) -> None:
    context = record.input
    decision = record.decision

    _require_equal("turn_id", record.turn_id, context.turn_id)
    _require_equal("decision.turn_id", decision.turn_id, context.turn_id)
    _require_equal(
        "decision.conversation_id",
        decision.conversation_id,
        context.conversation_id,
    )
    _require_equal("decision.agent_key", decision.agent_key, context.agent_key)
    _require_equal("decision.channel", decision.channel, context.channel)

    if record.validator_result.decision_id != decision.decision_id:
        raise TracePersistenceError("validator_result decision_id mismatch")
    if record.render_plan != decision.template_plan:
        raise TracePersistenceError("render_plan must match validated decision")
    if record.sales_inbox_projection.conversation_id != context.conversation_id:
        raise TracePersistenceError("sales_inbox_projection conversation_id mismatch")
    if record.action_decision:
        _require_equal(
            "action_decision.turn_id",
            record.action_decision.get("turn_id"),
            context.turn_id,
        )
        _require_equal(
            "action_decision.conversation_id",
            record.action_decision.get("conversation_id"),
            context.conversation_id,
        )
    if record.render_plan.items and not record.rendered_messages:
        raise TracePersistenceError("rendered_messages are required for rendered turns")
    if not record.delivery_events:
        raise TracePersistenceError("delivery_events are required")
    if not record.trace_complete:
        raise TracePersistenceError("trace_complete must be true")

    _validate_rendered_message_sequence(record.rendered_messages)


def _validate_rendered_message_sequence(messages: list[RenderedMessage]) -> None:
    for expected_sequence, message in enumerate(messages, start=1):
        if message.sequence is not None and message.sequence != expected_sequence:
            raise TracePersistenceError("rendered_messages sequence mismatch")


def _require_equal(field_name: str, left: object, right: object) -> None:
    if left != right:
        raise TracePersistenceError(f"{field_name} mismatch")


def _stable_trace_id(context: TurnContext, decision: ConductorDecision) -> str:
    digest = hashlib.sha256(
        json.dumps(
            {
                "turn_id": context.turn_id,
                "conversation_id": context.conversation_id,
                "decision_id": decision.decision_id,
            },
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()
    return f"trace_{context.turn_id}_{digest[:16]}"


def _safe_trace_id(trace_id: str) -> str:
    safe_id = "".join(
        character
        if character.isalnum() or character in {"-", "_", "."}
        else "_"
        for character in trace_id.strip()
    )
    if not safe_id:
        raise ValueError("trace_id cannot be empty")
    return safe_id
