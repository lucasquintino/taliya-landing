# Conductor T011-054 Manual Validation

Date: 2026-05-30

Task: T011-054 - Require conductor self-checks without trusting them as final validation.

Scope: isolated Spec 011 core only. No public runtime cutover, no renderer implementation, no validator/repair implementation, no `/pilates` change, no WhatsApp customer/studio connection, no multi-tenant work.

## Behavior Checked

- Provider decisions must include explicit `policy_checks`.
- `policy_checks` must include every current `PolicyChecks` boolean.
- Explicit `false` self-checks are accepted as advisory/uncertain signals.
- Self-checks set to `true` cannot bypass hard boundary validation.
- Conductor instructions tell the LLM to fill every policy check and use `false` when uncertain.
- Conductor instructions state self-checks are not final validation.

## Red Baseline

Command from `services/taliya-agent-runtime`:

```powershell
python -m pytest tests/test_spec011_conductor_self_checks.py -q
```

Result before implementation: 3 failed, 3 passed.

Expected failures:

- Missing `policy_checks` was accepted through schema defaults.
- Partial `policy_checks` was accepted through field defaults.
- Conductor request did not yet describe self-checks as explicit, advisory, and non-final.

## Implementation Notes

- `PolicyChecks` booleans are now required schema fields.
- `ConductorDecision.policy_checks` is now required.
- The conductor request instructs the LLM to fill every boolean and use `false` when uncertain.
- The schema fingerprint changed intentionally because `policy_checks` became required. The reviewed fingerprint is now:

```text
sha256:cf08cb089a2fda982069dd8269e6439de52c486cfd988c63371f4c40193357bc
```

## Green Validation

Commands from `services/taliya-agent-runtime`:

```powershell
python -m pytest tests/test_spec011_conductor_self_checks.py -q
python -m pytest tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_core_schemas.py -q
python -m pytest tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
python -m ruff check app/core/taliya_commercial tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_core_schemas.py tests/test_spec011_template_registry.py tests/test_spec011_schema_versioning.py
```

Results:

- Focused self-check tests: 6 passed.
- Focused conductor/core schema set: 30 passed.
- Isolated Spec 011 core/conductor suite: 110 passed.
- Ruff: all checks passed.

## Static Review

Commands from `services/taliya-agent-runtime`:

```powershell
rg "request\.message\.text|inbound\.text|\bre\.|regex|isdigit|normalized|497|897|1497" app\core\taliya_commercial\conductor.py app\core\taliya_commercial\conductor_policy.py app\core\taliya_commercial\schemas.py app\core\taliya_commercial\template_registry.py app\core\taliya_commercial\schema_versioning.py
rg "policy_checks.*passed|policy_checks.*pass|if .*policy_checks|elif .*policy_checks|validator_result.*policy_checks" app\core\taliya_commercial\conductor.py app\core\taliya_commercial\schemas.py app\core\taliya_commercial\schema_versioning.py
```

Result: no matches.

## LLM-First Review

Accepted pattern:

- The LLM still owns commercial understanding and returns self-checks in JSON.
- Deterministic code requires self-check presence and shape only.
- Self-checks do not choose route/template, do not validate product facts, and do not mark the turn as PASS.
- A decision with all self-checks set to `true` still fails if another hard boundary fails.

Remaining later gates:

- T011-069 must add corroboration so self-check booleans cannot pass direct-question, official-fact, diagnostic-complete, or policy behavior alone.
- T011-108 must include manual transcript quality review.
