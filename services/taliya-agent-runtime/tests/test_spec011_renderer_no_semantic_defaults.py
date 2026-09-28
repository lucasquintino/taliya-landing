from __future__ import annotations

import pytest

from app.core.taliya_commercial.renderer import (
    RenderError,
    render_validated_template_plan,
)
from app.core.taliya_commercial.schemas import (
    RenderPlan,
    RenderPlanItem,
    TemplateVariableValue,
    ValidatorResult,
)


def _passed_validation() -> ValidatorResult:
    return ValidatorResult(
        decision_id="decision_renderer_defaults_1",
        status="passed",
        final_disposition="accepted",
    )


def _value(
    *,
    kind: str,
    value: str,
    source: str,
    evidence: list[str] | None = None,
    max_length: int | None = None,
) -> TemplateVariableValue:
    return TemplateVariableValue.model_validate(
        {
            "kind": kind,
            "value": value,
            "source": source,
            "evidence": evidence or ["structured_evidence"],
            **({"max_length": max_length} if max_length is not None else {}),
        }
    )


def _plan(template_id: str, variables: dict[str, TemplateVariableValue]) -> RenderPlan:
    return RenderPlan(
        items=[RenderPlanItem(template_id=template_id, variables=variables)]
    )


def _render_text(plan: RenderPlan) -> str:
    messages = render_validated_template_plan(
        plan,
        _passed_validation(),
        channel="whatsapp",
    )
    return "\n".join(message.text for message in messages)


def test_renderer_does_not_default_missing_plan_fit_context() -> None:
    with pytest.raises(RenderError, match="plan_fit_context"):
        _render_text(_plan("product.plan_fit_with_diagnostic", {}))

    text = _render_text(
        _plan(
            "product.plan_fit_with_diagnostic",
            {
                "plan_fit_context": _value(
                    kind="short_text",
                    value="Pelo que voce contou, ainda falta comparar com calma.",
                    source="user_message",
                    evidence=["lead asked which plan fits"],
                    max_length=180,
                )
            },
        )
    )

    assert "Pelo que voce contou" in text
    assert "diagnostico gratuito" in text


def test_renderer_does_not_default_missing_current_tool_context() -> None:
    with pytest.raises(RenderError, match="current_tool_context"):
        _render_text(_plan("product.comparison_current_tool", {}))

    text = _render_text(
        _plan(
            "product.comparison_current_tool",
            {
                "current_tool_context": _value(
                    kind="short_text",
                    value="uma planilha compartilhada",
                    source="user_message",
                    evidence=["lead mentioned spreadsheet"],
                    max_length=120,
                )
            },
        )
    )

    assert "uma planilha compartilhada" in text
    assert "o processo atual" not in text


def test_renderer_does_not_default_missing_integration_topic() -> None:
    with pytest.raises(RenderError, match="integration_topic"):
        _render_text(_plan("product.integration_scope_direct", {}))

    text = _render_text(
        _plan(
            "product.integration_scope_direct",
            {
                "integration_topic": _value(
                    kind="short_text",
                    value="integracao com agenda externa",
                    source="user_message",
                    evidence=["lead asked about calendar integration"],
                    max_length=100,
                )
            },
        )
    )

    assert "integracao com agenda externa" in text
    assert "essa integracao" not in text


def test_renderer_omits_optional_feedback_without_replacing_it() -> None:
    text_without_feedback = _render_text(_plan("diagnostic.ask_priority", {}))

    assert text_without_feedback == (
        "Pensando na rotina do studio, qual tarefa voce mais gostaria de deixar "
        "mais leve primeiro?"
    )

    text_with_feedback = _render_text(
        _plan(
            "diagnostic.ask_priority",
            {
                "answer_feedback": _value(
                    kind="short_text",
                    value="Boa, isso ajuda a separar agenda de vendas.",
                    source="diagnostic_ledger",
                    evidence=["diagnostic.priority_context"],
                    max_length=180,
                )
            },
        )
    )

    assert text_with_feedback.startswith("Boa, isso ajuda")
    assert "Pensando na rotina do studio" in text_with_feedback
