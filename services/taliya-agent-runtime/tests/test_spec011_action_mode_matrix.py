from typing import Any

import pytest

from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn
from app.core.taliya_commercial.turn_situation import build_turn_situation
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import InMemoryMemoryStore, RuntimeState


def _request(text: str, *, message_suffix: str = "1") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {
                "conversation_id": "conv_mode_matrix",
                "lead_id": "lead_mode_matrix",
                "channel_conversation_id": "browser_mode_matrix",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": f"widget:conv_mode_matrix:{message_suffix}",
                "channel_message_id": f"web_mode_matrix_{message_suffix}",
                "type": "text",
                "text": text,
            },
            "sender": {"name": "Ana"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _state(
    *,
    diagnostic_status: str = "not_started",
    diagnostic_ledger: list[dict[str, Any]] | None = None,
    waitlist_status: str = "none",
    human_status: str = "none",
) -> RuntimeState:
    return RuntimeState(
        conversation_id="conv_mode_matrix",
        agent_key="taliya_commercial",
        current_agent_name="taliya_commercial_spec011_entry_agent",
        summary="Mode matrix state.",
        diagnostic={"status": diagnostic_status, "ledger": diagnostic_ledger or []},
        waitlist={"status": waitlist_status},
        demo={"status": "not_offered"},
        human_status=human_status,
    )


def _context(text: str, state: RuntimeState):
    return build_turn_context(
        turn_id="turn_mode_matrix",
        request=_request(text),
        state=state,
        recent_events=[],
        product_knowledge_keys=["prices", "plans", "links", "how_it_works"],
        spec006_contract_keys=["product_positioning"],
    )


@pytest.mark.parametrize(
    ("text", "state", "expected_mode", "expected_actions"),
    [
        (
            "quanto custa e quero entender se serve",
            _state(),
            "entry",
            {"answer_direct_product_question", "start_requested_diagnostic"},
        ),
        (
            "120",
            _state(diagnostic_status="in_progress"),
            "diagnostic",
            {"capture_pending_diagnostic_answer", "ask_next_diagnostic_question"},
        ),
        (
            "como funciona agora?",
            _state(
                diagnostic_status="completed",
                diagnostic_ledger=[
                    {
                        "question_key": key,
                        "status": "answered",
                        "answer_value": key,
                        "evidence": [f"message:{key}"],
                    }
                    for key in (
                        "active_students_or_size",
                        "main_pain",
                        "pain_detail",
                        "current_process",
                        "priority",
                        "urgency",
                    )
                ],
            ),
            "post_diagnostic",
            {"answer_product_question_with_saved_context", "send_demo"},
        ),
        (
            "quero entrar",
            _state(waitlist_status="pending_details"),
            "waitlist",
            {"collect_waitlist_missing_detail", "join_waitlist"},
        ),
        (
            "tudo bem",
            _state(human_status="active"),
            "handoff",
            {"suppress_ai_reply_while_human_active"},
        ),
    ],
)
def test_turn_situation_mode_matrix_provides_action_menu(
    text: str,
    state: RuntimeState,
    expected_mode: str,
    expected_actions: set[str],
) -> None:
    situation = build_turn_situation(_context(text, state))

    assert situation.mode == expected_mode
    assert expected_actions.issubset(set(situation.allowed_actions))


class RecordingActionProvider:
    def __init__(self) -> None:
        self.calls: list[Any] = []

    def __call__(self, request: Any) -> dict[str, Any]:
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
                "interpreted_intents": ["price_question", "diagnostic_interest"],
                "direct_question": {
                    "present": True,
                    "answered_first": True,
                    "answer_obligations": ["answer_price_from_official_facts"],
                },
                "captured_slots": [],
                "product_fact_keys_used": ["prices"],
                "numeric_interpretations": [],
                "diagnostic_intent": {
                    "status": "offer_after_answer",
                    "details": {
                        "plan_fit_context": (
                            "Como voce tambem quer fazer o diagnostico, faz sentido "
                            "comparar plano depois de entender a rotina."
                        )
                    },
                },
                "demo_intent": {"status": "none", "details": {}},
                "waitlist_intent": {"status": "none", "details": {}},
                "handoff_intent": {"status": "none", "details": {}},
                "reply_goal": "answer mixed price and diagnostic interest",
                "confidence": "high",
                "evidence": ["mixed_inbound_interpreted_by_llm"],
                "needs_clarification": False,
                "repair_hints": [],
            },
            "model_usage": {
                "model": "gpt-5.4-mini",
                "input_tokens": 180,
                "output_tokens": 44,
                "cost_usd": 0.001,
            },
        }


