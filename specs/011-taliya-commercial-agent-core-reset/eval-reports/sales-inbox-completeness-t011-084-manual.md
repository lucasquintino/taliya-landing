# Sales Inbox Completeness T011-084 Manual Report

Status: passed for isolated Spec 011 projection completeness scope.

Task: `T011-084 - Verify completed diagnostic, waitlist, demo, handoff, and product follow-up projection completeness`.

## Scope

This task added projection-completeness coverage for the main commercial case
families. It does not parse inbound text, read rendered output, choose
commercial meaning, invent product/payment/waitlist promises, send messages,
change Sales Inbox UI, change `/pilates`, change adapters, or touch
`runtime/runner.py`.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_sales_inbox_projection_completeness.py -q
```

Observed before implementation:

```text
KeyError: 'demo_customer_facing_concept'
KeyError: 'waitlist_eligibility'
```

This confirmed generated projections were valid for some cases but incomplete
for demo follow-up and waitlist state visibility.

## Implemented Checks

- Completed diagnostic projection includes complete ledger marker, all required
  diagnostic keys, final plan/range, final demo line, and validator acceptance.
- Demo/product-demo projection includes `demo_customer_facing_concept`,
  `demo_status`, and `demo_next_step`, while excluding technical/video demo
  fields.
- Waitlist projections distinguish offered, pending-details, joined, and
  declined states.
- Waitlist joined uses event idempotency key and joined timestamp.
- Waitlist fields do not introduce checkout, VIP, or opening-date promise text.
- Product follow-up projection keeps commercial stage, selected template ids,
  source labels, and operator next action.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_sales_inbox_projection_completeness.py -q
```

Result: `4 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_sales_inbox_projection_completeness.py tests/test_spec011_sales_inbox_projection_builder.py tests/test_spec011_sales_inbox_identity_projection.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_runtime_state_diff.py tests/test_spec011_validators_waitlist_demo_handoff.py -q
```

Result: `38 passed`.

Broad isolated Spec 011 core/conductor/validator/repair/fallback/policy/product/failed-path/renderer/trace/runtime-state/projection/completeness suite:

```powershell
python -m pytest tests/test_spec011_sales_inbox_projection_completeness.py tests/test_spec011_sales_inbox_identity_projection.py tests/test_spec011_sales_inbox_projection_builder.py tests/test_spec011_runtime_state_diff.py tests/test_spec011_trace_store.py tests/test_spec011_renderer_channel_rules.py tests/test_spec011_renderer_final_diagnostic.py tests/test_spec011_renderer_variable_contract.py tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_failed_path_guards.py tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `268 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/sales_inbox_projection.py tests/test_spec011_sales_inbox_projection_completeness.py tests/test_spec011_sales_inbox_identity_projection.py tests/test_spec011_sales_inbox_projection_builder.py
rg -n "app\.domains|runtime\.runner|AgentRunRequest|request\.message|inbound\.text|context\.inbound\.text|^import re\b|^from re\b|regex|\.search\(|\.match\(|isdigit|render_validated|render_template\(|get_template\(|ConductorProvider|openai|send\(|WhatsApp|SalesInboxClient|/pilates|497|120|R\$|checkout|desconto|vip|data de abertura|openai_demo|demo_video|video_production" app/core/taliya_commercial/sales_inbox_projection.py
```

Result: Ruff passed. Static `rg` returned no matches.

## Anti-Drift Review

- Projection completeness is derived from structured state/events, never from
  rendered messages or inbound text.
- Demo remains the customer-facing commercial product demo concept only.
- Waitlist projection exposes status and operational fields without payment or
  availability promises.
- This remains isolated-core proof. Adapter, database, trace export, and
  production evidence remain later phases.

Next task: `T011-085 - Prevent adapter/Sales Inbox inferred facts from re-entering conductor context as reliable facts without source/confidence labels`.
