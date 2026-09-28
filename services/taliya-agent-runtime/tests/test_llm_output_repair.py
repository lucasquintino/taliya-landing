import pytest

from app.runtime.runner import repair_structured_output_once
from app.runtime.schemas import AgentOutput, RuntimeDecision, Usage

pytestmark = pytest.mark.legacy_runner_reference


def test_repair_adds_safe_fallback_without_advancing_state_when_messages_missing():
    output = AgentOutput(
        decision=RuntimeDecision(
            previous_state="price_question",
            current_state="waitlist_offered",
            next_state="waitlist_joined",
        ),
        messages=[],
        usage=Usage(model="gpt-5.4-mini", input_tokens=1, output_tokens=1, cost_usd=0),
    )

    repaired = repair_structured_output_once(output, violation_code="empty_messages")

    assert repaired.decision.current_state == "price_question"
    assert repaired.decision.next_state == "price_question"
    assert repaired.decision.route == "safe_fallback"
    assert repaired.messages
