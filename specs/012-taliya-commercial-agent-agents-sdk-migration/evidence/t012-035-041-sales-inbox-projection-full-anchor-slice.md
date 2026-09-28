# T012-035/T012-041 Sales Inbox Projection Full Anchor Slice

Status: started / partial on 2026-06-11.

## Scope

This no-cost slice strengthens the T012-041 contract gate so all current
isolated Sales Inbox projection tests are mandatory, including the completed
diagnostic projection path.

No endpoint integration, runtime public cutover, prompt, renderer, `/pilates`,
checkout, multi-tenant, Sales Inbox UI, client/studio WhatsApp, or paid OpenAI
path was changed.

## Files

- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`

## Added Contract Coverage

The T012-041 manifest now requires
`test_t012_035_sales_inbox_projection_for_completed_diagnostic`.

With the existing anchors, `test_spec012_sales_inbox_projection.py` is now
fully covered by the contract gate:

- price-turn projection;
- completed diagnostic projection;
- joined waitlist projection history export;
- Sales Inbox projection evidence package export.

Trace export and manual review package tests were audited in the same pass and
were already fully anchored.

## Validation

Commands run from `C:\Users\lucas\agentes-landing-system`:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_action_trace_export.py services/taliya-agent-runtime/tests/test_spec012_sales_inbox_projection.py services/taliya-agent-runtime/tests/test_spec012_manual_review_package.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 9 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/tests/test_spec012_action_trace_export.py services/taliya-agent-runtime/tests/test_spec012_sales_inbox_projection.py services/taliya-agent-runtime/tests/test_spec012_manual_review_package.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 235 passed, 716 deselected.

## Anti-Determinism Review

Manifest-only reinforcement. No raw lead-text parser, commercial regex,
prompt, customer copy, template, or runtime behavior changed. The newly
anchored projection test verifies exported operational state derived after the
LLM-first action path has already produced a validated compiled turn.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.

## Still Open

T012-035 remains open for production Sales Inbox integration/review after
approved endpoint/runtime work. T012-041 remains open for the final full
contract gate after endpoint/runtime integration and approved real-model or
shadow evidence.
