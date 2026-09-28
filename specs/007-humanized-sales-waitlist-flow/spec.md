# Feature Specification: Humanized Sales And Waitlist Flow

**Feature Branch**: `007-humanized-sales-waitlist-flow`
**Created**: 2026-05-20
**Status**: Implemented locally - automated review passed; R4 real WhatsApp smoke and R5 product-owner transcript review pending
**Input**: User wants to use Spec Kit to redesign the Taliya AI attendant behavior for both widget and WhatsApp. The same agent brain must serve both channels, but WhatsApp must feel like human commercial atendimento. The flow must start with name capture, then pain/intent discovery, then a free diagnostic. Waitlist is not an early CTA: it appears only after high intent, such as a positive response after diagnostic or a positive response after demo. "Waitlist offered" and "waitlist joined" are separate states: the lead only joins after explicitly agreeing to be placed on the list. The implementation must include review stages with realistic simulations before release.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - WhatsApp Starts Like Human Atendimento (Priority: P1)

As a WhatsApp lead, I want the first exchange to feel like a human attendant receiving me, so I do not feel pushed into a bot funnel before saying who I am.

**Why this priority**: WhatsApp is a direct conversation channel. If the first answer feels scripted or sales-heavy, the lead loses trust before the diagnostic can start.

**Independent Test**: Can be tested by sending fresh WhatsApp starts such as "oi", "ola", "quero saber valores" and "vi o site" and verifying the agent asks the person's name before pushing product, plans, demo or waitlist.

**Acceptance Scenarios**:

1. **Given** a new WhatsApp conversation with no known name, **When** the lead sends only a greeting, **Then** the agent asks "com quem eu falo?" or equivalent and does not mention diagnostic, demo, plans or waitlist.
2. **Given** a new WhatsApp conversation with no known name, **When** the lead asks for values, demo or product details, **Then** the agent acknowledges briefly and asks for the name before continuing.
3. **Given** the lead provides a name, **When** the next turn starts, **Then** the agent greets by name and asks a pain/intent question, not a waitlist or checkout question.

---

### User Story 2 - Same Agent Brain With Channel Policies (Priority: P1)

As Taliya, I want the widget and WhatsApp to use the same AI attendant brain while respecting each channel's context, so behavior is consistent without making WhatsApp feel like a website widget.

**Why this priority**: The user explicitly wants the same agent, not a separate WhatsApp bot. Channel policy is allowed, but core commercial reasoning, diagnostic and storage must remain shared.

**Independent Test**: Can be tested by running the same buyer intent through web and WhatsApp scenarios and verifying the same commercial truth and diagnostic logic, with different opening style only where channel requires it.

**Acceptance Scenarios**:

1. **Given** a web widget conversation, **When** the visitor opens the widget, **Then** the widget may use landing-context opening, quick replies, cards and CTAs.
2. **Given** a WhatsApp conversation, **When** the lead starts cold, **Then** the same agent brain uses WhatsApp policy: name first, pain/intent second, diagnostic offer third.
3. **Given** a product, price or demo question in either channel, **When** the agent answers, **Then** product facts, pricing boundaries and unsupported-promise rules match across channels.
4. **Given** a web widget visitor asks price, demo or plans before diagnostic, **When** the agent answers, **Then** it may use widget affordances but must still avoid checkout, broad availability and early waitlist.

---

### User Story 3 - Diagnostic Before Commercial CTA (Priority: P1)

As a lead, I want the agent to understand my studio before offering next steps, so the conversation feels useful rather than aggressive.

**Why this priority**: The desired funnel is diagnostic-led. Plans, demo and waitlist should be earned through context, not shown as cold shortcuts.

**Independent Test**: Can be tested by running conversations from name capture to pain/intent to diagnostic offer and verifying that the agent does not offer waitlist before the required intent gate.

**Acceptance Scenarios**:

1. **Given** the lead has provided name but no pain or intent, **When** the lead waits for the next question, **Then** the agent asks what made them look for Taliya or what they want help with.
2. **Given** the lead shares a pain or intention, **When** the agent responds, **Then** it acknowledges the answer and offers the free diagnostic as the natural next step.
3. **Given** the lead accepts the diagnostic, **When** the diagnostic starts, **Then** the agent asks one short question at a time and adapts to the answer.
4. **Given** the diagnostic is incomplete, **When** the lead asks for plans or demo, **Then** the agent answers briefly and steers back to completing the diagnostic unless the lead explicitly refuses.

---

### User Story 4 - Waitlist Only After High Intent (Priority: P1)

