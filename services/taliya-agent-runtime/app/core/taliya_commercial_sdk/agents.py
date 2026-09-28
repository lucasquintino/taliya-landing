from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.core.taliya_commercial.template_registry import TEMPLATE_REGISTRY, VARIABLE_REGISTRY
from app.core.taliya_commercial_sdk.sdk_output_model import TaliyaSdkTurnOutput
from app.core.taliya_commercial_sdk.tools import get_sdk_tool_names, get_sdk_tools
from app.settings import get_settings

try:
    from agents import Agent, ModelSettings
except Exception:  # pragma: no cover - import fallback for static/no-sdk environments
    Agent = None
    ModelSettings = None

TRIAGE_AGENT = "taliya_triage_agent"
ENTRY_AGENT = "taliya_entry_agent"
PRODUCT_AGENT = "taliya_product_agent"
DIAGNOSTIC_AGENT = "taliya_diagnostic_agent"
WAITLIST_AGENT = "taliya_waitlist_agent"
HANDOFF_AGENT = "taliya_handoff_agent"

AGENT_ORDER = [
    TRIAGE_AGENT,
    ENTRY_AGENT,
    PRODUCT_AGENT,
    DIAGNOSTIC_AGENT,
    WAITLIST_AGENT,
    HANDOFF_AGENT,
]

BASE_LLM_FIRST_INSTRUCTION = """
You are part of Taliya's commercial sales agent for Pilates studio leads.
The LLM is the commercial understanding brain. Do not classify price, plan,
demo, diagnostic, waitlist, pain-first, social/source opening, objection, or
mixed-intent messages with deterministic shortcuts.

Produce structured proposal intent for the runtime. Do not deliver a final
customer-facing message directly. The runtime will validate official facts,
render approved templates, persist state, project Sales Inbox fields, and
deliver channel chunks after validation.

Use only official product knowledge/tool results for product claims. Never
invent prices, checkout links, launch dates, discounts, VIP access, availability,
or client/studio WhatsApp connection promises.

Output contract for every final turn:
1. template_plan.template_ids must never be empty: an empty plan means no
   reply is sent and the turn fails validation. Your approved templates are
   listed at the end of these instructions; use get_approved_template_catalog
   only if you need a template outside that list.
2. Fill every required variable of each chosen template in
   template_plan.variables, respecting each variable's kind, max_length, and
   allowed sources exactly as listed. Stay clearly under max_length. Compose
   values from official facts and the lead's concrete words. Declare where the
   underlying facts came from: a value synthesized from official facts you
   read is official_product_knowledge (cite the fact refs in evidence), not
   model_decision. Use model_decision only when the variable's allowed
   sources include it.
3. If the CURRENT inbound message asks a direct question, add it to
   answer_obligations and set answering_template_id to the template in your
   plan that answers it in this same turn. Answer first, steer second: the
   answering template must come before any steering template in template_ids.
   Questions from earlier turns that were already answered do not create new
   obligations; do not carry them forward.
4. Pick templates that match the actual commercial moment. Never use a
   waitlist offer template for curiosity without clear contract intent.
5. Read conversation state with the read-only state tools instead of guessing
   prior context. Batch independent tool calls in one round: you have few
   model operations per turn.
6. Your final structured output already carries every proposal (diagnostic
   ledger updates, demo, waitlist, handoff, template plan, state patch). Do
   not spend turns calling propose_* tools to duplicate what you will return
   in the final output; finalize directly. Typical turn shape: one batched
   read round, then the final structured output.
7. Operational rule: if conversation state shows a previous reply is still
   being delivered in chunks, do not answer the new inbound yet. Propose
   deferral in state_patch.delivery (defer_inbound_during_chunks=true with
   the deferred count) and keep the pending question recorded as an
   unanswered obligation for the next turn.
""".strip()

