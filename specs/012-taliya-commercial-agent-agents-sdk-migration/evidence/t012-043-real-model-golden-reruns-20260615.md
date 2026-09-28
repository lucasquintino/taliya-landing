# T012-043 Real-Model Golden Reruns - 2026-06-15

## Scope

Real-model golden transcript validation for the isolated Spec 012 action-first
SDK path. No public cutover, no `/pilates` layout changes, no Sales Inbox UI,
no checkout, no multi-tenant, no client/studio WhatsApp.

## Paid Approval And Cost

Paid OpenAI calls were approved by the user in chat on 2026-06-15 for T012-043.
The runner used `.env.local` without printing the key and enforced a local
`$1.00` cap per run.

Recorded T012-043 paid real-model runs:

- `20260615T150020Z`: 6/9 passed, 36 ops, `$0.092661`.
- `20260615T171723Z`: 6/9 passed, 33 ops, `$0.090510`.
- `20260615T172044Z`: aborted on `step3g-long-conversation`, 10 ops, `$0.021497`.
- `20260615T172957Z`: 7/9 passed, 33 ops, `$0.095216`.
- `20260615T173345Z`: 8/9 passed, 32 ops, `$0.081833`.
- `20260615T173647Z`: 8/9 passed, 33 ops, `$0.088537`.
- `20260615T174003Z`: 8/9 passed, 20 ops, `$0.045837`.
- `20260615T191817Z`: 8/9 passed, 36 ops, `$0.105263`.
- `20260615T192127Z`: 7/9 passed, 31 ops, `$0.082855`.
- `20260615T193040Z`: 8/9 passed, 31 ops, `$0.082742`.
- `20260615T193352Z`: 7/9 passed, 19 ops, `$0.044396`.
- `20260615T194909Z`: 8/9 passed, 35 ops, `$0.102520`.
- `20260615T195529Z`: 8/9 passed, 33 ops, `$0.089543`.
- `20260615T204145Z`: targeted `final-price-first`, 1/1 passed, 2 ops,
  `$0.004265`.
- `20260615T204345Z`: full rerun, 8/9 passed, 33 ops, `$0.090967`.
- `20260615T211155Z`: full rerun, 9/9 passed, 32 ops, `$0.087127`.

Total recorded T012-043 paid spend in these reports: `$1.205769`.

## No-Cost Fixes Landed During Reruns

- Pain-first no longer starts diagnostic questions without acceptance.
- `product.demo_direct` copy now matches the approved user wording.
- Instagram/general-interest opening copy no longer says "Legal voce vir por aqui"
  or vague "entender por onde comecar".
- Post-diagnostic stale `diagnostic_offered` state now derives
  `post_diagnostic` mode from completed/delivered diagnostic state.
- Waitlist "como funciona a entrada/lista" now uses
  `waitlist.current_path_explained` instead of leaking availability prose through
  `product.overview_short`.
- Diagnostic mode now blocks repeating the pending question without capturing or
  clarifying the lead's answer.
- Contextual price hooks now require a concrete current-turn pain anchor such as
  agenda/reposicao/WhatsApp/follow-up rather than generic "esse tipo de dor".
- Unneeded clarification for a direct question is no longer accepted as an
  answering action unless the LLM also marks `needs_clarification=true`.
- Non-numeric `plan_price` numeric interpretations are normalized to
  `unknown_number` before the legacy validator bridge.
- Long composed variables such as `waitlist_context_summary` are clamped to the
  registry max length before template validation.
- Product-agent instructions now explicitly call out price + operational
  context examples (`agenda`, `reposicao`, `WhatsApp`, `follow-up`, etc.).
- Price answers that the LLM itself declares as price + pain/context now fail
  validation if they compile to the generic `diagnostic.price_hook`; repair must
  add `plan_fit_context` so `diagnostic.price_hook_with_context` renders.
- Diagnostic completion repair now explicitly adds a missing final key such as
  `urgency` when the current inbound answers it, instead of completing with a
  missing ledger slot.
- Product fact declarations for `prices`, `plans`, or `demo_link` are treated as
  answerable direct obligations, so the LLM cannot keep a price/demo request in
  a clarifying action after declaring the official fact key.
- Demo repair now explicitly keeps `send_demo` while setting the current demo
  request as `direct_question` with an answer obligation.
- Post-diagnostic product follow-ups such as "como funciona mesmo?" now repair
  off-menu generic product actions to `answer_product_question_with_saved_context`.
- Post-diagnostic list/start intent now fails if the LLM declares waitlist
  structure but continues a price-objection answer instead of
  `offer_or_join_waitlist_if_eligible`.
