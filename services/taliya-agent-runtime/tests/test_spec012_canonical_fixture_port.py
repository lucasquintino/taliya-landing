from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPEC011_DIR = ROOT / "specs" / "011-taliya-commercial-agent-core-reset"
SPEC012_DIR = ROOT / "specs" / "012-taliya-commercial-agent-agents-sdk-migration"
FIXTURE_DIR = ROOT / "scripts" / "fixtures" / "agent-runtime"


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _ids(items: list[dict]) -> set[str]:
    return {str(item["id"]) for item in items}


def test_t012_038_canonical_fixture_map_matches_spec011_sources() -> None:
    fixture_map = _json(SPEC012_DIR / "canonical-fixture-map.json")
    golden = _json(FIXTURE_DIR / "spec-011-golden-transcripts.json")
    do_not_do_runtime = _json(FIXTURE_DIR / "spec-011-do-not-do-runtime.json")
    p0 = _json(FIXTURE_DIR / "spec-011-real-openai-p0.json")
    do_not_do_static = _json(SPEC011_DIR / "do-not-do-static-fixtures.json")

    assert fixture_map["schema_version"] == "012.canonical_fixture_map.v1"
    assert _ids(fixture_map["golden"]) == _ids(golden)
    assert _ids(fixture_map["do_not_do_runtime"]) == _ids(do_not_do_runtime)
    assert _ids(fixture_map["p0_regression"]) == _ids(p0)
    assert _ids(fixture_map["do_not_do_static"]) == _ids(do_not_do_static["cases"])


def test_t012_038_canonical_fixture_regression_ids_exist() -> None:
    regression_source = (SPEC011_DIR / "regression-cases.md").read_text(
        encoding="utf-8"
    )
    known_case_ids = set(re.findall(r"RC-011-[0-9A-Z]+", regression_source))
    assert len(known_case_ids) >= 70

    fixture_sources = [
        _json(FIXTURE_DIR / "spec-011-golden-transcripts.json"),
        _json(FIXTURE_DIR / "spec-011-do-not-do-runtime.json"),
        _json(FIXTURE_DIR / "spec-011-real-openai-p0.json"),
    ]
    referenced = {
        case_id
        for source in fixture_sources
        for item in source
        for field in ("golden_case_ids", "do_not_do_case_ids", "regression_case_ids")
        for case_id in item.get(field, [])
    }
    static_referenced = {
        case_id
        for item in _json(SPEC011_DIR / "do-not-do-static-fixtures.json")["cases"]
        for case_id in item["do_not_do_case_ids"]
    }

    assert referenced | static_referenced <= known_case_ids


def test_t012_038_every_ported_fixture_has_action_first_owner_and_proof_mode() -> None:
    fixture_map = _json(SPEC012_DIR / "canonical-fixture-map.json")
    allowed_owners = {
        "action_turn_runner",
        "action_validators",
        "conductor_decision",
        "decision_compiler",
        "diagnostic_agent",
        "entry_agent",
        "eval_harness",
        "handoff_agent",
        "product_agent",
        "product_knowledge",
        "profile_name_context",
        "renderer",
        "sales_inbox_projection",
        "static_audit",
        "turn_situation",
        "waitlist_agent",
    }
    allowed_proof_modes = {"mocked", "static", "real_model_required_later"}

    all_items = [
        item
        for section in (
            "golden",
            "do_not_do_runtime",
            "p0_regression",
            "do_not_do_static",
        )
        for item in fixture_map[section]
    ]

    assert all_items
    for item in all_items:
        assert item["action_first_owners"], item["id"]
        assert set(item["action_first_owners"]) <= allowed_owners, item["id"]
        assert item["proof_modes"], item["id"]
        assert set(item["proof_modes"]) <= allowed_proof_modes, item["id"]
        if item["proof_modes"] != ["static"]:
            assert "real_model_required_later" in item["proof_modes"], item["id"]


def test_t012_038_map_keeps_paid_real_model_work_explicitly_deferred() -> None:
    fixture_map = _json(SPEC012_DIR / "canonical-fixture-map.json")
    runtime_items = [
        item
        for section in ("golden", "do_not_do_runtime", "p0_regression")
        for item in fixture_map[section]
    ]

    assert runtime_items
    assert all("mocked" in item["proof_modes"] for item in runtime_items)
    assert all(
        "real_model_required_later" in item["proof_modes"] for item in runtime_items
    )
