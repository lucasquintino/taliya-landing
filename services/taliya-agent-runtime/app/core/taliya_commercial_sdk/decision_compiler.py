"""T012-030C: deterministic Decision Compiler.

Expands a valid `ConductorActionDecision` plus `TurnSituation` into the
runtime shape: canonical state transition, diagnostic ledger merge, template
plan (including the FULL staged final diagnostic), official-source variables,
Sales Inbox projection inputs, and chunk policy.

Boundaries (`011/action-contract.md`):
- never overrides the LLM's interpreted intent or reads raw text; it may
  correct action FORM when the LLM already declared the structured product
  signal (e.g. price/demo fact key or intent) but picked a steering action;
- never reads raw lead text (no text parameter, like the situation builder);
- never invents customer-facing semantic prose - model compositions carry the
  prose; the compiler carries structure and official facts;
- an action missing its required composition variables FAILS compilation
  (T011-105 lesson: no silent generic fallback).
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from app.core.taliya_commercial.template_registry import TEMPLATE_REGISTRY
from app.core.taliya_commercial_sdk.conductor_decision import (
    ConductorActionDecision,
    composition_variable_names,
    validate_action_decision,
)
from app.core.taliya_commercial_sdk.turn_situation import TurnSituation
from app.core.taliya_commercial_sdk.validators_adapter import (
    DIAGNOSTIC_ASK_TEMPLATE_BY_KEY,
    DIAGNOSTIC_MANDATORY_KEYS,
)

_COMPLETE_STATUSES = {"answered", "inferred_from_prior_message", "not_applicable"}

# Composition variables an action cannot compile without (T011-105 lesson).
REQUIRED_COMPOSITIONS_BY_ACTION: dict[str, tuple[str, ...]] = {
    "offer_diagnostic_from_pain": ("pain_context_human",),
    "complete_diagnostic": (
        "pain_context_human",
        "crm_base_recommendation",
        "operational_first_step",
    ),
    "handoff_requested": ("handoff_reason",),
    "pause_for_human": ("handoff_reason",),
    "clarify_ambiguous_opening": ("clarification_question",),
    "clarify_ambiguous_diagnostic_answer": ("clarification_question",),
    "clarify_ambiguous_followup": ("clarification_question",),
    "clarify_product_question": ("clarification_question",),
    "answer_plan_fit_with_diagnostic_offer": ("plan_fit_context",),
    "answer_integration_scope_safely": ("integration_topic",),
    "offer_or_join_waitlist_if_eligible": ("waitlist_context_summary",),
    "offer_waitlist": ("waitlist_context_summary",),
}

# Canonical state transition per action: (current_state, next_state).
_STATE_BY_ACTION: dict[str, tuple[str, str]] = {
    "answer_general_interest": ("general_interest", "general_interest"),
    "answer_source_opening": ("source_instagram", "general_interest"),
    "offer_diagnostic_from_pain": ("pain_detected", "diagnostic_offered"),
    "answer_direct_product_question": ("product_question", "product_question"),
    "start_requested_diagnostic": ("diagnostic_requested", "diagnostic_waiting_answer"),
    "handoff_requested": ("human_requested", "human_handoff"),
    "clarify_ambiguous_opening": ("unknown_or_low_confidence", "general_interest"),
    "capture_pending_diagnostic_answer": (
        "diagnostic_in_progress",
        "diagnostic_waiting_answer",
    ),
    "answer_direct_question_then_continue_diagnostic": (
        "diagnostic_in_progress",
        "diagnostic_waiting_answer",
    ),
    "ask_next_diagnostic_question": (
        "diagnostic_in_progress",
        "diagnostic_waiting_answer",
    ),
    "complete_diagnostic": ("diagnostic_ready", "diagnostic_delivered"),
    "clarify_ambiguous_diagnostic_answer": (
        "diagnostic_in_progress",
        "diagnostic_waiting_answer",
    ),
    "respect_diagnostic_refusal": ("product_question", "general_interest"),
    "answer_product_question_with_saved_context": (
        "post_diagnostic_questions",
        "post_diagnostic_questions",
    ),
    "send_demo": ("demo_offered", "demo_reaction_pending"),
    "answer_price_objection_with_context": (
        "post_diagnostic_questions",
        "post_diagnostic_questions",
    ),
    "offer_or_join_waitlist_if_eligible": ("waitlist_eligible", "waitlist_offered"),
    "ask_demo_reaction": ("demo_reaction_pending", "demo_reaction_pending"),
    "clarify_ambiguous_followup": (
        "post_diagnostic_questions",
        "post_diagnostic_questions",
    ),
    "answer_price": ("price_question", "diagnostic_offered"),
    "answer_plan_fit_with_diagnostic_offer": ("plan_question", "diagnostic_offered"),
    "answer_how_it_works": ("product_question", "diagnostic_offered"),
    "answer_whatsapp_scope": ("product_question", "product_question"),
    "answer_integration_scope_safely": ("product_question", "product_question"),
    "answer_comparison_current_tool": ("product_question", "product_question"),
    "answer_security_and_data": ("product_question", "product_question"),
    "answer_availability_and_onboarding": ("product_question", "product_question"),
    "answer_out_of_profile": ("out_of_scope", "out_of_scope"),
    "answer_price_objection": ("price_question", "diagnostic_offered"),
    "offer_diagnostic_after_answer": ("product_question", "diagnostic_offered"),
    "clarify_product_question": ("product_question", "product_question"),
    "offer_waitlist": ("waitlist_eligible", "waitlist_offered"),
    "collect_waitlist_missing_detail": ("waitlist_pending_data", "waitlist_pending_data"),
    "join_waitlist": ("waitlist_pending_data", "waitlist_joined"),
    "decline_waitlist": ("waitlist_offered", "post_diagnostic_questions"),
    "answer_question_then_continue_waitlist": (
        "waitlist_pending_data",
        "waitlist_pending_data",
    ),
    "pause_for_human": ("human_handoff", "paused_by_human"),
    "resume_only_with_explicit_resume_event": ("paused_by_human", "paused_by_human"),
    "suppress_ai_reply_while_human_active": ("paused_by_human", "paused_by_human"),
}

# Product answer template by official fact key (signal = the LLM's structured
# fact-key choice, never raw text).
_PRODUCT_TEMPLATE_BY_FACT_KEY: tuple[tuple[str, str], ...] = (
    ("prices", "product.price_direct"),
    ("plans", "product.price_direct"),
    ("demo_link", "product.demo_direct"),
    ("whatsapp_scope", "product.whatsapp_direct"),
    ("how_it_works", "product.how_it_works_direct"),
    ("routine_areas", "product.overview_short"),
    ("integration_scope", "product.integration_scope_direct"),
    ("comparison_spreadsheet", "product.comparison_current_tool"),
    ("comparison_management_system", "product.comparison_current_tool"),
    ("security_and_data", "product.security_data_direct"),
    ("availability_and_onboarding", "product.overview_short"),
    ("out_of_profile", "product.out_of_profile_redirect"),
)

_DIAGNOSTIC_FEEDBACK_BY_CAPTURED_KEY: dict[str, str] = {
    "active_students_or_size": ("Entendi. Já dá para ter uma noção do tamanho do studio."),
    "main_pain": "Entendi. Já dá para ver onde a rotina está pesando mais.",
    "pain_detail": "Certo. Isso ajuda a entender o impacto no dia a dia.",
    "current_process": "Entendi. Já dá para ver como isso está organizado hoje.",
    "priority": "Certo. Isso mostra o que vale priorizar primeiro.",
    "urgency": "Entendi. Isso ajuda a calibrar o próximo passo.",
}

# Official/runtime variables the compiler must fill per template, from the
# resolved official facts handed to it (retrieval wiring is T012-031).
_OFFICIAL_VARIABLES_BY_TEMPLATE: dict[str, tuple[str, ...]] = {
    "product.price_direct": ("plan_price_summary",),
    "product.demo_direct": ("official_demo_link",),
    "product.whatsapp_direct": ("official_demo_link",),
    "diagnostic.deliver_plan_recommendation": ("recommended_plan_or_range",),
}


@dataclass(frozen=True)
class CompiledTurn:
    selected_action: str
    previous_state: str
    current_state: str
    next_state: str
    template_ids: tuple[str, ...]
    variables: dict[str, dict[str, Any]]
    ledger_updates: tuple[dict[str, Any], ...]
    state_patch: dict[str, Any]
    sales_inbox_projection: dict[str, Any]
    chunk_policy: str
    issues: tuple[str, ...] = field(default_factory=tuple)

    @property
    def ok(self) -> bool:
        return not self.issues


def _registry_template(template_id: str, fallback: str) -> str:
    return template_id if template_id in TEMPLATE_REGISTRY else fallback


def _composition_payloads(
    decision: ConductorActionDecision,
) -> dict[str, dict[str, Any]]:
    composable = composition_variable_names()
    payloads: dict[str, dict[str, Any]] = {}
    for variable in decision.composition_variables:
        if variable.name not in composable:
            continue
        payloads[variable.name] = {
            "kind": "short_text",
            "value": variable.value,
            "source": "user_message",
            "evidence": list(variable.evidence),
        }
    return payloads


def _normalize_variable(name: str, payload: dict[str, Any]) -> dict[str, Any]:
    from app.core.taliya_commercial.template_registry import VARIABLE_REGISTRY

    spec = VARIABLE_REGISTRY.get(name)
    if spec is None:
        return payload
    normalized = dict(payload)
    normalized["kind"] = spec.kind
    if spec.max_length is not None:
        normalized["max_length"] = spec.max_length
        value = normalized.get("value")
        if isinstance(value, str) and len(value) > spec.max_length:
            normalized["value"] = value[: spec.max_length - 3].rstrip() + "..."
    if normalized.get("source") not in spec.allowed_sources:
        preferred = (
            "diagnostic_ledger",
            "user_message",
            "runtime_state",
            "official_product_knowledge",
            "spec_006_product_contract",
            "model_decision",
        )
        normalized["source"] = next(
            (source for source in preferred if source in spec.allowed_sources),
            normalized.get("source"),
        )
    return normalized


def _official_variable(name: str, official_facts: Mapping[str, Any]) -> dict[str, Any] | None:
    fact = official_facts.get(name)
    if fact is None:
        return None
    if isinstance(fact, Mapping):
        return dict(fact)
    return {
        "kind": "short_text",
        "value": fact,
        "source": "official_product_knowledge",
        "evidence": [f"official_facts.{name}"],
    }


def _first_name_variable(situation: TurnSituation) -> dict[str, Any] | None:
    context = situation.profile_name_context or {}
    if context.get("usage") != "used_reliable_name" or not context.get("first_name"):
        return None
    return {
        "kind": "short_text",
        "value": str(context["first_name"]),
        "source": "runtime_state",
        "evidence": ["turn_situation.profile_name_context"],
    }


def _waitlist_missing_details(situation: TurnSituation) -> list[str]:
    return list(
        (dict(situation.state_snapshot).get("waitlist") or {}).get("missing_details")
        or ["contact_path"]
    )


def _waitlist_detail_template(detail: str) -> str:
    return {
        "studio_name": "waitlist.ask_missing_studio",
        "city_state": "waitlist.ask_missing_city",
        "contact_path": "waitlist.ask_missing_contact_path",
    }.get(detail, "waitlist.ask_missing_contact_path")


def _waitlist_missing_detail_template(situation: TurnSituation) -> str:
    return _waitlist_detail_template(_waitlist_missing_details(situation)[0])


_PRODUCT_TEMPLATE_BY_INTENT: tuple[tuple[str, str], ...] = (
    ("price_objection", "product.price_objection_value"),
    ("objection_price", "product.price_objection_value"),
    ("price", "product.price_direct"),
    ("preco", "product.price_direct"),
    ("plan", "product.price_direct"),
    ("demo", "product.demo_direct"),
    ("whatsapp", "product.whatsapp_direct"),
    ("how_it_works", "product.how_it_works_direct"),
    ("como_funciona", "product.how_it_works_direct"),
    ("routine", "product.overview_short"),
    ("rotina", "product.overview_short"),
    ("integration", "product.integration_scope_direct"),
    ("comparison", "product.comparison_current_tool"),
    ("comparacao", "product.comparison_current_tool"),
    ("security", "product.security_data_direct"),
    ("trust_security", "product.security_data_direct"),
    ("availability", "product.overview_short"),
    ("onboarding", "product.overview_short"),
    ("out_of_profile", "product.out_of_profile_redirect"),
)


def _product_templates_for(decision: ConductorActionDecision) -> list[str]:
    chosen: list[str] = []
    for fact_key, template_id in _PRODUCT_TEMPLATE_BY_FACT_KEY:
        if fact_key in decision.product_fact_keys_used:
            chosen.append(_registry_template(template_id, "product.overview_short"))
    if not chosen:
        # Second structured signal: the model's normalized intents (its own
        # interpretation, never raw lead text).
        intents = " ".join(decision.interpreted_intents).lower()
        for marker, template_id in _PRODUCT_TEMPLATE_BY_INTENT:
            if marker in intents:
                chosen.append(_registry_template(template_id, "product.overview_short"))
                break
    if not chosen:
        chosen.append("product.overview_short")
    deduped: list[str] = []
    for template_id in chosen:
        if template_id not in deduped:
            deduped.append(template_id)
    if "product.whatsapp_direct" in deduped:
        deduped = [
            template_id
            for template_id in deduped
            if template_id != "product.how_it_works_direct"
        ]
    if any(
        template_id
        in {
            "product.whatsapp_direct",
            "product.how_it_works_direct",
            "product.integration_scope_direct",
            "product.comparison_current_tool",
            "product.security_data_direct",
            "product.out_of_profile_redirect",
        }
        for template_id in deduped
    ):
        deduped = [
            template_id
            for template_id in deduped
            if template_id != "product.overview_short"
        ]
    return deduped


def _diagnostic_answer_feedback(captured: set[str]) -> dict[str, Any] | None:
    for key in DIAGNOSTIC_MANDATORY_KEYS:
        if key in captured:
            return {
                "kind": "short_text",
                "value": _DIAGNOSTIC_FEEDBACK_BY_CAPTURED_KEY[key],
                "source": "runtime_state",
                "evidence": [f"captured_slots.{key}"],
            }
    return None


def _structured_answer_action(
    decision: ConductorActionDecision,
    situation: TurnSituation,
) -> str:
    action = decision.selected_action
    if action not in {
        "answer_general_interest",
        "answer_source_opening",
        "clarify_ambiguous_opening",
        "clarify_product_question",
    }:
        return action

    allowed = set(situation.allowed_actions)
    fact_keys = set(decision.product_fact_keys_used)
    intents = " ".join(decision.interpreted_intents).lower()
    product_answer_allowed = "answer_direct_product_question" in allowed

    if decision.demo_intent == "requested" or "demo_link" in fact_keys or "demo" in intents:
        if "send_demo" in allowed:
            return "send_demo"
        if product_answer_allowed:
            return "answer_direct_product_question"

    if (
        {"prices", "plans"} & fact_keys
        or "price" in intents
        or "preco" in intents
        or "preço" in intents
    ) and product_answer_allowed:
        return "answer_direct_product_question"

    return action


def _merge_ledger_updates(
    decision: ConductorActionDecision,
) -> tuple[tuple[dict[str, Any], ...], set[str]]:
    updates: list[dict[str, Any]] = []
    captured_keys: set[str] = set()
    for slot in decision.captured_slots:
        if slot.key not in DIAGNOSTIC_MANDATORY_KEYS:
            continue
        if slot.status == "ambiguous":
            continue
        updates.append(
            {
                "question_key": slot.key,
                "status": slot.status,
                "answer_value": slot.value_text,
                "evidence": list(slot.evidence),
            }
        )
        captured_keys.add(slot.key)
    return tuple(updates), captured_keys


def _captured_waitlist_detail_payloads(
    decision: ConductorActionDecision,
) -> dict[str, dict[str, Any]]:
    payloads: dict[str, dict[str, Any]] = {}
    for slot in decision.captured_slots:
        if slot.key not in {"studio_name", "city_state", "contact_path"}:
            continue
        if slot.status == "ambiguous":
            continue
        payloads[slot.key] = {
            "kind": "short_text",
            "value": slot.value_text,
            "source": "user_message",
            "evidence": list(slot.evidence),
        }
    return payloads


def _staged_delivery(
    situation: TurnSituation,
    official_facts: Mapping[str, Any],
) -> tuple[list[str], list[str]]:
    """The contract-mandated staged final diagnostic, derived by code."""

    issues: list[str] = []
    templates = [
        "diagnostic.deliver_hold",
        "diagnostic.deliver_context",
        "diagnostic.deliver_crm_base",
        "diagnostic.deliver_operational_step",
    ]
    indicated_agents = official_facts.get("indicated_agents") or []
    if indicated_agents:
        templates.extend(["diagnostic.deliver_agent_recommendation"] * len(indicated_agents))
    else:
        issues.append("compile_missing_official_fact:indicated_agents")
    templates.append("diagnostic.deliver_plan_recommendation")
    demo_state = (dict(situation.state_snapshot).get("demo") or {}).get("status")
    if demo_state in {"offered", "link_sent", "viewed_or_asked", "reacted_positive"}:
        templates.append("diagnostic.deliver_demo_already_offered")
    else:
        templates.append("diagnostic.deliver_demo_not_offered")
    return templates, issues


def compile_action_decision(
    decision: ConductorActionDecision,
    situation: TurnSituation,
    *,
    official_facts: Mapping[str, Any] | None = None,
) -> CompiledTurn:
    """Compile the LLM's chosen action into the deterministic turn shape."""

    facts = dict(official_facts or {})
    action = _structured_answer_action(decision, situation)
    captured_waitlist_details = _captured_waitlist_detail_payloads(decision)
    waitlist_missing_details = _waitlist_missing_details(situation)
    if (
        action == "collect_waitlist_missing_detail"
        and waitlist_missing_details
        and not [key for key in waitlist_missing_details if key not in captured_waitlist_details]
    ):
        # The model supplied structured values for every pending detail. The
        # compiler closes the operational collection step instead of asking
        # again for data already captured.
        action = "join_waitlist"

    # Product-family specializations: when the menu offers the generic
    # answer_direct_product_question, the more specific answering actions are
    # accepted as equivalent form - same meaning, more precise. This keeps the
    # 011 menus verbatim while not punishing a better-typed choice.
    product_specializations = frozenset(
        {
            "answer_price",
            "answer_plan_fit_with_diagnostic_offer",
            "answer_how_it_works",
            "answer_whatsapp_scope",
            "answer_integration_scope_safely",
            "answer_comparison_current_tool",
            "answer_security_and_data",
            "answer_availability_and_onboarding",
            "answer_out_of_profile",
            "answer_price_objection",
            "send_demo",
            "clarify_product_question",
        }
    )
    # Clear contract intent can appear at ANY moment (waitlist policy); when
    # the model declares it structurally, the waitlist offer is accepted even
    # off-menu - the signal is the model's typed declaration, never raw text.
    waitlist_intent_accepted = (
        decision.selected_action in {"offer_waitlist", "offer_or_join_waitlist_if_eligible"}
        and decision.waitlist_intent == "contract_intent"
    )
    specialization_accepted = (
        action in product_specializations
        and "answer_direct_product_question" in situation.allowed_actions
    ) or waitlist_intent_accepted
    # Non-composable compositions are advisory: the compiler ignores or
    # overwrites them (official variables come from facts), so an extra
    # harmless variable must not block the turn.
    issues = [
        issue
        for issue in validate_action_decision(
            decision,
            allowed_actions=(
                (*situation.allowed_actions, action)
                if action != decision.selected_action
                else situation.allowed_actions
            ),
        )
        if not issue.startswith("conductor_composition_variable_not_composable")
        and not (issue == "conductor_action_not_in_allowed_menu" and specialization_accepted)
    ]
    previous_state = str(dict(situation.state_snapshot).get("canonical_state") or "new_lead")
    current_state, next_state = _STATE_BY_ACTION.get(action, (previous_state, previous_state))

    compositions = _composition_payloads(decision)
    for required in REQUIRED_COMPOSITIONS_BY_ACTION.get(action, ()):
        if required not in compositions:
            issues.append(f"compile_missing_composition:{required}")

    templates: list[str] = []
    variables: dict[str, dict[str, Any]] = {}
    state_patch: dict[str, Any] = {}
    chunk_policy = "whatsapp_max_3" if situation.channel == "whatsapp" else "default"
    ledger_updates: tuple[dict[str, Any], ...] = ()

    if action in {"handoff_requested", "pause_for_human"}:
        templates = ["handoff.acknowledge"]
        state_patch["handoff"] = {"status": "requested", "pause_ai": True}
    elif action in {
        "resume_only_with_explicit_resume_event",
        "suppress_ai_reply_while_human_active",
    }:
        templates = []
    elif action in {
        "clarify_ambiguous_opening",
        "clarify_ambiguous_diagnostic_answer",
        "clarify_ambiguous_followup",
        "clarify_product_question",
    }:
        templates = ["fallback.unmapped_adaptive"]
    elif action == "answer_general_interest":
        # Cold first contact renders the plain greeting; an ongoing
        # conversation renders the short overview (state-derived form).
        named_cold_greeting = (
            previous_state in {"new_lead", "greeting_only"}
            and _first_name_variable(situation) is not None
        )
        templates = [
            "opening.cold_greeting_named"
            if named_cold_greeting
            else "opening.cold_greeting"
            if previous_state in {"new_lead", "greeting_only"}
            else "opening.general_interest"
        ]
    elif action == "answer_source_opening":
        source = str(dict(situation.state_snapshot).get("source") or "instagram")
        templates = ["opening.site_cta" if source == "site" else "opening.instagram_source"]
    elif action in {"offer_diagnostic_from_pain", "offer_diagnostic_after_answer"}:
        templates = ["diagnostic.offer_soft"]
        if action == "offer_diagnostic_from_pain" and previous_state in {
            "new_lead",
            "greeting_only",
        }:
            templates = ["opening.contextual_ack", *templates]
    elif action in {"answer_direct_product_question", "answer_product_question_with_saved_context"}:
        templates = _product_templates_for(decision)
        if (
            "product.price_direct" in templates
            and action != "answer_product_question_with_saved_context"
        ):
            templates.append(
                "diagnostic.price_hook_with_context"
                if "plan_fit_context" in compositions
                else "diagnostic.price_hook"
            )
    elif action == "start_requested_diagnostic":
        pending = situation.pending_question_key or DIAGNOSTIC_MANDATORY_KEYS[0]
        templates = []
        snapshot = dict(situation.state_snapshot)
        should_render_cold_greeting = previous_state in {"new_lead", "greeting_only"} and not (
            situation.channel == "widget"
            and snapshot.get("client_has_prior_assistant_messages") is True
        )
        if should_render_cold_greeting:
            templates.append(
                "opening.cold_greeting_named"
                if _first_name_variable(situation) is not None
                else "opening.cold_greeting"
            )
        templates = [
            *templates,
            "diagnostic.start_named"
            if _first_name_variable(situation) is not None
            else "diagnostic.start",
            DIAGNOSTIC_ASK_TEMPLATE_BY_KEY[pending],
        ]
        state_patch["diagnostic"] = {"status": "in_progress"}
    elif action == "capture_pending_diagnostic_answer":
        ledger_updates, captured = _merge_ledger_updates(decision)
        pending = situation.pending_question_key
        existing_answered = {
            key
            for key, entry in (
                (dict(situation.state_snapshot).get("diagnostic") or {}).get("ledger") or {}
            ).items()
            if isinstance(entry, Mapping) and entry.get("status") in _COMPLETE_STATUSES
        }
        correction_only = bool(captured) and captured <= existing_answered
        if pending and pending not in captured and not correction_only:
            issues.append(f"compile_missing_captured_answer:{pending}")
        remaining = [key for key in situation.missing_diagnostic_keys if key not in captured]
        if remaining:
            templates = [DIAGNOSTIC_ASK_TEMPLATE_BY_KEY[remaining[0]]]
        else:
            issues.append("compile_capture_completed_use_complete_diagnostic")
    elif action == "answer_direct_question_then_continue_diagnostic":
        ledger_updates, _captured = _merge_ledger_updates(decision)
        templates = _product_templates_for(decision)
        if situation.pending_question_key:
            templates.append(DIAGNOSTIC_ASK_TEMPLATE_BY_KEY[situation.pending_question_key])
    elif action == "ask_next_diagnostic_question":
        pending = situation.pending_question_key
        if pending is None:
            issues.append("compile_no_pending_question")
        elif situation.mode == "diagnostic":
            issues.append("compile_repeated_pending_question_without_capture")
        else:
            templates = [DIAGNOSTIC_ASK_TEMPLATE_BY_KEY[pending]]
    elif action == "complete_diagnostic":
        ledger_updates, captured = _merge_ledger_updates(decision)
        still_missing = [key for key in situation.missing_diagnostic_keys if key not in captured]
        if still_missing:
            issues.append("compile_completion_with_missing_keys:" + ",".join(still_missing))
        staged, staged_issues = _staged_delivery(situation, facts)
        issues.extend(staged_issues)
        templates = staged
        chunk_policy = "staged_diagnostic"
        state_patch["diagnostic"] = {"status": "delivered"}
    elif action == "respect_diagnostic_refusal":
        templates = _product_templates_for(decision)
    elif action == "send_demo":
        templates = ["product.demo_direct"]
        state_patch["demo"] = {"status": "offered"}
    elif action == "ask_demo_reaction":
        templates = ["diagnostic.deliver_demo_already_offered"]
    elif action in {"answer_price_objection", "answer_price_objection_with_context"}:
        templates = [_registry_template("product.price_objection_value", "product.overview_short")]
    elif action == "answer_price":
        templates = [
            "product.price_direct",
            "diagnostic.price_hook_with_context"
            if "plan_fit_context" in compositions
            else "diagnostic.price_hook",
        ]
    elif action == "answer_plan_fit_with_diagnostic_offer":
        templates = [
            _registry_template("product.plan_fit_with_diagnostic", "product.overview_short")
        ]
    elif action == "answer_how_it_works":
        templates = [_registry_template("product.how_it_works_direct", "product.overview_short")]
    elif action == "answer_whatsapp_scope":
        templates = ["product.whatsapp_direct"]
    elif action == "answer_integration_scope_safely":
        templates = [
            _registry_template(
                "product.integration_scope_direct",
                "fallback.product_knowledge_missing",
            )
        ]
    elif action == "answer_comparison_current_tool":
        templates = ["product.comparison_current_tool"]
    elif action == "answer_security_and_data":
        templates = ["product.security_data_direct"]
    elif action == "answer_availability_and_onboarding":
        templates = ["product.overview_short"]
    elif action == "answer_out_of_profile":
        templates = ["product.out_of_profile_redirect"]
    elif action in {"offer_waitlist", "offer_or_join_waitlist_if_eligible"}:
        templates = ["waitlist.offer_after_contract_intent"]
        state_patch["waitlist"] = {"status": "offered"}
    elif action == "collect_waitlist_missing_detail":
        remaining_details = [
            key for key in waitlist_missing_details if key not in captured_waitlist_details
        ]
        templates = [
            _waitlist_detail_template(
                remaining_details[0] if remaining_details else waitlist_missing_details[0]
            )
        ]
        state_patch["waitlist"] = {
            "status": "pending_data",
            "missing_details": remaining_details,
            **{key: payload["value"] for key, payload in captured_waitlist_details.items()},
        }
    elif action == "join_waitlist":
        templates = ["waitlist.joined"]
        state_patch["waitlist"] = {
            "status": "joined",
            "missing_details": [],
            **{key: payload["value"] for key, payload in captured_waitlist_details.items()},
        }
    elif action == "decline_waitlist":
        templates = ["waitlist.status_preserved"]
        state_patch["waitlist"] = {"status": "declined"}
    elif action == "pause_waitlist_decision":
        templates = ["waitlist.pause_decision"]
    elif action == "answer_question_then_continue_waitlist":
        if "how_it_works" in decision.product_fact_keys_used:
            templates = [
                _registry_template("product.how_it_works_direct", "product.overview_short")
            ]
        elif "availability_and_onboarding" in decision.product_fact_keys_used:
            templates = ["waitlist.current_path_explained"]
        elif "answer_feedback" in compositions and (
            _registry_template(
                "waitlist.answer_question",
                "fallback.product_knowledge_missing",
            )
            == "waitlist.answer_question"
        ):
            templates = ["waitlist.answer_question"]
        elif decision.waitlist_intent == "contract_intent":
            templates = ["waitlist.current_path_explained"]
        else:
            templates = _product_templates_for(decision)
        templates.append(_waitlist_missing_detail_template(situation))
    else:  # pragma: no cover - every TurnAction is mapped; guard for drift
        issues.append(f"compile_unmapped_action:{action}")

    # Template-group boundary: the compiler only emits templates the situation
    # allows (form constraint; the action choice stays the model's).
    for template_id in templates:
        if waitlist_intent_accepted and template_id.startswith("waitlist."):
            continue
        if not any(template_id.startswith(prefix) for prefix in situation.eligible_template_groups):
            issues.append(f"compile_template_outside_mode_groups:{template_id}")

    # Attach model compositions, then compiler-owned official variables.
    for name, payload in compositions.items():
        variables[name] = _normalize_variable(name, payload)
    for name, payload in captured_waitlist_details.items():
        variables[name] = _normalize_variable(name, payload)
    for template_id in templates:
        for official_name in _OFFICIAL_VARIABLES_BY_TEMPLATE.get(template_id, ()):
            payload = _official_variable(official_name, facts)
            if payload is None:
                issues.append(f"compile_missing_official_fact:{official_name}")
            else:
                variables[official_name] = _normalize_variable(official_name, payload)
    if "product.overview_short" in templates and "product_fact_summary" in facts:
        variables["product_fact_summary"] = _normalize_variable(
            "product_fact_summary", _official_variable("product_fact_summary", facts) or {}
        )
    if action == "capture_pending_diagnostic_answer":
        feedback = _diagnostic_answer_feedback(
            {
                str(update.get("question_key"))
                for update in ledger_updates
                if update.get("question_key")
            }
        )
        if feedback is not None:
            variables["answer_feedback"] = _normalize_variable(
                "answer_feedback",
                feedback,
            )
    if "opening.cold_greeting_named" in templates or "diagnostic.start_named" in templates:
        first_name = _first_name_variable(situation)
        if first_name is None:
            issues.append("compile_missing_reliable_first_name")
        else:
            variables["first_name"] = _normalize_variable("first_name", first_name)

    # State-derived enum variables (renderer expands the approved copy).
    if "product.how_it_works_direct" in templates:
        diagnostic_status = (dict(situation.state_snapshot).get("diagnostic") or {}).get("status")
        if diagnostic_status == "in_progress":
            next_step_token = "continue_diagnostic"
        elif diagnostic_status in {"delivered", "complete", "completed"}:
            next_step_token = "no_cta"
        elif situation.completed_diagnostic_keys or previous_state == "pain_detected":
            next_step_token = "diagnostic_offer_with_pain"
        else:
            next_step_token = "diagnostic_offer_generic"
        variables["contextual_next_step"] = {
            "kind": "enum",
            "value": next_step_token,
            "source": "runtime_state",
            "evidence": ["turn_situation.mode"],
        }
    demo_templates = {
        "diagnostic.deliver_demo_not_offered": "not_offered",
        "diagnostic.deliver_demo_already_offered": "offered",
    }
    for template_id, token in demo_templates.items():
        if template_id in templates:
            variables["demo_status"] = {
                "kind": "enum",
                "value": token,
                "source": "runtime_state",
                "evidence": ["demo_state.status"],
            }
    if "diagnostic.deliver_agent_recommendation" in templates:
        for agent_payload in facts.get("indicated_agents") or []:
            if isinstance(agent_payload, Mapping):
                for agent_variable, agent_value in agent_payload.items():
                    variables[agent_variable] = _normalize_variable(
                        agent_variable,
                        {
                            "kind": "short_text",
                            "value": str(agent_value),
                            "source": "official_product_knowledge",
                            "evidence": ["product_knowledge.routine_areas"],
                        },
                    )

    # Only attach variables the chosen templates accept; surplus compositions
    # are dropped (the renderer rejects unknown variables).
    accepted: set[str] = set()
    for template_id in templates:
        template = TEMPLATE_REGISTRY.get(template_id)
        if template is not None:
            accepted.update(template.required_variables)
            accepted.update(template.optional_variables)
    variables = {name: payload for name, payload in variables.items() if name in accepted}
    for template_id in templates:
        template = TEMPLATE_REGISTRY.get(template_id)
        if template is None:
            continue
        for required_name in template.required_variables:
            if required_name not in variables:
                issues.append(f"compile_missing_template_variable:{template_id}:{required_name}")

    diagnostic_offer_templates = {
        "diagnostic.offer_soft",
        "diagnostic.price_hook",
        "diagnostic.price_hook_with_context",
        "product.plan_fit_with_diagnostic",
    }
    contextual_next_step = (variables.get("contextual_next_step") or {}).get("value")
    if current_state == "product_question" and (
        any(template_id in diagnostic_offer_templates for template_id in templates)
        or contextual_next_step in {"diagnostic_offer_with_pain", "diagnostic_offer_generic"}
    ):
        next_state = "diagnostic_offered"

    projection = {
        "commercial_stage": next_state,
        "last_action": action,
        "diagnostic_status": (
            "delivered"
            if action == "complete_diagnostic"
            else (dict(situation.state_snapshot).get("diagnostic") or {}).get("status")
        ),
        "waitlist_status": (state_patch.get("waitlist") or {}).get("status")
        or (dict(situation.state_snapshot).get("waitlist") or {}).get("status"),
        "handoff_status": (state_patch.get("handoff") or {}).get("status"),
    }

    return CompiledTurn(
        selected_action=action,
        previous_state=previous_state,
        current_state=current_state,
        next_state=next_state,
        template_ids=tuple(templates),
        variables=variables,
        ledger_updates=ledger_updates,
        state_patch=state_patch,
        sales_inbox_projection=projection,
        chunk_policy=chunk_policy,
        issues=tuple(issues),
    )
