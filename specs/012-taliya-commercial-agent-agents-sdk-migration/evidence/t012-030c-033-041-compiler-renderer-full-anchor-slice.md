# T012-030C/T012-033/T012-041 Compiler Renderer Full Anchor Slice

Status: started / partial on 2026-06-12.

## Scope

This no-cost slice strengthens the T012-041 contract gate so all current
decision-compiler and renderer-over-compiler tests are mandatory.

No runtime behavior, prompt, endpoint, `/pilates`, checkout, multi-tenant,
Sales Inbox UI, client/studio WhatsApp, or paid OpenAI path was changed.

## Files

- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`

## Added Contract Coverage

The manifest now requires all current tests in:

- `test_spec012_decision_compiler.py`
- `test_spec012_renderer_compiler.py`

This includes anchors for:

- compiler signature has no lead-text parameter;
- compiler-owned official variables for price answers;
- T011-105 regression where actions without required composition fail;
- diagnostic ledger merge, next-question sequencing, and staged final sequence;
- handoff pause patch and handoff reason;
- delta product contract keys: how-it-works, comparison, security/data,
  integration, availability/onboarding, and out-of-profile;
- no checkout/date promise on availability;
- diagnostic correction, multiple answers, messy price interruption, messy demo;
- price objection mid-diagnostic;
- product-question interruption matrix during diagnostic;
- resume after days and post-diagnostic memory;
- post-diagnostic price resume without diagnostic restart;
- waitlist resume and demo resume;
- diagnostic refusal answering price without reoffering diagnostic;
- profile name policy and ask-name-at-diagnostic-entry;
- every `TurnAction` explicitly compiled;
- template-group boundary flags out-of-mode templates;
- renderer accepts compiler plans for diagnostic-entry name question,
  compiler-owned how-it-works enum, and staged final diagnostic.

## Validation

Commands run from `C:\Users\lucas\agentes-landing-system`:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_decision_compiler.py services/taliya-agent-runtime/tests/test_spec012_renderer_compiler.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 38 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/tests/test_spec012_decision_compiler.py services/taliya-agent-runtime/tests/test_spec012_renderer_compiler.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 235 passed, 716 deselected.

## Anti-Determinism Review

Manifest-only reinforcement. No raw lead-text parser, commercial regex,
prompt, customer copy, or runtime behavior changed. These anchors preserve the
LLM-first boundary: the LLM chooses structured action JSON; the compiler expands
state/templates/facts and the renderer renders only approved plans.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.

## Still Open

T012-041 remains open for the final full contract gate after endpoint/runtime
integration and approved real-model/shadow evidence.
