# T012-041/T012-046 Joined Waitlist Projection Export Slice

Status: started / partial on 2026-06-12.

## Scope

This no-cost slice strengthens the Sales Inbox projection evidence package for
the action-first SDK path.

It covers a lead who already joined the waitlist, returns later, and asks a
product question. The exported package must preserve the historical waitlist
join metadata so Sales Inbox can distinguish:

- waitlist offered;
- waitlist pending details;
- waitlist joined on the current turn;
- waitlist already joined before the current turn.

No public endpoint cutover, Sales Inbox UI change, `/pilates` visual change,
checkout, multi-tenant work, client/studio WhatsApp work, or paid OpenAI call
was made.

## Files

- `services/taliya-agent-runtime/tests/test_spec012_sales_inbox_projection.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`

## Added Coverage

`test_t012_046_exports_joined_waitlist_projection_history` runs a mocked
action-first conversation with:

- `canonical_state=waitlist_joined`;
- `diagnostic.status=completed`;
- complete diagnostic ledger and final diagnostic fields;
- `waitlist.status=joined`;
- historical `waitlist.idempotency_key`;
- historical `waitlist.joined_at`.

The mocked SDK model emits structured `ConductorActionDecision`:

- `selected_action=answer_product_question_with_saved_context`;
- `interpreted_intents=["conversation_resume", "product_how_it_works"]`;
- `product_fact_keys_used=["how_it_works"]`.

The exported `012.sales_inbox_projection_export.v1` package asserts:

- `projection_complete=True`;
- one delivered turn has one projection;
- no missing required fields;
- `commercial_stage=post_diagnostic_questions`;
- `diagnostic_status=completed`;
- `waitlist_status=joined`;
- `template_ids=["product.how_it_works_direct"]`;
- `waitlist_idempotency_key=waitlist:joined:historical`;
- `waitlist_joined_at=2026-06-01T12:00:00Z`;
- `operator_next_action=monitor_waitlist`.

The T012-041 contract gate now requires this anchor.

## Validation

Commands run from `C:\Users\lucas\agentes-landing-system`:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_sales_inbox_projection.py::test_t012_046_exports_joined_waitlist_projection_history services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 3 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/tests/test_spec012_sales_inbox_projection.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 234 passed, 716 deselected.

## Anti-Determinism Review

This is export-package coverage only. It does not add raw lead-text parsing,
keyword routing, commercial regex, new customer copy, or template-first
behavior. The mocked LLM still chooses the structured action and product fact
key; deterministic code packages the validated projection.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.

## Still Open

T012-046 remains open overall for final endpoint persistence/integration,
real-model golden transcripts, shadow/cutover evidence, and product-owner
approval. T012-041 remains open for the final full contract gate after those
runtime integrations exist.
