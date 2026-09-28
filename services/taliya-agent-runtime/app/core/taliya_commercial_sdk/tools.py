from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from typing import Any

from app.core.taliya_commercial.product_knowledge import (
    build_official_product_knowledge_refs,
    build_spec006_product_contract_refs,
)
from app.core.taliya_commercial.template_registry import TEMPLATE_REGISTRY, VARIABLE_REGISTRY
from app.core.taliya_commercial_sdk.run_context import TaliyaSpikeContext

try:
    from agents import RunContextWrapper, function_tool
except Exception:  # pragma: no cover - import fallback for static/no-sdk environments

    class RunContextWrapper:  # type: ignore[no-redef]
        context: Any = None

    def function_tool(func: Any) -> Any:
        func.name = func.__name__
        return func


READ_ONLY_TOOL_NAMES = (
    "get_product_knowledge",
    "get_spec006_product_contracts",
    "get_diagnostic_ledger",
    "get_conversation_summary",
    "get_demo_waitlist_handoff_state",
    "get_approved_template_catalog",
)

PROPOSAL_ONLY_TOOL_NAMES = (
    "propose_diagnostic_update",
    "propose_waitlist_update",
    "propose_demo_state_update",
    "propose_handoff",
    "propose_template_plan",
    "propose_sales_inbox_projection",
)

COMMIT_TOOL_NAMES: tuple[str, ...] = ()


def _dedupe(values: Sequence[str] | None) -> list[str]:
    if values is None:
        return []
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = str(value).strip()
        if not normalized or normalized in seen:
            continue
        output.append(normalized)
        seen.add(normalized)
    return output


def _envelope(
    *,
    tool_name: str,
    side_effect_class: str,
    payload: Mapping[str, Any],
    evidence: Sequence[str] | None = None,
    uncertainty: str = "medium",
) -> dict[str, Any]:
    return {
        "tool_name": tool_name,
        "side_effect_class": side_effect_class,
        "commits_state": False,
        "renders_customer_response": False,
        "chooses_commercial_route": False,
        "payload": dict(payload),
        "evidence": _dedupe(evidence),
        "uncertainty": uncertainty,
    }


def _snapshot_value(state_snapshot: Mapping[str, Any] | None, key: str) -> Any:
    if not state_snapshot:
        return None
    return state_snapshot.get(key)


def _spike_context(ctx: Any) -> TaliyaSpikeContext | None:
    context = getattr(ctx, "context", None)
    if isinstance(context, TaliyaSpikeContext):
        return context
    return None


