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

PRACTICAL_LANGUAGE_TERMS = (
    "sistema",
    "rotina",
    "base organizada",
    "atendimento",
    "agenda",
    "vendas",
    "alunos",
    "turmas",
    "proximos passos",
)


def _request(text: str = "O que e a Taliya para meu studio?") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_language_policy_1",
                "lead_id": "lead_language_policy_1",
                "channel_conversation_id": "wa_language_policy_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_language_policy_1:1",
                "channel_message_id": "wamid_language_policy_1",
                "type": "text",
                "text": text,
            },
            "sender": {"name": "Ana"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _context(text: str = "O que e a Taliya para meu studio?") -> TurnContext:
    return build_turn_context(
        turn_id="turn_language_policy_1",
        request=_request(text),
        state=RuntimeState(
            conversation_id="conv_language_policy_1",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_product_agent",
            summary="Lead perguntou o que e a Taliya.",
            diagnostic={"status": "not_started", "ledger": []},
            waitlist={"status": "none"},
            demo={"status": "not_offered"},
        ),
        recent_events=[],
        product_knowledge_keys=["product_overview"],
        spec006_contract_keys=["product_positioning"],
    )


def _language_policy(
    *,
    crm_term_policy: str = "avoid_by_default",
    crm_allowed_reasons: list[str] | None = None,
    crm_evidence: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "register": "studio_owner_practical",
        "crm_term_policy": crm_term_policy,
        "crm_allowed_reasons": crm_allowed_reasons or [],
        "crm_evidence": crm_evidence or [],
    }


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
        "language_policy": _language_policy(),
        "template_plan": {
            "items": [
                {
                    "template_id": "product.overview_short",
                    "variables": {
                        "product_fact_summary": {
                            "kind": "long_text",
                            "value": "Resumo de produto vindo de conhecimento oficial.",
                            "source": "official_product_knowledge",
                            "evidence": ["product_knowledge.product_overview"],
                            "max_length": 320,
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
        "input_tokens": 152,
        "output_tokens": 42,
        "cost_usd": 0.0014,
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
async def test_conductor_accepts_default_studio_owner_language_policy_without_crm() -> None:
    context = _context()
    provider = FakeConductorProvider(_provider_result(_valid_decision_payload(context)))

    result = await conduct_turn(context, provider=provider)

    assert result.decision.language_policy.language_register == "studio_owner_practical"
    assert result.decision.language_policy.crm_term_policy == "avoid_by_default"
    assert result.decision.language_policy.crm_allowed_reasons == []
    assert result.decision.language_policy.crm_evidence == []


@pytest.mark.asyncio
async def test_conductor_rejects_decision_without_language_policy() -> None:
    context = _context()
    decision = _valid_decision_payload(context)
    decision.pop("language_policy")
    provider = FakeConductorProvider(_provider_result(decision))

    with pytest.raises(ConductorDecisionValidationError):
        await conduct_turn(context, provider=provider)


@pytest.mark.asyncio
async def test_conductor_rejects_crm_allowed_without_evidence() -> None:
    context = _context("O que e um CRM para meu studio?")
    decision = _valid_decision_payload(context)
    decision["language_policy"] = _language_policy(
        crm_term_policy="allowed_with_evidence",
        crm_allowed_reasons=["lead_used_or_asked_crm"],
        crm_evidence=[],
    )
    provider = FakeConductorProvider(_provider_result(decision))

    with pytest.raises(ConductorDecisionValidationError):
        await conduct_turn(context, provider=provider)


@pytest.mark.asyncio
async def test_conductor_accepts_crm_allowed_only_with_reason_and_evidence() -> None:
    context = _context("O que e um CRM para meu studio?")
    decision = _valid_decision_payload(context)
    decision["language_policy"] = _language_policy(
        crm_term_policy="allowed_with_evidence",
        crm_allowed_reasons=["lead_used_or_asked_crm"],
        crm_evidence=["inbound_text:O que e um CRM para meu studio?"],
    )
    provider = FakeConductorProvider(_provider_result(decision))

    result = await conduct_turn(context, provider=provider)

    assert result.decision.language_policy.crm_term_policy == "allowed_with_evidence"
    assert result.decision.language_policy.crm_allowed_reasons == [
        "lead_used_or_asked_crm"
    ]


@pytest.mark.asyncio
async def test_provider_request_and_policy_pack_include_studio_language_rule() -> None:
    provider = FakeConductorProvider()

    await conduct_turn(_context(), provider=provider)

    request_text = " ".join(provider.calls[0].instructions).lower()
    policy_text = provider.calls[0].specialist_policy.model_dump_json().lower()
    combined = f"{request_text} {policy_text}"
    for term in PRACTICAL_LANGUAGE_TERMS:
        assert term in combined
    assert "crm is not the default" in combined
    assert "lead_used_or_asked_crm" in combined
    assert "approved_template_requires_crm" in combined
    assert "category_name_needed" in combined


@pytest.mark.asyncio
async def test_language_policy_is_stable_and_not_inbound_routing() -> None:
    provider = FakeConductorProvider()

    await conduct_turn(_context("O que e a Taliya?"), provider=provider)
    await conduct_turn(_context("Isso e CRM?"), provider=provider)

    assert len(provider.calls) == 2
    assert provider.calls[0].instructions == provider.calls[1].instructions
    assert provider.calls[0].specialist_policy == provider.calls[1].specialist_policy
    assert provider.calls[0].llm_must_decide is True
    assert provider.calls[1].llm_must_decide is True
