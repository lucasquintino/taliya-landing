# T012-038B Slice - Product-Question Interruption Matrix

Date: 2026-06-11

## Scope

Advanced T012-038B with no-cost action-first fixtures for product questions
interrupting an in-progress diagnostic.

Covered interruption cells:

- how-it-works question;
- integration/specific-system question;
- security/data question;
- availability/checkout question;
- out-of-profile/student question;
- comparison/current-tool question.

These are mocked `ConductorActionDecision` fixtures. They prove the compiler
can consume the LLM's structured semantic output and resume the diagnostic
without adding raw-text commercial parsing.

## Sources

- `specs/012-taliya-commercial-agent-agents-sdk-migration/tasks.md`
  - T012-038B requires an interruption matrix across question types and phases.
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/product-followup-delta-contract.md`
  - direct questions must be answered first;
  - product follow-up routes include how-it-works, integration, security/data,
    availability/onboarding, comparison, out-of-profile;
  - diagnostic and post-diagnostic flows must not restart or lose state after
    a side question.
- `specs/012-taliya-commercial-agent-agents-sdk-migration/design-lock-v2-action-first.md`
  - LLM chooses action/intents/fact keys; compiler expands and validates.
- `.agents/skills/taliya-llm-first-agent/SKILL.md`
  - mixed/ambiguous commercial messages must remain LLM-first.

## Files Changed

- `services/taliya-agent-runtime/tests/test_spec012_decision_compiler.py`

## Behavior Proved

For each product-question interruption, the mocked LLM decision selects
`answer_direct_question_then_continue_diagnostic` with structured
`interpreted_intents` and `product_fact_keys_used`.

The compiler emits:

1. the correct approved product answer template;
2. the pending diagnostic question `diagnostic.ask_main_pain`;
3. `next_state = diagnostic_waiting_answer`.

No current-message text is inspected by runtime code. The messy/direct wording
exists only as fixture evidence.

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_decision_compiler.py -q`
  - result: 32 passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 201 passed, 716 deselected
- `python -m ruff check tests\test_spec012_decision_compiler.py`
  - result: all checks passed

## Anti-Determinism Review

No raw lead-text parser, regex, token list, or commercial shortcut was added.
The compiler reacts only to structured LLM output: selected action,
interpreted intents, product fact keys, and composition variables.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, public
endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None.

## Still Open

T012-038B still needs broader phase coverage, real-model evidence after
explicit approval, and final quality-judge/manual review packaging before it
can be closed completely.
