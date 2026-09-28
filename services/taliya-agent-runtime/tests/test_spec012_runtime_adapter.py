from __future__ import annotations

import pytest

from app.core.taliya_commercial_sdk.action_turn_runner import (
    ActionConversationReport,
    ActionTurnReport,
)
from app.core.taliya_commercial_sdk.conductor_decision import ConductorActionDecision
from app.core.taliya_commercial_sdk.runtime_adapter import run_action_first_agent_turn
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import InMemoryMemoryStore, RuntimeState
from tests.test_spec012_sdk_paid_harness_dry_run import (
    ScriptedFakeModel,
    _function_call,
    _message,
)


def _decision_json(action: str, **overrides) -> str:
    payload = {"selected_action": action, "evidence": ["inbound.text"], **overrides}
    return ConductorActionDecision.model_validate(payload).model_dump_json()


@pytest.mark.asyncio
async def test_t012_031_runtime_adapter_returns_agent_run_response_with_no_cost_model() -> None:
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_direct_product_question",
                        direct_question="quanto custa?",
                        product_fact_keys_used=["prices"],
                    )
                )
            ],
        ]
    )
    request = AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {
                "conversation_id": "conv_spec012_runtime_adapter",
                "lead_id": "lead_spec012_runtime_adapter",
                "source": "pilates_landing",
                "entry_intent": "price_question",
            },
            "message": {
                "idempotency_key": "widget:conv_spec012_runtime_adapter:1",
                "type": "text",
                "text": "quanto custa?",
            },
            "sender": {"name": "Ana"},
            "metadata": {"page_path": "/pilates", "provider": "widget"},
        }
    )
    memory_store = InMemoryMemoryStore()

    result = await run_action_first_agent_turn(
        request,
        memory_store=memory_store,
        provider="mock",
        model="mocked-sdk-dry-run",
        sdk_model=fake_model,
    )

    assert result.status == "succeeded"
    assert result.conversation_id == "conv_spec012_runtime_adapter"
    assert result.current_agent == "taliya_triage_agent"
    assert result.output.messages
    assert result.output.decision.current_state == "product_question"
    assert result.output.decision.next_state == "diagnostic_offered"
    assert result.output.decision.template_ids == [
        "product.price_direct",
        "diagnostic.price_hook",
    ]
    assert result.output.turn_situation["mode"] == "entry"
    assert (
        result.output.action_decision["selected_action"]
        == "answer_direct_product_question"
    )
    assert result.output.validator_results[0]["status"] == "passed"
    assert result.output.repair_attempts[0]["repair_attempt_count"] == 0
    assert result.output.context_snapshot["state_snapshot"] == {
        "conversation_id": "conv_spec012_runtime_adapter",
        "lead_id": "lead_spec012_runtime_adapter",
        "source": "pilates_landing",
        "channel": "widget",
    }
    assert result.output.delivery_events[0]["trace_delivery"]["public_delivery"] is False
    assert result.output.delivery_events[0]["trace_delivery"]["outbox_reserved"] is False
    assert result.output.trace_complete is True
    assert result.output.sales_inbox_projection
    assert result.output.sales_inbox_projection["conversation_id"] == (
        "conv_spec012_runtime_adapter"
    )
    assert result.output.sales_inbox_projection["lead_id"] == (
        "lead_spec012_runtime_adapter"
    )
    assert result.output.sales_inbox_projection["commercial_stage"] == (
        "diagnostic_offered"
    )
    assert result.output.sales_inbox_projection["fields"]["template_ids"] == [
        "product.price_direct",
        "diagnostic.price_hook",
    ]
    assert result.output.usage.cost_usd == 0
    assert result.output.usage.model_operations == 2
    assert result.output.usage.input_tokens == 2_000
    assert result.output.usage.cached_input_tokens == 0
    assert result.output.usage.cache_write_input_tokens == 0
    assert result.output.usage.output_tokens == 400
    assert result.output.usage.reasoning_tokens == 0
    assert result.output.usage.repairs == 0
    assert result.output.usage.latency_ms >= 0
    state = await memory_store.load_state(
        "conv_spec012_runtime_adapter",
        "taliya_commercial",
    )
    assert state is not None
    assert state.last_decision is not None
    assert state.last_decision["next_state"] == "diagnostic_offered"
    assert state.last_decision["template_ids"] == [
        "product.price_direct",
        "diagnostic.price_hook",
    ]
    assert state.cost_usd == 0

    usage_records = await memory_store.list_model_usage(
        "conv_spec012_runtime_adapter"
    )
    assert len(usage_records) == 1
    assert usage_records[0]["model"] == "mocked-sdk-dry-run"
    assert usage_records[0]["model_operations"] == 2
    assert usage_records[0]["input_tokens"] == 2_000
    assert usage_records[0]["output_tokens"] == 400
    assert usage_records[0]["provider"] == "mock"

    events = await memory_store.list_events("conv_spec012_runtime_adapter")
    assert len(events) == 1
    trace_summary = events[0].metadata["trace_summary"]
    assert trace_summary["schema"] == "012.runtime_action_trace_summary.v1"
    assert trace_summary["trace_id"] == result.trace_id
    assert trace_summary["trace_complete"] is True
    assert trace_summary["sdk_run_items"]
    assert trace_summary["turn_situation"]["mode"] == "entry"
    assert trace_summary["action_decision"]["selected_action"] == (
        "answer_direct_product_question"
    )
    assert trace_summary["compiler"]["template_ids"] == [
        "product.price_direct",
        "diagnostic.price_hook",
    ]
    assert trace_summary["validators"]["status"] == "passed"
    assert trace_summary["sales_inbox_projection"]["lead_id"] == (
        "lead_spec012_runtime_adapter"
    )
    assert trace_summary["delivery"]["public_delivery"] is False
    assert "inbound" not in trace_summary
    assert "rendered_messages" not in trace_summary


