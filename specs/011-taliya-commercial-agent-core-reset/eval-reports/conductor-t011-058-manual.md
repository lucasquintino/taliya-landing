# Conductor T011-058 Manual Validation

Date: 2026-05-30

Task: T011-058 - Preserve commercial demo/product demo as one customer-facing concept while keeping OpenAI technical demo and video-production assets out of scope.

Scope: isolated Spec 011 core/conductor boundary only. No public runtime cutover, no renderer copy, no `/pilates` changes, no widget/WhatsApp adapter changes, no video production, no visual demo assets, and no `runner.py` commercial changes.

## Contract Checked

- Commercial demo, product demo, demo, demonstration, and `ver funcionando` are one customer-facing commercial concept.
- The conductor schema exposes one demo concept: `demo.customer_facing_concept = commercial_product_demo`.
- The conductor continues to use existing `demo` structured fields: status and next step.
- Provider request and specialist policy pack instruct the LLM to keep OpenAI technical reference demos, video production, and visual demo assets out of scope.
- Out-of-scope demo fields such as `technical_demo`, `openai_demo`, `video_demo`, `demo_video`, `demo_asset`, `demo_assets`, `video_production`, and `visual_demo_assets` are explicitly rejected.
- The policy remains stable across different inbound texts. Code does not inspect inbound text to decide demo meaning.

## Red Baseline

Command:

```powershell
python -m pytest tests/test_spec011_conductor_demo_concept.py -q
```

Result before implementation: 4 failed.

Observed failure reason:

- `demo.customer_facing_concept` was not part of `DemoDecision`.
- Out-of-scope demo fields were rejected only by generic Pydantic extra-field validation.
- Provider instructions and specialist policy did not explicitly unify commercial/product demo terms or exclude technical/video/asset demo work.

## Implementation

- Added `demo.customer_facing_concept = commercial_product_demo` to `DemoDecision`.
- Added shared constants for demo-equivalent terms, out-of-scope demo terms, and forbidden demo scope fields.
- Added conductor-boundary rejection for forbidden demo scope fields in provider envelopes, decision payloads, and nested `decision.demo`.
- Added provider instructions and policy-pack global rules that unify commercial/product demo as a sales concept and keep technical/video/asset demo work out of scope.
- Updated the reviewed conductor schema fingerprint and schema-versioning note.

This is policy/schema determinism only. It does not inspect inbound text, choose demo route by keyword, compose customer-facing copy, generate demo assets, or touch public landing/runtime paths.

## Validation

Focused test:

```powershell
python -m pytest tests/test_spec011_conductor_demo_concept.py -q
```

Result: 4 passed.

Isolated Spec 011 core/conductor suite:

```powershell
python -m pytest tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: 145 passed.

Ruff:

```powershell
python -m ruff check app/core/taliya_commercial tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_core_schemas.py tests/test_spec011_template_registry.py tests/test_spec011_schema_versioning.py
```

Result: all checks passed.

Static review:

```powershell
rg "request\.message\.text|inbound\.text|\bre\.|regex|isdigit|normalized|497|897|1497" app\core\taliya_commercial\conductor.py app\core\taliya_commercial\conductor_policy.py app\core\taliya_commercial\schemas.py app\core\taliya_commercial\template_registry.py app\core\taliya_commercial\schema_versioning.py
rg "if user says|when the message|keyword|hardcoded reply|fallback copy|customer-facing fallback|deterministic reply|safe answer|video production.*return|technical demo.*return" app\core\taliya_commercial\conductor.py app\core\taliya_commercial\conductor_policy.py app\core\taliya_commercial\schemas.py tests\test_spec011_conductor_demo_concept.py
```

Result: no matches.

## Review

- LLM-first preserved: the LLM still owns demo intent and next-step decisions in structured JSON.
- Deterministic code remained limited to schema/policy boundary validation.
- No product/demo facts were added to templates or fallback copy.
- The proof is isolated-core proof only. Demo persistence, Sales Inbox projection, renderer output, real-model transcripts, adapter cutover, and production monitoring remain later tasks.
