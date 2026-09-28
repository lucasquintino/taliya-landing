from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.auth.hmac import (
    HMAC_HEADER_REQUEST_ID,
    HMAC_HEADER_SIGNATURE,
    HMAC_HEADER_TIMESTAMP,
    compute_signature,
)
from app.core.taliya_commercial.conductor import (
    ActionConductorProviderRequest,
    ConductorProviderRequest,
)
from app.core.taliya_commercial.context_profile import (
    RUNTIME_CORE_PRODUCT_KNOWLEDGE_KEYS,
    RUNTIME_CORE_SPEC006_CONTRACT_KEYS,
)
from app.core.taliya_commercial.schemas import (
    ConductorDecision,
    LanguagePolicyDecision,
    ModelUsage,
    PolicyChecks,
    RenderPlan,
    RenderPlanItem,
    TemplateVariableValue,
    TurnFact,
)
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import InMemoryMemoryStore, RuntimeState


def _signed_headers(body: bytes, request_id: str) -> dict[str, str]:
    timestamp = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return {
        HMAC_HEADER_TIMESTAMP: timestamp,
        HMAC_HEADER_REQUEST_ID: request_id,
        HMAC_HEADER_SIGNATURE: compute_signature("dev-secret", timestamp, body),
        "content-type": "application/json",
    }


def _widget_request() -> AgentRunRequest:
    return AgentRunRequest(
        agent_key="taliya_commercial",
        channel="widget",
        conversation={
            "conversation_id": "widget_session_123",
            "lead_id": "lead_widget_123",
            "channel_conversation_id": "browser_session_123",
            "source": "pilates_landing",
            "entry_intent": "widget",
        },
        message={
            "idempotency_key": "widget:widget_session_123:1:abc",
            "channel_message_id": "web_msg_123",
            "type": "text",
            "text": "quanto custa?",
            "timestamp": "2026-05-30T12:00:00Z",
        },
        sender={"name": "Ana"},
        metadata={
            "page_path": "/pilates",
            "source_section": "floating_agent",
            "provider": "widget",
        },
    )


def _whatsapp_request() -> AgentRunRequest:
    return AgentRunRequest(
        agent_key="taliya_commercial",
        channel="whatsapp",
        conversation={
            "conversation_id": "wa_conv_5511999990000",
            "lead_id": "lead_whatsapp_123",
            "channel_conversation_id": "wa_conv_5511999990000",
            "source": "taliya_whatsapp",
            "entry_intent": "whatsapp",
        },
        message={
            "idempotency_key": "whatsapp:wamid.HBgMNTUxMTk5OTk5MDAwMA",
            "channel_message_id": "wamid.HBgMNTUxMTk5OTk5MDAwMA",
            "type": "text",
            "text": "vi no whatsapp, serve pro meu studio?",
            "timestamp": "2026-05-30T12:00:00Z",
        },
        sender={"name": "Ana WhatsApp", "whatsapp_phone": "+5511999990000"},
        metadata={
            "spec011_core_contract": "taliya_commercial_core_reset_v1",
            "page_path": "whatsapp:taliya",
            "source_section": "taliya_owned_whatsapp",
            "provider": "whatsapp",
        },
    )


class FakeConductorProvider:
    def __init__(self, *, next_question_key: str | None = None) -> None:
        self.calls: list[ConductorProviderRequest] = []
        self.next_question_key = next_question_key

    def __call__(self, request: ConductorProviderRequest) -> dict[str, Any]:
        self.calls.append(request)
        context = request.context
        plan_price = TemplateVariableValue(
            kind="long_text",
            value="Resumo oficial dos planos disponiveis.",
            source="official_product_knowledge",
            evidence=["product_knowledge.prices"],
            max_length=360,
        )
        decision = ConductorDecision(
            schema_version="011.0",
            turn_id=context.turn_id,
            conversation_id=context.conversation_id,
            channel=context.channel,
            agent_key=context.agent_key,
            role="product",
            route="product",
            previous_state="new_lead",
            current_state="product_question",
            next_state="product_question",
            detected_intents=["price_question"],
            direct_question_present=True,
            direct_question_answered_first=True,
            diagnostic={
                "action": "offer",
                "next_question_key": self.next_question_key,
            },
            facts=[
                TurnFact(
                    key="asked_price",
                    value="quanto custa?",
                    source="user_message",
                    reliability="customer_provided",
                    evidence=["inbound.text"],
                )
            ],
            language_policy=LanguagePolicyDecision(
                register="studio_owner_practical",
                crm_term_policy="avoid_by_default",
            ),
            template_plan=RenderPlan(
                items=[
                    RenderPlanItem(
                        template_id="product.price_direct",
                        channel=context.channel,
                        variables={"plan_price_summary": plan_price},
                    ),
                    RenderPlanItem(
                        template_id="diagnostic.price_hook",
                        channel=context.channel,
                        variables={},
                    ),
                ]
            ),
            policy_checks=PolicyChecks(
                direct_question_answered_first=True,
                diagnostic_timing_ok=True,
                waitlist_timing_ok=True,
                official_facts_only=True,
                no_internal_text_leak=True,
                no_early_contact_capture=True,
                no_human_overlap=True,
            ),
        )
        return {
            "decision": decision.model_dump(mode="json"),
            "model_usage": ModelUsage(
                model="gpt-5.4-mini",
                input_tokens=321,
                output_tokens=123,
                cost_usd=0.001,
            ).model_dump(mode="json"),
        }


class FakeActionConductorProvider:
    def __init__(self) -> None:
        self.calls: list[ActionConductorProviderRequest] = []

    def __call__(self, request: ActionConductorProviderRequest) -> dict[str, Any]:
        self.calls.append(request)
        context = request.context
        return {
            "decision": {
                "schema_version": "011.action_decision.v1",
                "turn_id": context.turn_id,
                "conversation_id": context.conversation_id,
                "channel": context.channel,
                "agent_key": context.agent_key,
                "selected_action": "answer_direct_product_question",
                "interpreted_intents": ["price_question"],
                "direct_question": {
                    "present": True,
                    "answered_first": True,
                    "answer_obligations": ["answer_price_from_official_facts"],
                },
                "captured_slots": [],
                "product_fact_keys_used": ["prices"],
                "numeric_interpretations": [],
                "diagnostic_intent": {"status": "offer_after_answer", "details": {}},
                "demo_intent": {"status": "none", "details": {}},
                "waitlist_intent": {"status": "none", "details": {}},
                "handoff_intent": {"status": "none", "details": {}},
                "reply_goal": "answer price and offer diagnostic",
                "confidence": "high",
                "evidence": ["latest_inbound_interpreted_by_llm"],
                "needs_clarification": False,
                "repair_hints": [],
            },
            "model_usage": {
                "model": "gpt-5.4-mini",
                "input_tokens": 210,
                "output_tokens": 45,
                "cost_usd": 0.001,
            },
        }


class RepairingActionConductorProvider(FakeActionConductorProvider):
    def __call__(self, request: ActionConductorProviderRequest) -> dict[str, Any]:
        if not self.calls:
            self.calls.append(request)
            context = request.context
            return {
                "decision": {
                    "schema_version": "011.action_decision.v1",
                    "turn_id": context.turn_id,
                    "conversation_id": context.conversation_id,
                    "channel": context.channel,
                    "agent_key": context.agent_key,
                    "selected_action": "unsupported_action",
                    "interpreted_intents": ["price_question"],
                    "direct_question": {
                        "present": True,
                        "answered_first": True,
                        "answer_obligations": ["answer_price_from_official_facts"],
                    },
                    "captured_slots": [],
                    "product_fact_keys_used": ["prices"],
                    "numeric_interpretations": [],
                    "diagnostic_intent": {"status": "offer_after_answer", "details": {}},
                    "demo_intent": {"status": "none", "details": {}},
                    "waitlist_intent": {"status": "none", "details": {}},
                    "handoff_intent": {"status": "none", "details": {}},
                    "reply_goal": "invalid first attempt",
                    "confidence": "high",
                    "evidence": ["latest_inbound_interpreted_by_llm"],
                    "needs_clarification": False,
                    "repair_hints": [],
                },
                "model_usage": {
                    "model": "gpt-5.4-mini",
                    "input_tokens": 200,
                    "output_tokens": 40,
                    "cost_usd": 0.001,
                },
            }
        return super().__call__(request)


