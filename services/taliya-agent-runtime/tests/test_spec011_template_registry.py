from __future__ import annotations

import re
from pathlib import Path

from app.core.taliya_commercial.schemas import RenderPlanItem, TemplateVariableValue
from app.core.taliya_commercial.template_registry import (
    TEMPLATE_REGISTRY,
    VARIABLE_REGISTRY,
    validate_render_plan_item_variables,
    validate_template_registry,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
MESSAGE_TEMPLATE_CONTRACT = (
    REPO_ROOT
    / "specs/010-openai-cs-agents-adaptation-for-taliya-commercial/message-template-contract.md"
)
PRODUCT_FOLLOWUP_CONTRACT = (
    REPO_ROOT
    / "specs/010-openai-cs-agents-adaptation-for-taliya-commercial/"
    "product-followup-delta-contract.md"
)


def _section(text: str, start: str, end: str) -> str:
    start_index = text.index(start)
    end_index = text.index(end, start_index)
    return text[start_index:end_index]


def _template_ids(text: str) -> set[str]:
    return set(re.findall(r"`([a-z]+(?:\.[a-z0-9_]+)+)`", text))


def test_registry_covers_contract_approved_templates() -> None:
    message_contract = MESSAGE_TEMPLATE_CONTRACT.read_text(encoding="utf-8")
    product_contract = PRODUCT_FOLLOWUP_CONTRACT.read_text(encoding="utf-8")

    required_template_ids = set()
    required_template_ids.update(
        _template_ids(
            _section(message_contract, "## Template Categories", "## Template Record Shape")
        )
    )
    required_template_ids.update(
        _template_ids(
            _section(
                message_contract,
                "### New Required Templates",
                "Do not create `product.general_objection_response`",
            )
        )
    )
    required_template_ids.update(
        _template_ids(
            _section(
                product_contract,
                "## Protected Behavior That Must Not Change",
                "## Missing Or Partial Coverage To Implement",
            )
        )
    )

    assert required_template_ids - set(TEMPLATE_REGISTRY) == set()
    assert "product.general_objection_response" not in TEMPLATE_REGISTRY


def test_registry_is_internally_consistent_and_typed() -> None:
    assert validate_template_registry() == []

    for variable in VARIABLE_REGISTRY.values():
        assert variable.kind
        assert variable.allowed_sources
        assert variable.validation_rule
        if variable.kind in {"short_text", "long_text", "list"}:
            assert variable.max_length is not None


def test_registry_rejects_unknown_template_and_unregistered_variables() -> None:
    unknown_template = RenderPlanItem.model_validate(
        {
            "template_id": "product.unapproved_freeform",
            "variables": {},
        }
    )
    assert validate_render_plan_item_variables(unknown_template) == [
        "unknown_template_id:product.unapproved_freeform"
    ]

    hidden_reply = RenderPlanItem.model_validate(
        {
            "template_id": "product.price_direct",
            "variables": {
                "custom_reply": {
                    "kind": "long_text",
                    "value": "resposta comercial inteira escondida na variavel",
                    "source": "model_decision",
                    "evidence": ["model"],
                    "max_length": 500,
                }
            },
        }
    )

    assert "unknown_variable:custom_reply" in validate_render_plan_item_variables(
        hidden_reply
    )


def test_registry_validates_variable_shape_source_and_length() -> None:
    valid_how_it_works = RenderPlanItem.model_validate(
        {
            "template_id": "product.how_it_works_direct",
            "variables": {
                "contextual_next_step": {
                    "kind": "enum",
                    "value": "diagnostic_offer_with_pain",
                    "source": "model_decision",
                    "evidence": ["decision:product_followup"],
                }
            },
        }
    )
    assert validate_render_plan_item_variables(valid_how_it_works) == []

    invalid_how_it_works = RenderPlanItem.model_validate(
        {
            "template_id": "product.how_it_works_direct",
            "variables": {
                "contextual_next_step": {
                    "kind": "long_text",
                    "value": "texto livre grande o suficiente para virar resposta inteira",
                    "source": "model_decision",
                    "evidence": ["model"],
                    "max_length": 500,
                }
            },
        }
    )
    errors = validate_render_plan_item_variables(invalid_how_it_works)

    assert "kind_mismatch:contextual_next_step:long_text!=enum" in errors
    assert "max_length_too_large:contextual_next_step:500>0" in errors


def test_registry_validates_actual_text_value_length_before_rendering() -> None:
    too_long_variable = RenderPlanItem.model_validate(
        {
            "template_id": "diagnostic.deliver_crm_base",
            "variables": {
                "crm_base_recommendation": {
                    "kind": "long_text",
                    "value": "x" * 300,
                    "source": "diagnostic_ledger",
                    "evidence": ["diagnostic.ledger"],
                    "max_length": 260,
                }
            },
        }
    )

    assert "value_too_long:crm_base_recommendation:300>260" in (
        validate_render_plan_item_variables(too_long_variable)
    )

    invalid_price = RenderPlanItem.model_validate(
        {
            "template_id": "product.price_direct",
            "variables": {
                "plan_price_summary": {
                    "kind": "long_text",
                    "value": "497",
                    "source": "user_message",
                    "evidence": ["lead said 497"],
                    "max_length": 120,
                }
            },
        }
    )

    assert "source_not_allowed:plan_price_summary:user_message" in (
        validate_render_plan_item_variables(invalid_price)
    )


def test_registry_allows_reliable_channel_name_only_through_typed_first_name() -> None:
    named_opening = RenderPlanItem.model_validate(
        {
            "template_id": "opening.cold_greeting_named",
            "variables": {
                "first_name": {
                    "kind": "short_text",
                    "value": "Lucas",
                    "source": "channel_metadata",
                    "evidence": ["verified_person_name_fact"],
                    "max_length": 40,
                }
            },
        }
    )

    assert isinstance(named_opening.variables["first_name"], TemplateVariableValue)
    assert validate_render_plan_item_variables(named_opening) == []
