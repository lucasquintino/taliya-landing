# Conductor T011-053 Manual Validation

Date: 2026-05-30

Task: T011-053 - Require template plan and variables in structured output.

Scope: isolated Spec 011 core only. No public runtime cutover, no renderer implementation, no `/pilates` change, no WhatsApp customer/studio connection, no multi-tenant work.

## Behavior Checked

- Provider decisions must include `template_plan`.
- Normal conductor decisions must include at least one template plan item.
- Template ids must be registered in the approved template registry.
- Template variables must be typed `TemplateVariableValue` objects.
- Required variables for the selected template must be present.
- Template variables must include evidence.
- Whole-response fields and variables remain rejected; customer-facing prose cannot bypass the renderer as a free-form field.

## Red Baseline

Command from `services/taliya-agent-runtime`:

```powershell
python -m pytest tests/test_spec011_conductor_template_plan.py -q
```

Result before implementation: 5 failed, 2 passed.

Expected failures:

- Empty `template_plan.items` was accepted.
- Unregistered template ids were accepted.
- Missing required variables were accepted.
- Template variables without evidence were accepted.
- Conductor request instructions did not yet name registered template ids/variables and whole-response fields.

## Green Validation

Commands from `services/taliya-agent-runtime`:

```powershell
python -m pytest tests/test_spec011_conductor_template_plan.py -q
python -m pytest tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_policy_pack.py -q
python -m pytest tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
python -m ruff check app/core/taliya_commercial tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_core_schemas.py tests/test_spec011_template_registry.py
```

Results:

- Focused template-plan tests: 7 passed.
- Focused conductor template/policy tests: 11 passed.
- Isolated Spec 011 core/conductor suite: 104 passed.
- Ruff: all checks passed.

## Static Review

Commands from `services/taliya-agent-runtime`:

```powershell
rg "request\.message\.text|inbound\.text|\bre\.|regex|isdigit|normalized|if .*template|elif .*template|if .*route|elif .*route|497|897|1497" app\core\taliya_commercial\conductor.py app\core\taliya_commercial\conductor_policy.py app\core\taliya_commercial\schemas.py app\core\taliya_commercial\template_registry.py
rg "request\.message\.text|inbound\.text|\bre\.|regex|isdigit|normalized|497|897|1497" app\core\taliya_commercial\conductor.py app\core\taliya_commercial\conductor_policy.py app\core\taliya_commercial\schemas.py app\core\taliya_commercial\template_registry.py
```

Result:

- The wider search found only template-registry validation branches and the conductor's `template_plan.items` non-empty guard.
- The stricter search found no inbound-text parsing, regex, normalization, `isdigit`, or hardcoded product prices.

## LLM-First Review

Accepted pattern:

- The LLM still chooses role, route, intent, state, template ids, and variables.
- Deterministic code only rejects unsafe/unrenderable structured output after the provider responds.
- No code was added to choose product, price, diagnostic, waitlist, demo, handoff, or fallback templates by keywords or inbound text.

Remaining later gates:

- T011-054 must add self-checks without treating them as final validation.
- T011-056 must keep generic whole-response fields prohibited at the conductor-output level.
- T011-070..T011-074 must implement renderer behavior using only validated template plans.
