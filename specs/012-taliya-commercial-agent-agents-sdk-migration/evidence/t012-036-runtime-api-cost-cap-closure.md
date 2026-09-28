# T012-036 Runtime API And Cost Cap Closure

Status: completed on 2026-06-15.

## Scope

This no-cost closure proves the action-first SDK path preserves the public
runtime API boundary while adding the per-conversation cost cap. It does not
enable paid provider calls, public cutover, shadow traffic, or public SDK
delivery.

No `/pilates`, landing visual/copy/layout, Sales Inbox UI, checkout,
multi-tenant, client/studio WhatsApp, or production activation path changed.

## Files

- `services/taliya-agent-runtime/app/main.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/runtime_adapter.py`
- `services/taliya-agent-runtime/tests/test_agent_runs_api.py`
- `services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`

## Proof

- `/v1/taliya-commercial/turn` remains the public endpoint.
- HMAC validation remains before runner execution.
- Request-id idempotency remains owned by the endpoint; repeated request ids
  return the saved response.
- With `TALIYA_SPEC012_ACTION_FIRST_ENABLED=false`, the endpoint keeps the
  current Spec 011 path.
- With the flag on, the endpoint routes through the action-first adapter
  without public cutover.
- `TALIYA_AGENT_PROVIDER=openai` remains blocked without paid approval and does
  not write idempotency cache.
- `TALIYA_AGENT_HARD_COST_CAP_USD` is passed into the action-first adapter.
- If prior persisted conversation cost is already at or above the cap, the
  adapter returns `cost_capped`, emits no assistant messages, marks handoff
  active, records a guardrail event, and does not require an injected SDK
  model.

## Validation

Commands run from `C:\Users\lucas\agentes-landing-system`:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_agent_runs_api.py services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 16 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/app/main.py services/taliya-agent-runtime/app/core/taliya_commercial_sdk/runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 242 passed, 716 deselected.

## Anti-Determinism Review

The new branch is a cost/turn-gate boundary only. It does not parse lead text,
classify commercial intent, choose product answers, or route diagnostic,
waitlist, demo, plan, or pricing meaning. Normal commercial turns still require
the LLM to produce structured `ConductorActionDecision`.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.
