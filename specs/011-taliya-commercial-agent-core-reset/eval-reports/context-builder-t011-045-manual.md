# Context Builder T011-045 Manual Validation

Task: `T011-045 - Add context snapshot persistence for eval/debug`.

Date: 2026-05-30.

Proof level: isolated Spec 011 core and eval/debug artifact proof. This does not yet prove production trace persistence, adapter cutover, or Sales Inbox projection persistence; those remain owned by Phase 8 and Phase 9.

## Scope Checked

- No `/pilates` visual, layout, copy, or routing file was touched.
- No multi-tenant or client/studio WhatsApp path was touched.
- No runtime adapter, public API, production database migration, Sales Inbox UI, or `runtime/runner.py` code was touched.
- No commercial routing, regex, template-first decision, diagnostic state machine, price logic, waitlist logic, demo logic, or output rendering was added.
- The change is limited to internal eval/debug serialization and isolated file-store export of an already-built `TurnContext`.

## Red Result Before Fix

Command from `services/taliya-agent-runtime`:

```powershell
python -m pytest tests/test_spec011_context_snapshot.py -q
```

Observed result before implementation:

- Collection failed with `ModuleNotFoundError: No module named 'app.core.taliya_commercial.context_snapshot'`.

This was the intended red failure: the context builder could produce a typed `TurnContext`, but there was no replayable snapshot artifact for Phase 5 conductor tests or later trace evidence.

## Implementation Result

Added `services/taliya-agent-runtime/app/core/taliya_commercial/context_snapshot.py`:

- `ContextSnapshotRecord`: strict internal record for eval/debug only.
- `build_context_snapshot(context, ...)`: builds a snapshot from a typed `TurnContext`.
- `context_snapshot_to_json(...)`: exports stable sorted JSON.
- `context_snapshot_from_json(...)`: loads the snapshot back into the typed schema.
- `replay_turn_context(...)`: returns the original `TurnContext` for eval/conductor replay.
- `ContextSnapshotFileStore`: small isolated file store for local eval/debug artifacts.

The snapshot:

- mirrors top-level context identifiers and schema version;
- keeps `customer_visible=False`;
- preserves `source`, `reliability`, `confidence`, `renderable`, `missing`, `evidence`, and product source versions;
- does not add decision, route, intent, render plan, rendered messages, model usage, validators, repair, or outbox fields.

## Manual Snapshot Scenario

Input context includes:

- Channel source/entry labels including `lead came from the site` and `Reliable profile first name`.
- Channel profile/contact metadata.
- Customer-provided memory name with evidence.
- Sales Inbox projection name marked `inferred`.
- Official product knowledge refs including missing `integration_calendar`.
- Spec 006 product contract ref for product positioning.
- Recent transcript with previous assistant `template_id`.
- Diagnostic ledger, demo state, waitlist state, handoff state, and Sales Inbox inputs.

Observed snapshot behavior:

- JSON export is stable across roundtrip.
- Replayed `TurnContext` equals the original typed context.
- Channel profile remains `channel_metadata/channel_provided/renderable=False`.
- Projected profile remains `sales_inbox_projection/inferred/renderable=False`.
- Missing product ref remains `missing=True/renderable=False` with source version and evidence.
- Spec 006 ref keeps `source="spec_006_product_contract"` and a `spec006-...` version.
- File-store save/load preserves the full snapshot.
- The JSON key set does not include conductor/render/validator/usage decision fields.

## Green Validation

Focused test:

```powershell
python -m pytest tests/test_spec011_context_snapshot.py -q
```

Result: `4 passed`.

Nearest relevant isolated-core suite:

```powershell
python -m pytest tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `84 passed`.

Ruff:

```powershell
python -m ruff check app/core/taliya_commercial tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_core_schemas.py
```

Result: `All checks passed!`

Static review:

```powershell
rg "if .*request\.message\.text|elif .*request\.message\.text|if .*inbound\.text|elif .*inbound\.text|\bre\.|regex|detected_intents|\broute\b" app\core\taliya_commercial\context_builder.py app\core\taliya_commercial\product_knowledge.py app\core\taliya_commercial\context_snapshot.py
```

Result: no suspicious text-branching or routing patterns found in context/product/snapshot helpers.

## Remaining Risk

This task provides replayable context snapshots for eval/debug. It does not yet:

- persist the full mandatory production trace;
- persist conductor decision JSON, validator result, repair result, rendered messages, usage, runtime diff, delivery events, or Sales Inbox projection;
- connect widget/WhatsApp adapters to the new core;
- prove real-model conductor behavior.

Those remain Phase 5, Phase 8, and Phase 9 work.
