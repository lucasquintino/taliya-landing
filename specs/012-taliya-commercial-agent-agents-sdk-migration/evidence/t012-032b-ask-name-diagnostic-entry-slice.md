# T012-032B Slice - Ask Name At Diagnostic Entry

Date: 2026-06-11

## Scope

Advanced T012-032B with the approved name-question boundary at diagnostic
entry.

Covered:

- added the structured action `ask_name_at_diagnostic_entry`;
- added approved template `diagnostic.ask_name_at_entry`;
- rendered the exact approved behavior-contract copy:
  "Claro, faco sim. Antes de eu montar o diagnostico: com quem eu falo?";
- kept pure cold greeting unchanged;
- kept the diagnostic unblocked if the lead skips/refuses the name.

This is a mocked/no-cost isolated-core slice. It does not add public endpoint
cutover.

## Sources

- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/behavior-contract.md`
  - cold greeting must not ask name;
  - unreliable profile names must be ignored;
  - approved name question at diagnostic entry:
    "Claro, faco sim. Antes de eu montar o diagnostico: com quem eu falo?";
  - if the lead skips or refuses the name, continue delivering value.
- `specs/012-taliya-commercial-agent-agents-sdk-migration/conformity-matrix.pt-BR.md`
  - maps name policy, including ask-at-diagnostic-entry, to T012-032B.
- `.agents/skills/taliya-llm-first-agent/SKILL.md`
  - the LLM remains the commercial brain; deterministic code may render
    approved templates after the LLM chooses the action.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/conductor_decision.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/decision_compiler.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_agents.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial/template_registry.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial/renderer.py`
- `services/taliya-agent-runtime/tests/test_spec012_conductor_decision.py`
- `services/taliya-agent-runtime/tests/test_spec012_decision_compiler.py`

## Behavior

`ask_name_at_diagnostic_entry` is available as a structured entry action. The
compiler maps it to `diagnostic.ask_name_at_entry` and records
`diagnostic.status = name_requested` while keeping `next_state =
diagnostic_offered`.

That state choice is intentional: the diagnostic has not started until the
first diagnostic question is asked. A following turn can still choose
`start_requested_diagnostic` and ask `diagnostic.ask_active_students` even if
the lead skipped/refused the name.

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_conductor_decision.py tests\test_spec012_decision_compiler.py tests\test_spec011_template_registry.py -q`
  - result: 39 passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 195 passed, 716 deselected
- `python -m ruff check app\core\taliya_commercial_sdk\conductor_decision.py app\core\taliya_commercial_sdk\decision_compiler.py app\core\taliya_commercial_sdk\action_agents.py app\core\taliya_commercial\template_registry.py app\core\taliya_commercial\renderer.py tests\test_spec012_conductor_decision.py tests\test_spec012_decision_compiler.py`
  - result: all checks passed

## Anti-Determinism Review

No raw lead-text route, regex, or token list was added. The runtime does not
infer from the current message that it should ask for name. The LLM must select
the explicit structured action, and the compiler only renders the approved
template for that action.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, public
endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None.

## Still Open

T012-032B remains open as a whole because final acceptance still requires
real-model evidence/reporting for the new product-followup routes, plus broader
eval coverage and product-owner review.

## Follow-Up Note

During the T012-034 trace slice, the rendered validator was aligned with this
template: `com quem eu falo?` is still blocked as generic customer-facing copy,
but passes when rendered by the approved `diagnostic.ask_name_at_entry`
template. Focused validation:

- `python -m pytest tests\test_spec012_action_validators_ported.py::test_action_validator_allows_approved_name_question_at_diagnostic_entry -q`
  - result: 1 passed
