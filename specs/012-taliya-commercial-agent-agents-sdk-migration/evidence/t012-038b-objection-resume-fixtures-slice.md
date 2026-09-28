# T012-038B Slice - Objection And Resume Fixtures

Date: 2026-06-11

## Scope

Advanced T012-038B with no-cost action-first fixtures for two uncovered
conversational cells:

- price objection mid-diagnostic;
- resume after days using saved post-diagnostic memory.

These are mocked `ConductorActionDecision` fixtures. They prove the compiler
can consume the LLM's structured intent/action output without adding raw-text
commercial routing.

## Sources

- `specs/012-taliya-commercial-agent-agents-sdk-migration/tasks.md`
  - T012-038B requires objection mid-diagnostic and resume-after-days fixtures.
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/product-followup-delta-contract.md`
  - general objections and conversation resume are LLM-selected intents;
  - post-diagnostic turns must use saved diagnostic memory and not restart the
    diagnostic.
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/conversation-route-coverage-matrix.md`
  - `general_objection` and `conversation_resume` remain missing routes to
    cover through LLM+policy+memory first.
- `.agents/skills/taliya-llm-first-agent/SKILL.md`
  - objections, product follow-up, diagnostic interruptions, and resume must
    remain LLM-first.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/decision_compiler.py`
- `services/taliya-agent-runtime/tests/test_spec012_decision_compiler.py`

## Behavior

The compiler now recognizes structured product intent
`price_objection`/`objection_price` when the selected action is an answering
product path such as `answer_direct_question_then_continue_diagnostic`.

The new fixtures prove:

- mid-diagnostic "achei caro" style objection compiles to
  `product.price_objection_value` first, then resumes the pending diagnostic
  question;
- post-diagnostic resume uses `post_diagnostic_context` from persisted state
  and does not re-ask diagnostic questions.

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_decision_compiler.py -q`
  - result: 22 passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 149 passed, 716 deselected
- `python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_turn_situation.py tests\test_spec012_action_agents.py tests\test_spec012_decision_compiler.py tests\test_spec012_action_turn_runner.py tests\test_spec012_action_validators_ported.py tests\test_spec012_static_audit.py tests\test_spec012_action_safety.py`
  - result: all checks passed

## Anti-Determinism Review

No raw lead-text parser, regex, or token list was added. The only compiler
mapping uses `interpreted_intents`, which is part of the LLM's structured
decision. The messy/objection/resume phrases live in tests as direct-question
fixtures, not in runtime routing code.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, or
client/studio WhatsApp files were edited.

## Paid Calls

None.

## Still Open

- broaden the interruption matrix across more phases/question types;
- add resume-after-days fixtures for waitlist and demo states;
- port the canonical Spec 011 fixture set under T012-038;
- run real-model golden evidence only after explicit paid approval.
