# Feedback Loop T011-085 Manual Report

Status: passed for isolated Spec 011 inferred-fact feedback-loop scope.

Task: `T011-085 - Prevent adapter/Sales Inbox inferred facts from re-entering conductor context as reliable facts without source/confidence labels`.

## Scope

This task added a safe export boundary for Sales Inbox identity/contact fields
when they are reused as future context facts. It does not parse inbound text,
choose commercial meaning, send messages, change public adapters, change Sales
Inbox UI, change `/pilates`, persist to production storage, or touch
`runtime/runner.py`.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_feedback_loop_prevention.py -q
```

Observed before implementation:

```text
ImportError: cannot import name 'export_projection_identity_facts_for_context'
```

This confirmed there was no explicit safe export boundary for projection
identity/contact values.

## Implemented Checks

- `export_projection_identity_facts_for_context` exports projection identity
  values as `source=sales_inbox_projection`.
- Exported projection facts always re-enter as `reliability=unverified` and
  `confidence=low`.
- Original projection source/verified values are preserved as metadata, but not
  promoted into reliable conductor context.
- Rehydrated `TurnContext` keeps those facts non-renderable and unverified.
- Channel-provided and projection-provided identity/contact values cannot become
  customer/operator-provided facts through this loop.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_feedback_loop_prevention.py -q
```

Result: `1 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_feedback_loop_prevention.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_sales_inbox_identity_projection.py tests/test_spec011_sales_inbox_projection_builder.py tests/test_spec011_context_builder.py tests/test_spec011_internal_metadata_non_renderable.py -q
```

Result: `17 passed`.

Broad isolated Spec 011 core/conductor/validator/repair/fallback/policy/product/failed-path/renderer/trace/runtime-state/projection/feedback-loop suite:

```powershell
python -m pytest tests/test_spec011_feedback_loop_prevention.py tests/test_spec011_sales_inbox_projection_completeness.py tests/test_spec011_sales_inbox_identity_projection.py tests/test_spec011_sales_inbox_projection_builder.py tests/test_spec011_runtime_state_diff.py tests/test_spec011_trace_store.py tests/test_spec011_renderer_channel_rules.py tests/test_spec011_renderer_final_diagnostic.py tests/test_spec011_renderer_variable_contract.py tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_failed_path_guards.py tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `269 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/sales_inbox_projection.py tests/test_spec011_feedback_loop_prevention.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_sales_inbox_identity_projection.py
rg -n "app\.domains|runtime\.runner|request\.message|inbound\.text|context\.inbound\.text|^import re\b|^from re\b|regex|\.search\(|\.match\(|isdigit|render_validated|render_template\(|get_template\(|ConductorProvider|openai|send\(|WhatsApp|SalesInboxClient|/pilates|497|120|R\$|checkout|desconto|vip|data de abertura|openai_demo|demo_video|video_production" app/core/taliya_commercial/sales_inbox_projection.py
```

Result: Ruff passed. Static `rg` returned no matches for the changed projection module.

## Anti-Drift Review

- Sales Inbox-projected identity/contact values can be shown operationally, but
  they cannot become reliable conductor facts on re-entry.
- The export carries source/confidence labels and fails closed to unverified.
- This remains isolated-core proof. Production persistence and adapter cutover
  are still later phases.

Next task: `T011-086 - Export trace artifacts in the eval/report format required by eval-plan.md`.
