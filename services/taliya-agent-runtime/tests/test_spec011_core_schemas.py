from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.core.taliya_commercial.schemas import (
    ConductorDecision,
    DiagnosticLedgerItem,
    ModelUsage,
    NumericInterpretation,
    RenderPlan,
    RenderPlanItem,
    RepairResult,
    SalesInboxProjection,
    TemplateVariableValue,
    TraceRecord,
    TurnContext,
    TurnFact,
    ValidatorResult,
)


def _minimal_context() -> TurnContext:
    return TurnContext.model_validate(
        {
            "turn_id": "turn_1",
            "conversation_id": "conv_1",
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "inbound": {
                "message_id": "msg_1",
                "idempotency_key": "wa:conv_1:1",
                "text": "Vi o plano de 497 e tenho 120 alunos",
            },
            "facts": [
                {
                    "key": "source",
                    "value": "lead came from the site",
                    "source": "channel_metadata",
                    "reliability": "internal",
                    "renderable": False,
                    "evidence": ["metadata.source"],
                }
            ],
            "product_knowledge": [
                {
                    "key": "plans",
                    "source": "official_product_knowledge",
                    "version": "taliya-commercial-2026-05-22",
                    "value": [{"id": "base"}],
                    "excerpt": '[{"id": "base"}]',
                    "evidence": ["product_knowledge.plans"],
                }
            ],
        }
    )


def test_turn_context_labels_internal_metadata_as_non_renderable():
    context = _minimal_context()

    assert context.facts[0].reliability == "internal"
    assert context.facts[0].renderable is False
    assert context.product_knowledge[0].source == "official_product_knowledge"

    with pytest.raises(ValidationError):
        TurnFact.model_validate(
            {
                "key": "source",
                "value": "lead came from the site",
                "source": "channel_metadata",
                "reliability": "internal",
                "renderable": True,
                "evidence": ["metadata.source"],
            }
        )


