from __future__ import annotations

import inspect
import json
from collections.abc import Awaitable, Callable, Mapping
from typing import Any

from pydantic import Field, ValidationError

from app.core.taliya_commercial.conductor_policy import (
    SpecialistPolicyPack,
    get_specialist_policy_pack,
)
from app.core.taliya_commercial.context_snapshot import (
    ContextSnapshotRecord,
    build_context_snapshot,
    context_snapshot_to_json,
    replay_turn_context,
)
from app.core.taliya_commercial.schemas import (
    CRM_ALLOWED_REASON_VALUES,
    DEMO_CUSTOMER_FACING_CONCEPT,
    DEMO_EQUIVALENT_TERMS,
    DEMO_OUT_OF_SCOPE_TERMS,
    FORBIDDEN_DEMO_SCOPE_FIELDS,
    FORBIDDEN_TEMPLATE_VARIABLE_NAMES,
    STUDIO_OWNER_LANGUAGE_TERMS,
    ConductorActionDecision,
    ConductorDecision,
    ModelUsage,
    ProductKnowledgeRef,
    StrictModel,
    TurnContext,
)
from app.core.taliya_commercial.template_registry import TEMPLATE_REGISTRY, VARIABLE_REGISTRY
from app.core.taliya_commercial.turn_situation import (
    TurnSituation,
    build_turn_situation,
)

_LLM_HIDDEN_TEMPLATE_IDS = {
    "diagnostic.deliver",
}
_FACT_RELIABILITY_DEFAULT_BY_SOURCE = {
    "channel_metadata": "channel_provided",
    "operator": "operator_provided",
    "sales_inbox_projection": "unverified",
    "user_message": "customer_provided",
    "official_product_knowledge": "internal",
    "memory": "unverified",
}
_FACT_RELIABILITY_ALLOWED_BY_SOURCE = {
    "channel_metadata": {"channel_provided", "internal"},
    "operator": {"operator_provided"},
    "sales_inbox_projection": {"channel_provided", "inferred", "unverified"},
    "user_message": {"customer_provided", "inferred", "unverified"},
    "official_product_knowledge": {"internal"},
    "memory": {"customer_provided", "inferred", "unverified"},
}
_FACT_SOURCE_ALIASES = {
    "context": "memory",
    "conversation_state": "memory",
    "runtime_state": "memory",
    "state": "memory",
}


class ConductorError(Exception):
    """Base error for the isolated Spec 011 conductor boundary."""


class ConductorOutputError(ConductorError):
    """Raised when the provider does not return a JSON object."""


class ConductorDecisionValidationError(ConductorError):
    """Raised when provider JSON does not validate as the turn decision."""


class ConductorTurnResult(StrictModel):
    decision: ConductorDecision
    model_usage: ModelUsage


class ActionConductorTurnResult(StrictModel):
    decision: ConductorActionDecision
    model_usage: ModelUsage


type ConductorInput = TurnContext | ContextSnapshotRecord | str
type ConductorProviderOutput = ConductorTurnResult | Mapping[str, Any] | str
type ConductorProvider = Callable[
    ["ConductorProviderRequest"],
    ConductorProviderOutput | Awaitable[ConductorProviderOutput],
]
type ActionConductorProviderOutput = ActionConductorTurnResult | Mapping[str, Any] | str
type ActionConductorProvider = Callable[
    ["ActionConductorProviderRequest"],
    ActionConductorProviderOutput | Awaitable[ActionConductorProviderOutput],
]


class ConductorProviderRequest(StrictModel):
    request_schema_version: str = "011.conductor_request.v1"
    context: TurnContext
    context_snapshot_json: str
    specialist_policy: SpecialistPolicyPack
    response_schema: dict[str, Any]
    llm_must_decide: bool = True
    instructions: list[str] = Field(default_factory=list)
    provider_requirements: list[str] = Field(default_factory=list)


class ActionConductorProviderRequest(StrictModel):
    request_schema_version: str = "011.action_conductor_request.v1"
    context: TurnContext
    turn_situation: TurnSituation
    context_snapshot_json: str
    specialist_policy: SpecialistPolicyPack
    response_schema: dict[str, Any]
    llm_must_decide: bool = True
    instructions: list[str] = Field(default_factory=list)
    provider_requirements: list[str] = Field(default_factory=list)


def build_conductor_model_input_payload(
    request: ConductorProviderRequest,
) -> dict[str, Any]:
    return {
        "specialist_policy": _model_specialist_policy_payload(
            request.specialist_policy
        ),
        "provider_requirements": request.provider_requirements,
        "context": build_model_turn_context_payload(request.context),
    }


