from __future__ import annotations

import json
from typing import Any

from app.core.taliya_commercial.schemas import (
    IDENTITY_CONTACT_FACT_KEYS,
    ConductorDecision,
    DeliveryEvent,
    IdentityField,
    SalesInboxProjection,
    TurnContext,
    ValidatorResult,
)
from app.core.taliya_commercial.validators import validate_sales_inbox_projection

_VALIDATED_STATE_SOURCES = {"accepted_decision", "repaired_decision"}
_VALID_DIAGNOSTIC_STATUSES = {
    "not_started",
    "offered",
    "in_progress",
    "completed",
    "insufficient_evidence",
}
_VALID_WAITLIST_STATUSES = {"none", "offered", "pending_details", "joined", "declined"}
_VALID_HANDOFF_STATUSES = {"none", "requested", "active", "resumed"}
_REQUIRED_DIAGNOSTIC_KEYS = (
    "active_students_or_size",
    "main_pain",
    "pain_detail",
    "current_process",
    "priority",
    "urgency",
)
_COMPLETE_DIAGNOSTIC_STATUSES = {
    "answered",
    "inferred_from_prior_message",
    "not_applicable",
}
_IDENTITY_SOURCES = {
    "customer_provided",
    "operator_provided",
    "channel_provided",
    "inferred",
    "unverified",
}


class SalesInboxProjectionBuildError(ValueError):
    pass


def export_projection_identity_facts_for_context(
    projection: SalesInboxProjection,
) -> list[dict[str, Any]]:
    """Export projection identity fields for future context without promotion."""
    facts: list[dict[str, Any]] = []
    for identity in projection.identity:
        facts.append(
            {
                "key": identity.key,
                "value": identity.value,
                "source": "sales_inbox_projection",
                "reliability": "unverified",
                "confidence": "low",
                "evidence": [f"sales_inbox_projection.identity.{identity.key}"],
                "projection_identity_source": identity.source,
                "projection_verified": identity.verified,
            }
        )
    return facts


def build_sales_inbox_projection(
    *,
    context: TurnContext,
    decision: ConductorDecision,
    validator_result: ValidatorResult,
    runtime_state_diff: dict[str, Any],
    delivery_events: list[DeliveryEvent] | None = None,
) -> SalesInboxProjection:
    """Build Sales Inbox projection from validated runtime state and events."""
    events = delivery_events or []
    _validate_projection_sources(
        context=context,
        decision=decision,
        validator_result=validator_result,
        runtime_state_diff=runtime_state_diff,
    )

    fields = _common_fields(
        context=context,
        runtime_state_diff=runtime_state_diff,
        validator_result=validator_result,
    )
    diagnostic_status = _diagnostic_status(context, runtime_state_diff)
    waitlist_status = _waitlist_status(context, runtime_state_diff)
    handoff_status = _handoff_status(context, runtime_state_diff)

    fields.update(
        _diagnostic_fields(
            context=context,
            decision=decision,
            runtime_state_diff=runtime_state_diff,
            diagnostic_status=diagnostic_status,
        )
    )
    fields.update(_demo_fields(runtime_state_diff))
    fields.update(
        _waitlist_fields(
            context=context,
            runtime_state_diff=runtime_state_diff,
            waitlist_status=waitlist_status,
            delivery_events=events,
        )
    )
    fields.update(
        _handoff_fields(
            context=context,
            runtime_state_diff=runtime_state_diff,
            handoff_status=handoff_status,
        )
    )

    projection = SalesInboxProjection(
        conversation_id=context.conversation_id,
        lead_id=_optional_string(context.sales_inbox_inputs.get("lead_id")),
        commercial_stage=_commercial_stage(runtime_state_diff),
        summary=_summary(context, runtime_state_diff),
        diagnostic_status=diagnostic_status,
        waitlist_status=waitlist_status,
        handoff_status=handoff_status,
        identity=_identity_fields(context, runtime_state_diff),
        fields=fields,
    )
    _raise_if_invalid_projection(projection, decision, context)
    return projection


