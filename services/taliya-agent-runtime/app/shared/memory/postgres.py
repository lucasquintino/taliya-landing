from __future__ import annotations

from collections.abc import Awaitable, Callable
from copy import deepcopy
from decimal import Decimal
from typing import Any
from uuid import uuid4

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb
from pydantic import BaseModel, Field

try:
    from psycopg_pool import ConnectionPool
except Exception:  # pragma: no cover - optional runtime optimization
    ConnectionPool = None  # type: ignore[assignment]

from app.runtime.events import RuntimeEvent
from app.runtime.schemas import AgentRunResponse


class RuntimeState(BaseModel):
    conversation_id: str
    agent_key: str
    current_agent_name: str
    lead_id: str | None = None
    channel: str = "widget"
    channel_conversation_id: str | None = None
    source: str | None = None
    entry_intent: str | None = None
    input_items: list[dict[str, Any]] = Field(default_factory=list)
    summary: str | None = None
    lead_facts: list[dict[str, Any]] = Field(default_factory=list)
    diagnostic: dict[str, Any] | None = None
    demo: dict[str, Any] | None = None
    waitlist: dict[str, Any] | None = None
    human_status: str = "none"
    human_reason: str | None = None
    last_decision: dict[str, Any] | None = None
    last_route: str | None = None
    last_opening_type: str | None = None
    asked_questions: list[str] = Field(default_factory=list)
    answered_direct_questions: list[str] = Field(default_factory=list)
    profile_name_status: str | None = None
    product_source_version: str | None = None
    cost_usd: float = 0


