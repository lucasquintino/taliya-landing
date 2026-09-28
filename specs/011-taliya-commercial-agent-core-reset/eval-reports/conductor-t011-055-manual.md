# Conductor T011-055 Manual Validation

Date: 2026-05-30

Task: T011-055 - Log model usage for every conductor call.

Scope: isolated Spec 011 core only. No real OpenAI provider integration, no trace persistence, no billing/cost table work, no public runtime cutover, no `/pilates` change, no WhatsApp customer/studio connection, no multi-tenant work.

## Behavior Checked

- Successful `conduct_turn` returns a typed result containing both `decision` and `model_usage`.
- Provider output must use an envelope with `decision` and `model_usage`.
- Bare decision output is rejected.
- Missing `model_usage` is rejected.
- Empty model names are rejected.
- Zero input/output token usage is rejected.
- Provider request carries provider-level requirements to attach `model_usage` outside the LLM decision JSON.

## Red Baseline

Command from `services/taliya-agent-runtime`:

```powershell
python -m pytest tests/test_spec011_conductor_usage.py -q
```

Result before implementation: collection failed because `ConductorTurnResult` did not exist.

The old boundary returned only `ConductorDecision`, so there was no place for required usage metadata.

## Implementation Notes

- Added `ConductorTurnResult` with `decision: ConductorDecision` and `model_usage: ModelUsage`.
- Changed provider output parsing to require a `decision` + `model_usage` envelope.
- Added `provider_requirements` to `ConductorProviderRequest` so the provider wrapper, not the LLM decision JSON, is responsible for usage metadata.
- Tightened `ModelUsage` so model name must be non-empty, input tokens and output tokens must be positive, and cost cannot be negative.
- Existing conductor fixtures now return provider envelopes with positive model usage.

No usage is estimated or faked from message length. No real OpenAI provider integration was added in this step.

## Green Validation

Commands from `services/taliya-agent-runtime`:

```powershell
python -m pytest tests/test_spec011_conductor_usage.py -q
python -m pytest tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_core_schemas.py -q
python -m pytest tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
python -m ruff check app/core/taliya_commercial tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_core_schemas.py tests/test_spec011_template_registry.py tests/test_spec011_schema_versioning.py
```

Results:

- Focused usage tests: 6 passed.
- Focused conductor/core schema set: 36 passed.
- Isolated Spec 011 core/conductor suite: 116 passed.
- Ruff: all checks passed.

## Static Review

Commands from `services/taliya-agent-runtime`:

```powershell
rg "request\.message\.text|inbound\.text|\bre\.|regex|isdigit|normalized|497|897|1497" app\core\taliya_commercial\conductor.py app\core\taliya_commercial\conductor_policy.py app\core\taliya_commercial\schemas.py app\core\taliya_commercial\template_registry.py app\core\taliya_commercial\schema_versioning.py
rg "usage_from_tokens|estimate_cost|input_tokens =|output_tokens =|cost_usd =|max\(1|len\(.*//|fake|estimated" app\core\taliya_commercial\conductor.py app\core\taliya_commercial\schemas.py
```

Result: no matches.

## LLM-First Review

Accepted pattern:

- The LLM still returns only the structured conductor decision.
- The provider wrapper must attach usage metadata from provider-reported values.
- Deterministic code validates usage shape and rejects missing or zero-token usage.
- No model/cost data is invented by parsing user text, output text, or prompt length.

Remaining later gates:

- Real OpenAI provider integration remains later work.
- T011-080/T011-107 must persist/export usage in the mandatory trace.
- T011-089 must add cost optimization reports proving savings without removing model usage.
