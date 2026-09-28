# Cost Report T011-089 Manual Report

Status: passed for isolated Spec 011 cost-report governance scope.

Task: `T011-089 - Add cost optimization reports proving token/cost reduction without removing model usage or degrading golden transcripts`.

## Scope

This task added a cost optimization report validator. It does not change model
selection, prompts, routing, templates, runtime behavior, adapters, Sales Inbox
UI, `/pilates`, delivery, database persistence, or `runtime/runner.py`.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_cost_report.py -q
```

Observed before implementation:

```text
ModuleNotFoundError: No module named 'app.core.taliya_commercial.cost_report'
```

This confirmed there was no cost optimization report gate.

## Implemented Checks

- Report requires before/after runtime model usage by scenario.
- Normal commercial turns fail if after-optimization runtime usage has zero or
  missing input/output tokens.
- Cost savings cannot pass if behavior gate regresses.
- Cost savings require approved golden transcript diff.
- Eval-only/judge usage is represented separately from runtime usage.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_cost_report.py -q
```

Result: `3 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_cost_report.py tests/test_spec011_conductor_usage.py tests/test_spec011_trace_export.py tests/test_spec011_governance_metadata.py tests/test_spec011_conductor_boundary.py -q
```

Result: `20 passed`.

Broad isolated Spec 011 core/conductor/validator/repair/fallback/policy/product/failed-path/renderer/trace/runtime-state/projection/export/governance/static-audit/cost suite:

```powershell
python -m pytest tests/test_spec011_cost_report.py tests/test_spec011_product_fact_static_audit.py tests/test_spec011_governance_metadata.py tests/test_spec011_trace_export.py tests/test_spec011_feedback_loop_prevention.py tests/test_spec011_sales_inbox_projection_completeness.py tests/test_spec011_sales_inbox_identity_projection.py tests/test_spec011_sales_inbox_projection_builder.py tests/test_spec011_runtime_state_diff.py tests/test_spec011_trace_store.py tests/test_spec011_renderer_channel_rules.py tests/test_spec011_renderer_final_diagnostic.py tests/test_spec011_renderer_variable_contract.py tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_failed_path_guards.py tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `281 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/cost_report.py tests/test_spec011_cost_report.py
rg -n "runtime\.runner|request\.message|inbound\.text|context\.inbound\.text|^import re\b|^from re\b|regex|\.search\(|\.match\(|isdigit|render_validated|render_template\(|get_template\(|ConductorProvider|send\(|WhatsApp|SalesInboxClient|/pilates|if .*pre[cç]o|if .*demo|if .*diagn" app/core/taliya_commercial/cost_report.py
```

Result: Ruff passed. Static `rg` returned no matches.

## Anti-Drift Review

- Lower cost is blocked when model usage disappears.
- Lower cost is blocked when behavior regresses or transcript diff lacks
  approval.
- This is reporting/validation only, with no runtime optimization shortcut.

Next task: `T011-090 - Point widget runtime adapter to the new core`.
