from __future__ import annotations

import json

import pytest

from app.core.taliya_commercial_sdk.action_sales_inbox_evidence import (
    export_sales_inbox_projection_package,
    write_sales_inbox_projection_package,
)
from app.core.taliya_commercial_sdk.action_turn_runner import run_action_conversation
from app.core.taliya_commercial_sdk.conductor_decision import ConductorActionDecision
from tests.test_spec012_sdk_paid_harness_dry_run import (
    ScriptedFakeModel,
    _function_call,
    _message,
)


def _decision_json(action: str, **overrides) -> str:
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
            "agent_pain_resolved": "interessados sem retorno",
            "agent_practical_action": "organizar retornos para a equipe",
        }
    ],
}


def _waiting_for_urgency_state() -> dict:
    ledger = {
        key: {"status": "answered", "answer_value": value}
        for key, value in {
            "active_students_or_size": "95 alunos",
            "main_pain": "WhatsApp e follow-up",
            "pain_detail": "nao ve quem precisa de retorno",
            "current_process": "planilha e WhatsApp",
            "priority": "vendas primeiro",
        }.items()
    }
    return {
        "conversation_id": "conv_spec012_projection",
        "lead_id": "lead_spec012_projection",
        "canonical_state": "diagnostic_in_progress",
        "source": "pilates_landing",
        "summary": "Lead quer organizar atendimento e vendas.",
        "diagnostic": {"status": "in_progress", "ledger": ledger},
    }


def _joined_waitlist_resume_state() -> dict:
    return {
        "conversation_id": "conv_spec012_waitlist_projection",
        "lead_id": "lead_spec012_waitlist_projection",
        "canonical_state": "waitlist_joined",
        "source": "pilates_landing",
        "summary": "Lead entrou na lista e voltou depois de alguns dias.",
        "diagnostic": {
            "status": "completed",
            "ledger": {
                "active_students_or_size": {
                    "status": "answered",
                    "answer_value": "80",
                },
                "main_pain": {
                    "status": "answered",
                    "answer_value": "interessados sem retorno",
                },
                "pain_detail": {
                    "status": "answered",
                    "answer_value": "demora no WhatsApp",
                },
                "current_process": {
                    "status": "answered",
                    "answer_value": "WhatsApp manual",
                },
                "priority": {
                    "status": "answered",
                    "answer_value": "vendas",
                },
                "urgency": {
                    "status": "answered",
                    "answer_value": "resolver esse mes",
                },
            },
            "final_fields": {
                "final_plan_or_range": "Essencial (R$ 497/mes)",
                "final_demo_line": "Quer que eu te mande a demonstracao?",
            },
            "first_recommended_step": "organizar atendimento e follow-up",
            "recommended_plan_or_range": "Essencial",
        },
        "waitlist": {
            "status": "joined",
            "idempotency_key": "waitlist:joined:historical",
            "joined_at": "2026-06-01T12:00:00Z",
        },
    }


def _stale_completed_diagnostic_state() -> dict:
    ledger = {
        key: {"status": "answered", "answer_value": value}
        for key, value in {
            "active_students_or_size": "95 alunos",
            "main_pain": "WhatsApp e follow-up",
            "pain_detail": "nao ve quem precisa de retorno",
            "current_process": "planilha e WhatsApp",
            "priority": "vendas primeiro",
            "urgency": "resolver agora",
        }.items()
    }
    return {
        "conversation_id": "conv_spec012_stale_post_diag",
        "lead_id": "lead_spec012_stale_post_diag",
        "canonical_state": "diagnostic_offered",
        "source": "pilates_landing",
        "summary": "Diagnostico completo; lead avaliou preco e quer comecar.",
        "diagnostic": {
            "status": "delivered",
            "ledger": ledger,
            "final_fields": {
                "final_plan_or_range": "Essencial (R$ 497/mes)",
                "final_demo_line": (
                    "Temos algumas demonstracoes que mostram o funcionamento "
                    "na pratica. Quer que eu te mande?"
                ),
            },
        },
    }


