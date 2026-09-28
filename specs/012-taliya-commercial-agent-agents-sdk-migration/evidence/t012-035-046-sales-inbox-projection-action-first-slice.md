# T012-035/T012-046 Sales Inbox projection action-first slice

Date: 2026-06-11

## Scope

Added mocked/no-cost Sales Inbox projection evidence for the isolated
action-first SDK runner. This is a partial closure for T012-035 and T012-046:
it proves the SDK path can derive and export a valid projection from validated
state, but it does not yet wire production endpoint persistence or Sales Inbox
UI.

## Files

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_validators.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_turn_runner.py`
- `services/taliya-agent-runtime/tests/test_spec012_sales_inbox_projection.py`

## Behavior Proven

- The action-first runner now attaches `sales_inbox_projection` to each
  delivered turn report.
- The projection is built only after action validation passes.
- The projection reuses the preserved Spec 011 builder and validator:
  action-first compiled output is adapted to the existing
  `ConductorDecision`/`TurnContext`, `build_runtime_state_diff`, and
  `build_sales_inbox_projection` path.
- A price turn projects commercial stage, diagnostic-offered status, template
  ids, validator status, source labels, conversation id, and lead id.
- A completed diagnostic turn projects completed diagnostic status, complete
  mandatory ledger, final plan/range, final demo line, and operator next
  action.
- Completed diagnostic `final_fields` are persisted in the isolated runner
  state so later product/demo/waitlist/handoff turns can keep Sales Inbox
  consistent without recalculating commercial meaning.

## Anti-Determinism Review

No raw lead-text router, regex brain, or Sales Inbox inference brain was added.
Sales Inbox remains a projection of accepted action-first decisions, compiled
template ids, validated runtime state, and delivery events. The LLM/fake model
still owns semantic action and slot selection.

## Commands

- `python -m pytest tests\test_spec012_sales_inbox_projection.py -q`
  - `2 passed`
- `python -m pytest tests\test_spec012_sales_inbox_projection.py tests\test_spec012_canonical_p0_mocked.py tests\test_spec012_canonical_action_first_mocked.py -q`
  - `19 passed`
- `python -m pytest tests\test_spec011_sales_inbox_projection_builder.py tests\test_spec011_validators_sales_inbox.py -q`
  - `17 passed`
- `python -m pytest tests\ -k spec012 -q`
  - `183 passed, 716 deselected`
- `python -m ruff check app\core\taliya_commercial_sdk\action_validators.py app\core\taliya_commercial_sdk\action_turn_runner.py tests\test_spec012_sales_inbox_projection.py`
  - passed

## Protected Scope

No `/pilates` layout, landing visual, Sales Inbox UI, multi-tenant, client or
studio WhatsApp integration, checkout, or public endpoint cutover was touched.

## Paid Calls

None. All execution used mocked/no-cost SDK model paths; total cost remained
`$0`.

## Still Open

- T012-035 production-path persistence/end-to-end endpoint wiring.
- T012-046 final export package after trace/export integration.
- Quality judge/repetition gates.
- Real-model evidence only after explicit paid approval.
