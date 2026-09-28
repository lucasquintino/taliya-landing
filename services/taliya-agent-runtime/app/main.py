from __future__ import annotations

import json
import os
from datetime import timedelta
from importlib.metadata import PackageNotFoundError, version
from typing import Any
from uuid import uuid4

import psycopg
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.auth.hmac import HmacAuthError, verify_hmac_headers
from app.core.taliya_commercial_sdk.action_agents import (
    ACTION_MODEL_REASONING_EFFORT,
)
from app.core.taliya_commercial_sdk.runtime_adapter import (
    ActionFirstRuntimeBlocked,
    run_action_first_agent_turn,
)
from app.runtime.events import RuntimeEvent
from app.runtime.registry import AgentRegistryError, build_default_registry
from app.runtime.schemas import (
    COMMERCIAL_OPS_CONTRACT_VERSION,
    AgentOutput,
    AgentRunRequest,
    AgentRunResponse,
    HandoffOutput,
    RuntimeDecision,
    Usage,
)
from app.settings import RuntimeSettingsError, get_settings, validate_production_settings
from app.shared.memory.postgres import RuntimeState, create_memory_store

app = FastAPI(title="Taliya Agent Runtime", version="0.1.0")
registry = build_default_registry()
settings = get_settings()
memory_store = create_memory_store(settings.database_url)

TALIYA_COMMERCIAL_AGENT_KEY = "taliya_commercial"
TALIYA_HANDOFF_AGENT = "taliya_commercial_handoff_agent"


def _installed_version(distribution: str) -> str:
    try:
        return version(distribution)
    except PackageNotFoundError:  # pragma: no cover - stripped build environment
        return "unavailable"


def _health_metadata(current) -> dict[str, str]:
    return {
        "build_sha": os.getenv("TALIYA_AGENT_BUILD_SHA")
        or os.getenv("RAILWAY_GIT_COMMIT_SHA")
        or "unavailable",
        "contract_version": COMMERCIAL_OPS_CONTRACT_VERSION,
        "model": current.model,
        "reasoning_effort": ACTION_MODEL_REASONING_EFFORT,
        "openai_sdk_version": _installed_version("openai"),
        "agents_sdk_version": _installed_version("openai-agents"),
    }


def _error(code: str, message: str, *, status_code: int, retryable: bool = False) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message, "retryable": retryable}},
    )


def _database_unavailable_error() -> JSONResponse:
    return _error(
        "runtime_database_unavailable",
        "Runtime database is temporarily unavailable.",
        status_code=503,
        retryable=True,
    )


def _runtime_control(payload: AgentRunRequest) -> dict[str, Any] | None:
    control = payload.metadata.get("runtime_control")
    if not isinstance(control, dict):
        return None
    action = control.get("action")
    if action not in {"pause_human", "resume_human"}:
        return None
    return control


def _previous_state_value(previous_state: RuntimeState | None) -> str:
    if previous_state and previous_state.last_decision:
        candidate = previous_state.last_decision.get(
            "next_state"
        ) or previous_state.last_decision.get("current_state")
        if isinstance(candidate, str) and candidate.strip():
            return candidate
    if previous_state and previous_state.human_status == "active":
        return "paused_by_human"
    return "new_lead"


