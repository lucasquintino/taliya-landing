from __future__ import annotations

from typing import Any

import pytest

from app.core.taliya_commercial.conductor import (
    ConductorDecisionValidationError,
    ConductorProviderRequest,
    conduct_turn,
)
from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.schemas import TurnContext
from app.core.taliya_commercial.validators import validate_conductor_result
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState


def _request(text: str = "Quanto custa e como funciona?") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_template_plan_1",
                "lead_id": "lead_template_plan_1",
                "channel_conversation_id": "wa_template_plan_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_template_plan_1:1",
                "channel_message_id": "wamid_template_plan_1",
                "type": "text",
                "text": text,
            },
            "sender": {"name": "Ana"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _context(text: str = "Quanto custa e como funciona?") -> TurnContext:
    return build_turn_context(
        turn_id="turn_template_plan_1",
        request=_request(text),
        state=RuntimeState(
            conversation_id="conv_template_plan_1",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_product_agent",
            summary="Lead perguntou sobre preco e funcionamento.",
            diagnostic={"status": "not_started", "ledger": []},
            waitlist={"status": "none"},
            demo={"status": "not_offered"},
        ),
        recent_events=[],
        product_knowledge_keys=["prices"],
        spec006_contract_keys=["product_positioning"],
    )


def _valid_decision_payload(context: TurnContext) -> dict[str, Any]:
    return {
        "schema_version": "011.0",
        "turn_id": context.turn_id,
        "conversation_id": context.conversation_id,
        "channel": context.channel,
        "agent_key": context.agent_key,
        "role": "product",
        "route": "product",
        "previous_state": "new_lead",
        "current_state": "product_question",
        "next_state": "product_question",
        "detected_intents": ["price_question", "product_question"],
        "direct_question_present": True,
        "direct_question_answered_first": True,
        "language_policy": {
            "register": "studio_owner_practical",
            "crm_term_policy": "avoid_by_default",
        },
        "template_plan": {
            "items": [
                {
                    "template_id": "product.price_direct",
                    "variables": {
                        "plan_price_summary": {
                            "kind": "long_text",
                            "value": "Resumo de preco vindo de conhecimento oficial.",
                            "source": "official_product_knowledge",
                            "evidence": ["product_knowledge.prices"],
                            "max_length": 360,
                        }
                    },
                }
            ]
        },
        "policy_checks": {
            "direct_question_answered_first": True,
            "diagnostic_timing_ok": True,
            "waitlist_timing_ok": True,
            "official_facts_only": True,
            "no_internal_text_leak": True,
            "no_early_contact_capture": True,
            "no_human_overlap": True,
        },
        "confidence": "high",
    }


def _model_usage() -> dict[str, Any]:
    return {
        "model": "gpt-5.4-mini",
        "input_tokens": 122,
        "output_tokens": 35,
        "cost_usd": 0.001,
    }


def _provider_result(decision: dict[str, Any]) -> dict[str, Any]:
    return {"decision": decision, "model_usage": _model_usage()}


class FakeConductorProvider:
    def __init__(self, output: Any | None = None) -> None:
        self.output = output
        self.calls: list[ConductorProviderRequest] = []

    async def __call__(self, request: ConductorProviderRequest) -> Any:
        self.calls.append(request)
        if self.output is None:
            return _provider_result(_valid_decision_payload(request.context))
        if isinstance(self.output, dict) and "schema_version" in self.output:
            return _provider_result(self.output)
        return self.output


@pytest.mark.asyncio
async def test_conductor_accepts_registered_template_plan_with_typed_variables() -> None:
    context = _context()
    provider = FakeConductorProvider(_valid_decision_payload(context))

    result = await conduct_turn(context, provider=provider)

    plan_item = result.decision.template_plan.items[0]
    assert plan_item.template_id == "product.price_direct"
    assert plan_item.variables["plan_price_summary"].kind == "long_text"
    assert plan_item.variables["plan_price_summary"].source == "official_product_knowledge"
    assert plan_item.variables["plan_price_summary"].evidence == [
        "product_knowledge.prices"
    ]


@pytest.mark.asyncio
async def test_conductor_rejects_missing_template_plan() -> None:
    context = _context()
    payload = _valid_decision_payload(context)
    payload.pop("template_plan")

    with pytest.raises(ConductorDecisionValidationError):
        await conduct_turn(context, provider=FakeConductorProvider(payload))


@pytest.mark.asyncio
async def test_conductor_leaves_empty_template_plan_to_validators_for_repair() -> None:
    context = _context()
    payload = _valid_decision_payload(context)
    payload["template_plan"] = {"items": []}

    result = await conduct_turn(context, provider=FakeConductorProvider(payload))
    validator_result = validate_conductor_result(result.decision, context)

    assert validator_result.status == "repairable"
    assert validator_result.errors[0].code == "template_plan_empty"


@pytest.mark.asyncio
async def test_conductor_leaves_unregistered_template_id_to_validators_for_repair() -> None:
    context = _context()
    payload = _valid_decision_payload(context)
    payload["template_plan"]["items"][0]["template_id"] = "product.freeform_reply"

    result = await conduct_turn(context, provider=FakeConductorProvider(payload))
    validator_result = validate_conductor_result(result.decision, context)

    assert validator_result.status == "repairable"
    assert validator_result.errors[0].code == "template_plan_invalid"


@pytest.mark.asyncio
async def test_conductor_leaves_missing_template_variable_to_validators_for_repair() -> None:
    context = _context()
    payload = _valid_decision_payload(context)
    payload["template_plan"]["items"][0]["variables"] = {}

    result = await conduct_turn(context, provider=FakeConductorProvider(payload))
    validator_result = validate_conductor_result(result.decision, context)

    assert validator_result.status == "repairable"
    assert validator_result.errors[0].code == "template_plan_invalid"


@pytest.mark.asyncio
async def test_conductor_rejects_template_variable_without_evidence() -> None:
    context = _context()
    payload = _valid_decision_payload(context)
    payload["template_plan"]["items"][0]["variables"]["plan_price_summary"].pop(
        "evidence"
    )

    with pytest.raises(ConductorDecisionValidationError):
        await conduct_turn(context, provider=FakeConductorProvider(payload))


@pytest.mark.asyncio
async def test_conductor_request_mentions_registered_template_plan_not_freeform() -> None:
    provider = FakeConductorProvider()

    await conduct_turn(_context(), provider=provider)

    instructions = " ".join(provider.calls[0].instructions).lower()
    assert "registered template" in instructions
    assert "template variables" in instructions
    assert "whole-response" in instructions
