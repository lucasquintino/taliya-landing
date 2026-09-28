from __future__ import annotations

import re
import unicodedata
from typing import Any

from pydantic import ValidationError

from app.core.taliya_commercial.schema_versioning import (
    validate_conductor_schema_contract,
    validate_conductor_schema_version,
)
from app.core.taliya_commercial.schemas import (
    ConductorDecision,
    SalesInboxProjection,
    Severity,
    TurnContext,
    ValidationIssue,
    ValidatorResult,
)
from app.core.taliya_commercial.template_registry import (
    validate_render_plan_item_variables,
)
from app.domains.taliya_commercial.behavior_policy import assess_profile_name

_PRODUCT_SOURCES = {"official_product_knowledge", "spec_006_product_contract"}
_PRICE_VARIABLE_NAMES = {"plan_price_summary", "recommended_plan_or_range"}
_STUDENT_COUNT_FACT_KEYS = {
    "active_students",
    "active_students_or_size",
    "student_count",
    "studio_size",
}
_REQUIRED_DIAGNOSTIC_KEYS = (
    "active_students_or_size",
    "main_pain",
    "pain_detail",
    "current_process",
    "priority",
    "urgency",
)
_DIAGNOSTIC_COMPLETE_STATUSES = {
    "answered",
    "inferred_from_prior_message",
    "not_applicable",
}
_DIAGNOSTIC_EVIDENCE_STATUSES = {
    "answered",
    "inferred_from_prior_message",
    "not_applicable",
}
_DIAGNOSTIC_QUESTION_TEMPLATE_BY_KEY = {
    "active_students_or_size": "diagnostic.ask_active_students",
    "main_pain": "diagnostic.ask_main_pain",
    "pain_detail": "diagnostic.ask_pain_detail",
    "current_process": "diagnostic.ask_current_process",
    "priority": "diagnostic.ask_priority",
    "urgency": "diagnostic.ask_urgency",
}
_DIAGNOSTIC_KEY_BY_QUESTION_TEMPLATE = {
    template_id: question_key
    for question_key, template_id in _DIAGNOSTIC_QUESTION_TEMPLATE_BY_KEY.items()
}
_DIAGNOSTIC_QUESTION_TEMPLATE_IDS = frozenset(_DIAGNOSTIC_KEY_BY_QUESTION_TEMPLATE)
_ENTRY_DIAGNOSTIC_OFFER_TEMPLATE_IDS = {
    "opening.general_interest",
    "opening.instagram_source",
    "opening.site_cta",
    "opening.widget_empty_diagnostic",
}
_OPENING_TEMPLATE_IDS = {
    "opening.cold_greeting",
    "opening.cold_greeting_named",
    "opening.contextual_ack",
    "opening.general_interest",
    "opening.instagram_source",
    "opening.site_cta",
    "opening.widget_empty_diagnostic",
    "opening.diagnostic_cta",
}
_ACTIVE_WAITLIST_STATUSES = {"offered", "pending_details", "joined"}
_DEMO_CURIOSITY_STATUSES = {"viewed_or_asked", "reacted_positive"}
_DEMO_OFFER_TEMPLATE_IDS = {
    "product.demo_direct",
    "diagnostic.deliver_demo_not_offered",
}
_DEMO_REQUEST_INTENTS = {
    "demo_request",
    "demo_link_request",
    "product_demo_request",
    "commercial_demo_request",
    "demonstration_request",
    "send_demo_request",
}
_FINAL_DIAGNOSTIC_DEMO_TEMPLATE_IDS = {
    "diagnostic.deliver_demo_not_offered",
    "diagnostic.deliver_demo_already_offered",
}
_FINAL_DIAGNOSTIC_REQUIRED_PREFIX = (
    "diagnostic.deliver_hold",
    "diagnostic.deliver_context",
    "diagnostic.deliver_crm_base",
    "diagnostic.deliver_operational_step",
)
_FINAL_DIAGNOSTIC_PLAN_TEMPLATE_ID = "diagnostic.deliver_plan_recommendation"
_PRICE_HOOK_TEMPLATE_IDS = {
    "diagnostic.price_hook",
    "diagnostic.price_hook_with_context",
    "product.price_objection_value",
}
_PRICE_OBJECTION_TEMPLATE_ID = "product.price_objection_value"
_PRICE_ANSWER_TEMPLATE_IDS = {
    "product.price_direct",
    "product.price_complete_direct",
    "product.plan_direct",
    _PRICE_OBJECTION_TEMPLATE_ID,
}
_DIAGNOSTIC_OFFER_TEMPLATE_IDS = {
    "diagnostic.offer_soft",
    "diagnostic.price_hook",
    "diagnostic.price_hook_with_context",
    "product.plan_fit_with_diagnostic",
}
_HOW_IT_WORKS_TEMPLATE_ID = "product.how_it_works_direct"
_PLAN_FIT_DIRECT_ANSWER_TEMPLATE_IDS = {
    "product.plan_fit_with_diagnostic",
    "product.price_complete_direct",
    "product.plan_direct",
    "product.price_direct",
}
_PLAN_FIT_OWNER_COPY_TEMPLATE_IDS = {
    "product.plan_fit_with_diagnostic",
    "diagnostic.price_hook",
    "diagnostic.price_hook_with_context",
    "diagnostic.offer_soft",
}
_WHATSAPP_DIRECT_TEMPLATE_ID = "product.whatsapp_direct"
_WHATSAPP_REQUIRED_PHRASES = (
    "baixar aplicativo",
    "criar senha",
    "atualiza o painel",
    "avisa o respons",
)
_LEGACY_DIAGNOSTIC_DELIVER_TEMPLATE_ID = "diagnostic.deliver"
_HOW_IT_WORKS_REDUNDANT_FOLLOWUP_TEMPLATE_IDS = {
    "diagnostic.offer_soft",
    "diagnostic.price_hook",
    "diagnostic.ask_active_students",
    "diagnostic.ask_main_pain",
    "diagnostic.ask_current_process",
    "diagnostic.ask_pain_detail",
    "diagnostic.ask_priority",
    "diagnostic.ask_urgency",
}
_HANDOFF_ACTIVE_CONTEXT_STATUSES = {
    "active",
    "human_active",
    "human_handoff",
    "paused_by_human",
}
_INTERNAL_LEAK_PHRASES = (
    "reliable profile first name",
    "lead came from the site",
    "channel metadata",
    "channel_metadata",
    "schema_version",
    "trace_id",
    "validator result",
    "runtime_state",
    "product_knowledge.",
    "spec_006_product_contract",
)
_BANNED_CUSTOMER_PHRASES = (
    "pelo contexto, o principal gargalo parece",
    "para plano, eu compararia",
    "isso faz sentido para o momento do seu studio",
    "gargalo principal",
)
_ENGLISH_TRANSLATION_LEAK_PHRASES = (
    "lead loses",
    "interested leads",
    "team takes too long",
    "current routine",
    "pain point",
)
_BANNED_WAITLIST_PROMISE_PHRASES = (
    "checkout",
    "link de pagamento",
    "pagamento",
    "desconto",
    "vip",
    "pre-venda",
    "pre venda",
    "data de abertura",
    "garantia de resultado",
)
_SALES_INBOX_COMMON_REQUIRED_FIELDS = (
    "template_ids",
    "validator_status",
    "validator_final_disposition",
    "source_labels",
    "operator_next_action",
)
_VALIDATOR_STATUSES = {"passed", "repairable", "blocked", "failed"}
_VALIDATOR_FINAL_DISPOSITIONS = {"accepted", "repaired", "blocked", "fallback"}
_UNVERIFIED_IDENTITY_SOURCES = {"channel_provided", "inferred", "unverified"}
_OFFICIAL_FACT_INTENTS = {
    "price_question",
    "plan_question",
    "demo_request",
    "product_question",
    "product_how_it_works",
    "comparison_current_tool",
    "current_system_question",
    "instagram_integration_question",
    "integration_question",
    "integration_scope_question",
    "trust_security_question",
    "whatsapp_product_question",
}
_INTEGRATION_SCOPE_TEMPLATE_ID = "product.integration_scope_direct"
_INTEGRATION_SCOPE_INTENTS = {
    "current_system_question",
    "instagram_integration_question",
    "integration_question",
    "integration_scope",
    "integration_scope_question",
}
_HUMAN_HANDOFF_REQUEST_INTENTS = {
    "human_handoff_request",
    "human_request",
    "operator_request",
    "speak_to_human",
    "talk_to_human",
}
_OFFICIAL_STATIC_PRODUCT_TEMPLATE_IDS = {
    "product.how_it_works_direct",
    "product.integration_scope_direct",
    "product.price_objection_value",
    "product.security_data_direct",
}
_PRODUCT_CLAIM_VARIABLE_NAMES = {
    "agent_name",
    "official_demo_link",
    "plan_name",
    "plan_price_summary",
    "product_fact_summary",
    "recommended_plan_or_range",
}
_PURE_COLD_GREETINGS = {
    "oi",
    "ola",
    "bom dia",
    "boa tarde",
    "boa noite",
    "tudo bem",
    "oi tudo bem",
    "ola tudo bem",
}
_PAIN_FIRST_INTENTS = {
    "pain",
    "pain_first",
    "pain_point",
    "pain_report",
    "pain_statement",
    "pain_description",
    "whatsapp_followup_issue",
}


def validate_conductor_result(
    decision_or_result: ConductorDecision | Any,
    context: TurnContext,
) -> ValidatorResult:
    decision = _coerce_decision(decision_or_result)
    errors: list[ValidationIssue] = []
    errors.extend(_validate_schema_and_version(decision))
    errors.extend(_validate_context_identity(decision, context))
    errors.extend(_validate_state_fields(decision, context))
    errors.extend(_validate_template_plan(decision))
    errors.extend(_validate_channel_constraints(decision, context))
    errors.extend(_validate_pure_cold_greeting_boundary(decision, context))
    errors.extend(_validate_cold_greeting_profile_name(decision, context))
    errors.extend(_validate_widget_empty_opening_boundary(decision, context))
    errors.extend(_validate_entry_opening_consistency(decision))
    errors.extend(_validate_social_source_opening_template(decision))
    errors.extend(_validate_diagnostic_cta_opening(decision, context))
    errors.extend(_validate_product_grounding(decision, context))
    errors.extend(_validate_product_claims(decision, context))
    errors.extend(_validate_whatsapp_direct_answer(decision))
    errors.extend(_validate_price_question_followup(decision, context))
    errors.extend(_validate_price_objection_value_response(decision))
    errors.extend(_validate_diagnostic_refusal_respected(decision))
    errors.extend(_validate_plan_fit_direct_answer(decision))
    errors.extend(_validate_product_route_followup_shape(decision))
    errors.extend(_validate_integration_scope_template(decision))
    errors.extend(_validate_how_it_works_template(decision))
    errors.extend(_validate_numeric_grounding(decision, context))
    errors.extend(_validate_diagnostic_ledger(decision, context))
    errors.extend(_validate_diagnostic_question_feedback(decision))
    errors.extend(_validate_first_turn_diagnostic_greeting(decision, context))
    errors.extend(_validate_pain_first_offer_boundary(decision, context))
    errors.extend(_validate_waitlist_demo_handoff(decision, context))
    errors.extend(_validate_post_diagnostic_demo_request(decision, context))
    errors.extend(_validate_demo_direct_question_flags(decision))
    errors.extend(_validate_variable_text_safety(decision))
    errors.extend(_validate_policy_check_corroboration(decision, context))

    return ValidatorResult(
        decision_id=decision.decision_id,
        status=_status_for_errors(errors),
        errors=errors,
        repair_attempt_count=0,
        final_disposition=_final_disposition_for_errors(errors),
    )


