# Renderer T011-072 Variable Contract Manual Report

Status: passed for isolated Spec 011 core renderer variable-contract scope.

Task: `T011-072 - Validate required variables before rendering`.

## Scope

This task added renderer-body contract validation. It does not parse inbound
text, choose commercial routes, answer product questions, repair decisions,
persist traces, deliver output, change `/pilates`, cut over adapters, import the
legacy renderer, or touch `runtime/runner.py`.

The renderer now audits approved body placeholders against the Spec 011 template
registry and variable registry before rendering text.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_renderer_variable_contract.py -q
```

Observed before implementation:

```text
ImportError: cannot import name 'validate_renderer_template_bodies'
```

This confirmed the renderer had no reusable body/placeholder contract audit.

## Implemented Checks

- Approved renderer body contract must be clean.
- Unknown template body ids are rejected.
- Unknown placeholder variables are rejected.
- Placeholders not declared by the body line are rejected.
- Declared body variables that are not used in the line are rejected.
- Body variables not allowed by the template registry are rejected.
- Required template variables cannot appear only on optional lines.
- Required template variables must be rendered by at least one non-optional line.
- The renderer checks body-contract errors before producing `RenderedMessage`.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_renderer_variable_contract.py -q
```

Result: `5 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_renderer_variable_contract.py tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_template_registry.py tests/test_spec011_validators_core.py tests/test_spec011_validators_product_claims.py tests/test_spec011_failed_path_guards.py tests/test_spec011_safe_fallback.py tests/test_spec011_core_schemas.py -q
```

Result: `59 passed`.

Broad isolated Spec 011 core/conductor/validator/repair/fallback/policy/product/failed-path/renderer/no-default/variable-contract suite:

```powershell
python -m pytest tests/test_spec011_renderer_variable_contract.py tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_failed_path_guards.py tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `237 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/renderer.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_variable_contract.py
rg -n "497|120|R\$|checkout|desconto|vip|data de abertura|app\.domains|runtime\.runner|AgentRunRequest|request|inbound|import re|regex|\.search\(|\.match\(|isdigit|render_template\(|get_template\(|processo atual|essa integracao|demo_contextual_next_step" app/core/taliya_commercial/renderer.py tests/test_spec011_renderer_variable_contract.py
```

Result: Ruff passed. Static `rg` returned no matches.

## Anti-Drift Review

- The renderer body audit uses template/body structure only and does not inspect
  lead text.
- Missing variables fail before rendering; they are not supplied by renderer
  defaults.
- Approved body placeholders must remain registered and template-allowed.
- This is isolated-core proof only. Final diagnostic staged rendering, WhatsApp
  chunk/link rules, persistence, adapters, and production cutover remain later
  phases.

Next task: `T011-073 - Preserve final diagnostic staged order and complete final sentence`.
