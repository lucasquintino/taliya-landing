from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from app.core.taliya_commercial.schemas import (
    Channel,
    ConductorDecision,
    RepairResult,
    StrictModel,
    TurnContext,
    ValidatorResult,
)
from app.core.taliya_commercial.template_registry import TEMPLATE_REGISTRY

FailureSource = Literal[
    "validator_blocked",
    "repair_failed",
    "provider_timeout",
    "provider_output_invalid",
    "llm_error",
]
FallbackStatus = Literal["not_needed", "safe_fallback", "handoff_required"]
FallbackRoute = Literal["none", "safe_fallback", "handoff"]
HandoffStatus = Literal["none", "requested"]

_SAFE_TEMPLATE_BY_SOURCE: dict[FailureSource, str] = {
    "validator_blocked": "handoff.acknowledge",
    "repair_failed": "handoff.acknowledge",
    "provider_timeout": "fallback.provider_timeout",
    "provider_output_invalid": "fallback.invalid_json",
    "llm_error": "handoff.acknowledge",
}
_SAFE_FALLBACK_TEMPLATES = frozenset(_SAFE_TEMPLATE_BY_SOURCE.values())


class SafeFallbackResult(StrictModel):
    turn_id: str
    conversation_id: str
    channel: Channel
    status: FallbackStatus
    route: FallbackRoute = "none"
    source: FailureSource | None = None
    reason_code: str | None = None
    decision_id: str | None = None
    validator_status: str | None = None
    repair_status: str | None = None
    template_id: str | None = None
    handoff_status: HandoffStatus = "none"
    ai_pause_required: bool = False
    commercial_answer_allowed: bool = False
    error_codes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def fallback_never_allows_commercial_answer(self) -> SafeFallbackResult:
        if self.commercial_answer_allowed:
            raise ValueError("safe fallback cannot allow commercial answers")

        if self.status == "not_needed":
            if self.route != "none" or self.template_id is not None:
                raise ValueError("not_needed fallback cannot select a template")
            return self

        if self.template_id not in _SAFE_FALLBACK_TEMPLATES:
            raise ValueError("safe fallback template must be approved")
        if self.template_id not in TEMPLATE_REGISTRY:
            raise ValueError("safe fallback template must exist in registry")

        if self.status == "handoff_required":
            if self.route != "handoff":
                raise ValueError("handoff fallback must use handoff route")
            if self.handoff_status != "requested":
                raise ValueError("handoff fallback must request handoff")
            if not self.ai_pause_required:
                raise ValueError("handoff fallback must pause AI")
            return self

        if self.route != "safe_fallback":
            raise ValueError("safe_fallback status must use safe_fallback route")
        if self.handoff_status != "none" or self.ai_pause_required:
            raise ValueError("safe fallback cannot mark human handoff active")
        return self


def build_safe_fallback_disposition(
    *,
    context: TurnContext,
    failure_source: FailureSource,
    decision: ConductorDecision | None = None,
    validator_result: ValidatorResult | None = None,
    repair_result: RepairResult | None = None,
    failure_reason: str | None = None,
) -> SafeFallbackResult:
    if _fallback_not_needed(validator_result, repair_result):
        return SafeFallbackResult(
            turn_id=context.turn_id,
            conversation_id=context.conversation_id,
            channel=context.channel,
            status="not_needed",
            route="none",
            decision_id=_decision_id(decision, validator_result),
            validator_status=_validator_status(validator_result),
            repair_status=_repair_status(repair_result),
            commercial_answer_allowed=False,
        )

    template_id = _SAFE_TEMPLATE_BY_SOURCE[failure_source]
    reason_code = failure_reason or failure_source
    error_codes = _error_codes(
        validator_result=validator_result,
        repair_result=repair_result,
        reason_code=reason_code,
    )

    if template_id == "handoff.acknowledge":
        return SafeFallbackResult(
            turn_id=context.turn_id,
            conversation_id=context.conversation_id,
            channel=context.channel,
            status="handoff_required",
            route="handoff",
            source=failure_source,
            reason_code=reason_code,
            decision_id=_decision_id(decision, validator_result),
            validator_status=_validator_status(validator_result),
            repair_status=_repair_status(repair_result),
            template_id=template_id,
            handoff_status="requested",
            ai_pause_required=True,
            commercial_answer_allowed=False,
            error_codes=error_codes,
        )

    return SafeFallbackResult(
        turn_id=context.turn_id,
        conversation_id=context.conversation_id,
        channel=context.channel,
        status="safe_fallback",
        route="safe_fallback",
        source=failure_source,
        reason_code=reason_code,
        decision_id=_decision_id(decision, validator_result),
        validator_status=_validator_status(validator_result),
        repair_status=_repair_status(repair_result),
        template_id=template_id,
        handoff_status="none",
        ai_pause_required=False,
        commercial_answer_allowed=False,
        error_codes=error_codes,
    )


def _fallback_not_needed(
    validator_result: ValidatorResult | None,
    repair_result: RepairResult | None,
) -> bool:
    validator_ok = validator_result is not None and validator_result.status == "passed"
    repair_ok = repair_result is None or repair_result.status in {
        "not_needed",
        "repaired",
    }
    return validator_ok and repair_ok


def _decision_id(
    decision: ConductorDecision | None,
    validator_result: ValidatorResult | None,
) -> str | None:
    if decision is not None:
        return decision.decision_id
    if validator_result is not None:
        return validator_result.decision_id
    return None


def _validator_status(validator_result: ValidatorResult | None) -> str | None:
    return validator_result.status if validator_result is not None else None


def _repair_status(repair_result: RepairResult | None) -> str | None:
    return repair_result.status if repair_result is not None else None


def _error_codes(
    *,
    validator_result: ValidatorResult | None,
    repair_result: RepairResult | None,
    reason_code: str,
) -> list[str]:
    codes = {reason_code}
    if validator_result is not None:
        codes.update(issue.code for issue in validator_result.errors)
    if repair_result is not None:
        codes.update(repair_result.errors_sent)
    return sorted(codes)
