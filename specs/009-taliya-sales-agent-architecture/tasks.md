# Tasks: Taliya Sales Agent Architecture

**Input**: Design documents from `/specs/009-taliya-sales-agent-architecture/`  
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `conversation-policy.md`, `scenario-matrix.md`  
**Tests**: Required. The spec requires layer tests, integrated realistic simulations, transcripts, rubric scores, cost estimates and manual widget/WhatsApp review gates.

## Phase 1: Setup And Baseline

**Purpose**: Confirm constraints, preserve the protected landing and prepare implementation files.

- [X] T001 Read required context in `AGENTS.md`, `specs/009-taliya-sales-agent-architecture/spec.md`, `specs/009-taliya-sales-agent-architecture/conversation-policy.md`, `specs/009-taliya-sales-agent-architecture/scenario-matrix.md`, `specs/002-floating-ai-sales-agent/spec.md`, `specs/002-floating-ai-sales-agent/tasks.md`, `specs/001-niche-landing-system/spec.md`
- [X] T002 Read relevant Next.js route/runtime docs in `node_modules/next/dist/docs/`
- [X] T003 Capture or confirm protected `/pilates` desktop and mobile baseline in `specs/009-taliya-sales-agent-architecture/baseline.md`
- [X] T004 [P] Create implementation notes for current agent/runtime files in `specs/009-taliya-sales-agent-architecture/current-runtime-audit.md`
- [X] T005 [P] Implement and document v2 feature flags, capture-only mode and kill switch in `lib/landing/ai-attendant/agent-v2-flags.ts` and `docs/landing-agentes-pilates/source/taliya-agent-v2-env.md`
- [X] T006 Add required npm script entries for v2 evals in `package.json`

---

## Phase 2: Foundational Architecture

**Purpose**: Blocking shared infrastructure. No user story implementation should start before this phase is complete.

### Tests First

- [X] T007 [P] Add product knowledge contract tests in `scripts/eval-agent-v2-product-knowledge.mjs`
- [X] T008 [P] Add state/substate contract tests in `scripts/eval-agent-v2-state.mjs`
- [X] T009 [P] Add idempotency contract tests in `scripts/eval-agent-v2-idempotency.mjs`
- [X] T010 [P] Add guardrail contract tests in `scripts/eval-agent-v2-guardrails.mjs`
- [X] T011 [P] Add cost policy contract tests in `scripts/eval-agent-v2-cost.mjs`
- [X] T012 [P] Add trace completeness contract tests in `scripts/eval-agent-v2-trace.mjs`

### Implementation

- [X] T013 Create Postgres migration plus verification and rollback notes for agent v2 state, traces, tool actions, model usage, product source version and idempotency in `scripts/sql/003_taliya_agent_v2_architecture.sql` and `specs/009-taliya-sales-agent-architecture/migration-runbook.md`
- [X] T014 Create shared v2 types for macro state, substate, diagnostics, waitlist, traces and model usage in `lib/landing/ai-attendant/agent-v2-types.ts`
- [X] T015 Create compatibility mapper from existing `CommercialStage` to v2 macro/substate in `lib/landing/ai-attendant/agent-v2-state-compat.ts`
- [X] T016 Implement product knowledge source and versioned read path in `lib/landing/ai-attendant/product-knowledge-source.ts`
- [X] T017 Implement cost policy, budget categories and hard-cap fallback constants in `lib/landing/ai-attendant/agent-v2-cost-policy.ts`
- [X] T018 Implement trace store and model usage estimation helpers in `lib/landing/ai-attendant/agent-v2-trace-store.ts`
- [X] T019 Implement idempotency helpers for inbound events and tool actions in `lib/landing/ai-attendant/agent-v2-idempotency.ts`
- [X] T020 Implement v2 state/substate persistence helpers in `lib/landing/ai-attendant/agent-v2-state-store.ts`
- [X] T021 Implement deterministic hard guardrails in `lib/landing/ai-attendant/agent-v2-guardrails.ts`
- [X] T022 Implement internal tool action registry and idempotent execution wrapper in `lib/landing/ai-attendant/agent-v2-tools.ts`
- [X] T023 Implement shared channel adapter interface in `lib/landing/ai-attendant/agent-v2-channel-adapter.ts`
- [X] T024 Implement agent loop skeleton with ordered steps and trace hooks in `lib/landing/ai-attendant/agent-v2-loop.ts`
- [X] T025 Wire foundation tests into `package.json` scripts

