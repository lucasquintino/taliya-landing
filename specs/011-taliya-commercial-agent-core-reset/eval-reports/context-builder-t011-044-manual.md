# Context Builder T011-044 Manual Validation

Task: `T011-044 - Mark identity/contact facts by reliability source`.

Date: 2026-05-30.

Proof level: isolated Spec 011 core and schema proof. This does not yet prove Sales Inbox projection persistence or adapter feedback loops; those remain owned by `T011-083` and `T011-085`.

## Scope Checked

- No `/pilates` visual, layout, copy, or routing file was touched.
- No multi-tenant or client/studio WhatsApp path was touched.
- No runtime adapter, WhatsApp delivery, Sales Inbox UI, or `runtime/runner.py` code was touched.
- No commercial routing, regex, template-first decision, diagnostic state machine, price logic, waitlist logic, or demo logic was added.
- The change is limited to typed context/schema provenance for identity/contact facts.

## Red Result Before Fix

Command from `services/taliya-agent-runtime`:

```powershell
python -m pytest tests/test_spec011_identity_contact_reliability.py -q
```

Observed result before implementation:

- `3 failed`.
- Operator-provided email from `state.lead_facts` was converted to `source="memory"` and `reliability="customer_provided"`.
- A memory `first_name` with no evidence remained `customer_provided`.
- The schema accepted invalid reliable source pairs such as channel metadata marked as customer-provided.

This was the intended red failure for the observed leak class where profile/channel identity can be treated as a reliable person name.

## Implementation Result

Changed `services/taliya-agent-runtime/app/core/taliya_commercial/schemas.py`:

- Added `IDENTITY_CONTACT_FACT_KEYS`.
- Added source/reliability compatibility checks for channel metadata, operator facts, Sales Inbox projection facts, user-message facts, and product-knowledge facts.
- Required customer-provided identity/contact facts to carry evidence.
- Rejected projected identity/contact facts marked as confirmed customer/operator identity.

Changed `services/taliya-agent-runtime/app/core/taliya_commercial/context_builder.py`:

- Preserves persisted `source` and `reliability` for `state.lead_facts`.
- Defaults old-format memory facts to `source="memory"` and `reliability="customer_provided"`.
- Preserves operator-provided facts as `source="operator"` and `reliability="operator_provided"`.
- Preserves projection facts as `source="sales_inbox_projection"` with `inferred`/`unverified` reliability.
- Downgrades customer-provided identity/contact memory facts without evidence to `unverified`.
- Keeps all facts `renderable=False`.

## Manual Snapshot Scenario

Input context:

- Channel profile name: `Reliable profile first name: Ana`
- Channel WhatsApp phone and email
- Memory fact: `first_name=Ana`, `source=memory`, `reliability=customer_provided`, evidence `message:m2`
- Operator fact: `email=ana@studio.com`, `source=operator`, `reliability=operator_provided`
- Sales Inbox projection fact: `first_name=Reliable profile first name: Ana`, `source=sales_inbox_projection`, `reliability=inferred`
- Sales Inbox projection phone: `whatsapp_phone=+5511888888888`, `reliability=unverified`

Observed context behavior:

- Channel profile/contact values remain `source="channel_metadata"`, `reliability="channel_provided"`, `renderable=False`.
- Customer-provided name remains customer-provided only because it has conversation evidence.
- Operator email remains operator-provided and does not become customer-provided.
- Projected profile-name guess remains inferred.
- Projected phone remains unverified.
- No fact with value `Reliable profile first name: Ana` is marked `customer_provided`.

## Green Validation

Focused test:

```powershell
python -m pytest tests/test_spec011_identity_contact_reliability.py -q
```

Result: `3 passed`.

Nearest relevant isolated-core suite:

```powershell
python -m pytest tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `80 passed`.

Ruff:

```powershell
python -m ruff check app/core/taliya_commercial tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_core_schemas.py
```

Result: `All checks passed!`

Static review:

```powershell
rg "if .*request\.message\.text|elif .*request\.message\.text|if .*inbound\.text|elif .*inbound\.text|\bre\.|regex|detected_intents|\broute\b" app\core\taliya_commercial\context_builder.py app\core\taliya_commercial\product_knowledge.py
```

Result: no suspicious text-branching or routing patterns found in context/product helpers.

## Remaining Risk

This task proves identity/contact provenance in isolated core context. It does not yet prove that:

- the Sales Inbox projection itself is complete and consistent;
- inferred projection facts cannot loop back through adapters after cutover;
- template variables using `first_name` are validator-checked against reliability.

Those remain intentionally assigned to `T011-083`, `T011-085`, and renderer/validator tasks in Phase 6/7.
