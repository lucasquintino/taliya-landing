from __future__ import annotations

import json

import pytest

from app.core.taliya_commercial.schemas import (
    ConductorDecision,
    DeliveryEvent,
    ModelUsage,
    RenderedMessage,
    RepairResult,
    SalesInboxProjection,
    TurnContext,
    ValidatorResult,
)
from app.core.taliya_commercial.trace_export import (
    TraceExportError,
    build_trace_eval_record,
    trace_eval_report_to_json,
    trace_eval_report_to_markdown,
)
from app.core.taliya_commercial.trace_store import build_turn_trace

_REPORT_KEYS = {
    "scenario_id",
    "status",
    "severity",
    "channel",
    "input_messages",
    "rendered_messages",
    "decision_json",
    "validator_results",
    "repair_attempts",
    "model_usage",
    "runtime_state",
    "sales_inbox_projection",
    "delivery_events",
    "trace_complete",
    "schema_version",
    "golden_transcript_diff",
    "assertions",
    "failure_reason",
    "artifact_paths",
}


def _context() -> TurnContext:
    return TurnContext.model_validate(
        {
            "turn_id": "turn_trace_export_1",
            "conversation_id": "conv_trace_export_1",
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "inbound": {
                "message_id": "msg_trace_export_1",
                "idempotency_key": "wa:conv_trace_export_1:1",
                "text": "quanto custa?",
            },
            "sales_inbox_inputs": {"lead_id": "lead_trace_export_1"},
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
                        "variables": {},
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


def _trace():
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
        runtime_state_diff={"current_state": "product_answered"},
        delivery_events=[
            DeliveryEvent(
                event="reserved",
                idempotency_key="outbox:turn_trace_export_1:1",
                status="planned",
            )
        ],
        sales_inbox_projection=SalesInboxProjection(
            conversation_id=context.conversation_id,
            lead_id="lead_trace_export_1",
            commercial_stage="product_answered",
            summary="Lead perguntou preco.",
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
        ),
    )


def test_trace_export_builds_eval_plan_record_and_stable_json() -> None:
    record = build_trace_eval_record(
        _trace(),
        scenario_id="price_direct",
        assertions=["direct_question_answered_first"],
        artifact_paths=["trace/price_direct.json"],
    )
    payload = json.loads(trace_eval_report_to_json([record]))

    assert set(record) == _REPORT_KEYS
    assert record["scenario_id"] == "price_direct"
    assert record["status"] == "PASS"
    assert record["channel"] == "whatsapp"
    assert record["input_messages"][0]["text"] == "quanto custa?"
    assert record["decision_json"]["route"] == "product"
    assert record["validator_results"][0]["status"] == "passed"
    assert record["repair_attempts"][0]["status"] == "not_needed"
    assert record["model_usage"]["input_tokens"] == 120
    assert record["runtime_state"]["current_state"] == "product_answered"
    assert record["sales_inbox_projection"]["commercial_stage"] == "product_answered"
    assert record["delivery_events"][0]["event"] == "reserved"
    assert record["trace_complete"] is True
    assert payload["schema_version"] == "011.eval_report.v1"
    assert payload["summary"]["scenario_count"] == 1
    assert payload["scenarios"][0] == record
    assert trace_eval_report_to_json([record]) == trace_eval_report_to_json([record])


def test_trace_export_markdown_contains_manual_review_sections() -> None:
    markdown = trace_eval_report_to_markdown(
        [build_trace_eval_record(_trace(), scenario_id="price_direct")]
    )

    assert "# Spec 011 Trace Eval Report" in markdown
    assert "## price_direct" in markdown
    assert "Trace complete: true" in markdown
    assert "Model usage: gpt-5.4-mini" in markdown
    assert "Sales Inbox stage: product_answered" in markdown


def test_trace_export_rejects_incomplete_trace_artifacts() -> None:
    incomplete_trace = _trace().model_copy(update={"rendered_messages": []})

    with pytest.raises(TraceExportError, match="rendered_messages"):
        build_trace_eval_record(incomplete_trace, scenario_id="missing_render")