@pytest.mark.asyncio
async def test_t012_035_sales_inbox_projection_for_price_turn() -> None:
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
        ]
    )

    report = await run_action_conversation(
        ["quanto custa?"],
        model=fake_model,
        initial_state={
            "conversation_id": "conv_spec012_price_projection",
            "lead_id": "lead_spec012_price_projection",
            "source": "pilates_landing",
            "summary": "Lead perguntou preco.",
        },
    )

    [turn] = report.turns
    projection = turn.sales_inbox_projection
    assert turn.status == "delivered"
    assert projection["conversation_id"] == "conv_spec012_price_projection"
    assert projection["lead_id"] == "lead_spec012_price_projection"
    assert projection["commercial_stage"] == "diagnostic_offered"
    assert projection["diagnostic_status"] == "offered"
    assert projection["fields"]["template_ids"] == [
        "product.price_direct",
        "diagnostic.price_hook",
    ]
    assert projection["fields"]["validator_status"] == "passed"
    assert projection["fields"]["source_labels"]["state_source"] == (
        "accepted_decision"
    )
    assert report.total_cost_usd == 0


@pytest.mark.asyncio
async def test_t012_043_waitlist_offer_after_stale_completed_diagnostic_state() -> None:
    fake_model = ScriptedFakeModel(
        [
            [
                _message(
                    _decision_json(
                        "offer_or_join_waitlist_if_eligible",
                        interpreted_intents=["contract_intent", "waitlist_interest"],
                        waitlist_intent="contract_intent",
                        composition_variables=[
                            {
                                "name": "waitlist_context_summary",
                                "value": (
                                    "Lead quer comecar apos diagnostico completo "
                                    "com foco em vendas e follow-up."
                                ),
                                "evidence": ["diagnostic.ledger", "inbound.text"],
                            }
                        ],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        ["quero comecar, me coloca na lista"],
        model=fake_model,
        initial_state=_stale_completed_diagnostic_state(),
        official_facts_overrides=COMPLETION_FACTS,
    )

    [turn] = report.turns
    projection = turn.sales_inbox_projection
    assert turn.status == "delivered"
    assert turn.mode == "post_diagnostic"
    assert turn.selected_action == "offer_or_join_waitlist_if_eligible"
    assert projection["commercial_stage"] == "waitlist_offered"
    assert projection["diagnostic_status"] == "completed"
    assert projection["waitlist_status"] == "offered"
    assert projection["fields"]["template_ids"] == [
        "waitlist.offer_after_contract_intent"
    ]
    assert projection["fields"]["diagnostic_ledger_complete"] is True
    assert report.final_state["canonical_state"] == "waitlist_offered"
    assert report.total_cost_usd == 0


@pytest.mark.asyncio
async def test_t012_035_sales_inbox_projection_for_completed_diagnostic() -> None:
    fake_model = ScriptedFakeModel(
        [
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
                                    "O atendimento e follow-up estao deixando "
                                    "interessados sem retorno."
                                ),
                                "evidence": ["diagnostic.ledger"],
                            },
                            {
                                "name": "crm_base_recommendation",
                                "value": (
                                    "Centralizar contatos e proximos retornos "
                                    "para a equipe."
                                ),
                                "evidence": ["diagnostic.ledger"],
                            },
                            {
                                "name": "operational_first_step",
                                "value": "Comecar por uma lista diaria de retorno.",
                                "evidence": ["diagnostic.ledger"],
                            },
                        ],
                    )
                )
            ]
        ]
    )

    report = await run_action_conversation(
        ["quero resolver agora"],
        model=fake_model,
        initial_state=_waiting_for_urgency_state(),
        official_facts_overrides=COMPLETION_FACTS,
    )

    [turn] = report.turns
    projection = turn.sales_inbox_projection
    assert turn.status == "delivered"
    assert projection["commercial_stage"] == "diagnostic_delivered"
    assert projection["diagnostic_status"] == "completed"
    assert projection["fields"]["diagnostic_ledger_complete"] is True
    assert set(projection["fields"]["required_diagnostic_keys"]) == {
        "active_students_or_size",
        "main_pain",
        "pain_detail",
        "current_process",
        "priority",
        "urgency",
    }
    assert projection["fields"]["final_plan_or_range"] == "Essencial (R$ 497/mes)"
    assert "demonstracoes" in projection["fields"]["final_demo_line"]
    assert projection["fields"]["operator_next_action"] == (
        "review_completed_diagnostic"
    )
    assert report.total_cost_usd == 0