class PainFirstRepairingActionConductorProvider:
    def __init__(self) -> None:
        self.calls: list[ActionConductorProviderRequest] = []

    def __call__(self, request: ActionConductorProviderRequest) -> dict[str, Any]:
        self.calls.append(request)
        context = request.context
        details = {}
        reply_goal = "invalid pain-first attempt"
        if len(self.calls) > 1:
            details = {
                "pain_context_human": (
                    "O ponto que voce trouxe esta no WhatsApp: muitos interessados "
                    "ficam esperando quando a equipe demora para responder."
                )
            }
            reply_goal = "offer diagnostic while preserving lead pain context"
        return {
            "decision": {
                "schema_version": "011.action_decision.v1",
                "turn_id": context.turn_id,
                "conversation_id": context.conversation_id,
                "channel": context.channel,
                "agent_key": context.agent_key,
                "selected_action": "offer_diagnostic_from_pain",
                "interpreted_intents": ["pain_statement", "interest_in_solutions"],
                "direct_question": {
                    "present": False,
                    "answered_first": False,
                    "answer_obligations": [],
                },
                "captured_slots": [],
                "product_fact_keys_used": [],
                "numeric_interpretations": [],
                "diagnostic_intent": {"status": "offer", "details": details},
                "demo_intent": {"status": "none", "details": {}},
                "waitlist_intent": {"status": "none", "details": {}},
                "handoff_intent": {"status": "none", "details": {}},
                "reply_goal": reply_goal,
                "confidence": "high",
                "evidence": [context.inbound.text or "latest_inbound"],
                "needs_clarification": False,
                "repair_hints": [],
            },
            "model_usage": {
                "model": "gpt-5.4-mini",
                "input_tokens": 220,
                "output_tokens": 50,
                "cost_usd": 0.001,
            },
        }


class FakeColdGreetingProvider:
    def __init__(self) -> None:
        self.calls: list[ConductorProviderRequest] = []

    def __call__(self, request: ConductorProviderRequest) -> dict[str, Any]:
        self.calls.append(request)
        context = request.context
        decision = ConductorDecision(
            schema_version="011.0",
            turn_id=context.turn_id,
            conversation_id=context.conversation_id,
            channel=context.channel,
            agent_key=context.agent_key,
            role="entry",
            route="entry",
            previous_state="new_lead",
            current_state="greeting_only",
            next_state="greeting_only",
            detected_intents=["greeting"],
            direct_question_present=False,
            direct_question_answered_first=True,
            language_policy=LanguagePolicyDecision(
                register="studio_owner_practical",
                crm_term_policy="avoid_by_default",
            ),
            template_plan=RenderPlan(
                items=[
                    RenderPlanItem(
                        template_id="opening.cold_greeting_named",
                        channel=context.channel,
                        variables={
                            "first_name": TemplateVariableValue(
                                kind="short_text",
                                value="Ana",
                                source="channel_metadata",
                                evidence=["sender.name"],
                                max_length=40,
                            )
                        },
                    )
                ],
                chunk_policy="none",
            ),
            policy_checks=PolicyChecks(
                direct_question_answered_first=True,
                diagnostic_timing_ok=True,
                waitlist_timing_ok=True,
                official_facts_only=True,
                no_internal_text_leak=True,
                no_early_contact_capture=True,
                no_human_overlap=True,
            ),
        )
        return {
            "decision": decision.model_dump(mode="json"),
            "model_usage": ModelUsage(
                model="gpt-5.4-mini",
                input_tokens=100,
                output_tokens=40,
                cost_usd=0.0005,
            ).model_dump(mode="json"),
        }


class FakeWaitlistJoinedProvider:
    def __init__(self) -> None:
        self.calls: list[ConductorProviderRequest] = []

    def __call__(self, request: ConductorProviderRequest) -> dict[str, Any]:
        self.calls.append(request)
        context = request.context
        decision = ConductorDecision(
            schema_version="011.0",
            turn_id=context.turn_id,
            conversation_id=context.conversation_id,
            channel=context.channel,
            agent_key=context.agent_key,
            role="waitlist",
            route="waitlist",
            previous_state="waitlist_pending_details",
            current_state="waitlist_pending_details",
            next_state="waitlist_joined",
            detected_intents=["waitlist_acceptance"],
            direct_question_present=False,
            direct_question_answered_first=True,
            waitlist={
                "eligibility": "eligible",
                "status": "joined",
                "missing_details": [],
            },
            language_policy=LanguagePolicyDecision(
                register="studio_owner_practical",
                crm_term_policy="avoid_by_default",
            ),
            template_plan=RenderPlan(
                items=[
                    RenderPlanItem(
                        template_id="waitlist.joined",
                        channel=context.channel,
                        variables={
                            "studio_name": TemplateVariableValue(
                                kind="short_text",
                                value="Studio Ana Pilates",
                                source="user_message",
                                evidence=["inbound.text"],
                                max_length=80,
                            ),
                            "city_state": TemplateVariableValue(
                                kind="short_text",
                                value="Sao Paulo, SP",
                                source="user_message",
                                evidence=["inbound.text"],
                                max_length=80,
                            ),
                        },
                    )
                ],
                chunk_policy="none",
            ),
            policy_checks=PolicyChecks(
                direct_question_answered_first=True,
                diagnostic_timing_ok=True,
                waitlist_timing_ok=True,
                official_facts_only=True,
                no_internal_text_leak=True,
                no_early_contact_capture=True,
                no_human_overlap=True,
            ),
        )
        return {
            "decision": decision.model_dump(mode="json"),
            "model_usage": ModelUsage(
                model="gpt-5.4-mini",
                input_tokens=100,
                output_tokens=40,
                cost_usd=0.0005,
            ).model_dump(mode="json"),
        }


class FakeHandoffProvider:
    def __init__(self) -> None:
        self.calls: list[ConductorProviderRequest] = []

    def __call__(self, request: ConductorProviderRequest) -> dict[str, Any]:
        self.calls.append(request)
        context = request.context
        decision = ConductorDecision(
            schema_version="011.0",
            turn_id=context.turn_id,
            conversation_id=context.conversation_id,
            channel=context.channel,
            agent_key=context.agent_key,
            role="handoff",
            route="handoff",
            previous_state="diagnostic_completed",
            current_state="handoff_requested",
            next_state="handoff_requested",
            detected_intents=["human_handoff_request"],
            direct_question_present=False,
            direct_question_answered_first=True,
            handoff={"status": "requested", "reason": "lead_requested_human"},
            language_policy=LanguagePolicyDecision(
                register="studio_owner_practical",
                crm_term_policy="avoid_by_default",
            ),
            template_plan=RenderPlan(
                items=[
                    RenderPlanItem(
                        template_id="handoff.acknowledge",
                        channel=context.channel,
                        variables={},
                    )
                ],
                chunk_policy="none",
            ),
            policy_checks=PolicyChecks(
                direct_question_answered_first=True,
                diagnostic_timing_ok=True,
                waitlist_timing_ok=True,
                official_facts_only=True,
                no_internal_text_leak=True,
                no_early_contact_capture=True,
                no_human_overlap=True,
            ),
        )
        return {
            "decision": decision.model_dump(mode="json"),
            "model_usage": ModelUsage(
                model="gpt-5.4-mini",
                input_tokens=100,
                output_tokens=40,
                cost_usd=0.0005,
            ).model_dump(mode="json"),
        }


