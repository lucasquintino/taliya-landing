"""T012-033: renderer compatibility with compiler-owned render plans."""

from __future__ import annotations

from app.core.taliya_commercial_sdk.action_validators import validate_compiled_turn
from app.core.taliya_commercial_sdk.conductor_decision import ConductorActionDecision
from app.core.taliya_commercial_sdk.decision_compiler import compile_action_decision
from app.core.taliya_commercial_sdk.turn_situation import build_turn_situation


def _decision(action: str, **overrides) -> ConductorActionDecision:
    return ConductorActionDecision.model_validate(
        {"selected_action": action, "evidence": ["inbound.text"], **overrides}
    )


def _composition(name: str, value: str) -> dict[str, object]:
    return {"name": name, "value": value, "evidence": ["inbound.text"]}


def test_033_renderer_starts_diagnostic_without_name_question() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "diagnostic_offered"},
        channel="whatsapp",
    )
    decision = _decision("start_requested_diagnostic")
    compiled = compile_action_decision(decision, situation)

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="quero fazer o diagnostico",
        has_history=True,
    )

    assert result.ok, result.validator_result.errors
    assert compiled.template_ids == (
        "diagnostic.start",
        "diagnostic.ask_active_students",
    )
    rendered_text = "\n".join(message.text for message in result.rendered_preview)
    assert "com quem eu falo" not in rendered_text.lower()
    assert "vou entender rapidinho" in rendered_text.lower()


def test_033_renderer_accepts_compiler_owned_how_it_works_enum_variable() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "product_question"},
        channel="whatsapp",
    )
    decision = _decision(
        "answer_how_it_works",
        direct_question="como funciona?",
        interpreted_intents=["product_how_it_works"],
        product_fact_keys_used=["how_it_works"],
    )
    compiled = compile_action_decision(decision, situation)

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="como funciona?",
        has_history=True,
    )

    assert result.ok, result.validator_result.errors
    assert compiled.variables["contextual_next_step"]["source"] == "runtime_state"
    rendered_text = "\n".join(message.text for message in result.rendered_preview)
    assert "Funciona assim" in rendered_text
    assert "diagnóstico gratuito" in rendered_text


def test_043_renderer_uses_approved_whatsapp_scope_copy() -> None:
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "product_question"},
        channel="whatsapp",
    )
    decision = _decision(
        "answer_whatsapp_scope",
        direct_question="o aluno precisa baixar aplicativo?",
        interpreted_intents=["whatsapp_scope"],
        product_fact_keys_used=["whatsapp_scope"],
    )
    compiled = compile_action_decision(
        decision,
        situation,
        official_facts={
            "official_demo_link": {
                "kind": "url",
                "value": "https://www.taliya.com.br/pilates/planos/demonstracao",
                "source": "official_product_knowledge",
                "evidence": ["product_knowledge.links.demonstration"],
            }
        },
    )

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="o aluno precisa baixar aplicativo?",
        has_history=False,
    )

    assert result.ok, result.validator_result.errors
    assert [message.text for message in result.rendered_preview] == [
        "Oi, tudo bem?",
        (
            "O aluno não precisa baixar aplicativo nem criar senha. Ele conversa "
            "no WhatsApp; a Taliya registra a ação, atualiza o painel e avisa "
            "o responsável."
        ),
        (
            "Se quiser ver isso funcionando na prática, aqui está uma "
            "demonstração: https://www.taliya.com.br/pilates/planos/demonstracao"
        ),
    ]


def test_043_renderer_uses_approved_handoff_context_copy() -> None:
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
        current_user_text="quero falar com alguem",
        has_history=True,
    )

    assert result.ok, result.validator_result.errors
    rendered_text = "\n".join(message.text for message in result.rendered_preview)
    assert (
        "Vou deixar o contexto da conversa salvo para você não precisar repetir tudo."
        in rendered_text
    )
    assert "Tambem deixo o contexto salvo" not in rendered_text


def test_waitlist_hesitation_pauses_without_collecting_or_changing_status() -> None:
    situation = build_turn_situation(
        state_snapshot={
            "canonical_state": "waitlist_offered",
            "waitlist": {"status": "offered"},
        },
        channel="whatsapp",
    )
    decision = _decision(
        "pause_waitlist_decision",
        waitlist_intent="curiosity",
        interpreted_intents=["wants_to_understand_before_deciding"],
    )
    compiled = compile_action_decision(decision, situation)

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="talvez, antes eu queria entender melhor",
        has_history=True,
    )

    assert result.ok, result.validator_result.errors
    assert compiled.template_ids == ("waitlist.pause_decision",)
    assert compiled.state_patch == {}
    assert [message.text for message in result.rendered_preview] == [
        "Claro. O que você quer entender melhor antes de decidir?"
    ]


def test_033_renderer_accepts_compiler_staged_final_diagnostic_plan() -> None:
    situation = build_turn_situation(
        state_snapshot={
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
                        "answer_value": "interessados sem retorno",
                    },
                    "pain_detail": {
                        "status": "answered",
                        "answer_value": "equipe perde acompanhamento",
                    },
                    "current_process": {
                        "status": "answered",
                        "answer_value": "WhatsApp e planilha",
                    },
                    "priority": {
                        "status": "answered",
                        "answer_value": "vendas e atendimento",
                    },
                },
            },
        },
        channel="whatsapp",
    )
    decision = _decision(
        "complete_diagnostic",
        captured_slots=[
                {
                    "key": "urgency",
                    "value_text": "quer resolver ainda este mes",
                    "status": "answered",
                    "evidence": ["quero resolver ainda este mes"],
                }
        ],
        composition_variables=[
            _composition(
                "pain_context_human",
                "Hoje o retorno de interessados parece ser o ponto mais urgente.",
            ),
            _composition(
                "crm_base_recommendation",
                "Antes de colocar agentes, vale organizar a base de atendimento.",
            ),
            _composition(
                "operational_first_step",
                "O primeiro passo pratico e mapear retornos pendentes no WhatsApp.",
            ),
        ],
    )
    compiled = compile_action_decision(
        decision,
        situation,
        official_facts={
            "recommended_plan_or_range": {
                "kind": "short_text",
                "value": "Essencial (R$ 497/mes)",
                "source": "official_product_knowledge",
                "evidence": ["product_knowledge.plans"],
            },
            "indicated_agents": [
                {
                    "agent_name": "Atendimento",
                    "agent_pain_resolved": "retornos que ficam sem dono",
                    "agent_practical_action": "avisar a equipe do que precisa de acao",
                }
            ],
        },
    )

    result = validate_compiled_turn(
        compiled,
        decision=decision,
        situation=situation,
        current_user_text="quero resolver ainda este mes",
        has_history=True,
    )

    assert result.ok, result.validator_result.errors
    assert compiled.chunk_policy == "staged_diagnostic"
    assert "diagnostic.deliver_plan_recommendation" in compiled.template_ids
    assert len(result.rendered_preview) <= 3
    rendered_text = "\n".join(message.text for message in result.rendered_preview)
    assert "Essencial" in rendered_text
    assert "Agente de Atendimento" in rendered_text
    assert (
        "organiza interessados, aulas experimentais, próximos passos e follow-up"
        in rendered_text
    )
    assert "retornos que ficam sem dono" not in rendered_text
    assert "Na prática, a equipe enxerga o que precisa resolver primeiro." in rendered_text
    assert "organizados.," not in rendered_text
    assert "Também posso te mandar uma demonstração" in rendered_text
    assert "Temos algumas demonstracoes" not in rendered_text
