# Reference Map: OpenAI CS Agents Demo To Taliya Runtime

This feature treats `openai/openai-cs-agents-demo` as a binding architecture reference. The domain changes from airline support to Taliya commercial sales, but the runtime structure should remain recognizable.

Reference repository: `https://github.com/openai/openai-cs-agents-demo`

Local review snapshot: `C:\Users\lucas\AppData\Local\Temp\openai-cs-agents-demo` at commit `bd7bfca`.

## File Mapping

| Reference Demo File | Role In Demo | Taliya Target |
|---------------------|--------------|---------------|
| `python-backend/airline/agents.py` | Defines triage and specialist agents, tools, guardrails, and handoffs | `services/taliya-agent-runtime/app/domains/taliya_commercial/agents.py` |
| `python-backend/airline/tools.py` | Model-callable tools with context mutation and progress events | `services/taliya-agent-runtime/app/domains/taliya_commercial/tools.py` plus shared runtime tools |
| `python-backend/airline/guardrails.py` | LLM input guardrails and tripwire outputs | `services/taliya-agent-runtime/app/domains/taliya_commercial/guardrails.py` and `app/shared/guardrails/validators.py` |
| `python-backend/airline/context.py` | Pydantic context and public context projection | `services/taliya-agent-runtime/app/domains/taliya_commercial/context.py` |
| `python-backend/airline/server.py` | ChatKit server, state loading, runner execution, event streaming, memory updates | `services/taliya-agent-runtime/app/main.py` and `app/runtime/runner.py` |
| `python-backend/airline/memory_store.py` | In-memory demo store | `services/taliya-agent-runtime/app/shared/memory/postgres.py` |
| `python-backend/airline/demo_data.py` | Demo domain data | `services/taliya-agent-runtime/app/shared/product_knowledge/source.py` |
| `ui/components/chatkit-panel.tsx` | Chat UI panel and ChatKit connection | Existing widget remains in `components/landing/shared/FloatingAiAttendant.tsx`; no visual redesign |
| `ui/components/agent-panel.tsx` | Shows agents, context, guardrails, runner output | Extend `components/internal/SalesInboxClient.tsx` with trace summaries |
| `ui/components/runner-output.tsx` | Groups tool calls, handoffs, messages, context events | Sales Inbox trace detail and eval reports |

## Concept Mapping

| Reference Concept | Taliya Adaptation |
|-------------------|-------------------|
| Triage Agent | `taliya_commercial_triage`, routes commercial turns to Taliya specialist roles by LLM decision |
| Flight Information Agent | `taliya_commercial_product_agent`, pricing, plan, demo, links, availability, and product facts |
| Booking/Cancellation Agent | `taliya_commercial_waitlist_agent`, waitlist and checkout-unavailable path |
| Seat/Special Services Agent | `taliya_commercial_diagnostic_agent`, studio context and diagnostic |
| FAQ Agent | `taliya_commercial_entry_agent`, openings, source-specific entry messages, product overview, and objections when no deeper specialist is needed |
| Escalation/Human path | `taliya_commercial_handoff_agent`, human pause and resume behavior |
| Refunds/Compensation Agent | Not copied as domain behavior; pattern can inform policies for unsupported claims and cancellation |
| `@function_tool` tools | Product knowledge, save facts, save diagnostic, mark waitlist, pause human, resume human, record trace |
| Handoffs | Current implementation: one LLM-first conductor selects the specialist role and persists the role transition; human handoff is a real operational pause/resume boundary. Full SDK multi-call agent-to-agent handoff is not implemented in the normal turn loop. |
| Input guardrails | Prompt injection, relevance, abuse, sensitive data, unsupported media |
| Output validation | No invented price/link/checkout, no WhatsApp phone request, no fake certainty, source version required |
| `input_items` memory | Persisted message history plus compact summary and current agent |
| Runner events | Persisted agent runtime trace and Sales Inbox trace summary |

## Required Fidelity Checks

- Agent definitions must be explicit, not hidden behind route `if/else`.
- Tools must be model-callable contracts, not only internal functions selected by deterministic orchestration.
- Human handoffs must be represented as first-class events and persisted.
- Specialist role changes must be visible in structured output and traces. Do not claim full SDK agent-to-agent handoff execution unless separate specialist agents actually run and transfer control in the runtime loop.
- Guardrails must exist outside the main conversation prompt.
- Context must be typed and persisted.
- The runner must update current agent and input history after every successful turn.
- Trace output must show messages, tool calls, handoffs, guardrails, context changes, and final output.
- Runtime structure should preserve the reference split between `agents.py`, `tools.py`, `guardrails.py`, `context.py`, runner/server orchestration, and memory store rather than concentrating behavior in one orchestrator file.
- The live non-mock path must prove that the specialist role definitions influence behavior, not only that the model returns a `current_agent` string.
- Normal-turn architecture may remain a one-call conductor if the LLM owns commercial interpretation and the role definitions, tool contracts, guardrails, and evals materially constrain behavior.
- The behavior contract must be represented in prompts, structured output, validators, and evals; keeping it only in docs is insufficient.

## Implemented Runtime Paths

- `services/taliya-agent-runtime/app/domains/taliya_commercial/agents.py`
- `services/taliya-agent-runtime/app/domains/taliya_commercial/tools.py`
- `services/taliya-agent-runtime/app/domains/taliya_commercial/guardrails.py`
- `services/taliya-agent-runtime/app/domains/taliya_commercial/context.py`
- `services/taliya-agent-runtime/app/domains/taliya_commercial/prompts.py`
- `services/taliya-agent-runtime/app/runtime/runner.py`
- `services/taliya-agent-runtime/app/shared/memory/postgres.py`
- `services/taliya-agent-runtime/app/main.py`

## Allowed Domain Adaptations

- Keep the existing custom widget UI instead of ChatKit on `/pilates`.
- Use Sales Inbox as the operator trace surface instead of the demo Agent View.
- Use Postgres instead of in-memory demo storage.
- Use Taliya product knowledge instead of airline demo data.
- Use Taliya commercial specialists instead of airline support specialists.

## Disallowed Drift

- Rebuilding the conversation as regex, templates, and state machine logic.
- Calling the LLM only as a fallback after deterministic routes fail.
- Keeping templates as the deterministic conversation brain or selecting them through route `if/else` instead of LLM structured output.
- Treating tools as hidden side effects that the model cannot select.
- Treating the reference as naming inspiration only.
