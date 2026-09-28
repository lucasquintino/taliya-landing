import pytest

from app.domains.taliya_commercial.guardrails import validate_diagnostic_evidence
from app.runtime.runner import run_agent_turn
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import InMemoryMemoryStore

pytestmark = pytest.mark.legacy_runner_reference


def _request(conversation_id: str, text: str) -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {"conversation_id": conversation_id, "source": "pilates_landing"},
            "message": {
                "idempotency_key": f"widget:{conversation_id}:1",
                "type": "text",
                "text": text,
            },
            "sender": {},
            "metadata": {},
        }
    )


@pytest.mark.asyncio
async def test_rich_context_diagnostic_completes_with_evidence_and_persistence():
    store = InMemoryMemoryStore()
    response = await run_agent_turn(
        _request(
            "conv_diag_rich",
            "Tenho 90 alunos, uso planilha e o maior problema e reposicao baguncada. "
            "Quero aliviar agenda primeiro.",
        ),
        memory_store=store,
        provider="mock",
        model="gpt-5.2",
    )
    diagnostics = await store.list_diagnostics("conv_diag_rich")

    assert response.current_agent == "taliya_commercial_diagnostic_agent"
    assert response.output.diagnostic is not None
    assert response.output.diagnostic.status == "completed"
    assert response.output.diagnostic.evidence
    assert response.output.lead_facts
    assert diagnostics[0]["status"] == "completed"


@pytest.mark.asyncio
async def test_thin_context_diagnostic_asks_one_useful_question():
    store = InMemoryMemoryStore()
    response = await run_agent_turn(
        _request("conv_diag_thin", "Quero um diagnostico."),
        memory_store=store,
        provider="mock",
        model="gpt-5.2",
    )

    assert response.output.diagnostic is not None
    assert response.output.diagnostic.status == "insufficient_evidence"
    assert response.output.diagnostic.next_question
    assert "?" in response.output.messages[0].text
    assert "pelo que voce contou" not in response.output.messages[0].text.lower()


def test_diagnostic_evidence_validator_blocks_fake_certainty():
    result = validate_diagnostic_evidence(
        {
            "status": "completed",
            "main_bottleneck": "agenda",
            "evidence": [],
            "facts_used": [],
        }
    )

    assert result.passed is False
    assert result.reason == "completed_diagnostic_without_evidence"
