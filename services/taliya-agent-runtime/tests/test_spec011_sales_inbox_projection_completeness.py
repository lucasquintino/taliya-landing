from __future__ import annotations

from typing import Any

from app.core.taliya_commercial.runtime_state import build_runtime_state_diff
from app.core.taliya_commercial.sales_inbox_projection import (
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


def _context(*, diagnostic_ledger: list[dict[str, Any]] | None = None) -> TurnContext:
    return TurnContext.model_validate(
        {
            "turn_id": "turn_projection_completeness_1",
            "conversation_id": "conv_projection_completeness_1",
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "inbound": {
                "message_id": "msg_projection_completeness_1",
                "idempotency_key": "wa:conv_projection_completeness_1:1",
                "text": "ok",
            },
            "compact_memory": [
                {"kind": "summary", "value": "Lead em fluxo comercial."}
            ],
            "diagnostic_ledger": diagnostic_ledger or [],
            "sales_inbox_inputs": {
                "lead_id": "lead_projection_completeness_1",
                "source": "pilates_landing",
                "entry_intent": "site_widget",
                "channel_conversation_id": "wa_projection_completeness_1",
                "diagnostic_status": "not_started",
                "waitlist_status": "none",
                "handoff_status": "none",
                "demo_status": "not_offered",
            },
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
        "previous_state": "product_question",
        "current_state": "product_followup",
        "next_state": "product_followup",
        "detected_intents": ["product_followup"],
        "direct_question_present": False,
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
        "template_plan": {"items": [{"template_id": "product.overview_short"}]},
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


def _projection(
    context: TurnContext,
    decision: ConductorDecision,
    *,
    events: list[DeliveryEvent] | None = None,
) -> Any:
    validator_result = _validator(decision)
    return build_sales_inbox_projection(
        context=context,
        decision=decision,
        validator_result=validator_result,
        runtime_state_diff=build_runtime_state_diff(decision, validator_result),
        delivery_events=events or [DeliveryEvent(event="reserved")],
    )


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


def test_completed_diagnostic_projection_is_complete_and_validated() -> None:
    context = _context(diagnostic_ledger=_complete_ledger())
    decision = _decision(
        context,
        role="diagnostic",
        route="diagnostic",
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

    projection = _projection(context, decision)

    assert projection.fields["diagnostic_ledger_complete"] is True
    assert projection.fields["required_diagnostic_keys"] == list(
        _REQUIRED_DIAGNOSTIC_KEYS
    )
    assert projection.fields["final_plan_or_range"] == "Essencial ou Avance"
    assert projection.fields["final_demo_line"] == "quer ver a demonstracao?"
    assert validate_sales_inbox_projection(projection, decision, context).status == "passed"


def test_demo_followup_projection_preserves_commercial_demo_state_only() -> None:
    context = _context()
    decision = _decision(
        context,
        demo={
            "customer_facing_concept": "commercial_product_demo",
            "status": "viewed_or_asked",
            "next_step": "ask_demo_reaction",
        },
        template_plan={"items": [{"template_id": "product.demo_followup"}]},
    )

    projection = _projection(context, decision)

    assert projection.fields["demo_customer_facing_concept"] == (
        "commercial_product_demo"
    )
    assert projection.fields["demo_status"] == "viewed_or_asked"
    assert projection.fields["demo_next_step"] == "ask_demo_reaction"
    assert "openai_demo" not in projection.fields
    assert "demo_video" not in projection.fields
    assert "video_production" not in projection.fields
    assert validate_sales_inbox_projection(projection, decision, context).status == "passed"


def test_waitlist_projection_distinguishes_offered_pending_joined_and_declined() -> None:
    context = _context()
    offered = _decision(
        context,
        role="waitlist",
        route="waitlist",
        current_state="waitlist_offered",
        next_state="waitlist_offered",
        waitlist={"eligibility": "eligible", "status": "offered"},
        template_plan={"items": [{"template_id": "waitlist.offer"}]},
    )
    pending = _decision(
        context,
        role="waitlist",
        route="waitlist",
        current_state="waitlist_pending_data",
        next_state="waitlist_pending_data",
        waitlist={
            "eligibility": "eligible",
            "status": "pending_details",
            "missing_details": ["studio_name", "city_state"],
        },
        template_plan={"items": [{"template_id": "waitlist.pending_details"}]},
    )
    joined = _decision(
        context,
        role="waitlist",
        route="waitlist",
        current_state="waitlist_pending_data",
        next_state="waitlist_joined",
        waitlist={"eligibility": "eligible", "status": "joined"},
        template_plan={"items": [{"template_id": "waitlist.joined"}]},
    )
    declined = _decision(
        context,
        role="waitlist",
        route="waitlist",
        current_state="waitlist_offered",
        next_state="waitlist_declined",
        waitlist={"eligibility": "eligible", "status": "declined"},
        template_plan={"items": [{"template_id": "waitlist.declined"}]},
    )

    offered_projection = _projection(context, offered)
    pending_projection = _projection(context, pending)
    joined_projection = _projection(
        context,
        joined,
        events=[
            DeliveryEvent(
                event="waitlist_joined",
                idempotency_key="waitlist:joined:1",
                metadata={"joined_at": "2026-05-30T12:00:00Z"},
            )
        ],
    )
    declined_projection = _projection(context, declined)

    assert offered_projection.fields["waitlist_eligibility"] == "eligible"
    assert offered_projection.waitlist_status == "offered"
    assert pending_projection.fields["missing_waitlist_fields"] == [
        "studio_name",
        "city_state",
    ]
    assert joined_projection.fields["waitlist_idempotency_key"] == "waitlist:joined:1"
    assert declined_projection.waitlist_status == "declined"
    for projection in (
        offered_projection,
        pending_projection,
        joined_projection,
        declined_projection,
    ):
        joined_text = " ".join(str(value) for value in projection.fields.values())
        assert "checkout" not in joined_text
        assert "vip" not in joined_text
        assert "data de abertura" not in joined_text


def test_product_followup_projection_keeps_stage_template_source_and_next_action() -> None:
    context = _context()
    decision = _decision(
        context,
        current_state="product_followup",
        next_state="product_followup_answered",
        template_plan={
            "items": [
                {"template_id": "product.plan_fit_with_diagnostic"},
                {"template_id": "product.demo_direct"},
            ]
        },
    )

    projection = _projection(context, decision)

    assert projection.commercial_stage == "product_followup_answered"
    assert projection.fields["template_ids"] == [
        "product.plan_fit_with_diagnostic",
        "product.demo_direct",
    ]
    assert projection.fields["source_labels"]["source"] == "pilates_landing"
    assert projection.fields["operator_next_action"] == "none"
    assert validate_sales_inbox_projection(projection, decision, context).status == "passed"
