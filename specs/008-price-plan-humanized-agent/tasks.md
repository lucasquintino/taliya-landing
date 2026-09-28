# Tasks: Price, Plan And Humanized Agent Experience

**Input**: Design artifacts from `specs/008-price-plan-humanized-agent/`  
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

## Phase 1: Setup

- [X] T001 Confirm working branch is `008-price-plan-humanized-agent` and worktree has no unrelated unstaged changes
- [X] T002 Read `AGENTS.md`, `specs/002-floating-ai-sales-agent/plan.md`, `specs/002-floating-ai-sales-agent/spec.md`, `specs/002-floating-ai-sales-agent/tasks.md`, `specs/001-niche-landing-system/spec.md`, and `docs/landing-agentes-pilates/source/`
- [X] T003 Confirm `/pilates` protected layout is not touched by this feature
- [X] T004 Add npm scripts for `eval:price-plan-commercial-matrix` and `eval:message-delivery-matrix` in `package.json`

## Phase 2: Foundational Evals And Test Fixtures

- [X] T005 [P] Create `scripts/eval-price-plan-commercial-matrix.mjs` covering all cases from `contracts/eval-matrix.md`
- [X] T006 [P] Create `scripts/eval-message-delivery-matrix.mjs` covering widget and WhatsApp delivery/humanization assertions
- [X] T007 Extend `scripts/eval-commercial-conversation-matrix.mjs` only where needed to include new cross-matrix regressions
- [X] T008 Add report generation for price/plan and delivery matrices under `reports/`
- [X] T009 Run baseline evals locally through the real agent/runtime path with controlled scenario count and save failure plus usage summaries for implementation targeting

## Phase 3: User Story 1 - Price And Plans Are Answered Without Blocking (P1)

**Independent Test**: Price/plan matrix passes for cold, named, pain-captured, diagnostic-offered, diagnostic-in-progress and diagnostic-completed states in both widget and WhatsApp.

- [X] T010 [US1] Update price/plan response path in `lib/landing/floating-agent.ts` to answer prices before context capture using the shared commercial source of truth
- [X] T011 [US1] Update plan-only handling in `lib/landing/ai-attendant/sales-cadence.ts` to offer direct comparison without making diagnostic mandatory
- [X] T012 [US1] Update diagnostic bridge wording in `lib/landing/ai-attendant/conversion-gates.ts` to remove diagnostic-as-blocker language
- [X] T013 [US1] Update price side-question handling during diagnostic in `lib/landing/ai-attendant/crm-diagnostic.ts` or related diagnostic flow files
- [X] T014 [US1] Ensure cold WhatsApp price/plan starts answer price before name capture in `lib/landing/ai-attendant/commercial-state.ts`
- [X] T015 [US1] Add price/plan source-of-truth assertions comparing agent output with `/pilates/planos` or the shared commercial config
- [X] T016 [US1] Run `npm run eval:price-plan-commercial-matrix -- --target=http://localhost:3999 --sales-token=codex_sales_token`

## Phase 4: User Story 2 - Commercial CTAs Respect Readiness (P1)

**Independent Test**: Buying, recommendation, diagnostic-positive/negative and demo-positive/negative paths produce correct CTA state and no early checkout/waitlist.

- [X] T017 [US2] Update plan recommendation readiness gates in `lib/landing/ai-attendant/sales-cadence.ts`
- [X] T018 [US2] Update checkout gating in `lib/landing/ai-attendant/conversion-gates.ts`
- [X] T019 [US2] Preserve high-intent waitlist gates in `lib/landing/ai-attendant/commercial-state.ts`
- [X] T020 [US2] Add buying-without-diagnostic, buying-with-context and demo-unavailable eval cases to `scripts/eval-price-plan-commercial-matrix.mjs`
- [X] T021 [US2] Run commercial and price/plan matrices together and fix regressions

## Phase 5: User Story 3 - Widget And WhatsApp Deliver Messages Like A Human Conversation (P1)

