# T012-041/T012-047 Manual Review Anchor Slice

Date: 2026-06-11

## Scope

Added the T012-047 manual transcript review package test to the no-cost SDK
contract gate manifest.

The T012-041 manifest now requires:

- `test_spec012_manual_review_package.py::test_t012_047_exports_manual_transcript_review_package`

This keeps the mocked manual-review package format from living only as a loose
test/evidence artifact.

## Files Changed

- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-041-047-manual-review-anchor-slice.md`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/implementation-ledger.md`

## Tests

Run from repository root:

- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_manual_review_package.py -q`
  - result: 3 passed
- `python -m ruff check services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_manual_review_package.py`
  - result: all checks passed
- `python -m pytest services/taliya-agent-runtime/tests -k spec012 -q`
  - result: 224 passed, 716 deselected

## Anti-Determinism Review

This slice changes only the test manifest. It adds no raw lead-text routing, no
prompt change, no template change, no validator shortcut, and no customer copy.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, public
endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None. Cost: `$0`.

## Still Open

T012-041 and T012-047 remain open for final verification after endpoint/runtime
integration, real-model golden transcripts, shadow/cutover evidence, and
product-owner manual review are available and approved.
