from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from app.core.taliya_commercial_sdk.output_schema import (
    AgentPathItem,
    TaliyaTurnProposal,
)
from app.core.taliya_commercial_sdk.sdk_output_model import (
    TaliyaSdkTurnOutput,
    sdk_turn_output_to_proposal_fields,
)


class SdkOutputAdapterError(ValueError):
    pass


def adapt_sdk_run_result_to_turn_proposal(
    run_result: Any,
    *,
    turn_id: str,
    conversation_id: str,
    channel: str,
    starting_agent: str,
    usage: dict[str, Any],
) -> TaliyaTurnProposal:
    """Adapt a real Agents SDK RunResult into TaliyaTurnProposal.

    The model only produces `TaliyaSdkTurnOutput` content. Identity fields,
    the agent path (derived from SDK run items), and usage (measured by the
    harness from the runner, never self-reported by the model) are added here.
    Anything that is not the strict structured output is rejected.
    """

    final_output = _extract_final_output(run_result)
    if not isinstance(final_output, TaliyaSdkTurnOutput):
        raise SdkOutputAdapterError("sdk_final_output_must_be_structured_proposal")

    payload = {
        "schema_version": "012.turn_proposal.v1",
        "turn_id": turn_id,
        "conversation_id": conversation_id,
        "channel": channel,
        "starting_agent": starting_agent,
        "agent_path": _agent_path({}, run_result, starting_agent),
        **sdk_turn_output_to_proposal_fields(final_output),
        "usage": usage,
    }
    try:
        return TaliyaTurnProposal.model_validate(payload)
    except ValidationError as exc:
        raise SdkOutputAdapterError(f"sdk_proposal_schema_invalid:{exc}") from exc


def adapt_sdk_output_to_turn_proposal(
    sdk_result: Any,
    *,
    turn_id: str,
    conversation_id: str,
    channel: str,
    starting_agent: str,
) -> TaliyaTurnProposal:
    """Adapt an SDK run result or mocked SDK output into TaliyaTurnProposal.

    This adapter accepts only structured proposal output. Free-form SDK final
    text remains blocked because rendering is owned by the validated Taliya path.
    """

    raw_output = _extract_final_output(sdk_result)
    if isinstance(raw_output, TaliyaTurnProposal):
        return raw_output
    if not isinstance(raw_output, dict):
        raise SdkOutputAdapterError("sdk_final_output_must_be_structured_proposal")

    payload = {
        **raw_output,
        "turn_id": raw_output.get("turn_id") or turn_id,
        "conversation_id": raw_output.get("conversation_id") or conversation_id,
        "channel": raw_output.get("channel") or channel,
        "starting_agent": raw_output.get("starting_agent") or starting_agent,
        "agent_path": _agent_path(raw_output, sdk_result, starting_agent),
    }
    try:
        return TaliyaTurnProposal.model_validate(payload)
    except ValidationError as exc:
        raise SdkOutputAdapterError(f"sdk_proposal_schema_invalid:{exc}") from exc


def _extract_final_output(sdk_result: Any) -> Any:
    if isinstance(sdk_result, dict):
        if "final_output" in sdk_result:
            return sdk_result["final_output"]
        return sdk_result
    if hasattr(sdk_result, "final_output"):
        return sdk_result.final_output
    return sdk_result


def _agent_path(
    raw_output: dict[str, Any],
    sdk_result: Any,
    starting_agent: str,
) -> list[dict[str, Any]]:
    candidate = raw_output.get("agent_path")
    if isinstance(candidate, list) and candidate:
        return candidate

    items: list[dict[str, Any]] = [
        AgentPathItem(event="start", agent=starting_agent).model_dump(mode="json")
    ]
    for item in _extract_sdk_items(sdk_result):
        event = _event_from_sdk_item(item)
        if event is not None:
            items.append(event)

    last_agent = _last_agent_name(sdk_result)
    if last_agent and last_agent != starting_agent:
        items.append(
            AgentPathItem(
                event="handoff",
                from_agent=starting_agent,
                to_agent=last_agent,
            ).model_dump(mode="json")
        )
    items.append(
        AgentPathItem(event="final", agent=last_agent or starting_agent).model_dump(mode="json")
    )
    return items


def _extract_sdk_items(sdk_result: Any) -> list[Any]:
    for attr_name in ("new_items", "items", "run_items"):
        value = getattr(sdk_result, attr_name, None)
        if isinstance(value, list):
            return value
    if isinstance(sdk_result, dict):
        for key in ("new_items", "items", "run_items"):
            value = sdk_result.get(key)
            if isinstance(value, list):
                return value
    return []


def _event_from_sdk_item(item: Any) -> dict[str, Any] | None:
    item_type = str(_item_value(item, "type") or _item_value(item, "item_type") or "")
    agent_name = _agent_name(_item_value(item, "agent"))
    raw_name = str(_item_value(item, "name") or _item_value(item, "tool_name") or "")
    if "tool" in item_type or raw_name:
        return AgentPathItem(
            event="tool",
            agent=agent_name,
            tool_name=raw_name or None,
        ).model_dump(mode="json")
    if "handoff" in item_type:
        return AgentPathItem(
            event="handoff",
            agent=agent_name,
            to_agent=_agent_name(_item_value(item, "target_agent")),
        ).model_dump(mode="json")
    if "guardrail" in item_type:
        return AgentPathItem(
            event="guardrail",
            agent=agent_name,
            guardrail_name=raw_name or None,
        ).model_dump(mode="json")
    return None


def _item_value(item: Any, name: str) -> Any:
    if isinstance(item, dict):
        return item.get(name)
    return getattr(item, name, None)


def _last_agent_name(sdk_result: Any) -> str | None:
    if isinstance(sdk_result, dict):
        return _agent_name(sdk_result.get("last_agent"))
    return _agent_name(getattr(sdk_result, "last_agent", None))


def _agent_name(agent: Any) -> str | None:
    if agent is None:
        return None
    if isinstance(agent, str):
        return agent
    if isinstance(agent, dict):
        name = agent.get("name")
        return str(name) if name else None
    name = getattr(agent, "name", None)
    return str(name) if name else None
