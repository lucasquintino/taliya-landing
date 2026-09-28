# T012-027 Attempt 2 Analysis - 2026-06-09

Approved by the user on 2026-06-09 ("pode ser, aprovado") for a second run with
a new `$1.00` ceiling. Executed once.

## Run Facts

- Model: `gpt-5.4-mini`, tracing disabled, no public cutover.
- Total model operations: 42 of 45. Total estimated cost: `$0.200663` of
  `$1.00` (three scenarios hit `max_turns` and were conservatively charged at
  the worst-case `$0.03825` each; actual spend is lower).
- Aborts: none. All non-`max_turns` scenarios returned valid strict output.
- Result: 3 of 15 `passed_structural` (5 diagnostic_start,
  14 do_not_do_checkout_discount_date_vip, 15 delivery_concurrency) - up from
  0 of 15 in attempt 1.

## Progress Versus Attempt 1

The attempt-1 contract fixes worked: the model now plans templates and uses
the catalog. Failures moved from "empty plan everywhere" (12/15) to narrow
mechanical issues:

1. `long_text` variables missing `max_length` (scenarios 4, 6).
2. Variable kind/source mismatches against the official variable registry
   (scenarios 3, 8: `kind_mismatch`, `source_not_allowed:model_decision`).
3. `max_turns_exceeded` (scenarios 7, 11, 12): the new "call the catalog
   before finalizing" instruction added a tool round, exceeding the approved
   3 operations per scenario.
4. Residual empty plans (scenarios 1, 2, 9): the model spent all turns on
   tool rounds (summary + state + catalog) and finalized with an empty plan.
5. `answered_before_steering` still false on 9 and 10.

## Fixes Applied Before Run 3 (No Cost)

- Each agent's instructions now embed its approved-template slice and the
  variable specs (kind, max_length, allowed sources), generated from the
  official `TEMPLATE_REGISTRY`/`VARIABLE_REGISTRY` at build time. This removes
  the catalog tool round entirely - the direct cause of failure classes 3
  and 4 - and gives the model the exact variable contract (classes 1 and 2).
- `get_approved_template_catalog` payload now includes full variable specs
  for agents that still consult it.
- The proposal adapter normalizes variable `kind` and `max_length` to the
  canonical registry spec (deterministic rendering plumbing). The declared
  `source` is intentionally never coerced: a wrong source must fail
  validation, not be masked.
- Instructions now tell agents to batch independent tool calls in one round.
- Verified no-cost: 58 tests passed, ruff clean, strict schema intact.

## Status

T012-027 remains open. Attempt-2 approval is consumed (42/45 operations).
Run 3 requires new explicit approval per D-012-005.
