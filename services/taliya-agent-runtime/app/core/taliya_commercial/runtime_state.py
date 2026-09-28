from __future__ import annotations

from typing import Any

from app.core.taliya_commercial.schemas import (
    ConductorDecision,
    DiagnosticDecision,
    RepairResult,
    ValidatorResult,
)

_ACCEPTED_DISPOSITIONS = {"accepted", "repaired"}
_FINAL_DIAGNOSTIC_PLAN_TEMPLATE_ID = "diagnostic.deliver_plan_recommendation"
_FINAL_DIAGNOSTIC_DEMO_LINES = {
    "diagnostic.deliver_demo_not_offered": (
        "Temos algumas demonstracoes que mostram o funcionamento na pratica. "
        "Quer que eu te mande?"
    ),
    "diagnostic.deliver_demo_already_offered": (
        "Chegou a olhar as demonstracoes? O que voce achou?"
    ),
}
_REQUIRED_DIAGNOSTIC_KEYS = (
    "active_students_or_size",
    "main_pain",
    "pain_detail",
    "current_process",
    "priority",
    "urgency",
)
_DIAGNOSTIC_STATUS_RANK = {
    "missing": 0,
    "ambiguous": 1,
    "refused": 2,
    "answered": 3,
    "inferred_from_prior_message": 3,
    "not_applicable": 3,
}


class RuntimeStatePersistenceError(ValueError):
    pass


def build_runtime_state_diff(
    decision: ConductorDecision,
    validator_result: ValidatorResult,
    *,
    repair_result: RepairResult | None = None,
) -> dict[str, Any]:
    """Build an isolated runtime-state diff from a validated conductor decision."""
    _require_decision(decision)
    _require_validator_result(validator_result)
    _require_validator_matches_decision(decision, validator_result)
    source = _validated_source(
        decision=decision,
        validator_result=validator_result,
        repair_result=repair_result,
    )

    selected_template_ids = [
        item.template_id for item in decision.template_plan.items
    ]

    set_values: dict[str, Any] = {
        "current_state": decision.next_state,
        "last_decision_id": decision.decision_id,
        "last_turn_id": decision.turn_id,
        "last_route": decision.route,
        "last_role": decision.role,
        "last_confidence": decision.confidence,
        "last_selected_template_ids": selected_template_ids,
    }
    if _has_diagnostic_update(decision.diagnostic):
        set_values["diagnostic"] = _diagnostic_state(decision)
    if _has_demo_update(decision):
        set_values["demo"] = decision.demo.model_dump(mode="json")
    if _has_waitlist_update(decision):
        set_values["waitlist"] = decision.waitlist.model_dump(mode="json")
    if _has_handoff_update(decision):
        set_values["handoff"] = decision.handoff.model_dump(
            mode="json",
            exclude_none=True,
        )

    return {
        "schema_version": "011.runtime_state_diff.v1",
        "source": source,
        "decision_id": decision.decision_id,
        "turn_id": decision.turn_id,
        "conversation_id": decision.conversation_id,
        "agent_key": decision.agent_key,
        "channel": decision.channel,
        "state_transition": {
            "previous_state": decision.previous_state,
            "decision_current_state": decision.current_state,
            "next_state": decision.next_state,
        },
        "set": set_values,
        "append": {
            "diagnostic_ledger": [
                item.model_dump(mode="json", exclude_none=True)
                for item in decision.diagnostic.ledger_updates
            ],
            "fact_updates": [
                fact.model_dump(mode="json", exclude_none=True)
                for fact in decision.facts
            ],
        },
        "validation": {
            "status": validator_result.status,
            "final_disposition": validator_result.final_disposition,
            "repair_attempt_count": validator_result.repair_attempt_count,
        },
    }


def merge_diagnostic_ledger(
    existing: list[Any] | None,
    updates: list[Any] | None,
) -> list[dict[str, Any]]:
    """Keep the diagnostic ledger as current state, not as an append-only log."""
    by_key: dict[str, dict[str, Any]] = {}
    unknown_items: list[dict[str, Any]] = []

    for raw_item in [*(existing or []), *(updates or [])]:
        if not isinstance(raw_item, dict):
            continue
        item = dict(raw_item)
        question_key = str(item.get("question_key") or "").strip()
        if not question_key:
            unknown_items.append(item)
            continue

        previous = by_key.get(question_key)
        if previous is None or _diagnostic_ledger_item_should_replace(previous, item):
            by_key[question_key] = item

    ordered = [
        by_key[question_key]
        for question_key in _REQUIRED_DIAGNOSTIC_KEYS
        if question_key in by_key
    ]
    ordered.extend(
        item
        for question_key, item in by_key.items()
        if question_key not in _REQUIRED_DIAGNOSTIC_KEYS
    )
    ordered.extend(unknown_items)
    return ordered