class FakePriceObjectionProvider:
    def __init__(self) -> None:
        self.calls: list[ConductorProviderRequest] = []

    def __call__(self, request: ConductorProviderRequest) -> dict[str, Any]:
        self.calls.append(request)
        context = request.context
        plan_price = TemplateVariableValue(
            kind="long_text",
            value=(
                "Base R$ 197/mes; Essencial R$ 497/mes; Avance R$ 897/mes; "
                "Completo R$ 1.497/mes."
            ),
            source="official_product_knowledge",
            evidence=["product_knowledge.prices"],
            max_length=360,
        )
        decision = ConductorDecision(
            schema_version="011.0",
            turn_id=context.turn_id,
            conversation_id=context.conversation_id,
            channel=context.channel,
            agent_key=context.agent_key,
            role="product",
            route="product",
            previous_state="diagnostic_completed_demo_viewed_or_asked",
            current_state="product_price_objection",
            next_state="product_followup",
            detected_intents=["price_objection"],
            direct_question_present=True,
            direct_question_answered_first=True,
            diagnostic={"action": "none"},
            language_policy=LanguagePolicyDecision(
                register="studio_owner_practical",
                crm_term_policy="avoid_by_default",
            ),
            template_plan=RenderPlan(
                items=[
                    RenderPlanItem(
                        template_id="product.price_direct",
                        channel=context.channel,
                        variables={"plan_price_summary": plan_price},
                    )
                ],
                chunk_policy="none",
            ),
            policy_checks=PolicyChecks(
                direct_question_answered_first=True,
                diagnostic_timing_ok=True,
                waitlist_timing_ok=True,
                official_facts_only=True,
                no_internal_text_leak=True,
                no_early_contact_capture=True,
                no_human_overlap=True,
            ),
        )
        return {
            "decision": decision.model_dump(mode="json"),
            "model_usage": ModelUsage(
                model="gpt-5.4-mini",
                input_tokens=100,
                output_tokens=40,
                cost_usd=0.0005,
            ).model_dump(mode="json"),
        }


class FakeFinalDiagnosticStaleNextProvider:
    def __init__(self) -> None:
        self.calls: list[ConductorProviderRequest] = []

    def __call__(self, request: ConductorProviderRequest) -> dict[str, Any]:
        self.calls.append(request)
        context = request.context
        ledger_updates = [
            {
                "question_key": "active_students_or_size",
                "status": "answered",
                "answer_value": "95 alunos",
                "evidence": ["tenho 95 alunos"],
                "confidence": "high",
                "may_ask_again": False,
            },
            {
                "question_key": "main_pain",
                "status": "answered",
                "answer_value": "perco interessados no whatsapp",
                "evidence": ["perco interessados no whatsapp"],
                "confidence": "high",
                "may_ask_again": False,
            },
            {
                "question_key": "pain_detail",
                "status": "inferred_from_prior_message",
                "answer_value": "interessados ficam sem retorno",
                "evidence": ["perco interessados no whatsapp"],
                "confidence": "high",
                "may_ask_again": False,
            },
            {
                "question_key": "current_process",
                "status": "answered",
                "answer_value": "planilha e whatsapp",
                "evidence": ["planilha e whatsapp"],
                "confidence": "high",
                "may_ask_again": False,
            },
            {
                "question_key": "priority",
                "status": "answered",
                "answer_value": "vendas primeiro",
                "evidence": ["prioridade e vendas primeiro"],
                "confidence": "high",
                "may_ask_again": False,
            },
            {
                "question_key": "urgency",
                "status": "answered",
                "answer_value": "quero resolver agora",
                "evidence": ["quero resolver agora"],
                "confidence": "high",
                "may_ask_again": False,
            },
        ]
        decision = ConductorDecision(
            schema_version="011.0",
            turn_id=context.turn_id,
            conversation_id=context.conversation_id,
            channel=context.channel,
            agent_key=context.agent_key,
            role="diagnostic",
            route="diagnostic",
            previous_state="diagnostic_in_progress",
            current_state="diagnostic_in_progress",
            next_state="diagnostic_in_progress",
            detected_intents=["diagnostic_progress", "urgency_answer"],
            direct_question_present=False,
            direct_question_answered_first=False,
            diagnostic={
                "action": "ask_next",
                "next_question_key": "urgency",
                "ledger_updates": ledger_updates,
                "final_fields": {"recommended_plan_or_range": "Essencial"},
            },
            language_policy=LanguagePolicyDecision(
                register="studio_owner_practical",
                crm_term_policy="avoid_by_default",
            ),
            template_plan=RenderPlan(
                items=[
                    RenderPlanItem(
                        template_id="diagnostic.deliver_hold",
                        channel=context.channel,
                        variables={},
                    ),
                    RenderPlanItem(
                        template_id="diagnostic.deliver_plan_recommendation",
                        channel=context.channel,
                        variables={
                            "recommended_plan_or_range": TemplateVariableValue(
                                kind="short_text",
                                value=(
                                    "Essencial ou Avance para organizar vendas, "
                                    "WhatsApp, follow-up e os retornos que hoje "
                                    "ficam espalhados."
                                ),
                                source="official_product_knowledge",
                                evidence=["product_knowledge.plans"],
                                max_length=90,
                            )
                        },
                    ),
                ]
            ),
            policy_checks=PolicyChecks(
                direct_question_answered_first=True,
                diagnostic_timing_ok=True,
                waitlist_timing_ok=True,
                official_facts_only=True,
                no_internal_text_leak=True,
                no_early_contact_capture=True,
                no_human_overlap=True,
            ),
        )
        return {
            "decision": decision.model_dump(mode="json"),
            "model_usage": ModelUsage(
                model="gpt-5.4-mini",
                input_tokens=1000,
                output_tokens=500,
                cost_usd=0.01,
            ).model_dump(mode="json"),
        }


class FakeDemoDirectStalePriceIntentProvider:
    def __init__(self) -> None:
        self.calls: list[ConductorProviderRequest] = []

    def __call__(self, request: ConductorProviderRequest) -> dict[str, Any]:
        self.calls.append(request)
        context = request.context
        decision = ConductorDecision(
            schema_version="011.0",
            turn_id=context.turn_id,
            conversation_id=context.conversation_id,
            channel=context.channel,
            agent_key=context.agent_key,
            role="product",
            route="product",
            previous_state="diagnostic_completed",
            current_state="product_demo_requested",
            next_state="product_demo_sent",
            detected_intents=["price_question", "demo_request"],
            direct_question_present=False,
            direct_question_answered_first=False,
            diagnostic={"action": "none"},
            demo={
                "customer_facing_concept": "commercial_product_demo",
                "status": "viewed_or_asked",
                "next_step": "offer_demo",
            },
            language_policy=LanguagePolicyDecision(
                register="studio_owner_practical",
                crm_term_policy="avoid_by_default",
            ),
            template_plan=RenderPlan(
                items=[
                    RenderPlanItem(
                        template_id="product.demo_direct",
                        channel=context.channel,
                        variables={
                            "official_demo_link": TemplateVariableValue(
                                kind="url",
                                value="https://www.taliya.com.br/pilates/planos/demonstracao",
                                source="official_product_knowledge",
                                evidence=["product_knowledge.links"],
                            )
                        },
                    )
                ],
                chunk_policy="none",
            ),
            policy_checks=PolicyChecks(
                direct_question_answered_first=False,
                diagnostic_timing_ok=True,
                waitlist_timing_ok=True,
                official_facts_only=True,
                no_internal_text_leak=True,
                no_early_contact_capture=True,
                no_human_overlap=True,
            ),
        )
        return {
            "decision": decision.model_dump(mode="json"),
            "model_usage": ModelUsage(
                model="gpt-5.4-mini",
                input_tokens=1000,
                output_tokens=500,
                cost_usd=0.01,
            ).model_dump(mode="json"),
        }


