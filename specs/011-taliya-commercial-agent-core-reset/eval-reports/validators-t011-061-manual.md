# Validators T011-061 Manual Validation

Date: 2026-05-30

Task: T011-061 - Implement product fact and price/student-count validators.

Scope: isolated Spec 011 core validator only. No adapter cutover, no public runtime path, no `/pilates` visual or copy change, no Sales Inbox UI change, no multi-tenant work, and no customer/studio WhatsApp connection.

## What Changed

- Extended `validate_conductor_result(...)` with product grounding checks for template variables whose source is `official_product_knowledge` or `spec_006_product_contract`.
- Validated that official-source template variable evidence resolves to product refs actually present in `TurnContext.product_knowledge`.
- Validated URL variables against official product links, including exact `official_demo_link` matching.
- Validated `plan_price` numeric interpretations against official prices from product knowledge.
- Validated price-bearing template variables so invented price amounts are blocked before rendering.
- Kept `student_count` separate from `plan_price`: simple user-grounded `120` remains valid, while a student-count value that collides with an official price such as `497` is blocked unless separately grounded as a user fact.
- Validator still returns only `ValidatorResult`; it does not repair, render, persist, deliver, hand off, or compose customer-facing fallback copy.

## Red Baseline

Command from `services/taliya-agent-runtime`:

```powershell
python -m pytest tests/test_spec011_validators_core.py -q
```

Initial result after adding product/numeric tests: 5 failed, 9 passed.

Expected failures proved the previous validator accepted:

- official product variable evidence missing from context;
- invented or shortened official demo URL;
- `plan_price` value not present in official product knowledge;
- invented price text inside an official price variable;
- `497` treated as `student_count` without user fact grounding.

Additional red guard after implementation review:

- Added simple `120` student-count fixture without a mirrored fact.
- It failed because the first implementation was too strict and could have recreated the valid-number stall bug.
- The validator was then narrowed so fact grounding is required only for student-count values that collide with official prices.

## Validation Commands

Focused validator suite:

```powershell
python -m pytest tests/test_spec011_validators_core.py -q
```

Result: 15 passed.

Isolated Spec 011 core/conductor/validator suite:

```powershell
python -m pytest tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: 160 passed.

Ruff:

```powershell
python -m ruff check app/core/taliya_commercial/validators.py tests/test_spec011_validators_core.py
```

Result: all checks passed.

Static review:

```powershell
rg -n "request\.message\.text|context\.inbound\.text|inbound\.text|\bre\.|regex|isdigit|\b197\b|\b497\b|\b897\b|\b1497\b|rendered_messages|RepairResult|repaired_decision|run_agent_turn|render_template|fallback copy|customer-facing fallback" app\core\taliya_commercial\validators.py
```

Result: no matches. The validator does not parse inbound text, import regex, hardcode official price values, render messages, repair decisions, call runtime paths, or produce fallback copy.

## LLM-First Review

- The validator does not choose route, role, intent, diagnostic action, waitlist action, demo action, or template id.
- It does not inspect `request.message.text`, `context.inbound.text`, or raw inbound text to infer commercial meaning.
- It only checks whether the LLM's structured decision is grounded in official sources and user evidence before any renderer/persistence side effect.
- Official prices are read dynamically from `TurnContext.product_knowledge`, not hardcoded in the validator.
- The `497` regression is handled as a validation collision with official price context, not as keyword or routing logic.

## Remaining Work

- T011-062 must implement diagnostic ledger validators, including mandatory urgency.
- T011-063 still owns no-repeat diagnostic question validation.
- T011-064..T011-069B still own waitlist/demo/handoff, leak, Sales Inbox, repair, fallback, corroboration, product-claim, and failed-path validation.
- Renderer proof that no rendered text says "497 alunos" remains later, because T011-061 is isolated pre-render validation.
