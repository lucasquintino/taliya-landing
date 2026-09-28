# T012-036 Slice - Isolated Per-Conversation Cost Cap

Date: 2026-06-11

## Scope

Started T012-036 with a per-conversation cost cap in the isolated action-first
runner.

Implemented behavior:

- `run_action_conversation(..., max_total_cost_usd=0.30)` has a default hard
  cap aligned with `design-lock-v2-action-first.md`;
- when accumulated measured cost reaches the cap, the next inbound is deferred
  without calling the SDK;
- the deferred turn records `mode = cost_cap`, `status = deferred`,
  `llm_called = False`, and issue `cost_budget_exceeded`;
- `ActionConversationReport` records `cost_cap_usd` and
  `cost_cap_exceeded`;
- local harnesses can pass `max_total_cost_usd=None` to disable the cap when
  generating no-cost evidence.

This slice does not implement endpoint HMAC/idempotency/turn gate integration.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_turn_runner.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-036-isolated-cost-cap-slice.md`

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_action_turn_runner.py -q`
  - result: 8 passed
- `python -m ruff check app\core\taliya_commercial_sdk\action_turn_runner.py tests\test_spec012_action_turn_runner.py`
  - result: all checks passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 219 passed, 716 deselected

## Anti-Determinism Review

This is operational cost control only. It does not inspect raw lead text, choose
commercial actions, alter prompts, or render new customer copy. Commercial
understanding still goes through the LLM when the cap allows a turn to run.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, public
endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None. Cost: `$0`.

## Still Open

T012-036 remains open for public runtime API/HMAC/idempotency/turn-gate
integration and end-to-end endpoint proof after that scope is explicitly
allowed. This slice proves the isolated runner cost cap.
