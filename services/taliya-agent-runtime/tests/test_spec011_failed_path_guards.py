from __future__ import annotations

from typing import Any

from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.failed_path_guards import (
    validate_failed_path_result,
)
from app.core.taliya_commercial.fallback import build_safe_fallback_disposition
from app.core.taliya_commercial.schemas import (
    ConductorDecision,
    RepairResult,
    TurnContext,
    ValidatorResult,
)
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState


def _request(text: str = "quanto custa?") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_failed_path_1",
                "lead_id": "lead_failed_path_1",
                "channel_conversation_id": "wa_failed_path_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_failed_path_1:1",
                "channel_message_id": "wamid_failed_path_1",
                "type": "text",
                "text": text,
            },
            "sender": {"name": "Ana"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _context(text: str = "quanto custa?") -> TurnContext:
    return build_turn_context(
        turn_id="turn_failed_path_1",
        request=_request(text),
        state=RuntimeState(
            conversation_id="conv_failed_path_1",
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
        "role": "product",
        "route": "product",
        "previous_state": "new_lead",
        "current_state": "product_question",
        "next_state": "product_answered",
        "detected_intents": ["price_question"],
        "direct_question_present": True,
        "direct_question_answered_first": True,
        "language_policy": {
            "register": "studio_owner_practical",
            "crm_term_policy": "avoid_by_default",
        },
        "template_plan": {
            "items": [
                {
                    "template_id": "product.price_direct",
                    "variables": {
                        "plan_price_summary": {
                            "kind": "short_text",
                            "value": "Plano mensal",
                            "source": "official_product_knowledge",
                            "evidence": ["product_knowledge.prices"],
                        }
                    },
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


def _blocked_validator_result() -> ValidatorResult:
    return ValidatorResult(
        decision_id="decision_failed_path_1",
        status="blocked",
        errors=[
            {
                "code": "context_field_mismatch",
                "severity": "P0",
                "message": "context mismatch",
                "path": "conversation_id",
            }
        ],
        final_disposition="blocked",
    )


def test_failed_path_guard_accepts_safe_fallback_disposition_without_copy() -> None:
    context = _context()
    fallback = build_safe_fallback_disposition(
        context=context,
        failure_source="provider_timeout",
        failure_reason="openai_timeout",
    )

    result = validate_failed_path_result(fallback)

    assert result.status == "passed"
    assert result.errors == []
    assert fallback.template_id == "fallback.provider_timeout"
    assert not hasattr(fallback, "message_text")
    assert not hasattr(fallback, "rendered_messages")


def test_failed_path_guard_accepts_visible_validator_and_repair_failures() -> None:
    blocked_validation = _blocked_validator_result()
    failed_repair = RepairResult(
        attempted=True,
        attempt_count=1,
        status="failed",
        errors_sent=["template_plan_invalid"],
    )

    validation_result = validate_failed_path_result(blocked_validation)
    repair_result = validate_failed_path_result(failed_repair)

    assert validation_result.status == "passed"
    assert repair_result.status == "passed"


def test_failed_path_guard_rejects_rendered_text_and_product_template() -> None:
    result = validate_failed_path_result(
        {
            "source": "provider_timeout",
            "status": "safe_fallback",
            "template_id": "product.price_direct",
            "rendered_messages": [
                {
                    "text": "O plano custa X e resolve seu atendimento.",
                    "template_id": "product.price_direct",
                }
            ],
        },
        decision_id="decision_failed_path_rendered",
    )

    codes = {error.code for error in result.errors}
    assert result.status == "blocked"
    assert "failed_path_template_forbidden" in codes
    assert "failed_path_rendered_output_forbidden" in codes
    assert "failed_path_customer_copy_forbidden" in codes


def test_failed_path_guard_rejects_commercial_route_advancement_and_variables() -> None:
    result = validate_failed_path_result(
        {
            "status": "failed",
            "route": "product",
            "next_state": "product_answered",
            "template_plan": {
                "items": [
                    {
                        "template_id": "product.price_direct",
                        "variables": {
                            "plan_price_summary": {
                                "value": "Plano mensal",
                                "source": "official_product_knowledge",
                            }
                        },
                    }
                ]
            },
        },
        decision_id="decision_failed_path_route",
    )

    codes = {error.code for error in result.errors}
    assert result.status == "blocked"
    assert "failed_path_route_forbidden" in codes
    assert "failed_path_state_advancement_forbidden" in codes
    assert "failed_path_template_forbidden" in codes
    assert "failed_path_commercial_variable_forbidden" in codes


def test_failed_path_guard_rejects_accepted_or_repaired_conversion() -> None:
    context = _context()
    accepted_validation = ValidatorResult(
        decision_id="decision_failed_path_accepted",
        status="passed",
        final_disposition="accepted",
    )
    accepted_dict = {
        "decision_id": "decision_failed_path_accepted_dict",
        "status": "passed",
        "final_disposition": "accepted",
    }
    repaired = RepairResult(
        attempted=True,
        attempt_count=1,
        status="repaired",
        repaired_decision=_decision(context),
    )

    validation_result = validate_failed_path_result(accepted_validation)
    dict_result = validate_failed_path_result(accepted_dict)
    repair_result = validate_failed_path_result(repaired)

    assert validation_result.status == "blocked"
    assert dict_result.status == "blocked"
    assert repair_result.status == "blocked"
    assert {
        error.code for error in validation_result.errors
    } == {"failed_path_accepted_decision_forbidden"}
    assert {
        error.code for error in dict_result.errors
    } == {"failed_path_accepted_decision_forbidden"}
    assert "failed_path_repaired_decision_forbidden" in {
        error.code for error in repair_result.errors
    }


def test_failed_path_guard_rejects_dict_commercial_answer_flag() -> None:
    result = validate_failed_path_result(
        {
            "status": "safe_fallback",
            "route": "safe_fallback",
            "template_id": "fallback.invalid_json",
            "commercial_answer_allowed": True,
        },
        decision_id="decision_failed_path_commercial_flag",
    )

    assert result.status == "blocked"
    assert {error.code for error in result.errors} == {
        "failed_path_commercial_answer_allowed"
    }


def test_failed_path_guard_rejects_embedded_conductor_decision() -> None:
    result = validate_failed_path_result(_decision(_context()))

    assert result.status == "blocked"
    assert {error.code for error in result.errors} >= {
        "failed_path_decision_embedded",
        "failed_path_route_forbidden",
        "failed_path_template_forbidden",
    }
