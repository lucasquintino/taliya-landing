# RAG Policy - Spec 012

Revision 2026-06-10 (spike evidence): delivering the final diagnostic REQUIRES
reading official plan facts in the same turn - `recommended_plan_or_range`
must be grounded in `official_product_knowledge` with fact refs in evidence,
or the delivery is blocked. Under action-first (design-lock-v2), the Decision
Compiler injects official-source variables from retrieved refs; the model
never fills them.

Purpose: make the retrieval layer explicit without turning it into the conversation brain.

RAG means retrieval-augmented generation. In the Taliya commercial agent, RAG is the official-facts layer used by SDK agents to answer product questions safely.

## Core Rule

RAG is source of truth, not conversation control.

The SDK agents understand the lead and decide what needs to be answered or asked. RAG retrieves official facts. Validators enforce that product claims are grounded. The renderer turns validated proposals into approved customer-facing language.

## Approved Sources

Allowed retrieval sources:

- official product knowledge under `services/taliya-agent-runtime/app/shared/product_knowledge/`;
- Spec 006 product contracts;
- approved template catalog for language families and variable requirements;
- preserved Spec 010/011 behavior contracts for policy constraints.

Forbidden retrieval sources:

- landing copy as product truth unless explicitly promoted into official product knowledge;
- prior model outputs as product facts;
- traces, Sales Inbox notes, or lead claims as product truth;
- hardcoded prompt/template facts outside official knowledge;
- internet search during lead turns.

## Retrieval Modes

Allowed modes:

- key-based retrieval for known product facts such as price, WhatsApp scope, demo, waitlist, availability, and plan constraints;
- topic-based retrieval selected by the SDK agent through typed tool inputs;
- optional semantic retrieval later, only if it returns stable fact refs and source ids.

Initial implementation should prefer key-based and topic-based retrieval because the product surface is small and high-stakes.

## Claim Grounding

Every customer-facing product claim must map to:

```text
claim -> fact_ref -> source_id -> validator result
```

Examples of claims requiring fact refs:

- price;
- what Taliya does;
- what WhatsApp number/account is used;
- whether client/studio WhatsApp can be connected;
- demo availability or demo boundaries;
- waitlist/contracting availability;
- guarantees, discounts, dates, checkout, and support promises.

If a required fact is missing, the proposal must mark uncertainty and avoid inventing.

## SDK Tool Contract

`get_product_knowledge` and related retrieval tools:

- may return official facts, source ids, short summaries, and constraints;
- must not decide commercial route from raw lead text;
- must not generate final lead-facing text;
- must not mutate state;
- must not return unofficial facts;
- must include enough source metadata for validators and trace.

SDK agents may decide that retrieval is needed. Deterministic code may retrieve facts requested by the agent or needed by context policy, but deterministic retrieval must not become a commercial intent classifier.

## Validator Contract

Validators must fail if:

- a product claim lacks a fact ref;
- a fact ref points outside approved sources;
- the rendered text strengthens a fact beyond the retrieved source;
- price is confused with student count;
- WhatsApp scope is answered without official source;
- checkout, discount, launch date, VIP promise, or availability is invented;
- fallback/template text contains product facts not present in official knowledge.

## Trace Contract

Trace must record:

- retrieval tool name;
- retrieval input;
- source ids/fact refs returned;
- claims that used each fact ref;
- validator result for product claims;
- rendered variables that depend on retrieved facts.

## Eval Requirements

No-cost and paid evals must include:

- product question with fact refs;
- price question with fact refs;
- WhatsApp scope question with fact refs;
- unsupported/missing fact where the agent must avoid invention;
- do-not-do case where a product fact appears in text without a fact ref and fails.

## Anti-Determinism Boundary

RAG may answer "what facts exist?".

RAG must not answer:

- "what is the user's commercial intent?";
- "should we start diagnostic?";
- "should we offer waitlist?";
- "is this a buying intent?";
- "which conversational route should own this turn?";
- "which sales move is best now?".

Those decisions belong to the SDK agent proposal and are checked by validators/evals.
