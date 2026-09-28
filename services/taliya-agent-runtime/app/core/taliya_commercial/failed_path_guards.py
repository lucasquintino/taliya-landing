from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from app.core.taliya_commercial.fallback import SafeFallbackResult
from app.core.taliya_commercial.schemas import (
    ConductorDecision,
    RepairResult,
    Severity,
    ValidationIssue,
    ValidatorResult,
)

_ALLOWED_FAILED_PATH_TEMPLATE_IDS = frozenset(
    {
        "fallback.invalid_json",
        "fallback.provider_timeout",
        "handoff.acknowledge",
    }
)
_ALLOWED_FAILED_PATH_ROUTES = frozenset({"safe_fallback", "handoff", "none"})
_FORBIDDEN_OUTPUT_FIELDS = frozenset(
    {
        "delivery_events",
        "messages",
        "outbox",
        "outbox_messages",
        "outbox_plan",
        "rendered_message",
        "rendered_messages",
    }
)
_FORBIDDEN_COPY_FIELDS = frozenset(
    {
        "assistant_message",
        "assistant_reply",
        "freeform_response",
        "full_response",
        "message_text",
        "reply_text",
        "response_text",
    }
)
_CUSTOMER_OUTPUT_PATH_MARKERS = (
    "messages",
    "outbox",
    "rendered_message",
    "rendered_messages",
)
_FORBIDDEN_COMMERCIAL_VARIABLE_NAMES = frozenset(
    {
        "agent_name",
        "demo_link",
        "demo_status",
        "final_demo_line",
        "final_plan_or_range",
        "official_demo_link",
        "plan_name",
        "plan_price_summary",
        "product_fact_summary",
        "recommended_plan_or_range",
        "waitlist_status",
    }
)
_STATE_ADVANCEMENT_FIELDS = frozenset(
    {
        "current_state",
        "next_state",
        "previous_state",
    }
)


def validate_failed_path_result(
    payload: Any,
    *,
    decision_id: str | None = None,
) -> ValidatorResult:
    """Validate that a failure-path payload cannot become a commercial answer."""
    errors: list[ValidationIssue] = []
    errors.extend(_validate_known_failure_type(payload))
    normalized = _to_plain_payload(payload)
    errors.extend(_scan_failed_path_payload(normalized, path="payload"))

    return ValidatorResult(
        decision_id=_decision_id(payload, normalized, decision_id),
        status="blocked" if errors else "passed",
        errors=errors,
        repair_attempt_count=0,
        final_disposition="blocked" if errors else None,
    )


def _validate_known_failure_type(payload: Any) -> list[ValidationIssue]:
    if isinstance(payload, ConductorDecision):
        return [
            _issue(
                code="failed_path_decision_embedded",
                message="failed path result cannot contain a conductor decision",
                path="payload",
            )
        ]

    if isinstance(payload, ValidatorResult):
        if payload.status == "passed" or payload.final_disposition in {
            "accepted",
            "repaired",
        }:
            return [
                _issue(
                    code="failed_path_accepted_decision_forbidden",
                    message=(
                        "failed path cannot convert validation into an accepted "
                        "or repaired decision"
                    ),
                    path="payload.status",
                )
            ]
        return []

    if isinstance(payload, RepairResult):
        if payload.status == "repaired" or payload.repaired_decision is not None:
            return [
                _issue(
                    code="failed_path_repaired_decision_forbidden",
                    message="failed path cannot contain a repaired decision",
                    path="payload.repaired_decision",
                )
            ]
        if payload.status == "not_needed":
            return [
                _issue(
                    code="failed_path_not_needed_forbidden",
                    message="failed path cannot be marked not_needed",
                    path="payload.status",
                )
            ]
        return []

    if isinstance(payload, SafeFallbackResult):
        if payload.status == "not_needed":
            return [
                _issue(
                    code="failed_path_not_needed_forbidden",
                    message="failed path cannot be marked not_needed",
                    path="payload.status",
                )
            ]
        return []

    return []


def _scan_failed_path_payload(payload: Any, *, path: str) -> list[ValidationIssue]:
    if isinstance(payload, dict):
        return _scan_mapping(payload, path=path)
    if isinstance(payload, list | tuple | set):
        issues: list[ValidationIssue] = []
        for index, item in enumerate(payload):
            issues.extend(_scan_failed_path_payload(item, path=f"{path}[{index}]"))
        return issues
    return []


