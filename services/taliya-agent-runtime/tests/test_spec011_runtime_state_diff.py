from __future__ import annotations

from typing import Any

import pytest

from app.core.taliya_commercial.runtime_state import (
    RuntimeStatePersistenceError,
    build_runtime_state_diff,
    merge_diagnostic_ledger,
)
from app.core.taliya_commercial.schemas import (
    ConductorDecision,
    ModelUsage,
    RepairResult,
    ValidatorResult,
)


def _decision(**overrides: Any) -> ConductorDecision:
    payload: dict[str, Any] = {
        "schema_version": "011.0",
        "turn_id": "turn_state_1",
        "conversation_id": "conv_state_1",
        "channel": "whatsapp",
        "agent_key": "taliya_commercial",
        "role": "diagnostic",
        "route": "diagnostic",
        "previous_state": "diagnostic_intro",
        "current_state": "diagnostic_collecting",
        "next_state": "diagnostic_collecting_main_pain",
        "detected_intents": ["diagnostic_answer"],
        "facts": [
            {
                "key": "active_students",
                "value": 120,
                "source": "user_message",
                "reliability": "customer_provided",
                "evidence": ["turn_state_1.inbound"],
                "confidence": "high",
            }
        ],
        "diagnostic": {
            "action": "ask_next",
            "next_question_key": "main_pain",
            "ledger_updates": [
                {
                    "question_key": "active_students_or_size",
                    "status": "answered",
                    "answer_value": "120 alunos ativos",
                    "evidence": ["turn_state_1.inbound"],
                    "confidence": "high",
                }
            ],
        },
        "demo": {
            "customer_facing_concept": "commercial_product_demo",
            "status": "offered",
            "next_step": "ask_demo_reaction",
        },
        "waitlist": {
            "eligibility": "unknown",
            "status": "none",
            "missing_details": [],
        },
        "handoff": {
            "status": "none",
        },
        "language_policy": {
            "register": "studio_owner_practical",
            "crm_term_policy": "avoid_by_default",
        },
        "template_plan": {
            "items": [
                {
                    "template_id": "diagnostic.ask_main_pain",
                }
            ]
        },
        "policy_checks": {
            "direct_question_answered_first": True,
            "diagnostic_timing_ok": True,
            "waitlist_timing_ok": True,
            "official_facts_only": True,
            "no_internal_text_leak": True,
            "no_early_contact_capture": True,
            "no_human_overlap": True,
        },
        "confidence": "high",
    }
    payload.update(overrides)
    return ConductorDecision.model_validate(payload)


def _accepted(decision: ConductorDecision) -> ValidatorResult:
    return ValidatorResult(
        decision_id=decision.decision_id,
        status="passed",
        final_disposition="accepted",
    )


def _repaired(decision: ConductorDecision) -> ValidatorResult:
    return ValidatorResult(
        decision_id=decision.decision_id,
        status="passed",
        repair_attempt_count=1,
        final_disposition="repaired",
    )


def test_runtime_state_diff_is_derived_from_accepted_decision_only() -> None:
    decision = _decision()

    diff = build_runtime_state_diff(decision, _accepted(decision))

    assert diff["schema_version"] == "011.runtime_state_diff.v1"
    assert diff["source"] == "accepted_decision"
    assert diff["decision_id"] == decision.decision_id
    assert diff["state_transition"] == {
        "previous_state": "diagnostic_intro",
        "decision_current_state": "diagnostic_collecting",
        "next_state": "diagnostic_collecting_main_pain",
    }
    assert diff["set"]["current_state"] == "diagnostic_collecting_main_pain"
    assert diff["set"]["diagnostic"]["status"] == "in_progress"
    assert diff["set"]["demo"]["status"] == "offered"
    assert "waitlist" not in diff["set"]
    assert "handoff" not in diff["set"]
    assert diff["set"]["last_selected_template_ids"] == ["diagnostic.ask_main_pain"]
    assert diff["append"]["diagnostic_ledger"][0]["question_key"] == (
        "active_students_or_size"
    )
    assert diff["append"]["fact_updates"][0]["value"] == 120
    assert _missing_everywhere(
        diff,
        {
            "inbound_text",
            "message_text",
            "rendered_messages",
            "sales_inbox_projection",
        },
    )


