# T012-054 - First-Hours Emergency Watch Prepared Locally

Date: 2026-06-16

## Scope

Prepared the first-hours emergency watch as a local/no-real-leads runbook.

Because the current production environment has no real leads, this task does
not create a live monitoring rotation, does not enable public SDK activation,
does not run real traffic shadowing, and does not spend OpenAI credits.

## Watch Purpose

If T012-055 is explicitly approved later, the first-hours watch is the short
operational checklist used immediately after activation to catch:

- missing or malformed assistant delivery;
- unexpected public fallback to the old commercial motor;
- model/provider errors;
- cost cap or paid-call anomalies;
- trace/projection gaps;
- internal-label or policy-text leaks;
- unsafe promise regressions;
- handoff pause/resume regressions;
- idempotency or duplicate delivery issues.

## First-Hours Watch Window

Recommended watch window after any future activation:

- first check within 5 minutes;
- active watch for at least 2 hours;
- verify every delivered turn has local trace/projection evidence;
- verify every blocked turn has a clear operational reason;
- verify no paid cost exceeds the configured cap;
- stop activation if any P0 issue appears.

## Stop Conditions

Stop/rollback immediately if any of these happen:

- customer-visible internal instruction, source label, policy text, or prompt
  content appears;
- SDK final free-form text bypasses approved rendering;
- old deterministic commercial brain receives public commercial traffic;
- public delivery occurs while shadow mode is expected;
- a human-handoff paused conversation receives automated follow-up;
- price, discount, checkout, availability, integration, security, or health
  claims violate official facts or validators;
- cost cap is exceeded or cost accounting is missing;
- trace or Sales Inbox projection is absent for a delivered turn.

## Evidence Sources To Inspect During Watch

Use these existing local evidence paths as the baseline:

- `evidence/t012-043-real-model-golden-transcripts/20260616T121413Z/`
- `evidence/t012-044-do-not-do-fixtures.md`
- `evidence/t012-045-mandatory-trace-evidence/`
- `evidence/t012-046-sales-inbox-projection-evidence/`
- `evidence/t012-047-manual-transcript-review-package/`
- `evidence/t012-050-simulated-shadow-mode.md`
- `evidence/t012-051-simulated-shadow-comparison/`
- `evidence/t012-052-rollback-no-old-brain.md`
- `evidence/t012-053-production-preflight-local-no-real-leads.md`

## Checks Reused From Preflight

The local watch preparation relies on the T012-053 checks:

```text
35 passed in 3.12s
```

for SDK preflight, paid harness dry-run, static audit, and contract gate.

The real-model golden runner was also checked in preflight-only mode:

```text
paid_call_status: not_attempted_preflight_only
scenario_count: 9
```

## Anti-Determinism Review

This task adds an operational watch runbook only.

It does not add raw lead-text routing, template-first shortcuts, direct SDK
free-form delivery, old-runner fallback, or SDK tool commits during reasoning.

## Protected-Scope Diff

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant,
client/studio WhatsApp, endpoint cutover, or production delivery files were
changed for this task.

## Paid-Call Status

No paid call was made for T012-054.

## Closure

T012-054 is closed as local/no-real-leads first-hours emergency watch
preparation.

Next task: T012-055 activation. This remains blocked until explicit user
approval for public activation.
