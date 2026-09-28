from __future__ import annotations

from typing import Any

from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.schemas import ConductorDecision, TurnContext
from app.core.taliya_commercial.validators import validate_conductor_result
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState

_REQUIRED_DIAGNOSTIC_KEYS = (
    "active_students_or_size",
    "main_pain",
    "pain_detail",
    "current_process",
    "priority",
    "urgency",
)


def _request(text: str = "me explica a Taliya") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {
                "conversation_id": "conv_validator_leak_1",
                "lead_id": "lead_validator_leak_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "widget:conv_validator_leak_1:1",
                "type": "text",
                "text": text,
            },
            "sender": {},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _complete_ledger() -> list[dict[str, Any]]:
    return [
        {
            "question_key": question_key,
            "status": "answered",
            "answer_value": f"answer:{question_key}",
            "evidence": [f"user answered {question_key}"],
            "confidence": "high",
        }
        for question_key in _REQUIRED_DIAGNOSTIC_KEYS
    ]


def _context() -> TurnContext:
    return build_turn_context(
        turn_id="turn_validator_leak_1",
        request=_request(),
        state=RuntimeState(
            conversation_id="conv_validator_leak_1",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_product_agent",
            summary="Lead pediu explicacao do produto.",
            diagnostic={"status": "completed", "ledger": _complete_ledger()},
            waitlist={"status": "none"},
            demo={"status": "not_offered"},
        ),
        recent_events=[],
        product_knowledge_keys=["plans", "links"],
        spec006_contract_keys=["product_positioning"],
    )


def _decision_payload(
    context: TurnContext,
    *,
    template_item: dict[str, Any],
    route: str = "product",
    role: str = "product",
    diagnostic_action: str = "none",
) -> dict[str, Any]:
    return {
        "schema_version": "011.0",
        "turn_id": context.turn_id,
        "conversation_id": context.conversation_id,
        "channel": context.channel,
        "agent_key": context.agent_key,
        "role": role,
        "route": route,
        "previous_state": "product_question",
        "current_state": "product_question",
        "next_state": "product_question",
        "detected_intents": ["product_question"],
        "direct_question_present": True,
        "direct_question_answered_first": True,
        "diagnostic": {"action": diagnostic_action},
        "language_policy": {
            "register": "studio_owner_practical",
            "crm_term_policy": "avoid_by_default",
        },
        "template_plan": {"items": [template_item]},
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


def _decision(context: TurnContext, **overrides: Any) -> ConductorDecision:
    return ConductorDecision.model_validate(_decision_payload(context, **overrides))


def _issue_codes(result: Any) -> set[str]:
    return {issue.code for issue in result.errors}


def _product_summary_template(value: str) -> dict[str, Any]:
    return {
        "template_id": "product.overview_short",
        "variables": {
            "product_fact_summary": {
                "kind": "long_text",
                "value": value,
                "source": "official_product_knowledge",
                "evidence": ["product_knowledge.plans"],
                "max_length": 320,
            }
        },
    }


def test_validator_blocks_internal_reliability_label_in_customer_variable() -> None:
    context = _context()
    decision = _decision(
        context,
        template_item={
            "template_id": "opening.cold_greeting_named",
            "variables": {
                "first_name": {
                    "kind": "short_text",
                    "value": "Reliable profile first name: Ana",
                    "source": "channel_metadata",
                    "evidence": ["sender.name"],
                    "max_length": 40,
                }
            },
        },
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "internal_text_leak" in _issue_codes(result)


def test_validator_blocks_internal_source_label_in_product_variable() -> None:
    context = _context()
    decision = _decision(
        context,
        template_item=_product_summary_template(
            "lead came from the site and asked about product knowledge"
        ),
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "internal_text_leak" in _issue_codes(result)


def test_validator_blocks_banned_final_diagnostic_phrase_in_variable() -> None:
    context = _context()
    decision = _decision(
        context,
        role="diagnostic",
        route="diagnostic",
        diagnostic_action="complete",
        template_item={
            "template_id": "diagnostic.deliver_context",
            "variables": {
                "pain_context_human": {
                    "kind": "long_text",
                    "value": "Pelo contexto, o principal gargalo parece agenda.",
                    "source": "diagnostic_ledger",
                    "evidence": ["diagnostic.main_pain"],
                    "max_length": 320,
                }
            },
        },
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "banned_customer_phrase" in _issue_codes(result)


def test_validator_blocks_waitlist_promise_phrase_in_variable() -> None:
    context = _context()
    decision = _decision(
        context,
        role="waitlist",
        route="waitlist",
        template_item={
            "template_id": "waitlist.offer_after_contract_intent",
            "variables": {
                "waitlist_context_summary": {
                    "kind": "long_text",
                    "value": "Tem checkout VIP com desconto se entrar hoje.",
                    "source": "runtime_state",
                    "evidence": ["waitlist.eligibility"],
                    "max_length": 220,
                }
            },
        },
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "banned_waitlist_promise" in _issue_codes(result)


def test_validator_accepts_safe_product_variable_without_internal_or_banned_text() -> None:
    context = _context()
    decision = _decision(
        context,
        template_item=_product_summary_template(
            "Taliya ajuda o studio a organizar rotina, alunos, agenda e proximos passos."
        ),
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "passed"
    assert result.errors == []