def test_runtime_state_diff_ignores_stray_next_question_when_action_is_none() -> None:
    decision = _decision(
        role="product",
        route="product",
        diagnostic={"action": "none", "next_question_key": "urgency"},
        demo={
            "customer_facing_concept": "commercial_product_demo",
            "status": "not_offered",
            "next_step": "none",
        },
        template_plan={"items": [{"template_id": "product.overview_short"}]},
    )

    diff = build_runtime_state_diff(decision, _accepted(decision))

    assert "diagnostic" not in diff["set"]


def test_runtime_state_diff_allows_repaired_decision_only_with_matching_repair() -> None:
    repaired_decision = _decision(next_state="diagnostic_collecting_priority")
    repair_result = RepairResult(
        attempted=True,
        attempt_count=1,
        status="repaired",
        repaired_decision=repaired_decision,
        model_usage=ModelUsage(
            model="gpt-5.4-mini",
            input_tokens=100,
            output_tokens=40,
            cost_usd=0.001,
        ),
    )

    diff = build_runtime_state_diff(
        repaired_decision,
        _repaired(repaired_decision),
        repair_result=repair_result,
    )

    assert diff["source"] == "repaired_decision"
    assert diff["set"]["current_state"] == "diagnostic_collecting_priority"

    with pytest.raises(RuntimeStatePersistenceError, match="repair_result"):
        build_runtime_state_diff(
            repaired_decision,
            _repaired(repaired_decision),
        )

    mismatched_repair = repair_result.model_copy(
        update={"repaired_decision": _decision(next_state="other_state")}
    )
    with pytest.raises(RuntimeStatePersistenceError, match="repaired decision"):
        build_runtime_state_diff(
            repaired_decision,
            _repaired(repaired_decision),
            repair_result=mismatched_repair,
        )


@pytest.mark.parametrize(
    ("status", "final_disposition"),
    [
        ("repairable", None),
        ("blocked", "blocked"),
        ("failed", None),
        ("passed", "fallback"),
    ],
)
def test_runtime_state_diff_rejects_unaccepted_validator_paths(
    status: str,
    final_disposition: str | None,
) -> None:
    decision = _decision()
    validator_result = ValidatorResult(
        decision_id=decision.decision_id,
        status=status,  # type: ignore[arg-type]
        final_disposition=final_disposition,  # type: ignore[arg-type]
    )

    with pytest.raises(RuntimeStatePersistenceError, match="validated decision"):
        build_runtime_state_diff(decision, validator_result)


def test_runtime_state_diff_rejects_decision_validator_mismatch() -> None:
    decision = _decision()
    validator_result = ValidatorResult(
        decision_id="decision_other",
        status="passed",
        final_disposition="accepted",
    )

    with pytest.raises(RuntimeStatePersistenceError, match="decision_id"):
        build_runtime_state_diff(decision, validator_result)


def test_runtime_state_diff_rejects_failed_path_payloads_as_state_source() -> None:
    validator_result = ValidatorResult(
        decision_id="failed_path",
        status="passed",
        final_disposition="accepted",
    )

    with pytest.raises(RuntimeStatePersistenceError, match="ConductorDecision"):
        build_runtime_state_diff(  # type: ignore[arg-type]
            {
                "status": "safe_fallback",
                "template_id": "fallback.provider_timeout",
            },
            validator_result,
        )


def test_runtime_state_diff_does_not_reset_existing_state_with_neutral_values() -> None:
    decision = _decision(
        role="product",
        route="product",
        previous_state="diagnostic_completed",
        current_state="product_followup",
        next_state="product_followup",
        diagnostic={"action": "none"},
        demo={
            "customer_facing_concept": "commercial_product_demo",
            "status": "not_offered",
            "next_step": "none",
        },
        waitlist={
            "eligibility": "unknown",
            "status": "none",
            "missing_details": [],
        },
        handoff={"status": "none"},
        template_plan={"items": [{"template_id": "product.overview_short"}]},
    )

    diff = build_runtime_state_diff(decision, _accepted(decision))

    assert "diagnostic" not in diff["set"]
    assert "demo" not in diff["set"]
    assert "waitlist" not in diff["set"]
    assert "handoff" not in diff["set"]
    assert diff["append"]["diagnostic_ledger"] == []


