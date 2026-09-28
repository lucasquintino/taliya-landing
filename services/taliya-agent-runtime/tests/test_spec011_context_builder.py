from __future__ import annotations

from app.core.taliya_commercial.context_builder import build_turn_context
from app.runtime.events import RuntimeEvent
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState


def _request(text: str = "Tenho 120 alunos e agenda baguncada") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_1",
                "lead_id": "lead_1",
                "channel_conversation_id": "wa_thread_1",
                "source": "pilates_landing",
                "entry_intent": "diagnostic_requested",
            },
            "message": {
                "idempotency_key": "inbound:v1:whatsapp:abc",
                "channel_message_id": "wamid_1",
                "type": "text",
                "text": text,
                "timestamp": "2026-05-30T12:00:00Z",
            },
            "sender": {
                "name": "Lucas",
                "whatsapp_phone": "+5511999999999",
                "email": None,
            },
            "metadata": {
                "page_path": "/pilates",
                "utm_source": "instagram",
                "provider": "meta_whatsapp",
                "runtime_control": {"ignored": True},
            },
        }
    )


def _state() -> RuntimeState:
    return RuntimeState(
        conversation_id="conv_1",
        agent_key="taliya_commercial",
        current_agent_name="taliya_commercial_product_agent",
        input_items=[
            {"role": "user", "content": "Oi", "id": "m0"},
            {"role": "assistant", "content": "Oi, tudo bem?", "id": "a0"},
            {"role": "user", "content": "Tenho 120 alunos", "id": "m1"},
        ],
        summary="Lead quer organizar agenda e reposicoes.",
        lead_facts=[
            {
                "key": "active_students_or_size",
                "value": "120",
                "confidence": "high",
                "evidence": ["m1"],
            }
        ],
        diagnostic={
            "status": "in_progress",
            "ledger": [
                {
                    "question_key": "active_students_or_size",
                    "status": "answered",
                    "answer_value": "120",
                    "evidence": ["m1"],
                    "confidence": "high",
                    "may_ask_again": False,
                },
                {
                    "question_key": "urgency",
                    "status": "missing",
                    "answer_value": None,
                    "evidence": [],
                    "confidence": "low",
                    "may_ask_again": True,
                },
            ],
        },
        demo={"status": "offered", "last_template_id": "demo.offer"},
        waitlist={"status": "none"},
        human_status="active",
        human_reason="operator took over",
        product_source_version="pk-2026-05-30",
        cost_usd=0.031,
    )


def test_context_builder_assembles_typed_context_from_runtime_state_and_channel_metadata() -> None:
    context = build_turn_context(
        turn_id="turn_1",
        request=_request(),
        state=_state(),
        recent_events=[
            RuntimeEvent(
                run_id="run_1",
                conversation_id="conv_1",
                agent_key="taliya_commercial",
                type="message",
                agent="taliya_commercial",
                content="Mensagem anterior",
                metadata={"role": "assistant", "template_id": "diagnostic.offer_soft"},
                timestamp_ms=100,
            )
        ],
        max_recent_transcript_items=3,
    )

    assert context.turn_id == "turn_1"
    assert context.conversation_id == "conv_1"
    assert context.channel == "whatsapp"
    assert context.inbound.message_id == "wamid_1"
    assert context.inbound.idempotency_key == "inbound:v1:whatsapp:abc"
    assert context.inbound.text == "Tenho 120 alunos e agenda baguncada"
    assert context.compact_memory == [
        {"kind": "summary", "value": "Lead quer organizar agenda e reposicoes."}
    ]
    assert context.diagnostic_ledger[0]["question_key"] == "active_students_or_size"
    assert context.diagnostic_ledger[1]["question_key"] == "urgency"
    assert context.waitlist_state == {"status": "none"}
    assert context.demo_state == {"status": "offered", "last_template_id": "demo.offer"}
    assert context.handoff_state == {"status": "active", "reason": "operator took over"}
    assert context.sales_inbox_inputs["lead_id"] == "lead_1"
    assert context.sales_inbox_inputs["source"] == "pilates_landing"
    assert len(context.recent_transcript) == 3
    assert context.recent_transcript[-1]["content"] == "Mensagem anterior"


