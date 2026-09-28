from __future__ import annotations

from typing import Any

import pytest

from app.core.taliya_commercial.conductor import ConductorProviderRequest, conduct_turn
from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.schemas import TurnContext
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState

EXPECTED_ROLES = ["entry", "product", "diagnostic", "waitlist", "handoff", "safety"]


def _request(text: str) -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_policy_1",
                "lead_id": "lead_policy_1",
                "channel_conversation_id": "wa_policy_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": f"wa:conv_policy_1:{abs(hash(text))}",
                "channel_message_id": f"wamid_{abs(hash(text))}",
                "type": "text",
                "text": text,
            },
            "sender": {"name": "Ana"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _context(text: str) -> TurnContext:
    return build_turn_context(
        turn_id="turn_policy_1",
        request=_request(text),
        state=RuntimeState(
            conversation_id="conv_policy_1",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_product_agent",
            summary="Lead tem interesse comercial misto.",
            diagnostic={"status": "not_started", "ledger": []},
            waitlist={"status": "none"},
            demo={"status": "not_offered"},
        ),
        recent_events=[],
        product_knowledge_keys=["prices", "links"],
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
        "detected_intents": ["mixed_commercial_interest"],
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
        "confidence": "medium",
    }


def _model_usage() -> dict[str, Any]:
    return {
        "model": "gpt-5.4-mini",
        "input_tokens": 124,
        "output_tokens": 37,
        "cost_usd": 0.001,
    }


def _provider_result(decision: dict[str, Any]) -> dict[str, Any]:
    return {"decision": decision, "model_usage": _model_usage()}


class ContextAwareProvider:
    def __init__(self) -> None:
        self.calls: list[ConductorProviderRequest] = []

    async def __call__(self, request: ConductorProviderRequest) -> dict[str, Any]:
        self.calls.append(request)
        return _provider_result(_valid_decision_payload(request.context))


@pytest.mark.asyncio
async def test_conductor_request_includes_full_logical_specialist_policy_pack() -> None:
    provider = ContextAwareProvider()
    context = _context("Quero preco, demo e saber se faz sentido para meu studio")

    await conduct_turn(context, provider=provider)

    assert len(provider.calls) == 1
    policy = provider.calls[0].specialist_policy
    assert [role.role for role in policy.roles] == EXPECTED_ROLES
    assert policy.normal_turn_call_strategy == "single_conductor_call"
    assert policy.llm_selects_role_and_route is True
    assert policy.code_must_not_preselect_role is True
    assert all(role.responsibilities for role in policy.roles)
    assert all(role.forbidden_actions for role in policy.roles)
    instructions = " ".join(provider.calls[0].instructions)
    assert "entry_intent=site_cta" in instructions
    assert "opening.site_cta" in instructions
    assert "entry_intent=diagnostic_cta" in instructions


@pytest.mark.asyncio
async def test_specialist_policy_pack_is_stable_and_not_based_on_inbound_text() -> None:
    provider = ContextAwareProvider()

    await conduct_turn(
        _context("Quanto custa e tenho 120 alunos?"),
        provider=provider,
    )
    await conduct_turn(
        _context("Vim pelo Instagram, quero diagnostico e lista de espera"),
        provider=provider,
    )

    assert len(provider.calls) == 2
    first_policy = provider.calls[0].specialist_policy
    second_policy = provider.calls[1].specialist_policy
    assert first_policy == second_policy
    assert provider.calls[0].context.inbound.text != provider.calls[1].context.inbound.text


def test_specialist_policy_pack_has_no_hardcoded_product_facts_or_customer_copy() -> None:
    policy = ContextAwareProvider()
    context = _context("Mensagem qualquer")

    async def _capture_policy() -> None:
        await conduct_turn(context, provider=policy)

    import asyncio

    asyncio.run(_capture_policy())
    text = policy.calls[0].specialist_policy.model_dump_json().lower()

    forbidden_snippets = {
        "497",
        "897",
        "1497",
        "r$",
        "plano base",
        "plano pro",
        "sete agentes",
        "oi,",
        "tudo bem?",
        "se fizer sentido",
    }
    assert not forbidden_snippets.intersection(text)
    assert "if user says" not in text
    assert "when the message" not in text
    assert "keyword" not in text


@pytest.mark.asyncio
async def test_mixed_intent_context_still_uses_one_provider_call_with_all_roles() -> None:
    provider = ContextAwareProvider()

    await conduct_turn(
        _context("Tenho 120 alunos, quero preco, diagnostico, demo e falar com humano"),
        provider=provider,
    )

    assert len(provider.calls) == 1
    assert [role.role for role in provider.calls[0].specialist_policy.roles] == EXPECTED_ROLES
    assert provider.calls[0].llm_must_decide is True
