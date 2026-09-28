import asyncio
from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.auth.hmac import (
    HMAC_HEADER_REQUEST_ID,
    HMAC_HEADER_SIGNATURE,
    HMAC_HEADER_TIMESTAMP,
    compute_signature,
)
from app.main import app, memory_store
from app.runtime.schemas import (
    AgentOutput,
    AgentRunResponse,
    RuntimeDecision,
    Usage,
)
from app.settings import get_settings


def _signed_headers(
    body: bytes,
    request_id: str = "req_api_1",
    *,
    secret: str = "dev-secret",
) -> dict[str, str]:
    timestamp = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return {
        HMAC_HEADER_TIMESTAMP: timestamp,
        HMAC_HEADER_REQUEST_ID: request_id,
        HMAC_HEADER_SIGNATURE: compute_signature(secret, timestamp, body),
        "content-type": "application/json",
    }


def test_healthz_returns_service_identity(monkeypatch):
    monkeypatch.setenv("TALIYA_AGENT_RUNTIME_ENV", "test")
    monkeypatch.setenv("TALIYA_AGENT_MODEL", "gpt-5.6-luna")
    monkeypatch.setenv("TALIYA_AGENT_BUILD_SHA", "abc1234")
    get_settings.cache_clear()
    client = TestClient(app)

    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["service"] == "taliya-agent-runtime"
    assert response.json()["build_sha"] == "abc1234"
    assert response.json()["contract_version"] == "taliya-commercial-ops.v1"
    assert response.json()["model"] == "gpt-5.6-luna"
    assert response.json()["reasoning_effort"] == "none"
    assert response.json()["openai_sdk_version"]
    assert response.json()["agents_sdk_version"]
    assert "api_key" not in response.json()
    get_settings.cache_clear()


def test_healthz_rejects_incomplete_production_config(monkeypatch):
    monkeypatch.setenv("TALIYA_AGENT_RUNTIME_ENV", "production")
    monkeypatch.setenv("TALIYA_AGENT_PROVIDER", "mock")
    monkeypatch.setenv("TALIYA_AGENT_RUNTIME_HMAC_SECRET", "dev-secret")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    get_settings.cache_clear()
    client = TestClient(app)

    response = client.get("/healthz")

    assert response.status_code == 503
    payload = response.json()
    assert payload["ok"] is False
    assert payload["error"]["code"] == "runtime_misconfigured"
    get_settings.cache_clear()


def test_agent_run_rejects_taliya_commercial_commercial_turn_on_legacy_endpoint(monkeypatch):
    monkeypatch.setenv("TALIYA_AGENT_PROVIDER", "mock")
    client = TestClient(app)
    body = b"""{
      "agent_key":"taliya_commercial",
      "channel":"widget",
      "conversation":{
        "conversation_id":"conv_1",
        "source":"pilates_landing",
        "entry_intent":"price_question"
      },
      "message":{
        "idempotency_key":"widget:conv_1:1",
        "type":"text",
        "text":"quanto custa?",
        "timestamp":"2026-05-22T12:00:00Z"
      },
      "sender":{"name":"Ana"},
      "metadata":{"page_path":"/pilates","provider":"widget"}
    }"""

    response = client.post("/v1/agent-runs", content=body, headers=_signed_headers(body))

    assert response.status_code == 410
    payload = response.json()
    assert payload["error"]["code"] == "legacy_commercial_runner_quarantined"
    assert payload["error"]["retryable"] is False


def test_agent_run_keeps_legacy_endpoint_quarantined(monkeypatch):
    monkeypatch.setenv("TALIYA_AGENT_PROVIDER", "mock")
    get_settings.cache_clear()
    client = TestClient(app)
    body = b"""{
      "agent_key":"taliya_commercial",
      "channel":"widget",
      "conversation":{
        "conversation_id":"conv_rollback_legacy",
        "source":"pilates_landing",
        "entry_intent":"price_question"
      },
      "message":{
        "idempotency_key":"widget:conv_rollback_legacy:1",
        "type":"text",
        "text":"quanto custa?",
        "timestamp":"2026-05-31T12:30:00Z"
      },
      "sender":{"name":"Ana"},
      "metadata":{"page_path":"/pilates","provider":"widget"}
    }"""

    response = client.post(
        "/v1/agent-runs",
        content=body,
        headers=_signed_headers(body, "req_rollback_legacy_quarantine"),
    )

    assert response.status_code == 410
    assert response.json()["error"]["code"] == "legacy_commercial_runner_quarantined"
    get_settings.cache_clear()


