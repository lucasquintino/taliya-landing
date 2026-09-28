# T012-041 Contract Gate Trace Delivery Anchor Slice

Date: 2026-06-11

## Scope

Updated the no-cost SDK contract gate manifest so the new T012-040 trace
delivery static audit is part of the declared contract suite.

This keeps the local trace/export no-public-delivery invariant from becoming a
loose test that can be dropped without the contract gate noticing.

## Files Changed

- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`

## Behavior Covered

The T012-041 manifest now requires the anchor:

- `test_t012_040_sdk_trace_export_does_not_claim_public_delivery`

That anchor verifies isolated SDK Python code cannot claim:

- public delivery;
- outbox reservation;
- direct SDK delivery.

## Tests Run

- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_static_audit.py -q`
  - Result: `10 passed`
- `python -m ruff check services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_static_audit.py`
  - Result: passed

## Anti-Determinism Review

Manifest-only change. No lead text parsing, commercial routing, prompt,
template, validator, renderer, or runtime behavior changed.

## Protected Scope Review

No `/pilates`, landing visual, Sales Inbox UI, multi-tenant, client/studio
WhatsApp, checkout, or public endpoint files were changed.

## Paid Call Review

No paid OpenAI call was made.

## Open Items

T012-041 remains open for final contract verification after endpoint/runtime
integration and approved real-model/shadow evidence. This slice strengthens the
current no-cost manifest.
