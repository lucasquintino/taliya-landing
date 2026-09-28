import pytest

from app.domains.taliya_commercial.renderer import render_template_plan
from app.runtime.runner import (
    LLMStructuredDraft,
    _apply_decision_contract,
    _enforce_behavior_contract,
    _normalize_draft,
)
from app.runtime.schemas import AgentRunRequest

pytestmark = pytest.mark.legacy_runner_reference


def _widget_empty_request() -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {
                "conversation_id": "conv_widget_empty",
                "lead_id": "lead_widget_empty",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "msg_widget_empty_1",
                "type": "text",
                "text": "",
            },
            "sender": {},
        }
    )


def test_widget_empty_opening_offers_diagnostic_without_lead_capture():
    request = _widget_empty_request()
    draft = _normalize_draft(LLMStructuredDraft(), request, previous_state=None)
    draft = _enforce_behavior_contract(draft, request, previous_state=None)
    draft = _apply_decision_contract(draft, request, previous_state=None)
    messages = render_template_plan(
        draft.decision.template_ids,
        channel=request.channel,
        variables_by_template=draft.decision.template_variables,
    )

    assert draft.current_agent == "taliya_commercial_entry_agent"
    assert draft.decision.route == "entry"
    assert draft.decision.opening_type == "widget_opening"
    assert draft.decision.diagnostic_action == "offer"
    assert draft.decision.diagnostic_allowed_now is True
    assert draft.decision.waitlist_allowed_now is False
    assert draft.diagnostic is not None
    assert draft.diagnostic.status == "offered"
    assert draft.waitlist_action is None
    assert draft.decision.template_ids == ["opening.widget_empty_diagnostic"]
    assert [message.text for message in messages] == [
        "Oi, tudo bem?",
        "Em que posso ajudar?",
        "Se fizer sentido pra você, estamos oferecendo um diagnóstico gratuito "
        "pro seu studio. O que você acha?",
    ]
