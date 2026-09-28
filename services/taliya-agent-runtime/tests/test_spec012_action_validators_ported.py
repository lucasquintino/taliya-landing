"""T012-032 ported validator coverage for the action-first path."""

from __future__ import annotations

from app.core.taliya_commercial_sdk.action_validators import validate_compiled_turn
from app.core.taliya_commercial_sdk.conductor_decision import ConductorActionDecision
from app.core.taliya_commercial_sdk.decision_compiler import (
    CompiledTurn,
    compile_action_decision,
)
from app.core.taliya_commercial_sdk.turn_situation import build_turn_situation

OFFICIAL_FACTS = {
    "official_demo_link": {
        "kind": "url",
        "value": "https://www.taliya.com.br/pilates/planos/demonstracao",
        "source": "official_product_knowledge",
        "evidence": ["product_knowledge.links.demonstration"],
    },
    "plan_price_summary": {
        "kind": "long_text",
        "value": "Base R$ 197/mes ate Completo R$ 1.497/mes.",
        "source": "official_product_knowledge",
        "evidence": ["product_knowledge.prices"],
        "max_length": 360,
    },
}


def _decision(action: str, **overrides) -> ConductorActionDecision:
    return ConductorActionDecision.model_validate(
        {"selected_action": action, "evidence": ["inbound.text"], **overrides}
    )


def _composition(name: str, value: str) -> dict[str, object]:
    return {"name": name, "value": value, "evidence": ["inbound.text"]}


def _codes(result) -> set[str]:
    return {issue.code for issue in result.validator_result.errors}


def _validate(
    decision: ConductorActionDecision,
    situation,
    *,
    current_user_text: str,
    has_history: bool = True,
    official_facts: dict[str, object] | None = None,
):
    compiled = compile_action_decision(
        decision,
        situation,
        official_facts=official_facts or OFFICIAL_FACTS,
    )
    return validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text=current_user_text,
        has_history=has_history,
    )


def test_action_validator_blocks_waitlist_offer_from_demo_curiosity() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "buying_intent_detected",
            "demo": {"status": "viewed_or_asked"},
        },
        channel="whatsapp",
    )
    decision = _decision(
        "offer_waitlist",
        waitlist_intent="curiosity",
        demo_intent="curiosity",
        composition_variables=[
            _composition(
                "waitlist_context_summary",
                "Lead apenas perguntou como funciona a lista depois da demo.",
            )
        ],
    )
    compiled = compile_action_decision(decision, situation)

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="como funciona essa lista depois da demo?",
        has_history=True,
    )

    assert result.validator_result.status == "failed"
    assert "waitlist_requires_eligibility" in _codes(result)
    assert "waitlist_demo_curiosity_without_contract_intent" in _codes(result)


def test_action_validator_starts_diagnostic_without_name_question() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "diagnostic_offered"},
        channel="whatsapp",
    )
    decision = _decision("start_requested_diagnostic")
    result = _validate(
        decision,
        situation,
        current_user_text="quero fazer o diagnostico",
        has_history=True,
    )

    assert result.validator_result.status == "passed"
    assert all(
        "com quem eu falo" not in message.text.lower()
        for message in result.rendered_preview
    )


def test_action_validator_ports_internal_source_label_leak_block() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "pain_detected"},
        channel="whatsapp",
    )
    decision = _decision(
        "offer_diagnostic_from_pain",
        composition_variables=[
            _composition(
                "pain_context_human",
                "Lead came from the site; runtime_state mostra dor em vendas.",
            )
        ],
    )

    result = _validate(
        decision,
        situation,
        current_user_text="perco interessado no whatsapp",
    )

    assert result.validator_result.status == "failed"
    assert "internal_text_leak" in _codes(result)


def test_action_validator_blocks_crm_jargon_for_lay_lead() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "pain_detected"},
        channel="whatsapp",
    )
    decision = _decision(
        "offer_diagnostic_from_pain",
        composition_variables=[
            _composition(
                "pain_context_human",
                "A base de CRM precisa organizar os interessados do studio.",
            )
        ],
    )

    result = _validate(
        decision,
        situation,
        current_user_text="perco interessado no whatsapp",
    )

    assert result.validator_result.status == "failed"
    assert "voice_crm_jargon_for_lay_lead" in _codes(result)


def test_action_validator_allows_crm_term_when_lead_used_it() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "pain_detected"},
        channel="whatsapp",
    )
    decision = _decision(
        "offer_diagnostic_from_pain",
        composition_variables=[
            _composition(
                "pain_context_human",
                "Entendi: a base de CRM hoje nao deixa proximos passos claros.",
            )
        ],
    )

    result = _validate(
        decision,
        situation,
        current_user_text="meu CRM ta baguncado",
    )

    assert result.ok, [issue.code for issue in result.validator_result.errors]


def test_action_validator_blocks_rejected_final_diagnostic_phrase() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "pain_detected"},
        channel="whatsapp",
    )
    decision = _decision(
        "offer_diagnostic_from_pain",
        composition_variables=[
            _composition(
                "pain_context_human",
                "Pelo contexto, o principal gargalo parece agenda.",
            )
        ],
    )

    result = _validate(
        decision,
        situation,
        current_user_text="agenda e reposicao estao confusas",
    )

    assert result.validator_result.status == "failed"
    assert "banned_customer_phrase" in _codes(result)


