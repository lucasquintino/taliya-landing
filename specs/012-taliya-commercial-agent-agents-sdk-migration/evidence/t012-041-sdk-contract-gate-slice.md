# T012-041 Slice - SDK Contract Gate

Date: 2026-06-11

## Scope

Started T012-041 with an explicit no-cost SDK contract gate for the isolated
action-first path.

The new manifest test verifies that the contract suite still includes anchors
for:

- strict `ConductorActionDecision` output schema;
- action-first SDK agents and state-based starting agent selection;
- spike output adapter rejection of free-form/direct text;
- isolated runner paid-call block, state evolution, and repair loop;
- Spec 011 validator bridge and ported voice/adequacy rules;
- SDK-path safety guardrails;
- local trace export;
- Sales Inbox projection evidence;
- mocked SDK run-item fixtures;
- static anti-drift audits.

It also asserts the contract gate remains no-cost/isolated: no
`paid_openai_approved=True`, no `OPENAI_API_KEY`, and no public endpoint/landing
imports inside the declared contract test files.

## Files Changed

- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-041-sdk-contract-gate-slice.md`

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_sdk_contract_gate.py tests\test_spec012_conductor_decision.py tests\test_spec012_action_agents.py tests\test_spec012_sdk_output_adapter.py tests\test_spec012_action_turn_runner.py tests\test_spec012_action_validators.py tests\test_spec012_action_validators_ported.py tests\test_spec012_action_safety.py tests\test_spec012_action_trace_export.py tests\test_spec012_sales_inbox_projection.py tests\test_spec012_sdk_run_items_mocked.py tests\test_spec012_static_audit.py -q`
  - result: 74 passed
- `python -m ruff check tests\test_spec012_sdk_contract_gate.py`
  - result: all checks passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 216 passed, 716 deselected

## Anti-Determinism Review

The manifest adds no runtime behavior. It makes existing action-first contract
coverage explicit and keeps the contract gate isolated/no-cost. No raw lead
text routing, regex commercial parser, template-first branch, prompt change, or
customer-facing copy change was added.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, public
endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None. Cost: `$0`.

## Still Open

T012-041 remains open for the final verification pass after endpoint/runtime
integration and approved real-model/shadow evidence. This slice proves the
current isolated SDK contract gate.
