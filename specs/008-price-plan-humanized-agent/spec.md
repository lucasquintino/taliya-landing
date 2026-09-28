# Feature Specification: Price, Plan And Humanized Agent Experience

**Feature Branch**: `008-price-plan-humanized-agent`  
**Created**: 2026-05-20  
**Status**: Draft  
**Input**: User wants to use Spec Kit to refine the Taliya sales agent across widget and WhatsApp. The agent must answer price and plan questions before steering, offer diagnostic as an optional recommendation path, keep direct plan comparison available, improve humanized message delivery in both channels, and add operational safeguards for cost, abuse, human handoff, lead merging, waitlist data quality, priority, media messages, funnel metrics, handoff and conversation closure.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Price And Plans Are Answered Without Blocking (Priority: P1)

As a lead, I want clear price and plan information when I ask for it, so I do not feel the diagnostic is being used to hide pricing or force a funnel.

**Why this priority**: Price and plan questions are high-frequency commercial intents. If the agent blocks the answer, trust drops immediately.

**Independent Test**: Can be tested by asking price/plan questions in widget and WhatsApp from cold, named, pain-captured, diagnostic-offered, diagnostic-in-progress and diagnostic-completed states.

**Acceptance Scenarios**:

1. **Given** a cold lead with no name, **When** they ask "quanto custa?", **Then** the agent answers the current plans/prices before asking for name or diagnostic context.
2. **Given** a lead asks "quero ver planos" without diagnostic, **When** the agent responds, **Then** it provides or offers direct plan comparison without making diagnostic mandatory.
3. **Given** a lead asks "qual plano faz sentido?" without diagnostic or equivalent context, **When** the agent responds, **Then** it does not recommend a final plan and instead offers a diagnostic as an optional recommendation path plus direct comparison as an alternative.
4. **Given** a lead asks price while diagnostic is in progress, **When** the agent responds, **Then** it answers pricing and preserves the diagnostic state.
5. **Given** a lead has completed diagnostic, **When** they ask about price or plans, **Then** the agent answers and uses the diagnostic recommendation as context without offering diagnostic again.
6. **Given** the public plans page and the agent both mention prices or plan details, **When** they are compared, **Then** both use the same commercial source of truth and cannot diverge.

---

### User Story 2 - Commercial CTAs Respect Readiness (Priority: P1)

As Taliya, I want plan comparison, checkout, waitlist and human handoff to appear only at the correct moment, so the agent feels consultative and does not overpromise.

**Why this priority**: The product is not broadly open yet, and early checkout/lista de espera creates false expectations.

**Independent Test**: Can be tested by running buy, plan recommendation, demo-positive, diagnostic-positive and diagnostic-negative paths in both channels.

**Acceptance Scenarios**:

1. **Given** no diagnostic or equivalent context, **When** the lead says "quero contratar", **Then** the agent does not send checkout and offers diagnostic or direct plan comparison to confirm the path.
2. **Given** diagnostic is complete and the lead responds positively, **When** they ask to advance, **Then** the agent may offer the limited-studios waitlist narrative.
3. **Given** demo was discussed and the lead responds positively, **When** they ask to advance, **Then** the agent may offer waitlist.
4. **Given** diagnostic or demo response is negative or uncertain, **When** the agent responds, **Then** it must not offer waitlist and must route to clarification, demo explanation or objection handling.
5. **Given** a lead asks only for price or plans, **When** the agent answers, **Then** it must not mark the lead as waitlist joined or checkout-ready.
6. **Given** demo is not configured or not ready, **When** the lead asks to see a demo, **Then** the agent must not pretend a demo exists and must offer an honest guided explanation, diagnostic or human help.

---

### User Story 3 - Widget And WhatsApp Deliver Messages Like A Human Conversation (Priority: P1)

As a lead, I want the chat experience to arrive in short, paced messages, so the assistant feels like a helpful attendant instead of a bot dumping text.

**Why this priority**: The user's main concern is the conversation feeling human. Message rhythm is part of the experience, not just copy.

**Independent Test**: Can be tested by observing first replies and multi-message replies in widget and WhatsApp for split messages, typing indicators, proportional delay and absence of user-message echo.

**Acceptance Scenarios**:

1. **Given** the first response in widget or WhatsApp has multiple ideas, **When** it is delivered, **Then** it appears as separate short messages instead of a single large block.
2. **Given** any automatic reply contains multiple messages, **When** each message is delivered, **Then** a typing indicator appears before the message.
3. **Given** a longer message, **When** it is delivered, **Then** delay is proportionate to message length within configured limits.
4. **Given** the lead sends a message, **When** the assistant replies, **Then** it does not repeat the lead's message literally.
5. **Given** the assistant has no enough context, **When** it asks a question, **Then** it asks one short question at a time.

