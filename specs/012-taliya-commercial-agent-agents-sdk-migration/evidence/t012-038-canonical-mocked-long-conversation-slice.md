# T012-038 canonical mocked long-conversation slice

Date: 2026-06-11

## Scope

Added no-cost action-first execution for the canonical golden fixture:

- `step3g-long-conversation`

The test runs the original 14-message fixture through the isolated SDK runner
with `ScriptedFakeModel` structured `ConductorActionDecision` outputs. No paid
OpenAI call was made.

## Files

- `services/taliya-agent-runtime/tests/test_spec012_canonical_action_first_mocked.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_validators.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial/renderer.py`

## Behavior Proven

- The action-first runner preserves state across price, pain/context,
  diagnostic acceptance, six ordered diagnostic answers, staged final
  diagnostic delivery, demo link, price objection, waitlist interest,
  waitlist-scoped product question, and human handoff.
- Diagnostic ledger completes all mandatory keys in order:
  `active_students_or_size`, `main_pain`, `pain_detail`, `current_process`,
  `priority`, and `urgency`.
- The final diagnostic is delivered only after urgency timing evidence is
  captured, using the full staged sequence.
- Product follow-up after delivered diagnostic can answer
  `product.how_it_works_direct` inside a waitlist flow without restarting the
  diagnostic.
- Waitlist status is preserved through the product question, and the final
  handoff pauses automation.
- Rendered output includes all official prices and the official demo link, and
  avoids `checkout`, ROI promises, repeated size question copy, and
  misunderstanding copy.

## Fixes From The Slice

- Rebuilt render-plan items after the legacy validator bridge before final
  rendering, so compiler-owned variables remain intact for the approved
  renderer.
- Changed the approved `contextual_next_step=no_cta` enum rendering from empty
  text to a neutral non-CTA sentence. This keeps `product.how_it_works_direct`
  renderable after a diagnostic is already delivered, without asking the
  diagnostic again.

## Anti-Determinism Review

No raw lead-text commercial routing, regex shortcut, or template-first
conversation understanding was added. The mocked LLM selects every semantic
action and structured slot; deterministic code only validates, renders, and
commits the selected action.

## Commands

- `python -m pytest tests\test_spec012_canonical_action_first_mocked.py::test_t012_038_mocked_canonical_step3g_long_conversation_stateful -q`
  - `1 passed`
- `python -m pytest tests\test_spec012_canonical_action_first_mocked.py -q`
  - `10 passed`
- `python -m ruff check app\core\taliya_commercial\renderer.py app\core\taliya_commercial_sdk\action_validators.py tests\test_spec012_canonical_action_first_mocked.py`
  - passed
- `python -m pytest tests\ -k spec012 -q`
  - `181 passed, 716 deselected`

## Protected Scope

No `/pilates` layout, landing visual, Sales Inbox UI, multi-tenant, client or
studio WhatsApp integration, checkout, or public endpoint cutover was touched.

## Paid Calls

None. All execution used `ScriptedFakeModel`; total cost remained `$0`.

## Still Open

- Quality judge/repetition gates.
- Sales Inbox projection artifact beyond runner state fields.
- Real-model evidence only after explicit paid approval.
