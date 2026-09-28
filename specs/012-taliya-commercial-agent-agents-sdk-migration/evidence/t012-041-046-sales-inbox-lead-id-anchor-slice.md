# T012-041/T012-046 Sales Inbox Lead ID Anchor Slice

Date: 2026-06-11

## Scope

Tightened the T012-046 Sales Inbox export test so the T012-041 contract gate
explicitly proves `lead_id` is part of the required projection-field contract.

The T012-041 manifest already requires
`test_t012_046_exports_sales_inbox_projection_evidence_package`; this slice
makes that anchor assert the new `lead_id` requirement directly.

## Files Changed

- `services/taliya-agent-runtime/tests/test_spec012_sales_inbox_projection.py`

## Behavior Covered

The mocked Sales Inbox projection package test now asserts:

- package schema is `012.sales_inbox_projection_export.v1`;
- `lead_id` is present in `required_projection_fields`;
- projected turns carry `lead_id`;
- projection remains complete and no-cost.

## Tests Run

- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_sales_inbox_projection.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q`
  - Result: `5 passed`
- `python -m ruff check services/taliya-agent-runtime/tests/test_spec012_sales_inbox_projection.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`
  - Result: passed

## Anti-Determinism Review

Test-only contract reinforcement. No raw lead-text routing, prompt, template,
validator, renderer, exporter behavior, or runtime behavior changed.

## Protected Scope Review

No `/pilates`, landing visual, Sales Inbox UI, multi-tenant, client/studio
WhatsApp, checkout, or public endpoint files were changed.

## Paid Call Review

No paid OpenAI call was made.

## Open Items

T012-041 and T012-046 remain open for final verification after endpoint/runtime
integration and approved real-model/shadow evidence.
