# T012-038B/T012-035 Post-Waitlist Product Resume Runner Slice

Status: started / partial on 2026-06-12.

## Scope

This no-cost slice adds action-first runner coverage for a lead who already
joined the waitlist, returns after some time, and asks a product question.

The expected behavior is:

- the turn starts directly in `post_diagnostic` mode from persisted state;
- the mocked LLM selects `answer_product_question_with_saved_context`;
- the compiler answers only with the approved product template;
- the agent does not re-offer the waitlist;
- the agent does not restart or re-offer the diagnostic;
- the persisted `waitlist.joined` status, idempotency key, and joined timestamp
  are preserved into Sales Inbox projection.

No public endpoint cutover, `/pilates` visual change, Sales Inbox UI change,
checkout flow, multi-tenant work, client/studio WhatsApp work, or paid OpenAI
call was made.

## Files

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/decision_compiler.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_validators.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial/sales_inbox_projection.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`

## Behavior Covered

`test_post_waitlist_product_resume_preserves_joined_status` sets initial state
to:

- `canonical_state=waitlist_joined`;
- completed diagnostic ledger plus final diagnostic fields;
- `waitlist.status=joined`;
- historical `waitlist.idempotency_key`;
- historical `waitlist.joined_at`.

The fake SDK model emits structured `ConductorActionDecision`:

- `selected_action=answer_product_question_with_saved_context`;
- `interpreted_intents=["conversation_resume", "product_how_it_works"]`;
- `product_fact_keys_used=["how_it_works"]`.

The runner verifies:

- `starting_agent=taliya_product_agent`;
- `model_operations=1`;
- rendered templates are exactly `("product.how_it_works_direct",)`;
- no `waitlist.*` or `diagnostic.*` templates are rendered;
- rendered copy does not mention checkout or diagnostic re-offer;
- `offer_or_join_waitlist_if_eligible` is forbidden in the turn situation;
- final state preserves historical waitlist metadata;
- Sales Inbox projection exposes the historical waitlist idempotency key and
  joined timestamp.

## Implementation Notes

Two narrow operational fixes were required:

- `decision_compiler.py` now treats persisted `diagnostic.status="completed"`
  as a completed diagnostic when choosing the contextual next step for
  `product.how_it_works_direct`; previously only `delivered`/`complete` avoided
  the diagnostic CTA.
- the action-first Sales Inbox adapter/projection path now carries persisted
  `waitlist_idempotency_key` and `waitlist_joined_at` when a later turn happens
  after the waitlist was already joined. Current-turn `waitlist_joined` events
  still take precedence.

## Validation

Commands run from `C:\Users\lucas\agentes-landing-system`:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py::test_post_waitlist_product_resume_preserves_joined_status services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 3 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/app/core/taliya_commercial_sdk/decision_compiler.py services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_validators.py services/taliya-agent-runtime/app/core/taliya_commercial/sales_inbox_projection.py services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 233 passed, 716 deselected.

## Anti-Determinism Review

No raw lead-text parser, regex brain, or deterministic commercial router was
added. The product question is answered because the mocked LLM selects a
structured action and product fact key. Deterministic code only:

- interprets persisted state status values consistently;
- resolves official product facts;
- validates/renders approved templates;
- preserves persisted Sales Inbox projection metadata.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.

## Still Open

T012-038B and T012-035 remain open overall for broader resume/projection matrix,
endpoint persistence proof, real-model golden transcripts, and shadow/cutover
evidence after explicit approval.
