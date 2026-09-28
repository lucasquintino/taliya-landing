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


def _context() -> TurnContext:
    return TurnContext.model_validate(
        {
            "turn_id": "turn_identity_projection_1",
            "conversation_id": "conv_identity_projection_1",
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "inbound": {
                "message_id": "msg_identity_projection_1",
                "idempotency_key": "wa:conv_identity_projection_1:1",
                "text": "meu nome e Ana",
            },
            "facts": [
                {
                    "key": "profile_name",
                    "value": "Ana Perfil",
                    "source": "channel_metadata",
                    "reliability": "channel_provided",
                    "evidence": ["sender.name"],
                },
                {
                    "key": "phone",
                    "value": "+5511888888888",
                    "source": "sales_inbox_projection",
                    "reliability": "unverified",
                    "evidence": ["previous_projection"],
                },
            ],
            "compact_memory": [{"kind": "summary", "value": "Lead identificada."}],
            "sales_inbox_inputs": {
                "lead_id": "lead_identity_projection_1",
                "source": "pilates_landing",
                "entry_intent": "site_widget",
                "channel_conversation_id": "wa_identity_projection_1",
                "diagnostic_status": "not_started",
                "waitlist_status": "none",
                "handoff_status": "none",
                "demo_status": "not_offered",
            },
        }
    )


def _decision(context: TurnContext, *, facts: list[dict[str, Any]]) -> ConductorDecision:
    return ConductorDecision.model_validate(
        {
            "schema_version": "011.0",
            "turn_id": context.turn_id,
            "conversation_id": context.conversation_id,
            "channel": context.channel,
            "agent_key": context.agent_key,
            "role": "product",
            "route": "product",
            "previous_state": "product_question",
            "current_state": "product_question",
            "next_state": "product_answered",
            "detected_intents": ["product_question"],
            "direct_question_present": False,
            "direct_question_answered_first": True,
            "facts": facts,
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
    )


def _validator(decision: ConductorDecision) -> ValidatorResult:
    return ValidatorResult(
        decision_id=decision.decision_id,
        status="passed",
        final_disposition="accepted",
    )


def test_projection_merges_runtime_identity_facts_without_promoting_weak_sources() -> None:
    context = _context()
    decision = _decision(
        context,
        facts=[
            {
                "key": "profile_name",
                "value": "Ana Perfil",
                "source": "user_message",
                "reliability": "customer_provided",
                "evidence": ["turn_identity_projection_1.inbound"],
                "confidence": "high",
            },
            {
                "key": "email",
                "value": "ana@studio.com",
                "source": "operator",
                "reliability": "operator_provided",
                "evidence": ["operator.confirmed_email"],
                "confidence": "high",
            },
            {
                "key": "phone",
                "value": "+5511888888888",
                "source": "sales_inbox_projection",
                "reliability": "unverified",
                "evidence": ["previous_projection"],
                "confidence": "medium",
            },
        ],
    )
    validator_result = _validator(decision)
    projection = build_sales_inbox_projection(
        context=context,
        decision=decision,
        validator_result=validator_result,
        runtime_state_diff=build_runtime_state_diff(decision, validator_result),
        delivery_events=[DeliveryEvent(event="reserved")],
    )

    identity = {(item.key, item.value): item for item in projection.identity}

    assert identity[("profile_name", "Ana Perfil")].source == "customer_provided"
    assert identity[("profile_name", "Ana Perfil")].verified is True
    assert identity[("email", "ana@studio.com")].source == "operator_provided"
    assert identity[("email", "ana@studio.com")].verified is True
    assert identity[("phone", "+5511888888888")].source == "unverified"
    assert identity[("phone", "+5511888888888")].verified is False
    assert validate_sales_inbox_projection(projection, decision, context).status == "passed"
