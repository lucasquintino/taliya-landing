# Design Lock V2 - Action-First - Spec 012

Status: binding revision recorded on 2026-06-10. Supersedes the LLM-template
boundary of `design-lock.md`. Everything not revised here remains valid.

Reason: the spike re-discovered, across paid attempts 1-7 and ideal-conversation
runs 1-15, the same failure mode that Spec 011 had already corrected after the
T011-105 paid failures - letting the LLM select final template plans and fill
all variables directly. The binding correction is the action-first pipeline of
`specs/011-taliya-commercial-agent-core-reset/action-contract.md`. Full
conformity findings: `conformidade-contratos-binding-2026-06-10.pt-BR.md`.

## Binding Sources (in priority order on conflict)

1. `011/action-contract.md` - action-first pipeline (corrects 010 on the
   LLM-template boundary).
2. `011/contract-schema-map.md` - schema homes for every preserved contract.
3. `010/behavior-contract.md`, `010/diagnostic-contract.md`,
   `010/conversation-state-contract.md`, `010/message-template-contract.md`,
   `010/product-followup-delta-contract.md`, `010/sales-inbox-contract.md` -
   behavior, states, voice, delta routes.
4. `010/contracts/eval-contract.md` - the release gate (three layers plus
   judge >= 4.2/5; structural pass alone is never sufficient).
5. `011/regression-cases.md` and `011/do-not-do-static-fixtures.json` - the
   canonical fixtures. They replace the 15 reconstructed spike scenarios as
   the source of truth for paid evals.

## Revised Pipeline

```text
Channel Adapter
-> Runtime API (HMAC, idempotency, turn gate - unchanged)
-> Context Builder (compact memory, state preamble - spike-proven)
-> Turn Situation Builder (deterministic board: mode, pending_question_key,
   allowed_actions, eligible_template_groups, missing_diagnostic_keys,
   official_fact_keys_available, forbidden_actions_now)
-> Agents SDK orchestration (triage pure router + specialists)
   LLM returns ConductorActionDecision ONLY
-> Decision Compiler (deterministic expansion)
-> Contract Validators (full Spec 011 set + voice rules)
-> Focused Repair (one operation, design-lock budget)
-> Template Renderer (approved voice)
-> Persistence / Sales Inbox Projection
-> Delivery / Outbox (chunks, typing, deferral)
```

## What The LLM Returns (and what it never returns)

The SDK agents' `output_type` becomes a strict `ConductorActionDecision`:

- `selected_action` - exactly one, from `TurnSituation.allowed_actions`;
- `interpreted_intents`, `direct_question`, `direct_answer_obligations`
  (with `answering_action`, derived-verifiable);
- `captured_slots` (e.g. the pending diagnostic answer, typed);
- `numeric_interpretations` (plan_price vs student_count etc.);
- `product_fact_keys_used`, `evidence`, `confidence`, `needs_clarification`,
  `repair_hints`;
- free-composition variables ONLY where the contract assigns composition to
  the model (e.g. `answer_feedback`, `pain_context_human`), each with source
  and evidence, under the anti-parrot rule.

The LLM never returns: final template plan, staged delivery sequence,
official-source variable values, state transitions, rendered text, or
whole-response fields. (Forbidden list: `011/action-contract.md` lines 88-94.)

## What The Decision Compiler Owns (deterministic, code)

- State transition per `010/conversation-state-contract.md` canonical table;
- Diagnostic ledger merge; next pending key; completion detection;
- The ENTIRE staged final diagnostic sequence: deliver_hold -> deliver_context
  -> deliver_crm_base -> deliver_operational_step -> one
  deliver_agent_recommendation per indicated agent -> deliver_plan_recommendation
  -> demo line matching persisted demo status;
- Template group expansion from the selected action;
- Variables whose source is official product knowledge or runtime state;
- Sales Inbox projection inputs; render plan skeleton; chunk policy.

This makes the spike's main defects impossible by construction instead of
repaired: single-template final delivery, forgotten hold message, skipped
question, wrong sequence, plan-before-operational.

## What Survives From The Spike (proven, reused)

- Agents SDK as orchestration motor; triage as pure router
  (`tool_choice=required`); specialist topology; sticky flow-owners;
- Strict structured output discipline and the two-layer schema approach
  (model-facing strict schema adapted to the runtime shape);
- State preamble / compact memory injection; ctx-based state tools;
- Budget meter, abort gates, local-only tracing, provider-error capture;
- Single-repair operation with precise validator feedback;
- Multi-turn conversation harness with commit-after-validation state;
- Stale-direct-question scrub; deterministic diagnostic-sequence guardrails
  (which now move into the Turn Situation Builder / compiler as their
  natural home).

## Voice Rules Moved Into Validators (from 010 contracts, missing in spike)

- Banned phrases list (behavior-contract Voice And Style);
- Anti-parrot: `answer_feedback` grounded, not literal lead repetition,
  not generic filler repeated across turns;
- No repeated greeting mid-conversation; no "CRM" for lay leads;
- Owner-language control (no SaaS jargon unless lead used it);
- "pelo que voce contou" blocked when facts are thin (allowed when rich);
- Rejected final-diagnostic formats blocked.

## Behavior Coverage To Add (from delta contract, absent in spike)

- Name policy (reliable/unreliable profile name, ask-at-diagnostic-entry);
- Hold message before final delivery (compiler-owned);
- Product knowledge keys: how_it_works, routine_areas, whatsapp_scope,
  integration_scope, comparison_*, security_and_data,
  availability_and_onboarding, out_of_profile;
- Delta templates: product.how_it_works_direct, product.comparison_current_tool,
  product.integration_scope_direct, product.security_data_direct,
  product.out_of_profile_redirect;
- Post-diagnostic compact context payload; objection policy; diagnostic
  refusal; conversation resume; out-of-profile qualification.

## Release Gate (replaces "passed_structural" as success measure)

Per `010/contracts/eval-contract.md`:

1. Layer 1 deterministic invariants - any failure blocks regardless of score;
2. Layer 2 multi-turn scenario runner over the canonical fixture set;
3. Layer 2B real-provider transcripts (no mock as final evidence);
4. Layer 3 LLM quality judge: mapped P1 average >= 4.2/5, no scenario
   below 4.0/5;
5. Repetition policy: release-gate batteries run 3x consecutively;
6. Cost: normal lead <= $0.05 target, $0.10 review, $0.20-0.30 hard cap.

## Two Calibration Notes (verified against T011-105 primary evidence)

1. Action-first RELOCATES the composition-quality risk; it does not remove it.
   The recorded T011-105 paid failure was an action-first failure: the LLM
   chose the right action but omitted `pain_context_human`, and the compiler
   rendered a generic fallback. Therefore composition-variable validators
   (action rejected without its required composition variables; anti-parrot;
   grounding) are first-class, not optional polish.
2. T012-032 is a PORT, not new construction: the Spec 011 runtime already
   implements and tests the validator set (including
   `price_question_missing_price_answer`, `diagnostic_final_staged_order_invalid`,
   `diagnostic_next_question_invalid`, and the recovery gates listed in
   `t011-105-paid-approval-packet.md`).

## Cost Policy (user-approved 2026-06-10)

- Development iterations: no-cost only (fake-model dry-runs + mocked tests);
- Paid runs only at closed milestones; canary-first;
- 3x repetition only at the final release gate;
- Global Spec 012 paid ceiling to activation: $5 (stop and report if exceeded).
