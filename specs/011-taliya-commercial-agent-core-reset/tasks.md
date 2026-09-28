# Tasks - Taliya Commercial Agent Core Reset

These tasks are the active implementation checklist for Spec 011. The current task lock is controlled by `implementation-ledger.md`; do not skip ahead when an earlier unchecked Phase 10 task is blocked.

## Phase 0 - Approval And Freeze

- [x] T011-001 Confirm Spec 011 architecture decision and unresolved decisions in `spec.md`.
- [x] T011-002 Freeze preserved Spec 010 contracts as binding inputs for implementation.
- [x] T011-003 Freeze `specs/006-crm-operational-core/` as product truth for product/page/agent/mode/access/setup claims made by the commercial agent.
- [x] T011-004 Confirm no `/pilates` visual/layout/copy changes are in scope.
- [x] T011-005 Confirm no multi-tenant, client/studio WhatsApp, Design System, operational CRM agent implementation, checkout/payment, or demo/video production work is in scope.
- [x] T011-006 Confirm implementation approach: new core module plus legacy quarantine; refactoring `runtime/runner.py` in place is rejected.
- [x] T011-007 Confirm studio-owner language rule and approved wording variants for "base organizada"/"sistema"/CRM.
- [ ] T011-008 Create the decision/approval log location and owner. This remains final approval governance debt and must close through T011-112 before production activation.
- [x] T011-009 Capture or confirm current `/pilates` desktop/mobile visual baseline before any widget cutover or landing-behavior work.
- [x] T011-009A Treat `coverage-map.md` as the implementation coverage gate and update evidence/status rows as tasks close.
- [x] T011-009B Create `implementation-ledger.md` as the anti-drift control panel with current task lock, stop rules, validation checklist, and next-step handoff. Maintain it through the Definition of Done for each future task.

## Phase 1 - Regression Harness First

- [x] T011-010 Create regression fixtures from `regression-cases.md`.
- [ ] T011-011 For every observed bug targeted by this reset, prove the new regression case fails against the current system before any fix is implemented. Existing P0/paid failures have red evidence, but this remains open as a final audit item because not every historical bug row has an individually reconciled red-baseline artifact.
- [x] T011-012 Add static audit checks for forbidden commercial regex/if/template-first paths.
- [x] T011-013 Add static audit checks for product facts hardcoded outside official product knowledge or Spec 006-derived sources.
- [x] T011-014 Add static audit checks for new commercial logic in `runtime/runner.py` or old TS v2 public fallback paths.
- [x] T011-015 Add eval report schema from `eval-plan.md`.
- [x] T011-016 Add Sales Inbox projection consistency assertions.
- [x] T011-017 Add model-usage-required assertions for commercial turns.
- [x] T011-018 Add delivery/outbox duplicate and deferred-inbound regression tests.
- [x] T011-019 Create versioned golden transcripts for price, pain-first, Instagram/source opening, WhatsApp product, diagnostic, waitlist, human handoff, post-demo/product-demo, and long-conversation flows.
- [x] T011-019A Create "do not do" fixtures for early phone capture, invented checkout, invented availability/date/VIP/discount, invented integrations/certifications, client/studio WhatsApp capture, wrong student/customer language, and `497` as student count.

## Phase 2 - Core Contracts And Schema

- [x] T011-020 Define strict conductor decision schema.
- [x] T011-021 Define typed `TurnContext` schema.
- [x] T011-022 Define `ValidatorResult`, `RepairResult`, `RenderPlan`, `OutboxPlan`, and `ProjectionResult` schemas.
- [x] T011-023 Map preserved contracts to schema fields.
- [x] T011-024 Add numeric grounding fields to separate price, student count, phone/contact, date/time, and unknown number.
- [x] T011-025 Define typed template variable registry with allowed shape, grounding source, and validation rule for every customer-facing variable.
- [x] T011-026 Add explicit conductor schema versioning and compatibility/migration rules.
- [x] T011-027 Define mandatory trace schema for every normal commercial turn.
- [x] T011-028 Define expected Sales Inbox projection fields per commercial case family.

## Phase 3 - Turn Gate

- [x] T011-030 Implement per-conversation lock.
- [x] T011-031 Implement stable inbound idempotency.
- [x] T011-032 Implement human active/pause no-reply behavior.
- [x] T011-033 Implement inbound sequence number.
- [x] T011-034 Implement outbox reservation and deferred-inbound handling while current outbound delivery completes.
- [x] T011-035 Verify duplicate-message and "tudo bem during chunks" regressions using the chosen rule: finish current outbound delivery, defer new inbound, then process it as the next clean turn.

