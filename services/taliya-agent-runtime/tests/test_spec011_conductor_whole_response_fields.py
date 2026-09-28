from __future__ import annotations

from typing import Any

import pytest

from app.core.taliya_commercial.conductor import (
    ConductorDecisionValidationError,
    ConductorProviderRequest,
    conduct_turn,
)
from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.schemas import (
    FORBIDDEN_TEMPLATE_VARIABLE_NAMES,
    TurnContext,
)
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState


def _request(text: str = "Quero entender os planos da Taliya.") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_whole_response_1",
                "lead_id": "lead_whole_response_1",
                "channel_conversation_id": "wa_whole_response_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_whole_response_1:1",
                "channel_message_id": "wamid_whole_response_1",
                "type": "text",
                "text": text,
            },
            "sender": {"name": "Ana"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _context(text: str = "Quero entender os planos da Taliya.") -> TurnContext:
    return build_turn_context(
        turn_id="turn_whole_response_1",
        request=_request(text),
        state=RuntimeState(
            conversation_id="conv_whole_response_1",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_product_agent",
            summary="Lead pediu contexto sobre planos.",
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
        "detected_intents": ["product_question"],
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
        "input_tokens": 140,
        "output_tokens": 37,
        "cost_usd": 0.0012,
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
        return self.output


@pytest.mark.asyncio
@pytest.mark.parametrize("field_name", sorted(FORBIDDEN_TEMPLATE_VARIABLE_NAMES))
async def test_conductor_rejects_top_level_whole_response_fields(
    field_name: str,
) -> None:
    context = _context()
    output = _provider_result(_valid_decision_payload(context))
    output[field_name] = "Texto pronto que tentaria bypassar o renderer."
    provider = FakeConductorProvider(output)

    with pytest.raises(ConductorDecisionValidationError, match=field_name):
        await conduct_turn(context, provider=provider)

    assert len(provider.calls) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("field_name", sorted(FORBIDDEN_TEMPLATE_VARIABLE_NAMES))
async def test_conductor_rejects_decision_whole_response_fields_even_with_valid_plan(
    field_name: str,
) -> None:
    context = _context()
    decision = _valid_decision_payload(context)
    decision[field_name] = "Texto pronto que tentaria bypassar o renderer."
    provider = FakeConductorProvider(_provider_result(decision))

    with pytest.raises(ConductorDecisionValidationError, match=field_name):
        await conduct_turn(context, provider=provider)

    assert len(provider.calls) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("field_name", sorted(FORBIDDEN_TEMPLATE_VARIABLE_NAMES))
async def test_conductor_rejects_forbidden_template_variable_names(
    field_name: str,
) -> None:
    context = _context()
    decision = _valid_decision_payload(context)
    variables = decision["template_plan"]["items"][0]["variables"]
    variables[field_name] = {
        "kind": "long_text",
        "value": "Texto pronto que tentaria bypassar o renderer.",
        "source": "model_decision",
        "evidence": ["model_decision.freeform_text"],
        "max_length": 360,
    }
    provider = FakeConductorProvider(_provider_result(decision))

    with pytest.raises(ConductorDecisionValidationError, match=field_name):
        await conduct_turn(context, provider=provider)

    assert len(provider.calls) == 1


@pytest.mark.asyncio
async def test_conductor_request_names_forbidden_whole_response_fields() -> None:
    provider = FakeConductorProvider()

    await conduct_turn(_context(), provider=provider)

    request_text = " ".join(
        [
            *provider.calls[0].instructions,
            *provider.calls[0].provider_requirements,
        ]
    )
    assert "customer-facing free-form assistant text" in request_text
    for field_name in FORBIDDEN_TEMPLATE_VARIABLE_NAMES:
        assert field_name in request_text
