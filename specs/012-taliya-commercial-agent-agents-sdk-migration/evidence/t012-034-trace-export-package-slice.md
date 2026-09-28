# T012-034 Slice - Local Trace Export Package

Date: 2026-06-11

## Scope

Advanced T012-034 with a local, in-memory trace export package for isolated
action-first conversations.

The package is JSON-friendly and includes:

- scenario id;
- proof mode;
- explicit external trace export disabled marker;
- required trace section list from `trace-map.md`;
- turn count and trace count;
- trace completeness checks;
- missing-section and missing-trace indexes;
- final state, transcript, total model operations, and cost;
- per-turn status, mode, selected action, template ids, usage, Sales Inbox
  projection presence, and the turn trace.

Operational suppressed/deferred turns do not require a trace because no
customer response, SDK run, validator path, or state commit happened. Delivered,
failed, and safety-blocked turns do require complete traces.

## Sources

- `trace-map.md`
  - requires local evidence for inbound, turn gate, turn situation, SDK run
    items, final structured output, validators, repair/escalation, render,
    state diff, Sales Inbox projection, and usage/cost.
- `decision-log.md` / D-012-007 and D-012-009
  - external SDK/provider trace export remains disabled.
- `.agents/skills/taliya-llm-first-agent/SKILL.md`
  - observability/tracing is allowed deterministic infrastructure.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_trace.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_trace_export.py`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-034-trace-export-package-slice.md`

## Behavior

`export_action_conversation_trace_package(...)` builds
`012.action_trace_export.v1`.

It does not write to disk, does not call OpenAI, does not enable SDK tracing,
and does not expose raw provider payloads. SDK run items remain structural
summaries only:

```text
item_type, raw_item_type, agent_name, tool_name, handoff_target
```

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_action_trace_export.py -q`
  - result: 2 passed
- `python -m ruff check app\core\taliya_commercial_sdk\action_trace.py tests\test_spec012_action_trace_export.py`
  - result: all checks passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 208 passed, 716 deselected

## Anti-Determinism Review

This slice is observability/export packaging only. It reads already-produced
runner reports and traces; it does not inspect lead text to route commercial
meaning, does not choose actions, does not add templates, and does not change
LLM prompts.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, public
endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None. Cost: `$0`.

## Still Open

T012-034 remains open for runtime trace store/export integration after endpoint
integration is approved. T012-045 still requires final mandatory trace evidence
export for the verification package.