def test_conductor_decision_requires_schema_version_and_numeric_grounding():
    decision = ConductorDecision.model_validate(
        {
            "schema_version": "011.0",
            "turn_id": "turn_1",
            "conversation_id": "conv_1",
            "channel": "whatsapp",
            "agent_key": "taliya_commercial",
            "role": "product",
            "route": "product",
            "previous_state": "new_lead",
            "current_state": "product_question",
            "next_state": "product_question",
            "detected_intents": ["price_question", "student_count_fact"],
            "direct_question_present": True,
            "direct_question_answered_first": True,
            "language_policy": {
                "register": "studio_owner_practical",
                "crm_term_policy": "avoid_by_default",
            },
            "numeric_interpretations": [
                {
                    "raw_text": "497",
                    "kind": "plan_price",
                    "value": 497,
                    "currency": "BRL",
                    "evidence": ["Vi o plano de 497"],
                },
                {
                    "raw_text": "120",
                    "kind": "student_count",
                    "value": 120,
                    "evidence": ["tenho 120 alunos"],
                },
            ],
            "template_plan": {
                "items": [
                    {
                        "template_id": "product.price_direct",
                        "variables": {
                            "price_context": {
                                "kind": "short_text",
                                "value": "plano mencionado pelo lead",
                                "source": "user_message",
                                "evidence": ["Vi o plano de 497"],
                                "max_length": 80,
                            }
                        },
                    }
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
        }
    )

    assert [item.kind for item in decision.numeric_interpretations] == [
        "plan_price",
        "student_count",
    ]
    assert decision.template_plan.items[0].variables["price_context"].source == "user_message"


def test_conductor_decision_rejects_freeform_assistant_output_and_generic_variables():
    with pytest.raises(ValidationError):
        ConductorDecision.model_validate(
            {
                "schema_version": "011.0",
                "turn_id": "turn_1",
                "conversation_id": "conv_1",
                "channel": "widget",
                "agent_key": "taliya_commercial",
                "role": "product",
                "route": "product",
                "previous_state": "new_lead",
                "current_state": "product_question",
                "next_state": "product_question",
                "assistant_reply": "Hoje custa...",
                "template_plan": {"items": []},
            }
        )

    with pytest.raises(ValidationError):
        RenderPlan.model_validate(
            {
                "items": [
                    {
                        "template_id": "product.price_direct",
                        "variables": {
                            "message_text": {
                                "kind": "long_text",
                                "value": "resposta inteira escondida",
                                "source": "model_decision",
                                "evidence": ["none"],
                            }
                        },
                    }
                ]
            }
        )


def test_validator_repair_projection_and_trace_contracts_are_explicit():
    context = _minimal_context()
    decision = ConductorDecision.model_validate(
        {
            "schema_version": "011.0",
            "turn_id": "turn_1",
            "conversation_id": "conv_1",
            "channel": "whatsapp",
            "agent_key": "taliya_commercial",
            "role": "diagnostic",
            "route": "diagnostic",
            "previous_state": "diagnostic_in_progress",
            "current_state": "diagnostic_in_progress",
            "next_state": "diagnostic_in_progress",
            "language_policy": {
                "register": "studio_owner_practical",
                "crm_term_policy": "avoid_by_default",
            },
            "diagnostic": {
                "action": "ask_next",
                "ledger_updates": [
                    {
                        "question_key": "active_students_or_size",
                        "status": "answered",
                        "answer_value": "120",
                        "evidence": ["120"],
                        "confidence": "high",
                    }
                ],
                "next_question_key": "main_pain",
            },
            "template_plan": {
                "items": [
                    {
                        "template_id": "diagnostic.ask_main_pain",
                        "variables": {
                            "answer_feedback": {
                                "kind": "short_text",
                                "value": "Boa, esse tamanho ja ajuda.",
                                "source": "user_message",
                                "evidence": ["120"],
                                "max_length": 120,
                            }
                        },
                    }
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
        }
    )
    validator_result = ValidatorResult.model_validate(
        {
            "decision_id": decision.decision_id,
            "status": "repairable",
            "errors": [
                {
                    "code": "missing_urgency",
                    "severity": "P0",
                    "message": "Urgency is mandatory before final diagnostic.",
                    "path": "diagnostic.ledger",
                }
            ],
        }
    )
    repair = RepairResult.model_validate(
        {
            "attempted": True,
            "attempt_count": 1,
            "status": "repaired",
            "errors_sent": ["missing_urgency"],
        }
    )
    projection = SalesInboxProjection.model_validate(
        {
            "conversation_id": "conv_1",
            "lead_id": "lead_1",
            "commercial_stage": "diagnostic_in_progress",
            "summary": "Lead respondeu tamanho do studio.",
            "diagnostic_status": "in_progress",
            "waitlist_status": "none",
            "handoff_status": "none",
            "identity": [
                {
                    "key": "name",
                    "value": "Lucas",
                    "source": "channel_provided",
                    "verified": False,
                }
            ],
        }
    )
    trace = TraceRecord.model_validate(
        {
            "trace_id": "trace_1",
            "turn_id": "turn_1",
            "input": context,
            "decision": decision,
            "validator_result": validator_result,
            "repair_result": repair,
            "render_plan": decision.template_plan,
            "rendered_messages": [
                {"text": "Boa, esse tamanho ja ajuda.", "template_id": "diagnostic.ask_main_pain"}
            ],
            "model_usage": {
                "model": "gpt-5.4-mini",
                "input_tokens": 100,
                "output_tokens": 30,
                "cost_usd": 0.01,
            },
            "runtime_state_diff": {"diagnostic.status": "in_progress"},
            "delivery_events": [{"event": "reserved", "idempotency_key": "outbox:1"}],
            "sales_inbox_projection": projection,
        }
    )

    assert isinstance(decision.diagnostic.ledger_updates[0], DiagnosticLedgerItem)
    assert isinstance(decision.template_plan.items[0], RenderPlanItem)
    assert isinstance(
        decision.template_plan.items[0].variables["answer_feedback"],
        TemplateVariableValue,
    )
    assert isinstance(decision.numeric_interpretations, list)
    assert isinstance(
        NumericInterpretation(
            raw_text="120",
            kind="student_count",
            value=120,
            evidence=["120"],
        ),
        NumericInterpretation,
    )
    assert isinstance(trace.model_usage, ModelUsage)
    assert trace.validator_result.errors[0].code == "missing_urgency"
    assert trace.sales_inbox_projection.identity[0].source == "channel_provided"
