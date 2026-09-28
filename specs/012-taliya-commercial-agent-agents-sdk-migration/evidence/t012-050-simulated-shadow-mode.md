# T012-050 simulated shadow mode

- Date: 2026-06-16
- Scope: Spec 012 action-first runtime adapter
- Mode: simulated shadow, no real leads
- Paid OpenAI calls: none
- Public activation: none

## Result

T012-050 passed for the approved simulated/no-cost shadow scope.

Because production has no real leads yet, the product-owner approval in T012-048
limits this task to a controlled simulation. The runtime adapter now supports an
explicit Spec 012 shadow flag:

```json
{
  "metadata": {
    "spec012_shadow_mode": {
      "enabled": true,
      "reason": "t012_050_simulated_shadow_no_real_leads"
    }
  }
}
```

When enabled, the action-first SDK path still runs through the normal pipeline:

1. Turn situation is built from state.
2. The injected SDK model returns structured `ConductorActionDecision`.
3. Compiler expands the selected action.
4. Validators and renderer run.
5. Trace and Sales Inbox projection are produced.

But delivery and live mutation are suppressed:

- `output.messages` is empty;
- `delivery_control.shadow_mode` is true;
- `delivery_control.delivery_suppressed` is true;
- runtime event content is `spec012_shadow_turn_completed`;
- trace summary and Sales Inbox projection are persisted as local evidence;
- model usage is recorded with `shadow_mode: true`;
- live runtime state is not saved/updated.

## Verification

```powershell
python -m pytest -q services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result:

```text
6 passed in 2.84s
```

```powershell
python -m pytest -q services/taliya-agent-runtime/tests -k spec012
```

Result:

```text
275 passed, 716 deselected in 6.63s
```

```powershell
python -m ruff check services/taliya-agent-runtime/app/core/taliya_commercial_sdk/runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result:

```text
All checks passed!
```

## Contract Anchors

The new shadow behavior is anchored in the Spec 012 contract gate through:

- `test_t012_050_shadow_mode_suppresses_delivery_and_does_not_mutate_state`

This proves the simulated shadow path is not a loose test artifact.

## Anti-Determinism Review

The change is operational shadow control only. It does not add raw lead-text
commercial routing, regex/state-machine commercial interpretation, template-first
shortcuts, direct SDK free-text delivery, or public fallback to the old
commercial brain.

The LLM-first action path remains intact in the simulated run; deterministic
logic only suppresses delivery/state mutation after the action-first pipeline has
produced validated local evidence.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant,
client/studio WhatsApp, or public activation work was changed.

## Closure

T012-050 is closed for simulated/no-cost shadow mode. Real production lead
traffic shadowing remains unapproved and unnecessary while there are no real
leads.
