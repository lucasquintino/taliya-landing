# T012-053 - Production Preflight Prepared Locally

Date: 2026-06-16

## Scope

Prepared the Spec 012 production preflight in the only scope currently approved:
local/no-real-leads readiness checks.

The user clarified that there are no real production leads yet, so this task
does not run real traffic shadowing, does not activate the public SDK path, and
does not spend OpenAI credits.

## Preconditions Checked

- Spec 012 action-first SDK path exists behind feature flag.
- Public activation remains blocked by T012-055.
- Real production lead traffic shadowing remains unapproved and unnecessary for
  the current environment.
- External/provider trace export remains disabled.
- Rollback proof from T012-052 remains the operational rollback gate.
- T012-043 approved real-model golden transcript run exists and passed 9/9.
- T012-044 do-not-do fixtures passed.
- T012-045 trace evidence is complete.
- T012-046 Sales Inbox projection evidence is complete.
- T012-047 manual transcript review package exists.
- T012-050 simulated shadow mode is implemented.
- T012-051 simulated shadow comparison passed 9/9.

## Checks Run

```text
python -m pytest -q services/taliya-agent-runtime/tests/test_spec012_sdk_preflight.py services/taliya-agent-runtime/tests/test_spec012_sdk_paid_harness_dry_run.py services/taliya-agent-runtime/tests/test_spec012_static_audit.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result:

```text
35 passed in 3.12s
```

```text
python scripts\eval-agent-runtime-spec012-real-model-golden.py --preflight-only
```

Result:

```text
schema: 012.real_model_golden_transcripts_preflight.v1
scenario_count: 9
scenario_ids:
- final-price-first
- final-price-plus-pain
- final-pain-first
- final-instagram-interest
- final-whatsapp-question
- step3g-long-conversation
- final-waitlist-joined
- final-human-request-silent-after
- final-demo-request
openai_api_key_available: true
max_total_cost_usd: 1.0
paid_call_status: not_attempted_preflight_only
```

## Production Preflight Checklist

Pass:

- No-cost preflight loads all 9 canonical golden scenarios.
- No-cost preflight confirms the configured model has recorded pricing.
- No-cost preflight confirms a key is available, but does not call OpenAI.
- SDK contract gate, static audit, SDK preflight, and paid harness dry-run pass.
- Public fallback to the old commercial brain remains blocked by T012-052.
- Simulated shadow path suppresses public delivery and does not mutate live
  runtime state.

Still intentionally blocked:

- Public SDK activation.
- Real production traffic shadowing.
- Paid OpenAI confirmation beyond already approved T012-043 evidence.
- External trace export containing lead text.

## Anti-Determinism Review

This task changes no commercial routing logic. It adds evidence only.

No raw lead-text regex routing, template-first shortcut, direct SDK free-form
delivery, old runner fallback, or SDK reasoning-time commit was added.

## Protected-Scope Diff

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant,
client/studio WhatsApp, or public cutover files were changed for this task.

## Paid-Call Status

No paid call was made for T012-053.

The real-model preflight command was executed with `--preflight-only` and
reported `paid_call_status: not_attempted_preflight_only`.

## Closure

T012-053 is closed as local/no-real-leads production preflight preparation.

Next task: T012-054 first-hours emergency watch, also in a no-real-leads
preparation scope only.
