# Implementation Plan: Humanized Sales And Waitlist Flow

**Branch**: `007-humanized-sales-waitlist-flow` | **Date**: 2026-05-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/007-humanized-sales-waitlist-flow/spec.md`

## Summary

Adjust the existing Taliya floating AI sales attendant so web widget and WhatsApp share the same agent brain but use channel-specific conversation policy. WhatsApp must start like human atendimento: ask name, then pain/intent, then offer free diagnostic. Waitlist must only appear after high intent: positive response after diagnostic, positive response after demo, or explicit contract/start request with minimum context. Add commercial stage and waitlist/demo state to storage and require realistic review simulations before release. Waitlist offered and waitlist joined are separate states.

## Technical Context

**Language/Version**: TypeScript, React, Next.js App Router.
**Primary Dependencies**: Existing Next.js app, existing AI attendant modules, OpenAI provider path, Meta WhatsApp route, pg/Postgres storage.
**Storage**: Supabase/Postgres through the existing storage layer, with JSON-friendly extension for lead commercial state.
**Testing**: Existing npm scripts, TypeScript, ESLint, Next build, existing eval scripts plus new/updated scenario harness.
**Target Platform**: Vercel production for public landing and API routes; Supabase for persistence.
**Project Type**: Web application with API routes and sales agent runtime.
**Performance Goals**: No noticeable additional latency beyond current AI provider call; deterministic gates should run before provider calls when possible.
**Constraints**: Protected `/pilates` layout must not be visually redesigned; WhatsApp must respect 24h window, human takeover and direct Meta webhook validation; waitlist must not promise immediate availability or dates.
**Scale/Scope**: One Taliya WhatsApp number and current public widget only. No client/studio WhatsApp onboarding and no seven-agent tenant runtime in this feature.
**Branch Prerequisite**: Before implementation, switch to a Spec Kit-compatible feature branch such as `007-humanized-sales-waitlist-flow` or create an agreed Codex branch and account for the Spec Kit prerequisite script behavior.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Existing Spec Kit source of truth is present. This feature is a focused extension of `002-floating-ai-sales-agent`.
- Protected `/pilates` visual layout remains unchanged.
- Data storage changes must preserve future multi-tenant readiness without implementing multi-tenant onboarding now.
- Security and privacy rules from `005-security-code-data` apply: avoid raw sensitive logging, respect opt-out, do not leak prompts or secrets.
- No checkout/open availability claim may be introduced while waitlist mode is active.

## Project Structure

### Documentation (this feature)

```text
specs/007-humanized-sales-waitlist-flow/
├── spec.md
├── plan.md
├── tasks.md
├── simulation-review-matrix.md
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```text
app/
├── api/landing/ai-attendant/route.ts
├── api/landing/ai-attendant/whatsapp/route.ts
└── api/internal/sales-inbox/leads/

lib/landing/
├── floating-agent.ts
└── ai-attendant/
    ├── channels.ts
    ├── context.ts
    ├── conversion-gates.ts
    ├── crm-diagnostic.ts
    ├── leads.ts
    ├── sales-cadence.ts
    ├── sales-inbox-store.ts
    ├── schema.ts
    ├── session-store.ts
    ├── storage/postgres.ts
    └── whatsapp.ts

scripts/
├── eval-ai-sales-humanization.mjs
├── eval-conversation-route-matrix.mjs
└── eval-whatsapp-webhook.mjs

scripts/sql/
└── 002_ai_attendant_commercial_stage_waitlist.sql
```

**Structure Decision**: Implement in the existing landing AI attendant runtime. Prefer extending schema/store/state contracts over adding a separate WhatsApp agent. Add simulations in Spec Kit docs first, then encode the highest-risk simulations into eval scripts.

## Phase 0 Research

No external product research is required before implementation. The key product decisions are already captured by the user:

- WhatsApp should feel like human atendimento.
- Name comes before pain/intent.
- Pain/intent comes before diagnostic offer.
- Waitlist is only after total or near-total interest.
- Demo is an intermediate proof step for uncertainty after diagnostic.
- Same agent brain must remain shared across widget and WhatsApp.

