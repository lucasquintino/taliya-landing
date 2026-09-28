"""T012-047: manual transcript review package."""

from __future__ import annotations

import json

import pytest

from app.core.taliya_commercial_sdk.action_turn_runner import run_action_conversation
from app.core.taliya_commercial_sdk.conductor_decision import ConductorActionDecision
from app.core.taliya_commercial_sdk.manual_review_package import (
    MANUAL_REVIEW_CHECKLIST,
    export_manual_transcript_review_package,
    write_manual_transcript_review_package,
)
from tests.test_spec012_sdk_paid_harness_dry_run import (
    ScriptedFakeModel,
    _function_call,
    _message,
)


def _decision_json(action: str, **overrides) -> str:
    payload = {"selected_action": action, "evidence": ["inbound.text"], **overrides}
    return ConductorActionDecision.model_validate(payload).model_dump_json()


@pytest.mark.asyncio
async def test_t012_047_exports_manual_transcript_review_package(tmp_path) -> None:
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [
                _message(
                    _decision_json(
                        "answer_direct_product_question",
                        direct_question="quanto custa?",
                        product_fact_keys_used=["prices"],
                    )
                )
            ],
            [_function_call("transfer_to_taliya_diagnostic_agent")],
            [_message(_decision_json("start_requested_diagnostic"))],
            [
                _message(
                    _decision_json(
                        "handoff_requested",
                        handoff_intent="requested",
                        composition_variables=[
                            {
                                "name": "handoff_reason",
                                "value": "preferiu falar com uma pessoa da equipe",
                                "evidence": ["inbound.text"],
                            }
                        ],
                    )
                )
            ],
        ]
    )
    report = await run_action_conversation(
        [
            "quanto custa?",
            "quero fazer o diagnostico gratuito",
            "prefiro falar com uma pessoa",
            "alguem ai?",
        ],
        model=fake_model,
    )

    package = export_manual_transcript_review_package(
        report,
        scenario_id="t012-047-mocked-manual-review",
    )

    assert package["schema"] == "012.manual_transcript_review.v1"
    assert package["review_status"] == "pending_manual_review"
    assert package["manual_decision"] == "pending"
    assert package["summary"]["turn_count"] == 4
    assert package["summary"]["delivered_turn_count"] == 3
    assert package["summary"]["suppressed_turn_count"] == 1
    assert package["summary"]["total_cost_usd"] == 0
    assert len(package["checklist"]) == len(MANUAL_REVIEW_CHECKLIST)
    assert {item["status"] for item in package["checklist"]} == {"pending"}
    assert package["transcript"]
    assert package["turns"][0]["selected_action"] == "answer_direct_product_question"
    assert package["turns"][0]["trace_present"] is True
    assert package["turns"][0]["trace_complete"] is True
    assert package["turns"][0]["sales_inbox_projection_present"] is True
    assert package["turns"][-1]["trace_present"] is False
    assert package["turns"][-1]["sales_inbox_projection_present"] is False
    assert package["turns"][-1]["status"] == "suppressed"

    json_path = write_manual_transcript_review_package(package, tmp_path)
    markdown_path = tmp_path / "manual-transcript-review-package.md"
    written = json.loads(json_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert json_path.name == "manual-transcript-review-package.json"
    assert written["manual_decision"] == "pending"
    assert "# Spec 012 Manual Transcript Review Package" in markdown
    assert "Review status: pending_manual_review" in markdown
    assert "answers_direct_questions_first" in markdown
    assert "trace=True" in markdown
    assert "projection=True" in markdown
    assert "**USER:** quanto custa?" in markdown
    assert "handoff_requested" in markdown