def build_action_conductor_model_input_payload(
    request: ActionConductorProviderRequest,
) -> dict[str, Any]:
    return {
        "specialist_policy": _model_specialist_policy_payload(
            request.specialist_policy
        ),
        "provider_requirements": request.provider_requirements,
        "turn_situation": request.turn_situation.model_dump(mode="json"),
        "context": build_model_turn_context_payload(request.context),
    }


def _model_specialist_policy_payload(policy: SpecialistPolicyPack) -> dict[str, Any]:
    payload = policy.model_dump(mode="json")
    payload.pop("global_rules", None)
    payload["global_rules_ref"] = "see_conductor_instructions"
    return payload


def build_model_turn_context_payload(context: TurnContext) -> dict[str, Any]:
    payload = context.model_dump(mode="json")
    payload["product_knowledge"] = [
        _model_product_knowledge_ref(ref) for ref in context.product_knowledge
    ]
    return payload


def _model_product_knowledge_ref(ref: ProductKnowledgeRef) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "key": ref.key,
        "source": ref.source,
        "evidence": list(ref.evidence),
    }
    if ref.missing:
        payload["missing"] = True
    if ref.excerpt is not None:
        payload["excerpt"] = ref.excerpt
    return payload


async def conduct_turn(
    conductor_input: ConductorInput,
    *,
    provider: ConductorProvider,
) -> ConductorTurnResult:
    context = _resolve_context(conductor_input)
    request = _build_provider_request(context)
    raw_output = await _call_provider(provider, request)
    result = _parse_provider_result(raw_output)
    result = _normalize_result_context_fields(result, context)
    _validate_decision_matches_context(result.decision, context)
    return result


async def conduct_action_turn(
    conductor_input: ConductorInput,
    *,
    provider: ActionConductorProvider,
) -> ActionConductorTurnResult:
    context = _resolve_context(conductor_input)
    turn_situation = build_turn_situation(context)
    request = _build_action_provider_request(context, turn_situation)
    raw_output = await _call_provider(provider, request)
    result = _parse_action_provider_result(raw_output)
    _validate_action_decision_matches_context_and_situation(
        result.decision,
        context,
        turn_situation,
    )
    return result


def _resolve_context(conductor_input: ConductorInput) -> TurnContext:
    if isinstance(conductor_input, TurnContext):
        return conductor_input
    return replay_turn_context(conductor_input)


def _build_action_provider_request(
    context: TurnContext,
    turn_situation: TurnSituation,
) -> ActionConductorProviderRequest:
    snapshot = build_context_snapshot(context)
    fact_source_rules = _format_fact_source_rules()
    return ActionConductorProviderRequest(
        context=context,
        turn_situation=turn_situation,
        context_snapshot_json=context_snapshot_to_json(snapshot),
        specialist_policy=get_specialist_policy_pack(),
        response_schema=build_action_conductor_response_schema(),
        instructions=[
            "Return only a JSON object that matches the ConductorActionDecision schema.",
            "Use turn_situation as the operational board for this turn.",
            "Choose exactly one selected_action from turn_situation.allowed_actions.",
            "Interpret the latest inbound message commercially; deterministic code has "
            "not interpreted it for you.",
            "Do not return route, previous_state, current_state, next_state, "
            "template_plan, render_plan, rendered text, or whole-response variables.",
            "Use captured_slots only for values you interpreted from the inbound "
            "message or reliable context, and include evidence for every captured slot.",
            "Keep numeric_interpretations separated by kind: plan_price, "
            "student_count, phone, date_time, or unknown_number.",
            "Answer direct questions in direct_question.answer_obligations before "
            "diagnostic, waitlist, demo, or handoff steering.",
            "Use product_fact_keys_used only for official keys present in "
            "turn_situation.official_fact_keys_available.",
            "Use facts only for lead/context facts that should update memory. Do not "
            "store official product prices, plan catalog claims, or template copy as facts. "
            f"Allowed fact source/reliability pairs: {fact_source_rules}.",
            "For selected_action=offer_diagnostic_from_pain, diagnostic_intent.details "
            "must include pain_context_human: one practical customer-facing sentence "
            "grounded in the latest inbound and reusing concrete lead terms such as "
            "the channel, pain, audience, or delay they mentioned. Do not use generic "
            "phrases like 'existe um ponto da rotina'.",
            "The compiler, not the LLM, will derive state transition and template groups "
            "from selected_action after this action decision passes validation.",
        ],
        provider_requirements=[
            "The LLM response must be only the ConductorActionDecision JSON that matches "
            "response_schema.",
            "selected_action must be one item from turn_situation.allowed_actions.",
            "Do not include model_usage, usage, response text, route, state fields, "
            "template_plan, render_plan, or wrapper/envelope fields inside the action JSON.",
            "The runtime provider wrapper attaches model_usage from provider metadata "
            "after the LLM response is received.",
        ],
    )


