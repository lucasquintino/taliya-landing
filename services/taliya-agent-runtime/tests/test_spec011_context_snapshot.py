from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.context_snapshot import (
    ContextSnapshotFileStore,
    build_context_snapshot,
    context_snapshot_from_json,
    context_snapshot_to_json,
    replay_turn_context,
)
from app.runtime.events import RuntimeEvent
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState


def _request() -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_snapshot_1",
                "lead_id": "lead_snapshot_1",
                "channel_conversation_id": "wa_snapshot_1",
                "source": "lead came from the site",
                "entry_intent": "Reliable profile first name",
            },
            "message": {
                "idempotency_key": "wa:conv_snapshot_1:1",
                "channel_message_id": "wamid_snapshot_1",
                "type": "text",
                "text": "Oi, tenho 120 alunos",
                "timestamp": "2026-05-30T12:00:00Z",
            },
            "sender": {
                "name": "Reliable profile first name: Ana",
                "whatsapp_phone": "+5511999999999",
                "email": "perfil@canal.example",
            },
            "metadata": {
                "page_path": "/pilates",
                "utm_source": "instagram",
                "runtime_control": {"ignored": True},
            },
        }
    )


def _state() -> RuntimeState:
    return RuntimeState(
        conversation_id="conv_snapshot_1",
        agent_key="taliya_commercial",
        current_agent_name="taliya_commercial_product_agent",
        input_items=[
            {"role": "user", "content": "Oi", "id": "m1"},
            {"role": "assistant", "content": "Oi, tudo bem?", "id": "a1"},
        ],
        summary="Lead quer organizar agenda e reposicoes.",
        lead_facts=[
            {
                "key": "first_name",
                "value": "Ana",
                "source": "memory",
                "reliability": "customer_provided",
                "confidence": "high",
                "evidence": ["message:m2"],
            },
            {
                "key": "first_name",
                "value": "Reliable profile first name: Ana",
                "source": "sales_inbox_projection",
                "reliability": "inferred",
                "confidence": "low",
                "evidence": ["sales_inbox:profile_name_guess"],
            },
        ],
        diagnostic={
            "status": "in_progress",
            "ledger": [
                {
                    "question_key": "active_students_or_size",
                    "status": "answered",
                    "answer_value": "120",
                    "evidence": ["message:m3"],
                    "confidence": "high",
                    "may_ask_again": False,
                }
            ],
        },
        demo={"status": "offered", "last_template_id": "demo.offer"},
        waitlist={"status": "none"},
        human_status="none",
    )


def _context():
    return build_turn_context(
        turn_id="turn_snapshot_1",
        request=_request(),
        state=_state(),
        recent_events=[
            RuntimeEvent(
                run_id="run_snapshot_1",
                conversation_id="conv_snapshot_1",
                agent_key="taliya_commercial",
                type="message",
                agent="taliya_commercial",
                content="Mensagem anterior",
                metadata={"role": "assistant", "template_id": "diagnostic.ask_active_students"},
                timestamp_ms=100,
            )
        ],
        product_knowledge_keys=["prices", "integration_calendar"],
        spec006_contract_keys=["product_positioning"],
    )


def _collect_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for item in value.values():
            keys.update(_collect_keys(item))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_collect_keys(item))
        return keys
    return set()


def test_context_snapshot_serializes_stable_json_and_replays_turn_context() -> None:
    context = _context()

    snapshot = build_context_snapshot(
        context,
        snapshot_id="snapshot_turn_1",
        created_at="2026-05-30T12:00:01Z",
    )
    serialized = context_snapshot_to_json(snapshot)
    loaded = context_snapshot_from_json(serialized)
    replayed_context = replay_turn_context(loaded)

    assert serialized == context_snapshot_to_json(loaded)
    assert replayed_context == context
    assert snapshot.customer_visible is False
    assert snapshot.purpose == "eval_debug"
    assert snapshot.context_schema_version == "011.0"
    assert snapshot.turn_id == "turn_snapshot_1"
    assert snapshot.conversation_id == "conv_snapshot_1"
    assert snapshot.channel == "whatsapp"


def test_context_snapshot_preserves_non_renderable_reliability_and_product_source_metadata(
) -> None:
    snapshot = build_context_snapshot(_context(), snapshot_id="snapshot_turn_2")
    payload = json.loads(context_snapshot_to_json(snapshot))
    context_payload = payload["context"]

    profile_fact = next(
        fact
        for fact in context_payload["facts"]
        if fact["key"] == "profile_name"
        and fact["value"] == "Reliable profile first name: Ana"
    )
    assert profile_fact["source"] == "channel_metadata"
    assert profile_fact["reliability"] == "channel_provided"
    assert profile_fact["renderable"] is False
    assert profile_fact["evidence"] == ["sender.name"]

    inferred_name = next(
        fact
        for fact in context_payload["facts"]
        if fact["key"] == "first_name"
        and fact["value"] == "Reliable profile first name: Ana"
    )
    assert inferred_name["source"] == "sales_inbox_projection"
    assert inferred_name["reliability"] == "inferred"
    assert inferred_name["confidence"] == "low"
    assert inferred_name["renderable"] is False

    missing_ref = next(
        ref
        for ref in context_payload["product_knowledge"]
        if ref["key"] == "integration_calendar"
    )
    assert missing_ref["source"] == "official_product_knowledge"
    assert missing_ref["missing"] is True
    assert missing_ref["renderable"] is False
    assert missing_ref["version"]
    assert missing_ref["evidence"] == ["product_knowledge.integration_calendar"]

    spec_ref = next(
        ref
        for ref in context_payload["product_knowledge"]
        if ref["key"] == "spec006.product_positioning"
    )
    assert spec_ref["source"] == "spec_006_product_contract"
    assert spec_ref["version"].startswith("spec006-")
    assert spec_ref["renderable"] is False


def test_context_snapshot_store_persists_replayable_eval_debug_artifact(tmp_path: Path) -> None:
    store = ContextSnapshotFileStore(tmp_path)
    snapshot = build_context_snapshot(_context(), snapshot_id="snapshot_turn_3")

    saved_path = store.save(snapshot)
    loaded = ContextSnapshotFileStore(tmp_path).load("snapshot_turn_3")
    listed = ContextSnapshotFileStore(tmp_path).list_for_conversation("conv_snapshot_1")

    assert saved_path.exists()
    assert loaded == snapshot
    assert replay_turn_context(loaded) == snapshot.context
    assert [item.snapshot_id for item in listed] == ["snapshot_turn_3"]


def test_context_snapshot_does_not_add_customer_output_or_commercial_decision_fields() -> None:
    snapshot = build_context_snapshot(_context(), snapshot_id="snapshot_turn_4")
    payload = json.loads(context_snapshot_to_json(snapshot))
    keys = _collect_keys(payload)

    assert payload["customer_visible"] is False
    assert "context" in payload
    assert not {
        "decision",
        "decision_id",
        "detected_intents",
        "model_usage",
        "render_plan",
        "rendered_messages",
        "repair_result",
        "route",
        "template_plan",
        "validator_result",
    }.intersection(keys)
