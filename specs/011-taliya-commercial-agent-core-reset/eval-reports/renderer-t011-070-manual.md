# Renderer T011-070 Manual Report

Status: passed for isolated Spec 011 core renderer boundary scope.

Task: `T011-070 - Refactor renderer to accept only validated template plans`.

## Scope

This task added the isolated core renderer boundary. It does not parse inbound
text, choose commercial routes, answer product questions, repair decisions,
persist traces, deliver output, change `/pilates`, cut over adapters, import the
legacy renderer, or touch `runtime/runner.py`.

The renderer accepts a `RenderPlan` plus a passed/repaired `ValidatorResult` and
returns typed `RenderedMessage` objects. It renders approved template bodies from
provided variables only.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_renderer_validated_plan.py -q
```

Observed before implementation:

```text
ModuleNotFoundError: No module named 'app.core.taliya_commercial.renderer'
```

This confirmed the Spec 011 core renderer boundary did not exist.

## Implemented Checks

- Rendering requires `RenderPlan`.
- Rendering requires `ValidatorResult(status=passed)` with
  `final_disposition=accepted` or `final_disposition=repaired`.
- Repairable, blocked, failed, fallback-only, or empty render plans are rejected
  before text is produced.
- Template items are rechecked against the Spec 011 template registry before
  rendering.
- Channel mismatches are rejected before rendering.
- Missing semantic variables are rejected instead of filled with defaults.
- Unknown template ids or missing approved template bodies are rejected instead
  of falling back to generic copy.
- Rendered output is `RenderedMessage` only: text, template id, channel, and
  sequence.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_renderer_validated_plan.py -q
```

Result: `9 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_renderer_validated_plan.py tests/test_spec011_template_registry.py tests/test_spec011_validators_core.py tests/test_spec011_validators_product_claims.py tests/test_spec011_failed_path_guards.py tests/test_spec011_safe_fallback.py tests/test_spec011_core_schemas.py -q
```

Result: `50 passed`.

Broad isolated Spec 011 core/conductor/validator/repair/fallback/policy/product/failed-path/renderer suite:

```powershell
python -m pytest tests/test_spec011_renderer_validated_plan.py tests/test_spec011_failed_path_guards.py tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `228 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/renderer.py tests/test_spec011_renderer_validated_plan.py
rg -n "497|120|R\$|checkout|desconto|vip|data de abertura|app\.domains|runtime\.runner|AgentRunRequest|request|inbound|import re|regex|\.search\(|\.match\(|isdigit|render_template\(|get_template\(" app/core/taliya_commercial/renderer.py
```

Result: Ruff passed. Static `rg` returned no matches.

## Anti-Drift Review

- The renderer is not a conversation brain. It requires an already validated
  plan and does not inspect context or inbound text.
- The renderer does not import the legacy domain renderer or template defaults.
- Product facts and links must arrive as validated variables; the renderer does
  not invent them.
- This is isolated-core proof only. Full no-default coverage, diagnostic final
  rendering, WhatsApp chunk/link rules, persistence, adapters, and production
  cutover remain later phases.

Next task: `T011-071 - Remove semantic defaults from rendering`.
