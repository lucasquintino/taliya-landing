# Self Review - Spec 012 Draft

Review date: 2026-06-04.

## Review Scope

Reviewed the Spec 012 draft for:

- alignment with `AGENTS.md` and `taliya-llm-first-agent`;
- preservation of Spec 010/011 behavior;
- OpenAI Agents SDK fit;
- anti-determinism boundaries;
- protected scope;
- implementation-risk gaps.

## Mechanical Checks

Completed:

- All expected Spec 012 files exist.
- No unresolved draft markers found.
- No non-ASCII characters found in the new Spec 012 docs.
- No protected source diff under `/pilates`, landing visual files, `lib/landing/floating-agent.ts`, or `components/internal/SalesInboxClient.tsx`.
- No code implementation was changed.
- Added implementation control files after review: `implementation-ledger.md`, `coverage-map.md`, and `decision-log.md`.

## Architecture Review

The draft is directionally correct because it changes the failing part of Spec 011: the custom conversation motor.

Strong points:

- Keeps Spec 011 as behavior/quality source of truth.
- Moves agent-native work to Agents SDK instead of rebuilding it.
- Requires structured SDK output before validation/rendering.
- Blocks direct delivery of SDK free-form text.
- Classifies tools by side effect.
- Requires spike before implementation.
- Keeps shadow mode, rollback, manual review, and Sales Inbox gates.

## Main Risks Still Present

### R1 - SDK output may become another schema bottleneck

Risk: `TaliyaTurnProposal` could become as large and brittle as `ConductorDecision`.

Mitigation in docs:

- `TaliyaTurnProposal` must capture rich understanding, but not become a full hidden renderer/compiler.
- Spike aborts if a large custom compiler is still needed.

Further review needed:

- Define `TaliyaTurnProposal` carefully in T012-010.

### R2 - Real SDK handoffs may raise cost

Risk: triage plus specialist handoffs can use more model operations than current one-call target.

Mitigation in docs:

- persisted current-agent start is allowed from state;
- cost/max-turn policy required;
- spike must report calls and cost.

Further review needed:

- T012-015 must set concrete max-turn and budget thresholds.

### R3 - Tools can accidentally become state mutators

Risk: SDK tools make it easy to mutate context/state during reasoning, like the demo reference.

Mitigation in docs:

- read-only/proposal-only tools by default;
- commit tools are not exposed to free SDK reasoning;
- runtime commits only after validation.

Further review needed:

- T012-012 must explicitly list each tool and side-effect class.

### R4 - Validators may remain too large

Risk: keeping current `validators.py` mostly intact could preserve complexity.

Mitigation in docs:

- validators are preserved as contract enforcement, but may need reduction/splitting;
- no validator may become a second commercial brain.

Further review needed:

- Implementation should split validators by contract family before/while adapting them.

### R5 - We may overfit to the reference demo

Risk: copying `openai-cs-agents-demo` literally can overuse handoffs/tools and mutate state too early.

Mitigation in docs:

- `reference-map.md` says what not to copy literally;
- Spec 012 is stricter on validation, projection, WhatsApp delivery, and product facts.

Further review needed:

- Spike must compare cost/quality of handoff topology vs simpler specialist start.

## Conflicts Found

No hard conflict found between:

- Spec 012 and `AGENTS.md`;
- Spec 012 and the local `taliya-llm-first-agent` skill;
- Spec 012 and protected `/pilates` scope;
- Spec 012 and Spec 011 behavior contracts.

One intentional supersession:

- Spec 012 supersedes Spec 011's implementation strategy for the conversation motor, especially action-first conductor plus decision compiler. It does not supersede Spec 011 behavior, eval, or quality gates.

## Gaps To Close Before Implementation

Must close before code:

- Confirm D-012-001 through D-012-007 in `spec.md`.
- Record D-012-001 through D-012-007 in `decision-log.md`.
- Keep `implementation-ledger.md` updated after every task closure.
- Keep `coverage-map.md` free of uncovered P0/P1 behavior before SDK core implementation, shadow mode, or activation.
- Define `TaliyaTurnProposal`.
- Define exact SDK topology.
- Define tool side-effect catalog.
- Define trace privacy policy.
- Define paid spike budget.
- Define abort criteria with measurable thresholds.

## Follow-Up Review - 2026-06-05

Finding: the architecture was coherent, but execution guarantees were not explicit enough to prevent drift during implementation.

Resolution:

- added an implementation ledger for task-by-task closure evidence;
- added a coverage map for behavior/architecture ownership and release gates;
- added a decision log for Phase 0 confirmations;
- updated `spec.md`, `plan.md`, and `tasks.md` so these controls are mandatory before and during implementation.

Remaining risk: the controls do not guarantee that the LLM will always be perfect. They guarantee that implementation cannot silently drift back into deterministic commercial routing, skip evidence, skip product-owner approval, or ship with uncovered P0/P1 requirements.

## Current Recommendation

Continue documenting and reviewing Spec 012.

Do not implement SDK code until the user approves:

- the Spec 012 decision;
- spike scope;
- paid budget, if any;
- privacy/tracing policy.
