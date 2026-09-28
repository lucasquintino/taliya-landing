from __future__ import annotations

import inspect
import re
from collections.abc import Awaitable, Callable, Mapping
from typing import Any

from pydantic import Field

from app.core.taliya_commercial.conductor import (
    ConductorError,
    ConductorTurnResult,
    _format_fact_source_rules,
    _format_registered_template_catalog,
    _parse_provider_result,
    build_conductor_response_schema,
)
from app.core.taliya_commercial.context_snapshot import (
    build_context_snapshot,
    context_snapshot_to_json,
)
from app.core.taliya_commercial.schema_versioning import CURRENT_CONDUCTOR_SCHEMA_VERSION
from app.core.taliya_commercial.schemas import (
    ConductorDecision,
    DemoDecision,
    DiagnosticDecision,
    DiagnosticLedgerItem,
    HandoffDecision,
    RenderPlan,
    RenderPlanItem,
    RepairResult,
    StrictModel,
    TemplateVariableValue,
    TurnContext,
    ValidationIssue,
    ValidatorResult,
    WaitlistDecision,
)
from app.core.taliya_commercial.template_registry import VARIABLE_REGISTRY
from app.core.taliya_commercial.validators import validate_conductor_result
from app.domains.taliya_commercial.behavior_policy import assess_profile_name

_PRICE_ANSWER_TEMPLATE_IDS = {
    "product.price_direct",
    "product.price_complete_direct",
    "product.plan_direct",
    "product.price_objection_value",
}
_PRICE_HOOK_TEMPLATE_ID = "diagnostic.price_hook"
_PRICE_HOOK_TEMPLATE_IDS = {
    "diagnostic.price_hook",
    "diagnostic.price_hook_with_context",
    "product.price_objection_value",
}
_PRICE_OBJECTION_TEMPLATE_ID = "product.price_objection_value"
_PRICE_HOOK_REPAIR_CODES = {
    "banned_waitlist_promise",
    "duplicate_diagnostic_offer_templates",
    "price_objection_value_template_missing",
    "price_question_missing_price_answer",
    "price_question_missing_diagnostic_hook",
    "price_question_missing_diagnostic_offer",
    "price_plus_context_requires_context_hook",
    "product_route_must_not_ask_diagnostic_question",
    "stale_demo_direct_without_current_request",
    "unsupported_price_value",
}
_HOW_IT_WORKS_TEMPLATE_ID = "product.how_it_works_direct"
_HOW_IT_WORKS_REPAIR_CODES = {
    "how_it_works_template_missing",
    "how_it_works_redundant_followup",
    "template_plan_invalid",
    "diagnostic_required_field_missing",
    "diagnostic_final_demo_stage_missing",
    "diagnostic_final_staged_order_invalid",
    "diagnostic_self_check_uncorroborated",
}
_INTEGRATION_SCOPE_TEMPLATE_ID = "product.integration_scope_direct"
_INTEGRATION_SCOPE_REPAIR_CODES = {
    "integration_scope_handoff_without_product_answer",
    "integration_scope_template_missing",
}
_PLAN_FIT_REPAIR_CODES = {
    "plan_fit_direct_answer_template_missing",
    "plan_fit_owner_copy_template_missing",
    "plan_fit_redundant_diagnostic_offer",
    "product_route_must_not_ask_diagnostic_question",
    "template_plan_invalid",
}
_PRODUCT_ROUTE_SHAPE_REPAIR_CODES = {
    "diagnostic_final_demo_stage_missing",
    "diagnostic_final_staged_order_invalid",
    "demo_direct_requires_product_route",
    "demo_offer_template_missing",
    "duplicate_diagnostic_offer_templates",
    "official_facts_self_check_uncorroborated",
    "post_diagnostic_demo_request_redelivered_diagnostic",
    "post_diagnostic_demo_request_template_missing",
}
_WHATSAPP_DIRECT_REPAIR_CODES = {
    "whatsapp_direct_answer_incomplete",
    "whatsapp_direct_demo_link_missing",
}
_DEMO_DIRECT_REPAIR_CODES = {
    "demo_direct_question_flags_missing",
    "price_question_missing_price_answer",
    "price_question_missing_diagnostic_hook",
    "price_question_missing_diagnostic_offer",
}
_DIAGNOSTIC_FEEDBACK_REPAIR_CODES = {
    "diagnostic_feedback_language_leak",
    "diagnostic_question_missing_answer_feedback",
    "template_plan_invalid",
}
_DIAGNOSTIC_REFUSAL_REPAIR_CODES = {
    "diagnostic_refusal_not_respected",
}
_FINAL_DIAGNOSTIC_STAGE_REPAIR_CODES = {
    "diagnostic_final_demo_stage_missing",
    "diagnostic_final_staged_order_invalid",
}
_STALE_COMPLETED_DIAGNOSTIC_FOLLOWUP_REPAIR_CODES = {
    "diagnostic_final_demo_stage_missing",
    "diagnostic_final_staged_order_invalid",
}
_STALE_DEMO_FOLLOWUP_REPAIR_CODES = {
    "demo_offer_template_missing",
    "post_diagnostic_demo_request_template_missing",
    "stale_demo_direct_without_current_request",
}
_DIAGNOSTIC_QUESTION_TEMPLATE_IDS = {
    "diagnostic.ask_active_students",
    "diagnostic.ask_main_pain",
    "diagnostic.ask_current_process",
    "diagnostic.ask_pain_detail",
    "diagnostic.ask_priority",
    "diagnostic.ask_urgency",
}
_DIAGNOSTIC_COMPLETION_REPAIR_CODES = {
    "diagnostic_required_field_missing",
    "diagnostic_self_check_uncorroborated",
    "diagnostic_urgency_must_be_next",
    "diagnostic_urgency_evidence_is_assistant_prompt",
    "diagnostic_urgency_evidence_is_priority",
    "diagnostic_urgency_evidence_not_timing",
    "diagnostic_next_question_not_missing",
    "diagnostic_start_must_ask_active_students",
}
_COLD_GREETING_REPAIR_CODES = {
    "cold_greeting_must_stay_entry",
    "cold_greeting_reliable_name_missing",
    "cold_greeting_unreliable_name_used",
}
_ENTRY_OPENING_REPAIR_CODES = {
    "entry_opening_diagnostic_offer_not_marked",
    "instagram_source_opening_template_missing",
}
_DIAGNOSTIC_CTA_REPAIR_CODES = {
    "diagnostic_cta_opening_missing",
    "diagnostic_cta_question_missing",
    "diagnostic_cta_duplicate_start_template",
}
_FIRST_TURN_DIAGNOSTIC_REPAIR_CODES = {
    "first_turn_diagnostic_missing_greeting",
}
_PAIN_FIRST_REPAIR_CODES = {
    "pain_first_must_offer_diagnostic",
}
_WIDGET_EMPTY_OPENING_REPAIR_CODES = {
    "widget_empty_must_use_opening_template",
}
_SENSITIVE_DATA_REPAIR_CODES = {
    "direct_question_self_check_uncorroborated",
    "handoff_route_mismatch",
    "handoff_ack_template_missing",
}
_HANDOFF_FOLLOWUP_REPAIR_CODES = {
    "diagnostic_required_field_missing",
    "diagnostic_urgency_must_be_next",
    "diagnostic_final_demo_stage_missing",
    "diagnostic_final_staged_order_invalid",
    "diagnostic_self_check_uncorroborated",
}
_LLM_REPAIRABLE_BLOCKED_CODES = {
    "diagnostic_next_question_invalid",
    "diagnostic_urgency_answer_not_captured",
    "product_claim_source_missing",
    "unresolved_product_evidence",
    "unknown_plan_name",
    "waitlist_requires_eligibility",
}
_WAITLIST_REPAIR_CODES = {
    "waitlist_requires_eligibility",
    "waitlist_offer_missing_studio_details",
    "waitlist_pending_details_missing_fields",
    "waitlist_contact_path_not_needed_for_whatsapp",
    "waitlist_joined_missing_details",
    "waitlist_joined_unknown_details",
    "waitlist_contract_intent_missing_offer",
    "banned_waitlist_promise",
    "template_plan_invalid",
}
_POLICY_CHECK_REPAIR_CODES = {
    "direct_question_self_check_uncorroborated",
    "official_facts_self_check_uncorroborated",
}
_OFFICIAL_PRODUCT_VARIABLE_REPAIR_CODES = {
    "product_claim_source_invalid",
    "product_claim_source_missing",
    "template_plan_invalid",
    "unresolved_product_evidence",
    "unknown_plan_name",
}
_PRODUCT_KNOWLEDGE_SOURCES = {
    "official_product_knowledge",
    "spec_006_product_contract",
}
_REQUIRED_DIAGNOSTIC_ORDER = (
    "active_students_or_size",
    "main_pain",
    "pain_detail",
    "current_process",
    "priority",
    "urgency",
)
_DIAGNOSTIC_EVIDENCE_STATUSES = {
    "answered",
    "inferred_from_prior_message",
    "not_applicable",
}
_ENGLISH_TRANSLATION_LEAK_PHRASES = (
    "lead loses",
    "interested leads",
    "team takes too long",
    "current routine",
    "pain point",
)
_CURRENT_DEMO_REQUEST_MARKERS = (
    "demo",
    "demonstracao",
    "demonstração",
    "demonstracoes",
    "demonstrações",
    "demonstrar",
    "video",
    "videos",
)
_PRICE_OBJECTION_INBOUND_MARKERS = (
    "achei caro",
    "ta caro",
    "tá caro",
    "esta caro",
    "está caro",
    "muito caro",
    "valor alto",
    "preco alto",
    "preço alto",
    "custa muito",
    "fora do orcamento",
    "fora do orçamento",
    "sem orcamento",
    "sem orçamento",
    "tem desconto",
    "desconto",
    "compensa",
    "vale a pena",
    "roi",
    "retorno",
)
_DIAGNOSTIC_QUESTION_TEMPLATE_BY_KEY = {
    "active_students_or_size": "diagnostic.ask_active_students",
    "main_pain": "diagnostic.ask_main_pain",
    "pain_detail": "diagnostic.ask_pain_detail",
    "current_process": "diagnostic.ask_current_process",
    "priority": "diagnostic.ask_priority",
    "urgency": "diagnostic.ask_urgency",
}

type RepairProviderOutput = ConductorTurnResult | Mapping[str, Any] | str
type RepairProvider = Callable[
    ["RepairProviderRequest"],
    RepairProviderOutput | Awaitable[RepairProviderOutput],
]


class RepairProviderRequest(StrictModel):
    request_schema_version: str = "011.repair_request.v1"
    context: TurnContext
    context_snapshot_json: str
    original_decision: ConductorDecision
    validator_errors: list[ValidationIssue]
    response_schema: dict[str, Any]
    max_attempts: int = 1
    instructions: list[str] = Field(default_factory=list)
    provider_requirements: list[str] = Field(default_factory=list)


