from __future__ import annotations

import inspect
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

import pytest

from app.core.taliya_commercial_sdk import (
    DIAGNOSTIC_AGENT,
    ENTRY_AGENT,
    HANDOFF_AGENT,
    PRODUCT_AGENT,
    TRIAGE_AGENT,
    WAITLIST_AGENT,
    IsolatedSdkSpikeInput,
    adapt_sdk_output_to_turn_proposal,
    run_isolated_sdk_spike,
    validate_and_render_spike_output,
)


@dataclass(frozen=True)
class MockedSpikeScenario:
    scenario_id: str
    user_text: str
    channel: str
    output: dict[str, Any]


def _var(
    kind: str,
    value: Any,
    source: str,
    evidence: list[str],
    *,
    max_length: int | None = None,
) -> dict[str, Any]:
    payload = {
        "kind": kind,
        "value": value,
        "source": source,
        "evidence": evidence,
    }
    if max_length is not None:
        payload["max_length"] = max_length
    return payload


PRICE_SUMMARY = _var(
    "long_text",
    "Os planos oficiais comecam no Base R$ 197/mes e chegam ao Essencial "
    "R$ 497/mes, conforme escopo contratado.",
    "official_product_knowledge",
    ["product_knowledge.prices"],
    max_length=360,
)
PAIN_CONTEXT = _var(
    "long_text",
    "Quando leads interessados ficam esperando no WhatsApp, a rotina perde "
    "velocidade e oportunidade de venda.",
    "user_message",
    ["inbound.text"],
    max_length=420,
)
PLAN_FIT_CONTEXT = _var(
    "short_text",
    "Com WhatsApp caotico, faz sentido comparar plano depois de entender "
    "volume, rotina e urgencia.",
    "user_message",
    ["inbound.text"],
    max_length=180,
)
PRODUCT_WHATSAPP_FACT = _var(
    "long_text",
    "A Taliya pode apoiar conversas no WhatsApp Business do studio quando o "
    "canal esta conectado, com a equipe acompanhando e podendo assumir.",
    "official_product_knowledge",
    ["product_knowledge.whatsapp_scope"],
    max_length=320,
)
OFFICIAL_DEMO_LINK = _var(
    "url",
    "https://taliya.example/demo",
    "official_product_knowledge",
    ["product_knowledge.demo_link"],
)
ANSWER_FEEDBACK_120 = _var(
    "short_text",
    "Entendi: com 120 alunos ativos, ja existe volume para organizar "
    "atendimento e acompanhamento com mais criterio.",
    "diagnostic_ledger",
    ["diagnostic_ledger.active_students_or_size"],
    max_length=180,
)
WAITLIST_CONTEXT = _var(
    "long_text",
    "Depois do diagnostico/demo, a lead demonstrou intencao clara de seguir com a Taliya.",
    "runtime_state",
    ["waitlist_state.contract_intent"],
    max_length=220,
)
HUMAN_CONFIRMATION_TOPIC = _var(
    "short_text",
    "checkout, desconto, data e condicao VIP",
    "user_message",
    ["inbound.text"],
    max_length=100,
)
HANDOFF_REASON = _var(
    "short_text",
    "pedido direto para falar com uma pessoa da Taliya",
    "user_message",
    ["inbound.text"],
    max_length=120,
)
DIAGNOSTIC_VARIABLES = {
    "pain_context_human": _var(
        "long_text",
        "O principal gargalo aparece no retorno a interessados e na falta de "
        "visao diaria do que precisa de acao.",
        "diagnostic_ledger",
        ["diagnostic_ledger.main_pain", "diagnostic_ledger.pain_detail"],
        max_length=420,
    ),
    "crm_base_recommendation": _var(
        "long_text",
        "Antes de automatizar tudo, vale organizar a base de contatos, status "
        "de leads, alunos e pendencias da rotina.",
        "diagnostic_ledger",
        ["diagnostic_ledger.current_process"],
        max_length=260,
    ),
    "operational_first_step": _var(
        "long_text",
        "Comece pelo acompanhamento dos interessados que chegam pelo WhatsApp "
        "e defina quem precisa de retorno hoje.",
        "diagnostic_ledger",
        ["diagnostic_ledger.priority", "diagnostic_ledger.urgency"],
        max_length=240,
    ),
    "recommended_plan_or_range": _var(
        "short_text",
        "Essencial ou faixa equivalente validada pela equipe",
        "official_product_knowledge",
        ["product_knowledge.plans"],
        max_length=90,
    ),
    "demo_status": _var(
        "enum",
        "not_offered",
        "runtime_state",
        ["demo_state.status"],
    ),
}


