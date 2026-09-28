# T012-038B Slice - Waitlist And Demo Resume Fixtures

Date: 2026-06-11

## Scope

Advanced T012-038B with no-cost action-first fixtures for additional
resume-after-days cells:

- waitlist pending details + direct product question;
- demo request after post-diagnostic return.

## Sources

- `specs/012-taliya-commercial-agent-agents-sdk-migration/tasks.md`
  - T012-038B requires resume-after-days and interruption fixtures.
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/product-followup-delta-contract.md`
  - post-diagnostic and waitlist follow-up must answer direct questions first,
    preserve state, and avoid restarting diagnostic.
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/behavior-contract.md`
  - waitlist pending details: answer the product question first, then briefly
    return to the missing detail.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/decision_compiler.py`
- `services/taliya-agent-runtime/tests/test_spec012_decision_compiler.py`

## Behavior

The compiler now uses the persisted `waitlist.missing_details` value when
returning to a pending waitlist detail after answering a product question. It
no longer always falls back to `waitlist.ask_missing_contact_path`.

The fixtures prove:

- "qual era o valor mesmo?" during `waitlist_pending_data` answers with
  `product.price_direct`, then asks the actual missing `studio_name`;
- "me manda a demo de novo" after diagnostic delivery sends
  `product.demo_direct` and does not restart diagnostic.

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_decision_compiler.py -q`
  - result: 24 passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 151 passed, 716 deselected
- `python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_turn_situation.py tests\test_spec012_action_agents.py tests\test_spec012_decision_compiler.py tests\test_spec012_action_turn_runner.py tests\test_spec012_action_validators_ported.py tests\test_spec012_static_audit.py tests\test_spec012_action_safety.py`
  - result: all checks passed

## Anti-Determinism Review

No raw lead-text route or commercial regex was added. The compiler reads only
persisted waitlist state to choose which missing-detail template follows the
LLM-selected `answer_question_then_continue_waitlist` action. Demo resume is
also action-first: the LLM selects `send_demo`; the compiler fills official
demo facts.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, or
client/studio WhatsApp files were edited.

## Paid Calls

None.

## Still Open

- broaden resume-after-days to more post-waitlist and post-demo reactions;
- complete the larger interruption matrix;
- port canonical Spec 011 fixtures under T012-038;
- real-model evidence only after explicit paid approval.