@pytest.mark.asyncio
async def test_t012_031_runtime_adapter_persists_action_first_state_fields() -> None:
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "send_demo",
                        direct_question="tem demo?",
                        product_fact_keys_used=["links"],
                        demo_intent="requested",
                    )
                )
            ],
        ]
    )
    request = AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {
                "conversation_id": "conv_spec012_state_persistence",
                "lead_id": "lead_spec012_state_persistence",
                "source": "pilates_landing",
                "entry_intent": "demo_question",
            },
            "message": {
                "idempotency_key": "widget:conv_spec012_state_persistence:1",
                "type": "text",
                "text": "tem demo?",
            },
            "sender": {"name": "Bia"},
            "metadata": {"page_path": "/pilates", "provider": "widget"},
        }
    )
    memory_store = InMemoryMemoryStore()

    result = await run_action_first_agent_turn(
        request,
        memory_store=memory_store,
        provider="mock",
        model="mocked-sdk-dry-run",
        sdk_model=fake_model,
    )

    assert result.status == "succeeded"
    assert result.output.decision.template_ids == ["product.demo_direct"]
    assert result.output.runtime_state["demo"]["status"] == "offered"

    state = await memory_store.load_state(
        "conv_spec012_state_persistence",
        "taliya_commercial",
    )
    assert state is not None
    assert state.demo == {"status": "offered"}
    assert state.answered_direct_questions == ["tem demo?"]
    assert state.last_decision is not None
    assert state.last_decision["next_state"] == "demo_reaction_pending"
    assert state.input_items[-1]["content"] == "tem demo?"
    assert state.cost_usd == 0


@pytest.mark.asyncio
async def test_widget_diagnostic_acceptance_does_not_repeat_opening() -> None:
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_diagnostic_agent")],
            [_message(_decision_json("start_requested_diagnostic"))],
        ]
    )
    request = AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {
                "conversation_id": "conv_widget_accepts_diagnostic_offer",
                "lead_id": "lead_widget_accepts_diagnostic_offer",
                "source": "pilates_landing",
                "entry_intent": "pilates_landing",
            },
            "message": {
                "idempotency_key": "widget:conv_widget_accepts_diagnostic_offer:3",
                "type": "text",
                "text": "sim",
            },
            "sender": {},
            "metadata": {
                "page_path": "/pilates",
                "provider": "widget",
                "recent_client_messages": [
                    {
                        "role": "assistant",
                        "content": (
                            "Oi. Estou aqui para te acompanhar e responder "
                            "dúvidas sobre a Taliya."
                        ),
                    },
                    {
                        "role": "assistant",
                        "content": (
                            "Se fizer sentido para você, podemos fazer um "
                            "diagnóstico gratuito do seu studio. O que você acha?"
                        ),
                    },
                    {"role": "user", "content": "sim"},
                ],
            },
        }
    )
    memory_store = InMemoryMemoryStore()

    result = await run_action_first_agent_turn(
        request,
        memory_store=memory_store,
        provider="mock",
        model="mocked-sdk-dry-run",
        sdk_model=fake_model,
    )

    texts = [message.text for message in result.output.messages]
    rendered = "\n".join(texts)

    assert result.status == "succeeded"
    assert result.output.decision.template_ids == [
        "diagnostic.start",
        "diagnostic.ask_active_students",
    ]
    assert "Hoje seu studio tem mais ou menos quantos alunos ativos?" in rendered
    assert "Oi, tudo bem?" not in rendered
    assert "Em que posso ajudar?" not in rendered
    assert result.output.context_snapshot["state_snapshot"][
        "client_has_prior_assistant_messages"
    ] is True
    assert result.output.context_snapshot["state_snapshot"]["channel"] == "widget"


