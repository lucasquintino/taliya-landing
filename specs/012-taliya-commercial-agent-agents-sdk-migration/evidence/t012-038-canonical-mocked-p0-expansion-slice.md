# T012-038 canonical mocked P0 expansion slice

Date: 2026-06-11

## Scope

Expanded no-cost action-first execution for remaining low-risk P0 fixtures and
the last do-not-do runtime wording fixture.

Newly executed fixtures:

- `spec011-rc001-rc002-internal-metadata-leak`
- `spec011-rc009-final-diagnostic-not-truncated`
- `spec011-rc012-final-diagnostic-plain-studio-language`
- `spec011-rc013-sales-inbox-projection-consistency`
- `spec011-rc014-false-pass-protection`
- `spec011-rc004-urgency-before-final`
- `spec011-rc007-valid-short-answer-does-not-stall`
- `do-not-do-wrong-student-language`

All tests use original fixture messages and `ScriptedFakeModel` structured
`ConductorActionDecision` outputs. No paid OpenAI call was made.

## Files

- `services/taliya-agent-runtime/tests/test_spec012_canonical_p0_mocked.py`
- `services/taliya-agent-runtime/tests/test_spec012_canonical_do_not_do_mocked.py`

## Behavior Proven

- Internal metadata/source/profile labels stay out of rendered user text while
  `answer_how_it_works` answers the product question.
- Final diagnostic delivery uses the staged action-first sequence and the final
  demo/next-step line is complete, not truncated.
- Final diagnostic wording remains practical studio-owner language with no
  internal agent labels or CRM jargon.
- Sales Inbox consistency fixture now has a mocked action-first run proving
  price answer + contextual diagnostic hook, answered obligation, state
  transition, and non-empty rendered output.
- False-pass protection fixture proves model operations occurred, structured
  output rendered, all prices were included, and checkout language stayed out.
- Urgency-before-final fixture proves a premature final diagnostic is rejected
  and repaired; staged delivery only happens after the structured decision
  captures the pending `urgency` slot from lead timing evidence.
- Valid short-answer fixture proves a concise diagnostic answer
  (`agenda e reposicoes`) is accepted as `main_pain`, commits to the ledger,
  advances to the next required question, and does not repeat the diagnostic
  offer or produce misunderstanding copy.
- Wrong student-language fixture answers WhatsApp scope using `aluno/alunos`
  language and avoids mirroring "clientes precisam baixar app" or using
  "consumidores".

## Notes

The final-diagnostic P0 tests use original fixture messages with stateful
`initial_state` snapshots for the exact pending diagnostic key. This isolates
the action-first contract that matters for these fixtures: completion only
after pending evidence is captured, and staged final rendering only after
commit-safe validation.

For `spec011-rc004`, the first mocked model output intentionally tries to
complete without the pending `urgency` slot. The validator rejects it, the
repair pass returns a corrected structured decision, and only the repaired
decision is delivered.

## Anti-Determinism Review

No regex, token list, or raw-message commercial router was added. The mocked
LLM still selects the action and structured fields. Deterministic code only
validates, renders, and commits the selected action.

## Commands

- `python -m pytest tests\test_spec012_canonical_p0_mocked.py -q`
  - `7 passed`
- `python -m ruff check tests\test_spec012_canonical_p0_mocked.py`
  - passed
- `python -m pytest tests\ -k spec012 -q`
  - `180 passed, 716 deselected`

## Protected Scope

No `/pilates` layout, landing visual, Sales Inbox UI, multi-tenant, client or
studio WhatsApp integration, checkout, or public endpoint cutover was touched.

## Paid Calls

None. All execution used `ScriptedFakeModel`; total cost remained `$0`.

## Still Open

- Long conversation canonical fixture expansion.
- Quality judge/repetition gates.
- Sales Inbox projection artifact beyond runner state fields.
- Real-model evidence only after explicit paid approval.
