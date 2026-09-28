# T012-040 Slice - Public Isolation Static Audit

Date: 2026-06-11

## Scope

Advanced T012-040 with a no-cost static audit check for public isolation before
feature-flag cutover.

Covered in this slice:

- `app/` outside `app/core/taliya_commercial_sdk/` must not import
  `taliya_commercial_sdk`;
- public app code must not call `run_action_turn`;
- this complements the existing static checks for regex-as-commercial-brain,
  commit SDK tools, direct SDK free text, and old-runner fallback inside the
  isolated runner.

## Sources

- `specs/012-taliya-commercial-agent-agents-sdk-migration/static-anti-drift-audit.md`
  - blocks old runner/public fallback and SDK direct delivery before safe
    cutover.
- `specs/012-taliya-commercial-agent-agents-sdk-migration/tasks.md`
  - T012-031 endpoint integration is still open, so public SDK imports remain
    forbidden until feature-flag work is explicit.
- `.agents/skills/taliya-llm-first-agent/SKILL.md`
  - no public cutover or old deterministic commercial fallback while the SDK
    path is isolated.

## Files Changed

- `services/taliya-agent-runtime/tests/test_spec012_static_audit.py`

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_static_audit.py -q`
  - result: 5 passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 147 passed, 716 deselected
- `python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_turn_situation.py tests\test_spec012_action_agents.py tests\test_spec012_decision_compiler.py tests\test_spec012_action_turn_runner.py tests\test_spec012_action_validators_ported.py tests\test_spec012_static_audit.py tests\test_spec012_action_safety.py`
  - result: all checks passed

## Anti-Determinism Review

This is a static guard only. It does not alter runtime behavior or add
commercial interpretation. It prevents premature public imports of the isolated
SDK path before the feature-flag integration task is deliberately implemented.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, or
client/studio WhatsApp files were edited.

## Paid Calls

None.

## Still Open

- expand the audit when T012-031 introduces the feature-flagged endpoint path;
- add static checks for hardcoded prices/checkout/date promises in any new
  production templates/prompts;
- run T012-040 as part of the full verification phase.
