# Trace T011-080 Manual Report

Status: passed for isolated Spec 011 core trace-persistence scope.

Task: `T011-080 - Persist inbound, context, decision, validation, repair, render, usage, runtime diff, Sales Inbox projection, and delivery events as the mandatory turn trace`.

## Scope

This task added an isolated trace persistence boundary for completed core turns.
It does not parse inbound text, choose commercial routes, render messages, repair
decisions, send messages, change `/pilates`, cut over adapters, touch Sales
Inbox UI, or touch `runtime/runner.py`.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_trace_store.py -q
```

Observed before implementation:

```text
ModuleNotFoundError: No module named 'app.core.taliya_commercial.trace_store'
```

This confirmed the mandatory trace persistence boundary did not exist.

## Implemented Checks

- `build_turn_trace` creates a validated `TraceRecord`.
- Trace includes inbound/context, decision, validator result, repair result,
  render plan, rendered messages, model usage, runtime state diff, delivery
  events, and Sales Inbox projection.
- Stable JSON serialization roundtrips without changing content.
- `TraceFileStore` supports save/load/list by conversation.
- Missing rendered messages for rendered turns fail with `TracePersistenceError`.
- Cross-turn decision/context mismatches fail.
- Sales Inbox projection conversation mismatch fails.
- Template variables remain typed after trace roundtrip.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_trace_store.py -q
```

Result: `5 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_trace_store.py tests/test_spec011_context_snapshot.py tests/test_spec011_core_schemas.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_renderer_channel_rules.py tests/test_spec011_renderer_validated_plan.py -q
```

Result: `41 passed`.

Broad isolated Spec 011 core/conductor/validator/repair/fallback/policy/product/failed-path/renderer/trace suite:

```powershell
python -m pytest tests/test_spec011_trace_store.py tests/test_spec011_renderer_channel_rules.py tests/test_spec011_renderer_final_diagnostic.py tests/test_spec011_renderer_variable_contract.py tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_failed_path_guards.py tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `248 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/trace_store.py tests/test_spec011_trace_store.py
rg -n "app\.domains|runtime\.runner|AgentRunRequest|request\.message|inbound\.text|^import re\b|^from re\b|regex|\.search\(|\.match\(|isdigit|render_validated|render_template\(|get_template\(|ConductorProvider|openai|send\(|WhatsApp|SalesInboxClient|/pilates|497|120|R\$|checkout|desconto|vip|data de abertura" app/core/taliya_commercial/trace_store.py
```

Result: Ruff passed. Static `rg` returned no matches.

## Anti-Drift Review

- Trace persistence records artifacts only; it does not create customer-facing
  output or choose commercial meaning.
- Incomplete trace artifacts fail loudly with typed errors.
- Trace proof is isolated-core proof only. Runtime-state diff generation, Sales
  Inbox projection building, eval exports, adapters, and production cutover
  remain later phases.

Next task: `T011-081 - Persist runtime state from validated decision only`.