As Taliya, I want the waitlist CTA to appear only after the lead demonstrates strong interest, so it feels like a natural next step rather than a rejection or early barrier.

**Why this priority**: The product is not fully open for all studios yet. The waitlist must replace the final purchase step, not the diagnostic or demo experience.

**Independent Test**: Can be tested with post-diagnostic and post-demo positive/negative branches.

**Acceptance Scenarios**:

1. **Given** the diagnostic is complete, **When** the lead responds positively to the recommendation, **Then** the agent explains that Taliya is working with a small number of studios and asks whether to place the studio on the waitlist.
2. **Given** the diagnostic is complete, **When** the lead responds negatively or uncertainly, **Then** the agent does not offer waitlist and instead offers demo, clarifies the mismatch or answers doubts.
3. **Given** the lead has seen or requested a demo and responds positively, **When** they ask to advance, **Then** the agent offers the waitlist.
4. **Given** the lead asks to contract before diagnostic/demo context is sufficient, **When** the agent responds, **Then** it asks for minimum context or proposes diagnostic before waitlist.
5. **Given** the agent offered the waitlist, **When** the lead explicitly agrees to be added, **Then** the system marks the lead as joined; otherwise the lead remains offered, declined or undecided.

---

### User Story 5 - Operator-Visible Waitlist Storage (Priority: P2)

As a Taliya operator, I want leads, diagnostic state and waitlist state recorded in the sales inbox database, so no qualified interest disappears inside chat history.

**Why this priority**: The WhatsApp integration already stores conversations. The new commercial state must be visible and auditable before real lead traffic increases.

**Independent Test**: Can be tested by completing a simulated diagnostic-positive-waitlist path and verifying the lead appears with waitlist status, source channel, pain summary and next action.

**Acceptance Scenarios**:

1. **Given** a lead joins the waitlist, **When** the conversation is saved, **Then** the lead record includes waitlist status, joined timestamp, source channel and safe summary.
2. **Given** a lead declines or is unsure, **When** the conversation is saved, **Then** the lead is not marked as joined but keeps the appropriate commercial stage and next action.
3. **Given** a human takes over on WhatsApp, **When** manual echo is recorded, **Then** the agent pauses and the lead keeps its current stage without duplicate automated replies.
4. **Given** a lead has only a cold greeting or a direct question without name, **When** the conversation is saved, **Then** the system may store a WhatsApp session but must not mark the lead as waitlist eligible or joined.

---

### User Story 6 - Review Gates With Realistic Simulations (Priority: P1)

As the product owner, I want review stages with realistic start/middle/end simulations before implementation is considered done, so we can catch "chatbot-like", aggressive or mistimed CTA behavior before public traffic.

**Why this priority**: The user's main concern is conversation quality. Automated tests alone are not enough; scripted human review must be part of the acceptance path.

**Independent Test**: Can be tested by completing the review checklist and simulation matrix with pass/fail notes before deploy.

**Acceptance Scenarios**:

1. **Given** implementation is complete locally, **When** the review matrix is run, **Then** every P1 scenario has an expected response, prohibited behavior and pass/fail result.
2. **Given** a scenario fails because it feels robotic, aggressive or early, **When** the issue is logged, **Then** implementation cannot be considered ready until the scenario is corrected or explicitly accepted as a known risk.
3. **Given** production deployment is ready, **When** the final WhatsApp real-number smoke test runs, **Then** it validates name capture, pain/intent, diagnostic offer and no early waitlist.

### Edge Cases

- A lead sends name and intent in the same first message, such as "Sou Lucas, quero saber valores".
- A lead refuses to share a name but asks a direct question.
- A lead gives a nickname or first name only.
- A lead asks to contract immediately before giving enough context.
- A lead asks for demo before demos are ready.
- A lead responds "sim" ambiguously after diagnostic; the agent must infer from immediate context before offering waitlist.
- A lead gives a negative response after diagnostic or demo; the agent must not push waitlist.
- A widget visitor asks for price or demo immediately, where the UI has buttons/cards but the same commercial gates still apply.
- A demo is not yet available, but the lead asks to see one.
- A lead says "pode colocar" after waitlist is offered, but required fields are still missing.
- A lead moves between widget and WhatsApp; context may be merged only with strong identifiers.
- A WhatsApp Business App human reply pauses the agent.
- A lead sends opt-out language.

### Implementation Discovery & Change Control

During implementation, the team may discover missing conversation cases, storage fields, safety gates or review scenarios. These discoveries are allowed only when they stay inside this feature scope: humanized sales flow for the existing widget and the Taliya WhatsApp number, diagnostic-led qualification, waitlist after high intent and operator-visible storage.

