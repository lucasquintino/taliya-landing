# T012-047 Slice - Mocked Manual Transcript Review Package

Date: 2026-06-11

## Scope

Started T012-047 with a local manual transcript review package for the isolated
action-first runner.

Generated package:

- `evidence/t012-047-mocked-manual-transcript-review-package/manual-transcript-review-package.json`
- `evidence/t012-047-mocked-manual-transcript-review-package/manual-transcript-review-package.md`

The package includes:

- transcript in human-readable order;
- turn summary with status, mode, action, and templates;
- per-turn trace/projection presence flags for reviewer context;
- final state and usage/cost in JSON;
- manual-review checklist;
- `review_status = pending_manual_review`;
- `manual_decision = pending`.

The package intentionally does not self-approve quality. Product-owner/manual
review remains required.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/manual_review_package.py`
- `services/taliya-agent-runtime/tests/test_spec012_manual_review_package.py`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-047-mocked-manual-transcript-review-package/manual-transcript-review-package.json`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-047-mocked-manual-transcript-review-package/manual-transcript-review-package.md`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-047-mocked-manual-review-package-slice.md`

## Evidence Summary

From `manual-transcript-review-package.md`:

- schema: `012.manual_transcript_review.v1`;
- proof mode: `mocked_no_cost`;
- review status: `pending_manual_review`;
- manual decision: `pending`;
- turn count: `4`;
- delivered turns: `3`;
- suppressed turns: `1`;
- total model operations: `5`;
- total cost USD: `0.0`.
- delivered turns with trace present: `3`;
- delivered turns with Sales Inbox projection present: `3`;
- suppressed turns without trace/projection requirement: `1`.

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_manual_review_package.py -q`
  - result: 1 passed
- `python -m ruff check app\core\taliya_commercial_sdk\manual_review_package.py tests\test_spec012_manual_review_package.py`
  - result: all checks passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 224 passed, 716 deselected

Additional focused validation from repository root:

- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_manual_review_package.py services/taliya-agent-runtime/tests/test_spec012_action_trace_export.py services/taliya-agent-runtime/tests/test_spec012_sales_inbox_projection.py -q`
  - result: 6 passed
- JSON package assertion:
  - delivered turns: `3/3` have `trace_present=true` and `sales_inbox_projection_present=true`;
  - suppressed turns: `1/1` have `trace_present=false` and `sales_inbox_projection_present=false`.

## Anti-Determinism Review

This slice adds packaging only. It does not judge transcript quality
automatically, inspect raw lead text to choose actions, alter prompts, render
new customer copy, or add commercial routing. The transcript comes from mocked
LLM `ConductorActionDecision` outputs through the existing action-first runner.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, public
endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None. Cost: `$0`.

## Still Open

T012-047 remains open for the final product-owner/manual review package after
real-model golden transcripts and shadow/cutover evidence are approved and
available. This slice proves the package format and local mocked generation.
