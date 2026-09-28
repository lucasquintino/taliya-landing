# Implementation Plan: OpenAI CS Agents Adaptation For Taliya Commercial

**Branch**: `codex/010-openai-cs-agents-adaptation-for-taliya-commercial` | **Date**: 2026-05-22 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/010-openai-cs-agents-adaptation-for-taliya-commercial/spec.md`

**Note**: This plan covers architecture and implementation preparation only. Product code implementation must follow `tasks.md` after this plan is accepted.

## Summary

Replace the current deterministic Taliya commercial agent with a new LLM-first runtime that faithfully adapts the OpenAI Customer Service Agents Demo architecture. The new runtime runs as a Python service on Railway, exposes a generic `agent_key` based API, implements only the `taliya_commercial` agent now, and keeps Next/Vercel responsible for `/pilates`, widget, WhatsApp webhook, and Sales Inbox. Existing channel adapters, persistence concepts, Sales Inbox, product knowledge, waitlist, guardrails, and delivery behavior are reused where they help; deterministic conversation flow, regex-as-brain, state-machine response generation, and string-only evals are replaced. Approved message templates are retained as the official voice, but the LLM must choose templates and variables through structured output.

Corrective update: the first implementation pass proved the runtime/provider path, but product-owner review found that the full behavior contract from `009` had not been ported strongly enough. This plan now requires [behavior-contract.md](./behavior-contract.md), [conversation-state-contract.md](./conversation-state-contract.md), [message-template-contract.md](./message-template-contract.md), [diagnostic-contract.md](./diagnostic-contract.md), and [sales-inbox-contract.md](./sales-inbox-contract.md) before additional implementation claims can be treated as production-ready.

Final product-owner correction update: later transcript review found that automated passes still did not enforce the approved final diagnostic presentation, demo-state branch, name timing, or diagnostic question feedback cadence. The new T206-T226 phase in [tasks.md](./tasks.md) is now required before production approval. Previous `12/12`, `28/28`, Sales Inbox, and local pass results are historical evidence only for this final correction phase.

## Technical Context

**Language/Version**: Python 3.12 for `services/taliya-agent-runtime`; TypeScript on Next.js App Router 16.2.4 and React 19.2.4 for existing channel/UI integration. Next.js APIs must be checked in `node_modules/next/dist/docs/` before changing route/runtime code.  
**Primary Dependencies**: OpenAI Agents SDK architecture from `openai/openai-cs-agents-demo`, FastAPI ASGI server, Pydantic, Postgres client, pytest, existing Next.js app, existing WhatsApp Cloud/Dualhook integration, existing Sales Inbox, existing `pg`-based storage, existing eval scripts as migration input.  
**Storage**: Immediate focus is complete lead/Sales Inbox correctness, transcript durability, diagnostic ledger, waitlist status, handoff state, idempotency, product source versions, and minimal runtime observability. Full durable runtime replay/tracing tables can be completed after behavior is correct, but no production path may lose lead facts, diagnostic state, waitlist state, or handoff state. Existing Sales Inbox storage remains, extended by generic `agent_runtime_*` records where needed.  
**Testing**: Python unit/contract/integration tests for runtime; existing `npm run lint` for Next changes; focused TypeScript tests/evals for channel adapters; end-to-end transcript evals with deterministic invariants and LLM judge scoring; real WhatsApp smoke tests after deploy.  
**Target Platform**: Vercel-hosted Next.js app plus Railway-hosted Python runtime, serving browser widget and Taliya-owned WhatsApp Business number only.  
**Project Type**: Multi-service web application with a Python agent runtime, existing Next.js public app/API routes, internal Sales Inbox UI, and shared Postgres persistence.  
**Performance Goals**: Normal lead turn completes within the 60s runtime timeout; WhatsApp duplicate retries produce zero duplicate replies; most simple turns remain in the default model path; automatic conversation cost stays below configured target bands and stops at hard cap.  
**Constraints**: Preserve protected `/pilates` layout; no multi-tenant studio onboarding; no client WhatsApp connections; no seven studio agents; no checkout invention; no WhatsApp phone request; no legacy deterministic conversational fallback; HMAC required between Next and Railway; traces/logs must redact secrets and unnecessary raw provider payloads.  
**Scale/Scope**: Initial production scope is one Taliya-owned WhatsApp number plus the landing widget, expected early volume from hundreds to low thousands of leads/month. Runtime naming and storage must support future agent families without implementing them in this feature.

## Constitution Check

The local constitution file is still a template, so this feature applies the project-specific gates from `AGENTS.md`, prior specs, and user decisions:

- **Protected landing gate**: PASS. `/pilates` visual/layout direction must be preserved. Any task that can affect landing behavior must capture or confirm desktop and mobile baseline before code changes.
- **Next.js docs gate**: PASS. Any future Next.js API/runtime edit must first read relevant docs under `node_modules/next/dist/docs/`.
- **Scope gate**: PASS. Only `taliya_commercial` is implemented now. Multi-tenant studio agents, client WhatsApp numbers, and the seven future studio agents are out of scope.
- **Reference fidelity gate**: PASS. The OpenAI CS Agents Demo is a binding architecture reference, not vague inspiration.
- **Source of truth gate**: PASS. Product knowledge and Postgres/Sales Inbox remain the official facts and operational records.
- **Fallback gate**: PASS. The old deterministic runtime is not a production conversational fallback.

## Project Structure

### Documentation (this feature)

```text
specs/010-openai-cs-agents-adaptation-for-taliya-commercial/
|-- spec.md
|-- plan.md
|-- research.md
|-- data-model.md
|-- behavior-contract.md
|-- conversation-state-contract.md
|-- message-template-contract.md
|-- diagnostic-contract.md
|-- sales-inbox-contract.md
|-- quickstart.md
|-- reference-map.md
|-- current-runtime-gap-analysis.md
|-- eval-plan.md
|-- rollout-and-deploy.md
|-- checklists/
|   `-- requirements.md
|-- contracts/
|   |-- agent-runtime-api.md
|   |-- channel-adapters.md
|   |-- structured-output.md
|   |-- tools-and-guardrails.md
|   |-- memory-store.md
|   |-- product-knowledge.md
|   `-- eval-contract.md
|-- eval-reports/
`-- tasks.md
```