def _base_output(
    *,
    scenario_id: str,
    channel: str = "whatsapp",
    starting_agent: str = TRIAGE_AGENT,
    final_agent: str = ENTRY_AGENT,
    intents: list[str] | None = None,
    direct_question: str | None = None,
    mixed_intent: bool = False,
    template_ids: list[str],
    variables: dict[str, Any] | None = None,
    product_claims: list[dict[str, Any]] | None = None,
    answer_obligations: list[dict[str, Any]] | None = None,
    diagnostic_proposal: dict[str, Any] | None = None,
    demo_proposal: dict[str, Any] | None = None,
    waitlist_proposal: dict[str, Any] | None = None,
    handoff_proposal: dict[str, Any] | None = None,
    state_patch_proposal: dict[str, Any] | None = None,
    sales_stage: str = "lead_conversation",
    chunk_policy: str = "whatsapp_max_3",
    agent_path: list[dict[str, Any]] | None = None,
    extracted_facts: list[dict[str, Any]] | None = None,
    risks: list[str] | None = None,
) -> dict[str, Any]:
    path = agent_path or [
        {"event": "start", "agent": starting_agent},
        {"event": "handoff", "from_agent": starting_agent, "to_agent": final_agent},
        {"event": "final", "agent": final_agent},
    ]
    return {
        "schema_version": "012.turn_proposal.v1",
        "turn_id": f"turn_{scenario_id}",
        "conversation_id": f"conv_{scenario_id}",
        "channel": channel,
        "starting_agent": starting_agent,
        "agent_path": path,
        "commercial_understanding": {
            "intents": intents or ["general_interest"],
            "direct_question": direct_question,
            "customer_need": None,
            "pain_context": None,
            "mixed_intent": mixed_intent,
            "extracted_facts": extracted_facts or [],
            "evidence": ["inbound.text"],
        },
        "answer_obligations": answer_obligations or [],
        "product_claims": product_claims or [],
        "diagnostic_proposal": diagnostic_proposal
        or {"ledger_updates": [], "next_question_key": None, "final_diagnostic_ready": False},
        "demo_proposal": demo_proposal
        or {"status": "not_offered", "next_step": "none", "evidence": []},
        "waitlist_proposal": waitlist_proposal
        or {
            "eligibility": "unknown",
            "intent": "none",
            "missing_details": [],
            "evidence": [],
        },
        "handoff_proposal": handoff_proposal
        or {"status": "none", "reason": None, "pause_required": False, "evidence": []},
        "template_proposal": {
            "template_ids": template_ids,
            "variables": variables or {},
            "evidence": [f"template_registry.{template_ids[0]}"],
        },
        "safety": {"guardrails": [], "uncertainty": "low"},
        "state_patch_proposal": state_patch_proposal or {},
        "sales_inbox_projection_proposal": {
            "commercial_stage": sales_stage,
            "scenario_id": scenario_id,
        },
        "delivery_proposal": {
            "chunk_policy": chunk_policy,
            "render_plan_only": True,
            "evidence": [f"template_registry.{template_ids[0]}"],
        },
        "confidence": "high",
        "risks": risks or [],
        "usage": {
            "model": "mocked-sdk-no-cost",
            "model_operations": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "cost_usd": 0,
            "handoffs": sum(1 for item in path if item["event"] == "handoff"),
            "repairs": 0,
        },
    }


def _claim(claim: str, fact_ref: str) -> dict[str, Any]:
    return {"claim": claim, "fact_refs": [fact_ref], "evidence": [fact_ref]}


