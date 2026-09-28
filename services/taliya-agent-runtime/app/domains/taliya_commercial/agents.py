from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.domains.taliya_commercial.behavior_policy import (
    DIAGNOSTIC_AGENT,
    ENTRY_AGENT,
    HANDOFF_AGENT,
    PRODUCT_AGENT,
    TRIAGE_AGENT,
    WAITLIST_AGENT,
)
from app.domains.taliya_commercial.guardrails import GUARDRAIL_NAMES
from app.domains.taliya_commercial.prompts import (
    DIAGNOSTIC_PROMPT,
    ENTRY_PROMPT,
    HUMAN_HANDOFF_PROMPT,
    PRODUCT_PROMPT,
    TRIAGE_PROMPT,
    WAITLIST_PROMPT,
)
from app.domains.taliya_commercial.tools import get_model_callable_tool_names, get_model_callable_tools
from app.settings import get_settings

try:
    from agents import Agent
except Exception:  # pragma: no cover - SDK fallback
    Agent = None


@dataclass
class AgentSpec:
    name: str
    instructions: str
    handoff_description: str
    tools: list[Any] = field(default_factory=list)
    handoffs: list[str] = field(default_factory=list)
    input_guardrails: list[str] = field(default_factory=lambda: list(GUARDRAIL_NAMES))


def _sdk_agent(spec: AgentSpec) -> Any:
    if Agent is None:
        return spec
    return Agent(
        name=spec.name,
        model=get_settings().model,
        instructions=spec.instructions,
        handoff_description=spec.handoff_description,
        tools=spec.tools,
    )


def build_agent_specs() -> list[AgentSpec]:
    tools = get_model_callable_tools()
    return [
        AgentSpec(
            name=TRIAGE_AGENT,
            instructions=TRIAGE_PROMPT,
            handoff_description="Routes Taliya commercial leads to entry, product, diagnostic, waitlist, or human handoff.",
            tools=tools,
            handoffs=[
                ENTRY_AGENT,
                PRODUCT_AGENT,
                DIAGNOSTIC_AGENT,
                WAITLIST_AGENT,
                HANDOFF_AGENT,
            ],
        ),
        AgentSpec(
            name=ENTRY_AGENT,
            instructions=ENTRY_PROMPT,
            handoff_description="Handles openings, source-specific first messages, broad overviews, and early objections.",
            tools=tools,
            handoffs=[
                PRODUCT_AGENT,
                DIAGNOSTIC_AGENT,
                WAITLIST_AGENT,
                HANDOFF_AGENT,
            ],
        ),
        AgentSpec(
            name=PRODUCT_AGENT,
            instructions=PRODUCT_PROMPT,
            handoff_description="Answers price, plan, demo, guarantee, availability, and link questions from product knowledge.",
            tools=tools,
            handoffs=[
                DIAGNOSTIC_AGENT,
                WAITLIST_AGENT,
                HANDOFF_AGENT,
                TRIAGE_AGENT,
            ],
        ),
        AgentSpec(
            name=DIAGNOSTIC_AGENT,
            instructions=DIAGNOSTIC_PROMPT,
            handoff_description="Builds useful diagnostics from lead facts without fake certainty.",
            tools=tools,
            handoffs=[
                PRODUCT_AGENT,
                WAITLIST_AGENT,
                HANDOFF_AGENT,
                TRIAGE_AGENT,
            ],
        ),
        AgentSpec(
            name=WAITLIST_AGENT,
            instructions=WAITLIST_PROMPT,
            handoff_description="Handles waitlist offer, join, decline, and missing details after real interest.",
            tools=tools,
            handoffs=[
                PRODUCT_AGENT,
                DIAGNOSTIC_AGENT,
                HANDOFF_AGENT,
                TRIAGE_AGENT,
            ],
        ),
        AgentSpec(
            name=HANDOFF_AGENT,
            instructions=HUMAN_HANDOFF_PROMPT,
            handoff_description="Pauses automation for a human operator.",
            tools=[],
            handoffs=[],
            input_guardrails=[],
        ),
    ]


AGENT_SPECS = build_agent_specs()
AGENTS_BY_NAME = {spec.name: _sdk_agent(spec) for spec in AGENT_SPECS}


def get_taliya_agent_manifest() -> dict[str, Any]:
    return {
        "entry_agent": TRIAGE_AGENT,
        "tool_names": get_model_callable_tool_names(),
        "agents": [
            {
                "name": spec.name,
                "description": spec.handoff_description,
                "handoffs": list(spec.handoffs),
                "tools": get_model_callable_tool_names() if spec.tools else [],
                "input_guardrails": list(spec.input_guardrails),
            }
            for spec in AGENT_SPECS
        ],
    }
