from __future__ import annotations

from dataclasses import replace

from app.core.taliya_commercial_sdk.action_validators import validate_compiled_turn
from app.core.taliya_commercial_sdk.conductor_decision import ConductorActionDecision
from app.core.taliya_commercial_sdk.decision_compiler import compile_action_decision
from app.core.taliya_commercial_sdk.turn_situation import build_turn_situation

PRICE_FACTS = {
    "plan_price_summary": {
        "kind": "long_text",
        "value": "Base: R$ 197/mes. Essencial: R$ 497/mes.",
        "source": "official_product_knowledge",
        "evidence": ["product_knowledge.plans"],
        "max_length": 360,
    },
}


def _decision(action: str, **overrides) -> ConductorActionDecision:
    return ConductorActionDecision.model_validate(
        {"selected_action": action, "evidence": ["inbound.text"], **overrides}
    )


def _composition(name: str, value: str) -> dict:
    return {"name": name, "value": value, "evidence": ["inbound.text"]}


def _issue_codes(result) -> set[str]:
    return {issue.code for issue in result.validator_result.errors}


def test_action_validator_ports_spec011_price_hook_requirement() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "price_question"},
        channel="whatsapp",
    )
    decision = _decision(
        "answer_price",
        direct_question="quanto custa?",
        interpreted_intents=["price_question"],
    )
    compiled = compile_action_decision(decision, situation, official_facts=PRICE_FACTS)

    assert compiled.template_ids == ("product.price_direct", "diagnostic.price_hook")
    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="quanto custa?",
        has_history=False,
    )

    assert result.ok, _issue_codes(result)

    without_hook = replace(compiled, template_ids=("product.price_direct",))
    blocked = validate_compiled_turn(
        without_hook,
        decision=decision,
        situation=situation,
        current_user_text="quanto custa?",
        has_history=False,
    )

    assert not blocked.ok
    assert "price_question_missing_diagnostic_hook" in _issue_codes(blocked)


def test_action_validator_bridges_entry_price_objection_as_diagnostic_offer() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "diagnostic_offered"},
        channel="widget",
    )
    decision = _decision(
        "answer_price_objection",
        interpreted_intents=["price_objection", "budget_concern"],
        product_fact_keys_used=["prices"],
        reply_goal=(
            "Acolher a percepcao de que o valor pode pesar sem pressionar."
        ),
    )
    compiled = compile_action_decision(decision, situation, official_facts=PRICE_FACTS)

    assert compiled.previous_state == "diagnostic_offered"
    assert compiled.next_state == "diagnostic_offered"
    assert compiled.template_ids == ("product.price_objection_value",)

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="hmm, talvez fique pesado",
        has_history=True,
    )

    assert result.ok, _issue_codes(result)
    assert any(
        "valor para olhar com calma" in message.text.casefold()
        for message in result.rendered_preview
    )


def test_action_validator_accepts_approved_contextual_price_hook_copy() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "new_lead"},
        channel="whatsapp",
    )
    decision = _decision(
        "answer_price",
        direct_question="tenho reposicao baguncada na agenda e queria saber preco",
        interpreted_intents=["price_question", "pain_context"],
        composition_variables=[
            _composition(
                "plan_fit_context",
                "Esse tipo de dor pede uma conversa rapida sobre a sua rotina.",
            )
        ],
    )
    compiled = compile_action_decision(decision, situation, official_facts=PRICE_FACTS)

    accepted = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="tenho reposicao baguncada na agenda e queria saber preco",
        has_history=False,
    )

    assert accepted.ok, _issue_codes(accepted)
    rendered_text = "\n".join(message.text for message in accepted.rendered_preview)
    assert "Como você já trouxe um ponto da rotina que está te incomodando" in rendered_text
    assert "Esse tipo de dor" not in rendered_text

    grounded_decision = _decision(
        "answer_price",
        direct_question="tenho reposicao baguncada na agenda e queria saber preco",
        interpreted_intents=["price_question", "pain_context"],
        composition_variables=[
            _composition(
                "plan_fit_context",
                "Como a reposicao esta baguncada na agenda, vale olhar o valor "
                "junto com esse fluxo.",
            )
        ],
    )
    grounded = compile_action_decision(
        grounded_decision,
        situation,
        official_facts=PRICE_FACTS,
    )
    accepted = validate_compiled_turn(
        grounded,
        decision=grounded_decision,
        situation=situation,
        current_user_text="tenho reposicao baguncada na agenda e queria saber preco",
        has_history=False,
    )

    assert accepted.ok, _issue_codes(accepted)


