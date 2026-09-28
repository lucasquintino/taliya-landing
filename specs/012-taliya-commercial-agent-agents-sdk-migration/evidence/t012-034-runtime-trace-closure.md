# T012-034 Runtime Trace Closure

Status: completed on 2026-06-15.

## Scope

This closure adapts the action-first SDK trace path for local/runtime evidence:
SDK run items, context snapshot, turn situation, action decision, compiler
records, validator/repair records, state diff, Sales Inbox projection,
delivery metadata, and usage/cost are available without enabling external SDK
trace export.

No paid provider call, public cutover, shadow traffic, external trace export,
`/pilates` visual/copy/layout, Sales Inbox UI, checkout, multi-tenant, or
client/studio WhatsApp change was made.

## Files

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_trace.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_turn_runner.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/runtime_adapter.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_trace_export.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`
- `services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`
- `services/taliya-agent-runtime/tests/test_spec012_static_audit.py`

## Proof

- Isolated action-first turns build local trace records with required sections:
  context snapshot, turn situation, SDK start/run items, action decision,
  compiler, validators, repair/escalation, render plan, state diff, Sales Inbox
  projection, delivery, and usage/cost.
- Local trace package export uses schema `012.action_trace_export.v1` and keeps
  `external_trace_export.enabled=false`.
- Safety turns trace the zero-LLM path with empty SDK run items and zero cost.
- Runtime adapter responses expose trace-derived `context_snapshot`,
  `turn_situation`, `action_decision`, validator results, repair attempts,
  delivery metadata, and trace completeness.
- Runtime events persist `012.runtime_action_trace_summary.v1` with SDK run
  items, situation, decision, compiler, validators, projection, delivery, and
  usage/cost.
- Runtime event trace summaries intentionally omit raw `inbound` and
  `rendered_messages` fields.
- Static audit blocks public delivery claims and external trace export enablement.

## Validation

Commands run from `C:\Users\lucas\agentes-landing-system`:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_agent_runs_api.py services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 16 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/app/main.py services/taliya-agent-runtime/app/core/taliya_commercial_sdk/runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 242 passed, 716 deselected.

## Anti-Determinism Review

Trace and export code observes the action-first pipeline after the LLM has
returned structured `ConductorActionDecision`. It does not classify raw lead
text, choose commercial meaning, generate customer copy, or introduce a
template-first routing path.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.