def _build_provider_request(context: TurnContext) -> ConductorProviderRequest:
    snapshot = build_context_snapshot(context)
    forbidden_response_fields = _format_forbidden_whole_response_fields()
    studio_language_terms = _format_studio_owner_language_terms()
    crm_allowed_reasons = _format_crm_allowed_reasons()
    demo_equivalent_terms = _format_demo_equivalent_terms()
    demo_out_of_scope_terms = _format_demo_out_of_scope_terms()
    registered_templates = _format_registered_template_catalog()
    fact_source_rules = _format_fact_source_rules()
    return ConductorProviderRequest(
        context=context,
        context_snapshot_json=context_snapshot_to_json(snapshot),
        specialist_policy=get_specialist_policy_pack(),
        response_schema=build_conductor_response_schema(),
        instructions=[
            "Return only a JSON object that matches the ConductorDecision schema.",
            "Use specialist_policy as guidance inside this single conductor call.",
            "Return a flat ConductorDecision object: language_policy, template_plan, "
            "policy_checks, waitlist, handoff, demo, facts, confidence, and repair_hints "
            "are top-level siblings of diagnostic. Never nest those fields under diagnostic.",
            "The diagnostic object may contain only action, ledger_updates, "
            "next_question_key, and final_fields.",
            "The LLM owns route, role, intent, state, facts, diagnostic, waitlist, "
            "handoff, demo, and template-plan decisions for normal commercial turns.",
            "If channel/context says entry_intent=site_cta and the inbound text is only "
            "a general request to know Taliya better, keep route=entry and choose "
            "opening.site_cta or opening.general_interest. Do not start diagnostic "
            "unless the lead explicitly asks for or accepts the diagnostic; if the "
            "opening template offers the free diagnostic, set diagnostic.action=offer.",
            "If source or utm_source is Instagram and the lead mentions Instagram, "
            "use detected_intents source_from_instagram and template "
            "opening.instagram_source.",
            "If entry_intent=diagnostic_cta or the lead explicitly asks for the free "
            "diagnostic, then use the diagnostic route and opening.diagnostic_cta "
            "before any diagnostic question.",
            "Every facts item and numeric_interpretations item must include evidence "
            "from the inbound text, context, or official source keys.",
            "For rich one-turn diagnostic requests, extract or infer all six mandatory "
            "diagnostic keys from grounded inbound/context evidence when possible. If "
            "only pain_detail is not named as a field but the pain is described, mark "
            "pain_detail inferred_from_prior_message and complete the diagnostic.",
            "For direct integration, Instagram integration, or current-system questions, "
            "use product.integration_scope_direct and answer conservatively from official "
            "scope. Do not route straight to handoff unless the lead explicitly asks for "
            "a person; human confirmation can be marked after the safe product answer.",
            "Use facts only for lead/context facts that should update memory. Do not "
            "store official product prices, plan catalog claims, or template copy as facts. "
            f"Allowed fact source/reliability pairs: {fact_source_rules}.",
            "Keep numeric_interpretations separated by kind: plan_price, "
            "student_count, phone, date_time, or unknown_number.",
            "Choose registered template ids and template variables in template_plan; "
            "do not use whole-response fields or variables for customer-facing prose.",
            "Use only template ids from this registered catalog. Include every required "
            "variable for the chosen template and do not invent template ids. Catalog: "
            f"{registered_templates}.",
            "For completed diagnostics, use the staged diagnostic.deliver_* sequence. "
            "Never use the legacy exact template id diagnostic.deliver in template_plan.",
            "Completed diagnostic plan recommendations must use only official plan/range "
            "values and evidence that resolves to product_knowledge.plans or an approved "
            "Spec 006 product contract key.",
            "Keep completed diagnostic template variables concise; prefer one clear "
            "studio-owner sentence per staged template variable.",
            "Do not return generic whole-response fields anywhere in the provider "
            f"envelope, decision, or template variables: {forbidden_response_fields}.",
            "Use practical studio-owner language by default. Prefer these terms: "
            f"{studio_language_terms}.",
            "CRM is not the default customer-facing label. Use CRM only when "
            "language_policy.crm_term_policy is allowed_with_evidence and evidence "
            f"supports one of these reasons: {crm_allowed_reasons}.",
            "Set language_policy.register to studio_owner_practical. Use "
            "avoid_by_default unless CRM is actually allowed with reason and evidence.",
            "Treat commercial demo, product demo, demo, demonstration, and "
            f"ver funcionando as one customer-facing concept: {DEMO_CUSTOMER_FACING_CONCEPT}. "
            f"Equivalent terms: {demo_equivalent_terms}.",
            "Use the existing demo structured fields for this concept; do not create "
            "technical-demo, video-demo, or demo-asset routes, fields, or tools.",
            "Set demo.next_step=offer_demo only when the user explicitly asks for "
            "the commercial product demo or an active demo flow requires it, and "
            "include an approved demo offer template in template_plan. For price-only "
            "turns, leave demo.status=not_offered and demo.next_step=none.",
            "For price objections, value concerns, discount requests, or ROI concerns, "
            "detect the concern explicitly and include product.price_objection_value "
            "before any diagnostic, waitlist, demo, or handoff next step.",
            "Keep OpenAI technical reference demo, video production, and visual demo "
            f"assets out of scope for this conductor: {demo_out_of_scope_terms}.",
            "Fill every policy_checks boolean explicitly; use false when uncertain. "
            "These self-checks are not final validation and never bypass validators.",
            "Do not return customer-facing free-form assistant text.",
        ],
        provider_requirements=[
            "The LLM response must be only the ConductorDecision JSON that matches "
            "response_schema.",
            "Do not include model_usage, usage, response text, or wrapper/envelope fields "
            "inside the ConductorDecision JSON; model_usage must stay outside the LLM "
            "decision JSON.",
            "The runtime provider wrapper attaches model_usage from provider metadata "
            "after the LLM response is received.",
            f"Never add whole-response fields: {forbidden_response_fields}.",
        ],
    )


