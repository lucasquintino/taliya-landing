from __future__ import annotations

import json
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
from app.core.taliya_commercial.conductor import ConductorProviderRequest
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


def _request(*, channel: str = "widget", shadow: bool = True) -> AgentRunRequest:
    metadata: dict[str, Any] = {
        "spec011_core_contract": "taliya_commercial_core_reset_v1",
        "provider": channel,
        "source_section": "taliya_owned_whatsapp" if channel == "whatsapp" else "floating_agent",
    }
    if shadow:
        metadata["spec011_shadow_mode"] = {
            "enabled": True,
            "reason": "t011_096_shadow_review",
        }
    return AgentRunRequest(
        agent_key="taliya_commercial",
        channel=channel,  # type: ignore[arg-type]
        conversation={
            "conversation_id": f"{channel}_shadow_conv_1",
            "lead_id": f"lead_{channel}_shadow_1",
            "channel_conversation_id": f"{channel}_shadow_channel_1",
            "source": "taliya_whatsapp" if channel == "whatsapp" else "pilates_landing",
            "entry_intent": channel,
        },
        message={
            "idempotency_key": f"{channel}:shadow:1",
            "channel_message_id": f"{channel}_message_1",
            "type": "text",
            "text": "quanto custa e serve pro meu studio?",
            "timestamp": "2026-05-31T12:00:00Z",
        },
        sender={
            "name": "Ana",
            "whatsapp_phone": "+5511999990000" if channel == "whatsapp" else None,
        },
        metadata=metadata,
    )


class FakeConductorProvider:
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
            previous_state="new_lead",
            current_state="product_question",
            next_state="product_question",
            detected_intents=["price_question"],
            direct_question_present=True,
            direct_question_answered_first=True,
            diagnostic={"action": "offer"},
            facts=[
                TurnFact(
                    key="asked_price",
                    value="quanto custa",
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
                        variables={
                            "plan_price_summary": TemplateVariableValue(
                                kind="long_text",
                                value="Resumo oficial dos planos disponiveis.",
                                source="official_product_knowledge",
                                evidence=["product_knowledge.prices"],
                                max_length=360,
                            )
                        },
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
            confidence="high",
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


@pytest.mark.asyncio
async def test_shadow_mode_runs_core_trace_and_projection_without_public_reply() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    memory_store = InMemoryMemoryStore()
    provider = FakeConductorProvider()

    response = await run_spec011_agent_turn(
        _request(shadow=True),
        memory_store=memory_store,
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=provider,
    )

    assert len(provider.calls) == 1
    assert response.delivery_control.shadow_mode is True
    assert response.delivery_control.delivery_suppressed is True
    assert response.delivery_control.suppression_reason == "t011_096_shadow_review"
    assert response.delivery_control.rendered_message_count == 5
    assert response.output.messages == []
    assert response.output.usage.input_tokens == 321
    assert response.output.usage.output_tokens == 123
    assert response.output.decision.route == "product"
    assert "shadow_mode" in response.output.safety_flags
    assert "delivery_suppressed" in response.output.safety_flags
    assert response.output.tool_results[0].name == "shadow_mode"
    assert response.output.tool_results[0].status == "ok"

    events = await memory_store.list_events("widget_shadow_conv_1")
    assert [event.type for event in events] == ["context_update"]
    shadow_event = events[0]
    assert shadow_event.content == "spec011_shadow_turn_completed"
    assert shadow_event.metadata["shadow_mode"] is True
    assert shadow_event.metadata["delivery_suppressed"] is True
    assert shadow_event.metadata["rendered_message_count"] == 5
    assert (
        shadow_event.metadata["trace"]["rendered_messages"][0]["template_id"]
        == "product.price_direct"
    )
    assert shadow_event.metadata["trace"]["delivery_events"][0]["event"] == "delivery_suppressed"
    assert shadow_event.metadata["trace"]["delivery_events"][0]["status"] == "suppressed"
    assert shadow_event.metadata["runtime_state_diff"]["source"] == "accepted_decision"
    assert shadow_event.metadata["sales_inbox_projection"]["commercial_stage"] == "product_question"

    usage = await memory_store.list_model_usage("widget_shadow_conv_1")
    assert usage[0]["input_tokens"] == 321
    assert usage[0]["output_tokens"] == 123

    assert await memory_store.load_state("widget_shadow_conv_1", "taliya_commercial") is None


@pytest.mark.asyncio
async def test_normal_mode_still_returns_messages_and_persists_live_state() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    memory_store = InMemoryMemoryStore()
    response = await run_spec011_agent_turn(
        _request(shadow=False),
        memory_store=memory_store,
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=FakeConductorProvider(),
    )

    assert response.delivery_control.shadow_mode is False
    assert response.delivery_control.delivery_suppressed is False
    assert response.output.messages
    state = await memory_store.load_state("widget_shadow_conv_1", "taliya_commercial")
    assert isinstance(state, RuntimeState)
    assert any(item.get("role") == "assistant" for item in state.input_items)
    events = await memory_store.list_events("widget_shadow_conv_1")
    assert events[0].content == "spec011_core_turn_completed"
    assert events[0].metadata.get("delivery_suppressed") is not True


def test_shadow_mode_api_envelope_is_explicit_for_widget(monkeypatch) -> None:
    import app.main as runtime_main
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    async def fake_core_turn(
        request: AgentRunRequest,
        *,
        memory_store: InMemoryMemoryStore,
        provider: str,
        model: str,
    ):
        return await run_spec011_agent_turn(
            request,
            memory_store=InMemoryMemoryStore(),
            provider=provider,
            model=model,
            conductor_provider=FakeConductorProvider(),
        )

    monkeypatch.setattr(runtime_main, "run_spec011_agent_turn", fake_core_turn)
    body = json.dumps(_request(channel="widget", shadow=True).model_dump(mode="json")).encode()

    response = TestClient(runtime_main.app).post(
        "/v1/taliya-commercial/turn",
        content=body,
        headers=_signed_headers(body, "req_spec011_shadow_widget"),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["delivery_control"]["shadow_mode"] is True
    assert payload["delivery_control"]["delivery_suppressed"] is True
    assert payload["delivery_control"]["suppression_reason"] == "t011_096_shadow_review"
    assert payload["delivery_control"]["rendered_message_count"] == 5
    assert payload["output"]["messages"] == []
    assert payload["output"]["usage"]["input_tokens"] > 0
    assert payload["output"]["tool_results"][0]["name"] == "shadow_mode"


@pytest.mark.asyncio
async def test_shadow_mode_uses_same_core_boundary_for_taliya_whatsapp() -> None:
    from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn

    provider = FakeConductorProvider()
    response = await run_spec011_agent_turn(
        _request(channel="whatsapp", shadow=True),
        memory_store=InMemoryMemoryStore(),
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=provider,
    )

    assert len(provider.calls) == 1
    assert provider.calls[0].context.channel == "whatsapp"
    assert provider.calls[0].context.sales_inbox_inputs["source"] == "taliya_whatsapp"
    assert response.delivery_control.shadow_mode is True
    assert response.output.messages == []
    assert response.output.usage.input_tokens > 0
