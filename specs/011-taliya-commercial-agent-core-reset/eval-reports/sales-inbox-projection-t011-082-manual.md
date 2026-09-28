# Sales Inbox Projection T011-082 Manual Report

Status: passed for isolated Spec 011 core Sales Inbox projection scope.

Task: `T011-082 - Build Sales Inbox projection from runtime state/events`.

## Scope

This task added an isolated Sales Inbox projection builder. It builds
`SalesInboxProjection` from validated runtime-state diff, typed context/source
labels, and delivery/runtime events. It does not parse inbound text, read
rendered customer copy as source of truth, choose commercial routes, render,
send, call OpenAI, persist to the database, change Sales Inbox UI, change
`/pilates`, change adapters, or touch `runtime/runner.py`.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_sales_inbox_projection_builder.py -q
```

Observed before implementation:

```text
ModuleNotFoundError: No module named 'app.core.taliya_commercial.sales_inbox_projection'
```

This confirmed the Sales Inbox projection builder did not exist.

## Implemented Checks

- `build_sales_inbox_projection` requires a runtime-state diff with schema
  `011.runtime_state_diff.v1` and source `accepted_decision|repaired_decision`.
- Projection source ids must match context, decision, validator result, agent,
  turn, conversation, and channel.
- Projection includes conversation id, lead id, commercial stage, summary,
  diagnostic/waitlist/handoff status, identity labels, template ids, validator
  status/disposition, source labels, and operator next action.
- Completed diagnostic projection includes ledger completeness marker, required
  diagnostic keys, demo status, final plan/range, and final demo line.
- Waitlist joined projection requires event-sourced idempotency key and joined
  timestamp.
- Handoff requested/active projection includes reason plus `human_active` and
  `ai_paused`.
- Identity/contact projection preserves `customer_provided`,
  `operator_provided`, `channel_provided`, `inferred`, and `unverified` labels;
  only customer/operator-provided values are marked verified.
- The builder validates the generated projection with
  `validate_sales_inbox_projection` before returning it.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_sales_inbox_projection_builder.py -q
```

Result: `5 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_sales_inbox_projection_builder.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_runtime_state_diff.py tests/test_spec011_trace_store.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_context_builder.py -q
```

Result: `36 passed`.

Broad isolated Spec 011 core/conductor/validator/repair/fallback/policy/product/failed-path/renderer/trace/runtime-state/projection suite:

```powershell
python -m pytest tests/test_spec011_sales_inbox_projection_builder.py tests/test_spec011_runtime_state_diff.py tests/test_spec011_trace_store.py tests/test_spec011_renderer_channel_rules.py tests/test_spec011_renderer_final_diagnostic.py tests/test_spec011_renderer_variable_contract.py tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_failed_path_guards.py tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `263 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/sales_inbox_projection.py tests/test_spec011_sales_inbox_projection_builder.py app/core/taliya_commercial/runtime_state.py tests/test_spec011_runtime_state_diff.py
rg -n "app\.domains|runtime\.runner|AgentRunRequest|request\.message|inbound\.text|context\.inbound\.text|^import re\b|^from re\b|regex|\.search\(|\.match\(|isdigit|render_validated|render_template\(|get_template\(|ConductorProvider|openai|send\(|WhatsApp|SalesInboxClient|/pilates|497|120|R\$|checkout|desconto|vip|data de abertura" app/core/taliya_commercial/sales_inbox_projection.py app/core/taliya_commercial/runtime_state.py
```

Result: Ruff passed. Static `rg` returned no matches.

## Anti-Drift Review

- Sales Inbox is now a projection of validated state/events for the isolated
  core, not a second interpretation layer.
- The builder refuses mismatched decision/state/validator ids and failed/fallback
  state sources.
- Projection quality is checked by the existing Sales Inbox validator before the
  projection is returned.
- This is isolated-core proof only. Database persistence, adapter cutover,
  production traces, full eval exports, and Sales Inbox UI integration remain
  later phases.

Next task: `T011-083 - Distinguish customer-provided, channel-provided, operator-provided, inferred, and unverified identity/contact values`.
