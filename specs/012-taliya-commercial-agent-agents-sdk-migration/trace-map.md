# Trace Map - Spec 012

Revision 2026-06-10 (design-lock-v2): traces must additionally record the
Turn Situation (mode, pending key, allowed actions), the
`ConductorActionDecision`, the Decision Compiler expansion, repair events with
their validator feedback, and harness-measured usage (never model-reported).
SDK trace export stays disabled (local-only per D-012-007/D-012-009).

Purpose: define how SDK run evidence maps into Taliya runtime traces, eval reports, and Sales Inbox debug artifacts.

## Trace Policy

- Local traces may include lead text for development/debugging.
- External tracing with lead text is blocked until D-012-007 is explicitly approved.
- Trace records must support replay/debug without becoming a second source of product truth.
- Trace retention must follow the privacy policy recorded in `decision-log.md`.

## Required Trace Sections

| Taliya trace section | SDK/source input | Required before |
| --- | --- | --- |
| inbound | channel adapter payload | context build |
| turn gate | lock/idempotency/handoff state | SDK run |
| context snapshot | compact memory and official facts | SDK run |
| sdk_start | selected starting agent and reason | SDK run |
| sdk_run_items | SDK run items, handoffs, tools, guardrails | output adapter |
| sdk_final_output | raw structured SDK output | proposal adapter |
| taliya_proposal | `TaliyaTurnProposal` | validation |
| validators | validator pass/fail and reasons | rendering |
| repair_or_escalation | repair/escalation attempt if used | final decision |
| render_plan | template ids and typed variables | delivery |
| rendered_messages | final channel-specific chunks | outbox |
| state_diff | validated persistence changes | commit |
| sales_inbox_projection | projected inbox fields | inbox write |
| delivery | outbox reservation and status | response |
| usage_cost | model, operations, tokens, cost estimate | task/eval closure |

## Eval Report Requirements

Each scenario report must include:

- scenario id;
- input transcript;
- starting agent;
- agent path;
- handoffs;
- tools called;
- guardrail results;
- final proposal;
- validator result;
- rendered response;
- state diff;
- Sales Inbox projection;
- usage/cost;
- pass/fail reason;
- manual review notes when required.

## Failure Labels

Use stable labels:

- `sdk_schema_invalid`
- `sdk_freeform_direct_output`
- `missing_direct_answer`
- `product_fact_unofficial`
- `diagnostic_incomplete`
- `diagnostic_repeated_question`
- `numeric_fact_confusion`
- `internal_leak`
- `premature_waitlist`
- `handoff_not_persisted`
- `delivery_concurrency_violation`
- `sales_inbox_projection_mismatch`
- `trace_incomplete`
- `cost_budget_exceeded`
- `deterministic_commercial_route_detected`
