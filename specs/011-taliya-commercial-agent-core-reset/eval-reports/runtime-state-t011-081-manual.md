# Runtime State T011-081 Manual Report

Status: passed for isolated Spec 011 core runtime-state scope.

Task: `T011-081 - Persist runtime state from validated decision only`.

## Scope

This task added an isolated runtime-state diff builder for accepted/repaired
validated conductor decisions. It does not persist to the database, parse inbound
text, read rendered messages, use Sales Inbox as a source of truth, choose
commercial meaning, send messages, change adapters, change `/pilates`, touch
Sales Inbox UI, or touch `runtime/runner.py`.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_runtime_state_diff.py -q
```

Observed before implementation:

```text
ModuleNotFoundError: No module named 'app.core.taliya_commercial.runtime_state'
```

This confirmed the validated-decision runtime-state boundary did not exist.

## Implemented Checks

- `build_runtime_state_diff` accepts only `ConductorDecision` plus matching
  `ValidatorResult`.
- Runtime state diff requires `status=passed` and
  `final_disposition=accepted|repaired`.
- Repaired diffs require a matching `RepairResult(status=repaired)` and matching
  repaired decision id.
- Blocked, failed, repairable, fallback, and failed-path payloads fail before any
  state diff is produced.
- The diff records state transition, selected template ids, diagnostic state and
  ledger updates, demo/waitlist/handoff state, fact updates, and validation
  metadata from the decision.
- Neutral decision defaults such as diagnostic `none`, demo `not_offered`,
  waitlist `none`, and handoff `none` are treated as no-op updates so they do
  not erase existing runtime state on product follow-up turns.
- The diff contains no rendered messages, free-form customer output, Sales Inbox
  projection, inbound text parsing, delivery, or adapter data.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_runtime_state_diff.py -q
```

Result: `10 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_runtime_state_diff.py tests/test_spec011_trace_store.py tests/test_spec011_failed_path_guards.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py -q
```

Result: `42 passed`.

Broad isolated Spec 011 core/conductor/validator/repair/fallback/policy/product/failed-path/renderer/trace/runtime-state suite:

```powershell
python -m pytest tests/test_spec011_runtime_state_diff.py tests/test_spec011_trace_store.py tests/test_spec011_renderer_channel_rules.py tests/test_spec011_renderer_final_diagnostic.py tests/test_spec011_renderer_variable_contract.py tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_failed_path_guards.py tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `258 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/runtime_state.py tests/test_spec011_runtime_state_diff.py
rg -n "app\.domains|runtime\.runner|AgentRunRequest|request\.message|inbound\.text|^import re\b|^from re\b|regex|\.search\(|\.match\(|isdigit|render_validated|render_template\(|get_template\(|ConductorProvider|openai|send\(|WhatsApp|SalesInboxClient|/pilates|497|120|R\$|checkout|desconto|vip|data de abertura" app/core/taliya_commercial/runtime_state.py
```

Result: Ruff passed. Static `rg` returned no matches.

## Anti-Drift Review

- The LLM remains the source of commercial understanding through the
  `ConductorDecision`.
- Deterministic code only maps already-validated structured decision fields into
  state updates.
- No renderer output, Sales Inbox projection, inbound text, adapter payload, or
  old runner state machine can become the source of state.
- This is isolated-core proof only. Actual database persistence, Sales Inbox
  projection building, eval export, adapters, and production cutover remain later
  phases.

Next task: `T011-082 - Build Sales Inbox projection from runtime state/events`.
