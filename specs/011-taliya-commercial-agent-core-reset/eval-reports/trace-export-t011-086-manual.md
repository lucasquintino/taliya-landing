# Trace Export T011-086 Manual Report

Status: passed for isolated Spec 011 trace export scope.

Task: `T011-086 - Export trace artifacts in the eval/report format required by eval-plan.md`.

## Scope

This task added deterministic JSON/Markdown export for completed `TraceRecord`
artifacts. It does not call OpenAI, render messages, send messages, mutate
runtime state, parse inbound text for commercial meaning, change adapters, change
Sales Inbox UI, change `/pilates`, persist to production storage, or touch
`runtime/runner.py`.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_trace_export.py -q
```

Observed before implementation:

```text
ModuleNotFoundError: No module named 'app.core.taliya_commercial.trace_export'
```

This confirmed there was no isolated trace export boundary.

## Implemented Checks

- `build_trace_eval_record` exports all eval-plan reporting keys:
  scenario id, status, severity, channel, input messages, rendered messages,
  decision JSON, validator results, repair attempts, model usage, runtime state,
  Sales Inbox projection, delivery events, trace completeness, schema version,
  golden transcript diff, assertions, failure reason, and artifact paths.
- `trace_eval_report_to_json` emits deterministic JSON with schema
  `011.eval_report.v1` and summary counts.
- `trace_eval_report_to_markdown` emits concise manual-review sections.
- Export validates the underlying `TraceRecord` with trace-store validation and
  fails when required artifacts such as rendered messages are missing.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_trace_export.py -q
```

Result: `3 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_trace_export.py tests/test_spec011_trace_store.py tests/test_spec011_sales_inbox_projection_builder.py tests/test_spec011_runtime_state_diff.py tests/test_spec011_feedback_loop_prevention.py -q
```

Result: `24 passed`.

Broad isolated Spec 011 core/conductor/validator/repair/fallback/policy/product/failed-path/renderer/trace/runtime-state/projection/export suite:

```powershell
python -m pytest tests/test_spec011_trace_export.py tests/test_spec011_feedback_loop_prevention.py tests/test_spec011_sales_inbox_projection_completeness.py tests/test_spec011_sales_inbox_identity_projection.py tests/test_spec011_sales_inbox_projection_builder.py tests/test_spec011_runtime_state_diff.py tests/test_spec011_trace_store.py tests/test_spec011_renderer_channel_rules.py tests/test_spec011_renderer_final_diagnostic.py tests/test_spec011_renderer_variable_contract.py tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_failed_path_guards.py tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `272 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/trace_export.py tests/test_spec011_trace_export.py
rg -n "app\.domains|runtime\.runner|AgentRunRequest|request\.message|inbound\.text|context\.inbound\.text|^import re\b|^from re\b|regex|\.search\(|\.match\(|isdigit|render_validated|render_template\(|get_template\(|ConductorProvider|openai|send\(|WhatsApp|SalesInboxClient|/pilates|497|120|R\$|checkout|desconto|vip|data de abertura|openai_demo|demo_video|video_production" app/core/taliya_commercial/trace_export.py
```

Result: Ruff passed. Static `rg` returned no matches.

## Anti-Drift Review

- Trace export refuses incomplete trace artifacts instead of filling gaps.
- Export is deterministic and read-only.
- The exported shape covers the eval-plan reporting keys needed for later real
  model, Sales Inbox, and manual-review gates.
- This remains isolated-core proof. Adapter-level and production-path trace
  exports remain later phases.

Next task: `T011-087 - Add review metadata for prompt/policy/template/product-knowledge changes`.