@pytest.mark.asyncio
async def test_t012_050_shadow_mode_suppresses_delivery_and_does_not_mutate_state() -> None:
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_direct_product_question",
                        direct_question="quanto custa?",
                        product_fact_keys_used=["prices"],
                    )
                )
            ],
        ]
    )
    request = AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {
                "conversation_id": "conv_spec012_shadow_simulated",
                "lead_id": "lead_spec012_shadow_simulated",
                "source": "pilates_landing",
                "entry_intent": "price_question",
            },
            "message": {
                "idempotency_key": "widget:conv_spec012_shadow_simulated:1",
                "type": "text",
                "text": "quanto custa?",
            },
            "sender": {"name": "Ana"},
            "metadata": {
                "page_path": "/pilates",
                "provider": "widget",
                "spec012_shadow_mode": {
                    "enabled": True,
                    "reason": "t012_050_simulated_shadow_no_real_leads",
                },
            },
        }
    )
    memory_store = InMemoryMemoryStore()

    result = await run_action_first_agent_turn(
        request,
        memory_store=memory_store,
        provider="mock",
        model="mocked-sdk-dry-run",
        sdk_model=fake_model,
    )

    assert result.status == "succeeded"
    assert result.delivery_control.shadow_mode is True
    assert result.delivery_control.delivery_suppressed is True
    assert result.delivery_control.suppression_reason == (
        "t012_050_simulated_shadow_no_real_leads"
    )
    assert result.delivery_control.rendered_message_count > 0
    assert result.output.messages == []
    assert result.output.safety_flags == ["shadow_mode", "delivery_suppressed"]
    assert result.output.tool_results[0].name == "shadow_mode"
    assert result.output.delivery_events[0]["type"] == "delivery_suppressed"
    assert result.output.delivery_events[0]["shadow_mode"] is True
    assert result.output.sales_inbox_projection["lead_id"] == (
        "lead_spec012_shadow_simulated"
    )
    assert result.output.trace_complete is True

    events = await memory_store.list_events("conv_spec012_shadow_simulated")
    assert len(events) == 1
    assert events[0].type == "context_update"
    assert events[0].content == "spec012_shadow_turn_completed"
    assert events[0].metadata["shadow_mode"] is True
    assert events[0].metadata["delivery_suppressed"] is True
    assert events[0].metadata["rendered_message_count"] > 0
    assert events[0].metadata["trace_summary"]["trace_complete"] is True
    assert events[0].metadata["sales_inbox_projection"]["conversation_id"] == (
        "conv_spec012_shadow_simulated"
    )

    usage = await memory_store.list_model_usage("conv_spec012_shadow_simulated")
    assert len(usage) == 1
    assert usage[0]["model"] == "mocked-sdk-dry-run"
    assert usage[0]["model_operations"] == 2
    assert usage[0]["input_tokens"] == 2_000
    assert usage[0]["cached_input_tokens"] == 0
    assert usage[0]["cache_write_input_tokens"] == 0
    assert usage[0]["output_tokens"] == 400
    assert usage[0]["reasoning_tokens"] == 0
    assert usage[0]["repairs"] == 0
    assert usage[0]["latency_ms"] >= 0
    assert usage[0]["cost_usd"] == 0.0
    assert usage[0]["shadow_mode"] is True
    assert usage[0]["provider"] == "mock"
    assert (
        await memory_store.load_state(
            "conv_spec012_shadow_simulated",
            "taliya_commercial",
        )
        is None
    )


