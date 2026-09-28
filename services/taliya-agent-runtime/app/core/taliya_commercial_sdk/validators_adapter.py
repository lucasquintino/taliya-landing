from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Literal

from app.core.taliya_commercial.renderer import RenderError, render_validated_template_plan
from app.core.taliya_commercial.schemas import (
    RenderedMessage,
    RenderPlan,
    RenderPlanItem,
    TemplateVariableValue,
    ValidationIssue,
    ValidatorResult,
)
from app.core.taliya_commercial.template_registry import TEMPLATE_REGISTRY, normalize_template_id
from app.core.taliya_commercial_sdk.agents import AGENT_TEMPLATE_PREFIXES
from app.core.taliya_commercial_sdk.output_schema import TaliyaTurnProposal

# The diagnostic is a controlled flow: fixed mandatory order, feedback plus
# the next question after every answer, staged delivery only when complete.
# Sequencing is operational process state owned by code; the LLM owns the
# interpretation of answers and the composition of feedback.
DIAGNOSTIC_MANDATORY_KEYS = (
    "active_students_or_size",
    "main_pain",
    "pain_detail",
    "current_process",
    "priority",
    "urgency",
)
DIAGNOSTIC_ASK_TEMPLATE_BY_KEY = {
    "active_students_or_size": "diagnostic.ask_active_students",
    "main_pain": "diagnostic.ask_main_pain",
    "pain_detail": "diagnostic.ask_pain_detail",
    "current_process": "diagnostic.ask_current_process",
    "priority": "diagnostic.ask_priority",
    "urgency": "diagnostic.ask_urgency",
}
_DIAGNOSTIC_COMPLETE_STATUSES = {
    "answered",
    "inferred_from_prior_message",
    "not_applicable",
}


@dataclass(frozen=True)
class SdkSpikeValidatedOutput:
    proposal: TaliyaTurnProposal
    validator_result: ValidatorResult
    render_plan: RenderPlan | None = None
    rendered_preview: list[RenderedMessage] = field(default_factory=list)
    proof_type: Literal["mocked", "isolated_spike"] = "mocked"
    commits_state: bool = False
    public_delivery: bool = False


def _normalized_tokens(text: str) -> set[str]:
    cleaned = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
    return {token for token in cleaned.split() if len(token) > 3}


def _question_is_from_current_inbound(question: str, current_user_text: str) -> bool:
    """Deterministic extraction check: the claimed direct question must come
    from the current inbound message, not from earlier turns."""

    question_tokens = _normalized_tokens(question)
    if not question_tokens:
        return True
    inbound_tokens = _normalized_tokens(current_user_text)
    overlap = len(question_tokens & inbound_tokens) / len(question_tokens)
    return overlap >= 0.5


def scrub_stale_direct_question(
    proposal: TaliyaTurnProposal,
    current_user_text: str,
) -> TaliyaTurnProposal:
    """Deterministically discard a provably stale direct-question claim.

    When the claimed direct question is verifiably absent from the current
    inbound message, it is a resurrected obligation from an earlier turn.
    Discarding it touches no commercial content (templates, ledger, variables
    stay intact); it removes a metadata claim that is deterministically false.
    """

    direct_question = proposal.commercial_understanding.direct_question
    if not direct_question or _question_is_from_current_inbound(
        direct_question, current_user_text
    ):
        return proposal
    kept_obligations = [
        obligation
        for obligation in proposal.answer_obligations
        if obligation.answered_before_steering
        or _question_is_from_current_inbound(obligation.obligation, current_user_text)
    ]
    understanding = proposal.commercial_understanding.model_copy(
        update={"direct_question": None}
    )
    return proposal.model_copy(
        update={
            "commercial_understanding": understanding,
            "answer_obligations": kept_obligations,
            "risks": [*proposal.risks, "stale_direct_question_scrubbed"],
        }
    )


def validate_and_render_spike_output(
    proposal: TaliyaTurnProposal,
    *,
    state_snapshot: Mapping[str, Any] | None = None,
    current_user_text: str | None = None,
) -> SdkSpikeValidatedOutput:
    """Validate a TaliyaTurnProposal and render an isolated approved-template preview.

    `state_snapshot` is the prior conversation state when the caller has it;
    the diagnostic-sequence checks that depend on prior ledger state degrade
    gracefully to plan-internal consistency when it is absent.
    """

    issues = _validate_proposal_for_spike(
        proposal,
        state_snapshot=state_snapshot,
        current_user_text=current_user_text,
    )
    render_plan: RenderPlan | None = None
    rendered_preview: list[RenderedMessage] = []

    if not issues:
        render_plan, render_issues = _build_render_plan(proposal)
        issues.extend(render_issues)

    validator_result = ValidatorResult(
        decision_id=f"sdk_{proposal.turn_id}",
        status="passed" if not issues else "failed",
        errors=issues,
        final_disposition="accepted" if not issues else "blocked",
    )

    if not issues and render_plan is not None:
        try:
            rendered_preview = render_validated_template_plan(
                render_plan,
                validator_result,
                channel=proposal.channel,
            )
        except RenderError as exc:
            validator_result = ValidatorResult(
                decision_id=f"sdk_{proposal.turn_id}",
                status="failed",
                errors=[
                    _issue(
                        "sdk_render_preview_failed",
                        str(exc),
                        path="template_proposal",
                    )
                ],
                final_disposition="blocked",
            )
            rendered_preview = []

    return SdkSpikeValidatedOutput(
        proposal=proposal,
        validator_result=validator_result,
        render_plan=render_plan if validator_result.status == "passed" else None,
        rendered_preview=rendered_preview,
    )


