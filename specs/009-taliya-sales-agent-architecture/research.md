# Research: Taliya Sales Agent Architecture

## Decision: Reuse the existing Next.js app instead of creating a separate agent service

**Rationale**: The current widget, WhatsApp webhook, Sales Inbox and Postgres storage already live in the Next.js application. Keeping the agent inside `lib/landing/ai-attendant` reduces deployment complexity, keeps widget/WhatsApp behavior in one runtime and allows the existing Vercel deployment to remain the release path.

**Alternatives considered**:

- Separate agent microservice: rejected for this v2 release because it adds deployment, auth, tracing and data-sync overhead before the agent behavior is stable.
- External inbox/automation as primary runtime: rejected because Taliya should remain the system of record and the user explicitly removed Airtable as a source of truth.

## Decision: Implement a layered agent loop, not a larger prompt

**Rationale**: The current behavior failed because it mixed greeting, sales policy, diagnostic, persistence and delivery into brittle scripted logic. The new loop separates normalization, state, product knowledge, semantic interpretation, orchestration, tools, response generation, guardrails, persistence and delivery. This matches the OpenAI customer-service agent architecture pattern while keeping Taliya-specific policy.

**Alternatives considered**:

- One stronger model with a huge prompt: rejected because it increases cost and still lacks deterministic idempotency, state, guardrails and traceability.
- Regex-heavy intent tree: rejected because real leads send ambiguous, mixed and out-of-order messages.

## Decision: Use Postgres/Supabase as the source of truth for all lead state

**Rationale**: The Sales Inbox already depends on backend persistence, and future Taliya system data will also need a durable database. Postgres can store structured relational fields plus JSONB substate/traces while the schema stabilizes.

**Alternatives considered**:

- Airtable: rejected because the user no longer wants it and it would create duplicate truth.
- n8n as lead system: rejected because n8n should only be an optional integration/automation layer later, not lead memory.
- Local/session-only storage: rejected because WhatsApp, follow-up, handoff and waitlist need durable records.

## Decision: Store official product knowledge as a versioned source used by tools

**Rationale**: Plans, prices, links, demo status, availability, privacy and unsupported claims must not live only in prompts. A typed source gives both widget and WhatsApp the same commercial truth and allows traces to record `sourceVersion`.

**Alternatives considered**:

- Prompt-only product facts: rejected because the model can drift or invent.
- Hardcoded strings scattered in components/routes: rejected because it causes widget/WhatsApp inconsistency.

## Decision: Introduce macro state plus substate instead of relying on current commercial stages alone

**Rationale**: The existing `CommercialStage` values are useful but not enough to prevent repeated questions, diagnostic restarts, waitlist restarts and lost topic changes. The new substate stores asked questions, known facts, pending question, diagnostic step, missing fields, last answered direct question, sentiment, confidence and queued/suppressed response status.

**Alternatives considered**:

- Replace all old state immediately: rejected because it increases migration risk.
- Keep only the old stage enum: rejected because it cannot represent required memory and quality gates.

## Decision: Default to the current low-cost model path and escalate only by orchestrator decision

**Rationale**: Quality should come from better architecture, compact context, official data and evals before using more expensive models. A stronger model is reserved for low-confidence, conflicting, high-intent, safety-sensitive or recovery turns, with logged reason.

**Alternatives considered**:

- Always use stronger model: rejected because lead and eval cost would be too high.
- Never escalate: rejected because messy real conversations and safety cases need a reliable recovery path.

## Decision: Enforce a hard per-lead automatic AI cost cap

**Rationale**: The user wants high quality without runaway cost. The cap is part of product behavior, not just monitoring. At or above US$0.15, the agent must stop automatic generation, preserve context, log the cap and send only the approved fallback if needed.

**Alternatives considered**:

- Alert only: rejected because alerts do not stop runaway conversations.
- Lower hard cap: rejected for now because long diagnostic or complex leads may need room while still staying bounded.

## Decision: Use layered tests plus realistic transcript evals

**Rationale**: The old agent passed narrow tests but felt robotic. The new suite must test components independently and integrated transcripts with scoring, blocking failures, cost estimates, state transitions and tool/source traces.

**Alternatives considered**:

- Deterministic mocks only: rejected because the user explicitly wants realistic simulation, not purely mocked deterministic behavior.
- Manual testing only: rejected because regressions across widget/WhatsApp/state/guardrails would be easy to miss.

## Decision: Bound real-model eval spend with runner-level limits

**Rationale**: The user wants realistic simulation, but not unlimited test spend. The runner should validate fixtures cheaply first, then run a controlled subset or full matrix with explicit max scenarios, max real-model calls and max estimated cost.

**Alternatives considered**:

- Full real-model matrix with no budget: rejected because cost could grow unexpectedly.
- Mock-only evals: rejected because the user explicitly wants realistic quality simulation.

## Decision: Keep real WhatsApp manual tests after deploy

**Rationale**: Local tests can validate normalization, webhook payloads, delivery intent and traces, but true WhatsApp typing/delay, provider behavior and Business App coexistence must be validated in production/staging after deploy.

**Alternatives considered**:

- Pretend local tests prove full WhatsApp behavior: rejected because provider behavior and Dualhook/Meta details are external.
- Use WhatsApp tests before deploy: rejected because live WhatsApp requires deployed webhook and production env.
