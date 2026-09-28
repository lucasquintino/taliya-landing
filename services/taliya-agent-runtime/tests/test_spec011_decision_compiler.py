from __future__ import annotations

import inspect
from typing import Any

import pytest

import app.core.taliya_commercial.decision_compiler as decision_compiler_module
from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.decision_compiler import (
    DecisionCompilerError,
    compile_action_decision,
)
from app.core.taliya_commercial.schemas import ConductorActionDecision, TurnContext
from app.core.taliya_commercial.turn_situation import build_turn_situation
from app.core.taliya_commercial.validators import validate_conductor_result
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState


def _request(text: str = "Quanto custa?") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_compiler_1",
                "lead_id": "lead_compiler_1",
                "channel_conversation_id": "wa_compiler_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_compiler_1:1",
                "channel_message_id": "wamid_compiler_1",
                "type": "text",
                "text": text,
            },
            "sender": {"name": "Ana", "whatsapp_phone": "+5511999999999"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _state(
    *,
    diagnostic_status: str = "not_started",
    ledger: list[dict[str, Any]] | None = None,
) -> RuntimeState:
    return RuntimeState(
        conversation_id="conv_compiler_1",
        agent_key="taliya_commercial",
        current_agent_name="taliya_commercial_diagnostic_agent"
        if diagnostic_status == "in_progress"
        else "taliya_commercial_entry_agent",
        summary="Lead em conversa comercial da Taliya.",
        diagnostic={"status": diagnostic_status, "ledger": ledger or []},
        waitlist={"status": "none"},
        demo={"status": "not_offered"},
    )


def _context(
    text: str = "Quanto custa?",
    *,
    diagnostic_status: str = "not_started",
    ledger: list[dict[str, Any]] | None = None,
) -> TurnContext:
    return build_turn_context(
        turn_id="turn_compiler_1",
        request=_request(text),
        state=_state(diagnostic_status=diagnostic_status, ledger=ledger),
        recent_events=[],
        product_knowledge_keys=["prices", "plans", "links", "whatsapp_scope"],
        spec006_contract_keys=["product_positioning"],
    )


def _complete_ledger() -> list[dict[str, Any]]:
    return [
        {
            "question_key": key,
            "status": "answered",
            "answer_value": key,
            "evidence": [f"message:{key}"],
            "confidence": "high",
        }
        for key in (
            "active_students_or_size",
            "main_pain",
            "pain_detail",
            "current_process",
            "priority",
            "urgency",
        )
    ]


def _action_payload(
    context: TurnContext,
    *,
    selected_action: str,
    captured_slots: list[dict[str, Any]] | None = None,
    diagnostic_details: dict[str, Any] | None = None,
    waitlist_details: dict[str, Any] | None = None,
    handoff_details: dict[str, Any] | None = None,
    intents: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "011.action_decision.v1",
        "turn_id": context.turn_id,
        "conversation_id": context.conversation_id,
        "channel": context.channel,
        "agent_key": context.agent_key,
        "selected_action": selected_action,
        "interpreted_intents": intents or [selected_action],
        "direct_question": {
            "present": selected_action == "answer_direct_product_question",
            "answered_first": selected_action == "answer_direct_product_question",
            "answer_obligations": ["answer_current_question_first"]
            if selected_action == "answer_direct_product_question"
            else [],
        },
        "captured_slots": captured_slots or [],
        "product_fact_keys_used": ["prices", "plans", "links", "whatsapp_scope"],
        "numeric_interpretations": [],
        "diagnostic_intent": {
            "status": "complete"
            if selected_action == "capture_pending_diagnostic_answer"
            else "none",
            "details": diagnostic_details or {},
        },
        "demo_intent": {"status": "none"},
        "waitlist_intent": {"status": "none", "details": waitlist_details or {}},
        "handoff_intent": {"status": "none", "details": handoff_details or {}},
        "reply_goal": "compile tested action",
        "confidence": "high",
        "evidence": ["llm_interpreted_latest_inbound"],
        "needs_clarification": False,
        "repair_hints": [],
    }


def _action_decision(context: TurnContext, **kwargs: Any) -> ConductorActionDecision:
    return ConductorActionDecision.model_validate(_action_payload(context, **kwargs))


def test_compiler_turns_price_action_into_valid_official_price_plan() -> None:
    context = _context("Quanto custa?")
    turn_situation = build_turn_situation(context)
    action = _action_decision(
        context,
        selected_action="answer_direct_product_question",
    )

    decision = compile_action_decision(
        action,
        context=context,
        turn_situation=turn_situation,
    )
    result = validate_conductor_result(decision, context=context)

    assert result.status == "passed"
    assert decision.route == "product"
    assert [item.template_id for item in decision.template_plan.items] == [
        "product.price_direct",
        "diagnostic.price_hook",
    ]
    price_variable = decision.template_plan.items[0].variables["plan_price_summary"]
    assert price_variable.source == "official_product_knowledge"
    assert "R$ 497/mes" in price_variable.value


def test_compiler_captures_simple_number_and_asks_next_diagnostic_question() -> None:
    context = _context("120", diagnostic_status="in_progress")
    turn_situation = build_turn_situation(context)
    assert turn_situation.pending_question_key == "active_students_or_size"
    action = _action_decision(
        context,
        selected_action="capture_pending_diagnostic_answer",
        captured_slots=[
            {
                "key": "active_students_or_size",
                "value": "120",
                "evidence": ["message.latest:120"],
                "confidence": "high",
            }
        ],
    )

    decision = compile_action_decision(
        action,
        context=context,
        turn_situation=turn_situation,
    )
    result = validate_conductor_result(decision, context=context)

    assert result.status == "passed"
    assert decision.diagnostic.action == "ask_next"
    assert decision.diagnostic.ledger_updates[0].question_key == "active_students_or_size"
    assert decision.diagnostic.ledger_updates[0].answer_value == "120"
    assert decision.diagnostic.next_question_key == "main_pain"
    question_item = decision.template_plan.items[0]
    assert question_item.template_id == "diagnostic.ask_main_pain"
    assert "answer_feedback" in question_item.variables


def test_compiler_completes_diagnostic_after_urgency_capture_with_staged_plan() -> None:
    ledger = [
        {
            "question_key": "active_students_or_size",
            "status": "answered",
            "answer_value": "120 alunos",
            "evidence": ["message:m1"],
            "confidence": "high",
        },
        {
            "question_key": "main_pain",
            "status": "answered",
            "answer_value": "perde leads no WhatsApp",
            "evidence": ["message:m2"],
            "confidence": "high",
        },
        {
            "question_key": "pain_detail",
            "status": "answered",
            "answer_value": "retorno demora",
            "evidence": ["message:m3"],
            "confidence": "high",
        },
        {
            "question_key": "current_process",
            "status": "answered",
            "answer_value": "WhatsApp e planilha",
            "evidence": ["message:m4"],
            "confidence": "high",
        },
        {
            "question_key": "priority",
            "status": "answered",
            "answer_value": "vendas",
            "evidence": ["message:m5"],
            "confidence": "high",
        },
    ]
    context = _context("agora", diagnostic_status="in_progress", ledger=ledger)
    turn_situation = build_turn_situation(context)
    assert turn_situation.pending_question_key == "urgency"
    action = _action_decision(
        context,
        selected_action="capture_pending_diagnostic_answer",
        captured_slots=[
            {
                "key": "urgency",
                "value": "resolver agora",
                "evidence": ["message.latest:agora"],
                "confidence": "high",
            }
        ],
        diagnostic_details={
            "pain_context_human": "O ponto que mais pesa parece estar no retorno dos interessados.",
            "crm_base_recommendation": (
                "Eu organizaria interessados e proximos passos em uma base unica."
            ),
            "operational_first_step": (
                "Separar quem precisa de resposta hoje e quem precisa de follow-up."
            ),
            "agent_pain_resolved": "interessados ficando sem retorno",
            "agent_practical_action": "organiza contatos, respostas e proximos passos",
        },
    )

    decision = compile_action_decision(
        action,
        context=context,
        turn_situation=turn_situation,
    )
    result = validate_conductor_result(decision, context=context)

    assert result.status == "passed"
    assert decision.diagnostic.action == "complete"
    assert decision.template_plan.chunk_policy == "staged_diagnostic"
    assert [item.template_id for item in decision.template_plan.items] == [
        "diagnostic.deliver_hold",
        "diagnostic.deliver_context",
        "diagnostic.deliver_crm_base",
        "diagnostic.deliver_operational_step",
        "diagnostic.deliver_agent_recommendation",
        "diagnostic.deliver_plan_recommendation",
        "diagnostic.deliver_demo_not_offered",
    ]


def test_compiler_rejects_unsupported_actions_instead_of_guessing() -> None:
    context = _context("quero entrar na lista")
    turn_situation = build_turn_situation(context)
    action = _action_decision(context, selected_action="unsupported_action")

    with pytest.raises(DecisionCompilerError):
        compile_action_decision(
            action,
            context=context,
            turn_situation=turn_situation,
        )


def test_compiler_rejects_pain_first_without_llm_human_context() -> None:
    context = _context(
        "perco muitos interessados no WhatsApp porque a equipe demora para responder"
    )
    turn_situation = build_turn_situation(context)
    action = _action_decision(
        context,
        selected_action="offer_diagnostic_from_pain",
        intents=["pain_statement", "interest_in_solutions"],
        diagnostic_details={},
    )

    with pytest.raises(DecisionCompilerError) as exc_info:
        compile_action_decision(
            action,
            context=context,
            turn_situation=turn_situation,
        )

    assert "pain_context_human" in str(exc_info.value)


@pytest.mark.parametrize(
    ("selected_action", "text", "intents", "expected_route", "expected_template"),
    [
        ("answer_general_interest", "quero saber mais", [], "entry", "opening.general_interest"),
        (
            "answer_source_opening",
            "vim do instagram",
            ["source_from_instagram"],
            "entry",
            "opening.instagram_source",
        ),
        (
            "offer_diagnostic_from_pain",
            "perco interessados no WhatsApp",
            ["pain_first"],
            "diagnostic",
            "opening.cold_greeting",
        ),
        (
            "start_requested_diagnostic",
            "quero diagnostico",
            ["diagnostic_request"],
            "diagnostic",
            "opening.diagnostic_cta",
        ),
        (
            "handoff_requested",
            "quero falar com alguem",
            ["human_handoff_request"],
            "handoff",
            "handoff.acknowledge",
        ),
        (
            "clarify_ambiguous_opening",
            "nao sei",
            [],
            "entry",
            "fallback.unmapped_adaptive",
        ),
        (
            "answer_plan_fit_with_diagnostic_offer",
            "qual plano serve?",
            ["plan_fit_question"],
            "product",
            "product.plan_fit_with_diagnostic",
        ),
        (
            "answer_how_it_works",
            "como funciona?",
            ["how_it_works"],
            "product",
            "product.how_it_works_direct",
        ),
        (
            "answer_whatsapp_scope",
            "funciona no WhatsApp?",
            ["whatsapp_product_question"],
            "product",
            "product.whatsapp_direct",
        ),
        (
            "answer_integration_scope_safely",
            "integra com instagram?",
            ["integration_scope_question"],
            "product",
            "product.integration_scope_direct",
        ),
        (
            "answer_price_objection",
            "achei caro",
            ["price_objection"],
            "product",
            "product.price_objection_value",
        ),
        (
            "offer_diagnostic_after_answer",
            "serve pra mim?",
            [],
            "product",
            "diagnostic.offer_soft",
        ),
        (
            "clarify_product_question",
            "isso ai",
            [],
            "product",
            "fallback.unmapped_adaptive",
        ),
    ],
)
def test_compiler_handles_entry_and_product_action_matrix(
    selected_action: str,
    text: str,
    intents: list[str],
    expected_route: str,
    expected_template: str,
) -> None:
    context = _context(text)
    turn_situation = build_turn_situation(context)
    action = _action_decision(
        context,
        selected_action=selected_action,
        intents=intents or [selected_action],
        diagnostic_details={
            "pain_context_human": "O ponto citado merece diagnostico antes de comparar plano.",
            "plan_fit_context": "Para saber se encaixa, preciso entender tamanho e prioridade.",
            "integration_topic": "essa integracao",
            "clarification_question": "Voce quer tirar uma duvida ou fazer o diagnostico?",
        },
        handoff_details={"reason": "pedido do lead para falar com uma pessoa"},
    )

    decision = compile_action_decision(
        action,
        context=context,
        turn_situation=turn_situation,
    )
    result = validate_conductor_result(decision, context=context)

    assert result.status == "passed", [issue.code for issue in result.errors]
    assert decision.route == expected_route
    assert decision.template_plan.items[0].template_id == expected_template


@pytest.mark.parametrize(
    ("selected_action", "expected_route", "expected_template"),
    [
        ("send_demo", "product", "product.demo_direct"),
        (
            "answer_product_question_with_saved_context",
            "product",
            "product.how_it_works_direct",
        ),
        (
            "answer_price_objection_with_context",
            "product",
            "product.price_objection_value",
        ),
        (
            "offer_or_join_waitlist_if_eligible",
            "waitlist",
            "waitlist.offer_after_contract_intent",
        ),
    ],
)
def test_compiler_handles_post_diagnostic_followup_actions(
    selected_action: str,
    expected_route: str,
    expected_template: str,
) -> None:
    text = "manda a demo" if selected_action == "send_demo" else "follow-up"
    context = _context(
        text,
        diagnostic_status="completed",
        ledger=_complete_ledger(),
    )
    turn_situation = build_turn_situation(context)
    action = _action_decision(
        context,
        selected_action=selected_action,
        diagnostic_details={},
    )

    decision = compile_action_decision(
        action,
        context=context,
        turn_situation=turn_situation,
    )
    result = validate_conductor_result(decision, context=context)

    assert result.status == "passed"
    assert decision.route == expected_route
    assert decision.template_plan.items[0].template_id == expected_template


@pytest.mark.parametrize(
    ("selected_action", "expected_template", "expected_diagnostic_action"),
    [
        (
            "answer_direct_question_then_continue_diagnostic",
            "product.how_it_works_direct",
            "ask_next",
        ),
        ("ask_next_diagnostic_question", "diagnostic.ask_active_students", "ask_next"),
        (
            "clarify_ambiguous_diagnostic_answer",
            "diagnostic.insufficient_evidence",
            "insufficient_evidence",
        ),
        ("respect_diagnostic_refusal", "product.overview_short", "none"),
    ],
)
def test_compiler_handles_diagnostic_action_matrix(
    selected_action: str,
    expected_template: str,
    expected_diagnostic_action: str,
) -> None:
    context = _context("diagnostic followup", diagnostic_status="in_progress")
    turn_situation = build_turn_situation(context)
    action = _action_decision(
        context,
        selected_action=selected_action,
        intents=[selected_action],
        diagnostic_details={
            "clarification_question": "Pode responder com uma estimativa de alunos ativos?"
        },
    )

    decision = compile_action_decision(
        action,
        context=context,
        turn_situation=turn_situation,
    )
    result = validate_conductor_result(decision, context=context)

    assert result.status == "passed", [issue.code for issue in result.errors]
    assert decision.route in {"diagnostic", "product"}
    assert decision.template_plan.items[0].template_id == expected_template
    assert decision.diagnostic.action == expected_diagnostic_action


def test_compiler_completes_diagnostic_when_all_required_answers_are_already_saved() -> None:
    context = _context(
        "pode fechar",
        diagnostic_status="in_progress",
        ledger=_complete_ledger(),
    )
    turn_situation = build_turn_situation(context)
    assert turn_situation.mode == "post_diagnostic"
    action = _action_decision(
        context,
        selected_action="complete_diagnostic",
        diagnostic_details={
            "pain_context_human": "O studio ja trouxe contexto suficiente para uma leitura.",
            "crm_base_recommendation": "Organizar a base ajuda a priorizar proximos passos.",
            "operational_first_step": "Separar pendencias do dia antes de automatizar.",
            "agent_pain_resolved": "tarefas sem dono claro",
            "agent_practical_action": "organiza retornos e prioridades",
        },
    )
    turn_situation.allowed_actions.append("complete_diagnostic")

    decision = compile_action_decision(
        action,
        context=context,
        turn_situation=turn_situation,
    )
    result = validate_conductor_result(decision, context=context)

    assert result.status == "passed", [issue.code for issue in result.errors]
    assert decision.diagnostic.action == "complete"
    assert decision.template_plan.chunk_policy == "staged_diagnostic"


@pytest.mark.parametrize(
    ("selected_action", "expected_status", "expected_template"),
    [
        ("offer_waitlist", "offered", "waitlist.offer_after_contract_intent"),
        ("collect_waitlist_missing_detail", "pending_details", "waitlist.ask_missing_studio"),
        ("decline_waitlist", "declined", "waitlist.status_preserved"),
        (
            "answer_question_then_continue_waitlist",
            "pending_details",
            "product.how_it_works_direct",
        ),
    ],
)
def test_compiler_handles_waitlist_action_matrix(
    selected_action: str,
    expected_status: str,
    expected_template: str,
) -> None:
    context = _context(
        "lista de espera",
        diagnostic_status="completed",
        ledger=_complete_ledger(),
    )
    context.waitlist_state["status"] = "offered"
    context.waitlist_state["missing_details"] = ["studio_name", "city_state"]
    turn_situation = build_turn_situation(context)
    action = _action_decision(
        context,
        selected_action=selected_action,
        intents=["waitlist_request"],
        waitlist_details={
            "context_summary": "O lead ja demonstrou interesse comercial claro.",
            "missing_details": ["studio_name", "city_state"],
        },
    )

    decision = compile_action_decision(
        action,
        context=context,
        turn_situation=turn_situation,
    )
    result = validate_conductor_result(decision, context=context)

    assert result.status == "passed", [issue.code for issue in result.errors]
    assert decision.route == "waitlist"
    assert decision.waitlist.status == expected_status
    assert decision.template_plan.items[0].template_id == expected_template


def test_compiler_joins_waitlist_only_with_real_studio_details() -> None:
    context = _context(
        "Studio Flow, Campinas SP",
        diagnostic_status="completed",
        ledger=_complete_ledger(),
    )
    context.waitlist_state["status"] = "pending_details"
    context.waitlist_state["missing_details"] = ["studio_name", "city_state"]
    turn_situation = build_turn_situation(context)
    action = _action_decision(
        context,
        selected_action="join_waitlist",
        intents=["waitlist_request"],
        captured_slots=[
            {
                "key": "studio_name",
                "value": "Studio Flow",
                "evidence": ["message.latest:Studio Flow"],
                "confidence": "high",
            },
            {
                "key": "city_state",
                "value": "Campinas SP",
                "evidence": ["message.latest:Campinas SP"],
                "confidence": "high",
            },
        ],
    )

    decision = compile_action_decision(
        action,
        context=context,
        turn_situation=turn_situation,
    )
    result = validate_conductor_result(decision, context=context)

    assert result.status == "passed", [issue.code for issue in result.errors]
    assert decision.waitlist.status == "joined"
    assert decision.template_plan.items[0].template_id == "waitlist.joined"


def test_compiler_does_not_read_raw_inbound_text_or_regex_for_commercial_matching() -> None:
    source = inspect.getsource(decision_compiler_module)

    assert "context.inbound.text" not in source
    assert ".inbound.text" not in source
    assert "casefold(" not in source
    assert "lower(" not in source
    assert "import re" not in source
    assert "regex" not in source.lower()