**Independent Test**: Delivery matrix proves split messages, typing-before-each, proportional delay, no long blocks and no inbound echo in both channels.

- [X] T022 [US3] Audit current WhatsApp split/delay/typing behavior in `lib/landing/ai-attendant/whatsapp.ts`
- [X] T023 [US3] Adjust WhatsApp delay thresholds and maximum message part length in `lib/landing/ai-attendant/whatsapp.ts`
- [X] T024 [US3] Locate floating widget message rendering code and document current delivery behavior
- [X] T025 [US3] Implement widget message queue with typing indicator and proportional delay in the existing floating widget code
- [X] T026 [US3] Ensure widget does not render multi-message assistant replies all at once
- [X] T027 [US3] Add no-inbound-echo assertions for widget and WhatsApp in `scripts/eval-message-delivery-matrix.mjs`
- [X] T028 [US3] Run `npm run eval:message-delivery-matrix -- --target=http://localhost:3999 --sales-token=codex_sales_token`

## Phase 6: User Story 4 - Sales Inbox Shows Actionable Lead State (P1)

**Independent Test**: Cold, warm, hot, waitlist and human/manual states are visible and correct in Sales Inbox.

- [X] T029 [US4] Audit Sales Inbox API fields in `app/api/internal/sales-inbox/leads/route.ts` and related files
- [X] T030 [US4] Audit Sales Inbox UI fields in `app/internal/sales-inbox/` and related components
- [X] T031 [US4] Expose missing fields from `contracts/sales-inbox-state.md` without redesigning the UI
- [X] T032 [US4] Update lead creation/normalization in `lib/landing/ai-attendant/leads.ts`
- [X] T033 [US4] Add Sales Inbox assertions for priority, stage and waitlist data in eval scripts
- [X] T034 [US4] Run `npm run eval:lead-pipeline -- --target=http://localhost:3999 --sales-token=codex_sales_token`

## Phase 7: User Story 5 - Operational Guardrails Protect Cost, Abuse And Human Control (P1)

**Independent Test**: Rate limits, spam, human takeover/resumption and merge behavior match the operational rules.

- [X] T035 [US5] Audit existing rate-limit logic in `lib/landing/ai-attendant/usage.ts`
- [X] T036 [US5] Implement beginning-versus-middle humanized rate-limit messages in the agent response path
- [X] T037 [US5] Add per-phone/per-session abuse scenarios to `scripts/eval-message-delivery-matrix.mjs` or a dedicated operational eval section
- [X] T038 [US5] Verify WhatsApp Business App echo keeps AI paused in `app/api/landing/ai-attendant/whatsapp/route.ts`
- [X] T039 [US5] Implement explicit Sales Inbox operator re-enable action for AI after human takeover, including audit fields for who/what re-enabled and when
- [X] T040 [US5] Implement or verify strong-identifier merge by normalized phone/email in Sales Inbox lead upsert paths
- [X] T041 [US5] Add no-merge-by-name-only regression coverage

## Phase 8: User Story 6 - Media, Funnel Metrics, Handoff And Closure Are Explicit (P2)

**Independent Test**: Media fallback, funnel events, handoff next action and closure states are recorded predictably.

- [X] T042 [US6] Verify unsupported WhatsApp media fallback in `app/api/landing/ai-attendant/whatsapp/route.ts`
- [X] T043 [US6] Add media eval cases for audio, image and document payloads
- [X] T044 [US6] Audit current tracking/funnel event coverage in `lib/landing/tracking.ts` and AI attendant lead storage
- [X] T045 [US6] Add durable funnel event recording for price, plans, diagnostic, demo, waitlist, human, rate-limit and send-error milestones
- [X] T046 [US6] Implement idempotency for funnel event retries
- [X] T047 [US6] Expose funnel events through a local report, internal API response or documented database query for verification
- [X] T048 [US6] Add handoff next-action rules for human request, hot unknown integration, waitlist joined and mid-conversation limit
- [X] T049 [US6] Add closure state evaluation for waiting, cold closed, waitlist joined, waitlist declined, human active and error attention using documented default/configurable windows
- [X] T050 [US6] Preserve or add WhatsApp webhook validation, `phoneNumberId`/connection identification and provider-message idempotency regression coverage
- [X] T051 [US6] Add send-failure handling and evals so failed widget/WhatsApp replies become operator-visible `error_needs_attention` or manual priority
- [X] T052 [US6] Add eval coverage for funnel, handoff and closure cases

