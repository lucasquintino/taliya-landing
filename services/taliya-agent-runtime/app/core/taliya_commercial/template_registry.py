from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from app.core.taliya_commercial.schemas import (
    FORBIDDEN_TEMPLATE_VARIABLE_NAMES,
    RenderPlanItem,
)

VariableKind = Literal[
    "short_text",
    "long_text",
    "number",
    "boolean",
    "enum",
    "list",
    "url",
]


@dataclass(frozen=True, slots=True)
class TemplateVariableSpec:
    name: str
    kind: VariableKind
    allowed_sources: frozenset[str]
    max_length: int | None
    validation_rule: str
    customer_facing: bool = True


@dataclass(frozen=True, slots=True)
class TemplateSpec:
    template_id: str
    required_variables: tuple[str, ...] = ()
    optional_variables: tuple[str, ...] = ()


def _sources(*values: str) -> frozenset[str]:
    return frozenset(values)


def _var(
    name: str,
    kind: VariableKind,
    sources: frozenset[str],
    max_length: int | None,
    validation_rule: str,
) -> TemplateVariableSpec:
    return TemplateVariableSpec(
        name=name,
        kind=kind,
        allowed_sources=sources,
        max_length=max_length,
        validation_rule=validation_rule,
    )


def _tpl(
    template_id: str,
    *,
    required: tuple[str, ...] = (),
    optional: tuple[str, ...] = (),
) -> TemplateSpec:
    return TemplateSpec(
        template_id=template_id,
        required_variables=required,
        optional_variables=optional,
    )


