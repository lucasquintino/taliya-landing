from __future__ import annotations

import inspect

from app.core.taliya_commercial_sdk import (
    TRIAGE_AGENT,
    TaliyaTurnProposal,
    validate_and_render_spike_output,
)


def _proposal_payload() -> dict[str, object]:
    return {
        "turn_id": "turn_validator_1",
        "conversation_id": "conv_validator_1",
        "channel": "whatsapp",
        "starting_agent": TRIAGE_AGENT,
        "agent_path": [{"event": "start", "agent": TRIAGE_AGENT}],
        "commercial_understanding": {
            "intents": ["price_question"],
            "direct_question": "quanto custa?",
            "mixed_intent": False,
            "evidence": ["inbound.text"],
        },
        "answer_obligations": [
            {
                "obligation": "answer_price_before_diagnostic",
                "answered_before_steering": True,
                "evidence": ["inbound.text"],
            }
        ],
        "product_claims": [
            {
                "claim": "Use official plan prices only.",
                "fact_refs": ["product_knowledge.prices"],
                "evidence": ["product_knowledge.prices"],
            }
        ],
        "template_proposal": {
            "template_ids": ["product.price_direct"],
            "variables": {
                "plan_price_summary": {
                    "kind": "long_text",
                    "value": "Base R$ 197/mes; Essencial R$ 497/mes.",
                    "source": "official_product_knowledge",
                    "evidence": ["product_knowledge.prices"],
                    "max_length": 360,
                }
            },
            "evidence": ["product_knowledge.prices"],
        },
        "delivery_proposal": {
            "chunk_policy": "whatsapp_max_3",
            "render_plan_only": True,
            "evidence": ["template_registry.product.price_direct"],
        },
        "usage": {"model": "gpt-test-no-call", "model_operations": 1},
    }


def test_spec012_spike_validator_renders_approved_template_preview_only() -> None:
    proposal = TaliyaTurnProposal.model_validate(_proposal_payload())

    result = validate_and_render_spike_output(proposal)

    assert result.validator_result.status == "passed"
    assert result.commits_state is False
    assert result.public_delivery is False
    assert result.render_plan is not None
    assert [message.text for message in result.rendered_preview] == [
        "Oi, tudo bem?",
        "Base R$ 197/mês; Essencial R$ 497/mês.",
    ]
    assert all(message.template_id == "product.price_direct" for message in result.rendered_preview)


def test_spec012_spike_validator_blocks_unanswered_direct_question() -> None:
    payload = _proposal_payload()
    payload["answer_obligations"] = [
        {
            "obligation": "answer_price_before_diagnostic",
            "answered_before_steering": False,
            "evidence": ["inbound.text"],
        }
    ]
    proposal = TaliyaTurnProposal.model_validate(payload)

    result = validate_and_render_spike_output(proposal)

    assert result.validator_result.status == "failed"
    assert result.rendered_preview == []
    assert result.render_plan is None
    assert [issue.code for issue in result.validator_result.errors] == [
        "sdk_direct_question_not_answered_first"
    ]


def test_spec012_spike_validator_blocks_missing_required_template_variable() -> None:
    payload = _proposal_payload()
    payload["template_proposal"] = {
        "template_ids": ["product.price_direct"],
        "variables": {},
        "evidence": ["template_registry.product.price_direct"],
    }
    proposal = TaliyaTurnProposal.model_validate(payload)

    result = validate_and_render_spike_output(proposal)

    assert result.validator_result.status == "failed"
    assert result.rendered_preview == []
    assert result.render_plan is None
    assert result.validator_result.errors[0].code == "sdk_render_preview_failed"
    assert (
        "missing_required_variable:plan_price_summary"
        in result.validator_result.errors[0].message
    )


def test_spec012_spike_validator_blocks_unknown_template() -> None:
    payload = _proposal_payload()
    payload["template_proposal"] = {
        "template_ids": ["product.unapproved_freeform"],
        "variables": {},
        "evidence": ["model.template"],
    }
    proposal = TaliyaTurnProposal.model_validate(payload)

    result = validate_and_render_spike_output(proposal)

    assert result.validator_result.status == "failed"
    assert result.rendered_preview == []
    assert result.render_plan is None
    assert result.validator_result.errors[0].code == "sdk_unknown_template_id"


def test_spec012_spike_validator_adapter_does_not_parse_commercial_text() -> None:
    import app.core.taliya_commercial_sdk.validators_adapter as adapter

    source = inspect.getsource(adapter)
    assert "import re" not in source
    assert "route_from_text" not in source
    assert "BUY_INTENT_TOKENS" not in source
    assert "DIRECT_QUESTION_TOKENS" not in source


def test_spec012_spike_validator_adapter_is_not_public_endpoint_cutover() -> None:
    import app.main as runtime_main

    main_source = inspect.getsource(runtime_main)
    assert "run_action_first_agent_turn" in main_source
    assert "spec012_action_first_enabled" not in main_source
    assert "run_spec011_agent_turn" not in main_source
    assert "validate_and_render_spike_output" not in main_source
