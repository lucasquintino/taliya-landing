# T012-034 Trace Map Compatibility Slice

Date: 2026-06-11

## Scope

Aligned the local action-first trace package with the named sections in
`trace-map.md` while keeping SDK/provider trace export disabled.

This is an observability-only slice. It does not change model routing,
commercial interpretation, validators, renderer copy, endpoint wiring, or
public delivery.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_trace.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_trace_export.py`

## Behavior Covered

The action-first trace required section list now includes trace-map compatible
blocks:

- `context_snapshot`
- `taliya_proposal`
- `delivery`

For the v2 action-first architecture, `taliya_proposal` is represented as a
compatibility block:

- `boundary=action_first`
- `superseded_schema=TaliyaTurnProposal`
- `action_decision=<structured ConductorActionDecision>`
- `direct_sdk_delivery_allowed=false`

The `delivery` block records local preview/delivery state only:

- `public_delivery=false`
- `outbox_reserved=false`
- rendered count
- compiler chunk policy

Safety traces include the same compatibility sections with zero SDK items,
zero cost, no proposal text delivery, and no outbox reservation.

## Tests Run

- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_action_trace_export.py -q`
  - Result: `2 passed`
- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_action_trace_export.py services/taliya-agent-runtime/tests/test_spec012_sdk_run_items_mocked.py services/taliya-agent-runtime/tests/test_spec012_static_audit.py -q`
  - Result: `13 passed`
- `python -m ruff check services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_trace.py services/taliya-agent-runtime/tests/test_spec012_action_trace_export.py`
  - Result: passed

## Anti-Determinism Review

No lead text is interpreted by deterministic code. This slice only packages
already-produced pipeline artifacts for local debugging/evidence. The LLM still
selects the action decision; compiler/validators/renderer still own their
existing deterministic boundaries.

## Protected Scope Review

No `/pilates`, landing visual, Sales Inbox UI, multi-tenant, client/studio
WhatsApp, checkout, or public endpoint files were changed.

## Paid Call Review

No paid OpenAI call was made. Tests use mocked/no-cost runner traces.

## Open Items

T012-034 remains open for final endpoint/runtime trace-store proof after
public integration is authorized. This slice closes the local trace-map
compatibility gap for mocked action-first evidence packages.
