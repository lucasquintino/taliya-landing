from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from app.core.taliya_commercial.schemas import Channel, StrictModel, TurnContext

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

TurnAction = Literal[
    "answer_general_interest",
    "answer_source_opening",
    "offer_diagnostic_from_pain",
    "answer_direct_product_question",
    "start_requested_diagnostic",
    "handoff_requested",
    "clarify_ambiguous_opening",
    "capture_pending_diagnostic_answer",
    "answer_direct_question_then_continue_diagnostic",
    "ask_next_diagnostic_question",
    "complete_diagnostic",
    "clarify_ambiguous_diagnostic_answer",
    "respect_diagnostic_refusal",
    "answer_product_question_with_saved_context",
    "send_demo",
    "answer_price_objection_with_context",
    "offer_or_join_waitlist_if_eligible",
    "ask_demo_reaction",
    "clarify_ambiguous_followup",
    "answer_price",
    "answer_plan_fit_with_diagnostic_offer",
    "answer_how_it_works",
    "answer_whatsapp_scope",
    "answer_integration_scope_safely",
    "answer_price_objection",
    "offer_diagnostic_after_answer",
    "clarify_product_question",
    "offer_waitlist",
    "collect_waitlist_missing_detail",
    "join_waitlist",
    "decline_waitlist",
    "answer_question_then_continue_waitlist",
    "pause_for_human",
    "resume_only_with_explicit_resume_event",
    "suppress_ai_reply_while_human_active",
]

DiagnosticQuestionKey = Literal[
    "active_students_or_size",
    "main_pain",
    "pain_detail",
    "current_process",
    "priority",
    "urgency",
]

_REQUIRED_DIAGNOSTIC_KEYS: tuple[DiagnosticQuestionKey, ...] = (
    "active_students_or_size",
    "main_pain",
    "pain_detail",
    "current_process",
    "priority",
    "urgency",
)
_COMPLETE_DIAGNOSTIC_STATUSES = {
    "answered",
    "inferred_from_prior_message",
    "not_applicable",
}
_HANDOFF_ACTIVE_STATUSES = {
    "active",
    "human_active",
    "human_handoff",
    "paused_by_human",
}
_WAITLIST_ACTIVE_STATUSES = {"offered", "pending_details", "joined"}

_ENTRY_ACTIONS: tuple[TurnAction, ...] = (
    "answer_general_interest",
    "answer_source_opening",
    "offer_diagnostic_from_pain",
    "answer_direct_product_question",
    "send_demo",
    "answer_plan_fit_with_diagnostic_offer",
    "answer_how_it_works",
    "answer_whatsapp_scope",
    "answer_integration_scope_safely",
    "answer_price_objection",
    "offer_diagnostic_after_answer",
    "clarify_product_question",
    "start_requested_diagnostic",
    "handoff_requested",
    "clarify_ambiguous_opening",
)
_DIAGNOSTIC_ACTIONS: tuple[TurnAction, ...] = (
    "capture_pending_diagnostic_answer",
    "answer_direct_question_then_continue_diagnostic",
    "ask_next_diagnostic_question",
    "complete_diagnostic",
    "clarify_ambiguous_diagnostic_answer",
    "respect_diagnostic_refusal",
    "handoff_requested",
)
_POST_DIAGNOSTIC_ACTIONS: tuple[TurnAction, ...] = (
    "answer_product_question_with_saved_context",
    "send_demo",
    "answer_price_objection_with_context",
    "offer_or_join_waitlist_if_eligible",
    "handoff_requested",
    "ask_demo_reaction",
    "clarify_ambiguous_followup",
)
_PRODUCT_ACTIONS: tuple[TurnAction, ...] = (
    "answer_price",
    "answer_plan_fit_with_diagnostic_offer",
    "answer_how_it_works",
    "answer_whatsapp_scope",
    "answer_integration_scope_safely",
    "send_demo",
    "answer_price_objection",
    "offer_diagnostic_after_answer",
    "clarify_product_question",
    "handoff_requested",
)
_WAITLIST_ACTIONS: tuple[TurnAction, ...] = (
    "offer_waitlist",
    "collect_waitlist_missing_detail",
    "join_waitlist",
    "decline_waitlist",
    "answer_question_then_continue_waitlist",
    "handoff_requested",
)
_HANDOFF_ACTIONS: tuple[TurnAction, ...] = (
    "pause_for_human",
    "resume_only_with_explicit_resume_event",
    "suppress_ai_reply_while_human_active",
)


