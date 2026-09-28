# T012-032B/T012-038B Diagnostic Refusal Price Runner Slice

Date: 2026-06-11

## Scope

Added mocked/no-cost action-first runner coverage for a lead refusing to
continue the diagnostic while asking a direct price question.

Scenario:

- conversation is in `diagnostic_in_progress`;
- one diagnostic slot has already been captured;
- lead says `so me fala o preco`;
- mocked LLM emits structured `respect_diagnostic_refusal` with
  `diagnostic_intent="refusal"` and `product_fact_keys_used=["prices"]`;
- runner answers with official price copy and does not reoffer or restart the
  diagnostic.

## Files Changed

- `services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-032b-038b-diagnostic-refusal-price-runner-slice.md`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/implementation-ledger.md`

## Evidence

New test:

- `test_diagnostic_refusal_price_question_answers_without_reoffering_diagnostic`

Contract-gate anchor:

- `test_spec012_sdk_contract_gate.py` now requires the new runner test.

Verified behavior:

- turn stays in diagnostic mode;
- known-state turn starts directly at `taliya_diagnostic_agent`;
- turn uses one mocked model operation;
- selected action is `respect_diagnostic_refusal`;
- templates are only `product.price_direct`;
- rendered text includes official price values;
- rendered text does not include diagnostic offer or active-students prompt;
- direct question is recorded as answered;
- total cost is `$0`.

## Tests

Run from repository root:

- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py -q`
  - result: 18 passed
- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py -q`
  - result: 20 passed
- `python -m ruff check services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`
  - result: all checks passed
- `python -m pytest services/taliya-agent-runtime/tests -k spec012 -q`
  - result: 231 passed, 716 deselected

## Anti-Determinism Review

No raw lead-text refusal or price parser was added. The mocked LLM declares the
structured refusal intent, action, and product fact key; code resolves official
prices, validates, renders approved templates, traces, and commits after
validation.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout implementation,
multi-tenant, public endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None. Cost: `$0`.

## Still Open

T012-032B/T012-038B remain open for broader fixture coverage and real-model
evidence after explicit approval. T012-041 remains open for final contract
verification after endpoint/runtime integration and real-model/shadow gates.
