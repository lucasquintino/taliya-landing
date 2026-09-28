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
            "agent_pain_resolved": "demora no WhatsApp",
            "agent_practical_action": "organizar retornos e avisar a equipe",
        }
    ],
}


def _diagnostic_waiting_for_urgency_state() -> dict[str, Any]:
    answered = {
        key: {"status": "answered", "answer_value": "x"}
        for key in (
            "active_students_or_size",
            "main_pain",
            "pain_detail",
            "current_process",
            "priority",
        )
    }
    return {
        "canonical_state": "diagnostic_in_progress",
        "diagnostic": {"status": "in_progress", "ledger": answered},
    }


def _diagnostic_waiting_for_main_pain_state() -> dict[str, Any]:
    return {
        "canonical_state": "diagnostic_in_progress",
        "diagnostic": {
            "status": "in_progress",
            "ledger": {
                "active_students_or_size": {
                    "status": "answered",
                    "answer_value": "nao informado com precisao",
                }
            },
        },
    }


def _complete_diagnostic_decision() -> str:
    return _decision_json(
        "complete_diagnostic",
        captured_slots=[
            {
                "key": "urgency",
                "value_text": "urgente resolver nesse mes",
                "status": "answered",
                "evidence": ["user: nesse mes"],
            }
        ],
        composition_variables=[
            {
                "name": "pain_context_human",
                "value": (
                    "O atendimento e follow-up estao deixando interessados "
                    "escaparem."
                ),
                "evidence": ["inbound.text"],
            },
            {
                "name": "crm_base_recommendation",
                "value": (
                    "Organizar a base de contatos e o retorno comercial antes "
                    "de ampliar agentes."
                ),
                "evidence": ["inbound.text"],
            },
            {
                "name": "operational_first_step",
                "value": "Comecar por uma rotina diaria de follow-up dos interessados.",
                "evidence": ["inbound.text"],
            },
        ],
    )


@pytest.mark.asyncio
async def test_t012_038_p0_internal_metadata_leak_is_not_rendered() -> None:
    fixture_id = "spec011-rc001-rc002-internal-metadata-leak"
    assert fixture_id in _canonical_ids("p0_regression")

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_how_it_works",
                        direct_question="como funciona a Taliya na pratica?",
                        product_fact_keys_used=["how_it_works"],
                        interpreted_intents=["how_it_works"],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        _fixture_messages("spec-011-real-openai-p0.json", fixture_id),
        model=fake_model,
        initial_state={
            "source": "lead came from the site",
            "channel_metadata": {
                "profile_name": "Reliable profile first name: Marina",
                "source_label": "lead came from the site",
            },
        },
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.selected_action == "answer_how_it_works"
    assert turn.template_ids == ("product.how_it_works_direct",)
    assert "studio" in rendered
    assert "source_label" not in rendered
    assert "lead came from the site" not in rendered
    assert "Reliable profile first name" not in rendered
    assert "taliya_triage_agent" not in rendered
    assert report.total_cost_usd == 0
    assert fake_model.calls == 2


