from __future__ import annotations

import pytest

from app.core.taliya_commercial_sdk.ideal_conversation import (
    IDEAL_CONVERSATION_SCRIPT,
    ConversationTurnScript,
    diagnostic_keys_answered,
    run_ideal_conversation,
)
from tests.test_spec012_sdk_paid_harness_dry_run import (
    ScriptedFakeModel,
    _diagnostic_120_structured_output,
    _function_call,
    _message,
    _price_first_structured_output,
)


def test_ideal_conversation_script_covers_the_full_funnel() -> None:
    assert len(IDEAL_CONVERSATION_SCRIPT) == 12
    joined_goals = " ".join(turn.goal.lower() for turn in IDEAL_CONVERSATION_SCRIPT)
    for stage in (
        "source opening",
        "pain-first",
        "price-first",
        "diagnostic start",
        "urgency",
        "demo request",
        "contract intent",
    ):
        assert stage in joined_goals, stage
    # Urgency must be answered before demo/waitlist closing turns.
    urgency_index = next(
        index
        for index, turn in enumerate(IDEAL_CONVERSATION_SCRIPT)
        if "urgency captured" in turn.goal
    )
    assert urgency_index == 9


@pytest.mark.asyncio
async def test_ideal_conversation_commits_state_between_turns_no_cost() -> None:
    script = (
        ConversationTurnScript("quanto custa?", "price"),
        ConversationTurnScript("120", "diagnostic numeric"),
    )
    fake_model = ScriptedFakeModel(
        [
            # Turn 1: triage hands off to product, which finalizes with price.
            [_function_call("transfer_to_taliya_product_agent")],
            [_message(_price_first_structured_output().model_dump_json())],
            # Turn 2: diagnostic answer with ledger update.
            [_function_call("transfer_to_taliya_diagnostic_agent")],
            [_message(_diagnostic_120_structured_output().model_dump_json())],
        ]
    )

    report = await run_ideal_conversation(model=fake_model, script=script)

    assert report.turns_passed == 2
    assert report.stopped_at_turn is None
    assert report.total_cost_usd == 0

    # Turn 1's validated proposal was committed before turn 2 ran.
    assert diagnostic_keys_answered(report.final_state) == [
        "active_students_or_size"
    ]
    diagnostic = report.final_state["diagnostic"]
    assert diagnostic["status"] == "in_progress"
    assert diagnostic["next_question_key"] == "main_pain"
    assert report.final_state["current_sdk_agent"] == "taliya_diagnostic_agent"
    assert "summary" in report.final_state

    # Transcript carries both lead messages and rendered approved replies.
    roles = [item["role"] for item in report.full_transcript]
    assert roles.count("user") == 2
    assert roles.count("assistant") >= 2


@pytest.mark.asyncio
async def test_ideal_conversation_stops_at_first_failed_turn() -> None:
    script = (
        ConversationTurnScript("quanto custa?", "price"),
        ConversationTurnScript("120", "never runs"),
    )
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            # Free-form text instead of structured output: turn 1 fails.
            [_message("Oi! O preco e R$ 197...")],
        ]
    )

    report = await run_ideal_conversation(model=fake_model, script=script)

    assert report.turns_passed == 0
    assert report.stopped_at_turn == 1
    assert fake_model.calls == 2