def _validate_projection_sources(
    *,
    context: TurnContext,
    decision: ConductorDecision,
    validator_result: ValidatorResult,
    runtime_state_diff: dict[str, Any],
) -> None:
    if runtime_state_diff.get("schema_version") != "011.runtime_state_diff.v1":
        raise SalesInboxProjectionBuildError("runtime_state_diff schema_version invalid")
    _require_equal(
        "decision_id",
        runtime_state_diff.get("decision_id"),
        decision.decision_id,
    )
    _require_equal(
        "validator decision_id",
        validator_result.decision_id,
        decision.decision_id,
    )
    _require_equal(
        "conversation_id",
        runtime_state_diff.get("conversation_id"),
        context.conversation_id,
    )
    _require_equal("decision conversation_id", decision.conversation_id, context.conversation_id)
    _require_equal("turn_id", runtime_state_diff.get("turn_id"), context.turn_id)
    _require_equal("agent_key", runtime_state_diff.get("agent_key"), context.agent_key)
    _require_equal("channel", runtime_state_diff.get("channel"), context.channel)

    if runtime_state_diff.get("source") not in _VALIDATED_STATE_SOURCES:
        raise SalesInboxProjectionBuildError(
            "Sales Inbox projection requires validated state source"
        )
    if (
        validator_result.status != "passed"
        or validator_result.final_disposition not in {"accepted", "repaired"}
    ):
        raise SalesInboxProjectionBuildError(
            "Sales Inbox projection requires accepted or repaired validation"
        )

    validation = _mapping(runtime_state_diff.get("validation"))
    if validation:
        _require_equal("validator status", validation.get("status"), validator_result.status)
        _require_equal(
            "validator disposition",
            validation.get("final_disposition"),
            validator_result.final_disposition,
        )


def _common_fields(
    *,
    context: TurnContext,
    runtime_state_diff: dict[str, Any],
    validator_result: ValidatorResult,
) -> dict[str, Any]:
    return {
        "template_ids": _selected_template_ids(runtime_state_diff),
        "validator_status": validator_result.status,
        "validator_final_disposition": validator_result.final_disposition,
        "source_labels": _source_labels(context, runtime_state_diff),
        "operator_next_action": _operator_next_action(context, runtime_state_diff),
    }


def _diagnostic_fields(
    *,
    context: TurnContext,
    decision: ConductorDecision,
    runtime_state_diff: dict[str, Any],
    diagnostic_status: str,
) -> dict[str, Any]:
    if diagnostic_status != "completed":
        return {}

    ledger_by_key = _diagnostic_ledger_by_key(context, runtime_state_diff)
    diagnostic_state = _mapping(_state_set(runtime_state_diff).get("diagnostic"))
    final_fields = {
        **_mapping(context.sales_inbox_inputs.get("diagnostic_final_fields")),
        **_mapping(diagnostic_state.get("final_fields")),
    }

    return {
        "diagnostic_ledger_complete": all(
            ledger_by_key.get(question_key) in _COMPLETE_DIAGNOSTIC_STATUSES
            for question_key in _REQUIRED_DIAGNOSTIC_KEYS
        ),
        "required_diagnostic_keys": list(_REQUIRED_DIAGNOSTIC_KEYS),
        "demo_status": _demo_status(context, runtime_state_diff),
        "final_plan_or_range": final_fields.get("final_plan_or_range")
        or _template_variable_value(
            decision,
            template_id="diagnostic.deliver_plan_recommendation",
            variable_name="recommended_plan_or_range",
        ),
        "final_demo_line": final_fields.get("final_demo_line")
        or _diagnostic_demo_line(decision),
    }


def _waitlist_fields(
    *,
    context: TurnContext,
    runtime_state_diff: dict[str, Any],
    waitlist_status: str,
    delivery_events: list[DeliveryEvent],
) -> dict[str, Any]:
    waitlist_state = _mapping(_state_set(runtime_state_diff).get("waitlist"))
    fields: dict[str, Any] = {}
    if waitlist_state:
        fields["waitlist_eligibility"] = waitlist_state.get("eligibility")

    if waitlist_status == "pending_details":
        fields["missing_waitlist_fields"] = list(
            waitlist_state.get("missing_details") or []
        )
        return fields

    if waitlist_status != "joined":
        return fields

    joined_event = _first_event(delivery_events, "waitlist_joined")
    fields.update(
        {
            "waitlist_idempotency_key": (
                joined_event.idempotency_key
                if joined_event
                else context.sales_inbox_inputs.get("waitlist_idempotency_key")
            ),
            "waitlist_joined_at": (
                joined_event.metadata.get("joined_at")
                if joined_event
                else context.sales_inbox_inputs.get("waitlist_joined_at")
            ),
            "missing_waitlist_fields": [],
        }
    )
    return fields


