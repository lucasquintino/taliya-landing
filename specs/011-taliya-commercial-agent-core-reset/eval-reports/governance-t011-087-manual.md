# Governance T011-087 Manual Report

Status: passed for isolated Spec 011 governance metadata scope.

Task: `T011-087 - Add review metadata for prompt/policy/template/product-knowledge changes`.

## Scope

This task added a control-plane metadata contract and validator for future
prompt, policy, template, and product-knowledge changes. It does not change
runtime prompts, template wording, product facts, routing, adapters, Sales Inbox
UI, `/pilates`, database persistence, delivery, or `runtime/runner.py`.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_governance_metadata.py -q
```

Observed before implementation:

```text
ModuleNotFoundError: No module named 'app.core.taliya_commercial.governance'
```

This confirmed there was no governance metadata validator.

## Implemented Checks

- `validate_governance_metadata` accepts complete review metadata.
- Missing reason, transcript diff, before/after eval reference, or required
  approval evidence blocks the change metadata.
- Product facts are allowed only from official product knowledge or Spec 006
  product contracts.
- Added `governance-metadata-contract.md` documenting the required fields and
  scope boundary.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_governance_metadata.py -q
```

Result: `3 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_governance_metadata.py tests/test_spec011_template_registry.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_validators_product_claims.py tests/test_spec011_trace_export.py -q
```

Result: `19 passed`.

Broad isolated Spec 011 core/conductor/validator/repair/fallback/policy/product/failed-path/renderer/trace/runtime-state/projection/export/governance suite:

```powershell
python -m pytest tests/test_spec011_governance_metadata.py tests/test_spec011_trace_export.py tests/test_spec011_feedback_loop_prevention.py tests/test_spec011_sales_inbox_projection_completeness.py tests/test_spec011_sales_inbox_identity_projection.py tests/test_spec011_sales_inbox_projection_builder.py tests/test_spec011_runtime_state_diff.py tests/test_spec011_trace_store.py tests/test_spec011_renderer_channel_rules.py tests/test_spec011_renderer_final_diagnostic.py tests/test_spec011_renderer_variable_contract.py tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_failed_path_guards.py tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `275 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/governance.py tests/test_spec011_governance_metadata.py
rg -n "runtime\.runner|request\.message|inbound\.text|context\.inbound\.text|^import re\b|^from re\b|regex|\.search\(|\.match\(|isdigit|render_validated|render_template\(|get_template\(|ConductorProvider|openai|send\(|WhatsApp|SalesInboxClient|/pilates|497|120|R\$|checkout|desconto|vip|data de abertura|openai_demo|demo_video|video_production" app/core/taliya_commercial/governance.py
```

Result: Ruff passed. Static `rg` returned no matches.

## Anti-Drift Review

- Governance is metadata validation only.
- Product facts cannot move into prompts/templates/policies through this contract.
- No runtime behavior changed.

Next task: `T011-088 - Add CI/static audit to block product facts in prompts/templates/tests/fallbacks when they belong in official product knowledge or Spec 006`.
