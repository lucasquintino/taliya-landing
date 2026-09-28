# Research: Floating AI Attendant

**Feature**: [spec.md](./spec.md)
**Date**: 2026-04-30

## Decision: One Attendant Agent With A Guided Playbook

**Decision**: Implement one attendant agent that follows an attendance and consultative commercial flow: greet, answer doubts, identify pain, map pain to operational agents, explain value, qualify and route to guided demo, plan recommendation, checkout after recommendation, analysis or WhatsApp assisted close.

**Rationale**: The visitor needs one clear attendant, not a multi-agent architecture. The seven operational agents are the product being sold, not seven separate chat personalities inside the floating widget.

**Alternatives considered**:

- Multi-agent router inside the chat: rejected for v1 because it adds complexity and can confuse the attendance/sales journey.
- Static FAQ popup: rejected because it would not ask pains or qualify the owner.

## Decision: Sell The Configured Recommended/Highest-Value Plan By Default

**Decision**: The attendant must answer buyer questions first, diagnose the studio, then guide broad or multi-agent needs toward the configured recommended/highest-value plan. It should route to the guided demo when proof is needed, to the plans page when comparison is requested, and to checkout only after explicit buying intent or plan confirmation. Lower plans are used for comparison, budget-fit, narrow-scope requests and objection handling.

**Rationale**: The chat is a sales surface, not neutral support. If the visitor has several pains or wants the complete system, recommending a lower plan first weakens the offer and produces a worse sales experience.

**Alternatives considered**:

- Treat all plans equally: rejected because the product strategy is to sell the most complete/recommended plan when it fits.
- Always push the highest-value plan without answering questions: rejected because the visitor needs trust and clear answers before conversion.
- Hide lower plans entirely: rejected because they help handle budget objections and make the premium recommendation easier to understand.

## Decision: Mandatory Live AI With Guided Fallback

**Decision**: The first implementation must include a server-backed live AI response route for normal free-text conversations. Deterministic guided states remain available only as fallback for provider failure, timeout, blocked unsafe input or quick-reply convenience.

**Rationale**: The product promise requires a real AI attendant that can answer visitor questions naturally. The guided fallback still protects demos, builds and public runtime from provider failures, while approved context and guardrails keep claims controlled.

**Alternatives considered**:

- Guided chat only: rejected because the user explicitly requires a real AI layer.
- Live AI without fallback: rejected because provider failures or missing keys would break the sales surface.

## Decision: Keep The Floating UI In A Small Client Boundary

**Decision**: Render the floating agent as a dedicated Client Component from the landing orchestrator, with state isolated to the widget.

**Rationale**: Next.js 16 docs state that state, event handlers, effects and browser APIs belong in Client Components. Keeping the boundary narrow prevents the whole landing from becoming client-rendered.

**Alternatives considered**:

- Marking the entire landing as client code: rejected due to unnecessary bundle and hydration cost.
- Server-only chat rendering: rejected because open/close, typing and message input require client interactivity.

## Decision: Use Niche Config For Copy And Pain Mapping

**Decision**: Add floating-agent copy, quick replies, pains and pain-to-agent recommendations to the existing niche configuration model.

**Rationale**: The current landing is a multi-niche system. The floating agent should become reusable for future routes such as fisioterapia, estetica and personal without rewriting shared components.

**Alternatives considered**:

- Hardcode Pilates text in the component: rejected because it violates the multi-niche architecture.
- Store all agent prompts in one shared library: rejected because visible copy and pain mapping are niche-specific.

## Decision: Extend Existing Tracking Context

**Decision**: Reuse the landing tracking utility and add floating-agent event names and metadata.

**Rationale**: Existing landing events already require `niche`, `sourcePage`, `campaignStage` and `publicOfferMode`. The floating agent should contribute to the same funnel picture.

**Alternatives considered**:

- Create a separate analytics system for the agent: rejected for v1 because it fragments funnel data.

## Decision: Route Handler Only For Server-Side AI

**Decision**: Expose live AI through `app/api/landing/ai-attendant/route.ts`.

**Rationale**: Next.js 16 docs define Route Handlers inside `app` for custom request handlers, and secrets must not be exposed to Client Components. The route can validate input, apply guardrails, call the provider server-side and return structured metadata to the UI.

**Alternatives considered**:

- Calling an AI provider directly from the browser: rejected because it would expose credentials and bypass server-side guardrails.

## Decision: WhatsApp Is A First-Class Channel, Not The Chat Brain

**Decision**: Support WhatsApp through a server-side provider webhook that normalizes inbound messages into the same AI attendant core used by the web widget. WhatsApp reply delivery lives behind a provider adapter.

**Rationale**: Studio owners naturally use WhatsApp for attendance and sales. The agent should meet them there, but the conversation brain, guardrails, context, handoff and tracking must remain in the application backend so behavior stays consistent and auditable across channels.

**Alternatives considered**:

- Use n8n as the real-time WhatsApp chat brain: rejected because n8n should remain the post-handoff automation layer, not the place where every assistant turn, guardrail and model call is decided.
- Build a separate WhatsApp bot prompt: rejected because it would drift from the web widget and produce inconsistent agent behavior.
- Defer WhatsApp to later: rejected because the feature must work where this buyer already expects atendimento.

## Decision: WhatsApp Requires Server-Side Session And Idempotency

**Decision**: Add a server-side session/idempotency store for WhatsApp conversations, including provider message IDs, opt-in/opt-out state, recent safe history, qualification and handoff context.

**Rationale**: WhatsApp conversations happen outside the browser and provider webhooks can retry delivery. Client-only state cannot preserve context, prevent duplicate replies or respect opt-out.

**Alternatives considered**:

- Reuse only browser session state: rejected because WhatsApp has no browser session.
- Let n8n deduplicate messages: rejected because idempotency belongs at the application channel boundary before the AI core runs.
- Ignore duplicate webhook deliveries in v1: rejected because duplicate replies would damage trust quickly.

## Decision: Guardrails Are Acceptance Criteria, Not Prompt Suggestions

**Decision**: Treat refusals, unsupported claims, sensitive-data avoidance and fallback handoff as testable behavior.

**Rationale**: An AI attendant can receive prompt-injection attempts and sensitive information. The implementation needs explicit checks and adversarial scenarios, not just optimistic prompt wording.

**Alternatives considered**:

- Rely only on model instructions: rejected because prompt-only safeguards are not enough for a public attendant agent.
