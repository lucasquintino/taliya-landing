from __future__ import annotations

from typing import Any

from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.schemas import (
    ConductorDecision,
    SalesInboxProjection,
    TurnContext,
)
from app.core.taliya_commercial.validators import validate_sales_inbox_projection
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState

_REQUIRED_DIAGNOSTIC_KEYS = (
    "active_students_or_size",
    "main_pain",
    "pain_detail",
    "current_process",
    "priority",
    "urgency",
)


def _request(text: str = "quero seguir") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_validator_sales_inbox_1",
                "lead_id": "lead_validator_sales_inbox_1",
                "channel_conversation_id": "wa_validator_sales_inbox_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_validator_sales_inbox_1:1",
                "channel_message_id": "wamid_validator_sales_inbox_1",
                "type": "text",
                "text": text,
            },
            "sender": {"name": "Ana"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _complete_ledger() -> list[dict[str, Any]]:
    return [
        {
            "question_key": question_key,
            "status": "answered",
            "answer_value": f"answer:{question_key}",
            "evidence": [f"user answered {question_key}"],
            "confidence": "high",
        }
        for question_key in _REQUIRED_DIAGNOSTIC_KEYS
    ]


def _context(
    *,
    diagnostic_status: str = "not_started",
    diagnostic_ledger: list[dict[str, Any]] | None = None,
    waitlist: dict[str, Any] | None = None,
    demo: dict[str, Any] | None = None,
    human_status: str = "none",
    human_reason: str | None = None,
) -> TurnContext:
    return build_turn_context(
        turn_id="turn_validator_sales_inbox_1",
        request=_request(),
        state=RuntimeState(
            conversation_id="conv_validator_sales_inbox_1",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_product_agent",
            summary="Lead em fluxo comercial.",
            diagnostic={
                "status": diagnostic_status,
                "ledger": diagnostic_ledger or [],
            },
            waitlist=waitlist or {"status": "none"},
            demo=demo or {"status": "not_offered"},
            human_status=human_status,
            human_reason=human_reason,
        ),
        recent_events=[],
        product_knowledge_keys=["links", "prices", "plans"],
        spec006_contract_keys=["product_positioning"],
    )


def _decision_payload(
    context: TurnContext,
    *,
    role: str = "product",
    route: str = "product",
    current_state: str = "product_question",
    next_state: str = "product_question",
    diagnostic: dict[str, Any] | None = None,
    demo: dict[str, Any] | None = None,
    waitlist: dict[str, Any] | None = None,
    handoff: dict[str, Any] | None = None,
    template_ids: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "011.0",
        "turn_id": context.turn_id,
        "conversation_id": context.conversation_id,
        "channel": context.channel,
        "agent_key": context.agent_key,
        "role": role,
        "route": route,
        "previous_state": "product_question",
        "current_state": current_state,
        "next_state": next_state,
        "detected_intents": ["commercial_followup"],
        "direct_question_present": False,
        "direct_question_answered_first": True,
        "diagnostic": diagnostic or {"action": "none"},
        "demo": demo or {"status": "not_offered", "next_step": "none"},
        "waitlist": waitlist or {"eligibility": "unknown", "status": "none"},
        "handoff": handoff or {"status": "none"},
        "language_policy": {
            "register": "studio_owner_practical",
            "crm_term_policy": "avoid_by_default",
        },
        "template_plan": {
            "items": [
                {"template_id": template_id, "variables": {}}
                for template_id in (template_ids or ["product.overview_short"])
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


def _decision(context: TurnContext, **overrides: Any) -> ConductorDecision:
    return ConductorDecision.model_validate(_decision_payload(context, **overrides))


def _common_fields(
    *,
    template_ids: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "template_ids": template_ids or ["product.overview_short"],
        "validator_status": "passed",
        "validator_final_disposition": "accepted",
        "source_labels": {
            "channel": "whatsapp",
            "source": "pilates_landing",
        },
        "operator_next_action": "acompanhar proximo passo comercial",
    }


def _projection(
    *,
    fields: dict[str, Any] | None = None,
    diagnostic_status: str = "not_started",
    waitlist_status: str = "none",
    handoff_status: str = "none",
    commercial_stage: str = "product_question",
    identity: list[dict[str, Any]] | None = None,
) -> SalesInboxProjection:
    return SalesInboxProjection.model_validate(
        {
            "conversation_id": "conv_validator_sales_inbox_1",
            "lead_id": "lead_validator_sales_inbox_1",
            "commercial_stage": commercial_stage,
            "summary": "Lead em fluxo comercial.",
            "diagnostic_status": diagnostic_status,
            "waitlist_status": waitlist_status,
            "handoff_status": handoff_status,
            "identity": identity or [],
            "fields": fields if fields is not None else _common_fields(),
        }
    )


def _issue_codes(result: Any) -> set[str]:
    return {issue.code for issue in result.errors}


def test_sales_inbox_validator_blocks_conversation_mismatch() -> None:
    context = _context()
    decision = _decision(context)
    projection = _projection().model_copy(update={"conversation_id": "conv_other"})

    result = validate_sales_inbox_projection(projection, decision, context)

    assert result.status == "blocked"
    assert "sales_inbox_conversation_mismatch" in _issue_codes(result)


def test_sales_inbox_validator_returns_issue_for_invalid_projection_payload() -> None:
    context = _context()
    decision = _decision(context)

    result = validate_sales_inbox_projection(
        {"conversation_id": context.conversation_id},
        decision,
        context,
    )

    assert result.status == "blocked"
    assert "sales_inbox_projection_schema_invalid" in _issue_codes(result)
    assert result.final_disposition == "blocked"


def test_sales_inbox_validator_blocks_missing_common_runtime_fields() -> None:
    context = _context()
    decision = _decision(context)
    projection = _projection(fields={})

    result = validate_sales_inbox_projection(projection, decision, context)

    assert result.status == "blocked"
    assert "sales_inbox_common_fields_missing" in _issue_codes(result)


def test_sales_inbox_validator_blocks_completed_diagnostic_without_required_fields() -> None:
    context = _context(
        diagnostic_status="completed",
        diagnostic_ledger=_complete_ledger(),
    )
    decision = _decision(
        context,
        role="diagnostic",
        route="diagnostic",
        current_state="diagnostic_ready",
        next_state="diagnostic_delivered",
        diagnostic={"action": "complete"},
        template_ids=["diagnostic.deliver_hold"],
    )
    projection = _projection(
        diagnostic_status="completed",
        commercial_stage="diagnostic_delivered",
        fields=_common_fields(template_ids=["diagnostic.deliver_hold"]),
    )

    result = validate_sales_inbox_projection(projection, decision, context)

    assert result.status == "blocked"
    assert "sales_inbox_diagnostic_fields_missing" in _issue_codes(result)


def test_sales_inbox_validator_accepts_completed_diagnostic_projection() -> None:
    context = _context(
        diagnostic_status="completed",
        diagnostic_ledger=_complete_ledger(),
    )
    decision = _decision(
        context,
        role="diagnostic",
        route="diagnostic",
        current_state="diagnostic_ready",
        next_state="diagnostic_delivered",
        diagnostic={"action": "complete"},
        template_ids=["diagnostic.deliver_hold"],
    )
    fields = _common_fields(template_ids=["diagnostic.deliver_hold"])
    fields.update(
        {
            "diagnostic_ledger_complete": True,
            "required_diagnostic_keys": list(_REQUIRED_DIAGNOSTIC_KEYS),
            "demo_status": "not_offered",
            "final_plan_or_range": "Essencial ou Avance",
            "final_demo_line": "quer ver a demonstracao?",
        }
    )
    projection = _projection(
        diagnostic_status="completed",
        commercial_stage="diagnostic_delivered",
        fields=fields,
    )

    result = validate_sales_inbox_projection(projection, decision, context)

    assert result.status == "passed"
    assert result.errors == []


def test_sales_inbox_validator_blocks_waitlist_pending_without_missing_details() -> None:
    context = _context()
    decision = _decision(
        context,
        role="waitlist",
        route="waitlist",
        current_state="waitlist_pending_data",
        next_state="waitlist_pending_data",
        waitlist={
            "eligibility": "eligible",
            "status": "pending_details",
            "missing_details": ["studio_name", "city_state"],
        },
    )
    projection = _projection(
        waitlist_status="pending_details",
        commercial_stage="waitlist_pending_data",
    )

    result = validate_sales_inbox_projection(projection, decision, context)

    assert result.status == "blocked"
    assert "sales_inbox_waitlist_fields_missing" in _issue_codes(result)


def test_sales_inbox_validator_blocks_waitlist_joined_without_idempotency_marker() -> None:
    context = _context()
    decision = _decision(
        context,
        role="waitlist",
        route="waitlist",
        current_state="waitlist_pending_data",
        next_state="waitlist_joined",
        waitlist={"eligibility": "eligible", "status": "joined"},
    )
    projection = _projection(
        waitlist_status="joined",
        commercial_stage="waitlist_joined",
    )

    result = validate_sales_inbox_projection(projection, decision, context)

    assert result.status == "blocked"
    assert "sales_inbox_waitlist_fields_missing" in _issue_codes(result)


def test_sales_inbox_validator_blocks_handoff_without_reason_and_pause_flags() -> None:
    context = _context()
    decision = _decision(
        context,
        role="handoff",
        route="handoff",
        current_state="human_requested",
        next_state="human_handoff",
        handoff={"status": "requested", "reason": "lead_requested_human"},
        template_ids=["handoff.acknowledge"],
    )
    projection = _projection(
        handoff_status="requested",
        commercial_stage="human_handoff",
        fields=_common_fields(template_ids=["handoff.acknowledge"]),
    )

    result = validate_sales_inbox_projection(projection, decision, context)

    assert result.status == "blocked"
    assert "sales_inbox_handoff_fields_missing" in _issue_codes(result)


def test_sales_inbox_validator_blocks_verified_channel_identity_promotion() -> None:
    context = _context()
    decision = _decision(context)
    projection = _projection(
        identity=[
            {
                "key": "person_name",
                "value": "Ana",
                "source": "channel_provided",
                "verified": True,
            }
        ]
    )

    result = validate_sales_inbox_projection(projection, decision, context)

    assert result.status == "blocked"
    assert "sales_inbox_identity_source_invalid" in _issue_codes(result)
