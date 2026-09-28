# T012-038B Diagnostic Correction Runner Slice

Date: 2026-06-11

## Scope

Added mocked/no-cost action-first runner coverage for correcting a previously
captured diagnostic answer:

- lead starts diagnostic;
- lead answers `120` for `active_students_or_size`;
- lead corrects with `na verdade sao 80, nao 120`;
- mocked LLM emits structured `capture_pending_diagnostic_answer` for the
  already answered `active_students_or_size` slot with value `80`;
- compiler accepts the correction-only update and resumes the pending
  `main_pain` question;
- commit-after-validation replaces the stored answer with `80`.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/decision_compiler.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-038b-diagnostic-correction-runner-slice.md`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/implementation-ledger.md`

## Behavior Change

`capture_pending_diagnostic_answer` still requires the pending diagnostic key
by default. The only new exception is correction-only behavior:

- the model must emit structured captured slots;
- every captured key must already exist in the diagnostic ledger with a
  complete status;
- the compiler then allows the correction and keeps the diagnostic waiting for
  the original pending question.

This enables answer correction without turning raw lead text into a parser.

## Evidence

New test:

- `test_diagnostic_correction_replaces_previous_number_in_committed_state`

Contract-gate anchor:

- `test_spec012_sdk_contract_gate.py` now requires the new runner test.

Verified behavior:

- first diagnostic answer commits `active_students_or_size=120`;
- correction turn starts directly at `taliya_diagnostic_agent`;
- correction turn uses one mocked model operation;
- selected action remains `capture_pending_diagnostic_answer`;
- rendered templates are `diagnostic.partial_progress` and
  `diagnostic.ask_main_pain`;
- final diagnostic ledger stores `active_students_or_size=80`;
- trace records the structured captured slot value `80`;
- total cost is `$0`.

## Tests

Run from repository root:

- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_decision_compiler.py services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py -q`
  - result: 46 passed
- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py -q`
  - result: 15 passed
- `python -m ruff check services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py services/taliya-agent-runtime/app/core/taliya_commercial_sdk/decision_compiler.py`
  - result: all checks passed
- `python -m pytest services/taliya-agent-runtime/tests -k spec012 -q`
  - result: 226 passed, 716 deselected

## Anti-Determinism Review

No raw-text correction parser was added. The correction is accepted only from a
typed LLM `captured_slots` update and only when the slot already exists in the
persisted diagnostic ledger. The compiler still blocks unrelated off-pending
diagnostic captures.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout implementation,
multi-tenant, public endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None. Cost: `$0`.

## Still Open

T012-038B remains open for the broader fixture matrix and real-model evidence
after explicit approval. T012-041 remains open for final contract verification
after endpoint/runtime integration and real-model/shadow gates.
