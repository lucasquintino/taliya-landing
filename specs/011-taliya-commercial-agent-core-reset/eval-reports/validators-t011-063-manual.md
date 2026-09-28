# Validators T011-063 Manual Validation

Date: 2026-05-30

Task: T011-063 - Implement no-repeat diagnostic question validator.

Scope: isolated Spec 011 core validator only. No renderer, repair loop, persistence, adapter cutover, `/pilates` change, Sales Inbox UI change, multi-tenant work, or customer/studio WhatsApp connection.

## What Changed

- Added explicit no-repeat validation for diagnostic questions already completed in `TurnContext.diagnostic_ledger`.
- Blocked repeated `diagnostic.next_question_key` when the key is already `answered`, `inferred_from_prior_message`, or `not_applicable`.
- Blocked repeated diagnostic question templates hidden in `template_plan.items`.
- Preserved legal re-ask for ambiguous/missing cases.
- Validator still returns only `ValidatorResult`; it does not ask questions, choose strategy, render text, persist state, repair decisions, or compose fallback copy.

## Red Baseline

Command from `services/taliya-agent-runtime`:

```powershell
python -m pytest tests/test_spec011_validators_diagnostic.py -q
```

Initial result after adding no-repeat tests: 2 failed, 7 passed.

Expected failures proved the previous validator blocked repeated questions only with generic reasons:

- repeated active-students question after the ledger already had an answered value;
- repeated active-students template hidden behind a different `next_question_key`.

The new validator reports the specific `diagnostic_question_repeated` issue for both.

## Validation Commands

Focused diagnostic validator suite:

```powershell
python -m pytest tests/test_spec011_validators_diagnostic.py -q
```

Result: 9 passed.

Nearby validator/schema/template suite:

```powershell
python -m pytest tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py -q
```

Result: 36 passed.

Isolated Spec 011 core/conductor/validator suite:

```powershell
python -m pytest tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: 169 passed.

Ruff:

```powershell
python -m ruff check app/core/taliya_commercial tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_core_schemas.py tests/test_spec011_template_registry.py tests/test_spec011_schema_versioning.py
```

Result: all checks passed.

Static review:

```powershell
rg -n "request\.message\.text|context\.inbound\.text|inbound\.text|\bre\.|regex|isdigit|\b197\b|\b497\b|\b897\b|\b1497\b|rendered_messages|RepairResult|repaired_decision|run_agent_turn|render_template|fallback copy|customer-facing fallback" app\core\taliya_commercial\validators.py
```

Result: no matches.

## LLM-First Review

- The no-repeat validator reads only structured diagnostic ledger status and structured template ids.
- It does not parse inbound text, infer intent, or choose which question should come next.
- It blocks repeated completed questions and allows ambiguous/missing questions to be asked again.
- It does not render, repair, persist, deliver, hand off, or create fallback copy.

## Remaining Work

- T011-064 must implement waitlist/demo/handoff validators.
- T011-065..T011-069B still own leak, Sales Inbox, repair, fallback, corroboration, deeper product-claim, and failed-path validation.
