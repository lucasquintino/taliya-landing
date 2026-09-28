# Worktree Audit - Spec 011

Date: 2026-06-04

Purpose: no-cost pre-continuation audit before any further T011-105 paid golden/do-not-do run. This file exists to keep the implementation from drifting after long sessions and to prevent dirty worktree noise from being mistaken for release evidence.

## Current Decision

- Formal goal status remains blocked before T011-105 paid rerun until fresh paid evidence is explicitly approved and passes on the action-first source fingerprint.
- One explicitly approved T011-105 paid batch was run after this audit baseline and spent estimated US$0.108970 before stopping on the long-conversation failure, as designed.
- No production activation is allowed from this audit alone.
- T011-105 paid evidence is the current task lock and requires explicit user approval. T011-105 remains paused; T011-106 through T011-112 remain real release blockers.

## No-Cost Gate Snapshot

Latest no-cost checks observed during this reconciliation:

- T011-105 readiness: 13/13 passed, release gate `ready_for_paid_batch`.
- T011-105 closure: 2/11, expected `fail_missing_or_failed_paid_evidence`.
- Active-path static audit: 8/8 passed.
- Spec 011 runtime pytest sweep: 716 passed.
- Unit/contract gate: 7/7 passed.
- Known-validator recovery gate: 9/9 passed.
- Action coverage contract: every exposed `TurnAction` is either compiled or operationally handled; no pending action bucket remains before paid readiness.
- Protected source diff for `/pilates`, landing components/data, `lib/landing/floating-agent.ts`, and `components/internal/SalesInboxClient.tsx`: empty.

These checks prove local readiness and guardrails, not final behavioral closure.

## Paid Batch Observation - 2026-06-04

The latest approved paid batch started from readiness fingerprint `b818ed2356dcc3f52456cabdae2c95de740d30186fe935f1a10ec63ffcc8e9d8`, passed `final-pain-first`, then failed `step3g-long-conversation` with HTTP 500 on turns 9, 11, 12, and 13. It stopped before the do-not-do scenarios and consumed estimated US$0.108970.

Local no-cost fixes after that failure now cover the non-boolean `facts[].renderable` schema failure and the price-objection repair/template-plan failure. The deeper audit found that continuing to patch validator/repair branches is not enough: the conductor still produces an unconstrained full state/render plan, which leaves too many ways for long conversations to fail structurally. Do not use this worktree audit as justification for another paid run until T011-104A completes the action-first conductor correction.

Current no-cost readiness after pain-first context hardening is green on fingerprint `e458fcec6bb36bed281b3b7437582554e9b02d89d958d3bb4f216f95b4ef6987`, but T011-105 closure remains red with `fail_missing_or_failed_paid_evidence`.

## Paid Batch Observation - 2026-06-04, Pain-First Context

The approved paid batch on fingerprint `b6bc712960ac06a93f80eff575a732cfb7e3d86f22cc0e7a6cbfce54fe159c9b` spent US$0.005045 and stopped after `final-pain-first` failed. The runtime returned HTTP 200, but the golden evaluator correctly rejected the response because it did not reuse the lead context terms `whatsapp` and `interessado`.

Local no-cost fix: action-conductor validation now rejects `offer_diagnostic_from_pain` without LLM-provided `diagnostic_intent.details.pain_context_human`; the compiler no longer renders a generic fallback for pain-first; and the pain-first plan includes the approved greeting, diagnostic offer, and first required active-students question. Validation passed with 716 runtime tests, focused pain-first tests, Ruff, and readiness 13/13 on fingerprint `e458fcec6bb36bed281b3b7437582554e9b02d89d958d3bb4f216f95b4ef6987`.

## Worktree Risk Classification

| Area | Classification | Required handling before final release |
| --- | --- | --- |
| `specs/011-taliya-commercial-agent-core-reset/` | Expected Spec 011 source of truth and release evidence under active implementation | Keep, review, and commit intentionally only after current task closures are honest |
| `services/taliya-agent-runtime/app/core/`, Spec 011 tests, and `scripts/eval-agent-runtime-spec011*` | Expected Spec 011 runtime/eval implementation surface | Keep under the current task lock; no task may close without linked evidence |
| `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/` | Historical/legacy evidence noise | Do not treat as current Spec 011 release proof unless explicitly mapped in Spec 011 docs |
| `specs/006-crm-operational-core/` | Product truth input with many dirty files | Product truth changes must be reviewed before final approval so the agent does not ground claims on accidental edits |
| `.tmp-*`, `test-results/`, screenshots, and demo-kit artifacts | Temporary/manual evidence or local run artifacts | Decide keep/archive/ignore before final commit; do not let them obscure release-critical diffs |
| `services/taliya-agent-runtime/app/runtime/runner.py` | Forbidden-area dirty diff risk | Existing one-line diff adds `_looks_like_internal_lead_fact(current)` to legacy runner behavior. Static audit says active public Spec 011 path does not import/call runner, but this diff must be explained, reverted, or explicitly quarantined before final closure |

## Anti-Drift Rules Reconfirmed

- Do not change `/pilates` layout, copy, styling, sections, animations, mockups, or composition.
- Do not add commercial brain logic to `runtime/runner.py`.
- Do not use old TS v2 or Python runner paths as public fallback responders.
- Do not introduce regex, token lists, templates, or renderer defaults as the primary decider for price, demo, plan-fit, pain-first, diagnostic, waitlist, source/social openings, product questions, or mixed intent.
- Templates remain approved language after a structured LLM decision, not the conversation brain.
- Sales Inbox remains a projection of validated state/events, not a second interpretation engine.
- Low cost is acceptable only when prompt size was reduced while commercial turns still use structured LLM judgment.

## Next Allowed Paid Action

No paid action is currently allowed without explicit user approval. Phase 5B and T011-104A closure/readiness have no-cost evidence; T011-105 now needs the approved capped paid rerun on the action-first fingerprint.

Current T011-104A progress: T011-058A through T011-058F and T011-104A closure/readiness passed with no paid spend. Evidence covers `TurnSituation`, compact `ConductorActionDecision`, `DecisionCompiler`, action-first runtime adapter integration, static anti-determinism audit, mode matrix, long-conversation action preflight, action-level repair retry, full exposed action coverage, pain-first context enforcement, readiness 13/13, source fingerprint `e458fcec6bb36bed281b3b7437582554e9b02d89d958d3bb4f216f95b4ef6987`, and closure red only for missing/failing paid evidence.

After T011-104A passes and readiness is regenerated on the new fingerprint, only after explicit user approval, the current paid command shape remains:

```powershell
node scripts\eval-agent-runtime-spec011-t011-105-paid-batch.mjs --approval-token T011-105-US0.36 --approved-budget-usd 0.36
```

If that paid runner passes, run the no-cost closure gate:

```powershell
node scripts\eval-agent-runtime-spec011-t011-105-closure.mjs
```

Only if closure passes may T011-105 be marked complete in `tasks.md`, `coverage-map.md`, and `implementation-ledger.md`.
