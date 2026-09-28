from __future__ import annotations

from enum import StrEnum


class ConversationState(StrEnum):
    NEW_LEAD = "new_lead"
    GREETING_ONLY = "greeting_only"
    GENERAL_INTEREST = "general_interest"
    SOURCE_INSTAGRAM = "source_instagram"
    PAIN_DETECTED = "pain_detected"
    PRODUCT_QUESTION = "product_question"
    PRICE_QUESTION = "price_question"
    PLAN_QUESTION = "plan_question"
    DEMO_QUESTION = "demo_question"
    DIAGNOSTIC_REQUESTED = "diagnostic_requested"
    DIAGNOSTIC_OFFERED = "diagnostic_offered"
    DIAGNOSTIC_IN_PROGRESS = "diagnostic_in_progress"
    DIAGNOSTIC_WAITING_ANSWER = "diagnostic_waiting_answer"
    DIAGNOSTIC_READY = "diagnostic_ready"
    DIAGNOSTIC_DELIVERED = "diagnostic_delivered"
    POST_DIAGNOSTIC_QUESTIONS = "post_diagnostic_questions"
    BUYING_INTENT_DETECTED = "buying_intent_detected"
    WAITLIST_ELIGIBLE = "waitlist_eligible"
    WAITLIST_OFFERED = "waitlist_offered"
    WAITLIST_PENDING_DATA = "waitlist_pending_data"
    WAITLIST_JOINED = "waitlist_joined"
    HUMAN_REQUESTED = "human_requested"
    HUMAN_HANDOFF = "human_handoff"
    PAUSED_BY_HUMAN = "paused_by_human"
    OUT_OF_SCOPE = "out_of_scope"
    SAFETY_BLOCKED = "safety_blocked"
    UNKNOWN_OR_LOW_CONFIDENCE = "unknown_or_low_confidence"


