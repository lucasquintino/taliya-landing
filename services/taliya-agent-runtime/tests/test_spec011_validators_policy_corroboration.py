from __future__ import annotations

from typing import Any

from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.schemas import ConductorDecision, TurnContext
from app.core.taliya_commercial.validators import validate_conductor_result
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


def _request(text: str = "quanto custa?") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_policy_corroboration_1",
                "lead_id": "lead_policy_corroboration_1",
                "channel_conversation_id": "wa_policy_corroboration_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_policy_corroboration_1:1",
                "channel_message_id": "wamid_policy_corroboration_1",
                "type": "text",
                "text": text,
            },
            "sender": {"name": "Ana"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _ledger(status_by_key: dict[str, str]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for question_key in _REQUIRED_DIAGNOSTIC_KEYS:
        status = status_by_key.get(question_key, "missing")
        item: dict[str, Any] = {
            "question_key": question_key,
            "status": status,
            "confidence": "high" if status == "answered" else "low",
            "may_ask_again": status != "answered",
            "evidence": [],
        }
        if status == "answered":
            item["answer_value"] = f"answer:{question_key}"
            item["evidence"] = [f"user answered {question_key}"]
        items.append(item)
    return items


def _complete_ledger() -> list[dict[str, Any]]:
    return _ledger({key: "answered" for key in _REQUIRED_DIAGNOSTIC_KEYS})


def _context(
    *,
    text: str = "quanto custa?",
    diagnostic_status: str = "not_started",
    ledger: list[dict[str, Any]] | None = None,
) -> TurnContext:
    return build_turn_context(
        turn_id="turn_policy_corroboration_1",
        request=_request(text),
        state=RuntimeState(
            conversation_id="conv_policy_corroboration_1",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_product_agent",
            summary="Lead em conversa comercial.",
            diagnostic={"status": diagnostic_status, "ledger": ledger or []},
            waitlist={"status": "none"},
            demo={"status": "not_offered"},
        ),
        recent_events=[],
        product_knowledge_keys=["prices", "plans", "links"],
        spec006_contract_keys=["product_positioning"],
    )


def _price_template() -> dict[str, Any]:
    return {
        "template_id": "product.price_direct",
        "variables": {
            "plan_price_summary": {
                "kind": "long_text",
                "value": "Resumo dos planos vindo do conhecimento oficial.",
                "source": "official_product_knowledge",
                "evidence": ["product_knowledge.prices"],
                "max_length": 360,
            }
        },
    }


def _value(
    *,
    kind: str,
    value: str,
    source: str,
    evidence: list[str],
    max_length: int | None = None,
) -> dict[str, Any]:
    return {
        "kind": kind,
        "value": value,
        "source": source,
        "evidence": evidence,
        **({"max_length": max_length} if max_length is not None else {}),
    }


def _complete_diagnostic_delivery_templates() -> list[dict[str, Any]]:
    return [
        {"template_id": "diagnostic.deliver_hold"},
        {
            "template_id": "diagnostic.deliver_context",
            "variables": {
                "pain_context_human": _value(
                    kind="long_text",
                    value="O principal peso hoje e perder interessados no WhatsApp.",
                    source="diagnostic_ledger",
                    evidence=["user answered main_pain"],
                    max_length=320,
                )
            },
        },
        {
            "template_id": "diagnostic.deliver_crm_base",
            "variables": {
                "crm_base_recommendation": _value(
                    kind="long_text",
                    value="Antes dos agentes, eu organizaria contatos e retornos.",
                    source="diagnostic_ledger",
                    evidence=["user answered current_process"],
                    max_length=260,
                )
            },
        },
        {
            "template_id": "diagnostic.deliver_operational_step",
            "variables": {
                "operational_first_step": _value(
                    kind="long_text",
                    value="Separar novos interessados dos retornos pendentes.",
                    source="diagnostic_ledger",
                    evidence=["user answered priority"],
                    max_length=240,
                )
            },
        },
        {
            "template_id": "diagnostic.deliver_agent_recommendation",
            "variables": {
                "agent_name": _value(
                    kind="short_text",
                    value="Atendimento",
                    source="official_product_knowledge",
                    evidence=["product_knowledge.plans"],
                    max_length=60,
                ),
                "agent_pain_resolved": _value(
                    kind="long_text",
                    value="demora no retorno",
                    source="diagnostic_ledger",
                    evidence=["user answered main_pain"],
                    max_length=180,
                ),
                "agent_practical_action": _value(
                    kind="long_text",
                    value="organiza a fila e avisa a equipe quando precisa de humano",
                    source="spec_006_product_contract",
                    evidence=["specs/006-crm-operational-core/spec.md#Product Positioning"],
                    max_length=220,
                ),
            },
        },
        {
            "template_id": "diagnostic.deliver_plan_recommendation",
            "variables": {
                "recommended_plan_or_range": _value(
                    kind="short_text",
                    value="Avance",
                    source="official_product_knowledge",
                    evidence=["product_knowledge.plans"],
                    max_length=90,
                )
            },
        },
        {
            "template_id": "diagnostic.deliver_demo_not_offered",
            "variables": {
                "demo_status": _value(
                    kind="enum",
                    value="not_offered",
                    source="runtime_state",
                    evidence=["runtime_state.demo.status"],
                )
            },
        },
    ]


def _decision_payload(
    context: TurnContext,
    *,
    route: str = "product",
    role: str = "product",
    current_state: str = "product_question",
    next_state: str = "product_question",
    detected_intents: list[str] | None = None,
    direct_question_present: bool = True,
    direct_question_answered_first: bool = True,
    diagnostic: dict[str, Any] | None = None,
    template_items: list[dict[str, Any]] | None = None,
    policy_overrides: dict[str, bool] | None = None,
) -> dict[str, Any]:
    policy_checks = {
        "direct_question_answered_first": True,
        "diagnostic_timing_ok": True,
        "waitlist_timing_ok": True,
        "official_facts_only": True,
        "no_internal_text_leak": True,
        "no_early_contact_capture": True,
        "no_human_overlap": True,
    }
    if policy_overrides:
        policy_checks.update(policy_overrides)

    return {
        "schema_version": "011.0",
        "turn_id": context.turn_id,
        "conversation_id": context.conversation_id,
        "channel": context.channel,
        "agent_key": context.agent_key,
        "role": role,
        "route": route,
        "previous_state": "new_lead",
        "current_state": current_state,
        "next_state": next_state,
        "detected_intents": detected_intents or ["price_question"],
        "direct_question_present": direct_question_present,
        "direct_question_answered_first": direct_question_answered_first,
        "diagnostic": diagnostic or {"action": "none"},
        "language_policy": {
            "register": "studio_owner_practical",
            "crm_term_policy": "avoid_by_default",
        },
        "template_plan": {"items": template_items or [_price_template()]},
        "policy_checks": policy_checks,
        "confidence": "high",
    }


def _decision(context: TurnContext, **overrides: Any) -> ConductorDecision:
    return ConductorDecision.model_validate(_decision_payload(context, **overrides))


def _issue_codes(result: Any) -> set[str]:
    return {issue.code for issue in result.errors}


def test_validator_blocks_direct_question_self_check_without_decision_field() -> None:
    context = _context()
    decision = _decision(context, direct_question_answered_first=False)

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "direct_question_self_check_uncorroborated" in _issue_codes(result)


def test_validator_blocks_official_fact_self_check_without_official_fact_evidence() -> None:
    context = _context(text="como funciona?")
    decision = _decision(
        context,
        detected_intents=["product_how_it_works"],
        template_items=[{"template_id": "product.overview_short", "variables": {}}],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "official_facts_self_check_uncorroborated" in _issue_codes(result)


def test_validator_blocks_completed_diagnostic_self_check_without_required_ledger() -> None:
    context = _context(
        diagnostic_status="in_progress",
        ledger=_ledger(
            {
                "active_students_or_size": "answered",
                "main_pain": "answered",
                "pain_detail": "answered",
                "current_process": "answered",
                "priority": "answered",
                "urgency": "missing",
            }
        ),
    )
    decision = _decision(
        context,
        role="diagnostic",
        route="diagnostic",
        current_state="diagnostic_ready",
        next_state="diagnostic_delivered",
        diagnostic={"action": "complete"},
        template_items=[{"template_id": "diagnostic.deliver_hold"}],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "diagnostic_self_check_uncorroborated" in _issue_codes(result)
    assert "diagnostic_required_field_missing" in _issue_codes(result)


def test_validator_accepts_correlated_direct_product_answer() -> None:
    context = _context()
    decision = _decision(
        context,
        diagnostic={"action": "offer"},
        template_items=[_price_template(), {"template_id": "diagnostic.price_hook"}],
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "passed"
    assert result.errors == []


def test_validator_accepts_completed_diagnostic_with_correlated_ledger() -> None:
    context = _context(
        diagnostic_status="completed",
        ledger=_complete_ledger(),
    )
    decision = _decision(
        context,
        role="diagnostic",
        route="diagnostic",
        current_state="diagnostic_ready",
        next_state="diagnostic_delivered",
        direct_question_present=False,
        detected_intents=["diagnostic_complete"],
        diagnostic={"action": "complete"},
        template_items=_complete_diagnostic_delivery_templates(),
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "passed"
    assert result.errors == []
