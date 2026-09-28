from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, ValidationError

from app.core.taliya_commercial.schemas import (
    Severity,
    StrictModel,
    ValidationIssue,
    ValidatorResult,
)

_APPROVED_PRODUCT_FACT_SOURCES = {
    "official_product_knowledge",
    "spec_006_product_contract",
}


class ProductFactSource(StrictModel):
    key: str
    source: Literal[
        "official_product_knowledge",
        "spec_006_product_contract",
        "prompt",
        "policy",
        "template",
        "test",
        "fallback",
    ]
    reference: str


class GovernanceChangeMetadata(StrictModel):
    change_id: str
    date: str
    owner: str
    artifact_type: Literal["prompt", "policy", "template", "product_knowledge"]
    affected_artifacts: list[str] = Field(default_factory=list)
    reason: str
    expected_impact: str
    transcript_diff_reference: str
    eval_before_reference: str
    eval_after_reference: str
    approval_evidence: list[str] = Field(default_factory=list)
    sensitive_change: bool = True
    product_fact_sources: list[ProductFactSource] = Field(default_factory=list)


def validate_governance_metadata(payload: Any) -> ValidatorResult:
    errors: list[ValidationIssue] = []
    try:
        metadata = GovernanceChangeMetadata.model_validate(payload)
    except ValidationError as error:
        return ValidatorResult(
            decision_id=_payload_change_id(payload),
            status="blocked",
            errors=[
                _issue(
                    code="governance_schema_invalid",
                    message=str(error),
                    path="governance_metadata",
                )
            ],
            final_disposition="blocked",
        )

    errors.extend(_validate_required_review_fields(metadata))
    errors.extend(_validate_product_fact_sources(metadata))

    return ValidatorResult(
        decision_id=metadata.change_id,
        status="blocked" if errors else "passed",
        errors=errors,
        final_disposition="blocked" if errors else "accepted",
    )


def _validate_required_review_fields(
    metadata: GovernanceChangeMetadata,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not metadata.reason.strip():
        issues.append(
            _issue(
                code="governance_reason_missing",
                message="governance metadata requires a reason",
                path="reason",
            )
        )
    if not metadata.expected_impact.strip():
        issues.append(
            _issue(
                code="governance_expected_impact_missing",
                message="governance metadata requires expected impact",
                path="expected_impact",
            )
        )
    if not metadata.transcript_diff_reference.strip():
        issues.append(
            _issue(
                code="governance_transcript_diff_missing",
                message="governance metadata requires transcript diff reference",
                path="transcript_diff_reference",
            )
        )
    if not (
        metadata.eval_before_reference.strip()
        and metadata.eval_after_reference.strip()
    ):
        issues.append(
            _issue(
                code="governance_eval_reference_missing",
                message="governance metadata requires before and after eval references",
                path="eval_before_reference",
            )
        )
    if metadata.sensitive_change and not _has_text(metadata.approval_evidence):
        issues.append(
            _issue(
                code="governance_approval_missing",
                message="sensitive governance changes require approval evidence",
                path="approval_evidence",
            )
        )
    if not _has_text(metadata.affected_artifacts):
        issues.append(
            _issue(
                code="governance_affected_artifacts_missing",
                message="governance metadata requires affected artifacts",
                path="affected_artifacts",
            )
        )
    return issues


def _validate_product_fact_sources(
    metadata: GovernanceChangeMetadata,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for index, source in enumerate(metadata.product_fact_sources):
        if source.source in _APPROVED_PRODUCT_FACT_SOURCES:
            continue
        issues.append(
            _issue(
                code="governance_product_fact_source_invalid",
                message=(
                    "product facts must be sourced from official product "
                    "knowledge or Spec 006 product contracts"
                ),
                path=f"product_fact_sources[{index}].source",
            )
        )
    return issues


def _has_text(values: list[str]) -> bool:
    return any(value.strip() for value in values)


def _payload_change_id(payload: Any) -> str:
    if isinstance(payload, dict):
        value = payload.get("change_id")
        if isinstance(value, str) and value.strip():
            return value
    return "governance_metadata"


def _issue(*, code: str, message: str, path: str) -> ValidationIssue:
    return ValidationIssue(code=code, severity=_P0, message=message, path=path)


_P0: Severity = "P0"
