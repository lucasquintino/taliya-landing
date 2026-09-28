"""T012-030D: SDK agents rewired to the action-first contract.

The spike agents (`agents.py`) stay frozen as evidence; this module is the
production wiring per `design-lock-v2-action-first.md`:

- every agent's `output_type` is the strict `ConductorActionDecision`;
- the board (TurnSituation preamble) carries mode, pending key, allowed
  actions, and compact memory - so specialists need NO tools: a routed turn
  is one handoff plus one model operation, a known-state turn is one
  operation total;
- the triage agent stays a pure router (no tools, tool_choice=required);
- starting agent is selected deterministically from the situation MODE
  (state-based operational selection, never raw-text routing): known modes
  start directly at their specialist, only `entry` goes through the router.
"""

from __future__ import annotations

from typing import Any

from app.core.taliya_commercial_sdk.agents import (
    DIAGNOSTIC_AGENT,
    ENTRY_AGENT,
    HANDOFF_AGENT,
    PRODUCT_AGENT,
    TRIAGE_AGENT,
    WAITLIST_AGENT,
)
from app.core.taliya_commercial_sdk.conductor_decision import (
    ConductorActionDecision,
)
from app.core.taliya_commercial_sdk.turn_situation import TurnSituation
from app.settings import get_settings

try:
    from agents import Agent, ModelSettings
except Exception:  # pragma: no cover - import fallback for static/no-sdk environments
    Agent = None
    ModelSettings = None

ACTION_AGENT_ORDER = [
    TRIAGE_AGENT,
    ENTRY_AGENT,
    PRODUCT_AGENT,
    DIAGNOSTIC_AGENT,
    WAITLIST_AGENT,
    HANDOFF_AGENT,
]
ACTION_MODEL_REASONING_EFFORT = "none"

# Deterministic mode -> starting agent (state-based operational selection).
STARTING_AGENT_BY_MODE: dict[str, str | None] = {
    "entry": TRIAGE_AGENT,
    "diagnostic": DIAGNOSTIC_AGENT,
    "post_diagnostic": PRODUCT_AGENT,
    "product": PRODUCT_AGENT,
    "price": PRODUCT_AGENT,
    "demo": PRODUCT_AGENT,
    "waitlist": WAITLIST_AGENT,
    "handoff": HANDOFF_AGENT,
    # Operational modes never call the LLM.
    "safety": None,
    "delivery_deferred": None,
}

_BASE_ACTION_FIRST_INSTRUCTION = """
You are part of Taliya's commercial sales agent for Pilates studio leads.
You are the commercial understanding brain: interpret the lead's message in
the context of the conversation, then decide the turn.

The runtime context block "[runtime context] Turn situation" is authoritative
and code-derived: it gives you the mode, the pending diagnostic question, the
ALLOWED ACTIONS for this turn, constraints, and compact memory. Trust it; do
not re-derive state.

Output contract (ConductorActionDecision):
1. selected_action: EXACTLY ONE action from the allowed actions list. Which
   action fits the lead's message is your semantic decision; the list only
   constrains form.
2. direct_question: only a question asked in the CURRENT inbound message.
   Questions already answered in earlier turns are never new obligations.
3. captured_slots: facts the lead just gave (e.g. the pending diagnostic
   answer), typed by key, with the lead's words as evidence.
4. composition_variables: the human prose pieces assigned to you (e.g.
   pain_context_human, handoff_reason,
   clarification_question). Compose them in Brazilian Portuguese with correct
   accents and punctuation, in plain Pilates-studio-owner language (no SaaS
   jargon, no "CRM" unless the lead used it). Ground each in the lead's
   concrete words or the ledger - reuse their meaning naturally, never repeat
   their sentence literally, never write generic filler. Preserve concrete
   channels, processes, or objects that make the context specific, such as
   WhatsApp, agenda, reposições, cobranças, or follow-up. For normal diagnostic
   answer capture, do not invent answer_feedback: the runtime renders a short
   approved acknowledgement for the answered question. Each composition needs
   evidence.
5. You never output final customer text, template ids, or state transitions:
   the runtime compiles your chosen action into the approved delivery.
6. Never invent prices, links, dates, discounts, VIP access, availability, or
   client/studio WhatsApp connection promises - official facts are injected
   by the runtime from official sources.
""".strip()