def _scan_mapping(payload: dict[str, Any], *, path: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    if _looks_like_conductor_decision(payload):
        issues.append(
            _issue(
                code="failed_path_decision_embedded",
                message="failed path result cannot contain a conductor decision",
                path=path,
            )
        )

    for key, value in payload.items():
        child_path = f"{path}.{key}"

        if key in _FORBIDDEN_OUTPUT_FIELDS:
            issues.append(
                _issue(
                    code="failed_path_rendered_output_forbidden",
                    message="failed path cannot contain rendered or delivery output",
                    path=child_path,
                )
            )

        if key in _FORBIDDEN_COPY_FIELDS or _is_customer_text_field(key, path):
            issues.append(
                _issue(
                    code="failed_path_customer_copy_forbidden",
                    message="failed path cannot contain customer-facing free-form copy",
                    path=child_path,
                )
            )

        if key == "template_id":
            issues.extend(_validate_template_id(value, path=child_path))
        elif key == "template_ids":
            issues.extend(_validate_template_ids(value, path=child_path))

        if key in {"route", "role"} and _is_forbidden_route_value(value):
            issues.append(
                _issue(
                    code="failed_path_route_forbidden",
                    message="failed path cannot advance through a commercial route",
                    path=child_path,
                )
            )

        if key in _STATE_ADVANCEMENT_FIELDS and value is not None:
            issues.append(
                _issue(
                    code="failed_path_state_advancement_forbidden",
                    message="failed path cannot advance commercial state",
                    path=child_path,
                )
            )

        if key in _FORBIDDEN_COMMERCIAL_VARIABLE_NAMES:
            issues.append(
                _issue(
                    code="failed_path_commercial_variable_forbidden",
                    message="failed path cannot contain commercial answer variables",
                    path=child_path,
                )
            )

        if key == "status" and value == "passed":
            issues.append(
                _issue(
                    code="failed_path_accepted_decision_forbidden",
                    message="failed path cannot be marked as an accepted decision",
                    path=child_path,
                )
            )

        if key == "final_disposition" and value in {"accepted", "repaired"}:
            issues.append(
                _issue(
                    code="failed_path_accepted_decision_forbidden",
                    message=(
                        "failed path cannot convert validation into an accepted "
                        "or repaired decision"
                    ),
                    path=child_path,
                )
            )

        if key == "repaired_decision" and value is not None:
            issues.append(
                _issue(
                    code="failed_path_repaired_decision_forbidden",
                    message="failed path cannot contain a repaired decision",
                    path=child_path,
                )
            )

        if key == "commercial_answer_allowed" and value is True:
            issues.append(
                _issue(
                    code="failed_path_commercial_answer_allowed",
                    message="failed path cannot allow commercial answers",
                    path=child_path,
                )
            )

        if key in {"context", "input", "turn_context"}:
            continue
        issues.extend(_scan_failed_path_payload(value, path=child_path))

    return _dedupe_issues(issues)


def _validate_template_id(value: Any, *, path: str) -> list[ValidationIssue]:
    if value is None:
        return []
    if not isinstance(value, str):
        return []
    if value in _ALLOWED_FAILED_PATH_TEMPLATE_IDS:
        return []
    return [
        _issue(
            code="failed_path_template_forbidden",
            message="failed path can use only safe fallback or handoff templates",
            path=path,
        )
    ]


def _validate_template_ids(value: Any, *, path: str) -> list[ValidationIssue]:
    if isinstance(value, str):
        values = [value]
    elif isinstance(value, list | tuple | set):
        values = [str(item) for item in value]
    else:
        return []

    issues: list[ValidationIssue] = []
    for index, template_id in enumerate(values):
        issues.extend(_validate_template_id(template_id, path=f"{path}[{index}]"))
    return issues


def _is_forbidden_route_value(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    return value not in _ALLOWED_FAILED_PATH_ROUTES


def _is_customer_text_field(key: str, path: str) -> bool:
    if key != "text":
        return False
    return path == "payload" or any(marker in path for marker in _CUSTOMER_OUTPUT_PATH_MARKERS)


def _looks_like_conductor_decision(payload: dict[str, Any]) -> bool:
    required_keys = {
        "schema_version",
        "turn_id",
        "conversation_id",
        "route",
        "template_plan",
    }
    return required_keys.issubset(payload.keys())


def _to_plain_payload(payload: Any) -> Any:
    if isinstance(payload, BaseModel):
        return payload.model_dump(mode="python")
    return payload


def _decision_id(
    payload: Any,
    normalized: Any,
    fallback_decision_id: str | None,
) -> str:
    if fallback_decision_id:
        return fallback_decision_id

    payload_decision_id = getattr(payload, "decision_id", None)
    if isinstance(payload_decision_id, str) and payload_decision_id:
        return payload_decision_id

    if isinstance(normalized, dict):
        normalized_decision_id = normalized.get("decision_id")
        if isinstance(normalized_decision_id, str) and normalized_decision_id:
            return normalized_decision_id

    return "failed_path"


def _dedupe_issues(issues: list[ValidationIssue]) -> list[ValidationIssue]:
    seen: set[tuple[str, str | None]] = set()
    deduped: list[ValidationIssue] = []
    for issue in issues:
        key = (issue.code, issue.path)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(issue)
    return deduped


def _issue(*, code: str, message: str, path: str) -> ValidationIssue:
    return ValidationIssue(
        code=code,
        severity=_P0,
        message=message,
        path=path,
    )


_P0: Severity = "P0"
