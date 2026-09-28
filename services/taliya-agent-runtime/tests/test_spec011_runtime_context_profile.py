from __future__ import annotations

import json

from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.context_profile import (
    RUNTIME_CORE_PRODUCT_KNOWLEDGE_KEYS,
    RUNTIME_CORE_SPEC006_CONTRACT_KEYS,
    build_runtime_context_profile,
)
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState


def _request(text: str = "Tenho 120 alunos e agenda baguncada") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_budget_1",
                "lead_id": "lead_budget_1",
                "channel_conversation_id": "wa_budget_1",
                "source": "pilates_landing",
                "entry_intent": "diagnostic_requested",
            },
            "message": {
                "idempotency_key": "wa:conv_budget_1:1",
                "channel_message_id": "wamid_budget_1",
                "type": "text",
                "text": text,
                "timestamp": "2026-05-30T12:00:00Z",
            },
            "sender": {"name": "Ana", "whatsapp_phone": "+5511999999999"},
            "metadata": {"page_path": "/pilates", "utm_source": "instagram"},
        }
    )


def _state(*, diagnostic_status: str = "in_progress") -> RuntimeState:
    return RuntimeState(
        conversation_id="conv_budget_1",
        agent_key="taliya_commercial",
        current_agent_name="taliya_commercial_product_agent",
        input_items=[
            {"role": "user", "content": f"Mensagem antiga {index}", "id": f"m{index}"}
            for index in range(10)
        ],
        summary="Lead quer organizar agenda e reposicoes.",
        lead_facts=[
            {
                "key": "active_students_or_size",
                "value": "120",
                "confidence": "high",
                "source": "user_message",
                "reliability": "customer_provided",
                "evidence": ["m9"],
            }
        ],
        diagnostic={
            "status": diagnostic_status,
            "ledger": [
                {
                    "question_key": "active_students_or_size",
                    "status": "answered",
                    "answer_value": "120",
                    "evidence": ["m9"],
                    "confidence": "high",
                    "may_ask_again": False,
                },
                {
                    "question_key": "urgency",
                    "status": "missing",
                    "answer_value": None,
                    "evidence": [],
                    "confidence": "low",
                    "may_ask_again": True,
                },
            ],
        },
        waitlist={"status": "none"},
        demo={"status": "not_offered"},
    )


def _context_json_size(context) -> int:
    return len(
        json.dumps(
            context.model_dump(mode="json"),
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        )
    )


def test_runtime_context_profile_keeps_core_sources_but_not_full_default_pack() -> None:
    profile = build_runtime_context_profile(request=_request(), state=_state())

    assert set(RUNTIME_CORE_PRODUCT_KNOWLEDGE_KEYS).issubset(
        set(profile.product_knowledge_keys)
    )
    assert set(profile.spec006_contract_keys) == set(RUNTIME_CORE_SPEC006_CONTRACT_KEYS)
    assert "comparison_spreadsheet" not in profile.product_knowledge_keys
    assert "security_and_data" not in profile.product_knowledge_keys
    assert "cancellation_or_guarantee_policy" not in profile.product_knowledge_keys
    assert "operating_modes" not in profile.spec006_contract_keys
    assert profile.max_recent_transcript_items == 5


def test_runtime_context_profile_retrieves_extra_official_sources_only_when_needed() -> None:
    profile = build_runtime_context_profile(
        request=_request(
            "Uso planilha hoje, tenho duvida de LGPD e quero saber do setup depois de assinar"
        ),
        state=_state(),
    )

    assert "comparison_spreadsheet" in profile.product_knowledge_keys
    assert "comparison_management_system" in profile.product_knowledge_keys
    assert "privacy_or_data_notes" in profile.product_knowledge_keys
    assert "security_and_data" in profile.product_knowledge_keys
    assert "availability_and_onboarding" in profile.product_knowledge_keys
    assert "setup_scope" in profile.spec006_contract_keys


def test_runtime_context_profile_does_not_create_commercial_decision_fields() -> None:
    profile = build_runtime_context_profile(
        request=_request("Quanto custa e como fica minha agenda?"),
        state=_state(),
    )

    assert not hasattr(profile, "route")
    assert not hasattr(profile, "intent")
    assert not hasattr(profile, "template_id")


def test_runtime_context_uses_compact_prompt_budget_without_losing_diagnostic_ledger() -> None:
    request = _request()
    state = _state()
    profile = build_runtime_context_profile(request=request, state=state)
    default_context = build_turn_context(
        turn_id="turn_default",
        request=request,
        state=state,
        recent_events=[],
    )
    runtime_context = build_turn_context(
        turn_id="turn_runtime",
        request=request,
        state=state,
        recent_events=[],
        max_recent_transcript_items=profile.max_recent_transcript_items,
        product_knowledge_keys=list(profile.product_knowledge_keys),
        spec006_contract_keys=list(profile.spec006_contract_keys),
    )

    assert _context_json_size(runtime_context) < _context_json_size(default_context) * 0.65
    assert len(runtime_context.recent_transcript) == 5
    assert runtime_context.recent_transcript[-1]["content"] == "Mensagem antiga 9"
    assert runtime_context.diagnostic_ledger == default_context.diagnostic_ledger
    assert runtime_context.compact_memory == default_context.compact_memory
    assert runtime_context.sales_inbox_inputs == default_context.sales_inbox_inputs
