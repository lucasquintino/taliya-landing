# T012-026 Paid Spike Approval Packet

Status: prepared, not approved, not run.

This packet is the approval gate for T012-027. It does not authorize a paid
OpenAI run by itself.

## Scope

Allowed only after explicit user approval:

- run the isolated Spec 012 Agents SDK spike against real OpenAI model calls;
- use the 15 frozen scenarios from `spike-plan.md`;
- record SDK run items, handoffs, tools, structured proposal, validation,
  approved rendered preview, usage, cost, and pass/fail reason;
- keep all output local to the repo evidence directory.

Still forbidden:

- public endpoint cutover;
- `/pilates` visual/layout/copy changes;
- landing UI changes;
- Sales Inbox UI changes;
- multi-tenant work;
- client/studio WhatsApp work;
- checkout work;
- production state commits from SDK reasoning;
- direct free-form SDK text delivery to leads;
- external trace storage with lead text unless separately approved.

## Pre-Approval Evidence Already Green

- T012-020 isolated prototype path exists and is not imported by the public
  runtime endpoint.
- T012-021 minimal SDK agents and handoff graph exist.
- T012-022 SDK tools are read-only or proposal-only; no commit tools exist.
- T012-023 output adapter rejects free-form final output.
- T012-024 validator/render path renders approved templates only.
- T012-025 mocked contracts cover all required spike scenarios with no paid
  calls.
- T012-026B (added 2026-06-09) real `Runner.run` harness exists and passed its
  no-cost dry-run gate with a scripted fake model:
  - all agents declare the strict `TaliyaSdkTurnOutput` output type, so the
    SDK final output is always a structured proposal;
  - state snapshots reach read-only tools through the SDK local run context;
  - SDK trace export is disabled before any model call (D-012-007 local-only);
  - usage/cost are measured from the runner, never self-reported by the model;
  - the budget meter stops before exceeding the operation or cost ceiling and
    `max_turns=3` enforces the per-scenario operation cap;
  - the 15 frozen scenario inputs include prior transcript/state snapshots for
    the multi-turn scenarios (6, 7, 11, 15);
  - the report writer produces all required report fields locally.

Latest no-cost verification before this packet (updated 2026-06-09):

```text
python -m pytest tests\test_spec012_sdk_mocked_contracts.py tests\test_spec012_sdk_validators_adapter.py tests\test_spec012_sdk_output_adapter.py tests\test_spec012_sdk_agents.py tests\test_spec012_sdk_spike_isolation.py tests\test_spec012_sdk_paid_harness_dry_run.py -q
56 passed
```

```text
python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_sdk_mocked_contracts.py tests\test_spec012_sdk_validators_adapter.py tests\test_spec012_sdk_output_adapter.py tests\test_spec012_sdk_agents.py tests\test_spec012_sdk_spike_isolation.py tests\test_spec012_sdk_paid_harness_dry_run.py
All checks passed!
```

## Frozen Paid Spike Scenarios

Run exactly these scenarios first, in this order:

| # | Scenario | Required proof |
| --- | --- | --- |
| 1 | Cold greeting: `oi` | No unnecessary commercial shortcut beyond pure cold greeting; structured proposal and approved template preview. |
| 2 | Pain-first WhatsApp delay | Lead pain is understood by the LLM and reused naturally. |
| 3 | Price-first | Direct price question is answered before any diagnostic steering. |
| 4 | Price plus pain | Price answered first; pain context preserved for natural next step. |
| 5 | Diagnostic start | Diagnostic begins and asks one next question. |
| 6 | Numeric diagnostic answer: `120` | `120` becomes active-student/size answer, not price. |
| 7 | Diagnostic urgency final | Mandatory diagnostic keys complete; final staged diagnostic renders. |
| 8 | WhatsApp product scope | Official WhatsApp scope only; no client/studio WhatsApp overreach. |
| 9 | Demo request | Official demo path only; demo interest proposed. |
| 10 | Waitlist curiosity | Curiosity does not become waitlist offer. |
| 11 | Clear waitlist/contract intent | Waitlist offer only after qualified intent. |
| 12 | Human handoff request | Handoff pause is proposed in state, not just worded. |
| 13 | Do-not-do: `plano de 497` | `497` remains plan price, not student count. |
| 14 | Do-not-do: checkout/discount/date/VIP | No checkout, date, discount, or VIP promise. |
| 15 | Delivery concurrency simulation | Render remains local; defer proposal recorded, no public delivery. |

## Required Report Fields Per Scenario

T012-027 evidence must include, per scenario:

- input transcript;
- starting agent;
- agent path and handoffs;
- SDK tool calls and outputs;
- SDK final output;
- adapted `TaliyaTurnProposal`;
- validator result;
- approved rendered preview;
- proposed runtime state diff;
- proposed Sales Inbox projection;
- usage: model, model operations, input tokens, output tokens, cost;
- pass/fail reason;
- comparison notes against current Spec 011 path, if available locally without
  adding new paid calls.

## Model And Cost Estimate

Preferred model for the first paid spike: `gpt-5.4-mini`.

Pricing reference checked on 2026-06-05 from OpenAI API pricing:

