# T012-040 Slice - SDK External Tracing Static Audit

Date: 2026-06-11

## Scope

Added a static audit guard that keeps the isolated Agents SDK path local-only
for traces until explicit approval changes D-012-007/D-012-009.

The audit blocks:

- `set_tracing_disabled(False)`;
- `tracing_disabled=False`;
- JSON-like `tracing_disabled: false` markers;
- an enabled `external_trace_export` marker in the SDK core.

It also asserts the existing SDK runner and paid-spike harness keep tracing
disabled and that the local trace exporter marks external trace export as
disabled.

## Files Changed

- `services/taliya-agent-runtime/tests/test_spec012_static_audit.py`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-040-sdk-external-tracing-static-audit-slice.md`

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_static_audit.py -q`
  - result: 7 passed
- `python -m ruff check app\core\taliya_commercial_sdk\action_trace.py tests\test_spec012_action_trace_export.py tests\test_spec012_static_audit.py`
  - result: all checks passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 209 passed, 716 deselected

## Anti-Determinism Review

Static audit only. It does not inspect lead text, choose actions, alter prompts,
or add commercial routing.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, public
endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None. Cost: `$0`.

## Still Open

T012-040 remains open for the final verification pass after endpoint/API,
delivery, trace persistence, and cutover-related changes exist.