VARIABLE_REGISTRY: dict[str, TemplateVariableSpec] = {
    "first_name": _var(
        "first_name",
        "short_text",
        _sources("user_message", "channel_metadata", "runtime_state"),
        40,
        "Only a verified real person first name; never a studio name, handle, "
        "phone, internal reliability label, or unverified profile value.",
    ),
    "answer_feedback": _var(
        "answer_feedback",
        "short_text",
        _sources("diagnostic_ledger", "user_message"),
        180,
        "Grounded reflection on the immediately previous diagnostic answer; "
        "not generic filler and not mechanical repetition.",
    ),
    "pain_context_human": _var(
        "pain_context_human",
        "long_text",
        _sources("diagnostic_ledger", "user_message"),
        420,
        "Practical studio-owner reading grounded in diagnostic facts or the "
        "lead's own pain/context message.",
    ),
    "crm_base_recommendation": _var(
        "crm_base_recommendation",
        "long_text",
        _sources(
            "diagnostic_ledger",
            "official_product_knowledge",
            "spec_006_product_contract",
        ),
        260,
        "Grounded recommendation for organizing the base/routine before agents; "
        "no technical CRM jargon unless the lead used it.",
    ),
    "operational_first_step": _var(
        "operational_first_step",
        "long_text",
        _sources("diagnostic_ledger", "spec_006_product_contract"),
        240,
        "First practical operational step tied to the lead's stated priority.",
    ),
    "agent_name": _var(
        "agent_name",
        "short_text",
        _sources("official_product_knowledge", "spec_006_product_contract"),
        60,
        "Official routine or agent name from product knowledge.",
    ),
    "agent_fit_phrase": _var(
        "agent_fit_phrase",
        "enum",
        _sources("model_decision"),
        0,
        "Approved enum phrase such as first_fit or also_fit; renderer owns copy.",
    ),
    "agent_pain_resolved": _var(
        "agent_pain_resolved",
        "long_text",
        _sources("diagnostic_ledger", "spec_006_product_contract"),
        180,
        "Concrete pain this routine/agent helps with, grounded in diagnostic facts.",
    ),
    "agent_recommendation_reason": _var(
        "agent_recommendation_reason",
        "long_text",
        _sources("diagnostic_ledger", "spec_006_product_contract"),
        280,
        "Reason this routine/agent fits the diagnostic evidence.",
    ),
    "agent_practical_action": _var(
        "agent_practical_action",
        "long_text",
        _sources("diagnostic_ledger", "spec_006_product_contract"),
        280,
        "Practical action the studio can understand without technical SaaS terms.",
    ),
    "recommended_plan_or_range": _var(
        "recommended_plan_or_range",
        "short_text",
        _sources("official_product_knowledge", "spec_006_product_contract"),
        90,
        "Official plan or range from product knowledge; never inferred from one "
        "number without diagnostic evidence.",
    ),
    "demo_status": _var(
        "demo_status",
        "enum",
        _sources("runtime_state"),
        0,
        "Persisted demo state: not_offered, offered, viewed_or_asked, or "
        "reacted_positive.",
    ),
    "plan_price_summary": _var(
        "plan_price_summary",
        "long_text",
        _sources("official_product_knowledge", "spec_006_product_contract"),
        360,
        "Official price/plan summary assembled from product facts only.",
    ),
    "plan_name": _var(
        "plan_name",
        "short_text",
        _sources("official_product_knowledge", "spec_006_product_contract"),
        80,
        "Official plan name only.",
    ),
    "plan_fit_context": _var(
        "plan_fit_context",
        "short_text",
        _sources("user_message", "diagnostic_ledger"),
        180,
        "Lead-provided context used only to explain why fit needs diagnostic evidence.",
    ),
    "official_demo_link": _var(
        "official_demo_link",
        "url",
        _sources("official_product_knowledge", "spec_006_product_contract"),
        None,
        "Official demo URL from product knowledge; never invented or shortened ad hoc.",
    ),
    "product_fact_summary": _var(
        "product_fact_summary",
        "long_text",
        _sources("official_product_knowledge", "spec_006_product_contract"),
        320,
        "Short customer-facing product fact summary grounded in official sources.",
    ),
    "contextual_next_step": _var(
        "contextual_next_step",
        "enum",
        _sources("runtime_state", "diagnostic_ledger", "model_decision"),
        0,
        "Approved next-step enum from product-followup contract; renderer owns copy. "
        "Allowed values: diagnostic_offer_with_pain, diagnostic_offer_generic, "
        "continue_diagnostic, no_cta.",
    ),
    "recommended_area": _var(
        "recommended_area",
        "short_text",
        _sources("diagnostic_ledger", "runtime_state"),
        80,
        "Area recommended by a completed diagnostic; not a new diagnosis.",
    ),
    "current_tool_context": _var(
        "current_tool_context",
        "short_text",
        _sources("user_message", "runtime_state"),
        120,
        "Current tool or competitor name only when the lead mentioned it.",
    ),
    "integration_topic": _var(
        "integration_topic",
        "short_text",
        _sources("user_message"),
        100,
        "Integration or setup topic explicitly asked by the lead.",
    ),
    "human_confirmation_topic": _var(
        "human_confirmation_topic",
        "short_text",
        _sources("user_message", "runtime_state", "official_product_knowledge"),
        100,
        "Topic to hand to a human because official facts are missing or limited.",
    ),
    "waitlist_context_summary": _var(
        "waitlist_context_summary",
        "long_text",
        _sources("diagnostic_ledger", "runtime_state"),
        220,
        "Why waitlist is allowed now, grounded in clear intent and saved context.",
    ),
    "missing_detail_label": _var(
        "missing_detail_label",
        "enum",
        _sources("runtime_state"),
        0,
        "Approved enum for one missing waitlist detail.",
    ),
    "studio_name": _var(
        "studio_name",
        "short_text",
        _sources("user_message", "runtime_state"),
        80,
        "Studio name supplied or confirmed by the lead; separate from person name.",
    ),
    "city_state": _var(
        "city_state",
        "short_text",
        _sources("user_message", "runtime_state"),
        80,
        "City/state supplied or confirmed by the lead.",
    ),
    "contact_path": _var(
        "contact_path",
        "enum",
        _sources("user_message", "runtime_state"),
        0,
        "Approved contact-path enum; never ask WhatsApp leads for their phone.",
    ),
    "handoff_reason": _var(
        "handoff_reason",
        "short_text",
        _sources("user_message", "runtime_state"),
        120,
        "Lead-visible handoff reason grounded in request or operational state.",
    ),
    "unsupported_media_kind": _var(
        "unsupported_media_kind",
        "enum",
        _sources("runtime_state"),
        0,
        "Approved unsupported media type enum.",
    ),
    "safe_redirect_reason": _var(
        "safe_redirect_reason",
        "enum",
        _sources("runtime_state"),
        0,
        "Approved safety redirect enum; renderer owns copy.",
    ),
    "clarification_question": _var(
        "clarification_question",
        "short_text",
        _sources("model_decision"),
        140,
        "One neutral clarification question; no product claim, no side effect.",
    ),
}