def build_conductor_response_schema() -> dict[str, Any]:
    schema = _openai_strict_json_schema(ConductorDecision.model_json_schema())
    properties = schema.get("properties")
    if isinstance(properties, dict) and isinstance(
        properties.get("schema_version"),
        dict,
    ):
        properties["schema_version"] = {
            **properties["schema_version"],
            "const": "011.0",
        }
    return schema


def build_action_conductor_response_schema() -> dict[str, Any]:
    schema = _openai_strict_json_schema(ConductorActionDecision.model_json_schema())
    properties = schema.get("properties")
    if isinstance(properties, dict) and isinstance(
        properties.get("schema_version"),
        dict,
    ):
        properties["schema_version"] = {
            **properties["schema_version"],
            "const": "011.action_decision.v1",
        }
    return schema


def _openai_strict_json_schema(value: Any, *, _is_root: bool = True) -> Any:
    if isinstance(value, list):
        return [
            _openai_strict_json_schema(item, _is_root=False)
            for item in value
        ]
    if not isinstance(value, dict):
        return value

    schema = {
        key: _openai_strict_json_schema(item, _is_root=False)
        for key, item in value.items()
        if key != "default" and (key != "title" or _is_root)
    }
    properties = schema.get("properties")
    if isinstance(properties, dict):
        schema["required"] = list(properties.keys())
        schema.setdefault("additionalProperties", False)
    return schema


async def _call_provider(
    provider: ConductorProvider,
    request: ConductorProviderRequest,
) -> ConductorProviderOutput:
    result = provider(request)
    if inspect.isawaitable(result):
        return await result
    return result


def _parse_provider_result(raw_output: ConductorProviderOutput) -> ConductorTurnResult:
    if isinstance(raw_output, ConductorTurnResult):
        return raw_output

    payload: Any
    if isinstance(raw_output, str):
        try:
            payload = json.loads(raw_output)
        except json.JSONDecodeError as exc:
            raise ConductorOutputError("conductor provider returned non-JSON content") from exc
    elif isinstance(raw_output, Mapping):
        payload = dict(raw_output)
    else:
        raise ConductorOutputError("conductor provider returned unsupported content")

    if not isinstance(payload, dict):
        raise ConductorOutputError("conductor provider JSON must be an object")

    payload = _normalize_provider_payload(payload)
    _reject_forbidden_whole_response_fields(payload)
    _reject_forbidden_demo_scope_fields(payload)

    if "decision" not in payload or "model_usage" not in payload:
        raise ConductorDecisionValidationError(
            "conductor provider output requires decision and model_usage"
        )

    try:
        return ConductorTurnResult.model_validate(payload)
    except ValidationError as exc:
        error_summary = json.dumps(
            exc.errors(include_url=False, include_input=False)[:12],
            ensure_ascii=True,
            default=str,
            separators=(",", ":"),
        )
        raise ConductorDecisionValidationError(
            "conductor provider output failed ConductorTurnResult validation:"
            + error_summary
        ) from exc