### Source Code (repository root)

```text
services/
`-- taliya-agent-runtime/
    |-- Dockerfile
    |-- railway.toml
    |-- pyproject.toml
    |-- README.md
    |-- app/
    |   |-- main.py
    |   |-- settings.py
    |   |-- auth/
    |   |   `-- hmac.py
    |   |-- runtime/
    |   |   |-- runner.py
    |   |   |-- registry.py
    |   |   |-- schemas.py
    |   |   |-- events.py
    |   |   `-- usage.py
    |   |-- shared/
    |   |   |-- memory/
    |   |   |   `-- postgres.py
    |   |   |-- product_knowledge/
    |   |   |   `-- source.py
    |   |   `-- guardrails/
    |   |       `-- validators.py
    |   `-- domains/
    |       `-- taliya_commercial/
    |           |-- agents.py
    |           |-- context.py
    |           |-- tools.py
    |           |-- guardrails.py
    |           |-- prompts.py
    |           |-- behavior_policy.py
    |           |-- templates.py
    |           |-- renderer.py
    |           |-- diagnostic_ledger.py
    |           `-- evals.py
    |-- migrations/
    `-- tests/

app/
|-- api/landing/ai-attendant/route.ts
|-- api/landing/ai-attendant/whatsapp/route.ts
`-- api/internal/sales-inbox/

lib/landing/ai-attendant/
|-- runtime-client.ts
|-- whatsapp.ts
|-- leads.ts
|-- sales-inbox-store.ts
|-- storage/
`-- product-knowledge-source.ts

components/internal/SalesInboxClient.tsx
components/landing/shared/FloatingAiAttendant.tsx
scripts/
|-- eval-agent-runtime-*.mjs
`-- fixtures/agent-runtime/
```

**Structure Decision**: Add a Python service under `services/taliya-agent-runtime` to preserve the reference architecture and avoid re-creating a manual agent runner inside Next.js. Keep Next.js as the channel/UI layer and do not redesign `/pilates`. Use generic runtime names and `agent_key` routing from the start.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|--------------------------------------|
| Add a second service | The reference architecture is Python/Agents SDK based and the user explicitly wants a faithful adaptation instead of another TypeScript state machine | Keeping everything inside Next already produced deterministic flow and would weaken the 99% reference requirement |
| Generic runtime naming before multiple agents exist | Future Taliya configuration and studio operation agents are expected | Naming everything around sales now would create avoidable migration debt |
| HMAC service-to-service auth | Runtime will be called from public-facing Next routes | A bearer-only secret is easier to leak/replay and does not protect request body integrity |

