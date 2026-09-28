"""T012-030C tests: deterministic Decision Compiler."""

from __future__ import annotations

import inspect
import typing

import pytest

from app.core.taliya_commercial.template_registry import TEMPLATE_REGISTRY
from app.core.taliya_commercial_sdk.conductor_decision import (
    ACTION_MENU_BY_MODE,
    ConductorActionDecision,
    TurnAction,
)
from app.core.taliya_commercial_sdk.decision_compiler import (
    compile_action_decision,
)
from app.core.taliya_commercial_sdk.turn_situation import build_turn_situation

PRICE_FACTS = {
    "plan_price_summary": {
        "kind": "long_text",
        "value": "Base R$ 197/mes ate Completo R$ 1.497/mes.",
        "source": "official_product_knowledge",
        "evidence": ["product_knowledge.prices"],
        "max_length": 360,
    },
}
DEMO_FACTS = {
    "official_demo_link": {
        "kind": "url",
        "value": "https://taliya.example/demo",
        "source": "official_product_knowledge",
        "evidence": ["product_knowledge.demo_link"],
    },
}
DELTA_FACTS = {
    "product_fact_summary": {
        "kind": "long_text",
        "value": (
            "Taliya esta em entrada limitada para poucos studios; quando ha "
            "intencao real de comecar, o caminho comercial atual e lista de espera."
        ),
        "source": "official_product_knowledge",
        "evidence": ["product_knowledge.availability_and_onboarding"],
        "max_length": 320,
    },
}
COMPLETION_FACTS = {
    **PRICE_FACTS,
    "recommended_plan_or_range": {
        "kind": "short_text",
        "value": "Essencial (R$ 497/mes)",
        "source": "official_product_knowledge",
        "evidence": ["product_knowledge.plans"],
    },
    "indicated_agents": [
        {
            "agent_name": "Atendimento",
            "agent_pain_resolved": "demora nas conversas",
            "agent_practical_action": "organizar retornos e avisar a equipe",
        }
    ],
}


def _decision(action: str, **overrides) -> ConductorActionDecision:
    payload = {"selected_action": action, "evidence": ["inbound.text"], **overrides}
    return ConductorActionDecision.model_validate(payload)


def _composition(name: str, value: str) -> dict:
    return {"name": name, "value": value, "evidence": ["inbound.text"]}


def test_compiler_signature_has_no_lead_text_parameter() -> None:
    parameters = inspect.signature(compile_action_decision).parameters
    forbidden = {"text", "user_text", "message", "inbound", "lead_text"}
    assert not (forbidden & set(parameters))


def test_answer_price_compiles_with_compiler_owned_official_variable() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "price_question"}, channel="whatsapp"
    )
    compiled = compile_action_decision(
        _decision("answer_price", direct_question="quanto custa?"),
        situation,
        official_facts=PRICE_FACTS,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == ("product.price_direct", "diagnostic.price_hook")
    assert compiled.variables["plan_price_summary"]["source"] == (
        "official_product_knowledge"
    )
    assert compiled.current_state == "price_question"
    assert compiled.next_state == "diagnostic_offered"

    missing = compile_action_decision(
        _decision("answer_price"), situation, official_facts={}
    )
    assert "compile_missing_official_fact:plan_price_summary" in missing.issues


def test_answer_price_with_pain_context_uses_contextual_hook() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "price_question"}, channel="whatsapp"
    )
    compiled = compile_action_decision(
        _decision(
            "answer_price",
            direct_question="queria saber preco",
            composition_variables=[
                _composition(
                    "plan_fit_context",
                    "Como a reposicao esta baguncada, vale comparar plano com contexto.",
                )
            ],
        ),
        situation,
        official_facts=PRICE_FACTS,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == (
        "product.price_direct",
        "diagnostic.price_hook_with_context",
    )
    assert compiled.variables["plan_fit_context"]["source"] == "user_message"


def test_t011_105_regression_action_without_composition_fails() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "pain_detected"}, channel="whatsapp"
    )
    bare = compile_action_decision(
        _decision("offer_diagnostic_from_pain"), situation
    )
    assert "compile_missing_composition:pain_context_human" in bare.issues

    grounded = compile_action_decision(
        _decision(
            "offer_diagnostic_from_pain",
            composition_variables=[
                _composition(
                    "pain_context_human",
                    "Perder interessado porque o WhatsApp atrasa pesa na rotina.",
                )
            ],
        ),
        situation,
    )
    assert grounded.ok, grounded.issues
    assert grounded.template_ids == ("diagnostic.offer_soft",)
    assert grounded.variables["pain_context_human"]["kind"] == "long_text"


