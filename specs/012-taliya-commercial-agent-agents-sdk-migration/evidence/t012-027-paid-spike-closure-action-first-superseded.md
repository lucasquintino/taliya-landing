# T012-027 - Paid SDK Spike Closure

Date: 2026-06-16

## Status

Closed as executed and superseded.

T012-027 required running the approved paid SDK spike scenarios. That happened
across the documented paid attempts. The original template-first spike reached
the structural pass bar, but also exposed the same boundary failure that later
led to D-012-012: the LLM must not own final template plans, official variables,
or state transitions.

The production path is therefore not the original template-first spike. It is
the action-first Agents SDK architecture:

```text
Turn Situation Builder -> LLM ConductorActionDecision -> Decision Compiler
-> validators -> renderer -> commit/delivery
```

## Evidence Used

- `evidence/t012-027/attempt-1/`
- `evidence/t012-027/attempt-2/`
- `evidence/t012-027/attempt-3/`
- `evidence/t012-027/attempt-4/`
- `evidence/t012-027/attempt-5/`
- `evidence/t012-027/attempt-6/`
- `evidence/t012-027/attempt-7/`
- `evidence/t012-027/attempt-4-to-7-and-ideal-conversation-analysis.md`
- `evidence/t012-027/action-first-battery-summary.md`
- `decision-log.md` D-012-012 and D-012-013
- `evidence/t012-028-sdk-vs-spec011-comparison.md`
- `evidence/t012-029-continue-action-first-decision.md`

## Paid Spike Result

Original template-first spike:

- paid attempts were executed under explicit user approvals;
- the 15 frozen scenarios eventually reached the structural pass bar;
- attempt 7 passed 15/15 structurally with 27 operations and `$0.069680`;
- the spike proved strict SDK output, budget/tracing controls, grounding
  pressure, tool/run reporting, and repair mechanics;
- it also proved the production boundary was wrong because structural validity
  could hide bad conversation quality and final-plan ownership by the LLM.

Action-first validation battery:

- approved by D-012-013 with `$1.00` ceiling and no public cutover;
- canary passed 3/3;
- 15 frozen scenarios delivered across action-first passes;
- staged final diagnostic delivery worked on the real model;
- ideal conversation reached 11/12 in the action-first battery, then later
  quality gates and canonical goldens moved to T012-043+.

## Why Closure Is Safe

T012-028 and T012-029 already made the product decision that the migration
continues only on action-first. Later phases then proved the production-bound
action-first path with:

- T012-030A..D action-first core;
- T012-031..037 runtime/feature-flag/rollback boundaries;
- T012-038..042 canonical fixtures, quality harness, static audit, run items;
- T012-043 approved real-model golden transcripts, 9/9;
- T012-044 do-not-do fixtures;
- T012-045 trace evidence;
- T012-046 Sales Inbox projection evidence;
- T012-047 manual review package;
- T012-050..054 simulated shadow, comparison, rollback, preflight, and watch.

Leaving T012-027 unchecked would imply the paid spike never ran, which is not
true. Treating the original spike as the production motor would be worse: it
would contradict D-012-012 and the LLM-first action-first design.

## Anti-Determinism Review

This closure changes documentation only.

It does not add deterministic raw lead-text routing, template-first shortcuts,
regex commercial understanding, SDK free-form delivery, old-runner fallback, or
SDK tool commits during reasoning.

## Protected-Scope Diff

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant,
client/studio WhatsApp, endpoint activation, or public delivery behavior was
changed for this closure.

## Paid-Call Status

No new paid call was made for this closure.

Historical paid calls remain recorded in the T012-027 evidence and decision
log. This document only closes the task bookkeeping around already executed
and superseded evidence.

## Closure

T012-027 is closed as:

```text
executed_paid_spike_superseded_by_action_first
```

The remaining open task is T012-055 public activation, which still requires
explicit user approval.