def _answered(obligation: str) -> dict[str, Any]:
    return {
        "obligation": obligation,
        "answered_before_steering": True,
        "evidence": ["inbound.text"],
    }


def _scenarios() -> list[MockedSpikeScenario]:
    return [
        MockedSpikeScenario(
            "cold_greeting",
            "oi",
            "widget",
            _base_output(
                scenario_id="cold_greeting",
                channel="widget",
                final_agent=ENTRY_AGENT,
                template_ids=["opening.cold_greeting"],
                chunk_policy="default",
                agent_path=[
                    {"event": "start", "agent": ENTRY_AGENT},
                    {"event": "final", "agent": ENTRY_AGENT},
                ],
            ),
        ),
        MockedSpikeScenario(
            "pain_first",
            "perco leads interessados no WhatsApp porque a equipe responde tarde",
            "whatsapp",
            _base_output(
                scenario_id="pain_first",
                final_agent=DIAGNOSTIC_AGENT,
                intents=["pain_context", "diagnostic_offer"],
                template_ids=["diagnostic.offer_soft"],
                variables={"pain_context_human": PAIN_CONTEXT},
            ),
        ),
        MockedSpikeScenario(
            "price_first",
            "quanto custa?",
            "whatsapp",
            _base_output(
                scenario_id="price_first",
                final_agent=PRODUCT_AGENT,
                intents=["price_question"],
                direct_question="quanto custa?",
                template_ids=["product.price_direct"],
                variables={"plan_price_summary": PRICE_SUMMARY},
                product_claims=[
                    _claim(
                        "price summary uses official plan facts",
                        "product_knowledge.prices",
                    )
                ],
                answer_obligations=[_answered("answer_price_before_diagnostic")],
            ),
        ),
        MockedSpikeScenario(
            "price_plus_pain",
            "qual o preco? meu WhatsApp esta caotico no follow-up",
            "whatsapp",
            _base_output(
                scenario_id="price_plus_pain",
                final_agent=PRODUCT_AGENT,
                intents=["price_question", "pain_context"],
                direct_question="qual o preco?",
                mixed_intent=True,
                template_ids=["product.price_direct", "diagnostic.price_hook_with_context"],
                variables={
                    "plan_price_summary": PRICE_SUMMARY,
                    "plan_fit_context": PLAN_FIT_CONTEXT,
                },
                product_claims=[
                    _claim(
                        "price summary uses official plan facts",
                        "product_knowledge.prices",
                    )
                ],
                answer_obligations=[_answered("answer_price_before_diagnostic")],
            ),
        ),
        MockedSpikeScenario(
            "diagnostic_start",
            "quero fazer o diagnostico gratuito",
            "whatsapp",
            _base_output(
                scenario_id="diagnostic_start",
                final_agent=DIAGNOSTIC_AGENT,
                intents=["diagnostic_start"],
                template_ids=["diagnostic.start", "diagnostic.ask_active_students"],
                diagnostic_proposal={
                    "ledger_updates": [],
                    "next_question_key": "active_students_or_size",
                    "final_diagnostic_ready": False,
                    "evidence": ["inbound.text"],
                },
            ),
        ),
        MockedSpikeScenario(
            "diagnostic_numeric_120",
            "120",
            "whatsapp",
            _base_output(
                scenario_id="diagnostic_numeric_120",
                final_agent=DIAGNOSTIC_AGENT,
                intents=["diagnostic_answer"],
                template_ids=["diagnostic.ask_main_pain"],
                variables={"answer_feedback": ANSWER_FEEDBACK_120},
                diagnostic_proposal={
                    "ledger_updates": [
                        {
                            "question_key": "active_students_or_size",
                            "status": "answered",
                            "answer_value": "120",
                            "evidence": ["inbound.text"],
                        }
                    ],
                    "next_question_key": "main_pain",
                    "final_diagnostic_ready": False,
                    "evidence": ["inbound.text"],
                },
                extracted_facts=[
                    {
                        "key": "numeric_interpretation",
                        "kind": "student_count",
                        "raw_text": "120",
                        "value": 120,
                        "evidence": ["inbound.text"],
                    }
                ],
            ),
        ),
        MockedSpikeScenario(
            "diagnostic_urgency_final",
            "quero resolver agora",
            "whatsapp",
            _base_output(
                scenario_id="diagnostic_urgency_final",
                final_agent=DIAGNOSTIC_AGENT,
                intents=["diagnostic_complete"],
                template_ids=[
                    "diagnostic.deliver_hold",
                    "diagnostic.deliver_context",
                    "diagnostic.deliver_crm_base",
                    "diagnostic.deliver_operational_step",
                    "diagnostic.deliver_plan_recommendation",
                    "diagnostic.deliver_demo_not_offered",
                ],
                variables=DIAGNOSTIC_VARIABLES,
                diagnostic_proposal={
                    "ledger_updates": [
                        {
                            "question_key": "urgency",
                            "status": "answered",
                            "answer_value": "resolver agora",
                            "evidence": ["inbound.text"],
                        }
                    ],
                    "next_question_key": None,
                    "final_diagnostic_ready": True,
                    "evidence": ["diagnostic_ledger.complete"],
                },
                product_claims=[
                    _claim(
                        "plan recommendation uses official plan facts",
                        "product_knowledge.plans",
                    )
                ],
                chunk_policy="staged_diagnostic",
            ),
        ),
        MockedSpikeScenario(
            "whatsapp_scope",
            "a Taliya conecta no WhatsApp do meu studio?",
            "whatsapp",
            _base_output(
                scenario_id="whatsapp_scope",
                final_agent=PRODUCT_AGENT,
                intents=["whatsapp_scope_question"],
                direct_question="conecta no WhatsApp do meu studio?",
                template_ids=["product.whatsapp_direct"],
                variables={
                    "product_fact_summary": PRODUCT_WHATSAPP_FACT,
                    "official_demo_link": OFFICIAL_DEMO_LINK,
                },
                product_claims=[
                    _claim(
                        "WhatsApp scope uses official product facts",
                        "product_knowledge.whatsapp_scope",
                    )
                ],
                answer_obligations=[_answered("answer_whatsapp_scope_before_steering")],
            ),
        ),
        MockedSpikeScenario(
            "demo_request",
            "consigo ver funcionando?",
            "whatsapp",
            _base_output(
                scenario_id="demo_request",
                final_agent=PRODUCT_AGENT,
                intents=["demo_request"],
                direct_question="consigo ver funcionando?",
                template_ids=["product.demo_direct"],
                variables={"official_demo_link": OFFICIAL_DEMO_LINK},
                product_claims=[
                    _claim("demo link must be official", "product_knowledge.demo_link")
                ],
                answer_obligations=[_answered("answer_demo_request_before_steering")],
                demo_proposal={
                    "status": "offered",
                    "next_step": "offer_demo",
                    "evidence": ["product_knowledge.demo_link"],
                },
            ),
        ),
        MockedSpikeScenario(
            "waitlist_curiosity",
            "como funciona essa lista de espera?",
            "whatsapp",
            _base_output(
                scenario_id="waitlist_curiosity",
                final_agent=PRODUCT_AGENT,
                intents=["waitlist_curiosity"],
                direct_question="como funciona essa lista de espera?",
                template_ids=["opening.general_interest"],
                waitlist_proposal={
                    "eligibility": "unknown",
                    "intent": "curiosity",
                    "missing_details": [],
                    "evidence": ["inbound.text"],
                },
                answer_obligations=[_answered("answer_waitlist_curiosity_without_offering_join")],
            ),
        ),
        MockedSpikeScenario(
            "waitlist_contract_intent",
            "quero entrar na lista para contratar",
            "whatsapp",
            _base_output(
                scenario_id="waitlist_contract_intent",
                final_agent=WAITLIST_AGENT,
                intents=["waitlist_contract_intent"],
                template_ids=["waitlist.offer_after_contract_intent"],
                variables={"waitlist_context_summary": WAITLIST_CONTEXT},
                waitlist_proposal={
                    "eligibility": "eligible",
                    "intent": "contract",
                    "missing_details": ["studio_name", "city_state"],
                    "evidence": ["inbound.text"],
                },
                sales_stage="waitlist_offered",
            ),
        ),
        MockedSpikeScenario(
            "human_handoff",
            "quero falar com uma pessoa",
            "whatsapp",
            _base_output(
                scenario_id="human_handoff",
                final_agent=HANDOFF_AGENT,
                intents=["human_handoff_request"],
                template_ids=["handoff.acknowledge"],
                variables={"handoff_reason": HANDOFF_REASON},
                handoff_proposal={
                    "status": "requested",
                    "reason": "lead_requested_human",
                    "pause_required": True,
                    "evidence": ["inbound.text"],
                },
                state_patch_proposal={"handoff": {"status": "requested", "pause_ai": True}},
                sales_stage="handoff_requested",
            ),
        ),
        MockedSpikeScenario(
            "do_not_do_497",
            "plano de 497",
            "whatsapp",
            _base_output(
                scenario_id="do_not_do_497",
                final_agent=PRODUCT_AGENT,
                intents=["price_question"],
                direct_question="plano de 497",
                template_ids=["product.price_direct"],
                variables={"plan_price_summary": PRICE_SUMMARY},
                product_claims=[
                    _claim(
                        "R$ 497 is a plan price, not student count",
                        "product_knowledge.prices",
                    )
                ],
                answer_obligations=[_answered("answer_price_before_diagnostic")],
                extracted_facts=[
                    {
                        "key": "numeric_interpretation",
                        "kind": "plan_price",
                        "raw_text": "497",
                        "value": 497,
                        "currency": "BRL",
                        "evidence": ["inbound.text", "product_knowledge.prices"],
                    }
                ],
            ),
        ),
        MockedSpikeScenario(
            "do_not_do_checkout_discount_date_vip",
            "tem checkout, desconto, data garantida ou VIP?",
            "whatsapp",
            _base_output(
                scenario_id="do_not_do_checkout_discount_date_vip",
                final_agent=PRODUCT_AGENT,
                intents=["unsupported_commercial_claim_question"],
                direct_question="tem checkout, desconto, data garantida ou VIP?",
                template_ids=["fallback.product_knowledge_missing"],
                variables={"human_confirmation_topic": HUMAN_CONFIRMATION_TOPIC},
                answer_obligations=[_answered("avoid_unofficial_checkout_discount_date_vip_promise")],
                risks=["unsupported_claims_blocked"],
            ),
        ),
        MockedSpikeScenario(
            "delivery_concurrency",
            "nova mensagem chegou enquanto os chunks estavam saindo",
            "whatsapp",
            _base_output(
                scenario_id="delivery_concurrency",
                final_agent=HANDOFF_AGENT,
                intents=["delivery_concurrency"],
                template_ids=["handoff.paused"],
                state_patch_proposal={
                    "delivery": {
                        "defer_inbound_during_chunks": True,
                        "deferred_inbound_count": 1,
                    }
                },
                risks=["delivery_concurrency_requires_runtime_gate_t012_036"],
            ),
        ),
    ]


