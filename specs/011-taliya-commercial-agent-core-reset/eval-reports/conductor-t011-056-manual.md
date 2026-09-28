# Conductor T011-056 Manual Validation

Date: 2026-05-30

Task: T011-056 - Prohibit generic whole-response fields in conductor output.

Scope: isolated Spec 011 core/conductor boundary only. No public runtime cutover, no renderer implementation, no `/pilates` changes, no `runner.py` commercial changes, no Sales Inbox UI changes.

## Contract Checked

- Provider envelopes must not include top-level `message_text`, `freeform_response`, `assistant_reply`, `assistant_message`, `response_text`, or `full_response`.
- Decision payloads must not include those fields, even when the rest of the decision and `template_plan` are valid.
- Template variables must not use those names.
- Rejection must happen without deterministic customer-facing fallback copy.
- Provider request instructions must explicitly tell the LLM/provider not to return customer-facing free-form assistant text or generic whole-response fields.

## Red Baseline

Command:

```powershell
python -m pytest tests/test_spec011_conductor_whole_response_fields.py -q
```

Result before implementation: 19 failed.

Observed failure reason:

- Pydantic rejected some extra fields indirectly, but the raised conductor error was generic and did not expose the forbidden field name.
- The provider request did not list the exact forbidden whole-response field names.

## Implementation

- Added an explicit conductor-boundary check before `ConductorTurnResult` validation.
- The check inspects only structural output locations: provider envelope, direct decision payload keys, and `template_plan.items[].variables`.
- Rejections raise `ConductorDecisionValidationError` with the exact forbidden field path.
- Provider instructions and provider requirements now list all forbidden whole-response field names.

This is validation-only determinism. It does not inspect inbound message text, choose route/intent/template, render customer-facing copy, or provide a deterministic commercial fallback.

## Validation

Focused test:

```powershell
python -m pytest tests/test_spec011_conductor_whole_response_fields.py -q
```

Result: 19 passed.

Isolated Spec 011 core/conductor suite:

```powershell
python -m pytest tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: 135 passed.

Ruff:

```powershell
python -m ruff check app/core/taliya_commercial tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_core_schemas.py tests/test_spec011_template_registry.py tests/test_spec011_schema_versioning.py
```

Result: all checks passed.

Static review:

```powershell
rg "request\.message\.text|inbound\.text|\bre\.|regex|isdigit|normalized|497|897|1497" app\core\taliya_commercial\conductor.py app\core\taliya_commercial\conductor_policy.py app\core\taliya_commercial\schemas.py app\core\taliya_commercial\template_registry.py app\core\taliya_commercial\schema_versioning.py
rg "fallback copy|customer-facing fallback|hardcoded reply|deterministic reply|safe answer" app\core\taliya_commercial\conductor.py app\core\taliya_commercial\schemas.py app\core\taliya_commercial\template_registry.py tests\test_spec011_conductor_whole_response_fields.py
```

Result: no matches.

## Review

- LLM-first preserved: no commercial meaning moved into code.
- Deterministic code remained a structural validation guardrail.
- The proof is isolated-core proof only. Renderer, validators, adapters, persistence, real-provider evals, and production trace export remain later tasks.
