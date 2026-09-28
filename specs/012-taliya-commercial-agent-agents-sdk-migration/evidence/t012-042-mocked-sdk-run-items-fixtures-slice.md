# T012-042 Slice - Mocked SDK Run-Item Fixtures

Date: 2026-06-11

## Scope

Started T012-042 with mocked/no-cost SDK run-item fixtures for the isolated
action-first runner.

Covered cases:

- entry turn routed through the triage agent to the product agent;
- known diagnostic state starting directly at the diagnostic specialist;
- one-repair path with validator feedback and repair SDK run items;
- safety boundary with no SDK run items and zero model usage.

The trace now records repair validator feedback and structural repair run-item
summaries when a repair attempt occurs.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_trace.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_turn_runner.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_run_items_mocked.py`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-042-mocked-sdk-run-items-fixtures-slice.md`

## Behavior

`sdk_run_items` and `repair_or_escalation.repair_sdk_run_items` store only
structural summaries:

```text
item_type, raw_item_type, agent_name, tool_name, handoff_target
```

They do not store tool arguments, tool output, or raw provider payloads.

`repair_or_escalation` now includes:

- `repair_attempt_count`;
- `validator_feedback`;
- `repair_sdk_run_items`.

Safety turns remain no-LLM/no-SDK and keep `sdk_run_items = []`.

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_sdk_run_items_mocked.py -q`
  - result: 4 passed
- `python -m ruff check app\core\taliya_commercial_sdk\action_trace.py app\core\taliya_commercial_sdk\action_turn_runner.py tests\test_spec012_sdk_run_items_mocked.py`
  - result: all checks passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 214 passed, 716 deselected

## Anti-Determinism Review

The new tests use mocked `ConductorActionDecision` outputs from the fake SDK
model. No raw lead-text routing, regex commercial brain, or deterministic
commercial interpretation was added. The code change is observability only:
recording SDK run-item summaries and repair validator feedback after the LLM
decision path has already run.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, public
endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None. Cost: `$0`.

## Still Open

T012-042 remains open for the final verification package after endpoint/runtime
integration and any approved real-model/shadow evidence. This slice proves the
isolated action-first mocked run-item cases.