@pytest.mark.parametrize("scenario", _scenarios(), ids=lambda scenario: scenario.scenario_id)
@pytest.mark.asyncio
async def test_spec012_mocked_sdk_contract_scenarios_validate_and_render(
    scenario: MockedSpikeScenario,
) -> None:
    async def mocked_runner(_: IsolatedSdkSpikeInput) -> Mapping[str, Any]:
        return {
            "final_output": scenario.output,
            "new_items": [
                {
                    "type": "tool_call_item",
                    "agent": {"name": scenario.output["agent_path"][-1]["agent"]},
                    "name": "get_product_knowledge",
                }
            ],
        }

    spike_result = await run_isolated_sdk_spike(
        IsolatedSdkSpikeInput(
            conversation_id=f"conv_{scenario.scenario_id}",
            turn_id=f"turn_{scenario.scenario_id}",
            channel=scenario.channel,
            user_text=scenario.user_text,
        ),
        sdk_runner=mocked_runner,
    )
    proposal = adapt_sdk_output_to_turn_proposal(
        spike_result.sdk_output,
        turn_id=spike_result.turn_id,
        conversation_id=spike_result.conversation_id,
        channel=scenario.channel,
        starting_agent=TRIAGE_AGENT,
    )
    validated = validate_and_render_spike_output(proposal)

    assert spike_result.proof_type == "mocked"
    assert spike_result.paid_call_status == "not_run"
    assert spike_result.public_cutover is False
    assert proposal.usage.model == "mocked-sdk-no-cost"
    assert proposal.usage.cost_usd == 0
    assert proposal.usage.model_operations == 0
    assert proposal.delivery_proposal.render_plan_only is True
    assert validated.validator_result.status == "passed"
    assert validated.commits_state is False
    assert validated.public_delivery is False
    assert validated.rendered_preview
    assert all(message.text.strip() for message in validated.rendered_preview)
    assert all(
        obligation.answered_before_steering
        for obligation in proposal.answer_obligations
    )