def _json_object(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError("Expected a JSON object")
    return parsed


def _proposal_payload(
    *,
    proposal_type: str,
    proposal: Mapping[str, Any],
    evidence: Sequence[str] | None,
    uncertainty: str,
) -> dict[str, Any]:
    evidence_items = _dedupe(evidence)
    return {
        "proposal_type": proposal_type,
        "proposal": dict(proposal),
        "validation_required": True,
        "commit_after_validation_only": True,
        "missing_evidence": not evidence_items,
        "evidence": evidence_items,
        "uncertainty": uncertainty,
    }


@function_tool
def get_product_knowledge(keys: list[str] | None = None) -> dict[str, Any]:
    """Read official Taliya product facts by key without choosing a route."""

    refs = build_official_product_knowledge_refs(keys)
    return _envelope(
        tool_name="get_product_knowledge",
        side_effect_class="read_only",
        payload={
            "refs": [ref.model_dump(mode="json") for ref in refs],
            "requested_keys": _dedupe(keys),
        },
        evidence=[evidence for ref in refs for evidence in ref.evidence],
        uncertainty="low",
    )


@function_tool
def get_spec006_product_contracts(keys: list[str] | None = None) -> dict[str, Any]:
    """Read Spec 006 product contract refs without creating offers or dates."""

    refs = build_spec006_product_contract_refs(keys)
    return _envelope(
        tool_name="get_spec006_product_contracts",
        side_effect_class="read_only",
        payload={
            "refs": [ref.model_dump(mode="json") for ref in refs],
            "requested_keys": _dedupe(keys),
        },
        evidence=[evidence for ref in refs for evidence in ref.evidence],
        uncertainty="low",
    )


@function_tool
def get_diagnostic_ledger(ctx: RunContextWrapper[TaliyaSpikeContext]) -> dict[str, Any]:
    """Read the diagnostic ledger snapshot for this conversation without mutation."""

    context = _spike_context(ctx)
    state_snapshot = context.state_snapshot if context else None
    conversation_id = context.conversation_id if context else "unknown"
    ledger = _snapshot_value(state_snapshot, "diagnostic")
    return _envelope(
        tool_name="get_diagnostic_ledger",
        side_effect_class="read_only",
        payload={
            "conversation_id": conversation_id,
            "diagnostic": ledger or {},
            "source": "run_context_snapshot" if ledger is not None else "not_connected_in_spike",
        },
        evidence=[f"conversation.{conversation_id}.diagnostic"] if ledger is not None else [],
        uncertainty="low" if ledger is not None else "high",
    )


@function_tool
def get_conversation_summary(ctx: RunContextWrapper[TaliyaSpikeContext]) -> dict[str, Any]:
    """Read compact conversation memory without promoting inferred facts."""

    context = _spike_context(ctx)
    state_snapshot = context.state_snapshot if context else None
    conversation_id = context.conversation_id if context else "unknown"
    summary = _snapshot_value(state_snapshot, "summary")
    lead_facts = _snapshot_value(state_snapshot, "lead_facts") or []
    return _envelope(
        tool_name="get_conversation_summary",
        side_effect_class="read_only",
        payload={
            "conversation_id": conversation_id,
            "summary": summary,
            "lead_fact_count": len(lead_facts) if isinstance(lead_facts, list) else 0,
            "source": "run_context_snapshot" if state_snapshot else "not_connected_in_spike",
        },
        evidence=[f"conversation.{conversation_id}.summary"] if summary else [],
        uncertainty="medium" if summary else "high",
    )


@function_tool
def get_demo_waitlist_handoff_state(
    ctx: RunContextWrapper[TaliyaSpikeContext],
) -> dict[str, Any]:
    """Read demo, waitlist, and handoff state without committing state changes."""

    context = _spike_context(ctx)
    state_snapshot = context.state_snapshot if context else None
    conversation_id = context.conversation_id if context else "unknown"
    return _envelope(
        tool_name="get_demo_waitlist_handoff_state",
        side_effect_class="read_only",
        payload={
            "conversation_id": conversation_id,
            "demo": _snapshot_value(state_snapshot, "demo") or {},
            "waitlist": _snapshot_value(state_snapshot, "waitlist") or {},
            "human_status": _snapshot_value(state_snapshot, "human_status"),
            "human_reason": _snapshot_value(state_snapshot, "human_reason"),
            "source": "run_context_snapshot" if state_snapshot else "not_connected_in_spike",
        },
        evidence=[f"conversation.{conversation_id}.operational_state"] if state_snapshot else [],
        uncertainty="low" if state_snapshot else "high",
    )


@function_tool
def get_approved_template_catalog(route_or_family: str | None = None) -> dict[str, Any]:
    """Read approved template metadata; this tool never renders final copy."""

    family = str(route_or_family or "").strip()
    templates = []
    variable_names: set[str] = set()
    for template_id, template in sorted(TEMPLATE_REGISTRY.items()):
        if family and not template_id.startswith(family):
            continue
        variable_names.update(template.required_variables)
        variable_names.update(template.optional_variables)
        templates.append(
            {
                "template_id": template_id,
                "required_variables": list(template.required_variables),
                "optional_variables": list(template.optional_variables),
            }
        )
    variable_specs = {
        name: {
            "kind": spec.kind,
            "max_length": spec.max_length,
            "allowed_sources": sorted(spec.allowed_sources),
            "validation_rule": spec.validation_rule,
        }
        for name, spec in sorted(VARIABLE_REGISTRY.items())
        if name in variable_names
    }
    return _envelope(
        tool_name="get_approved_template_catalog",
        side_effect_class="read_only",
        payload={
            "route_or_family": family or None,
            "templates": templates,
            "variable_specs": variable_specs,
            "variable_registry_size": len(VARIABLE_REGISTRY),
        },
        evidence=["template_registry"],
        uncertainty="low",
    )


@function_tool
def propose_diagnostic_update(
    update_json: str,
    evidence: list[str] | None = None,
    uncertainty: str = "medium",
) -> dict[str, Any]:
    """Propose diagnostic ledger changes for later validator-controlled commit."""

    update = _json_object(update_json)
    return _envelope(
        tool_name="propose_diagnostic_update",
        side_effect_class="proposal_only",
        payload=_proposal_payload(
            proposal_type="diagnostic_update",
            proposal=update,
            evidence=evidence,
            uncertainty=uncertainty,
        ),
        evidence=evidence,
        uncertainty=uncertainty,
    )


@function_tool
def propose_waitlist_update(
    update_json: str,
    evidence: list[str] | None = None,
    uncertainty: str = "medium",
) -> dict[str, Any]:
    """Propose waitlist changes for later validation; do not join anyone here."""

    update = _json_object(update_json)
    return _envelope(
        tool_name="propose_waitlist_update",
        side_effect_class="proposal_only",
        payload=_proposal_payload(
            proposal_type="waitlist_update",
            proposal=update,
            evidence=evidence,
            uncertainty=uncertainty,
        ),
        evidence=evidence,
        uncertainty=uncertainty,
    )


@function_tool
def propose_demo_state_update(
    update_json: str,
    evidence: list[str] | None = None,
    uncertainty: str = "medium",
) -> dict[str, Any]:
    """Propose demo state changes for later validation and persistence."""

    update = _json_object(update_json)
    return _envelope(
        tool_name="propose_demo_state_update",
        side_effect_class="proposal_only",
        payload=_proposal_payload(
            proposal_type="demo_state_update",
            proposal=update,
            evidence=evidence,
            uncertainty=uncertainty,
        ),
        evidence=evidence,
        uncertainty=uncertainty,
    )


@function_tool
def propose_handoff(
    reason: str,
    evidence: list[str] | None = None,
    uncertainty: str = "medium",
) -> dict[str, Any]:
    """Propose human handoff pause; runtime state owns the actual pause."""

    return _envelope(
        tool_name="propose_handoff",
        side_effect_class="proposal_only",
        payload=_proposal_payload(
            proposal_type="handoff",
            proposal={"reason": reason},
            evidence=evidence,
            uncertainty=uncertainty,
        ),
        evidence=evidence,
        uncertainty=uncertainty,
    )


@function_tool
def propose_template_plan(
    template_ids: list[str],
    variables_json: str,
    evidence: list[str] | None = None,
    uncertainty: str = "medium",
) -> dict[str, Any]:
    """Propose approved template ids and variables without rendering them."""

    variables = _json_object(variables_json)
    return _envelope(
        tool_name="propose_template_plan",
        side_effect_class="proposal_only",
        payload=_proposal_payload(
            proposal_type="template_plan",
            proposal={"template_ids": _dedupe(template_ids), "variables": dict(variables)},
            evidence=evidence,
            uncertainty=uncertainty,
        ),
        evidence=evidence,
        uncertainty=uncertainty,
    )


@function_tool
def propose_sales_inbox_projection(
    fields_json: str,
    evidence: list[str] | None = None,
    uncertainty: str = "medium",
) -> dict[str, Any]:
    """Propose Sales Inbox fields; projection commit happens after validation."""

    fields = _json_object(fields_json)
    return _envelope(
        tool_name="propose_sales_inbox_projection",
        side_effect_class="proposal_only",
        payload=_proposal_payload(
            proposal_type="sales_inbox_projection",
            proposal=fields,
            evidence=evidence,
            uncertainty=uncertainty,
        ),
        evidence=evidence,
        uncertainty=uncertainty,
    )


READ_ONLY_TOOLS = (
    get_product_knowledge,
    get_spec006_product_contracts,
    get_diagnostic_ledger,
    get_conversation_summary,
    get_demo_waitlist_handoff_state,
    get_approved_template_catalog,
)

PROPOSAL_ONLY_TOOLS = (
    propose_diagnostic_update,
    propose_waitlist_update,
    propose_demo_state_update,
    propose_handoff,
    propose_template_plan,
    propose_sales_inbox_projection,
)

ALL_SDK_TOOLS = (*READ_ONLY_TOOLS, *PROPOSAL_ONLY_TOOLS)


def get_sdk_tools() -> list[Any]:
    return list(ALL_SDK_TOOLS)


def get_sdk_tool_names() -> list[str]:
    return [tool.name for tool in ALL_SDK_TOOLS]