class FakePainFirstSchemaAliasProvider:
    def __init__(self) -> None:
        self.calls: list[ConductorProviderRequest] = []

    def __call__(self, request: ConductorProviderRequest) -> dict[str, Any]:
        self.calls.append(request)
        context = request.context
        pain_context = TemplateVariableValue(
            kind="long_text",
            value=(
                "Voce esta perdendo interessados porque o atendimento no "
                "WhatsApp demora."
            ),
            source="user_message",
            evidence=[str(context.inbound.text or "")],
            max_length=420,
        )
        decision = ConductorDecision(
            schema_version="011.conductor_decision.v1",
            turn_id=context.turn_id,
            conversation_id=context.conversation_id,
            channel=context.channel,
            agent_key=context.agent_key,
            role="diagnostic",
            route="diagnostic",
            previous_state="new_lead",
            current_state="diagnostic_offered",
            next_state="diagnostic_waiting_acceptance",
            detected_intents=["pain_statement", "diagnostic_relevant"],
            direct_question_present=False,
            direct_question_answered_first=True,
            diagnostic={
                "action": "offer",
                "next_question_key": "urgency",
                "ledger_updates": [
                    {
                        "question_key": "main_pain",
                        "status": "answered",
                        "answer_value": "perco interessados no WhatsApp",
                        "evidence": [str(context.inbound.text or "")],
                        "confidence": "high",
                    }
                ],
            },
            language_policy=LanguagePolicyDecision(
                register="studio_owner_practical",
                crm_term_policy="avoid_by_default",
            ),
            template_plan=RenderPlan(
                items=[
                    RenderPlanItem(
                        template_id="diagnostic.offer_soft",
                        channel=context.channel,
                        variables={"pain_context_human": pain_context},
                    ),
                    RenderPlanItem(
                        template_id="diagnostic.ask_urgency",
                        channel=context.channel,
                        variables={},
                    ),
                ]
            ),
            policy_checks=PolicyChecks(
                direct_question_answered_first=True,
                diagnostic_timing_ok=True,
                waitlist_timing_ok=True,
                official_facts_only=True,
                no_internal_text_leak=True,
                no_early_contact_capture=True,
                no_human_overlap=True,
            ),
        )
        return {
            "decision": decision.model_dump(mode="json"),
            "model_usage": ModelUsage(
                model="gpt-5.4-mini",
                input_tokens=456,
                output_tokens=180,
                cost_usd=0.001,
            ).model_dump(mode="json"),
        }


class FakePainFirstProductRouteProvider:
    def __init__(self) -> None:
        self.calls: list[ConductorProviderRequest] = []

    def __call__(self, request: ConductorProviderRequest) -> dict[str, Any]:
        self.calls.append(request)
        context = request.context
        pain_context = TemplateVariableValue(
            kind="long_text",
            value=(
                "Voces perdem interessados porque a equipe demora para responder "
                "no WhatsApp."
            ),
            source="diagnostic_ledger",
            evidence=["diagnostic_ledger"],
            max_length=420,
        )
        decision = ConductorDecision(
            schema_version="011.0",
            turn_id=context.turn_id,
            conversation_id=context.conversation_id,
            channel=context.channel,
            agent_key=context.agent_key,
            role="product",
            route="product",
            previous_state="entry",
            current_state="product",
            next_state="diagnostic",
            detected_intents=[
                "pain_report",
                "whatsapp_followup_issue",
                "product_interest",
            ],
            direct_question_present=False,
            direct_question_answered_first=False,
            diagnostic={
                "action": "offer",
                "next_question_key": "active_students_or_size",
                "ledger_updates": [
                    {
                        "question_key": "main_pain",
                        "status": "answered",
                        "answer_value": "perco interessados no WhatsApp",
                        "evidence": [str(context.inbound.text or "")],
                        "confidence": "high",
                    }
                ],
            },
            language_policy=LanguagePolicyDecision(
                register="studio_owner_practical",
                crm_term_policy="avoid_by_default",
            ),
            template_plan=RenderPlan(
                items=[
                    RenderPlanItem(
                        template_id="opening.general_interest",
                        channel=context.channel,
                        variables={},
                    ),
                    RenderPlanItem(
                        template_id="diagnostic.offer_soft",
                        channel=context.channel,
                        variables={"pain_context_human": pain_context},
                    ),
                ]
            ),
            policy_checks=PolicyChecks(
                direct_question_answered_first=True,
                diagnostic_timing_ok=True,
                waitlist_timing_ok=True,
                official_facts_only=True,
                no_internal_text_leak=True,
                no_early_contact_capture=True,
                no_human_overlap=True,
            ),
        )
        return {
            "decision": decision.model_dump(mode="json"),
            "model_usage": ModelUsage(
                model="gpt-5.4-mini",
                input_tokens=7886,
                output_tokens=810,
                cost_usd=0.00956,
            ).model_dump(mode="json"),
        }


class FakePainFirstQuestionOnlyProvider:
    def __init__(self) -> None:
        self.calls: list[ConductorProviderRequest] = []

    def __call__(self, request: ConductorProviderRequest) -> dict[str, Any]:
        self.calls.append(request)
        context = request.context
        decision = ConductorDecision(
            schema_version="011.0",
            turn_id=context.turn_id,
            conversation_id=context.conversation_id,
            channel=context.channel,
            agent_key=context.agent_key,
            role="diagnostic",
            route="diagnostic",
            previous_state="entry",
            current_state="diagnostic_asked_active_students",
            next_state="diagnostic_in_progress",
            detected_intents=["pain_statement", "diagnostic_relevant"],
            direct_question_present=False,
            direct_question_answered_first=True,
            diagnostic={
                "action": "ask_next",
                "next_question_key": "active_students_or_size",
                "ledger_updates": [
                    {
                        "question_key": "main_pain",
                        "status": "answered",
                        "answer_value": "perco interessados no WhatsApp",
                        "evidence": [str(context.inbound.text or "")],
                        "confidence": "high",
                    }
                ],
            },
            language_policy=LanguagePolicyDecision(
                register="studio_owner_practical",
                crm_term_policy="avoid_by_default",
            ),
            template_plan=RenderPlan(
                items=[
                    RenderPlanItem(
                        template_id="diagnostic.ask_active_students",
                        channel=context.channel,
                        variables={},
                    )
                ]
            ),
            policy_checks=PolicyChecks(
                direct_question_answered_first=True,
                diagnostic_timing_ok=True,
                waitlist_timing_ok=True,
                official_facts_only=True,
                no_internal_text_leak=True,
                no_early_contact_capture=True,
                no_human_overlap=True,
            ),
        )
        return {
            "decision": decision.model_dump(mode="json"),
            "model_usage": ModelUsage(
                model="gpt-5.4-mini",
                input_tokens=7886,
                output_tokens=810,
                cost_usd=0.00956,
            ).model_dump(mode="json"),
        }


class FakeUnusedRepairProvider:
    def __init__(self) -> None:
        self.calls: list[Any] = []

    def __call__(self, request: Any) -> dict[str, Any]:
        self.calls.append(request)
        return {"should_not": "be called"}


