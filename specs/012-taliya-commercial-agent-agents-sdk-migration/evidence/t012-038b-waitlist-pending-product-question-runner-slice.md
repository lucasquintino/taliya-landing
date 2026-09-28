# T012-038B Waitlist Pending Product Question Runner Slice

Date: 2026-06-11

## Scope

Added mocked/no-cost action-first runner coverage for a product question while
the waitlist flow is pending a missing detail.

Scenario:

- conversation is already in `waitlist_pending_data`;
- waitlist state is missing `studio_name`;
- lead asks `como funciona mesmo?`;
- mocked LLM emits structured `answer_question_then_continue_waitlist` with
  `product_fact_keys_used=["how_it_works"]`;
- runner answers with approved product copy and resumes the waitlist collection
  with `waitlist.ask_missing_studio`.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_validators.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-038b-waitlist-pending-product-question-runner-slice.md`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/implementation-ledger.md`

## Adapter Fix

The action-first to Spec 011 validator adapter now preserves
`waitlist.missing_details` from the authoritative `TurnSituation` state
snapshot when building the legacy waitlist payload. It also treats an already
active waitlist state as eligible only when that active status comes from the
state snapshot, not merely from a new waitlist offer patch.

This keeps curiosity-only waitlist offers blocked while allowing a legitimate
pending-details waitlist turn to validate.

## Evidence

New test:

- `test_waitlist_pending_product_question_answers_then_asks_missing_studio`

Contract-gate anchor:

- `test_spec012_sdk_contract_gate.py` now requires the new runner test.

Verified behavior:

- turn stays in waitlist mode;
- known-state turn starts directly at `taliya_waitlist_agent`;
- turn uses one mocked model operation;
- selected action is `answer_question_then_continue_waitlist`;
- templates are `product.how_it_works_direct` and
  `waitlist.ask_missing_studio`;
- state remains `waitlist_pending_data` with
  `missing_details=["studio_name"]`;
- direct question is recorded as answered;
- checkout/discount language is not rendered;
- total cost is `$0`.

## Tests

Run from repository root:

- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py services/taliya-agent-runtime/tests/test_spec012_action_validators.py services/taliya-agent-runtime/tests/test_spec012_action_validators_ported.py -q`
  - result: 34 passed
- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py -q`
  - result: 18 passed
- `python -m ruff check services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_validators.py`
  - result: all checks passed
- `python -m pytest services/taliya-agent-runtime/tests -k spec012 -q`
  - result: 229 passed, 716 deselected

## Anti-Determinism Review

No raw lead-text product-question or waitlist parser was added. The mocked LLM
declares the structured action and product fact key; code preserves state,
validates, renders approved templates, traces, and commits after validation.

The adapter change is state-contract preservation only: it copies missing
waitlist details already present in `TurnSituation.state_snapshot`.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout implementation,
multi-tenant, public endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None. Cost: `$0`.

## Still Open

T012-038B remains open for the broader fixture matrix and real-model evidence
after explicit approval. T012-041 remains open for final contract verification
after endpoint/runtime integration and real-model/shadow gates.
