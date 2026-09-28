# Architecture - Spec 012 Agents SDK Migration

## Target Architecture

```text
Widget / Taliya-owned WhatsApp
-> Channel Adapter
-> Runtime API
-> Turn Gate
-> Context Builder
-> OpenAI Agents SDK Runner
   -> Taliya Triage Agent
   -> Taliya Entry Agent
   -> Taliya Product Agent
   -> Taliya Diagnostic Agent
   -> Taliya Waitlist Agent
   -> Taliya Handoff Agent
   -> Safety Guardrails
   -> Read-only / proposal-only tools
-> SDK Output Adapter
-> Contract Validators
-> Approved Template Renderer
-> Runtime State + Sales Inbox Projection
-> Delivery / Outbox
```

## Why This Is Different From Spec 011

Spec 011 implemented these pieces manually:

- model call orchestration;
- logical specialist roles;
- action selection;
- action repair;
- action compilation;
- trace/run item semantics;
- final state/render derivation.

Spec 012 moves the agent-native pieces into OpenAI Agents SDK:

- agent definitions;
- handoffs;
- tool contracts;
- guardrails;
- runner execution;
- SDK run items and trace semantics.

Taliya keeps the product and production safety layers:

- channel adapters;
- turn gate;
- context builder;
- validators;
- approved renderer;
- persistence;
- Sales Inbox projection;
- delivery/outbox;
- feature flags;
- eval gates.

## Agent Topology

### Taliya Triage Agent

Purpose: understand first-turn or unclear-state messages and hand off to the right specialist.

Responsibilities:

- route by LLM understanding, not regex;
- preserve mixed-intent messages;
- answer simple opening only when appropriate;
- hand off to product, diagnostic, waitlist, or handoff specialist;
- never ask for name/phone on cold greeting;
- never offer waitlist on cold greeting.

### Taliya Entry Agent

Purpose: handle openings, source/social context, widget opening, diagnostic CTA openings, and broad interest.

Responsibilities:

- cold greeting;
- widget empty opening;
- site/social opening;
- "quero saber mais";
- soft diagnostic offer only when allowed;
- no product fact invention.

### Taliya Product Agent

Purpose: answer product, price, plan, demo, WhatsApp scope, integration, security, comparison, and out-of-profile questions.

Responsibilities:

- answer direct questions first;
- use product knowledge tools;
- separate price from student count;
- offer diagnostic after answer when helpful;
- keep demo/product-demo state;
- avoid CRM jargon unless allowed.

### Taliya Diagnostic Agent

Purpose: conduct the diagnostic as a consultative conversation.

Responsibilities:

- maintain mandatory diagnostic ledger;
- ask one question at a time;
- accept simple answers such as "120";
- avoid repeated questions;
- answer side questions first, then continue;
- deliver final staged diagnostic only after required fields are complete;
- produce grounded customer-facing semantic fragments for approved templates.

### Taliya Waitlist Agent

Purpose: handle qualified waitlist intent only after clear fit/intent.

Responsibilities:

- distinguish curiosity from buying/next-step intent;
- offer waitlist only when allowed;
- collect only missing actionable details;
- never ask WhatsApp phone on WhatsApp;
- avoid checkout/date/discount/VIP promises.

### Taliya Handoff Agent

Purpose: pause AI and route to human when requested or required.

Responsibilities:

- acknowledge human request;
- propose/persist human pause;
- suppress AI while human active;
- resume only with explicit resume event.

## Tools

Tools are grouped by side-effect class.

### Read-Only Tools

Allowed during SDK reasoning:

- `get_product_knowledge(keys)`
- `get_spec006_product_contracts(keys)`
- `get_diagnostic_ledger(conversation_id)`
- `get_conversation_summary(conversation_id)`
- `get_demo_waitlist_handoff_state(conversation_id)`
- `get_approved_template_catalog(route_or_family)`

Read-only tools must not mutate state.

### Proposal-Only Tools

Allowed during SDK reasoning, but not allowed to commit production state:

- `propose_diagnostic_update(update, evidence)`
- `propose_waitlist_update(update, evidence)`
- `propose_demo_state_update(update, evidence)`
- `propose_handoff(reason, evidence)`
- `propose_template_plan(template_ids, variables, evidence)`
- `propose_sales_inbox_projection(fields, evidence)`

