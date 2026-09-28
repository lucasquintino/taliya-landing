from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CORE_DIR = REPO_ROOT / "services" / "taliya-agent-runtime" / "app" / "core" / "taliya_commercial"


def _source(name: str) -> str:
    return (CORE_DIR / name).read_text(encoding="utf-8")


def test_turn_situation_and_compiler_do_not_parse_raw_lead_text() -> None:
    audited = {
        "turn_situation.py": _source("turn_situation.py"),
        "decision_compiler.py": _source("decision_compiler.py"),
    }
    forbidden_fragments = (
        "context.inbound.text",
        ".inbound.text",
        "message.text",
        "lower(",
        "casefold(",
        "import re",
        "regex",
    )

    violations = [
        f"{file_name}:{fragment}"
        for file_name, source in audited.items()
        for fragment in forbidden_fragments
        if fragment in source
    ]

    assert violations == []


def test_action_conductor_schema_keeps_templates_and_state_out_of_llm_action() -> None:
    source = _source("schemas.py")
    action_schema_section = source.split("class ConductorActionDecision", 1)[1].split(
        "class ConductorDecision",
        1,
    )[0]

    assert "template_plan" not in action_schema_section
    assert "render_plan" not in action_schema_section
    assert "previous_state" not in action_schema_section
    assert "current_state" not in action_schema_section
    assert "next_state" not in action_schema_section
    assert "route" not in action_schema_section
