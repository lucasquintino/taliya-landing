from __future__ import annotations

from pathlib import Path

from app.core.taliya_commercial.schema_versioning import (
    CONDUCTOR_SCHEMA_FINGERPRINT,
    CURRENT_CONDUCTOR_SCHEMA_VERSION,
    SUPPORTED_CONDUCTOR_SCHEMA_VERSIONS,
    conductor_schema_fingerprint,
    validate_conductor_schema_contract,
    validate_conductor_schema_version,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMA_VERSIONING_DOC = (
    REPO_ROOT / "specs/011-taliya-commercial-agent-core-reset/schema-versioning.md"
)


def test_current_conductor_schema_version_and_fingerprint_are_locked() -> None:
    assert CURRENT_CONDUCTOR_SCHEMA_VERSION == "011.0"
    assert SUPPORTED_CONDUCTOR_SCHEMA_VERSIONS == frozenset({"011.0"})
    assert conductor_schema_fingerprint() == CONDUCTOR_SCHEMA_FINGERPRINT
    assert validate_conductor_schema_contract().status == "compatible"


def test_unknown_or_silent_schema_versions_are_rejected() -> None:
    assert validate_conductor_schema_version({"schema_version": "011.0"}).status == (
        "compatible"
    )

    missing = validate_conductor_schema_version({})
    assert missing.status == "invalid"
    assert missing.issues == ("missing_schema_version",)

    legacy = validate_conductor_schema_version({"schema_version": "010.9"})
    assert legacy.status == "unsupported"
    assert legacy.issues == ("unsupported_schema_version:010.9",)

    silent_minor = validate_conductor_schema_version({"schema_version": "011.1"})
    assert silent_minor.status == "unsupported"
    assert silent_minor.issues == ("unsupported_schema_version:011.1",)


def test_schema_versioning_doc_records_migration_rules_and_gates() -> None:
    text = SCHEMA_VERSIONING_DOC.read_text(encoding="utf-8").lower()

    required_phrases = [
        "t011-026",
        "current conductor schema version: `011.0`",
        "schema fingerprint",
        "no silent migration",
        "no automatic downgrade",
        "compatibility review",
        "fixture updates",
        "eval coverage",
        "sales inbox projection review",
        "runner.py",
    ]

    for phrase in required_phrases:
        assert phrase in text
