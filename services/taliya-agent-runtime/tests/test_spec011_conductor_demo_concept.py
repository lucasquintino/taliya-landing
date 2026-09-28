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

DEMO_EQUIVALENT_TERMS = (
    "commercial demo",
    "product demo",
    "demo",
    "demonstration",
    "ver funcionando",
)

DEMO_OUT_OF_SCOPE_TERMS = (
    "openai technical reference demo",
    "technical demo",
    "video production",
    "visual demo assets",
)


def _request(text: str = "Quero ver uma demo da Taliya.") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_demo_concept_1",
                "lead_id": "lead_demo_concept_1",
                "channel_conversation_id": "wa_demo_concept_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_demo_concept_1:1",
                "channel_message_id": "wamid_demo_concept_1",
                "type": "text",
                "text": text,
            },
            "sender": {"name": "Ana"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _context(text: str = "Quero ver uma demo da Taliya.") -> TurnContext:
    return build_turn_context(
        turn_id="turn_demo_concept_1",
        request=_request(text),
        state=RuntimeState(
            conversation_id="conv_demo_concept_1",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_product_agent",
            summary="Lead pediu demonstracao do produto.",
            diagnostic={"status": "not_started", "ledger": []},
            waitlist={"status": "none"},
            demo={"status": "not_offered"},
        ),
        recent_events=[],
        product_knowledge_keys=["links"],
        spec006_contract_keys=["product_positioning"],
    )


def _language_policy() -> dict[str, Any]:
    return {
        "register": "studio_owner_practical",
        "crm_term_policy": "avoid_by_default",
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
        "current_state": "demo_question",
        "next_state": "demo_offered",
        "detected_intents": ["demo_request"],
        "direct_question_present": True,
        "direct_question_answered_first": True,
        "demo": {
            "customer_facing_concept": "commercial_product_demo",
            "status": "offered",
            "next_step": "offer_demo",
        },
        "language_policy": _language_policy(),
        "template_plan": {
            "items": [
                {
                    "template_id": "product.demo_direct",
                    "variables": {
                        "official_demo_link": {
                            "kind": "url",
                            "value": "https://www.taliya.com.br/pilates/planos/demonstracao",
                            "source": "official_product_knowledge",
                            "evidence": ["product_knowledge.links.demonstration"],
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
        "input_tokens": 148,
        "output_tokens": 39,
        "cost_usd": 0.0013,
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
async def test_conductor_accepts_single_customer_facing_demo_concept() -> None:
    context = _context("Tem demo ou demonstração do produto?")
    provider = FakeConductorProvider(_provider_result(_valid_decision_payload(context)))

    result = await conduct_turn(context, provider=provider)

    assert result.decision.demo.customer_facing_concept == "commercial_product_demo"
    assert result.decision.demo.status == "offered"
    assert result.decision.demo.next_step == "offer_demo"
    assert result.decision.route == "product"


@pytest.mark.asyncio
async def test_conductor_normalizes_common_demo_enum_aliases() -> None:
    context = _context("quero ver uma demonstracao")
    decision = _valid_decision_payload(context)
    decision["demo"]["status"] = "asked"
    decision["demo"]["next_step"] = "send_link"
    provider = FakeConductorProvider(_provider_result(decision))

    result = await conduct_turn(context, provider=provider)

    assert result.decision.demo.status == "viewed_or_asked"
    assert result.decision.demo.next_step == "offer_demo"


@pytest.mark.asyncio
async def test_conductor_rejects_out_of_scope_demo_fields() -> None:
    context = _context()
    decision = _valid_decision_payload(context)
    decision["technical_demo"] = {"status": "requested"}
    decision["demo"]["video_demo"] = "requested"
    provider = FakeConductorProvider(_provider_result(decision))

    with pytest.raises(ConductorDecisionValidationError, match="technical_demo"):
        await conduct_turn(context, provider=provider)


@pytest.mark.asyncio
async def test_provider_request_and_policy_pack_unify_demo_concept() -> None:
    provider = FakeConductorProvider()

    await conduct_turn(_context(), provider=provider)

    request_text = " ".join(provider.calls[0].instructions).lower()
    policy_text = provider.calls[0].specialist_policy.model_dump_json().lower()
    schema_text = str(provider.calls[0].response_schema).lower()
    combined = f"{request_text} {policy_text} {schema_text}"
    for term in DEMO_EQUIVALENT_TERMS:
        assert term in combined
    for term in DEMO_OUT_OF_SCOPE_TERMS:
        assert term in combined
    assert "demo structured fields" in combined
    assert "commercial_product_demo" in combined
    assert "technical_demo" not in schema_text
    assert "video_demo" not in schema_text


@pytest.mark.asyncio
async def test_demo_policy_is_stable_and_not_inbound_routing() -> None:
    provider = FakeConductorProvider()

    await conduct_turn(_context("Me manda a demo do produto"), provider=provider)
    await conduct_turn(
        _context("Quero um video demonstrativo produzido para campanha"),
        provider=provider,
    )

    assert len(provider.calls) == 2
    assert provider.calls[0].instructions == provider.calls[1].instructions
    assert provider.calls[0].specialist_policy == provider.calls[1].specialist_policy
    assert provider.calls[0].llm_must_decide is True
    assert provider.calls[1].llm_must_decide is True
