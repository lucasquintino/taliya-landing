from __future__ import annotations

from typing import Any

import pytest

from app.core.taliya_commercial.runtime_state import build_runtime_state_diff
from app.core.taliya_commercial.sales_inbox_projection import (
    SalesInboxProjectionBuildError,
    build_sales_inbox_projection,
)
from app.core.taliya_commercial.schemas import (
    ConductorDecision,
    DeliveryEvent,
    TurnContext,
    ValidatorResult,
)
from app.core.taliya_commercial.validators import validate_sales_inbox_projection

_REQUIRED_DIAGNOSTIC_KEYS = (
    "active_students_or_size",
    "main_pain",
    "pain_detail",
    "current_process",
    "priority",
    "urgency",
)


def _context(
    *,
    diagnostic_ledger: list[dict[str, Any]] | None = None,
    sales_inbox_inputs: dict[str, Any] | None = None,
    facts: list[dict[str, Any]] | None = None,
    compact_memory: list[dict[str, Any]] | None = None,
) -> TurnContext:
    inputs = {
        "lead_id": "lead_projection_1",
        "source": "pilates_landing",
        "entry_intent": "site_widget",
        "channel_conversation_id": "wa_projection_1",
        "diagnostic_status": "not_started",
        "waitlist_status": "none",
        "handoff_status": "none",
        "demo_status": "not_offered",
    }
    inputs.update(sales_inbox_inputs or {})
    return TurnContext.model_validate(
        {
            "turn_id": "turn_projection_1",
            "conversation_id": "conv_projection_1",
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "inbound": {
                "message_id": "msg_projection_1",
                "idempotency_key": "wa:conv_projection_1:1",
                "text": "quanto custa?",
            },
            "facts": facts or [],
            "compact_memory": compact_memory
            or [{"kind": "summary", "value": "Lead em fluxo comercial."}],
            "diagnostic_ledger": diagnostic_ledger or [],
            "sales_inbox_inputs": inputs,
        }
    )


