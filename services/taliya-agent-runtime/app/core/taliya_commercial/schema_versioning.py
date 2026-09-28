from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Literal

from app.core.taliya_commercial.schemas import ConductorDecision

CURRENT_CONDUCTOR_SCHEMA_VERSION = "011.0"
SUPPORTED_CONDUCTOR_SCHEMA_VERSIONS = frozenset({CURRENT_CONDUCTOR_SCHEMA_VERSION})
CONDUCTOR_SCHEMA_FINGERPRINT = (
    "sha256:e093d16fc05f349b3ddc27389eabaa33544fc10366606b4323e3e9a92bef7bb4"
)


@dataclass(frozen=True, slots=True)
class SchemaCompatibilityResult:
    status: Literal["compatible", "invalid", "unsupported", "fingerprint_mismatch"]
    schema_version: str | None
    issues: tuple[str, ...] = ()


def conductor_schema_fingerprint() -> str:
    schema = ConductorDecision.model_json_schema()
    payload = json.dumps(
        schema,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return f"sha256:{hashlib.sha256(payload.encode('utf-8')).hexdigest()}"


def validate_conductor_schema_contract() -> SchemaCompatibilityResult:
    current_fingerprint = conductor_schema_fingerprint()
    if current_fingerprint != CONDUCTOR_SCHEMA_FINGERPRINT:
        return SchemaCompatibilityResult(
            status="fingerprint_mismatch",
            schema_version=CURRENT_CONDUCTOR_SCHEMA_VERSION,
            issues=(
                "conductor_schema_fingerprint_changed:"
                f"{current_fingerprint}!={CONDUCTOR_SCHEMA_FINGERPRINT}",
            ),
        )

    return SchemaCompatibilityResult(
        status="compatible",
        schema_version=CURRENT_CONDUCTOR_SCHEMA_VERSION,
    )


def validate_conductor_schema_version(
    payload: Mapping[str, Any],
) -> SchemaCompatibilityResult:
    schema_version = payload.get("schema_version")
    if not isinstance(schema_version, str):
        return SchemaCompatibilityResult(
            status="invalid",
            schema_version=None,
            issues=("missing_schema_version",),
        )

    if schema_version in SUPPORTED_CONDUCTOR_SCHEMA_VERSIONS:
        return SchemaCompatibilityResult(
            status="compatible",
            schema_version=schema_version,
        )

    return SchemaCompatibilityResult(
        status="unsupported",
        schema_version=schema_version,
        issues=(f"unsupported_schema_version:{schema_version}",),
    )
