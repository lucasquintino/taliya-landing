# T012-030B/T012-041 Turn Situation Full Anchor Slice

Status: started / partial on 2026-06-12.

## Scope

This no-cost slice strengthens the T012-041 contract gate so all current
Turn Situation Builder tests are mandatory.

No runtime behavior, prompt, renderer, endpoint, `/pilates`, checkout,
multi-tenant, Sales Inbox UI, client/studio WhatsApp, or paid OpenAI path was
changed.

## Files

- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`

## Added Contract Coverage

The T012-041 manifest now requires all current tests in
`test_spec012_turn_situation.py`, covering:

- builder signature has no raw lead-text parameter;
- empty state produces entry mode first-contact board;
- diagnostic in-progress pending key and completion gate;
- last pending diagnostic key allows completion;
- operational precedence over canonical commercial state;
- canonical states map to expected modes;
- joined waitlist blocks reoffer in post-diagnostic mode;
- post-diagnostic preamble carries compact delta context from state;
- reliable/unreliable profile name context;
- compact memory in the LLM preamble.

## Validation

Commands run from `C:\Users\lucas\agentes-landing-system`:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_turn_situation.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 12 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/tests/test_spec012_turn_situation.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 235 passed, 716 deselected.

## Anti-Determinism Review

Manifest-only reinforcement. No raw lead-text routing, commercial regex,
prompt, customer copy, or runtime behavior changed. The anchored tests preserve
the required action-first boundary: the deterministic board is built only from
persisted state and compact memory, while semantic action selection stays with
the LLM.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.

## Still Open

T012-041 remains open for the final full contract gate after endpoint/runtime
integration and approved real-model/shadow evidence.