def test_pain_first_offer_does_not_start_diagnostic_without_acceptance() -> None:
    situation = build_turn_situation(state_snapshot={}, channel="whatsapp")
    compiled = compile_action_decision(
        _decision(
            "offer_diagnostic_from_pain",
            composition_variables=[
                _composition(
                    "pain_context_human",
                    "A demora no WhatsApp esta esfriando interessados.",
                )
            ],
        ),
        situation,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == ("opening.contextual_ack", "diagnostic.offer_soft")
    assert "diagnostic.ask_active_students" not in compiled.template_ids


def test_widget_diagnostic_acceptance_does_not_repeat_cold_greeting() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "new_lead",
            "channel": "widget",
            "client_has_prior_assistant_messages": True,
        },
        channel="widget",
    )

    compiled = compile_action_decision(
        _decision("start_requested_diagnostic"),
        situation,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == (
        "diagnostic.start",
        "diagnostic.ask_active_students",
    )
    assert "opening.cold_greeting" not in compiled.template_ids


def test_capture_answer_merges_ledger_and_asks_next() -> None:
    snapshot = {
        "canonical_state": "diagnostic_in_progress",
        "diagnostic": {
            "status": "in_progress",
            "ledger": {
                "active_students_or_size": {"status": "answered", "answer_value": "120"}
            },
        },
    }
    situation = build_turn_situation(state_snapshot=snapshot, channel="whatsapp")
    assert situation.pending_question_key == "main_pain"

    compiled = compile_action_decision(
        _decision(
            "capture_pending_diagnostic_answer",
            captured_slots=[
                {
                    "key": "main_pain",
                    "value_text": "perde interessados por demora",
                    "status": "answered",
                    "evidence": ["inbound.text"],
                }
            ],
        ),
        situation,
    )

    assert compiled.ok, compiled.issues
    assert compiled.ledger_updates[0]["question_key"] == "main_pain"
    assert compiled.template_ids == ("diagnostic.ask_pain_detail",)
    assert compiled.variables["answer_feedback"]["value"] == (
        "Entendi. Já dá para ver onde a rotina está pesando mais."
    )
    assert compiled.variables["answer_feedback"]["source"] == "diagnostic_ledger"

    without_slot = compile_action_decision(
        _decision(
            "capture_pending_diagnostic_answer",
        ),
        situation,
    )
    assert any(
        issue.startswith("compile_missing_captured_answer")
        for issue in without_slot.issues
    )


def test_diagnostic_ask_next_cannot_repeat_pending_question_without_capture() -> None:
    snapshot = {
        "canonical_state": "diagnostic_in_progress",
        "diagnostic": {
            "status": "in_progress",
            "ledger": {
                "active_students_or_size": {
                    "status": "answered",
                    "answer_value": "95 alunos",
                },
                "main_pain": {
                    "status": "answered",
                    "answer_value": "WhatsApp e follow-up",
                },
            },
        },
    }
    situation = build_turn_situation(state_snapshot=snapshot, channel="whatsapp")
    assert situation.pending_question_key == "pain_detail"

    compiled = compile_action_decision(
        _decision(
            "ask_next_diagnostic_question",
            composition_variables=[
                _composition(
                    "answer_feedback",
                    "Entendi, hoje falta ver quem precisa de retorno.",
                )
            ],
        ),
        situation,
    )

    assert not compiled.ok
    assert "compile_repeated_pending_question_without_capture" in compiled.issues
    assert compiled.template_ids == ()


def test_complete_diagnostic_derives_full_staged_sequence() -> None:
    ledger = {
        key: {"status": "answered", "answer_value": "x"}
        for key in (
            "active_students_or_size",
            "main_pain",
            "pain_detail",
            "current_process",
            "priority",
        )
    }
    snapshot = {
        "canonical_state": "diagnostic_in_progress",
        "diagnostic": {"status": "in_progress", "ledger": ledger},
    }
    situation = build_turn_situation(state_snapshot=snapshot, channel="whatsapp")
    decision = _decision(
        "complete_diagnostic",
        captured_slots=[
            {
                "key": "urgency",
                "value_text": "resolver agora",
                "status": "answered",
                "evidence": ["inbound.text"],
            }
        ],
        composition_variables=[
            _composition("pain_context_human", "O que pesa e perder interessado."),
            _composition("crm_base_recommendation", "Organizar a base de contatos."),
            _composition("operational_first_step", "Comecar pelo follow-up diario."),
        ],
    )

    compiled = compile_action_decision(
        decision, situation, official_facts=COMPLETION_FACTS
    )

    assert compiled.ok, compiled.issues
    # The contract-mandated staged order, derived by code - the model cannot
    # forget the hold message or deliver a single-template final anymore.
    assert compiled.template_ids == (
        "diagnostic.deliver_hold",
        "diagnostic.deliver_context",
        "diagnostic.deliver_crm_base",
        "diagnostic.deliver_operational_step",
        "diagnostic.deliver_agent_recommendation",
        "diagnostic.deliver_plan_recommendation",
        "diagnostic.deliver_demo_not_offered",
    )
    assert compiled.chunk_policy == "staged_diagnostic"
    assert compiled.next_state == "diagnostic_delivered"
    assert compiled.variables["recommended_plan_or_range"]["source"] == (
        "official_product_knowledge"
    )

    # Demo already offered -> the other demo bridge.
    snapshot_with_demo = {**snapshot, "demo": {"status": "offered"}}
    situation2 = build_turn_situation(
        state_snapshot=snapshot_with_demo, channel="whatsapp"
    )
    compiled2 = compile_action_decision(
        decision, situation2, official_facts=COMPLETION_FACTS
    )
    assert compiled2.template_ids[-1] == "diagnostic.deliver_demo_already_offered"

    # Premature completion is caught even here (defense in depth).
    early_snapshot = {
        "canonical_state": "diagnostic_in_progress",
        "diagnostic": {
            "status": "in_progress",
            "ledger": {"active_students_or_size": {"status": "answered"}},
        },
    }
    early = compile_action_decision(
        decision,
        build_turn_situation(state_snapshot=early_snapshot, channel="whatsapp"),
        official_facts=COMPLETION_FACTS,
    )
    assert any(
        issue.startswith("compile_completion_with_missing_keys")
        for issue in early.issues
    )


def test_handoff_compiles_pause_patch_and_requires_reason() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "general_interest"}, channel="whatsapp"
    )
    compiled = compile_action_decision(
        _decision(
            "handoff_requested",
            handoff_intent="requested",
            composition_variables=[
                _composition("handoff_reason", "pediu para falar com uma pessoa")
            ],
        ),
        situation,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == ("handoff.acknowledge",)
    assert compiled.state_patch["handoff"] == {"status": "requested", "pause_ai": True}
    assert compiled.sales_inbox_projection["handoff_status"] == "requested"


def test_delta_contract_compiles_how_it_works_with_state_next_step() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "product_question"}, channel="whatsapp"
    )
    compiled = compile_action_decision(
        _decision(
            "answer_how_it_works",
            direct_question="como funciona?",
            product_fact_keys_used=["how_it_works", "routine_areas"],
        ),
        situation,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == ("product.how_it_works_direct",)
    assert compiled.variables["contextual_next_step"]["value"] == (
        "diagnostic_offer_generic"
    )


def test_delta_contract_compiles_comparison_only_with_lead_context() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "product_question"}, channel="whatsapp"
    )
    missing_context = compile_action_decision(
        _decision(
            "answer_comparison_current_tool",
            direct_question="uso planilha hoje, qual a diferenca?",
            interpreted_intents=["comparison_current_tool"],
            product_fact_keys_used=["comparison_spreadsheet"],
        ),
        situation,
    )

    assert (
        "compile_missing_template_variable:"
        "product.comparison_current_tool:current_tool_context"
    ) in missing_context.issues

    grounded = compile_action_decision(
        _decision(
            "answer_comparison_current_tool",
            direct_question="uso planilha hoje, qual a diferenca?",
            interpreted_intents=["comparison_current_tool"],
            product_fact_keys_used=["comparison_spreadsheet"],
            composition_variables=[
                _composition("current_tool_context", "planilha e WhatsApp manual")
            ],
        ),
        situation,
    )

    assert grounded.ok, grounded.issues
    assert grounded.template_ids == ("product.comparison_current_tool",)
    assert grounded.variables["current_tool_context"]["source"] == "user_message"


