from __future__ import annotations

import pytest

from app.core.taliya_commercial.renderer import (
    RenderError,
    render_validated_template_plan,
    validate_renderer_template_bodies,
)
from app.core.taliya_commercial.schemas import (
    RenderPlan,
    RenderPlanItem,
    TemplateVariableValue,
    ValidatorResult,
)


def _passed_validation(final_disposition: str = "accepted") -> ValidatorResult:
    return ValidatorResult(
        decision_id="decision_renderer_1",
        status="passed",
        final_disposition=final_disposition,
    )


def _price_plan() -> RenderPlan:
    return RenderPlan(
        items=[
            RenderPlanItem(
                template_id="product.price_direct",
                variables={
                    "plan_price_summary": TemplateVariableValue(
                        kind="long_text",
                        value="Planos oficiais carregados do contexto.",
                        source="official_product_knowledge",
                        evidence=["product_knowledge.prices"],
                        max_length=360,
                    )
                },
            )
        ]
    )


def test_renderer_accepts_only_validated_render_plan_and_returns_typed_messages() -> None:
    messages = render_validated_template_plan(
        _price_plan(),
        _passed_validation(),
        channel="whatsapp",
    )

    assert [message.text for message in messages] == [
        "Oi, tudo bem?",
        "Planos oficiais carregados do contexto.",
    ]
    assert messages[1].template_id == "product.price_direct"
    assert messages[1].channel == "whatsapp"
    assert messages[1].sequence == 2


def test_renderer_accepts_repaired_validator_disposition_after_revalidation() -> None:
    messages = render_validated_template_plan(
        _price_plan(),
        _passed_validation("repaired"),
        channel="widget",
    )

    assert messages[1].channel == "widget"
    assert messages[1].text == "Planos oficiais carregados do contexto."


def test_renderer_has_approved_price_objection_value_language() -> None:
    plan = RenderPlan(
        items=[RenderPlanItem(template_id="product.price_objection_value", variables={})]
    )

    messages = render_validated_template_plan(
        plan,
        _passed_validation(),
        channel="whatsapp",
    )
    text = "\n".join(message.text for message in messages).lower()

    assert "valor para olhar com calma" in text
    assert "nao e so" in text
    assert "whatsapp" in text
    assert "diagnostico gratuito" in text


def test_renderer_has_approved_body_for_diagnostic_opening_and_questions() -> None:
    plan = RenderPlan(
        items=[
            RenderPlanItem(template_id="opening.diagnostic_cta", variables={}),
            RenderPlanItem(template_id="diagnostic.ask_current_process", variables={}),
            RenderPlanItem(template_id="diagnostic.ask_pain_detail", variables={}),
            RenderPlanItem(template_id="diagnostic.ask_urgency", variables={}),
            RenderPlanItem(
                template_id="diagnostic.partial_progress",
                variables={
                    "answer_feedback": TemplateVariableValue(
                        kind="short_text",
                        value="Entendi: 120 alunos.",
                        source="diagnostic_ledger",
                        evidence=["diagnostic.ledger"],
                        max_length=180,
                    )
                },
            ),
        ]
    )

    messages = render_validated_template_plan(
        plan,
        _passed_validation(),
        channel="widget",
    )

    assert [message.template_id for message in messages] == [
        "opening.diagnostic_cta",
        "opening.diagnostic_cta",
        "diagnostic.ask_current_process",
        "diagnostic.ask_pain_detail",
        "diagnostic.ask_urgency",
        "diagnostic.partial_progress",
        "diagnostic.partial_progress",
    ]
    assert "rotina do studio" in messages[1].text
    assert "algum sistema" in messages[2].text


def test_renderer_maps_product_how_it_works_next_step_enum_to_approved_copy() -> None:
    plan = RenderPlan(
        items=[
            RenderPlanItem(
                template_id="product.how_it_works_direct",
                variables={
                    "contextual_next_step": TemplateVariableValue(
                        kind="enum",
                        value="diagnostic_offer_with_pain",
                        source="model_decision",
                        evidence=["decision:product_followup"],
                    )
                },
            )
        ]
    )

    messages = render_validated_template_plan(
        plan,
        _passed_validation(),
        channel="widget",
    )

    assert "WhatsApp Business" in messages[-1].text
    assert "diagnostico gratuito" in messages[-1].text


