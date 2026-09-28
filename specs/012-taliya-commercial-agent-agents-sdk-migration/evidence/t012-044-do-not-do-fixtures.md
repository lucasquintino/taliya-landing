# T012-044 do-not-do fixtures

- Date: 2026-06-16
- Scope: Spec 012 action-first SDK path only
- Paid OpenAI calls: none
- Public cutover: none
- Protected surfaces changed: none

## Result

T012-044 passed for the Spec 012 action-first/no-cost fixture gate.

The canonical do-not-do fixtures were executed through the mocked SDK/action
conversation path, with safety guardrails included. The run covered the
forbidden behavior cells that must stay blocked before shadow mode:

- no early phone/name/WhatsApp capture after a price question;
- no checkout, payment link, card, Pix, VIP, discount, special condition, or
  guaranteed entry date;
- no invented integrations or automatic Instagram/system connections;
- no certification, encryption, audit, or LGPD guarantee claims beyond official
  facts;
- no client/studio WhatsApp connection capture or QR/code request;
- no lay-lead wording regression such as treating students as generic
  consumers;
- no interpreting plan price `497` as `497 alunos`;
- prompt injection, unsupported media, sensitive data, and medical/health advice
  outside scope are blocked before SDK/model execution.

## Verification

```powershell
python -m pytest -q services/taliya-agent-runtime/tests/test_spec012_canonical_do_not_do_mocked.py services/taliya-agent-runtime/tests/test_spec012_action_safety.py
```

Result:

```text
19 passed in 2.44s
```

```powershell
python -m pytest -q services/taliya-agent-runtime/tests/test_spec012_canonical_fixture_port.py services/taliya-agent-runtime/tests/test_spec012_canonical_do_not_do_mocked.py services/taliya-agent-runtime/tests/test_spec012_action_safety.py
```

Result:

```text
23 passed in 2.36s
```

```powershell
python -m pytest -q services/taliya-agent-runtime/tests -k spec012
```

Result:

```text
274 passed, 716 deselected in 14.88s
```

```powershell
python -m ruff check services/taliya-agent-runtime/tests/test_spec012_canonical_do_not_do_mocked.py services/taliya-agent-runtime/tests/test_spec012_action_safety.py
```

Result:

```text
All checks passed!
```

## Out-of-scope legacy note

An exploratory broad selector was also run:

```powershell
python -m pytest -q services/taliya-agent-runtime/tests -k "do_not_do or safety_guardrail"
```

That selector intentionally reaches outside Spec 012 and includes legacy Spec
011 tests. It returned 24 passed and 1 failed in
`test_spec011_mocked_conductor_fixtures.py` for
`do-not-do-wrong-student-language`, because the legacy Spec 011 adapter fixture
still sends `product_fact_summary` to `product.whatsapp_direct` while the Spec
012 SDK/action-first path now uses the hardened approved WhatsApp copy.

This is not a T012-044 blocker because:

- AGENTS.md explicitly says not to implement Spec 011;
- T012-044 is closing the Spec 012 action-first SDK path;
- the equivalent Spec 012 canonical do-not-do fixture passed;
- the full Spec 012 suite passed after the check.

The legacy failure is recorded here so it is visible and not mistaken for a
hidden green run.

## Anti-determinism Review

No runtime code was changed for this closure. The passing do-not-do checks use
mocked structured LLM decisions and validate/render approved templates through
the action-first SDK path. Deterministic behavior remains limited to safety
boundaries, validators, rendering, fixture verification, and cost/test gates.

No raw lead-text commercial routing, regex brain, public fallback, direct SDK
free-text delivery, endpoint cutover, `/pilates` visual change, checkout,
Sales Inbox UI, multi-tenant work, or client/studio WhatsApp connection work was
introduced.

## Closure

T012-044 is closed for the no-cost Spec 012 verification gate. The next allowed
task is T012-045, exporting mandatory trace evidence.
