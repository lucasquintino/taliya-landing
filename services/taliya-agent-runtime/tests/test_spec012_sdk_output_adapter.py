from __future__ import annotations

from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from app.core.taliya_commercial_sdk import (
    PRODUCT_AGENT,
    TRIAGE_AGENT,
    SdkOutputAdapterError,
    TaliyaTurnProposal,
    adapt_sdk_output_to_turn_proposal,
)


def _base_proposal_payload() -> dict[str, object]:
    return {
        "agent_path": [{"event": "start", "agent": TRIAGE_AGENT}],
        "commercial_understanding": {
            "intents": ["price_question", "pain_context"],
            "direct_question": "quanto custa?",
            "pain_context": "perco leads no WhatsApp",
            "mixed_intent": True,
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
                "claim": "pricing summary must use official plan refs",
                "fact_refs": ["product_knowledge.prices"],
                "evidence": ["product_knowledge.prices"],
            }
        ],
        "diagnostic_proposal": {
            "ledger_updates": [],
            "next_question_key": "active_students_or_size",
            "final_diagnostic_ready": False,
            "evidence": ["inbound.text"],
        },
        "demo_proposal": {"status": "not_offered", "next_step": "none", "evidence": []},
        "waitlist_proposal": {
            "eligibility": "unknown",
            "intent": "none",
            "missing_details": [],
            "evidence": [],
        },
        "handoff_proposal": {
            "status": "none",
            "reason": None,
            "pause_required": False,
            "evidence": [],
        },
        "template_proposal": {
            "template_ids": ["product.price_direct"],
            "variables": {
                "plan_price_summary": {
                    "kind": "long_text",
                    "source": "official_product_knowledge",
                    "evidence": ["product_knowledge.prices"],
                    "max_length": 360,
                }
            },
            "evidence": ["product_knowledge.prices"],
        },
        "safety": {"guardrails": [], "uncertainty": "low"},
        "state_patch_proposal": {"demo": {"status": "not_offered"}},
        "sales_inbox_projection_proposal": {"commercial_stage": "product_question"},
        "delivery_proposal": {
            "chunk_policy": "none",
            "render_plan_only": True,
            "evidence": ["template_registry.product.price_direct"],
        },
        "confidence": "medium",
        "risks": [],
        "usage": {
            "model": "gpt-test-no-call",
            "model_operations": 1,
            "input_tokens": 0,
            "output_tokens": 0,
            "cost_usd": 0,
            "handoffs": 0,
            "repairs": 0,
        },
    }


def test_spec012_turn_proposal_schema_accepts_structured_proposal() -> None:
    proposal = TaliyaTurnProposal.model_validate(
        {
            **_base_proposal_payload(),
            "turn_id": "turn_123",
            "conversation_id": "conv_123",
            "channel": "widget",
            "starting_agent": TRIAGE_AGENT,
        }
    )

    assert proposal.schema_version == "012.turn_proposal.v1"
    assert proposal.agent_path[0].event == "start"
    assert proposal.delivery_proposal.render_plan_only is True
    assert proposal.product_claims[0].fact_refs == ["product_knowledge.prices"]


def test_spec012_output_adapter_adds_runtime_identity_fields() -> None:
    proposal = adapt_sdk_output_to_turn_proposal(
        {"final_output": _base_proposal_payload()},
        turn_id="turn_adapter_1",
        conversation_id="conv_adapter_1",
        channel="whatsapp",
        starting_agent=TRIAGE_AGENT,
    )

    assert proposal.turn_id == "turn_adapter_1"
    assert proposal.conversation_id == "conv_adapter_1"
    assert proposal.channel == "whatsapp"
    assert proposal.starting_agent == TRIAGE_AGENT


def test_spec012_output_adapter_extracts_basic_sdk_run_items_when_agent_path_missing() -> None:
    sdk_result = SimpleNamespace(
        final_output={
            key: value
            for key, value in _base_proposal_payload().items()
            if key != "agent_path"
        },
        last_agent=SimpleNamespace(name=PRODUCT_AGENT),
        new_items=[
            SimpleNamespace(
                type="tool_call_item",
                agent=SimpleNamespace(name=PRODUCT_AGENT),
                name="get_product_knowledge",
            )
        ],
    )

    proposal = adapt_sdk_output_to_turn_proposal(
        sdk_result,
        turn_id="turn_adapter_2",
        conversation_id="conv_adapter_2",
        channel="widget",
        starting_agent=TRIAGE_AGENT,
    )

    assert proposal.agent_path[0].event == "start"
    assert any(
        item.event == "tool" and item.tool_name == "get_product_knowledge"
        for item in proposal.agent_path
    )
    assert any(
        item.event == "handoff" and item.to_agent == PRODUCT_AGENT
        for item in proposal.agent_path
    )
    assert proposal.agent_path[-1].event == "final"


def test_spec012_output_adapter_rejects_freeform_final_output() -> None:
    with pytest.raises(SdkOutputAdapterError, match="sdk_final_output_must_be_structured_proposal"):
        adapt_sdk_output_to_turn_proposal(
            {"final_output": "Claro, vou te explicar o preco agora."},
            turn_id="turn_bad_text",
            conversation_id="conv_bad_text",
            channel="widget",
            starting_agent=TRIAGE_AGENT,
        )


@pytest.mark.parametrize("forbidden_key", ["final_text", "message", "full_response"])
def test_spec012_turn_proposal_rejects_direct_output_fields(forbidden_key: str) -> None:
    payload = {
        **_base_proposal_payload(),
        forbidden_key: "Texto final para enviar ao lead.",
        "turn_id": "turn_bad_direct",
        "conversation_id": "conv_bad_direct",
        "channel": "widget",
        "starting_agent": TRIAGE_AGENT,
    }

    with pytest.raises(ValidationError, match="forbidden direct-output fields"):
        TaliyaTurnProposal.model_validate(payload)


def test_spec012_turn_proposal_rejects_product_claim_without_fact_ref() -> None:
    payload = {
        **_base_proposal_payload(),
        "product_claims": [
            {
                "claim": "Taliya has a special launch discount",
                "fact_refs": [],
                "evidence": ["model.claim"],
            }
        ],
        "turn_id": "turn_bad_claim",
        "conversation_id": "conv_bad_claim",
        "channel": "widget",
        "starting_agent": TRIAGE_AGENT,
    }

    with pytest.raises(ValidationError, match="product claims require official fact refs"):
        TaliyaTurnProposal.model_validate(payload)


def test_spec012_output_adapter_does_not_import_public_runtime_endpoint() -> None:
    import inspect

    import app.main as runtime_main

    main_source = inspect.getsource(runtime_main)
    assert "run_action_first_agent_turn" in main_source
    assert "spec012_action_first_enabled" not in main_source
    assert "run_spec011_agent_turn" not in main_source
    assert "adapt_sdk_output_to_turn_proposal" not in main_source
