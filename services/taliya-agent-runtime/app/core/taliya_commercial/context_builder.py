from __future__ import annotations

from typing import Any

from app.core.taliya_commercial.product_knowledge import (
    build_official_product_knowledge_refs,
    build_spec006_product_contract_refs,
)
from app.core.taliya_commercial.runtime_state import canonical_diagnostic_ledger
from app.core.taliya_commercial.schemas import (
    IDENTITY_CONTACT_FACT_KEYS,
    TurnContext,
    TurnFact,
)
from app.runtime.events import RuntimeEvent
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState

_ALLOWED_FACT_SOURCES = {
    "user_message",
    "channel_metadata",
    "operator",
    "memory",
    "sales_inbox_projection",
    "official_product_knowledge",
}

_ALLOWED_FACT_RELIABILITIES = {
    "customer_provided",
    "operator_provided",
    "channel_provided",
    "inferred",
    "unverified",
    "internal",
}

_DEFAULT_RELIABILITY_BY_SOURCE = {
    "user_message": "customer_provided",
    "channel_metadata": "channel_provided",
    "operator": "operator_provided",
    "memory": "customer_provided",
    "sales_inbox_projection": "unverified",
    "official_product_knowledge": "internal",
}
_REQUIRED_DIAGNOSTIC_KEYS = (
    "active_students_or_size",
    "main_pain",
    "pain_detail",
    "current_process",
    "priority",
    "urgency",
)
_COMPLETE_DIAGNOSTIC_STATUSES = {
    "answered",
    "inferred_from_prior_message",
    "not_applicable",
}


def build_turn_context(
    *,
    turn_id: str,
    request: AgentRunRequest,
    state: RuntimeState | None = None,
    recent_events: list[RuntimeEvent] | None = None,
    max_recent_transcript_items: int = 8,
    product_knowledge_keys: list[str] | None = None,
    spec006_contract_keys: list[str] | None = None,
) -> TurnContext:
    conversation_id = request.conversation.conversation_id
    events = recent_events or []

    return TurnContext(
        turn_id=turn_id,
        conversation_id=conversation_id,
        agent_key=request.agent_key,
        channel=request.channel,
        inbound={
            "message_id": request.message.channel_message_id or request.message.idempotency_key,
            "idempotency_key": request.message.idempotency_key,
            "text": request.message.text,
            "message_type": request.message.type,
            "timestamp": request.message.timestamp,
        },
        facts=_build_facts(request=request, state=state),
        product_knowledge=[
            *build_official_product_knowledge_refs(product_knowledge_keys),
            *build_spec006_product_contract_refs(spec006_contract_keys),
        ],
        compact_memory=_build_compact_memory(state),
        recent_transcript=_build_recent_transcript(
            state=state,
            events=events,
            max_items=max_recent_transcript_items,
        ),
        diagnostic_ledger=_build_diagnostic_ledger(state),
        waitlist_state=_plain_dict(state.waitlist if state else None),
        demo_state=_plain_dict(state.demo if state else None),
        handoff_state=_build_handoff_state(state),
        sales_inbox_inputs=_build_sales_inbox_inputs(request=request, state=state),
    )


def _build_facts(*, request: AgentRunRequest, state: RuntimeState | None) -> list[TurnFact]:
    facts: list[TurnFact] = []

    _append_fact(
        facts,
        key="source",
        value=request.conversation.source,
        source="channel_metadata",
        reliability="internal",
        evidence=["conversation.source"],
    )
    _append_fact(
        facts,
        key="entry_intent",
        value=request.conversation.entry_intent,
        source="channel_metadata",
        reliability="internal",
        evidence=["conversation.entry_intent"],
    )
    _append_fact(
        facts,
        key="channel_conversation_id",
        value=request.conversation.channel_conversation_id,
        source="channel_metadata",
        reliability="internal",
        evidence=["conversation.channel_conversation_id"],
    )
    _append_fact(
        facts,
        key="page_path",
        value=request.metadata.get("page_path"),
        source="channel_metadata",
        reliability="internal",
        evidence=["metadata.page_path"],
    )
    _append_fact(
        facts,
        key="utm_source",
        value=request.metadata.get("utm_source"),
        source="channel_metadata",
        reliability="internal",
        evidence=["metadata.utm_source"],
    )
    _append_fact(
        facts,
        key="profile_name",
        value=request.sender.name,
        source="channel_metadata",
        reliability="channel_provided",
        evidence=["sender.name"],
    )
    _append_fact(
        facts,
        key="whatsapp_phone",
        value=request.sender.whatsapp_phone,
        source="channel_metadata",
        reliability="channel_provided",
        evidence=["sender.whatsapp_phone"],
    )
    _append_fact(
        facts,
        key="email",
        value=request.sender.email,
        source="channel_metadata",
        reliability="channel_provided",
        evidence=["sender.email"],
    )

    if state:
        for fact in state.lead_facts:
            state_fact = _state_lead_fact_to_turn_fact(fact)
            if state_fact is not None:
                facts.append(state_fact)

    return facts


def _state_lead_fact_to_turn_fact(fact: dict[str, Any]) -> TurnFact | None:
    key = str(fact.get("key") or "memory_fact")
    value = fact.get("value")
    if value is None or value == "":
        return None

    evidence = [str(item) for item in fact.get("evidence") or []]
    source = _normalize_state_fact_source(fact)
    reliability = _normalize_state_fact_reliability(
        key=key,
        source=source,
        raw_reliability=fact.get("reliability"),
        evidence=evidence,
    )

    return TurnFact(
        key=key,
        value=value,
        source=source,
        reliability=reliability,
        renderable=False,
        confidence=_normalize_confidence(fact.get("confidence")),
        evidence=evidence,
    )


