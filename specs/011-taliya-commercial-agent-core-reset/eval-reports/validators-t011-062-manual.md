# Validators T011-062 Manual Validation

Date: 2026-05-30

Task: T011-062 - Implement diagnostic ledger validators, including mandatory urgency.

Scope: isolated Spec 011 core validator only. No renderer, repair loop, persistence, adapter cutover, `/pilates` change, Sales Inbox UI change, multi-tenant work, or customer/studio WhatsApp connection.

## What Changed

- Extended `validate_conductor_result(...)` with diagnostic ledger validation.
- Blocked `diagnostic.complete` and diagnostic delivery templates unless every mandatory diagnostic key is complete, including `urgency`.
- Validated that `diagnostic.ask_next` targets a mandatory diagnostic key that is not already complete.
- Blocked multiple `diagnostic.ask_*` templates in one turn.
- Required answered, inferred, or not-applicable diagnostic ledger updates to include evidence, and answered/inferred updates to include `answer_value`.
- Preserved the `120` regression guard: a simple user-grounded student-count answer for a pending active-students field can pass and move to the next question.
- Validator still returns only `ValidatorResult`; it does not ask questions, choose strategy, render text, persist state, repair decisions, or compose fallback copy.

## Red Baseline

Command from `services/taliya-agent-runtime`:

```powershell
python -m pytest tests/test_spec011_validators_diagnostic.py -q
```

Initial result after adding diagnostic tests: 4 failed, 2 passed.

Expected failures proved the previous validator accepted:

- completed diagnostic with `urgency` still missing;
- invalid `next_question_key` outside the mandatory diagnostic keys;
- multiple diagnostic question templates in one turn;
- answered diagnostic ledger update without evidence.

The two already-passing cases were useful guardrails:

- completed diagnostic with all mandatory fields remained valid;
- simple `120` answer for pending active-students field remained valid.

## Validation Commands

Focused diagnostic validator suite:

```powershell
python -m pytest tests/test_spec011_validators_diagnostic.py -q
```

Result: 6 passed.

Nearby validator/schema/template suite:

```powershell
python -m pytest tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py -q
```

Result: 33 passed.

Isolated Spec 011 core/conductor/validator suite:

```powershell
python -m pytest tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: 166 passed.

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

- The diagnostic validator reads structured context/decision state; it does not parse inbound text for commercial meaning.
- It does not decide which route, intent, or diagnostic question should be chosen. It only checks whether the LLM-selected `ask_next` target is legal and incomplete.
- It blocks final diagnostic delivery before required evidence is complete, especially `urgency`.
- It does not render the final diagnostic, does not repair, and does not create fallback copy.
- The dedicated no-repeat validator remains T011-063.

## Remaining Work

- T011-063 must prevent repeated already-answered diagnostic questions except explicit ambiguity/confirmation cases.
- T011-064..T011-069B still own waitlist/demo/handoff, leak, Sales Inbox, repair, fallback, corroboration, deeper product-claim, and failed-path validation.
- Renderer proof for final diagnostic staged order and last sentence remains T011-073.