@pytest.mark.asyncio
async def test_widget_runtime_adapter_calls_spec011_core_and_preserves_payload_ids() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    request = _widget_request()
    provider = FakeConductorProvider()

    response = await run_spec011_agent_turn(
        request,
        memory_store=InMemoryMemoryStore(),
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=provider,
    )

    assert len(provider.calls) == 1
    context = provider.calls[0].context
    assert context.conversation_id == "widget_session_123"
    assert context.channel == "widget"
    assert context.inbound.idempotency_key == "widget:widget_session_123:1:abc"
    assert context.inbound.message_id == "web_msg_123"
    assert context.sales_inbox_inputs["source"] == "pilates_landing"
    assert context.sales_inbox_inputs["channel_conversation_id"] == "browser_session_123"
    official_keys = [
        ref.key
        for ref in context.product_knowledge
        if ref.source == "official_product_knowledge"
    ]
    spec006_keys = [
        ref.key.removeprefix("spec006.")
        for ref in context.product_knowledge
        if ref.source == "spec_006_product_contract"
    ]
    assert set(RUNTIME_CORE_PRODUCT_KNOWLEDGE_KEYS).issubset(set(official_keys))
    assert set(spec006_keys) == set(RUNTIME_CORE_SPEC006_CONTRACT_KEYS)
    assert "comparison_spreadsheet" not in official_keys
    assert "security_and_data" not in official_keys

    assert response.conversation_id == "widget_session_123"
    assert response.lead_id == "lead_widget_123"
    assert response.current_agent == "taliya_commercial_spec011_product_agent"
    assert response.output.usage.model == "gpt-5.4-mini"
    assert response.output.usage.input_tokens > 0
    assert response.output.decision.route == "product"
    assert response.output.messages[0].channel_hint == "widget"
    assert response.output.messages[0].template_id == "product.price_direct"
    assert response.trace_id.startswith("trace_")
    assert response.output.context_snapshot == {}
    assert response.output.conductor_json == {}
    assert response.output.validator_results == []
    assert response.output.repair_attempts == []
    assert response.output.runtime_state == {}
    assert response.output.sales_inbox_projection == {}
    assert response.output.delivery_events == []
    assert response.output.trace_complete is False


@pytest.mark.asyncio
async def test_runtime_adapter_uses_action_conductor_when_legacy_provider_is_absent() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    request = _widget_request()
    provider = FakeActionConductorProvider()

    response = await run_spec011_agent_turn(
        request,
        memory_store=InMemoryMemoryStore(),
        provider="mock",
        model="gpt-5.4-mini",
        action_conductor_provider=provider,
    )

    assert len(provider.calls) == 1
    action_request = provider.calls[0]
    assert action_request.request_schema_version == "011.action_conductor_request.v1"
    assert action_request.turn_situation.mode == "entry"
    assert (
        "answer_direct_product_question"
        in action_request.turn_situation.allowed_actions
    )
    assert response.output.decision.route == "product"
    template_ids = [message.template_id for message in response.output.messages]
    assert template_ids[0] == "product.price_direct"
    assert "diagnostic.price_hook" in template_ids
    assert response.output.usage.input_tokens == 210


@pytest.mark.asyncio
async def test_runtime_adapter_eval_trace_includes_action_first_artifacts() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    request = _widget_request()
    request.metadata["spec011_eval_trace"] = True
    provider = FakeActionConductorProvider()

    response = await run_spec011_agent_turn(
        request,
        memory_store=InMemoryMemoryStore(),
        provider="mock",
        model="gpt-5.4-mini",
        action_conductor_provider=provider,
    )

    assert response.output.turn_situation["mode"] == "entry"
    assert (
        "answer_direct_product_question"
        in response.output.turn_situation["allowed_actions"]
    )
    assert response.output.action_decision["schema_version"] == (
        "011.action_decision.v1"
    )
    assert response.output.action_decision["selected_action"] == (
        "answer_direct_product_question"
    )
    assert response.output.action_repair_attempt_count == 0
    assert response.output.conductor_json["route"] == "product"
    assert response.output.sales_inbox_projection["commercial_stage"] == (
        "product_question_answered"
    )
    assert response.output.trace_complete is True


@pytest.mark.asyncio
async def test_runtime_adapter_repairs_invalid_action_decision_once() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    request = _widget_request()
    provider = RepairingActionConductorProvider()

    response = await run_spec011_agent_turn(
        request,
        memory_store=InMemoryMemoryStore(),
        provider="mock",
        model="gpt-5.4-mini",
        action_conductor_provider=provider,
    )

    assert len(provider.calls) == 2
    assert "Previous ConductorActionDecision was rejected" in " ".join(
        provider.calls[1].instructions
    )
    assert response.output.decision.route == "product"
    assert response.output.messages[0].template_id == "product.price_direct"


@pytest.mark.asyncio
async def test_runtime_adapter_repairs_pain_first_missing_context_before_rendering() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    request = _widget_request()
    request.message.text = (
        "perco muitos interessados no WhatsApp porque a equipe demora para responder"
    )
    provider = PainFirstRepairingActionConductorProvider()

    response = await run_spec011_agent_turn(
        request,
        memory_store=InMemoryMemoryStore(),
        provider="mock",
        model="gpt-5.4-mini",
        action_conductor_provider=provider,
    )

    rendered_text = "\n".join(message.text.lower() for message in response.output.messages)
    assert len(provider.calls) == 2
    assert "Previous ConductorActionDecision was rejected" in " ".join(
        provider.calls[1].instructions
    )
    assert response.output.decision.route == "diagnostic"
    assert "whatsapp" in rendered_text
    assert "interessad" in rendered_text
    assert "existe um ponto da rotina" not in rendered_text


@pytest.mark.asyncio
async def test_runtime_adapter_projects_opening_and_profile_name_usage() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    request = _whatsapp_request()
    request.message.text = "oi"
    provider = FakeColdGreetingProvider()
    store = InMemoryMemoryStore()

    response = await run_spec011_agent_turn(
        request,
        memory_store=store,
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=provider,
    )
    state = await store.load_state(request.conversation.conversation_id, request.agent_key)

    assert len(provider.calls) == 1
    assert response.output.decision.opening_type == "cold_greeting_only"
    assert response.output.decision.profile_name_usage == "used_reliable_name"
    assert state is not None
    assert state.last_opening_type == "cold_greeting_only"
    assert state.profile_name_status == "used_reliable_name"


@pytest.mark.asyncio
async def test_runtime_adapter_suppresses_ai_when_human_handoff_is_active() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    request = _whatsapp_request()
    request.message.text = "ainda estou aqui"
    store = InMemoryMemoryStore()
    await store.save_state(
        RuntimeState(
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            current_agent_name="taliya_commercial_spec011_handoff_agent",
            human_status="active",
            human_reason="lead_requested_human",
        )
    )
    provider = FakeConductorProvider()

    response = await run_spec011_agent_turn(
        request,
        memory_store=store,
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=provider,
    )
    state = await store.load_state(request.conversation.conversation_id, request.agent_key)

    assert provider.calls == []
    assert response.status == "human_paused"
    assert response.output.decision.route == "handoff"
    assert response.output.messages == []
    assert response.output.handoff is not None
    assert response.output.handoff.status == "active"
    assert response.output.usage.model is None
    assert response.delivery_control.delivery_suppressed is True
    assert state is not None
    assert state.human_status == "active"
    assert state.input_items[-1]["delivery"] == "suppressed_by_human_handoff"


@pytest.mark.asyncio
async def test_runtime_adapter_maps_spec011_diagnostic_question_to_legacy_kind() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    response = await run_spec011_agent_turn(
        _widget_request(),
        memory_store=InMemoryMemoryStore(),
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=FakeConductorProvider(next_question_key="main_pain"),
    )

    assert response.output.diagnostic is not None
    assert response.output.diagnostic.next_question == "main_pain"
    assert response.output.decision.next_question_kind == "pain"


@pytest.mark.asyncio
async def test_runtime_adapter_repairs_known_schema_alias_on_pain_first_without_500() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    request = _widget_request()
    request.message.text = "perco interessados porque demoro no WhatsApp"
    request.metadata["spec011_eval_trace"] = True
    provider = FakePainFirstSchemaAliasProvider()
    repair_provider = FakeUnusedRepairProvider()

    response = await run_spec011_agent_turn(
        request,
        memory_store=InMemoryMemoryStore(),
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=provider,
        repair_provider=repair_provider,
    )

    repair_attempt = response.output.repair_attempts[0]
    error_codes = set(repair_attempt["errors_sent"])

    assert response.status == "succeeded"
    assert len(provider.calls) == 1
    assert repair_provider.calls == []
    assert response.output.decision.route == "diagnostic"
    assert response.output.decision.diagnostic_action == "ask_next"
    assert response.output.decision.next_question_kind == "plan_fit"
    assert response.output.decision.template_ids == [
        "opening.cold_greeting",
        "diagnostic.offer_soft",
        "diagnostic.ask_active_students",
    ]
    assert response.output.conductor_json["schema_version"] == "011.0"
    assert response.output.conductor_json["diagnostic"]["next_question_key"] == (
        "active_students_or_size"
    )
    assert repair_attempt["status"] == "repaired"
    assert repair_attempt["repaired_decision"]["schema_version"] == "011.0"
    assert "diagnostic_start_must_ask_active_students" in error_codes
    assert response.output.messages