def test_public_commercial_turn_routes_only_to_spec012_action_first(monkeypatch):
    import app.main as runtime_main

    async def fake_action_first_turn(payload, **kwargs):  # noqa: ARG001
        return AgentRunResponse(
            run_id="run_spec012_flagged",
            conversation_id=payload.conversation.conversation_id,
            lead_id=payload.conversation.lead_id,
            agent_key=payload.agent_key,
            current_agent="taliya_product_agent",
            status="succeeded",
            output=AgentOutput(
                decision=RuntimeDecision(
                    route="product",
                    template_ids=["product.price_direct"],
                ),
                messages=[],
                usage=Usage(model="mocked-sdk-dry-run", input_tokens=0, output_tokens=0),
                trace_complete=True,
            ),
            trace_id="trace_spec012_flagged",
        )

    monkeypatch.setenv("TALIYA_AGENT_PROVIDER", "mock")
    get_settings.cache_clear()
    monkeypatch.setattr(runtime_main, "run_action_first_agent_turn", fake_action_first_turn)
    client = TestClient(app)
    request_id = "req_spec012_action_first_flag"
    body = b"""{
      "agent_key":"taliya_commercial",
      "channel":"widget",
      "conversation":{
        "conversation_id":"conv_spec012_flag",
        "lead_id":"lead_spec012_flag",
        "source":"pilates_landing",
        "entry_intent":"price_question"
      },
      "message":{
        "idempotency_key":"widget:conv_spec012_flag:1",
        "type":"text",
        "text":"quanto custa?",
        "timestamp":"2026-06-15T12:30:00Z"
      },
      "sender":{"name":"Ana"},
      "metadata":{"page_path":"/pilates","provider":"widget"}
    }"""

    response = client.post(
        "/v1/taliya-commercial/turn",
        content=body,
        headers=_signed_headers(body, request_id),
    )
    repeated = client.post(
        "/v1/taliya-commercial/turn",
        content=body,
        headers=_signed_headers(body, request_id),
    )

    assert response.status_code == 200
    assert response.json()["run_id"] == "run_spec012_flagged"
    assert response.json()["current_agent"] == "taliya_product_agent"
    assert repeated.status_code == 200
    assert repeated.json() == response.json()
    get_settings.cache_clear()


