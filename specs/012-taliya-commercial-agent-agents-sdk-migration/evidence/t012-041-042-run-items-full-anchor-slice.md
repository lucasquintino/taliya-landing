# T012-041/T012-042 Run-Items Full Anchor Slice

Status: started / partial on 2026-06-12.

## Scope

This no-cost slice strengthens the T012-041 contract gate so every current
T012-042 mocked SDK run-item fixture is mandatory.

No runtime behavior, prompt, renderer, endpoint, `/pilates`, checkout,
multi-tenant, Sales Inbox UI, client/studio WhatsApp, or paid OpenAI path was
changed.

## Files

- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`

## Added Contract Coverage

The T012-041 manifest already required:

- `test_t012_042_router_handoff_run_items_are_structural`;
- `test_t012_042_repair_trace_records_validator_feedback_and_repair_items`.

This slice adds the remaining T012-042 fixtures:

- `test_t012_042_specialist_direct_run_items_skip_router`;
- `test_t012_042_safety_boundary_has_no_sdk_run_items`.

The required T012-042 set now covers:

- routed entry turn with router handoff;
- specialist-direct diagnostic turn;
- repair run with validator feedback and structural repair run items;
- safety boundary with no SDK run items and zero usage/cost.

## Validation

Commands run from `C:\Users\lucas\agentes-landing-system`:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_sdk_run_items_mocked.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 6 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/tests/test_spec012_sdk_run_items_mocked.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 235 passed, 716 deselected.

## Anti-Determinism Review

Manifest-only test reinforcement. No raw lead text is parsed and no commercial
decisioning behavior is changed. The underlying fixtures continue to use mocked
structured SDK run output and inspect only structural run-item metadata.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.

## Still Open

T012-042 remains open overall for final verification after endpoint/runtime
integration and approved real-model/shadow evidence. T012-041 remains open for
the final full contract gate after those integrations exist.