**Checkpoint**: Product source, v2 state, idempotency, guardrails, trace and cost tests fail before implementation, then pass after implementation.

---

## Phase 3: User Story 1 - Natural Openings By Source And Channel (Priority: P1)

**Goal**: First responses match source/channel, avoid fake enthusiasm, avoid name/phone capture at opening and use reliable WhatsApp names only when safe.

**Independent Test**: Run SRC-001 to SRC-007 and FST direct-opening variants for widget and WhatsApp, checking first response, stored name confidence and no premature data capture.

### Tests

- [X] T026 [P] [US1] Add opening scenario fixtures for SRC-001 through SRC-007 in `scripts/fixtures/agent-v2/source-openings.json`
- [X] T027 [P] [US1] Add profile-name reliability tests in `scripts/eval-agent-v2-openings.mjs`
- [X] T028 [P] [US1] Add first-message direct intent opening tests in `scripts/eval-agent-v2-openings.mjs`

### Implementation

- [X] T029 [US1] Implement WhatsApp profile-name reliability classifier in `lib/landing/ai-attendant/agent-v2-identity.ts`
- [X] T030 [US1] Implement source and entry-intent normalization for widget and WhatsApp in `lib/landing/ai-attendant/agent-v2-normalize.ts`
- [X] T031 [US1] Implement opening policy orchestration actions in `lib/landing/ai-attendant/agent-v2-orchestrator.ts`
- [X] T032 [US1] Implement opening response objectives in `lib/landing/ai-attendant/agent-v2-response-generator.ts`
- [X] T033 [US1] Wire widget endpoint to normalize through v2 loop behind feature flag in `app/api/landing/ai-attendant/route.ts`
- [X] T034 [US1] Wire WhatsApp webhook to normalize through v2 loop behind feature flag in `app/api/landing/ai-attendant/whatsapp/route.ts`

**Checkpoint**: Cold greetings, named greetings, bad profile names, site/social/ad forced messages and first-message direct questions behave naturally without asking name/phone.

---

## Phase 4: User Story 2 - Direct Questions Are Answered Before Steering (Priority: P1)

**Goal**: Price, plans, demo, WhatsApp, product, guarantee, uncertainty and human questions are answered directly before diagnostic/waitlist steering.

**Independent Test**: Run DIR-001 through DIR-010 in cold, mid-diagnostic, diagnostic-complete and waitlist states.

### Tests

- [X] T035 [P] [US2] Add direct question fixtures in `scripts/fixtures/agent-v2/direct-questions.json`
- [X] T036 [P] [US2] Add directness and product-source assertions in `scripts/eval-agent-v2-direct-questions.mjs`
- [X] T037 [P] [US2] Add no-prompt-only-pricing guardrail tests in `scripts/eval-agent-v2-guardrails.mjs`

### Implementation

- [X] T038 [US2] Implement semantic interpretation for direct questions, secondary intents and mixed messages in `lib/landing/ai-attendant/agent-v2-semantic-interpreter.ts`
- [X] T039 [US2] Implement product/price/demo/WhatsApp answer actions in `lib/landing/ai-attendant/agent-v2-orchestrator.ts`
- [X] T040 [US2] Implement source-backed commercial answer generation in `lib/landing/ai-attendant/agent-v2-response-generator.ts`
- [X] T041 [US2] Add response validation for answering direct questions before steering in `lib/landing/ai-attendant/agent-v2-guardrails.ts`
- [X] T042 [US2] Record product source version for commercial answers in `lib/landing/ai-attendant/agent-v2-trace-store.ts`

**Checkpoint**: Direct questions are answered first, no plan/price facts are invented and diagnostic remains optional when not already accepted.

---

## Phase 5: User Story 3 - Diagnostic Is A Helpful Commercial Offer (Priority: P1)

**Goal**: The diagnostic is offered only at the right moment and sounds like a useful mini-consultation, not a form.

**Independent Test**: Trigger diagnostic from clear pain, plan recommendation, "como ficaria", ad CTA and widget CTA; verify approved meaning and channel formatting.

### Tests