class TurnSituation(StrictModel):
    schema_version: Literal["011.turn_situation.v1"] = "011.turn_situation.v1"
    turn_id: str
    conversation_id: str
    channel: Channel
    mode: TurnMode
    pending_question_key: DiagnosticQuestionKey | None = None
    completed_diagnostic_keys: list[DiagnosticQuestionKey] = Field(default_factory=list)
    missing_diagnostic_keys: list[DiagnosticQuestionKey] = Field(default_factory=list)
    allowed_actions: list[TurnAction]
    required_obligations: list[str] = Field(default_factory=list)
    eligible_template_groups: list[str] = Field(default_factory=list)
    official_fact_keys_available: list[str] = Field(default_factory=list)
    state_constraints: list[str] = Field(default_factory=list)
    forbidden_actions_now: list[TurnAction] = Field(default_factory=list)

    @model_validator(mode="after")
    def allowed_actions_are_not_empty(self) -> TurnSituation:
        if not self.allowed_actions:
            raise ValueError("turn situation requires at least one allowed action")
        return self


def build_turn_situation(context: TurnContext) -> TurnSituation:
    diagnostic_status = _diagnostic_status(context)
    completed_keys = _completed_diagnostic_keys(context)
    missing_keys = _missing_diagnostic_keys(completed_keys)
    pending_key = missing_keys[0] if diagnostic_status == "in_progress" else None
    mode = _turn_mode(
        context=context,
        diagnostic_status=diagnostic_status,
    )

    return TurnSituation(
        turn_id=context.turn_id,
        conversation_id=context.conversation_id,
        channel=context.channel,
        mode=mode,
        pending_question_key=pending_key,
        completed_diagnostic_keys=completed_keys,
        missing_diagnostic_keys=missing_keys,
        allowed_actions=list(_allowed_actions_for_mode(mode)),
        required_obligations=_required_obligations(
            mode=mode,
            pending_question_key=pending_key,
            missing_keys=missing_keys,
        ),
        eligible_template_groups=_eligible_template_groups(mode),
        official_fact_keys_available=_official_fact_keys_available(context),
        state_constraints=_state_constraints(
            mode=mode,
            diagnostic_status=diagnostic_status,
        ),
        forbidden_actions_now=_forbidden_actions_now(mode),
    )


def _turn_mode(
    *,
    context: TurnContext,
    diagnostic_status: str | None,
) -> TurnMode:
    handoff_status = str(context.handoff_state.get("status") or "none")
    if handoff_status in _HANDOFF_ACTIVE_STATUSES:
        return "handoff"

    waitlist_status = str(context.waitlist_state.get("status") or "none")
    if waitlist_status in _WAITLIST_ACTIVE_STATUSES:
        return "waitlist"

    if diagnostic_status == "completed":
        return "post_diagnostic"
    if diagnostic_status in {"offered", "in_progress", "insufficient_evidence"}:
        return "diagnostic"

    return "entry"


def _diagnostic_status(context: TurnContext) -> str | None:
    raw_status = context.sales_inbox_inputs.get("diagnostic_status")
    if raw_status:
        return str(raw_status)

    completed = set(_completed_diagnostic_keys(context))
    if all(question_key in completed for question_key in _REQUIRED_DIAGNOSTIC_KEYS):
        return "completed"
    if completed or context.diagnostic_ledger:
        return "in_progress"
    return None


