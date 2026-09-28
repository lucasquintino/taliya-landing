# Validators T011-060 Manual Validation

Date: 2026-05-30

Task: T011-060 - Implement schema/state/template/channel validators.

Scope: isolated Spec 011 core validator layer only. No public runtime cutover, no renderer, no persistence, no repair loop, no customer-facing fallback text, no `/pilates` changes, no `runner.py` commercial changes, and no Sales Inbox UI changes.

## Contract Checked

- Validator accepts either a typed `ConductorTurnResult` or a typed `ConductorDecision` plus `TurnContext`.
- Validator returns `ValidatorResult` with typed `ValidationIssue` entries.
- Schema/version checks use the existing schema-versioning contract and report unsupported versions as structured issues instead of generic exceptions.
- Context/state checks catch context identity mismatch, non-empty state requirements, and prior-state mismatch when context carries an explicit state hint.
- Template checks reuse the existing template registry validation and preserve missing/unknown/forbidden variable protections.
- Channel checks catch template item channel mismatch against the turn context.
- Validation failure does not render, repair, persist, deliver, or produce customer-facing fallback copy.

## Red Baseline

Command:

```powershell
python -m pytest tests/test_spec011_validators_core.py -q
```

Result before implementation: collection failed because `app.core.taliya_commercial.validators` did not exist.

## Implementation

- Added `app/core/taliya_commercial/validators.py`.
- Added `validate_conductor_result(...)`.
- Validation areas implemented:
  - schema fingerprint and schema version;
  - context identity fields: `turn_id`, `conversation_id`, `agent_key`, and `channel`;
  - structural state fields and optional compact-memory state hint;
  - template plan presence and template registry errors;
  - template item channel matching.
- Status mapping:
  - no errors => `passed` and `final_disposition = accepted`;
  - any `P0` issue => `blocked` and `final_disposition = blocked`;
  - only non-P0 errors => `repairable`, with no final disposition.

This is validation-only determinism. It does not inspect inbound text, route commercial intent, check product facts/prices/student counts, check diagnostic/waitlist/demo business rules, repair decisions, render copy, or create fallback text.

## Validation

Focused test:

```powershell
python -m pytest tests/test_spec011_validators_core.py -q
```

Result: 8 passed.

Nearby schema/template/core validation:

```powershell
python -m pytest tests/test_spec011_validators_core.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py -q
```

Result: 20 passed.

Isolated Spec 011 core/conductor/validator suite:

```powershell
python -m pytest tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: 153 passed.

Ruff:

```powershell
python -m ruff check app/core/taliya_commercial tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_core_schemas.py tests/test_spec011_template_registry.py tests/test_spec011_schema_versioning.py
```

Result: all checks passed.

Static review:

```powershell
rg "request\.message\.text|inbound\.text|\bre\.|regex|isdigit|normalized|497|897|1497" app\core\taliya_commercial\validators.py
rg "if user says|when the message|keyword|hardcoded reply|fallback copy|customer-facing fallback|deterministic reply|safe answer|render_template|rendered_messages|RepairResult|repaired_decision|product_knowledge\.prices|diagnostic\.ledger|waitlist|student_count|demo_request|price_question" app\core\taliya_commercial\validators.py
```

Result: no matches.

## Review

- LLM-first preserved: validators do not decide commercial meaning.
- Deterministic code stayed limited to schema/state/template/channel guardrails.
- Product fact/price/student-count validators remain T011-061.
- Diagnostic, no-repeat, waitlist/demo/handoff, leak, Sales Inbox, repair, fallback, and corroboration validators remain T011-062..T011-069B.
- The proof is isolated-core proof only. Pipeline integration, trace persistence, renderer gating, adapters, and production behavior remain later tasks.
