# T012-038 canonical mocked action-first execution slice

Date: 2026-06-11

## Scope

Ported the first canonical Spec 011 fixtures from metadata-only coverage into
no-cost action-first execution through the isolated OpenAI Agents SDK runner:

- `final-price-first`
- `final-demo-request`
- `final-human-request-silent-after`
- `spec011-rc005-rc006-rc008-simple-number-answer`

The tests load the canonical fixture IDs/messages from the real Spec 011
fixture files and run them through:

1. `TurnSituation`
2. SDK `Runner.run` with `ScriptedFakeModel`
3. `ConductorActionDecision`
4. `DecisionCompiler`
5. action validators and renderer
6. commit-after-validation state evolution

## Files

- `services/taliya-agent-runtime/tests/test_spec012_canonical_action_first_mocked.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/decision_compiler.py`

## Behavior Proven

- Price-first canonical fixture routes through the product agent, answers with
  official price facts, renders `product.price_direct` plus
  `diagnostic.price_hook`, avoids checkout/payment language, and records the
  answered obligation.
- Demo canonical fixture routes through the product agent, renders
  `product.demo_direct`, uses the official `/pilates/planos/demonstracao`
  path, avoids checkout language, and commits demo offered state.
- Human handoff canonical fixture acknowledges the handoff once, commits
  `human_status=requested`, then suppresses the next inbound with zero model
  calls.
- Simple numeric diagnostic canonical fixture starts the diagnostic, captures
  `120` as `active_students_or_size`, advances to
  `diagnostic.ask_main_pain`, and does not repeat the answered size question or
  claim misunderstanding.

## Fix Discovered By Fixture

The simple numeric canonical fixture exposed a valid Spec 011 inherited rule:
first-turn diagnostic questions must include an approved opening before the
diagnostic question. The compiler now adds `opening.cold_greeting` only when
`start_requested_diagnostic` happens from `new_lead` or `greeting_only`.
Mid-conversation diagnostic starts remain unchanged, so existing history-based
flows do not gain repeated greetings.

This is rendering/validator alignment after the LLM-selected action, not raw
lead-text commercial routing.

## Anti-Determinism Review

No regex or deterministic commercial intent classification was added. The
mocked model returns structured `ConductorActionDecision` objects; deterministic
code only expands selected actions, resolves official facts, validates, renders,
and commits state.

## Commands

- `python -m pytest tests\test_spec012_canonical_action_first_mocked.py -q`
  - `4 passed`
- `python -m pytest tests\test_spec012_decision_compiler.py tests\test_spec012_action_turn_runner.py tests\test_spec012_canonical_action_first_mocked.py -q`
  - `34 passed`
- `python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_canonical_action_first_mocked.py`
  - passed
- `python -m pytest tests\ -k spec012 -q`
  - `159 passed, 716 deselected`

## Protected Scope

No `/pilates` layout, landing visual, Sales Inbox UI, multi-tenant, client or
studio WhatsApp, checkout, or public endpoint cutover was touched.

## Paid Calls

None. All execution used `ScriptedFakeModel`; total cost remained `$0`.

## Still Open

- Expand mocked canonical execution to the remaining golden, do-not-do runtime,
  and P0 fixtures.
- Add Sales Inbox projection evidence when that isolated contract is in scope.
- Add quality-judge/repetition gates.
- Run real-model evidence only after explicit paid approval.
