from __future__ import annotations

from typing import Any

from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.schemas import ConductorDecision, TurnContext
from app.core.taliya_commercial.validators import validate_conductor_result
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState


def _request(text: str = "quero falar com alguem") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_validator_wdh_1",
                "lead_id": "lead_validator_wdh_1",
                "channel_conversation_id": "wa_validator_wdh_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_validator_wdh_1:1",
                "channel_message_id": "wamid_validator_wdh_1",
                "type": "text",
                "text": text,
            },
            "sender": {"name": "Ana", "whatsapp_phone": "+5511999999999"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _context(
    *,
    text: str = "quero falar com alguem",
    waitlist: dict[str, Any] | None = None,
    demo: dict[str, Any] | None = None,
    human_status: str = "none",
    human_reason: str | None = None,
) -> TurnContext:
    return build_turn_context(
        turn_id="turn_validator_wdh_1",
        request=_request(text),
        state=RuntimeState(
            conversation_id="conv_validator_wdh_1",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_product_agent",
            summary="Lead em fluxo comercial.",
            diagnostic={"status": "not_started", "ledger": []},
            waitlist=waitlist or {"status": "none"},
            demo=demo or {"status": "not_offered"},
            human_status=human_status,
            human_reason=human_reason,
        ),
        recent_events=[],
        product_knowledge_keys=["links", "prices", "plans"],
        spec006_contract_keys=["product_positioning"],
    )


def _waitlist_offer_template(value: str = "Lead pediu para entrar quando abrir.") -> dict[str, Any]:
    return {
        "template_id": "waitlist.offer_after_contract_intent",
        "variables": {
            "waitlist_context_summary": {
                "kind": "long_text",
                "value": value,
                "source": "runtime_state",
                "evidence": ["waitlist.eligibility"],
                "max_length": 220,
            }
        },
    }


def _demo_direct_template() -> dict[str, Any]:
    return {
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


def _decision_payload(
    context: TurnContext,
    *,
    route: str = "product",
    role: str = "product",
    current_state: str = "product_question",
    next_state: str = "product_question",
    waitlist: dict[str, Any] | None = None,
    demo: dict[str, Any] | None = None,
    handoff: dict[str, Any] | None = None,
    template_items: list[dict[str, Any]] | None = None,
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
        "detected_intents": ["product_question"],
        "direct_question_present": True,
        "direct_question_answered_first": True,
        "demo": demo or {"status": "not_offered", "next_step": "none"},
        "waitlist": waitlist or {"eligibility": "unknown", "status": "none"},
        "handoff": handoff or {"status": "none"},
        "language_policy": {
            "register": "studio_owner_practical",
            "crm_term_policy": "avoid_by_default",
        },
        "template_plan": {
            "items": template_items or [{"template_id": "product.overview_short"}]
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


def _issue_codes(result: Any) -> set[str]:
    return {issue.code for issue in result.errors}


def test_validator_blocks_waitlist_offer_without_structured_eligibility() -> None:
    context = _context()
    decision = _decision(
        context,
        route="waitlist",
        role="waitlist",
        current_state="waitlist_offered",
        next_state="waitlist_offered",
        waitlist={"eligibility": "unknown", "status": "offered"},
        template_items=[_waitlist_offer_template()],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "waitlist_requires_eligibility" in _issue_codes(result)


def test_validator_accepts_waitlist_offer_when_structurally_eligible() -> None:
    context = _context()
    decision = _decision(
        context,
        route="waitlist",
        role="waitlist",
        current_state="waitlist_eligible",
        next_state="waitlist_offered",
        waitlist={"eligibility": "eligible", "status": "offered"},
        template_items=[_waitlist_offer_template()],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "passed"
    assert result.errors == []


def test_validator_blocks_whatsapp_waitlist_contact_path_question() -> None:
    context = _context()
    decision = _decision(
        context,
        route="waitlist",
        role="waitlist",
        current_state="waitlist_pending_data",
        next_state="waitlist_pending_data",
        waitlist={
            "eligibility": "eligible",
            "status": "offered",
            "missing_details": ["studio_name", "city_state", "contact_path"],
        },
        template_items=[
            _waitlist_offer_template(),
            {"template_id": "waitlist.ask_missing_contact_path"},
        ],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "repairable"
    assert "waitlist_contact_path_not_needed_for_whatsapp" in _issue_codes(result)


def test_validator_blocks_waitlist_joined_with_missing_details() -> None:
    context = _context()
    decision = _decision(
        context,
        route="waitlist",
        role="waitlist",
        current_state="waitlist_pending_data",
        next_state="waitlist_joined",
        waitlist={
            "eligibility": "eligible",
            "status": "joined",
            "missing_details": ["studio_name"],
        },
        template_items=[{"template_id": "waitlist.joined"}],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "waitlist_joined_with_missing_details" in _issue_codes(result)


def test_validator_blocks_waitlist_from_demo_curiosity_without_contract_intent() -> None:
    context = _context(demo={"status": "viewed_or_asked"})
    decision = _decision(
        context,
        route="waitlist",
        role="waitlist",
        current_state="demo_reaction_pending",
        next_state="waitlist_offered",
        demo={"status": "viewed_or_asked", "next_step": "ask_demo_reaction"},
        waitlist={"eligibility": "unknown", "status": "offered"},
        template_items=[_waitlist_offer_template()],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "waitlist_demo_curiosity_without_contract_intent" in _issue_codes(result)


def test_validator_blocks_demo_offer_without_demo_template() -> None:
    context = _context(text="tem demo?")
    decision = _decision(
        context,
        route="product",
        role="product",
        current_state="demo_question",
        next_state="demo_offered",
        demo={"status": "offered", "next_step": "offer_demo"},
        template_items=[{"template_id": "product.overview_short"}],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "demo_offer_template_missing" in _issue_codes(result)


def test_validator_accepts_commercial_demo_offer_with_official_template() -> None:
    context = _context(text="tem demo?")
    decision = _decision(
        context,
        route="product",
        role="product",
        current_state="demo_question",
        next_state="demo_offered",
        demo={"status": "offered", "next_step": "offer_demo"},
        template_items=[_demo_direct_template()],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "passed"
    assert result.errors == []


def test_validator_blocks_handoff_requested_without_reason() -> None:
    context = _context()
    decision = _decision(
        context,
        route="handoff",
        role="handoff",
        current_state="human_requested",
        next_state="human_handoff",
        handoff={"status": "requested"},
        template_items=[{"template_id": "handoff.acknowledge"}],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "handoff_reason_missing" in _issue_codes(result)


def test_validator_accepts_handoff_request_with_acknowledge_template() -> None:
    context = _context()
    decision = _decision(
        context,
        route="handoff",
        role="handoff",
        current_state="human_requested",
        next_state="human_handoff",
        handoff={"status": "requested", "reason": "lead_requested_human"},
        template_items=[
            {
                "template_id": "handoff.acknowledge",
                "variables": {
                    "handoff_reason": {
                        "kind": "short_text",
                        "value": "lead_requested_human",
                        "source": "runtime_state",
                        "evidence": ["handoff.reason"],
                        "max_length": 120,
                    }
                },
            }
        ],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "passed"
    assert result.errors == []


def test_validator_blocks_human_active_context_with_normal_ai_delivery() -> None:
    context = _context(human_status="active", human_reason="operator took over")
    decision = _decision(
        context,
        route="product",
        role="product",
        current_state="product_question",
        next_state="product_question",
        template_items=[{"template_id": "product.overview_short"}],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "handoff_active_blocks_delivery" in _issue_codes(result)