_ROLE_INSTRUCTIONS: dict[str, str] = {
    TRIAGE_AGENT: (
        "Role: pure router. You never write the reply: hand off to exactly "
        "one specialist by semantic understanding - entry for openings/"
        "source/broad interest, product for price/plans/product/demo/"
        "WhatsApp scope, diagnostic for diagnostic requests or answers, "
        "waitlist for clear buying intent, handoff for human requests. "
        "Preserve mixed intent when choosing."
    ),
    ENTRY_AGENT: (
        "Role: openings and broad interest. Greet naturally without offering "
        "diagnostic on a pure cold greeting; acknowledge source context; "
        "when the lead explicitly names a source such as Instagram and asks "
        "broadly to know more, choose answer_source_opening, not "
        "answer_general_interest, and do not declare a product fact key "
        "because the approved source-opening template already gives the "
        "overview; "
        "offer the diagnostic softly only when pain/context makes it useful "
        "(offer_diagnostic_from_pain requires your pain_context_human "
        "composition grounded in the lead's pain, but word it as a practical "
        "reading of the situation, not a repeat of the lead's sentence). "
        "When the lead ACCEPTS or "
        "asks to start the diagnostic - including 'faz sentido', 'pode "
        "fazer', or asking how the diagnostic works after an offer - choose "
        "start_requested_diagnostic and begin the diagnostic without asking "
        "for name first. Never ask for phone, never ask for name on a pure "
        "cold greeting, and never re-offer a diagnostic the lead just "
        "accepted."
    ),
    PRODUCT_AGENT: (
        "Role: product, price, plan, demo, WhatsApp scope, integration, "
        "security, comparison, objections, and post-diagnostic consultative "
        "follow-up. Answer the direct question first (pick the answering "
        "action), then steer. Keep price separate from student counts such "
        "as '497'. Declare product_fact_keys_used for the official facts "
        "your answer needs (e.g. prices, demo_link, whatsapp_scope, "
        "routine_areas). For "
        "price + pain/context in the same message, still answer price first, "
        "but include a grounded plan_fit_context composition so the runtime "
        "can render the contextual diagnostic hook; never use the generic "
        "price hook when the lead gave a concrete pain. If the lead mentions "
        "a concrete operational context in the price message - agenda, "
        "reposicao, WhatsApp, follow-up, cobranca, vendas, financeiro, "
        "alunos, atendimento, reposicoes, or similar - that is price + "
        "context: include plan_fit_context with that concrete anchor. For "
        "general objections like 'vou pensar', 'nao tenho tempo', 'preciso "
        "falar com minha socia', 'parece complicado', or 'minha equipe nao "
        "vai usar', acknowledge without pressure and use saved diagnostic "
        "context when present; do not create checkout/date/discount promises. "
        "Interpret short follow-ups from the immediately preceding context: "
        "after a price answer, wording such as 'talvez fique pesado' usually "
        "signals a budget or value concern, not operational workload, unless "
        "the conversation provides evidence for another meaning. "
        "For conversation_resume such as 'pode continuar', 'como funciona "
        "mesmo?', or plan recall, use answer_product_question_with_saved_context "
        "with post_diagnostic_context and never restart the diagnostic. If a "
        "direct product question can be answered by one specific official fact, "
        "choose only that smallest sufficient fact set. In particular, a direct "
        "question about how the product works on WhatsApp uses whatsapp_scope "
        "without also adding the generic how_it_works fact. If a "
        "post-diagnostic lead says they want to start or be put on the list, "
        "choose offer_or_join_waitlist_if_eligible and include "
        "waitlist_context_summary; do not choose join_waitlist unless the "
        "runtime mode is already waitlist with missing details being supplied."
    ),
    DIAGNOSTIC_AGENT: (
        "Role: conduct the controlled diagnostic. The pending question comes "
        "from the runtime context. Interpret the lead's answer (accept "
        "simple answers such as '120') and capture it as a typed slot. For "
        "normal diagnostic answers, do not compose answer_feedback; the "
        "runtime renders the approved short acknowledgement for that question. "
        "If the lead's answer is too broad, conditional, or ambiguous for "
        "the pending question, choose clarify_ambiguous_diagnostic_answer "
        "instead of advancing. Compose one short clarification_question that "
        "asks for a more direct or approximate answer to the same pending "
        "question; do not repeat the full diagnostic menu unless it helps the "
        "lead choose. "
        "Side "
        "questions: answer first, then continue "
        "(answer_direct_question_then_continue_diagnostic). Complete only "
        "when the context says the last key can close this turn; completion "
        "requires your pain_context_human, crm_base_recommendation, and "
        "operational_first_step compositions grounded in the ledger. When the "
        "current inbound answers the last pending key such as urgency "
        "('agora', 'esse mes', or 'so pesquisando'), include that captured "
        "slot in the same complete_diagnostic decision; do not complete with "
        "the key missing. If the "
        "lead refuses diagnostic or asks for a direct answer only ('sem "
        "perguntas agora', 'so me fala o preco'), choose "
        "respect_diagnostic_refusal, answer the direct matter if present, and "
        "do not offer diagnostic again in the same turn."
    ),
    WAITLIST_AGENT: (
        "Role: qualified waitlist flow. Distinguish curiosity from contract "
        "intent; collect only missing details, one at a time; never ask for "
        "the WhatsApp phone on WhatsApp; never promise checkout, dates, "
        "discounts, or VIP access. If the lead hesitates, withdraws intent, "
        "or wants to understand first, choose pause_waitlist_decision; do not "
        "collect details or mark them as joined. Use "
        "answer_question_then_continue_waitlist only when the lead actually "
        "asked a concrete product question. Capture every pending waitlist "
        "detail supplied in the current message. If that message supplies all "
        "remaining details and confirms entry, choose join_waitlist; do not ask "
        "again for a field you already captured."
    ),
    HANDOFF_AGENT: (
        "Role: human handoff. Acknowledge directly and pause automation; "
        "compose handoff_reason from the lead's words. Resumption only "
        "happens through an explicit operator event, never your decision."
    ),
}


