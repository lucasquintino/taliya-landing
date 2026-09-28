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
        decision_id="decision_renderer_channel_1",
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
            "evidence": ["validated_variable"],
            **({"max_length": max_length} if max_length is not None else {}),
        }
    )


def _price_item() -> RenderPlanItem:
    return RenderPlanItem(
        template_id="product.price_direct",
        variables={
            "plan_price_summary": _value(
                kind="long_text",
                value="Resumo oficial de planos.",
                source="official_product_knowledge",
                max_length=360,
            )
        },
    )


def _plan_fit_item() -> RenderPlanItem:
    return RenderPlanItem(
        template_id="product.plan_fit_with_diagnostic",
        variables={
            "plan_fit_context": _value(
                kind="short_text",
                value="Para comparar plano, preciso olhar o contexto do studio.",
                source="user_message",
                max_length=180,
            )
        },
    )


def test_whatsapp_max_three_policy_caps_normal_output_without_buttons() -> None:
    plan = RenderPlan(
        chunk_policy="whatsapp_max_3",
        items=[_price_item(), _plan_fit_item()],
    )

    messages = render_validated_template_plan(
        plan,
        _passed_validation(),
        channel="whatsapp",
    )

    assert len(messages) == 3
    assert [message.sequence for message in messages] == [1, 2, 3]
    assert all(message.channel == "whatsapp" for message in messages)
    assert all(not hasattr(message, "kind") for message in messages)
    assert all(not hasattr(message, "buttons") for message in messages)


def test_widget_output_is_not_capped_by_whatsapp_policy() -> None:
    plan = RenderPlan(
        chunk_policy="whatsapp_max_3",
        items=[_price_item(), _plan_fit_item()],
    )

    messages = render_validated_template_plan(
        plan,
        _passed_validation(),
        channel="widget",
    )

    assert len(messages) == 6
    assert [message.sequence for message in messages] == [1, 2, 3, 4, 5, 6]
    assert all(message.channel == "widget" for message in messages)


def test_staged_diagnostic_is_not_truncated_for_whatsapp() -> None:
    plan = RenderPlan(
        chunk_policy="staged_diagnostic",
        items=[
            RenderPlanItem(template_id="diagnostic.deliver_hold"),
            RenderPlanItem(
                template_id="diagnostic.deliver_demo_already_offered",
                variables={
                    "demo_status": _value(
                        kind="enum",
                        value="offered",
                        source="runtime_state",
                    )
                },
            ),
        ],
    )

    messages = render_validated_template_plan(
        plan,
        _passed_validation(),
        channel="whatsapp",
    )

    assert len(messages) == 2
    assert messages[-1].text.endswith(
        "Chegou a olhar as demonstracoes? O que voce achou?"
    )


def test_staged_diagnostic_whatsapp_is_coalesced_to_three_chunks() -> None:
    plan = RenderPlan(
        chunk_policy="staged_diagnostic",
        items=[
            RenderPlanItem(template_id="diagnostic.deliver_hold"),
            RenderPlanItem(
                template_id="diagnostic.deliver_context",
                variables={
                    "pain_context_human": _value(
                        kind="long_text",
                        value="O peso principal esta no retorno comercial.",
                        source="diagnostic_ledger",
                        max_length=420,
                    )
                },
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
        channel="whatsapp",
    )

    assert len(messages) == 3
    assert [message.sequence for message in messages] == [1, 2, 3]
    assert messages[-1].text.endswith("Quer que eu te mande?")


def test_demo_link_is_plain_text_from_validated_variable_for_both_channels() -> None:
    url = "https://www.taliya.com.br/pilates/planos/demonstracao"
    plan = RenderPlan(
        items=[
            RenderPlanItem(
                template_id="product.demo_direct",
                variables={
                    "official_demo_link": _value(
                        kind="url",
                        value=url,
                        source="official_product_knowledge",
                    )
                },
            )
        ]
    )

    whatsapp_messages = render_validated_template_plan(
        plan,
        _passed_validation(),
        channel="whatsapp",
    )
    widget_messages = render_validated_template_plan(
        plan,
        _passed_validation(),
        channel="widget",
    )

    assert any(message.text == f"Ver demonstracao: {url}" for message in whatsapp_messages)
    assert any(message.text == f"Ver demonstracao: {url}" for message in widget_messages)
    assert all(not hasattr(message, "kind") for message in whatsapp_messages)
    assert all(not hasattr(message, "kind") for message in widget_messages)
