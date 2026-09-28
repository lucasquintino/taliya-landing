# Conductor T011-052 Manual Validation

Date: 2026-05-30

Task: T011-052 - Require evidence for extracted facts and numeric interpretations.

Scope: isolated Spec 011 core only. No public runtime cutover, no `/pilates` change, no WhatsApp customer/studio connection, no multi-tenant work.

## Behavior Checked

- Provider decisions that claim `facts` must include evidence on each fact.
- Provider decisions that claim `numeric_interpretations` must include evidence on each numeric interpretation.
- The same mocked turn can carry distinct numeric meanings for `497` as `plan_price` and `120` as `student_count`.
- The conductor request tells the LLM to include evidence for facts and numeric interpretations.
- The conductor/schema path validates evidence but does not parse or classify numbers from inbound text.

## Red Baseline

Command from `services/taliya-agent-runtime`:

```powershell
python -m pytest tests/test_spec011_conductor_evidence.py -q
```

Result before implementation: 3 failed, 1 passed.

Expected failures:

- Missing evidence on a claimed fact was accepted.
- Missing evidence on a numeric interpretation was accepted.
- Conductor instructions did not yet ask the LLM for evidence.

## Green Validation

Commands from `services/taliya-agent-runtime`:

```powershell
python -m pytest tests/test_spec011_conductor_evidence.py -q
python -m pytest tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
python -m ruff check app/core/taliya_commercial tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_core_schemas.py
```

Results:

- Focused evidence tests: 4 passed.
- Isolated Spec 011 core/conductor suite: 97 passed.
- Ruff: all checks passed.

## Static Review

Commands from `services/taliya-agent-runtime`:

```powershell
rg "request\.message\.text|inbound\.text|\bre\.|regex|isdigit|normalized|497|897|1497" app\core\taliya_commercial\conductor.py app\core\taliya_commercial\conductor_policy.py
rg "497|897|1497|\bre\.|regex|isdigit|normalized" app\core\taliya_commercial\schemas.py
```

Result: no matches.

## LLM-First Review

Accepted pattern:

- The LLM still owns route, role, intent, state, fact extraction, and numeric interpretation.
- Code validates the structured output only after the provider returns it.
- The code does not inspect inbound text to decide whether a number is price, student count, phone, date/time, or unknown.

Remaining later gates:

- T011-061 must validate product facts and price/student-count consistency against official context.
- T011-070..T011-074 must prove rendered text cannot turn `497` into `497 alunos`.
- T011-080+ must persist the evidence in trace/projection artifacts.
