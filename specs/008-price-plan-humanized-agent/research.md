# Research: Price, Plan And Humanized Agent Experience

## Decision: Price and plan answers must precede diagnostic steering

**Rationale**: The user explicitly wants price transparency. The agent loses trust if it treats diagnostic as a gate before answering. The diagnostic should be framed as a recommendation aid.

Price and plan details must come from the same source of truth used by the public plans page or a documented shared commercial config, so the agent cannot drift from `/pilates/planos`.

**Alternatives considered**:
- Require diagnostic before prices: rejected because it feels evasive.
- Answer prices only after name capture on WhatsApp: rejected for direct price/plan first messages.

## Decision: Recommendation readiness has levels

**Rationale**: The system needs to distinguish a helpful hypothesis from a final plan recommendation. Pain-only context can support a cautious explanation, but not a final plan or checkout.

**Alternatives considered**:
- Never discuss fit before diagnostic: too rigid for natural sales.
- Recommend from any stated pain: too risky and may over-sell.

## Decision: Waitlist remains a high-intent CTA only

**Rationale**: The system is not broadly available. Waitlist must replace final purchase only after interest is strong, not appear after basic price or plans questions.

**Alternatives considered**:
- Offer waitlist after any buying phrase: rejected because cold buying intent still needs context.
- Hide waitlist until human review: rejected because the agent already needs to capture qualified demand.

## Decision: Message delivery is a shared experience contract

**Rationale**: Humanization depends on pacing and format in both widget and WhatsApp. The widget should not dump all messages at once if WhatsApp is paced.

**Alternatives considered**:
- Keep delivery pacing WhatsApp-only: rejected because user explicitly requires both channels.
- Let the model decide splitting: rejected because the channel should enforce maximum length and pacing.

## Decision: Conversation evals must use real agent simulation

**Rationale**: The user wants realistic simulations, not deterministic mock approval. Cost must be controlled by limiting scenario count, reporting usage and using budget guardrails, while keeping the agent/runtime path real for acceptance.

**Alternatives considered**:
- Use deterministic mock responses for acceptance: rejected because it does not test tone, reasoning or CTA timing.
- Run unlimited real-model evals: rejected because it risks unnecessary cost.

## Decision: Demo unavailable must be explicit

**Rationale**: Demo status may be false while the product is still being prepared. The agent should be honest and offer a guided explanation, diagnostic or human help instead of inventing a demo.

**Alternatives considered**:
- Pretend a demo exists: rejected because it damages trust.
- Block the conversation until demo is ready: rejected because price, plan and diagnostic paths can still move the lead forward.

## Decision: Human intervention pauses AI until explicit re-enable

**Rationale**: Coexistence with WhatsApp Business App requires avoiding automation over a human. Automatic resumption could confuse the lead and operator.

**Alternatives considered**:
- Resume after timeout: rejected for first release because it risks AI replying over an ongoing manual conversation.

## Decision: Lead merge uses strong identifiers only

**Rationale**: Phone and email can safely associate widget and WhatsApp. Name-only merge can corrupt leads when many studio owners share common names.

**Alternatives considered**:
- Merge by name + city automatically: rejected; use as future manual suggestion only.

## Decision: Waitlist data has a minimum quality contract

**Rationale**: Leads will be activated when the system is ready. A list without studio/city/contact/pain is not actionable.

**Alternatives considered**:
- Join waitlist immediately and fill fields later: rejected because it creates dirty waitlist records.

## Decision: Funnel metrics live in the primary system

**Rationale**: n8n and external tools must not be the source of truth. Funnel reporting should be derived from stored lead/conversation events.

**Alternatives considered**:
- Depend on n8n for funnel events: rejected because n8n is optional and can fail without losing state.

## Decision: Media messages request text summaries

**Rationale**: The current scope does not include audio/image understanding. The honest response is to ask for a short text summary.

**Alternatives considered**:
- Ignore media: rejected because it feels broken.
- Claim the media was understood: rejected because it is false and risky.

## Decision: Closure states are explicit but follow-up remains out of scope

**Rationale**: The system needs to know when a conversation is waiting, closed, joined, declined or human-active. Automated follow-up templates outside the 24-hour WhatsApp window are not part of this feature.

**Alternatives considered**:
- Add automated follow-ups now: rejected because it introduces template, consent and timing work outside this feature.
