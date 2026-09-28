# T012-038B Diagnostic Availability Interruption Runner Slice

Date: 2026-06-11

## Scope

Added mocked/no-cost action-first runner coverage for a product availability
interruption during an in-progress diagnostic.

Scenario:

- lead starts the diagnostic;
- lead answers the first diagnostic key with `80`;
- before answering the pending `main_pain` question, lead asks
  `tem vaga pra entrar agora ou checkout?`;
- mocked LLM selects structured action
  `answer_direct_question_then_continue_diagnostic`;
- runner answers with official availability/onboarding context and resumes the
  pending diagnostic question.

The test proves the end-to-end runner behavior, not just compiler expansion.

## Files Changed

- `services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-038b-diagnostic-availability-interruption-runner-slice.md`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/implementation-ledger.md`

## Evidence

New test:

- `test_diagnostic_interruption_availability_answers_then_resumes_pending_question`

Contract-gate anchor:

- `test_spec012_sdk_contract_gate.py` now requires the new runner test.

Verified behavior:

- turn stays in diagnostic mode;
- known-state turn starts directly at `taliya_diagnostic_agent`;
- SDK/model operation count for the interruption turn is `1`;
- selected action is the mocked structured action
  `answer_direct_question_then_continue_diagnostic`;
- templates are `product.overview_short` then `diagnostic.ask_main_pain`;
- rendered answer uses `official_product_knowledge` override for
  `availability_and_onboarding`;
- rendered text avoids checkout/discount/VIP/date promise language;
- trace records `pending_question_key=main_pain`;
- final state remains `diagnostic_waiting_answer`;
- total cost is `$0`.

## Tests

Run from repository root:

- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py -q`
  - result: 12 passed
- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py -q`
  - result: 14 passed
- `python -m ruff check services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`
  - result: all checks passed
- `python -m pytest services/taliya-agent-runtime/tests -k spec012 -q`
  - result: 225 passed, 716 deselected

## Anti-Determinism Review

This slice does not parse raw lead text for checkout, availability, or
diagnostic intent. The mocked LLM emits the structured action and fact key; the
runner/compiler resolve official facts, validate, render approved templates,
trace, and commit after validation.

The official availability answer is supplied as `official_product_knowledge`
test data because this fixture is proving runner behavior, not adding a new
commercial parser.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout implementation,
multi-tenant, public endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None. Cost: `$0`.

## Still Open

T012-038B remains open for the broader fixture matrix and real-model evidence
after explicit approval. T012-041 remains open for final contract verification
after endpoint/runtime integration and real-model/shadow gates.