## Phase 4 - Context Builder

- [x] T011-040 Build typed context from memory, channel metadata, diagnostic ledger, waitlist/demo/handoff state, and recent transcript.
- [x] T011-041 Add official product knowledge retrieval as context, not routing.
- [x] T011-042 Add Spec 006-derived product contract retrieval/summaries for product/access/setup/agent/mode/page claims, not routing.
- [x] T011-043 Mark internal metadata as non-renderable.
- [x] T011-044 Mark identity/contact facts by reliability source.
- [x] T011-045 Add context snapshot persistence for eval/debug.

## Phase 5 - LLM Conductor

- [x] T011-050 Implement one-call conductor using the strict decision schema.
- [x] T011-051 Encode logical specialist roles in policy pack: entry, product, diagnostic, waitlist, handoff, safety.
- [x] T011-052 Require evidence for extracted facts and numeric interpretations.
- [x] T011-053 Require template plan and variables in structured output.
- [x] T011-054 Require conductor self-checks without trusting them as final validation.
- [x] T011-055 Log model usage for every conductor call.
- [x] T011-056 Prohibit generic whole-response fields such as `message_text`, `freeform_response`, or `assistant_reply` in conductor output.
- [x] T011-057 Enforce studio-owner language defaults and avoid technical "CRM" phrasing unless allowed by spec.
- [x] T011-058 Preserve commercial demo/product demo as one customer-facing concept while keeping OpenAI technical demo and video-production assets out of scope.

## Phase 5B - Action-First Conductor Correction

- [x] T011-058A Implement `TurnSituation` schema and builder for entry, diagnostic, post-diagnostic, product/price/demo, waitlist, handoff, and delivery-deferred modes.
- [x] T011-058B Replace the unconstrained full-plan conductor output for normal turns with a smaller `ConductorActionDecision` that chooses one action from `TurnSituation.allowed_actions`.
- [x] T011-058C Implement `DecisionCompiler` to derive state transition, diagnostic ledger merge, template group expansion, render-plan skeleton, and projection inputs from the LLM-selected action.
- [x] T011-058D Add static audit rules proving `TurnSituation` and `DecisionCompiler` do not map raw lead text keywords to price/demo/objection/pain/diagnostic/waitlist/handoff/source actions.
- [x] T011-058E Add no-cost mode matrix tests proving mixed-intent messages still call the LLM and every major mode provides an allowed-action menu.
- [x] T011-058F Rebuild the long-conversation preflight around action decisions, covering pending urgency, demo after diagnostic, price objection after diagnostic, waitlist intent, and post-diagnostic "como funciona".

## Phase 6 - Validators And Repair

- [x] T011-060 Implement schema/state/template/channel validators.
- [x] T011-061 Implement product fact and price/student-count validators.
- [x] T011-062 Implement diagnostic ledger validators, including mandatory urgency.
- [x] T011-063 Implement no-repeat diagnostic question validator.
- [x] T011-064 Implement waitlist/demo/handoff validators.
- [x] T011-065 Implement internal text leak and banned phrase validators.
- [x] T011-066 Implement Sales Inbox completeness validator.
- [x] T011-067 Implement one-call repair loop.
- [x] T011-068 Implement safe fallback/handoff after failed repair.
- [x] T011-069 Add corroboration checks so direct-question, official-fact, diagnostic-complete, and policy self-checks cannot pass solely because the conductor set a boolean.
- [x] T011-069A Validate product claims against official product knowledge and Spec 006 product contracts.
- [x] T011-069B Validate that failed LLM/validator/repair/timeout paths do not produce deterministic commercial answers.

## Phase 7 - Renderer

- [x] T011-070 Refactor renderer to accept only validated template plans.
- [x] T011-071 Remove semantic defaults from rendering.
- [x] T011-072 Validate required variables before rendering.
- [x] T011-073 Preserve final diagnostic staged order and complete final sentence.
- [x] T011-074 Preserve WhatsApp no-button/link/chunk rules.

## Phase 8 - Persistence And Sales Inbox Projection

- [x] T011-080 Persist inbound, context, decision, validation, repair, render, usage, runtime diff, Sales Inbox projection, and delivery events as the mandatory turn trace.
- [x] T011-081 Persist runtime state from validated decision only.
- [x] T011-082 Build Sales Inbox projection from runtime state/events.
- [x] T011-083 Distinguish customer-provided, channel-provided, operator-provided, inferred, and unverified identity/contact values.
- [x] T011-084 Verify completed diagnostic, waitlist, demo, handoff, and product follow-up projection completeness.
- [x] T011-085 Prevent adapter/Sales Inbox inferred facts from re-entering conductor context as reliable facts without source/confidence labels.
- [x] T011-086 Export trace artifacts in the eval/report format required by `eval-plan.md`.