def test_runtime_state_diff_persists_final_fields_derived_from_diagnostic_templates() -> None:
    decision = _decision(
        role="diagnostic",
        route="diagnostic",
        previous_state="diagnostic_collecting",
        current_state="diagnostic_ready",
        next_state="diagnostic_delivered",
        diagnostic={"action": "complete"},
        template_plan={
            "items": [
                {"template_id": "diagnostic.deliver_hold"},
                {
                    "template_id": "diagnostic.deliver_plan_recommendation",
                    "variables": {
                        "recommended_plan_or_range": {
                            "kind": "short_text",
                            "value": "Avance ou Completo",
                            "source": "official_product_knowledge",
                            "evidence": ["product_knowledge.plans"],
                            "max_length": 90,
                        }
                    },
                },
                {"template_id": "diagnostic.deliver_demo_not_offered"},
            ]
        },
    )

    diff = build_runtime_state_diff(decision, _accepted(decision))

    final_fields = diff["set"]["diagnostic"]["final_fields"]
    assert final_fields["final_plan_or_range"] == "Avance ou Completo"
    assert final_fields["final_demo_line"] == (
        "Temos algumas demonstracoes que mostram o funcionamento na pratica. "
        "Quer que eu te mande?"
    )


def test_runtime_state_diff_includes_only_active_commercial_state_updates() -> None:
    decision = _decision(
        waitlist={
            "eligibility": "eligible",
            "status": "pending_details",
            "missing_details": ["studio_name"],
        },
        handoff={"status": "requested", "reason": "lead_requested_human"},
    )

    diff = build_runtime_state_diff(decision, _accepted(decision))

    assert diff["set"]["diagnostic"]["status"] == "in_progress"
    assert diff["set"]["demo"]["status"] == "offered"
    assert diff["set"]["waitlist"]["status"] == "pending_details"
    assert diff["set"]["handoff"]["status"] == "requested"


def test_merge_diagnostic_ledger_keeps_current_state_instead_of_raw_history() -> None:
    existing = [
        {
            "question_key": "active_students_or_size",
            "status": "answered",
            "answer_value": "95 alunos",
            "evidence": ["95 alunos"],
        },
        {
            "question_key": "current_process",
            "status": "missing",
            "evidence": [],
        },
        {
            "question_key": "priority",
            "status": "missing",
            "evidence": [],
        },
        {
            "question_key": "urgency",
            "status": "missing",
            "evidence": [],
        },
    ]
    updates = [
        {
            "question_key": "current_process",
            "status": "answered",
            "answer_value": "planilha e whatsapp",
            "evidence": ["planilha e whatsapp"],
        },
        {
            "question_key": "priority",
            "status": "answered",
            "answer_value": "vendas primeiro",
            "evidence": ["vendas primeiro"],
        },
        {
            "question_key": "urgency",
            "status": "answered",
            "answer_value": "resolver agora",
            "evidence": ["resolver agora"],
        },
        {
            "question_key": "urgency",
            "status": "missing",
            "evidence": [],
        },
    ]

    ledger = merge_diagnostic_ledger(existing, updates)

    assert [item["question_key"] for item in ledger] == [
        "active_students_or_size",
        "current_process",
        "priority",
        "urgency",
    ]
    assert {item["question_key"]: item["status"] for item in ledger} == {
        "active_students_or_size": "answered",
        "current_process": "answered",
        "priority": "answered",
        "urgency": "answered",
    }
    assert ledger[-1]["answer_value"] == "resolver agora"


def _missing_everywhere(payload: Any, forbidden_keys: set[str]) -> bool:
    if isinstance(payload, dict):
        return all(
            key not in forbidden_keys and _missing_everywhere(value, forbidden_keys)
            for key, value in payload.items()
        )
    if isinstance(payload, list | tuple):
        return all(_missing_everywhere(item, forbidden_keys) for item in payload)
    return True
