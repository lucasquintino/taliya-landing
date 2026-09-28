# T012-040 Slice - Hardcoded Promise Static Audit

Date: 2026-06-11

## Scope

Advanced T012-040 with a no-cost static audit for unsafe hardcoded promises in
the action-first prompt/copy surface.

Covered promise classes:

- checkout/payment-now promises;
- discount/VIP promises;
- guaranteed availability/date/opening promises;
- guaranteed integration/migration/setup promises;
- guaranteed certification/encryption/LGPD claims.

This is a static guard only. It does not add public endpoint cutover, runtime
commercial routing, or paid OpenAI calls.

## Sources

- `specs/012-taliya-commercial-agent-agents-sdk-migration/static-anti-drift-audit.md`
  - blocks product prices, discounts, checkout URLs, launch dates, or
    availability hardcoded in prompts/templates/fallbacks.
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/product-followup-delta-contract.md`
  - forbids checkout/date/discount/VIP promises, unsupported integration
    promises, and invented security/LGPD/certification claims.
- `.agents/skills/taliya-llm-first-agent/SKILL.md`
  - deterministic checks may guard official facts/promises; they must not
    become commercial understanding.

## Files Changed

- `services/taliya-agent-runtime/tests/test_spec012_static_audit.py`

## Behavior

The static audit now scans the action-first agent prompt/copy surfaces:

- `app/core/taliya_commercial_sdk/action_agents.py`;
- `app/core/taliya_commercial/renderer.py`.

It looks for positive promise fragments such as `checkout aberto`, `link de
pagamento`, `desconto garantido`, `data garantida`, `integracao garantida`,
`migracao automatica`, `certificacao garantida`, `criptografia garantida`, and
`lgpd garantida`.

The scan intentionally does not block negative guardrail language such as
"never promise checkout" or "nao mandar pagamento"; those are required safety
instructions/copy.

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_static_audit.py -q`
  - result: 6 passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 202 passed, 716 deselected
- `python -m ruff check tests\test_spec012_static_audit.py`
  - result: all checks passed

## Anti-Determinism Review

This is static validation only. It does not inspect lead messages, classify
commercial meaning, or route any conversation. It only blocks future prompt/copy
drift that would bypass official-fact validators.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, public
endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None.

## Still Open

T012-040 remains open for the full verification phase and must be revisited
after T012-031/T012-036 introduce any feature-flagged endpoint, runtime API,
or delivery integration changes.