def test_spec012_mocked_contract_covers_required_spike_scenarios() -> None:
    assert [scenario.scenario_id for scenario in _scenarios()] == [
        "cold_greeting",
        "pain_first",
        "price_first",
        "price_plus_pain",
        "diagnostic_start",
        "diagnostic_numeric_120",
        "diagnostic_urgency_final",
        "whatsapp_scope",
        "demo_request",
        "waitlist_curiosity",
        "waitlist_contract_intent",
        "human_handoff",
        "do_not_do_497",
        "do_not_do_checkout_discount_date_vip",
        "delivery_concurrency",
    ]


def test_spec012_mocked_contract_keeps_497_as_plan_price_not_student_count() -> None:
    scenario = next(item for item in _scenarios() if item.scenario_id == "do_not_do_497")
    extracted = scenario.output["commercial_understanding"]["extracted_facts"]

    assert extracted == [
        {
            "key": "numeric_interpretation",
            "kind": "plan_price",
            "raw_text": "497",
            "value": 497,
            "currency": "BRL",
            "evidence": ["inbound.text", "product_knowledge.prices"],
        }
    ]


def test_spec012_mocked_contract_does_not_offer_waitlist_for_curiosity() -> None:
    scenario = next(
        item for item in _scenarios() if item.scenario_id == "waitlist_curiosity"
    )

    assert scenario.output["waitlist_proposal"]["intent"] == "curiosity"
    assert "waitlist.offer_after_contract_intent" not in scenario.output[
        "template_proposal"
    ]["template_ids"]


