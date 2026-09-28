from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CONTRACT_SCHEMA_MAP = (
    REPO_ROOT / "specs/011-taliya-commercial-agent-core-reset/contract-schema-map.md"
)

REQUIRED_PRESERVED_SOURCES = [
    "behavior-contract.md",
    "diagnostic-contract.md",
    "conversation-state-contract.md",
    "message-template-contract.md",
    "product-followup-delta-contract.md",
    "sales-inbox-contract.md",
    "current-runtime-gap-analysis.md",
    "reference-map.md",
    "specs/006-crm-operational-core/",
    "specs/009-taliya-sales-agent-architecture/",
]

REQUIRED_SCHEMA_NAMES = [
    "TurnContext",
    "ConductorDecision",
    "NumericInterpretation",
    "DiagnosticLedgerItem",
    "DiagnosticDecision",
    "TemplateVariableValue",
    "RenderPlan",
    "ValidatorResult",
    "RepairResult",
    "OutboxPlan",
    "TraceRecord",
    "SalesInboxProjection",
]

REQUIRED_HOME_TYPES = ["schema", "validator", "renderer", "projection", "trace", "eval"]


def _table_row_for(source: str, text: str) -> str:
    row_prefix = f"| `{source}` |"
    for line in text.splitlines():
        if line.startswith(row_prefix):
            return line
    raise AssertionError(f"Missing contract-schema-map row for {source}")


def test_preserved_contracts_have_explicit_schema_map_rows() -> None:
    text = CONTRACT_SCHEMA_MAP.read_text(encoding="utf-8")

    for source in REQUIRED_PRESERVED_SOURCES:
        row = _table_row_for(source, text)
        assert any(home in row.lower() for home in REQUIRED_HOME_TYPES), row


def test_contract_schema_map_names_required_schema_homes() -> None:
    text = CONTRACT_SCHEMA_MAP.read_text(encoding="utf-8")

    for schema_name in REQUIRED_SCHEMA_NAMES:
        assert f"`{schema_name}`" in text


def test_contract_schema_map_blocks_doc_only_and_runner_brain_regression() -> None:
    text = CONTRACT_SCHEMA_MAP.read_text(encoding="utf-8").lower()

    required_phrases = [
        "not a docs-only source",
        "no commercial deterministic routing",
        "runner.py",
        "template-first",
        "schema/context/prompt/validator/eval",
        "known gaps",
    ]

    for phrase in required_phrases:
        assert phrase in text