def _parse_action_provider_result(
    raw_output: ActionConductorProviderOutput,
) -> ActionConductorTurnResult:
    if isinstance(raw_output, ActionConductorTurnResult):
        return raw_output

    payload: Any
    if isinstance(raw_output, str):
        try:
            payload = json.loads(raw_output)
        except json.JSONDecodeError as exc:
            raise ConductorOutputError("conductor provider returned non-JSON content") from exc
    elif isinstance(raw_output, Mapping):
        payload = dict(raw_output)
    else:
        raise ConductorOutputError("conductor provider returned unsupported content")

    if not isinstance(payload, dict):
        raise ConductorOutputError("conductor provider JSON must be an object")

    _reject_forbidden_whole_response_fields(payload)
    _reject_forbidden_demo_scope_fields(payload)

    if "decision" not in payload or "model_usage" not in payload:
        raise ConductorDecisionValidationError(
            "action conductor provider output requires decision and model_usage"
        )

    try:
        return ActionConductorTurnResult.model_validate(payload)
    except ValidationError as exc:
        error_summary = json.dumps(
            exc.errors(include_url=False, include_input=False)[:12],
            ensure_ascii=True,
            default=str,
            separators=(",", ":"),
        )
        raise ConductorDecisionValidationError(
            "action conductor provider output failed ActionConductorTurnResult validation:"
            + error_summary
        ) from exc


def _normalize_provider_payload(payload: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)
    decision_payload = normalized.get("decision")
    if isinstance(decision_payload, Mapping):
        normalized_decision = dict(decision_payload)
        normalized_decision = _normalize_decision_alias_fields(normalized_decision)
        normalized_decision = _drop_output_only_decision_fields(normalized_decision)
        render_plan = normalized_decision.pop("render_plan", None)
        if "template_plan" not in normalized_decision and render_plan is not None:
            normalized_decision["template_plan"] = render_plan
        normalized_facts = _normalize_fact_reliability(normalized_decision.get("facts"))
        if normalized_facts is not None:
            normalized_decision["facts"] = normalized_facts
        normalized_diagnostic = _normalize_diagnostic_payload(
            normalized_decision.get("diagnostic")
        )
        if normalized_diagnostic is not None:
            normalized_decision["diagnostic"] = normalized_diagnostic
        normalized_demo = _normalize_demo_payload(normalized_decision.get("demo"))
        if normalized_demo is not None:
            normalized_decision["demo"] = normalized_demo
        normalized_waitlist = _normalize_waitlist_payload(
            normalized_decision.get("waitlist")
        )
        if normalized_waitlist is not None:
            normalized_decision["waitlist"] = normalized_waitlist
        normalized_decision = _hoist_template_item_decision_fields(normalized_decision)
        normalized_policy_checks = _normalize_policy_checks_payload(
            normalized_decision.get("policy_checks")
        )
        if normalized_policy_checks is not None:
            normalized_decision["policy_checks"] = normalized_policy_checks
        normalized_template_plan = _normalize_template_variable_evidence(
            normalized_decision.get("template_plan")
        )
        if normalized_template_plan is not None:
            normalized_decision["template_plan"] = normalized_template_plan
        normalized["decision"] = normalized_decision
    return normalized


def _normalize_decision_alias_fields(
    decision_payload: dict[str, Any],
) -> dict[str, Any]:
    normalized = dict(decision_payload)
    aliases = {
        "diagnostic_decision": "diagnostic",
        "waitlist_decision": "waitlist",
        "handoff_decision": "handoff",
        "demo_decision": "demo",
    }
    for alias, canonical in aliases.items():
        value = normalized.pop(alias, None)
        if canonical not in normalized and value is not None:
            normalized[canonical] = value
    return normalized


def _drop_output_only_decision_fields(
    decision_payload: dict[str, Any],
) -> dict[str, Any]:
    output_only_fields = {
        "diagnostic_allowed_now",
        "diagnostic_ledger_status",
        "diagnostic_status",
        "facts_missing",
        "facts_used",
        "next_question_kind",
        "opening_type",
        "profile_name_usage",
        "template_ids",
        "template_variables",
        "waitlist_allowed_now",
    }
    return {
        key: value
        for key, value in decision_payload.items()
        if key not in output_only_fields
    }


def _hoist_template_item_decision_fields(
    decision_payload: dict[str, Any],
) -> dict[str, Any]:
    template_plan = decision_payload.get("template_plan")
    if not isinstance(template_plan, Mapping):
        return decision_payload
    items = template_plan.get("items")
    if not isinstance(items, list):
        return decision_payload

    hoistable = {"policy_checks", "confidence", "repair_hints"}
    clean_items: list[Any] = []
    changed = False
    for item in items:
        if not isinstance(item, Mapping):
            clean_items.append(item)
            continue
        item_dict = dict(item)
        for field in hoistable:
            if field not in decision_payload and field in item_dict:
                decision_payload[field] = item_dict[field]
                changed = True
        clean_item = {
            key: value
            for key, value in item_dict.items()
            if key in {"template_id", "channel", "variables"}
        }
        if clean_item != item_dict:
            changed = True
        clean_items.append(clean_item)

    if changed:
        decision_payload["template_plan"] = {
            **dict(template_plan),
            "items": clean_items,
        }
    return decision_payload


