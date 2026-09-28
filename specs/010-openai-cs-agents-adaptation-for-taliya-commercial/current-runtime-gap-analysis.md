# Current Runtime Gap Analysis

## Summary

The current Taliya v2 implementation has useful production plumbing, but its conversation brain diverged from the desired OpenAI CS Agents Demo architecture. The replacement should keep integration assets and remove the deterministic response engine from the official path.

## Current Files To Reuse

| File/Area | Reuse Decision |
|-----------|----------------|
| `lib/landing/ai-attendant/whatsapp.ts` | Reuse webhook parsing, Dualhook/Meta coexistence, status handling, outbound send, typing, delay, and idempotency concepts |
| `components/landing/shared/FloatingAiAttendant.tsx` | Reuse widget surface and CTA wiring only; no visual redesign |
| `lib/landing/ai-attendant/leads.ts` | Reuse lead projection ideas and extend for runtime trace fields |
| `lib/landing/ai-attendant/sales-inbox-store.ts` | Reuse Sales Inbox storage and extend with generic runtime records |
| `components/internal/SalesInboxClient.tsx` | Reuse operator UI and add trace/agent/cost summaries |
| `lib/landing/ai-attendant/product-knowledge-source.ts` | Reuse or migrate as official product knowledge source; make it tool-backed |
| `lib/landing/ai-attendant/agent-v2-guardrails.ts` | Reuse hard validation policies as output validators, not as the only guardrail layer |
| `scripts/fixtures/agent-v2/` | Reuse scenario ideas as seed fixtures for new evals |
| `scripts/eval-message-delivery-matrix.mjs` | Reuse delivery smoke concepts, not quality scoring approach |
| Existing Postgres/Sales Inbox tables | Reuse where stable; extend with generic `agent_runtime_*` tables |

## Current Files To Replace Or Quarantine

| File/Area | Replacement Decision |
|-----------|----------------------|
| `lib/landing/floating-agent.ts` v2 routing brain | Replace official v2 conversation path with runtime client call |
| `lib/landing/ai-attendant/agent-v2-loop.ts` | Replace deterministic loop with call to Python agent runtime |
| `lib/landing/ai-attendant/agent-v2-semantic-interpreter.ts` | Remove as brain; any retained preflight must be non-decisional telemetry only |
| `lib/landing/ai-attendant/agent-v2-orchestrator.ts` | Remove as brain; LLM runner and handoffs decide actions |
| `lib/landing/ai-attendant/agent-v2-response-generator.ts` | Remove as normal response mechanism; do not reuse it as the new official template library. Operational fallback wording may be migrated only after review |
| `lib/landing/ai-attendant/agent-v2-tools.ts` | Convert concepts into model-callable Python tools and idempotent persistence |
| `lib/landing/ai-attendant/ai-json.ts` | Replace for official agent turns; structured output comes from runtime |
| `scripts/eval-agent-v2-conversation-matrix.mjs` | Replace static/fixture-only validation with real transcript runner |
| `scripts/eval-agent-v2-quality-judge.mjs` | Replace rubric-only checks with actual judge execution and reports |
| `reports/agent-v2-humanized-transcripts-latest.md` | Keep as regression evidence; do not treat as approval for new runtime |

## Architecture Drift Found

- The current implementation calls local interpretation, orchestration, tool selection, and response generation before normal LLM usage.
- Direct questions and diagnostic flow are handled through hardcoded branches.
- Tools are executed by code-selected actions instead of model-selected function calls.
- Guardrails are useful but mostly deterministic output validators, not a full guardrail architecture.
- Evals pass by checking snippets and expected tree paths, not by measuring real conversation quality.
- Cost is near zero because normal turns avoid model calls, which is a symptom of the wrong architecture for this goal.

## Replacement Principle

Keep the plumbing. Replace the brain.

The new official path is:

```text
channel event -> Next adapter -> HMAC runtime call -> Python Agents SDK runner
  -> LLM triage/specialist decision -> tool calls/handoffs/guardrails
  -> structured JSON output -> persistence/trace -> channel delivery
```

The old official path must not remain:

```text
channel event -> regex interpreter -> state machine -> template response
```

## Corrective Gap After First Runtime Pass

After the first `010` implementation pass, the new runtime did call OpenAI on the non-mock path and produced structured responses. That is necessary, but not sufficient.

Gaps identified at that point:

- The live prompt does not yet carry the full `009` behavior contract for openings, diagnostic timing, waitlist timing, name usage, and voice.
- The runtime does not yet expose enough structured decision fields to audit why a turn offered diagnostic, skipped diagnostic, offered waitlist, used a profile name, or answered a direct question first.
- The real-provider smoke eval did not cover the mapped opening matrix: cold "oi", cold "bom dia", reliable/unreliable profile names, source openings, diagnostic CTA opening, and human-first messages.
- Specialist roles exist conceptually, but the live non-mock path still needs to prove true triage plus role-specific behavior rather than a thin single prompt with a `current_agent` label.
- Validators need to enforce behavior contract violations, not only product-safety violations.
- Cost reports must use current provider pricing before release approval.

Corrective source of truth:

- [behavior-contract.md](./behavior-contract.md)
- [conversation-state-contract.md](./conversation-state-contract.md)
- [message-template-contract.md](./message-template-contract.md)
- [diagnostic-contract.md](./diagnostic-contract.md)
- [sales-inbox-contract.md](./sales-inbox-contract.md)
- [eval-plan.md](./eval-plan.md)
- Final product-owner diagnostic/demo/name correction tasks T206-T226 in [tasks.md](./tasks.md)

Current status: T139-T156 and T158-T204 are historical implementation evidence only. Product-owner review found that those results were not sufficient: the agent still did not prove the approved final diagnostic presentation, demo-state branching, WhatsApp/widget name timing, diagnostic feedback cadence, and updated Sales Inbox completeness. T206-T226 are now the active corrective implementation plan and must pass before product-owner approval or production cutover.