def test_action_validator_final_guard_blocks_public_internal_text() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "product_question"},
        channel="whatsapp",
    )
    decision = _decision(
        "answer_availability_and_onboarding",
        direct_question="quando abre?",
        interpreted_intents=["availability_and_onboarding"],
        product_fact_keys_used=["availability_and_onboarding"],
    )
    compiled = compile_action_decision(
        decision,
        situation,
        official_facts={
            "product_fact_summary": {
                "kind": "long_text",
                "value": "This answer must stay internal.",
                "source": "official_product_knowledge",
                "evidence": ["product_knowledge.availability_and_onboarding"],
            }
        },
    )

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="quando abre?",
        has_history=True,
    )

    assert not result.ok
    assert "customer_visible_internal_text_leak" in _issue_codes(result)


def test_action_validator_final_guard_blocks_broken_public_punctuation() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "product_question"},
        channel="whatsapp",
    )
    decision = _decision(
        "answer_availability_and_onboarding",
        direct_question="como funciona?",
        interpreted_intents=["availability_and_onboarding"],
        product_fact_keys_used=["availability_and_onboarding"],
    )
    compiled = compile_action_decision(
        decision,
        situation,
        official_facts={
            "product_fact_summary": {
                "kind": "long_text",
                "value": "A equipe enxerga o que precisa resolver primeiro..",
                "source": "official_product_knowledge",
                "evidence": ["product_knowledge.availability_and_onboarding"],
            }
        },
    )

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="como funciona?",
        has_history=True,
    )

    assert not result.ok
    assert "customer_visible_text_quality" in _issue_codes(result)


def test_action_validator_requires_context_hook_when_decision_declares_price_pain() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "new_lead"},
        channel="whatsapp",
    )
    decision = _decision(
        "answer_price",
        direct_question="queria saber preco",
        interpreted_intents=["price_question", "pain_signal"],
        product_fact_keys_used=["prices"],
        captured_slots=[
            {
                "key": "main_pain",
                "value_text": "reposicao baguncada na agenda",
                "status": "answered",
                "evidence": ["tenho reposicao baguncada na agenda"],
            }
        ],
        composition_variables=[
            _composition(
                "pain_context_human",
                "a agenda de reposicao esta desorganizada",
            )
        ],
    )
    compiled = compile_action_decision(decision, situation, official_facts=PRICE_FACTS)

    assert compiled.template_ids == ("product.price_direct", "diagnostic.price_hook")
    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="tenho reposicao baguncada na agenda e queria saber preco",
        has_history=False,
    )

    assert not result.ok
    assert "price_plus_context_requires_context_hook" in _issue_codes(result)


def test_action_validator_corrects_unneeded_clarification_for_direct_question() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "new_lead"},
        channel="whatsapp",
    )
    decision = _decision(
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
            _composition("clarification_question", "Voce quer saber o valor?")
        ],
    )
    compiled = compile_action_decision(decision, situation, official_facts=PRICE_FACTS)

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="quanto custa?",
        has_history=False,
    )

    assert result.ok, _issue_codes(result)
    assert compiled.selected_action == "answer_direct_product_question"
    assert compiled.template_ids == ("product.price_direct", "diagnostic.price_hook")
    assert any("R$ 497" in message.text for message in result.rendered_preview)


def test_action_validator_corrects_price_clarification_when_price_fact_declared() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "new_lead"},
        channel="whatsapp",
    )
    decision = _decision(
        "clarify_ambiguous_opening",
        direct_question="quanto custa?",
        interpreted_intents=["price_question"],
        product_fact_keys_used=["prices"],
        needs_clarification=True,
        composition_variables=[
            _composition("clarification_question", "Voce quer saber qual plano?")
        ],
    )
    compiled = compile_action_decision(decision, situation, official_facts=PRICE_FACTS)

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="quanto custa?",
        has_history=False,
    )

    assert result.ok, _issue_codes(result)
    assert compiled.selected_action == "answer_direct_product_question"
    assert compiled.template_ids == ("product.price_direct", "diagnostic.price_hook")


def test_action_validator_corrects_price_clarification_when_price_intent_declared() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "new_lead"},
        channel="whatsapp",
    )
    decision = _decision(
        "clarify_ambiguous_opening",
        direct_question="quanto custa?",
        interpreted_intents=["price_question", "opening_without_context"],
        needs_clarification=True,
        composition_variables=[
            _composition("clarification_question", "Voce quer saber qual plano?")
        ],
    )
    compiled = compile_action_decision(decision, situation, official_facts=PRICE_FACTS)

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="quanto custa?",
        has_history=False,
    )

    assert result.ok, _issue_codes(result)
    assert compiled.selected_action == "answer_direct_product_question"
    assert compiled.template_ids == ("product.price_direct", "diagnostic.price_hook")