Every discovered adjustment MUST be classified before production acceptance:

- **Clarification**: improves wording, examples or review notes without changing behavior. Update the relevant spec or simulation note.
- **In-scope behavior gap**: adds or corrects a conversation branch, state transition, eval or storage field needed to satisfy this spec. Update `spec.md`, `tasks.md` and `simulation-review-matrix.md` before or alongside the code change.
- **Out-of-scope expansion**: adds multi-tenant onboarding, client/studio WhatsApp numbers, seven customer agents, landing redesign, new pricing/billing flow or broad product availability. Defer to a future spec unless explicitly approved by the product owner.

If a discovery changes when the agent offers diagnostic, demo, waitlist or human handoff, at least one new simulation case MUST be added or an existing case MUST be amended before the change is considered ready.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST keep one shared AI attendant engine for widget and WhatsApp.
- **FR-002**: The system MUST support channel-specific conversation policy without duplicating the agent brain.
- **FR-003**: WhatsApp cold conversations MUST ask for the lead's name before product pitch, diagnostic offer, demo offer, plan offer or waitlist offer.
- **FR-004**: After a name is known, WhatsApp conversations MUST ask a pain/intent question before offering diagnostic, unless the lead already provided pain/intent in the same message.
- **FR-005**: The agent MUST offer the free diagnostic only after minimum name plus pain/intent context, except when the lead explicitly asks for diagnostic.
- **FR-006**: The agent MUST NOT offer waitlist before high intent is established.
- **FR-007**: High intent for waitlist MUST require one of: positive response after diagnostic recommendation; positive response after a demo that was shown or discussed; explicit contract/start request after minimum context is known; or human/operator decision.
- **FR-008**: A negative or uncertain response after diagnostic MUST route to demo, clarification or objection handling, not waitlist.
- **FR-009**: A negative or uncertain response after demo MUST route to objection discovery or open-ended help, not waitlist.
- **FR-010**: The agent MUST use the waitlist narrative: "estamos trabalhando com um numero pequeno de studios; podemos colocar o studio na lista de espera e chamar assim que possivel."
- **FR-011**: The system MUST record commercial stage for meaningful lead conversations as defined in FR-022.
- **FR-012**: The system MUST record waitlist status separately from generic lead status.
- **FR-013**: The system MUST preserve source channel and source detail for widget and WhatsApp leads.
- **FR-014**: The Sales Inbox/internal lead view MUST be able to distinguish diagnostic completed, demo interest, waitlist offered, waitlist joined and human handoff states.
- **FR-015**: WhatsApp automatic replies MUST remain paused after human intervention from WhatsApp Business App.
- **FR-016**: The implementation MUST include automated eval scenarios for cold opening, diagnostic offer, post-diagnostic positive, post-diagnostic negative, post-demo positive, post-demo negative and early contract request.
- **FR-017**: The implementation MUST include manual review stages with realistic simulations before production acceptance.
- **FR-018**: The agent MUST NOT claim the system is broadly available for immediate onboarding while waitlist mode is active.
- **FR-019**: The agent MUST NOT promise a specific waitlist date or approval timing unless configured later.
- **FR-020**: The widget MUST not be made visually different as part of this feature unless needed for CTA wiring or state copy; the protected `/pilates` layout remains unchanged.
- **FR-021**: "Minimum context" for a high-intent waitlist offer MUST mean at least a known person name plus one of: completed diagnostic recommendation, demo-positive signal, or explicit contract/start request with a known pain/intent.
- **FR-022**: "Meaningful lead conversation" for storage MUST start when at least one of these is true: the lead provides a name; the lead provides pain/intent; the lead accepts diagnostic; the lead asks for demo/plans/contracting; a human handoff occurs; or waitlist is offered/joined.
- **FR-023**: Waitlist status MUST use distinct values for not offered, eligible, offered, joined, declined and undecided; joined MUST only be set after explicit lead agreement.
- **FR-024**: If required waitlist fields are missing after the lead agrees, the agent MUST collect missing fields before final confirmation or mark the lead as waitlist pending-details.
- **FR-025**: If a lead refuses to share a name, the agent MUST answer reasonable direct questions briefly while making clear it can help better with a name later; it MUST NOT block all assistance or offer waitlist.
- **FR-026**: Demo state MUST distinguish not offered, offered, unavailable, viewed/discussed, positive and negative.
- **FR-027**: A demo may count as viewed/discussed only when the lead clicked/viewed a configured demo surface, or the agent delivered a demo-style explanation and asked whether it made sense.
- **FR-028**: The implementation MUST include widget-specific eval/review scenarios for price, demo, diagnostic-complete positive/negative, and waitlist CTA rendering.
- **FR-029**: Any in-scope improvement or missing case discovered during implementation MUST update the relevant spec, task and simulation artifact before production acceptance.