---

### User Story 4 - Sales Inbox Shows Actionable Lead State (Priority: P1)

As a Taliya operator, I want every meaningful lead to show channel, stage, priority, waitlist state, diagnostic state and next action, so I can follow up when the product is ready.

**Why this priority**: Capturing leads is only useful if the operator can trust and act on stored state.

**Independent Test**: Can be tested by generating cold, warm, hot, waitlist and human-handoff leads and verifying the Sales Inbox record after each path.

**Acceptance Scenarios**:

1. **Given** a lead asks price only, **When** the conversation is stored, **Then** Sales Inbox marks it as cold unless additional intent exists.
2. **Given** a lead shares pain or starts diagnostic, **When** the conversation is stored, **Then** Sales Inbox marks it as warm.
3. **Given** a lead joins the waitlist, **When** the conversation is stored, **Then** Sales Inbox marks it as hot with `waitlistStatus=joined`.
4. **Given** a lead requests human help, **When** the conversation is stored, **Then** Sales Inbox shows human attention/handoff status and a next action.
5. **Given** required waitlist fields are missing, **When** the lead agrees to waitlist, **Then** Sales Inbox shows pending details, not joined.

---

### User Story 5 - Operational Guardrails Protect Cost, Abuse And Human Control (Priority: P1)

As Taliya, I want the agent to avoid runaway cost, spam, duplicate leads and automation after human intervention, so real lead traffic remains safe to operate.

**Why this priority**: Once divulgation starts, the system must not spend uncontrollably or answer over a human operator.

**Independent Test**: Can be tested by triggering rate limits, repeated messages, WhatsApp Business App human echoes and widget/WhatsApp duplicate identity flows.

**Acceptance Scenarios**:

1. **Given** a phone or session exceeds configured usage limits, **When** the lead sends another message, **Then** the agent sends a humanized pause message, records the reason and stops additional AI spending for that turn.
2. **Given** a human replies through WhatsApp Business App, **When** the lead sends another message, **Then** the AI stays paused and only records the inbound message.
3. **Given** a lead identifies with the same normalized phone or email in widget and WhatsApp, **When** both conversations are stored, **Then** they merge or associate into one lead without losing history.
4. **Given** only a matching name is available, **When** a second channel appears, **Then** the system does not auto-merge and may leave a suggested manual match.
5. **Given** a lead sends repeated spam-like messages, **When** the limit is reached, **Then** the lead is not dropped and the operator can see an attention state.

---

### User Story 6 - Media, Funnel Metrics, Handoff And Closure Are Explicit (Priority: P2)

As a Taliya operator, I want media messages, funnel events, human handoff and conversation closure handled predictably, so reporting and follow-up do not depend on memory.

**Why this priority**: Real WhatsApp leads will send audio/images and stop responding. The system needs a stable operational record.

**Independent Test**: Can be tested with unsupported media webhooks, funnel-step conversations, human handoff requests and stale/closed conversation transitions.

**Acceptance Scenarios**:

1. **Given** a lead sends audio, image, print, document or video, **When** the webhook is processed, **Then** the assistant asks for a short text summary and does not pretend to interpret the media.
2. **Given** a lead advances through price, diagnostic, demo or waitlist, **When** the conversation is stored, **Then** funnel events are recorded once per step without depending on external automation.
3. **Given** a human handoff trigger occurs, **When** the lead record is updated, **Then** next action and safe summary are visible to the operator.
4. **Given** a cold lead stops responding, **When** closure criteria are evaluated, **Then** the lead can move to waiting or cold-closed without follow-up templates.
5. **Given** waitlist is declined or joined, **When** the conversation ends, **Then** the final state remains explicit and is not overwritten by later generic replies.

### Edge Cases