@pytest.mark.asyncio
async def test_t012_046_exports_joined_waitlist_projection_history(tmp_path) -> None:
    fake_model = ScriptedFakeModel(
        [
            [
                _message(
                    _decision_json(
                        "answer_product_question_with_saved_context",
                        direct_question="como funciona mesmo?",
                        interpreted_intents=["conversation_resume", "product_how_it_works"],
                        product_fact_keys_used=["how_it_works"],
                    )
                )
            ],
        ]
    )
    report = await run_action_conversation(
        ["como funciona mesmo?"],
        model=fake_model,
        initial_state=_joined_waitlist_resume_state(),
    )

    package = export_sales_inbox_projection_package(
        report,
        scenario_id="t012-046-joined-waitlist-projection-history",
    )

    assert package["schema"] == "012.sales_inbox_projection_export.v1"
    assert package["turn_count"] == 1
    assert package["projection_count"] == 1
    assert package["projection_complete"] is True
    assert package["missing_required_fields"] == {}
    assert package["missing_projection_turn_indexes"] == []
    assert package["conversation_summary"]["total_cost_usd"] == 0

    projection = package["turns"][0]["projection"]
    assert projection["conversation_id"] == "conv_spec012_waitlist_projection"
    assert projection["lead_id"] == "lead_spec012_waitlist_projection"
    assert projection["commercial_stage"] == "post_diagnostic_questions"
    assert projection["diagnostic_status"] == "completed"
    assert projection["waitlist_status"] == "joined"
    assert projection["fields"]["template_ids"] == ["product.how_it_works_direct"]
    assert projection["fields"]["waitlist_idempotency_key"] == (
        "waitlist:joined:historical"
    )
    assert projection["fields"]["waitlist_joined_at"] == "2026-06-01T12:00:00Z"
    assert projection["fields"]["missing_waitlist_fields"] == []
    assert projection["fields"]["operator_next_action"] == "monitor_waitlist"

    json_path = write_sales_inbox_projection_package(package, tmp_path)
    written = json.loads(json_path.read_text(encoding="utf-8"))
    assert written["projection_complete"] is True
    assert "waitlist:joined:historical" in json_path.read_text(encoding="utf-8")


@pytest.mark.asyncio
async def test_t012_046_exports_sales_inbox_projection_evidence_package(tmp_path) -> None:
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
                        "handoff_requested",
                        handoff_intent="requested",
                        composition_variables=[
                            {
                                "name": "handoff_reason",
                                "value": "preferiu falar com uma pessoa da equipe",
                                "evidence": ["inbound.text"],
                            }
                        ],
                    )
                )
            ],
        ]
    )
    report = await run_action_conversation(
        [
            "quanto custa?",
            "quero fazer o diagnostico gratuito",
            "prefiro falar com uma pessoa",
            "alguem ai?",
        ],
        model=fake_model,
        initial_state={
            "conversation_id": "conv_spec012_projection_export",
            "lead_id": "lead_spec012_projection_export",
            "source": "pilates_landing",
        },
    )

    package = export_sales_inbox_projection_package(
        report,
        scenario_id="t012-046-sales-inbox-projection-export",
    )

    assert package["schema"] == "012.sales_inbox_projection_export.v1"
    assert "lead_id" in package["required_projection_fields"]
    assert package["turn_count"] == 4
    assert package["projection_count"] == 3
    assert package["projection_complete"] is True
    assert package["missing_required_fields"] == {}
    assert package["missing_projection_turn_indexes"] == []
    assert package["conversation_summary"]["total_cost_usd"] == 0
    assert package["turns"][0]["projection"]["conversation_id"] == (
        "conv_spec012_projection_export"
    )
    assert package["turns"][0]["projection"]["lead_id"] == (
        "lead_spec012_projection_export"
    )
    assert package["turns"][0]["projection"]["fields"]["source_labels"][
        "state_source"
    ] == "accepted_decision"
    assert package["turns"][3]["status"] == "suppressed"
    assert package["turns"][3]["projection_required"] is False
    assert package["turns"][3]["projection_present"] is False

    json_path = write_sales_inbox_projection_package(package, tmp_path)
    markdown_path = tmp_path / "sales-inbox-projection-package.md"
    written = json.loads(json_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert json_path.name == "sales-inbox-projection-package.json"
    assert written["projection_complete"] is True
    assert "conv_spec012_projection_export" in json_path.read_text(
        encoding="utf-8"
    )
    assert "# Spec 012 Sales Inbox Projection Package" in markdown
    assert "Projection complete: True" in markdown
    assert "diagnostic_offered" in markdown
