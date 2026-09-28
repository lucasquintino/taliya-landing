# T012-038 canonical mocked do-not-do/P0 slice

Date: 2026-06-11

## Scope

Added no-cost action-first execution for seven canonical do-not-do runtime
fixtures and one safety distinction required by a do-not-do security fixture.

Executed fixtures:

- `do-not-do-early-phone-capture`
- `final-checkout-buy-intent`
- `do-not-do-date-vip-discount`
- `product-delta-integration-scope`
- `product-delta-security-data`
- `do-not-do-client-studio-whatsapp-capture`
- `spec011-rc003-price-497-not-student-count`

The tests load original Spec 011 fixture messages and run through the isolated
SDK action pipeline using `ScriptedFakeModel`:

1. `TurnSituation`
2. SDK `Runner.run`
3. `ConductorActionDecision`
4. Decision compiler
5. action validators and preserved Spec 011 validator bridge
6. renderer
7. commit-after-validation state

## Files

- `services/taliya-agent-runtime/tests/test_spec012_canonical_do_not_do_mocked.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_safety.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_safety.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial/validators.py`

## Behavior Proven

- Price question with "call me later" answers official prices and does not ask
  for name, phone, WhatsApp, or contact.
- Buy/checkout intent is routed by the structured LLM decision to waitlist,
  renders waitlist language, and avoids checkout/payment/card/PIX promises.
- Date/VIP/discount/payment-now request renders waitlist without date,
  discount, VIP, payment link, or checkout promises.
- Integration-scope question renders `product.integration_scope_direct`, says
  the topic must be confirmed, and avoids invented integration/mass-message
  claims.
- Security/LGPD/data question renders `product.security_data_direct`, mentions
  data safety, and avoids certification, guaranteed encryption/LGPD, or audit
  claims.
- Studio WhatsApp connection question answers product WhatsApp scope and avoids
  asking for number, code, QR code, or promising immediate connection.
- `497` in "plano de 497" is not interpreted as active students; no `497
  alunos/estudantes` language appears.

## Fixes Discovered By Fixtures

- Safety preguard now distinguishes a security policy question
  ("posso mandar dados dos alunos?") from actual sensitive-data submission. CPF
  and direct sensitive-data submissions remain blocked.
- `product.security_data_direct` is registered as an official static product
  template for the preserved Spec 011 corroboration validator, matching the
  existing treatment of `product.integration_scope_direct`,
  `product.how_it_works_direct`, and `product.price_objection_value`.

## Anti-Determinism Review

No regex or raw-message commercial router was added. The tests use scripted
structured model decisions. Deterministic code remains limited to safety
boundary distinction, official-template corroboration, validation, rendering,
and state commit after validation.

## Commands

- `python -m pytest tests\test_spec012_canonical_do_not_do_mocked.py -q`
  - `7 passed`
- `python -m pytest tests\test_spec012_canonical_do_not_do_mocked.py tests\test_spec012_action_safety.py -q`
  - `14 passed`
- `python -m ruff check app\core\taliya_commercial_sdk\action_safety.py app\core\taliya_commercial\validators.py tests\test_spec012_action_safety.py tests\test_spec012_canonical_do_not_do_mocked.py`
  - passed
- `python -m pytest tests\ -k spec012 -q`
  - `172 passed, 716 deselected`

## Protected Scope

No `/pilates` layout, landing visual, Sales Inbox UI, multi-tenant, client or
studio WhatsApp integration, checkout, or public endpoint cutover was touched.

## Paid Calls

None. All execution used `ScriptedFakeModel`; total cost remained `$0`.

## Still Open

- Remaining P0 mocked execution:
  - `spec011-rc001-rc002-internal-metadata-leak`
  - `spec011-rc004-urgency-before-final`
  - `spec011-rc007-valid-short-answer-does-not-stall`
  - `spec011-rc009-final-diagnostic-not-truncated`
  - `spec011-rc012-final-diagnostic-plain-studio-language`
  - `spec011-rc013-sales-inbox-projection-consistency`
  - `spec011-rc014-false-pass-protection`
- Remaining do-not-do runtime fixture:
  - `do-not-do-wrong-student-language`
- Long conversation canonical fixture.
- Quality judge/repetition gates.
- Sales Inbox projection evidence when isolated projection proof is in scope.
- Real-model proof only after explicit paid approval.
