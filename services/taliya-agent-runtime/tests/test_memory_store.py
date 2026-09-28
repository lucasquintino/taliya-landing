import pytest

from app.runtime.events import RuntimeEvent
from app.runtime.schemas import AgentOutput, AgentRunResponse, RuntimeInputSnapshot, Usage
from app.shared.memory.postgres import InMemoryMemoryStore, PostgresMemoryStore, RuntimeState


class RecordingCursor:
    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def execute(self, query, params=None):
        self.connection.queries.append((query, params or ()))

    def fetchone(self):
        if self.connection.fetchone_rows:
            return self.connection.fetchone_rows.pop(0)
        return None

    def fetchall(self):
        if self.connection.fetchall_rows:
            return self.connection.fetchall_rows.pop(0)
        return []


class RecordingConnection:
    def __init__(self):
        self.queries = []
        self.fetchone_rows = []
        self.fetchall_rows = []

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def cursor(self):
        return RecordingCursor(self)


@pytest.mark.asyncio
async def test_memory_store_persists_and_returns_idempotent_result():
    store = InMemoryMemoryStore()
    output = AgentOutput(
        messages=[],
        usage=Usage(model=None, input_tokens=0, output_tokens=0, cost_usd=0),
    )

    await store.save_idempotent_result("req_1", output)
    again = await store.get_idempotent_result("req_1")

    assert again == output


@pytest.mark.asyncio
async def test_memory_store_round_trips_runtime_state():
    store = InMemoryMemoryStore()
    state = RuntimeState(
        conversation_id="conv_1",
        agent_key="taliya_commercial",
        current_agent_name="taliya_commercial_triage",
        input_items=[{"role": "user", "content": "oi"}],
        summary="lead asked about price",
    )

    await store.save_state(state)
    loaded = await store.load_state("conv_1", "taliya_commercial")

    assert loaded is not None
    assert loaded.current_agent_name == "taliya_commercial_triage"
    assert loaded.input_items[0]["content"] == "oi"


@pytest.mark.asyncio
async def test_memory_store_round_trips_runtime_identity():
    store = InMemoryMemoryStore()
    state = RuntimeState(
        conversation_id="conv_identity",
        agent_key="taliya_commercial",
        current_agent_name="taliya_commercial_entry_agent",
        lead_id="lead_identity",
        channel="whatsapp",
        channel_conversation_id="5511999999999",
        source="instagram",
        entry_intent="price_question",
    )

    await store.save_state(state)
    loaded = await store.load_state("conv_identity", "taliya_commercial")

    assert loaded is not None
    assert loaded.lead_id == "lead_identity"
    assert loaded.channel == "whatsapp"
    assert loaded.channel_conversation_id == "5511999999999"
    assert loaded.source == "instagram"
    assert loaded.entry_intent == "price_question"


@pytest.mark.asyncio
async def test_memory_store_records_runner_events():
    store = InMemoryMemoryStore()
    event = RuntimeEvent(
        run_id="run_1",
        conversation_id="conv_1",
        agent_key="taliya_commercial",
        type="tool_call",
        agent="taliya_commercial_entry_agent",
        content="get_product_knowledge",
    )

    await store.record_event(event)
    events = await store.list_events("conv_1")

    assert len(events) == 1
    assert events[0].type == "tool_call"


@pytest.mark.asyncio
async def test_postgres_store_persists_runtime_state_with_runtime_meta():
    connection = RecordingConnection()
    store = PostgresMemoryStore("postgres://local", connect_factory=lambda: connection)
    state = RuntimeState(
        conversation_id="conv_sql",
        agent_key="taliya_commercial",
        current_agent_name="taliya_commercial_diagnostic_agent",
        input_items=[{"role": "user", "content": "tenho 80 alunos"}],
        lead_facts=[{"key": "active_students", "value": "80"}],
        diagnostic={"status": "in_progress"},
        waitlist={"status": "offered"},
        human_status="none",
        human_reason="operator",
        last_route="diagnostic",
        asked_questions=["pain"],
        answered_direct_questions=["price"],
        profile_name_status="used_reliable_name",
        product_source_version="test-version",
        cost_usd=0.012,
        lead_id="lead_sql",
        channel="whatsapp",
        channel_conversation_id="5511888888888",
        source="instagram",
        entry_intent="demo_request",
    )

    await store.save_state(state)

    executed_sql = "\n".join(query for query, _params in connection.queries)
    assert "insert into agent_runtime_state" in executed_sql
    assert "runtime_meta" in executed_sql
    assert "update agent_runtime_conversations" in executed_sql
    conversation_params = next(
        params
        for query, params in connection.queries
        if "insert into agent_runtime_conversations" in query
    )
    assert conversation_params[4:10] == (
        "lead_sql",
        "whatsapp",
        "5511888888888",
        "instagram",
        "demo_request",
        "taliya_commercial_diagnostic_agent",
    )


