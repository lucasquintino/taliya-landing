# Validators T011-065 Manual Validation

Date: 2026-05-30

Task: T011-065 - Implement internal text leak and banned phrase validators.

Scope: isolated Spec 011 core validator only. No renderer, repair loop, persistence, adapter cutover, `/pilates` change, Sales Inbox UI change, multi-tenant work, customer/studio WhatsApp connection, or fallback copy.

## What Changed

- Added pre-render template-variable text safety validation.
- Blocked internal/source/debug text in customer-facing variables, including `Reliable profile first name` and `lead came from the site`.
- Blocked banned customer-facing diagnostic phrases such as the old fixed "principal gargalo" style.
- Blocked forbidden waitlist promise language inside waitlist variables, including checkout/VIP/discount/payment/date-style promises.
- Kept the validator limited to structured `template_plan.items[].variables[].value`.
- Validator still returns only `ValidatorResult`; it does not rewrite copy, render text, repair decisions, persist state, deliver messages, or create fallback copy.

## Red Baseline

Command from `services/taliya-agent-runtime`:

```powershell
python -m pytest tests/test_spec011_validators_leak_banned_phrases.py -q
```

Initial result after adding leak/banned phrase tests: 4 failed, 1 passed.

Expected failures proved the previous validator accepted:

- `Reliable profile first name` inside a customer-facing first-name variable;
- `lead came from the site` inside a product variable;
- banned final diagnostic phrase inside a diagnostic variable;
- forbidden waitlist promise language inside a waitlist variable.

## Validation Commands

Focused leak/banned phrase validator suite:

```powershell
python -m pytest tests/test_spec011_validators_leak_banned_phrases.py -q
```

Result: 5 passed.

Nearby validator/schema/template suite:

```powershell
python -m pytest tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py -q
```

Result: 50 passed.

Isolated Spec 011 core/conductor/validator suite:

```powershell
python -m pytest tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: 183 passed.

Ruff:

```powershell
python -m ruff check app/core/taliya_commercial tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_core_schemas.py tests/test_spec011_template_registry.py tests/test_spec011_schema_versioning.py
```

Result: all checks passed.

Static review:

```powershell
rg -n "request\.message\.text|context\.inbound\.text|inbound\.text|\bre\.|regex|isdigit|\b197\b|\b497\b|\b897\b|\b1497\b|rendered_messages|RepairResult|repaired_decision|run_agent_turn|render_template|fallback copy|customer-facing fallback" app\core\taliya_commercial\validators.py
```

Result: no matches.

## LLM-First Review

- The validator inspects only structured template variable values selected by the LLM.
- It does not parse inbound user text, choose route/intent, or generate replacement wording.
- It blocks unsafe pre-render values before renderer/persistence/delivery.
- It does not implement Sales Inbox completeness, repair, fallback, or broad quality judging.

## Remaining Work

- T011-066 must implement Sales Inbox completeness validators.
- T011-067..T011-069B still own repair, fallback, corroboration, deeper product-claim, and failed-path validation.