def _demo_fields(runtime_state_diff: dict[str, Any]) -> dict[str, Any]:
    demo_state = _mapping(_state_set(runtime_state_diff).get("demo"))
    if not demo_state:
        return {}
    return {
        "demo_customer_facing_concept": demo_state.get(
            "customer_facing_concept",
        ),
        "demo_status": demo_state.get("status"),
        "demo_next_step": demo_state.get("next_step"),
    }


def _template_variable_value(
    decision: ConductorDecision,
    *,
    template_id: str,
    variable_name: str,
) -> Any:
    for item in decision.template_plan.items:
        if item.template_id.split("#", 1)[0] != template_id:
            continue
        variable = item.variables.get(variable_name)
        if variable is not None:
            return variable.value
    return None


def _diagnostic_demo_line(decision: ConductorDecision) -> str | None:
    template_ids = {
        item.template_id.split("#", 1)[0]
        for item in decision.template_plan.items
    }
    if "diagnostic.deliver_demo_not_offered" in template_ids:
        return (
            "Temos algumas demonstracoes que mostram o funcionamento na pratica. "
            "Quer que eu te mande?"
        )
    if "diagnostic.deliver_demo_already_offered" in template_ids:
        return "Chegou a olhar as demonstracoes? O que voce achou?"
    return None


def _handoff_fields(
    *,
    context: TurnContext,
    runtime_state_diff: dict[str, Any],
    handoff_status: str,
) -> dict[str, Any]:
    if handoff_status not in {"requested", "active"}:
        return {}

    handoff_state = _mapping(_state_set(runtime_state_diff).get("handoff"))
    return {
        "handoff_reason": handoff_state.get("reason") or context.handoff_state.get("reason"),
        "human_active": True,
        "ai_paused": True,
    }


def _identity_fields(
    context: TurnContext,
    runtime_state_diff: dict[str, Any],
) -> list[IdentityField]:
    candidates: dict[tuple[str, str], dict[str, Any]] = {}
    for fact in context.facts:
        _merge_identity_candidate(
            candidates,
            key=fact.key,
            value=fact.value,
            source=fact.source,
            reliability=fact.reliability,
        )

    append = _mapping(runtime_state_diff.get("append"))
    fact_updates = append.get("fact_updates")
    if isinstance(fact_updates, list):
        for fact in fact_updates:
            if not isinstance(fact, dict):
                continue
            _merge_identity_candidate(
                candidates,
                key=fact.get("key"),
                value=fact.get("value"),
                source=fact.get("source"),
                reliability=fact.get("reliability"),
            )

    return [
        IdentityField(
            key=str(candidate["key"]),
            value=str(candidate["value"]),
            source=str(candidate["identity_source"]),
            verified=bool(candidate["verified"]),
        )
        for candidate in sorted(
            candidates.values(),
            key=lambda item: (
                str(item["key"]),
                -int(item["rank"]),
                str(item["value"]),
            ),
        )
    ]


def _merge_identity_candidate(
    candidates: dict[tuple[str, str], dict[str, Any]],
    *,
    key: Any,
    value: Any,
    source: Any,
    reliability: Any,
) -> None:
    identity_key = str(key or "").strip()
    if identity_key not in IDENTITY_CONTACT_FACT_KEYS:
        return

    identity_value = str(value or "").strip()
    if not identity_value:
        return

    identity_source = _identity_source(source=source, reliability=reliability)
    if identity_source is None:
        return

    candidate_key = (identity_key, identity_value)
    rank = _identity_rank(identity_source)
    existing = candidates.get(candidate_key)
    if existing is not None and int(existing["rank"]) >= rank:
        return

    candidates[candidate_key] = {
        "key": identity_key,
        "value": identity_value,
        "identity_source": identity_source,
        "verified": identity_source in {"customer_provided", "operator_provided"},
        "rank": rank,
    }


