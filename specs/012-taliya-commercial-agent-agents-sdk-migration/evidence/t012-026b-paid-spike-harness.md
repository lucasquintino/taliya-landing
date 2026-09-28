# T012-026B Evidence - No-Cost Real SDK Runner Harness And Dry-Run Gate

Status: completed on 2026-06-09. No paid OpenAI call was run.

## Why This Task Exists

T012-020 deferred the real Agents SDK runner ("A real Agents SDK runner is not
implemented in T012-020") and no later task delivered it. Approving T012-027
without a real harness would burn paid calls on infrastructure failures:

- agents had no `output_type`, so a real run would return free-form text and
  every scenario would fail at the output adapter;
- `TaliyaTurnProposal` is not strict-JSON-schema compatible (verified locally:
  `AgentOutputSchema(TaliyaTurnProposal)` raises `UserError` because of
  `dict[str, Any]` fields);
- the SDK exports traces to OpenAI by default, violating D-012-007 local-only
  traces on the first call;
- no usage/cost capture or budget abort enforcement existed, so the packet's
  "usage/cost cannot be recorded" abort gate would fire immediately;
- multi-turn scenarios (6, 7, 11, 15) had no frozen input fixtures with prior
  transcript/state.

T012-026B closes all of these before any budget request.

## Scope Completed

- Strict SDK-facing output model `TaliyaSdkTurnOutput` in
  `sdk_output_model.py`: fully typed (no `dict[str, Any]`), verified
  compatible with `AgentOutputSchema` strict mode. The model owns only
  commercial content; identity, agent path, and usage are harness-owned.
- All six agents now declare `output_type=TaliyaSdkTurnOutput`
  (`agents.py`), so SDK final output is always a structured proposal.
- Local run context `TaliyaSpikeContext` (`run_context.py`): the state
  snapshot travels in the SDK local context; the three state-read tools
  (`get_diagnostic_ledger`, `get_conversation_summary`,
  `get_demo_waitlist_handoff_state`) read it via `RunContextWrapper` instead
  of requiring the model to echo `state_snapshot_json`.
- `adapt_sdk_run_result_to_turn_proposal` (`output_adapter.py`): adapts a real
  `RunResult` into `TaliyaTurnProposal`; rejects anything that is not the
  strict structured output; injects harness-measured usage so the model
  cannot self-report cost.
- Frozen paid spike inputs (`spike_scenarios.py`): the 15 packet scenarios in
  packet order, including prior transcript and state snapshots for scenarios
  6 (numeric `120`), 7 (urgency final), 11 (contract intent after
  diagnostic/demo), and 15 (delivery concurrency).
- Paid spike harness (`paid_spike_harness.py`):
  - `set_tracing_disabled(True)` plus
    `RunConfig(tracing_disabled=True, trace_include_sensitive_data=False)`
    before any model call (D-012-007);
  - paid gate: `require_paid_approval` plus preconditions (recorded pricing,
    `OPENAI_API_KEY` present); an injected SDK `Model` instance runs the same
    harness as a no-cost dry-run;
  - budget meter: stops before exceeding 45 model operations or `$1.00`
    estimated cost; `max_turns=3` enforces the per-scenario operation cap;
  - abort gates: free-form/non-structured output aborts the run; unrecorded
    usage aborts the run; `MaxTurnsExceeded` charges worst-case usage for
    budget safety;
  - local-only report writer: per-scenario JSON plus run summary JSON/markdown
    with all packet-required report fields.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/run_context.py` (new)
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/sdk_output_model.py` (new)
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/spike_scenarios.py` (new)
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/paid_spike_harness.py` (new)
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/agents.py` (output_type wiring)
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/tools.py` (context-based state reads)
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/output_adapter.py` (RunResult adapter)
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/__init__.py` (exports)
- `services/taliya-agent-runtime/tests/test_spec012_sdk_paid_harness_dry_run.py` (new)

## Tests And Static Checks

```text
python -m pytest tests\test_spec012_sdk_mocked_contracts.py
  tests\test_spec012_sdk_validators_adapter.py
  tests\test_spec012_sdk_output_adapter.py
  tests\test_spec012_sdk_agents.py
  tests\test_spec012_sdk_spike_isolation.py
  tests\test_spec012_sdk_paid_harness_dry_run.py -q
56 passed
```

```text
python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_sdk_*.py
All checks passed!
```

Dry-run proof (scripted fake `Model` through the real `Runner.run`):

- triage handoff -> specialist tool call -> strict structured final output;
- ctx-based ledger tool reads the frozen state snapshot through the real
  runner (`run_context_snapshot` source recorded in tool output);
- usage measured from the runner (`requests`/tokens), not from model output;
- budget meter aborts before exceeding the operation ceiling;
- free-form final output aborts the run with `sdk_output_not_structured`;
- paid path stays blocked without explicit approval
  (`SdkSpikePaidCallBlocked`) and without pricing/API key
  (`SpikePreconditionError`);
- report files are written locally with all packet-required fields.

## Proof Type

Mocked dry-run through the real Agents SDK runner. No paid call.

## Anti-Determinism Review

No regex/token routing added. The harness is operational plumbing (budget,
tracing, reporting, fixtures). Commercial understanding remains in the SDK
agents/LLM. Tools remain read-only/proposal-only; `COMMIT_TOOL_NAMES` is empty.

## Protected-Scope Diff Result

Only `app/core/taliya_commercial_sdk/`, Spec 012 tests, and Spec 012 docs were
touched. No `/pilates`, landing UI, Sales Inbox UI, multi-tenant, client/studio
WhatsApp, checkout, or public endpoint change. `app/main.py` still does not
import the SDK package (covered by isolation tests).

## Paid-Call Status

Not run. Cost: $0.00.

## Decisions Taken Under User Delegation (2026-06-09)

- D-012-008 strict SDK-facing output model instead of
  `strict_json_schema=False` on `TaliyaTurnProposal`;
- D-012-009 SDK trace export fully disabled for spike runs (local-only);
- D-012-010 spike guardrails (prompt injection/unsupported media/sensitive)
  formally deferred to Phase 3 — the 15 frozen scenarios do not exercise them;
- D-012-011 scenario 15 stays in the frozen paid list for packet fidelity, with
  the report noting it proves structure (defer proposal), not runtime gating.

## Next Task Lock

T012-027 only, and only after the user gives the packet's explicit approval
wording for paid OpenAI calls and the `$1.00` ceiling.
