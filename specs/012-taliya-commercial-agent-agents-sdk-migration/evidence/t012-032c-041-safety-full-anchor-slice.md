# T012-032C/T012-041 Safety Full Anchor Slice

Status: started / partial on 2026-06-12.

## Scope

This no-cost slice strengthens the T012-041 contract gate so all current
T012-032C SDK-path safety guardrail tests are mandatory.

No runtime behavior, prompt, renderer, endpoint, `/pilates`, checkout,
multi-tenant, Sales Inbox UI, client/studio WhatsApp, or paid OpenAI path was
changed.

## Files

- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`

## Added Contract Coverage

The contract gate already required:

- prompt injection block;
- action runner safety guardrail skip-SDK rendering.

This slice adds required anchors for:

- unsupported media block;
- sensitive data block;
- security policy question allowed as commercial/product scope;
- medical advice block;
- commercial price question not misclassified as safety.

The required T012-032C safety set now covers the full current SDK-path safety
test file.

## Validation

Commands run from `C:\Users\lucas\agentes-landing-system`:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_action_safety.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 13 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/tests/test_spec012_action_safety.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 235 passed, 716 deselected.

## Anti-Determinism Review

Manifest-only reinforcement. The underlying safety guardrails are allowed
deterministic operational boundaries. This slice adds no commercial
classification, raw lead-text routing, prompt, template, customer copy, or
runtime behavior.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.

## Still Open

T012-041 remains open for the final full contract gate after endpoint/runtime
integration and approved real-model/shadow evidence. T012-032C is already
implemented for the isolated SDK path, but endpoint integration must re-run
these anchors before shadow mode.
