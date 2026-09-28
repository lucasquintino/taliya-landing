from __future__ import annotations

from app.core.taliya_commercial.renderer import (
    TemplateBodyLine,
    validate_renderer_template_bodies,
)


def test_renderer_approved_body_contract_is_clean() -> None:
    assert validate_renderer_template_bodies() == []


def test_renderer_body_contract_rejects_unknown_placeholder_variable() -> None:
    errors = validate_renderer_template_bodies(
        {
            "product.price_direct": (
                TemplateBodyLine(
                    "{invented_fact}",
                    required_variables=frozenset({"invented_fact"}),
                ),
            )
        }
    )

    assert "unknown_body_variable:product.price_direct:invented_fact" in errors


def test_renderer_body_contract_rejects_undeclared_placeholder() -> None:
    errors = validate_renderer_template_bodies(
        {
            "product.price_direct": (
                TemplateBodyLine("{plan_price_summary}"),
            )
        }
    )

    assert "undeclared_body_placeholder:product.price_direct:plan_price_summary" in errors


def test_renderer_body_contract_rejects_required_variable_on_optional_line() -> None:
    errors = validate_renderer_template_bodies(
        {
            "product.price_direct": (
                TemplateBodyLine(
                    "{plan_price_summary}",
                    required_variables=frozenset({"plan_price_summary"}),
                    optional=True,
                ),
            )
        }
    )

    assert (
        "required_variable_on_optional_line:product.price_direct:plan_price_summary"
        in errors
    )


def test_renderer_body_contract_rejects_required_template_variable_not_rendered() -> None:
    errors = validate_renderer_template_bodies(
        {
            "product.price_direct": (
                TemplateBodyLine("Nao uso a variavel obrigatoria aqui."),
            )
        }
    )

    assert (
        "required_template_variable_not_rendered:"
        "product.price_direct:plan_price_summary"
    ) in errors
