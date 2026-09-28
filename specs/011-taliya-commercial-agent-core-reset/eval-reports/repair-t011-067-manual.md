# Repair T011-067 Manual Report

Status: passed for isolated Spec 011 core repair scope.

Task: `T011-067 - Implement one-call repair loop`.

## Scope

This task added a structured repair boundary for repairable validator failures.
It did not render messages, persist traces, deliver output, create fallback copy,
change `/pilates`, cut over widget/WhatsApp adapters, or touch
`runtime/runner.py`.

The repair loop is LLM-first: it sends the original structured decision,
`TurnContext`, context snapshot, validator issues, strict schema, and policy
reminders back to a provider for one correction attempt. The repaired decision
must pass the same validators before it can be accepted.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_repair_loop.py -q
```

Observed before implementation:

```text
ModuleNotFoundError: No module named 'app.core.taliya_commercial.repair'
```

This confirmed the repair boundary did not exist.

## Implemented Checks

- Valid decisions return `RepairResult(status=not_needed)` and do not call the
  repair provider.
- P0/blocked validator results return `RepairResult(status=blocked)` and do not
  call the repair provider.
- Repairable validator results call the provider exactly once.
- The repair request carries context, context snapshot JSON, original decision,
  validator errors, strict `ConductorDecision` schema, max attempts = 1, and
  instructions forbidding render/persist/delivery/fallback copy.
- Provider output must use the existing `ConductorTurnResult` envelope with
  `decision` and `model_usage`.
- Repaired decisions are revalidated with `validate_conductor_result`.
- Successful repairs return `RepairResult(status=repaired)` with repaired
  decision and repair model usage.
- Still-invalid repairs return `RepairResult(status=failed)` with validator
  issue codes and no fallback copy.
- Bad provider output returns `RepairResult(status=failed)` with
  `repair_provider_output_invalid` and no customer-facing fallback.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_repair_loop.py -q
```

Result: `5 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_boundary.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py -q
```

Result: `101 passed`.

Broad isolated Spec 011 core/conductor/validator/repair suite:

```powershell
python -m pytest tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `197 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/repair.py app/core/taliya_commercial/schemas.py tests/test_spec011_repair_loop.py
git diff --check -- services/taliya-agent-runtime/app/core/taliya_commercial/repair.py services/taliya-agent-runtime/app/core/taliya_commercial/schemas.py services/taliya-agent-runtime/tests/test_spec011_repair_loop.py
```

Result: Ruff passed and diff whitespace check passed.

Targeted static review found no matches for inbound text parsing, regex
import/use, hardcoded official price literals, active render/delivery/persist
calls, runtime calls, or fallback-message construction in the repair path.

## Anti-Drift Review

- Repair does not become a second commercial brain.
- Repair is capped at one provider call.
- P0 blocked validator failures stay blocked for T011-068.
- Failed repair produces no deterministic commercial answer.
- The proof is isolated-core proof, not adapter, persistence, or production
  cutover proof.

Next task: `T011-068 - Implement safe fallback/handoff after failed repair`.