- [X] T043 [P] [US3] Add diagnostic-offer fixtures in `scripts/fixtures/agent-v2/diagnostic-offers.json`
- [X] T044 [P] [US3] Add diagnostic offer timing and copy tests in `scripts/eval-agent-v2-diagnostic.mjs`
- [X] T045 [P] [US3] Add no-diagnostic-after-cold-greeting tests in `scripts/eval-agent-v2-diagnostic.mjs`

### Implementation

- [X] T046 [US3] Implement diagnostic-offer eligibility rules in `lib/landing/ai-attendant/agent-v2-orchestrator.ts`
- [X] T047 [US3] Implement approved diagnostic offer response objectives in `lib/landing/ai-attendant/agent-v2-response-generator.ts`
- [X] T048 [US3] Implement widget diagnostic CTA mapping without visual redesign in `components/landing/shared/FloatingAiAttendant.tsx`
- [X] T049 [US3] Implement WhatsApp diagnostic offer chunking plan in `lib/landing/ai-attendant/agent-v2-whatsapp-delivery.ts`

**Checkpoint**: Diagnostic is never pushed after "oi" only, never precedes an unanswered direct question and is split naturally on WhatsApp.

---

## Phase 6: User Story 4 - Diagnostic Uses Only Necessary Questions (Priority: P1)

**Goal**: Diagnostic questions adapt to prior context, skip known facts and produce a specific recommendation with evidence.

**Independent Test**: Run DIA-004 through DIA-009 with prior pain, student count, current tool, urgency and out-of-order answers.

### Tests

- [X] T050 [P] [US4] Add diagnostic state fixtures with known facts in `scripts/fixtures/agent-v2/diagnostic-state.json`
- [X] T051 [P] [US4] Add no-repetition diagnostic tests in `scripts/eval-agent-v2-diagnostic.mjs`
- [X] T052 [P] [US4] Add diagnostic schema quality tests in `scripts/eval-agent-v2-diagnostic.mjs`

### Implementation

- [X] T053 [US4] Implement diagnostic schema and step planner in `lib/landing/ai-attendant/agent-v2-diagnostic.ts`
- [X] T054 [US4] Implement fact extraction and known-fact reuse in `lib/landing/ai-attendant/agent-v2-semantic-interpreter.ts`
- [X] T055 [US4] Implement diagnostic tool actions in `lib/landing/ai-attendant/agent-v2-tools.ts`
- [X] T056 [US4] Implement diagnostic recommendation generator with evidence and confidence in `lib/landing/ai-attendant/agent-v2-response-generator.ts`
- [X] T057 [US4] Implement guardrail blocking generic diagnostic completion in `lib/landing/ai-attendant/agent-v2-guardrails.ts`

**Checkpoint**: Diagnostic asks only missing necessary questions, handles mid-flow product questions and outputs bottleneck, cause, first step, agents, plan/range, confidence and validation question.

---

## Phase 7: User Story 5 - Lead Data Is Completed After Value (Priority: P1)

**Goal**: Extra lead details are requested only after diagnostic value or waitlist agreement; WhatsApp never asks for phone.

**Independent Test**: Complete diagnostic with missing studio/city/contact and verify extra fields are requested only after positive validation/waitlist agreement by channel.

### Tests

- [X] T058 [P] [US5] Add post-value lead data fixtures in `scripts/fixtures/agent-v2/lead-data-after-value.json`
- [X] T059 [P] [US5] Add WhatsApp no-phone-request tests in `scripts/eval-agent-v2-lead-data.mjs`
- [X] T060 [P] [US5] Add widget contact optionality tests in `scripts/eval-agent-v2-lead-data.mjs`

### Implementation

- [X] T061 [US5] Implement lead data completion policy in `lib/landing/ai-attendant/agent-v2-orchestrator.ts`
- [X] T062 [US5] Implement lead fact persistence for post-value fields in `lib/landing/ai-attendant/agent-v2-tools.ts`
- [X] T063 [US5] Update Sales Inbox lead profile mapping for cold/warm/hot and missing fields in `lib/landing/ai-attendant/sales-inbox-store.ts`
- [X] T064 [US5] Implement widget contact request behavior without blocking diagnostic in `lib/landing/ai-attendant/agent-v2-response-generator.ts`

**Checkpoint**: Studio name/city/contact collection happens after value and respects channel policy.

---

