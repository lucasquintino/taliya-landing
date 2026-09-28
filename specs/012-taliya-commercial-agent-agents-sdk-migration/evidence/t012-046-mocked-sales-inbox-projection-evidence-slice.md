# T012-046 Slice - Mocked Sales Inbox Projection Evidence

Date: 2026-06-11

## Scope

Started T012-046 with a local Sales Inbox projection evidence package generated
from the isolated action-first runner and a mocked no-cost Agents SDK model.

Generated package:

- `evidence/t012-046-mocked-sales-inbox-projection-package/sales-inbox-projection-package.json`
- `evidence/t012-046-mocked-sales-inbox-projection-package/sales-inbox-projection-package.md`

The scenario covers:

- price answer projected as `diagnostic_offered`;
- diagnostic start projected as `diagnostic_waiting_answer`;
- human handoff projected as `human_handoff`;
- suppressed follow-up turn while human handoff is active, with no projection
  required.

The package proves projections are derived from delivered, validated turns and
that suppressed operational turns are not treated as missing projections.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_sales_inbox_evidence.py`
- `services/taliya-agent-runtime/tests/test_spec012_sales_inbox_projection.py`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-046-mocked-sales-inbox-projection-package/sales-inbox-projection-package.json`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-046-mocked-sales-inbox-projection-package/sales-inbox-projection-package.md`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-046-mocked-sales-inbox-projection-evidence-slice.md`

## Evidence Summary

From `sales-inbox-projection-package.md`:

- schema: `012.sales_inbox_projection_export.v1`;
- proof mode: `mocked_no_cost`;
- projection complete: `True`;
- turn count: `4`;
- projection count: `3`;
- total model operations: `5`;
- total cost USD: `0.0`.

Refresh note 2026-06-11: the package was regenerated after `lead_id` became a
required top-level projection field. See
`evidence/t012-046-sales-inbox-lead-id-required-refresh-slice.md`.

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_sales_inbox_projection.py -q`
  - result: 3 passed
- `python -m ruff check app\core\taliya_commercial_sdk\action_sales_inbox_evidence.py tests\test_spec012_sales_inbox_projection.py`
  - result: all checks passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 210 passed, 716 deselected

## Anti-Determinism Review

This slice exports projections already produced by the validated action-first
runner. It does not inspect raw lead text, choose commercial meaning, or add
Sales Inbox inference logic. Semantic action choice remains in the mocked LLM
`ConductorActionDecision`; projection generation remains the preserved Spec 011
adapter path.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, public
endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None. Cost: `$0`.

## Still Open

T012-046 remains open for final Sales Inbox projection evidence after endpoint
persistence/integration and real-model/shadow evidence are approved and
available. This slice is mocked/isolated proof only.