class QueueActionProvider:
    def __init__(self, actions: list[dict[str, Any]]) -> None:
        self.actions = list(actions)
        self.calls: list[Any] = []

    def __call__(self, request: Any) -> dict[str, Any]:
        self.calls.append(request)
        action = self.actions.pop(0)
        context = request.context
        return {
            "decision": {
                "schema_version": "011.action_decision.v1",
                "turn_id": context.turn_id,
                "conversation_id": context.conversation_id,
                "channel": context.channel,
                "agent_key": context.agent_key,
                "selected_action": action["selected_action"],
                "interpreted_intents": action["interpreted_intents"],
                "direct_question": action.get(
                    "direct_question",
                    {
                        "present": False,
                        "answered_first": False,
                        "answer_obligations": [],
                    },
                ),
                "captured_slots": action.get("captured_slots", []),
                "product_fact_keys_used": action.get("product_fact_keys_used", []),
                "numeric_interpretations": [],
                "diagnostic_intent": action.get(
                    "diagnostic_intent",
                    {"status": "none", "details": {}},
                ),
                "demo_intent": action.get("demo_intent", {"status": "none", "details": {}}),
                "waitlist_intent": action.get(
                    "waitlist_intent",
                    {"status": "none", "details": {}},
                ),
                "handoff_intent": {"status": "none", "details": {}},
                "reply_goal": action.get("reply_goal", action["selected_action"]),
                "confidence": "high",
                "evidence": action.get("evidence", ["llm_action_queue"]),
                "needs_clarification": False,
                "repair_hints": [],
            },
            "model_usage": {
                "model": "gpt-5.4-mini",
                "input_tokens": 160,
                "output_tokens": 42,
                "cost_usd": 0.001,
            },
        }


@pytest.mark.asyncio
async def test_mixed_commercial_message_goes_through_action_provider() -> None:
    provider = RecordingActionProvider()

    response = await run_spec011_agent_turn(
        _request("quanto custa e quero fazer o diagnostico"),
        memory_store=InMemoryMemoryStore(),
        provider="mock",
        model="gpt-5.4-mini",
        action_conductor_provider=provider,
    )

    assert len(provider.calls) == 1
    assert provider.calls[0].turn_situation.mode == "entry"
    assert response.output.usage.input_tokens == 180
    assert response.output.decision.detected_intents == [
        "price_question",
        "diagnostic_interest",
    ]


@pytest.mark.asyncio
async def test_long_conversation_action_preflight_covers_paid_failure_path() -> None:
    store = InMemoryMemoryStore()
    await store.save_state(
        _state(
            diagnostic_status="in_progress",
            diagnostic_ledger=[
                {
                    "question_key": key,
                    "status": "answered",
                    "answer_value": key,
                    "evidence": [f"message:{key}"],
                    "confidence": "high",
                }
                for key in (
                    "active_students_or_size",
                    "main_pain",
                    "pain_detail",
                    "current_process",
                    "priority",
                )
            ],
        )
    )
    provider = QueueActionProvider(
        [
            {
                "selected_action": "capture_pending_diagnostic_answer",
                "interpreted_intents": ["diagnostic_urgency_answer"],
                "captured_slots": [
                    {
                        "key": "urgency",
                        "value": "resolver agora",
                        "evidence": ["message:agora"],
                        "confidence": "high",
                    }
                ],
                "product_fact_keys_used": ["plans"],
                "diagnostic_intent": {
                    "status": "complete",
                    "details": {
                        "pain_context_human": "O ponto mais sensivel esta nos retornos.",
                        "crm_base_recommendation": (
                            "Organizar alunos e conversas em uma base unica."
                        ),
                        "operational_first_step": "Separar retornos pendentes do dia.",
                        "agent_pain_resolved": "retornos sem acompanhamento",
                        "agent_practical_action": "organiza contatos e proximos passos",
                    },
                },
            },
            {
                "selected_action": "send_demo",
                "interpreted_intents": ["demo_request"],
                "product_fact_keys_used": ["links"],
                "direct_question": {
                    "present": True,
                    "answered_first": True,
                    "answer_obligations": ["send_official_demo_link"],
                },
            },
            {
                "selected_action": "answer_price_objection_with_context",
                "interpreted_intents": ["price_objection"],
                "product_fact_keys_used": ["plans"],
                "direct_question": {
                    "present": True,
                    "answered_first": True,
                    "answer_obligations": ["answer_value_concern"],
                },
            },
            {
                "selected_action": "answer_product_question_with_saved_context",
                "interpreted_intents": ["how_it_works"],
                "product_fact_keys_used": ["how_it_works"],
                "direct_question": {
                    "present": True,
                    "answered_first": True,
                    "answer_obligations": ["answer_how_it_works"],
                },
            },
            {
                "selected_action": "offer_or_join_waitlist_if_eligible",
                "interpreted_intents": ["waitlist_interest"],
                "waitlist_intent": {
                    "status": "offered",
                    "details": {
                        "context_summary": (
                            "Lead completou diagnostico e demonstrou interesse em seguir."
                        )
                    },
                },
            },
        ]
    )
    turns = [
        ("agora", "a"),
        ("manda a demo", "b"),
        ("achei caro", "c"),
        ("como funciona?", "d"),
        ("quero entrar na lista", "e"),
    ]
    template_ids_by_turn: list[list[str | None]] = []

    for text, suffix in turns:
        response = await run_spec011_agent_turn(
            _request(text, message_suffix=suffix),
            memory_store=store,
            provider="mock",
            model="gpt-5.4-mini",
            action_conductor_provider=provider,
        )
        assert response.status == "succeeded"
        template_ids_by_turn.append(
            [message.template_id for message in response.output.messages]
        )

    assert len(provider.calls) == 5
    assert "diagnostic.deliver_hold" in template_ids_by_turn[0]
    assert "product.demo_direct" in template_ids_by_turn[1]
    assert "product.price_objection_value" in template_ids_by_turn[2]
    assert "product.how_it_works_direct" in template_ids_by_turn[3]
    assert "waitlist.offer_after_contract_intent" in template_ids_by_turn[4]