def test_action_validator_blocks_post_diagnostic_waitlist_intent_as_objection() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "diagnostic_delivered",
            "diagnostic": {"status": "delivered", "ledger": {}},
        },
        channel="whatsapp",
    )
    decision = _decision(
        "answer_price_objection_with_context",
        interpreted_intents=["price_objection", "wants_to_start"],
        product_fact_keys_used=["prices"],
        composition_variables=[
            _composition(
                "waitlist_context_summary",
                "Lead quer comecar e entrar na lista.",
            )
        ],
    )
    compiled = compile_action_decision(decision, situation, official_facts=PRICE_FACTS)

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="quero comecar, me coloca na lista",
        has_history=True,
    )

    assert not result.ok
    assert (
        "post_diagnostic_waitlist_intent_requires_waitlist_action"
        in _issue_codes(result)
    )


def test_action_validator_ignores_stale_price_objection_on_waitlist_action() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "diagnostic_delivered",
            "diagnostic": {"status": "delivered", "ledger": {}},
        },
        channel="whatsapp",
    )
    decision = _decision(
        "offer_or_join_waitlist_if_eligible",
        interpreted_intents=["waitlist_request", "price_objection"],
        waitlist_intent="contract_intent",
        composition_variables=[
            _composition(
                "waitlist_context_summary",
                "Lead quer comecar e entrar na lista.",
            )
        ],
    )
    compiled = compile_action_decision(decision, situation)

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="quero comecar, me coloca na lista",
        has_history=True,
    )

    assert result.ok, _issue_codes(result)


def test_action_validator_treats_non_numeric_plan_price_as_unknown_number() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "new_lead"},
        channel="whatsapp",
    )
    decision = _decision(
        "answer_direct_product_question",
        direct_question="quanto custa?",
        interpreted_intents=["price_question"],
        product_fact_keys_used=["prices"],
        numeric_interpretations=[
            {
                "kind": "plan_price",
                "raw_text": "quanto custa",
                "value_text": "preco nao especificado no texto do lead",
                "evidence": ["quanto custa?"],
            }
        ],
    )
    compiled = compile_action_decision(decision, situation, official_facts=PRICE_FACTS)

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="quanto custa?",
        has_history=False,
    )

    assert result.ok, _issue_codes(result)


def test_action_validator_blocks_invented_demo_link() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "demo_question"},
        channel="whatsapp",
    )
    decision = _decision(
        "send_demo",
        direct_question="tem demo?",
        interpreted_intents=["demo_request"],
        product_fact_keys_used=["demo_link"],
    )
    compiled = compile_action_decision(
        decision,
        situation,
        official_facts={
            "official_demo_link": {
                "kind": "url",
                "value": "https://taliya.link/demo-inventado",
                "source": "official_product_knowledge",
                "evidence": ["product_knowledge.links.demo"],
            }
        },
    )

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="tem demo?",
        has_history=False,
    )

    assert not result.ok
    assert "official_link_mismatch" in _issue_codes(result)


def test_action_validator_blocks_waitlist_from_demo_curiosity() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "diagnostic_delivered",
            "diagnostic": {"status": "delivered", "ledger": {}},
            "demo": {"status": "viewed_or_asked"},
        },
        channel="whatsapp",
    )
    decision = _decision(
        "offer_or_join_waitlist_if_eligible",
        interpreted_intents=["demo_request"],
        demo_intent="curiosity",
        waitlist_intent="curiosity",
        composition_variables=[
            _composition("waitlist_context_summary", "Lead demonstrou curiosidade pela demo.")
        ],
    )
    compiled = compile_action_decision(decision, situation)

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="quero ver a demo",
        has_history=True,
    )

    assert not result.ok
    assert {
        "waitlist_requires_eligibility",
        "waitlist_demo_curiosity_without_contract_intent",
    }.issubset(_issue_codes(result))


def test_action_validator_blocks_internal_label_leak_in_composition() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "pain_detected"},
        channel="whatsapp",
    )
    decision = _decision(
        "offer_diagnostic_from_pain",
        composition_variables=[
            _composition(
                "pain_context_human",
                "lead came from the site and asked about product knowledge",
            )
        ],
    )
    compiled = compile_action_decision(decision, situation)

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="vim pelo site e quero entender melhor",
        has_history=False,
    )

    assert not result.ok
    assert "internal_text_leak" in _issue_codes(result)
