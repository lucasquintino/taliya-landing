# Tasks: OpenAI CS Agents Adaptation For Taliya Commercial

**Input**: Design documents from `/specs/010-openai-cs-agents-adaptation-for-taliya-commercial/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Required. This feature exists to replace a deterministic runtime that passed weak tests, so contract, integration, invariant, judge, and manual test artifacts are part of the implementation.

**Current Authority**: Earlier checked tasks are historical implementation evidence. The active final product-owner correction plan is T206-T226, with T211-T226 still open for implementation and validation. Production cutover and product-owner approval are blocked until T211-T226 pass, T205/T157/T137 approvals are recorded, and explicit deploy/live-action confirmation is given.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing where possible. Setup and foundational phases block story work.

## Phase 1: Setup And Reference Baseline

**Purpose**: Establish the new runtime workspace, reference baseline, protected landing baseline, and spec context.

- [X] T001 Read required context in `AGENTS.md`, `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/spec.md`, `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/plan.md`, `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/reference-map.md`, `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/current-runtime-gap-analysis.md`
- [X] T002 Read legacy/current context in `specs/009-taliya-sales-agent-architecture/spec.md`, `specs/009-taliya-sales-agent-architecture/plan.md`, `specs/009-taliya-sales-agent-architecture/tasks.md`, `specs/002-floating-ai-sales-agent/spec.md`, `specs/002-floating-ai-sales-agent/tasks.md`, `specs/001-niche-landing-system/spec.md`
- [X] T003 Read source handoff docs under `docs/landing-agentes-pilates/source/README.md` and the referenced source files in that directory
- [X] T004 Read relevant Next.js route/runtime docs under `node_modules/next/dist/docs/` before changing `app/api/landing/ai-attendant/route.ts` or `app/api/landing/ai-attendant/whatsapp/route.ts`
- [X] T005 Capture or confirm protected `/pilates` desktop and mobile baseline in `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/baseline.md`
- [X] T006 Clone or refresh the OpenAI reference review notes in `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/reference-map.md`
- [X] T007 Create Python runtime service directory in `services/taliya-agent-runtime/README.md`
- [X] T008 Create Python project configuration in `services/taliya-agent-runtime/pyproject.toml`
- [X] T009 Create runtime package skeleton in `services/taliya-agent-runtime/app/__init__.py`
- [X] T010 Create tests package skeleton in `services/taliya-agent-runtime/tests/__init__.py`
- [X] T011 Create runtime env documentation in `docs/landing-agentes-pilates/source/taliya-agent-runtime-env.md`

---

## Phase 2: Foundational Runtime Infrastructure

**Purpose**: Core infrastructure that must exist before any user story implementation.

**CRITICAL**: No user story work can begin until this phase is complete.

### Tests First

- [X] T012 [P] Add HMAC auth, stale timestamp, and replay-window contract tests in `services/taliya-agent-runtime/tests/test_hmac_auth.py`
- [X] T013 [P] Add generic agent-run API contract tests in `services/taliya-agent-runtime/tests/test_agent_runs_api.py`
- [X] T014 [P] Add agent registry tests for `taliya_commercial` and unknown keys in `services/taliya-agent-runtime/tests/test_agent_registry.py`
- [X] T015 [P] Add structured output validation tests in `services/taliya-agent-runtime/tests/test_structured_output.py`
- [X] T016 [P] Add Postgres memory-store contract tests in `services/taliya-agent-runtime/tests/test_memory_store.py`
- [X] T017 [P] Add product knowledge source contract tests in `services/taliya-agent-runtime/tests/test_product_knowledge.py`
- [X] T018 [P] Add tool idempotency contract tests in `services/taliya-agent-runtime/tests/test_tool_idempotency.py`
- [X] T019 [P] Add output guardrail and trace redaction validator tests in `services/taliya-agent-runtime/tests/test_output_guardrails.py`

### Implementation

- [X] T020 Create runtime settings loader in `services/taliya-agent-runtime/app/settings.py`
- [X] T021 Create FastAPI app with `GET /healthz` in `services/taliya-agent-runtime/app/main.py`
- [X] T022 Implement HMAC verification in `services/taliya-agent-runtime/app/auth/hmac.py`
- [X] T023 Implement generic runtime schemas in `services/taliya-agent-runtime/app/runtime/schemas.py`
- [X] T024 Implement agent registry in `services/taliya-agent-runtime/app/runtime/registry.py`
- [X] T025 Implement runtime event models in `services/taliya-agent-runtime/app/runtime/events.py`
- [X] T026 Implement model usage tracking helpers in `services/taliya-agent-runtime/app/runtime/usage.py`
- [X] T027 Implement Postgres memory store interface in `services/taliya-agent-runtime/app/shared/memory/postgres.py`
- [X] T028 Create SQL migration for generic runtime tables in `services/taliya-agent-runtime/migrations/001_agent_runtime_tables.sql`
- [X] T029 Implement product knowledge source reader in `services/taliya-agent-runtime/app/shared/product_knowledge/source.py`
- [X] T030 Implement shared output and trace redaction validators in `services/taliya-agent-runtime/app/shared/guardrails/validators.py`
- [X] T031 Implement generic `/v1/agent-runs` endpoint shell in `services/taliya-agent-runtime/app/main.py`
- [X] T032 Add Railway deployment config and docs in `services/taliya-agent-runtime/Dockerfile`, `services/taliya-agent-runtime/railway.toml`, and `services/taliya-agent-runtime/README.md`

**Checkpoint**: Runtime service can start, authenticate requests, reject unknown agents, validate output shape, and persist basic run records.

---

## Phase 3: User Story 2 - Architecture Follows The OpenAI Demo (Priority: P1)

**Goal**: Create a faithful Agents SDK style runtime with explicit agents, tools, guardrails, context, handoffs, and runner events.

**Independent Test**: Inspect source structure and run registry/runner tests proving normal turns go through the agent runner, not deterministic orchestration.

### Tests

- [X] T033 [P] [US2] Add reference structure conformance test in `services/taliya-agent-runtime/tests/test_reference_structure.py`
- [X] T034 [P] [US2] Add runner event persistence tests in `services/taliya-agent-runtime/tests/test_runner_events.py`
- [X] T035 [P] [US2] Add handoff persistence tests in `services/taliya-agent-runtime/tests/test_handoffs.py`
- [X] T036 [P] [US2] Add model-callable tool registration tests in `services/taliya-agent-runtime/tests/test_tool_registration.py`

### Implementation

- [X] T037 [US2] Create Taliya commercial context model in `services/taliya-agent-runtime/app/domains/taliya_commercial/context.py`
- [X] T038 [US2] Create Taliya commercial prompts module in `services/taliya-agent-runtime/app/domains/taliya_commercial/prompts.py`
- [X] T039 [US2] Define triage and specialist agents in `services/taliya-agent-runtime/app/domains/taliya_commercial/agents.py`
- [X] T040 [US2] Define model-callable commercial tools in `services/taliya-agent-runtime/app/domains/taliya_commercial/tools.py`
- [X] T041 [US2] Define domain guardrail agents and validators in `services/taliya-agent-runtime/app/domains/taliya_commercial/guardrails.py`
- [X] T042 [US2] Implement runner orchestration wrapper in `services/taliya-agent-runtime/app/runtime/runner.py`
- [X] T043 [US2] Persist current agent and input history after runner completion in `services/taliya-agent-runtime/app/shared/memory/postgres.py`
- [X] T044 [US2] Update `reference-map.md` with final implemented file paths in `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/reference-map.md`

**Checkpoint**: `taliya_commercial` can run through explicit agent definitions and produce persisted runner events.

---

## Phase 4: User Story 1 - Leads Get An LLM-First Commercial Conversation (Priority: P1)

**Goal**: Normal widget and WhatsApp lead turns are handled by the LLM-first runner and produce natural, structured responses.

**Independent Test**: Send realistic free-form turns to the runtime API and verify LLM runner usage, structured output, and no deterministic template path.

### Tests

- [X] T045 [P] [US1] Add free-form opening fixtures in `scripts/fixtures/agent-runtime/free-form-openings.json`
- [X] T046 [P] [US1] Add mixed-message fixtures in `scripts/fixtures/agent-runtime/mixed-messages.json`
- [X] T047 [P] [US1] Add runtime transcript integration tests in `scripts/eval-agent-runtime-conversations.mjs`
- [X] T048 [P] [US1] Add no-deterministic-path invariant tests in `scripts/eval-agent-runtime-invariants.mjs`

### Implementation

- [X] T049 [US1] Implement runtime client request signing in `lib/landing/ai-attendant/runtime-client.ts`
- [X] T050 [US1] Wire widget route to runtime client in `app/api/landing/ai-attendant/route.ts`
- [X] T051 [US1] Wire WhatsApp webhook route to runtime client in `app/api/landing/ai-attendant/whatsapp/route.ts`
- [X] T052 [US1] Map runtime structured messages to widget response shape in `lib/landing/ai-attendant/runtime-client.ts`
- [X] T053 [US1] Map runtime structured messages to WhatsApp delivery plan in `lib/landing/ai-attendant/whatsapp.ts`
- [X] T054 [US1] Remove old deterministic v2 official routing from `lib/landing/floating-agent.ts`
- [X] T055 [US1] Quarantine old v2 interpreter/orchestrator/generator from production path in `lib/landing/ai-attendant/agent-v2-loop.ts`
- [X] T056 [US1] Add operational fallback behavior without legacy conversation fallback in `lib/landing/ai-attendant/runtime-client.ts`

**Checkpoint**: A lead can receive an LLM-first response through both channels.

---

## Phase 5: User Story 3 - Product Knowledge Answers Are Official (Priority: P1)

**Goal**: Price, plan, demo, waitlist, availability, and link answers use only official product knowledge.

**Independent Test**: Ask product questions and verify direct answers, source versions, and blocked hallucinations.

### Tests

- [X] T057 [P] [US3] Add product question fixtures in `scripts/fixtures/agent-runtime/product-questions.json`
- [X] T058 [P] [US3] Add no-invented-link tests in `scripts/eval-agent-runtime-invariants.mjs`
- [X] T059 [P] [US3] Add product source version tests in `scripts/eval-agent-runtime-product-knowledge.mjs`
- [X] T060 [P] [US3] Add checkout-unavailable tests in `scripts/eval-agent-runtime-product-knowledge.mjs`

### Implementation

- [X] T061 [US3] Finalize official product knowledge data in `services/taliya-agent-runtime/app/shared/product_knowledge/source.py`
- [X] T062 [US3] Mirror or migrate existing product knowledge from `lib/landing/ai-attendant/product-knowledge-source.ts`
- [X] T063 [US3] Implement `get_product_knowledge` tool in `services/taliya-agent-runtime/app/domains/taliya_commercial/tools.py`
- [X] T064 [US3] Add product-source-required output validator in `services/taliya-agent-runtime/app/shared/guardrails/validators.py`
- [X] T065 [US3] Persist product source version on every product answer in `services/taliya-agent-runtime/app/shared/memory/postgres.py`
- [X] T066 [US3] Add Sales Inbox projection for product-source warnings in `lib/landing/ai-attendant/sales-inbox-store.ts`

**Checkpoint**: The agent answers commercial facts directly and cannot deliver unverified product claims.

---

## Phase 6: User Story 4 - Diagnostic Is Adaptive And Evidence-Based (Priority: P1)

**Goal**: The diagnostic is useful, fact-aware, and honest about uncertainty.

**Independent Test**: Run rich-context and thin-context diagnostics and verify evidence, unknowns, confidence, and no generic completion.

### Tests

- [X] T067 [P] [US4] Add rich-context diagnostic fixtures in `scripts/fixtures/agent-runtime/diagnostic-rich-context.json`
- [X] T068 [P] [US4] Add thin-context diagnostic fixtures in `scripts/fixtures/agent-runtime/diagnostic-thin-context.json`
- [X] T069 [P] [US4] Add fake-certainty blocking tests in `scripts/eval-agent-runtime-diagnostic.mjs`
- [X] T070 [P] [US4] Add diagnostic usefulness judge cases in `scripts/eval-agent-runtime-quality-judge.mjs`

### Implementation

- [X] T071 [US4] Implement diagnostic specialist instructions in `services/taliya-agent-runtime/app/domains/taliya_commercial/agents.py`
- [X] T072 [US4] Implement lead fact extraction tool behavior in `services/taliya-agent-runtime/app/domains/taliya_commercial/tools.py`
- [X] T073 [US4] Implement `save_diagnostic_record` tool in `services/taliya-agent-runtime/app/domains/taliya_commercial/tools.py`
- [X] T074 [US4] Add diagnostic evidence validator in `services/taliya-agent-runtime/app/domains/taliya_commercial/guardrails.py`
- [X] T075 [US4] Persist diagnostic records in `services/taliya-agent-runtime/app/shared/memory/postgres.py`
- [X] T076 [US4] Project diagnostic summary into Sales Inbox in `lib/landing/ai-attendant/sales-inbox-store.ts`

**Checkpoint**: Diagnostic can complete only when useful or explicitly ask for missing facts.

---

## Phase 7: User Story 5 - Waitlist Appears Only After Real Interest (Priority: P1)

**Goal**: Waitlist is offered naturally at the right time and persisted as an actionable lead state.

**Independent Test**: Run cold, warm, diagnostic-positive, and direct-buy scenarios and verify waitlist timing.

### Tests

- [X] T077 [P] [US5] Add waitlist timing fixtures in `scripts/fixtures/agent-runtime/waitlist-timing.json`
- [X] T078 [P] [US5] Add waitlist idempotency tests in `services/taliya-agent-runtime/tests/test_waitlist_tool.py`
- [X] T079 [P] [US5] Add no-early-waitlist evals in `scripts/eval-agent-runtime-waitlist.mjs`
- [X] T080 [P] [US5] Add post-waitlist question preservation tests in `scripts/eval-agent-runtime-waitlist.mjs`

### Implementation

- [X] T081 [US5] Implement waitlist specialist behavior in `services/taliya-agent-runtime/app/domains/taliya_commercial/agents.py`
- [X] T082 [US5] Implement `mark_waitlist` tool in `services/taliya-agent-runtime/app/domains/taliya_commercial/tools.py`
- [X] T083 [US5] Persist waitlist records in `services/taliya-agent-runtime/app/shared/memory/postgres.py`
- [X] T084 [US5] Add no-checkout waitlist guardrail in `services/taliya-agent-runtime/app/domains/taliya_commercial/guardrails.py`
- [X] T085 [US5] Project waitlist status and missing fields into Sales Inbox in `lib/landing/ai-attendant/sales-inbox-store.ts`
- [X] T086 [US5] Preserve landing subscribe/Assinar entry intent without visual redesign in `components/landing/shared/FloatingAiAttendant.tsx`

**Checkpoint**: Waitlist is qualified, persisted, and visible without pretending checkout exists.

---

## Phase 8: User Story 6 - Human Handoff Pauses Automation (Priority: P1)

**Goal**: Human handoff pauses automation across widget and WhatsApp, including WhatsApp Business App coexistence.

**Independent Test**: Simulate human request, manual WhatsApp reply, Sales Inbox pause/resume, and duplicate webhook retries.

### Tests

- [X] T087 [P] [US6] Add handoff runtime tests in `services/taliya-agent-runtime/tests/test_human_handoff.py`
- [X] T088 [P] [US6] Add WhatsApp manual echo pause fixtures in `scripts/fixtures/agent-runtime/handoff-whatsapp.json`
- [X] T089 [P] [US6] Add AI pause/resume evals in `scripts/eval-agent-runtime-handoff.mjs`
- [X] T090 [P] [US6] Add duplicate webhook no-reply tests in `scripts/eval-agent-runtime-delivery.mjs`

### Implementation

- [X] T091 [US6] Implement `pause_for_human` tool in `services/taliya-agent-runtime/app/domains/taliya_commercial/tools.py`
- [X] T092 [US6] Implement `resume_from_human` tool in `services/taliya-agent-runtime/app/domains/taliya_commercial/tools.py`
- [X] T093 [US6] Persist handoff events in `services/taliya-agent-runtime/app/shared/memory/postgres.py`
- [X] T094 [US6] Enforce human-active no-reply validator in `services/taliya-agent-runtime/app/shared/guardrails/validators.py`
- [X] T095 [US6] Preserve manual WhatsApp Business App echo detection in `lib/landing/ai-attendant/whatsapp.ts`
- [X] T096 [US6] Wire Sales Inbox pause/resume to runtime state in `app/api/internal/sales-inbox/[leadId]/handoff/route.ts`

**Checkpoint**: The AI never responds over an active human handoff.

---

## Phase 9: User Story 7 - Operator Visibility And Cost Signals (Priority: P2)

**Goal**: Operators can inspect the lead, facts, current agent, trace summary, tool calls, guardrails, handoff, waitlist, diagnostic, and cost.

**Independent Test**: Generate representative leads and inspect Sales Inbox payload and UI.

### Tests

- [X] T097 [P] [US7] Add Sales Inbox runtime projection fixtures in `scripts/fixtures/agent-runtime/sales-inbox.json`
- [X] T098 [P] [US7] Add Sales Inbox payload tests in `scripts/eval-agent-runtime-sales-inbox.mjs`
- [X] T099 [P] [US7] Add model usage/cost cap tests in `services/taliya-agent-runtime/tests/test_model_usage.py`
- [X] T100 [P] [US7] Add cost cap behavior evals in `scripts/eval-agent-runtime-cost.mjs`

### Implementation

- [X] T101 [US7] Persist model usage records in `services/taliya-agent-runtime/app/runtime/usage.py`
- [X] T102 [US7] Persist guardrail events with redacted evidence in `services/taliya-agent-runtime/app/shared/memory/postgres.py`
- [X] T103 [US7] Persist tool call summaries in `services/taliya-agent-runtime/app/shared/memory/postgres.py`
- [X] T104 [US7] Extend Sales Inbox store query for runtime fields in `lib/landing/ai-attendant/sales-inbox-store.ts`
- [X] T105 [US7] Extend Sales Inbox API payload in `app/api/internal/sales-inbox/route.ts`
- [X] T106 [US7] Add runtime trace summary UI in `components/internal/SalesInboxClient.tsx`
- [X] T107 [US7] Add cost cap operator next-action flag in `lib/landing/ai-attendant/sales-inbox-store.ts`

**Checkpoint**: Operators can understand what the runtime did without reading raw database rows.

---

## Phase 10: User Story 8 - Future-Agent Naming Without Scope Creep (Priority: P2)

**Goal**: Runtime names, endpoints, storage, and registry support future agents while only `taliya_commercial` is active.

**Independent Test**: Verify generic names and safe rejection of future/unknown keys.

### Tests

- [X] T108 [P] [US8] Add unknown future agent key tests in `services/taliya-agent-runtime/tests/test_agent_registry.py`
- [X] T109 [P] [US8] Add schema tests for `agent_key`, `agent_family`, `owner_scope`, and nullable `tenant_id` in `services/taliya-agent-runtime/tests/test_runtime_schema_scope.py`
- [X] T110 [P] [US8] Add repository grep guard test preventing new `sales_agent_*` tables in `scripts/eval-agent-runtime-naming.mjs`

### Implementation

- [X] T111 [US8] Define reserved future agent keys in `services/taliya-agent-runtime/app/runtime/registry.py`
- [X] T112 [US8] Ensure migrations use generic `agent_runtime_*` names in `services/taliya-agent-runtime/migrations/001_agent_runtime_tables.sql`
- [X] T113 [US8] Document future agent boundaries in `services/taliya-agent-runtime/README.md`
- [X] T114 [US8] Document out-of-scope multi-tenant/studio-agent behavior in `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/rollout-and-deploy.md`

**Checkpoint**: The runtime is extensible by name and contract without implementing future agents.

---

## Phase 11: User Story 9 - Quality Gates Prove The New Agent (Priority: P1)

**Goal**: Evals prove conversational quality, safety, directness, diagnostic usefulness, waitlist timing, and no architecture regression.

**Independent Test**: Run the eval suite and inspect reports under the spec folder.

### Tests And Eval Runner

- [X] T115 [P] [US9] Create shared eval utilities in `scripts/eval-agent-runtime-utils.mjs`
- [X] T116 [P] [US9] Create multi-turn conversation runner in `scripts/eval-agent-runtime-conversations.mjs`
- [X] T117 [P] [US9] Create deterministic invariant runner in `scripts/eval-agent-runtime-invariants.mjs`
- [X] T118 [P] [US9] Create LLM quality judge runner in `scripts/eval-agent-runtime-quality-judge.mjs`
- [X] T119 [P] [US9] Create delivery eval runner in `scripts/eval-agent-runtime-delivery.mjs`
- [X] T120 [P] [US9] Create cost report runner in `scripts/eval-agent-runtime-cost.mjs`
- [X] T121 [US9] Wire new eval scripts into `package.json`
- [X] T122 [US9] Add transcript report writer under `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/`
- [X] T123 [US9] Add eval budget controls for max scenarios, max model calls, and max cost in `scripts/eval-agent-runtime-utils.mjs`
- [X] T124 [US9] Produce latest eval reports in `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/agent-runtime-transcripts-latest.md`

**Checkpoint**: The new runtime fails when it is robotic, unsafe, evasive, or unsupported.

---

## Final Phase: Verification, Deploy, And Production Replacement

**Purpose**: Complete production readiness without keeping the old deterministic agent as fallback.

**Current Gate**: T132-T137 must not be executed until the later Product-Owner Final Diagnostic/Demo/Name Correction Phase T206-T226 is complete, zero-cost gates pass, quota-limited real OpenAI correction scenarios pass, the updated behavior matrix passes, and product-owner transcript approval is recorded. Their position here is historical from the first implementation plan, not permission to deploy before the final correction phase.

- [X] T125 [P] Run Python runtime tests from `services/taliya-agent-runtime/pyproject.toml`
- [X] T126 [P] Run `npm run lint` for touched Next/TypeScript files
- [X] T127 Run all new agent runtime eval scripts from `package.json`
- [X] T128 Run existing WhatsApp and delivery regression evals from `package.json`
- [X] T129 Validate `/pilates` desktop and mobile baseline still matches `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/baseline.md`
- [X] T130 Perform local widget manual tests and save transcript in `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/manual-widget-test-report.md`
- [X] T131 Request explicit user confirmation before any production database migration, Railway deploy, Vercel deploy, or live WhatsApp production action in `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/release-readiness.md`
- [ ] T132 Deploy `services/taliya-agent-runtime` to Railway only after explicit confirmation and record service URL in `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/rollout-and-deploy.md`
- [ ] T133 Configure Vercel runtime env vars documented in `docs/landing-agentes-pilates/source/taliya-agent-runtime-env.md` only after explicit confirmation
- [ ] T134 Deploy Next integration and verify HMAC runtime calls in `app/api/landing/ai-attendant/route.ts` only after explicit confirmation
- [ ] T135 Run real WhatsApp smoke tests and save report in `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/whatsapp-post-deploy-test-report.md` only after explicit confirmation
- [X] T136 Confirm old deterministic runtime is not reachable as official fallback in `lib/landing/floating-agent.ts`
- [ ] T137 Record product-owner transcript approval in `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/release-readiness.md`
- [X] T138 Document remaining risks, operational fallback, cost cap behavior, and production replacement result in `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/release-readiness.md`

---

## Historical Corrective Phase: Behavior Contract Realignment

**Purpose**: Historical implementation evidence from the earlier correction pass. These checked tasks do not approve final behavior readiness. The active final plan is T206-T226.

- [X] T139 Create binding behavior contract in `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/behavior-contract.md`
- [X] T140 Update `spec.md`, `plan.md`, `eval-plan.md`, and `release-readiness.md` to mark prior real OpenAI results as smoke/integration evidence rather than final behavior approval
- [X] T141 Add behavior policy pack in `services/taliya-agent-runtime/app/domains/taliya_commercial/behavior_policy.py`
- [X] T142 Expand structured output models in `services/taliya-agent-runtime/app/runtime/schemas.py` and runtime draft parsing in `services/taliya-agent-runtime/app/runtime/runner.py` with route, opening type, intents, direct-question status, diagnostic action, diagnostic eligibility, waitlist eligibility, profile-name usage, facts, next-question kind, and policy checks
- [X] T143 Update `services/taliya-agent-runtime/app/domains/taliya_commercial/prompts.py` so the LLM receives the full behavior contract, voice policy, opening/source policy, diagnostic policy, waitlist policy, and role-specific specialist instructions
- [X] T144 Wire the live non-mock runtime path to use the `taliya_commercial_triage` plus `entry`, `product`, `diagnostic`, `waitlist`, and `handoff` specialist role definitions instead of a single thin prompt with only a `current_agent` label
- [X] T145 Implement reliable/unreliable WhatsApp profile-name handling without early name capture
- [X] T146 Add behavior validators for cold openings, source openings, direct-question-first, diagnostic timing, waitlist timing, early contact capture, banned voice phrases, thin-evidence wording, repeated fact/question requests, and human-active no-reply
- [X] T147 Expand diagnostic output and persistence to include evidence, main bottleneck, likely cause, first step, indicated Taliya routines/agents, plan or plan range, confidence, unknowns, and validation question
- [X] T148 Update `services/taliya-agent-runtime/app/runtime/usage.py` pricing rates to current provider pricing and add a regression test proving cost reports use the configured rates
- [X] T149 Add behavior fixtures under `scripts/fixtures/agent-runtime/` for cold greetings, source openings, diagnostic CTA, pain first message, price first message, plan fit, mixed price plus pain, reliable/unreliable profile name, waitlist timing, unsupported media, and handoff
- [X] T150 Add real OpenAI behavior eval runner and report output, saving full transcripts to `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/agent-runtime-real-openai-behavior-latest.md`
- [X] T151 Strengthen invariant and judge evals so mapped behavior failures cannot pass through keyword-only checks
- [X] T152 Run Python runtime tests from `services/taliya-agent-runtime`
- [X] T153 Run `npm run lint` for touched TypeScript/Next files if any Next-side files are touched
- [X] T154 Run local non-mock-safe eval suite and save reports
- [X] T155 Run real OpenAI behavior eval with `TALIYA_AGENT_PROVIDER=openai` and no mock fallback
- [X] T156 Review every behavior transcript, record failures/fixes, and update `release-readiness.md`
- [ ] T157 Record product-owner approval only after the behavior matrix passes; block T132-T137 until then

---

## Final Product-Owner Behavior Phase: LLM-First Template-Controlled Agent

**Purpose**: Historical implementation evidence for the LLM-first template-controlled plan. This phase superseded the first weak interpretation, but it is now itself superseded for release approval by the Product-Owner Final Diagnostic/Demo/Name Correction Phase T206-T226.

### Contract And Spec Alignment

- [X] T158 Update implementation references to treat `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/conversation-state-contract.md` as the canonical state source
- [X] T159 Update implementation references to treat `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/message-template-contract.md` as the canonical template/rendering source
- [X] T160 Update implementation references to treat `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/diagnostic-contract.md` as the canonical diagnostic source
- [X] T161 Update implementation references to treat `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/sales-inbox-contract.md` as the canonical Sales Inbox completeness source

### Tests First: Zero-Cost Gates

- [X] T162 [P] Add canonical conversation state transition tests in `services/taliya-agent-runtime/tests/test_conversation_state_contract.py`
- [X] T163 [P] Add template registry and allowed-state tests in `services/taliya-agent-runtime/tests/test_message_templates.py`
- [X] T164 [P] Add renderer brevity and channel-shape tests in `services/taliya-agent-runtime/tests/test_message_renderer.py`
- [X] T165 [P] Add diagnostic ledger no-repeat and completion tests in `services/taliya-agent-runtime/tests/test_diagnostic_ledger.py`
- [X] T166 [P] Add waitlist clear-contract-intent validator tests in `services/taliya-agent-runtime/tests/test_waitlist_contract.py`
- [X] T167 [P] Add real-person-name-only tests in `services/taliya-agent-runtime/tests/test_name_policy.py`
- [X] T168 [P] Add invalid JSON repair and no-state-advance fallback tests in `services/taliya-agent-runtime/tests/test_llm_output_repair.py`
- [X] T169 [P] Add idempotency tests for inbound retries, outbound replies, diagnostic writes, waitlist joins, and handoff events in `services/taliya-agent-runtime/tests/test_idempotency_contract.py`
- [X] T170 [P] Add rapid consecutive message ordering tests in `services/taliya-agent-runtime/tests/test_conversation_ordering.py`
- [X] T171 [P] Add Sales Inbox completeness fixture tests in `scripts/eval-agent-runtime-sales-inbox.mjs`
- [X] T172 [P] Add widget/WhatsApp delivery shape tests in `scripts/eval-agent-runtime-delivery.mjs`

### Runtime State, Templates, And Renderer

- [X] T173 Implement canonical state enum, allowed transitions, and tendency helpers in `services/taliya-agent-runtime/app/domains/taliya_commercial/state.py`
- [X] T174 Implement approved message template registry in `services/taliya-agent-runtime/app/domains/taliya_commercial/templates.py`
- [X] T175 Implement channel-aware message renderer in `services/taliya-agent-runtime/app/domains/taliya_commercial/renderer.py`
- [X] T176 Update structured schemas in `services/taliya-agent-runtime/app/runtime/schemas.py` to include previous/current/next state, template IDs, template variables, render plan, and diagnostic ledger
- [X] T177 Update runner parsing and validation in `services/taliya-agent-runtime/app/runtime/runner.py` so LLM selects templates/variables and the renderer produces final messages
- [X] T178 Remove or quarantine any remaining deterministic response-generation path from the official runtime path in `services/taliya-agent-runtime/app/runtime/runner.py`

### LLM Prompt And Behavior Policy

- [X] T179 Update commercial prompts in `services/taliya-agent-runtime/app/domains/taliya_commercial/prompts.py` so the LLM acts as interpreter/director, not free-form copywriter or deterministic state machine
- [X] T180 Update behavior policy pack in `services/taliya-agent-runtime/app/domains/taliya_commercial/behavior_policy.py` with canonical states, multi-intent priority, template rules, diagnostic rules, waitlist rules, and name policy
- [X] T181 Ensure direct questions are answered before diagnostic/waitlist/qualification in `services/taliya-agent-runtime/app/domains/taliya_commercial/guardrails.py`
- [X] T182 Ensure unmapped cases use the approved safe adaptive fallback policy in `services/taliya-agent-runtime/app/domains/taliya_commercial/guardrails.py`

### Diagnostic

- [X] T183 Implement diagnostic answer ledger in `services/taliya-agent-runtime/app/domains/taliya_commercial/diagnostic_ledger.py`
- [X] T184 Map all mandatory diagnostic questions from prior `009` behavior docs into the ledger in `services/taliya-agent-runtime/app/domains/taliya_commercial/diagnostic_ledger.py`
- [X] T185 Update fact extraction/merge behavior in `services/taliya-agent-runtime/app/domains/taliya_commercial/tools.py` so facts volunteered outside diagnostic satisfy ledger questions
- [X] T186 Block diagnostic completion until ledger completion in `services/taliya-agent-runtime/app/domains/taliya_commercial/guardrails.py`
- [X] T187 Update diagnostic persistence and runtime output with ledger, evidence, unknowns, confidence, recommendation, and validation question in `services/taliya-agent-runtime/app/shared/memory/postgres.py`

### Waitlist, Name, Handoff, Safety

- [X] T188 Update waitlist validator so waitlist requires clear intent to contract in `services/taliya-agent-runtime/app/domains/taliya_commercial/guardrails.py`
- [X] T189 Update waitlist tool to persist partial/pending data without duplicate joins in `services/taliya-agent-runtime/app/domains/taliya_commercial/tools.py`
- [X] T190 Implement real-person-name-only policy for WhatsApp profile and lead-provided names in `services/taliya-agent-runtime/app/domains/taliya_commercial/tools.py`
- [X] T191 Ensure handoff suppresses AI replies across widget, WhatsApp, and Sales Inbox resume/pause paths in `services/taliya-agent-runtime/app/shared/guardrails/validators.py`
- [X] T192 Ensure out-of-scope, prompt-injection, and medical-advice cases use short safe templates in `services/taliya-agent-runtime/app/domains/taliya_commercial/templates.py`

### Channel Delivery

- [X] T193 Update widget response mapping to preserve short bubbles, typing/delay behavior, and validated buttons in `lib/landing/ai-attendant/runtime-client.ts`
- [X] T194 Update WhatsApp delivery mapping to use short chunks, typing/delay, and official text/link equivalents instead of widget buttons in `lib/landing/ai-attendant/whatsapp.ts`
- [X] T195 Ensure channel adapters do not choose commercial behavior or generate sales text outside runtime output in `app/api/landing/ai-attendant/route.ts` and `app/api/landing/ai-attendant/whatsapp/route.ts`

### Sales Inbox Completeness

- [X] T196 Update runtime-to-lead projection to persist every required field from `sales-inbox-contract.md` in `lib/landing/ai-attendant/runtime-client.ts`
- [X] T197 Update lead record and store contracts for diagnostic ledger, template IDs, state, waitlist intent evidence, product source version, guardrail flags, and cost in `lib/landing/ai-attendant/leads.ts` and `lib/landing/ai-attendant/sales-inbox-store.ts`
- [X] T198 Update Sales Inbox UI to show the required operator fields without redesigning `/pilates` in `components/internal/SalesInboxClient.tsx`

### Quota-Aware Real OpenAI Validation

- [X] T199 Add zero-cost gate runner/report and package script in `scripts/eval-agent-runtime-zero-cost-gates.mjs` and `package.json`
- [X] T200 Add max scenario, max model call, max cost, dry-run, and stop-on-first-failure controls to real OpenAI eval runners in `scripts/eval-agent-runtime-real-openai.py` and `scripts/eval-agent-runtime-legacy-behavior.py`
- [X] T201 Add final behavior matrix fixtures for openings, direct questions, diagnostic ledger, waitlist intent, names, handoff, safety, delivery, and Sales Inbox in `scripts/fixtures/agent-runtime/final-behavior-matrix.json`
- [X] T202 Run zero-cost gates and save `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/agent-runtime-zero-cost-gates-latest.md`
- [X] T203 Run quota-limited real OpenAI smoke only after T202 passes and save transcripts under `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/`
- [X] T204 Run the full mapped behavior matrix only after smoke passes and cost limits are explicitly configured
- [ ] T205 Perform product-owner transcript review and record approval/failures in `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/release-readiness.md`

---

## Product-Owner Final Diagnostic/Demo/Name Correction Phase

**Purpose**: Capture and implement the product-owner corrections discovered after the previous automated pass. The prior `12/12`, `28/28`, and Sales Inbox passes are now historical evidence only for this phase because they did not enforce the approved final diagnostic presentation, demo-state branch, name timing, or diagnostic feedback cadence.

### Contract And Spec Update Before Code

- [X] T206 Update `diagnostic-contract.md` with the approved staged final diagnostic, dynamic plan line, dynamic demo line, diagnostic question feedback cadence, and blocked old diagnostic formats
- [X] T207 Update `behavior-contract.md` with WhatsApp/widget name timing, demo policy/state, diagnostic staged-order policy, and validators for old weak formats
- [X] T208 Update `message-template-contract.md` with staged diagnostic templates, diagnostic feedback variables, channel-specific demo CTA/link rules, and staged delivery exception
- [X] T209 Update `conversation-state-contract.md`, `data-model.md`, and `sales-inbox-contract.md` with demo state and persistence requirements
- [X] T210 Update `spec.md`, `plan.md`, `eval-plan.md`, `release-readiness.md`, `product-owner-transcript-review.md`, `completion-audit.md`, `requirements-evidence-matrix.md`, and `deploy-preflight-report.md` so the new corrections block production approval until retested

### Tests First: New Blocking Gates

- [X] T211 Add zero-cost tests proving direct diagnostic requests do not ask the first question dry and diagnostic-in-progress turns acknowledge the prior answer before the next question
- [X] T212 Add zero-cost tests proving completed diagnostic staged order: hold, pain/context, CRM base, operational step, agents one by one, dynamic plan line, dynamic demo line
- [X] T213 Add zero-cost tests blocking old final diagnostic copy patterns: "Pelo contexto, o principal gargalo parece", "Para plano, eu compararia", and final close "Isso faz sentido para o momento do seu studio?"
- [X] T214 Add zero-cost tests for demo state branches: demo not offered -> "Temos algumas demonstracoes..."; demo already offered -> "Chegou a olhar as demonstracoes?"
- [X] T215 Add zero-cost tests for WhatsApp/widget name timing: reliable WhatsApp name used, unreliable name ignored, widget/cold greeting does not ask name, qualified diagnostic entry may ask name without blocking
- [X] T216 Add Sales Inbox completeness tests for demo status, final plan line, final demo line, CRM base recommendation, and per-agent recommendation details

### Runtime And Template Implementation

- [X] T217 Implement/persist demo state in runtime memory, structured output, tool records, and Sales Inbox projection
- [X] T218 Update diagnostic templates/renderer to support staged final diagnostic delivery and approved staged exception to normal chunk limits
- [X] T219 Update diagnostic runner/prompt behavior so LLM fills grounded variables for pain context, CRM base, operational step, agent recommendations, dynamic plan, and demo branch
- [X] T220 Update diagnostic question flow so start and subsequent questions include grounded feedback before asking the next missing question
- [X] T221 Update name policy execution so WhatsApp and widget ask/use names exactly according to the contract
- [X] T222 Update waitlist gating so demo curiosity alone is blocked and positive demo reaction requires clear next-step/contract intent before waitlist

### Quota-Aware Validation

- [X] T223 Run Python runtime tests and all new zero-cost gates before any real OpenAI test
- [X] T224 Run quota-limited real OpenAI scenarios only for the new correction matrix: diagnostic direct request, in-progress feedback, completed staged diagnostic, demo not offered, demo already offered, name timing, post-demo waitlist gating, and Sales Inbox persistence
- [X] T225 Save full before/after transcripts and cost report under `eval-reports/` and list every message exchange in the final report
- [X] T226 Update `release-readiness.md` and `product-owner-transcript-review.md` with the new evidence and keep production blocked until product-owner transcript approval

---

## Product-Owner Product Explanation And Follow-Up Delta Phase

**Purpose**: Implement only the missing or partial product explanation, post-diagnostic follow-up, comparison, integration/scope, security/data, out-of-profile, diagnostic-refusal, and conversation-resume behavior defined in `product-followup-delta-contract.md`. This phase must not reopen protected behavior that already exists and is approved.

### Contract And Spec Alignment

- [X] T227 Create binding delta contract in `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/product-followup-delta-contract.md`
- [X] T228 Update `behavior-contract.md` with product explanation, post-diagnostic context, selective knowledge, CRM-word control, and protected-route regression rules
- [X] T229 Update `message-template-contract.md` with the new missing templates and variable grounding rules
- [X] T230 Update `eval-plan.md` with how-it-works, post-diagnostic, comparison, integration, security, out-of-profile, diagnostic-refusal, and protected-route regression gates
- [X] T231 Update `plan.md` and `tasks.md` so this delta is tracked before implementation

### Tests First: Zero-Cost Gates

- [X] T232 Add product knowledge tests for new keys in `services/taliya-agent-runtime/tests/test_product_knowledge.py`: `how_it_works`, `routine_areas`, `whatsapp_scope`, `integration_scope`, `comparison_spreadsheet`, `comparison_management_system`, `security_and_data`, `availability_and_onboarding`, and `out_of_profile`
- [X] T233 Add template registry tests for `product.how_it_works_direct`, `product.comparison_current_tool`, `product.integration_scope_direct`, `product.security_data_direct`, and `product.out_of_profile_redirect` in `services/taliya-agent-runtime/tests/test_message_templates.py`
- [X] T234 Add renderer/validator tests proving new templates stay short, channel-safe, and grounded in product knowledge or saved diagnostic state
- [X] T235 Add tests proving approved openings remain unchanged and never use "CRM" in lay-lead openings
- [X] T236 Add tests proving price-objection/customer-facing lay explanations do not use "CRM" unless the lead directly asked about CRM
- [X] T237 Add tests proving post-diagnostic follow-up uses saved diagnostic context and does not restart diagnostic
- [X] T238 Add tests proving diagnostic refusal is respected and not followed immediately by another diagnostic offer
- [X] T239 Add tests proving new product/comparison/integration/security/out-of-profile decisions are not implemented through deterministic commercial regex shortcuts and that commercial product-followup routes record real LLM/model usage unless they are explicitly allowed operational zero-cost exceptions

### Product Knowledge And Templates

- [X] T240 Add official product knowledge keys and source payloads in `services/taliya-agent-runtime/app/shared/product_knowledge/source.py`
- [X] T241 Add selective product-knowledge retrieval for the new keys in `services/taliya-agent-runtime/app/runtime/runner.py`
- [X] T242 Add new product templates in `services/taliya-agent-runtime/app/domains/taliya_commercial/templates.py`
- [X] T243 Add variable grounding validation for `contextual_next_step`, `recommended_area`, `current_tool_context`, `integration_topic`, and security/out-of-profile restrictions in runtime/domain validators

### LLM-First Policy, Prompt, And Runtime Context

- [X] T244 Update `services/taliya-agent-runtime/app/domains/taliya_commercial/behavior_policy.py` with the product-followup delta rules without re-opening protected copy
- [X] T245 Update `services/taliya-agent-runtime/app/domains/taliya_commercial/prompts.py` so the LLM can choose `product_how_it_works`, `comparison_current_tool`, `integration_scope_question`, `trust_security_question`, `out_of_profile`, `conversation_resume`, `general_objection`, and `diagnostic_refusal`
- [X] T246 Add compact `post_diagnostic_context` to the LLM payload in `services/taliya-agent-runtime/app/runtime/runner.py`, populated only from saved diagnostic/demo/waitlist state
- [X] T247 Ensure post-diagnostic direct questions answer first, use saved diagnostic context when useful, and do not re-run the diagnostic
- [X] T248 Ensure diagnostic refusal keeps the conversation useful without forcing diagnostic in the same turn
- [X] T249 Ensure general objections are handled through LLM+policy first, with no new `product.general_objection_response` template unless eval evidence proves it is needed

### Evals And Fixtures

- [X] T250 Add fixture coverage under `scripts/fixtures/agent-runtime/` for how-it-works, post-diagnostic follow-up, comparison, integration/WhatsApp scope, security/data, out-of-profile, diagnostic refusal, and protected-route regression
- [X] T251 Extend eval checks to validate no-CRM lay-copy, owner-language/non-technical copy, post-diagnostic memory use, no diagnostic restart, no unsupported integration/security promises, diagnostic-refusal respect, and required LLM evidence on commercial product-followup routes
- [X] T252 Add or extend quality-judge scenarios for the new delta routes, scoring directness, naturalness, usefulness, official facts, state awareness, brevity, and Pilates-studio-owner language
- [X] T253 Run zero-cost gates for all new delta routes before any real OpenAI run
- [X] T254 Run quota-limited real OpenAI scenarios only for representative new routes after zero-cost gates pass
- [X] T255 Save full transcripts, route decisions, template ids, product source keys, cost, and latency under `eval-reports/`

### Protected Regression And Completion

- [X] T256 Run protected-route regression for openings, price direct, price-plus-pain, demo direct, WhatsApp direct, diagnostic script, final diagnostic, waitlist, handoff, safety, Sales Inbox, and delivery shape
- [X] T257 Verify protected-route cost and latency remain inside configured bands and do not regress by more than 10% versus the latest approved baseline without product-owner approval; verify new routes stay inside configured model-call and spend caps
- [X] T258 Verify Sales Inbox persists new meaningful route signals, including product explanation, comparison, integration, security, out-of-profile, diagnostic refusal, conversation resume, and post-diagnostic follow-up
- [X] T259 Update `release-readiness.md`, `product-owner-transcript-review.md`, and completion evidence with the new delta results
- [ ] T260 Record product-owner approval only after reviewing representative transcripts for the new delta and confirming protected behavior did not regress

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1**: No dependencies.
- **Phase 2**: Depends on Phase 1. Blocks all user story implementation.
- **US2**: Should be first because it establishes reference-faithful runtime architecture.
- **US1**: Depends on US2 and integrates channels.
- **US3, US4, US5, US6**: Depend on US2; can proceed in parallel after basic runner exists.
- **US7**: Depends on runtime persistence from US2-US6.
- **US8**: Can proceed after Phase 2 and in parallel with US2.
- **US9**: Depends on enough runtime behavior to run realistic transcripts.
- **Corrective Phase**: Required after product-owner behavior audit and blocks deploy/cutover tasks T132-T137.
- **Final Product-Owner Behavior Phase T158-T205**: Historical behavior realignment evidence. It remains useful, but it does not approve production after the later diagnostic/demo/name corrections.
- **Product-Owner Final Diagnostic/Demo/Name Correction Phase T206-T226**: Required after final product-owner corrections and blocks deploy/cutover tasks T132-T137 and product-owner approval T157/T205.
- **Production deploy tasks T132-T137**: Depend on all required P1 stories, corrective behavior tasks, final diagnostic/demo/name correction tasks T206-T226, product-owner transcript approval, and production gate docs.

### User Story Dependencies

- **US2 (Architecture fidelity)**: Required before production conversation behavior.
- **US1 (LLM-first conversation)**: Requires US2.
- **US3 (Product knowledge)**: Requires US2 and foundational product source.
- **US4 (Diagnostic)**: Requires US2 and lead facts tools.
- **US5 (Waitlist)**: Requires US2 and product/lead tools.
- **US6 (Handoff)**: Requires US2 and memory/handoff tools.
- **US7 (Operator visibility)**: Requires persisted runtime events from earlier stories.
- **US8 (Future-agent naming)**: Independent after foundation.
- **US9 (Quality gates)**: Validates all P1 stories.

### Parallel Opportunities

- Foundation tests T012-T019 can run in parallel.
- Product knowledge, diagnostic, waitlist, and handoff fixtures can be authored in parallel.
- US3, US4, US5, and US6 can be implemented by separate workers if their file ownership is coordinated.
- Eval runners can be built in parallel once the runtime API contract is stable.
- T162-T172 can be authored in parallel because they cover separate zero-cost gates.
- T173-T178 should be serial because schemas, templates, renderer, and runner behavior depend on each other.
- T183-T187 should be serial because diagnostic ledger semantics must be implemented before persistence and completion validators.

---

## Implementation Strategy

### MVP First

1. Complete Phase 1 and Phase 2.
2. Complete US2 architecture fidelity.
3. Complete US1 channel-to-runtime conversation path.
4. Complete US3 official product knowledge answers.
5. Stop and validate with direct commercial conversations before adding diagnostic/waitlist complexity.

### Production Completion

1. Complete final diagnostic/demo/name correction tasks T206-T226.
2. Pass zero-cost gates before any broad real OpenAI run.
3. Run quota-limited real OpenAI smoke.
4. Run full mapped behavior matrix.
5. Complete Sales Inbox completeness validation.
6. Record product-owner transcript approval.
7. Deploy Railway runtime and Next integration only after explicit confirmation.
8. Make new runtime the only official production conversation path.

### Explicit Non-Goals

- Do not redesign `/pilates`.
- Do not implement client/studio WhatsApp connections.
- Do not implement multi-tenant studio agents.
- Do not implement the seven future studio operation agents.
- Do not keep the deterministic v2 as conversational fallback.
