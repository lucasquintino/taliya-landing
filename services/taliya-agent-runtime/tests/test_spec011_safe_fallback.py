from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.fallback import (
    SafeFallbackResult,
    build_safe_fallback_disposition,
)
from app.core.taliya_commercial.schemas import (
    ConductorDecision,
    RepairResult,
    TurnContext,
    ValidatorResult,
)
from app.core.taliya_commercial.validators import validate_conductor_result
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState


def _request(text: str = "quero saber mais") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_fallback_1",
                "lead_id": "lead_fallback_1",
                "channel_conversation_id": "wa_fallback_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_fallback_1:1",
                "channel_message_id": "wamid_fallback_1",
                "type": "text",
                "text": text,
            },
            "sender": {"name": "Ana"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _context(text: str = "quero saber mais") -> TurnContext:
    return build_turn_context(
        turn_id="turn_fallback_1",
        request=_request(text),
        state=RuntimeState(
            conversation_id="conv_fallback_1",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_product_agent",
            summary="Lead perguntou sobre preco.",
            diagnostic={"status": "not_started", "ledger": []},
            waitlist={"status": "none"},
            demo={"status": "not_offered"},
        ),
        recent_events=[],
        product_knowledge_keys=["prices"],
        spec006_contract_keys=["product_positioning"],
    )


def _decision_payload(context: TurnContext) -> dict[str, Any]:
    return {
        "schema_version": "011.0",
        "turn_id": context.turn_id,
        "conversation_id": context.conversation_id,
        "channel": context.channel,
        "agent_key": context.agent_key,
        "role": "entry",
        "route": "entry",
        "previous_state": "new_lead",
        "current_state": "general_interest",
        "next_state": "general_interest",
        "detected_intents": ["general_interest"],
        "direct_question_present": False,
        "direct_question_answered_first": True,
        "diagnostic": {"action": "offer"},
        "language_policy": {
            "register": "studio_owner_practical",
            "crm_term_policy": "avoid_by_default",
        },
        "template_plan": {
            "items": [
                {
                    "template_id": "opening.general_interest",
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


def _decision(context: TurnContext) -> ConductorDecision:
    return ConductorDecision.model_validate(_decision_payload(context))


def test_safe_fallback_not_needed_for_accepted_decision() -> None:
    context = _context()
    decision = _decision(context)
    validator_result = validate_conductor_result(decision, context)

    result = build_safe_fallback_disposition(
        context=context,
        decision=decision,
        validator_result=validator_result,
        repair_result=RepairResult(),
        failure_source="validator_blocked",
    )

    assert result.status == "not_needed"
    assert result.route == "none"
    assert result.template_id is None
    assert result.commercial_answer_allowed is False


def test_safe_fallback_for_blocked_validator_requests_handoff_without_copy() -> None:
    context = _context()
    decision = _decision(context).model_copy(update={"conversation_id": "conv_other"})
    validator_result = validate_conductor_result(decision, context)

    result = build_safe_fallback_disposition(
        context=context,
        decision=decision,
        validator_result=validator_result,
        failure_source="validator_blocked",
    )

    assert validator_result.status == "blocked"
    assert result.status == "handoff_required"
    assert result.route == "handoff"
    assert result.template_id == "handoff.acknowledge"
    assert result.handoff_status == "requested"
    assert result.ai_pause_required is True
    assert result.commercial_answer_allowed is False
    assert "context_field_mismatch" in result.error_codes
    assert not hasattr(result, "message_text")
    assert not hasattr(result, "rendered_messages")


def test_safe_fallback_for_failed_repair_preserves_failure_state() -> None:
    context = _context()
    decision = _decision(context)
    validator_result = ValidatorResult(
        decision_id=decision.decision_id,
        status="repairable",
        errors=[
            {
                "code": "template_plan_invalid",
                "severity": "P1",
                "message": "missing variable",
                "path": "template_plan.items[0]",
            }
        ],
    )
    repair_result = RepairResult(
        attempted=True,
        attempt_count=1,
        status="failed",
        errors_sent=["template_plan_invalid"],
    )

    result = build_safe_fallback_disposition(
        context=context,
        decision=decision,
        validator_result=validator_result,
        repair_result=repair_result,
        failure_source="repair_failed",
    )

    assert result.status == "handoff_required"
    assert result.source == "repair_failed"
    assert result.repair_status == "failed"
    assert result.template_id == "handoff.acknowledge"
    assert result.reason_code == "repair_failed"
    assert result.commercial_answer_allowed is False


def test_safe_fallback_for_provider_timeout_uses_only_timeout_template() -> None:
    context = _context()

    result = build_safe_fallback_disposition(
        context=context,
        failure_source="provider_timeout",
        failure_reason="openai_timeout",
    )

    assert result.status == "safe_fallback"
    assert result.route == "safe_fallback"
    assert result.template_id == "fallback.provider_timeout"
    assert result.handoff_status == "none"
    assert result.ai_pause_required is False
    assert result.commercial_answer_allowed is False
    assert not result.template_id.startswith("product.")
    assert not result.template_id.startswith("diagnostic.")
    assert not result.template_id.startswith("waitlist.")


def test_safe_fallback_for_invalid_json_uses_only_invalid_json_template() -> None:
    context = _context()

    result = build_safe_fallback_disposition(
        context=context,
        failure_source="provider_output_invalid",
        failure_reason="invalid_json",
    )

    assert result.status == "safe_fallback"
    assert result.route == "safe_fallback"
    assert result.template_id == "fallback.invalid_json"
    assert result.reason_code == "invalid_json"
    assert result.commercial_answer_allowed is False


def test_safe_fallback_schema_rejects_customer_facing_text_fields() -> None:
    context = _context()

    with pytest.raises(ValidationError):
        SafeFallbackResult.model_validate(
            {
                "turn_id": context.turn_id,
                "conversation_id": context.conversation_id,
                "channel": context.channel,
                "status": "safe_fallback",
                "route": "safe_fallback",
                "template_id": "fallback.invalid_json",
                "message_text": "vou te explicar os planos mesmo assim",
            }
        )
