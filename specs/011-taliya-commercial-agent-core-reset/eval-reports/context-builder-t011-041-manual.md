# Context Builder T011-041 Manual Validation

Date: 2026-05-30

Scope: isolated Spec 011 Context Builder. This validates official product knowledge retrieval as context only. It does not validate the future conductor, validators, renderer, adapters, or production cutover.

## Inputs

- Price-style inbound: `quanto custa?`
- Pain-style inbound: `minha agenda e reposicoes estao baguncadas`
- Missing-fact requested key: `integration_calendar`

## Observed Output

Default product knowledge keys for both price-style and pain-style inbound:

```text
plans
prices
plan_comparison
links
demo_status
waitlist_status
checkout_status
availability
unsupported_claims
```

Both default contexts used the same source version:

```text
taliya-commercial-2026-05-22
```

Missing fact result:

```text
integration_calendar -> missing=True, value=None, excerpt=None
```

State comparison:

```text
same_default_keys=True
state_unchanged=True
```

## Review

- Product knowledge comes from `services/taliya-agent-runtime/app/shared/product_knowledge/source.py`.
- Retrieval does not inspect `request.message.text`.
- Retrieval does not set route, intent, template, diagnostic action, waitlist action, or demo action.
- The context now carries structured values plus source version/evidence for later validators.
- Product-followup delta keys such as `how_it_works` are not pulled into every default turn; they remain explicit requested keys for later phases.

## Commands

```powershell
python -m pytest tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: 71 passed.

```powershell
python -m ruff check app/core/taliya_commercial tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_core_schemas.py
```

Result: all checks passed.

```powershell
rg -n "normalize_text|request\.message\.text|route|intent|template_id|diagnostic|waitlist|demo|preco|custa|plano|planos|regex|re\." app/core/taliya_commercial/product_knowledge.py
```

Result: no message-text/route/template/regex commercial branching in the retrieval helper.