def test_delta_contract_compiles_security_and_integration_safe_templates() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "product_question"}, channel="whatsapp"
    )
    security = compile_action_decision(
        _decision(
            "answer_security_and_data",
            direct_question="e seguro? tem LGPD?",
            interpreted_intents=["trust_security_question"],
            product_fact_keys_used=["security_and_data"],
        ),
        situation,
    )
    integration = compile_action_decision(
        _decision(
            "answer_integration_scope_safely",
            direct_question="integra com Instagram?",
            interpreted_intents=["integration_scope_question"],
            product_fact_keys_used=["integration_scope"],
            composition_variables=[
                _composition("integration_topic", "integracao com Instagram")
            ],
        ),
        situation,
    )

    assert security.ok, security.issues
    assert security.template_ids == ("product.security_data_direct",)
    assert integration.ok, integration.issues
    assert integration.template_ids == ("product.integration_scope_direct",)
    assert integration.variables["integration_topic"]["value"] == (
        "integracao com Instagram"
    )


def test_delta_contract_compiles_availability_without_checkout_or_date_promise() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "product_question"}, channel="whatsapp"
    )
    compiled = compile_action_decision(
        _decision(
            "answer_availability_and_onboarding",
            direct_question="quando posso comecar?",
            interpreted_intents=["availability_question"],
            product_fact_keys_used=["availability_and_onboarding"],
        ),
        situation,
        official_facts=DELTA_FACTS,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == ("product.overview_short",)
    assert compiled.variables["product_fact_summary"]["evidence"] == [
        "product_knowledge.availability_and_onboarding"
    ]
    rendered_source = compiled.variables["product_fact_summary"]["value"].casefold()
    assert "checkout" not in rendered_source
    assert "desconto" not in rendered_source
    assert "data" not in rendered_source


def test_delta_contract_compiles_out_of_profile_without_diagnostic_offer() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "product_question"}, channel="whatsapp"
    )
    compiled = compile_action_decision(
        _decision(
            "answer_out_of_profile",
            direct_question="sou aluno, isso serve pra mim?",
            interpreted_intents=["out_of_profile"],
            product_fact_keys_used=["out_of_profile"],
        ),
        situation,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == ("product.out_of_profile_redirect",)
    assert not any(template.startswith("diagnostic.") for template in compiled.template_ids)


def test_038b_fixture_correction_replaces_previous_diagnostic_number() -> None:
    snapshot = {
        "canonical_state": "diagnostic_in_progress",
        "diagnostic": {"status": "in_progress", "ledger": {}},
    }
    situation = build_turn_situation(state_snapshot=snapshot, channel="whatsapp")
    compiled = compile_action_decision(
        _decision(
            "capture_pending_diagnostic_answer",
            captured_slots=[
                {
                    "key": "active_students_or_size",
                    "value_text": "80",
                    "status": "answered",
                    "evidence": ["inbound.text"],
                }
            ],
            composition_variables=[
                _composition(
                    "answer_feedback",
                    "Entendi: corrigindo para 80 alunos, nao 120.",
                )
            ],
        ),
        situation,
    )

    assert compiled.ok, compiled.issues
    assert compiled.ledger_updates == (
        {
            "question_key": "active_students_or_size",
            "status": "answered",
            "answer_value": "80",
            "evidence": ["inbound.text"],
        },
    )
    assert compiled.template_ids == ("diagnostic.ask_main_pain",)


def test_038b_fixture_multiple_diagnostic_answers_in_one_message() -> None:
    snapshot = {
        "canonical_state": "diagnostic_in_progress",
        "diagnostic": {"status": "in_progress", "ledger": {}},
    }
    situation = build_turn_situation(state_snapshot=snapshot, channel="whatsapp")
    compiled = compile_action_decision(
        _decision(
            "capture_pending_diagnostic_answer",
            captured_slots=[
                {
                    "key": "active_students_or_size",
                    "value_text": "80",
                    "status": "answered",
                    "evidence": ["inbound.text"],
                },
                {
                    "key": "main_pain",
                    "value_text": "demora para responder interessados",
                    "status": "answered",
                    "evidence": ["inbound.text"],
                },
            ],
            composition_variables=[
                _composition(
                    "answer_feedback",
                    "Entendi: 80 alunos e gargalo no retorno aos interessados.",
                )
            ],
        ),
        situation,
    )

    assert compiled.ok, compiled.issues
    assert [item["question_key"] for item in compiled.ledger_updates] == [
        "active_students_or_size",
        "main_pain",
    ]
    assert compiled.template_ids == ("diagnostic.ask_pain_detail",)


def test_038b_fixture_messy_price_interruption_answers_then_resumes_diagnostic() -> None:
    snapshot = {
        "canonical_state": "diagnostic_in_progress",
        "diagnostic": {
            "status": "in_progress",
            "ledger": {
                "active_students_or_size": {
                    "status": "answered",
                    "answer_value": "80",
                }
            },
        },
    }
    situation = build_turn_situation(state_snapshot=snapshot, channel="whatsapp")
    compiled = compile_action_decision(
        _decision(
            "answer_direct_question_then_continue_diagnostic",
            direct_question="qto fica?",
            interpreted_intents=["price"],
            product_fact_keys_used=["prices"],
        ),
        situation,
        official_facts=PRICE_FACTS,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == (
        "product.price_direct",
        "diagnostic.ask_main_pain",
    )
    assert compiled.variables["plan_price_summary"]["source"] == (
        "official_product_knowledge"
    )


def test_038b_fixture_messy_demo_request_uses_official_demo_link() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "product_question"}, channel="whatsapp"
    )
    compiled = compile_action_decision(
        _decision(
            "send_demo",
            direct_question="tem como ver ai mn",
            interpreted_intents=["demo"],
            product_fact_keys_used=["demo_link"],
        ),
        situation,
        official_facts=DEMO_FACTS,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == ("product.demo_direct",)
    assert compiled.state_patch["demo"] == {"status": "offered"}
    assert compiled.variables["official_demo_link"]["evidence"] == [
        "product_knowledge.demo_link"
    ]


def test_038b_fixture_price_objection_mid_diagnostic_answers_then_resumes() -> None:
    snapshot = {
        "canonical_state": "diagnostic_in_progress",
        "diagnostic": {
            "status": "in_progress",
            "ledger": {
                "active_students_or_size": {
                    "status": "answered",
                    "answer_value": "80",
                },
                "main_pain": {
                    "status": "answered",
                    "answer_value": "demora para responder interessados",
                },
            },
        },
    }
    situation = build_turn_situation(state_snapshot=snapshot, channel="whatsapp")
    compiled = compile_action_decision(
        _decision(
            "answer_direct_question_then_continue_diagnostic",
            direct_question="achei caro, nao sei se compensa",
            interpreted_intents=["price_objection"],
        ),
        situation,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == (
        "product.price_objection_value",
        "diagnostic.ask_pain_detail",
    )
    assert compiled.next_state == "diagnostic_waiting_answer"


@pytest.mark.parametrize(
    (
        "direct_question",
        "interpreted_intents",
        "product_fact_keys_used",
        "composition_variables",
        "official_facts",
        "expected_template",
    ),
    [
        (
            "mas como funciona isso na pratica?",
            ["product_how_it_works"],
            ["how_it_works"],
            [],
            {},
            "product.how_it_works_direct",
        ),
        (
            "integra com meu sistema ai?",
            ["integration_scope_question"],
            ["integration_scope"],
            [_composition("integration_topic", "meu sistema atual")],
            {},
            "product.integration_scope_direct",
        ),
        (
            "e seguro mandar dados dos alunos?",
            ["trust_security_question"],
            ["security_and_data"],
            [],
            {},
            "product.security_data_direct",
        ),
        (
            "tem vaga pra entrar agora ou checkout?",
            ["availability_question"],
            ["availability_and_onboarding"],
            [],
            DELTA_FACTS,
            "product.overview_short",
        ),
        (
            "sou aluno, serve pra mim?",
            ["out_of_profile"],
            ["out_of_profile"],
            [],
            {},
            "product.out_of_profile_redirect",
        ),
        (
            "uso planilha, isso troca tudo?",
            ["comparison_current_tool"],
            ["comparison_spreadsheet"],
            [_composition("current_tool_context", "planilha")],
            {},
            "product.comparison_current_tool",
        ),
    ],
)
def test_038b_interruption_matrix_answers_product_question_then_resumes_diagnostic(
    direct_question: str,
    interpreted_intents: list[str],
    product_fact_keys_used: list[str],
    composition_variables: list[dict],
    official_facts: dict,
    expected_template: str,
) -> None:
    snapshot = {
        "canonical_state": "diagnostic_in_progress",
        "diagnostic": {
            "status": "in_progress",
            "ledger": {
                "active_students_or_size": {
                    "status": "answered",
                    "answer_value": "80",
                }
            },
        },
    }
    situation = build_turn_situation(state_snapshot=snapshot, channel="whatsapp")
    compiled = compile_action_decision(
        _decision(
            "answer_direct_question_then_continue_diagnostic",
            direct_question=direct_question,
            interpreted_intents=interpreted_intents,
            product_fact_keys_used=product_fact_keys_used,
            composition_variables=composition_variables,
        ),
        situation,
        official_facts=official_facts,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == (expected_template, "diagnostic.ask_main_pain")
    assert compiled.next_state == "diagnostic_waiting_answer"


def test_038b_fixture_resume_after_days_uses_post_diagnostic_memory() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "diagnostic_delivered",
            "summary": "Lead voltou depois de alguns dias.",
            "diagnostic": {
                "status": "completed",
                "pain_context_human": "interessados ficam sem retorno claro",
                "first_recommended_step": "organizar atendimento e follow-up",
                "recommended_plan_or_range": "Essencial",
            },
            "demo": {"status": "offered"},
        },
        channel="whatsapp",
    )
    compiled = compile_action_decision(
        _decision(
            "answer_product_question_with_saved_context",
            direct_question="pode continuar de onde parou?",
            interpreted_intents=["conversation_resume", "product_how_it_works"],
            product_fact_keys_used=["how_it_works"],
        ),
        situation,
    )

    assert compiled.ok, compiled.issues
    assert situation.post_diagnostic_context["first_recommended_step"] == (
        "organizar atendimento e follow-up"
    )
    assert compiled.template_ids == ("product.how_it_works_direct",)
    assert not any(template.startswith("diagnostic.ask_") for template in compiled.template_ids)
    assert compiled.next_state == "post_diagnostic_questions"


def test_032b_post_diagnostic_price_resume_does_not_restart_diagnostic() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "diagnostic_delivered",
            "summary": "Lead voltou depois de alguns dias perguntando valor.",
            "diagnostic": {
                "status": "completed",
                "pain_context_human": "interessados ficam sem retorno claro",
                "first_recommended_step": "organizar atendimento e follow-up",
                "recommended_plan_or_range": "Essencial",
            },
        },
        channel="whatsapp",
    )
    compiled = compile_action_decision(
        _decision(
            "answer_product_question_with_saved_context",
            direct_question="qto ficava msm?",
            interpreted_intents=["conversation_resume", "price"],
            product_fact_keys_used=["prices"],
        ),
        situation,
        official_facts=PRICE_FACTS,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == ("product.price_direct",)
    assert compiled.variables["plan_price_summary"]["source"] == (
        "official_product_knowledge"
    )
    assert not any(
        template.startswith("diagnostic.") for template in compiled.template_ids
    )
    assert compiled.next_state == "post_diagnostic_questions"


def test_038b_fixture_waitlist_resume_answers_question_then_missing_studio() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "waitlist_pending_data",
            "waitlist": {"status": "pending_data", "missing_details": ["studio_name"]},
        },
        channel="whatsapp",
    )
    compiled = compile_action_decision(
        _decision(
            "answer_question_then_continue_waitlist",
            direct_question="qual era o valor mesmo?",
            interpreted_intents=["conversation_resume", "price"],
            product_fact_keys_used=["prices"],
        ),
        situation,
        official_facts=PRICE_FACTS,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == (
        "product.price_direct",
        "waitlist.ask_missing_studio",
    )
    assert compiled.variables["plan_price_summary"]["source"] == (
        "official_product_knowledge"
    )


def test_043_waitlist_availability_question_uses_waitlist_path_template() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "waitlist_offered",
            "waitlist": {"status": "offered", "missing_details": ["contact_path"]},
            "diagnostic": {"status": "delivered", "ledger": {}},
        },
        channel="whatsapp",
    )
    compiled = compile_action_decision(
        _decision(
            "answer_question_then_continue_waitlist",
            direct_question="como funciona mesmo?",
            interpreted_intents=["waitlist_curiosity"],
            product_fact_keys_used=["availability_and_onboarding"],
            waitlist_intent="accepts",
        ),
        situation,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == (
        "waitlist.current_path_explained",
        "waitlist.ask_missing_contact_path",
    )
    assert "product.overview_short" not in compiled.template_ids


def test_043_waitlist_question_without_fact_key_uses_answer_feedback() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "waitlist_offered",
            "waitlist": {"status": "offered", "missing_details": ["contact_path"]},
            "diagnostic": {"status": "delivered", "ledger": {}},
        },
        channel="whatsapp",
    )
    compiled = compile_action_decision(
        _decision(
            "answer_question_then_continue_waitlist",
            direct_question="como funciona mesmo?",
            interpreted_intents=["waitlist_curiosity"],
            composition_variables=[
                _composition(
                    "answer_feedback",
                    "Funciona por uma lista de entrada para poucos studios agora.",
                )
            ],
            waitlist_intent="accepts",
        ),
        situation,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == (
        "waitlist.answer_question",
        "waitlist.ask_missing_contact_path",
    )
    assert (
        compiled.variables["answer_feedback"]["value"]
        == "Funciona por uma lista de entrada para poucos studios agora."
    )


def test_043_whatsapp_scope_uses_fixed_public_copy_and_demo_link_only() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "product_question"},
        channel="whatsapp",
    )
    compiled = compile_action_decision(
        _decision(
            "answer_whatsapp_scope",
            direct_question="o aluno precisa baixar app?",
            interpreted_intents=["whatsapp_scope"],
            product_fact_keys_used=["whatsapp_scope"],
        ),
        situation,
        official_facts={
            **DEMO_FACTS,
            "product_fact_summary": {
                "kind": "long_text",
                "value": "Nao prometa WhatsApp Business interno.",
                "source": "official_product_knowledge",
                "evidence": ["product_knowledge.whatsapp_scope"],
            },
        },
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == ("product.whatsapp_direct",)
    assert compiled.current_state == "product_question"
    assert compiled.next_state == "product_question"
    assert "product_fact_summary" not in compiled.variables
    assert compiled.variables["official_demo_link"]["value"] == "https://taliya.example/demo"


def test_specific_whatsapp_fact_suppresses_redundant_generic_product_answer() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "new_lead"},
        channel="widget",
    )
    compiled = compile_action_decision(
        _decision(
            "answer_direct_product_question",
            direct_question="como funciona no WhatsApp?",
            interpreted_intents=["whatsapp_scope"],
            product_fact_keys_used=["whatsapp_scope", "how_it_works"],
        ),
        situation,
        official_facts=DEMO_FACTS,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == ("product.whatsapp_direct",)
    assert compiled.current_state == "product_question"
    assert compiled.next_state == "product_question"


def test_043_waitlist_context_summary_is_clamped_to_registry_limit() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "diagnostic_delivered",
            "diagnostic": {"status": "delivered", "ledger": {}},
        },
        channel="whatsapp",
    )
    long_summary = (
        "A lead viu a demonstracao, avaliou o valor, quer comecar agora, "
        "entendeu que a rotina de vendas e follow-up precisa de organizacao, "
        "e quer entrar na lista para a equipe seguir com o proximo passo sem "
        "promessa de vaga imediata, data, desconto ou condicao especial."
    )

    compiled = compile_action_decision(
        _decision(
            "offer_or_join_waitlist_if_eligible",
            interpreted_intents=["contract_intent"],
            waitlist_intent="contract_intent",
            composition_variables=[
                _composition("waitlist_context_summary", long_summary)
            ],
        ),
        situation,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == ("waitlist.offer_after_contract_intent",)
    assert "waitlist_context_summary" not in compiled.variables


def test_038b_fixture_demo_resume_after_days_does_not_restart_diagnostic() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "diagnostic_delivered",
            "summary": "Lead voltou depois de alguns dias pedindo demo.",
            "diagnostic": {
                "status": "completed",
                "first_recommended_step": "organizar atendimento e follow-up",
                "recommended_plan_or_range": "Essencial",
            },
            "demo": {"status": "offered"},
        },
        channel="whatsapp",
    )
    compiled = compile_action_decision(
        _decision(
            "send_demo",
            direct_question="me manda a demo de novo",
            interpreted_intents=["conversation_resume", "demo"],
            product_fact_keys_used=["demo_link"],
        ),
        situation,
        official_facts=DEMO_FACTS,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == ("product.demo_direct",)
    assert compiled.state_patch["demo"] == {"status": "offered"}
    assert not any(template.startswith("diagnostic.") for template in compiled.template_ids)


def test_032b_diagnostic_refusal_answers_price_without_reoffering_diagnostic() -> None:
    snapshot = {
        "canonical_state": "diagnostic_in_progress",
        "diagnostic": {
            "status": "in_progress",
            "ledger": {
                "active_students_or_size": {
                    "status": "answered",
                    "answer_value": "80",
                }
            },
        },
    }
    situation = build_turn_situation(state_snapshot=snapshot, channel="whatsapp")
    compiled = compile_action_decision(
        _decision(
            "respect_diagnostic_refusal",
            direct_question="so me fala o preco",
            interpreted_intents=["diagnostic_refusal", "price"],
            diagnostic_intent="refusal",
            product_fact_keys_used=["prices"],
        ),
        situation,
        official_facts=PRICE_FACTS,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == ("product.price_direct",)
    assert "diagnostic.price_hook" not in compiled.template_ids
    assert not any(template.startswith("diagnostic.") for template in compiled.template_ids)


def test_032b_reliable_profile_name_personalizes_cold_greeting_only() -> None:
    reliable = build_turn_situation(
        state_snapshot={
            "canonical_state": "new_lead",
            "channel_metadata": {"profile_name": "Lucas Alves"},
        },
        channel="whatsapp",
    )
    unreliable = build_turn_situation(
        state_snapshot={
            "canonical_state": "new_lead",
            "channel_metadata": {"profile_name": "Studio Vida Pilates"},
        },
        channel="whatsapp",
    )

    reliable_compiled = compile_action_decision(
        _decision("answer_general_interest"),
        reliable,
    )
    unreliable_compiled = compile_action_decision(
        _decision("answer_general_interest"),
        unreliable,
    )

    assert reliable_compiled.ok, reliable_compiled.issues
    assert reliable_compiled.template_ids == ("opening.cold_greeting_named",)
    assert reliable_compiled.variables["first_name"]["value"] == "Lucas"
    assert unreliable_compiled.ok, unreliable_compiled.issues
    assert unreliable_compiled.template_ids == ("opening.cold_greeting",)
    assert "first_name" not in unreliable_compiled.variables


def test_032b_reliable_profile_name_personalizes_diagnostic_start() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "diagnostic_offered",
            "channel_metadata": {"profile_name": "Mariana Costa"},
        },
        channel="whatsapp",
    )
    compiled = compile_action_decision(
        _decision("start_requested_diagnostic"),
        situation,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == (
        "diagnostic.start_named",
        "diagnostic.ask_active_students",
    )
    assert compiled.variables["first_name"]["value"] == "Mariana"


def test_032b_diagnostic_acceptance_starts_without_name_question() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "diagnostic_offered"},
        channel="whatsapp",
    )
    compiled = compile_action_decision(
        _decision("start_requested_diagnostic"),
        situation,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == (
        "diagnostic.start",
        "diagnostic.ask_active_students",
    )
    assert compiled.next_state == "diagnostic_waiting_answer"
    assert compiled.state_patch == {"diagnostic": {"status": "in_progress"}}
    assert "first_name" not in compiled.variables


def test_032b_diagnostic_start_still_works_after_name_was_skipped() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "diagnostic_offered",
            "diagnostic": {"status": "name_requested"},
        },
        channel="whatsapp",
    )
    compiled = compile_action_decision(
        _decision("start_requested_diagnostic"),
        situation,
    )

    assert compiled.ok, compiled.issues
    assert compiled.template_ids == (
        "diagnostic.start",
        "diagnostic.ask_active_students",
    )
    assert "first_name" not in compiled.variables