def _proposes_delivery_deferral(proposal: TaliyaTurnProposal) -> bool:
    delivery_patch = proposal.state_patch_proposal.get("delivery")
    if not isinstance(delivery_patch, dict):
        return False
    return bool(delivery_patch.get("defer_inbound_during_chunks"))


def _validate_proposal_for_spike(
    proposal: TaliyaTurnProposal,
    *,
    state_snapshot: Mapping[str, Any] | None = None,
    current_user_text: str | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    direct_question = proposal.commercial_understanding.direct_question
    # Deterministic extraction check: a claimed direct question that does not
    # come from the current inbound is a stale obligation resurrected from
    # earlier turns. It must be cleared, not enforced.
    stale_direct_question = bool(
        direct_question
        and current_user_text is not None
        and not _question_is_from_current_inbound(direct_question, current_user_text)
    )
    if stale_direct_question:
        issues.append(
            _issue(
                "sdk_direct_question_not_in_current_inbound",
                f"direct_question '{direct_question}' is not asked in the "
                "current inbound message. Questions already answered in "
                "earlier turns are not obligations of this turn: set "
                "direct_question to null and remove the stale obligation.",
                path="commercial_understanding.direct_question",
            )
        )
    # Operational deferral exception: while a previous reply is still being
    # delivered in chunks, the correct behavior is to defer the inbound, so an
    # unanswered direct question is expected, not a violation.
    if (
        direct_question
        and not stale_direct_question
        and not _proposes_delivery_deferral(proposal)
    ):
        if not proposal.answer_obligations:
            issues.append(
                _issue(
                    "sdk_missing_answer_obligation",
                    "Direct questions require answer obligations before steering.",
                    path="answer_obligations",
                )
            )
        unanswered = [
            obligation.obligation
            for obligation in proposal.answer_obligations
            if not obligation.answered_before_steering
        ]
        if unanswered:
            issues.append(
                _issue(
                    "sdk_direct_question_not_answered_first",
                    f"Answer obligations not marked answered first: {', '.join(unanswered)}",
                    path="answer_obligations",
                )
            )

    if proposal.product_claims:
        for index, claim in enumerate(proposal.product_claims):
            if not claim.fact_refs:
                issues.append(
                    _issue(
                        "sdk_product_claim_missing_fact_refs",
                        "Product claims require official fact refs.",
                        path=f"product_claims[{index}].fact_refs",
                    )
                )

    if not proposal.template_proposal.template_ids:
        issues.append(
            _issue(
                "sdk_missing_template_plan",
                "Spike render path requires approved template ids.",
                path="template_proposal.template_ids",
            )
        )

    issues.extend(_validate_template_ownership(proposal))
    issues.extend(_validate_diagnostic_sequence(proposal, state_snapshot))

    if not proposal.delivery_proposal.render_plan_only:
        issues.append(
            _issue(
                "sdk_delivery_not_render_plan_only",
                "SDK delivery proposal must remain render_plan_only.",
                path="delivery_proposal.render_plan_only",
            )
        )

    return issues


def _validate_template_ownership(proposal: TaliyaTurnProposal) -> list[ValidationIssue]:
    """Role boundary: an agent may only propose templates from its own catalog.

    This is deterministic proposal-internal consistency (which agent finalized
    vs which templates it chose), not commercial routing: the routing decision
    stays with the SDK agents.
    """

    final_agent = next(
        (
            item.agent
            for item in reversed(proposal.agent_path)
            if item.event == "final" and item.agent
        ),
        None,
    )
    if final_agent is None:
        return []
    prefixes = AGENT_TEMPLATE_PREFIXES.get(final_agent)
    if prefixes is None:
        return [
            _issue(
                "sdk_router_cannot_finalize",
                f"Agent {final_agent} is a router and must hand off, not reply.",
                path="agent_path",
            )
        ]
    issues: list[ValidationIssue] = []
    for index, template_id in enumerate(proposal.template_proposal.template_ids):
        if not any(template_id.startswith(prefix) for prefix in prefixes):
            issues.append(
                _issue(
                    "sdk_template_not_owned_by_agent",
                    f"Template {template_id} is outside {final_agent}'s approved "
                    "catalog; the owning specialist must handle this turn.",
                    path=f"template_proposal.template_ids[{index}]",
                )
            )
    return issues


def _validate_diagnostic_sequence(
    proposal: TaliyaTurnProposal,
    state_snapshot: Mapping[str, Any] | None,
) -> list[ValidationIssue]:
    """Deterministic guardrail for the controlled diagnostic flow.

    The mandatory question order is process state, not commercial judgment:
    after every recorded answer the turn must carry feedback plus exactly the
    next pending question, and delivery happens only when all six mandatory
    keys are complete. The LLM still interprets answers, composes feedback,
    and handles side questions.
    """

    plan_ids = [
        normalize_template_id(template_id)
        for template_id in proposal.template_proposal.template_ids
    ]
    ask_ids = [t for t in plan_ids if t.startswith("diagnostic.ask_")]
    deliver_ids = [t for t in plan_ids if t.startswith("diagnostic.deliver")]
    diagnostic = proposal.diagnostic_proposal
    recorded_keys = [
        update.get("question_key")
        for update in diagnostic.ledger_updates
        if update.get("question_key") in DIAGNOSTIC_MANDATORY_KEYS
        and update.get("status") in _DIAGNOSTIC_COMPLETE_STATUSES
    ]
    start_ids = [t for t in plan_ids if t.startswith("diagnostic.start")]
    active = bool(
        recorded_keys
        or diagnostic.next_question_key
        or diagnostic.final_diagnostic_ready
        or ask_ids
        or deliver_ids
        or start_ids
    )
    if not active:
        return []

    issues: list[ValidationIssue] = []

    if start_ids and not diagnostic.next_question_key:
        issues.append(
            _issue(
                "sdk_diagnostic_start_without_first_question",
                "Starting the diagnostic requires next_question_key (the first "
                "pending mandatory key) and its ask template in the same turn.",
                path="diagnostic_proposal.next_question_key",
            )
        )
    if diagnostic.final_diagnostic_ready and diagnostic.next_question_key:
        issues.append(
            _issue(
                "sdk_diagnostic_final_and_next_question_conflict",
                "final_diagnostic_ready and next_question_key cannot both be set.",
                path="diagnostic_proposal",
            )
        )
    prior_diagnostic_complete = bool(
        state_snapshot is not None
        and (dict(state_snapshot).get("diagnostic") or {}).get("status") == "complete"
    )
    if (
        diagnostic.final_diagnostic_ready
        and not deliver_ids
        and not prior_diagnostic_complete
    ):
        issues.append(
            _issue(
                "sdk_diagnostic_final_without_delivery",
                "final_diagnostic_ready requires diagnostic.deliver* templates.",
                path="template_proposal.template_ids",
            )
        )
    if deliver_ids and not diagnostic.final_diagnostic_ready:
        issues.append(
            _issue(
                "sdk_diagnostic_delivery_before_complete",
                "diagnostic.deliver* templates are forbidden before "
                "final_diagnostic_ready: all six mandatory keys must be "
                "complete first.",
                path="template_proposal.template_ids",
            )
        )
    if diagnostic.next_question_key:
        expected_template = DIAGNOSTIC_ASK_TEMPLATE_BY_KEY.get(
            diagnostic.next_question_key
        )
        if expected_template is None:
            issues.append(
                _issue(
                    "sdk_diagnostic_unknown_question_key",
                    f"Unknown diagnostic question key: {diagnostic.next_question_key}",
                    path="diagnostic_proposal.next_question_key",
                )
            )
        elif expected_template not in plan_ids:
            issues.append(
                _issue(
                    "sdk_diagnostic_next_question_template_missing",
                    f"next_question_key={diagnostic.next_question_key} requires "
                    f"template {expected_template} in the plan.",
                    path="template_proposal.template_ids",
                )
            )
    if (
        recorded_keys
        and diagnostic.next_question_key
        and "answer_feedback" not in proposal.template_proposal.variables
    ):
        issues.append(
            _issue(
                "sdk_diagnostic_feedback_missing",
                "After recording an answer, the turn must include the "
                "answer_feedback variable before asking the next question.",
                path="template_proposal.variables",
            )
        )

    if state_snapshot is None:
        return issues

    prior_ledger = (dict(state_snapshot).get("diagnostic") or {}).get("ledger") or {}
    complete = {
        key
        for key in DIAGNOSTIC_MANDATORY_KEYS
        if isinstance(prior_ledger.get(key), dict)
        and prior_ledger[key].get("status") in _DIAGNOSTIC_COMPLETE_STATUSES
    }
    previously_complete = set(complete)
    complete.update(recorded_keys)
    pending = [key for key in DIAGNOSTIC_MANDATORY_KEYS if key not in complete]

    if pending:
        expected_next = pending[0]
        if diagnostic.final_diagnostic_ready:
            issues.append(
                _issue(
                    "sdk_diagnostic_premature_completion",
                    "final_diagnostic_ready with pending mandatory keys: "
                    + ", ".join(pending),
                    path="diagnostic_proposal.final_diagnostic_ready",
                )
            )
        elif (
            diagnostic.next_question_key
            and diagnostic.next_question_key != expected_next
        ):
            issues.append(
                _issue(
                    "sdk_diagnostic_wrong_next_question",
                    f"Expected next mandatory key {expected_next} "
                    f"(template {DIAGNOSTIC_ASK_TEMPLATE_BY_KEY[expected_next]}), "
                    f"got {diagnostic.next_question_key}.",
                    path="diagnostic_proposal.next_question_key",
                )
            )
        repeated = [
            template_id
            for key, template_id in DIAGNOSTIC_ASK_TEMPLATE_BY_KEY.items()
            if template_id in ask_ids and key in previously_complete
        ]
        for template_id in repeated:
            issues.append(
                _issue(
                    "sdk_diagnostic_repeated_question",
                    f"Template {template_id} re-asks an already answered "
                    "diagnostic question.",
                    path="template_proposal.template_ids",
                )
            )
    elif not diagnostic.final_diagnostic_ready:
        issues.append(
            _issue(
                "sdk_diagnostic_completion_not_delivered",
                "All six mandatory keys are complete: this turn must set "
                "final_diagnostic_ready and deliver the staged diagnostic.",
                path="diagnostic_proposal.final_diagnostic_ready",
            )
        )

    return issues


def _build_render_plan(
    proposal: TaliyaTurnProposal,
) -> tuple[RenderPlan | None, list[ValidationIssue]]:
    issues: list[ValidationIssue] = []
    items: list[RenderPlanItem] = []
    template_variables = proposal.template_proposal.variables

    for index, template_id in enumerate(proposal.template_proposal.template_ids):
        normalized = normalize_template_id(template_id)
        template = TEMPLATE_REGISTRY.get(normalized)
        if template is None:
            issues.append(
                _issue(
                    "sdk_unknown_template_id",
                    f"Unknown approved template id: {template_id}",
                    path=f"template_proposal.template_ids[{index}]",
                )
            )
            continue

        variable_names = set(template.required_variables) | set(template.optional_variables)
        variables: dict[str, TemplateVariableValue] = {}
        for variable_name in sorted(variable_names):
            raw_variable = template_variables.get(variable_name)
            if raw_variable is None:
                continue
            if not isinstance(raw_variable, dict):
                issues.append(
                    _issue(
                        "sdk_template_variable_invalid",
                        f"Template variable must be an object: {variable_name}",
                        path=f"template_proposal.variables.{variable_name}",
                    )
                )
                continue
            try:
                variables[variable_name] = TemplateVariableValue.model_validate(raw_variable)
            except ValueError as exc:
                reasons = []
                for error in getattr(exc, "errors", lambda: [])():
                    message = str(error.get("msg", "")).removeprefix("Value error, ")
                    if message:
                        reasons.append(message)
                detail = "; ".join(reasons) if reasons else str(exc)
                issues.append(
                    _issue(
                        "sdk_template_variable_invalid",
                        f"variable {variable_name}: {detail}",
                        path=f"template_proposal.variables.{variable_name}",
                    )
                )

        try:
            items.append(
                RenderPlanItem(
                    template_id=template_id,
                    channel=proposal.channel,
                    variables=variables,
                )
            )
        except ValueError as exc:
            issues.append(
                _issue(
                    "sdk_render_plan_item_invalid",
                    str(exc),
                    path=f"template_proposal.template_ids[{index}]",
                )
            )

    if issues:
        return None, issues
    return (
        RenderPlan(
            items=items,
            chunk_policy=_chunk_policy_for(proposal),
        ),
        [],
    )


def _chunk_policy_for(proposal: TaliyaTurnProposal) -> Literal[
    "default",
    "whatsapp_max_3",
    "staged_diagnostic",
    "none",
]:
    requested = proposal.delivery_proposal.chunk_policy
    if requested in {"default", "whatsapp_max_3", "staged_diagnostic", "none"}:
        return requested  # type: ignore[return-value]
    return "whatsapp_max_3" if proposal.channel == "whatsapp" else "default"


def _issue(code: str, message: str, *, path: str | None = None) -> ValidationIssue:
    return ValidationIssue(code=code, severity="P0", message=message, path=path)