class InMemoryMemoryStore:
    def __init__(self) -> None:
        self._idempotency: dict[str, Any] = {}
        self._states: dict[tuple[str, str], RuntimeState] = {}
        self._events: list[RuntimeEvent] = []
        self._tool_calls: dict[str, Any] = {}
        self._tool_call_counts: dict[str, int] = {}
        self._lead_facts: dict[str, list[dict[str, Any]]] = {}
        self._waitlist: dict[str, dict[str, Any]] = {}
        self._diagnostics: dict[str, list[dict[str, Any]]] = {}
        self._handoffs: dict[str, list[dict[str, Any]]] = {}
        self._guardrail_events: dict[str, list[dict[str, Any]]] = {}
        self._tool_summaries: dict[str, list[dict[str, Any]]] = {}
        self._model_usage: dict[str, list[dict[str, Any]]] = {}

    async def get_idempotent_result(self, request_id: str) -> Any | None:
        return deepcopy(self._idempotency.get(request_id))

    async def save_idempotent_result(self, request_id: str, result: Any) -> None:
        self._idempotency[request_id] = deepcopy(result)

    async def load_state(self, conversation_id: str, agent_key: str) -> RuntimeState | None:
        state = self._states.get((conversation_id, agent_key))
        return state.model_copy(deep=True) if state else None

    async def save_state(self, state: RuntimeState) -> None:
        self._states[(state.conversation_id, state.agent_key)] = state.model_copy(deep=True)

    async def record_event(self, event: RuntimeEvent) -> None:
        self._events.append(event.model_copy(deep=True))

    async def list_events(self, conversation_id: str) -> list[RuntimeEvent]:
        return [
            event.model_copy(deep=True)
            for event in self._events
            if event.conversation_id == conversation_id
        ]

    async def run_idempotent_tool(
        self,
        idempotency_key: str,
        action: Callable[[], Awaitable[Any]],
    ) -> Any:
        if idempotency_key in self._tool_calls:
            return deepcopy(self._tool_calls[idempotency_key])
        result = await action()
        self._tool_calls[idempotency_key] = deepcopy(result)
        self._tool_call_counts[idempotency_key] = self._tool_call_counts.get(idempotency_key, 0) + 1
        return deepcopy(result)

    async def count_tool_calls(self, idempotency_key: str) -> int:
        return self._tool_call_counts.get(idempotency_key, 0)

    async def append_lead_facts(self, conversation_id: str, facts: list[dict[str, Any]]) -> None:
        bucket = self._lead_facts.setdefault(conversation_id, [])
        seen = {(fact.get("key"), fact.get("value")) for fact in bucket}
        for fact in facts:
            key = (fact.get("key"), fact.get("value"))
            if key not in seen:
                bucket.append(deepcopy(fact))
                seen.add(key)

    async def list_lead_facts(self, conversation_id: str) -> list[dict[str, Any]]:
        return deepcopy(self._lead_facts.get(conversation_id, []))

    async def save_diagnostic(self, conversation_id: str, diagnostic: dict[str, Any]) -> None:
        self._diagnostics.setdefault(conversation_id, []).append(deepcopy(diagnostic))

    async def list_diagnostics(self, conversation_id: str) -> list[dict[str, Any]]:
        return deepcopy(self._diagnostics.get(conversation_id, []))

    async def set_waitlist(self, conversation_id: str, data: dict[str, Any]) -> None:
        self._waitlist[conversation_id] = deepcopy(data)

    async def get_waitlist(self, conversation_id: str) -> dict[str, Any] | None:
        return deepcopy(self._waitlist.get(conversation_id))

    async def set_human_status(
        self,
        conversation_id: str,
        status: str,
        reason: str | None = None,
    ) -> None:
        self._handoffs.setdefault(conversation_id, []).append(
            {
                "status": status,
                "reason": reason,
            }
        )

    async def list_handoffs(self, conversation_id: str) -> list[dict[str, Any]]:
        return deepcopy(self._handoffs.get(conversation_id, []))

    async def record_guardrail_event(self, conversation_id: str, event: dict[str, Any]) -> None:
        self._guardrail_events.setdefault(conversation_id, []).append(deepcopy(event))

    async def list_guardrail_events(self, conversation_id: str) -> list[dict[str, Any]]:
        return deepcopy(self._guardrail_events.get(conversation_id, []))

    async def record_tool_summary(self, conversation_id: str, summary: dict[str, Any]) -> None:
        self._tool_summaries.setdefault(conversation_id, []).append(deepcopy(summary))

    async def list_tool_summaries(self, conversation_id: str) -> list[dict[str, Any]]:
        return deepcopy(self._tool_summaries.get(conversation_id, []))

    async def record_model_usage(self, conversation_id: str, usage: dict[str, Any]) -> None:
        self._model_usage.setdefault(conversation_id, []).append(deepcopy(usage))

    async def list_model_usage(self, conversation_id: str) -> list[dict[str, Any]]:
        return deepcopy(self._model_usage.get(conversation_id, []))


