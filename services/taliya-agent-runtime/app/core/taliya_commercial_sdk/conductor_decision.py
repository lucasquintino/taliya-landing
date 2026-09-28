"""T012-030A: strict ConductorActionDecision schema and per-mode action menus.

Action-first boundary per `specs/011-.../action-contract.md` and
`design-lock-v2-action-first.md` (D-012-012):

- the LLM returns a COMPACT action decision - one selected action from the
  menu the Turn Situation Builder allows, plus interpretation, captured slots,
  and the few composition variables the contracts assign to the model;
- the LLM never returns final template plans, official-source variable values,
  state transitions, or rendered text;
- the schema constrains FORM (strict Literals make invented keys/actions
  unrepresentable); validators judge CONTENT downstream. The action menu
  constrains form, never meaning: which action fits the lead's message is
  always the model's semantic decision.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.core.taliya_commercial.template_registry import VARIABLE_REGISTRY

SCHEMA_VERSION = "012.conductor_action_decision.v1"

TurnMode = Literal[
    "entry",
    "diagnostic",
    "post_diagnostic",
    "product",
    "price",
    "demo",
    "waitlist",
    "handoff",
    "safety",
    "delivery_deferred",
]

# Union of every action in the per-mode menus below. A model cannot emit an
# action outside this Literal (the invented-key lesson from the spike).
TurnAction = Literal[
    # entry
    "answer_general_interest",
    "answer_source_opening",
    "offer_diagnostic_from_pain",
    "answer_direct_product_question",
    "start_requested_diagnostic",
    "handoff_requested",
    "clarify_ambiguous_opening",
    # diagnostic
    "capture_pending_diagnostic_answer",
    "answer_direct_question_then_continue_diagnostic",
    "ask_next_diagnostic_question",
    "complete_diagnostic",
    "clarify_ambiguous_diagnostic_answer",
    "respect_diagnostic_refusal",
    # post_diagnostic
    "answer_product_question_with_saved_context",
    "send_demo",
    "answer_price_objection_with_context",
    "offer_or_join_waitlist_if_eligible",
    "ask_demo_reaction",
    "clarify_ambiguous_followup",
    # product / price / demo
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
    "offer_diagnostic_after_answer",
    "clarify_product_question",
    # waitlist
    "offer_waitlist",
    "collect_waitlist_missing_detail",
    "join_waitlist",
    "decline_waitlist",
    "pause_waitlist_decision",
    "answer_question_then_continue_waitlist",
    # handoff
    "pause_for_human",
    "resume_only_with_explicit_resume_event",
    "suppress_ai_reply_while_human_active",
]

_PRODUCT_FAMILY_MENU: tuple[str, ...] = (
    "answer_price",
    "answer_plan_fit_with_diagnostic_offer",
    "answer_how_it_works",
    "answer_whatsapp_scope",
    "answer_integration_scope_safely",
    "answer_comparison_current_tool",
    "answer_security_and_data",
    "answer_availability_and_onboarding",
    "answer_out_of_profile",
    "send_demo",
    "answer_price_objection",
    "offer_diagnostic_after_answer",
    "clarify_product_question",
    "handoff_requested",
)

# Mode action menus, verbatim from 011/action-contract.md. `safety` and
# `delivery_deferred` are operational modes: the runtime handles them
# deterministically (allowed determinism) and does not call the LLM, so their
# menus are empty by design.
ACTION_MENU_BY_MODE: dict[str, tuple[str, ...]] = {
    "entry": (
        "answer_general_interest",
        "answer_source_opening",
        "offer_diagnostic_from_pain",
        "answer_direct_product_question",
        "start_requested_diagnostic",
        "handoff_requested",
        "clarify_ambiguous_opening",
    ),
    "diagnostic": (
        "capture_pending_diagnostic_answer",
        "answer_direct_question_then_continue_diagnostic",
        "ask_next_diagnostic_question",
        "complete_diagnostic",
        "clarify_ambiguous_diagnostic_answer",
        "respect_diagnostic_refusal",
        "handoff_requested",
    ),
    "post_diagnostic": (
        "answer_product_question_with_saved_context",
        "send_demo",
        "answer_price_objection_with_context",
        "offer_or_join_waitlist_if_eligible",
        "handoff_requested",
        "ask_demo_reaction",
        "clarify_ambiguous_followup",
    ),
    "product": _PRODUCT_FAMILY_MENU,
    "price": _PRODUCT_FAMILY_MENU,
    "demo": _PRODUCT_FAMILY_MENU,
    "waitlist": (
        "offer_waitlist",
        "collect_waitlist_missing_detail",
        "join_waitlist",
        "decline_waitlist",
        "pause_waitlist_decision",
        "answer_question_then_continue_waitlist",
        "handoff_requested",
    ),
    "handoff": (
        "pause_for_human",
        "resume_only_with_explicit_resume_event",
        "suppress_ai_reply_while_human_active",
    ),
    "safety": (),
    "delivery_deferred": (),
}

SlotKey = Literal[
    # diagnostic mandatory keys
    "active_students_or_size",
    "main_pain",
    "pain_detail",
    "current_process",
    "priority",
    "urgency",
    # waitlist detail keys
    "studio_name",
    "city_state",
    "contact_path",
    # name policy
    "person_name",
]

SlotStatus = Literal[
    "answered",
    "inferred_from_prior_message",
    "not_applicable",
    "ambiguous",
]

NumericKind = Literal[
    "plan_price",
    "student_count",
    "phone",
    "date_time",
    "unknown_number",
]

DiagnosticIntent = Literal[
    "none",
    "offer",
    "start",
    "capture_answer",
    "ask_next",
    "complete",
    "refusal",
    "insufficient_evidence",
]
DemoIntent = Literal["none", "requested", "curiosity", "reaction_pending", "reaction_positive"]
WaitlistIntent = Literal[
    "none", "curiosity", "contract_intent", "accepts", "declines", "provides_detail"
]
HandoffIntent = Literal["none", "requested"]
Confidence = Literal["low", "medium", "high"]

ProductFactKey = Literal[
    "prices",
    "plans",
    "demo_link",
    "whatsapp_scope",
    "how_it_works",
    "routine_areas",
    "integration_scope",
    "security_and_data",
    "availability_and_onboarding",
    "out_of_profile",
    "comparison_spreadsheet",
    "product_overview",
    "links",
]


class ConductorStrictModel(BaseModel):
    """Strict base: invented fields are unrepresentable; content judgment is
    downstream (validators), so no raising cross-field validators here."""

    model_config = ConfigDict(extra="forbid")


class CapturedSlot(ConductorStrictModel):
    key: SlotKey
    value_text: str
    status: SlotStatus = "answered"
    evidence: list[str] = Field(default_factory=list)


class NumericInterpretation(ConductorStrictModel):
    kind: NumericKind
    raw_text: str
    value_text: str
    evidence: list[str] = Field(default_factory=list)


class AnswerObligation(ConductorStrictModel):
    obligation: str
    evidence: list[str] = Field(default_factory=list)


class CompositionVariable(ConductorStrictModel):
    """A model-composed human variable (e.g. answer_feedback,
    pain_context_human). Only context variables - never official-source ones;
    the compiler fills those. Membership is validated downstream against the
    registry-derived composition set."""

    name: str
    value: str
    evidence: list[str] = Field(
        default_factory=list,
        description=(
            "REQUIRED downstream: where this value came from (ledger key, "
            "lead-message excerpt). Compositions without evidence fail "
            "validation - they are never silently rendered (T011-105 lesson)."
        ),
    )


class ConductorActionDecision(ConductorStrictModel):
    """The compact turn decision. Identity fields are overwritten by the
    runtime with authoritative values; the model cannot fabricate them."""

    schema_version: Literal["012.conductor_action_decision.v1"] = SCHEMA_VERSION
    decision_id: str = ""
    turn_id: str = ""
    selected_action: TurnAction = Field(
        description=(
            "Exactly one action, chosen ONLY from the allowed_actions menu "
            "provided in the turn situation. Which action fits the lead's "
            "message is your semantic decision."
        )
    )
    interpreted_intents: list[str] = Field(default_factory=list)
    direct_question: str | None = Field(
        default=None,
        description=(
            "A direct question asked in the CURRENT inbound message only. "
            "Questions already answered in earlier turns are not direct "
            "questions of this turn; leave null when the current message asks "
            "nothing."
        ),
    )
    direct_answer_obligations: list[AnswerObligation] = Field(default_factory=list)
    captured_slots: list[CapturedSlot] = Field(default_factory=list)
    product_fact_keys_used: list[ProductFactKey] = Field(
        default_factory=list,
        description=(
            "The official fact keys your answer needs, REQUIRED whenever you "
            "answer a product matter: prices, plans, demo_link, "
            "whatsapp_scope, how_it_works, routine_areas, integration_scope, "
            "security_and_data, availability_and_onboarding, out_of_profile. "
            "The runtime injects the official values from these keys; without "
            "them a price/demo/scope answer cannot be assembled."
        ),
    )
    numeric_interpretations: list[NumericInterpretation] = Field(default_factory=list)
    diagnostic_intent: DiagnosticIntent = "none"
    demo_intent: DemoIntent = "none"
    waitlist_intent: WaitlistIntent = "none"
    handoff_intent: HandoffIntent = "none"
    composition_variables: list[CompositionVariable] = Field(default_factory=list)
    reply_goal: str = ""
    confidence: Confidence = "medium"
    evidence: list[str] = Field(default_factory=list)
    needs_clarification: bool = False
    repair_hints: list[str] = Field(default_factory=list)


_COMPOSITION_SOURCES = frozenset({"user_message", "diagnostic_ledger", "model_decision"})
_OFFICIAL_ONLY_SOURCES = frozenset(
    {"official_product_knowledge", "spec_006_product_contract", "runtime_state"}
)


def composition_variable_names() -> frozenset[str]:
    """Variables the model may compose.

    Composable = the registry allows a lead-context source (user_message,
    diagnostic_ledger, or model_decision): the model writes the prose,
    grounded in what the lead said or the ledger holds - the compiler must
    never invent customer-facing semantic prose. Variables whose allowed
    sources are exclusively official/runtime (e.g. recommended_plan_or_range,
    plan_price_summary, official_demo_link) are compiler-owned: the model
    composing them could smuggle an ungrounded product claim.
    """

    return frozenset(
        name
        for name, spec in VARIABLE_REGISTRY.items()
        if _COMPOSITION_SOURCES & spec.allowed_sources
    )


def validate_action_decision(
    decision: ConductorActionDecision,
    *,
    allowed_actions: tuple[str, ...] | list[str],
) -> list[str]:
    """Deterministic form checks for a decision against its turn situation.

    Returns issue codes; empty list means the decision is structurally
    acceptable for compilation. Content quality stays with validators/judge.
    """

    issues: list[str] = []
    if decision.selected_action not in allowed_actions:
        issues.append("conductor_action_not_in_allowed_menu")
    composable = composition_variable_names()
    for variable in decision.composition_variables:
        if variable.name not in composable:
            issues.append(f"conductor_composition_variable_not_composable:{variable.name}")
        elif not any(item.strip() for item in variable.evidence):
            issues.append(f"conductor_composition_variable_missing_evidence:{variable.name}")
    if decision.needs_clarification and decision.selected_action not in {
        "clarify_ambiguous_opening",
        "clarify_ambiguous_diagnostic_answer",
        "clarify_ambiguous_followup",
        "clarify_product_question",
    }:
        issues.append("conductor_clarification_flag_without_clarify_action")
    return issues