@pytest.mark.asyncio
async def test_t012_038_p0_urgency_timing_is_captured_before_final() -> None:
    fixture_id = "spec011-rc004-urgency-before-final"
    assert fixture_id in _canonical_ids("p0_regression")

    fake_model = ScriptedFakeModel(
        [
            [
                _message(
                    _decision_json(
                        "complete_diagnostic",
                        composition_variables=[
                            {
                                "name": "pain_context_human",
                                "value": (
                                    "O studio ja tem 120 alunos e esta perdendo "
                                    "interessados por atendimento e follow-up no "
                                    "WhatsApp."
                                ),
                                "evidence": ["inbound.text"],
                            },
                            {
                                "name": "crm_base_recommendation",
                                "value": (
                                    "Centralizar os interessados e retornos antes "
                                    "de comparar a Taliya completa."
                                ),
                                "evidence": ["inbound.text"],
                            },
                            {
                                "name": "operational_first_step",
                                "value": (
                                    "Comecar pelo fluxo diario de atendimento e "
                                    "follow-up comercial."
                                ),
                                "evidence": ["inbound.text"],
                            },
                        ],
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
                                "value_text": "quer comparar agora",
                                "status": "answered",
                                "evidence": ["user: a prioridade agora e vendas"],
                            }
                        ],
                        composition_variables=[
                            {
                                "name": "pain_context_human",
                                "value": (
                                    "O studio ja tem 120 alunos e esta perdendo "
                                    "interessados por atendimento e follow-up no "
                                    "WhatsApp."
                                ),
                                "evidence": ["inbound.text"],
                            },
                            {
                                "name": "crm_base_recommendation",
                                "value": (
                                    "Centralizar os interessados e retornos antes "
                                    "de comparar a Taliya completa."
                                ),
                                "evidence": ["inbound.text"],
                            },
                            {
                                "name": "operational_first_step",
                                "value": (
                                    "Comecar pelo fluxo diario de atendimento e "
                                    "follow-up comercial."
                                ),
                                "evidence": ["inbound.text"],
                            },
                        ],
                    )
                )
            ]
        ]
    )

    report = await run_action_conversation(
        _fixture_messages("spec-011-real-openai-p0.json", fixture_id),
        model=fake_model,
        initial_state=_diagnostic_waiting_for_urgency_state(),
        official_facts_overrides=COMPLETION_FACTS,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.selected_action == "complete_diagnostic"
    assert turn.repairs == 1
    assert "diagnostic.ask_urgency" not in turn.template_ids
    assert "diagnostic.deliver_plan_recommendation" in turn.template_ids
    assert "quer comparar agora" in report.final_state["diagnostic"]["ledger"]["urgency"][
        "answer_value"
    ]
    assert "120 alunos" in rendered
    assert "checkout" not in rendered.lower()
    assert "taliya_" not in rendered
    assert report.total_cost_usd == 0
    assert fake_model.calls == 2


@pytest.mark.asyncio
async def test_t012_038_p0_valid_short_answer_advances_diagnostic() -> None:
    fixture_id = "spec011-rc007-valid-short-answer-does-not-stall"
    assert fixture_id in _canonical_ids("p0_regression")
    _start_request, short_answer = _fixture_messages(
        "spec-011-real-openai-p0.json", fixture_id
    )

    fake_model = ScriptedFakeModel(
        [
            [
                _message(
                    _decision_json(
                        "capture_pending_diagnostic_answer",
                        captured_slots=[
                            {
                                "key": "main_pain",
                                "value_text": "agenda e reposicoes",
                                "status": "answered",
                                "evidence": ["user: agenda e reposicoes"],
                            }
                        ],
                        composition_variables=[
                            {
                                "name": "answer_feedback",
                                "value": (
                                    "Entendi, agenda e reposicoes parecem estar "
                                    "pesando na rotina."
                                ),
                                "evidence": ["inbound.text"],
                            }
                        ],
                    )
                )
            ]
        ]
    )

    report = await run_action_conversation(
        [short_answer],
        model=fake_model,
        initial_state=_diagnostic_waiting_for_main_pain_state(),
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.selected_action == "capture_pending_diagnostic_answer"
    assert turn.template_ids == ("diagnostic.ask_pain_detail",)
    assert "diagnostic.offer_soft" not in turn.template_ids
    assert "agenda e reposicoes" in report.final_state["diagnostic"]["ledger"][
        "main_pain"
    ]["answer_value"]
    assert "nao entendi" not in rendered.lower()
    assert "taliya_" not in rendered
    assert report.total_cost_usd == 0
    assert fake_model.calls == 1


@pytest.mark.asyncio
async def test_t012_038_p0_final_diagnostic_not_truncated() -> None:
    fixture_id = "spec011-rc009-final-diagnostic-not-truncated"
    assert fixture_id in _canonical_ids("p0_regression")

    fake_model = ScriptedFakeModel([[_message(_complete_diagnostic_decision())]])

    report = await run_action_conversation(
        _fixture_messages("spec-011-real-openai-p0.json", fixture_id),
        model=fake_model,
        initial_state=_diagnostic_waiting_for_urgency_state(),
        official_facts_overrides=COMPLETION_FACTS,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.selected_action == "complete_diagnostic"
    assert turn.template_ids == (
        "diagnostic.deliver_hold",
        "diagnostic.deliver_context",
        "diagnostic.deliver_crm_base",
        "diagnostic.deliver_operational_step",
        "diagnostic.deliver_agent_recommendation",
        "diagnostic.deliver_plan_recommendation",
        "diagnostic.deliver_demo_not_offered",
    )
    assert rendered.strip().endswith("Quer que eu te envie?")
    assert "pelo que voce contou" not in rendered.lower()
    assert report.final_state["diagnostic"]["status"] == "delivered"
    assert report.final_state["diagnostic"]["ledger"]["urgency"][
        "answer_value"
    ] == "urgente resolver nesse mes"
    assert report.total_cost_usd == 0
    assert fake_model.calls == 1


@pytest.mark.asyncio
async def test_t012_038_p0_final_diagnostic_plain_studio_language() -> None:
    fixture_id = "spec011-rc012-final-diagnostic-plain-studio-language"
    assert fixture_id in _canonical_ids("p0_regression")

    fake_model = ScriptedFakeModel([[_message(_complete_diagnostic_decision())]])

    report = await run_action_conversation(
        _fixture_messages("spec-011-real-openai-p0.json", fixture_id),
        model=fake_model,
        initial_state=_diagnostic_waiting_for_urgency_state(),
        official_facts_overrides=COMPLETION_FACTS,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.selected_action == "complete_diagnostic"
    assert "studio" in rendered
    assert "interessados" in rendered
    assert "plano Essencial" in rendered
    assert "CRM" not in rendered
    assert "lead" not in rendered.lower()
    assert "consumidores" not in rendered.lower()
    assert "taliya_" not in rendered
    assert report.total_cost_usd == 0
    assert fake_model.calls == 1


@pytest.mark.asyncio
async def test_t012_038_p0_sales_inbox_consistency_price_plus_pain() -> None:
    fixture_id = "spec011-rc013-sales-inbox-projection-consistency"
    assert fixture_id in _canonical_ids("p0_regression")

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_direct_product_question",
                        direct_question="quanto custa?",
                        interpreted_intents=["price_question", "pain_description"],
                        product_fact_keys_used=["prices"],
                        composition_variables=[
                            {
                                "name": "plan_fit_context",
                                "value": (
                                    "Follow-up dos interessados pede diagnostico "
                                    "antes de escolher plano."
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

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.template_ids == (
        "product.price_direct",
        "diagnostic.price_hook_with_context",
    )
    assert "Como você já trouxe um ponto da rotina que está te incomodando" in rendered
    assert "taliya_" not in rendered
    assert report.final_state["canonical_state"] == "diagnostic_offered"
    assert report.final_state["answered_obligations"] == ["quanto custa?"]
    assert report.total_model_operations == 2
    assert report.total_cost_usd == 0


@pytest.mark.asyncio
async def test_t012_038_p0_false_pass_requires_model_and_rendered_behavior() -> None:
    fixture_id = "spec011-rc014-false-pass-protection"
    assert fixture_id in _canonical_ids("p0_regression")

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
        _fixture_messages("spec-011-real-openai-p0.json", fixture_id),
        model=fake_model,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.llm_called is True
    assert turn.model_operations == 2
    assert turn.template_ids == ("product.price_direct", "diagnostic.price_hook")
    assert rendered.strip()
    for price in ("R$ 197", "R$ 497", "R$ 897", "R$ 1.497"):
        assert price in rendered
    assert "checkout" not in rendered.lower()
    assert report.total_cost_usd == 0
    assert fake_model.calls == 2
