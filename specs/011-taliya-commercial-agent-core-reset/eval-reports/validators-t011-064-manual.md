# Validators T011-064 Manual Validation

Date: 2026-05-30

Task: T011-064 - Implement waitlist/demo/handoff validators.

Scope: isolated Spec 011 core validator only. No renderer, repair loop, persistence, adapter cutover, `/pilates` change, Sales Inbox UI change, multi-tenant work, customer/studio WhatsApp connection, checkout/payment, or handoff side-effect implementation.

## What Changed

- Added waitlist validation for structured eligibility before offer/pending/joined states.
- Blocked waitlist from demo curiosity without structured eligible status.
- Blocked `joined` waitlist decisions that still contain missing details.
- Added demo validation so `demo.next_step = offer_demo` requires an approved demo template.
- Preserved commercial/product demo as the existing `commercial_product_demo` schema concept; no technical/video/demo-asset scope was added.
- Added handoff validation for missing handoff reason, route/template consistency, and human-active context blocking normal AI delivery.
- Validator still returns only `ValidatorResult`; it does not offer waitlist, send demo, pause humans, persist handoff, repair, render, or compose fallback copy.

## Red Baseline

Command from `services/taliya-agent-runtime`:

```powershell
python -m pytest tests/test_spec011_validators_waitlist_demo_handoff.py -q
```

Initial result after adding waitlist/demo/handoff tests: 6 failed, 3 passed.

Expected failures proved the previous validator accepted:

- waitlist offer with `eligibility = unknown`;
- joined waitlist while missing details remained;
- waitlist after demo curiosity without contract intent;
- demo offer without approved demo template;
- handoff request without a reason;
- normal AI delivery while context said human was active.

After the first implementation, nearby tests caught a fixture bug: price validator tests inherited `demo.next_step = offer_demo` from a demo helper while using a price template. The fixture was corrected so price decisions no longer pretend to offer a demo.

## Validation Commands

Focused waitlist/demo/handoff validator suite:

```powershell
python -m pytest tests/test_spec011_validators_waitlist_demo_handoff.py -q
```

Result: 9 passed.

Nearby validator/schema/template suite:

```powershell
python -m pytest tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py -q
```

Result: 45 passed.

Isolated Spec 011 core/conductor/validator suite:

```powershell
python -m pytest tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: 178 passed.

Ruff:

```powershell
python -m ruff check app/core/taliya_commercial tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_core_schemas.py tests/test_spec011_template_registry.py tests/test_spec011_schema_versioning.py
```

Result: all checks passed.

Static review:

```powershell
rg -n "request\.message\.text|context\.inbound\.text|inbound\.text|\bre\.|regex|isdigit|\b197\b|\b497\b|\b897\b|\b1497\b|rendered_messages|RepairResult|repaired_decision|run_agent_turn|render_template|fallback copy|customer-facing fallback" app\core\taliya_commercial\validators.py
```

Result: no matches.

## LLM-First Review

- The validators read structured `waitlist`, `demo`, `handoff`, template ids, and context handoff state.
- They do not parse inbound text, infer buy intent, infer demo reaction, or choose waitlist/handoff route.
- They block impossible or unsafe structured decisions before rendering/persistence.
- They do not connect studio WhatsApp, create checkout, send handoff, render demo, repair, persist, deliver, or produce fallback copy.

## Remaining Work

- T011-065 must implement internal text leak and banned phrase validators.
- T011-066..T011-069B still own Sales Inbox, repair, fallback, corroboration, deeper product-claim, and failed-path validation.