async def repair_conductor_decision(
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
    *,
    provider: RepairProvider,
) -> RepairResult:
    if validator_result.status == "passed":
        return RepairResult()

    original_error_codes = _issue_codes(validator_result.errors)
    if _is_known_schema_version_alias(decision.schema_version):
        decision = decision.model_copy(
            update={"schema_version": CURRENT_CONDUCTOR_SCHEMA_VERSION},
            deep=True,
        )
        validator_result = validate_conductor_result(decision, context)
        if validator_result.status == "passed":
            return RepairResult(
                attempted=True,
                attempt_count=1,
                status="repaired",
                errors_sent=original_error_codes,
                repaired_decision=decision,
            )

    structural_repair = _repair_structural_cold_greeting(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_widget_empty_opening(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_entry_opening_consistency(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_diagnostic_cta_opening(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_first_turn_diagnostic_greeting(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_pain_first_offer(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_sensitive_data_safety(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_template_variable_sources(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_official_product_evidence(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_whatsapp_direct_answer(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_plan_fit_direct_answer(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_handoff_followup(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_missing_diagnostic_question(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_stale_completed_diagnostic_followup(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_how_it_works(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_stale_demo_followup(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_product_route_shape(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_demo_direct_flags(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_integration_scope_answer(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_diagnostic_refusal(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_price_objection_value(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_price_hook(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_stale_completed_diagnostic_followup(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_missing_diagnostic_question(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_final_diagnostic_demo_stage(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_waitlist_offer(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_policy_checks(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_how_it_works(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    if validator_result.status != "repairable" and not _blocked_result_can_use_llm_repair(
        validator_result
    ):
        return RepairResult(
            attempted=False,
            attempt_count=0,
            status="blocked",
            errors_sent=original_error_codes,
        )

    structural_repair = _repair_structural_how_it_works(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_diagnostic_feedback(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_missing_diagnostic_question(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    structural_repair = _repair_structural_final_diagnostic_demo_stage(
        decision=decision,
        context=context,
        validator_result=validator_result,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair

    request = _build_repair_request(
        context=context,
        original_decision=decision,
        validator_result=validator_result,
    )

    try:
        raw_output = await _call_repair_provider(provider, request)
        repaired_result = _parse_provider_result(raw_output)
    except (ConductorError, TypeError, ValueError) as error:
        return RepairResult(
            attempted=True,
            attempt_count=1,
            status="failed",
            errors_sent=[
                *original_error_codes,
                "repair_provider_output_invalid",
                error.__class__.__name__,
            ],
        )

    repaired_validation = validate_conductor_result(repaired_result.decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=1,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_result.decision,
            model_usage=repaired_result.model_usage,
        )

    structural_repair = _repair_structural_official_product_evidence(
        decision=repaired_result.decision,
        context=context,
        validator_result=repaired_validation,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair.model_copy(
            update={
                "attempt_count": 1,
                "errors_sent": sorted(
                    {
                        *original_error_codes,
                        *_issue_codes(repaired_validation.errors),
                    }
                ),
                "model_usage": repaired_result.model_usage,
            }
        )

    structural_repair = _repair_structural_stale_completed_diagnostic_followup(
        decision=repaired_result.decision,
        context=context,
        validator_result=repaired_validation,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair.model_copy(
            update={
                "attempt_count": 1,
                "errors_sent": sorted(
                    {
                        *original_error_codes,
                        *_issue_codes(repaired_validation.errors),
                    }
                ),
                "model_usage": repaired_result.model_usage,
            }
        )

    structural_repair = _repair_structural_final_diagnostic_demo_stage(
        decision=repaired_result.decision,
        context=context,
        validator_result=repaired_validation,
    )
    if structural_repair.attempted and structural_repair.status == "repaired":
        return structural_repair.model_copy(
            update={
                "attempt_count": 1,
                "errors_sent": sorted(
                    {
                        *original_error_codes,
                        *_issue_codes(repaired_validation.errors),
                    }
                ),
                "model_usage": repaired_result.model_usage,
            }
        )

    return RepairResult(
        attempted=True,
        attempt_count=1,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
        model_usage=repaired_result.model_usage,
    )


def _build_repair_request(
    *,
    context: TurnContext,
    original_decision: ConductorDecision,
    validator_result: ValidatorResult,
) -> RepairProviderRequest:
    snapshot = build_context_snapshot(context)
    registered_templates = _format_registered_template_catalog()
    fact_source_rules = _format_fact_source_rules()
    return RepairProviderRequest(
        context=context,
        context_snapshot_json=context_snapshot_to_json(snapshot),
        original_decision=original_decision,
        validator_errors=validator_result.errors,
        response_schema=build_conductor_response_schema(),
        instructions=[
            "Repair only the structured ConductorDecision JSON.",
            "Use the validator_errors as hard constraints.",
            "Return the same ConductorDecision schema and preserve context ids.",
            "Return a flat ConductorDecision object. language_policy, template_plan, "
            "policy_checks, waitlist, handoff, demo, facts, confidence, and repair_hints "
            "are top-level siblings of diagnostic, never nested inside diagnostic.",
            "Use only template ids from this registered catalog and include every required "
            f"variable for the chosen template. Catalog: {registered_templates}.",
            "Use diagnostic.price_hook for generic price questions. Use "
            "diagnostic.price_hook_with_context only when plan_fit_context is grounded "
            "in user_message or diagnostic_ledger evidence.",
            "If demo.next_step=offer_demo, include an approved demo offer template. "
            "For price-only turns, repair demo.status to not_offered and "
            "demo.next_step to none unless the user explicitly asked for the demo.",
            "If validator_errors include diagnostic_inferable_pain_detail_should_complete, "
            "infer pain_detail only from inbound text or diagnostic evidence, mark "
            "it inferred_from_prior_message, and complete the diagnostic with the "
            "staged diagnostic delivery templates.",
            "If validator_errors include diagnostic_next_question_invalid, choose only "
            "one mandatory diagnostic next_question_key or complete the diagnostic "
            "when the current inbound answers the pending final mandatory field.",
            "If validator_errors include diagnostic_urgency_answer_not_captured, "
            "capture the current inbound as the urgency answer with user_message "
            "evidence and complete the diagnostic when urgency is the final pending "
            "mandatory field.",
            "If validator_errors include unresolved_product_evidence or "
            "product_claim_source_missing, keep only official product variables "
            "grounded in context product_knowledge or approved Spec 006 keys; correct "
            "the evidence keys or choose a template plan that does not need that "
            "product claim.",
            "For completed diagnostics, use the staged diagnostic.deliver_* sequence. "
            "Never use the legacy exact template id diagnostic.deliver in template_plan.",
            "Keep completed diagnostic template variables concise; prefer one clear "
            "studio-owner sentence per staged template variable.",
            f"Allowed fact source/reliability pairs: {fact_source_rules}.",
            "Do not add customer-facing free-form text.",
            "Do not render, persist, deliver, hand off, or produce fallback copy.",
            "This is the only repair attempt for the turn.",
        ],
        provider_requirements=[
            "The LLM repair response must be only the repaired ConductorDecision JSON.",
            "Do not include model_usage, usage, response text, or wrapper/envelope fields "
            "inside the repaired ConductorDecision JSON.",
            "The runtime provider wrapper attaches model_usage from provider metadata "
            "after the repair response is received.",
            "Do not invent product facts or diagnostic answers.",
        ],
    )


def _repair_structural_official_product_evidence(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _OFFICIAL_PRODUCT_VARIABLE_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    changed = False
    repaired_items: list[RenderPlanItem] = []
    for item in repaired_decision.template_plan.items:
        variables = dict(item.variables)
        for variable_name, variable in item.variables.items():
            variable_update = _product_or_diagnostic_variable_repair(
                variable_name=variable_name,
                variable=variable,
                context=context,
            )
            if variable_update is None:
                continue
            variables[variable_name] = variable.model_copy(update=variable_update)
            changed = True
        repaired_items.append(item.model_copy(update={"variables": variables}))

    if not changed:
        if not _FINAL_DIAGNOSTIC_STAGE_REPAIR_CODES.intersection(original_error_codes):
            return RepairResult()

    repaired_decision.template_plan = repaired_decision.template_plan.model_copy(
        update={"items": repaired_items}
    )
    if _FINAL_DIAGNOSTIC_STAGE_REPAIR_CODES.intersection(original_error_codes):
        normalized_items = _normalized_final_diagnostic_items(repaired_decision, context)
        if normalized_items is None:
            return RepairResult()
        repaired_decision.template_plan = repaired_decision.template_plan.model_copy(
            update={"items": normalized_items}
        )
        changed = True

    if not changed:
        return RepairResult()

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=0,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=0,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _repair_structural_final_diagnostic_demo_stage(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _FINAL_DIAGNOSTIC_STAGE_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_decision.role = "diagnostic"
    repaired_decision.route = "diagnostic"
    repaired_decision.current_state = "diagnostic_completed"
    repaired_decision.next_state = "diagnostic_completed"
    repaired_decision.diagnostic = repaired_decision.diagnostic.model_copy(
        update={"action": "complete", "next_question_key": None}
    )
    repaired_decision.demo = repaired_decision.demo.model_copy(
        update={
            "status": repaired_decision.demo.status,
            "next_step": repaired_decision.demo.next_step,
        }
    )
    repaired_items = _normalized_final_diagnostic_items(repaired_decision, context)
    if repaired_items is None:
        return RepairResult()
    repaired_decision.template_plan = repaired_decision.template_plan.model_copy(
        update={"items": repaired_items}
    )

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=0,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=0,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _repair_structural_cold_greeting(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _COLD_GREETING_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_decision.role = "entry"
    repaired_decision.route = "entry"
    repaired_decision.current_state = "greeting_only"
    repaired_decision.next_state = "greeting_only"
    repaired_decision.detected_intents = ["greeting"]
    repaired_decision.direct_question_present = False
    repaired_decision.direct_question_answered_first = True
    repaired_decision.facts = []
    repaired_decision.numeric_interpretations = []
    repaired_decision.diagnostic = DiagnosticDecision()
    repaired_decision.demo = DemoDecision()
    repaired_decision.waitlist = WaitlistDecision()
    repaired_decision.handoff = HandoffDecision()
    repaired_decision.policy_checks = repaired_decision.policy_checks.model_copy(
        update={
            "direct_question_answered_first": True,
            "diagnostic_timing_ok": True,
            "waitlist_timing_ok": True,
            "official_facts_only": True,
            "no_internal_text_leak": True,
            "no_early_contact_capture": True,
            "no_human_overlap": True,
        }
    )

    first_name = _reliable_profile_first_name(context)
    if first_name:
        item = RenderPlanItem(
            template_id="opening.cold_greeting_named",
            channel=context.channel,
            variables={
                "first_name": TemplateVariableValue(
                    kind="short_text",
                    value=first_name,
                    source="channel_metadata",
                    evidence=["sender.name"],
                    max_length=40,
                )
            },
        )
    else:
        item = RenderPlanItem(
            template_id="opening.cold_greeting",
            channel=context.channel,
            variables={},
        )
    repaired_decision.template_plan = RenderPlan(items=[item], chunk_policy="none")

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=0,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=0,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _repair_structural_widget_empty_opening(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _WIDGET_EMPTY_OPENING_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_decision.role = "entry"
    repaired_decision.route = "entry"
    repaired_decision.current_state = "widget_opening"
    repaired_decision.next_state = "diagnostic_offered"
    repaired_decision.detected_intents = ["widget_empty_opening", "diagnostic_offer"]
    repaired_decision.direct_question_present = False
    repaired_decision.direct_question_answered_first = True
    repaired_decision.facts = []
    repaired_decision.numeric_interpretations = []
    repaired_decision.diagnostic = DiagnosticDecision(action="offer")
    repaired_decision.demo = DemoDecision()
    repaired_decision.waitlist = WaitlistDecision()
    repaired_decision.handoff = HandoffDecision()
    repaired_decision.policy_checks = repaired_decision.policy_checks.model_copy(
        update={
            "direct_question_answered_first": True,
            "diagnostic_timing_ok": True,
            "waitlist_timing_ok": True,
            "official_facts_only": True,
            "no_internal_text_leak": True,
            "no_early_contact_capture": True,
            "no_human_overlap": True,
        }
    )
    repaired_decision.template_plan = RenderPlan(
        items=[
            RenderPlanItem(
                template_id="opening.widget_empty_diagnostic",
                channel=context.channel,
                variables={},
            )
        ],
        chunk_policy="none",
    )

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=0,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=0,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _repair_structural_entry_opening_consistency(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _ENTRY_OPENING_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_decision.role = "entry"
    repaired_decision.route = "entry"
    repaired_decision.waitlist = WaitlistDecision()
    repaired_decision.diagnostic = repaired_decision.diagnostic.model_copy(
        update={"action": "offer", "next_question_key": None}
    )
    repaired_decision.policy_checks = repaired_decision.policy_checks.model_copy(
        update={
            "diagnostic_timing_ok": True,
            "waitlist_timing_ok": True,
            "no_early_contact_capture": True,
            "no_human_overlap": True,
        }
    )

    if "instagram_source_opening_template_missing" in original_error_codes:
        repaired_decision.current_state = "social_source_opening"
        repaired_decision.next_state = "diagnostic_offered"
        repaired_decision.template_plan = RenderPlan(
            items=[
                RenderPlanItem(
                    template_id="opening.instagram_source",
                    channel=context.channel,
                    variables={},
                )
            ],
            chunk_policy="whatsapp_max_3" if context.channel == "whatsapp" else "default",
        )

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=0,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=0,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _repair_structural_diagnostic_cta_opening(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _DIAGNOSTIC_CTA_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_decision.role = "diagnostic"
    repaired_decision.route = "diagnostic"
    repaired_decision.current_state = "diagnostic_opening"
    repaired_decision.next_state = "diagnostic_in_progress"
    if repaired_decision.direct_question_present:
        repaired_decision.direct_question_answered_first = True
    if repaired_decision.diagnostic.action == "none":
        repaired_decision.diagnostic = repaired_decision.diagnostic.model_copy(
            update={"action": "start", "next_question_key": "active_students_or_size"}
        )

    items = list(repaired_decision.template_plan.items)
    if not any(item.template_id == "opening.diagnostic_cta" for item in items):
        items.insert(
            0,
            RenderPlanItem(
                template_id="opening.diagnostic_cta",
                channel=context.channel,
                variables={},
            ),
        )
    items = [
        item
        for item in items
        if item.template_id.split("#", 1)[0] != "diagnostic.start"
    ]
    if not any(
        item.template_id.split("#", 1)[0] in _DIAGNOSTIC_QUESTION_TEMPLATE_IDS
        for item in items
    ):
        repaired_decision.diagnostic = repaired_decision.diagnostic.model_copy(
            update={"action": "start", "next_question_key": "active_students_or_size"}
        )
        items.append(
            RenderPlanItem(
                template_id="diagnostic.ask_active_students",
                channel=context.channel,
                variables={},
            )
        )
    repaired_decision.template_plan = repaired_decision.template_plan.model_copy(
        update={"items": items}
    )
    _apply_diagnostic_feedback(repaired_decision)

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=0,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=0,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _repair_structural_first_turn_diagnostic_greeting(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _FIRST_TURN_DIAGNOSTIC_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    items = list(repaired_decision.template_plan.items)
    items.insert(
        0,
        RenderPlanItem(
            template_id="opening.cold_greeting",
            channel=context.channel,
            variables={},
        ),
    )
    repaired_decision.template_plan = repaired_decision.template_plan.model_copy(
        update={"items": items}
    )
    _apply_diagnostic_feedback(repaired_decision)

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=0,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=0,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _repair_structural_pain_first_offer(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _PAIN_FIRST_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_decision.role = "diagnostic"
    repaired_decision.route = "diagnostic"
    repaired_decision.current_state = "pain_first_diagnostic_offer"
    repaired_decision.next_state = "diagnostic_offered"
    repaired_decision.diagnostic = DiagnosticDecision(
        action="offer",
        next_question_key="active_students_or_size",
    )
    repaired_decision.waitlist = WaitlistDecision()
    repaired_decision.template_plan = RenderPlan(
        items=[
            RenderPlanItem(
                template_id="opening.cold_greeting",
                channel=context.channel,
                variables={},
            ),
            RenderPlanItem(
                template_id="diagnostic.offer_soft",
                channel=context.channel,
                variables={
                    "pain_context_human": TemplateVariableValue(
                        kind="long_text",
                        value=f"Entendi: {_inbound_text(context)}",
                        source="user_message",
                        evidence=_diagnostic_evidence(context),
                        max_length=320,
                    )
                },
            ),
            RenderPlanItem(
                template_id="diagnostic.ask_active_students",
                channel=context.channel,
                variables={},
            ),
        ],
        chunk_policy="whatsapp_max_3" if context.channel == "whatsapp" else "default",
    )

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=0,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=0,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _repair_structural_sensitive_data_safety(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _SENSITIVE_DATA_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()

    template_ids = {
        item.template_id.split("#", 1)[0]
        for item in decision.template_plan.items
    }
    intents = " ".join(decision.detected_intents).casefold()
    if (
        "sensitive" not in intents
        and "cpf" not in intents
        and "personal_data" not in intents
        and "safety.sensitive_data" not in template_ids
    ):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_decision.role = "safety"
    repaired_decision.route = "safe_fallback"
    repaired_decision.current_state = "sensitive_data_blocked"
    repaired_decision.next_state = "sensitive_data_blocked"
    repaired_decision.direct_question_answered_first = True
    repaired_decision.facts = []
    repaired_decision.numeric_interpretations = []
    repaired_decision.diagnostic = DiagnosticDecision(action="none")
    repaired_decision.demo = DemoDecision()
    repaired_decision.waitlist = WaitlistDecision()
    repaired_decision.handoff = HandoffDecision()
    repaired_decision.policy_checks = repaired_decision.policy_checks.model_copy(
        update={
            "direct_question_answered_first": True,
            "diagnostic_timing_ok": True,
            "waitlist_timing_ok": True,
            "official_facts_only": True,
            "no_internal_text_leak": True,
            "no_early_contact_capture": True,
            "no_human_overlap": True,
        }
    )
    repaired_decision.template_plan = RenderPlan(
        items=[
            RenderPlanItem(
                template_id="safety.sensitive_data",
                channel=context.channel,
                variables={},
            )
        ],
        chunk_policy="none",
    )

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=0,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=0,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _repair_structural_template_variable_sources(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if "template_plan_invalid" not in original_error_codes:
        return RepairResult()
    if not any(
        issue.message.startswith("source_not_allowed:")
        for issue in validator_result.errors
    ):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_items: list[RenderPlanItem] = []
    changed = False
    for item in repaired_decision.template_plan.items:
        variables = dict(item.variables)
        for variable_name, variable in item.variables.items():
            update = _allowed_source_repair(
                variable_name=variable_name,
                variable=variable,
                decision=repaired_decision,
                context=context,
            )
            if update is None:
                continue
            variables[variable_name] = variable.model_copy(update=update)
            changed = True
        repaired_items.append(item.model_copy(update={"variables": variables}))

    if not changed:
        return RepairResult()

    repaired_decision.template_plan = repaired_decision.template_plan.model_copy(
        update={"items": repaired_items}
    )
    if not _decision_has_product_source_variables(repaired_decision):
        repaired_decision.policy_checks = repaired_decision.policy_checks.model_copy(
            update={"official_facts_only": False}
        )
    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=0,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=0,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _allowed_source_repair(
    *,
    variable_name: str,
    variable: TemplateVariableValue,
    decision: ConductorDecision,
    context: TurnContext,
) -> dict[str, Any] | None:
    variable_spec = VARIABLE_REGISTRY.get(variable_name)
    if variable_spec is None or variable.source in variable_spec.allowed_sources:
        return None

    if (
        variable_name == "answer_feedback"
        and "diagnostic_ledger" in variable_spec.allowed_sources
    ):
        feedback = _diagnostic_feedback_from_ledger(decision)
        if feedback is None:
            feedback = _diagnostic_feedback_from_context(context)
        if feedback is not None:
            return feedback.model_dump(mode="python")

    for source in (
        "user_message",
        "diagnostic_ledger",
        "runtime_state",
        "model_decision",
        "channel_metadata",
        "official_product_knowledge",
        "spec_006_product_contract",
    ):
        if source not in variable_spec.allowed_sources:
            continue
        evidence = _evidence_for_allowed_source(
            source=source,
            variable_name=variable_name,
            context=context,
        )
        if not evidence:
            continue
        return {"source": source, "evidence": evidence}

    return None


def _evidence_for_allowed_source(
    *,
    source: str,
    variable_name: str,
    context: TurnContext,
) -> list[str]:
    inbound_text = _inbound_text(context)
    if source == "user_message":
        return [inbound_text] if inbound_text else []
    if source == "diagnostic_ledger":
        return _diagnostic_evidence(context)
    if source == "runtime_state":
        return [f"runtime_state.{variable_name}"]
    if source == "model_decision":
        return ["model_decision"]
    if source == "channel_metadata":
        return ["sender.name"]
    return []


def _diagnostic_feedback_from_context(
    context: TurnContext,
) -> TemplateVariableValue | None:
    for item in context.diagnostic_ledger:
        if not isinstance(item, Mapping):
            continue
        status = str(item.get("status") or "")
        answer = str(item.get("answer_value") or "").strip()
        if status not in {"answered", "inferred_from_prior_message", "not_applicable"}:
            continue
        if not answer:
            continue
        evidence = [
            str(value)
            for value in item.get("evidence", [])
            if str(value).strip()
        ]
        return TemplateVariableValue(
            kind="short_text",
            value=_short_feedback(answer),
            source="diagnostic_ledger",
            evidence=evidence or [f"diagnostic.{item.get('question_key') or 'answer'}"],
            max_length=180,
        )
    return None


def _decision_has_product_source_variables(decision: ConductorDecision) -> bool:
    return any(
        variable.source in _PRODUCT_KNOWLEDGE_SOURCES
        for item in decision.template_plan.items
        for variable in item.variables.values()
    )


def _has_user_grounding_evidence(evidence: list[str]) -> bool:
    return any(
        item.strip()
        and not item.startswith("product_knowledge.")
        and not item.startswith("spec006.")
        and not item.startswith("specs/006-")
        for item in evidence
    )


def _drop_ungrounded_diagnostic_updates(decision: ConductorDecision) -> bool:
    kept_updates: list[DiagnosticLedgerItem] = []
    changed = False
    for update in decision.diagnostic.ledger_updates:
        if update.status in _DIAGNOSTIC_EVIDENCE_STATUSES and not _has_user_grounding_evidence(
            update.evidence
        ):
            changed = True
            continue
        kept_updates.append(update)

    if changed:
        decision.diagnostic = decision.diagnostic.model_copy(
            update={"ledger_updates": kept_updates}
        )
    return changed


def _reliable_profile_first_name(context: TurnContext) -> str | None:
    for fact in context.facts:
        if fact.key != "profile_name" or fact.source != "channel_metadata":
            continue
        assessment = assess_profile_name(str(fact.value or ""))
        if assessment.status == "reliable":
            return assessment.first_name
    return None


def _repair_structural_whatsapp_direct_answer(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _WHATSAPP_DIRECT_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()

    demo_link = _official_demo_link(context)
    if demo_link is None:
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_items: list[RenderPlanItem] = []
    changed = False
    for item in repaired_decision.template_plan.items:
        if item.template_id.split("#", 1)[0] != "product.whatsapp_direct":
            if item.template_id.split("#", 1)[0].startswith("diagnostic."):
                changed = True
                continue
            repaired_items.append(item)
            continue
        variables = dict(item.variables)
        variables["product_fact_summary"] = TemplateVariableValue(
            kind="long_text",
            value=(
                "O aluno nao precisa baixar aplicativo nem criar senha. "
                "Ele conversa no WhatsApp; a Taliya registra a acao, "
                "atualiza o painel e avisa o responsavel."
            ),
            source="official_product_knowledge",
            evidence=["product_knowledge.whatsapp_scope"],
            max_length=320,
        )
        variables["official_demo_link"] = TemplateVariableValue(
            kind="url",
            value=demo_link,
            source="official_product_knowledge",
            evidence=["product_knowledge.links.demonstration"],
        )
        repaired_items.append(item.model_copy(update={"variables": variables}))
        changed = True

    if not changed:
        return RepairResult()

    repaired_decision.template_plan = repaired_decision.template_plan.model_copy(
        update={"items": repaired_items}
    )
    if "diagnostic_answer_evidence_missing" in original_error_codes:
        _drop_ungrounded_diagnostic_updates(repaired_decision)

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=0,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=0,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _repair_structural_plan_fit_direct_answer(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _PLAN_FIT_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()
    if not (
        {
            "plan_recommendation",
            "price_fit_question",
            "pricing_fit",
            "plan_fit_question",
            "plan_question",
        }.intersection(decision.detected_intents)
        or any(
            item.template_id.split("#", 1)[0] == "product.plan_fit_with_diagnostic"
            for item in decision.template_plan.items
        )
    ):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_decision.role = "product"
    repaired_decision.route = "product"
    repaired_decision.current_state = "plan_fit_question"
    repaired_decision.next_state = "diagnostic_offered"
    repaired_decision.detected_intents = ["plan_fit_question"]
    repaired_decision.direct_question_present = True
    repaired_decision.direct_question_answered_first = True
    repaired_decision.diagnostic = repaired_decision.diagnostic.model_copy(
        update={"action": "offer", "next_question_key": None}
    )
    repaired_decision.policy_checks = repaired_decision.policy_checks.model_copy(
        update={
            "direct_question_answered_first": True,
            "diagnostic_timing_ok": True,
            "waitlist_timing_ok": True,
            "official_facts_only": False,
            "no_internal_text_leak": True,
            "no_early_contact_capture": True,
            "no_human_overlap": True,
        }
    )
    repaired_decision.template_plan = RenderPlan(
        items=[
            RenderPlanItem(
                template_id="product.plan_fit_with_diagnostic",
                channel=context.channel,
                variables={
                    "plan_fit_context": TemplateVariableValue(
                        kind="short_text",
                        value=(
                            "Nao quero chutar um plano sem entender tamanho, "
                            "dor principal e prioridade do studio."
                        ),
                        source="user_message",
                        evidence=_diagnostic_evidence(context),
                        max_length=180,
                    )
                },
            )
        ],
        chunk_policy="default",
    )

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=0,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=0,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _repair_structural_product_route_shape(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _PRODUCT_ROUTE_SHAPE_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()
    if (
        "diagnostic_final_demo_stage_missing" in original_error_codes
        and not _has_current_demo_request_signal(decision, context)
        and not {
            "demo_direct_requires_product_route",
            "demo_offer_template_missing",
            "post_diagnostic_demo_request_redelivered_diagnostic",
            "post_diagnostic_demo_request_template_missing",
        }.intersection(original_error_codes)
    ):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_decision.role = "product"
    repaired_decision.route = "product"
    repaired_decision.direct_question_present = True
    repaired_decision.direct_question_answered_first = True
    if "duplicate_diagnostic_offer_templates" in original_error_codes:
        seen_offer = False
        repaired_items: list[RenderPlanItem] = []
        for item in repaired_decision.template_plan.items:
            template_id = item.template_id.split("#", 1)[0]
            if template_id in {
                "diagnostic.offer_soft",
                "diagnostic.price_hook",
                "diagnostic.price_hook_with_context",
                "product.plan_fit_with_diagnostic",
            }:
                if seen_offer:
                    continue
                seen_offer = True
            repaired_items.append(item)
        repaired_decision.template_plan = repaired_decision.template_plan.model_copy(
            update={"items": repaired_items}
        )
    repaired_decision.policy_checks = repaired_decision.policy_checks.model_copy(
        update={
            "direct_question_answered_first": True,
            "diagnostic_timing_ok": True,
            "waitlist_timing_ok": True,
            "official_facts_only": False,
            "no_early_contact_capture": True,
            "no_human_overlap": True,
        }
    )
    if {
        "demo_offer_template_missing",
        "diagnostic_final_demo_stage_missing",
        "post_diagnostic_demo_request_redelivered_diagnostic",
        "post_diagnostic_demo_request_template_missing",
    }.intersection(original_error_codes):
        demo_link = _official_demo_link(context)
        if demo_link is None:
            return RepairResult()
        repaired_decision.role = "product"
        repaired_decision.route = "product"
        repaired_decision.current_state = "demo_question"
        repaired_decision.next_state = "demo_offered"
        repaired_decision.detected_intents = [
            *[
                intent
                for intent in repaired_decision.detected_intents
                if "diagnostic" not in intent.lower()
            ],
            "demo_request",
        ]
        repaired_decision.diagnostic = DiagnosticDecision()
        repaired_decision.waitlist = WaitlistDecision()
        repaired_decision.handoff = HandoffDecision()
        repaired_decision.demo = repaired_decision.demo.model_copy(
            update={"status": "viewed_or_asked", "next_step": "offer_demo"}
        )
        repaired_decision.policy_checks = repaired_decision.policy_checks.model_copy(
            update={
                "direct_question_answered_first": True,
                "diagnostic_timing_ok": True,
                "waitlist_timing_ok": True,
                "official_facts_only": True,
                "no_early_contact_capture": True,
                "no_human_overlap": True,
            }
        )
        repaired_decision.template_plan = RenderPlan(
            items=[
                RenderPlanItem(
                    template_id="product.demo_direct",
                    channel=context.channel,
                    variables={
                        "official_demo_link": TemplateVariableValue(
                            kind="url",
                            value=demo_link,
                            source="official_product_knowledge",
                            evidence=["product_knowledge.links.demonstration"],
                        )
                    },
                )
            ],
            chunk_policy="whatsapp_max_3" if context.channel == "whatsapp" else "default",
        )

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=0,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=0,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _repair_structural_handoff_followup(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _HANDOFF_FOLLOWUP_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()
    if not _has_handoff_signal(decision):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_decision.role = "handoff"
    repaired_decision.route = "handoff"
    repaired_decision.current_state = "human_requested"
    repaired_decision.next_state = "handoff_active"
    repaired_decision.direct_question_present = False
    repaired_decision.direct_question_answered_first = False
    repaired_decision.diagnostic = DiagnosticDecision()
    repaired_decision.demo = DemoDecision()
    repaired_decision.handoff = HandoffDecision(
        status="requested",
        reason=_handoff_reason(decision, context),
    )
    repaired_decision.policy_checks = repaired_decision.policy_checks.model_copy(
        update={
            "direct_question_answered_first": True,
            "diagnostic_timing_ok": True,
            "waitlist_timing_ok": True,
            "official_facts_only": False,
            "no_early_contact_capture": True,
            "no_human_overlap": True,
        }
    )
    reason = _handoff_reason(decision, context)
    repaired_decision.template_plan = RenderPlan(
        items=[
            RenderPlanItem(
                template_id="handoff.acknowledge",
                channel=context.channel,
                variables={
                    "handoff_reason": TemplateVariableValue(
                        kind="short_text",
                        value=reason,
                        source="user_message",
                        evidence=[_inbound_text(context) or reason],
                        max_length=120,
                    )
                },
            )
        ],
        chunk_policy="whatsapp_max_3" if context.channel == "whatsapp" else "default",
    )

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=0,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=0,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _has_handoff_signal(decision: ConductorDecision) -> bool:
    intents = {intent.lower() for intent in decision.detected_intents}
    template_ids = {
        item.template_id.split("#", 1)[0]
        for item in decision.template_plan.items
    }
    return (
        decision.handoff.status in {"requested", "active"}
        or "handoff.acknowledge" in template_ids
        or any("handoff" in intent or "human" in intent for intent in intents)
    )


def _handoff_reason(decision: ConductorDecision, context: TurnContext) -> str:
    reason = str(decision.handoff.reason or "").strip()
    if reason:
        return reason[:120]
    inbound = _inbound_text(context).strip()
    if inbound:
        return inbound[:120]
    return "lead_requested_human"


def _repair_structural_stale_completed_diagnostic_followup(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _STALE_COMPLETED_DIAGNOSTIC_FOLLOWUP_REPAIR_CODES.intersection(
        original_error_codes
    ):
        return RepairResult()
    if "stale_demo_direct_without_current_request" in original_error_codes:
        return RepairResult()
    if decision.diagnostic.action != "complete":
        return RepairResult()
    if not _context_diagnostic_completed(context):
        return RepairResult()
    if _has_final_diagnostic_delivery_template(decision):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_decision.diagnostic = DiagnosticDecision()
    route = _route_from_followup_templates(repaired_decision)
    if route is not None:
        repaired_decision.role = route
        repaired_decision.route = route
    if route in {"waitlist", "handoff"}:
        repaired_decision.demo = DemoDecision()
    repaired_decision.policy_checks = repaired_decision.policy_checks.model_copy(
        update={"diagnostic_timing_ok": True}
    )

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=0,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=0,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _repair_structural_stale_demo_followup(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _STALE_DEMO_FOLLOWUP_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()
    if not _context_diagnostic_completed(context):
        return RepairResult()
    if _has_current_demo_request_signal(decision, context):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_decision.demo = DemoDecision()
    repaired_items = [
        item
        for item in repaired_decision.template_plan.items
        if item.template_id.split("#", 1)[0] != "product.demo_direct"
    ]
    if (
        repaired_decision.diagnostic.action == "complete"
        and not _has_final_diagnostic_delivery_template(repaired_decision)
    ):
        repaired_decision.diagnostic = DiagnosticDecision()

    inbound_price_objection = _inbound_has_price_objection_signal(context)
    if inbound_price_objection and not _has_price_objection_intent(repaired_decision):
        non_demo_intents = [
            intent
            for intent in repaired_decision.detected_intents
            if "demo" not in intent.lower() and "demonstr" not in intent.lower()
        ]
        repaired_decision.detected_intents = [*non_demo_intents, "price_objection"]

    if _has_price_objection_intent(repaired_decision):
        repaired_decision.role = "product"
        repaired_decision.route = "product"
        repaired_decision.current_state = "product_price_objection"
        repaired_decision.next_state = "product_followup"
        repaired_decision.diagnostic = DiagnosticDecision()
        repaired_items = [
            item
            for item in repaired_items
            if not item.template_id.split("#", 1)[0].startswith("diagnostic.deliver")
        ]
        has_price_answer = any(
            item.template_id.split("#", 1)[0] in _PRICE_ANSWER_TEMPLATE_IDS
            for item in repaired_items
        )
        if not has_price_answer:
            official_price_summary = _official_price_summary(context)
            if official_price_summary is not None:
                repaired_items.insert(
                    0,
                    RenderPlanItem(
                        template_id="product.price_direct",
                        channel=context.channel,
                        variables={"plan_price_summary": official_price_summary},
                    ),
                )
        repaired_items = _with_price_objection_value_item(
            repaired_items,
            context=context,
        )
        repaired_decision.direct_question_present = True
        repaired_decision.direct_question_answered_first = True
        repaired_decision.policy_checks = repaired_decision.policy_checks.model_copy(
            update={"direct_question_answered_first": True}
        )

    repaired_decision.template_plan = repaired_decision.template_plan.model_copy(
        update={"items": repaired_items}
    )
    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=0,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=0,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _has_current_demo_request_signal(
    decision: ConductorDecision,
    context: TurnContext,
) -> bool:
    if not _inbound_has_demo_request_signal(context):
        return False
    intents = {intent.lower() for intent in decision.detected_intents}
    return (
        any("demo" in intent or "demonstr" in intent for intent in intents)
        or decision.demo.next_step == "offer_demo"
        or decision.demo.status in {"viewed_or_asked", "reacted_positive"}
        or any(
            item.template_id.split("#", 1)[0] == "product.demo_direct"
            for item in decision.template_plan.items
        )
    )


def _context_diagnostic_completed(context: TurnContext) -> bool:
    if context.sales_inbox_inputs.get("diagnostic_status") == "completed":
        return True
    statuses: dict[str, str] = {}
    for item in context.diagnostic_ledger:
        if not isinstance(item, dict):
            continue
        key = str(item.get("question_key") or "")
        status = str(item.get("status") or "")
        if key:
            statuses[key] = status
    return bool(statuses) and all(
        statuses.get(key) in _DIAGNOSTIC_EVIDENCE_STATUSES
        for key in _REQUIRED_DIAGNOSTIC_ORDER
    )


def _has_final_diagnostic_delivery_template(decision: ConductorDecision) -> bool:
    return any(
        item.template_id.split("#", 1)[0].startswith("diagnostic.deliver")
        for item in decision.template_plan.items
    )


def _route_from_followup_templates(decision: ConductorDecision) -> str | None:
    template_ids = {
        item.template_id.split("#", 1)[0]
        for item in decision.template_plan.items
    }
    if any(template_id.startswith("waitlist.") for template_id in template_ids):
        return "waitlist"
    if any(template_id.startswith("handoff.") for template_id in template_ids):
        return "handoff"
    if any(template_id.startswith("product.") for template_id in template_ids):
        return "product"
    return None


def _inbound_has_demo_request_signal(context: TurnContext) -> bool:
    normalized = _normalize_text(_inbound_text(context))
    return any(marker in normalized for marker in _CURRENT_DEMO_REQUEST_MARKERS)


def _inbound_has_price_objection_signal(context: TurnContext) -> bool:
    normalized = _normalize_text(_inbound_text(context))
    return any(marker in normalized for marker in _PRICE_OBJECTION_INBOUND_MARKERS)


def _normalized_final_diagnostic_items(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[RenderPlanItem] | None:
    existing_items = list(decision.template_plan.items)
    agent_items = _items_for_template(
        existing_items,
        "diagnostic.deliver_agent_recommendation",
    ) or _default_agent_items_from_diagnostic(decision, context)
    plan_item = _repaired_or_default_plan_item(existing_items, decision, context)

    if not agent_items or plan_item is None:
        return None

    context_item = _first_item_for_template(
        existing_items,
        "diagnostic.deliver_context",
    ) or _default_diagnostic_context_item(context)
    crm_item = _first_item_for_template(
        existing_items,
        "diagnostic.deliver_crm_base",
    ) or _default_diagnostic_crm_base_item(context)
    operational_item = _first_item_for_template(
        existing_items,
        "diagnostic.deliver_operational_step",
    ) or _default_diagnostic_operational_step_item(context)
    demo_item = _first_existing_demo_item(existing_items) or _final_diagnostic_demo_item(
        decision,
        context,
    )

    return [
        _first_item_for_template(existing_items, "diagnostic.deliver_hold")
        or RenderPlanItem(template_id="diagnostic.deliver_hold", channel=context.channel),
        context_item,
        crm_item,
        operational_item,
        *agent_items,
        plan_item,
        demo_item,
    ]


def _first_item_for_template(
    items: list[RenderPlanItem],
    template_id: str,
) -> RenderPlanItem | None:
    for item in items:
        if item.template_id.split("#", 1)[0] == template_id:
            return item
    return None


def _items_for_template(
    items: list[RenderPlanItem],
    template_id: str,
) -> list[RenderPlanItem]:
    return [
        item
        for item in items
        if item.template_id.split("#", 1)[0] == template_id
    ]


def _first_existing_demo_item(items: list[RenderPlanItem]) -> RenderPlanItem | None:
    for item in items:
        if item.template_id.split("#", 1)[0] in {
            "diagnostic.deliver_demo_not_offered",
            "diagnostic.deliver_demo_already_offered",
        }:
            return item
    return None


def _default_diagnostic_context_item(context: TurnContext) -> RenderPlanItem:
    return RenderPlanItem(
        template_id="diagnostic.deliver_context",
        channel=context.channel,
        variables={
            "pain_context_human": TemplateVariableValue(
                kind="long_text",
                value=(
                    "Pelo que voce contou, o principal peso esta na rotina "
                    "comercial e nos follow-ups que dependem de controle manual."
                ),
                source="diagnostic_ledger",
                evidence=_diagnostic_evidence(context),
                max_length=420,
            )
        },
    )


def _default_diagnostic_crm_base_item(context: TurnContext) -> RenderPlanItem:
    return RenderPlanItem(
        template_id="diagnostic.deliver_crm_base",
        channel=context.channel,
        variables={
            "crm_base_recommendation": TemplateVariableValue(
                kind="long_text",
                value=(
                    "Antes dos agentes, eu organizaria contatos, conversas, "
                    "situacao de cada interessado e proximos passos em uma base unica."
                ),
                source="diagnostic_ledger",
                evidence=_diagnostic_evidence(context),
                max_length=260,
            )
        },
    )


def _default_diagnostic_operational_step_item(context: TurnContext) -> RenderPlanItem:
    return RenderPlanItem(
        template_id="diagnostic.deliver_operational_step",
        channel=context.channel,
        variables={
            "operational_first_step": TemplateVariableValue(
                kind="long_text",
                value=(
                    "O primeiro passo e separar novos interessados, retornos "
                    "pendentes e conversas paradas para a equipe saber onde agir."
                ),
                source="diagnostic_ledger",
                evidence=_diagnostic_evidence(context),
                max_length=240,
            )
        },
    )


def _default_agent_items_from_diagnostic(
    decision: ConductorDecision,
    context: TurnContext,
) -> list[RenderPlanItem]:
    evidence = _diagnostic_evidence(context)
    evidence_text = _normalize_text(" ".join(evidence))
    selected = [
        display_name
        for normalized_name, display_name in _official_agent_name_map(context).items()
        if normalized_name in evidence_text
    ]
    if not selected:
        return []
    return [
        _default_agent_item(
            agent_name=agent_name,
            index=index,
            context=context,
            evidence=evidence,
        )
        for index, agent_name in enumerate(selected[:2])
    ]


def _default_agent_item(
    *,
    agent_name: str,
    index: int,
    context: TurnContext,
    evidence: list[str],
) -> RenderPlanItem:
    return RenderPlanItem(
        template_id=(
            "diagnostic.deliver_agent_recommendation"
            if index == 0
            else f"diagnostic.deliver_agent_recommendation#{index + 1}"
        ),
        channel=context.channel,
        variables={
            "agent_name": TemplateVariableValue(
                kind="short_text",
                value=agent_name,
                source="official_product_knowledge",
                evidence=["product_knowledge.plans"],
                max_length=60,
            ),
            "agent_fit_phrase": TemplateVariableValue(
                kind="enum",
                value="faria sentido primeiro" if index == 0 else "tambem faria sentido",
                source="model_decision",
                evidence=["model_decision"],
            ),
            "agent_pain_resolved": TemplateVariableValue(
                kind="long_text",
                value="a rotina citada no diagnostico",
                source="diagnostic_ledger",
                evidence=evidence,
                max_length=180,
            ),
            "agent_recommendation_reason": TemplateVariableValue(
                kind="long_text",
                value="essa rotina apareceu nas respostas do diagnostico",
                source="diagnostic_ledger",
                evidence=evidence,
                max_length=280,
            ),
            "agent_practical_action": TemplateVariableValue(
                kind="long_text",
                value="ajuda a organizar proximos passos e evitar conversas paradas",
                source="diagnostic_ledger",
                evidence=evidence,
                max_length=280,
            ),
        },
    )


def _default_plan_item_from_diagnostic(
    decision: ConductorDecision,
    context: TurnContext,
) -> RenderPlanItem | None:
    raw_value = (
        decision.diagnostic.final_fields.get("final_plan_or_range")
        or decision.diagnostic.final_fields.get("recommended_plan_or_range")
        or " ".join(_diagnostic_evidence(context))
    )
    plan_value = _canonical_official_plan_value(raw_value, context)
    if plan_value is None:
        plan_value = _plan_value_from_mentioned_agents(context)
    if plan_value is None:
        return None
    return RenderPlanItem(
        template_id="diagnostic.deliver_plan_recommendation",
        channel=context.channel,
        variables={
            "recommended_plan_or_range": TemplateVariableValue(
                kind="short_text",
                value=plan_value,
                source="official_product_knowledge",
                evidence=["product_knowledge.plans"],
                max_length=90,
            )
        },
    )


def _plan_value_from_mentioned_agents(context: TurnContext) -> str | None:
    evidence_text = _normalize_text(" ".join(_diagnostic_evidence(context)))
    mentioned_agents = [
        name
        for name in _official_agent_name_map(context)
        if name in evidence_text
    ]
    plan_names = _official_plan_names(context)
    if len(mentioned_agents) >= 2 and "avance" in plan_names:
        return plan_names["avance"]
    if len(mentioned_agents) == 1 and "essencial" in plan_names:
        return plan_names["essencial"]
    return None


def _repaired_or_default_plan_item(
    existing_items: list[RenderPlanItem],
    decision: ConductorDecision,
    context: TurnContext,
) -> RenderPlanItem | None:
    existing_plan_item = _first_item_for_template(
        existing_items,
        "diagnostic.deliver_plan_recommendation",
    )
    if existing_plan_item is not None:
        variable = existing_plan_item.variables.get("recommended_plan_or_range")
        if variable is not None:
            plan_value = _canonical_official_plan_value(variable.value, context)
            if plan_value is not None:
                variables = dict(existing_plan_item.variables)
                variables["recommended_plan_or_range"] = variable.model_copy(
                    update={
                        "value": plan_value,
                        "source": "official_product_knowledge",
                        "evidence": ["product_knowledge.plans"],
                    }
                )
                return existing_plan_item.model_copy(update={"variables": variables})

    return _default_plan_item_from_diagnostic(decision, context)


def _final_diagnostic_demo_item(
    decision: ConductorDecision,
    context: TurnContext,
) -> RenderPlanItem:
    template_id = (
        "diagnostic.deliver_demo_already_offered"
        if decision.demo.status in {"offered", "viewed_or_asked", "reacted_positive"}
        else "diagnostic.deliver_demo_not_offered"
    )
    return RenderPlanItem(
        template_id=template_id,
        channel=context.channel,
        variables={
            "demo_status": TemplateVariableValue(
                kind="enum",
                value=decision.demo.status,
                source="runtime_state",
                evidence=["runtime_state.demo.status"],
            )
        },
    )


def _product_or_diagnostic_variable_repair(
    *,
    variable_name: str,
    variable: TemplateVariableValue,
    context: TurnContext,
) -> dict[str, Any] | None:
    official_update = _official_product_variable_repair(
        variable_name=variable_name,
        value=variable.value,
        context=context,
    )
    if official_update is not None and variable.source == "official_product_knowledge":
        return official_update

    diagnostic_update = _diagnostic_source_repair(
        variable_name=variable_name,
        variable=variable,
        context=context,
    )
    if diagnostic_update is not None:
        return diagnostic_update

    return None


def _official_product_variable_repair(
    *,
    variable_name: str,
    value: Any,
    context: TurnContext,
) -> dict[str, Any] | None:
    if variable_name == "agent_name" and _value_mentions_official_agent_name(
        value,
        context,
    ):
        return {"evidence": ["product_knowledge.plans"]}
    if variable_name in {"plan_name", "recommended_plan_or_range"}:
        canonical_plan_value = _canonical_official_plan_value(value, context)
        if canonical_plan_value is not None:
            return {
                "value": canonical_plan_value,
                "evidence": ["product_knowledge.plans"],
            }
    if variable_name == "plan_price_summary" and _has_product_key(context, "prices"):
        return {"evidence": ["product_knowledge.prices"]}
    if variable_name == "official_demo_link" and _has_product_key(context, "links"):
        return {"evidence": ["product_knowledge.links"]}
    return None


def _diagnostic_source_repair(
    *,
    variable_name: str,
    variable: TemplateVariableValue,
    context: TurnContext,
) -> dict[str, Any] | None:
    if variable_name not in {
        "agent_pain_resolved",
        "agent_recommendation_reason",
        "agent_practical_action",
        "crm_base_recommendation",
        "operational_first_step",
    }:
        return None
    if variable.source not in {
        "spec_006_product_contract",
        "official_product_knowledge",
    }:
        return None
    evidence = _diagnostic_evidence(context)
    if not evidence:
        return None
    return {"source": "diagnostic_ledger", "evidence": evidence}


def _value_mentions_official_agent_name(value: Any, context: TurnContext) -> bool:
    normalized_value = _normalize_text(value)
    if not normalized_value:
        return False
    return any(name in normalized_value for name in _official_agent_name_map(context))


def _canonical_official_plan_value(value: Any, context: TurnContext) -> str | None:
    normalized_value = _normalize_text(value)
    if not normalized_value:
        return None
    plan_names = _official_plan_names(context)
    mentioned = [
        display_name
        for normalized_name, display_name in plan_names.items()
        if normalized_name in normalized_value
    ]
    if "completa" in normalized_value and "completo" in plan_names:
        mentioned.append(plan_names["completo"])
    if "avanc" in normalized_value and "avance" in plan_names:
        mentioned.append(plan_names["avance"])
    unique = list(dict.fromkeys(mentioned))
    if not unique:
        return None
    if len(unique) == 1:
        return unique[0]
    return " ou ".join(unique)


def _official_agent_name_map(context: TurnContext) -> dict[str, str]:
    names: dict[str, str] = {}
    for plan in _official_plan_values(context):
        for agent_name in plan.get("included_agents") or []:
            raw_name = str(agent_name or "").strip()
            normalized = _normalize_text(agent_name)
            if normalized and not normalized[0].isdigit():
                names[normalized] = raw_name
    return names


def _official_plan_names(context: TurnContext) -> dict[str, str]:
    names: dict[str, str] = {}
    for plan in _official_plan_values(context):
        raw_name = str(plan.get("name") or "").strip()
        normalized = _normalize_text(raw_name)
        if normalized:
            names[normalized] = raw_name
    return names


def _official_plan_values(context: TurnContext) -> list[dict[str, Any]]:
    for ref in context.product_knowledge:
        if (
            ref.source == "official_product_knowledge"
            and ref.key == "plans"
            and isinstance(ref.value, list)
            and not ref.missing
        ):
            return [plan for plan in ref.value if isinstance(plan, dict)]
    return []


def _has_product_key(context: TurnContext, key: str) -> bool:
    return any(
        ref.source == "official_product_knowledge" and ref.key == key and not ref.missing
        for ref in context.product_knowledge
    )


def _official_demo_link(context: TurnContext) -> str | None:
    for ref in context.product_knowledge:
        if (
            ref.source == "official_product_knowledge"
            and ref.key == "links"
            and isinstance(ref.value, Mapping)
            and not ref.missing
        ):
            value = ref.value.get("demonstration")
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None


def _diagnostic_evidence(context: TurnContext) -> list[str]:
    evidence: list[str] = []
    text = _inbound_text(context)
    if text:
        _append_unique_evidence(evidence, text)
    for ledger_item in context.diagnostic_ledger:
        if not isinstance(ledger_item, dict):
            continue
        answer_value = ledger_item.get("answer_value")
        if isinstance(answer_value, str):
            _append_unique_evidence(evidence, answer_value)
        raw_evidence = ledger_item.get("evidence")
        if isinstance(raw_evidence, list):
            for item in raw_evidence:
                if isinstance(item, str):
                    _append_unique_evidence(evidence, item)
    return evidence or ["diagnostic_ledger"]


def _append_unique_evidence(evidence: list[str], value: str) -> None:
    stripped = value.strip()
    if stripped and stripped not in evidence:
        evidence.append(stripped)


def _inbound_text(context: TurnContext) -> str:
    inbound = context.inbound
    raw_text = inbound.get("text") if isinstance(inbound, dict) else getattr(inbound, "text", None)
    return str(raw_text or "").strip()


def _is_first_turn_context(context: TurnContext) -> bool:
    inbound = context.inbound
    message_type = (
        inbound.get("message_type")
        if isinstance(inbound, dict)
        else getattr(inbound, "message_type", None)
    )
    if message_type != "text":
        return False
    return not (
        context.compact_memory
        or context.recent_transcript
        or context.diagnostic_ledger
    )


def _normalize_text(value: Any) -> str:
    return " ".join(str(value or "").casefold().split())


def _blocked_result_can_use_llm_repair(validator_result: ValidatorResult) -> bool:
    p0_codes = {
        issue.code for issue in validator_result.errors if issue.severity == "P0"
    }
    if not p0_codes:
        return False
    return p0_codes.issubset(_LLM_REPAIRABLE_BLOCKED_CODES)


def _repair_structural_diagnostic_feedback(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _DIAGNOSTIC_FEEDBACK_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()

    feedback = _diagnostic_feedback_from_ledger(decision)
    if feedback is None:
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_items: list[RenderPlanItem] = []
    for item in repaired_decision.template_plan.items:
        if (
            item.template_id in _DIAGNOSTIC_QUESTION_TEMPLATE_IDS
            and _needs_answer_feedback_repair(item)
        ):
            variables = dict(item.variables)
            variables["answer_feedback"] = feedback
            item = item.model_copy(update={"variables": variables})
        repaired_items.append(item)
    repaired_decision.template_plan = repaired_decision.template_plan.model_copy(
        update={"items": repaired_items}
    )

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=1,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=1,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _diagnostic_feedback_from_ledger(
    decision: ConductorDecision,
) -> TemplateVariableValue | None:
    for update in decision.diagnostic.ledger_updates:
        if update.status not in {"answered", "inferred_from_prior_message", "not_applicable"}:
            continue
        answer = _feedback_source_text(update)
        if not answer:
            continue
        feedback = _short_feedback(answer)
        return TemplateVariableValue(
            kind="short_text",
            value=feedback,
            source="diagnostic_ledger",
            evidence=update.evidence or [f"diagnostic.{update.question_key}"],
            max_length=180,
        )
    return None


def _apply_diagnostic_feedback(decision: ConductorDecision) -> bool:
    feedback = _diagnostic_feedback_from_ledger(decision)
    if feedback is None:
        return False
    changed = False
    repaired_items: list[RenderPlanItem] = []
    for item in decision.template_plan.items:
        if (
            item.template_id in _DIAGNOSTIC_QUESTION_TEMPLATE_IDS
            and _needs_answer_feedback_repair(item)
        ):
            variables = dict(item.variables)
            variables["answer_feedback"] = feedback
            item = item.model_copy(update={"variables": variables})
            changed = True
        repaired_items.append(item)
    if changed:
        decision.template_plan = decision.template_plan.model_copy(
            update={"items": repaired_items}
        )
    return changed


def _short_feedback(answer: str) -> str:
    normalized = " ".join(answer.split())
    if len(normalized) > 150:
        normalized = normalized[:147].rstrip() + "..."
    return f"Entendi: {normalized}."


def _needs_answer_feedback_repair(item: RenderPlanItem) -> bool:
    current = item.variables.get("answer_feedback")
    if current is None:
        return True
    if _contains_english_translation_leak(current.value):
        return True
    return current.source != "diagnostic_ledger" or not current.evidence


def _feedback_source_text(update: DiagnosticLedgerItem) -> str:
    answer = (update.answer_value or "").strip()
    if answer and not _contains_english_translation_leak(answer):
        return answer
    for evidence in update.evidence:
        cleaned = _clean_feedback_evidence(evidence)
        if cleaned and not _contains_english_translation_leak(cleaned):
            return cleaned
    return answer


def _clean_feedback_evidence(value: Any) -> str:
    text = " ".join(str(value or "").split()).strip()
    if not text:
        return ""
    lowered = text.casefold()
    if lowered.startswith("product_knowledge.") or lowered.startswith("specs/006-"):
        return ""
    if lowered.startswith("diagnostic."):
        return ""
    if lowered.startswith("detected_intents."):
        return ""
    if lowered.startswith("inbound:"):
        text = text.split(":", 1)[1].strip()
    return text


def _contains_english_translation_leak(value: Any) -> bool:
    normalized = " ".join(str(value or "").casefold().split())
    return any(phrase in normalized for phrase in _ENGLISH_TRANSLATION_LEAK_PHRASES)


def _repair_structural_missing_diagnostic_question(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _DIAGNOSTIC_COMPLETION_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()
    if _has_current_demo_request_signal(decision, context) and {
        "demo_offer_template_missing",
        "post_diagnostic_demo_request_redelivered_diagnostic",
        "post_diagnostic_demo_request_template_missing",
    }.intersection(original_error_codes):
        return RepairResult()

    missing_key = _first_missing_diagnostic_key(validator_result)
    if missing_key is None and "diagnostic_next_question_not_missing" in original_error_codes:
        missing_key = _first_missing_diagnostic_key_from_status(decision, context)
    if missing_key is None:
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_decision.role = "diagnostic"
    repaired_decision.route = "diagnostic"
    repaired_decision.current_state = "diagnostic_in_progress"
    repaired_decision.next_state = "diagnostic_in_progress"
    price_objection_intent_present = _has_price_objection_intent(repaired_decision)
    price_intent_present = _has_price_intent(repaired_decision) or price_objection_intent_present
    if price_intent_present:
        repaired_decision.direct_question_present = True
        repaired_decision.direct_question_answered_first = True
    repaired_decision.diagnostic = repaired_decision.diagnostic.model_copy(
        update={
            "action": "ask_next",
            "next_question_key": missing_key,
            "final_fields": {},
        }
    )
    repaired_decision.demo = DemoDecision()
    repaired_decision.waitlist = WaitlistDecision()
    repaired_decision.handoff = HandoffDecision()
    repaired_decision.policy_checks = repaired_decision.policy_checks.model_copy(
        update={
            "diagnostic_timing_ok": True,
            "waitlist_timing_ok": True,
            "no_human_overlap": True,
        }
    )
    if missing_key == "urgency":
        repaired_decision.diagnostic = repaired_decision.diagnostic.model_copy(
            update={
                "ledger_updates": _reset_urgency_ledger_update(
                    repaired_decision.diagnostic.ledger_updates
                )
            }
        )

    variables: dict[str, TemplateVariableValue] = {}
    feedback = _diagnostic_feedback_from_ledger(repaired_decision)
    if feedback is not None:
        variables["answer_feedback"] = feedback

    repaired_items: list[RenderPlanItem] = []
    if _is_first_turn_context(context):
        repaired_items.append(
            RenderPlanItem(
                template_id="opening.cold_greeting",
                channel=context.channel,
                variables={},
            )
        )
    if missing_key == "active_students_or_size":
        offer_item = _existing_template_item(decision, "diagnostic.offer_soft")
        if offer_item is not None:
            repaired_items.append(offer_item)
    if (
        "price_question_missing_diagnostic_hook" in original_error_codes
        and not price_objection_intent_present
    ):
        repaired_items.append(
            RenderPlanItem(
                template_id=_PRICE_HOOK_TEMPLATE_ID,
                channel=context.channel,
                variables={},
            )
        )
    if price_intent_present:
        official_price_summary = _official_price_summary(context)
        if official_price_summary is not None:
            repaired_items.insert(
                0,
                RenderPlanItem(
                    template_id="product.price_direct",
                    channel=context.channel,
                    variables={"plan_price_summary": official_price_summary},
                ),
            )
    if price_objection_intent_present:
        insert_at = _price_objection_insert_index(
            [item.template_id.split("#", 1)[0] for item in repaired_items]
        )
        repaired_items.insert(
            insert_at,
            RenderPlanItem(
                template_id=_PRICE_OBJECTION_TEMPLATE_ID,
                channel=context.channel,
                variables={},
            ),
        )
    repaired_items.append(
        RenderPlanItem(
            template_id=_DIAGNOSTIC_QUESTION_TEMPLATE_BY_KEY[missing_key],
            channel=context.channel,
            variables=variables,
        )
    )
    repaired_decision.template_plan = repaired_decision.template_plan.model_copy(
        update={"items": repaired_items}
    )

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=1,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=1,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _existing_template_item(
    decision: ConductorDecision,
    template_id: str,
) -> RenderPlanItem | None:
    for item in decision.template_plan.items:
        if item.template_id == template_id:
            return item
    return None


def _first_missing_diagnostic_key(validator_result: ValidatorResult) -> str | None:
    if any(
        issue.code == "diagnostic_urgency_must_be_next"
        for issue in validator_result.errors
    ):
        return "urgency"
    if any(
        issue.code == "diagnostic_urgency_evidence_is_assistant_prompt"
        for issue in validator_result.errors
    ):
        return "urgency"
    if any(
        issue.code == "diagnostic_urgency_evidence_is_priority"
        for issue in validator_result.errors
    ):
        return "urgency"
    if any(
        issue.code == "diagnostic_urgency_evidence_not_timing"
        for issue in validator_result.errors
    ):
        return "urgency"
    if any(
        issue.code == "diagnostic_start_must_ask_active_students"
        for issue in validator_result.errors
    ):
        return "active_students_or_size"
    missing = {
        (issue.path or "").removeprefix("diagnostic.ledger.")
        for issue in validator_result.errors
        if issue.code == "diagnostic_required_field_missing"
    }
    if "urgency" in missing:
        return "urgency"
    for key in _REQUIRED_DIAGNOSTIC_ORDER:
        if key in missing:
            return key
    return None


def _has_price_intent(decision: ConductorDecision) -> bool:
    return any(
        "price" in intent.lower() or "preco" in intent.lower()
        for intent in decision.detected_intents
    )


def _has_price_objection_intent(decision: ConductorDecision) -> bool:
    for raw_intent in decision.detected_intents:
        intent = raw_intent.lower()
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


def _reset_urgency_ledger_update(
    ledger_updates: list[DiagnosticLedgerItem],
) -> list[DiagnosticLedgerItem]:
    reset_update = DiagnosticLedgerItem(
        question_key="urgency",
        status="missing",
        answer_value=None,
        evidence=[],
        confidence="low",
        may_ask_again=True,
    )
    updated: list[DiagnosticLedgerItem] = []
    replaced = False
    for item in ledger_updates:
        if item.question_key == "urgency":
            updated.append(reset_update)
            replaced = True
            continue
        updated.append(item)
    if not replaced:
        updated.append(reset_update)
    return updated


def _first_missing_diagnostic_key_from_status(
    decision: ConductorDecision,
    context: TurnContext,
) -> str | None:
    statuses: dict[str, str] = {}
    for item in context.diagnostic_ledger:
        if not isinstance(item, dict):
            continue
        key = str(item.get("question_key") or "")
        status = str(item.get("status") or "")
        if key:
            statuses[key] = status
    for update in decision.diagnostic.ledger_updates:
        statuses[update.question_key] = update.status

    for key in _REQUIRED_DIAGNOSTIC_ORDER:
        if statuses.get(key) not in {
            "answered",
            "inferred_from_prior_message",
            "not_applicable",
        }:
            return key
    return None


def _drop_unknown_template_variables_from_invalid_items(
    items: list[RenderPlanItem],
    validator_result: ValidatorResult,
) -> list[RenderPlanItem]:
    invalid_by_index: dict[int, set[str]] = {}
    for issue in validator_result.errors:
        if issue.code != "template_plan_invalid" or issue.path is None:
            continue
        match = re.search(r"template_plan\.items\[(\d+)\]", issue.path)
        if match is None:
            continue
        variable_name = _template_issue_variable_name(issue.message)
        if variable_name is None:
            continue
        invalid_by_index.setdefault(int(match.group(1)), set()).add(variable_name)

    if not invalid_by_index:
        return items

    repaired_items: list[RenderPlanItem] = []
    for index, item in enumerate(items):
        invalid_variables = invalid_by_index.get(index)
        if not invalid_variables:
            repaired_items.append(item)
            continue
        variables = {
            key: value
            for key, value in item.variables.items()
            if key not in invalid_variables
        }
        repaired_items.append(item.model_copy(update={"variables": variables}))
    return repaired_items


def _template_issue_variable_name(message: str) -> str | None:
    for prefix in ("unknown_variable:", "source_not_allowed:"):
        if message.startswith(prefix):
            return message.removeprefix(prefix).split(":", 1)[0]
    return None


def _repair_structural_price_objection_value(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if "price_objection_value_template_missing" not in original_error_codes:
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_items = [
        item
        for item in repaired_decision.template_plan.items
        if item.template_id.split("#", 1)[0] != _PRICE_OBJECTION_TEMPLATE_ID
    ]
    completed_context = _context_diagnostic_completed(context)
    if completed_context and _has_final_diagnostic_delivery_template(repaired_decision):
        repaired_items = [
            item
            for item in repaired_items
            if not item.template_id.split("#", 1)[0].startswith("diagnostic.deliver")
        ]
        repaired_decision.diagnostic = DiagnosticDecision()
        if repaired_decision.route == "diagnostic":
            repaired_decision.role = "product"
            repaired_decision.route = "product"
            repaired_decision.current_state = "product_price_objection"
            repaired_decision.next_state = "product_followup"

    insert_at = _price_objection_insert_index(
        [item.template_id.split("#", 1)[0] for item in repaired_items]
    )
    repaired_items.insert(
        insert_at,
        RenderPlanItem(
            template_id=_PRICE_OBJECTION_TEMPLATE_ID,
            channel=context.channel,
            variables={},
        ),
    )
    repaired_decision.template_plan = repaired_decision.template_plan.model_copy(
        update={
            "items": repaired_items,
            "chunk_policy": (
                "whatsapp_max_3"
                if context.channel == "whatsapp"
                else repaired_decision.template_plan.chunk_policy
            ),
        }
    )
    if not completed_context and repaired_decision.diagnostic.action == "none":
        repaired_decision.diagnostic = repaired_decision.diagnostic.model_copy(
            update={"action": "offer"}
        )
    repaired_decision.direct_question_present = True
    repaired_decision.direct_question_answered_first = True
    repaired_decision.policy_checks = repaired_decision.policy_checks.model_copy(
        update={
            "direct_question_answered_first": True,
            "diagnostic_timing_ok": True,
        }
    )

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=1,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=1,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _price_objection_insert_index(template_ids: list[str]) -> int:
    for index, template_id in enumerate(template_ids):
        if template_id in {
            "product.price_direct",
            "product.price_complete_direct",
            "product.plan_direct",
        }:
            return index + 1
    for index, template_id in enumerate(template_ids):
        if (
            template_id.startswith("diagnostic.")
            or template_id.startswith("waitlist.")
            or template_id.startswith("handoff.")
        ):
            return index
    return len(template_ids)


def _with_price_objection_value_item(
    items: list[RenderPlanItem],
    *,
    context: TurnContext,
) -> list[RenderPlanItem]:
    if any(
        item.template_id.split("#", 1)[0] == _PRICE_OBJECTION_TEMPLATE_ID
        for item in items
    ):
        return items
    repaired_items = list(items)
    insert_at = _price_objection_insert_index(
        [item.template_id.split("#", 1)[0] for item in repaired_items]
    )
    repaired_items.insert(
        insert_at,
        RenderPlanItem(
            template_id=_PRICE_OBJECTION_TEMPLATE_ID,
            channel=context.channel,
            variables={},
        ),
    )
    return repaired_items


def _repair_structural_price_hook(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _PRICE_HOOK_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()

    template_ids = [item.template_id for item in decision.template_plan.items]
    has_price_answer = bool(_PRICE_ANSWER_TEMPLATE_IDS.intersection(template_ids))
    if not has_price_answer and original_error_codes == ["unsupported_price_value"]:
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_items = list(repaired_decision.template_plan.items)
    diagnostic_completed = _context_diagnostic_completed(context)
    if "stale_demo_direct_without_current_request" in original_error_codes:
        repaired_items = [
            item
            for item in repaired_items
            if item.template_id.split("#", 1)[0] != "product.demo_direct"
        ]
        repaired_decision.demo = DemoDecision()
    if repaired_decision.route == "product" and "banned_waitlist_promise" in original_error_codes:
        repaired_items = [
            item
            for item in repaired_items
            if not item.template_id.split("#", 1)[0].startswith("waitlist.")
        ]
    if "price_question_missing_diagnostic_hook" in original_error_codes:
        repaired_items = [
            item
            for item in repaired_items
            if item.template_id.split("#", 1)[0] != "diagnostic.offer_soft"
        ]
    if "duplicate_diagnostic_offer_templates" in original_error_codes:
        seen_offer = False
        deduped_items: list[RenderPlanItem] = []
        for item in repaired_items:
            template_id = item.template_id.split("#", 1)[0]
            if template_id in {
                "diagnostic.offer_soft",
                "diagnostic.price_hook",
                "diagnostic.price_hook_with_context",
                "product.plan_fit_with_diagnostic",
            }:
                if seen_offer:
                    continue
                seen_offer = True
            deduped_items.append(item)
        repaired_items = deduped_items
    if (
        "template_plan_invalid" in original_error_codes
        and "price_plus_context_requires_context_hook" not in original_error_codes
    ):
        repaired_items = _drop_unknown_template_variables_from_invalid_items(
            repaired_items,
            validator_result,
        )
        repaired_items = [
            item.model_copy(update={"template_id": "diagnostic.price_hook", "variables": {}})
            if item.template_id.split("#", 1)[0] == "diagnostic.price_hook_with_context"
            else item
            for item in repaired_items
        ]
    if not has_price_answer and any(
        code in original_error_codes
        for code in {
            "price_question_missing_price_answer",
            "price_question_missing_diagnostic_hook",
            "price_plus_context_requires_context_hook",
        }
    ):
        official_price_summary = _official_price_summary(context)
        if official_price_summary is not None:
            repaired_items.insert(
                0,
                RenderPlanItem(
                    template_id="product.price_direct",
                    channel=context.channel,
                    variables={"plan_price_summary": official_price_summary},
                ),
            )
            has_price_answer = True
    if "product_route_must_not_ask_diagnostic_question" in original_error_codes:
        repaired_items = [
            item
            for item in repaired_items
            if item.template_id.split("#", 1)[0] not in _DIAGNOSTIC_QUESTION_TEMPLATE_IDS
        ]
        repaired_decision.diagnostic = repaired_decision.diagnostic.model_copy(
            update={"action": "offer", "next_question_key": None}
        )
    if "unsupported_price_value" in original_error_codes and has_price_answer:
        official_price_summary = _official_price_summary(context)
        if official_price_summary is None:
            return RepairResult()
        repaired_items = [
            _with_official_price_summary(item, official_price_summary)
            if item.template_id in _PRICE_ANSWER_TEMPLATE_IDS
            else item
            for item in repaired_items
        ]
    elif has_price_answer and (
        "template_plan_invalid" in original_error_codes
        or "product_claim_source_invalid" in original_error_codes
        or "price_question_missing_diagnostic_offer" in original_error_codes
    ):
        official_price_summary = _official_price_summary(context)
        if official_price_summary is not None:
            repaired_items = [
                _with_official_price_summary(item, official_price_summary)
                if item.template_id in _PRICE_ANSWER_TEMPLATE_IDS
                else item
                for item in repaired_items
            ]

    if "price_plus_context_requires_context_hook" in original_error_codes:
        repaired_items = [
            item
            for item in repaired_items
            if item.template_id.split("#", 1)[0]
            not in {"diagnostic.price_hook", "diagnostic.price_hook_with_context"}
        ]
        insert_at = _price_hook_insert_index(
            [item.template_id for item in repaired_items]
        )
        repaired_items.insert(
            insert_at,
            _contextual_price_hook_item(context),
        )
        repaired_decision.template_plan = repaired_decision.template_plan.model_copy(
            update={"items": repaired_items}
        )
    elif not diagnostic_completed and not any(
        item.template_id.split("#", 1)[0] in _PRICE_HOOK_TEMPLATE_IDS
        for item in repaired_items
    ):
        insert_at = _price_hook_insert_index(
            [item.template_id for item in repaired_items]
        )
        repaired_items.insert(
            insert_at,
            RenderPlanItem(
                template_id=_PRICE_HOOK_TEMPLATE_ID,
                channel=context.channel,
                variables={},
            ),
        )
        repaired_decision.template_plan = repaired_decision.template_plan.model_copy(
            update={"items": repaired_items}
        )
    if _has_price_objection_intent(repaired_decision):
        repaired_items = _with_price_objection_value_item(
            repaired_items,
            context=context,
        )
    repaired_decision.template_plan = repaired_decision.template_plan.model_copy(
        update={
            "items": repaired_items,
            "chunk_policy": (
                "whatsapp_max_3"
                if context.channel == "whatsapp"
                else repaired_decision.template_plan.chunk_policy
            ),
        }
    )

    if diagnostic_completed:
        repaired_decision.diagnostic = DiagnosticDecision()
    elif repaired_decision.diagnostic.action == "none":
        repaired_decision.diagnostic = repaired_decision.diagnostic.model_copy(
            update={"action": "offer"}
        )

    _apply_diagnostic_feedback(repaired_decision)

    if _FINAL_DIAGNOSTIC_STAGE_REPAIR_CODES.intersection(original_error_codes):
        normalized_items = _normalized_final_diagnostic_items(repaired_decision, context)
        if normalized_items is not None:
            repaired_decision.template_plan = repaired_decision.template_plan.model_copy(
                update={"items": normalized_items}
            )

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=1,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=1,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _price_hook_insert_index(template_ids: list[str]) -> int:
    for index, template_id in enumerate(template_ids):
        if template_id in _PRICE_ANSWER_TEMPLATE_IDS:
            return index + 1
    for index, template_id in enumerate(template_ids):
        if template_id in _DIAGNOSTIC_QUESTION_TEMPLATE_IDS:
            return index
    return len(template_ids)


def _contextual_price_hook_item(context: TurnContext) -> RenderPlanItem:
    inbound = _inbound_text(context)
    return RenderPlanItem(
        template_id="diagnostic.price_hook_with_context",
        channel=context.channel,
        variables={
            "plan_fit_context": TemplateVariableValue(
                kind="short_text",
                value=(
                    f"Voce comentou: {inbound}"
                    if inbound
                    else "Voce trouxe um ponto da rotina do studio."
                ),
                source="user_message",
                evidence=_diagnostic_evidence(context),
                max_length=180,
            )
        },
    )


def _with_official_price_summary(
    item: RenderPlanItem,
    price_summary: TemplateVariableValue,
) -> RenderPlanItem:
    if item.template_id.split("#", 1)[0] == _PRICE_OBJECTION_TEMPLATE_ID:
        return item
    variables = {"plan_price_summary": price_summary}
    return item.model_copy(update={"variables": variables})


def _official_price_summary(context: TurnContext) -> TemplateVariableValue | None:
    prices_ref = next(
        (
            ref
            for ref in context.product_knowledge
            if ref.key == "prices" and isinstance(ref.value, dict) and not ref.missing
        ),
        None,
    )
    if prices_ref is None:
        return None
    prices = prices_ref.value
    inbound = _normalize_text(_inbound_text(context))
    if "completo" in inbound:
        complete_price = prices.get("seven_agents")
        if isinstance(complete_price, str) and complete_price.strip():
            return TemplateVariableValue(
                kind="long_text",
                value=f"O plano Completo custa {complete_price.strip()}.",
                source="official_product_knowledge",
                evidence=["product_knowledge.prices"],
                max_length=360,
            )
    summary = (
        f"Base: {prices.get('base')}; "
        f"Essencial: {prices.get('one_agent')}; "
        f"Avance: {prices.get('three_agents')}; "
        f"Completo: {prices.get('seven_agents')}."
    )
    if "None" in summary:
        return None
    return TemplateVariableValue(
        kind="long_text",
        value=summary,
        source="official_product_knowledge",
        evidence=["product_knowledge.prices"],
        max_length=360,
    )


def _repair_structural_waitlist_offer(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _WAITLIST_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()

    has_waitlist_surface = decision.waitlist.status in {
        "offered",
        "pending_details",
        "joined",
    } or any(
        item.template_id.split("#", 1)[0].startswith("waitlist.")
        for item in decision.template_plan.items
    )
    has_contract_intent = bool(
        {
            "buy_intent",
            "checkout_request",
            "contract_intent",
            "waitlist_interest",
            "waitlist_intent",
            "waitlist_request",
            "subscription_intent",
        }.intersection(decision.detected_intents)
    )
    if not has_waitlist_surface and not has_contract_intent:
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_decision.role = "waitlist"
    repaired_decision.route = "waitlist"
    repaired_decision.current_state = "waitlist_offered"
    repaired_decision.next_state = "waitlist_offered"
    repaired_decision.direct_question_present = (
        repaired_decision.direct_question_present or has_contract_intent
    )
    repaired_decision.direct_question_answered_first = True
    repaired_decision.diagnostic = DiagnosticDecision()
    repaired_decision.demo = DemoDecision()
    if (
        "waitlist_contact_path_not_needed_for_whatsapp" in original_error_codes
        or "waitlist_offer_missing_studio_details" in original_error_codes
        or "waitlist_joined_missing_details" in original_error_codes
        or "waitlist_joined_unknown_details" in original_error_codes
    ):
        repaired_decision.current_state = "waitlist_pending_details"
        repaired_decision.next_state = "waitlist_pending_details"
        repaired_decision.waitlist = WaitlistDecision(
            eligibility="eligible",
            status="pending_details",
            missing_details=["studio_name", "city_state"],
        )
        repaired_items = [
            RenderPlanItem(
                template_id="waitlist.ask_missing_studio",
                channel=context.channel,
                variables={},
            )
        ]
    else:
        repaired_decision.waitlist = WaitlistDecision(eligibility="eligible", status="offered")
        repaired_items = [
            RenderPlanItem(
                template_id="waitlist.offer_after_contract_intent",
                channel=context.channel,
                variables={
                    "waitlist_context_summary": TemplateVariableValue(
                        kind="long_text",
                        value=(
                            "Voce pediu para contratar agora; vou tratar isso "
                            "como interesse direto na Taliya."
                        ),
                        source="runtime_state",
                        evidence=["decision.waitlist.contract_intent"],
                        max_length=220,
                    )
                },
            )
        ]
    repaired_decision.handoff = HandoffDecision()
    repaired_decision.policy_checks = repaired_decision.policy_checks.model_copy(
        update={
            "direct_question_answered_first": True,
            "diagnostic_timing_ok": True,
            "waitlist_timing_ok": True,
            "official_facts_only": False,
            "no_internal_text_leak": True,
            "no_early_contact_capture": True,
            "no_human_overlap": True,
        }
    )
    repaired_decision.template_plan = RenderPlan(
        items=repaired_items,
        chunk_policy="whatsapp_max_3" if context.channel == "whatsapp" else "default",
    )

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=0,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=0,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _repair_structural_policy_checks(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _POLICY_CHECK_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    if "direct_question_self_check_uncorroborated" in original_error_codes:
        repaired_decision.direct_question_answered_first = True
    repaired_decision.policy_checks = repaired_decision.policy_checks.model_copy(
        update={
            "direct_question_answered_first": (
                True
                if "direct_question_self_check_uncorroborated" in original_error_codes
                else repaired_decision.policy_checks.direct_question_answered_first
            ),
            "official_facts_only": (
                False
                if "official_facts_self_check_uncorroborated" in original_error_codes
                else repaired_decision.policy_checks.official_facts_only
            ),
        }
    )

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=0,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=0,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _repair_structural_how_it_works(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _HOW_IT_WORKS_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()
    intents = {intent.lower() for intent in decision.detected_intents}
    template_ids = [item.template_id.split("#", 1)[0] for item in decision.template_plan.items]
    if (
        _HOW_IT_WORKS_TEMPLATE_ID not in template_ids
        and "how_it_works" not in intents
        and "product_how_it_works" not in intents
        and "how_it_works_question" not in intents
    ):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_decision.role = "product"
    repaired_decision.route = "product"
    repaired_decision.current_state = "product_how_it_works"
    repaired_decision.next_state = "product_question_answered"
    repaired_decision.diagnostic = DiagnosticDecision()
    repaired_decision.demo = DemoDecision()
    repaired_decision.waitlist = WaitlistDecision()
    repaired_decision.handoff = HandoffDecision()
    repaired_decision.policy_checks = repaired_decision.policy_checks.model_copy(
        update={
            "direct_question_answered_first": True,
            "diagnostic_timing_ok": True,
            "official_facts_only": True,
            "no_human_overlap": True,
        }
    )
    next_step_value = (
        "continue_diagnostic"
        if _first_missing_diagnostic_key_from_status(decision, context) is not None
        else "diagnostic_offer_generic"
    )
    repaired_items = [
        item
        for item in repaired_decision.template_plan.items
        if not item.template_id.split("#", 1)[0].startswith("diagnostic.deliver")
        and not item.template_id.split("#", 1)[0].startswith("waitlist.")
        and item.template_id.split("#", 1)[0]
        not in {
            "product.overview_short",
            "product.demo_direct",
            "diagnostic.offer_soft",
            "diagnostic.price_hook",
            "diagnostic.ask_active_students",
            "diagnostic.ask_main_pain",
            "diagnostic.ask_current_process",
            "diagnostic.ask_pain_detail",
            "diagnostic.ask_priority",
            "diagnostic.ask_urgency",
        }
    ]
    cleaned_items: list[RenderPlanItem] = []
    has_how_it_works = False
    for item in repaired_items:
        if item.template_id.split("#", 1)[0] != _HOW_IT_WORKS_TEMPLATE_ID:
            cleaned_items.append(item)
            continue
        variables = {
            "contextual_next_step": TemplateVariableValue(
                kind="enum",
                value=next_step_value,
                source="model_decision",
                evidence=["detected_intents.how_it_works"],
            )
        }
        recommended_area = item.variables.get("recommended_area")
        if (
            recommended_area is not None
            and recommended_area.source in {"diagnostic_ledger", "runtime_state"}
        ):
            variables["recommended_area"] = recommended_area
        cleaned_items.append(item.model_copy(update={"variables": variables}))
        has_how_it_works = True

    if not has_how_it_works:
        repaired_items.insert(
            0,
            RenderPlanItem(
                template_id=_HOW_IT_WORKS_TEMPLATE_ID,
                channel=context.channel,
                variables={
                    "contextual_next_step": TemplateVariableValue(
                        kind="enum",
                        value=next_step_value,
                        source="model_decision",
                        evidence=["detected_intents.how_it_works"],
                    )
                },
            ),
        )
        cleaned_items = repaired_items
    repaired_decision.template_plan = repaired_decision.template_plan.model_copy(
        update={"items": cleaned_items}
    )

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=1,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=1,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _repair_structural_integration_scope_answer(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _INTEGRATION_SCOPE_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_decision.role = "product"
    repaired_decision.route = "product"
    repaired_decision.current_state = "product_question"
    repaired_decision.next_state = "product_question"
    repaired_decision.direct_question_present = True
    repaired_decision.direct_question_answered_first = True
    repaired_decision.diagnostic = DiagnosticDecision(action="none")
    repaired_decision.waitlist = WaitlistDecision()
    repaired_decision.handoff = HandoffDecision()
    repaired_decision.policy_checks = repaired_decision.policy_checks.model_copy(
        update={
            "direct_question_answered_first": True,
            "diagnostic_timing_ok": True,
            "official_facts_only": True,
            "no_human_overlap": True,
        }
    )

    if "integration_scope_question" not in {
        intent.lower() for intent in repaired_decision.detected_intents
    }:
        repaired_decision.detected_intents.append("integration_scope_question")

    variables: dict[str, TemplateVariableValue] = {}
    integration_topic = _inbound_text(context)[:100].strip()
    if integration_topic:
        variables["integration_topic"] = TemplateVariableValue(
            kind="short_text",
            value=integration_topic,
            source="user_message",
            evidence=[integration_topic],
            max_length=100,
        )
    repaired_decision.template_plan = RenderPlan(
        items=[
            RenderPlanItem(
                template_id=_INTEGRATION_SCOPE_TEMPLATE_ID,
                channel=context.channel,
                variables=variables,
            )
        ],
        chunk_policy=(
            "whatsapp_max_3" if context.channel == "whatsapp" else "default"
        ),
    )

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=1,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=1,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _repair_structural_demo_direct_flags(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _DEMO_DIRECT_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    if _has_current_demo_request_signal(decision, context) and any(
        item.template_id.split("#", 1)[0] == "product.demo_direct"
        for item in repaired_decision.template_plan.items
    ):
        repaired_decision.detected_intents = [
            intent
            for intent in repaired_decision.detected_intents
            if "price" not in intent.casefold() and "preco" not in intent.casefold()
        ]
        if not any(
            "demo" in intent.casefold()
            for intent in repaired_decision.detected_intents
        ):
            repaired_decision.detected_intents.append("demo_request")
    repaired_decision.direct_question_present = True
    repaired_decision.direct_question_answered_first = True
    repaired_decision.policy_checks = repaired_decision.policy_checks.model_copy(
        update={"direct_question_answered_first": True}
    )

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=1,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=1,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


def _repair_structural_diagnostic_refusal(
    *,
    decision: ConductorDecision,
    context: TurnContext,
    validator_result: ValidatorResult,
) -> RepairResult:
    original_error_codes = _issue_codes(validator_result.errors)
    if not _DIAGNOSTIC_REFUSAL_REPAIR_CODES.intersection(original_error_codes):
        return RepairResult()

    repaired_decision = decision.model_copy(deep=True)
    repaired_decision.diagnostic = DiagnosticDecision(action="none")
    repaired_decision.template_plan = repaired_decision.template_plan.model_copy(
        update={
            "items": [
                item
                for item in repaired_decision.template_plan.items
                if item.template_id.split("#", 1)[0]
                not in {
                    "diagnostic.offer_soft",
                    "diagnostic.price_hook",
                    "diagnostic.price_hook_with_context",
                    "product.plan_fit_with_diagnostic",
                }
            ]
        }
    )
    repaired_decision.policy_checks = repaired_decision.policy_checks.model_copy(
        update={"diagnostic_timing_ok": True}
    )

    repaired_validation = validate_conductor_result(repaired_decision, context)
    if repaired_validation.status == "passed":
        return RepairResult(
            attempted=True,
            attempt_count=1,
            status="repaired",
            errors_sent=original_error_codes,
            repaired_decision=repaired_decision,
        )

    return RepairResult(
        attempted=True,
        attempt_count=1,
        status="failed",
        errors_sent=sorted(
            {
                *original_error_codes,
                *_issue_codes(repaired_validation.errors),
            }
        ),
    )


async def _call_repair_provider(
    provider: RepairProvider,
    request: RepairProviderRequest,
) -> RepairProviderOutput:
    result = provider(request)
    if inspect.isawaitable(result):
        return await result
    return result


def _is_known_schema_version_alias(schema_version: str) -> bool:
    return schema_version == "011.conductor_decision.v1"


def _issue_codes(errors: list[ValidationIssue]) -> list[str]:
    return [issue.code for issue in errors]