## Phase 8: User Story 6 - Waitlist Appears Only After Real Interest (Priority: P1)

**Goal**: Waitlist is offered after validated interest or buying intent, preserves approved narrative and remains conversational after join.

**Independent Test**: Run WAI-001 through WAI-014, including "quero assinar" and post-waitlist questions.

### Tests

- [X] T065 [P] [US6] Add waitlist route fixtures in `scripts/fixtures/agent-v2/waitlist.json`
- [X] T066 [P] [US6] Add waitlist narrative and no-checkout tests in `scripts/eval-agent-v2-waitlist.mjs`
- [X] T067 [P] [US6] Add post-waitlist question preservation tests in `scripts/eval-agent-v2-waitlist.mjs`

### Implementation

- [X] T068 [US6] Implement waitlist eligibility and buying-intent routing in `lib/landing/ai-attendant/agent-v2-orchestrator.ts`
- [X] T069 [US6] Implement waitlist tool actions and actionable data status in `lib/landing/ai-attendant/agent-v2-tools.ts`
- [X] T070 [US6] Implement approved waitlist copy and post-waitlist answer behavior in `lib/landing/ai-attendant/agent-v2-response-generator.ts`
- [X] T071 [US6] Implement no-checkout/no-payment guardrail while broad availability is closed in `lib/landing/ai-attendant/agent-v2-guardrails.ts`
- [X] T072 [US6] Wire landing subscribe/Assinar entry intent to chat/WhatsApp flow without visual redesign in `components/landing/shared/FloatingAiAttendant.tsx`

**Checkpoint**: Waitlist only appears after real interest, direct buy routes to waitlist, no checkout is sent and follow-up questions continue normally after join.

---

## Phase 9: User Story 7 - Human Handoff Pauses AI (Priority: P1)

**Goal**: AI pauses for human request or manual WhatsApp/operator intervention and resumes only by explicit operator action.

**Independent Test**: Run HUM-001 through HUM-003 and manual intervention fallback scenarios.

### Tests

- [X] T073 [P] [US7] Add handoff fixtures in `scripts/fixtures/agent-v2/handoff.json`
- [X] T074 [P] [US7] Add AI pause/resume tests in `scripts/eval-agent-v2-handoff.mjs`
- [X] T075 [P] [US7] Add queued-response suppression tests in `scripts/eval-agent-v2-handoff.mjs`

### Implementation

- [X] T076 [US7] Implement human request interpretation and handoff actions in `lib/landing/ai-attendant/agent-v2-orchestrator.ts`
- [X] T077 [US7] Implement `pauseForHuman` and `resumeFromHuman` tools in `lib/landing/ai-attendant/agent-v2-tools.ts`
- [X] T078 [US7] Add manual pause/resume Sales Inbox API routes in `app/api/internal/sales-inbox/[leadId]/handoff/route.ts`
- [X] T079 [US7] Add pause/resume controls and status display in `components/internal/SalesInboxClient.tsx`
- [X] T080 [US7] Implement hard guardrail blocking AI response while `human_active` in `lib/landing/ai-attendant/agent-v2-guardrails.ts`

**Checkpoint**: Human handoff fully suppresses AI and keeps recording inbound messages.

---

## Phase 10: User Story 8 - Same Brain, Channel-Specific Delivery (Priority: P1)

**Goal**: Widget and WhatsApp share commercial reasoning but deliver appropriately for their channels.

**Independent Test**: Run matched widget/WhatsApp scenarios for price, diagnostic, waitlist and demo; verify parity and channel-specific formatting.

### Tests

- [X] T081 [P] [US8] Add channel parity fixtures in `scripts/fixtures/agent-v2/channel-parity.json`
- [X] T082 [P] [US8] Add WhatsApp chunk/typing/delay tests in `scripts/eval-agent-v2-delivery.mjs`
- [X] T083 [P] [US8] Add widget CTA/link parity tests in `scripts/eval-agent-v2-delivery.mjs`

### Implementation