async def _apply_taliya_runtime_control(
    payload: AgentRunRequest, control: dict[str, Any]
) -> AgentRunResponse:
    action = str(control["action"])
    reason = str(control.get("reason") or action)
    previous_state = await memory_store.load_state(
        payload.conversation.conversation_id, payload.agent_key
    )
    previous_state_value = _previous_state_value(previous_state)
    paused = action == "pause_human"
    current_state = "paused_by_human" if paused else previous_state_value
    next_state = "paused_by_human" if paused else "new_lead"
    human_status = "active" if paused else "none"
    trace_id = f"trace_{uuid4().hex}"
    run_id = f"run_{uuid4().hex}"

    decision = RuntimeDecision(
        previous_state=previous_state_value,
        current_state=current_state,
        next_state=next_state,
        route="handoff",
        opening_type="none",
        detected_intents=[],
        direct_question_present=False,
        direct_question_answered_first=True,
        diagnostic_action="none",
        diagnostic_allowed_now=False,
        waitlist_allowed_now=False,
        template_ids=[],
        template_variables={},
        render_plan=[],
    )
    output = AgentOutput(
        decision=decision,
        messages=[],
        handoff=HandoffOutput(status="active" if paused else "resumed", reason=reason),
        safety_flags=[f"runtime_control:{action}"],
        usage=Usage(model=None, input_tokens=0, output_tokens=0, cost_usd=0),
        confidence="high",
    )
    input_items = previous_state.input_items if previous_state else []
    state = RuntimeState(
        conversation_id=payload.conversation.conversation_id,
        agent_key=payload.agent_key,
        current_agent_name=TALIYA_HANDOFF_AGENT,
        input_items=[
            *input_items,
            {
                "role": "operator_control",
                "content": action,
                "id": payload.message.idempotency_key,
            },
        ],
        summary=previous_state.summary if previous_state else None,
        lead_facts=previous_state.lead_facts if previous_state else [],
        diagnostic=previous_state.diagnostic if previous_state else None,
        demo=previous_state.demo if previous_state else None,
        waitlist=previous_state.waitlist if previous_state else None,
        human_status=human_status,
        human_reason=reason if paused else None,
        last_decision=decision.model_dump(mode="json"),
        last_route=decision.route,
        last_opening_type=decision.opening_type,
        asked_questions=previous_state.asked_questions if previous_state else [],
        answered_direct_questions=previous_state.answered_direct_questions
        if previous_state
        else [],
        profile_name_status=previous_state.profile_name_status if previous_state else None,
        product_source_version=previous_state.product_source_version if previous_state else None,
        cost_usd=previous_state.cost_usd if previous_state else 0,
    )
    await memory_store.save_state(state)
    await memory_store.set_human_status(
        payload.conversation.conversation_id, human_status, reason if paused else None
    )
    await memory_store.record_event(
        RuntimeEvent(
            run_id=run_id,
            conversation_id=payload.conversation.conversation_id,
            agent_key=payload.agent_key,
            type="handoff",
            agent=TALIYA_HANDOFF_AGENT,
            content=action,
            metadata={
                "reason": reason,
                "actor_user_id": control.get("actor_user_id"),
                "source": "runtime_control",
            },
        )
    )
    return AgentRunResponse(
        run_id=run_id,
        conversation_id=payload.conversation.conversation_id,
        lead_id=payload.conversation.lead_id,
        agent_key=payload.agent_key,
        current_agent=TALIYA_HANDOFF_AGENT,
        status="human_paused" if paused else "succeeded",
        output=output,
        trace_id=trace_id,
    )


@app.get("/healthz")
async def healthz():
    current = get_settings()
    try:
        validate_production_settings(current)
    except RuntimeSettingsError as exc:
        return JSONResponse(
            status_code=503,
            content={
                "ok": False,
                "service": "taliya-agent-runtime",
                "environment": current.environment,
                **_health_metadata(current),
                "error": {"code": "runtime_misconfigured", "details": exc.errors},
            },
        )
    return {
        "ok": True,
        "service": "taliya-agent-runtime",
        "environment": current.environment,
        **_health_metadata(current),
    }


