# T012-040 Trace Delivery Static Audit Slice

Date: 2026-06-11

## Scope

Added a static audit that prevents local SDK trace/export code from claiming
public delivery before the authorized public endpoint/cutover phase.

This complements the T012-034 trace-map compatibility slice: local traces may
record rendered previews and chunk policy, but they must not represent public
outbox reservation or direct SDK delivery while the SDK path remains isolated.

## Files Changed

- `services/taliya-agent-runtime/tests/test_spec012_static_audit.py`

## Behavior Covered

The static audit scans isolated SDK Python files and blocks:

- `public_delivery=True`
- `outbox_reserved=True`
- `direct_sdk_delivery_allowed=True`

It also asserts the local trace implementation explicitly keeps:

- `public_delivery=False`
- `outbox_reserved=False`
- `direct_sdk_delivery_allowed=False`

## Tests Run

- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_static_audit.py -q`
  - Result: `8 passed`
- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_static_audit.py services/taliya-agent-runtime/tests/test_spec012_action_trace_export.py -q`
  - Result: `10 passed`
- `python -m ruff check services/taliya-agent-runtime/tests/test_spec012_static_audit.py`
  - Result: passed

## Anti-Determinism Review

This is static verification only. It does not parse lead text, route commercial
intent, change prompts, change templates, or alter runtime behavior.

## Protected Scope Review

No `/pilates`, landing visual, Sales Inbox UI, multi-tenant, client/studio
WhatsApp, checkout, or public endpoint files were changed.

## Paid Call Review

No paid OpenAI call was made.

## Open Items

T012-040 remains open for the final verification pass after endpoint/API/
delivery integration. This slice strengthens the current isolated/no-public-
delivery invariant.
