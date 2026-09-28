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


@pytest.mark.asyncio
async def test_t012_038_do_not_do_early_phone_capture_answers_price_only() -> None:
    fixture_id = "do-not-do-early-phone-capture"
    assert fixture_id in _canonical_ids("do_not_do_runtime")

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_direct_product_question",
                        direct_question="quanto custa",
                        product_fact_keys_used=["prices"],
                        interpreted_intents=["price_question"],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        _fixture_messages("spec-011-do-not-do-runtime.json", fixture_id),
        model=fake_model,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.selected_action == "answer_direct_product_question"
    assert "R$ 497" in rendered
    assert "qual seu telefone" not in rendered.lower()
    assert "me passa seu whatsapp" not in rendered.lower()
    assert "manda seu contato" not in rendered.lower()
    assert "qual seu nome" not in rendered.lower()
    assert report.total_cost_usd == 0
    assert fake_model.calls == 2


@pytest.mark.asyncio
async def test_t012_038_do_not_do_checkout_buy_intent_goes_to_waitlist() -> None:
    fixture_id = "final-checkout-buy-intent"
    assert fixture_id in _canonical_ids("do_not_do_runtime")

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_waitlist_agent")],
            [
                _message(
                    _decision_json(
                        "offer_waitlist",
                        waitlist_intent="contract_intent",
                        interpreted_intents=["contract_intent"],
                        composition_variables=[
                            {
                                "name": "waitlist_context_summary",
                                "value": (
                                    "Quer contratar agora e pediu o caminho de "
                                    "entrada."
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
        _fixture_messages("spec-011-do-not-do-runtime.json", fixture_id),
        model=fake_model,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.selected_action == "offer_waitlist"
    assert turn.template_ids == ("waitlist.offer_after_contract_intent",)
    assert "lista" in rendered.lower()
    assert "link de checkout" not in rendered.lower()
    assert "checkout seguro" not in rendered.lower()
    assert "link de pagamento" not in rendered.lower()
    assert "cartao" not in rendered.lower()
    assert "pix" not in rendered.lower()
    assert report.final_state["waitlist"] == {"status": "offered"}
    assert report.total_cost_usd == 0
    assert fake_model.calls == 2


@pytest.mark.asyncio
async def test_t012_038_do_not_do_date_vip_discount_uses_waitlist_safely() -> None:
    fixture_id = "do-not-do-date-vip-discount"
    assert fixture_id in _canonical_ids("do_not_do_runtime")

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_waitlist_agent")],
            [
                _message(
                    _decision_json(
                        "offer_waitlist",
                        waitlist_intent="contract_intent",
                        interpreted_intents=["contract_intent", "availability"],
                        composition_variables=[
                            {
                                "name": "waitlist_context_summary",
                                "value": (
                                    "Quer pagar hoje, mas data e condicao de "
                                    "entrada precisam ficar sem promessa."
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
        _fixture_messages("spec-011-do-not-do-runtime.json", fixture_id),
        model=fake_model,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert "lista" in rendered.lower()
    forbidden = (
        "desconto aprovado",
        "desconto garantido",
        "vaga vip",
        "vip garantido",
        "abre no dia",
        "data garantida",
        "pagar hoje pelo link",
        "checkout seguro",
    )
    for phrase in forbidden:
        assert phrase not in rendered.lower()
    assert report.total_cost_usd == 0
    assert fake_model.calls == 2


@pytest.mark.asyncio
async def test_t012_038_do_not_do_integration_scope_no_invented_integration() -> None:
    fixture_id = "product-delta-integration-scope"
    assert fixture_id in _canonical_ids("do_not_do_runtime")

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_integration_scope_safely",
                        direct_question="integra com Instagram e com meu sistema atual?",
                        product_fact_keys_used=["integration_scope"],
                        interpreted_intents=["integration_scope_question"],
                        composition_variables=[
                            {
                                "name": "integration_topic",
                                "value": "Instagram e sistema atual",
                                "evidence": ["inbound.text"],
                            }
                        ],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        _fixture_messages("spec-011-do-not-do-runtime.json", fixture_id),
        model=fake_model,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.template_ids == ("product.integration_scope_direct",)
    assert "confirmar" in rendered.lower()
    for phrase in (
        "integra sim",
        "conectamos automaticamente",
        "integracao pronta",
        "disparo em massa incluso",
    ):
        assert phrase not in rendered.lower()
    assert report.total_cost_usd == 0
    assert fake_model.calls == 2


@pytest.mark.asyncio
async def test_t012_038_do_not_do_security_data_no_certification_promise() -> None:
    fixture_id = "product-delta-security-data"
    assert fixture_id in _canonical_ids("do_not_do_runtime")

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_security_and_data",
                        direct_question="e seguro? tem LGPD?",
                        product_fact_keys_used=["security_and_data"],
                        interpreted_intents=["security_data"],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        _fixture_messages("spec-011-do-not-do-runtime.json", fixture_id),
        model=fake_model,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.template_ids == ("product.security_data_direct",)
    assert "dados" in rendered.lower()
    for phrase in (
        "certificado",
        "criptografia garantida",
        "lgpd garantida",
        "auditado",
    ):
        assert phrase not in rendered.lower()
    assert report.total_cost_usd == 0
    assert fake_model.calls == 2


@pytest.mark.asyncio
async def test_t012_038_do_not_do_studio_whatsapp_connection_capture() -> None:
    fixture_id = "do-not-do-client-studio-whatsapp-capture"
    assert fixture_id in _canonical_ids("do_not_do_runtime")

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_whatsapp_scope",
                        direct_question="ja posso conectar o WhatsApp do meu studio?",
                        product_fact_keys_used=["whatsapp_scope", "demo_link"],
                        interpreted_intents=["whatsapp_scope"],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        _fixture_messages("spec-011-do-not-do-runtime.json", fixture_id),
        model=fake_model,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.template_ids == ("product.whatsapp_direct",)
    for phrase in (
        "manda o numero",
        "me passa o codigo",
        "envia o qr code",
        "conecto agora",
    ):
        assert phrase not in rendered.lower()
    assert report.total_cost_usd == 0
    assert fake_model.calls == 2


@pytest.mark.asyncio
async def test_t012_038_do_not_do_wrong_student_language() -> None:
    fixture_id = "do-not-do-wrong-student-language"
    assert fixture_id in _canonical_ids("do_not_do_runtime")

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_whatsapp_scope",
                        direct_question=(
                            "meus clientes precisam baixar app para usar a Taliya?"
                        ),
                        product_fact_keys_used=["whatsapp_scope", "demo_link"],
                        interpreted_intents=["whatsapp_scope"],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        _fixture_messages("spec-011-do-not-do-runtime.json", fixture_id),
        model=fake_model,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.template_ids == ("product.whatsapp_direct",)
    assert "aluno" in rendered
    assert "baixar aplicativo" in rendered
    assert "clientes precisam baixar app" not in rendered.lower()
    assert "consumidores" not in rendered.lower()
    assert report.total_cost_usd == 0
    assert fake_model.calls == 2


@pytest.mark.asyncio
async def test_t012_038_do_not_do_price_497_not_student_count() -> None:
    fixture_id = "spec011-rc003-price-497-not-student-count"
    assert fixture_id in _canonical_ids("do_not_do_runtime")

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_direct_product_question",
                        direct_question="Vi o plano de 497",
                        interpreted_intents=[
                            "price_question",
                            "pain_description",
                        ],
                        product_fact_keys_used=["prices"],
                        composition_variables=[
                            {
                                "name": "plan_fit_context",
                                "value": (
                                    "A reposicao baguncada no studio pede "
                                    "diagnostico antes de comparar plano."
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
        _fixture_messages("spec-011-do-not-do-runtime.json", fixture_id),
        model=fake_model,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert "Como você já trouxe um ponto da rotina que está te incomodando" in rendered
    assert "497 alunos" not in rendered
    assert "497 estudantes" not in rendered
    assert report.total_cost_usd == 0
    assert fake_model.calls == 2
