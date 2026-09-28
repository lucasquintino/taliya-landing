# Validators T011-066 Manual Report

Status: passed for isolated Spec 011 core validator scope.

Task: `T011-066 - Implement Sales Inbox completeness validator`.

## Scope

This task added a deterministic validator for explicit `SalesInboxProjection`
payloads only. It did not build the projection engine, persist traces, redesign
Sales Inbox, change `/pilates`, cut over widget/WhatsApp adapters, or touch
`runtime/runner.py`.

The validator checks structured projection consistency against the validated
decision/context boundary. It does not parse inbound text, infer commercial
meaning, choose routes, render copy, repair decisions, persist records, deliver
messages, or perform fallback/handoff behavior.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_validators_sales_inbox.py -q
```

Observed before implementation:

```text
ImportError: cannot import name 'validate_sales_inbox_projection'
```

This confirmed the new Sales Inbox projection validator boundary did not exist.

A second red guard was added before final closure for invalid projection-like
payloads. It failed because the validator raised a Pydantic `ValidationError`
instead of returning a typed `ValidatorResult` issue. The final implementation
now returns `sales_inbox_projection_schema_invalid`.

## Implemented Checks

- Projection `conversation_id` and `lead_id` must match context/decision.
- Invalid projection-like payloads must return a typed `ValidatorResult` issue.
- Common runtime fields must exist: `template_ids`, `validator_status`,
  `validator_final_disposition`, `source_labels`, and `operator_next_action`.
- Projection template ids must match the validated render plan.
- Projection commercial stage must come from validated `current_state` or
  `next_state`.
- Completed diagnostic projections must include completed diagnostic status,
  complete required diagnostic keys including urgency, demo status, final
  plan/range, and final demo line.
- Pending waitlist projections must expose exact missing details.
- Joined waitlist projections must expose joined timestamp, idempotency marker,
  and no missing details.
- Handoff projections must expose handoff reason, `human_active`, and
  `ai_paused` flags.
- Channel-provided, inferred, or unverified identity cannot be promoted to
  verified identity.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_validators_sales_inbox.py -q
```

Result: `9 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_sales_inbox_projection_cases.py -q
```

Result: `65 passed`.

Broad isolated Spec 011 core/conductor/validator suite:

```powershell
python -m pytest tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `192 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/validators.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py
git diff --check -- services/taliya-agent-runtime/app/core/taliya_commercial/validators.py services/taliya-agent-runtime/tests/test_spec011_validators_sales_inbox.py
```

Result: Ruff passed and diff whitespace check passed.

Targeted static review found no matches for inbound text parsing, regex
import/use, hardcoded official price literals, rendering, repair, runtime calls,
or fallback copy in the changed validator path.

## Anti-Drift Review

- LLM remains the owner of commercial understanding.
- Sales Inbox remains a projection of validated state/context, not a second
  interpretation engine.
- Validator failures return `ValidatorResult` issues only.
- The proof is isolated-core proof, not adapter, persistence, or production
  cutover proof.

Next task: `T011-067 - Implement one-call repair loop`.