@pytest.mark.asyncio
async def test_t012_036_runtime_adapter_cost_cap_blocks_before_sdk_call() -> None:
    request = AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {
                "conversation_id": "conv_spec012_cost_cap",
                "lead_id": "lead_spec012_cost_cap",
                "source": "pilates_landing",
                "entry_intent": "price_question",
            },
            "message": {
                "idempotency_key": "widget:conv_spec012_cost_cap:1",
                "type": "text",
                "text": "quanto custa?",
            },
            "sender": {"name": "Caio"},
            "metadata": {"page_path": "/pilates", "provider": "widget"},
        }
    )
    memory_store = InMemoryMemoryStore()
    await memory_store.save_state(
        RuntimeState(
            conversation_id="conv_spec012_cost_cap",
            agent_key="taliya_commercial",
            current_agent_name="taliya_product_agent",
            cost_usd=0.20,
            last_decision={"next_state": "diagnostic_offered"},
        )
    )

    result = await run_action_first_agent_turn(
        request,
        memory_store=memory_store,
        provider="mock",
        model="mocked-sdk-dry-run",
        cost_cap_usd=0.15,
        sdk_model=None,
    )

    assert result.status == "cost_capped"
    assert result.output.messages == []
    assert result.output.handoff is not None
    assert result.output.handoff.status == "active"
    assert result.output.safety_flags == [
        "cost_cap_reached",
        "human_follow_up_required",
    ]
    assert result.output.decision.route == "safe_fallback"
    assert result.output.decision.next_state == "cost_cap_deferred"
    assert result.output.delivery_events == [
        {
            "type": "cost_cap_suppressed",
            "message_count": 0,
            "cost_cap_usd": 0.15,
            "prior_cost_usd": 0.20,
        }
    ]
    guardrails = await memory_store.list_guardrail_events("conv_spec012_cost_cap")
    assert guardrails[0]["reason"] == "cost_cap_reached"
    events = await memory_store.list_events("conv_spec012_cost_cap")
    assert events[0].type == "guardrail"
    assert events[0].metadata["status"] == "cost_capped"


@pytest.mark.asyncio
async def test_t012_055_runtime_adapter_runs_openai_provider_after_public_activation(
    monkeypatch,
) -> None:
    captured_kwargs = {}

    async def fake_paid_conversation(user_messages, **kwargs):
        captured_kwargs["user_messages"] = list(user_messages)
        captured_kwargs.update(kwargs)
        return ActionConversationReport(
            turns=[
                ActionTurnReport(
                    user_text="quanto custa?",
                    mode="entry",
                    starting_agent="taliya_triage_agent",
                    llm_called=True,
                    status="delivered",
                    selected_action="answer_direct_product_question",
                    template_ids=("product.price_direct", "diagnostic.price_hook"),
                    rendered_messages=("Plano Essencial: R$ 497/mês.",),
                    cost_usd=0.004,
                    next_state="diagnostic_offered",
                    sales_inbox_projection={
                        "conversation_id": "conv_spec012_paid_runtime",
                        "lead_id": "lead_spec012_paid_runtime",
                        "commercial_stage": "diagnostic_offered",
                        "fields": {
                            "template_ids": [
                                "product.price_direct",
                                "diagnostic.price_hook",
                            ],
                            "validator_status": "passed",
                            "source_labels": [],
                        },
                    },
                    trace={
                        "trace_complete": True,
                        "compiler": {
                            "previous_state": "new_lead",
                            "current_state": "product_question",
                            "next_state": "diagnostic_offered",
                            "route": "product",
                            "template_ids": [
                                "product.price_direct",
                                "diagnostic.price_hook",
                            ],
                            "render_plan": [
                                {"template_id": "product.price_direct"},
                                {"template_id": "diagnostic.price_hook"},
                            ],
                        },
                        "validators": {"status": "passed"},
                        "delivery": {
                            "public_delivery": False,
                            "outbox_reserved": False,
                        },
                    },
                )
            ],
            final_state={"canonical_state": "diagnostic_offered"},
            total_model_operations=1,
            total_cost_usd=0.004,
            cost_cap_usd=0.15,
        )

    import app.core.taliya_commercial_sdk.runtime_adapter as adapter

    monkeypatch.setattr(adapter, "run_action_conversation", fake_paid_conversation)
    request = AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {
                "conversation_id": "conv_spec012_paid_runtime",
                "lead_id": "lead_spec012_paid_runtime",
                "source": "pilates_landing",
                "entry_intent": "price_question",
            },
            "message": {
                "idempotency_key": "widget:conv_spec012_paid_runtime:1",
                "type": "text",
                "text": "quanto custa?",
            },
            "sender": {"name": "Ana"},
            "metadata": {"page_path": "/pilates", "provider": "widget"},
        }
    )
    memory_store = InMemoryMemoryStore()

    result = await run_action_first_agent_turn(
        request,
        memory_store=memory_store,
        provider="openai",
        model="gpt-5.4-mini",
    )

    assert result.status == "succeeded"
    assert result.output.messages[0].text == "Plano Essencial: R$ 497/mês."
    assert result.output.usage.cost_usd == 0.004
    assert captured_kwargs["model"] == "gpt-5.4-mini"
    assert captured_kwargs["paid_openai_approved"] is True
    assert captured_kwargs["max_total_cost_usd"] == 0.15

    state = await memory_store.load_state(
        "conv_spec012_paid_runtime",
        "taliya_commercial",
    )
    assert state is not None
    assert state.cost_usd == 0.004