# The triage agent is intentionally absent: it is a pure router and never
# finalizes a turn, so it has no approved-template catalog.
AGENT_TEMPLATE_PREFIXES: dict[str, tuple[str, ...]] = {
    ENTRY_AGENT: ("opening.", "diagnostic.offer_soft", "fallback."),
    PRODUCT_AGENT: (
        "product.",
        "diagnostic.price_hook",
        "diagnostic.offer_soft",
        "opening.general_interest",
        "fallback.product_knowledge_missing",
    ),
    DIAGNOSTIC_AGENT: ("diagnostic.",),
    WAITLIST_AGENT: ("waitlist.", "fallback.product_knowledge_missing"),
    HANDOFF_AGENT: ("handoff.",),
}


def _approved_catalog_section(prefixes: tuple[str, ...]) -> str:
    """Render the agent's approved-template slice from the official registry."""

    template_lines: list[str] = []
    variable_names: set[str] = set()
    for template_id in sorted(TEMPLATE_REGISTRY):
        if not any(template_id.startswith(prefix) for prefix in prefixes):
            continue
        template = TEMPLATE_REGISTRY[template_id]
        parts = []
        if template.required_variables:
            parts.append("required: " + ", ".join(template.required_variables))
            variable_names.update(template.required_variables)
        if template.optional_variables:
            parts.append("optional: " + ", ".join(template.optional_variables))
            variable_names.update(template.optional_variables)
        suffix = f" ({'; '.join(parts)})" if parts else ""
        template_lines.append(f"- {template_id}{suffix}")

    variable_lines: list[str] = []
    for name in sorted(variable_names):
        spec = VARIABLE_REGISTRY.get(name)
        if spec is None:
            continue
        max_length = f", max_length={spec.max_length}" if spec.max_length else ""
        sources = "|".join(sorted(spec.allowed_sources))
        variable_lines.append(f"- {name}: {spec.kind}{max_length}, sources: {sources}")

    return (
        "\n\nApproved templates for this role:\n"
        + "\n".join(template_lines)
        + "\n\nVariable specs (kind, max_length, allowed sources):\n"
        + "\n".join(variable_lines)
    )