Research output is embedded in [simulation-review-matrix.md](./simulation-review-matrix.md) as concrete behavioral expectations.

## Phase 1 Design

### Conversation State Design

Use a lightweight commercial stage model:

- `awaiting_name`
- `awaiting_pain_or_intent`
- `diagnostic_offered`
- `diagnostic_in_progress`
- `diagnostic_completed`
- `recommendation_validation`
- `demo_offered`
- `demo_seen`
- `waitlist_eligible`
- `waitlist_offered`
- `waitlist_pending_details`
- `waitlist_joined`
- `waitlist_declined`
- `human_handoff`

The visible conversation should not expose these stage names. They are internal gates for the AI and storage.

### Waitlist Gate Design

Waitlist may be offered only when:

- diagnostic recommendation was delivered and the lead responds positively;
- demo was offered/seen and the lead responds positively;
- lead explicitly asks to start/contract and minimum context is known;
- operator manually marks or invites waitlist.

Minimum context for a non-cold waitlist offer is:

- person name, and
- at least one pain/intent, and
- one of: completed diagnostic recommendation, positive demo signal, explicit contract/start request, or operator decision.

Waitlist status transitions:

```text
not_offered -> eligible -> offered -> joined
                              |       ^
                              |       |
                              -> pending_details
                              -> declined
                              -> undecided
```

`joined` is allowed only after explicit lead agreement. If required details are missing after agreement, use `pending_details` until they are collected.

Waitlist must not be offered:

- on first greeting;
- before name;
- before pain/intent;
- immediately after diagnostic before the lead reacts;
- after a negative/uncertain diagnostic or demo response.

### Review Gate Design

The release must pass six review stages:

1. **R0 Spec Review**: Product owner reviews this spec and simulation matrix.
2. **R1 Static/Eval Review**: Automated evals for P1 paths pass locally.
3. **R2 Local API Simulation**: Local Next server with mock provider validates widget and WhatsApp policy.
4. **R3 Production-Like Webhook Simulation**: WhatsApp webhook route is tested with signed/mock Meta payloads and storage checks.
5. **R4 Real Number Smoke Review**: Taliya WhatsApp number is cleaned for test, then real conversation validates cold start, name, pain/intent and diagnostic offer.
6. **R5 Product Owner Transcript Review**: Product owner reviews required realistic transcripts and approves or requests copy/flow fixes.

### Implementation Discovery Policy

Implementation discoveries are expected and must be handled explicitly. Any discovered missing case, state transition, storage need or safety issue must be classified as clarification, in-scope behavior gap or out-of-scope expansion. In-scope behavior gaps require an update to the relevant Spec Kit artifact and at least one simulation/eval amendment when agent behavior changes. Out-of-scope expansions are deferred unless the product owner explicitly approves a new scope.

### Storage Contract Design

Prefer storing state in the existing lead JSON data if that keeps migrations smaller, but expose stable fields through the store/API contract:

- `commercialStage`
- `waitlistStatus`
- `waitlistOfferedAt`
- `waitlistJoinedAt`
- `waitlistDeclinedAt`
- `diagnosticStatus`
- `diagnosticCompletedAt`
- `demoStatus`
- `demoOfferedAt`
- `demoSeenAt`
- `leadSourceChannel`
- `leadSourceDetail`
- `primaryPainOrIntent`
- `nextAction`

If fields need filtering or sorting in the Sales Inbox, add explicit columns or generated indexes instead of burying everything in unindexed JSON.

## Phase 2 Implementation Strategy

Implement in slices:

1. Add/normalize schema fields for commercial stage, waitlist status and demo status.
2. Update prompt/context and deterministic gates for WhatsApp name-first flow.
3. Update diagnostic completion gates so recommendation asks for validation before waitlist.
4. Add waitlist path and storage updates.
5. Update Sales Inbox/internal lead route to expose stage/waitlist fields.
6. Add widget-specific and WhatsApp-specific eval scenarios.
7. Encode simulation matrix into eval fixtures/scripts.
8. Run review stages and only then publish.

## Complexity Tracking

No constitution violations expected. The feature extends existing agent architecture and existing storage.
