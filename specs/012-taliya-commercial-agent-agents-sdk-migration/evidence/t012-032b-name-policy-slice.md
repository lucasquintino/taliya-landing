# T012-032B Slice - Profile Name Policy

Date: 2026-06-11

## Scope

Advanced T012-032B with no-cost action-first coverage for reliable/unreliable
profile-name handling.

Covered in this slice:

- reliable WhatsApp/profile names are assessed from channel metadata and may
  personalize cold greeting or diagnostic start;
- unreliable profile names such as studio/business names are ignored;
- raw unreliable profile names are not exposed in the model preamble;
- no name capture is added to cold greeting.

This slice does not yet implement the optional "ask name at diagnostic entry"
path because the action-first registry does not currently have an approved
name-question template. That remains open rather than invented.

## Sources

- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/behavior-contract.md`
  - real person names only;
  - reliable WhatsApp names may be used naturally;
  - unreliable names must be ignored and not saved as verified names;
  - cold greeting must not ask for name.
- `specs/012-taliya-commercial-agent-agents-sdk-migration/conformity-matrix.pt-BR.md`
  - maps profile-name policy to T012-032B.
- `.agents/skills/taliya-llm-first-agent/SKILL.md`
  - deterministic code may package operational context, but not interpret
    commercial meaning from raw lead text.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/turn_situation.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/decision_compiler.py`
- `services/taliya-agent-runtime/tests/test_spec012_turn_situation.py`
- `services/taliya-agent-runtime/tests/test_spec012_decision_compiler.py`

## Behavior

`TurnSituation` now includes `profile_name_context` derived from persisted
channel metadata only:

- `used_reliable_name` with a first name for person-like profile names;
- `ignored_unreliable_name` for studio/business/handle/unclear names;
- `not_available` when no profile name exists.

The decision compiler uses this context to choose:

- `opening.cold_greeting_named` + `first_name` for reliable names;
- `opening.cold_greeting` for unreliable names;
- `diagnostic.start_named` when a reliable name is available at diagnostic
  start.

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_turn_situation.py tests\test_spec012_decision_compiler.py -q`
  - result: 30 passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 146 passed, 716 deselected
- `python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_turn_situation.py tests\test_spec012_action_agents.py tests\test_spec012_decision_compiler.py tests\test_spec012_action_turn_runner.py tests\test_spec012_action_validators_ported.py tests\test_spec012_static_audit.py tests\test_spec012_action_safety.py`
  - result: all checks passed

## Anti-Determinism Review

This is an operational identity/context boundary. It does not classify
commercial intent, route price/demo/diagnostic/waitlist behavior, or inspect
the current lead message. It only assesses channel metadata with the existing
behavior-policy helper and lets the compiler fill approved `first_name`
variables when the selected action already renders a named template.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, or
client/studio WhatsApp files were edited.

## Paid Calls

None.

## Still Open

- approved "ask name at diagnostic entry" template/action boundary;
- persistence semantics for verified lead-stated names versus unverified
  channel names when endpoint integration is in scope;
- broader name-policy fixtures in the canonical/eval suite.
