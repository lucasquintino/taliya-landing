# Fallback T011-068 Manual Report

Status: passed for isolated Spec 011 core fallback/handoff disposition scope.

Task: `T011-068 - Implement safe fallback/handoff after failed repair`.

## Scope

This task added a safe failure disposition boundary. It does not render messages,
persist traces, deliver output, answer commercial questions, change `/pilates`,
cut over widget/WhatsApp adapters, or touch `runtime/runner.py`.

Fallback is represented as structured state only. It may select an approved
fallback/handoff template id for a later renderer, but it cannot carry
customer-facing free-form text.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_safe_fallback.py -q
```

Observed before implementation:

```text
ModuleNotFoundError: No module named 'app.core.taliya_commercial.fallback'
```

This confirmed the fallback/handoff disposition boundary did not exist.

## Implemented Checks

- Accepted decisions return `SafeFallbackResult(status=not_needed)`.
- Blocked validator results request handoff with `handoff.acknowledge`, no
  customer-facing text, and `ai_pause_required = true`.
- Failed repair results request handoff and preserve validator/repair status.
- Provider timeout uses only `fallback.provider_timeout`.
- Invalid provider output uses only `fallback.invalid_json`.
- Safe fallback templates must exist in the approved template registry.
- `commercial_answer_allowed` must remain false.
- Extra fields such as `message_text` are rejected by the strict schema.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_safe_fallback.py -q
```

Result: `6 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_template_registry.py tests/test_spec011_schema_versioning.py tests/test_spec011_core_schemas.py -q
```

Result: `70 passed`.

Broad isolated Spec 011 core/conductor/validator/repair/fallback suite:

```powershell
python -m pytest tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `203 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/fallback.py tests/test_spec011_safe_fallback.py app/core/taliya_commercial/repair.py tests/test_spec011_repair_loop.py
git diff --check -- services/taliya-agent-runtime/app/core/taliya_commercial/fallback.py services/taliya-agent-runtime/tests/test_spec011_safe_fallback.py
```

Result: Ruff passed and diff whitespace check passed.

Targeted static review found no matches for inbound text parsing, regex
import/use, hardcoded official price literals, active render/delivery/persist
calls, runtime calls, or fallback-message construction in the fallback path.

## Anti-Drift Review

- Fallback is operational state, not deterministic commercial answering.
- Only approved `fallback.*` or `handoff.acknowledge` template ids are selected.
- No free-form customer-facing message field exists.
- The proof is isolated-core proof, not renderer, adapter, persistence, or
  production cutover proof.

Next task: `T011-069 - Add corroboration checks for conductor self-checks`.
