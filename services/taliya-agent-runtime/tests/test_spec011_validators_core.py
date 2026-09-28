from __future__ import annotations

from typing import Any

from app.core.taliya_commercial.conductor import ConductorTurnResult
from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.schemas import (
    ConductorDecision,
    ModelUsage,
    TurnContext,
    ValidatorResult,
)
from app.core.taliya_commercial.validators import validate_conductor_result
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState


def _request(text: str = "Quero ver uma demo da Taliya.") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_validator_1",
                "lead_id": "lead_validator_1",
                "channel_conversation_id": "wa_validator_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_validator_1:1",
                "channel_message_id": "wamid_validator_1",
                "type": "text",
                "text": text,
            },
            "sender": {"name": "Ana"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _context(
    text: str = "Quero ver uma demo da Taliya.",
    *,
    product_knowledge_keys: list[str] | None = None,
    spec006_contract_keys: list[str] | None = None,
) -> TurnContext:
    return build_turn_context(
        turn_id="turn_validator_1",
        request=_request(text),
        state=RuntimeState(
            conversation_id="conv_validator_1",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_product_agent",
            summary="Lead pediu demonstracao do produto.",
            diagnostic={"status": "not_started", "ledger": []},
            waitlist={"status": "none"},
            demo={"status": "not_offered"},
        ),
        recent_events=[],
        product_knowledge_keys=product_knowledge_keys or ["links"],
        spec006_contract_keys=spec006_contract_keys or ["product_positioning"],
    )


def _fresh_context(text: str) -> TurnContext:
    return build_turn_context(
        turn_id="turn_validator_fresh",
        request=_request(text),
        state=None,
        recent_events=[],
        product_knowledge_keys=["links"],
        spec006_contract_keys=["product_positioning"],
    )


def _widget_empty_context() -> TurnContext:
    request = AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {
                "conversation_id": "conv_widget_empty_validator",
                "lead_id": "lead_widget_empty_validator",
                "channel_conversation_id": "browser_widget_empty_validator",
                "source": "pilates_landing",
                "entry_intent": "widget",
            },
            "message": {
                "idempotency_key": "widget:empty-validator:1",
                "channel_message_id": "web_empty_validator_1",
                "type": "text",
                "text": "",
            },
            "sender": {},
            "metadata": {"page_path": "/pilates", "source_section": "floating_agent"},
        }
    )
    return build_turn_context(
        turn_id="turn_widget_empty_validator",
        request=request,
        state=None,
        recent_events=[],
        product_knowledge_keys=["links"],
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
        "current_state": "demo_question",
        "next_state": "demo_offered",
        "detected_intents": ["demo_request"],
        "direct_question_present": True,
        "direct_question_answered_first": True,
        "demo": {
            "customer_facing_concept": "commercial_product_demo",
            "status": "offered",
            "next_step": "offer_demo",
        },
        "language_policy": {
            "register": "studio_owner_practical",
            "crm_term_policy": "avoid_by_default",
        },
        "template_plan": {
            "items": [
                {
                    "template_id": "product.demo_direct",
                    "variables": {
                        "official_demo_link": {
                            "kind": "url",
                            "value": "https://www.taliya.com.br/pilates/planos/demonstracao",
                            "source": "official_product_knowledge",
                            "evidence": ["product_knowledge.links.demonstration"],
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


def _price_decision_payload(context: TurnContext) -> dict[str, Any]:
    payload = _decision_payload(context)
    payload.update(
        {
            "current_state": "product_question",
            "next_state": "product_question",
            "detected_intents": ["price_question", "student_count_fact"],
            "diagnostic": {"action": "offer"},
            "demo": {
                "customer_facing_concept": "commercial_product_demo",
                "status": "not_offered",
                "next_step": "none",
            },
            "numeric_interpretations": [
                {
                    "raw_text": "497",
                    "kind": "plan_price",
                    "value": 497,
                    "currency": "BRL",
                    "evidence": ["plano de 497"],
                    "confidence": "high",
                },
                {
                    "raw_text": "120",
                    "kind": "student_count",
                    "value": 120,
                    "evidence": ["tenho 120 alunos"],
                    "confidence": "high",
                },
            ],
            "facts": [
                {
                    "key": "active_students_or_size",
                    "value": 120,
                    "source": "user_message",
                    "reliability": "customer_provided",
                    "confidence": "high",
                    "evidence": ["tenho 120 alunos"],
                }
            ],
            "template_plan": {
                "items": [
                    {
                        "template_id": "product.price_direct",
                        "variables": {
                            "plan_price_summary": {
                                "kind": "long_text",
                                "value": (
                                    "Base R$ 197/mes, Essencial R$ 497/mes, "
                                    "Avance R$ 897/mes e Completo R$ 1.497/mes."
                                ),
                                "source": "official_product_knowledge",
                                "evidence": ["product_knowledge.prices"],
                                "max_length": 360,
                            }
                        },
                    },
                    {
                        "template_id": "diagnostic.price_hook",
                        "variables": {},
                    }
                ]
            },
        }
    )
    return payload


def _price_decision(context: TurnContext) -> ConductorDecision:
    return ConductorDecision.model_validate(_price_decision_payload(context))


def _turn_result(context: TurnContext) -> ConductorTurnResult:
    return ConductorTurnResult(
        decision=_decision(context),
        model_usage=ModelUsage(
            model="gpt-5.4-mini",
            input_tokens=150,
            output_tokens=42,
            cost_usd=0.0014,
        ),
    )


def _issue_codes(result: ValidatorResult) -> set[str]:
    return {issue.code for issue in result.errors}


def test_validator_accepts_typed_conductor_turn_result() -> None:
    context = _context()

    result = validate_conductor_result(_turn_result(context), context)

    assert result.status == "passed"
    assert result.final_disposition == "accepted"
    assert result.errors == []
    assert result.repair_attempt_count == 0


def test_validator_accepts_decision_directly_without_requiring_provider_envelope() -> None:
    context = _context()

    result = validate_conductor_result(_decision(context), context)

    assert result.status == "passed"
    assert result.errors == []


def test_validator_reports_unsupported_schema_version_without_throwing() -> None:
    context = _context()
    decision = _decision(context).model_copy(update={"schema_version": "011.1"})

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert result.final_disposition == "blocked"
    assert _issue_codes(result) == {"unsupported_schema_version"}
    assert result.errors[0].path == "schema_version"


def test_validator_blocks_context_identity_mismatch() -> None:
    context = _context()
    decision = _decision(context).model_copy(update={"conversation_id": "conv_other"})

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "context_field_mismatch" in _issue_codes(result)
    assert result.errors[0].path == "conversation_id"


def test_validator_blocks_previous_state_mismatch_when_context_has_state_hint() -> None:
    context = _context().model_copy(
        update={"compact_memory": [{"current_state": "diagnostic_in_progress"}]}
    )
    decision = _decision(context).model_copy(update={"previous_state": "new_lead"})

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "state_context_mismatch" in _issue_codes(result)
    assert result.errors[0].path == "previous_state"


def test_validator_reuses_template_registry_errors_as_repairable_issues() -> None:
    context = _context()
    decision = _decision(context).model_copy(deep=True)
    decision.template_plan.items[0].variables = {}

    result = validate_conductor_result(decision, context)

    assert result.status == "repairable"
    assert result.final_disposition is None
    assert "template_plan_invalid" in _issue_codes(result)
    assert "missing_required_variable:official_demo_link" in result.errors[0].message
    assert result.errors[0].path == "template_plan.items[0]"


def test_validator_blocks_template_item_channel_mismatch() -> None:
    context = _context()
    decision = _decision(context).model_copy(deep=True)
    decision.template_plan.items[0].channel = "widget"

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "channel_mismatch" in _issue_codes(result)
    assert result.errors[0].path == "template_plan.items[0].channel"


def test_validator_blocks_empty_state_fields_without_commercial_fallback() -> None:
    context = _context()
    decision = _decision(context).model_copy(update={"next_state": " "})

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "invalid_state_field" in _issue_codes(result)
    assert not hasattr(result, "rendered_messages")
    assert not hasattr(result, "repaired_decision")


def test_validator_resolves_official_product_variable_evidence_in_context() -> None:
    context = _context(product_knowledge_keys=["links"])
    decision = _price_decision(context)

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "unresolved_product_evidence" in _issue_codes(result)
    assert result.errors[0].path == "template_plan.items[0].variables.plan_price_summary"


def test_validator_blocks_invented_or_shortened_official_demo_link() -> None:
    context = _context(product_knowledge_keys=["links"])
    decision = _decision(context).model_copy(deep=True)
    decision.template_plan.items[0].variables[
        "official_demo_link"
    ].value = "https://taliya.link/demo"

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "official_link_mismatch" in _issue_codes(result)
    assert result.errors[0].path == "template_plan.items[0].variables.official_demo_link"


def test_validator_accepts_official_plan_price_and_separate_student_count() -> None:
    context = _context(
        "Vi o plano de 497 e tenho 120 alunos",
        product_knowledge_keys=["prices", "plans"],
    )
    decision = _price_decision(context)

    result = validate_conductor_result(decision, context)

    assert result.status == "passed"
    assert result.errors == []


def test_validator_blocks_pure_cold_greeting_that_starts_diagnostic() -> None:
    context = _fresh_context("bom dia")
    payload = _decision_payload(context)
    payload.update(
        {
            "role": "diagnostic",
            "route": "diagnostic",
            "current_state": "diagnostic_started",
            "next_state": "diagnostic_in_progress",
            "detected_intents": ["greeting", "diagnostic"],
            "direct_question_present": False,
            "direct_question_answered_first": True,
            "demo": {
                "customer_facing_concept": "commercial_product_demo",
                "status": "not_offered",
                "next_step": "none",
            },
            "diagnostic": {
                "action": "ask_next",
                "next_question_key": "active_students_or_size",
            },
            "template_plan": {
                "items": [{"template_id": "diagnostic.ask_active_students"}]
            },
        }
    )
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "repairable"
    assert "cold_greeting_must_stay_entry" in _issue_codes(result)


def test_validator_blocks_empty_widget_opening_as_site_cta() -> None:
    context = _widget_empty_context()
    payload = _decision_payload(context)
    payload.update(
        {
            "role": "entry",
            "route": "entry",
            "current_state": "site_opening",
            "next_state": "diagnostic_offered",
            "detected_intents": ["site_cta"],
            "direct_question_present": False,
            "direct_question_answered_first": True,
            "demo": {
                "customer_facing_concept": "commercial_product_demo",
                "status": "not_offered",
                "next_step": "none",
            },
            "diagnostic": {"action": "offer"},
            "template_plan": {"items": [{"template_id": "opening.site_cta"}]},
        }
    )
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "repairable"
    assert "widget_empty_must_use_opening_template" in _issue_codes(result)


def test_validator_blocks_plan_fit_question_that_only_asks_diagnostic() -> None:
    context = _fresh_context("qual plano voce recomenda pra mim?")
    payload = _decision_payload(context)
    payload.update(
        {
            "role": "product",
            "route": "product",
            "current_state": "plan_fit_question",
            "next_state": "diagnostic_offered",
            "detected_intents": ["plan_recommendation", "pricing_fit"],
            "direct_question_present": True,
            "direct_question_answered_first": True,
            "demo": {
                "customer_facing_concept": "commercial_product_demo",
                "status": "not_offered",
                "next_step": "none",
            },
            "diagnostic": {"action": "offer", "next_question_key": "main_pain"},
            "template_plan": {"items": [{"template_id": "diagnostic.ask_main_pain"}]},
        }
    )
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "repairable"
    assert "plan_fit_direct_answer_template_missing" in _issue_codes(result)


def test_validator_blocks_incomplete_whatsapp_direct_answer() -> None:
    context = _context(
        "como funciona no WhatsApp?",
        product_knowledge_keys=["whatsapp_scope", "links"],
    )
    payload = _decision_payload(context)
    payload.update(
        {
            "role": "product",
            "route": "product",
            "current_state": "whatsapp_question",
            "next_state": "product_question",
            "detected_intents": ["product_question", "whatsapp_product_question"],
            "direct_question_present": True,
            "direct_question_answered_first": True,
            "demo": {
                "customer_facing_concept": "commercial_product_demo",
                "status": "not_offered",
                "next_step": "none",
            },
            "template_plan": {
                "items": [
                    {
                        "template_id": "product.whatsapp_direct",
                        "variables": {
                            "product_fact_summary": {
                                "kind": "long_text",
                                "value": "Os alunos nao precisam baixar app nem criar senha.",
                                "source": "official_product_knowledge",
                                "evidence": ["product_knowledge.whatsapp_scope"],
                                "max_length": 320,
                            }
                        },
                    }
                ]
            },
        }
    )
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "repairable"
    assert {
        "whatsapp_direct_answer_incomplete",
        "whatsapp_direct_demo_link_missing",
    }.issubset(_issue_codes(result))


def test_validator_requires_diagnostic_hook_after_price_answer() -> None:
    context = _context(
        "Quanto custa?",
        product_knowledge_keys=["prices", "plans"],
    )
    payload = _price_decision_payload(context)
    payload["diagnostic"] = {"action": "none"}
    payload["template_plan"]["items"] = [
        item
        for item in payload["template_plan"]["items"]
        if item["template_id"] != "diagnostic.price_hook"
    ]
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "repairable"
    assert "price_question_missing_diagnostic_hook" in _issue_codes(result)
    assert "price_question_missing_diagnostic_offer" in _issue_codes(result)


def test_validator_requires_price_answer_before_price_hook() -> None:
    context = _context(
        "Quanto custa?",
        product_knowledge_keys=["prices", "plans"],
    )
    payload = _price_decision_payload(context)
    payload["template_plan"]["items"] = [
        item
        for item in payload["template_plan"]["items"]
        if item["template_id"] != "product.price_direct"
    ]
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "price_question_missing_price_answer" in _issue_codes(result)


def test_validator_requires_approved_value_template_for_price_objection() -> None:
    context = _context(
        "Achei caro.",
        product_knowledge_keys=["prices", "plans"],
    )
    payload = _price_decision_payload(context)
    payload["detected_intents"] = ["price_objection"]
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "repairable"
    assert "price_objection_value_template_missing" in _issue_codes(result)


def test_validator_accepts_price_objection_value_template_as_answer_and_hook() -> None:
    context = _context(
        "Achei caro.",
        product_knowledge_keys=["prices", "plans"],
    )
    payload = _price_decision_payload(context)
    payload["detected_intents"] = ["price_objection"]
    payload["diagnostic"] = {"action": "offer"}
    payload["template_plan"]["items"] = [
        {"template_id": "product.price_objection_value", "variables": {}}
    ]
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "passed"


def test_validator_requires_demo_direct_request_flags() -> None:
    context = _context("quero ver uma demonstracao")
    payload = _decision_payload(context)
    payload["direct_question_present"] = False
    payload["direct_question_answered_first"] = False
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "repairable"
    assert "demo_direct_question_flags_missing" in _issue_codes(result)


def test_validator_requires_contextual_hook_for_price_request_plus_pain() -> None:
    context = _context(
        "Tenho reposicao baguncada na agenda e queria saber preco.",
        product_knowledge_keys=["prices", "plans"],
    )
    payload = _price_decision_payload(context)
    payload["detected_intents"] = ["price_request", "pain_description"]
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "repairable"
    assert "price_plus_context_requires_context_hook" in _issue_codes(result)


def test_validator_allows_price_answer_without_hook_after_diagnostic_refusal() -> None:
    context = _context(
        "Quanto custa? Mas nao quero diagnostico agora.",
        product_knowledge_keys=["prices", "plans"],
    )
    payload = _price_decision_payload(context)
    payload["detected_intents"] = ["price_question", "diagnostic_refusal"]
    payload["diagnostic"] = {"action": "none"}
    payload["template_plan"]["items"] = [
        item
        for item in payload["template_plan"]["items"]
        if item["template_id"] != "diagnostic.price_hook"
    ]
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "passed"
    assert result.errors == []


def test_validator_blocks_diagnostic_hook_after_diagnostic_refusal() -> None:
    context = _context(
        "Nao quero diagnostico agora, so me fala o preco.",
        product_knowledge_keys=["prices", "plans"],
    )
    payload = _price_decision_payload(context)
    payload["detected_intents"] = ["price_question", "diagnostic_refusal"]
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "repairable"
    assert "diagnostic_refusal_not_respected" in _issue_codes(result)


def test_validator_accepts_simple_student_count_with_user_evidence() -> None:
    context = _context("120", product_knowledge_keys=["prices", "plans"])
    payload = _price_decision_payload(context)
    payload["numeric_interpretations"] = [
        {
            "raw_text": "120",
            "kind": "student_count",
            "value": 120,
            "evidence": ["120"],
            "confidence": "high",
        }
    ]
    payload["facts"] = []
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "passed"
    assert result.errors == []


def test_validator_blocks_plan_price_not_found_in_official_knowledge() -> None:
    context = _context(product_knowledge_keys=["prices", "plans"])
    payload = _price_decision_payload(context)
    payload["numeric_interpretations"][0]["raw_text"] = "333"
    payload["numeric_interpretations"][0]["value"] = 333
    payload["numeric_interpretations"][0]["evidence"] = ["plano de 333"]
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "unknown_plan_price" in _issue_codes(result)
    assert result.errors[0].path == "numeric_interpretations[0]"


def test_validator_blocks_invented_price_inside_official_price_variable() -> None:
    context = _context(product_knowledge_keys=["prices", "plans"])
    payload = _price_decision_payload(context)
    payload["template_plan"]["items"][0]["variables"]["plan_price_summary"][
        "value"
    ] = "Plano especial R$ 999/mes."
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "unsupported_price_value" in _issue_codes(result)
    assert result.errors[0].path == "template_plan.items[0].variables.plan_price_summary"


def test_validator_blocks_official_price_value_as_student_count_regression() -> None:
    context = _context("Vi o plano de 497", product_knowledge_keys=["prices", "plans"])
    payload = _price_decision_payload(context)
    payload["numeric_interpretations"] = [
        {
            "raw_text": "497",
            "kind": "student_count",
            "value": 497,
            "evidence": ["plano de 497"],
            "confidence": "high",
        }
    ]
    payload["facts"] = []
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "student_count_matches_official_price" in _issue_codes(result)
    assert result.errors[0].path == "numeric_interpretations[0]"
