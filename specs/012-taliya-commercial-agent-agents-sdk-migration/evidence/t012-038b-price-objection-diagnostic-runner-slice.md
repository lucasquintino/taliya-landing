# T012-038B Price Objection During Diagnostic Runner Slice

Date: 2026-06-11

## Scope

Added mocked/no-cost action-first runner coverage for a price objection during
an in-progress diagnostic.

Scenario:

- lead starts the diagnostic;
- lead provides size and main pain in one message;
- diagnostic is waiting for `pain_detail`;
- lead says `achei caro, nao sei se compensa`;
- mocked LLM emits structured
  `answer_direct_question_then_continue_diagnostic` with
  `interpreted_intents=["price_objection"]`;
- runner answers with approved `product.price_objection_value` and resumes
  `diagnostic.ask_pain_detail`.

## Files Changed

- `services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-038b-price-objection-diagnostic-runner-slice.md`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/implementation-ledger.md`

## Evidence

New test:

- `test_diagnostic_price_objection_answers_then_resumes_pending_question`

Contract-gate anchor:

- `test_spec012_sdk_contract_gate.py` now requires the new runner test.

Verified behavior:

- objection turn stays in diagnostic mode;
- known-state turn starts directly at `taliya_diagnostic_agent`;
- objection turn uses one mocked model operation;
- selected action is `answer_direct_question_then_continue_diagnostic`;
- templates are `product.price_objection_value` and
  `diagnostic.ask_pain_detail`;
- diagnostic ledger keeps the prior size and main-pain values;
- trace records `interpreted_intents=["price_objection"]`;
- rendered text avoids checkout language;
- total cost is `$0`.

## Tests

Run from repository root:

- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py -q`
  - result: 15 passed
- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py -q`
  - result: 17 passed
- `python -m ruff check services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`
  - result: all checks passed
- `python -m pytest services/taliya-agent-runtime/tests -k spec012 -q`
  - result: 228 passed, 716 deselected

## Anti-Determinism Review

No raw lead-text price-objection detector was added. The mocked LLM declares
the structured intent and action; the runner/compiler validate, render approved
templates, trace, and commit state after validation.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout implementation,
multi-tenant, public endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None. Cost: `$0`.

## Still Open

T012-038B remains open for the broader fixture matrix and real-model evidence
after explicit approval. T012-041 remains open for final contract verification
after endpoint/runtime integration and real-model/shadow gates.
