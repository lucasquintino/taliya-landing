"""T012-030B: deterministic Turn Situation Builder.

"The core prepares the board. The LLM plays the turn."
(`011/action-contract.md`)

The builder computes the turn situation ONLY from persisted state and
operational metadata. It never receives or interprets the lead's message -
its function signature has no text parameter, and a test enforces that.
Commercial meaning stays with the LLM; this module owns process state:
which mode the conversation is in, which diagnostic key is pending, which
actions and template groups the moment allows.

Absorbs the spike-proven pieces: the deterministic state preamble (compact
memory) and the diagnostic-sequence knowledge (mandatory key order).
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from app.core.taliya_commercial_sdk.conductor_decision import (
    ACTION_MENU_BY_MODE,
)
from app.core.taliya_commercial_sdk.validators_adapter import (
    DIAGNOSTIC_MANDATORY_KEYS,
)
from app.domains.taliya_commercial.behavior_policy import assess_profile_name

_COMPLETE_STATUSES = {"answered", "inferred_from_prior_message", "not_applicable"}

# Persisted canonical state (conversation-state-contract.md) -> turn mode.
# Operational flags (safety, human, delivery) take precedence over this map.
_MODE_BY_CANONICAL_STATE: dict[str, str] = {
    "new_lead": "entry",
    "greeting_only": "entry",
    "general_interest": "entry",
    "source_instagram": "entry",
    "pain_detected": "entry",
    "unknown_or_low_confidence": "entry",
    "out_of_scope": "entry",
    "product_question": "product",
    "price_question": "price",
    "plan_question": "product",
    "demo_question": "demo",
    "demo_offered": "demo",
    "demo_reaction_pending": "demo",
    "demo_reacted_positive": "post_diagnostic",
    "diagnostic_requested": "diagnostic",
    "diagnostic_offered": "entry",
    "diagnostic_in_progress": "diagnostic",
    "diagnostic_waiting_answer": "diagnostic",
    "diagnostic_ready": "diagnostic",
    "diagnostic_delivered": "post_diagnostic",
    "post_diagnostic_questions": "post_diagnostic",
    "buying_intent_detected": "waitlist",
    "waitlist_eligible": "waitlist",
    "waitlist_offered": "waitlist",
    "waitlist_pending_data": "waitlist",
    "waitlist_joined": "post_diagnostic",
    "human_requested": "handoff",
    "human_handoff": "handoff",
    "paused_by_human": "handoff",
    "safety_blocked": "safety",
}

# Mode -> template families the renderer may use this turn (form, not meaning).
# "handoff." is eligible everywhere: a lead can ask for a human in any mode.
_TEMPLATE_GROUPS_BY_MODE: dict[str, tuple[str, ...]] = {
    # entry includes "product.": the entry menu's answer_direct_product_question
    # must be expressible (direct questions at opening are answered, not dodged)
    # and "diagnostic.": start_requested_diagnostic compiles start + first ask.
    "entry": ("opening.", "diagnostic.", "product.", "handoff.", "fallback."),
    # waitlist. included: clear contract intent can appear mid-diagnostic.
    "diagnostic": ("diagnostic.", "product.", "waitlist.", "handoff.", "fallback."),
    "post_diagnostic": (
        "product.",
        "diagnostic.price_hook",
        "diagnostic.deliver_demo_already_offered",
        "waitlist.",
        "handoff.",
        "fallback.",
    ),
    "product": (
        "product.",
        "diagnostic.offer_soft",
        "diagnostic.price_hook",
        "opening.general_interest",
        "handoff.",
        "fallback.",
    ),
    "price": (
        "product.",
        "diagnostic.offer_soft",
        "diagnostic.price_hook",
        "handoff.",
        "fallback.",
    ),
    "demo": ("product.", "diagnostic.offer_soft", "handoff.", "fallback."),
    "waitlist": ("waitlist.", "product.", "handoff.", "fallback."),
    "handoff": ("handoff.",),
    "safety": ("safety.",),
    "delivery_deferred": (),
}


@dataclass(frozen=True)
class TurnSituation:
    """The deterministic board for one turn."""

    mode: str
    channel: str
    allowed_actions: tuple[str, ...]
    forbidden_actions_now: tuple[str, ...]
    eligible_template_groups: tuple[str, ...]
    pending_question_key: str | None = None
    completed_diagnostic_keys: tuple[str, ...] = ()
    missing_diagnostic_keys: tuple[str, ...] = ()
    required_obligations: tuple[str, ...] = ()
    official_fact_keys_available: tuple[str, ...] = ()
    profile_name_context: Mapping[str, Any] | None = None
    post_diagnostic_context: Mapping[str, Any] | None = None
    state_constraints: tuple[str, ...] = ()
    llm_turn_allowed: bool = True
    state_snapshot: Mapping[str, Any] = field(default_factory=dict)

    def to_preamble(self) -> str:
        """Deterministic compact-memory preamble for the model input.

        Spike-proven: loading the board into the turn removes state-rediscovery
        tool rounds and stale-context confusion.
        """

        lines = ["[runtime context] Turn situation (authoritative, code-derived):"]
        lines.append(f"mode: {self.mode}")
        if self.pending_question_key:
            lines.append(
                f"pending diagnostic question: {self.pending_question_key} "
                f"(completed: {', '.join(self.completed_diagnostic_keys) or 'none'})"
            )
        lines.append("allowed actions: " + ", ".join(self.allowed_actions))
        if self.forbidden_actions_now:
            lines.append(
                "forbidden right now: " + ", ".join(self.forbidden_actions_now)
            )
        for constraint in self.state_constraints:
            lines.append(f"constraint: {constraint}")
        snapshot = dict(self.state_snapshot)
        summary = snapshot.get("summary")
        if summary:
            lines.append(f"summary: {summary}")
        answered = snapshot.get("answered_obligations")
        if answered:
            lines.append(
                "questions already answered in earlier turns (not new "
                "obligations): " + "; ".join(answered)
            )
        operational = {
            key: snapshot[key]
            for key in ("diagnostic", "demo", "waitlist", "human_status")
            if snapshot.get(key) is not None
        }
        if operational:
            lines.append("state: " + json.dumps(operational, ensure_ascii=False))
        if self.profile_name_context:
            lines.append(
                "profile_name_policy: "
                + json.dumps(self.profile_name_context, ensure_ascii=False)
            )
        if self.post_diagnostic_context:
            lines.append(
                "post_diagnostic_context: "
                + json.dumps(self.post_diagnostic_context, ensure_ascii=False)
            )
        if not snapshot:
            lines.append(
                "no stored conversation state: first contact; state read tools "
                "would return nothing."
            )
        return "\n".join(lines)


def _diagnostic_progress(
    state_snapshot: Mapping[str, Any],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    ledger = (dict(state_snapshot).get("diagnostic") or {}).get("ledger") or {}
    completed = tuple(
        key
        for key in DIAGNOSTIC_MANDATORY_KEYS
        if isinstance(ledger.get(key), dict)
        and ledger[key].get("status") in _COMPLETE_STATUSES
    )
    missing = tuple(
        key for key in DIAGNOSTIC_MANDATORY_KEYS if key not in completed
    )
    return completed, missing


def _derive_mode(state_snapshot: Mapping[str, Any]) -> str:
    snapshot = dict(state_snapshot)
    # Operational precedence: these are allowed-determinism boundaries.
    if snapshot.get("safety_blocked"):
        return "safety"
    if snapshot.get("human_status") in {"requested", "active", "paused"}:
        return "handoff"
    delivery = snapshot.get("delivery") or {}
    if isinstance(delivery, Mapping) and (
        delivery.get("status") == "delivering" or delivery.get("chunks_remaining")
    ):
        return "delivery_deferred"

    waitlist = snapshot.get("waitlist") or {}
    if isinstance(waitlist, Mapping) and waitlist.get("status") in {
        "offered",
        "pending_data",
    }:
        return "waitlist"

    canonical = snapshot.get("canonical_state")
    if canonical in {"waitlist_eligible", "waitlist_offered", "waitlist_pending_data"}:
        return "waitlist"

    diagnostic = snapshot.get("diagnostic") or {}
    if isinstance(diagnostic, Mapping):
        status = diagnostic.get("status")
        if status == "in_progress":
            return "diagnostic"
        if status in {"complete", "completed", "delivered"}:
            return "post_diagnostic"

    if isinstance(canonical, str) and canonical in _MODE_BY_CANONICAL_STATE:
        return _MODE_BY_CANONICAL_STATE[canonical]

    # No canonical state persisted: fall back to operational substates.
    return "entry"


def _profile_name_context(state_snapshot: Mapping[str, Any]) -> dict[str, Any] | None:
    snapshot = dict(state_snapshot)
    raw_name = snapshot.get("profile_name")
    if raw_name is None and isinstance(snapshot.get("channel_metadata"), Mapping):
        raw_name = dict(snapshot["channel_metadata"]).get("profile_name")
    assessment = assess_profile_name(str(raw_name or ""))
    if assessment.status == "not_available":
        return {"usage": "not_available"}
    if assessment.status == "unreliable":
        return {
            "usage": "ignored_unreliable_name",
            "reason": assessment.reason,
        }
    return {
        "usage": "used_reliable_name",
        "first_name": assessment.first_name,
    }


def _compact_post_diagnostic_context(
    state_snapshot: Mapping[str, Any],
    *,
    mode: str,
) -> dict[str, Any] | None:
    """Build the product-followup delta's compact saved diagnostic context.

    Source: `product-followup-delta-contract.md`. This is memory packaging for
    the LLM, not a commercial classifier: it reads only persisted diagnostic,
    demo, and waitlist state and never inspects the current lead text.
    """

    if mode != "post_diagnostic":
        return None
    snapshot = dict(state_snapshot)
    diagnostic = snapshot.get("diagnostic") or {}
    if not isinstance(diagnostic, Mapping):
        return None
    status = diagnostic.get("status")
    if status not in {"complete", "completed", "delivered"}:
        return None

    indicated_agents = (
        diagnostic.get("indicated_agents")
        or diagnostic.get("indicated_routines_or_agents")
        or []
    )
    recommended_area = (
        diagnostic.get("recommended_area")
        or diagnostic.get("first_recommended_step")
        or diagnostic.get("priority")
    )
    context = {
        "pain_context_human": diagnostic.get("pain_context_human")
        or diagnostic.get("main_bottleneck"),
        "likely_cause": diagnostic.get("likely_cause"),
        "first_recommended_step": diagnostic.get("first_recommended_step"),
        "recommended_area": recommended_area,
        "indicated_agents": indicated_agents,
        "recommended_plan_or_range": diagnostic.get("recommended_plan_or_range")
        or diagnostic.get("plan_or_range_to_compare")
        or diagnostic.get("final_plan_line"),
        "demo_status": (snapshot.get("demo") or {}).get("status")
        if isinstance(snapshot.get("demo"), Mapping)
        else None,
        "waitlist_status": (snapshot.get("waitlist") or {}).get("status")
        if isinstance(snapshot.get("waitlist"), Mapping)
        else None,
        "unknowns": diagnostic.get("unknowns") or [],
    }
    compact = {
        key: value
        for key, value in context.items()
        if value not in (None, "", [], {})
    }
    return compact or None


def build_turn_situation(
    *,
    state_snapshot: Mapping[str, Any],
    channel: str,
    official_fact_keys: tuple[str, ...] = (),
) -> TurnSituation:
    """Build the deterministic board for this turn.

    Deliberately takes NO lead text: deriving anything commercial from raw
    text here is the forbidden pattern (`011/action-contract.md`).
    """

    mode = _derive_mode(state_snapshot)
    profile_context = _profile_name_context(state_snapshot)
    post_diagnostic_context = _compact_post_diagnostic_context(
        state_snapshot,
        mode=mode,
    )
    completed, missing = _diagnostic_progress(state_snapshot)
    menu = list(ACTION_MENU_BY_MODE.get(mode, ()))
    forbidden: list[str] = []
    constraints: list[str] = []
    obligations: list[str] = []
    pending: str | None = None

    if mode == "diagnostic":
        pending = missing[0] if missing else None
        if len(missing) > 1 and "complete_diagnostic" in menu:
            # Completion is possible only when this turn's captured answer can
            # close the LAST missing key.
            menu.remove("complete_diagnostic")
            forbidden.append("complete_diagnostic")
            constraints.append(
                "diagnostic cannot complete this turn: missing keys beyond the "
                "pending one (" + ", ".join(missing) + ")"
            )
        if pending:
            obligations.append(
                f"resume the pending diagnostic question ({pending}) after "
                "answering any direct question"
            )
            constraints.append(
                "ask exactly one question per turn; give grounded feedback on "
                "the previous answer before the next question"
            )

    if mode == "handoff":
        constraints.append(
            "human handoff owns this conversation: AI replies stay suppressed "
            "until an explicit operator resume event"
        )

    if mode == "delivery_deferred":
        constraints.append(
            "a previous reply is still being delivered in chunks: defer this "
            "inbound; do not answer it yet"
        )

    if mode == "post_diagnostic":
        waitlist = dict(state_snapshot).get("waitlist") or {}
        if isinstance(waitlist, Mapping) and waitlist.get("status") == "joined":
            if "offer_or_join_waitlist_if_eligible" in menu:
                menu.remove("offer_or_join_waitlist_if_eligible")
                forbidden.append("offer_or_join_waitlist_if_eligible")
            constraints.append(
                "studio is already on the waitlist: preserve status, never "
                "re-offer it"
            )
        constraints.append(
            "use the saved diagnostic as commercial memory; never restart the "
            "diagnostic or re-ask answered facts"
        )

    return TurnSituation(
        mode=mode,
        channel=channel,
        allowed_actions=tuple(menu),
        forbidden_actions_now=tuple(forbidden),
        eligible_template_groups=_TEMPLATE_GROUPS_BY_MODE.get(mode, ()),
        pending_question_key=pending,
        completed_diagnostic_keys=completed,
        missing_diagnostic_keys=missing,
        required_obligations=tuple(obligations),
        official_fact_keys_available=tuple(official_fact_keys),
        profile_name_context=profile_context,
        post_diagnostic_context=post_diagnostic_context,
        state_constraints=tuple(constraints),
        # Handoff mode is pure suppression: once a handoff was acknowledged
        # (human_status set / canonical handoff states), no AI reply happens
        # until an explicit operator resume. The handoff REQUEST itself is an
        # LLM action chosen from within a commercial mode, not here.
        llm_turn_allowed=mode not in {"safety", "delivery_deferred", "handoff"},
        state_snapshot=dict(state_snapshot),
    )
