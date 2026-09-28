# T012-038B Multiple Diagnostic Answers Runner Slice

Date: 2026-06-11

## Scope

Added mocked/no-cost action-first runner coverage for a lead answering more
than one diagnostic slot in a single message.

Scenario:

- lead starts the diagnostic;
- lead replies with both size and pain context in one message:
  `80 alunos e o maior problema e responder interessados rapido`;
- mocked LLM emits one structured `capture_pending_diagnostic_answer` decision
  with two captured slots:
  `active_students_or_size=80 alunos` and
  `main_pain=demora para responder interessados`;
- runner validates, renders approved diagnostic templates, commits both slots,
  and asks the next pending key (`diagnostic.ask_pain_detail`).

## Files Changed

- `services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-038b-multiple-diagnostic-answers-runner-slice.md`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/implementation-ledger.md`

## Evidence

New test:

- `test_diagnostic_multiple_answers_in_one_message_commits_both_slots`

Contract-gate anchor:

- `test_spec012_sdk_contract_gate.py` now requires the new runner test.

Verified behavior:

- turn starts directly at `taliya_diagnostic_agent`;
- interruption/multi-answer turn uses one mocked model operation;
- selected action is `capture_pending_diagnostic_answer`;
- templates are `diagnostic.partial_progress` and `diagnostic.ask_pain_detail`;
- final diagnostic ledger stores both captured values;
- trace records the two structured captured slots;
- total cost is `$0`.

## Tests

Run from repository root:

- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py -q`
  - result: 14 passed
- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py -q`
  - result: 16 passed
- `python -m ruff check services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`
  - result: all checks passed
- `python -m pytest services/taliya-agent-runtime/tests -k spec012 -q`
  - result: 227 passed, 716 deselected

## Anti-Determinism Review

No raw lead-text parser was added. The mocked LLM emits typed captured slots;
the runner/compiler validate, render, trace, and commit after validation. The
test proves the runtime can preserve multiple LLM-extracted facts without
turning message parsing into deterministic code.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout implementation,
multi-tenant, public endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None. Cost: `$0`.

## Still Open

T012-038B remains open for the broader fixture matrix and real-model evidence
after explicit approval. T012-041 remains open for final contract verification
after endpoint/runtime integration and real-model/shadow gates.
