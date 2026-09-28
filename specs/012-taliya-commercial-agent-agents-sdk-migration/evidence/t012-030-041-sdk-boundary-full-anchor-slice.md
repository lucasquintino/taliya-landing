# T012-030/T012-041 SDK Boundary Full Anchor Slice

Status: started / partial on 2026-06-12.

## Scope

This no-cost slice strengthens the T012-041 contract gate so all current
SDK-boundary tests for action-first schema, agent topology, and output adapter
are mandatory.

No runtime behavior, prompt, renderer, endpoint, `/pilates`, checkout,
multi-tenant, Sales Inbox UI, client/studio WhatsApp, or paid OpenAI path was
changed.

## Files

- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`

## Added Contract Coverage

The manifest now requires all current tests in:

- `test_spec012_conductor_decision.py`
- `test_spec012_action_agents.py`
- `test_spec012_sdk_output_adapter.py`

This includes anchors for:

- strict `ConductorActionDecision` SDK-compatible output;
- superseded template-plan/state-transition boundary fields rejected;
- invented actions and slot keys rejected;
- action menus preserving Spec 011 plus Spec 012 delta actions;
- `TurnAction` literal and mode menus staying consistent;
- composition variables excluding official-only variables;
- form validation for action decisions;
- action-first agents using `ConductorActionDecision` with specialist tools off;
- deterministic starting-agent selection from mode;
- instructions carrying action-first contract, refusal, objection, and resume policy;
- no-cost board-to-compiled-turn smoke;
- structured proposal schema acceptance;
- runtime identity fields added by the adapter;
- SDK run-item structural extraction when agent path is absent;
- freeform final output rejection;
- direct-output fields rejected;
- product claims requiring fact refs;
- no public runtime endpoint import in the output adapter tests.

## Validation

Commands run from `C:\Users\lucas\agentes-landing-system`:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_conductor_decision.py services/taliya-agent-runtime/tests/test_spec012_action_agents.py services/taliya-agent-runtime/tests/test_spec012_sdk_output_adapter.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 23 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/tests/test_spec012_conductor_decision.py services/taliya-agent-runtime/tests/test_spec012_action_agents.py services/taliya-agent-runtime/tests/test_spec012_sdk_output_adapter.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 235 passed, 716 deselected.

## Anti-Determinism Review

Manifest-only reinforcement. No raw lead-text parsing, commercial routing,
prompt, customer copy, or runtime behavior changed. The reinforced tests keep
the action-first SDK boundary explicit: the LLM returns structured action JSON,
while code validates schema, topology, adapter shape, and no-public-cutover
constraints.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.

## Still Open

T012-041 remains open for the final full contract gate after endpoint/runtime
integration and approved real-model/shadow evidence.