def canonical_diagnostic_ledger(ledger: list[Any] | None) -> list[dict[str, Any]]:
    return merge_diagnostic_ledger([], ledger)


def _diagnostic_ledger_item_should_replace(
    previous: dict[str, Any],
    candidate: dict[str, Any],
) -> bool:
    previous_rank = _DIAGNOSTIC_STATUS_RANK.get(str(previous.get("status") or ""), -1)
    candidate_rank = _DIAGNOSTIC_STATUS_RANK.get(str(candidate.get("status") or ""), -1)
    return candidate_rank >= previous_rank


def _require_decision(decision: ConductorDecision) -> None:
    if not isinstance(decision, ConductorDecision):
        raise RuntimeStatePersistenceError(
            "runtime state diff requires a ConductorDecision source"
        )


def _require_validator_result(validator_result: ValidatorResult) -> None:
    if not isinstance(validator_result, ValidatorResult):
        raise RuntimeStatePersistenceError(
            "runtime state diff requires a ValidatorResult"
        )


def _require_validator_matches_decision(
    decision: ConductorDecision,
    validator_result: ValidatorResult,
) -> None:
    if validator_result.decision_id != decision.decision_id:
        raise RuntimeStatePersistenceError(
            "validator_result decision_id does not match decision_id"
        )


def _validated_source(
    *,
    decision: ConductorDecision,
    validator_result: ValidatorResult,
    repair_result: RepairResult | None,
) -> str:
    if (
        validator_result.status != "passed"
        or validator_result.final_disposition not in _ACCEPTED_DISPOSITIONS
    ):
        raise RuntimeStatePersistenceError(
            "runtime state diff requires a validated decision"
        )

    if validator_result.final_disposition == "accepted":
        return "accepted_decision"

    if repair_result is None:
        raise RuntimeStatePersistenceError(
            "repaired runtime state diff requires repair_result"
        )
    if repair_result.status != "repaired" or repair_result.repaired_decision is None:
        raise RuntimeStatePersistenceError(
            "repaired runtime state diff requires a repaired decision"
        )
    if repair_result.repaired_decision.decision_id != decision.decision_id:
        raise RuntimeStatePersistenceError(
            "repair_result repaired decision does not match decision"
        )
    return "repaired_decision"


def _diagnostic_state(decision: ConductorDecision) -> dict[str, Any]:
    diagnostic = decision.diagnostic
    state = diagnostic.model_dump(
        mode="json",
        exclude={"ledger_updates"},
        exclude_none=True,
    )
    if diagnostic.action == "complete":
        state["final_fields"] = _completed_diagnostic_final_fields(decision)
    state["status"] = _diagnostic_status(diagnostic.action)
    return state


def _completed_diagnostic_final_fields(
    decision: ConductorDecision,
) -> dict[str, Any]:
    final_fields = dict(decision.diagnostic.final_fields)
    final_fields.setdefault(
        "final_plan_or_range",
        _template_variable_value(
            decision,
            template_id=_FINAL_DIAGNOSTIC_PLAN_TEMPLATE_ID,
            variable_name="recommended_plan_or_range",
        ),
    )
    final_fields.setdefault("final_demo_line", _diagnostic_demo_line(decision))
    return {
        key: value
        for key, value in final_fields.items()
        if value is not None and value != ""
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
    for template_id, demo_line in _FINAL_DIAGNOSTIC_DEMO_LINES.items():
        if template_id in template_ids:
            return demo_line
    return None


def _has_diagnostic_update(diagnostic: DiagnosticDecision) -> bool:
    return (
        diagnostic.action != "none"
        or bool(diagnostic.ledger_updates)
        or bool(diagnostic.final_fields)
    )


def _has_demo_update(decision: ConductorDecision) -> bool:
    return decision.demo.status != "not_offered" or decision.demo.next_step != "none"


def _has_waitlist_update(decision: ConductorDecision) -> bool:
    return (
        decision.waitlist.status != "none"
        or decision.waitlist.eligibility != "unknown"
        or bool(decision.waitlist.missing_details)
    )


def _has_handoff_update(decision: ConductorDecision) -> bool:
    return decision.handoff.status != "none" or decision.handoff.reason is not None


def _diagnostic_status(action: str) -> str:
    if action == "offer":
        return "offered"
    if action in {"start", "ask_next"}:
        return "in_progress"
    if action == "complete":
        return "completed"
    if action == "insufficient_evidence":
        return "insufficient_evidence"
    return "not_started"