@pytest.mark.asyncio
async def test_postgres_store_persists_run_with_real_input_snapshot():
    connection = RecordingConnection()
    store = PostgresMemoryStore("postgres://local", connect_factory=lambda: connection)
    response = AgentRunResponse(
        run_id="run_contract",
        conversation_id="conv_contract",
        lead_id="lead_contract",
        agent_key="taliya_commercial",
        current_agent="taliya_commercial_entry_agent",
        status="succeeded",
        trace_id="trace_contract",
        input_snapshot=RuntimeInputSnapshot(
            channel="widget",
            conversation_id="conv_contract",
            lead_id="lead_contract",
            channel_conversation_id="widget_session_1",
            source="pilates_landing",
            entry_intent="price_question",
            message_id="message_contract",
            channel_message_id="browser_message_1",
            page_path="/pilates",
            source_section="hero",
        ),
        output=AgentOutput(
            messages=[],
            usage=Usage(model="gpt-5.6-luna"),
        ),
    )

    await store.save_idempotent_result("request_contract", response)

    run_params = next(
        params for query, params in connection.queries if "insert into agent_runtime_runs" in query
    )
    assert run_params[0] == "run_contract"
    assert run_params[1] == "conv_contract"
    assert run_params[8] == "trace_contract"
    input_payload = run_params[9].obj
    assert input_payload["contract_version"] == "taliya-commercial-ops.v1"
    assert input_payload["lead_id"] == "lead_contract"
    assert input_payload["source_section"] == "hero"


@pytest.mark.asyncio
async def test_postgres_store_persists_complete_model_usage_with_real_run_id():
    connection = RecordingConnection()
    store = PostgresMemoryStore("postgres://local", connect_factory=lambda: connection)

    await store.record_model_usage(
        "conv_usage",
        {
            "run_id": "run_usage",
            "agent_key": "taliya_commercial",
            "model": "gpt-5.6-luna",
            "model_operations": 2,
            "input_tokens": 120,
            "cached_input_tokens": 40,
            "cache_write_input_tokens": 20,
            "output_tokens": 30,
            "reasoning_tokens": 10,
            "repairs": 1,
            "latency_ms": 321.5,
            "provider": "openai",
            "status": "succeeded",
            "cost_usd": 0.004,
        },
    )

    usage_params = next(
        params
        for query, params in connection.queries
        if "insert into agent_runtime_model_usage" in query
    )
    assert len(usage_params) == 17
    assert usage_params[1] == "run_usage"
    assert usage_params[6:17] == (
        2,
        120,
        40,
        20,
        30,
        10,
        1,
        321.5,
        "openai",
        "succeeded",
        0.004,
    )


@pytest.mark.asyncio
async def test_postgres_store_loads_runtime_state_from_sql_row():
    connection = RecordingConnection()
    connection.fetchone_rows.append(
        {
            "conversation_id": "conv_sql",
            "agent_key": "taliya_commercial",
            "current_agent_name": "taliya_commercial_diagnostic_agent",
            "input_items": [{"role": "user", "content": "tenho 80 alunos"}],
            "lead_facts": [{"key": "active_students", "value": "80"}],
            "diagnostic": {"status": "in_progress"},
            "waitlist": {"status": "offered"},
            "human_status": "active",
            "compact_summary": "lead has capacity pain",
            "runtime_meta": {
                "human_reason": "operator",
                "last_route": "diagnostic",
                "asked_questions": ["pain"],
                "answered_direct_questions": ["price"],
                "profile_name_status": "used_reliable_name",
            },
            "product_source_version": "test-version",
            "cost_usd": 0.012,
        }
    )
    store = PostgresMemoryStore("postgres://local", connect_factory=lambda: connection)

    loaded = await store.load_state("conv_sql", "taliya_commercial")

    assert loaded is not None
    assert loaded.current_agent_name == "taliya_commercial_diagnostic_agent"
    assert loaded.lead_facts[0]["value"] == "80"
    assert loaded.human_reason == "operator"
    assert loaded.answered_direct_questions == ["price"]


@pytest.mark.asyncio
async def test_postgres_store_does_not_resurrect_deleted_state_from_memory_mirror():
    connection = RecordingConnection()
    store = PostgresMemoryStore("postgres://local", connect_factory=lambda: connection)
    state = RuntimeState(
        conversation_id="conv_deleted",
        agent_key="taliya_commercial",
        current_agent_name="taliya_commercial_diagnostic_agent",
        cost_usd=0.15,
    )

    await store.save_state(state)
    loaded = await store.load_state("conv_deleted", "taliya_commercial")

    assert loaded is None


@pytest.mark.asyncio
async def test_postgres_store_persists_tool_idempotency_without_repeating_action():
    connection = RecordingConnection()
    store = PostgresMemoryStore("postgres://local", connect_factory=lambda: connection)
    calls = 0

    async def action():
        nonlocal calls
        calls += 1
        return {"status": "ok"}

    first = await store.run_idempotent_tool("tool:sql", action)
    second = await store.run_idempotent_tool("tool:sql", action)

    executed_sql = "\n".join(query for query, _params in connection.queries)
    assert first == {"status": "ok"}
    assert second == {"status": "ok"}
    assert calls == 1
    assert "insert into agent_runtime_idempotency" in executed_sql

