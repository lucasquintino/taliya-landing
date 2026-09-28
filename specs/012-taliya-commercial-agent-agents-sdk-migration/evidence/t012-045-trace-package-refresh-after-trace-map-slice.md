# T012-045 Trace Package Refresh After Trace-Map Slice

Date: 2026-06-11

## Scope

Regenerated the mocked mandatory trace evidence package after the T012-034
trace-map compatibility slice added new required local trace sections.

This keeps the stored T012-045 artifact aligned with the current trace
contract.

## Files Changed

- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-045-mocked-mandatory-trace-package/mandatory-trace-package.json`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-045-mocked-mandatory-trace-package/mandatory-trace-package.md`

## Behavior Covered

The refreshed package now declares and includes:

- `context_snapshot`
- `taliya_proposal`
- `delivery`

For every trace-required turn, the package validates that:

- the new sections are present;
- `trace_complete=true`;
- `public_delivery=false`;
- `outbox_reserved=false`;
- `direct_sdk_delivery_allowed=false`;
- external SDK/provider trace export remains disabled.

## Tests And Checks Run

- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_action_trace_export.py services/taliya-agent-runtime/tests/test_spec012_static_audit.py -q`
  - Result: `10 passed`
- Package validation script:
  - `trace_complete=True`
  - no missing required package sections
  - no missing required turn sections
  - `trace_count=4`

## Anti-Determinism Review

Artifact refresh only. The package was regenerated from the mocked action-first
runner with structured fake SDK decisions. No raw lead-text routing, prompt,
template, validator, renderer, or runtime behavior changed.

## Protected Scope Review

No `/pilates`, landing visual, Sales Inbox UI, multi-tenant, client/studio
WhatsApp, checkout, or public endpoint files were changed.

## Paid Call Review

No paid OpenAI call was made. The package uses `ScriptedFakeModel`.

## Open Items

T012-045 remains open for final mandatory trace evidence after endpoint/runtime
persistence, real-model golden runs, and shadow/cutover evidence.
