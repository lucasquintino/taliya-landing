# Renderer T011-074 Channel Rules Manual Report

Status: passed for isolated Spec 011 core renderer channel-rule scope.

Task: `T011-074 - Preserve WhatsApp no-button/link/chunk rules`.

## Scope

This task added typed channel shaping at the Spec 011 core renderer boundary. It
does not send messages, create adapter-specific buttons, persist traces, parse
inbound text, choose commercial routes, repair decisions, change `/pilates`, cut
over adapters, import the legacy renderer, or touch `runtime/runner.py`.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_renderer_channel_rules.py -q
```

Observed before implementation:

```text
1 failed, 3 passed
```

The failing case showed explicit `whatsapp_max_3` did not cap normal WhatsApp
output to three messages.

## Implemented Checks

- WhatsApp output remains typed `RenderedMessage` text only.
- The core renderer emits no `kind`, `button`, or adapter-action fields.
- `whatsapp_max_3` caps normal WhatsApp output to three messages.
- Widget output is not capped by the WhatsApp policy.
- `staged_diagnostic` is not truncated for WhatsApp.
- Official demo links render as plain text from validated variables on both
  widget and WhatsApp.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_renderer_channel_rules.py -q
```

Result: `4 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_renderer_channel_rules.py tests/test_spec011_renderer_final_diagnostic.py tests/test_spec011_renderer_variable_contract.py tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_template_registry.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_core_schemas.py -q
```

Result: `57 passed`.

Broad isolated Spec 011 core/conductor/validator/repair/fallback/policy/product/failed-path/renderer/channel suite:

```powershell
python -m pytest tests/test_spec011_renderer_channel_rules.py tests/test_spec011_renderer_final_diagnostic.py tests/test_spec011_renderer_variable_contract.py tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_failed_path_guards.py tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `243 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/renderer.py tests/test_spec011_renderer_channel_rules.py tests/test_spec011_renderer_final_diagnostic.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_variable_contract.py
rg -n "497|120|R\$|checkout|desconto|vip|data de abertura|app\.domains|runtime\.runner|AgentRunRequest|request|inbound|^import re\b|^from re\b|regex|\.search\(|\.match\(|isdigit|render_template\(|get_template\(|processo atual|essa integracao|demo_contextual_next_step|gargalo principal|Para plano|Isso faz sentido|send\(|deliver\(|Outbox|button|buttons|kind" app/core/taliya_commercial/renderer.py
```

Result: Ruff passed. Static `rg` returned no matches in the renderer.

## Anti-Drift Review

- Channel shaping remains renderer output shaping only; no delivery or adapter
  behavior was implemented.
- WhatsApp does not receive buttons/action fields from the core renderer.
- Links are rendered only from validated variables.
- Staged diagnostics are not cut by normal WhatsApp caps.
- Phase 7 is closed for isolated-core proof only. Persistence, adapters, and
  production cutover remain later phases.

Next task: `T011-080 - Persist mandatory turn trace artifacts`.