def validate_sales_inbox_projection(
    projection_or_payload: SalesInboxProjection | Any,
    decision_or_result: ConductorDecision | Any,
    context: TurnContext,
) -> ValidatorResult:
    decision = _coerce_decision(decision_or_result)
    errors: list[ValidationIssue] = []
    try:
        projection = _coerce_sales_inbox_projection(projection_or_payload)
    except (TypeError, ValueError, ValidationError) as error:
        errors.append(
            _issue(
                code="sales_inbox_projection_schema_invalid",
                severity="P0",
                message=f"Sales Inbox projection payload is invalid: {error}",
                path="sales_inbox_projection",
            )
        )
        return ValidatorResult(
            decision_id=decision.decision_id,
            status=_status_for_errors(errors),
            errors=errors,
            repair_attempt_count=0,
            final_disposition=_final_disposition_for_errors(errors),
        )

    errors.extend(_validate_sales_inbox_identity(projection, decision, context))
    errors.extend(_validate_sales_inbox_common_fields(projection, decision, context))
    errors.extend(_validate_sales_inbox_diagnostic(projection, decision, context))
    errors.extend(_validate_sales_inbox_waitlist(projection, decision))
    errors.extend(_validate_sales_inbox_handoff(projection, decision, context))

    return ValidatorResult(
        decision_id=decision.decision_id,
        status=_status_for_errors(errors),
        errors=errors,
        repair_attempt_count=0,
        final_disposition=_final_disposition_for_errors(errors),
    )


def _coerce_decision(decision_or_result: ConductorDecision | Any) -> ConductorDecision:
    if isinstance(decision_or_result, ConductorDecision):
        return decision_or_result

    decision = getattr(decision_or_result, "decision", None)
    if isinstance(decision, ConductorDecision):
        return decision

    raise TypeError("validator requires ConductorDecision or result.decision")


def _coerce_sales_inbox_projection(
    projection_or_payload: SalesInboxProjection | Any,
) -> SalesInboxProjection:
    if isinstance(projection_or_payload, SalesInboxProjection):
        return projection_or_payload

    projection = getattr(projection_or_payload, "sales_inbox_projection", None)
    if isinstance(projection, SalesInboxProjection):
        return projection
    if isinstance(projection, dict):
        return SalesInboxProjection.model_validate(projection)

    if isinstance(projection_or_payload, dict):
        return SalesInboxProjection.model_validate(projection_or_payload)

    raise TypeError("validator requires SalesInboxProjection or projection payload")


