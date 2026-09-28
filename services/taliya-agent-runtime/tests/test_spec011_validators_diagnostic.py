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
_FINAL_STAGED_TEMPLATES = [
    "diagnostic.deliver_hold",
    "diagnostic.deliver_context",
    "diagnostic.deliver_crm_base",
    "diagnostic.deliver_operational_step",
    "diagnostic.deliver_agent_recommendation",
    "diagnostic.deliver_plan_recommendation",
    "diagnostic.deliver_demo_not_offered",
]


def _request(text: str = "120") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_validator_diagnostic_1",
                "lead_id": "lead_validator_diagnostic_1",
                "channel_conversation_id": "wa_validator_diagnostic_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_validator_diagnostic_1:1",
                "channel_message_id": "wamid_validator_diagnostic_1",
                "type": "text",
                "text": text,
            },
            "sender": {"name": "Ana"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _ledger(status_by_key: dict[str, str]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for question_key in _REQUIRED_DIAGNOSTIC_KEYS:
        status = status_by_key.get(question_key, "missing")
        item: dict[str, Any] = {
            "question_key": question_key,
            "status": status,
            "confidence": "high" if status == "answered" else "low",
            "may_ask_again": status != "answered",
        }
        if status == "answered":
            item["answer_value"] = f"answer:{question_key}"
            item["evidence"] = [f"user answered {question_key}"]
        else:
            item["evidence"] = []
        items.append(item)
    return items


def _complete_ledger_without_urgency() -> list[dict[str, Any]]:
    return _ledger(
        {
            "active_students_or_size": "answered",
            "main_pain": "answered",
            "pain_detail": "answered",
            "current_process": "answered",
            "priority": "answered",
            "urgency": "missing",
        }
    )


def _complete_ledger() -> list[dict[str, Any]]:
    return _ledger({key: "answered" for key in _REQUIRED_DIAGNOSTIC_KEYS})


def _context(
    *,
    text: str = "120",
    ledger: list[dict[str, Any]] | None = None,
) -> TurnContext:
    return build_turn_context(
        turn_id="turn_validator_diagnostic_1",
        request=_request(text),
        state=RuntimeState(
            conversation_id="conv_validator_diagnostic_1",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_diagnostic_agent",
            summary="Lead esta no diagnostico gratuito.",
            diagnostic={"status": "in_progress", "ledger": ledger or []},
            waitlist={"status": "none"},
            demo={"status": "not_offered"},
        ),
        recent_events=[],
        product_knowledge_keys=["prices", "plans"],
        spec006_contract_keys=["product_positioning"],
    )


def _decision_payload(
    context: TurnContext,
    *,
    action: str = "ask_next",
    next_question_key: str | None = "main_pain",
    ledger_updates: list[dict[str, Any]] | None = None,
    template_ids: list[str] | None = None,
    numeric_interpretations: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if action == "complete":
        current_state = "diagnostic_ready"
        next_state = "diagnostic_delivered"
        default_template_ids = ["diagnostic.deliver_hold"]
    else:
        current_state = "diagnostic_in_progress"
        next_state = "diagnostic_in_progress"
        default_template_ids = ["diagnostic.ask_main_pain"]
    answered_update = next(
        (
            update
            for update in (ledger_updates or [])
            if update.get("status") == "answered" and update.get("answer_value")
        ),
        None,
    )
    question_variables = (
        {
            "answer_feedback": {
                "kind": "short_text",
                "value": f"Entendi: {answered_update['answer_value']}.",
                "source": "diagnostic_ledger",
                "evidence": answered_update.get("evidence") or ["diagnostic.ledger"],
                "max_length": 180,
            }
        }
        if action == "ask_next" and answered_update
        else {}
    )

    def template_variables(template_id: str) -> dict[str, Any]:
        if template_id.startswith("diagnostic.ask_"):
            return question_variables
        if template_id in {
            "diagnostic.deliver_demo_not_offered",
            "diagnostic.deliver_demo_already_offered",
        }:
            return {
                "demo_status": {
                    "kind": "enum",
                    "value": "not_offered",
                    "source": "runtime_state",
                    "evidence": ["runtime_state.demo.status"],
                }
            }
        if template_id == "diagnostic.deliver_context":
            return {
                "pain_context_human": {
                    "kind": "long_text",
                    "value": "O peso principal esta em atendimento e follow-up.",
                    "source": "diagnostic_ledger",
                    "evidence": ["user_message"],
                    "max_length": 420,
                }
            }
        if template_id == "diagnostic.deliver_crm_base":
            return {
                "crm_base_recommendation": {
                    "kind": "long_text",
                    "value": "Eu organizaria contatos e conversas em uma base unica.",
                    "source": "diagnostic_ledger",
                    "evidence": ["user_message"],
                    "max_length": 260,
                }
            }
        if template_id == "diagnostic.deliver_operational_step":
            return {
                "operational_first_step": {
                    "kind": "long_text",
                    "value": "Separar novos interessados e retornos pendentes.",
                    "source": "diagnostic_ledger",
                    "evidence": ["user_message"],
                    "max_length": 240,
                }
            }
        if template_id == "diagnostic.deliver_agent_recommendation":
            return {
                "agent_name": {
                    "kind": "short_text",
                    "value": "Atendimento",
                    "source": "official_product_knowledge",
                    "evidence": ["product_knowledge.plans"],
                    "max_length": 60,
                },
                "agent_fit_phrase": {
                    "kind": "enum",
                    "value": "faria sentido primeiro",
                    "source": "model_decision",
                    "evidence": ["model_decision"],
                },
                "agent_pain_resolved": {
                    "kind": "long_text",
                    "value": "interessados sem resposta",
                    "source": "diagnostic_ledger",
                    "evidence": ["user_message"],
                    "max_length": 180,
                },
                "agent_recommendation_reason": {
                    "kind": "long_text",
                    "value": "essa dor apareceu no diagnostico",
                    "source": "diagnostic_ledger",
                    "evidence": ["user_message"],
                    "max_length": 280,
                },
                "agent_practical_action": {
                    "kind": "long_text",
                    "value": "organiza respostas e proximos passos",
                    "source": "diagnostic_ledger",
                    "evidence": ["user_message"],
                    "max_length": 280,
                },
            }
        if template_id == "diagnostic.deliver_plan_recommendation":
            return {
                "recommended_plan_or_range": {
                    "kind": "short_text",
                    "value": "Completo",
                    "source": "official_product_knowledge",
                    "evidence": ["product_knowledge.plans"],
                    "max_length": 90,
                }
            }
        return {}

    return {
        "schema_version": "011.0",
        "turn_id": context.turn_id,
        "conversation_id": context.conversation_id,
        "channel": context.channel,
        "agent_key": context.agent_key,
        "role": "diagnostic",
        "route": "diagnostic",
        "previous_state": "diagnostic_in_progress",
        "current_state": current_state,
        "next_state": next_state,
        "detected_intents": ["diagnostic_answer"],
        "direct_question_present": False,
        "direct_question_answered_first": True,
        "numeric_interpretations": numeric_interpretations or [],
        "diagnostic": {
            "action": action,
            "ledger_updates": ledger_updates or [],
            "next_question_key": next_question_key,
        },
        "language_policy": {
            "register": "studio_owner_practical",
            "crm_term_policy": "avoid_by_default",
        },
        "template_plan": {
            "items": [
                {
                    "template_id": template_id,
                    "variables": template_variables(template_id),
                }
                for template_id in (template_ids or default_template_ids)
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


def _decision(context: TurnContext, **overrides: Any) -> ConductorDecision:
    return ConductorDecision.model_validate(_decision_payload(context, **overrides))


def _issue_codes(result: Any) -> set[str]:
    return {issue.code for issue in result.errors}


def test_validator_blocks_completed_diagnostic_without_mandatory_urgency() -> None:
    context = _context(ledger=_complete_ledger_without_urgency())
    decision = _decision(context, action="complete", next_question_key=None)

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "diagnostic_required_field_missing" in _issue_codes(result)
    assert result.errors[0].path == "diagnostic.ledger.urgency"


def test_validator_sends_only_missing_pain_detail_to_repair() -> None:
    context = _context(
        ledger=_ledger(
            {
                "active_students_or_size": "answered",
                "main_pain": "answered",
                "pain_detail": "missing",
                "current_process": "answered",
                "priority": "answered",
                "urgency": "answered",
            }
        )
    )
    decision = _decision(
        context,
        action="complete",
        next_question_key=None,
        template_ids=_FINAL_STAGED_TEMPLATES,
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "repairable"
    assert _issue_codes(result) == {"diagnostic_inferable_pain_detail_should_complete"}


def test_validator_accepts_completed_diagnostic_with_all_required_fields() -> None:
    context = _context(ledger=_complete_ledger())
    decision = _decision(
        context,
        action="complete",
        next_question_key=None,
        template_ids=_FINAL_STAGED_TEMPLATES,
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "passed"
    assert result.errors == []


def test_validator_blocks_urgency_completed_from_assistant_question_prompt() -> None:
    assistant_prompt = (
        "Voces estao buscando resolver isso agora ou so pesquisando por enquanto?"
    )
    context = _context(text="meu foco principal e vendas", ledger=_complete_ledger())
    context = context.model_copy(
        update={
            "recent_transcript": [
                {
                    "role": "assistant",
                    "content": assistant_prompt,
                    "source": "runtime_state",
                }
            ]
        }
    )
    decision = _decision(
        context,
        action="complete",
        next_question_key=None,
        ledger_updates=[
            {
                "question_key": "urgency",
                "status": "answered",
                "answer_value": "agora",
                "evidence": [assistant_prompt],
                "confidence": "high",
            }
        ],
        template_ids=_FINAL_STAGED_TEMPLATES,
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "repairable"
    assert "diagnostic_urgency_evidence_is_assistant_prompt" in _issue_codes(result)


def test_validator_allows_urgency_grounded_in_current_lead_answer() -> None:
    assistant_prompt = (
        "Voces estao buscando resolver isso agora ou so pesquisando por enquanto?"
    )
    context = _context(text="quero resolver agora", ledger=_complete_ledger())
    context = context.model_copy(
        update={
            "recent_transcript": [
                {
                    "role": "assistant",
                    "content": assistant_prompt,
                    "source": "runtime_state",
                }
            ]
        }
    )
    decision = _decision(
        context,
        action="complete",
        next_question_key=None,
        ledger_updates=[
            {
                "question_key": "urgency",
                "status": "answered",
                "answer_value": "agora",
                "evidence": ["quero resolver agora"],
                "confidence": "high",
            }
        ],
        template_ids=_FINAL_STAGED_TEMPLATES,
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "passed"
    assert result.errors == []


def test_validator_blocks_legacy_one_piece_diagnostic_delivery_template() -> None:
    context = _context(ledger=_complete_ledger())
    payload = _decision_payload(
        context,
        action="complete",
        next_question_key=None,
        template_ids=["diagnostic.deliver", *_FINAL_STAGED_TEMPLATES],
    )
    payload["template_plan"]["items"][0]["variables"] = {
        "pain_context_human": {
            "kind": "long_text",
            "value": "A rotina comercial esta perdendo interessados no WhatsApp.",
            "source": "diagnostic_ledger",
            "evidence": ["user_message"],
            "max_length": 320,
        },
        "crm_base_recommendation": {
            "kind": "long_text",
            "value": "Eu organizaria contatos, conversas e proximos passos em um so lugar.",
            "source": "diagnostic_ledger",
            "evidence": ["user_message"],
            "max_length": 260,
        },
        "operational_first_step": {
            "kind": "long_text",
            "value": "O primeiro passo e separar novos interessados de retornos pendentes.",
            "source": "diagnostic_ledger",
            "evidence": ["user_message"],
            "max_length": 240,
        },
        "recommended_plan_or_range": {
            "kind": "short_text",
            "value": "Completo",
            "source": "official_product_knowledge",
            "evidence": ["product_knowledge.plans"],
            "max_length": 90,
        },
        "demo_status": {
            "kind": "enum",
            "value": "not_offered",
            "source": "runtime_state",
            "evidence": ["runtime_state.demo.status"],
        },
    }
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "repairable"
    assert _issue_codes(result) == {"legacy_diagnostic_deliver_template_not_allowed"}


def test_validator_does_not_require_price_hook_after_completed_diagnostic() -> None:
    context = _context(ledger=_complete_ledger())
    payload = _decision_payload(
        context,
        action="complete",
        next_question_key=None,
        template_ids=_FINAL_STAGED_TEMPLATES,
    )
    payload["detected_intents"] = ["price_question", "diagnostic_request"]
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "passed"
    assert result.errors == []


def test_validator_requires_ask_next_to_target_missing_required_field() -> None:
    context = _context(
        ledger=_ledger(
            {
                "active_students_or_size": "answered",
                "main_pain": "missing",
                "urgency": "missing",
            }
        )
    )
    decision = _decision(context, action="ask_next", next_question_key="plan_fit_context")

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "diagnostic_next_question_invalid" in _issue_codes(result)
    assert result.errors[0].path == "diagnostic.next_question_key"


def test_validator_blocks_multiple_diagnostic_question_templates_in_one_turn() -> None:
    context = _context(
        ledger=_ledger(
            {
                "active_students_or_size": "answered",
                "main_pain": "missing",
                "urgency": "missing",
            }
        )
    )
    decision = _decision(
        context,
        action="ask_next",
        next_question_key="main_pain",
        template_ids=["diagnostic.ask_main_pain", "diagnostic.ask_urgency"],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "diagnostic_multiple_next_questions" in _issue_codes(result)
    assert result.errors[0].path == "template_plan.items"


def test_validator_requires_evidence_for_answered_diagnostic_update() -> None:
    context = _context(
        ledger=_ledger(
            {
                "active_students_or_size": "answered",
                "main_pain": "answered",
                "priority": "missing",
            }
        )
    )
    decision = _decision(
        context,
        action="ask_next",
        next_question_key="urgency",
        ledger_updates=[
            {
                "question_key": "priority",
                "status": "answered",
                "answer_value": "agenda",
                "evidence": [],
                "confidence": "high",
            }
        ],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "diagnostic_answer_evidence_missing" in _issue_codes(result)
    assert result.errors[0].path == "diagnostic.ledger_updates[0].evidence"


def test_validator_accepts_simple_student_count_answer_for_pending_field() -> None:
    context = _context(
        text="120",
        ledger=_ledger({"active_students_or_size": "missing", "main_pain": "missing"}),
    )
    decision = _decision(
        context,
        action="ask_next",
        next_question_key="main_pain",
        ledger_updates=[
            {
                "question_key": "active_students_or_size",
                "status": "answered",
                "answer_value": "120",
                "evidence": ["120"],
                "confidence": "high",
            }
        ],
        numeric_interpretations=[
            {
                "raw_text": "120",
                "kind": "student_count",
                "value": 120,
                "evidence": ["120"],
                "confidence": "high",
            }
        ],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "passed"
    assert result.errors == []


def test_validator_blocks_first_diagnostic_question_before_active_students() -> None:
    context = _context(
        text="perco muitos interessados no WhatsApp porque a equipe demora para responder",
        ledger=_ledger({"active_students_or_size": "missing", "main_pain": "missing"}),
    )
    decision = _decision(
        context,
        action="offer",
        next_question_key="urgency",
        ledger_updates=[
            {
                "question_key": "main_pain",
                "status": "answered",
                "answer_value": "perco interessados no WhatsApp",
                "evidence": [
                    "perco muitos interessados no WhatsApp porque a equipe demora para responder"
                ],
                "confidence": "high",
            }
        ],
        template_ids=["diagnostic.offer_soft", "diagnostic.ask_urgency"],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "repairable"
    assert "diagnostic_start_must_ask_active_students" in _issue_codes(result)


def test_validator_blocks_pain_first_offer_misrouted_as_product() -> None:
    context = build_turn_context(
        turn_id="turn_validator_pain_first_product_route",
        request=_request(
            "perco muitos interessados no WhatsApp porque a equipe demora para responder"
        ),
        state=None,
        recent_events=[],
        product_knowledge_keys=["prices", "plans"],
        spec006_contract_keys=["product_positioning"],
    )
    payload = _decision_payload(
        context,
        action="offer",
        next_question_key="active_students_or_size",
        ledger_updates=[
            {
                "question_key": "main_pain",
                "status": "answered",
                "answer_value": "perco interessados no WhatsApp",
                "evidence": [
                    "perco muitos interessados no WhatsApp porque a equipe demora para responder"
                ],
                "confidence": "high",
            }
        ],
        template_ids=["opening.general_interest", "diagnostic.offer_soft"],
    )
    payload.update(
        {
            "role": "product",
            "route": "product",
            "current_state": "product",
            "next_state": "diagnostic",
            "detected_intents": [
                "pain_report",
                "whatsapp_followup_issue",
                "product_interest",
            ],
        }
    )
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "repairable"
    assert "pain_first_diagnostic_offer_must_use_diagnostic_route" in _issue_codes(result)
    assert "diagnostic_start_must_ask_active_students" in _issue_codes(result)


def test_validator_blocks_repeating_answered_active_students_question() -> None:
    context = _context(
        ledger=_ledger(
            {
                "active_students_or_size": "answered",
                "main_pain": "missing",
            }
        )
    )
    decision = _decision(
        context,
        action="ask_next",
        next_question_key="active_students_or_size",
        template_ids=["diagnostic.ask_active_students"],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "diagnostic_question_repeated" in _issue_codes(result)
    assert result.errors[0].path == "diagnostic.next_question_key"


def test_validator_blocks_repeated_question_hidden_in_template_plan() -> None:
    context = _context(
        ledger=_ledger(
            {
                "active_students_or_size": "answered",
                "main_pain": "missing",
            }
        )
    )
    decision = _decision(
        context,
        action="ask_next",
        next_question_key="main_pain",
        template_ids=["diagnostic.ask_active_students"],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "diagnostic_question_repeated" in _issue_codes(result)


def test_validator_allows_reasking_ambiguous_diagnostic_question() -> None:
    context = _context(
        ledger=_ledger(
            {
                "active_students_or_size": "ambiguous",
                "main_pain": "missing",
            }
        )
    )
    decision = _decision(
        context,
        action="ask_next",
        next_question_key="active_students_or_size",
        template_ids=["diagnostic.ask_active_students"],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "passed"
    assert result.errors == []
