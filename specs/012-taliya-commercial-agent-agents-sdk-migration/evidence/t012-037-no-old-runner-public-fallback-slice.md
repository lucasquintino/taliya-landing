# T012-037 No Old Runner Public Fallback Slice

Status: completed on 2026-06-15.

## Scope

This no-cost slice proves the current public Taliya commercial entry points do
not fall back to the old TypeScript v2 commercial engine while the Spec 012
action-first SDK path is being integrated.

No runtime behavior, `/pilates` visual/copy/layout, Sales Inbox UI, checkout,
multi-tenant, client/studio WhatsApp, shadow traffic, or public cutover was
changed.

## Files

- `services/taliya-agent-runtime/tests/test_spec012_static_audit.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`
- `lib/landing/ai-attendant/runtime-client.ts` (read-only audit target)
- `app/api/landing/ai-attendant/whatsapp/route.ts` (read-only audit target)

## Added Static Proof

- `runTaliyaCommercialRuntimeTurn` calls the runtime endpoint resolver and does
  not call `/v1/agent-runs` for commercial turns.
- The commercial runtime endpoint resolver returns
  `/v1/taliya-commercial/turn`.
- The public runtime client does not import or call old TS v2 commercial runner
  fragments such as `agent-v2-loop`, `agent-v2-semantic-interpreter`,
  `agent-v2-diagnostic`, `runAgentV2`, `runFloatingAgent`, or `runLegacy`.
- The WhatsApp public route delegates commercial turns through
  `runTaliyaCommercialRuntimeTurn`.
- The only allowed `agent-v2` import in the WhatsApp route is the existing
  idempotency helper; it is not a commercial fallback engine.
- The T012-041 no-cost contract gate now anchors these T012-037 tests.

## Validation

Commands run from `C:\Users\lucas\agentes-landing-system`:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_static_audit.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 13 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/app/core/taliya_commercial_sdk/runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_runtime_adapter.py services/taliya-agent-runtime/tests/test_spec012_static_audit.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 240 passed, 716 deselected.

## Anti-Determinism Review

This is a static boundary test only. It does not add raw lead-text parsing,
commercial regex routing, customer copy, or a fallback answer path. The public
adapter remains a transport layer to `/v1/taliya-commercial/turn`; commercial
meaning stays inside the action-first SDK runtime path.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.
