# T012-034 Slice - Local Action-First Trace

Date: 2026-06-11

## Scope

Started T012-034 with a local, JSON-friendly trace record for the isolated
action-first SDK runner.

Covered trace sections:

- inbound;
- turn gate status;
- turn situation: mode, pending key, allowed actions, template groups,
  obligations, profile-name context, post-diagnostic context;
- SDK start: selected starting agent and whether the LLM was called;
- SDK run-item structural summaries;
- structured `ConductorActionDecision`;
- Decision Compiler expansion: selected action, states, template ids, issues;
- validator result;
- repair attempt count;
- render plan and rendered messages;
- state diff;
- Sales Inbox projection;
- model usage/cost.

SDK trace export remains disabled. This slice only adds local trace data to
`ActionTurnReport`.

## Sources

- `specs/012-taliya-commercial-agent-agents-sdk-migration/trace-map.md`
  - requires action-first traces to record Turn Situation,
    `ConductorActionDecision`, Decision Compiler expansion, repair events,
    validator feedback, rendered output, projection, and usage.
- `specs/011-taliya-commercial-agent-core-reset/spec.md`
  - mandatory trace is required for normal commercial turns.
- `.agents/skills/taliya-llm-first-agent/SKILL.md`
  - tracing/observability is allowed deterministic infrastructure.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_trace.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_turn_runner.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_safety.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_validators.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_validators_ported.py`

## Behavior

`ActionTurnReport.trace` now carries `trace_schema =
012.action_turn_trace.v1`.

For normal mocked SDK turns, the trace proves the full action-first path:

```text
turn_situation -> sdk_start/sdk_run_items -> action_decision -> compiler
-> validators -> render_plan/rendered_messages -> state_diff
-> sales_inbox_projection -> usage_cost
```

For safety turns, the trace proves the operational no-LLM path:

```text
safety boundary -> approved safety template -> zero SDK run items
-> zero model operations
```

The SDK run-item section stores only structural summaries such as item type,
raw item type, agent name, tool name, and handoff target when available. It does
not export raw provider payloads.

During this work, the validator was also aligned with the approved
T012-032B name-question template: `com quem eu falo?` remains blocked in
general customer copy, but is allowed for `diagnostic.ask_name_at_entry`.

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_action_turn_runner.py tests\test_spec012_action_safety.py -q`
  - result: 17 passed
- `python -m pytest tests\test_spec012_action_validators_ported.py::test_action_validator_allows_approved_name_question_at_diagnostic_entry -q`
  - result: 1 passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 203 passed, 716 deselected
- `python -m ruff check app\core\taliya_commercial_sdk\action_trace.py app\core\taliya_commercial_sdk\action_turn_runner.py app\core\taliya_commercial_sdk\action_validators.py tests\test_spec012_action_turn_runner.py tests\test_spec012_action_safety.py tests\test_spec012_action_validators_ported.py`
  - result: all checks passed

## Anti-Determinism Review

This is observability only. It does not inspect lead text to choose actions,
does not alter model routing, and does not render new customer copy. It records
what the LLM selected and what compiler/validators/rendering did afterward.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, public
endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None.

## Still Open

T012-034 remains open for full trace store/export integration once
T012-031/T012-036 endpoint/runtime integration is allowed. T012-045 will still
need exported mandatory trace evidence.