- A first WhatsApp message is "quanto custa?" with no name.
- A first widget message is "quero ver planos" with no name.
- A lead asks for a recommendation but refuses diagnostic.
- A lead asks price while diagnostic is in progress.
- A lead asks "qual plano faz sentido?" after diagnostic completed.
- A lead says "quero contratar" before any pain or diagnostic context.
- A lead asks for discount, free plan or trial.
- A lead has only one pain, such as agenda, and asks if a smaller plan is enough.
- A lead has many pains and asks if the complete plan is required.
- A lead asks for a demo before demo is configured or available.
- A lead sends audio/image/document in cold state and in the middle of diagnostic.
- A human operator replies manually and the lead continues talking.
- The same lead appears in widget and WhatsApp with the same phone in different formats.
- A waitlist acceptance lacks studio name, city or contact.
- A conversation hits a rate limit at the beginning versus in the middle.
- A lead stops responding before diagnostic, after diagnostic offer, after waitlist offer, and after waitlist join.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The agent MUST answer price or plan questions before asking for diagnostic, name or additional context, including in cold widget and cold WhatsApp starts.
- **FR-001a**: Price, plan names, plan limits and commercial availability shown by the agent MUST come from the same source of truth used by `/pilates/planos` or a documented shared commercial config. Divergent hardcoded prices or plan details are not allowed.
- **FR-002**: The agent MUST present diagnostic as an optional path for plan recommendation, not as a prerequisite to see prices or plan comparison.
- **FR-003**: The agent MUST offer direct plan comparison as an alternative when the lead asks for plans, prices or recommendation before diagnostic.
- **FR-004**: The agent MUST NOT recommend a final plan without completed diagnostic or equivalent context.
- **FR-004a**: "Equivalent context" MUST mean operator-confirmed fit or enough lead-provided context to safely compare plans without final recommendation: known contact identity, clear primary pain or intent, studio size or operating context, and explicit interest in advancing. Pain-only context is not equivalent context.
- **FR-005**: The agent MAY provide a non-final hypothesis when the lead has a clear pain but no diagnostic, as long as it does not mark `plan_recommendation`.
- **FR-006**: The agent MUST NOT send checkout or checkout intent without a confirmed plan and clear buying intent.
- **FR-007**: The agent MUST NOT offer waitlist for price-only, plan-only, cold or uncertain leads.
- **FR-008**: The agent MUST NOT offer diagnostic again when `diagnosticCompleted=true`.
- **FR-009**: During an in-progress diagnostic, a price/plan side question MUST be answered and the diagnostic state MUST remain resumable.
- **FR-010**: If the lead asks to contract while the product remains limited, the agent MUST use the limited-studios waitlist narrative only after strong interest and minimum context.
- **FR-010a**: If a demo is unavailable or not configured, the agent MUST say that honestly and route to a guided explanation, diagnostic, plan comparison or human help; it MUST NOT invent a demo link or claim the lead has seen a demo.
- **FR-011**: The widget and WhatsApp MUST share commercial logic for price, plans, recommendation, buying, waitlist and human handoff.
- **FR-012**: Widget and WhatsApp MUST deliver automatic responses as short sequential messages with typing before each message and proportional delay.
- **FR-013**: Automatic replies MUST NOT repeat the lead's inbound message literally.
- **FR-014**: The system MUST enforce maximum message length for individual assistant message parts and split longer content into natural short messages.
- **FR-015**: The system MUST rate limit by WhatsApp phone/contact and widget session, with a separate global daily cap, configurable thresholds, reset windows and stored limit reasons.
- **FR-016**: Rate limit responses MUST be humanized and adapted to beginning versus middle of conversation.
- **FR-017**: Human intervention through WhatsApp Business App MUST pause AI until an explicit operator re-enable action.
- **FR-018**: While human is active, new inbound WhatsApp messages MUST be stored but not answered automatically.
- **FR-019**: The system MUST merge or associate widget and WhatsApp leads by normalized phone or normalized email.
- **FR-020**: The system MUST NOT auto-merge leads by name alone.
- **FR-021**: Waitlist joined state MUST require person name, contact, studio name, city/state, source channel, primary pain or diagnostic summary and explicit waitlist acceptance.
- **FR-022**: Missing waitlist fields MUST result in `waitlist_pending_details` until collected, and the missing fields MUST be operator-visible.
- **FR-023**: Lead priority MUST be derived from explicit criteria: cold for weak/price-only, warm for pain/diagnostic/demo interest, hot for waitlist joined/strong buying context/demo-positive/diagnostic-positive.
- **FR-024**: Human/manual priority MUST be set for human request, mid-conversation rate limit, send error, hot lead missing required details or hot unknown integration.
- **FR-025**: Unsupported media in WhatsApp MUST receive a text-summary request and MUST NOT start diagnostic or claim media understanding.
- **FR-026**: Funnel metrics MUST record key commercial events once per conversation step without relying on external automation, and must be inspectable through an internal report, API response or database query used by the verification report.
- **FR-027**: Human handoff MUST create an operator-visible next action and safe summary.
- **FR-028**: Conversations MUST support closure states including `waiting_user`, `cold_closed`, `waitlist_joined`, `waitlist_declined`, `human_active`, `do_not_contact` and `error_needs_attention`, with default or configurable evaluation windows documented before release.
- **FR-029**: This feature MUST NOT redesign, restyle or reorder the protected `/pilates` landing page.
- **FR-030**: The implementation MUST include automated eval matrices for price/plans, delivery/humanization, commercial state, WhatsApp webhook and lead pipeline.
- **FR-031**: The implementation MUST include manual test scripts for widget and post-deploy WhatsApp Web with DB cleanup by target number/session before each scenario. WhatsApp Web real-message tests are a post-deploy gate for divulgation, not a pre-deploy local gate.
- **FR-032**: Automated conversation evals MUST exercise the real agent/runtime path with controlled scenario count, budget guardrails and reportable model usage. Deterministic mocks may be used only for infrastructure checks, not as the acceptance signal for conversation quality.
- **FR-033**: WhatsApp webhook behavior MUST preserve existing security and idempotency guarantees, including expected payload validation, `phoneNumberId`/connection identification, provider message idempotency and no duplicate auto-replies.
- **FR-034**: If sending an assistant reply fails in widget or WhatsApp transport, the lead/session MUST remain stored, the failure MUST become operator-visible as `error_needs_attention` or manual priority, and the generated response MUST NOT disappear silently.