@app.post("/v1/agent-runs")
async def agent_runs(request: Request):
    current = get_settings()
    try:
        validate_production_settings(current)
    except RuntimeSettingsError:
        return _error(
            "runtime_misconfigured",
            "Runtime production configuration is incomplete.",
            status_code=503,
            retryable=True,
        )

    raw_body = await request.body()
    try:
        verified = verify_hmac_headers(
            body=raw_body,
            headers=dict(request.headers),
            secret=current.hmac_secret,
            max_skew=timedelta(seconds=current.hmac_max_skew_seconds),
        )
    except HmacAuthError as exc:
        status_code = 401 if exc.code == "invalid_signature" else 400
        return _error(exc.code, exc.message, status_code=status_code)

    try:
        existing = await memory_store.get_idempotent_result(verified.request_id)
    except psycopg.Error:
        return _database_unavailable_error()
    if existing is not None:
        if isinstance(existing, AgentRunResponse):
            return existing.model_dump(mode="json")
        return existing

    try:
        payload = AgentRunRequest.model_validate(json.loads(raw_body.decode("utf-8")))
    except (UnicodeDecodeError, json.JSONDecodeError, ValidationError) as exc:
        return _error("malformed_request", str(exc), status_code=400)

    try:
        registry.get_active(payload.agent_key)
    except AgentRegistryError as exc:
        status = 404 if exc.code in {"unknown_agent_key", "disabled_agent_key"} else 400
        return _error(exc.code, exc.message, status_code=status)

    if payload.agent_key == TALIYA_COMMERCIAL_AGENT_KEY:
        control = _runtime_control(payload)
        if control is None:
            return _error(
                "legacy_commercial_runner_quarantined",
                "Taliya commercial turns must use /v1/taliya-commercial/turn.",
                status_code=410,
            )
        try:
            result = await _apply_taliya_runtime_control(payload, control)
            await memory_store.save_idempotent_result(verified.request_id, result)
        except psycopg.Error:
            return _database_unavailable_error()
        return result.model_dump(mode="json")

    return _error(
        "legacy_agent_runner_unavailable",
        "The legacy agent runner is not available for public commercial turns.",
        status_code=410,
    )


@app.post("/v1/taliya-commercial/turn")
async def taliya_commercial_turn(request: Request):
    current = get_settings()
    try:
        validate_production_settings(current)
    except RuntimeSettingsError:
        return _error(
            "runtime_misconfigured",
            "Runtime production configuration is incomplete.",
            status_code=503,
            retryable=True,
        )

    raw_body = await request.body()
    try:
        verified = verify_hmac_headers(
            body=raw_body,
            headers=dict(request.headers),
            secret=current.hmac_secret,
            max_skew=timedelta(seconds=current.hmac_max_skew_seconds),
        )
    except HmacAuthError as exc:
        status_code = 401 if exc.code == "invalid_signature" else 400
        return _error(exc.code, exc.message, status_code=status_code)

    try:
        existing = await memory_store.get_idempotent_result(verified.request_id)
    except psycopg.Error:
        return _database_unavailable_error()
    if existing is not None:
        if isinstance(existing, AgentRunResponse):
            return existing.model_dump(mode="json")
        return existing

    try:
        payload = AgentRunRequest.model_validate(json.loads(raw_body.decode("utf-8")))
    except (UnicodeDecodeError, json.JSONDecodeError, ValidationError) as exc:
        return _error("malformed_request", str(exc), status_code=400)

    try:
        registry.get_active(payload.agent_key)
    except AgentRegistryError as exc:
        status = 404 if exc.code in {"unknown_agent_key", "disabled_agent_key"} else 400
        return _error(exc.code, exc.message, status_code=status)

    try:
        result = await run_action_first_agent_turn(
            payload,
            memory_store=memory_store,
            provider=current.provider,
            model=current.model,
            cost_cap_usd=current.hard_cost_cap_usd,
        )
    except ActionFirstRuntimeBlocked as exc:
        return _error(exc.code, exc.message, status_code=503, retryable=True)
    except psycopg.Error:
        return _database_unavailable_error()
    except Exception as exc:  # pragma: no cover - defensive API boundary
        return _error("spec012_action_first_failed", str(exc), status_code=500, retryable=True)

    try:
        await memory_store.save_idempotent_result(verified.request_id, result)
    except psycopg.Error:
        return _database_unavailable_error()
    return result.model_dump(mode="json")