def _decision(context: TurnContext, **overrides: Any) -> ConductorDecision:
    payload: dict[str, Any] = {
        "schema_version": "011.0",
        "turn_id": context.turn_id,
        "conversation_id": context.conversation_id,
        "channel": context.channel,
        "agent_key": context.agent_key,
        "role": "product",
        "route": "product",
        "previous_state": "new_lead",
        "current_state": "product_question",
        "next_state": "product_answered",
        "detected_intents": ["price_question"],
        "direct_question_present": True,
        "direct_question_answered_first": True,
        "diagnostic": {"action": "none"},
        "demo": {
            "customer_facing_concept": "commercial_product_demo",
            "status": "not_offered",
            "next_step": "none",
        },
        "waitlist": {
            "eligibility": "unknown",
            "status": "none",
            "missing_details": [],
        },
        "handoff": {"status": "none"},
        "language_policy": {
            "register": "studio_owner_practical",
            "crm_term_policy": "avoid_by_default",
        },
        "template_plan": {
            "items": [
                {
                    "template_id": "product.price_direct",
                    "variables": {},
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


def _validator(decision: ConductorDecision) -> ValidatorResult:
    return ValidatorResult(
        decision_id=decision.decision_id,
        status="passed",
        final_disposition="accepted",
    )


def _state_diff(decision: ConductorDecision) -> dict[str, Any]:
    return build_runtime_state_diff(decision, _validator(decision))


def _complete_ledger() -> list[dict[str, Any]]:
    return [
        {
            "question_key": question_key,
            "status": "answered",
            "answer_value": f"answer:{question_key}",
            "evidence": [f"evidence:{question_key}"],
            "confidence": "high",
        }
        for question_key in _REQUIRED_DIAGNOSTIC_KEYS
    ]


def test_projection_is_built_from_runtime_state_context_and_events() -> None:
    context = _context()
    decision = _decision(context)
    validator_result = _validator(decision)

    projection = build_sales_inbox_projection(
        context=context,
        decision=decision,
        validator_result=validator_result,
        runtime_state_diff=build_runtime_state_diff(decision, validator_result),
        delivery_events=[
            DeliveryEvent(
                event="reserved",
                idempotency_key="outbox:turn_projection_1:1",
                status="planned",
            )
        ],
    )

    result = validate_sales_inbox_projection(projection, decision, context)
    assert result.status == "passed"
    assert projection.conversation_id == "conv_projection_1"
    assert projection.lead_id == "lead_projection_1"
    assert projection.commercial_stage == "product_answered"
    assert projection.summary == "Lead em fluxo comercial."
    assert "quanto custa?" not in projection.summary
    assert projection.fields["template_ids"] == ["product.price_direct"]
    assert projection.fields["validator_status"] == "passed"
    assert projection.fields["validator_final_disposition"] == "accepted"
    assert projection.fields["source_labels"]["state_source"] == "accepted_decision"
    assert projection.fields["operator_next_action"] == "none"


def test_projection_completed_diagnostic_includes_required_fields() -> None:
    context = _context(diagnostic_ledger=_complete_ledger())
    decision = _decision(
        context,
        role="diagnostic",
        route="diagnostic",
        previous_state="diagnostic_collecting",
        current_state="diagnostic_ready",
        next_state="diagnostic_delivered",
        diagnostic={
            "action": "complete",
            "final_fields": {
                "final_plan_or_range": "Essencial ou Avance",
                "final_demo_line": "quer ver a demonstracao?",
            },
        },
        template_plan={"items": [{"template_id": "diagnostic.deliver_hold"}]},
    )

    projection = build_sales_inbox_projection(
        context=context,
        decision=decision,
        validator_result=_validator(decision),
        runtime_state_diff=_state_diff(decision),
        delivery_events=[DeliveryEvent(event="reserved")],
    )

    result = validate_sales_inbox_projection(projection, decision, context)
    assert result.status == "passed"
    assert projection.diagnostic_status == "completed"
    assert projection.fields["diagnostic_ledger_complete"] is True
    assert set(projection.fields["required_diagnostic_keys"]) == set(
        _REQUIRED_DIAGNOSTIC_KEYS
    )
    assert projection.fields["demo_status"] == "not_offered"
    assert projection.fields["final_plan_or_range"] == "Essencial ou Avance"
    assert projection.fields["final_demo_line"] == "quer ver a demonstracao?"


def test_projection_completed_diagnostic_derives_final_fields_from_template_plan() -> None:
    context = _context(diagnostic_ledger=_complete_ledger())
    decision = _decision(
        context,
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
                {
                    "template_id": "diagnostic.deliver_demo_not_offered",
                    "variables": {
                        "demo_status": {
                            "kind": "enum",
                            "value": "not_offered",
                            "source": "runtime_state",
                            "evidence": ["runtime_state.demo.status"],
                        }
                    },
                },
            ]
        },
    )

    projection = build_sales_inbox_projection(
        context=context,
        decision=decision,
        validator_result=_validator(decision),
        runtime_state_diff=_state_diff(decision),
        delivery_events=[DeliveryEvent(event="reserved")],
    )

    result = validate_sales_inbox_projection(projection, decision, context)
    assert result.status == "passed"
    assert projection.fields["final_plan_or_range"] == "Avance ou Completo"
    assert projection.fields["final_demo_line"] == (
        "Temos algumas demonstracoes que mostram o funcionamento na pratica. "
        "Quer que eu te mande?"
    )


def test_projection_reuses_prior_completed_diagnostic_final_fields_from_context() -> None:
    context = _context(
        diagnostic_ledger=_complete_ledger(),
        sales_inbox_inputs={
            "diagnostic_status": "completed",
            "diagnostic_final_fields": {
                "final_plan_or_range": "Avance ou Completo",
                "final_demo_line": "Quer que eu te mande a demonstracao?",
            },
        },
    )
    decision = _decision(
        context,
        role="product",
        route="product",
        previous_state="diagnostic_delivered",
        current_state="product_followup",
        next_state="product_followup_answered",
        diagnostic={"action": "none"},
        template_plan={"items": [{"template_id": "product.demo_followup"}]},
    )

    projection = build_sales_inbox_projection(
        context=context,
        decision=decision,
        validator_result=_validator(decision),
        runtime_state_diff=_state_diff(decision),
        delivery_events=[DeliveryEvent(event="reserved")],
    )

    result = validate_sales_inbox_projection(projection, decision, context)
    assert result.status == "passed"
    assert projection.diagnostic_status == "completed"
    assert projection.fields["final_plan_or_range"] == "Avance ou Completo"
    assert projection.fields["final_demo_line"] == "Quer que eu te mande a demonstracao?"


def test_projection_derives_completed_diagnostic_when_status_is_stale() -> None:
    context = _context(
        diagnostic_ledger=_complete_ledger(),
        sales_inbox_inputs={
            "diagnostic_status": "offered",
            "diagnostic_final_fields": {
                "final_plan_or_range": "Essencial",
                "final_demo_line": "Quer que eu te mande a demonstracao?",
            },
            "waitlist_status": "offered",
        },
    )
    decision = _decision(
        context,
        role="handoff",
        route="handoff",
        previous_state="diagnostic_completed_waitlist_offered",
        current_state="human_requested",
        next_state="handoff_active",
        diagnostic={"action": "none"},
        handoff={"status": "requested", "reason": "lead_requested_human"},
        template_plan={"items": [{"template_id": "handoff.acknowledge"}]},
    )

    projection = build_sales_inbox_projection(
        context=context,
        decision=decision,
        validator_result=_validator(decision),
        runtime_state_diff=_state_diff(decision),
        delivery_events=[DeliveryEvent(event="handoff_requested")],
    )

    result = validate_sales_inbox_projection(projection, decision, context)
    assert result.status == "passed"
    assert projection.diagnostic_status == "completed"
    assert projection.handoff_status == "requested"
    assert projection.fields["diagnostic_ledger_complete"] is True
    assert projection.fields["final_plan_or_range"] == "Essencial"
    assert projection.fields["operator_next_action"] == "human_follow_up"


def test_projection_waitlist_joined_and_handoff_fields_come_from_state_events() -> None:
    context = _context()
    waitlist_decision = _decision(
        context,
        role="waitlist",
        route="waitlist",
        current_state="waitlist_pending_data",
        next_state="waitlist_joined",
        waitlist={
            "eligibility": "eligible",
            "status": "joined",
            "missing_details": [],
        },
        template_plan={"items": [{"template_id": "waitlist.joined"}]},
    )
    waitlist_projection = build_sales_inbox_projection(
        context=context,
        decision=waitlist_decision,
        validator_result=_validator(waitlist_decision),
        runtime_state_diff=_state_diff(waitlist_decision),
        delivery_events=[
            DeliveryEvent(
                event="waitlist_joined",
                idempotency_key="waitlist:conv_projection_1:1",
                status="recorded",
                metadata={"joined_at": "2026-05-30T12:00:00Z"},
            )
        ],
    )

    waitlist_result = validate_sales_inbox_projection(
        waitlist_projection,
        waitlist_decision,
        context,
    )
    assert waitlist_result.status == "passed"
    assert waitlist_projection.waitlist_status == "joined"
    assert waitlist_projection.fields["waitlist_idempotency_key"] == (
        "waitlist:conv_projection_1:1"
    )
    assert waitlist_projection.fields["waitlist_joined_at"] == (
        "2026-05-30T12:00:00Z"
    )

    handoff_decision = _decision(
        context,
        role="handoff",
        route="handoff",
        current_state="human_requested",
        next_state="human_handoff",
        handoff={"status": "requested", "reason": "lead_requested_human"},
        template_plan={"items": [{"template_id": "handoff.acknowledge"}]},
    )
    handoff_projection = build_sales_inbox_projection(
        context=context,
        decision=handoff_decision,
        validator_result=_validator(handoff_decision),
        runtime_state_diff=_state_diff(handoff_decision),
        delivery_events=[DeliveryEvent(event="handoff_requested")],
    )

    handoff_result = validate_sales_inbox_projection(
        handoff_projection,
        handoff_decision,
        context,
    )
    assert handoff_result.status == "passed"
    assert handoff_projection.handoff_status == "requested"
    assert handoff_projection.fields["handoff_reason"] == "lead_requested_human"
    assert handoff_projection.fields["human_active"] is True
    assert handoff_projection.fields["ai_paused"] is True


def test_projection_preserves_identity_source_labels_without_verified_promotion() -> None:
    context = _context(
        facts=[
            {
                "key": "profile_name",
                "value": "Ana Perfil",
                "source": "channel_metadata",
                "reliability": "channel_provided",
                "evidence": ["sender.name"],
            },
            {
                "key": "person_name",
                "value": "Ana",
                "source": "user_message",
                "reliability": "customer_provided",
                "evidence": ["turn_projection_1.inbound"],
            },
            {
                "key": "phone",
                "value": "+5511999999999",
                "source": "sales_inbox_projection",
                "reliability": "unverified",
                "evidence": ["previous_projection"],
            },
        ]
    )
    decision = _decision(context)

    projection = build_sales_inbox_projection(
        context=context,
        decision=decision,
        validator_result=_validator(decision),
        runtime_state_diff=_state_diff(decision),
        delivery_events=[DeliveryEvent(event="reserved")],
    )

    identity = {item.key: item for item in projection.identity}
    assert identity["profile_name"].source == "channel_provided"
    assert identity["profile_name"].verified is False
    assert identity["person_name"].source == "customer_provided"
    assert identity["person_name"].verified is True
    assert identity["phone"].source == "unverified"
    assert identity["phone"].verified is False
    assert validate_sales_inbox_projection(projection, decision, context).status == "passed"


def test_projection_rejects_mismatched_or_failed_runtime_state_source() -> None:
    context = _context()
    decision = _decision(context)
    runtime_state_diff = _state_diff(decision)
    runtime_state_diff["decision_id"] = "decision_other"

    with pytest.raises(SalesInboxProjectionBuildError, match="decision_id"):
        build_sales_inbox_projection(
            context=context,
            decision=decision,
            validator_result=_validator(decision),
            runtime_state_diff=runtime_state_diff,
            delivery_events=[DeliveryEvent(event="reserved")],
        )

    failed_source = _state_diff(decision)
    failed_source["source"] = "fallback"
    with pytest.raises(SalesInboxProjectionBuildError, match="validated state"):
        build_sales_inbox_projection(
            context=context,
            decision=decision,
            validator_result=_validator(decision),
            runtime_state_diff=failed_source,
            delivery_events=[DeliveryEvent(event="reserved")],
        )