- `gpt-5.4-mini` input: `$0.75 / 1M tokens`;
- `gpt-5.4-mini` cached input: `$0.075 / 1M tokens`;
- `gpt-5.4-mini` output: `$4.50 / 1M tokens`.

Budget assumptions for approval:

- 15 scenarios;
- maximum 3 SDK model operations per scenario;
- maximum 45 total SDK model operations;
- estimate cap per operation: 8,000 input tokens and 1,500 output tokens;
- maximum estimated input tokens: 360,000;
- maximum estimated output tokens: 67,500;
- estimated uncached cost: `$0.57375`;
- requested approval ceiling with buffer: `$1.00`.

The paid spike must stop before exceeding either:

- 45 SDK model operations; or
- `$1.00` estimated cost; or
- any P0 abort condition below.

If the configured model is unavailable, if pricing differs materially, or if the
runner cannot report usage/cost, T012-027 must stop and return for approval
instead of continuing.

## Required User Approval Wording

To authorize T012-027, the user must explicitly approve paid OpenAI calls and a
budget. Acceptable approval wording:

```text
Approve T012-027 paid SDK spike for the 15 frozen scenarios with a hard ceiling
of $1.00 estimated OpenAI API cost. Do not cut over public traffic.
```

Any narrower approval must be obeyed literally. Any ambiguous approval is not
enough to run paid calls.

## T012-027 Execution Preconditions

Before the first paid call in T012-027:

1. Re-run mocked Spec 012 tests (including the T012-026B dry-run gate).
2. Re-run Ruff on the isolated SDK package and Spec 012 tests.
3. Confirm no public runtime imports `taliya_commercial_sdk`.
4. Confirm no `/pilates`, landing UI, Sales Inbox UI, multi-tenant,
   client/studio WhatsApp, or checkout changes are in the T012-027 diff.
5. Confirm `OPENAI_API_KEY` is available without printing or committing it.
6. Confirm exact model name and current pricing (the harness refuses models
   without recorded pricing).
7. Confirm local-only trace/report output path. The harness disables SDK trace
   export (`set_tracing_disabled` plus `RunConfig(tracing_disabled=True)`)
   before any model call.
8. Confirm the harness dry-run gate is green: real `Runner.run` path with a
   fake model, structured output end to end, budget abort, free-form abort,
   and runner-measured usage (`tests\test_spec012_sdk_paid_harness_dry_run.py`).
9. Use only the frozen inputs from `spike_scenarios.py`
   (`load_frozen_spike_scenarios()`), including the prior transcript/state
   snapshots for scenarios 6, 7, 11, and 15.
10. Usage/cost in every report comes from the harness/runner; model-reported
    usage values are never trusted.

Scenario 15 note: it stays in the frozen paid list for packet fidelity, but it
proves structure only (defer proposal recorded in the state patch); the actual
inbound-deferral gate is runtime behavior owned by T012-036.

## Canary-First Protocol (added 2026-06-09 after attempts 1-2)

To stop paying full 15-scenario runs to discover systematic contract errors:

1. A no-cost preflight gate (`tests\test_spec012_sdk_preflight.py`) must be
   green before any paid call. It statically proves the model is never set up
   to fail for known reasons: every golden template id is embedded in the
   owning agent's catalog, every template variable has a registry spec, and
   golden variables conform to canonical kind/source.
2. Within one approved ceiling, run the canary subset first: scenarios 1
   (cold_greeting), 3 (price_first), and 7 (diagnostic_urgency_final) - they
   cover all failure classes observed in attempts 1-2. Estimated canary cost:
   under `$0.05`.
3. Only if all three canary scenarios pass structural validation, continue to
   the full frozen 15 within the same ceiling. Otherwise stop, fix no-cost,
   and re-run the canary within the remaining ceiling.
4. The full-run report still covers all 15 frozen scenarios in packet order.

## Abort Conditions

Abort the paid spike immediately if any of these occur:

- SDK free-form output would be delivered directly to a lead;
- SDK output cannot adapt to `TaliyaTurnProposal`;
- validator/render path is skipped;
- any SDK tool commits production commercial state during reasoning;
- direct question is hidden behind diagnostic steering;
- product answer lacks official fact refs;
- `plano de 497` is interpreted as 497 students;
- waitlist is offered for curiosity only;
- human handoff does not propose AI pause;
- SDK trace cannot show agent path/tool/handoff evidence;
- usage/cost cannot be recorded;
- estimated cost would exceed approved ceiling;
- public endpoint, `/pilates`, Sales Inbox UI, multi-tenant, client/studio
  WhatsApp, or checkout scope would be touched.

## Pass Bar

The paid spike is promising only if:

- no P0 scenario fails;
- all 15 scenarios produce structured proposals and validator results;
- all product claims are grounded in official facts;
- rendered preview uses approved templates only;
- trace evidence is clearer than the current custom path;
- cost is visible and within ceiling;
- conversational understanding is better than or clearly more debuggable than
  current Spec 011 on critical scenarios.

Equal structural validity alone is not enough.

## Current Decision

T012-026 is complete when this packet is recorded and the ledger is updated.

T012-027 remains blocked until the user explicitly approves paid OpenAI calls
and budget.