@pytest.mark.asyncio
async def test_runtime_adapter_delivers_when_state_persistence_fails(monkeypatch) -> None:
    async def fake_paid_conversation(user_messages, **kwargs):
        return ActionConversationReport(
            turns=[
                ActionTurnReport(
                    user_text="100",
                    mode="diagnostic",
                    starting_agent="taliya_diagnostic_agent",
                    llm_called=True,
                    status="delivered",
                    selected_action="capture_pending_diagnostic_answer",
                    template_ids=("diagnostic.ask_main_pain",),
                    rendered_messages=(
                        "Entendi. Já dá para ter uma noção do tamanho do studio.",
                        "Quais partes mais dão trabalho hoje: WhatsApp, agenda/reposições, "
                        "vendas, financeiro ou acompanhamento dos alunos?",
                    ),
                    cost_usd=0.004,
                    next_state="diagnostic_waiting_answer",
                    sales_inbox_projection={
                        "conversation_id": "conv_spec012_persistence_degraded",
                        "lead_id": "lead_spec012_persistence_degraded",
                        "commercial_stage": "diagnostic_waiting_answer",
                        "fields": {
                            "template_ids": ["diagnostic.ask_main_pain"],
                            "validator_status": "passed",
                            "source_labels": [],
                        },
                    },
                    trace={
                        "trace_complete": True,
                        "compiler": {
                            "previous_state": "diagnostic_waiting_answer",
                            "current_state": "diagnostic_in_progress",
                            "next_state": "diagnostic_waiting_answer",
                            "route": "diagnostic",
                            "template_ids": ["diagnostic.ask_main_pain"],
                            "render_plan": [{"template_id": "diagnostic.ask_main_pain"}],
                        },
                        "validators": {"status": "passed"},
                        "delivery": {
                            "public_delivery": False,
                            "outbox_reserved": False,
                        },
                    },
                )
            ],
            final_state={
                "canonical_state": "diagnostic_waiting_answer",
                "diagnostic": {
                    "status": "in_progress",
                    "ledger": {
                        "active_students_or_size": {
                            "status": "answered",
                            "answer_value": "100",
                        }
                    },
                },
            },
            total_model_operations=1,
            total_cost_usd=0.004,
            cost_cap_usd=0.15,
        )

    class FailingSaveStateStore(InMemoryMemoryStore):
        async def save_state(self, state):  # type: ignore[no-untyped-def]
            raise RuntimeError("database write failed")

    import app.core.taliya_commercial_sdk.runtime_adapter as adapter

    monkeypatch.setattr(adapter, "run_action_conversation", fake_paid_conversation)
    request = AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {
                "conversation_id": "conv_spec012_persistence_degraded",
                "lead_id": "lead_spec012_persistence_degraded",
                "source": "pilates_landing",
                "entry_intent": "diagnostic_cta",
            },
            "message": {
                "idempotency_key": "widget:conv_spec012_persistence_degraded:2",
                "type": "text",
                "text": "100",
            },
            "sender": {},
            "metadata": {"page_path": "/pilates", "provider": "widget"},
        }
    )

    result = await run_action_first_agent_turn(
        request,
        memory_store=FailingSaveStateStore(),
        provider="openai",
        model="gpt-5.4-mini",
    )

    assert result.status == "succeeded"
    assert result.output.messages
    assert "persistence_degraded" in result.output.safety_flags
    assert result.output.tool_results[-1].name == "save_runtime_state"
