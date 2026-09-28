# T012-057 canonical round 1 stop review

## Result

- Result: `6/9` passed.
- Model operations: `33`.
- Reported round cost: `$0.118506`.
- Reported cumulative cost: `$0.170970`.
- Operationally accounted cumulative cost, including the unreconciled reserve:
  `$0.190970`.
- Evidence: `canonical-round-1/20260805T005102Z/report.md`.

No production switch or public delivery occurred.

## Failed scenarios

### final-pain-first

Luna correctly selected `offer_diagnostic_from_pain`, captured the pain, and
offered the diagnostic. The composed acknowledgement paraphrased the delay and
lost the concrete channel name `WhatsApp`, so the canonical context check
failed.

### final-instagram-interest

Luna understood both the Instagram origin and the broad information request,
but selected `answer_general_interest`. During repair it also emitted the
invented fact key `how_it_works_direct`, which bypassed the intended official
fact contract and left the cold-greeting template in place.

### final-waitlist-joined

Luna correctly extracted both pending fields, `Studio Viva` and `Vitória, ES`,
but selected `collect_waitlist_missing_detail`. The compiler rendered the first
field from the old missing-details list without subtracting the newly captured
slots, so it asked for the studio name again instead of completing the join.

## Runner defect

The paid runner recorded all nine scenarios even though a failed scenario is a
stop condition. Future batches must abort immediately after the first failed
scenario. No additional paid run is allowed until this behavior has a no-cost
regression.

## No-cost correction scope

- constrain official product fact keys in the structured SDK schema;
- clarify source-opening and concrete-context instructions without adding
  deterministic raw-text routing;
- preserve the LLM-selected source action in the legacy validator adapter;
- apply captured waitlist slots to pending details and join when none remain;
- enforce paid-run fail-fast after a failed scenario;
- add exact mocked regressions for all three failed conversations.

## Correction verification

- Focused action-first set: `103 passed`.
- Full Spec 012 set: `293 passed / 718 deselected`.
- Active production gate: `525 passed`.
- Focused Ruff and `git diff --check`: passed.
- Pinned Linux image: `/healthz` passed with model `gpt-5.6-luna`, OpenAI
  `2.44.0`, and Agents SDK `0.18.0`.

The fixes preserve the LLM-first boundary: the model still interprets the lead
and selects the commercial action. Deterministic code only constrains the
structured contract, validates consistency, consumes already extracted form
slots, renders approved output, and stops paid execution on failure.