@pytest.mark.asyncio
async def test_runtime_adapter_repairs_pain_first_product_route_without_paid_repair() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    request = _widget_request()
    request.message.text = (
        "perco muitos interessados no WhatsApp porque a equipe demora para responder"
    )
    request.metadata["spec011_eval_trace"] = True
    provider = FakePainFirstProductRouteProvider()
    repair_provider = FakeUnusedRepairProvider()

    response = await run_spec011_agent_turn(
        request,
        memory_store=InMemoryMemoryStore(),
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=provider,
        repair_provider=repair_provider,
    )

    repair_attempt = response.output.repair_attempts[0]
    error_codes = set(repair_attempt["errors_sent"])

    assert response.status == "succeeded"
    assert len(provider.calls) == 1
    assert repair_provider.calls == []
    assert response.current_agent == "taliya_commercial_spec011_diagnostic_agent"
    assert response.output.decision.route == "diagnostic"
    assert response.output.decision.diagnostic_action == "ask_next"
    assert response.output.decision.template_ids == [
        "opening.cold_greeting",
        "diagnostic.offer_soft",
        "diagnostic.ask_active_students",
    ]
    assert response.output.conductor_json["route"] == "diagnostic"
    assert response.output.conductor_json["diagnostic"]["next_question_key"] == (
        "active_students_or_size"
    )
    assert repair_attempt["status"] == "repaired"
    assert "pain_first_diagnostic_offer_must_use_diagnostic_route" in error_codes
    assert "diagnostic_start_must_ask_active_students" in error_codes
    assert "alunos ativos" in "\n".join(
        message.text.lower() for message in response.output.messages
    )


@pytest.mark.asyncio
async def test_runtime_adapter_repairs_pain_first_question_only_without_500() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    request = _widget_request()
    request.message.text = (
        "perco muitos interessados no WhatsApp porque a equipe demora para responder"
    )
    request.metadata["spec011_eval_trace"] = True
    provider = FakePainFirstQuestionOnlyProvider()
    repair_provider = FakeUnusedRepairProvider()

    response = await run_spec011_agent_turn(
        request,
        memory_store=InMemoryMemoryStore(),
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=provider,
        repair_provider=repair_provider,
    )

    repair_attempt = response.output.repair_attempts[0]
    error_codes = set(repair_attempt["errors_sent"])

    assert response.status == "succeeded"
    assert len(provider.calls) == 1
    assert repair_provider.calls == []
    assert response.current_agent == "taliya_commercial_spec011_diagnostic_agent"
    assert response.output.decision.route == "diagnostic"
    assert response.output.decision.diagnostic_action == "offer"
    assert response.output.decision.template_ids == [
        "opening.cold_greeting",
        "diagnostic.offer_soft",
        "diagnostic.ask_active_students",
    ]
    assert response.output.conductor_json["diagnostic"]["next_question_key"] == (
        "active_students_or_size"
    )
    assert repair_attempt["status"] == "repaired"
    assert "pain_first_must_offer_diagnostic" in error_codes
    rendered_text = "\n".join(message.text.lower() for message in response.output.messages)
    assert "alunos ativos" in rendered_text


@pytest.mark.asyncio
async def test_widget_runtime_adapter_exports_eval_trace_artifacts_only_when_requested() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    request = _widget_request()
    request.metadata["spec011_eval_trace"] = True
    provider = FakeConductorProvider()

    response = await run_spec011_agent_turn(
        request,
        memory_store=InMemoryMemoryStore(),
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=provider,
    )

    assert response.output.context_snapshot["inbound"]["text"] == "quanto custa?"
    assert response.output.context_snapshot["sales_inbox_inputs"]["lead_id"] == "lead_widget_123"
    assert response.output.conductor_json["route"] == "product"
    assert response.output.conductor_json["template_plan"]["items"][0]["template_id"] == (
        "product.price_direct"
    )
    assert response.output.validator_results[0]["status"] == "passed"
    assert response.output.repair_attempts[0]["status"] == "not_needed"
    assert response.output.runtime_state
    assert response.output.sales_inbox_projection["conversation_id"] == "widget_session_123"
    assert response.output.sales_inbox_projection["commercial_stage"] == "product_question"
    assert response.output.delivery_events[0]["event"] == "rendered"
    assert response.output.delivery_events[0]["status"] == "planned"
    assert response.output.trace_complete is True


@pytest.mark.asyncio
async def test_runtime_adapter_emits_waitlist_joined_event_for_projection() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    request = _whatsapp_request()
    request.message.text = "sim, Studio Ana Pilates em Sao Paulo SP"
    request.metadata["spec011_eval_trace"] = True
    provider = FakeWaitlistJoinedProvider()

    response = await run_spec011_agent_turn(
        request,
        memory_store=InMemoryMemoryStore(),
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=provider,
    )

    assert response.output.waitlist_action is not None
    assert response.output.waitlist_action.status == "joined"
    assert [event["event"] for event in response.output.delivery_events] == [
        "rendered",
        "waitlist_joined",
    ]
    fields = response.output.sales_inbox_projection["fields"]
    assert fields["waitlist_idempotency_key"].startswith(
        "waitlist:wa_conv_5511999990000:"
    )
    assert fields["waitlist_joined_at"] == "2026-05-30T12:00:00Z"
    assert fields["missing_waitlist_fields"] == []


@pytest.mark.asyncio
async def test_runtime_adapter_preserves_completed_diagnostic_output_on_handoff() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    request = _whatsapp_request()
    request.message.text = "quero falar com alguem"
    request.metadata["spec011_eval_trace"] = True
    completed_ledger = [
        {
            "question_key": "active_students_or_size",
            "status": "answered",
            "answer_value": "120 alunos",
            "evidence": ["120 alunos"],
        },
        {
            "question_key": "main_pain",
            "status": "answered",
            "answer_value": "perde interessados no whatsapp",
            "evidence": ["perde interessados no whatsapp"],
        },
        {
            "question_key": "pain_detail",
            "status": "inferred_from_prior_message",
            "answer_value": "follow-up demora",
            "evidence": ["perde interessados no whatsapp"],
        },
        {
            "question_key": "current_process",
            "status": "answered",
            "answer_value": "planilha e whatsapp",
            "evidence": ["planilha e whatsapp"],
        },
        {
            "question_key": "priority",
            "status": "answered",
            "answer_value": "vendas primeiro",
            "evidence": ["vendas primeiro"],
        },
        {
            "question_key": "urgency",
            "status": "answered",
            "answer_value": "agora",
            "evidence": ["agora"],
        },
    ]
    store = InMemoryMemoryStore()
    await store.save_state(
        RuntimeState(
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            current_agent_name="taliya_commercial_spec011_diagnostic_agent",
            diagnostic={
                "status": "completed",
                "ledger": completed_ledger,
                "final_fields": {
                    "main_bottleneck": "perda de interessados no WhatsApp",
                    "crm_base_recommendation": "organizar base e retorno",
                    "first_recommended_step": "mapear retorno de interessados",
                    "final_plan_or_range": "Essencial ou Avance",
                    "final_demo_line": "Ver uma demonstracao pratica pode ajudar.",
                },
            },
            waitlist={"status": "none"},
            demo={"status": "not_offered"},
        )
    )

    response = await run_spec011_agent_turn(
        request,
        memory_store=store,
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=FakeHandoffProvider(),
    )

    assert response.status == "human_paused"
    assert response.output.diagnostic is not None
    assert response.output.diagnostic.status == "completed"
    assert response.output.diagnostic.plan_or_range_to_compare == "Essencial ou Avance"
    assert response.output.diagnostic.final_demo_line == (
        "Ver uma demonstracao pratica pode ajudar."
    )
    assert response.output.diagnostic.ledger == completed_ledger
    assert response.output.sales_inbox_projection["diagnostic_status"] == "completed"