## Phase 9: Safe Cleanup And Manual Test Harness

- [X] T053 Create or document safe cleanup for one test phone/session without clearing the full database
- [X] T054 Add logging to cleanup so the report lists removed sessions/leads/messages
- [X] T055 Prepare widget manual test checklist from `quickstart.md`
- [X] T056 Prepare post-deploy WhatsApp Web manual test checklist from `quickstart.md`
- [X] T057 Execute widget manual tests and save transcript/results under `reports/`
- [X] T058 Confirm WhatsApp Web real-message tests are marked as post-deploy divulgation gates, not pre-deploy local gates

## Phase 10: Final Verification And Deploy

- [X] T059 Run `npm run eval:price-plan-commercial-matrix -- --target=http://localhost:3999 --sales-token=codex_sales_token`
- [X] T060 Run `npm run eval:message-delivery-matrix -- --target=http://localhost:3999 --sales-token=codex_sales_token`
- [X] T061 Run `npm run eval:commercial-conversation-matrix -- --target=http://localhost:3999 --sales-token=codex_sales_token`
- [X] T062 Run `npm run eval:ai-sales-humanization -- --target=http://localhost:3999 --sales-token=codex_sales_token`
- [X] T063 Run `npm run eval:whatsapp-webhook -- --target=http://localhost:3999`
- [X] T064 Run `npm run eval:lead-pipeline -- --target=http://localhost:3999 --sales-token=codex_sales_token`
- [X] T065 Run `npm run eval:ai-routes -- --target=http://localhost:3999` and classify any remaining legacy failures
- [X] T066 Run `npm run eval:ai-multiturn -- --target=http://localhost:3999` and classify any remaining legacy failures
- [X] T067 Run `npx tsc --noEmit`
- [X] T068 Run `npm run lint`
- [X] T069 Run `npm run build`
- [X] T070 Commit, push to `master`, wait for Vercel Ready and smoke test `/pilates`, `/pilates/planos`, webhook verification and Sales Inbox
- [ ] T071 Execute post-deploy WhatsApp Web real-message tests through the user's logged-in WhatsApp Web and save transcript/results under `reports/`
- [X] T072 Produce final report with automated results, widget manual transcripts, post-deploy WhatsApp transcripts, Sales Inbox state, production smoke and known risks

## Dependencies

- Phase 1 before all other work.
- Phase 2 before implementation, because evals define the behavioral target.
- US1 and US2 can run in parallel after foundational evals.
- US3 can run in parallel with US4 after eval harness exists.
- US5 depends on Sales Inbox/lead state understanding from US4 for merge and human controls.
- US6 depends on foundational storage decisions but can be implemented after P1 gates.
- Manual tests run only after automated gates pass locally.

## Parallel Opportunities

- T005 and T006 can be built in parallel.
- US1 commercial text/gates and US3 widget delivery can be implemented in parallel if write sets stay separate.
- US4 Sales Inbox visibility and US6 media/funnel eval cases can be investigated in parallel.

## Internal MVP Scope

Internal MVP is Phases 1-5 plus required gates for price/plans and delivery:
- price/plans answered first,
- no early recommendation/checkout/waitlist,
- widget and WhatsApp message delivery humanized,
- automated matrices passing.

This internal MVP is not enough for real divulgation. Before public lead capture or paid traffic, Phases 6-8 are required: cost/abuse limits, human re-enable, merge/duplicate handling, waitlist data quality, priority, media fallback, funnel metrics, handoff and closure.
