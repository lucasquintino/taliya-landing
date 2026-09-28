# Product Fact Static Audit T011-088 Manual Report

Status: passed for isolated Spec 011 product-fact static audit scope.

Task: `T011-088 - Add CI/static audit to block product facts in prompts/templates/tests/fallbacks when they belong in official product knowledge or Spec 006`.

## Scope

This task added a deterministic product-fact audit helper. It detects forbidden
product facts and promise terms in non-official surfaces. It does not change
prompts, templates, product knowledge, runtime behavior, adapters, Sales Inbox
UI, `/pilates`, delivery, database persistence, or `runtime/runner.py`.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_product_fact_static_audit.py -q
```

Observed before implementation:

```text
ModuleNotFoundError: No module named 'app.core.taliya_commercial.product_fact_static_audit'
```

This confirmed no isolated product-fact audit helper existed.

## Implemented Checks

- Audit flags price-like literals, checkout/payment/discount/VIP promises,
  opening-date/pre-sale promises, unsupported integration/certification claims,
  and technical/video demo claims outside approved sources.
- Official product knowledge and Spec 006 contract paths are allowed.
- Explicit fixture paths can be allowlisted for do-not-do metadata.
- Findings include code, path, line, snippet, and matched term.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_product_fact_static_audit.py -q
```

Result: `3 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_product_fact_static_audit.py tests/test_spec011_governance_metadata.py tests/test_spec011_validators_product_claims.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_template_registry.py -q
```

Result: `19 passed`.

Broad isolated Spec 011 core/conductor/validator/repair/fallback/policy/product/failed-path/renderer/trace/runtime-state/projection/export/governance/static-audit suite:

```powershell
python -m pytest tests/test_spec011_product_fact_static_audit.py tests/test_spec011_governance_metadata.py tests/test_spec011_trace_export.py tests/test_spec011_feedback_loop_prevention.py tests/test_spec011_sales_inbox_projection_completeness.py tests/test_spec011_sales_inbox_identity_projection.py tests/test_spec011_sales_inbox_projection_builder.py tests/test_spec011_runtime_state_diff.py tests/test_spec011_trace_store.py tests/test_spec011_renderer_channel_rules.py tests/test_spec011_renderer_final_diagnostic.py tests/test_spec011_renderer_variable_contract.py tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_failed_path_guards.py tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `278 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/product_fact_static_audit.py tests/test_spec011_product_fact_static_audit.py
rg -n "runtime\.runner|request\.message|inbound\.text|context\.inbound\.text|^import re\b|^from re\b|regex|\.search\(|\.match\(|isdigit|render_validated|render_template\(|get_template\(|ConductorProvider|send\(|WhatsApp|SalesInboxClient|/pilates" app/core/taliya_commercial/product_fact_static_audit.py
```

Result: Ruff passed. Static `rg` returned no matches for runtime/adapter/parser risks. Product/promise terms appear only as blocked audit patterns and test fixtures.

## Anti-Drift Review

- The audit is detection-only and does not modify runtime behavior.
- Product facts remain sourced from official product knowledge or Spec 006.
- Test fixture allowlisting is explicit.

Next task: `T011-089 - Add cost optimization reports proving token/cost reduction without removing model usage or degrading golden transcripts`.
