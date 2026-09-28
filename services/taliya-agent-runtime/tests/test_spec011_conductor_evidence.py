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
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState


def _request(text: str = "Vi o plano de 497 e tenho 120 alunos") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_evidence_1",
                "lead_id": "lead_evidence_1",
                "channel_conversation_id": "wa_evidence_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_evidence_1:1",
                "channel_message_id": "wamid_evidence_1",
                "type": "text",
                "text": text,
            },
            "sender": {"name": "Ana"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _context(text: str = "Vi o plano de 497 e tenho 120 alunos") -> TurnContext:
    return build_turn_context(
        turn_id="turn_evidence_1",
        request=_request(text),
        state=RuntimeState(
            conversation_id="conv_evidence_1",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_product_agent",
            summary="Lead comparou preco e tamanho do studio.",
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
        "detected_intents": ["price_question", "student_count_fact"],
        "direct_question_present": True,
        "direct_question_answered_first": True,
        "language_policy": {
            "register": "studio_owner_practical",
            "crm_term_policy": "avoid_by_default",
        },
        "facts": [
            {
                "key": "active_students_or_size",
                "value": 120,
                "source": "user_message",
                "reliability": "customer_provided",
                "confidence": "high",
                "evidence": ["tenho 120 alunos"],
            }
        ],
        "numeric_interpretations": [
            {
                "raw_text": "497",
                "kind": "plan_price",
                "value": 497,
                "currency": "BRL",
                "evidence": ["plano de 497"],
                "confidence": "high",
            },
            {
                "raw_text": "120",
                "kind": "student_count",
                "value": 120,
                "evidence": ["tenho 120 alunos"],
                "confidence": "high",
            },
        ],
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
        "input_tokens": 121,
        "output_tokens": 34,
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
async def test_conductor_accepts_evidenced_facts_and_distinct_numeric_meanings() -> None:
    context = _context()
    provider = FakeConductorProvider(_valid_decision_payload(context))

    result = await conduct_turn(context, provider=provider)

    assert result.decision.facts[0].evidence == ["tenho 120 alunos"]
    assert [item.kind for item in result.decision.numeric_interpretations] == [
        "plan_price",
        "student_count",
    ]
    assert [item.evidence for item in result.decision.numeric_interpretations] == [
        ["plano de 497"],
        ["tenho 120 alunos"],
    ]


@pytest.mark.asyncio
async def test_conductor_rejects_extracted_fact_without_evidence() -> None:
    context = _context()
    payload = _valid_decision_payload(context)
    payload["facts"][0].pop("evidence")
    provider = FakeConductorProvider(payload)

    with pytest.raises(ConductorDecisionValidationError):
        await conduct_turn(context, provider=provider)


@pytest.mark.asyncio
async def test_conductor_rejects_numeric_interpretation_without_evidence() -> None:
    context = _context()
    payload = _valid_decision_payload(context)
    payload["numeric_interpretations"][0].pop("evidence")
    provider = FakeConductorProvider(payload)

    with pytest.raises(ConductorDecisionValidationError):
        await conduct_turn(context, provider=provider)


@pytest.mark.asyncio
async def test_conductor_request_tells_llm_to_return_evidence_without_number_parsing() -> None:
    provider = FakeConductorProvider()

    await conduct_turn(_context(), provider=provider)

    instructions = " ".join(provider.calls[0].instructions).lower()
    assert "evidence" in instructions
    assert "numeric" in instructions