- The real-model runner now prints ASCII-safe JSON to avoid Windows console
  `UnicodeEncodeError`; saved Markdown/JSON transcripts remain intact.
- Direct price questions cannot remain in a clarifying action when the LLM's
  own `interpreted_intents` include `price_question`, even if it did not declare
  the `prices` fact key.
- Waitlist-mode "como funciona" product questions now prioritize
  `product.how_it_works_direct` before continuing missing-detail collection,
  even when the LLM also declares `availability_and_onboarding`.
- Latest no-cost validation after these guardrails: full Spec 012 suite
  `264 passed / 716 deselected`; focused ruff clean.

## Current Result

Latest full run: `evidence/t012-043-real-model-golden-transcripts/20260615T211155Z/`.

Result: 9/9 passed, not aborted.

No scenario failures remained in the latest full run.

Latest targeted confirmation:
`evidence/t012-043-real-model-golden-transcripts/20260615T204145Z/`.
Result: `final-price-first` 1/1 passed after the no-cost price-intent guardrail.

Observed failures across the latest two reruns:

- `20260615T193040Z`: `final-price-plus-pain` passed after the structured
  price+context hook guardrail. The only failure was
  `step3g-long-conversation`, where completion missed the final `urgency` slot;
  this was fixed no-cost after the run by repair/diagnostic instructions and a
  mocked regression test.
- `20260615T193352Z`: stochastic regression. `step3g-long-conversation` failed
  on the first price turn because the model selected
  `clarify_ambiguous_opening` for a declared price question. `final-demo-request`
  failed because `send_demo` omitted `direct_question`. Both were fixed no-cost
  after the run with structured product-fact direct-answer validation and
  explicit repair instructions/tests.
- `20260615T194909Z`: `step3g-long-conversation` reached post-diagnostic turn
  12, then failed because the model chose off-menu `answer_how_it_works`
  instead of `answer_product_question_with_saved_context`; turn 11 also showed
  a waitlist/start intent answered as a price objection. Both were fixed no-cost
  after the run with post-diagnostic repair instructions and structured
  waitlist-intent validation/tests.
- `20260615T195529Z`: `final-price-first` failed because the model selected
  `clarify_ambiguous_opening` for `quanto custa?` with structured
  `price_question` intent but no `clarification_question`; this was fixed
  no-cost after the run by treating model-declared price intent as an answerable
  direct-price obligation.
- `20260615T204345Z`: full rerun confirmed `final-price-first` passed, but
  `step3g-long-conversation` failed at waitlist turn 12 because the model
  correctly chose `answer_question_then_continue_waitlist` for "como funciona
  mesmo?" while declaring `how_it_works` and `availability_and_onboarding`; the
  compiler rendered `waitlist.current_path_explained` instead of required
  `product.how_it_works_direct`. This was fixed no-cost after the run by
  prioritizing how-it-works product answers before waitlist missing-detail
  continuation.
- `20260615T211155Z`: full rerun after the waitlist how-it-works compiler fix
  passed all 9 canonical scenarios, including `step3g-long-conversation`.

## Anti-Determinism Review

The fixes preserved the LLM-first action boundary:

- No raw lead-text commercial router was added for price, demo, pain, waitlist,
  diagnostic, or plan-fit.
- Deterministic changes are state/mode normalization, compiler form guards,
  approved renderer templates, and validators after the LLM action.
- The residual `quanto custa?` routing failure should be fixed through prompt,
  repair, or action-contract constraints, not by adding a regex-first price
  shortcut.

## Manual Review After 9/9

The automated gate passed, but manual review rejected T012-043 closure. The
latest customer-facing transcripts still have release-blocking quality issues:

- rendered Portuguese contains mojibake such as `vocÃª`, `reposiÃ§Ã£o`,
  `estÃ¡`, `cenÃ¡rio`, `VitÃ³ria`, and `â€”`;
- `product.whatsapp_direct` leaks internal policy wording to the lead:
  "Nao prometa configuracao automatica no chat comercial";
- the long-conversation waitlist turn says "A pessoa achou..." in third person,
  which reads like internal operator summary, not customer copy;
- diagnostic progress chunks duplicate the same acknowledgement on every
  answer, once inside `diagnostic.partial_progress` and once before the next
  question;
- the report check explanations are inverted/confusing, e.g. `PASS` with
  "missing expected rendered text" or "template was not selected";
- the waitlist "como funciona mesmo?" turn passed while the saved
  `template_ids` show `product.overview_short` instead of the intended
  `product.how_it_works_direct`.

## Next Lock

T012-043 remains open despite the latest automated 9/9. Do not advance to
T012-044 until the manual-review findings above are fixed, rerun, and reviewed
with the user.