## Phase 0 Research Summary

See [research.md](./research.md). Key decisions are: Python runtime on Railway, generic `/v1/agent-runs`, HMAC auth, `taliya_commercial` as first active agent key, generic `agent_runtime_*` storage, product knowledge as source of truth, and no legacy conversational fallback.

## Phase 1 Design Summary

See [data-model.md](./data-model.md) and [contracts](./contracts/). The design introduces durable agent runs, structured output, agent registry, model-callable tools, guardrail events, product source versions, and Sales Inbox projections.

## Phase 2 Corrective Behavior Realignment

This phase is mandatory before production readiness and supersedes any earlier "passed locally" interpretation.

### Behavior Source

[behavior-contract.md](./behavior-contract.md) is the binding behavior source. It ports the earlier `009` conversation policy and scenario matrix into the `010` implementation track. It is supported by:

- [conversation-state-contract.md](./conversation-state-contract.md) for canonical states and transitions.
- [message-template-contract.md](./message-template-contract.md) for template IDs, variables, renderer, and channel delivery rules.
- [diagnostic-contract.md](./diagnostic-contract.md) for mandatory diagnostic questions and no-repeat behavior.
- [sales-inbox-contract.md](./sales-inbox-contract.md) for lead persistence completeness.

### Runtime Shape

The commercial runtime exposes one logical agent family:

```text
taliya_commercial_triage
  -> taliya_commercial_entry_agent
  -> taliya_commercial_product_agent
  -> taliya_commercial_diagnostic_agent
  -> taliya_commercial_waitlist_agent
  -> taliya_commercial_handoff_agent
```

Architecture clarification: the current production candidate is an LLM-first conductor runtime, not a multi-call specialist handoff loop. Normal commercial turns should use one default-model operation unless repair, escalation, or judge/eval execution is needed. The model receives the specialist role definitions and returns structured JSON with route, current specialist role, facts, state, tool intent, template IDs, and variables. Code then validates, renders approved templates, executes tool boundaries, persists state, and delivers channel-specific messages.

This is intentional for the current scope: it preserves LLM-first commercial judgment while keeping latency, cost, state management, and transcript debugging manageable. The specialist split is used for behavior ownership, traceability, and eval coverage. It should not be described as full OpenAI Agents SDK agent-to-agent handoff execution unless the runtime is later changed so separate SDK agents run and hand off across the turn.

### Required Code Adjustments

- Add a domain policy pack under `services/taliya-agent-runtime/app/domains/taliya_commercial/behavior_policy.py`.
- Add template library and renderer modules under `services/taliya-agent-runtime/app/domains/taliya_commercial/templates.py` and `renderer.py`.
- Expand structured output in `services/taliya-agent-runtime/app/runtime/schemas.py` and `runner.py` with previous/current/next state, route, opening type, intents, direct-question status, diagnostic action, waitlist eligibility, profile-name usage, template ids, template variables, facts, next-question kind, and policy checks.
- Update `services/taliya-agent-runtime/app/domains/taliya_commercial/prompts.py` so the LLM receives the behavior contract, role-specific instructions, and source/opening policy.
- Ensure the live non-mock path actually uses the triage/specialist role definitions instead of a single thin prompt with only a `current_agent` label.
- Add behavior validators to `services/taliya-agent-runtime/app/shared/guardrails/validators.py` or domain guardrails.
- Add a diagnostic ledger module that tracks mandatory questions, prior answers, evidence, missing facts, and no-repeat rules.
- Update diagnostic schema to include ledger status, evidence, internal main bottleneck, natural-language pain/context reading, likely cause, CRM base recommendation, first operational step, indicated routines/agents one by one, dynamic plan recommendation line, demo status at delivery, dynamic demo line, confidence, and unknowns.
- Update runtime state and Sales Inbox projection with demo state: `not_offered`, `offered`, `viewed_or_asked`, or `reacted_positive`.
- Enforce WhatsApp/widget name timing: reliable WhatsApp profile name may be used; unreliable profile names are ignored; cold greetings do not ask name; qualified diagnostic entry may ask name without blocking value.
- Enforce diagnostic question feedback cadence before the first and subsequent diagnostic questions.
- Update Sales Inbox projection so every meaningful turn persists the required fields in [sales-inbox-contract.md](./sales-inbox-contract.md).
- Enforce widget/WhatsApp delivery rules: short chunks in both channels, widget buttons where valid, WhatsApp text/official links instead of buttons, typing/delay in both existing delivery surfaces where supported.
- Update cost pricing in `services/taliya-agent-runtime/app/runtime/usage.py` before trusting cost reports.