@pytest.mark.asyncio
async def test_runtime_adapter_long_conversation_preflight_covers_last_real_gate_failures() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    store = InMemoryMemoryStore()
    completed_ledger = [
        {
            "question_key": "active_students_or_size",
            "status": "answered",
            "answer_value": "95 alunos",
            "evidence": ["tenho 95 alunos"],
        },
        {
            "question_key": "main_pain",
            "status": "answered",
            "answer_value": "perco interessados no whatsapp",
            "evidence": ["perco interessados no whatsapp"],
        },
        {
            "question_key": "pain_detail",
            "status": "inferred_from_prior_message",
            "answer_value": "interessados ficam sem retorno",
            "evidence": ["perco interessados no whatsapp"],
        },
        {
            "question_key": "current_process",
            "status": "answered",
            "answer_value": "planilha e whatsapp",
            "evidence": ["planilha e whatsapp"],
        },
        {
            "question_key": "priority",
            "status": "answered",
            "answer_value": "vendas primeiro",
            "evidence": ["vendas primeiro"],
        },
        {
            "question_key": "urgency",
            "status": "answered",
            "answer_value": "resolver agora",
            "evidence": ["resolver agora"],
        },
    ]
    dirty_completed_ledger = [
        {
            "question_key": "current_process",
            "status": "missing",
            "evidence": [],
        },
        *completed_ledger,
        {
            "question_key": "urgency",
            "status": "missing",
            "evidence": [],
        },
    ]
    await store.save_state(
        RuntimeState(
            conversation_id="wa_conv_5511999990000",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_spec011_diagnostic_agent",
            diagnostic={
                "status": "completed",
                "ledger": dirty_completed_ledger,
                "final_fields": {
                    "main_bottleneck": "perda de interessados no WhatsApp",
                    "crm_base_recommendation": "organizar base e retorno",
                    "first_recommended_step": "mapear retorno de interessados",
                    "final_plan_or_range": "Essencial",
                    "final_demo_line": "Ver a demonstracao pratica pode ajudar.",
                },
            },
            waitlist={"status": "none"},
            demo={"status": "viewed_or_asked"},
        )
    )

    price_request = _whatsapp_request()
    price_request.message.idempotency_key = "whatsapp:long-preflight:11"
    price_request.message.channel_message_id = "wamid_long_preflight_11"
    price_request.message.text = "achei caro"
    price_request.metadata["spec011_eval_trace"] = True
    repair_provider = FakeUnusedRepairProvider()
    price_response = await run_spec011_agent_turn(
        price_request,
        memory_store=store,
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=FakePriceObjectionProvider(),
        repair_provider=repair_provider,
    )
    price_text = "\n".join(message.text for message in price_response.output.messages).lower()

    assert repair_provider.calls == []
    assert price_response.output.diagnostic is not None
    assert price_response.output.diagnostic.status == "completed"
    assert "product.price_objection_value" in price_response.output.decision.template_ids
    assert "valor para olhar com calma" in price_text
    assert "nao e so" in price_text
    assert any(
        term in price_text
        for term in (
            "rotinas",
            "retorno",
            "agenda",
            "reposi",
            "cobran",
            "acompanhamento",
            "whatsapp",
        )
    )
    assert price_response.output.diagnostic is not None
    assert len(price_response.output.diagnostic.ledger) == 6
    assert all(
        item["status"] != "missing"
        for item in price_response.output.diagnostic.ledger
    )
    state_after_price = await store.load_state(
        "wa_conv_5511999990000",
        "taliya_commercial",
    )
    assert state_after_price is not None
    assert state_after_price.diagnostic is not None
    assert len(state_after_price.diagnostic["ledger"]) == 6
    assert all(
        item["status"] != "missing"
        for item in state_after_price.diagnostic["ledger"]
    )

    handoff_request = _whatsapp_request()
    handoff_request.message.idempotency_key = "whatsapp:long-preflight:14"
    handoff_request.message.channel_message_id = "wamid_long_preflight_14"
    handoff_request.message.text = "quero falar com alguem"
    handoff_request.metadata["spec011_eval_trace"] = True
    handoff_response = await run_spec011_agent_turn(
        handoff_request,
        memory_store=store,
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=FakeHandoffProvider(),
    )

    assert handoff_response.status == "human_paused"
    assert handoff_response.output.handoff is not None
    assert handoff_response.output.handoff.status == "requested"
    assert handoff_response.output.diagnostic is not None
    assert handoff_response.output.diagnostic.status == "completed"
    assert {
        item["question_key"]
        for item in handoff_response.output.diagnostic.ledger
        if item["status"] in {"answered", "inferred_from_prior_message", "not_applicable"}
    } == {
        "active_students_or_size",
        "main_pain",
        "pain_detail",
        "current_process",
        "priority",
        "urgency",
    }


@pytest.mark.asyncio
async def test_runtime_adapter_long_conversation_preflight_covers_latest_paid_500s() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    store = InMemoryMemoryStore()
    pending_urgency_ledger = [
        {
            "question_key": "active_students_or_size",
            "status": "answered",
            "answer_value": "95 alunos",
            "evidence": ["tenho 95 alunos"],
        },
        {
            "question_key": "main_pain",
            "status": "answered",
            "answer_value": "perco interessados no whatsapp",
            "evidence": ["perco interessados no whatsapp"],
        },
        {
            "question_key": "pain_detail",
            "status": "inferred_from_prior_message",
            "answer_value": "interessados ficam sem retorno",
            "evidence": ["perco interessados no whatsapp"],
        },
        {
            "question_key": "current_process",
            "status": "answered",
            "answer_value": "planilha e whatsapp",
            "evidence": ["planilha e whatsapp"],
        },
        {
            "question_key": "priority",
            "status": "answered",
            "answer_value": "vendas primeiro",
            "evidence": ["prioridade e vendas primeiro"],
        },
        {
            "question_key": "urgency",
            "status": "missing",
            "evidence": ["Voces estao buscando resolver isso agora?"],
        },
    ]
    await store.save_state(
        RuntimeState(
            conversation_id="wa_conv_5511999990000",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_spec011_diagnostic_agent",
            diagnostic={"status": "in_progress", "ledger": pending_urgency_ledger},
            waitlist={"status": "none"},
            demo={"status": "not_offered"},
        )
    )

    urgency_request = _whatsapp_request()
    urgency_request.message.idempotency_key = "whatsapp:long-preflight-latest:9"
    urgency_request.message.channel_message_id = "wamid_long_preflight_latest_9"
    urgency_request.message.text = "quero resolver agora"
    urgency_request.metadata["spec011_eval_trace"] = True
    repair_provider = FakeUnusedRepairProvider()
    urgency_response = await run_spec011_agent_turn(
        urgency_request,
        memory_store=store,
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=FakeFinalDiagnosticStaleNextProvider(),
        repair_provider=repair_provider,
    )
    urgency_error_codes = set(
        urgency_response.output.repair_attempts[0]["errors_sent"]
    )
    urgency_template_ids = urgency_response.output.decision.template_ids

    assert urgency_response.status == "succeeded"
    assert repair_provider.calls == []
    assert {
        "diagnostic_next_question_not_missing",
        "diagnostic_final_demo_stage_missing",
        "diagnostic_final_staged_order_invalid",
    }.issubset(urgency_error_codes)
    assert urgency_response.output.decision.diagnostic_action == "complete"
    assert urgency_response.output.diagnostic is not None
    assert urgency_response.output.diagnostic.status == "completed"
    assert urgency_response.output.diagnostic.next_question is None
    assert urgency_template_ids[:4] == [
        "diagnostic.deliver_hold",
        "diagnostic.deliver_context",
        "diagnostic.deliver_crm_base",
        "diagnostic.deliver_operational_step",
    ]
    assert urgency_template_ids[-1] == "diagnostic.deliver_demo_not_offered"

    demo_request = _whatsapp_request()
    demo_request.message.idempotency_key = "whatsapp:long-preflight-latest:10"
    demo_request.message.channel_message_id = "wamid_long_preflight_latest_10"
    demo_request.message.text = "me manda demo"
    demo_request.metadata["spec011_eval_trace"] = True
    demo_response = await run_spec011_agent_turn(
        demo_request,
        memory_store=store,
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=FakeDemoDirectStalePriceIntentProvider(),
        repair_provider=repair_provider,
    )
    demo_error_codes = set(demo_response.output.repair_attempts[0]["errors_sent"])

    assert demo_response.status == "succeeded"
    assert repair_provider.calls == []
    assert {
        "price_question_missing_price_answer",
        "demo_direct_question_flags_missing",
    }.issubset(demo_error_codes)
    assert demo_response.output.decision.route == "product"
    assert demo_response.output.decision.detected_intents == ["demo_request"]
    assert demo_response.output.decision.direct_question_answered_first is True
    assert demo_response.output.decision.template_ids == ["product.demo_direct"]
    assert demo_response.output.diagnostic is not None
    assert demo_response.output.diagnostic.status == "completed"


