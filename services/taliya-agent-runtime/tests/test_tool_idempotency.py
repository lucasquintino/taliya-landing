import pytest

from app.domains.taliya_commercial.context import TaliyaCommercialContext
from app.domains.taliya_commercial.tools import mark_waitlist, save_lead_facts
from app.shared.memory.postgres import InMemoryMemoryStore


@pytest.mark.asyncio
async def test_mark_waitlist_is_idempotent_by_key():
    store = InMemoryMemoryStore()
    context = TaliyaCommercialContext(conversation_id="conv_1", lead_id="lead_1", memory_store=store)

    first = await mark_waitlist(
        context,
        idempotency_key="waitlist:conv_1:join",
        status="joined",
        reason="lead asked to join",
        missing_fields=[],
    )
    second = await mark_waitlist(
        context,
        idempotency_key="waitlist:conv_1:join",
        status="joined",
        reason="lead asked to join again",
        missing_fields=[],
    )

    assert first == second
    assert (await store.count_tool_calls("waitlist:conv_1:join")) == 1


@pytest.mark.asyncio
async def test_save_lead_facts_dedupes_repeated_tool_call():
    store = InMemoryMemoryStore()
    context = TaliyaCommercialContext(conversation_id="conv_1", lead_id="lead_1", memory_store=store)
    facts = [{"key": "main_pain", "value": "reposicoes", "confidence": "medium", "evidence": ["msg_1"]}]

    await save_lead_facts(context, idempotency_key="facts:conv_1:msg_1", facts=facts)
    await save_lead_facts(context, idempotency_key="facts:conv_1:msg_1", facts=facts)

    saved = await store.list_lead_facts("conv_1")
    assert len(saved) == 1
    assert saved[0]["key"] == "main_pain"