ALL_STATES: tuple[str, ...] = tuple(state.value for state in ConversationState)

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    ConversationState.NEW_LEAD: {
        ConversationState.GREETING_ONLY,
        ConversationState.GENERAL_INTEREST,
        ConversationState.SOURCE_INSTAGRAM,
        ConversationState.DIAGNOSTIC_REQUESTED,
        ConversationState.PAIN_DETECTED,
        ConversationState.PRODUCT_QUESTION,
        ConversationState.PRICE_QUESTION,
        ConversationState.PLAN_QUESTION,
        ConversationState.DEMO_QUESTION,
        ConversationState.HUMAN_REQUESTED,
        ConversationState.OUT_OF_SCOPE,
        ConversationState.SAFETY_BLOCKED,
    },
    ConversationState.GREETING_ONLY: {
        ConversationState.GENERAL_INTEREST,
        ConversationState.PRODUCT_QUESTION,
        ConversationState.PRICE_QUESTION,
        ConversationState.PLAN_QUESTION,
        ConversationState.PAIN_DETECTED,
        ConversationState.DIAGNOSTIC_REQUESTED,
        ConversationState.HUMAN_REQUESTED,
        ConversationState.OUT_OF_SCOPE,
    },
    ConversationState.GENERAL_INTEREST: {
        ConversationState.DIAGNOSTIC_OFFERED,
        ConversationState.PRODUCT_QUESTION,
        ConversationState.PAIN_DETECTED,
        ConversationState.DIAGNOSTIC_REQUESTED,
        ConversationState.HUMAN_REQUESTED,
    },
    ConversationState.SOURCE_INSTAGRAM: {
        ConversationState.GENERAL_INTEREST,
        ConversationState.DIAGNOSTIC_OFFERED,
        ConversationState.PAIN_DETECTED,
        ConversationState.PRODUCT_QUESTION,
        ConversationState.DIAGNOSTIC_REQUESTED,
    },
    ConversationState.PAIN_DETECTED: {
        ConversationState.DIAGNOSTIC_OFFERED,
        ConversationState.DIAGNOSTIC_IN_PROGRESS,
        ConversationState.PRODUCT_QUESTION,
        ConversationState.HUMAN_REQUESTED,
    },
    ConversationState.PRODUCT_QUESTION: {
        ConversationState.DIAGNOSTIC_OFFERED,
        ConversationState.DIAGNOSTIC_IN_PROGRESS,
        ConversationState.BUYING_INTENT_DETECTED,
        ConversationState.HUMAN_REQUESTED,
        ConversationState.OUT_OF_SCOPE,
    },
    ConversationState.PRICE_QUESTION: {
        ConversationState.DIAGNOSTIC_OFFERED,
        ConversationState.PLAN_QUESTION,
        ConversationState.BUYING_INTENT_DETECTED,
        ConversationState.HUMAN_REQUESTED,
    },
    ConversationState.PLAN_QUESTION: {
        ConversationState.DIAGNOSTIC_OFFERED,
        ConversationState.DIAGNOSTIC_IN_PROGRESS,
        ConversationState.BUYING_INTENT_DETECTED,
    },
    ConversationState.DEMO_QUESTION: {
        ConversationState.DIAGNOSTIC_OFFERED,
        ConversationState.BUYING_INTENT_DETECTED,
        ConversationState.HUMAN_REQUESTED,
    },
    ConversationState.DIAGNOSTIC_REQUESTED: {
        ConversationState.DIAGNOSTIC_IN_PROGRESS,
        ConversationState.DIAGNOSTIC_WAITING_ANSWER,
        ConversationState.HUMAN_REQUESTED,
    },
    ConversationState.DIAGNOSTIC_OFFERED: {
        ConversationState.DIAGNOSTIC_IN_PROGRESS,
        ConversationState.PRODUCT_QUESTION,
        ConversationState.GENERAL_INTEREST,
        ConversationState.HUMAN_REQUESTED,
    },
    ConversationState.DIAGNOSTIC_IN_PROGRESS: {
        ConversationState.DIAGNOSTIC_WAITING_ANSWER,
        ConversationState.DIAGNOSTIC_READY,
        ConversationState.PRODUCT_QUESTION,
        ConversationState.HUMAN_REQUESTED,
    },
    ConversationState.DIAGNOSTIC_WAITING_ANSWER: {
        ConversationState.DIAGNOSTIC_IN_PROGRESS,
        ConversationState.DIAGNOSTIC_READY,
        ConversationState.PRODUCT_QUESTION,
        ConversationState.HUMAN_REQUESTED,
    },
    ConversationState.DIAGNOSTIC_READY: {ConversationState.DIAGNOSTIC_DELIVERED, ConversationState.HUMAN_REQUESTED},
    ConversationState.DIAGNOSTIC_DELIVERED: {
        ConversationState.POST_DIAGNOSTIC_QUESTIONS,
        ConversationState.BUYING_INTENT_DETECTED,
        ConversationState.WAITLIST_ELIGIBLE,
        ConversationState.PRODUCT_QUESTION,
        ConversationState.HUMAN_REQUESTED,
    },
    ConversationState.POST_DIAGNOSTIC_QUESTIONS: {
        ConversationState.BUYING_INTENT_DETECTED,
        ConversationState.WAITLIST_ELIGIBLE,
        ConversationState.PRODUCT_QUESTION,
        ConversationState.HUMAN_REQUESTED,
    },
    ConversationState.BUYING_INTENT_DETECTED: {
        ConversationState.WAITLIST_ELIGIBLE,
        ConversationState.WAITLIST_OFFERED,
        ConversationState.HUMAN_REQUESTED,
    },
    ConversationState.WAITLIST_ELIGIBLE: {
        ConversationState.WAITLIST_OFFERED,
        ConversationState.PRODUCT_QUESTION,
        ConversationState.HUMAN_REQUESTED,
    },
    ConversationState.WAITLIST_OFFERED: {
        ConversationState.WAITLIST_PENDING_DATA,
        ConversationState.WAITLIST_JOINED,
        ConversationState.POST_DIAGNOSTIC_QUESTIONS,
        ConversationState.HUMAN_REQUESTED,
    },
    ConversationState.WAITLIST_PENDING_DATA: {
        ConversationState.WAITLIST_JOINED,
        ConversationState.POST_DIAGNOSTIC_QUESTIONS,
        ConversationState.HUMAN_REQUESTED,
    },
    ConversationState.WAITLIST_JOINED: {
        ConversationState.POST_DIAGNOSTIC_QUESTIONS,
        ConversationState.PRODUCT_QUESTION,
        ConversationState.HUMAN_REQUESTED,
    },
    ConversationState.HUMAN_REQUESTED: {ConversationState.HUMAN_HANDOFF},
    ConversationState.HUMAN_HANDOFF: {ConversationState.PAUSED_BY_HUMAN},
    ConversationState.PAUSED_BY_HUMAN: {
        ConversationState.GENERAL_INTEREST,
        ConversationState.PRODUCT_QUESTION,
        ConversationState.DIAGNOSTIC_IN_PROGRESS,
        ConversationState.WAITLIST_JOINED,
    },
    ConversationState.OUT_OF_SCOPE: {
        ConversationState.GENERAL_INTEREST,
        ConversationState.DIAGNOSTIC_OFFERED,
        ConversationState.HUMAN_REQUESTED,
    },
    ConversationState.SAFETY_BLOCKED: {
        ConversationState.GENERAL_INTEREST,
        ConversationState.HUMAN_REQUESTED,
        ConversationState.PAUSED_BY_HUMAN,
    },
    ConversationState.UNKNOWN_OR_LOW_CONFIDENCE: {
        ConversationState.GENERAL_INTEREST,
        ConversationState.PRODUCT_QUESTION,
        ConversationState.DIAGNOSTIC_OFFERED,
        ConversationState.HUMAN_REQUESTED,
    },
}

