# T012-038B Slice - Mocked Messy-Input Fixtures

Date: 2026-06-11

## Scope

Started T012-038B with no-cost action-first fixtures for uncovered
conversational cells.

Covered in this slice:

- correction of a diagnostic answer: "na verdade sao 80, nao 120";
- multiple diagnostic answers in one message;
- messy price interruption during diagnostic: "qto fica?";
- messy demo request: "tem como ver ai mn".

These are mocked `ConductorActionDecision` fixtures. They prove the action-first
compiler can consume the LLM's structured interpretation without adding raw-text
commercial parsing.

## Sources

- `specs/012-taliya-commercial-agent-agents-sdk-migration/tasks.md`
  - T012-038B requires correction, multiple answers, interruption matrix, and
    messy real-world input fixtures.
- `specs/012-taliya-commercial-agent-agents-sdk-migration/eval-plan.md`
  - names the uncovered cells: interruption matrix, answer correction, multiple
    answers in one message, and messy typos/slang/no punctuation.
- `specs/012-taliya-commercial-agent-agents-sdk-migration/coverage-map.md`
  - maps answer correction and messy input to LLM captured slots plus compiler
    merge.
- `specs/012-taliya-commercial-agent-agents-sdk-migration/design-lock-v2-action-first.md`
  - requires LLM action decision first, then deterministic compiler expansion.
- `.agents/skills/taliya-llm-first-agent/SKILL.md`
  - forbids deterministic commercial shortcuts for price/demo/diagnostic mixed
    cases.

## Files Changed

- `services/taliya-agent-runtime/tests/test_spec012_decision_compiler.py`

## Behavior Proved

- A corrected diagnostic number is represented as a structured captured slot
  and compiled into a ledger update for `active_students_or_size`.
- Multiple structured captured slots in one turn advance the diagnostic to the
  next missing question without re-asking already captured answers.
- During diagnostic, a messy price question compiles as answer-first
  `product.price_direct`, then resumes the pending diagnostic question.
- A slangy demo request compiles to `product.demo_direct` and uses the official
  demo link variable.

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_decision_compiler.py -q`
  - result: 17 passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 140 passed, 716 deselected
- `python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_decision_compiler.py tests\test_spec012_action_turn_runner.py tests\test_spec012_conductor_decision.py tests\test_spec012_action_validators_ported.py tests\test_spec012_static_audit.py tests\test_spec012_action_safety.py`
  - result: all checks passed

## Anti-Determinism Review

No text classifier, regex, token list, or commercial shortcut was added. The
messy phrases exist only in test `direct_question` values. The runtime path
still depends on the LLM returning structured actions, intents, captured slots,
and product fact keys.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, or
client/studio WhatsApp files were edited.

## Paid Calls

None.

## Still Open

- port the canonical Spec 011 fixture set under T012-038;
- broaden the T012-038B interruption matrix across phases and question types;
- add objection mid-diagnostic, resume-after-days, and more slang/typo cases;
- later, after explicit approval only, run real-model golden/quality-judge
  evidence for these fixtures.
