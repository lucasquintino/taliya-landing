from __future__ import annotations

from typing import Any

from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.schemas import ConductorDecision, TurnContext
from app.core.taliya_commercial.validators import validate_conductor_result
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState


def _request(text: str = "como funciona?") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_product_claims_1",
                "lead_id": "lead_product_claims_1",
                "channel_conversation_id": "wa_product_claims_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_product_claims_1:1",
                "channel_message_id": "wamid_product_claims_1",
                "type": "text",
                "text": text,
            },
            "sender": {"name": "Ana"},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _context(
    *,
    product_knowledge_keys: list[str] | None = None,
    spec006_contract_keys: list[str] | None = None,
) -> TurnContext:
    return build_turn_context(
        turn_id="turn_product_claims_1",
        request=_request(),
        state=RuntimeState(
            conversation_id="conv_product_claims_1",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_product_agent",
            summary="Lead quer entender produto.",
            diagnostic={"status": "not_started", "ledger": []},
            waitlist={"status": "none"},
            demo={"status": "not_offered"},
        ),
        recent_events=[],
        product_knowledge_keys=product_knowledge_keys
        or ["how_it_works", "unsupported_claims"],
        spec006_contract_keys=spec006_contract_keys or ["product_positioning"],
    )


def _product_summary_template(
    *,
    value: str,
    source: str = "official_product_knowledge",
    evidence: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "template_id": "product.overview_short",
        "variables": {
            "product_fact_summary": {
                "kind": "long_text",
                "value": value,
                "source": source,
                "evidence": evidence or ["product_knowledge.how_it_works"],
                "max_length": 320,
            }
        },
    }


def _decision_payload(
    context: TurnContext,
    *,
    template_item: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "011.0",
        "turn_id": context.turn_id,
        "conversation_id": context.conversation_id,
        "channel": context.channel,
        "agent_key": context.agent_key,
        "role": "product",
        "route": "product",
        "previous_state": "new_lead",
        "current_state": "product_question",
        "next_state": "product_question",
        "detected_intents": ["product_question"],
        "direct_question_present": True,
        "direct_question_answered_first": True,
        "language_policy": {
            "register": "studio_owner_practical",
            "crm_term_policy": "avoid_by_default",
        },
        "template_plan": {"items": [template_item]},
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


def test_validator_blocks_product_claim_variable_from_model_decision_source() -> None:
    context = _context()
    decision = _decision(
        context,
        template_item=_product_summary_template(
            value="Resumo inventado pelo modelo.",
            source="model_decision",
            evidence=["model.product_claim"],
        ),
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "product_claim_source_invalid" in _issue_codes(result)


def test_validator_blocks_officially_unsupported_product_claim() -> None:
    context = _context(product_knowledge_keys=["unsupported_claims", "how_it_works"])
    decision = _decision(
        context,
        template_item=_product_summary_template(
            value="A Taliya libera checkout para o studio.",
            evidence=["product_knowledge.unsupported_claims"],
        ),
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "unsupported_product_claim" in _issue_codes(result)


def test_validator_blocks_product_claim_with_missing_spec006_source() -> None:
    context = _context(spec006_contract_keys=["calendar_live_write"])
    decision = _decision(
        context,
        template_item=_product_summary_template(
            value="A Taliya escreve na agenda externa em tempo real.",
            source="spec_006_product_contract",
            evidence=["specs/006-crm-operational-core#calendar_live_write"],
        ),
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "blocked"
    assert "unresolved_product_evidence" in _issue_codes(result)
    assert "product_claim_source_missing" in _issue_codes(result)


def test_validator_accepts_product_claim_grounded_in_spec006_contract() -> None:
    context = _context(spec006_contract_keys=["product_positioning"])
    evidence = ["specs/006-crm-operational-core/spec.md#Product Positioning"]
    decision = _decision(
        context,
        template_item=_product_summary_template(
            value="A Taliya organiza a rotina comercial e operacional do studio.",
            source="spec_006_product_contract",
            evidence=evidence,
        ),
    )

    result = validate_conductor_result(decision, context)

    assert result.status == "passed"
    assert result.errors == []


def test_validator_blocks_integration_question_handoff_without_product_answer() -> None:
    context = _context(product_knowledge_keys=["integration_scope", "unsupported_claims"])
    payload = _decision_payload(
        context,
        template_item={"template_id": "handoff.acknowledge", "variables": {}},
    )
    payload.update(
        {
            "role": "handoff",
            "route": "handoff",
            "current_state": "handoff_requested",
            "next_state": "handoff_requested",
            "detected_intents": [
                "integration_question",
                "current_system_question",
                "instagram_integration_question",
            ],
            "direct_question_answered_first": False,
            "handoff": {
                "status": "requested",
                "reason": "confirmar integracao com Instagram e sistema atual",
            },
            "policy_checks": {
                **payload["policy_checks"],
                "direct_question_answered_first": False,
            },
        }
    )
    decision = ConductorDecision.model_validate(payload)

    result = validate_conductor_result(decision, context)

    assert result.status == "repairable"
    assert "integration_scope_handoff_without_product_answer" in _issue_codes(result)