def _identity_source(*, source: Any, reliability: Any) -> str | None:
    source_label = str(source or "").strip()
    reliability_label = str(reliability or "").strip()

    if source_label == "sales_inbox_projection":
        return "inferred" if reliability_label == "inferred" else "unverified"
    if source_label == "channel_metadata":
        return "channel_provided"
    if source_label == "operator":
        return "operator_provided"
    if reliability_label in _IDENTITY_SOURCES:
        return reliability_label
    return None


def _identity_rank(identity_source: str) -> int:
    return {
        "operator_provided": 4,
        "customer_provided": 3,
        "channel_provided": 2,
        "inferred": 1,
        "unverified": 0,
    }[identity_source]


def _diagnostic_status(context: TurnContext, runtime_state_diff: dict[str, Any]) -> str:
    diagnostic_state = _mapping(_state_set(runtime_state_diff).get("diagnostic"))
    status = diagnostic_state.get("status")
    context_status = _contextual_diagnostic_status(context)
    if status in _VALID_DIAGNOSTIC_STATUSES:
        if status == "not_started" and context_status in {
            "offered",
            "in_progress",
            "completed",
            "insufficient_evidence",
        }:
            return context_status
        if status == "offered" and context_status in {"in_progress", "completed"}:
            return context_status
        return str(status)

    if context_status is not None:
        return context_status
    return "not_started"


def _contextual_diagnostic_status(context: TurnContext) -> str | None:
    raw_status = context.sales_inbox_inputs.get("diagnostic_status")
    ledger_status = _diagnostic_status_from_context_ledger(context)
    if raw_status == "completed" or ledger_status == "completed":
        return "completed"
    if ledger_status == "in_progress" and raw_status in {
        None,
        "",
        "not_started",
        "offered",
    }:
        return "in_progress"
    if raw_status in _VALID_DIAGNOSTIC_STATUSES:
        return str(raw_status)
    return None


def _diagnostic_status_from_context_ledger(context: TurnContext) -> str | None:
    statuses: dict[str, str] = {}
    for item in context.diagnostic_ledger:
        if not isinstance(item, dict):
            continue
        question_key = str(item.get("question_key") or "")
        status = str(item.get("status") or "")
        if question_key in _REQUIRED_DIAGNOSTIC_KEYS and status:
            statuses[question_key] = status
    if not statuses:
        return None
    if all(
        statuses.get(question_key) in _COMPLETE_DIAGNOSTIC_STATUSES
        for question_key in _REQUIRED_DIAGNOSTIC_KEYS
    ):
        return "completed"
    return "in_progress"


def _waitlist_status(context: TurnContext, runtime_state_diff: dict[str, Any]) -> str:
    waitlist_state = _mapping(_state_set(runtime_state_diff).get("waitlist"))
    status = waitlist_state.get("status")
    if status in _VALID_WAITLIST_STATUSES:
        return str(status)

    context_status = context.sales_inbox_inputs.get("waitlist_status")
    if context_status in _VALID_WAITLIST_STATUSES:
        return str(context_status)
    return "none"


def _handoff_status(context: TurnContext, runtime_state_diff: dict[str, Any]) -> str:
    handoff_state = _mapping(_state_set(runtime_state_diff).get("handoff"))
    status = handoff_state.get("status")
    if status in _VALID_HANDOFF_STATUSES:
        return str(status)

    context_status = (
        context.sales_inbox_inputs.get("handoff_status")
        or context.sales_inbox_inputs.get("human_status")
        or context.handoff_state.get("status")
    )
    if context_status in _VALID_HANDOFF_STATUSES:
        return str(context_status)
    return "none"


def _demo_status(context: TurnContext, runtime_state_diff: dict[str, Any]) -> str:
    demo_state = _mapping(_state_set(runtime_state_diff).get("demo"))
    status = demo_state.get("status")
    if isinstance(status, str) and status:
        return status

    context_status = context.sales_inbox_inputs.get("demo_status")
    if isinstance(context_status, str) and context_status:
        return context_status
    return "not_offered"


