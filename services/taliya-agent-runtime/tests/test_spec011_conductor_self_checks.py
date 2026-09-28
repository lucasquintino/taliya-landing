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

ALL_POLICY_CHECKS_TRUE = {
    "direct_question_answered_first": True,
    "diagnostic_timing_ok": True,
    "waitlist_timing_ok": True,
    "official_facts_only": True,
    "no_internal_text_leak": True,
    "no_early_contact_capture": True,
    "no_human_overlap": True,
}

ALL_POLICY_CHECKS_FALSE = {
    "direct_question_answered_first": False,
    "diagnostic_timing_ok": False,
    "waitlist_timing_ok": False,
    "official_facts_only": False,
    "no_internal_text_leak": False,
    "no_early_contact_capture": False,
    "no_human_overlap": False,
}


def _request(text: str = "Quanto custa e como funciona?") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_self_checks_1",
                "lead_id": "lead_self_checks_1",
                "channel_conversation_id": "wa_self_checks_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_self_checks_1:1",
                "channel_message_id": "wamid_self_checks_1",
                "type": "text",
                "text": text,
            },
            "sender": {"name": "Ana"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _context(text: str = "Quanto custa e como funciona?") -> TurnContext:
    return build_turn_context(
        turn_id="turn_self_checks_1",
        request=_request(text),
        state=RuntimeState(
            conversation_id="conv_self_checks_1",
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
        "policy_checks": dict(ALL_POLICY_CHECKS_TRUE),
        "confidence": "high",
    }


def _model_usage() -> dict[str, Any]:
    return {
        "model": "gpt-5.4-mini",
        "input_tokens": 123,
        "output_tokens": 36,
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
async def test_conductor_accepts_explicit_policy_self_checks() -> None:
    context = _context()
    provider = FakeConductorProvider(_valid_decision_payload(context))

    result = await conduct_turn(context, provider=provider)

    assert result.decision.policy_checks.direct_question_answered_first is True
    assert result.decision.policy_checks.diagnostic_timing_ok is True
    assert result.decision.policy_checks.waitlist_timing_ok is True
    assert result.decision.policy_checks.official_facts_only is True
    assert result.decision.policy_checks.no_internal_text_leak is True
    assert result.decision.policy_checks.no_early_contact_capture is True
    assert result.decision.policy_checks.no_human_overlap is True


@pytest.mark.asyncio
async def test_conductor_accepts_false_policy_self_checks_as_advisory() -> None:
    context = _context()
    payload = _valid_decision_payload(context)
    payload["policy_checks"] = dict(ALL_POLICY_CHECKS_FALSE)

    result = await conduct_turn(context, provider=FakeConductorProvider(payload))

    assert result.decision.policy_checks.direct_question_answered_first is False
    assert result.decision.policy_checks.official_facts_only is False


@pytest.mark.asyncio
async def test_conductor_rejects_missing_policy_checks_in_provider_output() -> None:
    context = _context()
    payload = _valid_decision_payload(context)
    payload.pop("policy_checks")

    with pytest.raises(ConductorDecisionValidationError):
        await conduct_turn(context, provider=FakeConductorProvider(payload))


@pytest.mark.asyncio
async def test_conductor_rejects_partial_policy_checks_in_provider_output() -> None:
    context = _context()
    payload = _valid_decision_payload(context)
    payload["policy_checks"].pop("no_human_overlap")

    with pytest.raises(ConductorDecisionValidationError):
        await conduct_turn(context, provider=FakeConductorProvider(payload))


@pytest.mark.asyncio
async def test_policy_self_checks_do_not_bypass_validator_repair_boundary() -> None:
    context = _context()
    payload = _valid_decision_payload(context)
    payload["policy_checks"] = dict(ALL_POLICY_CHECKS_TRUE)
    payload["template_plan"]["items"] = []

    result = await conduct_turn(context, provider=FakeConductorProvider(payload))
    validator_result = validate_conductor_result(result.decision, context)

    assert validator_result.status == "repairable"
    assert validator_result.errors[0].code == "template_plan_empty"


@pytest.mark.asyncio
async def test_conductor_request_describes_self_checks_as_advisory() -> None:
    provider = FakeConductorProvider()

    await conduct_turn(_context(), provider=provider)

    instructions = " ".join(provider.calls[0].instructions).lower()
    assert "policy_checks" in instructions
    assert "false when uncertain" in instructions
    assert "not final validation" in instructions