- [X] T084 [US8] Implement WhatsApp delivery planner for chunks, typing and delay in `lib/landing/ai-attendant/agent-v2-whatsapp-delivery.ts`
- [X] T085 [US8] Implement widget delivery mapper for messages, buttons and cards in `lib/landing/ai-attendant/agent-v2-widget-delivery.ts`
- [X] T086 [US8] Wire WhatsApp Cloud API send and typing attempts through delivery planner in `lib/landing/ai-attendant/whatsapp.ts`
- [X] T087 [US8] Wire widget response shape through delivery mapper in `app/api/landing/ai-attendant/route.ts`
- [X] T088 [US8] Add no-literal-repeat response guardrail in `lib/landing/ai-attendant/agent-v2-guardrails.ts`

**Checkpoint**: Same question produces same commercial truth across channels; WhatsApp gets short paced chunks and widget gets appropriate CTAs.

---

## Phase 11: User Story 9 - Operator Visibility, Cost And Quality Signals (Priority: P2)

**Goal**: Sales Inbox shows cold/warm/hot/waitlist/handoff leads with state, diagnostic, next action, trace and cost.

**Independent Test**: Generate cold, warm, diagnostic, waitlist, human and cost-cap records and verify Sales Inbox fields.

### Tests

- [X] T089 [P] [US9] Add Sales Inbox data fixtures in `scripts/fixtures/agent-v2/sales-inbox.json`
- [X] T090 [P] [US9] Add Sales Inbox persistence tests in `scripts/eval-agent-v2-sales-inbox.mjs`
- [X] T091 [P] [US9] Add cost-cap visibility tests in `scripts/eval-agent-v2-sales-inbox.mjs`

### Implementation

- [X] T092 [US9] Extend Sales Inbox store query for v2 fields in `lib/landing/ai-attendant/sales-inbox-store.ts`
- [X] T093 [US9] Extend Sales Inbox API payload for priority, state, waitlist, diagnostic, trace and cost in `app/api/internal/sales-inbox/route.ts`
- [X] T094 [US9] Update Sales Inbox UI to show cold leads, hot leads, waitlist, handoff, next action and cost in `components/internal/SalesInboxClient.tsx`
- [X] T095 [US9] Add trace detail display or summary panel in `components/internal/SalesInboxClient.tsx`
- [X] T096 [US9] Implement cost hard-cap operator follow-up flag in `lib/landing/ai-attendant/agent-v2-tools.ts`
- [X] T097 [US9] Audit and constrain n8n/external automation so Sales Inbox/Postgres remains source of truth and Airtable is unused in `lib/landing/ai-attendant/n8n.ts` and `specs/009-taliya-sales-agent-architecture/external-automation-audit.md`

**Checkpoint**: Operator can see every lead category and debug why the agent acted.

---

## Phase 12: User Story 10 - Quality Gates Prove Human Commercial Quality (Priority: P1)

**Goal**: Realistic simulations prove the agent is natural, direct, non-aggressive, commercially correct, stateful and cost-aware before production replacement.

**Independent Test**: Run complete v2 eval matrix with transcripts, state transitions, tool calls, source versions, cost estimates, judge scores and blocking failures.

### Tests And Eval Runner

- [X] T098 [P] [US10] Add eval runner shared utilities in `scripts/eval-agent-v2-utils.mjs`
- [X] T099 [P] [US10] Add realistic transcript runner using real provider mode in `scripts/eval-agent-v2-conversation-matrix.mjs`
- [X] T100 [P] [US10] Add quality judge rubric implementation in `scripts/eval-agent-v2-quality-judge.mjs`
- [X] T101 [P] [US10] Add blocking-failure detector in `scripts/eval-agent-v2-blocking-failures.mjs`
- [X] T102 [P] [US10] Add cost, budget, skipped-scenario and escalation report generator in `scripts/eval-agent-v2-cost-report.mjs`
- [X] T103 [P] [US10] Add real-model eval budget controls for dry-run, max scenarios, max calls and max estimated cost in `scripts/eval-agent-v2-utils.mjs`
- [X] T104 [US10] Add scenario-matrix fixture loader for all P1 variants in `scripts/eval-agent-v2-conversation-matrix.mjs`
- [X] T105 [US10] Add transcript report output under `specs/009-taliya-sales-agent-architecture/eval-reports/`
- [X] T106 [US10] Wire all v2 eval scripts into `package.json`

**Checkpoint**: No production replacement until eval report has zero blocking failures, P1 minimum scores, trace completeness and cost thresholds.

---

## Final Phase: Polish, Verification And Release Preparation

**Purpose**: Cross-cutting cleanup and final validation.

