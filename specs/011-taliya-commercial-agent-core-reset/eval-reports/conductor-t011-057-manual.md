# Conductor T011-057 Manual Validation

Date: 2026-05-30

Task: T011-057 - Enforce studio-owner language defaults and avoid technical CRM phrasing unless allowed by spec.

Scope: isolated Spec 011 core/conductor boundary only. No public runtime cutover, no renderer copy, no final diagnostic wording rewrite, no `/pilates` changes, no `runner.py` commercial changes, and no Sales Inbox UI changes.

## Contract Checked

- The conductor request and specialist policy pack instruct the LLM to use practical studio-owner language by default.
- Preferred language terms are explicit: `sistema`, `rotina`, `base organizada`, `atendimento`, `agenda`, `vendas`, `alunos`, `turmas`, and `proximos passos`.
- `CRM` is not the default customer-facing label.
- `CRM` can be used only when the structured decision declares `language_policy.crm_term_policy = allowed_with_evidence` and provides at least one allowed reason and evidence.
- Allowed CRM reasons are `lead_used_or_asked_crm`, `approved_template_requires_crm`, and `category_name_needed`.
- The language policy remains stable across different inbound texts. Code does not parse inbound text to decide whether CRM is allowed.

## Red Baseline

Command:

```powershell
python -m pytest tests/test_spec011_conductor_language_policy.py -q
```

Result before implementation: 5 failed, 1 passed.

Observed failure reason:

- `language_policy` was not part of `ConductorDecision`.
- Decisions without language policy still passed.
- Decisions carrying a valid language policy were rejected as unknown extra fields.
- Provider instructions and specialist policy did not contain the studio-owner language rule or exact CRM allowance reasons.

## Implementation

- Added required `language_policy` to the conductor decision schema.
- The external JSON keeps `language_policy.register`; the Python model uses `language_register` internally to avoid Pydantic method shadowing.
- Added schema validation for CRM allowance: `allowed_with_evidence` requires at least one allowed reason and non-empty evidence; `avoid_by_default` rejects CRM reasons/evidence.
- Added practical language and CRM allowance instructions to the conductor provider request.
- Added the same language rule to the specialist policy pack global rules.
- Updated valid mocked conductor fixtures to include `language_policy`.
- Updated the reviewed conductor schema fingerprint and schema-versioning note.

This is policy/boundary determinism. It does not inspect inbound message text, choose route/intent/template, render customer-facing copy, or provide deterministic commercial fallback.

## Validation

Focused test:

```powershell
python -m pytest tests/test_spec011_conductor_language_policy.py -q
```

Result: 6 passed.

Isolated Spec 011 core/conductor suite:

```powershell
python -m pytest tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: 141 passed.

Ruff:

```powershell
python -m ruff check app/core/taliya_commercial tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_core_schemas.py tests/test_spec011_template_registry.py tests/test_spec011_schema_versioning.py
```

Result: all checks passed.

Static review:

```powershell
rg "request\.message\.text|inbound\.text|\bre\.|regex|isdigit|normalized|497|897|1497" app\core\taliya_commercial\conductor.py app\core\taliya_commercial\conductor_policy.py app\core\taliya_commercial\schemas.py app\core\taliya_commercial\template_registry.py app\core\taliya_commercial\schema_versioning.py
rg "if user says|when the message|keyword|hardcoded reply|fallback copy|customer-facing fallback|deterministic reply|safe answer" app\core\taliya_commercial\conductor.py app\core\taliya_commercial\conductor_policy.py app\core\taliya_commercial\schemas.py tests\test_spec011_conductor_language_policy.py
```

Result: no matches.

## Review

- LLM-first preserved: the LLM still owns commercial understanding and decides the structured language policy.
- Deterministic code remained limited to schema/policy validation.
- No product facts were added to prompts/templates/fallbacks.
- The proof is isolated-core proof only. Renderer text quality, final diagnostic transcript review, real-model evals, adapter cutover, and production monitoring remain later tasks.
