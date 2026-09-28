from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.core.taliya_commercial.schemas import (
    ConductorDecision,
    DeliveryEvent,
    ModelUsage,
    RenderedMessage,
    RepairResult,
    SalesInboxProjection,
    TemplateVariableValue,
    TraceRecord,
    TurnContext,
    ValidatorResult,
)
from app.core.taliya_commercial.trace_store import (
    TraceFileStore,
    TracePersistenceError,
    build_turn_trace,
    trace_record_from_json,
    trace_record_to_json,
)


def _context() -> TurnContext:
    return TurnContext.model_validate(
        {
            "turn_id": "turn_trace_1",
            "conversation_id": "conv_trace_1",
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "inbound": {
                "message_id": "msg_trace_1",
                "idempotency_key": "wa:conv_trace_1:1",
                "text": "quanto custa?",
            },
            "sales_inbox_inputs": {"lead_id": "lead_trace_1"},
        }
    )


def _decision(context: TurnContext) -> ConductorDecision:
    return ConductorDecision.model_validate(
        {
            "schema_version": "011.0",
            "turn_id": context.turn_id,
            "conversation_id": context.conversation_id,
            "channel": context.channel,
            "agent_key": context.agent_key,
            "role": "product",
            "route": "product",
            "previous_state": "new_lead",
            "current_state": "product_question",
            "next_state": "product_answered",
            "detected_intents": ["price_question"],
            "direct_question_present": True,
            "direct_question_answered_first": True,
            "language_policy": {
                "register": "studio_owner_practical",
                "crm_term_policy": "avoid_by_default",
            },
            "template_plan": {
                "items": [
                    {
                        "template_id": "product.price_direct",
                        "variables": {
                            "plan_price_summary": {
                                "kind": "long_text",
                                "value": "Resumo oficial dos planos.",
                                "source": "official_product_knowledge",
                                "evidence": ["product_knowledge.prices"],
                                "max_length": 360,
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
            "confidence": "high",
        }
    )


def _projection(context: TurnContext, decision: ConductorDecision) -> SalesInboxProjection:
    return SalesInboxProjection(
        conversation_id=context.conversation_id,
        lead_id="lead_trace_1",
        commercial_stage=decision.next_state,
        summary="Lead perguntou preco e recebeu resumo oficial.",
        diagnostic_status="not_started",
        waitlist_status="none",
        handoff_status="none",
        fields={
            "template_ids": ["product.price_direct"],
            "validator_status": "passed",
            "validator_final_disposition": "accepted",
            "source_labels": ["official_product_knowledge"],
            "operator_next_action": "none",
        },
    )


def _trace() -> TraceRecord:
    context = _context()
    decision = _decision(context)
    validator_result = ValidatorResult(
        decision_id=decision.decision_id,
        status="passed",
        final_disposition="accepted",
    )
    return build_turn_trace(
        context=context,
        decision=decision,
        validator_result=validator_result,
        repair_result=RepairResult(),
        render_plan=decision.template_plan,
        rendered_messages=[
            RenderedMessage(
                text="Resumo oficial dos planos.",
                template_id="product.price_direct",
                channel="whatsapp",
                sequence=1,
            )
        ],
        model_usage=ModelUsage(
            model="gpt-5.4-mini",
            input_tokens=120,
            output_tokens=40,
            cost_usd=0.002,
        ),
        runtime_state_diff={"current_state": decision.next_state},
        delivery_events=[
            DeliveryEvent(
                event="reserved",
                idempotency_key="outbox:turn_trace_1:1",
                status="planned",
            )
        ],
        sales_inbox_projection=_projection(context, decision),
    )


def test_trace_store_persists_complete_replayable_turn_artifact(tmp_path: Path) -> None:
    trace = _trace()
    serialized = trace_record_to_json(trace)
    loaded = trace_record_from_json(serialized)
    store = TraceFileStore(tmp_path)

    saved_path = store.save(trace)
    reloaded = store.load(trace.trace_id)
    listed = store.list_for_conversation("conv_trace_1")

    assert serialized == trace_record_to_json(loaded)
    assert saved_path.exists()
    assert reloaded == trace
    assert [item.trace_id for item in listed] == [trace.trace_id]
    assert trace.input.inbound.message_id == "msg_trace_1"
    assert trace.decision.template_plan.items[0].variables["plan_price_summary"]
    assert trace.rendered_messages[0].template_id == "product.price_direct"
    assert trace.model_usage.input_tokens == 120
    assert trace.delivery_events[0].event == "reserved"
    assert trace.sales_inbox_projection.lead_id == "lead_trace_1"


def test_trace_json_contains_all_mandatory_artifact_keys() -> None:
    payload = json.loads(trace_record_to_json(_trace()))

    assert set(payload) >= {
        "trace_id",
        "turn_id",
        "input",
        "decision",
        "validator_result",
        "repair_result",
        "render_plan",
        "rendered_messages",
        "model_usage",
        "runtime_state_diff",
        "delivery_events",
        "sales_inbox_projection",
        "trace_complete",
    }


def test_trace_rejects_missing_rendered_messages_for_rendered_turn() -> None:
    context = _context()
    decision = _decision(context)

    with pytest.raises(TracePersistenceError, match="rendered_messages"):
        build_turn_trace(
            context=context,
            decision=decision,
            validator_result=ValidatorResult(
                decision_id=decision.decision_id,
                status="passed",
                final_disposition="accepted",
            ),
            repair_result=RepairResult(),
            render_plan=decision.template_plan,
            rendered_messages=[],
            model_usage=ModelUsage(
                model="gpt-5.4-mini",
                input_tokens=120,
                output_tokens=40,
                cost_usd=0.002,
            ),
            runtime_state_diff={},
            delivery_events=[
                DeliveryEvent(event="reserved", idempotency_key="outbox:1")
            ],
            sales_inbox_projection=_projection(context, decision),
        )


def test_trace_rejects_cross_turn_or_projection_mismatch() -> None:
    context = _context()
    decision = _decision(context).model_copy(update={"conversation_id": "other"})

    with pytest.raises(TracePersistenceError, match="conversation_id"):
        build_turn_trace(
            context=context,
            decision=decision,
            validator_result=ValidatorResult(
                decision_id=decision.decision_id,
                status="passed",
                final_disposition="accepted",
            ),
            repair_result=RepairResult(),
            render_plan=decision.template_plan,
            rendered_messages=[
                RenderedMessage(text="ok", template_id="product.price_direct")
            ],
            model_usage=ModelUsage(
                model="gpt-5.4-mini",
                input_tokens=120,
                output_tokens=40,
                cost_usd=0.002,
            ),
            runtime_state_diff={},
            delivery_events=[DeliveryEvent(event="reserved")],
            sales_inbox_projection=SalesInboxProjection(
                conversation_id="other",
                commercial_stage="product_answered",
                summary="Mismatch.",
                diagnostic_status="not_started",
                waitlist_status="none",
                handoff_status="none",
            ),
        )


def test_trace_schema_keeps_template_variables_typed_after_roundtrip() -> None:
    trace = trace_record_from_json(trace_record_to_json(_trace()))
    variable = trace.render_plan.items[0].variables["plan_price_summary"]

    assert isinstance(variable, TemplateVariableValue)