def test_context_builder_labels_channel_metadata_as_internal_non_renderable_facts() -> None:
    context = build_turn_context(
        turn_id="turn_1",
        request=_request(),
        state=_state(),
        recent_events=[],
    )

    facts_by_key = {fact.key: fact for fact in context.facts}

    assert facts_by_key["source"].value == "pilates_landing"
    assert facts_by_key["source"].source == "channel_metadata"
    assert facts_by_key["source"].reliability == "internal"
    assert facts_by_key["source"].renderable is False
    assert facts_by_key["page_path"].value == "/pilates"
    assert facts_by_key["profile_name"].reliability == "channel_provided"
    assert facts_by_key["profile_name"].renderable is False
    assert facts_by_key["whatsapp_phone"].reliability == "channel_provided"
    assert facts_by_key["whatsapp_phone"].renderable is False


def test_context_builder_includes_default_product_knowledge() -> None:
    context = build_turn_context(
        turn_id="turn_1",
        request=_request("Quanto custa?"),
        state=_state(),
        recent_events=[],
    )

    keys = [item.key for item in context.product_knowledge]
    assert "prices" in keys
    assert "checkout_status" in keys
    assert context.inbound.text == "Quanto custa?"


def test_context_builder_carries_completed_diagnostic_final_fields_for_projection() -> None:
    state = _state()
    state.diagnostic = {
        "status": "completed",
        "final_fields": {
            "final_plan_or_range": "Avance ou Completo",
            "final_demo_line": "Quer que eu te mande a demonstracao?",
        },
        "ledger": state.diagnostic["ledger"] if state.diagnostic else [],
    }

    context = build_turn_context(
        turn_id="turn_1",
        request=_request("ok"),
        state=state,
        recent_events=[],
    )

    assert context.sales_inbox_inputs["diagnostic_status"] == "completed"
    assert context.sales_inbox_inputs["diagnostic_final_fields"] == {
        "final_plan_or_range": "Avance ou Completo",
        "final_demo_line": "Quer que eu te mande a demonstracao?",
    }


def test_context_builder_derives_completed_status_from_complete_ledger() -> None:
    state = _state()
    state.diagnostic = {
        "status": "offered",
        "ledger": [
            {
                "question_key": question_key,
                "status": "answered",
                "answer_value": f"answer:{question_key}",
                "evidence": [f"evidence:{question_key}"],
                "confidence": "high",
            }
            for question_key in (
                "active_students_or_size",
                "main_pain",
                "pain_detail",
                "current_process",
                "priority",
                "urgency",
            )
        ],
    }

    context = build_turn_context(
        turn_id="turn_1",
        request=_request("quero falar com alguem"),
        state=state,
        recent_events=[],
    )

    assert context.sales_inbox_inputs["diagnostic_status"] == "completed"


def test_context_builder_canonicalizes_stale_diagnostic_ledger_history() -> None:
    state = _state()
    state.diagnostic = {
        "status": "completed",
        "ledger": [
            {
                "question_key": "urgency",
                "status": "missing",
                "evidence": [],
                "confidence": "low",
            },
            {
                "question_key": "urgency",
                "status": "answered",
                "answer_value": "resolver agora",
                "evidence": ["resolver agora"],
                "confidence": "high",
            },
            {
                "question_key": "urgency",
                "status": "missing",
                "evidence": [],
                "confidence": "low",
            },
        ],
    }

    context = build_turn_context(
        turn_id="turn_1",
        request=_request("me manda a demo"),
        state=state,
        recent_events=[],
    )

    assert context.diagnostic_ledger == [
        {
            "question_key": "urgency",
            "status": "answered",
            "answer_value": "resolver agora",
            "evidence": ["resolver agora"],
            "confidence": "high",
        }
    ]


def test_context_builder_does_not_branch_on_commercial_message_text() -> None:
    state = _state()
    price_context = build_turn_context(
        turn_id="turn_price",
        request=_request("quanto custa?"),
        state=state,
        recent_events=[],
    )
    pain_context = build_turn_context(
        turn_id="turn_pain",
        request=_request("minha agenda esta baguncada"),
        state=state,
        recent_events=[],
    )

    assert price_context.compact_memory == pain_context.compact_memory
    assert price_context.diagnostic_ledger == pain_context.diagnostic_ledger
    assert price_context.waitlist_state == pain_context.waitlist_state
    assert price_context.demo_state == pain_context.demo_state
    assert price_context.handoff_state == pain_context.handoff_state
    assert price_context.product_knowledge == pain_context.product_knowledge
    assert price_context.product_knowledge
    assert price_context.inbound.text != pain_context.inbound.text