def _normalize_state_fact_source(fact: dict[str, Any]) -> str:
    raw_source = _clean_label(fact.get("source"))
    if raw_source in _ALLOWED_FACT_SOURCES:
        return raw_source

    raw_reliability = _clean_label(fact.get("reliability"))
    if raw_reliability == "operator_provided":
        return "operator"
    return "memory"


def _normalize_state_fact_reliability(
    *,
    key: str,
    source: str,
    raw_reliability: Any,
    evidence: list[str],
) -> str:
    reliability = _clean_label(raw_reliability)
    if reliability not in _ALLOWED_FACT_RELIABILITIES:
        reliability = _DEFAULT_RELIABILITY_BY_SOURCE[source]

    if source == "operator":
        reliability = "operator_provided"
    elif source == "sales_inbox_projection" and reliability in {
        "customer_provided",
        "operator_provided",
        "internal",
    }:
        reliability = "unverified"
    elif source == "channel_metadata" and reliability not in {
        "channel_provided",
        "internal",
    }:
        reliability = "channel_provided"
    elif source == "official_product_knowledge":
        reliability = "internal"

    if (
        key in IDENTITY_CONTACT_FACT_KEYS
        and reliability == "customer_provided"
        and not evidence
    ):
        return "unverified"

    return reliability


def _normalize_confidence(value: Any) -> str:
    confidence = _clean_label(value)
    return confidence if confidence in {"low", "medium", "high"} else "medium"


def _clean_label(value: Any) -> str:
    return str(value or "").strip()


def _append_fact(
    facts: list[TurnFact],
    *,
    key: str,
    value: Any,
    source: str,
    reliability: str,
    evidence: list[str],
) -> None:
    if value is None or value == "":
        return
    facts.append(
        TurnFact(
            key=key,
            value=value,
            source=source,
            reliability=reliability,
            renderable=False,
            evidence=evidence,
        )
    )


def _build_compact_memory(state: RuntimeState | None) -> list[dict[str, Any]]:
    if state is None:
        return []

    memory: list[dict[str, Any]] = []
    if state.summary:
        memory.append({"kind": "summary", "value": state.summary})
    return memory


def _build_recent_transcript(
    *,
    state: RuntimeState | None,
    events: list[RuntimeEvent],
    max_items: int,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    if state:
        for item in state.input_items:
            role = item.get("role")
            content = item.get("content")
            if role and content is not None:
                items.append(
                    {
                        "role": str(role),
                        "content": str(content),
                        "id": item.get("id"),
                        "source": "runtime_state",
                    }
                )

    for event in sorted(events, key=lambda item: item.timestamp_ms or 0):
        if event.type != "message":
            continue
        items.append(
            {
                "role": str(event.metadata.get("role") or event.agent),
                "content": event.content,
                "id": event.id,
                "template_id": event.metadata.get("template_id"),
                "source": "runtime_event",
            }
        )

    if max_items <= 0:
        return []
    return items[-max_items:]


def _build_diagnostic_ledger(state: RuntimeState | None) -> list[dict[str, Any]]:
    if state is None or not state.diagnostic:
        return []
    ledger = state.diagnostic.get("ledger")
    return canonical_diagnostic_ledger(ledger) if isinstance(ledger, list) else []


def _build_handoff_state(state: RuntimeState | None) -> dict[str, Any]:
    if state is None:
        return {"status": "none"}
    return {
        "status": state.human_status,
        "reason": state.human_reason,
    }


def _build_sales_inbox_inputs(
    *,
    request: AgentRunRequest,
    state: RuntimeState | None,
) -> dict[str, Any]:
    return {
        "lead_id": request.conversation.lead_id,
        "source": request.conversation.source,
        "entry_intent": request.conversation.entry_intent,
        "channel_conversation_id": request.conversation.channel_conversation_id,
        "human_status": state.human_status if state else "none",
        "diagnostic_status": _diagnostic_status_for_sales_inbox(state),
        "diagnostic_final_fields": _diagnostic_final_fields(state),
        "waitlist_status": (state.waitlist or {}).get("status") if state else None,
        "demo_status": (state.demo or {}).get("status") if state else None,
    }


def _diagnostic_status_for_sales_inbox(state: RuntimeState | None) -> str | None:
    if state is None or not isinstance(state.diagnostic, dict):
        return None

    raw_status = state.diagnostic.get("status")
    ledger = _build_diagnostic_ledger(state)
    ledger_status = _diagnostic_status_from_ledger(ledger)
    if raw_status == "completed" or ledger_status == "completed":
        return "completed"
    if ledger_status == "in_progress" and raw_status in {
        None,
        "",
        "not_started",
        "offered",
    }:
        return "in_progress"
    return str(raw_status) if raw_status else None


def _diagnostic_status_from_ledger(ledger: list[dict[str, Any]]) -> str | None:
    if not ledger:
        return None

    by_key = {
        str(item.get("question_key") or ""): str(item.get("status") or "")
        for item in ledger
        if isinstance(item, dict)
    }
    if all(
        by_key.get(question_key) in _COMPLETE_DIAGNOSTIC_STATUSES
        for question_key in _REQUIRED_DIAGNOSTIC_KEYS
    ):
        return "completed"
    if any(question_key in by_key for question_key in _REQUIRED_DIAGNOSTIC_KEYS):
        return "in_progress"
    return None


def _diagnostic_final_fields(state: RuntimeState | None) -> dict[str, Any]:
    if state is None or not isinstance(state.diagnostic, dict):
        return {}
    final_fields = state.diagnostic.get("final_fields")
    return dict(final_fields) if isinstance(final_fields, dict) else {}


def _plain_dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}
