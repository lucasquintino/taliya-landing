# Sales Inbox Identity T011-083 Manual Report

Status: passed for isolated Spec 011 identity/contact projection scope.

Task: `T011-083 - Distinguish customer-provided, channel-provided, operator-provided, inferred, and unverified identity/contact values`.

## Scope

This task hardened identity/contact projection inside the isolated Sales Inbox
projection builder. It does not parse inbound text, infer identity from adapter
payloads, update runtime state, send messages, change Sales Inbox UI, change
`/pilates`, change adapters, or touch `runtime/runner.py`.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_sales_inbox_identity_projection.py -q
```

Observed before implementation:

```text
AssertionError: assert 'channel_provided' == 'customer_provided'
```

This confirmed a validated customer-provided runtime fact could fail to replace
a weaker channel-provided identity projection.

## Implemented Checks

- Identity/contact projection now merges context facts with validated
  runtime-state `fact_updates`.
- Exact duplicate key/value pairs use a deterministic reliability rank:
  `operator_provided`, `customer_provided`, `channel_provided`, `inferred`,
  `unverified`.
- Customer-provided and operator-provided identity/contact values are verified.
- Channel-provided, inferred, and unverified values are never verified.
- Facts sourced from `sales_inbox_projection` remain inferred/unverified and are
  not promoted back into customer/operator-provided identity.
- Projection still returns typed `IdentityField` objects and passes
  `validate_sales_inbox_projection`.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_sales_inbox_identity_projection.py -q
```

Result: `1 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_sales_inbox_identity_projection.py tests/test_spec011_sales_inbox_projection_builder.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_runtime_state_diff.py tests/test_spec011_context_builder.py -q
```

Result: `32 passed`.

Broad isolated Spec 011 core/conductor/validator/repair/fallback/policy/product/failed-path/renderer/trace/runtime-state/projection/identity suite:

```powershell
python -m pytest tests/test_spec011_sales_inbox_identity_projection.py tests/test_spec011_sales_inbox_projection_builder.py tests/test_spec011_runtime_state_diff.py tests/test_spec011_trace_store.py tests/test_spec011_renderer_channel_rules.py tests/test_spec011_renderer_final_diagnostic.py tests/test_spec011_renderer_variable_contract.py tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_failed_path_guards.py tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `264 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/sales_inbox_projection.py tests/test_spec011_sales_inbox_identity_projection.py tests/test_spec011_sales_inbox_projection_builder.py
rg -n "app\.domains|runtime\.runner|AgentRunRequest|request\.message|inbound\.text|context\.inbound\.text|^import re\b|^from re\b|regex|\.search\(|\.match\(|isdigit|render_validated|render_template\(|get_template\(|ConductorProvider|openai|send\(|WhatsApp|SalesInboxClient|/pilates|497|120|R\$|checkout|desconto|vip|data de abertura" app/core/taliya_commercial/sales_inbox_projection.py
```

Result: Ruff passed. Static `rg` returned no matches.

## Anti-Drift Review

- Identity/contact reliability is now carried as structured labels, not inferred
  from text.
- A weaker channel/projection value cannot overwrite a stronger customer or
  operator-confirmed value.
- Sales Inbox projection remains a projection layer and cannot promote its own
  prior inferred values into reliable facts.

Next task: `T011-084 - Verify completed diagnostic, waitlist, demo, handoff, and product follow-up projection completeness`.
