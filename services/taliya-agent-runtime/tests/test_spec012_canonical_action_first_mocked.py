from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from app.core.taliya_commercial_sdk.action_turn_runner import run_action_conversation
from app.core.taliya_commercial_sdk.conductor_decision import ConductorActionDecision
from tests.test_spec012_sdk_paid_harness_dry_run import (
    ScriptedFakeModel,
    _function_call,
    _message,
)

ROOT = Path(__file__).resolve().parents[3]
SPEC012_DIR = ROOT / "specs" / "012-taliya-commercial-agent-agents-sdk-migration"
FIXTURE_DIR = ROOT / "scripts" / "fixtures" / "agent-runtime"


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _canonical_ids(section: str) -> set[str]:
    fixture_map = _json(SPEC012_DIR / "canonical-fixture-map.json")
    return {str(item["id"]) for item in fixture_map[section]}


def _fixture_messages(source: str, fixture_id: str) -> list[str]:
    fixtures = _json(FIXTURE_DIR / source)
    for item in fixtures:
        if item["id"] == fixture_id:
            return list(item["messages"])
    raise AssertionError(f"fixture not found: {fixture_id}")


def _decision_json(action: str, **overrides: Any) -> str:
    payload = {"selected_action": action, "evidence": ["inbound.text"], **overrides}
    return ConductorActionDecision.model_validate(payload).model_dump_json()


COMPLETION_FACTS = {
    "plan_price_summary": {
        "kind": "long_text",
        "value": (
            "Base R$ 197/mes. Essencial R$ 497/mes. Avance R$ 897/mes. "
            "Completo R$ 1.497/mes."
        ),
        "source": "official_product_knowledge",
        "evidence": ["product_knowledge.plans"],
        "max_length": 360,
    },
    "recommended_plan_or_range": {
        "kind": "short_text",
        "value": "Essencial (R$ 497/mes)",
        "source": "official_product_knowledge",
        "evidence": ["product_knowledge.plans"],
    },
    "indicated_agents": [
        {
            "agent_name": "Atendimento",
            "agent_pain_resolved": "interessados sem retorno no WhatsApp",
            "agent_practical_action": "organizar retornos e avisar a equipe",
        }
    ],
    "product_fact_summary": {
        "kind": "long_text",
        "value": (
            "A Taliya ajuda o studio a organizar atendimento, agenda, "
            "reposicoes, cobrancas, vendas e acompanhamento em um so lugar."
        ),
        "source": "official_product_knowledge",
        "evidence": ["product_knowledge.how_it_works"],
        "max_length": 320,
    },
}


def _feedback(value: str) -> list[dict[str, Any]]:
    return [{"name": "answer_feedback", "value": value, "evidence": ["inbound.text"]}]


@pytest.mark.asyncio
async def test_t012_038_mocked_canonical_price_first_runs_action_pipeline() -> None:
    fixture_id = "final-price-first"
    assert fixture_id in _canonical_ids("golden")

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_direct_product_question",
                        direct_question="quanto custa?",
                        product_fact_keys_used=["prices"],
                        interpreted_intents=["price_question"],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        _fixture_messages("spec-011-golden-transcripts.json", fixture_id),
        model=fake_model,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.mode == "entry"
    assert turn.selected_action == "answer_direct_product_question"
    assert turn.template_ids == ("product.price_direct", "diagnostic.price_hook")
    assert report.total_cost_usd == 0
    assert fake_model.calls == 2
    for price in ("R$ 197", "R$ 497", "R$ 897", "R$ 1.497"):
        assert price in rendered
    assert "checkout" not in rendered.lower()
    assert "link de pagamento" not in rendered.lower()
    assert report.final_state["answered_obligations"] == ["quanto custa?"]


@pytest.mark.asyncio
async def test_t012_038_mocked_canonical_price_plus_pain_uses_context_hook() -> None:
    fixture_id = "final-price-plus-pain"
    assert fixture_id in _canonical_ids("golden")

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_direct_product_question",
                        direct_question="queria saber preco",
                        interpreted_intents=[
                            "price_question",
                            "pain_description",
                        ],
                        product_fact_keys_used=["prices"],
                        composition_variables=[
                            {
                                "name": "plan_fit_context",
                                "value": (
                                    "Essa reposicao baguncada na agenda costuma "
                                    "pedir uma olhada no processo antes de "
                                    "escolher plano."
                                ),
                                "evidence": ["inbound.text"],
                            }
                        ],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        _fixture_messages("spec-011-golden-transcripts.json", fixture_id),
        model=fake_model,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.selected_action == "answer_direct_product_question"
    assert turn.template_ids == (
        "product.price_direct",
        "diagnostic.price_hook_with_context",
    )
    assert "R$ 497" in rendered
    assert "Como você já trouxe um ponto da rotina que está te incomodando" in rendered
    assert "diagnóstico gratuito" in rendered
    assert "497 alunos" not in rendered
    assert "checkout" not in rendered.lower()
    assert "lista vip" not in rendered.lower()
    assert report.total_cost_usd == 0
    assert fake_model.calls == 2