## Phase 8A - Prompt, Policy, Template, And Product Knowledge Governance

- [x] T011-087 Add review metadata for prompt/policy/template/product-knowledge changes: reason, expected impact, transcript diff, eval before/after, and approval evidence.
- [x] T011-088 Add CI/static audit to block product facts in prompts/templates/tests/fallbacks when they belong in official product knowledge or Spec 006.
- [x] T011-089 Add cost optimization reports proving token/cost reduction without removing model usage or degrading golden transcripts.

## Phase 9 - Adapter Cutover And Legacy Quarantine

- [x] T011-090 Point widget runtime adapter to the new core.
- [x] T011-091 Point Taliya-owned WhatsApp path to the new core.
- [x] T011-092 Block public fallback to old TS v2 commercial engine.
- [x] T011-093 Quarantine or retire `runtime/runner.py` commercial brain paths.
- [x] T011-094 Keep old behavior only as test fixtures or rollback reference, not active public path.
- [x] T011-095 Verify widget cutover produces no `/pilates` visual/layout drift against the approved desktop/mobile baseline.
- [x] T011-096 Implement shadow mode where the new core runs in parallel without replying to leads.
- [x] T011-097 Compare shadow-mode decision JSON, render plan, trace, and Sales Inbox projection against golden transcripts/manual review samples.
- [x] T011-098 Prove feature-flag rollback disables the new core without reactivating the old deterministic commercial brain as public responder.
- [x] T011-099 Prepare 100% production cutover first-hours emergency watch readiness for trace quality, handoff behavior, Sales Inbox completeness, cost, model usage, fallback rates, duplicate/interleaved delivery, and P0 behavior. This did not activate production; final activation remains blocked by Phase 10 approval.

## Phase 10 - Verification And Approval

- [x] T011-100 Run static audit.
- [x] T011-101 Run unit/contract tests.
- [x] T011-102 Run mocked conductor fixtures.
- [x] T011-103 Run P0 real model regression suite.
- [x] T011-104 Run full required real model suite.
- [x] T011-104A Complete the action-first conductor correction from Phase 5B before any additional paid T011-105 attempt.
- [ ] T011-105 Run golden transcripts and "do not do" fixtures.
- [ ] T011-106 Export Sales Inbox projection evidence.
- [ ] T011-107 Export mandatory trace evidence.
- [ ] T011-108 Prepare manual transcript package for product-owner review.
- [ ] T011-109 Get explicit product-owner approval.
- [ ] T011-110 Prepare separate production preflight/cutover plan.
- [ ] T011-111 Prove feature-flag rollback path before production activation.
- [ ] T011-112 Complete approval log for sensitive decisions.

## Definition Of Done Checklist

Each implementation task must close with:

- [ ] Regression case/fixture linked.
- [ ] Red failure captured first for real bug fixes.
- [ ] Tests passing after fix.
- [ ] Static audit clean for forbidden commercial regex/if/template-first logic.
- [ ] Mandatory trace present for normal commercial turns.
- [ ] Model usage present for normal commercial turns unless explicitly exempt.
- [ ] Sales Inbox projection complete and consistent.
- [ ] No unregistered free-form template variable.
- [ ] Product facts sourced from official product knowledge/Spec 006.
- [ ] Golden transcripts unaffected or approved diff recorded.
- [ ] `/pilates` baseline/no-drift evidence when widget/landing behavior is affected.
- [ ] Feature flag/rollback behavior preserved when cutover path is touched.
- [ ] Approval evidence recorded where required.
- [ ] `coverage-map.md` updated with linked evidence for every affected requirement, regression case, and acceptance criterion.
- [ ] `implementation-ledger.md` updated with current task status, validation run, completion review, and next task lock.

## Explicitly Out Of Scope Tasks

- Do not change `/pilates` landing layout, styling, sections, animations, mockups, or composition.
- Do not implement multi-tenant behavior.
- Do not connect client/studio WhatsApp accounts.
- Do not create checkout/payment flow.
- Do not redesign Sales Inbox UI.
- Do not create the CRM Design System/component library under Spec 011.
- Do not implement client-studio operational CRM agents under Spec 011.
- Do not produce demo videos or visual demo assets under Spec 011.