def test_spec012_mocked_contract_persists_handoff_pause_as_proposal_only() -> None:
    scenario = next(item for item in _scenarios() if item.scenario_id == "human_handoff")

    assert scenario.output["handoff_proposal"]["pause_required"] is True
    assert scenario.output["state_patch_proposal"] == {
        "handoff": {"status": "requested", "pause_ai": True}
    }


def test_spec012_mocked_contract_defers_delivery_concurrency_without_public_delivery() -> None:
    scenario = next(
        item for item in _scenarios() if item.scenario_id == "delivery_concurrency"
    )

    assert scenario.output["delivery_proposal"]["chunk_policy"] == "whatsapp_max_3"
    assert scenario.output["state_patch_proposal"]["delivery"] == {
        "defer_inbound_during_chunks": True,
        "deferred_inbound_count": 1,
    }


def test_spec012_mocked_contract_tests_do_not_call_real_sdk_runner() -> None:
    import app.core.taliya_commercial_sdk.spike_runner as spike_runner
    import tests.test_spec012_sdk_mocked_contracts as contract_tests

    source = inspect.getsource(contract_tests)
    spike_source = inspect.getsource(spike_runner)
    forbidden_runner_call = ".".join(("Runner", "run"))
    forbidden_model = "OpenAI" + "ChatCompletionsModel"
    forbidden_paid_override = "paid_openai_approved" + "=True"
    assert forbidden_runner_call not in source
    assert forbidden_model not in source
    assert forbidden_paid_override not in source
    assert "require_paid_approval(approved=paid_openai_approved)" in spike_source