def _normalize_fact_reliability(raw_facts: Any) -> Any:
    if not isinstance(raw_facts, list):
        return raw_facts
    normalized: list[Any] = []
    for fact in raw_facts:
        if not isinstance(fact, Mapping):
            normalized.append(fact)
            continue
        normalized_fact = dict(fact)
        source = normalized_fact.get("source")
        if source in _FACT_SOURCE_ALIASES:
            source = _FACT_SOURCE_ALIASES[source]
            normalized_fact["source"] = source
        reliability = normalized_fact.get("reliability")
        allowed = _FACT_RELIABILITY_ALLOWED_BY_SOURCE.get(source)
        if allowed is not None and reliability not in allowed:
            normalized_fact["reliability"] = _FACT_RELIABILITY_DEFAULT_BY_SOURCE[source]
        if source in {"channel_metadata", "official_product_knowledge"}:
            normalized_fact["renderable"] = False
        elif not isinstance(normalized_fact.get("renderable"), bool):
            normalized_fact["renderable"] = False
        if normalized_fact.get("confidence") not in {"low", "medium", "high", None}:
            normalized_fact["confidence"] = "medium"
        normalized.append(normalized_fact)
    return normalized


def _normalize_diagnostic_payload(raw_diagnostic: Any) -> Any:
    if raw_diagnostic is None:
        return {}
    if not isinstance(raw_diagnostic, Mapping):
        return {}
    allowed = {"action", "ledger_updates", "next_question_key", "final_fields"}
    return {
        key: value
        for key, value in dict(raw_diagnostic).items()
        if key in allowed
    }


def _normalize_policy_checks_payload(raw_policy_checks: Any) -> Any:
    if not isinstance(raw_policy_checks, Mapping):
        return raw_policy_checks
    return dict(raw_policy_checks)


def _normalize_demo_payload(raw_demo: Any) -> Any:
    if not isinstance(raw_demo, Mapping):
        return raw_demo
    demo = dict(raw_demo)
    status = str(demo.get("status") or "").strip().lower()
    status_aliases = {
        "asked": "viewed_or_asked",
        "requested": "viewed_or_asked",
        "demo_requested": "viewed_or_asked",
        "viewed_or_requested": "viewed_or_asked",
        "already_asked": "viewed_or_asked",
        "sent": "offered",
        "offered_demo": "offered",
        "positive": "reacted_positive",
        "liked": "reacted_positive",
    }
    if status in status_aliases:
        demo["status"] = status_aliases[status]

    next_step = str(demo.get("next_step") or "").strip().lower()
    next_step_aliases = {
        "offer": "offer_demo",
        "send_demo": "offer_demo",
        "send_link": "offer_demo",
        "demo_link": "offer_demo",
        "ask_reaction": "ask_demo_reaction",
        "ask_feedback": "ask_demo_reaction",
        "follow_positive": "follow_positive_demo_interest",
    }
    if next_step in next_step_aliases:
        demo["next_step"] = next_step_aliases[next_step]
    return demo


def _normalize_waitlist_payload(raw_waitlist: Any) -> Any:
    if not isinstance(raw_waitlist, Mapping):
        return raw_waitlist
    waitlist = dict(raw_waitlist)
    status = str(waitlist.get("status") or "").strip().lower()
    status_aliases = {
        "pending": "pending_details",
        "pending_detail": "pending_details",
        "pending_data": "pending_details",
        "needs_details": "pending_details",
        "missing_details": "pending_details",
        "requested": "offered",
        "request": "offered",
        "interested": "offered",
        "interest": "offered",
        "wants_to_join": "offered",
        "want_to_join": "offered",
        "ready_to_start": "offered",
        "contract_intent": "offered",
        "added": "joined",
        "registered": "joined",
        "on_waitlist": "joined",
        "confirmed": "joined",
        "accepted": "joined",
    }
    if status in status_aliases:
        waitlist["status"] = status_aliases[status]
    return waitlist