def _completed_diagnostic_keys(context: TurnContext) -> list[DiagnosticQuestionKey]:
    by_key: dict[str, str] = {}
    for item in context.diagnostic_ledger:
        question_key = str(item.get("question_key") or "")
        status = str(item.get("status") or "")
        if question_key in _REQUIRED_DIAGNOSTIC_KEYS:
            by_key[question_key] = status
    return [
        question_key
        for question_key in _REQUIRED_DIAGNOSTIC_KEYS
        if by_key.get(question_key) in _COMPLETE_DIAGNOSTIC_STATUSES
    ]


def _missing_diagnostic_keys(
    completed_keys: list[DiagnosticQuestionKey],
) -> list[DiagnosticQuestionKey]:
    completed = set(completed_keys)
    return [
        question_key
        for question_key in _REQUIRED_DIAGNOSTIC_KEYS
        if question_key not in completed
    ]


def _allowed_actions_for_mode(mode: TurnMode) -> tuple[TurnAction, ...]:
    if mode == "diagnostic":
        return _DIAGNOSTIC_ACTIONS
    if mode == "post_diagnostic":
        return _POST_DIAGNOSTIC_ACTIONS
    if mode in {"product", "price", "demo"}:
        return _PRODUCT_ACTIONS
    if mode == "waitlist":
        return _WAITLIST_ACTIONS
    if mode == "handoff":
        return _HANDOFF_ACTIONS
    return _ENTRY_ACTIONS


def _required_obligations(
    *,
    mode: TurnMode,
    pending_question_key: DiagnosticQuestionKey | None,
    missing_keys: list[DiagnosticQuestionKey],
) -> list[str]:
    obligations: list[str] = [
        "llm_must_choose_one_allowed_action",
        "llm_must_interpret_latest_inbound",
    ]
    if mode == "diagnostic" and pending_question_key is not None:
        obligations.append(f"pending_diagnostic_question:{pending_question_key}")
        obligations.append("direct_question_must_be_answered_before_continuing")
        if len(missing_keys) == 1:
            obligations.append("complete_diagnostic_if_pending_answer_is_captured")
    if mode == "post_diagnostic":
        obligations.append("preserve_completed_diagnostic_context")
        obligations.append("answer_current_followup_before_new_steering")
    if mode == "handoff":
        obligations.append("human_active_blocks_ai_commercial_reply")
    return obligations


def _eligible_template_groups(mode: TurnMode) -> list[str]:
    if mode == "diagnostic":
        return ["diagnostic_question", "diagnostic_completion", "product_answer_then_diagnostic"]
    if mode == "post_diagnostic":
        return ["post_diagnostic_product", "post_diagnostic_demo", "post_diagnostic_waitlist"]
    if mode in {"product", "price", "demo"}:
        return ["product_answer", "diagnostic_offer_after_product", "demo"]
    if mode == "waitlist":
        return ["waitlist"]
    if mode == "handoff":
        return ["handoff"]
    return ["entry_opening", "product_answer", "diagnostic_offer"]


def _official_fact_keys_available(context: TurnContext) -> list[str]:
    return sorted(
        {
            ref.key
            for ref in context.product_knowledge
            if not ref.missing and ref.key.strip()
        }
    )


def _state_constraints(
    *,
    mode: TurnMode,
    diagnostic_status: str | None,
) -> list[str]:
    constraints = [
        "raw_text_keyword_matching_for_commercial_action_forbidden",
        "template_selection_from_raw_text_forbidden",
    ]
    if diagnostic_status == "completed":
        constraints.append("completed_diagnostic_must_not_be_reopened_without_llm_reason")
    if mode == "handoff":
        constraints.append("no_ai_delivery_while_human_active")
    return constraints


def _forbidden_actions_now(mode: TurnMode) -> list[TurnAction]:
    if mode == "handoff":
        return [
            action
            for action in (
                *_ENTRY_ACTIONS,
                *_DIAGNOSTIC_ACTIONS,
                *_POST_DIAGNOSTIC_ACTIONS,
                *_PRODUCT_ACTIONS,
                *_WAITLIST_ACTIONS,
            )
            if action != "handoff_requested"
        ]
    if mode == "diagnostic":
        return ["join_waitlist", "offer_waitlist"]
    if mode == "entry":
        return ["join_waitlist", "collect_waitlist_missing_detail"]
    return []
