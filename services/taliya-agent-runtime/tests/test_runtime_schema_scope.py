from app.runtime.schemas import AgentRunRequest, AgentRunResponse, AgentOutput, Usage


def test_agent_run_request_defaults_to_taliya_scope_without_tenant():
    request = AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {"conversation_id": "conv_scope"},
            "message": {"idempotency_key": "widget:conv_scope:1", "type": "text", "text": "oi"},
            "sender": {},
            "metadata": {},
        }
    )

    assert request.agent_key == "taliya_commercial"
    assert request.agent_family == "taliya"
    assert request.owner_scope == "taliya"
    assert request.tenant_id is None


def test_agent_run_response_exposes_generic_scope_fields():
    response = AgentRunResponse(
        run_id="run_scope",
        conversation_id="conv_scope",
        lead_id=None,
        agent_key="taliya_commercial",
        current_agent="taliya_commercial_triage",
        status="succeeded",
        output=AgentOutput(messages=[], usage=Usage(model=None, input_tokens=0, output_tokens=0, cost_usd=0)),
        trace_id="trace_scope",
    )

    assert response.agent_family == "taliya"
    assert response.owner_scope == "taliya"
    assert response.tenant_id is None

