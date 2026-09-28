from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
PROJECTION_CASES = (
    REPO_ROOT
    / "specs/011-taliya-commercial-agent-core-reset/sales-inbox-projection-cases.json"
)
PROJECTION_DOC = (
    REPO_ROOT
    / "specs/011-taliya-commercial-agent-core-reset/sales-inbox-projection-cases.md"
)
REGRESSION_CASES_DOC = (
    REPO_ROOT / "specs/011-taliya-commercial-agent-core-reset/regression-cases.md"
)

REQUIRED_CASE_IDS = {
    "cold_greeting",
    "source_opening",
    "price_question",
    "plan_fit_question",
    "pain_first",
    "diagnostic_in_progress",
    "diagnostic_completed",
    "demo_offered",
    "demo_already_offered",
    "post_demo_reaction",
    "post_diagnostic_question",
    "direct_buying_intent",
    "waitlist_offered",
    "waitlist_accepted_missing_data",
    "waitlist_joined",
    "human_handoff",
    "paused_human_conversation",
    "duplicate_webhook",
    "invalid_json_fallback",
    "unsupported_media",
    "product_how_it_works",
    "post_diagnostic_followup",
    "comparison_current_tool",
    "whatsapp_integration_scope",
    "security_data",
    "out_of_profile",
    "diagnostic_refusal",
}

ALLOWED_STATUS = {"reuse", "reuse_with_validator", "missing"}
ALLOWED_REQUIREMENTS = {"required", "conditional", "optional", "forbidden"}
ALLOWED_SOURCES = {
    "channel_metadata",
    "delivery_outbox",
    "diagnostic_ledger",
    "none_forbidden",
    "official_product_knowledge",
    "operator_state",
    "spec_006_product_contract",
    "trace_store",
    "turn_gate",
    "validated_conductor_decision",
    "validated_runtime_state",
}


def _projection_cases() -> dict:
    return json.loads(PROJECTION_CASES.read_text(encoding="utf-8"))


def test_projection_cases_cover_sales_inbox_contract_families() -> None:
    data = _projection_cases()
    case_ids = {case["id"] for case in data["case_families"]}

    assert data["version"] == "011.0"
    assert REQUIRED_CASE_IDS - case_ids == set()
    assert "sales-inbox-contract.md" in data["source_contracts"]
    assert "regression-cases.md" in data["source_contracts"]


def test_projection_cases_reference_existing_regression_cases() -> None:
    data = _projection_cases()
    regression_text = REGRESSION_CASES_DOC.read_text(encoding="utf-8")

    referenced_ids = {
        regression_id
        for case in data["case_families"]
        for regression_id in case["regression_cases"]
    }

    missing_ids = {
        regression_id for regression_id in referenced_ids if regression_id not in regression_text
    }

    assert missing_ids == set()


def test_each_projection_case_maps_current_fields_to_truth_sources() -> None:
    data = _projection_cases()

    for case in data["case_families"]:
        fields = case["field_expectations"]
        statuses = {field["status"] for field in fields}

        assert case["regression_cases"], case["id"]
        assert fields, case["id"]
        assert statuses & {"reuse", "reuse_with_validator"}, case["id"]

        for field in fields:
            assert field["status"] in ALLOWED_STATUS, field
            assert field["requirement"] in ALLOWED_REQUIREMENTS, field
            assert field["source_of_truth"] in ALLOWED_SOURCES, field
            assert field["current_field"], field
            assert field["rule"], field
            if field["status"] == "missing":
                assert field.get("implementation_task"), field
            if field["requirement"] == "forbidden":
                assert field["source_of_truth"] == "none_forbidden", field


def test_projection_common_requirements_keep_trace_usage_and_inference_labels() -> None:
    data = _projection_cases()
    common_keys = {field["key"] for field in data["common_field_expectations"]}

    assert {
        "lead_identity",
        "conversation_state",
        "template_ids",
        "trace_id",
        "model_usage",
        "validator_status",
        "runtime_source_labels",
        "operator_next_action",
    } <= common_keys

    for field in data["common_field_expectations"]:
        assert field["status"] in ALLOWED_STATUS, field
        assert field["source_of_truth"] in ALLOWED_SOURCES, field
        assert field["current_field"], field


def test_projection_cases_protect_known_sales_inbox_regressions() -> None:
    data = _projection_cases()
    by_id = {case["id"]: case for case in data["case_families"]}

    price_rules = " ".join(field["rule"] for field in by_id["price_question"]["field_expectations"])
    assert "497" in price_rules
    assert "student" in price_rules

    diagnostic_keys = {
        field["key"] for field in by_id["diagnostic_completed"]["field_expectations"]
    }
    assert {
        "diagnostic_ledger_complete",
        "final_plan_or_range",
        "final_demo_line",
    } <= diagnostic_keys

    handoff_keys = {
        field["key"] for field in by_id["human_handoff"]["field_expectations"]
    }
    assert {"ai_paused", "human_active", "handoff_reason"} <= handoff_keys

    duplicate_rules = " ".join(
        field["rule"] for field in by_id["duplicate_webhook"]["field_expectations"]
    )
    assert "duplicate" in duplicate_rules
    assert "no new commercial state" in duplicate_rules


def test_projection_doc_explains_reuse_not_rewrite_policy() -> None:
    text = PROJECTION_DOC.read_text(encoding="utf-8").lower()

    required_phrases = [
        "t011-028",
        "reuse",
        "reuse_with_validator",
        "missing",
        "sales inbox is a projection",
        "not a second conversation brain",
        "current_field",
        "source_of_truth",
        "agentruntime",
        "qualificationdraft",
    ]

    for phrase in required_phrases:
        assert phrase in text
