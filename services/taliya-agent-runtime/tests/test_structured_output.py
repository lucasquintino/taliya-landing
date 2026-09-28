import pytest
from pydantic import ValidationError

from app.runtime.schemas import AgentMessage, AgentOutput, DiagnosticOutput, RuntimeDecision, SourceRef, Usage
from app.shared.guardrails.validators import OutputValidationError, validate_structured_output


def _usage() -> Usage:
    return Usage(model="gpt-5.2", input_tokens=100, output_tokens=40, cost_usd=0.001)


def test_valid_output_accepts_product_source_for_price_claim():
    output = AgentOutput(
        messages=[
            AgentMessage(
                text="Os planos comecam em R$ 197/mes no Base.",
                channel_hint="widget",
                requires_product_source=True,
            )
        ],
        sources=[SourceRef(type="product_knowledge", version="taliya-commercial-2026-05-22", keys=["prices"])],
        usage=_usage(),
    )

    validate_structured_output(output)


def test_price_claim_without_source_is_blocked():
    output = AgentOutput(
        messages=[
            AgentMessage(text="O plano custa R$ 197/mes.", channel_hint="widget", requires_product_source=True)
        ],
        usage=_usage(),
    )

    with pytest.raises(OutputValidationError) as exc:
        validate_structured_output(output)

    assert exc.value.code == "missing_product_source"


def test_completed_diagnostic_requires_evidence():
    output = AgentOutput(
        messages=[AgentMessage(text="Seu gargalo parece ser agenda.", channel_hint="widget")],
        diagnostic=DiagnosticOutput(status="completed", main_bottleneck="agenda", confidence="medium"),
        usage=_usage(),
    )

    with pytest.raises(OutputValidationError) as exc:
        validate_structured_output(output)

    assert exc.value.code == "diagnostic_without_evidence"


def test_handoff_active_blocks_messages():
    output = AgentOutput.model_validate(
        {
            "messages": [{"text": "Vou seguir respondendo.", "channel_hint": "whatsapp"}],
            "handoff": {"status": "active", "reason": "manual_whatsapp_reply_detected"},
            "usage": {"model": None, "input_tokens": 0, "output_tokens": 0, "cost_usd": 0},
        }
    )

    with pytest.raises(OutputValidationError) as exc:
        validate_structured_output(output)

    assert exc.value.code == "human_active_with_messages"


def test_invalid_confidence_value_fails_schema():
    with pytest.raises(ValidationError):
        AgentOutput.model_validate(
            {
                "messages": [{"text": "Oi", "channel_hint": "widget"}],
                "confidence": "certain",
                "usage": {"model": "gpt-5.2", "input_tokens": 1, "output_tokens": 1, "cost_usd": 0},
            }
        )


def test_structured_output_carries_behavior_decision():
    output = AgentOutput(
        decision=RuntimeDecision(
            route="diagnostic",
            opening_type="diagnostic_cta_opening",
            detected_intents=["diagnostic_request"],
            diagnostic_action="ask_next",
            diagnostic_allowed_now=True,
            next_question_kind="pain",
        ),
        messages=[AgentMessage(text="Claro. Qual e hoje a maior dificuldade do studio?", channel_hint="widget")],
        diagnostic=DiagnosticOutput(status="insufficient_evidence", next_question="Qual e hoje a maior dificuldade?"),
        usage=_usage(),
    )

    assert output.decision.route == "diagnostic"
    assert output.decision.diagnostic_allowed_now is True
    assert output.decision.next_question_kind == "pain"