def build_action_first_agents(*, model: Any | None = None) -> dict[str, Any]:
    """Build the production action-first agents.

    `model` accepts a model name string or an injected SDK `Model` instance
    (no-cost dry-runs). Specialists carry no tools by design: the board
    carries the state, the compiler carries the facts.
    """

    if Agent is None:  # pragma: no cover - static/no-sdk environments
        raise RuntimeError("openai-agents SDK is required for action-first agents")

    selected_model = model if model is not None else get_settings().model
    agents_by_name: dict[str, Any] = {}
    for name in ACTION_AGENT_ORDER:
        kwargs: dict[str, Any] = {}
        if ModelSettings is not None:
            kwargs["model_settings"] = ModelSettings(
                reasoning={"effort": ACTION_MODEL_REASONING_EFFORT},
                tool_choice="required" if name == TRIAGE_AGENT else None,
            )
        agents_by_name[name] = Agent(
            name=name,
            handoff_description=_ROLE_INSTRUCTIONS[name].split(".")[0],
            instructions=(_BASE_ACTION_FIRST_INSTRUCTION + "\n\n" + _ROLE_INSTRUCTIONS[name]),
            model=selected_model,
            output_type=ConductorActionDecision,
            tools=[],
            **kwargs,
        )

    agents_by_name[TRIAGE_AGENT].handoffs = [
        agents_by_name[ENTRY_AGENT],
        agents_by_name[PRODUCT_AGENT],
        agents_by_name[DIAGNOSTIC_AGENT],
        agents_by_name[WAITLIST_AGENT],
        agents_by_name[HANDOFF_AGENT],
    ]
    return agents_by_name


def starting_agent_name_for(situation: TurnSituation) -> str | None:
    """Deterministic starting agent from the situation mode.

    Returns None when the runtime must not call the LLM at all
    (`llm_turn_allowed` is false or the mode is operational).
    """

    if not situation.llm_turn_allowed:
        return None
    return STARTING_AGENT_BY_MODE.get(situation.mode)
