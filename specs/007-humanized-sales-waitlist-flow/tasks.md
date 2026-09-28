# Tasks: Humanized Sales And Waitlist Flow

**Input**: Design documents from `specs/007-humanized-sales-waitlist-flow/`
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [simulation-review-matrix.md](./simulation-review-matrix.md)

**Tests**: Required. This feature is conversation-quality sensitive and must include automated evals plus manual realistic simulation review.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel when files do not overlap.
- **[Story]**: Maps to user stories in `spec.md`.

## Phase 1: Spec And Review Setup

**Purpose**: Lock behavior before coding.

- [x] T001 [US6] Review `specs/007-humanized-sales-waitlist-flow/spec.md` with product owner and record approved changes.
- [x] T002 [US6] Review `specs/007-humanized-sales-waitlist-flow/simulation-review-matrix.md` and mark P1 scenarios approved for implementation.
- [x] T003 [US6] Confirm whether demo-ready state is currently false or configured, and record the decision in implementation notes.
- [x] T004 [US6] Confirm the exact required waitlist fields: person name, studio name, city, WhatsApp, pain summary and source channel.
- [x] T005 [US6] Switch to a Spec Kit-compatible feature branch before implementation or document the approved branch exception.

**Checkpoint**: Product script approved before implementation.

---

## Phase 2: Foundational State And Storage

**Purpose**: Add state contracts before changing agent behavior.

- [x] T006 [P] [US5] Extend `lib/landing/ai-attendant/schema.ts` with commercial stage, waitlist status, diagnostic status and demo status types.
- [x] T007 [P] [US5] Extend `lib/landing/ai-attendant/leads.ts` to include commercial stage, waitlist state, demo state, diagnostic state and timestamps in lead payloads.
- [x] T008 [US5] Extend `lib/landing/ai-attendant/sales-inbox-store.ts` to persist and read the new commercial/waitlist fields.
- [x] T009 [US5] Add or amend SQL migration under `scripts/sql/` if explicit columns are needed beyond existing JSON `data`.
- [x] T010 [US5] Update `app/api/internal/sales-inbox/leads/route.ts` and related lead detail/action routes so operators can see waitlist and stage fields.
- [x] T011 [US5] Document the storage contract in the feature implementation notes or a dedicated contract file before wiring behavior.

**Checkpoint**: Storage can represent the flow before the agent emits it.

---

## Phase 3: User Story 1 - WhatsApp Starts Like Human Atendimento (Priority: P1)

**Goal**: Cold WhatsApp start asks name first and avoids bot-like pitch.

**Independent Test**: S001-S004 pass locally and through WhatsApp webhook simulation.

### Tests

- [x] T012 [P] [US1] Add WhatsApp cold-start evals for S001-S004 in `scripts/eval-ai-sales-humanization.mjs`.
- [x] T013 [P] [US1] Add webhook-level cold-start scenario in `scripts/eval-whatsapp-webhook.mjs` or a companion harness to confirm actual WhatsApp route output.
- [x] T014 [P] [US1] Add refused-name eval S106.

### Implementation

- [x] T015 [US1] Update `lib/landing/ai-attendant/channels.ts` to carry WhatsApp channel policy and any known contact/name state.
- [x] T016 [US1] Update `lib/landing/floating-agent.ts` and/or dedicated channel policy helper so WhatsApp asks name before pitch.
- [x] T017 [US1] Ensure `app/api/landing/ai-attendant/whatsapp/route.ts` passes current user message only as `userMessage` and previous turns only as history.
- [x] T018 [US1] Verify human takeover, opt-out and duplicate webhook behavior still pass.

**Checkpoint**: WhatsApp no longer opens like a bot funnel.

---

## Phase 4: User Story 2 - Same Agent Brain With Channel Policies (Priority: P1)

**Goal**: Widget and WhatsApp use shared agent engine while adapting opening/copy by channel.

**Independent Test**: Same product/price/demo questions produce consistent facts and gates across web and WhatsApp.

### Tests

- [x] T019 [P] [US2] Add paired widget/WhatsApp scenarios to `scripts/eval-conversation-route-matrix.mjs` or `scripts/eval-ai-sales-humanization.mjs`.
- [x] T020 [P] [US2] Add widget-specific evals S005-S009.
- [x] T021 [P] [US2] Add prohibited behavior checks for channel divergence: unsupported promise, early waitlist, inconsistent pricing.

### Implementation

- [x] T022 [US2] Update `lib/landing/ai-attendant/context.ts` with explicit channel-policy instructions.
- [x] T023 [US2] Update `lib/landing/ai-attendant/commercial-knowledge.ts` if needed to clarify waitlist availability and current rollout narrative.
- [x] T024 [US2] Confirm widget opening still works and `/pilates` visual layout is untouched.

**Checkpoint**: Same brain, different channel surface.

---

## Phase 5: User Story 3 - Diagnostic Before Commercial CTA (Priority: P1)

**Goal**: Name -> pain/intent -> diagnostic offer -> diagnostic flow.

**Independent Test**: S101-S105 pass.

### Tests

- [x] T025 [P] [US3] Add eval for name then pain/intent path S101.
- [x] T026 [P] [US3] Add eval for name+intent same message S102.
- [x] T027 [P] [US3] Add eval for pain then diagnostic offer S103.
- [x] T028 [P] [US3] Add eval for diagnostic refusal S104.
- [x] T029 [P] [US3] Add eval for early contract request S105.
- [x] T030 [P] [US3] Add eval for ambiguous "sim" after diagnostic S107.

### Implementation

