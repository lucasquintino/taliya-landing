# T012-031/T012-036 Feature-Flag Runtime Adapter Slice

Status: started / partial on 2026-06-15.

## Scope

This no-cost slice starts the endpoint/runtime integration for the Spec 012
action-first SDK path without public cutover.

The current public endpoint remains `/v1/taliya-commercial/turn`. The new SDK
path is gated by `TALIYA_SPEC012_ACTION_FIRST_ENABLED`, which defaults to
`false`. When the flag is off, the endpoint keeps the existing Spec 011 runtime
path.

When the flag is on, the endpoint routes to a narrow action-first runtime
adapter. That adapter still blocks real OpenAI provider calls in this slice; it
requires an injected no-cost SDK model in mock mode for local proof.

No `/pilates`, landing visual/copy/layout, Sales Inbox UI, checkout,
multi-tenant, client/studio WhatsApp, shadow traffic, or public activation path
was changed.

## Files

- `services/taliya-agent-runtime/app/settings.py`
- `services/taliya-agent-runtime/app/main.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/runtime_adapter.py`
- `services/taliya-agent-runtime/tests/test_agent_runs_api.py`
- `services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py`
- `services/taliya-agent-runtime/tests/test_spec012_static_audit.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`
- SDK isolation tests updated to reflect the new allowed feature-flagged
  adapter boundary.

## Added Runtime Coverage

- `TALIYA_SPEC012_ACTION_FIRST_ENABLED=false` remains the default.
- Flag off preserves the current Spec 011 public endpoint behavior.
- Flag on routes `/v1/taliya-commercial/turn` to
  `run_action_first_agent_turn`.
- The legacy `/v1/agent-runs` commercial quarantine remains unchanged.
- HMAC verification and request-id idempotency remain owned by the endpoint
  before the SDK adapter runs.
- Repeating the same request id returns the saved SDK-path response.
- `TALIYA_AGENT_PROVIDER=openai` with the Spec 012 flag on is blocked with
  `spec012_action_first_paid_call_blocked`; the idempotency cache is not
  written for that blocked request.
- The runtime adapter can convert a no-cost injected SDK fake-model run into
  the public `AgentRunResponse` shape and persist runtime state.
- The runtime adapter now maps the canonical action-first trace sections
  (`compiler`, `action_decision`, `validators`, `repair_or_escalation`) into
  the public response shape instead of accepting older spike trace keys.
- The adapter contract test asserts compiler-derived state, template ids,
  action decision, validator status, repair count, and persisted
  `last_decision`.
- The runtime state bridge now preserves action-first state fields used by the
  public memory contract: demo, waitlist, diagnostic, lead_facts,
  asked_questions, answered_direct_questions, profile_name_status, and
  product_source_version when they are present in the runner final state.
- Added no-cost proof that a demo answer persists `demo.status=offered`,
  records the answered direct question, keeps input items, and saves the
  compiler next state.
- The public response now carries the runner's local `context_snapshot` and a
  local-preview delivery event with trace delivery metadata. The proof asserts
  `public_delivery=false` and `outbox_reserved=false`; external trace export
  stays disabled.
- The adapter now seeds the action-first runner with public transport identity
  from the request (`conversation_id`, `lead_id`, `source`, `channel`) so the
  Sales Inbox projection no longer falls back to isolated-runner defaults such
  as `spec012_action_conv`.
- The runtime adapter proof asserts the public response projection carries the
  real `conversation_id`, `lead_id`, commercial stage, and template ids.
- Runtime events now persist a local `012.runtime_action_trace_summary.v1`
  summary with SDK start/run items, context snapshot, turn situation, action
  decision, compiler, validators, repair, render plan, state diff, Sales Inbox
  projection, delivery metadata, and usage/cost. The summary intentionally
  omits raw `inbound` and `rendered_messages` fields.
- The public adapter now enforces the configured per-conversation cost cap
  before invoking the SDK. When prior persisted cost is at or above the cap,
  the adapter returns `cost_capped`, emits no assistant messages, marks human
  follow-up active, records a guardrail event, and does not require an injected
  SDK model.
- `app/main.py` passes `TALIYA_AGENT_HARD_COST_CAP_USD` into the action-first
  adapter.

## Static Audit Update

The old T012-040 invariant said the public runtime could not mention the SDK at
all before flag cutover. That invariant was correct before T012-031 started.

The new invariant is narrower and phase-appropriate:

- public app code may only touch the SDK through `app/main.py`;
- the path must be controlled by `spec012_action_first_enabled`;
- public code must not import the spike runner, paid harness, or output adapter
  as a direct delivery path.

## Validation

Commands run from `C:\Users\lucas\agentes-landing-system`:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_agent_runs_api.py services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_static_audit.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 23 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/app/main.py services/taliya-agent-runtime/app/settings.py services/taliya-agent-runtime/app/core/taliya_commercial_sdk/runtime_adapter.py services/taliya-agent-runtime/tests/test_agent_runs_api.py services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_static_audit.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_sdk_agents.py services/taliya-agent-runtime/tests/test_spec012_sdk_spike_isolation.py services/taliya-agent-runtime/tests/test_spec012_sdk_paid_harness_dry_run.py services/taliya-agent-runtime/tests/test_spec012_sdk_validators_adapter.py services/taliya-agent-runtime/tests/test_spec012_sdk_output_adapter.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 238 passed, 716 deselected.

Follow-up hardening on 2026-06-15:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py -q
```

Result: 1 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/app/core/taliya_commercial_sdk/runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_static_audit.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 240 passed, 716 deselected.

State persistence follow-up:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 4 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/app/core/taliya_commercial_sdk/runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_static_audit.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 241 passed, 716 deselected.

Runtime cost-cap follow-up:

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

Runtime trace-summary follow-up:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 4 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/app/core/taliya_commercial_sdk/runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 241 passed, 716 deselected.

Sales Inbox identity follow-up:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 4 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/app/core/taliya_commercial_sdk/runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 241 passed, 716 deselected.

Local trace-response follow-up:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 4 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/app/core/taliya_commercial_sdk/runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_static_audit.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 241 passed, 716 deselected.

## Anti-Determinism Review

The endpoint does not inspect raw lead text to choose commercial meaning. It
only selects an engine path by an operational feature flag. The adapter invokes
the existing action-first runner, where the LLM still returns structured
`ConductorActionDecision` output and deterministic code handles state,
official facts, compiler expansion, validation, rendering, persistence,
delivery metadata, trace and cost boundaries.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.

## Still Open

T012-031/T012-036 remain open overall. Remaining work:

- inject the real provider path only after explicit paid approval;
- complete endpoint persistence parity for all diagnostic/waitlist/handoff
  state fields;
- expand runtime trace-store/export evidence after the adapter is production
  shaped;
- re-run static audit/contract tests after any additional endpoint changes;
- prove shadow/rollback/cutover separately.
