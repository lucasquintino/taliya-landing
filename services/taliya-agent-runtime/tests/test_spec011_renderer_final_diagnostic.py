from __future__ import annotations

from app.core.taliya_commercial.renderer import render_validated_template_plan
from app.core.taliya_commercial.schemas import (
    RenderPlan,
    RenderPlanItem,
    TemplateVariableValue,
    ValidatorResult,
)


def _passed_validation() -> ValidatorResult:
    return ValidatorResult(
        decision_id="decision_renderer_diagnostic_1",
        status="passed",
        final_disposition="accepted",
    )


def _value(
    *,
    kind: str,
    value: str,
    source: str,
    max_length: int | None = None,
) -> TemplateVariableValue:
    return TemplateVariableValue.model_validate(
        {
            "kind": kind,
            "value": value,
            "source": source,
            "evidence": ["diagnostic_ledger.complete"],
            **({"max_length": max_length} if max_length is not None else {}),
        }
    )


def _agent_variables(name: str, fit_phrase: str, pain: str) -> dict[str, TemplateVariableValue]:
    return {
        "agent_name": _value(
            kind="short_text",
            value=name,
            source="official_product_knowledge",
            max_length=60,
        ),
        "agent_fit_phrase": _value(
            kind="enum",
            value=fit_phrase,
            source="model_decision",
        ),
        "agent_pain_resolved": _value(
            kind="long_text",
            value=pain,
            source="diagnostic_ledger",
            max_length=180,
        ),
        "agent_recommendation_reason": _value(
            kind="long_text",
            value=f"{pain} apareceu com mais forca no diagnostico",
            source="diagnostic_ledger",
            max_length=220,
        ),
        "agent_practical_action": _value(
            kind="long_text",
            value="ele organiza a fila e avisa a equipe quando precisa de humano",
            source="spec_006_product_contract",
            max_length=220,
        ),
    }


def test_renderer_preserves_completed_diagnostic_stage_order_and_final_sentence() -> None:
    plan = RenderPlan(
        chunk_policy="staged_diagnostic",
        items=[
            RenderPlanItem(template_id="diagnostic.deliver_hold"),
            RenderPlanItem(
                template_id="diagnostic.deliver_context",
                variables={
                    "pain_context_human": _value(
                        kind="long_text",
                        value="O principal peso hoje e perder interessados no WhatsApp.",
                        source="diagnostic_ledger",
                        max_length=320,
                    )
                },
            ),
            RenderPlanItem(
                template_id="diagnostic.deliver_crm_base",
                variables={
                    "crm_base_recommendation": _value(
                        kind="long_text",
                        value="Antes dos agentes, eu organizaria contatos e retornos.",
                        source="diagnostic_ledger",
                        max_length=260,
                    )
                },
            ),
            RenderPlanItem(
                template_id="diagnostic.deliver_operational_step",
                variables={
                    "operational_first_step": _value(
                        kind="long_text",
                        value=(
                            "O primeiro passo e separar novos interessados de "
                            "retornos pendentes."
                        ),
                        source="diagnostic_ledger",
                        max_length=240,
                    )
                },
            ),
            RenderPlanItem(
                template_id="diagnostic.deliver_agent_recommendation",
                variables=_agent_variables(
                    "Atendimento",
                    "faria sentido primeiro",
                    "demora no retorno",
                ),
            ),
            RenderPlanItem(
                template_id="diagnostic.deliver_agent_recommendation#2",
                variables=_agent_variables(
                    "Agenda",
                    "tambem faria sentido",
                    "reposicoes perdidas",
                ),
            ),
            RenderPlanItem(
                template_id="diagnostic.deliver_plan_recommendation",
                variables={
                    "recommended_plan_or_range": _value(
                        kind="short_text",
                        value="Avance",
                        source="official_product_knowledge",
                        max_length=90,
                    )
                },
            ),
            RenderPlanItem(
                template_id="diagnostic.deliver_demo_not_offered",
                variables={
                    "demo_status": _value(
                        kind="enum",
                        value="not_offered",
                        source="runtime_state",
                    )
                },
            ),
        ],
    )

    messages = render_validated_template_plan(
        plan,
        _passed_validation(),
        channel="widget",
    )
    texts = [message.text for message in messages]

    assert [message.sequence for message in messages] == list(range(1, 9))
    assert [message.template_id for message in messages] == [
        "diagnostic.deliver_hold",
        "diagnostic.deliver_context",
        "diagnostic.deliver_crm_base",
        "diagnostic.deliver_operational_step",
        "diagnostic.deliver_agent_recommendation",
        "diagnostic.deliver_agent_recommendation#2",
        "diagnostic.deliver_plan_recommendation",
        "diagnostic.deliver_demo_not_offered",
    ]
    assert "Agente Atendimento: ajuda com demora no retorno" in texts[4]
    assert "Na pratica: ele organiza a fila" in texts[4]
    assert "Agente Agenda: ajuda com reposicoes perdidas" in texts[5]
    assert "Na pratica: ele organiza a fila" in texts[5]
    assert texts[-1].endswith(
        "Temos algumas demonstracoes que mostram o funcionamento na pratica. "
        "Quer que eu te mande?"
    )


def test_renderer_preserves_demo_already_offered_final_sentence() -> None:
    plan = RenderPlan(
        chunk_policy="staged_diagnostic",
        items=[
            RenderPlanItem(
                template_id="diagnostic.deliver_demo_already_offered",
                variables={
                    "demo_status": _value(
                        kind="enum",
                        value="offered",
                        source="runtime_state",
                    )
                },
            )
        ],
    )

    messages = render_validated_template_plan(
        plan,
        _passed_validation(),
        channel="whatsapp",
    )

    assert messages[-1].text.endswith(
        "Chegou a olhar as demonstracoes? O que voce achou?"
    )
