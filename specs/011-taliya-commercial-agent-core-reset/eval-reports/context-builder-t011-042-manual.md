# Context Builder T011-042 Manual Validation

Date: 2026-05-30

Scope: isolated Spec 011 Context Builder. This validates Spec 006-derived product contract retrieval as context only. It does not validate the future conductor, validators, renderer, adapters, or production cutover.

## Inputs

- Price-style inbound: `quanto custa?`
- Pain-style inbound: `tenho faltas e vendas baguncadas`
- Missing Spec 006 contract key: `calendar_live_write`

## Observed Output

Default Spec 006 contract refs for both price-style and pain-style inbound:

```text
spec006.product_positioning
spec006.plan_entitlements
spec006.operating_modes
spec006.setup_scope
spec006.access_subscription
spec006.navigation_routes
```

Observed source evidence:

```text
spec006.product_positioning -> specs/006-crm-operational-core/spec.md#Product Positioning
spec006.plan_entitlements -> specs/006-crm-operational-core/agent-plan-entitlements.pt-BR.md#Regra central
spec006.operating_modes -> specs/006-crm-operational-core/operating-modes.md
spec006.setup_scope -> specs/006-crm-operational-core/setup-initial-configuration-scope.pt-BR.md#O Que O Setup Inicial Deve Configurar
spec006.access_subscription -> specs/006-crm-operational-core/access-subscription-pending-confirmation-approved.pt-BR.md#Papel Da Tela, specs/006-crm-operational-core/access-subscription-confirmed-setup-approved.pt-BR.md#Papel Da Tela
spec006.navigation_routes -> specs/006-crm-operational-core/final-navigation-web-app.pt-BR.md#Pre-CRM
```

Missing fact result:

```text
spec006.calendar_live_write -> missing=True, value=None, excerpt=None
```

State comparison:

```text
same_spec006_default_keys=True
state_unchanged=True
```

## Review

- Spec 006 contract refs come from `specs/006-crm-operational-core/` source files.
- Retrieval does not inspect `request.message.text`.
- Retrieval does not set route, intent, template, diagnostic action, waitlist action, or demo action.
- The context now carries official product knowledge plus Spec 006 product contract refs in the same `TurnContext.product_knowledge` field.
- Each Spec 006 ref has source path/heading evidence and a content-derived version hash for later validators/debugging.

## Commands

```powershell
python -m pytest tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: 74 passed.

```powershell
python -m ruff check app/core/taliya_commercial tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_core_schemas.py
```

Result: all checks passed.

```powershell
rg -n "request\.message\.text|normalize_text|regex|template_id|diagnostic_action|waitlist_allowed|current_state|next_state" app/core/taliya_commercial/product_knowledge.py
```

Result: no matches.