class PostgresMemoryStore(InMemoryMemoryStore):
    """Postgres-backed runtime store with an in-process mirror for local inspection."""

    DEFAULT_AGENT_KEY = "taliya_commercial"
    DEFAULT_AGENT_FAMILY = "taliya"
    DEFAULT_OWNER_SCOPE = "taliya"

    def __init__(
        self,
        database_url: str | None = None,
        connect_factory: Callable[[], Any] | None = None,
    ) -> None:
        super().__init__()
        self.database_url = database_url
        self._connect_factory = connect_factory
        self._pool: Any | None = None

    def _connect(self) -> Any:
        if self._connect_factory:
            return self._connect_factory()
        if not self.database_url:
            raise RuntimeError("PostgresMemoryStore requires a database_url.")
        if ConnectionPool is not None:
            if self._pool is None:
                pool_options: dict[str, Any] = {
                    "conninfo": self.database_url,
                    "kwargs": {"row_factory": dict_row, "prepare_threshold": None},
                    "min_size": 0,
                    "max_size": 5,
                    "max_idle": 60,
                    "max_lifetime": 900,
                    "open": True,
                }
                check_connection = getattr(ConnectionPool, "check_connection", None)
                if check_connection is not None:
                    pool_options["check"] = check_connection
                self._pool = ConnectionPool(
                    **pool_options,
                )
            return self._pool.connection()
        return psycopg.connect(self.database_url, row_factory=dict_row, prepare_threshold=None)

    @staticmethod
    def _plain(value: Any) -> Any:
        if isinstance(value, BaseModel):
            return value.model_dump(mode="json")
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, dict):
            return {str(key): PostgresMemoryStore._plain(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [PostgresMemoryStore._plain(item) for item in value]
        return deepcopy(value)

    @staticmethod
    def _json(value: Any) -> Jsonb:
        return Jsonb(PostgresMemoryStore._plain(value))

    @staticmethod
    def _state_meta(state: RuntimeState) -> dict[str, Any]:
        return {
            "lead_id": state.lead_id,
            "channel": state.channel,
            "channel_conversation_id": state.channel_conversation_id,
            "source": state.source,
            "entry_intent": state.entry_intent,
            "human_reason": state.human_reason,
            "last_decision": state.last_decision,
            "last_route": state.last_route,
            "last_opening_type": state.last_opening_type,
            "asked_questions": state.asked_questions,
            "answered_direct_questions": state.answered_direct_questions,
            "profile_name_status": state.profile_name_status,
            "demo": state.demo,
        }

    @staticmethod
    def _runtime_state_from_row(row: dict[str, Any]) -> RuntimeState:
        meta = row.get("runtime_meta") or {}
        return RuntimeState(
            conversation_id=row["conversation_id"],
            agent_key=row["agent_key"],
            current_agent_name=row["current_agent_name"],
            lead_id=meta.get("lead_id"),
            channel=meta.get("channel") or "widget",
            channel_conversation_id=meta.get("channel_conversation_id"),
            source=meta.get("source"),
            entry_intent=meta.get("entry_intent"),
            input_items=PostgresMemoryStore._plain(row.get("input_items") or []),
            summary=row.get("compact_summary"),
            lead_facts=PostgresMemoryStore._plain(row.get("lead_facts") or []),
            diagnostic=PostgresMemoryStore._plain(row.get("diagnostic")),
            demo=PostgresMemoryStore._plain(meta.get("demo")),
            waitlist=PostgresMemoryStore._plain(row.get("waitlist")),
            human_status=row.get("human_status") or "none",
            human_reason=meta.get("human_reason"),
            last_decision=meta.get("last_decision"),
            last_route=meta.get("last_route"),
            last_opening_type=meta.get("last_opening_type"),
            asked_questions=PostgresMemoryStore._plain(meta.get("asked_questions") or []),
            answered_direct_questions=PostgresMemoryStore._plain(
                meta.get("answered_direct_questions") or []
            ),
            profile_name_status=meta.get("profile_name_status"),
            product_source_version=row.get("product_source_version"),
            cost_usd=float(row.get("cost_usd") or 0),
        )

    def _ensure_agent(self, cur: Any, agent_key: str) -> None:
        cur.execute(
            """
            insert into agent_runtime_agents (
              agent_key, agent_family, owner_scope, enabled, description
            )
            values (%s, %s, %s, true, %s)
            on conflict (agent_key) do update set
              enabled = excluded.enabled,
              updated_at = now()
            """,
            (
                agent_key,
                self.DEFAULT_AGENT_FAMILY,
                self.DEFAULT_OWNER_SCOPE,
                "Taliya commercial sales agent runtime",
            ),
        )

    def _ensure_conversation(
        self,
        cur: Any,
        *,
        conversation_id: str,
        agent_key: str,
        channel: str = "widget",
        lead_id: str | None = None,
        channel_conversation_id: str | None = None,
        source: str | None = None,
        entry_intent: str | None = None,
        current_agent_name: str | None = None,
    ) -> None:
        self._ensure_agent(cur, agent_key)
        cur.execute(
            """
            insert into agent_runtime_conversations (
              id, agent_key, agent_family, owner_scope, lead_id, channel,
              channel_conversation_id, source, entry_intent, current_agent_name
            )
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            on conflict (id) do update set
              agent_key = excluded.agent_key,
              agent_family = excluded.agent_family,
              owner_scope = excluded.owner_scope,
              lead_id = coalesce(excluded.lead_id, agent_runtime_conversations.lead_id),
              channel = excluded.channel,
              channel_conversation_id = coalesce(
                excluded.channel_conversation_id,
                agent_runtime_conversations.channel_conversation_id
              ),
              source = coalesce(excluded.source, agent_runtime_conversations.source),
              entry_intent = coalesce(
                excluded.entry_intent,
                agent_runtime_conversations.entry_intent
              ),
              current_agent_name = coalesce(
                excluded.current_agent_name,
                agent_runtime_conversations.current_agent_name
              ),
              updated_at = now()
            """,
            (
                conversation_id,
                agent_key,
                self.DEFAULT_AGENT_FAMILY,
                self.DEFAULT_OWNER_SCOPE,
                lead_id,
                channel,
                channel_conversation_id,
                source,
                entry_intent,
                current_agent_name,
            ),
        )

    def _fetch_state_row(
        self,
        cur: Any,
        conversation_id: str,
        agent_key: str | None = None,
    ) -> dict[str, Any] | None:
        if agent_key:
            cur.execute(
                """
                select conversation_id, agent_key, current_agent_name, input_items, lead_facts,
                       diagnostic, waitlist, human_status, compact_summary, runtime_meta,
                       product_source_version, cost_usd
                from agent_runtime_state
                where conversation_id = %s and agent_key = %s
                """,
                (conversation_id, agent_key),
            )
        else:
            cur.execute(
                """
                select conversation_id, agent_key, current_agent_name, input_items, lead_facts,
                       diagnostic, waitlist, human_status, compact_summary, runtime_meta,
                       product_source_version, cost_usd
                from agent_runtime_state
                where conversation_id = %s
                order by updated_at desc
                limit 1
                """,
                (conversation_id,),
            )
        return cur.fetchone()

    async def get_idempotent_result(self, request_id: str) -> Any | None:
        cached = await super().get_idempotent_result(request_id)
        if cached is not None:
            return cached
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    select response
                    from agent_runtime_idempotency
                    where request_id = %s
                      and (expires_at is null or expires_at > now())
                    """,
                    (request_id,),
                )
                row = cur.fetchone()
        if not row:
            return None
        return self._plain(row.get("response"))

    async def save_idempotent_result(self, request_id: str, result: Any) -> None:
        await super().save_idempotent_result(request_id, result)
        payload = self._plain(result)
        with self._connect() as conn:
            with conn.cursor() as cur:
                is_run_response = isinstance(result, AgentRunResponse) or (
                    isinstance(payload, dict) and bool(payload.get("run_id"))
                )
                if is_run_response:
                    run_payload = payload
                    input_snapshot = run_payload.get("input_snapshot") or {}
                    self._ensure_conversation(
                        cur,
                        conversation_id=run_payload["conversation_id"],
                        agent_key=run_payload["agent_key"],
                        channel=input_snapshot.get("channel") or "widget",
                        lead_id=run_payload.get("lead_id") or input_snapshot.get("lead_id"),
                        channel_conversation_id=input_snapshot.get("channel_conversation_id"),
                        source=input_snapshot.get("source"),
                        entry_intent=input_snapshot.get("entry_intent"),
                        current_agent_name=run_payload.get("current_agent"),
                    )
                    cur.execute(
                        """
                        insert into agent_runtime_runs (
                          id, conversation_id, agent_key, agent_family, owner_scope, tenant_id,
                          current_agent_name, status, trace_id, input, output
                        )
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        on conflict (id) do update set
                          status = excluded.status,
                          output = excluded.output
                        """,
                        (
                            run_payload["run_id"],
                            run_payload["conversation_id"],
                            run_payload["agent_key"],
                            run_payload.get("agent_family") or self.DEFAULT_AGENT_FAMILY,
                            run_payload.get("owner_scope") or self.DEFAULT_OWNER_SCOPE,
                            run_payload.get("tenant_id"),
                            run_payload.get("current_agent"),
                            run_payload.get("status") or "succeeded",
                            run_payload.get("trace_id") or run_payload["run_id"],
                            self._json(input_snapshot),
                            self._json(run_payload.get("output") or {}),
                        ),
                    )
                cur.execute(
                    """
                    insert into agent_runtime_idempotency (request_id, response, status)
                    values (%s, %s, 'completed')
                    on conflict (request_id) do update set
                      response = excluded.response,
                      status = excluded.status
                    """,
                    (request_id, self._json(payload)),
                )

    async def load_state(self, conversation_id: str, agent_key: str) -> RuntimeState | None:
        with self._connect() as conn:
            with conn.cursor() as cur:
                row = self._fetch_state_row(cur, conversation_id, agent_key)
        if row:
            return self._runtime_state_from_row(row)
        return None

    async def save_state(self, state: RuntimeState) -> None:
        await super().save_state(state)
        with self._connect() as conn:
            with conn.cursor() as cur:
                self._ensure_conversation(
                    cur,
                    conversation_id=state.conversation_id,
                    agent_key=state.agent_key,
                    channel=state.channel,
                    lead_id=state.lead_id,
                    channel_conversation_id=state.channel_conversation_id,
                    source=state.source,
                    entry_intent=state.entry_intent,
                    current_agent_name=state.current_agent_name,
                )
                cur.execute(
                    """
                    insert into agent_runtime_state (
                      conversation_id, agent_key, agent_family, owner_scope, current_agent_name,
                      input_items, lead_facts, diagnostic, waitlist, human_status, compact_summary,
                      runtime_meta, product_source_version, cost_usd
                    )
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    on conflict (conversation_id) do update set
                      agent_key = excluded.agent_key,
                      agent_family = excluded.agent_family,
                      owner_scope = excluded.owner_scope,
                      current_agent_name = excluded.current_agent_name,
                      input_items = excluded.input_items,
                      lead_facts = excluded.lead_facts,
                      diagnostic = excluded.diagnostic,
                      waitlist = excluded.waitlist,
                      human_status = excluded.human_status,
                      compact_summary = excluded.compact_summary,
                      runtime_meta = excluded.runtime_meta,
                      product_source_version = excluded.product_source_version,
                      cost_usd = excluded.cost_usd,
                      updated_at = now()
                    """,
                    (
                        state.conversation_id,
                        state.agent_key,
                        self.DEFAULT_AGENT_FAMILY,
                        self.DEFAULT_OWNER_SCOPE,
                        state.current_agent_name,
                        self._json(state.input_items),
                        self._json(state.lead_facts),
                        self._json(state.diagnostic),
                        self._json(state.waitlist),
                        state.human_status,
                        state.summary,
                        self._json(self._state_meta(state)),
                        state.product_source_version,
                        state.cost_usd,
                    ),
                )
                cur.execute(
                    """
                    update agent_runtime_conversations
                    set current_agent_name = %s,
                        lead_id = coalesce(%s, lead_id),
                        channel = %s,
                        source = coalesce(%s, source),
                        human_status = %s,
                        compact_summary = %s,
                        product_source_version = %s,
                        cost_usd = %s,
                        updated_at = now()
                    where id = %s
                    """,
                    (
                        state.current_agent_name,
                        state.lead_id,
                        state.channel,
                        state.source,
                        state.human_status,
                        state.summary,
                        state.product_source_version,
                        state.cost_usd,
                        state.conversation_id,
                    ),
                )

    async def record_event(self, event: RuntimeEvent) -> None:
        await super().record_event(event)
        payload = self._plain(event)
        with self._connect() as conn:
            with conn.cursor() as cur:
                self._ensure_conversation(
                    cur,
                    conversation_id=event.conversation_id,
                    agent_key=event.agent_key,
                    current_agent_name=event.agent,
                )
                cur.execute(
                    """
                    insert into agent_runtime_messages (
                      conversation_id, run_id, role, channel, idempotency_key, text, payload
                    )
                    values (%s, %s, 'event', 'runtime', %s, %s, %s)
                    on conflict (idempotency_key) do nothing
                    """,
                    (
                        event.conversation_id,
                        event.run_id,
                        event.id,
                        event.content,
                        self._json(payload),
                    ),
                )

    async def list_events(self, conversation_id: str) -> list[RuntimeEvent]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    select payload
                    from agent_runtime_messages
                    where conversation_id = %s and role = 'event'
                    order by id asc
                    """,
                    (conversation_id,),
                )
                rows = cur.fetchall()
        if rows:
            return [RuntimeEvent.model_validate(self._plain(row["payload"])) for row in rows]
        return await super().list_events(conversation_id)

    async def run_idempotent_tool(
        self,
        idempotency_key: str,
        action: Callable[[], Awaitable[Any]],
    ) -> Any:
        if idempotency_key in self._tool_calls:
            return deepcopy(self._tool_calls[idempotency_key])
        existing = await self.get_idempotent_result(idempotency_key)
        if existing is not None:
            return existing
        result = await action()
        await super().run_idempotent_tool(idempotency_key, lambda: _ready(result))
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    insert into agent_runtime_idempotency (request_id, response, status)
                    values (%s, %s, 'completed')
                    on conflict (request_id) do update set
                      response = excluded.response,
                      status = excluded.status
                    """,
                    (idempotency_key, self._json(result)),
                )
        return self._plain(result)

    async def append_lead_facts(self, conversation_id: str, facts: list[dict[str, Any]]) -> None:
        await super().append_lead_facts(conversation_id, facts)
        with self._connect() as conn:
            with conn.cursor() as cur:
                row = self._fetch_state_row(cur, conversation_id)
                if row:
                    state = self._runtime_state_from_row(row)
                else:
                    state = RuntimeState(
                        conversation_id=conversation_id,
                        agent_key=self.DEFAULT_AGENT_KEY,
                        current_agent_name="taliya_commercial_entry_agent",
                    )
                bucket = state.lead_facts
                seen = {(fact.get("key"), fact.get("value")) for fact in bucket}
                for fact in facts:
                    key = (fact.get("key"), fact.get("value"))
                    if key not in seen:
                        bucket.append(deepcopy(fact))
                        seen.add(key)
                state.lead_facts = bucket
        await self.save_state(state)

    async def list_lead_facts(self, conversation_id: str) -> list[dict[str, Any]]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                row = self._fetch_state_row(cur, conversation_id)
        if row:
            return self._plain(row.get("lead_facts") or [])
        return await super().list_lead_facts(conversation_id)

    async def save_diagnostic(self, conversation_id: str, diagnostic: dict[str, Any]) -> None:
        await super().save_diagnostic(conversation_id, diagnostic)
        state = await self._load_or_default_state(
            conversation_id,
            "taliya_commercial_diagnostic_agent",
        )
        state.diagnostic = self._plain(diagnostic)
        await self.save_state(state)

    async def list_diagnostics(self, conversation_id: str) -> list[dict[str, Any]]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                row = self._fetch_state_row(cur, conversation_id)
        if row and row.get("diagnostic"):
            return [self._plain(row["diagnostic"])]
        return await super().list_diagnostics(conversation_id)

    async def set_waitlist(self, conversation_id: str, data: dict[str, Any]) -> None:
        await super().set_waitlist(conversation_id, data)
        state = await self._load_or_default_state(
            conversation_id,
            "taliya_commercial_waitlist_agent",
        )
        state.waitlist = self._plain(data)
        await self.save_state(state)

    async def get_waitlist(self, conversation_id: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            with conn.cursor() as cur:
                row = self._fetch_state_row(cur, conversation_id)
        if row and row.get("waitlist"):
            return self._plain(row["waitlist"])
        return await super().get_waitlist(conversation_id)

    async def set_human_status(
        self,
        conversation_id: str,
        status: str,
        reason: str | None = None,
    ) -> None:
        await super().set_human_status(conversation_id, status, reason)
        state = await self._load_or_default_state(
            conversation_id,
            "taliya_commercial_handoff_agent",
        )
        state.human_status = status
        state.human_reason = reason
        await self.save_state(state)
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    insert into agent_runtime_handoffs (
                      conversation_id, run_id, agent_key, agent_family, owner_scope,
                      handoff_type, reason, status
                    )
                    values (%s, %s, %s, %s, %s, 'human', %s, %s)
                    """,
                    (
                        conversation_id,
                        f"handoff_{uuid4().hex}",
                        state.agent_key,
                        self.DEFAULT_AGENT_FAMILY,
                        self.DEFAULT_OWNER_SCOPE,
                        reason,
                        status,
                    ),
                )

    async def list_handoffs(self, conversation_id: str) -> list[dict[str, Any]]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    select status, reason
                    from agent_runtime_handoffs
                    where conversation_id = %s
                    order by id asc
                    """,
                    (conversation_id,),
                )
                rows = cur.fetchall()
        if rows:
            return [self._plain(dict(row)) for row in rows]
        return await super().list_handoffs(conversation_id)

    async def record_guardrail_event(self, conversation_id: str, event: dict[str, Any]) -> None:
        await super().record_guardrail_event(conversation_id, event)
        payload = self._plain(event)
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    insert into agent_runtime_guardrail_events (
                      conversation_id, run_id, agent_key, agent_family, owner_scope,
                      name, phase, status, reason, blocked, repaired, metadata
                    )
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        conversation_id,
                        payload.get("run_id") or f"guardrail_{uuid4().hex}",
                        payload.get("agent_key") or self.DEFAULT_AGENT_KEY,
                        self.DEFAULT_AGENT_FAMILY,
                        self.DEFAULT_OWNER_SCOPE,
                        payload.get("name") or "runtime_guardrail",
                        payload.get("phase") or "output",
                        payload.get("status") or "observed",
                        payload.get("reason"),
                        bool(payload.get("blocked") or False),
                        bool(payload.get("repaired") or False),
                        self._json(payload),
                    ),
                )

    async def list_guardrail_events(self, conversation_id: str) -> list[dict[str, Any]]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    select metadata
                    from agent_runtime_guardrail_events
                    where conversation_id = %s
                    order by id asc
                    """,
                    (conversation_id,),
                )
                rows = cur.fetchall()
        if rows:
            return [self._plain(row["metadata"]) for row in rows]
        return await super().list_guardrail_events(conversation_id)

    async def record_tool_summary(self, conversation_id: str, summary: dict[str, Any]) -> None:
        await super().record_tool_summary(conversation_id, summary)
        payload = self._plain(summary)
        tool_name = payload.get("tool_name") or payload.get("name") or "runtime_tool"
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    insert into agent_runtime_tool_calls (
                      conversation_id, run_id, agent_key, agent_family, owner_scope,
                      tool_name, idempotency_key, input, output
                    )
                    values (%s, %s, %s, %s, %s, %s, %s, '{}'::jsonb, %s)
                    on conflict (idempotency_key) do nothing
                    """,
                    (
                        conversation_id,
                        payload.get("run_id") or f"tool_{uuid4().hex}",
                        payload.get("agent_key") or self.DEFAULT_AGENT_KEY,
                        self.DEFAULT_AGENT_FAMILY,
                        self.DEFAULT_OWNER_SCOPE,
                        tool_name,
                        payload.get("idempotency_key")
                        or f"{conversation_id}:{tool_name}:{uuid4().hex}",
                        self._json(payload),
                    ),
                )

    async def list_tool_summaries(self, conversation_id: str) -> list[dict[str, Any]]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    select output
                    from agent_runtime_tool_calls
                    where conversation_id = %s
                    order by id asc
                    """,
                    (conversation_id,),
                )
                rows = cur.fetchall()
        if rows:
            return [self._plain(row["output"]) for row in rows]
        return await super().list_tool_summaries(conversation_id)

    async def record_model_usage(self, conversation_id: str, usage: dict[str, Any]) -> None:
        await super().record_model_usage(conversation_id, usage)
        payload = self._plain(usage)
        with self._connect() as conn:
            with conn.cursor() as cur:
                agent_key = payload.get("agent_key") or self.DEFAULT_AGENT_KEY
                self._ensure_conversation(
                    cur,
                    conversation_id=conversation_id,
                    agent_key=agent_key,
                )
                cur.execute(
                    """
                    insert into agent_runtime_model_usage (
                      conversation_id, run_id, agent_key, agent_family, owner_scope,
                      model, model_operations, input_tokens, cached_input_tokens,
                      cache_write_input_tokens, output_tokens, reasoning_tokens, repairs,
                      latency_ms, provider, status, cost_usd
                    )
                    values (
                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s, %s, %s
                    )
                    on conflict (run_id) do update set
                      model = excluded.model,
                      model_operations = excluded.model_operations,
                      input_tokens = excluded.input_tokens,
                      cached_input_tokens = excluded.cached_input_tokens,
                      cache_write_input_tokens = excluded.cache_write_input_tokens,
                      output_tokens = excluded.output_tokens,
                      reasoning_tokens = excluded.reasoning_tokens,
                      repairs = excluded.repairs,
                      latency_ms = excluded.latency_ms,
                      provider = excluded.provider,
                      status = excluded.status,
                      cost_usd = excluded.cost_usd
                    """,
                    (
                        conversation_id,
                        payload.get("run_id") or f"usage_{uuid4().hex}",
                        agent_key,
                        self.DEFAULT_AGENT_FAMILY,
                        self.DEFAULT_OWNER_SCOPE,
                        payload.get("model"),
                        int(payload.get("model_operations") or 0),
                        int(payload.get("input_tokens") or 0),
                        int(payload.get("cached_input_tokens") or 0),
                        int(payload.get("cache_write_input_tokens") or 0),
                        int(payload.get("output_tokens") or 0),
                        int(payload.get("reasoning_tokens") or 0),
                        int(payload.get("repairs") or 0),
                        float(payload.get("latency_ms") or 0),
                        payload.get("provider"),
                        payload.get("status") or "succeeded",
                        float(payload.get("cost_usd") or 0),
                    ),
                )

    async def list_model_usage(self, conversation_id: str) -> list[dict[str, Any]]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    select model, input_tokens, output_tokens, cost_usd
                    from agent_runtime_model_usage
                    where conversation_id = %s
                    order by id asc
                    """,
                    (conversation_id,),
                )
                rows = cur.fetchall()
        if rows:
            return [self._plain(dict(row)) for row in rows]
        return await super().list_model_usage(conversation_id)

    async def _load_or_default_state(self, conversation_id: str, agent_name: str) -> RuntimeState:
        with self._connect() as conn:
            with conn.cursor() as cur:
                row = self._fetch_state_row(cur, conversation_id)
        if row:
            return self._runtime_state_from_row(row)
        return RuntimeState(
            conversation_id=conversation_id,
            agent_key=self.DEFAULT_AGENT_KEY,
            current_agent_name=agent_name,
        )


async def _ready(result: Any) -> Any:
    return result


def create_memory_store(database_url: str | None) -> InMemoryMemoryStore:
    if database_url:
        return PostgresMemoryStore(database_url)
    return InMemoryMemoryStore()