TEMPLATE_REGISTRY: dict[str, TemplateSpec] = {
    "opening.cold_greeting": _tpl("opening.cold_greeting"),
    "opening.cold_greeting_named": _tpl(
        "opening.cold_greeting_named",
        required=("first_name",),
    ),
    "opening.contextual_ack": _tpl("opening.contextual_ack"),
    "opening.widget_empty_diagnostic": _tpl("opening.widget_empty_diagnostic"),
    "opening.general_interest": _tpl("opening.general_interest"),
    "opening.instagram_source": _tpl("opening.instagram_source"),
    "opening.site_cta": _tpl("opening.site_cta"),
    "opening.diagnostic_cta": _tpl(
        "opening.diagnostic_cta",
        optional=("first_name",),
    ),
    "product.overview_short": _tpl(
        "product.overview_short",
        optional=("product_fact_summary",),
    ),
    "product.price_direct": _tpl(
        "product.price_direct",
        required=("plan_price_summary",),
        optional=("plan_fit_context",),
    ),
    "product.price_complete_direct": _tpl(
        "product.price_complete_direct",
        required=("plan_price_summary",),
        optional=("plan_fit_context",),
    ),
    "product.price_objection_value": _tpl("product.price_objection_value"),
    "product.plan_direct": _tpl(
        "product.plan_direct",
        required=("plan_price_summary",),
        optional=("plan_name",),
    ),
    "product.plan_fit_with_diagnostic": _tpl(
        "product.plan_fit_with_diagnostic",
        required=("plan_fit_context",),
    ),
    "product.demo_direct": _tpl(
        "product.demo_direct",
        required=("official_demo_link",),
    ),
    "product.whatsapp_direct": _tpl(
        "product.whatsapp_direct",
        optional=("official_demo_link",),
    ),
    "product.crm_direct": _tpl(
        "product.crm_direct",
        required=("product_fact_summary",),
    ),
    "product.agents_direct": _tpl(
        "product.agents_direct",
        required=("product_fact_summary",),
    ),
    "product.how_it_works_direct": _tpl(
        "product.how_it_works_direct",
        required=("contextual_next_step",),
        optional=("recommended_area",),
    ),
    "product.comparison_current_tool": _tpl(
        "product.comparison_current_tool",
        required=("current_tool_context",),
    ),
    "product.integration_scope_direct": _tpl(
        "product.integration_scope_direct",
        required=("integration_topic",),
        optional=("human_confirmation_topic",),
    ),
    "product.security_data_direct": _tpl(
        "product.security_data_direct",
        optional=("human_confirmation_topic",),
    ),
    "product.out_of_profile_redirect": _tpl("product.out_of_profile_redirect"),
    "diagnostic.offer_soft": _tpl(
        "diagnostic.offer_soft",
        optional=("pain_context_human",),
    ),
    "diagnostic.price_hook": _tpl("diagnostic.price_hook"),
    "diagnostic.price_hook_with_context": _tpl(
        "diagnostic.price_hook_with_context",
    ),
    "diagnostic.start": _tpl("diagnostic.start"),
    "diagnostic.start_named": _tpl(
        "diagnostic.start_named",
        required=("first_name",),
    ),
    "diagnostic.ask_active_students": _tpl(
        "diagnostic.ask_active_students",
        optional=("answer_feedback",),
    ),
    "diagnostic.ask_main_pain": _tpl(
        "diagnostic.ask_main_pain",
        optional=("answer_feedback",),
    ),
    "diagnostic.ask_current_process": _tpl(
        "diagnostic.ask_current_process",
        optional=("answer_feedback",),
    ),
    "diagnostic.ask_pain_detail": _tpl(
        "diagnostic.ask_pain_detail",
        optional=("answer_feedback",),
    ),
    "diagnostic.ask_priority": _tpl(
        "diagnostic.ask_priority",
        optional=("answer_feedback",),
    ),
    "diagnostic.ask_urgency": _tpl(
        "diagnostic.ask_urgency",
        optional=("answer_feedback",),
    ),
    "diagnostic.partial_progress": _tpl(
        "diagnostic.partial_progress",
        required=("answer_feedback",),
    ),
    "diagnostic.deliver": _tpl(
        "diagnostic.deliver",
        required=(
            "pain_context_human",
            "crm_base_recommendation",
            "operational_first_step",
            "recommended_plan_or_range",
            "demo_status",
        ),
    ),
    "diagnostic.deliver_hold": _tpl(
        "diagnostic.deliver_hold",
        optional=("first_name",),
    ),
    "diagnostic.deliver_context": _tpl(
        "diagnostic.deliver_context",
        required=("pain_context_human",),
    ),
    "diagnostic.deliver_crm_base": _tpl(
        "diagnostic.deliver_crm_base",
        required=("crm_base_recommendation",),
    ),
    "diagnostic.deliver_operational_step": _tpl(
        "diagnostic.deliver_operational_step",
        required=("operational_first_step",),
    ),
    "diagnostic.deliver_agent_recommendation": _tpl(
        "diagnostic.deliver_agent_recommendation",
        required=(
            "agent_name",
        ),
        optional=("agent_fit_phrase", "agent_recommendation_reason"),
    ),
    "diagnostic.deliver_plan_recommendation": _tpl(
        "diagnostic.deliver_plan_recommendation",
        required=("recommended_plan_or_range",),
    ),
    "diagnostic.deliver_demo_not_offered": _tpl(
        "diagnostic.deliver_demo_not_offered",
    ),
    "diagnostic.deliver_demo_already_offered": _tpl(
        "diagnostic.deliver_demo_already_offered",
        required=("demo_status",),
    ),
    "diagnostic.insufficient_evidence": _tpl(
        "diagnostic.insufficient_evidence",
        optional=("clarification_question",),
    ),
    "waitlist.offer_after_contract_intent": _tpl(
        "waitlist.offer_after_contract_intent",
    ),
    "waitlist.answer_question": _tpl(
        "waitlist.answer_question",
        required=("answer_feedback",),
    ),
    "waitlist.ask_missing_studio": _tpl(
        "waitlist.ask_missing_studio",
        optional=("missing_detail_label",),
    ),
    "waitlist.ask_missing_city": _tpl(
        "waitlist.ask_missing_city",
        optional=("missing_detail_label",),
    ),
    "waitlist.ask_missing_contact_path": _tpl(
        "waitlist.ask_missing_contact_path",
        optional=("missing_detail_label",),
    ),
    "waitlist.current_path_explained": _tpl("waitlist.current_path_explained"),
    "waitlist.joined": _tpl(
        "waitlist.joined",
        optional=("studio_name", "city_state", "contact_path"),
    ),
    "waitlist.pause_decision": _tpl("waitlist.pause_decision"),
    "waitlist.status_preserved": _tpl(
        "waitlist.status_preserved",
        optional=("waitlist_context_summary",),
    ),
    "handoff.acknowledge": _tpl(
        "handoff.acknowledge",
        optional=("handoff_reason",),
    ),
    "handoff.paused": _tpl("handoff.paused"),
    "fallback.invalid_json": _tpl("fallback.invalid_json"),
    "fallback.provider_timeout": _tpl("fallback.provider_timeout"),
    "fallback.product_knowledge_missing": _tpl(
        "fallback.product_knowledge_missing",
        optional=("human_confirmation_topic",),
    ),
    "fallback.cost_cap": _tpl("fallback.cost_cap"),
    "fallback.unmapped_adaptive": _tpl(
        "fallback.unmapped_adaptive",
        required=("clarification_question",),
    ),
    "fallback.unsupported_media": _tpl(
        "fallback.unsupported_media",
        optional=("unsupported_media_kind",),
    ),
    "safety.unsupported_media": _tpl(
        "safety.unsupported_media",
        optional=("unsupported_media_kind",),
    ),
    "safety.prompt_injection": _tpl(
        "safety.prompt_injection",
        optional=("safe_redirect_reason",),
    ),
    "safety.out_of_scope": _tpl(
        "safety.out_of_scope",
        optional=("safe_redirect_reason",),
    ),
    "safety.sensitive_data": _tpl(
        "safety.sensitive_data",
        optional=("safe_redirect_reason",),
    ),
    "safety.no_medical_advice": _tpl(
        "safety.no_medical_advice",
        optional=("safe_redirect_reason",),
    ),
}


