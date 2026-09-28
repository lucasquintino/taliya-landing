# T012-032 / T012-040 Slice - Validator Voice, Adequacy, Static Audit

Date: 2026-06-11

## Scope

No-cost, isolated action-first validator/static-audit slice.

Implemented/covered:

- internal/source label leak in action-first rendered variables;
- no CRM jargon for lay leads unless the lead used the term;
- rejected final-diagnostic wording;
- thin-context `pelo que voce contou` block;
- price answer adequacy map for messy input `qto fica?`;
- integration-scope question must be answered before handoff;
- waitlist checkout/discount/VIP promise block;
- partial T012-040 static audit:
  - no regex/raw-text commercial brain in action core;
  - no public old-runner fallback in isolated action runner;
  - no direct SDK free-text delivery;
  - no SDK commit tools during reasoning.

## Sources

- `implementation-source-discipline.md`: no source, no implementation.
- `conformity-matrix.pt-BR.md`: maps voice/banned/CRM/answer-adequacy and
  anti-determinism boundaries to T012-032 and T012-040.
- `design-lock-v2-action-first.md`: no CRM for lay leads; thin-context
  `pelo que voce contou` block; action-first architecture.
- `conformidade-contratos-binding-2026-06-10.pt-BR.md`: validators own voice
  rules including no CRM for lay leads and banned phrases.
- Spec 010:
  - `behavior-contract.md`: blocks `pelo que voce contou` when facts are thin.
  - `contracts/tools-and-guardrails.md`: evidence framing requires evidence.
- Spec 011 tests:
  - `tests/test_spec011_validators_leak_banned_phrases.py`;
  - `tests/test_spec011_validators_core.py`;
  - `tests/test_spec011_validators_product_claims.py`;
  - `tests/test_spec011_conductor_language_policy.py`.
- Spec 012 contracts:
  - `spec.md` FR-012-024 and FR-012-030;
  - `tool-catalog.md` read-only/proposal-only/commit-after-validation rules;
  - `static-anti-drift-audit.md` forbidden regression list.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_validators.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_validators_ported.py`
- `services/taliya-agent-runtime/tests/test_spec012_static_audit.py`

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_action_validators_ported.py -q`
  - result: 13 passed
- `python -m pytest tests\test_spec012_static_audit.py -q`
  - result: 4 passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 124 passed, 716 deselected
- `python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_action_validators_ported.py tests\test_spec012_static_audit.py`
  - result: all checks passed

## Anti-Determinism Review

No raw lead-text commercial routing was added.

The added deterministic checks are validation/static-audit boundaries:

- text that is already selected for rendering is blocked when it violates
  voice/safety contracts;
- raw-text inspection is limited to whether the lead themselves used `CRM`,
  which is a validator exception for jargon, not a route/intent decision;
- static audit tests scan source for forbidden architectural regressions.

The LLM still selects the action and commercial meaning through structured
`ConductorActionDecision`.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, or
client/studio WhatsApp files were edited by this slice.

## Paid Calls

None. All tests are mocked/no-cost/local.

## Still Open

- T012-032B full delta contract coverage for all product keys/templates:
  `how_it_works`, `whatsapp_scope`, `integration_scope`,
  `security_and_data`, `availability_and_onboarding`, `out_of_profile`;
- T012-032C full SDK-path safety guardrail implementation:
  prompt injection, unsupported media, sensitive data, medical/health advice;
- T012-038/038B canonical fixture port and messy-input suite expansion;
- broader T012-040 audit against endpoint/public-cutover surfaces once those
  surfaces are in scope.
