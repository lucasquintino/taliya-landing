# Renderer T011-071 No Defaults Manual Report

Status: passed for isolated Spec 011 core renderer no-default scope.

Task: `T011-071 - Remove semantic defaults from rendering`.

## Scope

This task added no-semantic-default coverage for the Spec 011 core renderer. It
does not parse inbound text, choose commercial routes, answer product questions,
repair decisions, persist traces, deliver output, change `/pilates`, cut over
adapters, import the legacy renderer, or touch `runtime/runner.py`.

The renderer may omit an optional line only when that line is explicitly marked
optional. It must not supply default product facts, demo links, plan-fit context,
current-tool labels, integration topics, diagnostic reflections, or next-step
copy.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_renderer_no_semantic_defaults.py -q
```

Observed before implementation:

```text
4 failed
```

Failures showed that the renderer did not yet have approved core bodies for the
tested templates, so it could not prove variable-specific no-default behavior.

## Implemented Checks

- `product.plan_fit_with_diagnostic` requires provided `plan_fit_context`.
- `product.comparison_current_tool` requires provided `current_tool_context`.
- `product.integration_scope_direct` requires provided `integration_topic`.
- Missing required semantic variables fail before rendering.
- Provided variable values are rendered as supplied.
- Old defaults such as `o processo atual`, `essa integracao`, and
  `demo_contextual_next_step` are not present in the core renderer.
- `diagnostic.ask_priority` can omit optional `answer_feedback` without replacing
  it with generic feedback, and renders feedback only when provided.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_renderer_no_semantic_defaults.py -q
```

Result: `4 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_template_registry.py tests/test_spec011_validators_core.py tests/test_spec011_validators_product_claims.py tests/test_spec011_failed_path_guards.py tests/test_spec011_safe_fallback.py tests/test_spec011_core_schemas.py -q
```

Result: `54 passed`.

Broad isolated Spec 011 core/conductor/validator/repair/fallback/policy/product/failed-path/renderer/no-default suite:

```powershell
python -m pytest tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_failed_path_guards.py tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `232 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/renderer.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_renderer_no_semantic_defaults.py
rg -n "497|120|R\$|checkout|desconto|vip|data de abertura|app\.domains|runtime\.runner|AgentRunRequest|request|inbound|import re|regex|\.search\(|\.match\(|isdigit|render_template\(|get_template\(|processo atual|essa integracao|demo_contextual_next_step" app/core/taliya_commercial/renderer.py
```

Result: Ruff passed. Static `rg` returned no matches.

## Anti-Drift Review

- The renderer still requires an already validated plan and does not inspect
  inbound text or context.
- Missing semantic variables fail instead of being filled by deterministic
  commercial copy.
- Optional diagnostic feedback is omitted, not invented.
- This is isolated-core proof only. Full variable-body audit, diagnostic final
  rendering, WhatsApp chunk/link rules, persistence, adapters, and production
  cutover remain later phases.

Next task: `T011-072 - Validate required variables before rendering`.