- [X] T107 [P] Add media, abuse, prompt-injection and sensitive-data fixtures in `scripts/fixtures/agent-v2/safety-and-media.json`
- [X] T108 Add media, abuse, prompt-injection and sensitive-data assertions in `scripts/eval-agent-v2-conversation-matrix.mjs`
- [X] T109 Implement unsupported media, abuse and sensitive-data guardrail responses in `lib/landing/ai-attendant/agent-v2-guardrails.ts`
- [X] T110 Implement unsupported media response objectives and human fallback wording in `lib/landing/ai-attendant/agent-v2-response-generator.ts`
- [X] T111 [P] Run `npm run lint` and fix issues in touched files
- [X] T112 Run product knowledge, state, idempotency, guardrail, cost and trace layer tests from `package.json`
- [X] T113 Run integrated v2 conversation matrix and save report in `specs/009-taliya-sales-agent-architecture/eval-reports/`
- [X] T114 Run existing regression evals `npm run eval:ai-routes`, `npm run eval:ai-multiturn`, `npm run eval:ai-sales-humanization`, `npm run eval:lead-pipeline`, `npm run eval:custom-diagnostic`, `npm run eval:whatsapp-webhook`, `npm run eval:commercial-conversation-matrix`, `npm run eval:price-plan-commercial-matrix`, `npm run eval:message-delivery-matrix`
- [X] T115 Validate `/pilates` desktop/mobile visual baseline still matches protected layout in `specs/009-taliya-sales-agent-architecture/baseline.md`
- [X] T116 Perform local widget manual tests and record transcripts in `specs/009-taliya-sales-agent-architecture/manual-test-report.md`
- [X] T117 Prepare post-deploy WhatsApp real manual test plan in `specs/009-taliya-sales-agent-architecture/whatsapp-post-deploy-test-plan.md`
- [X] T118 Document remaining risks, production switch conditions, product-owner approval, migration verification and rollback/kill-switch usage in `specs/009-taliya-sales-agent-architecture/release-readiness.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1 Setup must complete first.
- Phase 2 Foundational blocks all user stories.
- US1, US2, US3, US4, US5, US6, US7, US8 and US10 are P1 and should be implemented before production replacement.
- US9 is P2 but still required before production replacement because the user wants cold leads, hot leads, waitlist and debug visibility in Sales Inbox.
- Final Phase depends on all implementation phases.

### User Story Dependencies

- US1 depends on Phase 2 normalization/state/product basics.
- US2 depends on product knowledge, semantic interpretation and response guardrails.
- US3 depends on US1/US2 behavior so diagnostic does not interrupt greetings or direct answers.
- US4 depends on diagnostic offer plus state/substate.
- US5 depends on diagnostic state and lead fact tools.
- US6 depends on diagnostic validation and buying-intent interpretation.
- US7 can be implemented after Phase 2 but must be integrated before real WhatsApp testing.
- US8 depends on shared response/delivery contracts.
- US9 depends on persistence/trace records from previous stories.
- US10 can begin after Phase 2 fixtures but must be completed after all stories.

### Parallel Opportunities

- T007-T012 can run in parallel.
- T026-T028, T035-T037, T043-T045, T050-T052, T058-T060, T065-T067, T073-T075, T081-T083, T089-T091 and T098-T103 can be parallelized by file.
- US7 handoff and US9 Sales Inbox UI can proceed in parallel after foundational persistence is stable.
- Eval fixture creation can proceed in parallel with implementation, but final eval execution must wait for all P1 behavior.

## Implementation Strategy

1. Build foundation first: product source, state/substate, idempotency, guardrails, trace and cost.
2. Implement conversation behavior in P1 order: openings, direct answers, diagnostic, data-after-value, waitlist, handoff and delivery.
3. Add Sales Inbox visibility before final production readiness.
4. Run realistic eval matrix with real model mode for quality validation.
5. Run widget manual tests locally.
6. Deploy only after product-owner approval; run real WhatsApp manual tests after deploy.

## Notes

- Do not redesign `/pilates`.
- Do not implement multi-tenant client WhatsApps or future seven customer agents.
- Do not restore the old name-first chatbot behavior.
- Do not use Airtable as source of truth.
- Real WhatsApp manual testing belongs after deploy.
- Cost cap is behavior, not only observability.
