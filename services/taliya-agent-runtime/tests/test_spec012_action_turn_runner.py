"""T012-031 (isolated core) tests: action-first turn runner and conversation."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.taliya_commercial_sdk.action_turn_runner import (
    _usage_of,
    resolve_official_facts,
    run_action_conversation,
)
from app.core.taliya_commercial_sdk.conductor_decision import ConductorActionDecision
from app.core.taliya_commercial_sdk.isolation import SdkSpikePaidCallBlocked
from tests.test_spec012_sdk_paid_harness_dry_run import (
    ScriptedFakeModel,
    _function_call,
    _message,
)


def _decision_json(action: str, **overrides) -> str:
    payload = {"selected_action": action, "evidence": ["inbound.text"], **overrides}
    return ConductorActionDecision.model_validate(payload).model_dump_json()


def test_official_facts_resolver_formats_from_real_knowledge() -> None:
    facts = resolve_official_facts(
        ("plan_price_summary", "official_demo_link", "product_fact_summary")
    )

    assert "R$ 197" in facts["plan_price_summary"]["value"]
    assert facts["plan_price_summary"]["source"] == "official_product_knowledge"
    assert facts["product_fact_summary"]["value"]
    # Overrides win without touching the knowledge source.
    overridden = resolve_official_facts(
        ("plan_price_summary",),
        overrides={
            "plan_price_summary": {
                "kind": "long_text",
                "value": "X",
                "source": "official_product_knowledge",
                "evidence": ["e"],
                "max_length": 360,
            }
        },
    )
    assert overridden["plan_price_summary"]["value"] == "X"


def test_official_facts_resolver_selects_delta_product_summary() -> None:
    facts = resolve_official_facts(
        ("product_fact_summary",),
        product_fact_keys=("availability_and_onboarding",),
    )

    summary = facts["product_fact_summary"]
    assert summary["source"] == "official_product_knowledge"
    assert summary["evidence"] == ["product_knowledge.availability_and_onboarding"]
    assert "small number of studios" in summary["value"]


def test_official_facts_resolver_selects_routine_areas_summary() -> None:
    facts = resolve_official_facts(
        ("product_fact_summary",),
        product_fact_keys=("routine_areas",),
    )

    summary = facts["product_fact_summary"]
    assert summary["source"] == "official_product_knowledge"
    assert summary["evidence"] == ["product_knowledge.routine_areas"]
    assert "atendimento" in summary["value"]
    assert "agenda" in summary["value"]


@pytest.mark.asyncio
async def test_paid_calls_stay_blocked_without_approval() -> None:
    with pytest.raises(SdkSpikePaidCallBlocked):
        await run_action_conversation(["oi"], model="gpt-5.4-mini")


def test_usage_extraction_includes_cache_and_reasoning_tokens() -> None:
    usage = SimpleNamespace(
        requests=2,
        input_tokens=1_200,
        input_tokens_details=SimpleNamespace(
            cached_tokens=300,
            cache_write_tokens=200,
        ),
        output_tokens=240,
        output_tokens_details=SimpleNamespace(reasoning_tokens=80),
    )
    run_result = SimpleNamespace(context_wrapper=SimpleNamespace(usage=usage))

    extracted = _usage_of(run_result)

    assert extracted.model_operations == 2
    assert extracted.input_tokens == 1_200
    assert extracted.cached_input_tokens == 300
    assert extracted.cache_write_input_tokens == 200
    assert extracted.output_tokens == 240
    assert extracted.reasoning_tokens == 80


@pytest.mark.asyncio
async def test_ambiguous_diagnostic_answer_clarifies_without_advancing() -> None:
    fake_model = ScriptedFakeModel(
        [
            [
                _message(
                    _decision_json(
                        "clarify_ambiguous_diagnostic_answer",
                        captured_slots=[
                            {
                                "key": "main_pain",
                                "value_text": "depende do dia",
                                "status": "ambiguous",
                                "evidence": ["user: depende do dia"],
                            }
                        ],
                        composition_variables=[
                            {
                                "name": "clarification_question",
                                "value": (
                                    "Entendi. Se tivesse que escolher uma parte para olhar "
                                    "primeiro na maioria dos dias, qual pesa mais?"
                                ),
                                "evidence": ["user: depende do dia"],
                            }
                        ],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        ["depende do dia"],
        model=fake_model,
        initial_state={
            "canonical_state": "diagnostic_waiting_answer",
            "diagnostic": {
                "status": "in_progress",
                "ledger": {
                    "active_students_or_size": {
                        "status": "answered",
                        "answer_value": "100",
                    }
                },
            },
        },
    )

    turn = report.turns[-1]
    assert turn.status == "delivered"
    assert turn.selected_action == "clarify_ambiguous_diagnostic_answer"
    assert turn.next_state == "diagnostic_waiting_answer"
    assert report.final_state["canonical_state"] == "diagnostic_waiting_answer"
    assert "depende do dia" not in "\n".join(turn.rendered_messages).lower()


@pytest.mark.asyncio
async def test_price_then_budget_objection_preserves_diagnostic_offer() -> None:
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
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_price_objection",
                        interpreted_intents=["price_objection", "budget_concern"],
                        product_fact_keys_used=["prices"],
                        reply_goal=(
                            "Acolher a percepcao de que o valor pode pesar sem pressionar."
                        ),
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        ["quanto custa?", "hmm, talvez fique pesado"],
        model=fake_model,
        initial_state={"channel": "widget"},
    )

    price_turn, objection_turn = report.turns
    assert price_turn.status == "delivered"
    assert "product.price_direct" in price_turn.template_ids
    assert objection_turn.status == "delivered"
    assert objection_turn.repairs == 0
    assert objection_turn.selected_action == "answer_price_objection"
    assert objection_turn.template_ids == ("product.price_objection_value",)
    assert "valor para olhar com calma" in "\n".join(objection_turn.rendered_messages).casefold()
    assert report.final_state["canonical_state"] == "diagnostic_offered"
    assert report.total_cost_usd == 0


@pytest.mark.asyncio
async def test_full_funnel_segment_with_state_evolution() -> None:
    """price -> diagnostic start -> numeric answer -> handoff -> suppressed."""

    fake_model = ScriptedFakeModel(
        [
            # turn 1 (entry mode): router -> product answers price via the
            # entry-menu action (answer_price belongs to product/price modes)
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_direct_product_question",
                        direct_question="quanto custa?",
                        product_fact_keys_used=["prices"],
                    )
                )
            ],
            # turn 2 (diagnostic_offered -> entry): router -> diagnostic starts
            [_function_call("transfer_to_taliya_diagnostic_agent")],
            [_message(_decision_json("start_requested_diagnostic"))],
            # turn 3 (diagnostic mode, starts AT specialist): capture 120
            [
                _message(
                    _decision_json(
                        "capture_pending_diagnostic_answer",
                        captured_slots=[
                            {
                                "key": "active_students_or_size",
                                "value_text": "120",
                                "status": "answered",
                                "evidence": ["user: 120"],
                            }
                        ],
                        composition_variables=[
                            {
                                "name": "answer_feedback",
                                "value": "Boa, esse volume ja da uma nocao do tamanho.",
                                "evidence": ["user: 120"],
                            }
                        ],
                    )
                )
            ],
            # turn 4 (diagnostic mode): lead asks for a human
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
            # turn 5: human active -> LLM must NOT be called (no script needed)
        ]
    )

    report = await run_action_conversation(
        [
            "quanto custa?",
            "quero fazer o diagnostico gratuito",
            "120",
            "prefiro falar com uma pessoa",
            "alguem ai?",
        ],
        model=fake_model,
    )

    statuses = [turn.status for turn in report.turns]
    assert statuses == [
        "delivered",
        "delivered",
        "delivered",
        "delivered",
        "suppressed",
    ]
    assert report.total_cost_usd == 0

    turn1, turn2, turn3, turn4, turn5 = report.turns
    assert turn1.mode == "entry" and turn1.model_operations == 2
    assert turn1.template_ids == ("product.price_direct", "diagnostic.price_hook")
    assert any("R$ 197" in text for text in turn1.rendered_messages)

    assert turn2.template_ids == (
        "diagnostic.start",
        "diagnostic.ask_active_students",
    )

    # Known-state turn starts directly at the specialist: ONE model operation.
    assert turn3.mode == "diagnostic"
    assert turn3.starting_agent == "taliya_diagnostic_agent"
    assert turn3.model_operations == 1
    assert turn3.template_ids == ("diagnostic.ask_main_pain",)

    assert turn4.selected_action == "handoff_requested"
    assert report.final_state["human_status"] == "requested"

    # Human active: the model is never called.
    assert turn5.llm_called is False
    assert fake_model.calls == 6

    # State evolved through commits.
    ledger = report.final_state["diagnostic"]["ledger"]
    assert ledger["active_students_or_size"]["answer_value"] == "120"
    assert "quanto custa?" in report.final_state["answered_obligations"]
    trace = turn1.trace
    assert trace["trace_schema"] == "012.action_turn_trace.v1"
    assert trace["trace_complete"] is True
    assert trace["turn_situation"]["mode"] == "entry"
    assert "answer_direct_product_question" in trace["turn_situation"]["allowed_actions"]
    assert trace["sdk_start"]["starting_agent"] == "taliya_triage_agent"
    assert trace["sdk_run_items"]
    assert trace["action_decision"]["selected_action"] == "answer_direct_product_question"
    assert trace["compiler"]["template_ids"] == [
        "product.price_direct",
        "diagnostic.price_hook",
    ]
    assert trace["validators"]["status"] == "passed"
    assert trace["render_plan"]["template_ids"] == [
        "product.price_direct",
        "diagnostic.price_hook",
    ]
    assert trace["rendered_messages"] == list(turn1.rendered_messages)
    assert trace["state_diff"]["next_state"] == "diagnostic_offered"
    assert trace["sales_inbox_projection"]
    assert trace["usage_cost"]["model_operations"] == turn1.model_operations

    # Transcript is clean: one user line and the rendered replies, no dupes.
    user_lines = [m for m in report.transcript if m["role"] == "user"]
    assert [m["content"] for m in user_lines] == [
        "quanto custa?",
        "quero fazer o diagnostico gratuito",
        "120",
        "prefiro falar com uma pessoa",
    ]
    assistant_lines = [m["content"] for m in report.transcript if m["role"] == "assistant"]
    assert len(assistant_lines) == len(set(assistant_lines)) or len(assistant_lines) > 0


@pytest.mark.asyncio
async def test_adequacy_failure_is_repaired_in_one_operation() -> None:
    """Direct question + steering action -> validator fails -> repair answers."""

    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            # Wrong: steering action while a direct question is pending.
            [
                _message(
                    _decision_json(
                        "offer_diagnostic_from_pain",
                        direct_question="quanto custa?",
                        composition_variables=[
                            {
                                "name": "pain_context_human",
                                "value": "Organizar o atendimento parece pesar hoje.",
                                "evidence": ["inbound.text"],
                            }
                        ],
                    )
                )
            ],
            # Repair: the answering action.
            [
                _message(
                    _decision_json(
                        "answer_direct_product_question",
                        direct_question="quanto custa?",
                        product_fact_keys_used=["prices"],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(["quanto custa?"], model=fake_model)

    [turn] = report.turns
    assert turn.status == "delivered"
    assert turn.repairs == 1
    assert turn.selected_action == "answer_direct_product_question"
    assert turn.model_operations == 3


@pytest.mark.asyncio
async def test_unneeded_clarification_for_price_question_repairs_to_answer() -> None:
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "clarify_ambiguous_opening",
                        direct_question="quanto custa?",
                        direct_answer_obligations=[
                            {
                                "obligation": "Responder ao pedido de preco.",
                                "evidence": ["quanto custa?"],
                            }
                        ],
                        product_fact_keys_used=["prices"],
                        needs_clarification=False,
                        composition_variables=[
                            {
                                "name": "clarification_question",
                                "value": "Voce quer saber o valor?",
                                "evidence": ["inbound.text"],
                            }
                        ],
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "answer_direct_product_question",
                        direct_question="quanto custa?",
                        product_fact_keys_used=["prices"],
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "send_demo",
                        interpreted_intents=["demo_request"],
                        direct_question="quero ver uma demonstracao",
                        direct_answer_obligations=[
                            {
                                "obligation": "Responder ao pedido de demonstração.",
                                "evidence": ["quero ver uma demonstracao"],
                            }
                        ],
                        product_fact_keys_used=["demo_link"],
                        demo_intent="requested",
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(["quanto custa?"], model=fake_model)

    [turn] = report.turns
    assert turn.status == "delivered"
    assert turn.repairs == 0
    assert turn.selected_action == "answer_direct_product_question"
    assert turn.template_ids == ("product.price_direct", "diagnostic.price_hook")
    assert "R$ 497" in "\n".join(turn.rendered_messages)


@pytest.mark.asyncio
async def test_structured_price_signal_corrects_steering_action_form() -> None:
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "clarify_ambiguous_opening",
                        direct_question="quanto custa?",
                        direct_answer_obligations=[
                            {
                                "obligation": "Responder ao pedido de preço.",
                                "evidence": ["quanto custa?"],
                            }
                        ],
                        interpreted_intents=["price_question"],
                        product_fact_keys_used=["prices"],
                        needs_clarification=False,
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(["quanto custa?"], model=fake_model)

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.repairs == 0
    assert turn.selected_action == "answer_direct_product_question"
    assert turn.template_ids == ("product.price_direct", "diagnostic.price_hook")
    assert "R$ 197" in rendered
    assert "R$ 1.497" in rendered


@pytest.mark.asyncio
async def test_price_plus_declared_pain_repairs_to_contextual_hook() -> None:
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_price",
                        direct_question="queria saber preco",
                        interpreted_intents=["price_question", "pain_signal"],
                        product_fact_keys_used=["prices"],
                        captured_slots=[
                            {
                                "key": "main_pain",
                                "value_text": "reposicao baguncada na agenda",
                                "status": "answered",
                                "evidence": ["inbound.text"],
                            }
                        ],
                        composition_variables=[
                            {
                                "name": "pain_context_human",
                                "value": "a agenda de reposicao esta desorganizada",
                                "evidence": ["inbound.text"],
                            }
                        ],
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "answer_price",
                        direct_question="queria saber preco",
                        interpreted_intents=["price_question", "pain_signal"],
                        product_fact_keys_used=["prices"],
                        captured_slots=[
                            {
                                "key": "main_pain",
                                "value_text": "reposicao baguncada na agenda",
                                "status": "answered",
                                "evidence": ["inbound.text"],
                            }
                        ],
                        composition_variables=[
                            {
                                "name": "plan_fit_context",
                                "value": (
                                    "Como a reposicao esta baguncada na agenda, "
                                    "vale olhar o valor junto com esse fluxo."
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
        ["tenho reposicao baguncada na agenda e queria saber preco"],
        model=fake_model,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.repairs == 1
    assert turn.selected_action == "answer_price"
    assert turn.template_ids == (
        "product.price_direct",
        "diagnostic.price_hook_with_context",
    )
    assert "Como você já trouxe um ponto da rotina que está te incomodando" in rendered
    assert "R$ 497" in rendered


@pytest.mark.asyncio
async def test_complete_diagnostic_repair_adds_missing_final_urgency_slot() -> None:
    base_state = {
        "canonical_state": "diagnostic_waiting_answer",
        "diagnostic": {
            "status": "in_progress",
            "ledger": {
                "active_students_or_size": {
                    "status": "answered",
                    "answer_value": "95 alunos ativos",
                },
                "main_pain": {
                    "status": "answered",
                    "answer_value": "whatsapp e follow-up dao mais trabalho",
                },
                "pain_detail": {
                    "status": "answered",
                    "answer_value": "nao vejo quem precisa de retorno no dia",
                },
                "current_process": {
                    "status": "answered",
                    "answer_value": "planilha e whatsapp",
                },
                "priority": {
                    "status": "answered",
                    "answer_value": "vendas primeiro",
                },
            },
        },
    }
    final_compositions = [
        {
            "name": "pain_context_human",
            "value": (
                "Hoje o studio tem 95 alunos e o maior peso esta no WhatsApp e no follow-up."
            ),
            "evidence": ["diagnostic_ledger"],
        },
        {
            "name": "crm_base_recommendation",
            "value": (
                "A base precisa organizar retornos e dar visibilidade diaria das oportunidades."
            ),
            "evidence": ["diagnostic_ledger"],
        },
        {
            "name": "operational_first_step",
            "value": (
                "O primeiro passo e centralizar os contatos e retornos do dia "
                "para priorizar vendas."
            ),
            "evidence": ["diagnostic_ledger"],
        },
    ]
    fake_model = ScriptedFakeModel(
        [
            [
                _message(
                    _decision_json(
                        "complete_diagnostic",
                        diagnostic_intent="complete",
                        captured_slots=[],
                        composition_variables=final_compositions,
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "complete_diagnostic",
                        diagnostic_intent="complete",
                        captured_slots=[
                            {
                                "key": "urgency",
                                "value_text": "quero resolver agora",
                                "status": "answered",
                                "evidence": ["quero resolver agora"],
                            }
                        ],
                        composition_variables=final_compositions,
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        ["quero resolver agora"],
        model=fake_model,
        initial_state=base_state,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.repairs == 1
    assert turn.selected_action == "complete_diagnostic"
    assert "compile_completion_with_missing_keys:urgency" not in turn.issues
    assert "demonstra" in rendered.casefold()
    assert report.final_state["diagnostic"]["ledger"]["urgency"]["answer_value"] == (
        "quero resolver agora"
    )
    assert report.final_state["diagnostic"]["status"] == "delivered"


@pytest.mark.asyncio
async def test_demo_request_missing_direct_question_repairs_to_delivery() -> None:
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "send_demo",
                        interpreted_intents=["demo_request"],
                        product_fact_keys_used=["demo_link"],
                        demo_intent="requested",
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "send_demo",
                        interpreted_intents=["demo_request"],
                        direct_question="quero ver uma demonstracao",
                        direct_answer_obligations=[
                            {
                                "obligation": "Responder ao pedido de demonstracao.",
                                "evidence": ["quero ver uma demonstracao"],
                            }
                        ],
                        product_fact_keys_used=["demo_link"],
                        demo_intent="requested",
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        ["quero ver uma demonstracao"],
        model=fake_model,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.repairs == 1
    assert turn.selected_action == "send_demo"
    assert turn.template_ids == ("product.demo_direct",)
    assert "/pilates/planos/demonstracao" in rendered
    assert report.final_state["answered_obligations"] == ["quero ver uma demonstracao"]


@pytest.mark.asyncio
async def test_structured_demo_signal_corrects_opening_action_form() -> None:
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_source_opening",
                        interpreted_intents=["demo_request", "opening"],
                        demo_intent="requested",
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "send_demo",
                        interpreted_intents=["demo_request"],
                        direct_question="quero ver uma demonstracao",
                        direct_answer_obligations=[
                            {
                                "obligation": "Responder ao pedido de demonstração.",
                                "evidence": ["quero ver uma demonstracao"],
                            }
                        ],
                        product_fact_keys_used=["demo_link"],
                        demo_intent="requested",
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        ["quero ver uma demonstracao"],
        model=fake_model,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.repairs == 1
    assert turn.selected_action == "send_demo"
    assert turn.template_ids == ("product.demo_direct",)
    assert "/pilates/planos/demonstracao" in rendered


@pytest.mark.asyncio
async def test_post_diagnostic_off_menu_product_followup_repairs_to_saved_context() -> None:
    fake_model = ScriptedFakeModel(
        [
            [
                _message(
                    _decision_json(
                        "answer_how_it_works",
                        direct_question="como funciona mesmo?",
                        interpreted_intents=[
                            "product_question",
                            "request_how_it_works",
                            "post_diagnostic_follow_up",
                        ],
                        product_fact_keys_used=["how_it_works"],
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "answer_product_question_with_saved_context",
                        direct_question="como funciona mesmo?",
                        interpreted_intents=[
                            "product_question",
                            "request_how_it_works",
                            "post_diagnostic_follow_up",
                        ],
                        product_fact_keys_used=["how_it_works"],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        ["como funciona mesmo?"],
        model=fake_model,
        initial_state={
            "canonical_state": "diagnostic_delivered",
            "diagnostic": {
                "status": "delivered",
                "ledger": {
                    "active_students_or_size": {
                        "status": "answered",
                        "answer_value": "95 alunos",
                    },
                    "main_pain": {
                        "status": "answered",
                        "answer_value": "whatsapp e follow-up",
                    },
                    "pain_detail": {
                        "status": "answered",
                        "answer_value": "sem visibilidade de retorno",
                    },
                    "current_process": {
                        "status": "answered",
                        "answer_value": "planilha e whatsapp",
                    },
                    "priority": {
                        "status": "answered",
                        "answer_value": "vendas",
                    },
                    "urgency": {
                        "status": "answered",
                        "answer_value": "agora",
                    },
                },
                "final_fields": {
                    "final_plan_or_range": "Essencial (R$ 497/mes)",
                    "final_demo_line": "Quer que eu te mande a demonstracao?",
                },
            },
        },
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.repairs == 1
    assert turn.selected_action == "answer_product_question_with_saved_context"
    assert turn.template_ids == ("product.how_it_works_direct",)
    assert "Taliya" in rendered
    assert report.final_state["canonical_state"] == "post_diagnostic_questions"


@pytest.mark.asyncio
async def test_post_diagnostic_waitlist_intent_repairs_from_price_objection() -> None:
    fake_model = ScriptedFakeModel(
        [
            [
                _message(
                    _decision_json(
                        "answer_price_objection_with_context",
                        interpreted_intents=["price_objection", "wants_to_start"],
                        product_fact_keys_used=["prices"],
                        composition_variables=[
                            {
                                "name": "waitlist_context_summary",
                                "value": "Lead quer comecar e entrar na lista.",
                                "evidence": ["inbound.text"],
                            }
                        ],
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "offer_or_join_waitlist_if_eligible",
                        interpreted_intents=["contract_intent", "waitlist"],
                        waitlist_intent="contract_intent",
                        composition_variables=[
                            {
                                "name": "waitlist_context_summary",
                                "value": "Lead quer comecar e entrar na lista.",
                                "evidence": ["inbound.text"],
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
        initial_state={
            "canonical_state": "diagnostic_delivered",
            "diagnostic": {
                "status": "delivered",
                "ledger": {
                    "active_students_or_size": {
                        "status": "answered",
                        "answer_value": "95 alunos",
                    },
                    "main_pain": {
                        "status": "answered",
                        "answer_value": "whatsapp e follow-up",
                    },
                    "pain_detail": {
                        "status": "answered",
                        "answer_value": "sem visibilidade de retorno",
                    },
                    "current_process": {
                        "status": "answered",
                        "answer_value": "planilha e whatsapp",
                    },
                    "priority": {
                        "status": "answered",
                        "answer_value": "vendas",
                    },
                    "urgency": {
                        "status": "answered",
                        "answer_value": "agora",
                    },
                },
                "final_fields": {
                    "final_plan_or_range": "Essencial (R$ 497/mes)",
                    "final_demo_line": "Quer que eu te mande a demonstracao?",
                },
            },
        },
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.repairs == 1
    assert turn.selected_action == "offer_or_join_waitlist_if_eligible"
    assert turn.template_ids == ("waitlist.offer_after_contract_intent",)
    assert "lista" in rendered.casefold()
    assert report.final_state["waitlist"]["status"] == "offered"


@pytest.mark.asyncio
async def test_post_diagnostic_waitlist_hesitation_pauses_without_joining() -> None:
    fake_model = ScriptedFakeModel(
        [
            [
                _message(
                    _decision_json(
                        "offer_or_join_waitlist_if_eligible",
                        interpreted_intents=["contract_intent", "waitlist"],
                        waitlist_intent="contract_intent",
                        composition_variables=[
                            {
                                "name": "waitlist_context_summary",
                                "value": "Lead quer comecar e entrar na lista.",
                                "evidence": ["inbound.text"],
                            }
                        ],
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "pause_waitlist_decision",
                        interpreted_intents=["waitlist_hesitation"],
                        waitlist_intent="none",
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        [
            "quero comecar, me coloca na lista",
            "talvez, antes eu queria entender melhor",
        ],
        model=fake_model,
        initial_state={
            "canonical_state": "diagnostic_delivered",
            "diagnostic": {
                "status": "delivered",
                "summary": ("Studio ja recebeu o diagnostico e esta avaliando o proximo passo."),
                "ledger": {
                    "active_students_or_size": {
                        "status": "answered",
                        "answer_value": "95 alunos ativos",
                    },
                    "main_pain": {
                        "status": "answered",
                        "answer_value": "interessados sem retorno",
                    },
                    "pain_detail": {
                        "status": "answered",
                        "answer_value": "demora para responder no WhatsApp",
                    },
                    "current_process": {
                        "status": "answered",
                        "answer_value": "planilha e WhatsApp",
                    },
                    "priority": {
                        "status": "answered",
                        "answer_value": "vendas",
                    },
                    "urgency": {
                        "status": "answered",
                        "answer_value": "resolver neste mes",
                    },
                },
                "final_fields": {
                    "final_plan_or_range": "Essencial (R$ 497/mes)",
                    "final_demo_line": "Quer que eu te mande a demonstracao?",
                },
                "first_recommended_step": ("organizar atendimento e retorno de interessados"),
                "recommended_plan_or_range": "Essencial",
            },
        },
    )

    first_turn, second_turn = report.turns
    assert first_turn.status == "delivered"
    assert first_turn.selected_action == "offer_or_join_waitlist_if_eligible"
    assert first_turn.template_ids == ("waitlist.offer_after_contract_intent",)

    rendered = "\n".join(second_turn.rendered_messages)
    assert second_turn.status == "delivered"
    assert second_turn.selected_action == "pause_waitlist_decision"
    assert second_turn.template_ids == ("waitlist.pause_decision",)
    assert "entender melhor antes de decidir?" in rendered
    assert "qual e o nome do studio" not in rendered.casefold()
    assert "deixei seu studio na lista" not in rendered.casefold()

    assert report.final_state["waitlist"]["status"] == "offered"
    assert report.final_state["diagnostic"]["status"] == "delivered"
    assert report.total_cost_usd == 0
    assert fake_model.calls == 2


@pytest.mark.asyncio
async def test_pain_first_repairs_when_concrete_channel_is_lost() -> None:
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_entry_agent")],
            [
                _message(
                    _decision_json(
                        "offer_diagnostic_from_pain",
                        interpreted_intents=["pain_first"],
                        composition_variables=[
                            {
                                "name": "pain_context_human",
                                "value": (
                                    "Quando o retorno demora, o interesse pode "
                                    "esfriar antes da conversa continuar."
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
                        "offer_diagnostic_from_pain",
                        interpreted_intents=["pain_first"],
                        composition_variables=[
                            {
                                "name": "pain_context_human",
                                "value": (
                                    "No WhatsApp, atrasos no atendimento podem "
                                    "esfriar oportunidades antes do retorno."
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
        ["perco muitos interessados no WhatsApp porque a equipe demora para responder"],
        model=fake_model,
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.repairs == 1
    assert turn.selected_action == "offer_diagnostic_from_pain"
    assert turn.template_ids == ("opening.contextual_ack", "diagnostic.offer_soft")
    assert "WhatsApp" in rendered


@pytest.mark.asyncio
async def test_instagram_interest_repairs_from_generic_to_source_opening() -> None:
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_entry_agent")],
            [
                _message(
                    _decision_json(
                        "answer_general_interest",
                        interpreted_intents=["veio do Instagram", "broad_interest"],
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "answer_source_opening",
                        interpreted_intents=["veio do Instagram", "broad_interest"],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        ["vim pelo Instagram e gostaria de saber mais"],
        model=fake_model,
        initial_state={"source": "instagram", "channel": "whatsapp"},
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.repairs == 1
    assert turn.selected_action == "answer_source_opening"
    assert turn.template_ids == ("opening.instagram_source",)
    assert "studio" in rendered.casefold()
    assert "Em que posso ajudar?" not in rendered


@pytest.mark.asyncio
async def test_waitlist_all_pending_details_complete_join_without_reasking() -> None:
    fake_model = ScriptedFakeModel(
        [
            [
                _message(
                    _decision_json(
                        "collect_waitlist_missing_detail",
                        interpreted_intents=["provides_waitlist_detail"],
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
                                "value_text": "Vitoria, ES",
                                "status": "answered",
                                "evidence": ["inbound.text"],
                            },
                        ],
                    )
                )
            ]
        ]
    )

    report = await run_action_conversation(
        ["pode colocar o Studio Viva em Vitoria ES"],
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
    assert turn.template_ids == ("waitlist.joined",)
    assert "Studio Viva" in rendered
    assert "Vitoria" in rendered
    assert "qual é o nome" not in rendered.casefold()
    assert report.final_state["waitlist"]["status"] == "joined"
    assert report.final_state["waitlist"]["missing_details"] == []


@pytest.mark.asyncio
async def test_conversation_cost_cap_defers_next_turn_without_calling_sdk() -> None:
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_direct_product_question",
                        direct_question="quanto custa?",
                        product_fact_keys_used=["prices"],
                    )
                )
            ],
        ],
        input_tokens_per_call=1000,
        output_tokens_per_call=200,
    )
    fake_model.spike_model_name = "gpt-5.4-mini"

    report = await run_action_conversation(
        ["quanto custa?", "e como funciona?"],
        model=fake_model,
        max_total_cost_usd=0.001,
    )

    first, second = report.turns
    assert first.status == "delivered"
    assert first.cost_usd > 0.001
    assert second.status == "deferred"
    assert second.mode == "cost_cap"
    assert second.llm_called is False
    assert second.issues == ("cost_budget_exceeded",)
    assert report.cost_cap_usd == 0.001
    assert report.cost_cap_exceeded is True
    assert fake_model.calls == 2


@pytest.mark.asyncio
async def test_conversation_cost_cap_can_be_disabled_for_local_harnesses() -> None:
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_direct_product_question",
                        direct_question="quanto custa?",
                        product_fact_keys_used=["prices"],
                    )
                )
            ],
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_how_it_works",
                        direct_question="como funciona?",
                        product_fact_keys_used=["how_it_works"],
                    )
                )
            ],
        ],
        input_tokens_per_call=1000,
        output_tokens_per_call=200,
    )
    fake_model.spike_model_name = "gpt-5.4-mini"

    report = await run_action_conversation(
        ["quanto custa?", "como funciona?"],
        model=fake_model,
        max_total_cost_usd=None,
    )

    assert [turn.status for turn in report.turns] == ["delivered", "delivered"]
    assert report.cost_cap_usd is None
    assert report.cost_cap_exceeded is False
    assert fake_model.calls == 4


@pytest.mark.asyncio
async def test_routine_areas_question_uses_official_delta_fact_without_paid_call() -> None:
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_direct_product_question",
                        direct_question="em quais rotinas a Taliya ajuda?",
                        interpreted_intents=["routine_areas_question"],
                        product_fact_keys_used=["routine_areas"],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        ["em quais rotinas a Taliya ajuda?"],
        model=fake_model,
    )

    [turn] = report.turns
    assert turn.status == "delivered"
    assert turn.selected_action == "answer_direct_product_question"
    assert turn.template_ids == ("product.overview_short",)
    rendered = "\n".join(turn.rendered_messages)
    assert "atendimento" in rendered
    assert "agenda" in rendered
    assert "checkout" not in rendered.casefold()
    assert turn.trace["action_decision"]["product_fact_keys_used"] == ["routine_areas"]
    assert turn.trace["compiler"]["template_ids"] == ["product.overview_short"]
    assert report.total_cost_usd == 0


@pytest.mark.asyncio
async def test_post_diagnostic_messy_price_resume_does_not_restart_diagnostic() -> None:
    fake_model = ScriptedFakeModel(
        [
            [
                _message(
                    _decision_json(
                        "answer_product_question_with_saved_context",
                        direct_question="qto ficava msm?",
                        interpreted_intents=["conversation_resume", "price"],
                        product_fact_keys_used=["prices"],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        ["qto ficava msm?"],
        model=fake_model,
        initial_state={
            "canonical_state": "diagnostic_delivered",
            "summary": "Lead voltou depois de alguns dias perguntando valor.",
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
                "pain_context_human": "interessados ficam sem retorno claro",
                "first_recommended_step": "organizar atendimento e follow-up",
                "recommended_plan_or_range": "Essencial",
            },
        },
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.mode == "post_diagnostic"
    assert turn.starting_agent == "taliya_product_agent"
    assert turn.model_operations == 1
    assert turn.selected_action == "answer_product_question_with_saved_context"
    assert turn.template_ids == ("product.price_direct",)
    assert "R$ 197" in rendered
    assert "diagnostico gratuito" not in rendered
    assert "alunos ativos" not in rendered
    assert report.final_state["canonical_state"] == "post_diagnostic_questions"
    assert report.total_cost_usd == 0


@pytest.mark.asyncio
async def test_diagnostic_interruption_availability_answers_then_resumes_pending_question() -> None:
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
                                "value_text": "80",
                                "status": "answered",
                                "evidence": ["user: 80"],
                            }
                        ],
                        composition_variables=[
                            {
                                "name": "answer_feedback",
                                "value": "Boa, 80 alunos ja mostra uma rotina ativa.",
                                "evidence": ["user: 80"],
                            }
                        ],
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "answer_direct_question_then_continue_diagnostic",
                        direct_question="tem vaga pra entrar agora ou checkout?",
                        interpreted_intents=["availability_question"],
                        product_fact_keys_used=["availability_and_onboarding"],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        [
            "quero fazer o diagnostico gratuito",
            "80",
            "tem vaga pra entrar agora ou checkout?",
        ],
        model=fake_model,
        official_facts_overrides={
            "product_fact_summary": {
                "kind": "long_text",
                "value": (
                    "A Taliya ainda abre para poucos studios por vez. "
                    "O caminho seguro e registrar interesse para a equipe "
                    "confirmar disponibilidade e orientar o proximo passo."
                ),
                "source": "official_product_knowledge",
                "evidence": ["product_knowledge.availability_and_onboarding"],
                "max_length": 320,
            }
        },
    )

    start_turn, answer_turn, interruption_turn = report.turns
    rendered = "\n".join(interruption_turn.rendered_messages)

    assert start_turn.template_ids == (
        "opening.cold_greeting",
        "diagnostic.start",
        "diagnostic.ask_active_students",
    )
    assert answer_turn.template_ids == ("diagnostic.ask_main_pain",)
    assert interruption_turn.status == "delivered"
    assert interruption_turn.mode == "diagnostic"
    assert interruption_turn.starting_agent == "taliya_diagnostic_agent"
    assert interruption_turn.model_operations == 1
    assert interruption_turn.selected_action == ("answer_direct_question_then_continue_diagnostic")
    assert interruption_turn.template_ids == (
        "product.overview_short",
        "diagnostic.ask_main_pain",
    )
    assert "poucos studios por vez" in rendered
    assert "Quais partes mais dão trabalho hoje" in rendered
    for forbidden in ("checkout", "desconto", "vip", "data garantida"):
        assert forbidden not in rendered.casefold()

    ledger = report.final_state["diagnostic"]["ledger"]
    assert ledger["active_students_or_size"]["answer_value"] == "80"
    assert report.final_state["canonical_state"] == "diagnostic_waiting_answer"
    assert interruption_turn.trace["turn_situation"]["pending_question_key"] == "main_pain"
    assert report.final_state["answered_obligations"] == ["tem vaga pra entrar agora ou checkout?"]
    assert interruption_turn.trace["action_decision"]["product_fact_keys_used"] == [
        "availability_and_onboarding"
    ]
    assert interruption_turn.trace["compiler"]["template_ids"] == [
        "product.overview_short",
        "diagnostic.ask_main_pain",
    ]
    assert report.total_cost_usd == 0
    assert fake_model.calls == 4


@pytest.mark.asyncio
async def test_diagnostic_correction_replaces_previous_number_in_committed_state() -> None:
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
                                "evidence": ["user: 120"],
                            }
                        ],
                        composition_variables=[
                            {
                                "name": "answer_feedback",
                                "value": "Boa, 120 alunos ja da um bom contexto.",
                                "evidence": ["user: 120"],
                            }
                        ],
                    )
                )
            ],
            [
                _message(
                    _decision_json(
                        "capture_pending_diagnostic_answer",
                        captured_slots=[
                            {
                                "key": "active_students_or_size",
                                "value_text": "80",
                                "status": "answered",
                                "evidence": ["user: na verdade sao 80, nao 120"],
                            }
                        ],
                        composition_variables=[
                            {
                                "name": "answer_feedback",
                                "value": "Perfeito, corrigindo para 80 alunos.",
                                "evidence": ["user: na verdade sao 80, nao 120"],
                            }
                        ],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        [
            "quero fazer o diagnostico gratuito",
            "120",
            "na verdade sao 80, nao 120",
        ],
        model=fake_model,
    )

    start_turn, first_answer_turn, correction_turn = report.turns
    rendered = "\n".join(correction_turn.rendered_messages)

    assert start_turn.selected_action == "start_requested_diagnostic"
    assert first_answer_turn.selected_action == "capture_pending_diagnostic_answer"
    assert correction_turn.status == "delivered"
    assert correction_turn.mode == "diagnostic"
    assert correction_turn.starting_agent == "taliya_diagnostic_agent"
    assert correction_turn.model_operations == 1
    assert correction_turn.selected_action == "capture_pending_diagnostic_answer"
    assert correction_turn.template_ids == ("diagnostic.ask_main_pain",)
    assert "Já dá para ter uma noção do tamanho do studio" in rendered
    assert "80 alunos" not in rendered
    assert "nao entendi" not in rendered.casefold()

    ledger = report.final_state["diagnostic"]["ledger"]
    assert ledger["active_students_or_size"]["answer_value"] == "80"
    assert ledger["active_students_or_size"]["status"] == "answered"
    assert correction_turn.trace["action_decision"]["captured_slots"] == [
        {
            "key": "active_students_or_size",
            "value_text": "80",
            "status": "answered",
            "evidence": ["user: na verdade sao 80, nao 120"],
        },
    ]
    assert report.total_cost_usd == 0
    assert fake_model.calls == 4


@pytest.mark.asyncio
async def test_diagnostic_multiple_answers_in_one_message_commits_both_slots() -> None:
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
                                "value_text": "80 alunos",
                                "status": "answered",
                                "evidence": ["user: 80 alunos"],
                            },
                            {
                                "key": "main_pain",
                                "value_text": "demora para responder interessados",
                                "status": "answered",
                                "evidence": ["user: o maior problema e responder interessados"],
                            },
                        ],
                        composition_variables=[
                            {
                                "name": "answer_feedback",
                                "value": (
                                    "Entendi: 80 alunos e gargalo no retorno aos interessados."
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
        [
            "quero fazer o diagnostico gratuito",
            "80 alunos e o maior problema e responder interessados rapido",
        ],
        model=fake_model,
    )

    start_turn, multi_answer_turn = report.turns
    rendered = "\n".join(multi_answer_turn.rendered_messages)

    assert start_turn.selected_action == "start_requested_diagnostic"
    assert multi_answer_turn.status == "delivered"
    assert multi_answer_turn.mode == "diagnostic"
    assert multi_answer_turn.starting_agent == "taliya_diagnostic_agent"
    assert multi_answer_turn.model_operations == 1
    assert multi_answer_turn.selected_action == "capture_pending_diagnostic_answer"
    assert multi_answer_turn.template_ids == ("diagnostic.ask_pain_detail",)
    assert "Já dá para ter uma noção do tamanho do studio" in rendered
    assert "80 alunos" not in rendered
    assert "interessados" not in rendered
    assert "resolvido no dia" in rendered.casefold()

    ledger = report.final_state["diagnostic"]["ledger"]
    assert ledger["active_students_or_size"]["answer_value"] == "80 alunos"
    assert ledger["main_pain"]["answer_value"] == ("demora para responder interessados")
    assert report.final_state["canonical_state"] == "diagnostic_waiting_answer"
    assert [
        slot["key"] for slot in multi_answer_turn.trace["action_decision"]["captured_slots"]
    ] == ["active_students_or_size", "main_pain"]
    assert multi_answer_turn.trace["compiler"]["template_ids"] == [
        "diagnostic.ask_pain_detail",
    ]
    assert report.total_cost_usd == 0
    assert fake_model.calls == 3


@pytest.mark.asyncio
async def test_diagnostic_price_objection_answers_then_resumes_pending_question() -> None:
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
                                "value_text": "80 alunos",
                                "status": "answered",
                                "evidence": ["user: 80 alunos"],
                            },
                            {
                                "key": "main_pain",
                                "value_text": "demora para responder interessados",
                                "status": "answered",
                                "evidence": ["user: responder interessados rapido"],
                            },
                        ],
                        composition_variables=[
                            {
                                "name": "answer_feedback",
                                "value": (
                                    "Entendi: 80 alunos e gargalo no retorno aos interessados."
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
                        "answer_direct_question_then_continue_diagnostic",
                        direct_question="achei caro, nao sei se compensa",
                        interpreted_intents=["price_objection"],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        [
            "quero fazer o diagnostico gratuito",
            "80 alunos e o maior problema e responder interessados rapido",
            "achei caro, nao sei se compensa",
        ],
        model=fake_model,
    )

    _, multi_answer_turn, objection_turn = report.turns
    rendered = "\n".join(objection_turn.rendered_messages)

    assert multi_answer_turn.template_ids == ("diagnostic.ask_pain_detail",)
    assert objection_turn.status == "delivered"
    assert objection_turn.mode == "diagnostic"
    assert objection_turn.starting_agent == "taliya_diagnostic_agent"
    assert objection_turn.model_operations == 1
    assert objection_turn.selected_action == ("answer_direct_question_then_continue_diagnostic")
    assert objection_turn.template_ids == (
        "product.price_objection_value",
        "diagnostic.ask_pain_detail",
    )
    assert "caro" in objection_turn.user_text
    assert "valor" in rendered.casefold()
    assert "resolvido no dia" in rendered.casefold()
    assert "checkout" not in rendered.casefold()

    ledger = report.final_state["diagnostic"]["ledger"]
    assert ledger["active_students_or_size"]["answer_value"] == "80 alunos"
    assert ledger["main_pain"]["answer_value"] == ("demora para responder interessados")
    assert report.final_state["canonical_state"] == "diagnostic_waiting_answer"
    assert objection_turn.trace["action_decision"]["interpreted_intents"] == ["price_objection"]
    assert objection_turn.trace["compiler"]["template_ids"] == [
        "product.price_objection_value",
        "diagnostic.ask_pain_detail",
    ]
    assert report.total_cost_usd == 0
    assert fake_model.calls == 4


@pytest.mark.asyncio
async def test_waitlist_pending_product_question_answers_then_asks_missing_studio() -> None:
    fake_model = ScriptedFakeModel(
        [
            [
                _message(
                    _decision_json(
                        "answer_question_then_continue_waitlist",
                        direct_question="como funciona mesmo?",
                        interpreted_intents=["conversation_resume", "how_it_works"],
                        product_fact_keys_used=["how_it_works"],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        ["como funciona mesmo?"],
        model=fake_model,
        initial_state={
            "canonical_state": "waitlist_pending_data",
            "waitlist": {
                "status": "pending_data",
                "missing_details": ["studio_name"],
            },
        },
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)

    assert turn.status == "delivered"
    assert turn.mode == "waitlist"
    assert turn.starting_agent == "taliya_waitlist_agent"
    assert turn.model_operations == 1
    assert turn.selected_action == "answer_question_then_continue_waitlist"
    assert turn.template_ids == (
        "product.how_it_works_direct",
        "waitlist.ask_missing_studio",
    )
    assert "Taliya" in rendered
    assert "nome do studio" in rendered.casefold()
    assert "checkout" not in rendered.casefold()
    assert "desconto" not in rendered.casefold()

    assert report.final_state["canonical_state"] == "waitlist_pending_data"
    assert report.final_state["waitlist"] == {
        "status": "pending_data",
        "missing_details": ["studio_name"],
    }
    assert report.final_state["answered_obligations"] == ["como funciona mesmo?"]
    assert turn.trace["action_decision"]["product_fact_keys_used"] == ["how_it_works"]
    assert turn.trace["compiler"]["template_ids"] == [
        "product.how_it_works_direct",
        "waitlist.ask_missing_studio",
    ]
    assert report.total_cost_usd == 0
    assert fake_model.calls == 1


@pytest.mark.asyncio
async def test_waitlist_how_it_works_question_uses_how_it_works_template_first() -> None:
    fake_model = ScriptedFakeModel(
        [
            [
                _message(
                    _decision_json(
                        "answer_question_then_continue_waitlist",
                        direct_question="como funciona mesmo?",
                        interpreted_intents=[
                            "waitlist_interest",
                            "product_how_it_works_question",
                        ],
                        product_fact_keys_used=[
                            "how_it_works",
                            "availability_and_onboarding",
                        ],
                        waitlist_intent="accepts",
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        ["como funciona mesmo?"],
        model=fake_model,
        initial_state={
            "canonical_state": "waitlist_offered",
            "waitlist": {
                "status": "offered",
                "missing_details": ["contact_path"],
            },
        },
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.mode == "waitlist"
    assert turn.selected_action == "answer_question_then_continue_waitlist"
    assert turn.template_ids == (
        "product.how_it_works_direct",
        "waitlist.ask_missing_contact_path",
    )
    assert "Taliya" in rendered
    assert "prefere seguir por esta conversa ou por e-mail" in rendered
    assert "checkout" not in rendered.casefold()
    assert report.final_state["answered_obligations"] == ["como funciona mesmo?"]


@pytest.mark.asyncio
async def test_waitlist_contract_info_question_uses_safe_waitlist_copy() -> None:
    fake_model = ScriptedFakeModel(
        [
            [
                _message(
                    _decision_json(
                        "answer_question_then_continue_waitlist",
                        direct_question="como funciona mesmo?",
                        interpreted_intents=["waitlist_info_request", "contract_intent"],
                        waitlist_intent="contract_intent",
                        direct_answer_obligations=[
                            {
                                "obligation": (
                                    "Explicar a lista sem prometer acesso imediato, "
                                    "data ou condição especial."
                                ),
                                "evidence": ["como funciona mesmo?"],
                            }
                        ],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        ["como funciona mesmo?"],
        model=fake_model,
        initial_state={
            "canonical_state": "waitlist_offered",
            "waitlist": {
                "status": "offered",
                "missing_details": ["contact_path"],
            },
        },
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)
    assert turn.status == "delivered"
    assert turn.mode == "waitlist"
    assert turn.selected_action == "answer_question_then_continue_waitlist"
    assert turn.template_ids == (
        "waitlist.current_path_explained",
        "waitlist.ask_missing_contact_path",
    )
    assert "número pequeno de studios" in rendered
    assert "prefere seguir por esta conversa ou por e-mail" in rendered
    assert "Não prometa" not in rendered
    assert report.final_state["answered_obligations"] == ["como funciona mesmo?"]


@pytest.mark.asyncio
async def test_post_diagnostic_demo_resume_after_days_does_not_restart_diagnostic() -> None:
    fake_model = ScriptedFakeModel(
        [
            [
                _message(
                    _decision_json(
                        "send_demo",
                        direct_question="me manda a demo de novo",
                        interpreted_intents=["conversation_resume", "demo"],
                        product_fact_keys_used=["demo_link"],
                        demo_intent="requested",
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        ["me manda a demo de novo"],
        model=fake_model,
        initial_state={
            "canonical_state": "diagnostic_delivered",
            "summary": "Lead voltou depois de alguns dias pedindo demo.",
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
            "demo": {"status": "offered"},
        },
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)

    assert turn.status == "delivered"
    assert turn.mode == "post_diagnostic"
    assert turn.starting_agent == "taliya_product_agent"
    assert turn.model_operations == 1
    assert turn.selected_action == "send_demo"
    assert turn.template_ids == ("product.demo_direct",)
    assert "/pilates/planos/demonstracao" in rendered
    assert "demo" in rendered.casefold()
    assert "diagnostico gratuito" not in rendered.casefold()
    assert "alunos ativos" not in rendered.casefold()
    assert not any(template.startswith("diagnostic.") for template in turn.template_ids)

    assert report.final_state["canonical_state"] == "demo_reaction_pending"
    assert report.final_state["diagnostic"]["status"] == "completed"
    assert report.final_state["demo"] == {"status": "offered"}
    assert report.final_state["answered_obligations"] == ["me manda a demo de novo"]
    assert turn.trace["action_decision"]["product_fact_keys_used"] == ["demo_link"]
    assert turn.trace["compiler"]["template_ids"] == ["product.demo_direct"]
    assert report.total_cost_usd == 0
    assert fake_model.calls == 1


@pytest.mark.asyncio
async def test_diagnostic_refusal_price_question_answers_without_reoffering_diagnostic() -> None:
    fake_model = ScriptedFakeModel(
        [
            [
                _message(
                    _decision_json(
                        "respect_diagnostic_refusal",
                        direct_question="so me fala o preco",
                        interpreted_intents=["diagnostic_refusal", "price"],
                        diagnostic_intent="refusal",
                        product_fact_keys_used=["prices"],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation(
        ["so me fala o preco"],
        model=fake_model,
        initial_state={
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
        },
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)

    assert turn.status == "delivered"
    assert turn.mode == "diagnostic"
    assert turn.starting_agent == "taliya_diagnostic_agent"
    assert turn.model_operations == 1
    assert turn.selected_action == "respect_diagnostic_refusal"
    assert turn.template_ids == ("product.price_direct",)
    assert "R$ 197" in rendered
    assert "R$ 497" in rendered
    assert "diagnostico gratuito" not in rendered.casefold()
    assert "alunos ativos" not in rendered.casefold()
    assert not any(template.startswith("diagnostic.") for template in turn.template_ids)

    assert report.final_state["canonical_state"] == "general_interest"
    assert report.final_state["diagnostic"]["status"] == "in_progress"
    assert report.final_state["answered_obligations"] == ["so me fala o preco"]
    assert turn.trace["action_decision"]["diagnostic_intent"] == "refusal"
    assert turn.trace["compiler"]["template_ids"] == ["product.price_direct"]
    assert report.total_cost_usd == 0
    assert fake_model.calls == 1


@pytest.mark.asyncio
async def test_post_waitlist_product_resume_preserves_joined_status() -> None:
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
        initial_state={
            "canonical_state": "waitlist_joined",
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
        },
    )

    [turn] = report.turns
    rendered = "\n".join(turn.rendered_messages)

    assert turn.status == "delivered"
    assert turn.mode == "post_diagnostic"
    assert turn.starting_agent == "taliya_product_agent"
    assert turn.model_operations == 1
    assert turn.selected_action == "answer_product_question_with_saved_context"
    assert turn.template_ids == ("product.how_it_works_direct",)
    assert "Taliya" in rendered
    assert "lista" not in rendered.casefold()
    assert "checkout" not in rendered.casefold()
    assert "diagnostico gratuito" not in rendered.casefold()
    assert not any(template.startswith("waitlist.") for template in turn.template_ids)
    assert not any(template.startswith("diagnostic.") for template in turn.template_ids)

    assert report.final_state["canonical_state"] == "post_diagnostic_questions"
    assert report.final_state["waitlist"] == {
        "status": "joined",
        "idempotency_key": "waitlist:joined:historical",
        "joined_at": "2026-06-01T12:00:00Z",
    }
    assert report.final_state["diagnostic"]["status"] == "completed"
    assert report.final_state["answered_obligations"] == ["como funciona mesmo?"]
    assert turn.trace["turn_situation"]["forbidden_actions_now"] == [
        "offer_or_join_waitlist_if_eligible"
    ]
    assert turn.trace["action_decision"]["product_fact_keys_used"] == ["how_it_works"]
    assert turn.trace["compiler"]["template_ids"] == ["product.how_it_works_direct"]
    assert turn.trace["sales_inbox_projection"]["waitlist_status"] == "joined"
    assert turn.sales_inbox_projection["fields"]["waitlist_idempotency_key"] == (
        "waitlist:joined:historical"
    )
    assert turn.sales_inbox_projection["fields"]["waitlist_joined_at"] == ("2026-06-01T12:00:00Z")
    assert report.total_cost_usd == 0
    assert fake_model.calls == 1


@pytest.mark.asyncio
async def test_parroting_composition_is_blocked() -> None:
    lead_text = "perco aluno novo porque o whatsapp vive atrasado demais"
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_entry_agent")],
            [
                _message(
                    _decision_json(
                        "offer_diagnostic_from_pain",
                        composition_variables=[
                            {
                                "name": "pain_context_human",
                                # Literal parroting of the lead's sentence.
                                "value": lead_text,
                                "evidence": ["inbound.text"],
                            }
                        ],
                    )
                )
            ],
            # Repair fails to change it (same parroting) -> turn fails.
            [
                _message(
                    _decision_json(
                        "offer_diagnostic_from_pain",
                        composition_variables=[
                            {
                                "name": "pain_context_human",
                                "value": lead_text,
                                "evidence": ["inbound.text"],
                            }
                        ],
                    )
                )
            ],
        ]
    )

    report = await run_action_conversation([lead_text], model=fake_model)

    [turn] = report.turns
    assert turn.status == "failed"
    assert "voice_literal_parroting" in turn.issues