def test_renderer_has_approved_body_for_core_product_templates() -> None:
    plan = RenderPlan(
        items=[
            RenderPlanItem(template_id="product.overview_short", variables={}),
            RenderPlanItem(
                template_id="product.plan_direct",
                variables={
                    "plan_price_summary": TemplateVariableValue(
                        kind="long_text",
                        value="Base R$ 197/mes; Essencial R$ 497/mes.",
                        source="official_product_knowledge",
                        evidence=["product_knowledge.prices"],
                        max_length=360,
                    )
                },
            ),
        ]
    )

    messages = render_validated_template_plan(
        plan,
        _passed_validation(),
        channel="widget",
    )

    assert "studio de Pilates" in messages[0].text
    assert messages[1].text == "Base R$ 197/mes; Essencial R$ 497/mes."


def test_renderer_has_approved_body_for_new_operational_templates() -> None:
    assert validate_renderer_template_bodies() == []
    plan = RenderPlan(
        items=[
            RenderPlanItem(template_id="opening.cold_greeting", variables={}),
            RenderPlanItem(
                template_id="opening.cold_greeting_named",
                variables={
                    "first_name": TemplateVariableValue(
                        kind="short_text",
                        value="Ana",
                        source="channel_metadata",
                        evidence=["sender.name"],
                        max_length=40,
                    )
                },
            ),
            RenderPlanItem(template_id="opening.site_cta", variables={}),
            RenderPlanItem(template_id="waitlist.ask_missing_studio", variables={}),
            RenderPlanItem(
                template_id="waitlist.joined",
                variables={
                    "studio_name": TemplateVariableValue(
                        kind="short_text",
                        value="Studio Viva",
                        source="user_message",
                        evidence=["Studio Viva"],
                        max_length=80,
                    )
                },
            ),
            RenderPlanItem(template_id="safety.prompt_injection", variables={}),
            RenderPlanItem(template_id="fallback.unsupported_media", variables={}),
            RenderPlanItem(template_id="safety.unsupported_media", variables={}),
            RenderPlanItem(template_id="handoff.paused", variables={}),
        ]
    )

    messages = render_validated_template_plan(
        plan,
        _passed_validation(),
        channel="whatsapp",
    )

    texts = [message.text for message in messages]
    assert "Em que posso ajudar?" in texts
    assert "Studio: Studio Viva." in texts
    assert any("instrucoes internas" in text for text in texts)
    assert any("pessoa da Taliya" in text for text in texts)


@pytest.mark.parametrize("status", ["repairable", "blocked", "failed"])
def test_renderer_rejects_non_passed_validator_statuses(status: str) -> None:
    validator_result = ValidatorResult(
        decision_id="decision_renderer_rejected",
        status=status,
        final_disposition="blocked" if status == "blocked" else None,
    )

    with pytest.raises(RenderError, match="validated render plan"):
        render_validated_template_plan(
            _price_plan(),
            validator_result,
            channel="whatsapp",
        )


def test_renderer_rejects_fallback_disposition_before_rendering() -> None:
    validator_result = ValidatorResult(
        decision_id="decision_renderer_fallback",
        status="passed",
        final_disposition="fallback",
    )

    with pytest.raises(RenderError, match="validated render plan"):
        render_validated_template_plan(
            _price_plan(),
            validator_result,
            channel="whatsapp",
        )


def test_renderer_does_not_supply_semantic_defaults_for_missing_variables() -> None:
    missing_demo_link = RenderPlan(
        items=[
            RenderPlanItem(
                template_id="product.demo_direct",
                variables={},
            )
        ]
    )

    with pytest.raises(RenderError, match="missing_required_variable"):
        render_validated_template_plan(
            missing_demo_link,
            _passed_validation(),
            channel="widget",
        )


def test_renderer_rejects_template_channel_mismatch() -> None:
    widget_only_plan = RenderPlan(
        items=[
            RenderPlanItem(
                template_id="fallback.provider_timeout",
                channel="widget",
                variables={},
            )
        ]
    )

    with pytest.raises(RenderError, match="channel mismatch"):
        render_validated_template_plan(
            widget_only_plan,
            _passed_validation(),
            channel="whatsapp",
        )


def test_renderer_rejects_unknown_template_body_without_fallback_copy() -> None:
    unknown_template = RenderPlan(
        items=[
            RenderPlanItem(
                template_id="product.unapproved_freeform",
                variables={},
            )
        ]
    )

    with pytest.raises(RenderError, match="unknown_template_id"):
        render_validated_template_plan(
            unknown_template,
            _passed_validation(),
            channel="whatsapp",
        )
