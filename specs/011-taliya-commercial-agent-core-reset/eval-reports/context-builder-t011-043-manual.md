# Context Builder T011-043 Manual Validation

Task: `T011-043 - Mark internal metadata as non-renderable`.

Date: 2026-05-30.

Proof level: isolated Spec 011 core and schema proof. This does not yet prove final rendered customer output; rendered-output leak blocking remains owned by `T011-065` and `T011-070`.

## Scope Checked

- No `/pilates` visual, layout, copy, or routing file was touched.
- No multi-tenant or client/studio WhatsApp path was touched.
- No commercial routing, regex, template-first decision, diagnostic state machine, price logic, waitlist logic, or demo logic was added.
- The change is limited to typed context/schema protection for internal/channel/product source material.

## Red Result Before Fix

Command from `services/taliya-agent-runtime`:

```powershell
python -m pytest tests/test_spec011_internal_metadata_non_renderable.py -q
```

Observed result before implementation:

- `2 failed, 1 passed`.
- A `TurnFact` with `source="channel_metadata"`, `reliability="channel_provided"`, and `renderable=True` was accepted.
- `ProductKnowledgeRef` had no explicit `renderable` marker, so product refs could not be asserted as source-only context.

This was the intended red failure for the observed leak class:

- `Reliable profile first name`
- `lead came from the site`

## Implementation Result

Changed `services/taliya-agent-runtime/app/core/taliya_commercial/schemas.py`:

- `ProductKnowledgeRef.renderable` now defaults to `False`.
- `ProductKnowledgeRef(renderable=True)` is rejected.
- `TurnFact(source="channel_metadata", renderable=True)` is rejected.
- Existing `TurnFact(reliability="internal", renderable=True)` rejection remains.

The context builder stayed selection-only:

- it still copies only explicit channel metadata fields;
- it still ignores `metadata.runtime_control`;
- it still preserves runtime event `template_id` while omitting arbitrary debug event metadata;
- it still does not inspect the inbound commercial text to route or choose templates.

## Manual Snapshot Scenario

Input labels:

- `conversation.source = "lead came from the site"`
- `conversation.entry_intent = "Reliable profile first name"`
- `sender.name = "Reliable profile first name: Ana"`
- `metadata.runtime_control.debug_label = "lead came from the site"`
- runtime event metadata includes `internal_debug` and `profile_label`

Observed context behavior:

- channel/source facts exist only as `source="channel_metadata"`;
- every channel/source fact has `renderable=False`;
- `runtime_control` is not copied into `sales_inbox_inputs`;
- no fact evidence includes `runtime_control`;
- `recent_transcript` does not include `internal_debug` or `profile_label`;
- `recent_transcript` keeps only the allowed `template_id`;
- product refs from official product knowledge and Spec 006 have `renderable=False`;
- product refs cannot be validated with `renderable=True`.

## Green Validation

Focused test:

```powershell
python -m pytest tests/test_spec011_internal_metadata_non_renderable.py -q
```

Result: `3 passed`.

Nearest relevant isolated-core suite:

```powershell
python -m pytest tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `77 passed`.

Ruff:

```powershell
python -m ruff check app/core/taliya_commercial tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_core_schemas.py
```

Result: `All checks passed!`

Static review:

```powershell
rg "if .*request\.message\.text|elif .*request\.message\.text|if .*inbound\.text|elif .*inbound\.text|\bre\.|regex|detected_intents|\broute\b" app\core\taliya_commercial\context_builder.py app\core\taliya_commercial\product_knowledge.py
```

Result: no suspicious text-branching or routing patterns found.

## Remaining Risk

This task prevents internal/channel/product source material from being marked as renderable context. It does not yet validate final `RenderPlan` variables or rendered text. That is intentionally left to:

- `T011-065` internal text leak and banned phrase validators;
- `T011-070` renderer accepts only validated template plans;
- `T011-072` required variable validation before render.
