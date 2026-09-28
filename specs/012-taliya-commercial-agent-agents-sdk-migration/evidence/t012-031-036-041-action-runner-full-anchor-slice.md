# T012-031/T012-036/T012-041 Action Runner Full Anchor Slice

Status: started / partial on 2026-06-12.

## Scope

This no-cost slice strengthens the T012-041 contract gate so all current
isolated action-turn runner tests are mandatory.

No endpoint integration, runtime public cutover, prompt, renderer, `/pilates`,
checkout, multi-tenant, Sales Inbox UI, client/studio WhatsApp, or paid OpenAI
path was changed.

## Files

- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`

## Added Contract Coverage

The T012-041 manifest now requires all current tests in
`test_spec012_action_turn_runner.py`, covering:

- official fact resolver for real product knowledge;
- delta product summary selection;
- `routine_areas` fact selection;
- paid calls blocked without approval;
- multi-turn full-funnel state evolution;
- validator repair loop;
- per-conversation cost cap deferral without SDK call;
- local-harness cost-cap disable escape;
- routine areas no-cost product answer;
- post-diagnostic messy price resume;
- diagnostic availability interruption;
- diagnostic correction;
- multiple diagnostic answers in one message;
- price objection during diagnostic;
- waitlist pending product question;
- post-diagnostic demo resume;
- diagnostic refusal answering price without reoffering diagnostic;
- post-waitlist product resume preserving joined status;
- parroting composition blocked.

## Validation

Commands run from `C:\Users\lucas\agentes-landing-system`:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 21 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 235 passed, 716 deselected.

## Anti-Determinism Review

Manifest-only reinforcement. No raw lead-text parser, commercial regex,
prompt, customer copy, or runtime behavior changed. The anchored runner tests
continue to use mocked structured LLM decisions and verify that deterministic
code only resolves official facts, validates, renders, traces, commits after
validation, and applies operational cost/safety boundaries.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.

## Still Open

T012-031/T012-036 remain open for public endpoint feature-flag integration,
HMAC/idempotency/turn-gate preservation, and runtime proof. T012-041 remains
open for the final full contract gate after endpoint/runtime integration and
approved real-model/shadow evidence.