@pytest.mark.asyncio
async def test_whatsapp_runtime_adapter_preserves_provider_ids() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    request = _whatsapp_request()
    provider = FakeConductorProvider()

    response = await run_spec011_agent_turn(
        request,
        memory_store=InMemoryMemoryStore(),
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=provider,
    )

    assert len(provider.calls) == 1
    context = provider.calls[0].context
    assert context.conversation_id == "wa_conv_5511999990000"
    assert context.channel == "whatsapp"
    assert context.inbound.idempotency_key == "whatsapp:wamid.HBgMNTUxMTk5OTk5MDAwMA"
    assert context.inbound.message_id == "wamid.HBgMNTUxMTk5OTk5MDAwMA"
    assert any(
        fact.key == "whatsapp_phone"
        and fact.value == "+5511999990000"
        and fact.source == "channel_metadata"
        for fact in context.facts
    )
    assert context.sales_inbox_inputs["source"] == "taliya_whatsapp"
    assert context.sales_inbox_inputs["channel_conversation_id"] == "wa_conv_5511999990000"

    assert response.conversation_id == "wa_conv_5511999990000"
    assert response.lead_id == "lead_whatsapp_123"
    assert response.current_agent == "taliya_commercial_spec011_product_agent"
    assert response.output.usage.model == "gpt-5.4-mini"
    assert response.output.usage.input_tokens > 0
    assert response.output.decision.route == "product"
    assert response.output.messages[0].channel_hint == "whatsapp"
    assert response.output.messages[0].template_id == "product.price_direct"
    assert response.trace_id.startswith("trace_")


def test_spec011_runtime_api_endpoint_calls_core_adapter_for_widget(monkeypatch) -> None:
    import app.main as runtime_main
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    captured: list[AgentRunRequest] = []

    async def fake_core_turn(
        request: AgentRunRequest,
        *,
        memory_store: InMemoryMemoryStore,
        provider: str,
        model: str,
    ):
        captured.append(request)
        return await run_spec011_agent_turn(
            request,
            memory_store=InMemoryMemoryStore(),
            provider=provider,
            model=model,
            conductor_provider=FakeConductorProvider(),
        )

    monkeypatch.setattr(runtime_main, "run_spec011_agent_turn", fake_core_turn)
    body = b"""{
      "agent_key":"taliya_commercial",
      "channel":"widget",
      "conversation":{
        "conversation_id":"browser_session_123",
        "lead_id":"lead_widget_123",
        "channel_conversation_id":"browser_session_123",
        "source":"pilates_landing",
        "entry_intent":"widget"
      },
      "message":{
        "idempotency_key":"widget:browser_session_123:1:abc",
        "channel_message_id":"web_msg_123",
        "type":"text",
        "text":"quanto custa?",
        "timestamp":"2026-05-30T12:00:00Z"
      },
      "sender":{"name":"Ana"},
      "metadata":{
        "spec011_core_contract":"taliya_commercial_core_reset_v1",
        "page_path":"/pilates",
        "source_section":"floating_agent",
        "provider":"widget"
      }
    }"""

    response = TestClient(runtime_main.app).post(
        "/v1/taliya-commercial/turn",
        content=body,
        headers=_signed_headers(body, "req_spec011_widget_adapter_api"),
    )

    assert response.status_code == 200
    assert len(captured) == 1
    assert captured[0].channel == "widget"
    assert captured[0].conversation.source == "pilates_landing"
    assert captured[0].conversation.conversation_id == "browser_session_123"
    payload = response.json()
    assert payload["current_agent"] == "taliya_commercial_spec011_product_agent"
    assert payload["output"]["usage"]["input_tokens"] > 0


def test_spec011_runtime_api_endpoint_calls_core_adapter_for_taliya_whatsapp(monkeypatch) -> None:
    import app.main as runtime_main
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    captured: list[AgentRunRequest] = []

    async def fake_core_turn(
        request: AgentRunRequest,
        *,
        memory_store: InMemoryMemoryStore,
        provider: str,
        model: str,
    ):
        captured.append(request)
        return await run_spec011_agent_turn(
            request,
            memory_store=InMemoryMemoryStore(),
            provider=provider,
            model=model,
            conductor_provider=FakeConductorProvider(),
        )

    monkeypatch.setattr(runtime_main, "run_spec011_agent_turn", fake_core_turn)
    body = b"""{
      "agent_key":"taliya_commercial",
      "channel":"whatsapp",
      "conversation":{
        "conversation_id":"wa_conv_5511999990000",
        "lead_id":"lead_whatsapp_123",
        "channel_conversation_id":"wa_conv_5511999990000",
        "source":"taliya_whatsapp",
        "entry_intent":"whatsapp"
      },
      "message":{
        "idempotency_key":"whatsapp:wamid.HBgMNTUxMTk5OTk5MDAwMA",
        "channel_message_id":"wamid.HBgMNTUxMTk5OTk5MDAwMA",
        "type":"text",
        "text":"vi no whatsapp, serve pro meu studio?",
        "timestamp":"2026-05-30T12:00:00Z"
      },
      "sender":{"name":"Ana WhatsApp","whatsapp_phone":"+5511999990000"},
      "metadata":{
        "spec011_core_contract":"taliya_commercial_core_reset_v1",
        "page_path":"whatsapp:taliya",
        "source_section":"taliya_owned_whatsapp",
        "provider":"whatsapp"
      }
    }"""

    response = TestClient(runtime_main.app).post(
        "/v1/taliya-commercial/turn",
        content=body,
        headers=_signed_headers(body, "req_spec011_whatsapp_adapter_api"),
    )

    assert response.status_code == 200
    assert len(captured) == 1
    assert captured[0].channel == "whatsapp"
    assert captured[0].conversation.source == "taliya_whatsapp"
    assert captured[0].conversation.conversation_id == "wa_conv_5511999990000"
    assert captured[0].message.channel_message_id == "wamid.HBgMNTUxMTk5OTk5MDAwMA"
    payload = response.json()
    assert payload["current_agent"] == "taliya_commercial_spec011_product_agent"
    assert payload["output"]["usage"]["input_tokens"] > 0


def test_openai_runtime_uses_real_repair_provider_only_for_openai(monkeypatch) -> None:
    from app.core.taliya_commercial.runtime_adapter import (
        OpenAIRepairProvider,
        _repair_provider_for,
    )

    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    assert isinstance(
        _repair_provider_for(provider="openai", model="gpt-5.4-mini"),
        OpenAIRepairProvider,
    )
    assert _repair_provider_for(provider="mock", model="gpt-5.4-mini") is None