def _validate_sales_inbox_identity(
    projection: SalesInboxProjection,
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    if projection.conversation_id != context.conversation_id:
        issues.append(
            _issue(
                code="sales_inbox_conversation_mismatch",
                severity="P0",
                message="Sales Inbox projection conversation_id does not match context",
                path="sales_inbox_projection.conversation_id",
            )
        )
    if projection.conversation_id != decision.conversation_id:
        issues.append(
            _issue(
                code="sales_inbox_conversation_mismatch",
                severity="P0",
                message="Sales Inbox projection conversation_id does not match decision",
                path="sales_inbox_projection.conversation_id",
            )
        )

    expected_lead_id = context.sales_inbox_inputs.get("lead_id")
    if expected_lead_id and projection.lead_id != expected_lead_id:
        issues.append(
            _issue(
                code="sales_inbox_lead_mismatch",
                severity="P0",
                message="Sales Inbox projection lead_id does not match context lead",
                path="sales_inbox_projection.lead_id",
            )
        )

    for index, identity in enumerate(projection.identity):
        if identity.verified and identity.source in _UNVERIFIED_IDENTITY_SOURCES:
            issues.append(
                _issue(
                    code="sales_inbox_identity_source_invalid",
                    severity="P0",
                    message=(
                        "Sales Inbox projection cannot mark channel/inferred "
                        "identity as verified"
                    ),
                    path=f"sales_inbox_projection.identity[{index}].verified",
                )
            )

    return issues


def _validate_sales_inbox_common_fields(
    projection: SalesInboxProjection,
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    fields = projection.fields

    if not projection.summary.strip():
        issues.append(
            _issue(
                code="sales_inbox_common_fields_missing",
                severity="P0",
                message="Sales Inbox projection requires a non-empty summary",
                path="sales_inbox_projection.summary",
            )
        )
    if not projection.commercial_stage.strip():
        issues.append(
            _issue(
                code="sales_inbox_common_fields_missing",
                severity="P0",
                message="Sales Inbox projection requires a non-empty commercial_stage",
                path="sales_inbox_projection.commercial_stage",
            )
        )

    missing = [
        field_name
        for field_name in _SALES_INBOX_COMMON_REQUIRED_FIELDS
        if _is_missing_projection_value(fields.get(field_name))
    ]
    if missing:
        issues.append(
            _issue(
                code="sales_inbox_common_fields_missing",
                severity="P0",
                message=(
                    "Sales Inbox projection missing common runtime fields: "
                    + ", ".join(missing)
                ),
                path="sales_inbox_projection.fields",
            )
        )

    if fields.get("validator_status") not in {None, *_VALIDATOR_STATUSES}:
        issues.append(
            _issue(
                code="sales_inbox_common_fields_invalid",
                severity="P0",
                message="Sales Inbox projection validator_status is not a known status",
                path="sales_inbox_projection.fields.validator_status",
            )
        )
    if fields.get("validator_final_disposition") not in {
        None,
        *_VALIDATOR_FINAL_DISPOSITIONS,
    }:
        issues.append(
            _issue(
                code="sales_inbox_common_fields_invalid",
                severity="P0",
                message=(
                    "Sales Inbox projection validator_final_disposition is not a "
                    "known disposition"
                ),
                path="sales_inbox_projection.fields.validator_final_disposition",
            )
        )

    expected_template_ids = _template_ids(decision)
    projected_template_ids = _projection_string_set(fields.get("template_ids"))
    if expected_template_ids and projected_template_ids != expected_template_ids:
        issues.append(
            _issue(
                code="sales_inbox_template_ids_mismatch",
                severity="P0",
                message="Sales Inbox template ids must match the validated render plan",
                path="sales_inbox_projection.fields.template_ids",
            )
        )

    if projection.commercial_stage not in {
        decision.current_state,
        decision.next_state,
    }:
        issues.append(
            _issue(
                code="sales_inbox_commercial_stage_mismatch",
                severity="P0",
                message="Sales Inbox commercial stage must come from validated state",
                path="sales_inbox_projection.commercial_stage",
            )
        )

    expected_waitlist = _expected_waitlist_status(decision, context)
    if expected_waitlist is not None and projection.waitlist_status != expected_waitlist:
        issues.append(
            _issue(
                code="sales_inbox_waitlist_status_mismatch",
                severity="P0",
                message="Sales Inbox waitlist status does not match decision/context",
                path="sales_inbox_projection.waitlist_status",
            )
        )

    expected_handoff = _expected_handoff_status(decision, context)
    if expected_handoff is not None and projection.handoff_status != expected_handoff:
        issues.append(
            _issue(
                code="sales_inbox_handoff_status_mismatch",
                severity="P0",
                message="Sales Inbox handoff status does not match decision/context",
                path="sales_inbox_projection.handoff_status",
            )
        )

    return issues


def _validate_sales_inbox_diagnostic(
    projection: SalesInboxProjection,
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    expected_status = _expected_diagnostic_status(decision, context)
    if expected_status is not None and projection.diagnostic_status != expected_status:
        issues.append(
            _issue(
                code="sales_inbox_diagnostic_status_mismatch",
                severity="P0",
                message="Sales Inbox diagnostic status does not match decision/context",
                path="sales_inbox_projection.diagnostic_status",
            )
        )

    if expected_status != "completed":
        return issues

    fields = projection.fields
    missing: list[str] = []
    if fields.get("diagnostic_ledger_complete") is not True:
        missing.append("diagnostic_ledger_complete")

    required_keys = _projection_string_set(fields.get("required_diagnostic_keys"))
    if not set(_REQUIRED_DIAGNOSTIC_KEYS).issubset(required_keys):
        missing.append("required_diagnostic_keys")

    for field_name in ("demo_status", "final_plan_or_range", "final_demo_line"):
        if _is_missing_projection_value(fields.get(field_name)):
            missing.append(field_name)

    if missing:
        issues.append(
            _issue(
                code="sales_inbox_diagnostic_fields_missing",
                severity="P0",
                message=(
                    "completed diagnostic projection missing required fields: "
                    + ", ".join(missing)
                ),
                path="sales_inbox_projection.fields",
            )
        )

    return issues


def _validate_sales_inbox_waitlist(
    projection: SalesInboxProjection,
    decision: ConductorDecision,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    status = decision.waitlist.status
    fields = projection.fields

    if status == "pending_details":
        projected_missing_details = _projection_string_set(
            fields.get("missing_waitlist_fields") or fields.get("missing_details")
        )
        expected_missing_details = set(decision.waitlist.missing_details)
        if (
            not expected_missing_details
            or not expected_missing_details.issubset(projected_missing_details)
        ):
            issues.append(
                _issue(
                    code="sales_inbox_waitlist_fields_missing",
                    severity="P0",
                    message=(
                        "pending waitlist projection requires exact missing details"
                    ),
                    path="sales_inbox_projection.fields.missing_waitlist_fields",
                )
            )

    if status == "joined":
        projected_missing_details = _projection_string_set(
            fields.get("missing_waitlist_fields") or fields.get("missing_details")
        )
        has_idempotency_marker = not _is_missing_projection_value(
            fields.get("waitlist_idempotency_key") or fields.get("idempotency_key")
        )
        has_joined_timestamp = not _is_missing_projection_value(
            fields.get("waitlist_joined_at") or fields.get("joined_at")
        )
        if projected_missing_details or not has_idempotency_marker or not has_joined_timestamp:
            issues.append(
                _issue(
                    code="sales_inbox_waitlist_fields_missing",
                    severity="P0",
                    message=(
                        "joined waitlist projection requires joined timestamp, "
                        "idempotency marker, and no missing details"
                    ),
                    path="sales_inbox_projection.fields",
                )
            )

    return issues


def _validate_sales_inbox_handoff(
    projection: SalesInboxProjection,
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    status = _expected_handoff_status(decision, context)
    if status not in {"requested", "active"}:
        return []

    fields = projection.fields
    expected_reason = decision.handoff.reason or context.handoff_state.get("reason")
    reason_value = fields.get("handoff_reason")
    if (
        _is_missing_projection_value(reason_value)
        or (expected_reason and reason_value != expected_reason)
        or fields.get("human_active") is not True
        or fields.get("ai_paused") is not True
    ):
        return [
            _issue(
                code="sales_inbox_handoff_fields_missing",
                severity="P0",
                message=(
                    "handoff projection requires reason, human_active, and ai_paused"
                ),
                path="sales_inbox_projection.fields",
            )
        ]

    return []


def _expected_diagnostic_status(
    decision: ConductorDecision,
    context: TurnContext,
) -> str | None:
    if decision.diagnostic.action == "complete" or _has_diagnostic_delivery_template(
        decision
    ):
        return "completed"
    if decision.diagnostic.action in {"start", "ask_next"}:
        return "in_progress"
    if decision.diagnostic.action == "offer":
        return "offered"
    if decision.diagnostic.action == "insufficient_evidence":
        return "insufficient_evidence"

    status = _contextual_diagnostic_status(context)
    if status is not None:
        return status
    return None


def _contextual_diagnostic_status(context: TurnContext) -> str | None:
    raw_status = context.sales_inbox_inputs.get("diagnostic_status")
    ledger_status = _diagnostic_status_from_context_ledger(context)
    if raw_status == "completed" or ledger_status == "completed":
        return "completed"
    if ledger_status == "in_progress" and raw_status in {
        None,
        "",
        "not_started",
        "offered",
    }:
        return "in_progress"
    if raw_status in {
        "not_started",
        "offered",
        "in_progress",
        "insufficient_evidence",
    }:
        return str(raw_status)
    return None


def _diagnostic_status_from_context_ledger(context: TurnContext) -> str | None:
    statuses = _context_diagnostic_statuses(context)
    if not statuses:
        return None
    if all(
        statuses.get(question_key) in _DIAGNOSTIC_COMPLETE_STATUSES
        for question_key in _REQUIRED_DIAGNOSTIC_KEYS
    ):
        return "completed"
    return "in_progress"


def _expected_waitlist_status(
    decision: ConductorDecision,
    context: TurnContext,
) -> str | None:
    if decision.waitlist.status != "none":
        return decision.waitlist.status

    status = context.sales_inbox_inputs.get("waitlist_status")
    if status in {"none", "offered", "pending_details", "joined", "declined"}:
        return str(status)
    return None


def _expected_handoff_status(
    decision: ConductorDecision,
    context: TurnContext,
) -> str | None:
    if decision.handoff.status != "none":
        return decision.handoff.status

    context_status = str(context.handoff_state.get("status") or "none")
    if context_status in _HANDOFF_ACTIVE_CONTEXT_STATUSES:
        return "active"
    if context_status == "resumed":
        return "resumed"
    return "none"


def _validate_schema_and_version(decision: ConductorDecision) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    schema_contract = validate_conductor_schema_contract()
    if schema_contract.status != "compatible":
        issues.extend(
            _issue(
                code="schema_fingerprint_mismatch",
                severity="P0",
                message=issue,
                path="schema_version",
            )
            for issue in schema_contract.issues
        )

    version_result = validate_conductor_schema_version(
        decision.model_dump(by_alias=True)
    )
    if version_result.status != "compatible":
        for issue in version_result.issues:
            code = issue.split(":", 1)[0]
            issues.append(
                _issue(
                    code=code,
                    severity="P0",
                    message=issue,
                    path="schema_version",
                )
            )

    return issues


def _validate_context_identity(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    comparable_fields = ("turn_id", "conversation_id", "agent_key", "channel")
    for field_name in comparable_fields:
        if getattr(decision, field_name) != getattr(context, field_name):
            issues.append(
                _issue(
                    code="context_field_mismatch",
                    severity="P0",
                    message=f"decision {field_name} does not match context",
                    path=field_name,
                )
            )
    return issues


def _validate_state_fields(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for field_name in ("previous_state", "current_state", "next_state"):
        value = getattr(decision, field_name)
        if not value.strip():
            issues.append(
                _issue(
                    code="invalid_state_field",
                    severity="P0",
                    message=f"decision {field_name} must be non-empty",
                    path=field_name,
                )
            )

    expected_previous_state = _context_previous_state(context)
    if expected_previous_state and decision.previous_state != expected_previous_state:
        issues.append(
            _issue(
                code="state_context_mismatch",
                severity="P0",
                message="decision previous_state does not match context state hint",
                path="previous_state",
            )
        )

    return issues


def _context_previous_state(context: TurnContext) -> str | None:
    for item in context.compact_memory:
        if not isinstance(item, dict):
            continue
        value = item.get("current_state") or item.get("previous_state")
        if isinstance(value, str) and value.strip():
            return value
    return None


def _context_fact_value(context: TurnContext, key: str) -> str | None:
    for fact in context.facts:
        if fact.key == key and fact.value is not None:
            value = str(fact.value).strip()
            return value or None
    return None


def _validate_template_plan(decision: ConductorDecision) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not decision.template_plan.items:
        return [
            _issue(
                code="template_plan_empty",
                severity="P1",
                message="template_plan requires at least one item before rendering",
                path="template_plan.items",
            )
        ]

    for index, item in enumerate(decision.template_plan.items):
        if _normalize_template_id(item.template_id) == _LEGACY_DIAGNOSTIC_DELIVER_TEMPLATE_ID:
            issues.append(
                _issue(
                    code="legacy_diagnostic_deliver_template_not_allowed",
                    severity="P1",
                    message=(
                        "completed diagnostics must use staged diagnostic.deliver_* "
                        "templates, not the legacy exact diagnostic.deliver template"
                    ),
                    path=f"template_plan.items[{index}].template_id",
                )
            )
        for registry_error in validate_render_plan_item_variables(item):
            issues.append(
                _issue(
                    code="template_plan_invalid",
                    severity="P1",
                    message=registry_error,
                    path=f"template_plan.items[{index}]",
                )
            )
    return issues


def _validate_channel_constraints(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for index, item in enumerate(decision.template_plan.items):
        if item.channel is not None and item.channel != context.channel:
            issues.append(
                _issue(
                    code="channel_mismatch",
                    severity="P0",
                    message="template item channel does not match context channel",
                    path=f"template_plan.items[{index}].channel",
                )
            )
    return issues


def _validate_pure_cold_greeting_boundary(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    if not _is_pure_cold_greeting_context(context):
        return []

    template_ids = _template_ids(decision)
    allowed_templates = {
        "opening.cold_greeting",
        "opening.cold_greeting_named",
    }
    if (
        decision.route == "entry"
        and decision.diagnostic.action == "none"
        and decision.waitlist.status == "none"
        and not (template_ids - allowed_templates)
    ):
        return []

    return [
        _issue(
            code="cold_greeting_must_stay_entry",
            severity="P1",
            message=(
                "pure cold greeting may only greet; it must not start diagnostic, "
                "product, waitlist, or commercial steering"
            ),
            path="route",
        )
    ]


def _validate_cold_greeting_profile_name(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    if not _is_pure_cold_greeting_context(context):
        return []

    template_ids = _template_ids(decision)
    if not template_ids.intersection({"opening.cold_greeting", "opening.cold_greeting_named"}):
        return []

    profile_name = _context_fact_value(context, "profile_name")
    assessment = assess_profile_name(profile_name)
    has_first_name_variable = any(
        "first_name" in item.variables for item in decision.template_plan.items
    )
    if assessment.status == "reliable" and not has_first_name_variable:
        return [
            _issue(
                code="cold_greeting_reliable_name_missing",
                severity="P1",
                message="cold greeting should use a reliable WhatsApp first name naturally",
                path="template_plan.items",
            )
        ]
    if assessment.status == "unreliable" and (
        "opening.cold_greeting_named" in template_ids or has_first_name_variable
    ):
        return [
            _issue(
                code="cold_greeting_unreliable_name_used",
                severity="P0",
                message="cold greeting must ignore unreliable business/profile names",
                path="template_plan.items",
            )
        ]
    return []


def _validate_widget_empty_opening_boundary(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    if not _is_widget_empty_opening_context(context):
        return []

    template_ids = _template_ids(decision)
    if (
        decision.route == "entry"
        and decision.diagnostic.action == "offer"
        and decision.waitlist.status == "none"
        and template_ids == {"opening.widget_empty_diagnostic"}
    ):
        return []

    return [
        _issue(
            code="widget_empty_must_use_opening_template",
            severity="P1",
            message=(
                "empty widget opening must use the approved widget diagnostic "
                "opening and must not be treated as a site/social CTA"
            ),
            path="template_plan.items",
        )
    ]


def _validate_entry_opening_consistency(
    decision: ConductorDecision,
) -> list[ValidationIssue]:
    template_ids = _template_ids(decision)
    if not template_ids.intersection(_ENTRY_DIAGNOSTIC_OFFER_TEMPLATE_IDS):
        return []
    if decision.route != "entry" or decision.waitlist.status != "none":
        return []
    if decision.diagnostic.action == "offer":
        return []
    return [
        _issue(
            code="entry_opening_diagnostic_offer_not_marked",
            severity="P1",
            message=(
                "entry opening templates that offer the free diagnostic must mark "
                "diagnostic.action=offer so state and Sales Inbox stay consistent"
            ),
            path="diagnostic.action",
        )
    ]


def _validate_social_source_opening_template(
    decision: ConductorDecision,
) -> list[ValidationIssue]:
    if decision.route != "entry":
        return []
    if "source_from_instagram" not in decision.detected_intents:
        return []
    if "opening.instagram_source" in _template_ids(decision):
        return []
    return [
        _issue(
            code="instagram_source_opening_template_missing",
            severity="P1",
            message=(
                "Instagram-source openings detected by the conductor must use "
                "the approved Instagram source opening template"
            ),
            path="template_plan.items",
        )
    ]


def _validate_diagnostic_cta_opening(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    if not _is_first_turn_context(context):
        return []
    entry_intent = _context_fact_value(context, "entry_intent")
    if entry_intent != "diagnostic_cta":
        return []
    if decision.route != "diagnostic":
        return []
    template_ids = _template_ids(decision)
    has_opening = "opening.diagnostic_cta" in template_ids
    has_question = bool(template_ids.intersection(_DIAGNOSTIC_QUESTION_TEMPLATE_IDS))
    if has_opening and "diagnostic.start" in template_ids:
        return [
            _issue(
                code="diagnostic_cta_duplicate_start_template",
                severity="P1",
                message="diagnostic CTA opening already owns the start copy",
                path="template_plan.items",
            )
        ]
    if has_opening and has_question:
        return []
    if has_opening and decision.diagnostic.action == "complete":
        return []
    return [
        _issue(
            code=(
                "diagnostic_cta_question_missing"
                if has_opening
                else "diagnostic_cta_opening_missing"
            ),
            severity="P1",
            message=(
                "diagnostic CTA turns must preserve the approved diagnostic "
                "opening before asking diagnostic questions"
            ),
            path="opening_type",
        )
    ]


def _validate_product_grounding(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    evidence_index = _product_evidence_index(context)
    official_links = _official_link_map(context)
    official_price_amounts = _official_price_amounts(context)
    official_plan_names = _official_plan_names(context)

    for item_index, item in enumerate(decision.template_plan.items):
        for variable_name, variable in item.variables.items():
            path = f"template_plan.items[{item_index}].variables.{variable_name}"

            if variable.source in _PRODUCT_SOURCES and not _evidence_resolves(
                evidence=variable.evidence,
                source=variable.source,
                evidence_index=evidence_index,
            ):
                issues.append(
                    _issue(
                        code="unresolved_product_evidence",
                        severity="P0",
                        message="official product variable evidence is not present in context",
                        path=path,
                    )
                )

            if (
                variable.kind == "url"
                and variable.source in _PRODUCT_SOURCES
                and official_links
                and str(variable.value) not in official_links.values()
            ):
                issues.append(
                    _issue(
                        code="official_link_mismatch",
                        severity="P0",
                        message="official link variable does not match product knowledge",
                        path=path,
                    )
                )

            if variable_name == "official_demo_link":
                expected_demo_link = official_links.get("demonstration")
                if expected_demo_link and variable.value != expected_demo_link:
                    issues.append(
                        _issue(
                            code="official_link_mismatch",
                            severity="P0",
                            message="demo link must match the official demonstration URL",
                            path=path,
                        )
                    )

            if variable_name in _PRICE_VARIABLE_NAMES and official_price_amounts:
                unsupported_amounts = sorted(
                    amount
                    for amount in _extract_int_tokens(variable.value)
                    if amount >= 100 and amount not in official_price_amounts
                )
                if unsupported_amounts:
                    issues.append(
                        _issue(
                            code="unsupported_price_value",
                            severity="P0",
                            message=(
                                "price variable includes value not found in official "
                                "product knowledge"
                            ),
                            path=path,
                        )
                    )

            if (
                variable_name == "plan_name"
                and official_plan_names
                and str(variable.value) not in official_plan_names
            ):
                issues.append(
                    _issue(
                        code="unknown_plan_name",
                        severity="P0",
                        message="plan name is not present in official product knowledge",
                        path=path,
                    )
                )

    return issues


def _validate_numeric_grounding(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    official_price_amounts = _official_price_amounts(context)
    student_count_facts = _student_count_fact_values(decision)

    for index, numeric in enumerate(decision.numeric_interpretations):
        path = f"numeric_interpretations[{index}]"
        value = _coerce_int(numeric.value)

        if numeric.kind == "plan_price":
            if value is None:
                issues.append(
                    _issue(
                        code="invalid_plan_price_value",
                        severity="P0",
                        message="plan_price numeric interpretation must be numeric",
                        path=path,
                    )
                )
                continue
            if not official_price_amounts:
                issues.append(
                    _issue(
                        code="official_price_source_missing",
                        severity="P0",
                        message="plan_price requires official price context",
                        path=path,
                    )
                )
            elif value not in official_price_amounts:
                issues.append(
                    _issue(
                        code="unknown_plan_price",
                        severity="P0",
                        message="plan_price value is not present in official product knowledge",
                        path=path,
                    )
                )
            if numeric.currency != "BRL":
                issues.append(
                    _issue(
                        code="plan_price_currency_missing",
                        severity="P0",
                        message="plan_price must use BRL currency",
                        path=path,
                    )
                )

        if numeric.kind == "student_count":
            if value is None:
                issues.append(
                    _issue(
                        code="invalid_student_count_value",
                        severity="P0",
                        message="student_count numeric interpretation must be numeric",
                        path=path,
                    )
                )
                continue
            if not _has_user_grounding_evidence(numeric.evidence):
                issues.append(
                    _issue(
                        code="student_count_evidence_not_user_grounded",
                        severity="P0",
                        message="student_count must be grounded in user/message evidence",
                        path=path,
                    )
                )
            if value in official_price_amounts and value not in student_count_facts:
                issues.append(
                    _issue(
                        code="student_count_matches_official_price",
                        severity="P0",
                        message=(
                            "student_count value collides with an official plan price "
                            "without user fact grounding"
                        ),
                        path=path,
                    )
                )

    return issues


def _validate_whatsapp_direct_answer(
    decision: ConductorDecision,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for index, item in enumerate(decision.template_plan.items):
        if _normalize_template_id(item.template_id) != _WHATSAPP_DIRECT_TEMPLATE_ID:
            continue
        if "official_demo_link" not in item.variables:
            issues.append(
                _issue(
                    code="whatsapp_direct_demo_link_missing",
                    severity="P1",
                    message="WhatsApp direct answer must include official demo link",
                    path=f"template_plan.items[{index}].variables.official_demo_link",
                )
            )
    return issues


def _validate_plan_fit_direct_answer(
    decision: ConductorDecision,
) -> list[ValidationIssue]:
    if not _is_plan_fit_direct_question(decision):
        return []

    template_ids = _template_ids(decision)
    if "product.plan_fit_with_diagnostic" not in template_ids:
        return [
            _issue(
                code="plan_fit_direct_answer_template_missing",
                severity="P1",
                message=(
                    "plan-fit direct questions must answer the fit/recommendation "
                    "before asking a diagnostic question"
                ),
                path="template_plan.items",
            )
        ]
    if (
        decision.diagnostic.action == "offer"
        and "product.plan_fit_with_diagnostic" not in template_ids
    ):
        return [
            _issue(
                code="plan_fit_owner_copy_template_missing",
                severity="P1",
                message=(
                    "plan-fit diagnostic offers must use approved owner-copy "
                    "phrases before steering"
                ),
                path="template_plan.items",
            )
        ]
    return []


def _validate_product_route_followup_shape(
    decision: ConductorDecision,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    template_ids = _template_ids(decision)

    if "product.demo_direct" in template_ids and decision.route != "product":
        issues.append(
            _issue(
                code="demo_direct_requires_product_route",
                severity="P1",
                message="demo direct answers must remain on product route",
                path="route",
            )
        )

    if (
        "product.plan_fit_with_diagnostic" in template_ids
        and "diagnostic.offer_soft" in template_ids
    ):
        issues.append(
            _issue(
                code="plan_fit_redundant_diagnostic_offer",
                severity="P1",
                message=(
                    "plan-fit owner copy already offers the diagnostic and must "
                    "not be duplicated by diagnostic.offer_soft"
                ),
                path="template_plan.items",
            )
        )

    offer_template_count = len(template_ids.intersection(_DIAGNOSTIC_OFFER_TEMPLATE_IDS))
    if offer_template_count > 1:
        issues.append(
            _issue(
                code="duplicate_diagnostic_offer_templates",
                severity="P1",
                message="a turn may render only one diagnostic offer template",
                path="template_plan.items",
            )
        )

    if decision.route == "product" and template_ids.intersection(
        _DIAGNOSTIC_QUESTION_TEMPLATE_IDS
    ):
        issues.append(
            _issue(
                code="product_route_must_not_ask_diagnostic_question",
                severity="P1",
                message=(
                    "product turns may offer the diagnostic after answering, but "
                    "must not ask a diagnostic question in the same turn"
                ),
                path="template_plan.items",
            )
        )

    if (
        decision.route == "product"
        and _has_price_intent({intent.lower() for intent in decision.detected_intents})
        and {
            "pain_description",
            "pain_statement",
            "diagnostic_interest",
        }.intersection(decision.detected_intents)
        and "diagnostic.price_hook_with_context" not in template_ids
    ):
        issues.append(
            _issue(
                code="price_plus_context_requires_context_hook",
                severity="P1",
                message=(
                    "price plus pain/context turns must preserve the lead context "
                    "inside diagnostic.price_hook_with_context"
                ),
                path="template_plan.items",
            )
        )

    return issues


def _is_plan_fit_direct_question(decision: ConductorDecision) -> bool:
    if not decision.direct_question_present or decision.route != "product":
        return False
    return bool(
        {
            "plan_recommendation",
            "price_fit_question",
            "pricing_fit",
            "plan_fit_question",
            "plan_question",
        }.intersection(decision.detected_intents)
    )


def _validate_product_claims(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    evidence_index = _product_evidence_index(context)
    unsupported_claims = _unsupported_product_claims(context)

    for item_index, item in enumerate(decision.template_plan.items):
        for variable_name, variable in item.variables.items():
            if variable_name not in _PRODUCT_CLAIM_VARIABLE_NAMES:
                continue

            path = f"template_plan.items[{item_index}].variables.{variable_name}"
            if variable.source not in _PRODUCT_SOURCES:
                issues.append(
                    _issue(
                        code="product_claim_source_invalid",
                        severity="P0",
                        message=(
                            "product claim variable must use official product "
                            "or Spec 006 source"
                        ),
                        path=path,
                    )
                )
                continue

            if not _evidence_resolves(
                evidence=variable.evidence,
                source=variable.source,
                evidence_index=evidence_index,
            ):
                issues.append(
                    _issue(
                        code="product_claim_source_missing",
                        severity="P0",
                        message="product claim variable evidence is missing from context",
                        path=path,
                    )
                )

            for text in _iter_text_values(variable.value):
                normalized_text = text.casefold()
                if any(claim in normalized_text for claim in unsupported_claims):
                    issues.append(
                        _issue(
                            code="unsupported_product_claim",
                            severity="P0",
                            message="product claim matches an unsupported official claim",
                            path=path,
                        )
                    )
                    break

    return issues


def _validate_diagnostic_ledger(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    diagnostic = decision.diagnostic
    status_by_key = _merged_diagnostic_statuses(decision, context)

    for index, update in enumerate(diagnostic.ledger_updates):
        if update.status in _DIAGNOSTIC_EVIDENCE_STATUSES:
            if not _has_user_grounding_evidence(update.evidence):
                issues.append(
                    _issue(
                        code="diagnostic_answer_evidence_missing",
                        severity="P0",
                        message="answered diagnostic ledger updates require evidence",
                        path=f"diagnostic.ledger_updates[{index}].evidence",
                    )
                )
            if update.status != "not_applicable" and not (
                update.answer_value or ""
            ).strip():
                issues.append(
                    _issue(
                        code="diagnostic_answer_value_missing",
                        severity="P0",
                        message="answered diagnostic ledger updates require answer_value",
                        path=f"diagnostic.ledger_updates[{index}].answer_value",
                    )
                )

    if diagnostic.action == "ask_next":
        issues.extend(_validate_diagnostic_no_repeat(decision, context))
        issues.extend(_validate_diagnostic_next_question(decision, status_by_key))
        issues.extend(
            _validate_diagnostic_urgency_priority(decision, context, status_by_key)
        )
        issues.extend(
            _validate_current_urgency_answer_captured(
                decision,
                context,
                status_by_key,
            )
        )
        issues.extend(
            _validate_diagnostic_inferable_pain_detail_before_final(
                decision,
                status_by_key,
            )
        )
    if diagnostic.action == "start":
        issues.extend(_validate_diagnostic_start_first_question(decision, status_by_key))
    if diagnostic.action not in {"ask_next", "start"}:
        issues.extend(_validate_diagnostic_first_missing_question(decision, status_by_key))

    if diagnostic.action == "complete" or _has_diagnostic_delivery_template(decision):
        for question_key in _REQUIRED_DIAGNOSTIC_KEYS:
            if status_by_key.get(question_key) not in _DIAGNOSTIC_COMPLETE_STATUSES:
                if (
                    question_key == "pain_detail"
                    and _only_missing_diagnostic_key(status_by_key, "pain_detail")
                ):
                    issues.append(
                        _issue(
                            code="diagnostic_inferable_pain_detail_should_complete",
                            severity="P1",
                            message=(
                                "when only pain_detail is missing after a rich "
                                "single-turn diagnostic, repair should infer it from "
                                "inbound/context evidence and complete the diagnostic"
                            ),
                            path="diagnostic.ledger.pain_detail",
                        )
                    )
                    continue
                issues.append(
                    _issue(
                        code="diagnostic_required_field_missing",
                        severity="P0",
                        message="diagnostic completion requires every mandatory field",
                        path=f"diagnostic.ledger.{question_key}",
                    )
                )

        issues.extend(
            _validate_diagnostic_urgency_priority(decision, context, status_by_key)
        )

        if not _template_ids(decision).intersection(_FINAL_DIAGNOSTIC_DEMO_TEMPLATE_IDS):
            issues.append(
                _issue(
                    code="diagnostic_final_demo_stage_missing",
                    severity="P1",
                    message=(
                        "completed diagnostic delivery must end with an approved "
                        "demo/next-step stage"
                    ),
                    path="template_plan.items",
                )
            )
        issues.extend(_validate_final_diagnostic_staged_order(decision))

    return issues


def _validate_final_diagnostic_staged_order(
    decision: ConductorDecision,
) -> list[ValidationIssue]:
    template_ids = [
        _normalize_template_id(item.template_id)
        for item in decision.template_plan.items
        if _normalize_template_id(item.template_id).startswith("diagnostic.deliver")
    ]
    if not template_ids:
        return []

    required_missing = [
        template_id
        for template_id in _FINAL_DIAGNOSTIC_REQUIRED_PREFIX
        if template_id not in template_ids
    ]
    if not any(
        template_id == "diagnostic.deliver_agent_recommendation"
        for template_id in template_ids
    ):
        required_missing.append("diagnostic.deliver_agent_recommendation")
    if _FINAL_DIAGNOSTIC_PLAN_TEMPLATE_ID not in template_ids:
        required_missing.append(_FINAL_DIAGNOSTIC_PLAN_TEMPLATE_ID)
    if not set(template_ids).intersection(_FINAL_DIAGNOSTIC_DEMO_TEMPLATE_IDS):
        required_missing.append("diagnostic.deliver_demo_*")

    expected_order = [
        *_FINAL_DIAGNOSTIC_REQUIRED_PREFIX,
        "diagnostic.deliver_agent_recommendation",
        _FINAL_DIAGNOSTIC_PLAN_TEMPLATE_ID,
    ]
    order_index = 0
    order_invalid = False
    for template_id in template_ids:
        if template_id in _FINAL_DIAGNOSTIC_DEMO_TEMPLATE_IDS:
            if template_id != template_ids[-1]:
                order_invalid = True
            continue
        if template_id == "diagnostic.deliver_agent_recommendation":
            if order_index < 4 or order_index >= 6:
                order_invalid = True
            order_index = max(order_index, 5)
            continue
        if template_id == _FINAL_DIAGNOSTIC_PLAN_TEMPLATE_ID:
            if order_index < 5:
                order_invalid = True
            order_index = max(order_index, 6)
            continue
        if template_id in expected_order:
            expected_position = expected_order.index(template_id)
            if expected_position < order_index:
                order_invalid = True
            order_index = max(order_index, expected_position + 1)

    if not required_missing and not order_invalid:
        return []
    return [
        _issue(
            code="diagnostic_final_staged_order_invalid",
            severity="P1",
            message=(
                "completed diagnostic delivery must use hold, context, base, "
                "operational step, agent recommendation, plan, and demo stages "
                "in order"
            ),
            path="template_plan.items",
        )
    ]


def _validate_diagnostic_start_first_question(
    decision: ConductorDecision,
    status_by_key: dict[str, str],
) -> list[ValidationIssue]:
    if status_by_key.get("active_students_or_size") in _DIAGNOSTIC_COMPLETE_STATUSES:
        return []
    if "diagnostic.ask_active_students" in _template_ids(decision):
        return []
    return [
        _issue(
            code="diagnostic_start_must_ask_active_students",
            severity="P1",
            message="diagnostic start must ask active_students_or_size first",
            path="template_plan.items",
        )
    ]


def _validate_diagnostic_first_missing_question(
    decision: ConductorDecision,
    status_by_key: dict[str, str],
) -> list[ValidationIssue]:
    if decision.route != "diagnostic":
        return []
    if "diagnostic.offer_soft" not in _template_ids(decision):
        return []
    if status_by_key.get("active_students_or_size") in _DIAGNOSTIC_COMPLETE_STATUSES:
        return []
    question_templates = _diagnostic_question_templates(decision)
    if not question_templates or "diagnostic.ask_active_students" in question_templates:
        return []
    return [
        _issue(
            code="diagnostic_start_must_ask_active_students",
            severity="P1",
            message="diagnostic first missing question must ask active_students_or_size",
            path="template_plan.items",
        )
    ]


def _validate_diagnostic_urgency_priority(
    decision: ConductorDecision,
    context: TurnContext,
    status_by_key: dict[str, str],
) -> list[ValidationIssue]:
    if status_by_key.get("priority") not in _DIAGNOSTIC_COMPLETE_STATUSES:
        return []
    if status_by_key.get("urgency") in _DIAGNOSTIC_COMPLETE_STATUSES:
        if _urgency_uses_priority_only_evidence(decision):
            return [
                _issue(
                    code="diagnostic_urgency_evidence_is_priority",
                    severity="P1",
                    message=(
                        "urgency cannot be completed from the priority answer alone; "
                        "ask the explicit urgency question"
                    ),
                    path="diagnostic.ledger.urgency",
                )
            ]
        if _urgency_uses_assistant_prompt_evidence(decision, context):
            return [
                _issue(
                    code="diagnostic_urgency_evidence_is_assistant_prompt",
                    severity="P1",
                    message=(
                        "urgency cannot be completed from the assistant's own "
                        "question; use current or prior lead evidence"
                    ),
                    path="diagnostic.ledger.urgency",
                )
            ]
        if not _urgency_has_timing_evidence(decision):
            return [
                _issue(
                    code="diagnostic_urgency_evidence_not_timing",
                    severity="P1",
                    message=(
                        "urgency requires explicit timing evidence from the lead, "
                        "not plan interest or priority alone"
                    ),
                    path="diagnostic.ledger.urgency",
                )
            ]
        return []
    if decision.diagnostic.next_question_key == "urgency":
        return []
    return [
        _issue(
            code="diagnostic_urgency_must_be_next",
            severity="P1",
            message="once priority is known, urgency must be the next diagnostic question",
            path="diagnostic.next_question_key",
        )
    ]


def _urgency_uses_priority_only_evidence(decision: ConductorDecision) -> bool:
    priority_update = _diagnostic_update(decision, "priority")
    urgency_update = _diagnostic_update(decision, "urgency")
    if priority_update is None or urgency_update is None:
        return False
    if urgency_update.status not in _DIAGNOSTIC_COMPLETE_STATUSES:
        return False
    urgency_answer = " ".join((urgency_update.answer_value or "").lower().split())
    urgency_evidence = {
        " ".join(str(value).lower().split()) for value in urgency_update.evidence
    }
    priority_evidence = {
        " ".join(str(value).lower().split()) for value in priority_update.evidence
    }
    if not urgency_evidence.intersection(priority_evidence):
        return False
    if urgency_answer in {"agora", "agora mesmo", "imediato", "imediata"}:
        return True
    return any("prioridade" in evidence for evidence in urgency_evidence)


def _urgency_uses_assistant_prompt_evidence(
    decision: ConductorDecision,
    context: TurnContext,
) -> bool:
    urgency_update = _diagnostic_update(decision, "urgency")
    if urgency_update is None:
        return False
    if urgency_update.status not in _DIAGNOSTIC_COMPLETE_STATUSES:
        return False

    user_texts = _normalized_context_texts(context, role="user")
    assistant_texts = _normalized_context_texts(context, role="assistant")
    if not assistant_texts:
        return False

    for item in urgency_update.evidence:
        evidence = _normalize_customer_text(str(item))
        if not evidence:
            continue
        if _evidence_is_grounded_in_texts(evidence, user_texts):
            continue
        if _evidence_is_grounded_in_texts(evidence, assistant_texts):
            return True
    return False


def _normalized_context_texts(
    context: TurnContext,
    *,
    role: str,
) -> list[str]:
    texts: list[str] = []
    if role == "user":
        inbound = _normalize_customer_text(context.inbound.text)
        if inbound:
            texts.append(inbound)

    for item in context.recent_transcript:
        item_role = str(item.get("role") or "").strip().casefold()
        if role == "user":
            if item_role not in {"user", "lead", "customer"}:
                continue
        else:
            if item_role in {"user", "lead", "customer"}:
                continue
            if item_role not in {"assistant", "agent", "taliya_commercial"}:
                continue

        content = _normalize_customer_text(str(item.get("content") or ""))
        if content:
            texts.append(content)
    return texts


def _evidence_is_grounded_in_texts(evidence: str, texts: list[str]) -> bool:
    return any(evidence in text or text in evidence for text in texts)


def _urgency_has_timing_evidence(decision: ConductorDecision) -> bool:
    urgency_update = _diagnostic_update(decision, "urgency")
    if urgency_update is None:
        return True
    evidence_text = " ".join(str(value).lower() for value in urgency_update.evidence)
    return _text_has_urgency_timing_evidence(evidence_text)


def _text_has_urgency_timing_evidence(value: str | None) -> bool:
    evidence_text = str(value or "").lower()
    timing_markers = {
        "urgente",
        "urgencia",
        "urgência",
        "esse mes",
        "este mes",
        "mês",
        "mes",
        "semana",
        "resolver hoje",
        "comecar hoje",
        "começar hoje",
        "hoje mesmo",
        "amanha",
        "amanhã",
        "agora",
        "imediato",
        "imediata",
        "quanto antes",
        "curto prazo",
        "sem pressa",
        "prazo",
        "dias",
        "pra ontem",
        "proximo",
        "próximo",
    }
    return any(marker in evidence_text for marker in timing_markers)


def _validate_current_urgency_answer_captured(
    decision: ConductorDecision,
    context: TurnContext,
    status_by_key: dict[str, str],
) -> list[ValidationIssue]:
    if decision.diagnostic.next_question_key != "urgency":
        return []
    if status_by_key.get("urgency") in _DIAGNOSTIC_COMPLETE_STATUSES:
        return []
    if not _only_missing_diagnostic_key(status_by_key, "urgency"):
        return []
    if not _text_has_urgency_timing_evidence(context.inbound.text):
        return []
    return [
        _issue(
            code="diagnostic_urgency_answer_not_captured",
            severity="P1",
            message=(
                "current inbound appears to answer the pending urgency question; "
                "do not ask urgency again without capturing it"
            ),
            path="diagnostic.next_question_key",
        )
    ]


def _diagnostic_update(
    decision: ConductorDecision,
    question_key: str,
) -> Any | None:
    for update in decision.diagnostic.ledger_updates:
        if update.question_key == question_key:
            return update
    return None


def _validate_diagnostic_inferable_pain_detail_before_final(
    decision: ConductorDecision,
    status_by_key: dict[str, str],
) -> list[ValidationIssue]:
    if decision.diagnostic.next_question_key != "pain_detail":
        return []
    if not _only_missing_diagnostic_key(status_by_key, "pain_detail"):
        return []
    return [
        _issue(
            code="diagnostic_inferable_pain_detail_should_complete",
            severity="P1",
            message=(
                "when only pain_detail is missing after a rich single-turn "
                "diagnostic, repair should infer it from inbound/context "
                "evidence and complete the diagnostic"
            ),
            path="diagnostic.ledger.pain_detail",
        )
    ]


def _only_missing_diagnostic_key(
    status_by_key: dict[str, str],
    missing_key: str,
) -> bool:
    for question_key in _REQUIRED_DIAGNOSTIC_KEYS:
        status = status_by_key.get(question_key)
        if question_key == missing_key:
            if status in _DIAGNOSTIC_COMPLETE_STATUSES:
                return False
            continue
        if status not in _DIAGNOSTIC_COMPLETE_STATUSES:
            return False
    return True


def _validate_waitlist_demo_handoff(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(_validate_waitlist(decision, context))
    issues.extend(_validate_waitlist_channel_missing_details(decision, context))
    issues.extend(_validate_demo(decision, context))
    issues.extend(_validate_handoff(decision, context))
    return issues


def _validate_variable_text_safety(decision: ConductorDecision) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for item_index, item in enumerate(decision.template_plan.items):
        template_id = _normalize_template_id(item.template_id)
        for variable_name, variable in item.variables.items():
            path = f"template_plan.items[{item_index}].variables.{variable_name}"
            for text in _iter_text_values(variable.value):
                normalized_text = text.casefold()
                if _contains_phrase(normalized_text, _INTERNAL_LEAK_PHRASES):
                    issues.append(
                        _issue(
                            code="internal_text_leak",
                            severity="P0",
                            message="template variable contains internal/source text",
                            path=path,
                        )
                    )
                    break
                if _contains_phrase(normalized_text, _BANNED_CUSTOMER_PHRASES):
                    issues.append(
                        _issue(
                            code="banned_customer_phrase",
                            severity="P0",
                            message="template variable contains banned customer phrase",
                            path=path,
                        )
                    )
                    break
                if variable_name == "answer_feedback" and _contains_phrase(
                    normalized_text,
                    _ENGLISH_TRANSLATION_LEAK_PHRASES,
                ):
                    issues.append(
                        _issue(
                            code="diagnostic_feedback_language_leak",
                            severity="P1",
                            message=(
                                "diagnostic answer feedback contains English "
                                "translation-like wording"
                            ),
                            path=path,
                        )
                    )
                    break
                if template_id.startswith("waitlist.") and _contains_phrase(
                    normalized_text,
                    _BANNED_WAITLIST_PROMISE_PHRASES,
                ):
                    issues.append(
                        _issue(
                            code="banned_waitlist_promise",
                            severity="P0",
                            message="waitlist variable contains forbidden promise language",
                            path=path,
                        )
                    )
                    break
    return issues


def _validate_policy_check_corroboration(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    policy_checks = decision.policy_checks

    if (
        decision.direct_question_present
        and policy_checks.direct_question_answered_first
        and not decision.direct_question_answered_first
    ):
        issues.append(
            _issue(
                code="direct_question_self_check_uncorroborated",
                severity="P0",
                message=(
                    "direct-question self-check is true but decision field does "
                    "not corroborate it"
                ),
                path="policy_checks.direct_question_answered_first",
            )
        )

    if (
        policy_checks.official_facts_only
        and _requires_official_fact_corroboration(decision)
        and not _template_plan_has_validation_errors(decision)
        and not _decision_uses_resolved_official_source(decision, context)
    ):
        issues.append(
            _issue(
                code="official_facts_self_check_uncorroborated",
                severity="P0",
                message=(
                    "official-facts self-check is true without resolved official "
                    "source evidence"
                ),
                path="policy_checks.official_facts_only",
            )
        )

    if policy_checks.diagnostic_timing_ok and _diagnostic_completion_uncorroborated(
        decision,
        context,
    ):
        issues.append(
            _issue(
                code="diagnostic_self_check_uncorroborated",
                severity="P0",
                message=(
                    "diagnostic timing self-check is true but mandatory ledger "
                    "completion is not corroborated"
                ),
                path="policy_checks.diagnostic_timing_ok",
            )
        )

    return issues


def _requires_official_fact_corroboration(decision: ConductorDecision) -> bool:
    template_ids = _template_ids(decision)
    if any(template_id.startswith("product.") for template_id in template_ids):
        return True
    return (
        decision.route == "product"
        and bool(_OFFICIAL_FACT_INTENTS.intersection(decision.detected_intents))
    )


def _template_plan_has_validation_errors(decision: ConductorDecision) -> bool:
    return bool(_validate_template_plan(decision))


def _decision_uses_resolved_official_source(
    decision: ConductorDecision,
    context: TurnContext,
) -> bool:
    evidence_index = _product_evidence_index(context)
    if _OFFICIAL_STATIC_PRODUCT_TEMPLATE_IDS.intersection(_template_ids(decision)):
        if any(not ref.missing for ref in context.product_knowledge):
            return True
    for item in decision.template_plan.items:
        for variable in item.variables.values():
            if variable.source in _PRODUCT_SOURCES and _evidence_resolves(
                evidence=variable.evidence,
                source=variable.source,
                evidence_index=evidence_index,
            ):
                return True
    return False


def _diagnostic_completion_uncorroborated(
    decision: ConductorDecision,
    context: TurnContext,
) -> bool:
    if not (
        decision.diagnostic.action == "complete"
        or _has_diagnostic_delivery_template(decision)
    ):
        return False

    status_by_key = _merged_diagnostic_statuses(decision, context)
    if _only_missing_diagnostic_key(status_by_key, "pain_detail"):
        return False
    return any(
        status_by_key.get(question_key) not in _DIAGNOSTIC_COMPLETE_STATUSES
        for question_key in _REQUIRED_DIAGNOSTIC_KEYS
    )


def _iter_text_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        values: list[str] = []
        for item in value:
            values.extend(_iter_text_values(item))
        return values
    if isinstance(value, dict):
        values = []
        for item in value.values():
            values.extend(_iter_text_values(item))
        return values
    return []


def _is_missing_projection_value(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, list | tuple | set | dict):
        return len(value) == 0
    return False


def _projection_string_set(value: Any) -> set[str]:
    if isinstance(value, str):
        return {value} if value.strip() else set()
    if isinstance(value, list | tuple | set):
        return {str(item) for item in value if str(item).strip()}
    return set()


def _contains_phrase(text: str, phrases: tuple[str, ...]) -> bool:
    return any(phrase in text for phrase in phrases)


def _is_pure_cold_greeting_context(context: TurnContext) -> bool:
    if context.inbound.message_type != "text":
        return False
    normalized = _normalize_customer_text(context.inbound.text)
    if normalized not in _PURE_COLD_GREETINGS:
        return False
    if context.compact_memory or context.diagnostic_ledger:
        return False
    return True


def _is_widget_empty_opening_context(context: TurnContext) -> bool:
    if context.channel != "widget" or context.inbound.message_type != "text":
        return False
    if (context.inbound.text or "").strip():
        return False
    if context.compact_memory or context.diagnostic_ledger:
        return False
    return True


def _is_first_turn_context(context: TurnContext) -> bool:
    if context.inbound.message_type != "text":
        return False
    if context.compact_memory or context.recent_transcript or context.diagnostic_ledger:
        return False
    return True


def _normalize_customer_text(value: str | None) -> str:
    normalized = unicodedata.normalize("NFKD", (value or "").strip().casefold())
    without_marks = "".join(
        char for char in normalized if not unicodedata.combining(char)
    )
    return re.sub(r"[!?.,;:\s]+", " ", without_marks).strip()


def _validate_waitlist(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    waitlist = decision.waitlist
    intents = {intent.lower() for intent in decision.detected_intents}
    template_ids = _template_ids(decision)
    contract_or_waitlist_intent = bool(
        {
            "buy_intent",
            "checkout_request",
            "contract_intent",
            "waitlist_interest",
            "waitlist_intent",
            "waitlist_request",
            "subscription_intent",
        }.intersection(intents)
    )
    has_waitlist_surface = waitlist.status in _ACTIVE_WAITLIST_STATUSES or any(
        template_id.startswith("waitlist.") for template_id in template_ids
    )
    if (
        _context_diagnostic_completed(context)
        and contract_or_waitlist_intent
        and not has_waitlist_surface
    ):
        issues.append(
            _issue(
                code="waitlist_contract_intent_missing_offer",
                severity="P1",
                message=(
                    "post-diagnostic contract or waitlist intent requires an "
                    "approved waitlist offer path"
                ),
                path="template_plan.items",
            )
        )
    if waitlist.status not in _ACTIVE_WAITLIST_STATUSES:
        return issues

    if waitlist.eligibility != "eligible":
        issues.append(
            _issue(
                code="waitlist_requires_eligibility",
                severity="P0",
                message="waitlist action requires structured eligible status",
                path="waitlist.eligibility",
            )
        )

    if (
        decision.demo.status in _DEMO_CURIOSITY_STATUSES
        and waitlist.eligibility != "eligible"
    ):
        issues.append(
            _issue(
                code="waitlist_demo_curiosity_without_contract_intent",
                severity="P0",
                message="demo curiosity alone cannot enable waitlist",
                path="waitlist.eligibility",
            )
        )

    if waitlist.status == "pending_details" and not waitlist.missing_details:
        issues.append(
            _issue(
                code="waitlist_pending_details_missing_fields",
                severity="P0",
                message="pending_details requires at least one missing detail",
                path="waitlist.missing_details",
            )
        )

    if waitlist.status == "joined" and waitlist.missing_details:
        issues.append(
            _issue(
                code="waitlist_joined_with_missing_details",
                severity="P0",
                message="joined waitlist cannot keep missing details",
                path="waitlist.missing_details",
            )
        )

    if waitlist.status == "joined":
        joined_templates = [
            item
            for item in decision.template_plan.items
            if _normalize_template_id(item.template_id) == "waitlist.joined"
        ]
        if joined_templates and not any(item.variables for item in joined_templates):
            issues.append(
                _issue(
                    code="waitlist_joined_missing_details",
                    severity="P0",
                    message="joined waitlist requires real studio details",
                    path="template_plan.items",
                )
            )
        for item_index, item in enumerate(decision.template_plan.items):
            if _normalize_template_id(item.template_id) != "waitlist.joined":
                continue
            for variable_name, variable in item.variables.items():
                if variable_name not in {"studio_name", "city_state"}:
                    continue
                if _normalize_customer_text(str(variable.value)) in {
                    "unknown",
                    "desconhecido",
                    "nao informado",
                    "nao sei",
                }:
                    issues.append(
                        _issue(
                            code="waitlist_joined_unknown_details",
                            severity="P0",
                            message="joined waitlist cannot render unknown studio details",
                            path=f"template_plan.items[{item_index}].variables.{variable_name}",
                        )
                    )

    return issues


def _validate_waitlist_channel_missing_details(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    if context.channel != "whatsapp" or _context_fact_value(context, "whatsapp_phone") is None:
        return []
    template_ids = _template_ids(decision)
    if (
        decision.waitlist.status != "pending_details"
        and "waitlist.ask_missing_contact_path" not in template_ids
    ):
        return []
    if (
        "contact_path" not in decision.waitlist.missing_details
        and "waitlist.ask_missing_contact_path" not in template_ids
    ):
        return []
    return [
        _issue(
            code="waitlist_contact_path_not_needed_for_whatsapp",
            severity="P1",
            message=(
                "Taliya-owned WhatsApp leads already have the contact path; ask "
                "for studio/city details instead"
            ),
            path="waitlist.missing_details",
        )
    ]


def _validate_price_question_followup(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    intents = {intent.lower() for intent in decision.detected_intents}
    if not _has_price_intent(intents):
        return []
    if any("diagnostic_refusal" in intent or "diagnostic_refused" in intent for intent in intents):
        return []
    if decision.diagnostic.action == "complete" or _has_diagnostic_delivery_template(
        decision
    ):
        return []

    template_ids = _template_ids(decision)
    issues: list[ValidationIssue] = []
    if not template_ids.intersection(_PRICE_ANSWER_TEMPLATE_IDS):
        issues.append(
            _issue(
                code="price_question_missing_price_answer",
                severity="P1",
                message="price questions must answer with official prices before steering",
                path="template_plan.items",
            )
        )
    if _context_diagnostic_completed(context):
        return issues
    if decision.route == "diagnostic" and decision.diagnostic.action == "ask_next":
        return issues
    if not template_ids.intersection(_PRICE_HOOK_TEMPLATE_IDS):
        issues.append(
            _issue(
                code="price_question_missing_diagnostic_hook",
                severity="P1",
                message=(
                    "price answers must include the approved diagnostic price hook "
                    "unless the lead explicitly refused diagnostic"
                ),
                path="template_plan.items",
            )
        )
    if decision.diagnostic.action == "none":
        issues.append(
            _issue(
                code="price_question_missing_diagnostic_offer",
                severity="P1",
                message="price hook requires diagnostic.action=offer",
                path="diagnostic.action",
            )
        )
    return issues


def _validate_price_objection_value_response(
    decision: ConductorDecision,
) -> list[ValidationIssue]:
    intents = {intent.lower() for intent in decision.detected_intents}
    if not _has_price_objection_intent(intents):
        return []

    if _PRICE_OBJECTION_TEMPLATE_ID in _template_ids(decision):
        return []

    return [
        _issue(
            code="price_objection_value_template_missing",
            severity="P1",
            message=(
                "price objections require the approved value-language template "
                "before steering to diagnostic, waitlist, demo, or handoff"
            ),
            path="template_plan.items",
        )
    ]


def _validate_diagnostic_refusal_respected(
    decision: ConductorDecision,
) -> list[ValidationIssue]:
    intents = {intent.lower() for intent in decision.detected_intents}
    if not any(
        "diagnostic_refusal" in intent or "diagnostic_refused" in intent
        for intent in intents
    ):
        return []

    template_ids = _template_ids(decision)
    if (
        not template_ids.intersection(_DIAGNOSTIC_OFFER_TEMPLATE_IDS)
        and decision.diagnostic.action == "none"
    ):
        return []

    return [
        _issue(
            code="diagnostic_refusal_not_respected",
            severity="P1",
            message=(
                "when the lead explicitly refuses diagnostic, the turn may answer "
                "the direct question but must not offer or start diagnostic"
            ),
            path="diagnostic.action",
        )
    ]


def _has_price_intent(intents: set[str]) -> bool:
    return any("price" in intent or "preco" in intent for intent in intents)


def _has_price_objection_intent(intents: set[str]) -> bool:
    for intent in intents:
        if intent in {
            "price_objection",
            "price_concern",
            "value_objection",
            "cost_objection",
            "discount_request",
            "roi_question",
        }:
            return True
        if "objection" in intent and any(
            marker in intent for marker in ("price", "preco", "cost", "value")
        ):
            return True
    return False


def _validate_how_it_works_template(decision: ConductorDecision) -> list[ValidationIssue]:
    intents = {intent.lower() for intent in decision.detected_intents}
    if "how_it_works" not in intents and "product_how_it_works" not in intents:
        return []
    template_ids = _template_ids(decision)
    issues: list[ValidationIssue] = []
    if (
        _HOW_IT_WORKS_TEMPLATE_ID not in template_ids
        and _WHATSAPP_DIRECT_TEMPLATE_ID not in template_ids
    ):
        issues.append(
            _issue(
                code="how_it_works_template_missing",
                severity="P1",
                message="how-it-works answers require product.how_it_works_direct",
                path="template_plan.items",
            )
        )
    if _HOW_IT_WORKS_TEMPLATE_ID in template_ids and template_ids.intersection(
        _HOW_IT_WORKS_REDUNDANT_FOLLOWUP_TEMPLATE_IDS
    ):
        issues.append(
            _issue(
                code="how_it_works_redundant_followup",
                severity="P1",
                message="how-it-works template already owns the diagnostic next step",
                path="template_plan.items",
            )
        )
    return issues


def _validate_integration_scope_template(
    decision: ConductorDecision,
) -> list[ValidationIssue]:
    intents = {intent.lower() for intent in decision.detected_intents}
    if (
        not decision.direct_question_present
        or not _INTEGRATION_SCOPE_INTENTS.intersection(intents)
        or _HUMAN_HANDOFF_REQUEST_INTENTS.intersection(intents)
    ):
        return []

    if _INTEGRATION_SCOPE_TEMPLATE_ID in _template_ids(decision):
        return []

    code = "integration_scope_template_missing"
    message = (
        "direct integration-scope questions require "
        "product.integration_scope_direct before any handoff"
    )
    path = "template_plan.items"
    if decision.route == "handoff" or decision.handoff.status == "requested":
        code = "integration_scope_handoff_without_product_answer"
        path = "route"
        message = (
            "direct integration-scope questions must answer the official safe "
            "scope before escalating to human confirmation"
        )

    return [
        _issue(
            code=code,
            severity="P1",
            message=message,
            path=path,
        )
    ]


def _validate_demo(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    template_ids = _template_ids(decision)
    issues: list[ValidationIssue] = []
    if (
        "product.demo_direct" in template_ids
        and _context_diagnostic_completed(context)
        and not _inbound_has_demo_request(context)
    ):
        issues.append(
            _issue(
                code="stale_demo_direct_without_current_request",
                severity="P1",
                message=(
                    "product.demo_direct may not be reused from prior demo context "
                    "when the current lead message does not ask for a demo"
                ),
                path="template_plan.items",
            )
        )
    if decision.demo.next_step != "offer_demo":
        return issues

    if template_ids.intersection(_DEMO_OFFER_TEMPLATE_IDS):
        return issues

    issues.append(
        _issue(
            code="demo_offer_template_missing",
            severity="P0",
            message="demo offer requires an approved demo template",
            path="template_plan.items",
        )
    )
    return issues


def _validate_post_diagnostic_demo_request(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    if not _context_diagnostic_completed(context):
        return []

    intents = {intent.lower() for intent in decision.detected_intents}
    template_ids = _template_ids(decision)
    demo_requested = _inbound_has_demo_request(context) and (
        bool(_DEMO_REQUEST_INTENTS.intersection(intents))
        or decision.demo.next_step == "offer_demo"
        or decision.demo.status in _DEMO_CURIOSITY_STATUSES
        or "product.demo_direct" in template_ids
    )
    if not demo_requested:
        return []

    if _has_diagnostic_delivery_template(decision):
        return [
            _issue(
                code="post_diagnostic_demo_request_redelivered_diagnostic",
                severity="P1",
                message=(
                    "after a completed diagnostic, direct demo requests must answer "
                    "with product.demo_direct instead of delivering the diagnostic again"
                ),
                path="template_plan.items",
            )
        ]

    if "product.demo_direct" not in template_ids:
        return [
            _issue(
                code="post_diagnostic_demo_request_template_missing",
                severity="P1",
                message=(
                    "after a completed diagnostic, direct demo requests require "
                    "product.demo_direct with official demo link"
                ),
                path="template_plan.items",
            )
        ]
    return []


def _inbound_has_demo_request(context: TurnContext) -> bool:
    if context.inbound.message_type != "text":
        return False
    normalized = _normalize_customer_text(context.inbound.text)
    return any(
        marker in normalized
        for marker in (
            "demo",
            "demonstracao",
            "demonstracoes",
            "demonstrar",
            "video",
            "videos",
        )
    )


def _validate_demo_direct_question_flags(
    decision: ConductorDecision,
) -> list[ValidationIssue]:
    if "product.demo_direct" not in _template_ids(decision):
        return []
    if decision.direct_question_present and decision.direct_question_answered_first:
        return []
    return [
        _issue(
            code="demo_direct_question_flags_missing",
            severity="P1",
            message=(
                "product.demo_direct is a direct product-demo answer and must mark "
                "the direct request as answered first"
            ),
            path="direct_question_answered_first",
        )
    ]


def _validate_handoff(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    context_handoff_status = str(context.handoff_state.get("status") or "none")
    template_ids = _template_ids(decision)

    if (
        context_handoff_status in _HANDOFF_ACTIVE_CONTEXT_STATUSES
        and decision.handoff.status != "resumed"
    ):
        issues.append(
            _issue(
                code="handoff_active_blocks_delivery",
                severity="P0",
                message="human-active context blocks normal AI delivery",
                path="handoff_state.status",
            )
        )

    if decision.handoff.status == "requested":
        if not (decision.handoff.reason or "").strip():
            issues.append(
                _issue(
                    code="handoff_reason_missing",
                    severity="P0",
                    message="handoff request requires a structured reason",
                    path="handoff.reason",
                )
            )
        if decision.route != "handoff":
            issues.append(
                _issue(
                    code="handoff_route_mismatch",
                    severity="P0",
                    message="handoff request requires handoff route",
                    path="route",
                )
            )
        if "handoff.acknowledge" not in template_ids:
            issues.append(
                _issue(
                    code="handoff_ack_template_missing",
                    severity="P0",
                    message="handoff request requires acknowledge template",
                    path="template_plan.items",
                )
            )

    return issues


def _validate_diagnostic_next_question(
    decision: ConductorDecision,
    status_by_key: dict[str, str],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    next_question_key = decision.diagnostic.next_question_key
    question_templates = _diagnostic_question_templates(decision)

    if next_question_key not in _REQUIRED_DIAGNOSTIC_KEYS:
        issues.append(
            _issue(
                code="diagnostic_next_question_invalid",
                severity="P0",
                message="diagnostic ask_next must target a mandatory diagnostic key",
                path="diagnostic.next_question_key",
            )
        )
    elif status_by_key.get(next_question_key) in _DIAGNOSTIC_COMPLETE_STATUSES:
        issues.append(
            _issue(
                code="diagnostic_next_question_not_missing",
                severity="P0",
                message="diagnostic ask_next must target a missing or ambiguous key",
                path="diagnostic.next_question_key",
            )
        )

    if len(question_templates) > 1:
        issues.append(
            _issue(
                code="diagnostic_multiple_next_questions",
                severity="P0",
                message="diagnostic ask_next may include only one question template",
                path="template_plan.items",
            )
        )

    if (
        len(question_templates) == 1
        and next_question_key in _DIAGNOSTIC_QUESTION_TEMPLATE_BY_KEY
    ):
        expected_template = _DIAGNOSTIC_QUESTION_TEMPLATE_BY_KEY[next_question_key]
        if question_templates[0] != expected_template:
            issues.append(
                _issue(
                    code="diagnostic_next_question_template_mismatch",
                    severity="P0",
                    message="diagnostic question template must match next_question_key",
                    path="template_plan.items",
                )
            )

    return issues


def _validate_diagnostic_question_feedback(
    decision: ConductorDecision,
) -> list[ValidationIssue]:
    question_templates = _diagnostic_question_templates(decision)
    if not question_templates:
        return []
    answered_updates = [
        update
        for update in decision.diagnostic.ledger_updates
        if update.status in _DIAGNOSTIC_EVIDENCE_STATUSES
        and (update.answer_value or "").strip()
    ]
    if not answered_updates:
        return []

    issues: list[ValidationIssue] = []
    for index, item in enumerate(decision.template_plan.items):
        if item.template_id not in _DIAGNOSTIC_KEY_BY_QUESTION_TEMPLATE:
            continue
        if "answer_feedback" not in item.variables:
            issues.append(
                _issue(
                    code="diagnostic_question_missing_answer_feedback",
                    severity="P1",
                    message=(
                        "diagnostic follow-up questions after captured context "
                        "must include grounded answer_feedback"
                    ),
                    path=f"template_plan.items[{index}].variables.answer_feedback",
                )
            )
    return issues


def _validate_first_turn_diagnostic_greeting(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    if not _is_first_turn_context(context) or decision.route != "diagnostic":
        return []
    template_ids = _template_ids(decision)
    if not template_ids.intersection(
        _DIAGNOSTIC_QUESTION_TEMPLATE_IDS | {"diagnostic.offer_soft"}
    ):
        return []
    if template_ids.intersection(_OPENING_TEMPLATE_IDS):
        return []
    return [
        _issue(
            code="first_turn_diagnostic_missing_greeting",
            severity="P1",
            message=(
                "first-turn diagnostic questions must start with an approved "
                "opening/greeting before the diagnostic question"
            ),
            path="template_plan.items",
        )
    ]


def _validate_pain_first_offer_boundary(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    if not _is_first_turn_context(context):
        return []
    if "diagnostic_request" in decision.detected_intents:
        return []
    if not _PAIN_FIRST_INTENTS.intersection(set(decision.detected_intents)):
        return []
    active_students_update = next(
        (
            update
            for update in decision.diagnostic.ledger_updates
            if update.question_key == "active_students_or_size"
            and update.status in _DIAGNOSTIC_EVIDENCE_STATUSES
        ),
        None,
    )
    if active_students_update is not None:
        return []
    template_ids = _template_ids(decision)
    has_offer_soft = "diagnostic.offer_soft" in template_ids
    has_product_template = any(
        template_id.startswith("product.") for template_id in template_ids
    )
    if decision.route != "diagnostic":
        if (
            decision.route == "product"
            and not decision.direct_question_present
            and decision.diagnostic.action in {"offer", "start", "ask_next"}
            and has_offer_soft
            and not has_product_template
        ):
            return [
                _issue(
                    code="pain_first_diagnostic_offer_must_use_diagnostic_route",
                    severity="P1",
                    message=(
                        "pain-first diagnostic offers without a direct product "
                        "question must use the diagnostic route"
                    ),
                    path="route",
                ),
                _issue(
                    code="diagnostic_start_must_ask_active_students",
                    severity="P1",
                    message=(
                        "pain-first diagnostic offers must ask "
                        "active_students_or_size first"
                    ),
                    path="template_plan.items",
                ),
            ]
        return []
    if has_offer_soft:
        return []
    return [
        _issue(
            code="pain_first_must_offer_diagnostic",
            severity="P1",
            message=(
                "pain-first openings should offer the diagnostic with approved "
                "owner copy instead of immediately asking a diagnostic question"
            ),
            path="template_plan.items",
        )
    ]


def _validate_diagnostic_no_repeat(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    prior_statuses = _context_diagnostic_statuses(context)
    repeated_keys: set[str] = set()
    next_question_key = decision.diagnostic.next_question_key

    if (
        next_question_key in _REQUIRED_DIAGNOSTIC_KEYS
        and prior_statuses.get(next_question_key) in _DIAGNOSTIC_COMPLETE_STATUSES
    ):
        repeated_keys.add(next_question_key)
        issues.append(
            _issue(
                code="diagnostic_question_repeated",
                severity="P0",
                message="diagnostic question was already answered in context",
                path="diagnostic.next_question_key",
            )
        )

    for template_id in _diagnostic_question_templates(decision):
        question_key = _DIAGNOSTIC_KEY_BY_QUESTION_TEMPLATE.get(template_id)
        if question_key is None or question_key in repeated_keys:
            continue
        if prior_statuses.get(question_key) in _DIAGNOSTIC_COMPLETE_STATUSES:
            repeated_keys.add(question_key)
            issues.append(
                _issue(
                    code="diagnostic_question_repeated",
                    severity="P0",
                    message="diagnostic question template repeats completed context",
                    path="template_plan.items",
                )
            )

    return issues


def _merged_diagnostic_statuses(
    decision: ConductorDecision,
    context: TurnContext,
) -> dict[str, str]:
    statuses = _context_diagnostic_statuses(context)

    for update in decision.diagnostic.ledger_updates:
        statuses[update.question_key] = update.status

    return statuses


def _context_diagnostic_statuses(context: TurnContext) -> dict[str, str]:
    statuses: dict[str, str] = {}
    for item in context.diagnostic_ledger:
        if not isinstance(item, dict):
            continue
        question_key = str(item.get("question_key") or "")
        status = str(item.get("status") or "")
        if question_key in _REQUIRED_DIAGNOSTIC_KEYS and status:
            statuses[question_key] = status
    return statuses


def _context_diagnostic_completed(context: TurnContext) -> bool:
    if context.sales_inbox_inputs.get("diagnostic_status") == "completed":
        return True
    statuses = _context_diagnostic_statuses(context)
    return bool(statuses) and all(
        statuses.get(question_key) in _DIAGNOSTIC_COMPLETE_STATUSES
        for question_key in _REQUIRED_DIAGNOSTIC_KEYS
    )


def _diagnostic_question_templates(decision: ConductorDecision) -> list[str]:
    return [
        _normalize_template_id(item.template_id)
        for item in decision.template_plan.items
        if _normalize_template_id(item.template_id).startswith("diagnostic.ask_")
    ]


def _has_diagnostic_delivery_template(decision: ConductorDecision) -> bool:
    return any(
        _normalize_template_id(item.template_id).startswith("diagnostic.deliver")
        for item in decision.template_plan.items
    )


def _template_ids(decision: ConductorDecision) -> set[str]:
    return {
        _normalize_template_id(item.template_id)
        for item in decision.template_plan.items
    }


def _normalize_template_id(template_id: str) -> str:
    return template_id.split("#", 1)[0]


def _product_evidence_index(context: TurnContext) -> set[tuple[str, str]]:
    entries: set[tuple[str, str]] = set()
    for ref in context.product_knowledge:
        if ref.missing:
            continue
        entries.add((ref.source, ref.key))
        if ref.source == "official_product_knowledge":
            entries.add((ref.source, f"product_knowledge.{ref.key}"))
        for evidence in ref.evidence:
            entries.add((ref.source, evidence))
    return entries


def _evidence_resolves(
    *,
    evidence: list[str],
    source: str,
    evidence_index: set[tuple[str, str]],
) -> bool:
    for item in evidence:
        for indexed_source, prefix in evidence_index:
            if indexed_source != source:
                continue
            if item == prefix or item.startswith(f"{prefix}."):
                return True
    return False


def _official_link_map(context: TurnContext) -> dict[str, str]:
    for ref in context.product_knowledge:
        if (
            ref.source == "official_product_knowledge"
            and ref.key == "links"
            and isinstance(ref.value, dict)
        ):
            return {
                str(key): str(value)
                for key, value in ref.value.items()
                if isinstance(value, str) and value.strip()
            }
    return {}


def _official_price_amounts(context: TurnContext) -> set[int]:
    amounts: set[int] = set()
    for ref in context.product_knowledge:
        if ref.source != "official_product_knowledge" or ref.missing:
            continue
        if ref.key == "plans" and isinstance(ref.value, list):
            for plan in ref.value:
                if isinstance(plan, dict):
                    value = _coerce_int(plan.get("monthly_price_brl"))
                    if value is not None:
                        amounts.add(value)
        if ref.key == "prices" and isinstance(ref.value, dict):
            for price_label in ref.value.values():
                amounts.update(_extract_int_tokens(price_label))
    return amounts


def _official_plan_names(context: TurnContext) -> set[str]:
    names: set[str] = set()
    for ref in context.product_knowledge:
        if (
            ref.source == "official_product_knowledge"
            and ref.key == "plans"
            and isinstance(ref.value, list)
        ):
            for plan in ref.value:
                if isinstance(plan, dict) and isinstance(plan.get("name"), str):
                    names.add(str(plan["name"]))
    return names


def _unsupported_product_claims(context: TurnContext) -> set[str]:
    claims: set[str] = set()
    for ref in context.product_knowledge:
        if (
            ref.source != "official_product_knowledge"
            or ref.key != "unsupported_claims"
            or ref.missing
        ):
            continue
        if isinstance(ref.value, list):
            claims.update(
                str(item).casefold()
                for item in ref.value
                if isinstance(item, str) and item.strip()
            )
    return claims


def _student_count_fact_values(decision: ConductorDecision) -> set[int]:
    values: set[int] = set()
    for fact in decision.facts:
        if fact.key not in _STUDENT_COUNT_FACT_KEYS or fact.source != "user_message":
            continue
        value = _coerce_int(fact.value)
        if value is not None:
            values.add(value)
    return values


def _has_user_grounding_evidence(evidence: list[str]) -> bool:
    return any(
        item.strip()
        and not item.startswith("product_knowledge.")
        and not item.startswith("spec006.")
        and not item.startswith("specs/006-")
        for item in evidence
    )


def _coerce_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value) if value.is_integer() else None
    tokens = _extract_int_tokens(value)
    if len(tokens) == 1:
        return next(iter(tokens))
    return None


def _extract_int_tokens(value: Any) -> set[int]:
    text = str(value)
    tokens: set[int] = set()
    current = ""
    for character in text:
        if "0" <= character <= "9":
            current += character
            continue
        if character in {".", ","} and current:
            current += character
            continue
        _flush_int_token(tokens, current)
        current = ""
    _flush_int_token(tokens, current)
    return tokens


def _flush_int_token(tokens: set[int], raw_token: str) -> None:
    digits = "".join(
        character for character in raw_token if "0" <= character <= "9"
    )
    if digits:
        tokens.add(int(digits))


def _status_for_errors(
    errors: list[ValidationIssue],
) -> str:
    if not errors:
        return "passed"
    if any(error.severity == "P0" for error in errors):
        return "blocked"
    return "repairable"


def _final_disposition_for_errors(
    errors: list[ValidationIssue],
) -> str | None:
    if not errors:
        return "accepted"
    if any(error.severity == "P0" for error in errors):
        return "blocked"
    return None


def _issue(
    *,
    code: str,
    severity: Severity,
    message: str,
    path: str,
) -> ValidationIssue:
    return ValidationIssue(
        code=code,
        severity=severity,
        message=message,
        path=path,
    )
