# T012-032B / T012-038B Post-Diagnostic Price Resume Slice

Date: 2026-06-11

## Scope

Added no-cost action-first coverage for a lead returning after a completed
diagnostic with messy shorthand price wording (`qto ficava msm?`).

This closes a real regression risk in the post-diagnostic delta contract:
answering a price question with saved diagnostic context must not restart the
diagnostic or append the generic diagnostic offer.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/decision_compiler.py`
- `services/taliya-agent-runtime/tests/test_spec012_decision_compiler.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`

## Behavior Covered

- In `post_diagnostic` mode, `answer_product_question_with_saved_context` with
  `product_fact_keys_used=["prices"]` renders only `product.price_direct`.
- The compiler no longer appends `diagnostic.price_hook` for saved-context
  product answers after the diagnostic was already delivered.
- The mocked runner fixture proves the full chain:
  persisted completed diagnostic state -> specialist-direct SDK call ->
  structured action decision -> compiler -> validators -> renderer ->
  commit/projection.
- The fixture keeps a complete persisted diagnostic ledger and final fields so
  Sales Inbox projection validation remains active.

## Anti-Determinism Review

The runtime still does not inspect raw lead text. The messy phrase exists only
as mocked test input/direct question. The LLM remains responsible for selecting
`answer_product_question_with_saved_context` and declaring `prices`; deterministic
code only expands that structured decision and prevents an inappropriate
diagnostic restart.

## Tests Run

- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_decision_compiler.py -k "post_diagnostic_price_resume" -q`
  - Result: `1 passed`
- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py -k "post_diagnostic_messy_price_resume" -q`
  - Result: `1 passed`
- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_decision_compiler.py services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py -q`
  - Result: `44 passed`
- `python -m ruff check services/taliya-agent-runtime/app/core/taliya_commercial_sdk/decision_compiler.py services/taliya-agent-runtime/tests/test_spec012_decision_compiler.py services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`
  - Result: passed

## Protected Scope Review

No `/pilates`, landing visual, Sales Inbox UI, multi-tenant, client/studio
WhatsApp, checkout, or public endpoint files were changed.

## Paid Call Review

No paid OpenAI call was made. The runner proof uses `ScriptedFakeModel`.

## Open Items

T012-032B and T012-038B remain open overall. This slice strengthens
post-diagnostic resume and messy-input coverage, but full closure still needs
the remaining canonical/mocked coverage and later real-model/shadow gates.
