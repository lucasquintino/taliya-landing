# T012-038 canonical mocked golden expansion slice

Date: 2026-06-11

## Scope

Expanded the no-cost canonical Spec 011 action-first execution set from 4 to 9
fixtures in the isolated OpenAI Agents SDK runner.

Newly executed canonical fixtures:

- `final-price-plus-pain`
- `final-pain-first`
- `final-instagram-interest`
- `final-whatsapp-question`
- `final-waitlist-joined`

Already covered in the previous slice and still passing:

- `final-price-first`
- `final-demo-request`
- `final-human-request-silent-after`
- `spec011-rc005-rc006-rc008-simple-number-answer`

All tests load original fixture messages/IDs and use `ScriptedFakeModel` to
return structured `ConductorActionDecision` objects. No runtime code classifies
raw lead text commercially.

## Files

- `services/taliya-agent-runtime/tests/test_spec012_canonical_action_first_mocked.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/decision_compiler.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_validators.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial/renderer.py`
- `services/taliya-agent-runtime/app/shared/product_knowledge/source.py`

## Behavior Proven

- Price plus pain answers price first, uses official plan facts, and renders
  `diagnostic.price_hook_with_context` with grounded `plan_fit_context`.
- Pain-first opening renders approved greeting, `diagnostic.offer_soft`, and
  `diagnostic.ask_active_students`, satisfying the Spec 011 route/first
  diagnostic question rule.
- Instagram/source opening renders `opening.instagram_source` without leaking
  `utm_source`, `source_label`, or internal/source labels, while preserving the
  diagnostic offer state for validators/Sales Inbox consistency.
- WhatsApp scope renders the official PT-BR product fact: student does not need
  to download an app or create a password; Taliya updates the panel and alerts
  the responsible person; official demo path is included; no phone request.
- Waitlist contract intent can be accepted from entry mode only when the model
  structurally marks `waitlist_intent=contract_intent`; the second turn joins
  the waitlist with captured `studio_name` and `city_state`; no checkout, VIP,
  or discount language is rendered.

## Fixes Discovered By Fixtures

- `answer_direct_product_question` with `plan_fit_context` now chooses
  `diagnostic.price_hook_with_context` instead of the generic price hook.
- The legacy validator bridge now marks contextual price hook as
  `diagnostic.action=offer`.
- First-contact `offer_diagnostic_from_pain` now renders greeting + soft offer
  + first diagnostic question. Existing non-first-contact offer fixtures remain
  unchanged.
- The legacy route bridge now treats `offer_diagnostic_from_pain` as a
  diagnostic route.
- Source-opening templates that offer the diagnostic are bridged as
  `diagnostic.action=offer`.
- `waitlist_intent=contract_intent` allows waitlist templates from entry mode
  without adding raw-text waitlist routing.
- Captured waitlist slots now populate `waitlist.joined` variables.
- `waitlist.offer_after_contract_intent` no longer renders the blocked word
  `checkout`; it says no immediate entry/date/special condition instead.
- Official `whatsapp_scope` product knowledge was updated to the validator-
  required PT-BR facts and line-wrapped.

## Anti-Determinism Review

No regex, token list, or raw-message commercial router was added. The LLM/mock
still selects the action and structured fields. Deterministic code only:

- expands a selected action into templates/state;
- bridges selected action/templates into the preserved Spec 011 validator
  shape;
- resolves official product facts;
- renders approved templates;
- commits validated state.

## Commands

- `python -m pytest tests\test_spec012_canonical_action_first_mocked.py -q`
  - `9 passed`
- `python -m pytest tests\test_spec012_decision_compiler.py tests\test_spec012_action_turn_runner.py tests\test_spec012_canonical_action_first_mocked.py tests\test_spec012_action_validators_ported.py -q`
  - `52 passed`
- `python -m ruff check app\core\taliya_commercial_sdk app\core\taliya_commercial\renderer.py app\shared\product_knowledge\source.py tests\test_spec012_canonical_action_first_mocked.py`
  - passed
- `python -m pytest tests\ -k spec012 -q`
  - `164 passed, 716 deselected`

## Protected Scope

No `/pilates` layout, landing visual, Sales Inbox UI, multi-tenant, client or
studio WhatsApp integration, checkout, or public endpoint cutover was touched.

## Paid Calls

None. All execution used `ScriptedFakeModel`; total cost remained `$0`.

## Still Open

- Mocked execution for remaining do-not-do runtime and P0 fixtures.
- Long conversation canonical fixture expansion.
- Quality judge/repetition gates.
- Sales Inbox projection evidence when isolated projection proof is in scope.
- Real-model evidence only after explicit paid approval.
