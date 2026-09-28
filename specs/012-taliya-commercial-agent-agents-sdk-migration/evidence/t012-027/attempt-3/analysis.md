# T012-027 Attempt 3 Analysis - 2026-06-09

Approved by the user ("pode ser, vamos pra rodada 3") for the canary-first
protocol within a `$1.00` ceiling.

## Run Facts

- Canary (scenarios 1, 3, 7): 1 and 3 passed; 7 hit `max_turns`.
  Cost `$0.055582`.
- No-cost fix: state-based starting-agent selection per design lock
  (`current_sdk_agent` in the snapshot starts the run at the right
  specialist, skipping the triage handoff turn).
- Canary retest 1 (scenario 7): still `max_turns` even starting at the
  diagnostic agent. Cost `$0.038250` (worst-case charge). Harness improved
  no-cost to record partial run items and real usage from
  `MaxTurnsExceeded.run_data`.
- No-cost fix: instruction telling agents the final structured output already
  carries every proposal - do not duplicate via propose_* tools; typical
  turn shape is one batched read round then the final output.
- Canary retest 2 (scenario 7): passed with 2 operations (batched reads then
  final). Cost `$0.007838`. Canary 3/3 - proceeded to the full 15.
- Full 15 run: **10/15 passed_structural** (was 3/15 in attempt 2), 30
  operations, `$0.081956`, every scenario at exactly 2 operations, zero
  aborts, zero `max_turns`.
- Attempt-3 total spend: `$0.183626` of `$1.00`. Cumulative all attempts:
  `$0.465013`.

## The 5 Remaining Failures - Honest Classification

Real commercial behavior failures (the validators caught what they exist to
catch):

- Scenario 4 (price + pain): chose `opening.general_interest` and did not
  answer the price - the exact "hide price behind steering" do-not-do. The
  mini model flattened the mixed intent.
- Scenario 10 (waitlist curiosity): chose `waitlist.ask_missing_studio`,
  starting to collect signup details for a curiosity question.

Near-miss mechanical failures:

- Scenario 7: declared `source=model_decision` for the plan recommendation
  variable instead of the official source it actually read (run-to-run
  variance: this same scenario passed in the canary retest).
- Scenario 14: one variable 147 chars where the registry caps 140.

Scenario expectation mismatch:

- Scenario 15: the model did not propose delivery deferral (set
  `defer_inbound_during_chunks=false` and answered with a fallback). Per
  D-012-011, inbound deferral is runtime turn-gate territory (T012-036); the
  spike validator also wrongly demanded answer-first in a deferral situation.

## Fixes Applied Before Run 4 (No Cost, 67 Tests Green)

1. Single repair operation in the harness (design lock: at most one extra
   model operation, only when it fits the per-scenario cap): validator errors
   are fed back to the last agent for one corrected final output. Dry-run
   tested, including cap enforcement.
2. `answered_before_steering` description now carries a concrete example
   (price question -> product.price_direct -> true).
3. Instruction: declared variable sources must reflect where the underlying
   facts came from; synthesized official facts are official_product_knowledge,
   not model_decision. Stay clearly under max_length.
4. Operational instruction: when state shows delivery in flight, propose
   deferral and do not answer the inbound yet.
5. Spike validator now allows unanswered direct questions when the proposal
   itself defers delivery (operational deferral exception, allowed
   determinism).

## Variance Note

Scenario 7 passed in the canary retest and failed in the full run on a
different error. Structural pass is not deterministic run to run; the repair
operation is the designed mitigation, and the release gates (golden evals,
shadow mode, manual review) exist precisely because single-run results
cannot be trusted alone.

## Status

T012-027 remains open. Attempt-3 ceiling is partially used (`$0.18` of
`$1.00`), but the canary-first protocol as recorded covers one full-15 run;
run 4 (full 15 with repair enabled) requires new explicit approval.