def test_production_routes_commercial_turns_to_spec012_action_first(monkeypatch):
    import app.main as runtime_main

    captured_kwargs = {}

    async def fake_action_first_turn(payload, **kwargs):  # noqa: ARG001
        captured_kwargs.update(kwargs)
        return AgentRunResponse(
            run_id="run_spec012_production",
            conversation_id=payload.conversation.conversation_id,
            lead_id=payload.conversation.lead_id,
            agent_key=payload.agent_key,
            current_agent="taliya_product_agent",
            status="succeeded",
            output=AgentOutput(
                decision=RuntimeDecision(route="product"),
                messages=[],
                usage=Usage(model="gpt-5.4-mini", input_tokens=0, output_tokens=0),
                trace_complete=True,
            ),
            trace_id="trace_spec012_production",
        )

    monkeypatch.setenv("TALIYA_AGENT_RUNTIME_ENV", "production")
    monkeypatch.setenv("TALIYA_AGENT_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("DATABASE_URL", "postgres://user:pass@example.com:5432/db")
    production_secret = "production-secret-with-enough-length"
    monkeypatch.setenv("TALIYA_AGENT_RUNTIME_HMAC_SECRET", production_secret)
    get_settings.cache_clear()
    monkeypatch.setattr(runtime_main, "run_action_first_agent_turn", fake_action_first_turn)
    client = TestClient(app)
    request_id = "req_spec012_production"
    body = b"""{
      "agent_key":"taliya_commercial",
      "channel":"widget",
      "conversation":{
        "conversation_id":"conv_spec012_production",
        "lead_id":"lead_spec012_production",
        "source":"pilates_landing",
        "entry_intent":"price_question"
      },
      "message":{
        "idempotency_key":"widget:conv_spec012_production:1",
        "type":"text",
        "text":"quanto custa?",
        "timestamp":"2026-06-16T12:30:00Z"
      },
      "sender":{"name":"Ana"},
      "metadata":{"page_path":"/pilates","provider":"widget"}
    }"""

    response = client.post(
        "/v1/taliya-commercial/turn",
        content=body,
        headers=_signed_headers(body, request_id, secret=production_secret),
    )

    assert response.status_code == 200
    assert captured_kwargs["provider"] == "openai"
    assert "paid_openai_approved" not in captured_kwargs
    get_settings.cache_clear()


def test_commercial_turn_returns_retryable_database_error(monkeypatch):
    import psycopg

    import app.main as runtime_main

    class BrokenMemoryStore:
        async def get_idempotent_result(self, request_id):  # noqa: ARG002
            raise psycopg.OperationalError("server closed the connection unexpectedly")

    monkeypatch.setenv("TALIYA_AGENT_PROVIDER", "mock")
    get_settings.cache_clear()
    monkeypatch.setattr(runtime_main, "memory_store", BrokenMemoryStore())
    client = TestClient(app)
    body = b"""{
      "agent_key":"taliya_commercial",
      "channel":"widget",
      "conversation":{
        "conversation_id":"conv_db_unavailable",
        "lead_id":"lead_db_unavailable",
        "source":"pilates_landing",
        "entry_intent":"diagnostic"
      },
      "message":{
        "idempotency_key":"widget:conv_db_unavailable:1",
        "type":"text",
        "text":"sim",
        "timestamp":"2026-07-09T12:55:00Z"
      },
      "sender":{},
      "metadata":{"page_path":"/pilates","provider":"widget"}
    }"""

    response = client.post(
        "/v1/taliya-commercial/turn",
        content=body,
        headers=_signed_headers(body, "req_db_unavailable"),
    )

    assert response.status_code == 503
    assert response.json() == {
        "error": {
            "code": "runtime_database_unavailable",
            "message": "Runtime database is temporarily unavailable.",
            "retryable": True,
        }
    }
    get_settings.cache_clear()


def test_agent_run_accepts_taliya_runtime_control_without_commercial_runner(monkeypatch):
    monkeypatch.setenv("TALIYA_AGENT_PROVIDER", "mock")
    client = TestClient(app)
    body = b"""{
      "agent_key":"taliya_commercial",
      "channel":"widget",
      "conversation":{
        "conversation_id":"conv_control_pause",
        "lead_id":"lead_control",
        "source":"sales_inbox_widget_control",
        "entry_intent":"operator_handoff_control"
      },
      "message":{
        "idempotency_key":"runtime-control:lead_control:pause:1",
        "type":"text",
        "text":"operator paused automation",
        "timestamp":"2026-05-22T12:00:00Z"
      },
      "sender":{},
      "metadata":{
        "runtime_control":{
          "action":"pause_human",
          "reason":"operator_pause",
          "actor_user_id":"user_1"
        }
      }
    }"""

    response = client.post(
        "/v1/agent-runs", content=body, headers=_signed_headers(body, "req_control_pause")
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["agent_key"] == "taliya_commercial"
    assert payload["conversation_id"] == "conv_control_pause"
    assert payload["status"] == "human_paused"
    assert payload["current_agent"] == "taliya_commercial_handoff_agent"
    assert payload["output"]["messages"] == []
    assert payload["output"]["usage"]["input_tokens"] == 0
    assert payload["output"]["handoff"]["status"] == "active"

    state = asyncio.run(memory_store.load_state("conv_control_pause", "taliya_commercial"))
    assert state is not None
    assert state.human_status == "active"
    assert state.human_reason == "operator_pause"


def test_agent_run_rejects_unknown_agent_key_before_runner(monkeypatch):
    monkeypatch.setenv("TALIYA_AGENT_PROVIDER", "mock")
    client = TestClient(app)
    body = b"""{
      "agent_key":"studio_configuration",
      "channel":"widget",
      "conversation":{"conversation_id":"conv_unknown","source":"pilates_landing"},
      "message":{"idempotency_key":"widget:conv_unknown:1","type":"text","text":"oi","timestamp":"2026-05-22T12:00:00Z"},
      "sender":{},
      "metadata":{}
    }"""

    response = client.post(
        "/v1/agent-runs", content=body, headers=_signed_headers(body, "req_unknown")
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "disabled_agent_key"


def test_agent_run_rejects_invalid_hmac():
    client = TestClient(app)
    body = b'{"agent_key":"taliya_commercial"}'
    timestamp = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    headers = {
        HMAC_HEADER_TIMESTAMP: timestamp,
        HMAC_HEADER_REQUEST_ID: "req_invalid",
        HMAC_HEADER_SIGNATURE: "bad",
        "content-type": "application/json",
    }

    response = client.post("/v1/agent-runs", content=body, headers=headers)

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "invalid_signature"


def test_agent_run_rejects_incomplete_production_config_without_idempotent_side_effect(monkeypatch):
    monkeypatch.setenv("TALIYA_AGENT_RUNTIME_ENV", "production")
    monkeypatch.setenv("TALIYA_AGENT_PROVIDER", "mock")
    monkeypatch.setenv("TALIYA_AGENT_RUNTIME_HMAC_SECRET", "dev-secret")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    get_settings.cache_clear()
    client = TestClient(app)
    request_id = "req_misconfigured_prod"
    body = b"""{
      "agent_key":"taliya_commercial",
      "channel":"widget",
      "conversation":{"conversation_id":"conv_misconfigured","source":"pilates_landing"},
      "message":{"idempotency_key":"widget:conv_misconfigured:1","type":"text","text":"oi","timestamp":"2026-05-22T12:00:00Z"},
      "sender":{},
      "metadata":{}
    }"""

    response = client.post(
        "/v1/agent-runs", content=body, headers=_signed_headers(body, request_id)
    )

    assert response.status_code == 503
    payload = response.json()
    assert payload["error"]["code"] == "runtime_misconfigured"
    assert asyncio.run(memory_store.get_idempotent_result(request_id)) is None
    get_settings.cache_clear()
