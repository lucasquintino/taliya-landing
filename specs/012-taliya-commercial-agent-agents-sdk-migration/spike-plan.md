# Spike Plan - Agents SDK Proof Before Migration

Purpose: prove whether OpenAI Agents SDK is actually a better engine for Taliya before rewriting the public core.

The spike is not production code and must not change `/pilates`, widget UI, Sales Inbox UI, multi-tenant, client/studio WhatsApp, or checkout.

## Spike Goal

Build a minimal isolated SDK path that can run critical Taliya lead conversations and produce:

- SDK run items;
- handoff/tool trace;
- structured `TaliyaTurnProposal`;
- validator result;
- rendered approved messages;
- model usage/cost;
- comparison against current Spec 011 path.

## Spike Non-Goals

- No production cutover.
- No public endpoint replacement.
- No UI redesign.
- No final persistence migration.
- No broad rewrite of all validators.
- No paid run without explicit approval.

## Minimal SDK Prototype

Files may live under a temporary/prototype path such as:

```text
services/taliya-agent-runtime/app/core/taliya_commercial_sdk/
```

Minimum agents:

- Triage Agent
- Product Agent
- Diagnostic Agent
- Waitlist Agent
- Handoff Agent

Minimum tools:

- read official product knowledge;
- read diagnostic ledger;
- read demo/waitlist/handoff state;
- propose diagnostic update;
- propose handoff;
- propose template plan.

Minimum guardrails:

- prompt injection;
- unsupported media;
- sensitive/out-of-scope refusal.

## Required Spike Scenarios

Run these before declaring the SDK path promising:

1. Cold greeting: `oi`
2. Pain-first: losing interested leads on WhatsApp because the team responds late
3. Price-first: asks price directly
4. Price plus pain: asks price and says WhatsApp follow-up is chaotic
5. Diagnostic start: asks for free diagnostic
6. Simple numeric answer during diagnostic: `120`
7. Diagnostic with urgency: completes all mandatory keys and final staged diagnostic
8. WhatsApp product question: asks whether Taliya connects to the studio WhatsApp
9. Demo request: asks to see it working
10. Waitlist curiosity without contract intent
11. Clear waitlist/contract intent after diagnostic or demo
12. Human handoff request
13. Do-not-do: `plano de 497` must not become 497 students
14. Do-not-do: asks for checkout/discount/date/VIP
15. Delivery concurrency simulation: inbound arrives during chunks, must defer

## Comparison Against Current Core

For each scenario, compare:

- transcript quality;
- structured understanding;
- evidence use;
- direct question handling;
- tool calls;
- handoffs;
- validator result;
- rendered output;
- Sales Inbox projection shape;
- model usage/cost;
- failure reason.

The SDK path must beat the current path on conversational understanding. Equal structural validity is not enough.

## Pass Criteria

The spike passes only if:

- no P0 failure;
- no direct question hidden behind diagnostic;
- pain-first response reuses concrete lead context naturally;
- diagnostic does not skip urgency;
- simple numeric answer is accepted;
- no repeated diagnostic question;
- no internal/source label leak;
- no product fact hallucination;
- no waitlist before qualified intent;
- human handoff pauses AI;
- SDK trace is clearer than current custom trace;
- no module starts growing into a new custom agent framework.

## Abort Criteria

Abort or rethink Agents SDK if:

- the SDK prototype still needs a large custom decision compiler to be useful;
- SDK handoffs make normal turns too expensive or incoherent;
- final output can only be controlled by reverting to action enum selection;
- tool side effects cannot be safely constrained;
- trace data cannot satisfy Sales Inbox/eval needs;
- the SDK path performs no better than current Spec 011 on critical scenarios.

## Paid Budget Rule

No paid SDK run should happen until:

- local/mocked spike structure is green;
- scenario fixture set is frozen;
- expected max calls and cost are estimated;
- the user explicitly approves the budget.