def test_every_turn_action_is_explicitly_compiled() -> None:
    """011 quality gate: no pending-action bucket."""

    ledger = {
        key: {"status": "answered", "answer_value": "x"}
        for key in (
            "active_students_or_size",
            "main_pain",
            "pain_detail",
            "current_process",
            "priority",
        )
    }
    rich_snapshot = {
        "diagnostic": {"status": "in_progress", "ledger": ledger},
        "waitlist": {"status": "offered", "missing_details": ["studio_name"]},
    }
    generic_compositions = [
        _composition("pain_context_human", "dor concreta do lead"),
        _composition("crm_base_recommendation", "organizar a base"),
        _composition("operational_first_step", "comecar pelo follow-up"),
        _composition("answer_feedback", "entendi sua resposta"),
        _composition("handoff_reason", "pediu humano"),
        _composition("clarification_question", "Pode me dizer um pouco mais?"),
    ]
    slot = [
        {
            "key": "urgency",
            "value_text": "agora",
            "status": "answered",
            "evidence": ["e"],
        }
    ]

    for action in typing.get_args(TurnAction):
        mode = next(
            mode_name
            for mode_name, menu in ACTION_MENU_BY_MODE.items()
            if action in menu
        )
        situation = build_turn_situation(
            state_snapshot=rich_snapshot, channel="whatsapp"
        )
        # Force the menu context for the action under test.
        situation = type(situation)(
            **{
                **situation.__dict__,
                "mode": mode,
                "allowed_actions": ACTION_MENU_BY_MODE[mode],
                "eligible_template_groups": ("",),  # accept any family here
            }
        )
        compiled = compile_action_decision(
            _decision(
                action,
                captured_slots=slot,
                composition_variables=generic_compositions,
            ),
            situation,
            official_facts=COMPLETION_FACTS,
        )
        assert not any(
            issue.startswith("compile_unmapped_action") for issue in compiled.issues
        ), action
        for template_id in compiled.template_ids:
            assert template_id in TEMPLATE_REGISTRY, (action, template_id)


def test_template_group_boundary_flags_out_of_mode_templates() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "human_requested", "human_status": "requested"},
        channel="whatsapp",
    )
    assert situation.mode == "handoff"
    compiled = compile_action_decision(
        _decision(
            "pause_for_human",
            composition_variables=[_composition("handoff_reason", "pediu humano")],
        ),
        situation,
    )
    assert compiled.ok, compiled.issues

    # An action whose templates fall outside the mode's groups is flagged.
    foreign = compile_action_decision(
        _decision("answer_price"), situation, official_facts=PRICE_FACTS
    )
    assert "conductor_action_not_in_allowed_menu" in foreign.issues
