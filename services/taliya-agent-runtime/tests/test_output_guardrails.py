import pytest

from app.runtime.schemas import AgentMessage, AgentOutput, DiagnosticOutput, RuntimeDecision, SourceRef, Usage
from app.shared.guardrails.validators import (
    OutputValidationError,
    redact_trace_payload,
    validate_structured_output,
)


def _usage() -> Usage:
    return Usage(model="gpt-5.2", input_tokens=100, output_tokens=40, cost_usd=0.001)


def test_redacts_signatures_secrets_and_system_prompt_text():
    payload = {
        "headers": {"x-taliya-agent-signature": "abc123"},
        "secret": "sk-test-secret",
        "system_prompt": "internal policy",
        "safe": "keep me",
    }

    redacted = redact_trace_payload(payload)

    assert redacted["headers"]["x-taliya-agent-signature"] == "[REDACTED]"
    assert redacted["secret"] == "[REDACTED]"
    assert redacted["system_prompt"] == "[REDACTED]"
    assert redacted["safe"] == "keep me"


def test_blocks_whatsapp_phone_request():
    output = AgentOutput(
        messages=[AgentMessage(text="Qual seu WhatsApp para continuar?", channel_hint="whatsapp")],
        usage=_usage(),
    )

    with pytest.raises(OutputValidationError) as exc:
        validate_structured_output(output, channel="whatsapp")

    assert exc.value.code == "whatsapp_phone_request"


def test_blocks_invented_checkout_link():
    output = AgentOutput(
        messages=[AgentMessage(text="Pode fechar aqui: https://checkout.taliya.com.br/agora", channel_hint="widget")],
        sources=[SourceRef(type="product_knowledge", version="taliya-commercial-2026-05-22", keys=["prices"])],
        usage=_usage(),
    )

    with pytest.raises(OutputValidationError) as exc:
        validate_structured_output(output)

    assert exc.value.code == "invented_checkout"


def test_allows_product_sourced_unavailable_checkout_explanation():
    output = AgentOutput(
        messages=[
            AgentMessage(
                text="Hoje nao tem checkout disponivel; a Taliya esta trabalhando com lista de espera.",
                channel_hint="widget",
            )
        ],
        sources=[
            SourceRef(
                type="product_knowledge",
                version="taliya-commercial-2026-05-22",
                keys=["checkout_status", "waitlist_status"],
            )
        ],
        usage=_usage(),
    )

    validate_structured_output(output)


def test_blocks_evidence_claim_without_evidence():
    output = AgentOutput(
        messages=[AgentMessage(text="Pelo que voce contou, seu maior problema e agenda.", channel_hint="widget")],
        usage=_usage(),
    )

    with pytest.raises(OutputValidationError) as exc:
        validate_structured_output(output)

    assert exc.value.code == "unsupported_evidence_phrase"


def test_blocks_diagnostic_on_cold_greeting_decision():
    output = AgentOutput(
        decision=RuntimeDecision(opening_type="cold_greeting_only"),
        messages=[
            AgentMessage(
                text="Oi, tudo bem? Posso fazer um diagnostico gratuito rapidinho?",
                channel_hint="whatsapp",
            )
        ],
        usage=_usage(),
    )

    with pytest.raises(OutputValidationError) as exc:
        validate_structured_output(output, channel="whatsapp")

    assert exc.value.code == "cold_greeting_diagnostic"


def test_blocks_direct_question_steering_before_answer():
    output = AgentOutput(
        decision=RuntimeDecision(
            route="product",
            direct_question_present=True,
            direct_question_answered_first=False,
        ),
        messages=[AgentMessage(text="Antes de preco, posso fazer um diagnostico.", channel_hint="widget")],
        usage=_usage(),
    )

    with pytest.raises(OutputValidationError) as exc:
        validate_structured_output(output)

    assert exc.value.code == "direct_question_not_answered_first"


def test_allows_completed_diagnostic_memory_on_handoff_pause():
    output = AgentOutput(
        decision=RuntimeDecision(
            route="handoff",
            current_state="human_handoff",
            next_state="paused_by_human",
            diagnostic_action="none",
            diagnostic_allowed_now=False,
            template_ids=["handoff.acknowledge"],
        ),
        diagnostic=DiagnosticOutput(
            status="completed",
            main_bottleneck="interessados sem retorno",
            likely_cause="controle manual",
            first_recommended_step="organizar retornos",
            evidence=["lead tem interessados sem retorno"],
            ledger=[
                {"question_key": key, "status": "answered", "answer_value": "ok", "may_ask_again": False}
                for key in (
                    "active_students_or_size",
                    "main_pain",
                    "pain_detail",
                    "current_process",
                    "priority",
                    "urgency",
                )
            ],
        ),
        messages=[
            AgentMessage(
                text="Claro. Vou deixar uma pessoa assumir daqui.",
                channel_hint="whatsapp",
                template_id="handoff.acknowledge",
            )
        ],
        usage=_usage(),
    )

    validate_structured_output(output, channel="whatsapp")