### Key Entities *(include if feature involves data)*

- **Price Plan Interaction**: A conversation turn where the lead asks about price, plans, comparison, recommendation or buying.
- **Recommendation Readiness**: Whether the agent can recommend a plan: none, pain-only hypothesis, diagnostic-complete recommendation, or operator-confirmed.
- **Message Delivery Policy**: Channel-agnostic rules for splitting, typing indicator, proportional delay, maximum message length and no inbound echo.
- **Lead Identity**: Normalized phone, normalized email, channel identifiers, name, studio name and city used to associate conversations.
- **Waitlist Qualification**: Minimum data and explicit acceptance required to mark a lead as joined.
- **Lead Priority**: Cold, warm, hot or manual/urgent classification derived from conversation state.
- **Funnel Event**: Durable event for conversation started, price asked, plans requested, diagnostic offered/accepted/completed, demo requested/positive, waitlist offered/joined/declined, human requested/active, rate limit and send error.
- **Conversation Closure State**: Final or waiting state used to decide whether the agent should continue, wait, stop or alert a human.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of price/plan eval cases answer price or plans before asking for diagnostic or context.
- **SC-002**: 100% of plan recommendation eval cases avoid final plan recommendation without diagnostic-complete or equivalent context.
- **SC-003**: 100% of diagnostic-complete price/plan cases avoid offering diagnostic again.
- **SC-004**: 100% of buy-intent cases avoid checkout unless plan and buying intent are confirmed.
- **SC-005**: 100% of early price/plan/buying cases avoid waitlist until strong interest and minimum context are present.
- **SC-006**: 100% of widget and WhatsApp delivery evals confirm split messages, no inbound echo and no oversized assistant blocks.
- **SC-007**: 100% of widget and WhatsApp delivery evals confirm typing-before-send path is exercised before every assistant message part.
- **SC-008**: 100% of rate-limit evals store the lead/session and stop further AI spending for the limited turn.
- **SC-009**: 100% of human intervention evals keep AI paused until re-enabled.
- **SC-010**: 100% of merge evals merge by strong identifiers and reject name-only auto-merge.
- **SC-011**: 100% of waitlist-joined evals contain the minimum waitlist data set.
- **SC-012**: 100% of media evals avoid pretending to understand audio/image/document content.
- **SC-013**: 100% of funnel metric evals avoid duplicate events on retry.
- **SC-014**: The final automated gate passes for commercial matrix, price/plan matrix, delivery matrix, WhatsApp webhook, sales humanization, lead pipeline, typecheck, lint and production build.
- **SC-015**: Widget manual tests and post-deploy WhatsApp Web real-message tests produce reports with transcript, final lead state, Sales Inbox status and pass/fail result for every selected scenario.
- **SC-016**: Before real divulgation starts, all operational guardrail tasks for cost/abuse, human resumption, merge, waitlist data quality, priority, media, funnel metrics, handoff and closure are implemented and verified; any smaller MVP is internal-only.
- **SC-017**: The technical deploy may happen after automated gates and local/manual widget checks pass, but real WhatsApp Web tests must pass after deploy before public lead capture or paid traffic starts.
- **SC-018**: 100% of price/plan source-of-truth evals confirm the agent and `/pilates/planos` use matching plan names, price framing and availability status.
- **SC-019**: 100% of conversation-quality acceptance evals run through the real agent/runtime path and include usage/cost reporting; deterministic mocks do not count as acceptance for tone, reasoning or CTA behavior.
- **SC-020**: 100% of send-failure and webhook-idempotency evals preserve lead visibility, avoid duplicate replies and surface operator action when needed.

## Assumptions

- The existing landing design remains approved and protected.
- The existing Taliya WhatsApp Business number and Dualhook/Meta webhook remain the only WhatsApp channel in scope.
- The same agent engine continues to serve widget and WhatsApp.
- Supabase/Postgres and the internal Sales Inbox remain the source of truth for leads and conversations.
- No follow-up templates or marketing messages outside the WhatsApp 24-hour window are added in this feature.
- Multi-tenant studio onboarding, customer WhatsApp numbers and the future seven customer agents remain out of scope.
