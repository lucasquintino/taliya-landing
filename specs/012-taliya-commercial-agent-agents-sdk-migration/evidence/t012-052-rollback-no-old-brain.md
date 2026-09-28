# T012-052 rollback without old deterministic commercial brain

- Date: 2026-06-16
- Scope: runtime flags and API routing
- Paid OpenAI calls: none
- Public activation: none

## Result

T012-052 passed.

The runtime already exposes the required rollback shape for this migration:

- `TALIYA_SPEC012_ACTION_FIRST_ENABLED=true` routes `/v1/taliya-commercial/turn`
  to the Spec 012 action-first SDK adapter.
- If `TALIYA_AGENT_PROVIDER=openai`, the Spec 012 adapter blocks paid calls
  without explicit paid approval.
- If the Spec 012 flag is off and
  `TALIYA_SPEC011_COMMERCIAL_CORE_ENABLED=false`, the API returns an operational
  error instead of calling the old Spec 011 commercial core.
- `/v1/agent-runs` remains quarantined for public Taliya commercial turns.

This proves the rollback/disabling behavior does not restore the old commercial
brain as a public fallback.

## Verification

```powershell
python -m pytest -q services/taliya-agent-runtime/tests/test_agent_runs_api.py services/taliya-agent-runtime/tests/test_settings.py services/taliya-agent-runtime/tests/test_spec012_static_audit.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result:

```text
28 passed in 2.58s
```

```powershell
python -m ruff check services/taliya-agent-runtime/app/main.py services/taliya-agent-runtime/app/settings.py services/taliya-agent-runtime/tests/test_agent_runs_api.py services/taliya-agent-runtime/tests/test_settings.py
```

Result:

```text
All checks passed!
```

## Key Assertions

- `test_spec011_core_disabled_returns_operational_error_without_running_core`
  monkeypatches the old core to raise if called. The API returns
  `spec011_core_disabled` and the monkeypatched old core is not invoked.
- `test_agent_run_keeps_legacy_endpoint_quarantined_when_spec011_core_disabled`
  keeps `/v1/agent-runs` unavailable for commercial turns.
- `test_spec012_action_first_flag_routes_to_sdk_adapter_without_public_cutover`
  proves the Spec 012 flag routes to the SDK adapter and does not call the old
  core.
- `test_spec012_action_first_flag_blocks_openai_without_paid_approval` proves
  paid OpenAI provider calls stay blocked.

## Anti-Determinism Review

This is a runtime/operational rollback proof only. It does not add raw lead-text
commercial routing, regex/state-machine interpretation, direct SDK text
delivery, or an old-runner fallback.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant,
client/studio WhatsApp, public activation, or paid OpenAI work was changed.

## Closure

T012-052 is closed. The next task is T012-053 production preflight, still with no
public activation and no paid OpenAI calls unless explicitly approved later.