def test_action_validator_blocks_thin_context_pelo_que_voce_contou() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "pain_detected"},
        channel="whatsapp",
    )
    decision = _decision(
        "offer_diagnostic_from_pain",
        composition_variables=[
            _composition(
                "pain_context_human",
                "Pelo que voce contou, o problema parece estar no WhatsApp.",
            )
        ],
    )

    result = _validate(
        decision,
        situation,
        current_user_text="whatsapp",
    )

    assert result.validator_result.status == "failed"
    assert "voice_thin_context_evidence_framing" in _codes(result)


def test_action_validator_blocks_waitlist_checkout_discount_promise() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "post_diagnostic_questions"},
        channel="whatsapp",
    )
    decision = _decision(
        "offer_or_join_waitlist_if_eligible",
        waitlist_intent="contract_intent",
        composition_variables=[
            _composition(
                "waitlist_context_summary",
                "Tem checkout VIP com desconto se entrar hoje.",
            )
        ],
    )

    result = _validate(
        decision,
        situation,
        current_user_text="quero contratar quando abrir",
    )

    assert result.validator_result.status == "failed"
    assert "waitlist_context_summary_promises_blocked" in _codes(result)


def test_action_validator_ports_price_answer_adequacy_map() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "price_question"},
        channel="whatsapp",
    )
    decision = _decision(
        "answer_direct_product_question",
        direct_question="qto fica?",
        interpreted_intents=["price_question"],
        product_fact_keys_used=["product_overview"],
    )
    compiled = CompiledTurn(
        selected_action="answer_direct_product_question",
        previous_state="price_question",
        current_state="product_question",
        next_state="diagnostic_offered",
        template_ids=("product.overview_short", "diagnostic.price_hook"),
        variables={
            "product_fact_summary": {
                "kind": "long_text",
                "value": "A Taliya organiza a rotina comercial do studio.",
                "source": "official_product_knowledge",
                "evidence": ["product_knowledge.product_overview"],
                "max_length": 320,
            }
        },
        ledger_updates=(),
        state_patch={},
        sales_inbox_projection={
            "commercial_stage": "diagnostic_offered",
            "last_action": "answer_direct_product_question",
        },
        chunk_policy="whatsapp_max_3",
    )

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="qto fica?",
        has_history=True,
    )

    assert result.validator_result.status == "failed"
    assert "price_question_missing_price_answer" in _codes(result)


def test_action_validator_ports_integration_scope_before_handoff_contract() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "product_question"},
        channel="whatsapp",
    )
    decision = _decision(
        "handoff_requested",
        direct_question="integra com meu instagram?",
        interpreted_intents=["integration_scope_question"],
        handoff_intent="requested",
        composition_variables=[
            _composition("handoff_reason", "confirmar integracao com Instagram")
        ],
    )
    compiled = compile_action_decision(decision, situation)

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="integra com meu instagram?",
        has_history=True,
    )

    assert result.validator_result.status == "failed"
    assert "integration_scope_handoff_without_product_answer" in _codes(result)


def test_action_validator_accepts_waitlist_offer_for_contract_intent() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "post_diagnostic_questions"},
        channel="whatsapp",
    )
    decision = _decision(
        "offer_or_join_waitlist_if_eligible",
        waitlist_intent="contract_intent",
        composition_variables=[
            _composition(
                "waitlist_context_summary",
                "Lead terminou o diagnostico e pediu para contratar quando abrir.",
            )
        ],
    )
    compiled = compile_action_decision(decision, situation)

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="quero entrar na lista para contratar",
        has_history=True,
    )

    assert result.ok, [issue.code for issue in result.validator_result.errors]
    assert compiled.template_ids == ("waitlist.offer_after_contract_intent",)


def test_action_validator_blocks_demo_offer_without_demo_template() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "demo_question"},
        channel="whatsapp",
    )
    decision = _decision("send_demo", demo_intent="requested")
    compiled = CompiledTurn(
        selected_action="send_demo",
        previous_state="demo_question",
        current_state="demo_offered",
        next_state="demo_reaction_pending",
        template_ids=("product.overview_short",),
        variables={},
        ledger_updates=(),
        state_patch={"demo": {"status": "offered"}},
        sales_inbox_projection={
            "commercial_stage": "demo_reaction_pending",
            "last_action": "send_demo",
            "demo_status": "offered",
        },
        chunk_policy="whatsapp_max_3",
    )

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="tem demo?",
        has_history=True,
    )

    assert result.validator_result.status == "failed"
    assert "demo_offer_template_missing" in _codes(result)


def test_action_validator_requires_handoff_reason_and_ack_template() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "general_interest"},
        channel="whatsapp",
    )
    decision = _decision("handoff_requested", handoff_intent="requested")
    compiled = compile_action_decision(decision, situation)

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="quero falar com uma pessoa",
        has_history=True,
    )

    assert result.validator_result.status == "failed"
    assert "compile_missing_composition:handoff_reason" in _codes(result)


def test_action_validator_accepts_handoff_with_reason_and_pause_patch() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "general_interest"},
        channel="whatsapp",
    )
    decision = _decision(
        "handoff_requested",
        handoff_intent="requested",
        composition_variables=[
            _composition("handoff_reason", "pediu para falar com uma pessoa")
        ],
    )
    compiled = compile_action_decision(decision, situation)

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="quero falar com uma pessoa",
        has_history=True,
    )

    assert result.ok, [issue.code for issue in result.validator_result.errors]
    assert compiled.state_patch["handoff"] == {"status": "requested", "pause_ai": True}