def normalize_template_id(template_id: str) -> str:
    return template_id.split("#", 1)[0]


def validate_template_registry() -> list[str]:
    errors: list[str] = []
    for template_id, template in TEMPLATE_REGISTRY.items():
        if template.template_id != template_id:
            errors.append(f"template_key_mismatch:{template_id}")
        variables = template.required_variables + template.optional_variables
        if len(set(variables)) != len(variables):
            errors.append(f"duplicate_template_variable:{template_id}")
        for variable_name in variables:
            if variable_name not in VARIABLE_REGISTRY:
                errors.append(f"unknown_template_variable:{template_id}:{variable_name}")

    for variable_name, variable in VARIABLE_REGISTRY.items():
        if variable.name != variable_name:
            errors.append(f"variable_key_mismatch:{variable_name}")
        if not variable.allowed_sources:
            errors.append(f"missing_allowed_sources:{variable_name}")
        if not variable.validation_rule:
            errors.append(f"missing_validation_rule:{variable_name}")
        if variable.kind in {"short_text", "long_text", "list"} and variable.max_length is None:
            errors.append(f"missing_max_length:{variable_name}")
    return errors


def validate_render_plan_item_variables(item: RenderPlanItem) -> list[str]:
    template_id = normalize_template_id(item.template_id)
    template = TEMPLATE_REGISTRY.get(template_id)
    if template is None:
        return [f"unknown_template_id:{item.template_id}"]

    errors: list[str] = []
    required = set(template.required_variables)
    optional = set(template.optional_variables)
    allowed = required | optional
    provided = set(item.variables)

    for variable_name in sorted(required - provided):
        errors.append(f"missing_required_variable:{variable_name}")

    for variable_name in sorted(provided - allowed):
        errors.append(f"unknown_variable:{variable_name}")

    for variable_name in sorted(provided & FORBIDDEN_TEMPLATE_VARIABLE_NAMES):
        errors.append(f"forbidden_variable:{variable_name}")

    for variable_name in sorted(provided & allowed):
        variable = item.variables[variable_name]
        variable_spec = VARIABLE_REGISTRY[variable_name]
        if variable.kind != variable_spec.kind:
            errors.append(
                f"kind_mismatch:{variable_name}:{variable.kind}!={variable_spec.kind}"
            )
        if variable.source not in variable_spec.allowed_sources:
            errors.append(f"source_not_allowed:{variable_name}:{variable.source}")
        if variable_spec.max_length is not None:
            if variable.max_length is None and variable_spec.kind in {
                "short_text",
                "long_text",
                "list",
            }:
                errors.append(f"missing_max_length:{variable_name}")
            if (
                variable.max_length is not None
                and variable.max_length > variable_spec.max_length
            ):
                errors.append(
                    f"max_length_too_large:"
                    f"{variable_name}:{variable.max_length}>{variable_spec.max_length}"
                )
            if variable_spec.kind in {"short_text", "long_text"} and isinstance(
                variable.value, str
            ):
                if len(variable.value) > variable_spec.max_length:
                    errors.append(
                        f"value_too_long:"
                        f"{variable_name}:{len(variable.value)}>{variable_spec.max_length}"
                    )
            if variable_spec.kind == "list" and isinstance(variable.value, list):
                if len(variable.value) > variable_spec.max_length:
                    errors.append(
                        f"value_too_long:"
                        f"{variable_name}:{len(variable.value)}>{variable_spec.max_length}"
                    )

    return errors