### Required Eval Adjustments

- Add real-provider fixtures for cold openings, source openings, diagnostic-first paths, direct questions, profile-name use, waitlist timing, and handoff.
- Add zero-cost fixture and invariant coverage for state transitions, template selection, diagnostic no-repeat, waitlist clear-contract-intent, Sales Inbox completeness, idempotency, rapid-message ordering, and channel delivery shape.
- Ensure final reports include full visible transcripts, route, specialist role, policy checks, model usage, and cost.
- Treat prior `real-openai` smoke results as integration evidence only, not final behavior approval.

## Post-Design Constitution Check

- **Protected landing gate**: PASS. Tasks include baseline confirmation and prohibit visual redesign.
- **Scope gate**: PASS. Future agents are reserved by naming only.
- **Reference fidelity gate**: PASS. `reference-map.md` maps the OpenAI demo structure to planned Taliya files.
- **Fallback gate**: PASS. Tasks remove the old deterministic brain from official production path.
- **Behavior contract gate**: NOT PASSED for production until the final product-owner correction tasks T206-T226 are implemented and verified. Prior tasks T139-T204 are historical evidence only for this correction.
- **Eval gate**: NOT PASSED for production until zero-cost gates pass, quota-limited real OpenAI correction scenarios pass, the updated mapped behavior matrix passes, Sales Inbox completeness includes demo/final diagnostic fields, and product-owner transcript approval is recorded.

## Phase 3 Product Explanation And Follow-Up Delta

This phase is governed by [product-followup-delta-contract.md](./product-followup-delta-contract.md). It covers only missing or partial behavior discovered after the approved diagnostic/demo/name correction pass.

### Scope

Implement:

- product explanation for "como funciona?" and related questions as a product route, not an opening route;
- official product knowledge for how Taliya works, routine areas, WhatsApp Business scope, integration scope, comparisons, security/data, availability/onboarding, and out-of-profile handling;
- compact post-diagnostic context so follow-up conversation uses saved diagnostic memory without restarting diagnostic;
- conversation resume behavior for "pode continuar", plan recall, and post-diagnostic follow-up;
- comparison with current tools without attacking or inventing migration/integration;
- integration and WhatsApp scope answers without overpromising;
- conservative security/data answers based only on official facts;
- diagnostic refusal behavior;
- general objections through LLM+policy before adding any new objection template.

Do not implement:

- new `/pilates` layout or visual changes;
- customer/studio WhatsApp connection flows;
- multi-tenant studio behavior;
- the seven future studio operation agents;
- deterministic commercial routing by regex or phrase list;
- broad rewrites of approved openings, price, demo, diagnostic, waitlist, handoff, or safety paths.

### Cost And Quality Constraints

- Existing protected routes should keep the same or materially unchanged prompt payload, latency, and cost.
- New product knowledge must be retrieved selectively by topic.
- Normal commercial turns should remain one model operation unless repair/escalation is needed.
- New templates must reduce copy drift without replacing LLM interpretation.
- Regression gates must prove protected behavior did not degrade.

### Implementation Shape

1. Add new product knowledge keys to the runtime product knowledge source.
2. Add the new product templates defined in the delta contract.
3. Update behavior policy and prompts so the LLM can choose the new intents and templates.
4. Add compact `post_diagnostic_context` to the LLM payload only after diagnostic delivery.
5. Update selective product-knowledge retrieval.
6. Add validators for new template variables and unsupported claims.
7. Add zero-cost evals and quota-limited real OpenAI transcripts for the new routes.
8. Run protected-route regression before production approval.

### Additional Constitution Check

- **LLM-first gate**: NOT PASSED until tests prove new product explanation, comparison, integration, security, out-of-profile, and post-diagnostic routes are selected by LLM structured decisions rather than deterministic commercial shortcuts.
- **Protected route gate**: NOT PASSED until approved openings, price, demo, diagnostic, waitlist, handoff, safety, and Sales Inbox regressions pass after the delta.
- **Cost gate**: NOT PASSED until reports show protected-route cost/latency did not materially increase and new routes remain within configured caps.
