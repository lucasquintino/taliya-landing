# T012-057 targeted gate stop review

## What happened

The targeted batch started with three Luna scenarios. The price-objection case
passed with four model operations and a reported cost of `$0.011370`. Before a
complete transcript for the waitlist-hesitation case could be returned, Sales
Inbox projection rejected its initial state: the fixture claimed the diagnostic
was delivered but omitted the required complete ledger and final diagnostic
fields.

This is an invalid-fixture failure, not evidence that Luna misunderstood the
lead. Because the exception happened outside the normal completed report path,
the zero usage shown for that scenario is not treated as authoritative.

## Cost accounting

- Reported cumulative spend: `$0.039351`.
- Unreconciled conservative reserve: `$0.020000`.
- Operationally accounted spend: `$0.059351`.
- Remaining approved ceiling after the reserve: `$0.690649`.

No paid call was made after this stop.

## No-cost correction

- The waitlist fixture now supplies all six completed diagnostic ledger fields,
  both required final fields, and the saved recommendation fields.
- The paid runner validates every fixture before the first OpenAI call and
  blocks the whole batch when a completed diagnostic is structurally invalid.
- The Markdown reporter accepts preflight-only scenarios and preserves inbound
  messages for failures that happen before assistant delivery.
- An exact mocked two-turn regression covers the full waitlist flow: offer the
  waitlist, receive hesitation, render `waitlist.pause_decision`, collect no
  identity data, do not mark joined, and preserve the diagnostic state.

## Evidence

- Failed targeted batch: `targeted/20260805T003434Z/report.md`.
- Corrected no-cost preflight:
  `targeted-preflight-after-fix/preflight-20260805T003758Z/preflight.json`.
- Mocked regression:
  `services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`.

## Recovery result

The corrected waitlist-hesitation case passed in isolation at `$0.007805`, and
the diagnostic-acceptance case passed in isolation at `$0.005308`. Together
with the initial price-objection pass at `$0.011370`, the targeted phase closed
at `3/3` with `$0.024483` reported spend. The conservative `$0.020000` reserve
for the interrupted attempt remains in the cumulative ledger.

## Gate state

The targeted phase is closed. T012-057 remains open at the canonical battery;
production remains on the previous model until every paid gate and deployment
checkpoint closes.