HIGH_IMPACT_STATES = {
    ConversationState.DIAGNOSTIC_READY,
    ConversationState.DIAGNOSTIC_DELIVERED,
    ConversationState.WAITLIST_OFFERED,
    ConversationState.WAITLIST_JOINED,
    ConversationState.HUMAN_HANDOFF,
    ConversationState.PAUSED_BY_HUMAN,
    ConversationState.SAFETY_BLOCKED,
}


def normalize_state(value: str | ConversationState | None) -> ConversationState:
    if isinstance(value, ConversationState):
        return value
    if not value:
        return ConversationState.NEW_LEAD
    try:
        return ConversationState(value)
    except ValueError:
        return ConversationState.UNKNOWN_OR_LOW_CONFIDENCE


def allowed_next_states(state: str | ConversationState | None) -> set[str]:
    normalized = normalize_state(state)
    return {item.value for item in ALLOWED_TRANSITIONS.get(normalized, set())}


def is_transition_allowed(previous: str | ConversationState | None, next_state: str | ConversationState | None) -> bool:
    previous_state = normalize_state(previous)
    candidate = normalize_state(next_state)
    return candidate in ALLOWED_TRANSITIONS.get(previous_state, set()) or previous_state == candidate


def is_high_impact_transition(next_state: str | ConversationState | None) -> bool:
    return normalize_state(next_state) in HIGH_IMPACT_STATES


def state_for_route(route: str, *, opening_type: str = "none", diagnostic_action: str = "none", waitlist_status: str | None = None) -> ConversationState:
    if opening_type == "cold_greeting_only":
        return ConversationState.GREETING_ONLY
    if opening_type == "social_source_opening":
        return ConversationState.SOURCE_INSTAGRAM
    if route == "product":
        return ConversationState.PRODUCT_QUESTION
    if route == "diagnostic":
        if diagnostic_action == "offer":
            return ConversationState.DIAGNOSTIC_OFFERED
        if diagnostic_action == "complete":
            return ConversationState.DIAGNOSTIC_DELIVERED
        return ConversationState.DIAGNOSTIC_IN_PROGRESS
    if route == "waitlist":
        if waitlist_status == "joined":
            return ConversationState.WAITLIST_JOINED
        if waitlist_status == "pending_details":
            return ConversationState.WAITLIST_PENDING_DATA
        return ConversationState.WAITLIST_OFFERED
    if route == "handoff":
        return ConversationState.HUMAN_HANDOFF
    if route == "safe_fallback":
        return ConversationState.SAFETY_BLOCKED
    return ConversationState.GENERAL_INTEREST


def next_state_after_response(current_state: str | ConversationState, *, diagnostic_action: str = "none", waitlist_status: str | None = None) -> ConversationState:
    state = normalize_state(current_state)
    if state == ConversationState.DIAGNOSTIC_OFFERED:
        return ConversationState.DIAGNOSTIC_IN_PROGRESS
    if state == ConversationState.DIAGNOSTIC_IN_PROGRESS and diagnostic_action == "complete":
        return ConversationState.DIAGNOSTIC_DELIVERED
    if state == ConversationState.WAITLIST_OFFERED and waitlist_status == "pending_details":
        return ConversationState.WAITLIST_PENDING_DATA
    if state == ConversationState.WAITLIST_PENDING_DATA and waitlist_status == "joined":
        return ConversationState.WAITLIST_JOINED
    if state == ConversationState.HUMAN_HANDOFF:
        return ConversationState.PAUSED_BY_HUMAN
    return state
