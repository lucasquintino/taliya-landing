# T012-046 Sales Inbox Lead ID Required Refresh Slice

Date: 2026-06-11

## Scope

Strengthened the mocked Sales Inbox projection evidence package by making
`lead_id` a required top-level projection field, then regenerated the stored
local package.

Sales Inbox projection evidence is not useful if it cannot identify which lead
the projected row belongs to.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_sales_inbox_evidence.py`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-046-mocked-sales-inbox-projection-package/sales-inbox-projection-package.json`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-046-mocked-sales-inbox-projection-package/sales-inbox-projection-package.md`

## Behavior Covered

The Sales Inbox projection evidence exporter now requires:

- `conversation_id`
- `lead_id`
- `commercial_stage`
- `diagnostic_status`
- `fields`

The refreshed mocked package validates:

- `projection_complete=true`
- `projection_count=3`
- every delivered/projection-required turn has `lead_id`
- total cost remains `$0`

## Tests And Checks Run

- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_sales_inbox_projection.py -q`
  - Result: `3 passed`
- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_sales_inbox_projection.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q`
  - Result: `5 passed`
- `python -m ruff check services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_sales_inbox_evidence.py services/taliya-agent-runtime/tests/test_spec012_sales_inbox_projection.py`
  - Result: passed
- Package validation script:
  - `projection_complete=True`
  - `missing_lead_id_turns=[]`
  - `projection_count=3`

## Anti-Determinism Review

Evidence/export contract only. No raw lead-text routing, prompt, template,
validator, renderer, or commercial behavior changed.

## Protected Scope Review

No `/pilates`, landing visual, Sales Inbox UI, multi-tenant, client/studio
WhatsApp, checkout, or public endpoint files were changed.

## Paid Call Review

No paid OpenAI call was made. The package uses `ScriptedFakeModel`.

## Open Items

T012-046 remains open for final Sales Inbox projection evidence after endpoint
persistence/integration and real-model/shadow evidence.
