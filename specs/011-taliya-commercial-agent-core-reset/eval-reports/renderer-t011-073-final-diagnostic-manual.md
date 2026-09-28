# Renderer T011-073 Final Diagnostic Manual Report

Status: passed for isolated Spec 011 core renderer final-diagnostic scope.

Task: `T011-073 - Preserve final diagnostic staged order and complete final sentence`.

## Scope

This task added completed-diagnostic renderer bodies and final-sentence
regression coverage. It does not parse inbound text, choose commercial routes,
select agents/plans/demo state, repair decisions, persist traces, deliver output,
change `/pilates`, cut over adapters, import the legacy renderer, or touch
`runtime/runner.py`.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_renderer_final_diagnostic.py -q
```

Observed before implementation:

```text
2 failed
```

Failures showed completed diagnostic template bodies were not approved in the
Spec 011 core renderer yet. A second red pass caught final-sentence casing and
termination after `demo_status` was mapped into customer text.

## Implemented Checks

- Completed diagnostic stages render in this order: hold, context, base/routine
  recommendation, operational first step, agent recommendation(s), plan
  recommendation, demo/next-step sentence.
- Repeated `diagnostic.deliver_agent_recommendation` items render with their own
  item variables.
- `demo_status` is rendered from the provided enum value through approved labels.
- `diagnostic.deliver_demo_not_offered` preserves the complete final sentence.
- `diagnostic.deliver_demo_already_offered` preserves the complete final
  question.
- Staged diagnostics are not truncated by a generic three-message cap.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_renderer_final_diagnostic.py -q
```

Result: `2 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_renderer_final_diagnostic.py tests/test_spec011_renderer_variable_contract.py tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_template_registry.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_core_schemas.py -q
```

Result: `53 passed`.

Broad isolated Spec 011 core/conductor/validator/repair/fallback/policy/product/failed-path/renderer/final-diagnostic suite:

```powershell
python -m pytest tests/test_spec011_renderer_final_diagnostic.py tests/test_spec011_renderer_variable_contract.py tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_failed_path_guards.py tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `239 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/renderer.py tests/test_spec011_renderer_final_diagnostic.py tests/test_spec011_renderer_validated_plan.py tests/test_spec011_renderer_no_semantic_defaults.py tests/test_spec011_renderer_variable_contract.py
rg -n "497|120|R\$|checkout|desconto|vip|data de abertura|app\.domains|runtime\.runner|AgentRunRequest|request|inbound|^import re\b|^from re\b|regex|\.search\(|\.match\(|isdigit|render_template\(|get_template\(|processo atual|essa integracao|demo_contextual_next_step|gargalo principal|Para plano|Isso faz sentido" app/core/taliya_commercial/renderer.py tests/test_spec011_renderer_final_diagnostic.py
```

Result: Ruff passed. Static `rg` returned no matches.

## Anti-Drift Review

- The renderer preserves the staged plan selected by the LLM/validators; it does
  not choose diagnostic content.
- Final diagnostic rendering uses provided variables and enum labels only.
- The final demo/next-step sentence is complete and not capped by normal
  WhatsApp limits.
- This is isolated-core proof only. WhatsApp no-button/link/chunk rules,
  persistence, adapters, and production cutover remain later phases.

Next task: `T011-074 - Preserve WhatsApp no-button/link/chunk rules`.