def _normalize_template_variable_evidence(raw_template_plan: Any) -> Any:
    if not isinstance(raw_template_plan, Mapping):
        return raw_template_plan
    normalized_plan = dict(raw_template_plan)
    raw_items = normalized_plan.get("items")
    if not isinstance(raw_items, list):
        return normalized_plan

    normalized_items: list[Any] = []
    for item in raw_items:
        if isinstance(item, str):
            normalized_items.append({"template_id": item})
            continue
        if not isinstance(item, Mapping):
            normalized_items.append(item)
            continue
        normalized_item = dict(item)
        if "template_id" not in normalized_item:
            for alias in ("templateId", "template", "id"):
                if alias in normalized_item:
                    normalized_item["template_id"] = normalized_item.pop(alias)
                    break
        variables = normalized_item.get("variables")
        if isinstance(variables, Mapping):
            normalized_item["variables"] = {
                variable_name: _normalize_template_variable(variable_name, variable)
                for variable_name, variable in variables.items()
            }
        normalized_items.append(normalized_item)
    normalized_plan["items"] = normalized_items
    return normalized_plan


def _normalize_template_variable(variable_name: str, raw_variable: Any) -> Any:
    variable_spec = VARIABLE_REGISTRY.get(variable_name)
    if not isinstance(raw_variable, Mapping):
        if variable_spec is None:
            return raw_variable
        source = _default_template_variable_source(variable_name)
        return {
            "kind": variable_spec.kind,
            "value": raw_variable,
            "source": source,
            "evidence": _default_template_variable_evidence(variable_name, source),
            "max_length": variable_spec.max_length,
        }

    variable = dict(raw_variable)
    if variable.get("max_length") is None and variable_spec is not None:
        variable["max_length"] = variable_spec.max_length
    evidence = variable.get("evidence")
    if isinstance(evidence, list) and evidence:
        return variable
    source = variable.get("source")
    if source in {"runtime_state", "model_decision"}:
        variable["evidence"] = [str(source)]
    return variable


def _default_template_variable_source(variable_name: str) -> str:
    variable_spec = VARIABLE_REGISTRY[variable_name]
    if variable_name in {
        "agent_name",
        "recommended_plan_or_range",
        "plan_name",
        "plan_price_summary",
        "official_demo_link",
        "product_fact_summary",
    } and "official_product_knowledge" in variable_spec.allowed_sources:
        return "official_product_knowledge"
    if variable_name == "demo_status" and "runtime_state" in variable_spec.allowed_sources:
        return "runtime_state"
    if "diagnostic_ledger" in variable_spec.allowed_sources:
        return "diagnostic_ledger"
    if "model_decision" in variable_spec.allowed_sources:
        return "model_decision"
    if "runtime_state" in variable_spec.allowed_sources:
        return "runtime_state"
    return sorted(variable_spec.allowed_sources)[0]


def _default_template_variable_evidence(variable_name: str, source: str) -> list[str]:
    if source == "official_product_knowledge":
        if "price" in variable_name:
            return ["product_knowledge.prices"]
        if "demo" in variable_name:
            return ["product_knowledge.demo_status"]
        return ["product_knowledge.plans"]
    if source == "diagnostic_ledger":
        return ["diagnostic_ledger"]
    if source == "runtime_state":
        return [f"runtime_state.{variable_name}"]
    return [source]


def _format_forbidden_whole_response_fields() -> str:
    return ", ".join(sorted(FORBIDDEN_TEMPLATE_VARIABLE_NAMES))


def _format_studio_owner_language_terms() -> str:
    return ", ".join(STUDIO_OWNER_LANGUAGE_TERMS)


def _format_crm_allowed_reasons() -> str:
    return ", ".join(CRM_ALLOWED_REASON_VALUES)


def _format_demo_equivalent_terms() -> str:
    return ", ".join(DEMO_EQUIVALENT_TERMS)


def _format_demo_out_of_scope_terms() -> str:
    return ", ".join(DEMO_OUT_OF_SCOPE_TERMS)


def _format_registered_template_catalog() -> str:
    catalog = {
        template_id: [
            list(template.required_variables),
            list(template.optional_variables),
        ]
        for template_id, template in sorted(TEMPLATE_REGISTRY.items())
        if template_id not in _LLM_HIDDEN_TEMPLATE_IDS
    }
    variable_catalog = {
        name: [
            variable.kind,
            sorted(variable.allowed_sources),
            variable.max_length,
            variable.validation_rule,
        ]
        for name, variable in sorted(VARIABLE_REGISTRY.items())
    }
    return json.dumps(
        {
            "template_format": "id:[required_variables,optional_variables]",
            "templates": catalog,
            "variable_format": "name:[kind,allowed_sources,max_length,validation_rule]",
            "variables": variable_catalog,
        },
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )


def _format_fact_source_rules() -> str:
    return json.dumps(
        {
            "user_message": ["customer_provided", "inferred", "unverified"],
            "channel_metadata": ["channel_provided", "internal"],
            "operator": ["operator_provided"],
            "sales_inbox_projection": ["channel_provided", "inferred", "unverified"],
            "official_product_knowledge": ["internal"],
            "memory": ["customer_provided", "inferred", "unverified"],
        },
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )


def _reject_forbidden_whole_response_fields(payload: Mapping[str, Any]) -> None:
    locations = _forbidden_field_locations(payload, "provider")

    decision_payload = payload.get("decision")
    if isinstance(decision_payload, Mapping):
        locations.extend(_forbidden_field_locations(decision_payload, "decision"))

        template_plan = decision_payload.get("template_plan")
        if isinstance(template_plan, Mapping):
            items = template_plan.get("items")
            if isinstance(items, list):
                for index, item in enumerate(items):
                    if not isinstance(item, Mapping):
                        continue
                    variables = item.get("variables")
                    if isinstance(variables, Mapping):
                        locations.extend(
                            _forbidden_field_locations(
                                variables,
                                f"decision.template_plan.items[{index}].variables",
                            )
                        )

    if locations:
        joined = ", ".join(sorted(locations))
        raise ConductorDecisionValidationError(
            "conductor provider output contains forbidden whole-response fields: "
            + joined
        )


def _forbidden_field_locations(payload: Mapping[str, Any], path: str) -> list[str]:
    return [
        f"{path}.{field_name}"
        for field_name in sorted(FORBIDDEN_TEMPLATE_VARIABLE_NAMES.intersection(payload))
    ]


def _reject_forbidden_demo_scope_fields(payload: Mapping[str, Any]) -> None:
    locations = _forbidden_demo_field_locations(payload, "provider")

    decision_payload = payload.get("decision")
    if isinstance(decision_payload, Mapping):
        locations.extend(_forbidden_demo_field_locations(decision_payload, "decision"))
        demo_payload = decision_payload.get("demo")
        if isinstance(demo_payload, Mapping):
            locations.extend(
                _forbidden_demo_field_locations(demo_payload, "decision.demo")
            )

    if locations:
        joined = ", ".join(sorted(locations))
        raise ConductorDecisionValidationError(
            "conductor provider output contains out-of-scope demo fields: " + joined
        )


def _forbidden_demo_field_locations(payload: Mapping[str, Any], path: str) -> list[str]:
    return [
        f"{path}.{field_name}"
        for field_name in sorted(FORBIDDEN_DEMO_SCOPE_FIELDS.intersection(payload))
    ]


def _validate_decision_matches_context(
    decision: ConductorDecision,
    context: TurnContext,
) -> None:
    mismatches: list[str] = []
    if decision.turn_id != context.turn_id:
        mismatches.append("turn_id")
    if decision.conversation_id != context.conversation_id:
        mismatches.append("conversation_id")
    if decision.agent_key != context.agent_key:
        mismatches.append("agent_key")
    if decision.channel != context.channel:
        mismatches.append("channel")
    if mismatches:
        joined = ", ".join(mismatches)
        raise ConductorDecisionValidationError(
            f"conductor decision does not match context fields: {joined}"
        )


def _validate_action_decision_matches_context_and_situation(
    decision: ConductorActionDecision,
    context: TurnContext,
    turn_situation: TurnSituation,
) -> None:
    mismatches: list[str] = []
    if decision.turn_id != context.turn_id:
        mismatches.append("turn_id")
    if decision.conversation_id != context.conversation_id:
        mismatches.append("conversation_id")
    if decision.agent_key != context.agent_key:
        mismatches.append("agent_key")
    if decision.channel != context.channel:
        mismatches.append("channel")
    if decision.selected_action not in turn_situation.allowed_actions:
        mismatches.append("selected_action")
    unknown_product_keys = [
        key
        for key in decision.product_fact_keys_used
        if key not in turn_situation.official_fact_keys_available
    ]
    if unknown_product_keys:
        mismatches.append("product_fact_keys_used")
    if (
        decision.selected_action == "offer_diagnostic_from_pain"
        and not _non_empty_detail(decision.diagnostic_intent.details, "pain_context_human")
    ):
        mismatches.append("diagnostic_intent.details.pain_context_human")
    if mismatches:
        joined = ", ".join(mismatches)
        raise ConductorDecisionValidationError(
            f"action conductor decision does not match turn situation: {joined}"
        )


def _non_empty_detail(details: Mapping[str, Any], key: str) -> bool:
    value = details.get(key)
    return isinstance(value, str) and bool(value.strip())


def _normalize_result_context_fields(
    result: ConductorTurnResult,
    context: TurnContext,
) -> ConductorTurnResult:
    decision = result.decision
    normalized = decision.model_copy(
        update={
            "conversation_id": context.conversation_id,
        }
    )
    if normalized == decision:
        return result
    return result.model_copy(update={"decision": normalized})