- [x] T031 [US3] Update diagnostic offer gates in `lib/landing/floating-agent.ts`, `lib/landing/ai-attendant/conversion-gates.ts` and/or `lib/landing/ai-attendant/sales-cadence.ts`.
- [x] T032 [US3] Update `lib/landing/ai-attendant/crm-diagnostic.ts` to preserve one-question-at-a-time rhythm and completion state.
- [x] T033 [US3] Ensure direct questions before diagnostic are answered briefly before the agent resumes discovery.

**Checkpoint**: Diagnostic offer timing is human and not aggressive.

---

## Phase 6: User Story 4 - Waitlist Only After High Intent (Priority: P1)

**Goal**: Waitlist replaces final high-intent conversion, not early nurture.

**Independent Test**: S201-S207 pass.

### Tests

- [x] T034 [P] [US4] Add post-diagnostic positive eval S201.
- [x] T035 [P] [US4] Add post-diagnostic negative eval S202.
- [x] T036 [P] [US4] Add demo requested/seen positive eval S203-S204.
- [x] T037 [P] [US4] Add demo unavailable eval S203B.
- [x] T038 [P] [US4] Add demo negative eval S205.
- [x] T039 [P] [US4] Add waitlist accepted/declined eval S206-S207.
- [x] T040 [P] [US4] Add waitlist pending-details and details-completed evals S208-S209.

### Implementation

- [x] T041 [US4] Add `waitlist_intent` / waitlist status path to `lib/landing/ai-attendant/schema.ts` and response normalization.
- [x] T042 [US4] Update `lib/landing/ai-attendant/conversion-gates.ts` so post-diagnostic first asks for validation instead of offering waitlist immediately.
- [x] T043 [US4] Update `lib/landing/ai-attendant/sales-cadence.ts` with waitlist narrative and positive/negative intent handling.
- [x] T044 [US4] Update widget CTA rendering in `components/landing/shared/FloatingAiAttendant.tsx` only if needed for waitlist CTA wiring, without visual redesign.
- [x] T045 [US4] Update WhatsApp text serialization in `lib/landing/ai-attendant/whatsapp.ts` if response needs waitlist-specific text.
- [x] T046 [US4] Ensure `waitlistStatus=joined` is only set after explicit agreement and required details are complete.

**Checkpoint**: Waitlist appears only after high intent.

---

## Phase 7: User Story 5 - Operator-Visible Waitlist Storage (Priority: P2)

**Goal**: Waitlist state is visible and auditable.

**Independent Test**: Simulated waitlist join creates/updates a Sales Inbox lead with stage and waitlist status.

### Tests

- [x] T047 [P] [US5] Add storage assertion for waitlist offered vs joined in the lead pipeline eval.
- [x] T048 [P] [US5] Add storage assertion for waitlist pending-details and declined/not-offered state.

### Implementation

- [x] T049 [US5] Update `lib/landing/ai-attendant/leads.ts` to create safe summaries for waitlist leads.
- [x] T050 [US5] Update `lib/landing/ai-attendant/sales-inbox-store.ts` to merge waitlist state without overwriting unrelated lead data.
- [x] T051 [US5] Update internal lead actions under `app/api/internal/sales-inbox/leads/[leadId]/actions/route.ts` to support manual waitlist status changes if needed.
- [x] T052 [US5] Add minimal operator-visible fields to the internal sales inbox view if current UI hides them.

**Checkpoint**: No qualified waitlist interest disappears.

---

## Phase 8: Review Gates And Release

**Purpose**: Simulate realistic conversations before deploy.

- [x] T053 [US6] Run `npm run lint`.
- [x] T054 [US6] Run `npx tsc --noEmit`.
- [x] T055 [US6] Run `npm run build`.
- [x] T056 [US6] Run affected eval scripts for sales humanization, route matrix and WhatsApp webhook.
- [x] T057 [US6] Complete R2 local API simulations and record results in `simulation-review-matrix.md` or a dated review note.
- [x] T058 [US6] Complete R3 production-like webhook simulation with storage checks.
- [ ] T059 [US6] Complete R4 real WhatsApp number smoke test after cleaning the test number.
- [ ] T060 [US6] Product owner completes R5 transcript review for every mandatory P1 scenario in `simulation-review-matrix.md`.
- [x] T061 [US6] Fix any failed P1 scenario and rerun the relevant eval/review stage.
- [x] T062 [US6] Review all implementation discoveries and confirm any behavior/storage/review change was reflected in `spec.md`, `tasks.md` and `simulation-review-matrix.md`.

**Pending manual release gates**: T059 and T060 require a real WhatsApp-number smoke test and product-owner transcript approval after deployment. Automated/local implementation gates are complete; see [implementation-review-2026-05-20.md](./implementation-review-2026-05-20.md).

---

## Dependencies & Execution Order

1. Phase 1 must complete before code changes.
2. Phase 2 blocks behavior changes because the agent needs a durable state contract.
3. Phases 3 and 4 can proceed together if write scopes are coordinated.
4. Phase 5 must precede Phase 6 because waitlist depends on diagnostic and demo gating.
5. Phase 7 depends on Phase 6 waitlist response/status contract.
6. Phase 8 is mandatory before production acceptance.
7. Any discovered in-scope behavior gap must update the Spec Kit artifacts before release acceptance.

## Suggested Checkpoints

- After Phase 1: `docs: add humanized sales waitlist spec`
- After Phase 2: `feat: add sales commercial stage storage`
- After Phases 3-5: `feat: humanize attendant discovery flow`
- After Phases 6-7: `feat: add waitlist conversion path`
- After Phase 8: `test: add sales waitlist simulation coverage`
