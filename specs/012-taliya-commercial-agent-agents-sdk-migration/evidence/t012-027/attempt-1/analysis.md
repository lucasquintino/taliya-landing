# T012-027 Attempt 1 Analysis - 2026-06-09

Approved by the user on 2026-06-09 in direct response to the packet wording
(15 frozen scenarios, `$1.00` ceiling, no public cutover). Executed once.

## Run Facts

- Model: `gpt-5.4-mini` via OpenAI Agents SDK `Runner.run`.
- Total model operations: 39 of 45 approved.
- Total estimated cost: `$0.080724` of `$1.00` approved (8% of ceiling).
- Tracing: disabled (local-only, D-012-007 honored).
- Aborts: none. No `MaxTurnsExceeded`, no free-form output, no adapter
  rejection, no unrecorded usage.
- All 15 scenarios returned valid strict `TaliyaSdkTurnOutput`.
- Scenario pass/fail: 0 passed, 15 blocked by the spike validators.

## What Worked (Infrastructure And Understanding)

- The full pipeline ran end to end on real model calls: agents, handoffs,
  ctx-based state tools, strict structured output, adapter, validators,
  report writer, budget meter.
- Commercial understanding was good across scenarios: intents correct,
  `quanto custa?` produced an official grounded claim listing the real plans
  (Base R$ 197, Essencial R$ 497, Avance R$ 897, Completo R$ 1.497) with
  `fact_refs=["product_knowledge.plans"]` sourced from the product knowledge
  tool, not invented.
- Cost per scenario averaged ~$0.0054 at 2-3 operations - well under packet
  assumptions.

## Why Every Scenario Failed Validation

Two output-contract gaps, not architecture failures:

1. `sdk_missing_template_plan` (12 of 15): the model left
   `template_plan.template_ids` empty. Only 2 of 15 scenarios called
   `get_approved_template_catalog`. The model did not know template ids were
   mandatory or where to find them.
2. `sdk_direct_question_not_answered_first` / `sdk_missing_answer_obligation`:
   the model interpreted `answered_before_steering` as "not yet answered,
   rendering happens later" (e.g. scenario 3 obligation text: "Answer the
   pricing question ... only after validation", flagged false). Semantics of
   the field were never explained to it.

## Behavioral Near-Miss Worth Tracking

Scenario 10 (waitlist curiosity) chose `waitlist.offer_after_contract_intent`
- the offer template - for a curiosity question, while correctly reporting
`eligibility: unknown`. The spike validator does not check waitlist timing;
the full Spec 011 validator set does. Run 2 must watch this case, and the
production path (T012-032) must keep the waitlist timing validator.

## Fixes Applied Before Run 2 (No Cost)

- `sdk_output_model.py`: field descriptions now teach the contract inside the
  JSON schema the model receives (`template_ids` required from the catalog;
  `answered_before_steering` decided now, not at render time; variables must
  cover required template variables).
- `agents.py`: base instructions gained an explicit 5-point output contract
  (call the catalog before finalizing, never empty template plan, fill
  required variables, answer-first semantics, no waitlist offer template for
  curiosity).
- Strict schema compatibility re-verified; 56 no-cost tests and ruff green.

## Status

T012-027 remains open: the approved attempt-1 budget is consumed
(39/45 operations) and the pass bar was not met. A second full run requires
new explicit approval per D-012-005.