### Key Entities *(include if feature involves data)*

- **Conversation Channel Policy**: Channel-specific rules for opening tone, first required field, CTA rendering and message length.
- **Commercial Stage**: Current funnel stage for a lead. Allowed stages are `awaiting_name`, `awaiting_pain_or_intent`, `diagnostic_offered`, `diagnostic_in_progress`, `diagnostic_completed`, `recommendation_validation`, `demo_offered`, `demo_seen`, `waitlist_eligible`, `waitlist_offered`, `waitlist_pending_details`, `waitlist_joined`, `waitlist_declined`, `human_handoff`.
- **Diagnostic State**: Captured answers, pains, recommended agents, recommendation summary and completion status.
- **Demo State**: Whether demo was not offered, offered, unavailable, viewed/discussed, positive or negative.
- **Waitlist State**: Whether waitlist was not offered, eligible, offered, pending details, joined, declined or undecided, with timestamps and source channel.
- **Sales Lead**: Operator-visible lead record that stores contact, studio, channel, stage, safe summary, next action and waitlist/demo/diagnostic state.
- **Review Simulation Case**: Scripted conversation with channel, lead source, start/middle/end path, expected behavior, prohibited behavior and pass/fail result.

### Data Contract

The lead record MUST expose or store these stable fields, either as explicit columns or inside a documented JSON object:

- `commercialStage`: one of the Commercial Stage values.
- `waitlistStatus`: `not_offered`, `eligible`, `offered`, `pending_details`, `joined`, `declined` or `undecided`.
- `waitlistOfferedAt`: timestamp when waitlist is offered.
- `waitlistJoinedAt`: timestamp only after explicit agreement.
- `waitlistDeclinedAt`: timestamp when declined.
- `diagnosticStatus`: `not_started`, `offered`, `in_progress`, `completed` or `declined`.
- `diagnosticCompletedAt`: timestamp when diagnostic recommendation is delivered.
- `demoStatus`: one of the Demo State values.
- `demoOfferedAt` and `demoSeenAt`: timestamps when applicable.
- `leadSourceChannel`: `widget` or `whatsapp`.
- `leadSourceDetail`: route/source metadata safe for operator view.
- `primaryPainOrIntent`: short safe summary of what made the lead seek Taliya.
- `nextAction`: operator-readable next step.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of P1 WhatsApp cold-start simulations ask for name before diagnostic, demo, plan or waitlist.
- **SC-002**: 100% of P1 post-diagnostic positive simulations offer waitlist with the approved narrative.
- **SC-003**: 100% of P1 post-diagnostic negative simulations avoid waitlist and route to demo, clarification or objection handling.
- **SC-004**: 100% of P1 post-demo positive simulations offer waitlist with the approved narrative.
- **SC-005**: 0 P1 simulations contain prohibited behavior: early waitlist, checkout promise, broad availability claim, specific waitlist date promise, "beta" framing, or bot-like menu dump.
- **SC-006**: Every waitlist-joined simulated lead is visible in storage with source channel, waitlist status, stage and safe summary.
- **SC-007**: Automated evals and manual review matrix both pass before the feature can be marked ready.
- **SC-008**: Production smoke test with the Taliya WhatsApp number confirms name capture, pain/intent and diagnostic offer after deployment.
- **SC-009**: 100% of P1 widget simulations avoid early waitlist and broad availability claims.
- **SC-010**: 100% of waitlist-offered simulations keep `waitlistStatus=offered` until the lead explicitly agrees.
- **SC-011**: 100% of refused-name simulations still answer reasonable direct questions without offering waitlist.
- **SC-012**: 100% of implementation discoveries that affect behavior, storage or review expectations are reflected in Spec Kit artifacts before the feature is marked ready.

## Assumptions

- The current `runAiAttendantTurn` remains the shared agent engine.
- The current Supabase/Postgres storage remains the primary database for WhatsApp sessions and sales leads.
- Widget visual redesign is out of scope; only behavior, CTA gating and state wiring are in scope.
- Demos may be unavailable at implementation time; the agent must handle both demo-ready and demo-not-ready states.
- Waitlist is the final high-intent CTA while open self-serve signup is unavailable.
- The exact Sales Inbox UI can be minimal in this slice, as long as stored fields are queryable and operator-visible.
- The project must switch to an appropriate Spec Kit feature branch before implementation; current draft artifacts may exist while still on `master`.
