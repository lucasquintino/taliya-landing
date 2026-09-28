# T012-041 Contract Gate Delta And Resume Anchors Slice

Date: 2026-06-11

## Scope

Updated the no-cost SDK contract gate manifest so recent T012-032B/T012-038B
behavior guarantees are required by the contract suite.

This is a manifest-only governance change. It does not change runtime behavior.

## Files Changed

- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`

## Behavior Anchored

The T012-041 manifest now requires anchors for:

- `routine_areas` product-knowledge delta coverage in the action runner;
- post-diagnostic messy price resume in the action runner;
- compiler-level proof that post-diagnostic price resume does not restart or
  re-offer the diagnostic;
- existing how-it-works delta compiler coverage.

## Tests Run

- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py services/taliya-agent-runtime/tests/test_spec012_decision_compiler.py -q`
  - Result: `46 passed`
- `python -m ruff check services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`
  - Result: passed

## Anti-Determinism Review

Manifest-only change. No raw lead-text parsing, commercial routing, prompt,
template, validator, renderer, or runtime behavior changed.

## Protected Scope Review

No `/pilates`, landing visual, Sales Inbox UI, multi-tenant, client/studio
WhatsApp, checkout, or public endpoint files were changed.

## Paid Call Review

No paid OpenAI call was made.

## Open Items

T012-041 remains open for final verification after endpoint/runtime integration
and approved real-model/shadow evidence. This slice strengthens the current
mocked/no-cost contract manifest.