AGENT_INSTRUCTIONS: dict[str, str] = {
    TRIAGE_AGENT: (
        BASE_LLM_FIRST_INSTRUCTION
        + """

Role: you are a pure router. You never write the reply yourself: every turn
you hand off to exactly one specialist by semantic understanding of the
message and the conversation history. Preserve mixed-intent messages instead
of flattening them when choosing the specialist.

Routing map: pure cold openings, source/social context, and broad interest go
to the entry agent; price, plans, product, demo, and WhatsApp scope go to the
product agent; diagnostic requests, answers to diagnostic questions, and
in-progress diagnostics go to the diagnostic agent; clear buying/waitlist
intent goes to the waitlist agent; requests for a human go to the handoff
agent.
"""
    ),
    ENTRY_AGENT: (
        BASE_LLM_FIRST_INSTRUCTION
        + """

Role: handle cold openings, widget empty openings, source/social context,
diagnostic CTA openings, broad interest, and "quero saber mais". Keep the lead
moving naturally, but do not invent product facts. Offer a soft diagnostic only
when the conversation context makes it helpful and allowed.

You own openings and broad interest only. If the lead asks about price, plans,
product, demo, or WhatsApp scope, hand off to the product agent; if a
diagnostic is in progress or the lead answers a diagnostic question, hand off
to the diagnostic agent; for buying/waitlist intent, the waitlist agent; for a
human request, the handoff agent. Do not answer those with opening templates.
"""
    ),
    PRODUCT_AGENT: (
        BASE_LLM_FIRST_INSTRUCTION
        + """

Role: answer product, price, plan, demo, WhatsApp scope, integration, security,
comparison, and out-of-profile questions. Answer direct questions first, then
steer. Keep price separate from student count such as "497". Use official facts
before proposing product claims. Avoid CRM jargon unless the lead used it first.

You do not conduct the diagnostic. If the lead accepts or asks to start the
diagnostic, or answers a diagnostic question, hand off to the diagnostic agent;
your role ends at offering it softly (diagnostic.offer_soft) when relevant.
"""
    ),
    DIAGNOSTIC_AGENT: (
        BASE_LLM_FIRST_INSTRUCTION
        + """

Role: conduct a consultative diagnostic inside a controlled flow with a fixed
mandatory question order:
1. active_students_or_size  2. main_pain  3. pain_detail
4. current_process  5. priority  6. urgency

Every turn follows the same shape: interpret the lead's answer and
accept simple answers such as "120", record it as a ledger update for the
pending key, give a short grounded answer_feedback on what they said, and ask
exactly the next pending question with its ask template (diagnostic.ask_*).
Never re-ask
an answered question, never skip ahead, never deliver before all six keys are
complete. If the lead asks a side question, answer it first, then resume the
same pending question. When the sixth key is answered, set
final_diagnostic_ready and deliver the final staged diagnostic, grounded in
the ledger and official plan facts. Use concrete lead context instead of
generic pain wording.

Source labels for diagnostic variables: reflections on the lead's last answer
(answer_feedback) are source user_message or diagnostic_ledger; recommendations
you compose from the lead's diagnostic answers are diagnostic_ledger; plan or
product recommendations grounded in official facts are
official_product_knowledge. Never label these model_decision - the runtime
only renders grounded values, so model_decision fails validation for them.

Before delivering the final staged diagnostic, read official plan facts with
get_product_knowledge (plans/prices keys) in your read round, because
recommended_plan_or_range must be grounded in official_product_knowledge with
the fact refs in evidence. Without that read, you cannot deliver the final
diagnostic this turn.
"""
    ),
    WAITLIST_AGENT: (
        BASE_LLM_FIRST_INSTRUCTION
        + """

Role: handle qualified waitlist or contract intent only after clear fit and
next-step intent. Distinguish curiosity from buying intent. Collect only missing
actionable details. Never ask for WhatsApp phone on WhatsApp, and avoid checkout,
date, discount, VIP, or availability promises.
"""
    ),
    HANDOFF_AGENT: (
        BASE_LLM_FIRST_INSTRUCTION
        + """

Role: acknowledge human handoff requests and propose that AI should pause. Do
not continue automation while human support is active. Resumption must come from
an explicit runtime resume event, not from model interpretation alone.
"""
    ),
}


@dataclass(frozen=True)
class TaliyaSdkAgentSpec:
    name: str
    handoff_description: str
    instructions: str
    handoffs: tuple[str, ...] = field(default_factory=tuple)
    tool_names: tuple[str, ...] = field(default_factory=tuple)


def _instructions_with_catalog(agent_name: str) -> str:
    return AGENT_INSTRUCTIONS[agent_name] + _approved_catalog_section(
        AGENT_TEMPLATE_PREFIXES[agent_name]
    )


