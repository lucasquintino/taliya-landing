# Conductor T011-050 Manual Validation

Task: `T011-050 - Implement one-call conductor using the strict decision schema`.

Date: 2026-05-30.

Proof level: isolated Spec 011 core boundary proof with mocked provider. This does not yet prove real OpenAI behavior, model usage logging, specialist policy quality, validators, rendering, trace persistence, or public adapter cutover.

## Scope Checked

- No `/pilates` visual, layout, copy, or routing file was touched.
- No multi-tenant or client/studio WhatsApp path was touched.
- No runtime adapter, public API, production database migration, Sales Inbox UI, or `runtime/runner.py` code was touched.
- No deterministic commercial routing, regex, keyword classification, template-first response, diagnostic state machine, price logic, waitlist logic, demo logic, renderer, repair loop, or customer-facing fallback was added.
- The change is limited to an isolated LLM conductor boundary with an injectable provider and strict `ConductorDecision` validation.

## Red Result Before Fix

Command from `services/taliya-agent-runtime`:

```powershell
python -m pytest tests/test_spec011_conductor_boundary.py -q
```

Observed result before implementation:

- Collection failed with `ModuleNotFoundError: No module named 'app.core.taliya_commercial.conductor'`.

This was the intended red failure: Phase 4 had typed/replayable context, but no isolated LLM conductor boundary that required provider output to be strict structured JSON.

## Implementation Result

Added `services/taliya-agent-runtime/app/core/taliya_commercial/conductor.py`:

- `ConductorProviderRequest`: typed provider request containing `TurnContext`, stable context snapshot JSON, `ConductorDecision` JSON schema, and minimal boundary instructions.
- `conduct_turn(...)`: accepts a typed `TurnContext`, `ContextSnapshotRecord`, or snapshot JSON string and calls the injected provider once.
- `ConductorOutputError`: raised when provider output is free-form text, non-JSON, non-object JSON, or unsupported content.
- `ConductorDecisionValidationError`: raised when provider JSON fails `ConductorDecision` validation or does not match the input context identifiers.
- Provider output may be `ConductorDecision`, `dict`, or JSON string; all paths validate to the strict schema.

The conductor boundary:

- does not inspect inbound text for meaning;
- does not choose route/role/template/diagnostic/waitlist/demo decisions in code;
- does not render messages;
- does not invent a deterministic fallback if provider output is invalid;
- surfaces invalid/free-form provider output for later repair/validator tasks.

## Manual Scenario

Input context:

- WhatsApp lead asks: `Quanto custa e tenho 120 alunos?`
- Context includes memory, channel metadata, product knowledge `prices`, and Spec 006 product positioning.

Provider fixture returns:

- strict `schema_version="011.0"`;
- matching `turn_id`, `conversation_id`, `channel`, and `agent_key`;
- `role="product"` and `route="product"` chosen by the provider fixture;
- numeric interpretation for `120` as `student_count`;
- `template_plan` with an official product-knowledge variable.

Observed boundary behavior:

- Provider is called exactly once.
- Provider request includes the full typed context and stable context snapshot JSON.
- Provider request exposes the `ConductorDecision` JSON schema.
- Valid decision JSON validates and returns `ConductorDecision`.
- Free-form text fails with `ConductorOutputError`.
- JSON with `message_text` but no strict decision fields fails with `ConductorDecisionValidationError`.
- A decision with another `turn_id` fails with `ConductorDecisionValidationError`.

## Green Validation

Focused test:

```powershell
python -m pytest tests/test_spec011_conductor_boundary.py -q
```

Result: `5 passed`.

Nearest relevant isolated-core suite:

```powershell
python -m pytest tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `89 passed`.

Ruff:

```powershell
python -m ruff check app/core/taliya_commercial tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_core_schemas.py
```

Result: `All checks passed!`

Static review:

```powershell
rg "if .*request\.message\.text|elif .*request\.message\.text|if .*inbound\.text|elif .*inbound\.text|if .*context\.inbound|elif .*context\.inbound|\bre\.|regex|normalized" app\core\taliya_commercial\conductor.py
```

Result: no text-branching, regex, or normalization routing patterns found in conductor.

## Remaining Risk

This task proves only the conductor boundary and strict JSON acceptance/rejection with a mocked provider. It does not yet:

- encode the specialist policy pack (`T011-051`);
- require evidence for extracted facts/numbers (`T011-052`);
- require deep template planning (`T011-053`);
- add conductor self-checks (`T011-054`);
- log model usage (`T011-055`);
- run real OpenAI evals (`T011-103`, `T011-104`);
- validate or render the returned decision (`T011-060..T011-074`);
- persist production trace or Sales Inbox projection (`T011-080..T011-086`).
