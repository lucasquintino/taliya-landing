# T012-032/T012-041 Validator Full Anchor Slice

Status: started / partial on 2026-06-12.

## Scope

This no-cost slice strengthens the T012-041 contract gate so the current
T012-032 action-first validator coverage is mandatory, not partially sampled.

No runtime behavior, prompt, renderer, endpoint, `/pilates`, checkout,
multi-tenant, Sales Inbox UI, client/studio WhatsApp, or paid OpenAI path was
changed.

## Files

- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`

## Added Contract Coverage

The contract gate now requires all current tests in:

- `test_spec012_action_validators.py`
- `test_spec012_action_validators_ported.py`

This includes anchors for:

- price hook requirement;
- invented demo link block;
- waitlist from demo curiosity block;
- internal/source label leak block;
- no CRM jargon for lay leads and CRM allowed when the lead used the term;
- rejected final-diagnostic phrase block;
- thin-context `pelo que voce contou` block;
- waitlist checkout/discount promise block;
- price answer adequacy for messy `qto fica?`;
- integration-scope direct answer before handoff;
- valid waitlist offer for contract intent;
- demo offer requiring demo template;
- handoff reason/ack template requirement;
- valid handoff pause patch;
- approved diagnostic-entry name question exception.

## Validation

Commands run from `C:\Users\lucas\agentes-landing-system`:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_action_validators.py services/taliya-agent-runtime/tests/test_spec012_action_validators_ported.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 20 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/tests/test_spec012_action_validators.py services/taliya-agent-runtime/tests/test_spec012_action_validators_ported.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 235 passed, 716 deselected.

## Anti-Determinism Review

Manifest-only reinforcement. No raw lead text parser, commercial route regex,
prompt, template, customer copy, or runtime behavior changed. These tests keep
deterministic validators in their allowed role: post-LLM guardrails after a
structured action decision.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.

## Still Open

T012-041 remains open for the final full contract gate after endpoint/runtime
integration and approved real-model/shadow evidence. T012-032 remains closed as
a validator port overall, but future endpoint integration may still require
re-running these anchors.