def build_sdk_agent_specs() -> dict[str, TaliyaSdkAgentSpec]:
    all_tool_names = tuple(get_sdk_tool_names())
    specs = {
        TRIAGE_AGENT: TaliyaSdkAgentSpec(
            name=TRIAGE_AGENT,
            handoff_description=(
                "Routes unclear Taliya commercial lead turns to entry, product, "
                "diagnostic, waitlist, or human handoff specialists."
            ),
            # Pure router: no read/proposal tools, so with tool_choice
            # "required" the only action it can take is a handoff. Which
            # specialist receives the turn remains the model's semantic call.
            instructions=AGENT_INSTRUCTIONS[TRIAGE_AGENT],
            handoffs=(ENTRY_AGENT, PRODUCT_AGENT, DIAGNOSTIC_AGENT, WAITLIST_AGENT, HANDOFF_AGENT),
            tool_names=(),
        ),
        ENTRY_AGENT: TaliyaSdkAgentSpec(
            name=ENTRY_AGENT,
            handoff_description="Handles openings, source/social context, and broad interest.",
            instructions=_instructions_with_catalog(ENTRY_AGENT),
            handoffs=(PRODUCT_AGENT, DIAGNOSTIC_AGENT, WAITLIST_AGENT, HANDOFF_AGENT),
            tool_names=all_tool_names,
        ),
        PRODUCT_AGENT: TaliyaSdkAgentSpec(
            name=PRODUCT_AGENT,
            handoff_description="Answers product, price, plan, demo, and WhatsApp scope questions.",
            instructions=_instructions_with_catalog(PRODUCT_AGENT),
            handoffs=(DIAGNOSTIC_AGENT, WAITLIST_AGENT, HANDOFF_AGENT, TRIAGE_AGENT),
            tool_names=all_tool_names,
        ),
        DIAGNOSTIC_AGENT: TaliyaSdkAgentSpec(
            name=DIAGNOSTIC_AGENT,
            handoff_description="Conducts the diagnostic and proposes ledger updates.",
            instructions=_instructions_with_catalog(DIAGNOSTIC_AGENT),
            handoffs=(PRODUCT_AGENT, WAITLIST_AGENT, HANDOFF_AGENT, TRIAGE_AGENT),
            tool_names=all_tool_names,
        ),
        WAITLIST_AGENT: TaliyaSdkAgentSpec(
            name=WAITLIST_AGENT,
            handoff_description="Handles qualified waitlist and next-step intent.",
            instructions=_instructions_with_catalog(WAITLIST_AGENT),
            handoffs=(PRODUCT_AGENT, DIAGNOSTIC_AGENT, HANDOFF_AGENT, TRIAGE_AGENT),
            tool_names=all_tool_names,
        ),
        HANDOFF_AGENT: TaliyaSdkAgentSpec(
            name=HANDOFF_AGENT,
            handoff_description="Handles human handoff pause proposals.",
            instructions=_instructions_with_catalog(HANDOFF_AGENT),
            handoffs=(),
            tool_names=(
                "get_conversation_summary",
                "get_demo_waitlist_handoff_state",
                "propose_handoff",
                "propose_template_plan",
                "propose_sales_inbox_projection",
            ),
        ),
    }
    return {name: specs[name] for name in AGENT_ORDER}


def build_sdk_agents(*, model: Any | None = None) -> dict[str, Any]:
    """Build the real SDK agents.

    `model` accepts a model name string or an injected SDK `Model` instance
    (used by the no-cost dry-run harness). Every agent declares the strict
    `TaliyaSdkTurnOutput` output type so the final output is always a
    structured proposal, never free-form lead-facing text.
    """

    specs = build_sdk_agent_specs()
    if Agent is None:
        return dict(specs)

    selected_model = model if model is not None else get_settings().model
    sdk_tools_by_name = {tool.name: tool for tool in get_sdk_tools()}
    agents_by_name: dict[str, Any] = {}
    for name in AGENT_ORDER:
        spec = specs[name]
        agent_kwargs: dict[str, Any] = {}
        if name == TRIAGE_AGENT and ModelSettings is not None:
            # Force the router to act: with no tools and required tool choice,
            # the only possible action is one handoff to a specialist.
            agent_kwargs["model_settings"] = ModelSettings(tool_choice="required")
        agents_by_name[name] = Agent(
            name=spec.name,
            handoff_description=spec.handoff_description,
            instructions=spec.instructions,
            model=selected_model,
            output_type=TaliyaSdkTurnOutput,
            tools=[sdk_tools_by_name[tool_name] for tool_name in spec.tool_names],
            **agent_kwargs,
        )

    for name in AGENT_ORDER:
        spec = specs[name]
        agents_by_name[name].handoffs = [agents_by_name[handoff] for handoff in spec.handoffs]

    return agents_by_name


def get_sdk_agent_manifest() -> dict[str, Any]:
    specs = build_sdk_agent_specs()
    return {
        "entry_agent": TRIAGE_AGENT,
        "agents": [
            {
                "name": spec.name,
                "description": spec.handoff_description,
                "handoffs": list(spec.handoffs),
                "tools": list(spec.tool_names),
                "instructions": spec.instructions,
            }
            for spec in specs.values()
        ],
    }