@pytest.mark.asyncio
async def test_t012_038_mocked_canonical_pain_first_offers_before_starting_diagnostic() -> None:
    fixture_id = "final-pain-first"
    assert fixture_id in _canonical_ids("golden")

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_entry_agent")],
            [
                _message(
                    _decision_json(
                        "offer_diagnostic_from_pain",
                        interpreted_intents=["pain_description"],
                        composition_variables=[
                            {
                                "name": "pain_context_human",
                                "value": (
                                    "A demora no WhatsApp esta fazendo "
                                    "interessados escaparem antes do "
                                    "atendimento engrenar."
                                ),
                                "evidence": ["inbound.text"],
                            }
                        ],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        _fixture_messages("spec-011-golden-transcripts.json", fixture_id),
        model=fake_model,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.selected_action == "offer_diagnostic_from_pain"
    assert turn.template_ids == (
        "opening.contextual_ack",
        "diagnostic.offer_soft",
    )
    assert "diagnóstico gratuito" in rendered
    assert "interessados" in rendered
    assert "O que você acha?" in rendered
    assert "alunos ativos" not in rendered
    assert "clientes" not in rendered.lower()
    assert "consumidores" not in rendered.lower()
    assert report.total_cost_usd == 0
    assert fake_model.calls == 2


@pytest.mark.asyncio
async def test_t012_038_mocked_canonical_instagram_source_opening() -> None:
    fixture_id = "final-instagram-interest"
    assert fixture_id in _canonical_ids("golden")

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_entry_agent")],
            [
                _message(
                    _decision_json(
                        "answer_source_opening",
                        interpreted_intents=["source_opening", "general_interest"],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        _fixture_messages("spec-011-golden-transcripts.json", fixture_id),
        model=fake_model,
        initial_state={"source": "instagram"},
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.selected_action == "answer_source_opening"
    assert turn.template_ids == ("opening.instagram_source",)
    assert "studio" in rendered
    assert "Legal voce vir por aqui" not in rendered
    assert "entender por onde comecar" not in rendered
    assert "rotina" in rendered
    assert "gargalos" in rendered
    assert "prioridade" in rendered
    assert "utm_source" not in rendered
    assert "source_label" not in rendered
    assert "lead came from the site" not in rendered
    assert report.final_state["canonical_state"] == "general_interest"
    assert report.total_cost_usd == 0
    assert fake_model.calls == 2


@pytest.mark.asyncio
async def test_t012_038_mocked_canonical_whatsapp_question_uses_scope() -> None:
    fixture_id = "final-whatsapp-question"
    assert fixture_id in _canonical_ids("golden")

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_whatsapp_scope",
                        direct_question="como funciona no WhatsApp?",
                        product_fact_keys_used=["whatsapp_scope", "demo_link"],
                        interpreted_intents=["whatsapp_scope"],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        _fixture_messages("spec-011-golden-transcripts.json", fixture_id),
        model=fake_model,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.selected_action == "answer_whatsapp_scope"
    assert turn.template_ids == ("product.whatsapp_direct",)
    assert "WhatsApp" in rendered
    assert "aluno" in rendered
    assert "baixar aplicativo" in rendered
    assert "criar senha" in rendered
    assert "atualiza o painel" in rendered
    assert "avisa o responsável" in rendered
    assert "/pilates/planos/demonstracao" in rendered
    assert "me passa o WhatsApp" not in rendered
    assert "manda o telefone" not in rendered
    assert "instalar app" not in rendered
    assert report.total_cost_usd == 0
    assert fake_model.calls == 2


@pytest.mark.asyncio
async def test_t012_038_mocked_canonical_demo_request_uses_official_link() -> None:
    fixture_id = "final-demo-request"
    assert fixture_id in _canonical_ids("golden")

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "send_demo",
                        direct_question="quero ver uma demonstracao",
                        product_fact_keys_used=["demo_link"],
                        interpreted_intents=["demo"],
                        demo_intent="requested",
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        _fixture_messages("spec-011-golden-transcripts.json", fixture_id),
        model=fake_model,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.selected_action == "send_demo"
    assert turn.template_ids == ("product.demo_direct",)
    assert "/pilates/planos/demonstracao" in rendered
    assert "demo" in rendered.lower()
    assert "faz sentido pensar" not in rendered
    assert "retorna aqui se fez sentido para você" in rendered
    assert "se não entendeu alguma coisa" in rendered
    assert "checkout" not in rendered.lower()
    assert report.final_state["demo"] == {"status": "offered"}
    assert report.total_cost_usd == 0
    assert fake_model.calls == 2


@pytest.mark.asyncio
async def test_t012_038_mocked_canonical_waitlist_joined_keeps_no_checkout() -> None:
    fixture_id = "final-waitlist-joined"
    assert fixture_id in _canonical_ids("golden")

    fake_model = ScriptedFakeModel(
        [
            [
                _message(
                    _decision_json(
                        "join_waitlist",
                        waitlist_intent="provides_detail",
                        captured_slots=[
                            {
                                "key": "studio_name",
                                "value_text": "Studio Viva",
                                "status": "answered",
                                "evidence": ["inbound.text"],
                            },
                            {
                                "key": "city_state",
                                "value_text": "Vitoria ES",
                                "status": "answered",
                                "evidence": ["inbound.text"],
                            },
                        ],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        _fixture_messages("spec-011-golden-transcripts.json", fixture_id),
        model=fake_model,
        initial_state={
            "canonical_state": "waitlist_pending_data",
            "waitlist": {
                "status": "pending_data",
                "eligibility": "eligible",
                "missing_details": ["studio_name", "city_state"],
            },
        },
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.selected_action == "join_waitlist"
    assert turn.starting_agent == "taliya_waitlist_agent"
    assert turn.template_ids == ("waitlist.joined",)
    assert "Studio Viva" in rendered
    assert "Vitoria" in rendered
    assert "checkout" not in rendered.lower()
    assert "vip" not in rendered.lower()
    assert "desconto" not in rendered.lower()
    assert report.final_state["waitlist"]["status"] == "joined"
    assert report.final_state["waitlist"]["missing_details"] == []
    assert report.final_state["canonical_state"] == "waitlist_joined"
    assert report.total_cost_usd == 0
    assert fake_model.calls == 1


@pytest.mark.asyncio
async def test_t012_038_mocked_canonical_step3g_long_conversation_stateful() -> None:
    fixture_id = "step3g-long-conversation"
    assert fixture_id in _canonical_ids("golden")

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_direct_product_question",
                        direct_question="quanto custa?",
                        interpreted_intents=["price_question"],
                        product_fact_keys_used=["prices"],
                    )
                )
            ],
            [_function_call("transfer_to_taliya_diagnostic_agent")],
            [_message(_decision_json("start_requested_diagnostic"))],
            [
                _message(
                    _decision_json(
                        "capture_pending_diagnostic_answer",
                        captured_slots=[
                            {
                                "key": "active_students_or_size",
                                "value_text": "95 alunos ativos",
                                "status": "answered",
                                "evidence": ["inbound.text"],
                            }
                        ],
                        composition_variables=_feedback(
                            "Boa, 95 alunos ja pede uma rotina comercial organizada."
                        ),
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "capture_pending_diagnostic_answer",
                        captured_slots=[
                            {
                                "key": "main_pain",
                                "value_text": "WhatsApp e follow-up",
                                "status": "answered",
                                "evidence": ["inbound.text"],
                            }
                        ],
                        composition_variables=_feedback(
                            "Entendi, atendimento e follow-up estao puxando o peso."
                        ),
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "capture_pending_diagnostic_answer",
                        captured_slots=[
                            {
                                "key": "pain_detail",
                                "value_text": (
                                    "nao consegue ver quem precisa de retorno no dia"
                                ),
                                "status": "answered",
                                "evidence": ["inbound.text"],
                            }
                        ],
                        composition_variables=_feedback(
                            "Isso mostra que o problema e visibilidade diaria de retorno."
                        ),
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "capture_pending_diagnostic_answer",
                        captured_slots=[
                            {
                                "key": "current_process",
                                "value_text": "planilha e WhatsApp",
                                "status": "answered",
                                "evidence": ["inbound.text"],
                            }
                        ],
                        composition_variables=_feedback(
                            "Planilha com WhatsApp costuma espalhar os retornos."
                        ),
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "capture_pending_diagnostic_answer",
                        captured_slots=[
                            {
                                "key": "priority",
                                "value_text": "vendas primeiro",
                                "status": "answered",
                                "evidence": ["inbound.text"],
                            }
                        ],
                        composition_variables=_feedback(
                            "Faz sentido priorizar vendas antes de ampliar rotinas."
                        ),
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "complete_diagnostic",
                        captured_slots=[
                            {
                                "key": "urgency",
                                "value_text": "resolver agora",
                                "status": "answered",
                                "evidence": ["user: quero resolver agora"],
                            }
                        ],
                        composition_variables=[
                            {
                                "name": "pain_context_human",
                                "value": (
                                    "O studio tem 95 alunos e esta perdendo "
                                    "interessados porque WhatsApp e follow-up nao "
                                    "mostram quem precisa de retorno no dia."
                                ),
                                "evidence": ["diagnostic.ledger"],
                            },
                            {
                                "name": "crm_base_recommendation",
                                "value": (
                                    "Centralizar contatos, status e proximos retornos "
                                    "antes de escalar outras frentes."
                                ),
                                "evidence": ["diagnostic.ledger"],
                            },
                            {
                                "name": "operational_first_step",
                                "value": (
                                    "Comecar por uma lista diaria de interessados que "
                                    "precisam de retorno."
                                ),
                                "evidence": ["diagnostic.ledger"],
                            },
                        ],
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "send_demo",
                        direct_question="me manda demo",
                        interpreted_intents=["demo"],
                        product_fact_keys_used=["demo_link"],
                        demo_intent="requested",
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "answer_price_objection_with_context",
                        interpreted_intents=["price_objection"],
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "offer_or_join_waitlist_if_eligible",
                        waitlist_intent="contract_intent",
                        interpreted_intents=["contract_intent"],
                        composition_variables=[
                            {
                                "name": "waitlist_context_summary",
                                "value": (
                                    "Voce quer comecar depois de comparar valor e "
                                    "ver a demo."
                                ),
                                "evidence": ["inbound.text"],
                            }
                        ],
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "answer_question_then_continue_waitlist",
                        direct_question="como funciona mesmo?",
                        interpreted_intents=["how_it_works"],
                        product_fact_keys_used=["how_it_works"],
                        waitlist_intent="accepts",
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "handoff_requested",
                        handoff_intent="requested",
                        waitlist_intent="accepts",
                        composition_variables=[
                            {
                                "name": "handoff_reason",
                                "value": "pediu para falar com uma pessoa da equipe",
                                "evidence": ["user: quero falar com alguem"],
                            }
                        ],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        _fixture_messages("spec-011-golden-transcripts.json", fixture_id),
        model=fake_model,
        official_facts_overrides=COMPLETION_FACTS,
    )

    turn_summaries = [
        (
            turn.user_text,
            turn.status,
            turn.selected_action,
            turn.issues,
            turn.issue_details,
        )
        for turn in report.turns
    ]
    assert len(report.turns) == 13, turn_summaries
    assert all(turn.status == "delivered" for turn in report.turns), turn_summaries
    rendered = "\n".join(
        message for turn in report.turns for message in turn.rendered_messages
    )
    template_ids = tuple(
        template_id for turn in report.turns for template_id in turn.template_ids
    )

    assert "R$ 197" in rendered
    assert "R$ 497" in rendered
    assert "R$ 897" in rendered
    assert "R$ 1.497" in rendered
    assert "/pilates/planos/demonstracao" in rendered
    assert "diagnóstico" in rendered.lower()
    assert "retorno garantido" not in rendered.lower()
    assert "checkout" not in rendered.lower()
    assert "nao entendi" not in rendered.lower()
    assert "95 alunos ativos?" not in rendered

    assert report.turns[7].selected_action == "complete_diagnostic"
    assert report.turns[7].template_ids == (
        "diagnostic.deliver_hold",
        "diagnostic.deliver_context",
        "diagnostic.deliver_crm_base",
        "diagnostic.deliver_operational_step",
        "diagnostic.deliver_agent_recommendation",
        "diagnostic.deliver_plan_recommendation",
        "diagnostic.deliver_demo_not_offered",
    )
    assert "product.demo_direct" in template_ids
    assert "product.price_objection_value" in template_ids
    assert "waitlist.offer_after_contract_intent" in template_ids
    assert "product.how_it_works_direct" in template_ids
    assert "waitlist.ask_missing_contact_path" in template_ids
    assert report.turns[-1].selected_action == "handoff_requested"
    assert report.turns[-1].template_ids == ("handoff.acknowledge",)

    ledger = report.final_state["diagnostic"]["ledger"]
    assert ledger["active_students_or_size"]["answer_value"] == "95 alunos ativos"
    assert ledger["main_pain"]["answer_value"] == "WhatsApp e follow-up"
    assert ledger["pain_detail"]["answer_value"].startswith("nao consegue")
    assert ledger["current_process"]["answer_value"] == "planilha e WhatsApp"
    assert ledger["priority"]["answer_value"] == "vendas primeiro"
    assert ledger["urgency"]["answer_value"] == "resolver agora"
    assert report.final_state["diagnostic"]["status"] == "delivered"
    assert report.final_state["demo"] == {"status": "offered"}
    assert report.final_state["waitlist"] == {"status": "offered"}
    assert report.final_state["human_status"] == "requested"
    assert report.final_state["answered_obligations"] == [
        "quanto custa?",
        "me manda demo",
        "como funciona mesmo?",
    ]
    assert report.total_cost_usd == 0
    assert fake_model.calls == 15


@pytest.mark.asyncio
async def test_t012_038_mocked_canonical_human_request_suppresses_next_turn() -> None:
    fixture_id = "final-human-request-silent-after"
    assert fixture_id in _canonical_ids("golden")

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_handoff_agent")],
            [
                _message(
                    _decision_json(
                        "handoff_requested",
                        handoff_intent="requested",
                        composition_variables=[
                            {
                                "name": "handoff_reason",
                                "value": "pediu para falar com uma pessoa da equipe",
                                "evidence": ["inbound.text"],
                            }
                        ],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        _fixture_messages("spec-011-golden-transcripts.json", fixture_id),
        model=fake_model,
    )

    first, second = report.turns
    rendered = "\n".join(first.rendered_messages)
    assert first.status == "delivered"
    assert first.selected_action == "handoff_requested"
    assert "pessoa" in rendered.lower()
    assert "checkout" not in rendered.lower()
    assert "diagnóstico gratuito" not in rendered.lower()
    assert second.status == "suppressed"
    assert second.llm_called is False
    assert second.model_operations == 0
    assert second.rendered_messages == ()
    assert report.final_state["human_status"] == "requested"
    assert report.total_cost_usd == 0
    assert fake_model.calls == 2


@pytest.mark.asyncio
async def test_t012_038_mocked_canonical_simple_number_advances_diagnostic() -> None:
    fixture_id = "spec011-rc005-rc006-rc008-simple-number-answer"
    assert fixture_id in _canonical_ids("p0_regression")

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_diagnostic_agent")],
            [_message(_decision_json("start_requested_diagnostic"))],
            [
                _message(
                    _decision_json(
                        "capture_pending_diagnostic_answer",
                        captured_slots=[
                            {
                                "key": "active_students_or_size",
                                "value_text": "120",
                                "status": "answered",
                                "evidence": ["inbound.text"],
                            }
                        ],
                        composition_variables=[
                            {
                                "name": "answer_feedback",
                                "value": (
                                    "Boa, 120 alunos ja da uma boa base para "
                                    "entender o atendimento."
                                ),
                                "evidence": ["inbound.text"],
                            }
                        ],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        _fixture_messages("spec-011-real-openai-p0.json", fixture_id),
        model=fake_model,
    )

    first, second = report.turns
    assert first.status == "delivered"
    assert first.template_ids == (
        "opening.cold_greeting",
        "diagnostic.start",
        "diagnostic.ask_active_students",
    )
    assert second.status == "delivered"
    assert second.starting_agent == "taliya_diagnostic_agent"
    assert second.model_operations == 1
    assert second.template_ids == ("diagnostic.ask_main_pain",)
    ledger = report.final_state["diagnostic"]["ledger"]
    assert ledger["active_students_or_size"]["answer_value"] == "120"
    assert "diagnostic.ask_active_students" not in second.template_ids
    assert "nao entendi" not in "\n".join(second.rendered_messages).lower()
    assert report.total_cost_usd == 0
    assert fake_model.calls == 3
