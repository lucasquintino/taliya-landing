# T012-045 Slice - Mocked Mandatory Trace Evidence

Date: 2026-06-11

## Scope

Started T012-045 with a local mandatory trace evidence package generated from
the isolated action-first runner and a mocked no-cost Agents SDK model.

Generated package:

- `evidence/t012-045-mocked-mandatory-trace-package/mandatory-trace-package.json`
- `evidence/t012-045-mocked-mandatory-trace-package/mandatory-trace-package.md`

Refresh note 2026-06-11: the package was regenerated after the T012-034
trace-map compatibility slice. See
`evidence/t012-045-trace-package-refresh-after-trace-map-slice.md`.

The scenario covers:

- price question through triage + product agent;
- diagnostic start;
- diagnostic answer capture;
- human handoff request;
- suppressed follow-up turn while human handoff is active.

The package proves complete traces for delivered turns and no trace requirement
for the suppressed operational turn.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_trace.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_trace_export.py`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-045-mocked-mandatory-trace-package/mandatory-trace-package.json`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-045-mocked-mandatory-trace-package/mandatory-trace-package.md`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-045-mocked-mandatory-trace-evidence-slice.md`

## Evidence Summary

From `mandatory-trace-package.md`:

- schema: `012.action_trace_export.v1`;
- proof mode: `mocked_no_cost`;
- trace complete: `True`;
- external trace export enabled: `False`;
- turn count: `5`;
- trace count: `4`;
- total model operations: `6`;
- total cost USD: `0.0`.

The refreshed package now includes `context_snapshot`, `taliya_proposal`, and
`delivery` in `required_sections` and in every trace-required turn. Delivery
flags remain local-only: `public_delivery=false`, `outbox_reserved=false`, and
`direct_sdk_delivery_allowed=false`.

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_action_trace_export.py tests\test_spec012_static_audit.py -q`
  - result: 9 passed
- `python -m ruff check app\core\taliya_commercial_sdk\action_trace.py tests\test_spec012_action_trace_export.py tests\test_spec012_static_audit.py`
  - result: all checks passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 209 passed, 716 deselected

## Anti-Determinism Review

The semantic decisions in the scenario are mocked `ConductorActionDecision`
outputs from the fake SDK model. Runtime code does not parse raw lead text to
choose price, diagnostic, or handoff behavior. Deterministic work is limited to
trace packaging, compiler/validator/render records, and operational human
handoff suppression.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, public
endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None. Cost: `$0`.

## Still Open

T012-045 remains open for final mandatory trace evidence after the endpoint,
runtime persistence, real-model golden runs, and shadow/cutover path are
approved and available. This slice is mocked/isolated proof only.
