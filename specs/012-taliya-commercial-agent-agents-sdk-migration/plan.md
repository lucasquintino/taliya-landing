# Plan - Spec 012 Agents SDK Migration

Update 2026-06-11: steps 1-4 of the migration strategy are complete (spike
executed and approved; SDK improved commercial understanding). Production
design for steps 5-7 is governed by `design-lock-v2-action-first.md`
(D-012-012); behavior source of truth remains the binding Spec 010/011
contracts; rule-by-rule enforcement mapping lives in
`conformity-matrix.pt-BR.md`.

## Objective

Replace the current handcrafted Spec 011 conversation motor with an OpenAI Agents SDK based motor while preserving the Spec 011 behavior, quality, validation, Sales Inbox, and release gates.

This plan is documentation only. It does not authorize code implementation until the user approves the Spec 012 decision and spike budget.

## Technical Context

Current stack:

- Python 3.12 FastAPI runtime under `services/taliya-agent-runtime`.
- `openai-agents` dependency already present.
- Existing public Taliya commercial endpoint: `/v1/taliya-commercial/turn`.
- Legacy `/v1/agent-runs` quarantined for public Taliya commercial turns.
- Widget and Taliya-owned WhatsApp already route through the runtime boundary.
- Product knowledge and Spec 006 product contracts are existing sources of truth.
- Spec 011 provides fixtures, validators, renderer boundaries, Sales Inbox projection expectations, and release gates.

Target stack:

- OpenAI Agents SDK for agent orchestration.
- Existing FastAPI runtime for API boundary, HMAC, idempotency, feature flags, memory, persistence, and delivery.
- Existing product/domain modules adapted as sources and validators.
- Existing eval/reporting harness adapted to SDK traces and proposals.

## Migration Strategy

Do not edit the current Spec 011 public path first.

Proceed in this order:

1. Document and approve Spec 012.
2. Build an isolated SDK spike.
3. Compare SDK behavior against current Spec 011 on critical scenarios.
4. Continue only if SDK improves commercial understanding.
5. Implement SDK core behind a feature flag.
6. Run shadow mode.
7. Cut over only after gates pass.

## Implementation Control

Spec 012 must be implemented with a live control loop:

- `decision-log.md` must record Phase 0 decisions before SDK code starts.
- `coverage-map.md` must show owner, task, and evidence for each P0/P1 requirement.
- `implementation-ledger.md` must be updated after every task closure.
- every task closure must record anti-determinism review, protected-scope diff, evidence path, paid-call status, and next task lock.
- if a task exposes an uncovered requirement or architectural drift, implementation pauses until the spec/task map is corrected.

## Phase Plan

### Phase 0 - Approval

Outcome: user-approved Spec 012 decision.

Required:

- confirm OpenAI Agents SDK;
- confirm no scope expansion;
- confirm SDK spike before implementation;
- confirm no production-state mutation during SDK reasoning;
- confirm paid budget before real OpenAI SDK runs.

### Phase 1 - Design Lock

Outcome: no-code implementation contract.

Deliverables:

- recorded decision log;
- initialized coverage map;
- initialized implementation ledger;
- `TaliyaTurnProposal` schema;
- SDK agent topology;
- SDK tool side-effect classification;
- SDK trace mapping;
- contract map from Spec 011 to SDK owners;
- spike fixtures and pass/fail rubric.

### Phase 2 - Isolated Spike

Outcome: evidence that SDK is or is not better.

Deliverables:

- isolated SDK prototype;
- mocked/no-cost contract tests;
- approved paid spike run;
- comparison report against current Spec 011;
- continue/adapt/abort recommendation.

Entry gate:

- Phase 0 decisions recorded;
- design lock complete;
- no-cost static anti-drift audit pattern defined;
- isolated path only;
- no paid run until mocked spike is green and the user approves the budget.

### Phase 3 - SDK Core

Outcome: production-ready SDK path behind feature flag.

Deliverables:

- `app/core/taliya_commercial_sdk/`;
- runtime adapter;
- validator adapter;
- trace adapter;
- renderer integration;
- Sales Inbox projection integration;
- static audits.

### Phase 4 - Verification

Outcome: SDK path proves Spec 011 behavior.

Deliverables:

- static audit;
- unit/contract tests;
- mocked SDK run-item fixtures;
- real-model golden transcripts;
- do-not-do fixtures;
- trace export;
- Sales Inbox projection export;
- manual review package.

### Phase 5 - Shadow And Cutover

Outcome: controlled production readiness.

Deliverables:

- SDK shadow-mode report;
- rollback proof;
- production preflight;
- first-hours emergency watch;
- explicit approval before activation.

## Design Constraints

- No `/pilates` visual/layout/copy changes.
- No Sales Inbox UI redesign.
- No multi-tenant.
- No client/studio WhatsApp connection.
- No checkout.
- No old runner/TS v2 public fallback.
- No raw-text deterministic commercial routing.
- No SDK free-form direct delivery.
- No unvalidated state mutation by SDK tools.

## Complexity And Risk

High-risk areas:

- SDK handoffs may increase model calls.
- SDK agents may produce good free-form text that bypasses template/validator discipline if not blocked.
- Tool side effects can corrupt state if exposed incorrectly.
- Current Spec 011 validators are large and may need careful slimming rather than blind reuse.
- SDK trace privacy and retention must be reviewed before production.

Mitigation:

- spike first;
- proposal-only tool model;
- strict output adapter;
- validators remain after SDK;
- feature flag;
- shadow mode;
- rollback proof;
- manual approval.

## Success Definition

Spec 012 succeeds only if the SDK path:

- improves commercial understanding over current Spec 011 on critical flows;
- preserves Spec 011 P0/P1 behavior;
- keeps Taliya LLM-first;
- reduces custom orchestration burden;
- produces inspectable SDK/Taliya traces;
- preserves Sales Inbox consistency;
- does not create another large custom brain.

## Stop Conditions

Stop before implementation or cutover if:

- the SDK path needs a large custom compiler to work;
- SDK free-form output is required for acceptable quality and cannot be safely rendered;
- SDK tools cannot be kept read-only/proposal-only during reasoning;
- cost becomes unacceptable without deterministic commercial shortcuts;
- the SDK path does not beat current Spec 011 on critical scenarios;
- any implementation touches protected `/pilates` visual/layout/copy.
