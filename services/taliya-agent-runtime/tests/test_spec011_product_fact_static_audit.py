from __future__ import annotations

from app.core.taliya_commercial.product_fact_static_audit import (
    audit_product_fact_locations,
)


def test_product_fact_audit_blocks_forbidden_prompt_template_and_fallback_literals() -> None:
    result = audit_product_fact_locations(
        {
            "app/core/taliya_commercial/conductor_policy.py": (
                "Nunca prometa checkout seguro ou desconto vip."
            ),
            "app/core/taliya_commercial/templates.py": (
                "Plano por R$ 497 com data de abertura garantida."
            ),
            "app/core/taliya_commercial/fallback.py": (
                "Use openai_demo ou demo_video se falhar."
            ),
        }
    )

    assert result.passed is False
    assert {finding.code for finding in result.findings} >= {
        "product_fact_payment_promise",
        "product_fact_price_literal",
        "product_fact_availability_promise",
        "product_fact_technical_demo",
    }


def test_product_fact_audit_allows_official_sources_and_explicit_fixture_metadata() -> None:
    result = audit_product_fact_locations(
        {
            "app/core/taliya_commercial/product_knowledge.py": "R$ 497",
            "specs/006-crm-operational-core/product-contract.md": "checkout seguro",
            "tests/fixtures/spec011_do_not_do.json": "desconto vip",
        },
        allowlisted_paths={
            "tests/fixtures/spec011_do_not_do.json",
        },
    )

    assert result.passed is True
    assert result.findings == []


def test_product_fact_audit_returns_line_level_evidence() -> None:
    result = audit_product_fact_locations(
        {
            "app/core/taliya_commercial/templates.py": (
                "linha segura\n"
                "integração garantida com certificação oficial\n"
            )
        }
    )

    assert result.passed is False
    assert result.findings[0].path == "app/core/taliya_commercial/templates.py"
    assert result.findings[0].line == 2
    assert "integra" in result.findings[0].snippet
