import pytest

from app.runtime.schemas import AgentMessage, AgentOutput, RuntimeDecision, Usage, WaitlistAction
from app.shared.guardrails.validators import OutputValidationError, validate_structured_output


def _usage() -> Usage:
    return Usage(model="gpt-5.4-mini", input_tokens=1, output_tokens=1, cost_usd=0)


def test_waitlist_is_blocked_without_clear_contract_intent_flag():
    output = AgentOutput(
        decision=RuntimeDecision(
            current_state="general_interest",
            next_state="waitlist_offered",
            route="waitlist",
            waitlist_allowed_now=False,
        ),
        messages=[AgentMessage(text="Posso te colocar na lista de espera.", channel_hint="widget")],
        waitlist_action=WaitlistAction(status="offered", reason="curiosity"),
        usage=_usage(),
    )

    with pytest.raises(OutputValidationError) as exc:
        validate_structured_output(output)

    assert exc.value.code == "waitlist_offered_too_early"


def test_waitlist_allowed_with_clear_contract_intent_flag():
    output = AgentOutput(
        decision=RuntimeDecision(
            current_state="buying_intent_detected",
            next_state="waitlist_offered",
            route="waitlist",
            waitlist_allowed_now=True,
        ),
        messages=[AgentMessage(text="Estamos trabalhando com um numero pequeno de studios agora.", channel_hint="widget")],
        waitlist_action=WaitlistAction(status="offered", reason="clear_contract_intent"),
        usage=_usage(),
    )

    validate_structured_output(output)