def _operator_next_action(
    context: TurnContext,
    runtime_state_diff: dict[str, Any],
) -> str:
    handoff_status = _handoff_status(context, runtime_state_diff)
    if handoff_status in {"requested", "active"}:
        return "human_follow_up"

    waitlist_status = _waitlist_status(context, runtime_state_diff)
    if waitlist_status == "pending_details":
        return "collect_waitlist_missing_details"
    if waitlist_status == "joined":
        return "monitor_waitlist"

    if _diagnostic_status(context, runtime_state_diff) == "completed":
        return "review_completed_diagnostic"
    return "none"


def _source_labels(
    context: TurnContext,
    runtime_state_diff: dict[str, Any],
) -> dict[str, Any]:
    labels = {
        "channel": context.channel,
        "source": context.sales_inbox_inputs.get("source"),
        "entry_intent": context.sales_inbox_inputs.get("entry_intent"),
        "channel_conversation_id": context.sales_inbox_inputs.get(
            "channel_conversation_id"
        ),
        "state_source": runtime_state_diff.get("source"),
    }
    return {
        key: value
        for key, value in labels.items()
        if value is not None and value != ""
    }


def _commercial_stage(runtime_state_diff: dict[str, Any]) -> str:
    state = _state_set(runtime_state_diff)
    current_state = state.get("current_state")
    if isinstance(current_state, str) and current_state.strip():
        return current_state

    transition = _mapping(runtime_state_diff.get("state_transition"))
    next_state = transition.get("next_state")
    if isinstance(next_state, str) and next_state.strip():
        return next_state

    raise SalesInboxProjectionBuildError("runtime_state_diff current_state missing")


def _summary(context: TurnContext, runtime_state_diff: dict[str, Any]) -> str:
    for item in context.compact_memory:
        if not isinstance(item, dict) or item.get("kind") != "summary":
            continue
        value = item.get("value")
        if isinstance(value, str) and value.strip():
            return value
    return f"Estado comercial: {_commercial_stage(runtime_state_diff)}"


def _selected_template_ids(runtime_state_diff: dict[str, Any]) -> list[str]:
    value = _state_set(runtime_state_diff).get("last_selected_template_ids")
    if isinstance(value, list):
        return [
            str(item).split("#", 1)[0]
            for item in value
            if str(item).strip()
        ]
    return []


def _diagnostic_ledger_by_key(
    context: TurnContext,
    runtime_state_diff: dict[str, Any],
) -> dict[str, str]:
    ledger_by_key: dict[str, str] = {}
    for item in [*context.diagnostic_ledger, *_appended_diagnostic_ledger(runtime_state_diff)]:
        if not isinstance(item, dict):
            continue
        question_key = str(item.get("question_key") or "")
        status = str(item.get("status") or "")
        if question_key and status:
            ledger_by_key[question_key] = status
    return ledger_by_key


def _appended_diagnostic_ledger(runtime_state_diff: dict[str, Any]) -> list[Any]:
    append = _mapping(runtime_state_diff.get("append"))
    value = append.get("diagnostic_ledger")
    return value if isinstance(value, list) else []


def _first_event(
    delivery_events: list[DeliveryEvent],
    event_name: str,
) -> DeliveryEvent | None:
    for event in delivery_events:
        if event.event == event_name:
            return event
    return None


def _raise_if_invalid_projection(
    projection: SalesInboxProjection,
    decision: ConductorDecision,
    context: TurnContext,
) -> None:
    result = validate_sales_inbox_projection(projection, decision, context)
    if result.status == "passed":
        return
    codes = ", ".join(issue.code for issue in result.errors)
    details = json.dumps(
        [issue.model_dump(mode="json") for issue in result.errors[:8]],
        ensure_ascii=True,
        separators=(",", ":"),
    )
    raise SalesInboxProjectionBuildError(
        f"Sales Inbox projection failed validation: {codes}:{details}"
    )


def _state_set(runtime_state_diff: dict[str, Any]) -> dict[str, Any]:
    return _mapping(runtime_state_diff.get("set"))


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _require_equal(field_name: str, left: Any, right: Any) -> None:
    if left != right:
        raise SalesInboxProjectionBuildError(f"{field_name} mismatch")
