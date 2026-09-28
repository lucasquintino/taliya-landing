# T012-035 Sales Inbox Runtime Closure

Status: completed on 2026-06-15.

## Scope

This no-cost closure adapts the Sales Inbox projection path for the
action-first SDK runtime. It proves projection generation, endpoint-adapter
response shape, identity propagation, local persistence in runtime event trace
summary, and export-package evidence without changing the Sales Inbox UI.

No `/pilates`, landing visual/copy/layout, Sales Inbox UI, checkout,
multi-tenant, client/studio WhatsApp, shadow traffic, public cutover, or paid
provider path changed.

## Files

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_validators.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_turn_runner.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_sales_inbox_evidence.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/runtime_adapter.py`
- `services/taliya-agent-runtime/tests/test_spec012_sales_inbox_projection.py`
- `services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`

## Proof

- Delivered action-first turns build Sales Inbox projections from accepted
  action decisions, compiled templates, validated state, and delivery metadata.
- Projection generation reuses the preserved Spec 011 projection builder and
  validator path; there is no second Sales Inbox inference brain.
- Price and completed-diagnostic projections prove commercial stage, diagnostic
  status, template ids, validator status, final plan/range, final demo line,
  and operator next action.
- Joined-waitlist resume projection preserves historical waitlist idempotency
  key and joined timestamp.
- `012.sales_inbox_projection_export.v1` packages prove required projection
  fields and exempt suppressed human-active turns.
- The runtime adapter seeds request `conversation_id`, `lead_id`, `source`, and
  `channel` into the action-first runner, so endpoint-adapter projections carry
  real public identity rather than isolated-runner defaults.
- Runtime adapter output exposes the projection in `AgentOutput`.
- Runtime events persist the projection inside
  `012.runtime_action_trace_summary.v1`.

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

Projection code is downstream of the LLM's structured action decision and the
compiler/validator result. It does not parse raw lead text, classify commercial
meaning, or introduce deterministic price/demo/plan/diagnostic/waitlist
routing.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.