def test_blocks_technical_language_in_product_followup_for_lay_lead():
    output = AgentOutput(
        decision=RuntimeDecision(
            route="product",
            current_state="product_question",
            template_ids=["product.how_it_works_direct"],
        ),
        messages=[
            AgentMessage(
                text="A Taliya organiza o pipeline do seu studio.",
                channel_hint="widget",
                template_id="product.how_it_works_direct",
                requires_product_source=True,
            )
        ],
        sources=[SourceRef(type="product_knowledge", version="taliya-commercial-2026-05-22", keys=["how_it_works"])],
        usage=_usage(),
    )

    with pytest.raises(OutputValidationError) as exc:
        validate_structured_output(output)

    assert exc.value.code == "technical_language_for_lay_lead"


def test_blocks_crm_in_product_followup_for_lay_lead():
    output = AgentOutput(
        decision=RuntimeDecision(
            route="product",
            current_state="product_question",
            template_ids=["product.comparison_current_tool"],
        ),
        messages=[
            AgentMessage(
                text="A Taliya e um CRM melhor que planilha.",
                channel_hint="widget",
                template_id="product.comparison_current_tool",
                requires_product_source=True,
            )
        ],
        sources=[SourceRef(type="product_knowledge", version="taliya-commercial-2026-05-22", keys=["comparison_spreadsheet"])],
        usage=_usage(),
    )

    with pytest.raises(OutputValidationError) as exc:
        validate_structured_output(output)

    assert exc.value.code == "crm_for_lay_lead"


def test_privacidade_does_not_trigger_early_waitlist_city_capture():
    output = AgentOutput(
        decision=RuntimeDecision(
            route="product",
            current_state="product_question",
            next_state="product_question",
            template_ids=["product.security_data_direct"],
            waitlist_allowed_now=False,
        ),
        messages=[
            AgentMessage(
                text="Sobre seguranca, privacidade ou LGPD, eu prefiro seguir so informacoes oficiais.",
                channel_hint="widget",
                template_id="product.security_data_direct",
                requires_product_source=True,
            )
        ],
        sources=[SourceRef(type="product_knowledge", version="taliya-commercial-2026-05-22", keys=["security_and_data"])],
        usage=_usage(),
    )

    validate_structured_output(output, channel="widget")


def test_rapidinho_does_not_trigger_api_technical_language_guardrail():
    output = AgentOutput(
        decision=RuntimeDecision(
            route="product",
            current_state="product_question",
            next_state="product_question",
            template_ids=["product.out_of_profile_redirect"],
        ),
        messages=[
            AgentMessage(
                text="Se voce e aluno, me conta rapidinho o contexto para eu nao te orientar errado.",
                channel_hint="widget",
                template_id="product.out_of_profile_redirect",
                requires_product_source=True,
            )
        ],
        sources=[SourceRef(type="product_knowledge", version="taliya-commercial-2026-05-22", keys=["out_of_profile"])],
        usage=_usage(),
    )

    validate_structured_output(output, channel="widget")


def test_blocks_internal_agent_text_leak_to_lead():
    output = AgentOutput(
        decision=RuntimeDecision(route="diagnostic", current_state="diagnostic_offered"),
        messages=[
            AgentMessage(
                text="Entendi esse ponto: Lead informou ter 80 alunos.",
                channel_hint="widget",
                template_id=None,
            )
        ],
        usage=_usage(),
    )

    with pytest.raises(OutputValidationError) as exc:
        validate_structured_output(output, channel="widget")

    assert exc.value.code == "internal_text_leak"


def test_blocks_profile_metadata_leak_to_lead():
    output = AgentOutput(
        decision=RuntimeDecision(route="diagnostic", current_state="diagnostic_offered"),
        messages=[
            AgentMessage(
                text="Oi, Lucas, tudo bem? Entendi esse ponto: Reliable profile first name: Lucas.",
                channel_hint="whatsapp",
                template_id=None,
            )
        ],
        usage=_usage(),
    )

    with pytest.raises(OutputValidationError) as exc:
        validate_structured_output(output, channel="whatsapp")

    assert exc.value.code == "internal_text_leak"
