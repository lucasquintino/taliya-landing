# Implementation Plan: Taliya Sales Agent Architecture

**Branch**: `009-taliya-sales-agent-architecture` | **Date**: 2026-05-21 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/009-taliya-sales-agent-architecture/spec.md`

**Note**: This plan covers architecture and implementation preparation only. Code implementation must be generated from `tasks.md` after this plan is complete.

## Summary

Replace the current ad-hoc/scripted commercial assistant with a layered, cost-aware Taliya sales agent shared by the landing widget and Taliya-owned WhatsApp. The new architecture keeps the same business scope: one commercial lead agent for Taliya, one Taliya WhatsApp Business number, Postgres/Sales Inbox persistence, no client/studio WhatsApp onboarding, no future customer agents yet and no `/pilates` visual redesign.

The implementation will reuse the existing Next.js App Router endpoints, `lib/landing/ai-attendant` runtime, Supabase/Postgres storage and Sales Inbox UI where possible. The new design introduces explicit channel adapters, event normalization/idempotency, macro state plus substate, official product knowledge source, semantic interpretation, orchestrator decisions, idempotent internal tools, response generation, deterministic guardrails, channel-specific delivery, traces, cost caps and a realistic eval runner.

## Technical Context

**Language/Version**: TypeScript on Next.js App Router 16.2.4 and React 19.2.4. Next.js APIs must be checked in `node_modules/next/dist/docs/` before changing route/runtime code.  
**Primary Dependencies**: Existing Next.js app, OpenAI Responses API provider in `lib/landing/ai-attendant/provider.ts`, `pg` for Postgres/Supabase, existing WhatsApp Cloud/Dualhook webhook integration, existing eval scripts under `scripts/`.  
**Storage**: Supabase/Postgres as source of truth for leads, conversations, messages, diagnostic, waitlist, traces, model usage and idempotency. Airtable/n8n must not be source of truth for this feature.  
**Testing**: Existing `npm run lint` plus focused unit/integration scripts for product knowledge, state/substate, idempotency, tools, guardrails, delivery, eval runner and integrated realistic transcripts. Real WhatsApp manual tests happen only after deploy.  
**Target Platform**: Vercel-hosted Next.js app, browser widget, WhatsApp Cloud API via Taliya-owned WhatsApp Business number and Dualhook-managed coexistence.  
**Project Type**: Full-stack web app with backend API routes, AI-agent runtime, internal Sales Inbox UI and browser/WhatsApp channel adapters.  
**Performance Goals**: Persist inbound event quickly, deduplicate retries, keep normal AI turn within existing provider timeout budget, respect WhatsApp typing/delay bounds and keep 90%+ production-intended turns on default low-cost path while passing P1 quality gates.  
**Constraints**: Preserve `/pilates` layout and visual design; no multi-tenant client onboarding; no seven customer agents; no checkout while broad availability is closed; no WhatsApp phone request; no template/marketing outside 24h unless explicitly added later; hard automatic AI cost cap of US$0.15 per lead conversation.  
**Scale/Scope**: Initial scope is one Taliya-owned WhatsApp number plus landing widget, with expected early lead volume around hundreds to low thousands/month. Architecture should prepare future multi-tenant support through explicit channel, identity and product/source abstractions without implementing customer tenant onboarding now.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The project constitution file is still a placeholder and defines no enforceable gates. Project-specific gates for this feature come from `AGENTS.md`, `spec.md`, `conversation-policy.md` and `scenario-matrix.md`.

Pre-design gate status:

- PASS: Scope remains one Taliya commercial agent and one Taliya WhatsApp number.
- PASS: `/pilates` visual/layout redesign is out of scope and explicitly blocked.
- PASS: Product facts, prices and links must come from an official source instead of prompt-only memory.
- PASS: Human handoff, cost cap, idempotency, persistence and evals are first-class requirements.
- PASS: No shadow mode or controlled rollout phases are included because the user rejected those phases.
- PASS WITH CAUTION: Existing `CommercialStage` and runtime types do not match the new macro/substate model; implementation must introduce a compatibility/migration layer rather than rewriting state blindly.

## Project Structure

### Documentation (this feature)

```text
specs/009-taliya-sales-agent-architecture/
├── plan.md
├── spec.md
├── conversation-policy.md
├── scenario-matrix.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── agent-loop-contract.md
│   ├── api-channel-contracts.md
│   ├── eval-contract.md
│   ├── product-knowledge-contract.md
│   ├── state-and-tools-contract.md
│   └── trace-and-cost-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
app/
├── api/
│   ├── landing/ai-attendant/
│   │   ├── route.ts
│   │   └── whatsapp/route.ts
│   └── internal/sales-inbox/
components/
├── landing/shared/FloatingAiAttendant*.tsx
└── internal/SalesInboxClient.tsx
lib/
└── landing/ai-attendant/
    ├── provider.ts
    ├── schema.ts
    ├── whatsapp.ts
    ├── sales-inbox-store.ts
    ├── storage/postgres.ts
    └── new agent architecture modules to be added under this boundary
scripts/
├── eval-*.mjs
├── cleanup-ai-test-data.*
└── sql/
```

**Structure Decision**: Implement inside the existing Next.js application and `lib/landing/ai-attendant` boundary. Do not create a separate agent service for this v2 release. Keep channel-specific code near existing widget/WhatsApp routes and keep commercial reasoning in shared agent runtime modules.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Layered agent runtime instead of a single prompt | Required to handle direct questions, diagnostic, waitlist, handoff, persistence, idempotency, cost cap and quality gates without regressions | The existing prompt/script approach already passed some tests while still feeling robotic and brittle |
| Versioned state/substate and trace records | Required to prevent repeated questions, waitlist restarts, duplicate actions and un-debuggable failures | Macro stage alone cannot represent pending question, known facts, asked questions, cost state and handoff status |
| Realistic eval runner with judge rubric | Required because exact/keyword tests missed tone and conversation-quality bugs | Deterministic string tests alone cannot validate naturalness, directness and consultative quality |

## Phase 0 Research Summary

See [research.md](./research.md). All technical unknowns are resolved with implementation decisions: reuse the current Next.js backend, use Postgres as source of truth, introduce a layered agent runtime, keep default low-cost model path, store official product knowledge as versioned data/config and validate with layered plus integrated evals.

## Phase 1 Design Summary

See [data-model.md](./data-model.md) and [contracts/](./contracts/). The design defines macro state, substate, diagnostic schema, waitlist data quality, product source contract, agent loop, idempotent tool actions, channel contracts, trace/cost records and eval gates.

## Post-Design Constitution Check

- PASS: No unresolved `NEEDS CLARIFICATION` remains in plan artifacts.
- PASS: Design preserves `/pilates` visual/layout constraints.
- PASS: Architecture remains one Taliya agent for widget and WhatsApp only.
- PASS: Human handoff, cost cap, idempotency and official product knowledge are explicit implementation contracts.
- PASS: Evaluation gates are strict enough to block production replacement when the agent feels mediocre, repeats questions, invents facts, restarts state or exceeds cost policy.