Proposal tools return structured proposals. The runtime validates and commits later.

### Commit Tools

Not callable by the free reasoning path on normal turns:

- commit diagnostic ledger;
- commit waitlist;
- commit human pause/resume;
- commit Sales Inbox projection;
- commit delivery/outbox.

These are runtime operations after validation.

## SDK Output Contract

The SDK path must produce a structured `TaliyaTurnProposal`.

Required groups:

- `agent_path`: current SDK agent, handoffs, tools called.
- `commercial_understanding`: intents, direct question, customer need, pain/context, evidence.
- `answer_obligations`: what must be answered before steering.
- `product_claims`: official product fact refs and claims proposed.
- `diagnostic_proposal`: ledger updates, next question, final diagnostic readiness, evidence.
- `demo_proposal`: status and next step.
- `waitlist_proposal`: eligibility, intent, missing details.
- `handoff_proposal`: status, reason, pause requirement.
- `template_proposal`: approved template ids and registered variables.
- `safety`: guardrail outcomes and uncertainty.
- `usage`: model usage and cost metadata.

This proposal replaces both:

- the old full `ConductorDecision` as a raw model contract;
- the narrower `ConductorActionDecision` as the normal-turn brain.

## Validation And Rendering Boundary

The SDK may reason and propose. It may not deliver.

Validation must occur before:

- rendering;
- runtime state update;
- Sales Inbox projection commit;
- delivery/outbox reservation;
- waitlist state mutation;
- human pause mutation, except explicit runtime-control commands.

Rendered text must come from approved templates plus registered semantic fragments. The SDK cannot produce a whole final WhatsApp/widget message that bypasses the renderer.

## Session And State Strategy

Persisted Taliya state remains the source of operational truth.

SDK session/history may be used as model conversation memory only if:

- the runtime can replay the same state from Taliya persistence;
- Sales Inbox projection remains derived from validated state/events;
- inferred or channel facts do not become reliable facts without evidence;
- trace exports contain the SDK items needed for debugging.

The runtime may start `Runner.run` from the persisted `current_sdk_agent` when known. This is allowed because it uses state, not raw-text commercial routing.

## Cost Strategy

The SDK path is allowed to use real handoffs when they improve correctness, but must be capped.

Initial target:

- cold/simple turn: 1 model operation;
- specialist turn from persisted state: 1 model operation;
- triage plus specialist handoff: allowed when needed, with max-turn cap;
- repair/escalation: at most 1 extra model operation;
- judge/eval: eval-only and labeled separately.

Cost optimization must not remove LLM judgment from commercial turns.

## Trace Strategy

The trace must include:

- inbound and channel metadata;
- context snapshot;
- SDK starting agent;
- SDK handoffs;
- SDK tool calls and outputs;
- SDK guardrail results;
- SDK final proposal;
- Taliya validators;
- repair/escalation if any;
- approved render plan and rendered messages;
- runtime state diff;
- Sales Inbox projection;
- delivery/outbox events;
- model usage and cost.

## File Layout Target

Proposed new module path:

```text
services/taliya-agent-runtime/app/core/taliya_commercial_sdk/
  agents.py
  tools.py
  guardrails.py
  context.py
  output_schema.py
  runner.py
  output_adapter.py
  validators_adapter.py
  trace_adapter.py
  runtime_adapter.py
  __init__.py
```

Rules:

- `agents.py` defines agents, instructions, handoffs, and SDK model settings.
- `tools.py` defines read-only/proposal-only SDK tools.
- `runner.py` calls SDK `Runner`; it must not implement commercial branch logic.
- `output_adapter.py` converts SDK output/run items into `TaliyaTurnProposal`.
- validators/render/persist remain separate and may reuse existing modules after simplification.
- no file may become the new commercial brain.

## Cutover Strategy

1. Build SDK spike isolated from public endpoint.
2. Run critical fixtures locally and with approved paid model budget.
3. Add SDK core behind feature flag.
4. Run SDK shadow mode beside current public path.
5. Compare SDK and current path using golden/do-not-do fixtures.
6. Activate only after approval gates pass.
7. Rollback disables SDK path without re-enabling old runner/TS v2 as public responder.
