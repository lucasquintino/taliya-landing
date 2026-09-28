from __future__ import annotations

from typing import Any

import pytest

from app.core.taliya_commercial.conductor import (
    ConductorDecisionValidationError,
    ConductorProviderRequest,
    ConductorTurnResult,
    conduct_turn,
)
from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.schemas import TurnContext
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState


def _request(text: str = "Quanto custa?") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_usage_1",
                "lead_id": "lead_usage_1",
                "channel_conversation_id": "wa_usage_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_usage_1:1",
                "channel_message_id": "wamid_usage_1",
                "type": "text",
                "text": text,
            },
            "sender": {"name": "Ana"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _context(text: str = "Quanto custa?") -> TurnContext:
    return build_turn_context(
        turn_id="turn_usage_1",
        request=_request(text),
        state=RuntimeState(
            conversation_id="conv_usage_1",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_product_agent",
            summary="Lead perguntou sobre preco.",
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
        "detected_intents": ["price_question"],
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
        "input_tokens": 321,
        "output_tokens": 64,
        "cost_usd": 0.0021,
    }


def _provider_result(context: TurnContext) -> dict[str, Any]:
    return {"decision": _valid_decision_payload(context), "model_usage": _model_usage()}


class FakeConductorProvider:
    def __init__(self, output: Any | None = None) -> None:
        self.output = output
        self.calls: list[ConductorProviderRequest] = []

    async def __call__(self, request: ConductorProviderRequest) -> Any:
        self.calls.append(request)
        if self.output is None:
            return _provider_result(request.context)
        return self.output


@pytest.mark.asyncio
async def test_conductor_returns_decision_with_model_usage() -> None:
    context = _context()

    result = await conduct_turn(context, provider=FakeConductorProvider())

    assert isinstance(result, ConductorTurnResult)
    assert result.decision.route == "product"
    assert result.model_usage.model == "gpt-5.4-mini"
    assert result.model_usage.input_tokens == 321
    assert result.model_usage.output_tokens == 64
    assert result.model_usage.cost_usd == 0.0021


@pytest.mark.asyncio
async def test_conductor_rejects_bare_decision_without_usage() -> None:
    context = _context()

    with pytest.raises(ConductorDecisionValidationError):
        await conduct_turn(
            context,
            provider=FakeConductorProvider(_valid_decision_payload(context)),
        )


@pytest.mark.asyncio
async def test_conductor_rejects_provider_result_missing_usage() -> None:
    context = _context()

    with pytest.raises(ConductorDecisionValidationError):
        await conduct_turn(
            context,
            provider=FakeConductorProvider({"decision": _valid_decision_payload(context)}),
        )


@pytest.mark.asyncio
async def test_conductor_rejects_empty_model_name() -> None:
    context = _context()
    output = _provider_result(context)
    output["model_usage"]["model"] = " "

    with pytest.raises(ConductorDecisionValidationError):
        await conduct_turn(context, provider=FakeConductorProvider(output))


@pytest.mark.asyncio
async def test_conductor_rejects_zero_token_usage() -> None:
    context = _context()
    output = _provider_result(context)
    output["model_usage"]["input_tokens"] = 0

    with pytest.raises(ConductorDecisionValidationError):
        await conduct_turn(context, provider=FakeConductorProvider(output))


@pytest.mark.asyncio
async def test_provider_request_requires_usage_envelope_outside_llm_decision() -> None:
    provider = FakeConductorProvider()

    await conduct_turn(_context(), provider=provider)

    requirements = " ".join(provider.calls[0].provider_requirements).lower()
    assert "model_usage" in requirements
    assert "decision" in requirements
    assert "outside the llm decision json" in requirements
