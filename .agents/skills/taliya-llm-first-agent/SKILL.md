---
name: taliya-llm-first-agent
description: Keep the Taliya commercial sales agent LLM-first. Use before changing, optimizing, reviewing, testing, or debugging the Taliya Pilates commercial agent, especially files under services/taliya-agent-runtime, lib/landing/ai-attendant, WhatsApp/widget agent paths, behavior policy, templates, guardrails, evals, cost optimization, routing, triage, diagnostic, product questions, waitlist, or handoff. Prevent regressions back to deterministic chatbot/state-machine/regex-first behavior.
---

# Taliya LLM-First Agent

## Core Rule

Preserve the product intent: the Taliya commercial agent is an LLM-first sales attendant for Taliya leads on the widget and Taliya's own WhatsApp number.

The LLM is the conversation brain. Code provides guardrails, official facts, memory, tools, validators, rendering, persistence, delivery, cost controls, and safety boundaries.

Do not turn conversation understanding into a regex/state-machine/template-first chatbot.

## Allowed Determinism

Use deterministic code for operational boundaries where interpretation should not be creative:

- idempotency, HMAC, retries, persistence, delivery chunks, typing/delay, channel formatting;
- human handoff pause/resume, including "human active means automation stops";
- prompt injection refusal, sensitive data handling, unsupported media;
- product knowledge lookup and validators for prices, plans, links, checkout, availability, promises;
- template rendering after the LLM chooses the intent/action/template;
- cost accounting, hard caps, observability, tracing;
- widget empty opening and pure cold greeting only, if there is no product/pain/context signal.

These deterministic paths must remain small, explicit, and covered by tests.

## Forbidden Regression

Do not add or expand deterministic conversation shortcuts for:

- price, plan, demo, WhatsApp product questions;
- "quero saber mais", "vim pelo Instagram", "serve pro meu studio?", "como funciona?";
- pain-first messages;
- diagnostic acceptance when there is context or ambiguity;
- plan-fit/recommendation;
- buy/waitlist interest with mixed questions;
- long conversation state transitions;
- any message with two or more plausible intents.

For these, call the LLM and let it return structured JSON. If cost is a concern, reduce prompt size, retrieve fewer official facts, use a smaller model, cache official data, or add eval-based routing. Do not replace understanding with `if/else`.

## Required Architecture Pattern

When changing the agent, preserve this pipeline (action-first per
`specs/011-taliya-commercial-agent-core-reset/action-contract.md` and
`specs/012-.../design-lock-v2-action-first.md`, D-012-012):

1. Load official product knowledge and compact memory.
2. Deterministic Turn Situation Builder prepares the board from persisted
   state: mode, pending diagnostic key, allowed actions, eligible template
   groups. It must never interpret raw lead text commercially.
3. Ask the LLM to interpret the turn and return a compact structured action
   decision: selected action (from the allowed menu), intents, direct
   question, captured facts/slots, diagnostic/demo/waitlist/handoff intents,
   and the human composition variables (e.g. answer_feedback,
   pain_context_human) with evidence.
4. The Decision Compiler (code) expands the chosen action into state
   transition, template plan (including the full staged final diagnostic),
   and official-source variables. The LLM does not emit final template plans
   or official variable values - that pre-T011-105 boundary failed paid evals
   twice (T011-105 and the Spec 012 spike) and is superseded.
5. Validate and repair only against hard business rules; an action missing
   its required composition variables must fail, not silently fall back.
6. Render approved templates after validation.
7. Persist lead facts, diagnostic, waitlist, handoff, conversation, usage,
   and events.
8. Deliver as channel-specific short chunks with typing/delay.

Templates are approved language blocks, not the brain of the conversation.
The action menu constrains FORM, never MEANING: which action fits the lead's
message is always the LLM's semantic decision.

## Review Checklist

Before accepting code changes, answer these:

- Does a real ambiguous user message still go through the LLM?
- Did any new regex/token list become the primary decider for price/demo/plan/pain/diagnostic/waitlist?
- Are deterministic branches limited to operational/safety/cold-empty cases?
- Does the LLM still answer direct questions first and then steer naturally?
- Are official facts still sourced from product knowledge, not invented in prompts or templates?
- Are validators blocking hallucinated price, link, checkout, availability, and promises?
- Is human handoff actually paused in state and not just worded in the response?
- Are evals checking conversational behavior, not only exact strings?
- Did cost optimization reduce tokens without removing LLM judgment from commercial turns?

If the answer is unclear, stop and inspect the flow before editing further.

## Cost Optimization Rule

Optimize cost in this order:

1. Compact prompts and previous state.
2. Retrieve only relevant product knowledge keys.
3. Use `gpt-5.4-mini` or the configured low-cost model for normal turns.
4. Use templates for rendering after LLM decision.
5. Add deterministic shortcuts only for allowed operational cases.

Never optimize cost by making commercial understanding deterministic.

## Test Expectations

For any change touching routing, prompts, templates, diagnostics, product answers, or cost:

- include tests where LLM is required for mixed/ambiguous messages;
- include tests proving deterministic shortcuts do not catch product/pain/diagnostic mixed cases;
- run behavior transcripts for starts like greeting, Instagram, pain-first, price-first, demo-first, diagnostic-first, plan-fit, buy intent, human handoff;
- include at least one long conversation state test before shipping major changes;
- include cost/usage reporting, but treat low cost as suspicious if it means OpenAI was not called on commercial turns.

Good result: lower tokens with LLM still conducting.

Bad result: near-zero OpenAI cost because the agent stopped thinking.

## Taliya Scope Boundary

Keep scope narrow unless the user explicitly changes it:

- only Taliya's commercial lead agent for `/pilates`;
- widget and Taliya's own WhatsApp number;
- no customer/studio WhatsApp connections now;
- no seven customer agents now;
- no multi-tenant implementation now;
- no redesign of `/pilates`.
