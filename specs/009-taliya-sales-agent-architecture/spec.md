# Feature Specification: Taliya Sales Agent Architecture

**Feature Branch**: `009-taliya-sales-agent-architecture`  
**Created**: 2026-05-21  
**Status**: Draft  
**Input**: User wants to redesign the Taliya commercial AI agent so it fulfills the original proposal with a reliable agent architecture and a much better lead experience in WhatsApp and widget. The new agent must keep the same business role: answer Taliya leads, explain product and plans, offer a free diagnostic at the right moment, generate a useful recommendation, offer the waitlist only after real interest, persist lead state in Sales Inbox/Postgres, pause for human takeover, and expose quality/cost/debug signals. The implementation should use the OpenAI Customer Service Agents Demo as the main architectural reference for triage, specialist agents, tools, guardrails, handoff and traces, while using Intercom Fin/Sierra-level quality expectations and Taliya-specific conversation policy.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural Openings By Source And Channel (Priority: P1)

As a lead arriving from WhatsApp, the site, Instagram, Facebook or an ad, I want the first response to match my context without sounding fake or like a form, so I trust the conversation enough to continue.

**Why this priority**: The first two messages decide whether the lead feels helped or handled by a bot. The current behavior asks for name too early and can sound aggressive.

**Independent Test**: Can be tested by starting fresh widget and WhatsApp conversations from each mapped source and checking the first assistant response, stored lead facts, and absence of premature data capture.

**Acceptance Scenarios**:

1. **Given** a cold WhatsApp lead sends only "bom dia", "oi" or equivalent, **When** the agent replies, **Then** it greets naturally, asks "Em que posso te ajudar?" or equivalent, and does not ask for name, phone, diagnostic, plans or waitlist.
2. **Given** WhatsApp provides a reliable profile name, **When** a new WhatsApp lead starts a conversation, **Then** the system saves the name and may open with "Oi, [first name]. Tudo bem?", without asking the name again.
3. **Given** WhatsApp provides a profile name that looks like a business, studio, emoji, number, single letter or low-confidence label, **When** the lead starts, **Then** the agent does not use it as a personal name and does not ask for a name until persistence requires it.
4. **Given** the lead clicks the site WhatsApp CTA with the forced message "Oi, vim pelo site da Taliya e queria entender como ela pode ajudar meu studio de Pilates.", **When** the agent replies, **Then** it responds warmly but plainly, explains Taliya briefly, and asks whether the lead wants the general idea or has a specific routine weighing on the studio.
5. **Given** the lead clicks Instagram or Facebook WhatsApp CTA with the forced message "Oi, vim pelo Instagram da Taliya e queria entender melhor como funciona para studios de Pilates." or Facebook equivalent, **When** the agent replies, **Then** it acknowledges the origin without sounding overly excited and asks a useful context question.
6. **Given** the lead clicks an ad CTA for diagnostic with the forced message "Oi, vim pelo anúncio da Taliya. Quero fazer o diagnóstico gratuito para entender o que organizar primeiro no meu studio.", **When** the agent replies, **Then** it presents the diagnostic clearly and sympathetically, asks for confirmation, and does not ask for phone.
7. **Given** any source opening, **When** the agent responds, **Then** it must not use false enthusiasm such as "que bom te ver por aqui", "incrível", "maravilha", "amei", emojis or repeated greetings.
8. **Given** a direct question is the first lead message, such as "quanto custa?", "quero ver planos", "quero uma demo" or "como funciona no WhatsApp?", **When** the agent replies, **Then** it starts with a short greeting ("Oi! Tudo bem?" or "Oi, [first name]. Tudo bem?" if a reliable name exists) and then answers the direct question before any steering or data capture.

---

### User Story 2 - Direct Questions Are Answered Before Steering (Priority: P1)

As a lead, I want direct answers about Taliya, pricing, plans, WhatsApp, demo, guarantees and limits before being steered to a funnel, so I do not feel the agent is hiding information or forcing me.

**Why this priority**: Trust is lost when a commercial assistant avoids the question and asks for data or diagnostic first.

**Independent Test**: Can be tested by asking direct questions in cold, named, pain-captured, diagnostic-offered, diagnostic-in-progress, diagnostic-completed and waitlist-joined states across widget and WhatsApp.

**Acceptance Scenarios**:

1. **Given** a lead asks "quanto custa?", **When** the agent responds, **Then** it answers with the current pricing range or plan values before offering diagnostic or plan comparison.
2. **Given** a lead asks "quais são os planos?", **When** the agent responds, **Then** it explains the plan structure and offers either direct comparison or recommendation by diagnostic.
3. **Given** a lead asks "qual plano faz sentido para mim?", **When** no enough context exists, **Then** the agent explains it should not guess and offers a diagnostic as an optional recommendation path.
4. **Given** a lead asks what Taliya is, **When** the agent responds, **Then** it explains Taliya as a CRM for Pilates studios with AI support for atendimento, agenda, vendas, financeiro and acompanhamento.
5. **Given** a lead asks how WhatsApp works, **When** the agent responds, **Then** it explains that the team remains in control and Taliya organizes context, history and routine responses.
6. **Given** a lead asks what happens if the AI does not know, **When** the agent responds, **Then** it says the AI must not invent, should ask for context or pass to the team.
7. **Given** a lead asks for demo before a full demo is available, **When** the agent responds, **Then** it must not pretend a demo exists and may offer a guided explanation, plans link, diagnostic or human help.

---

### User Story 3 - Diagnostic Is A Helpful Commercial Offer, Not A Form (Priority: P1)

As a lead, I want the free diagnostic to feel like a useful mini-consultation, so I understand why answering a few questions benefits me.

**Why this priority**: The diagnostic is the central commercial offer. If it sounds like a form or is offered too early, it creates resistance.

**Independent Test**: Can be tested by triggering diagnostic offers from pain, plan recommendation, "how Taliya would fit my studio", ad CTA and widget CTA states.

**Acceptance Scenarios**:

1. **Given** the lead shares a clear pain or asks how Taliya would fit their studio, **When** the agent offers diagnostic, **Then** it uses the approved offer pattern: "Se fizer sentido, posso te ajudar com um diagnóstico gratuito rapidinho. A ideia é entender um pouco da rotina do studio e te devolver um caminho mais claro: o que organizar primeiro, quais agentes fariam sentido e qual plano vale comparar. O que você acha?"
2. **Given** the lead only says "oi" or sends a cold greeting, **When** the agent replies, **Then** it must not offer diagnostic.
3. **Given** the lead asks a direct question, **When** the agent has not answered it yet, **Then** diagnostic cannot be offered before the answer.
4. **Given** the lead comes from an ad diagnostic CTA, **When** the agent responds, **Then** it re-explains the diagnostic in a friendly, non-false tone and asks "Pode ser?" or equivalent before starting.
5. **Given** the diagnostic is offered in WhatsApp, **When** the response is delivered, **Then** the offer is split into short messages with natural pacing.
6. **Given** the diagnostic is offered in the widget, **When** the response is displayed, **Then** it may use visual CTA affordances but must preserve the same commercial meaning.

---

### User Story 4 - Diagnostic Uses Only Necessary Questions And Adapts To Prior Context (Priority: P1)

As a lead, I want diagnostic questions to feel relevant and not repetitive, so the agent appears to listen and can produce a real recommendation.

**Why this priority**: Repeating questions already answered is one of the strongest signals that the assistant is a bot. The diagnostic must generate value, not collect every lead field.

**Independent Test**: Can be tested by starting diagnostic after the lead has already shared pain, tool usage, urgency or student count, and verifying repeated questions are skipped or reframed.

**Acceptance Scenarios**:

1. **Given** the lead already shared a pain before diagnostic, **When** diagnostic starts, **Then** the agent acknowledges it and skips the generic pain question.
2. **Given** the lead already gave student count, contact or current tool usage, **When** diagnostic needs those facts, **Then** it reuses them instead of asking again.
3. **Given** the lead accepts diagnostic on WhatsApp, **When** the system already has the WhatsApp phone number, **Then** it does not ask for phone.
4. **Given** the lead accepts diagnostic in the widget and no contact exists, **When** the diagnostic needs to be saved, **Then** the agent may ask for WhatsApp or email while allowing the user to continue without it.
5. **Given** no reliable name exists and the diagnostic must be saved, **When** the agent needs a person name, **Then** it asks naturally at that point, not at the opening.
6. **Given** diagnostic is in progress, **When** the lead asks price, demo, WhatsApp or any product question, **Then** the agent answers briefly and returns to the diagnostic without losing state.
7. **Given** diagnostic has enough information to produce a recommendation, **When** the agent delivers the result, **Then** it summarizes the main bottleneck, likely cause, recommended first step, indicated agents, plan to compare and asks whether it makes sense.

---

### User Story 5 - Lead Data Is Completed After Value, Not Before (Priority: P1)

As a lead, I want to give extra details only after I see value, so the conversation does not feel like lead capture disguised as help.

**Why this priority**: The user explicitly decided that diagnostic questions should be only those needed for diagnostic plus channel contact when necessary; missing lead data comes after diagnostic.

**Independent Test**: Can be tested by completing a diagnostic with no studio/city data and verifying those fields are requested only after positive response to diagnostic or waitlist agreement.

**Acceptance Scenarios**:

1. **Given** diagnostic is running, **When** the agent asks questions, **Then** it only asks for facts needed for diagnostic and not for studio name/city unless already volunteered.
2. **Given** diagnostic result is delivered, **When** the lead responds positively, **Then** the agent may offer the limited-studios waitlist narrative.
3. **Given** the lead agrees to waitlist, **When** required lead fields are missing, **Then** the agent asks for studio name and city/state in a natural single step.
4. **Given** the conversation is on WhatsApp, **When** waitlist details are collected, **Then** the system uses the channel phone automatically and does not ask for a phone number.
5. **Given** the conversation is in the widget and no contact exists, **When** the lead joins waitlist, **Then** the agent asks for WhatsApp or email to make follow-up possible.

---

### User Story 6 - Waitlist Appears Only After Real Interest And Remains Conversational (Priority: P1)

As Taliya, I want the waitlist to replace the unavailable purchase step only when the lead has real interest, so it feels like a next step rather than a barrier.

**Why this priority**: The product is not broadly open yet. Early waitlist offers can feel like rejection or a fake CTA.

**Independent Test**: Can be tested by running diagnostic-positive, diagnostic-negative, demo-positive, demo-negative, direct-buy and cold-interest paths.

**Acceptance Scenarios**:

1. **Given** diagnostic is complete and the lead says it makes sense, **When** the agent responds, **Then** it explains Taliya is working with a small number of studios and asks whether to place the studio on the waitlist.
2. **Given** diagnostic is complete and the lead is negative or uncertain, **When** the agent responds, **Then** it must not offer waitlist and should answer doubts, offer practical explanation, plans link or human help.
3. **Given** the lead wants to test, start or contract after enough context, **When** broad availability is not open, **Then** waitlist may be offered as the next step.
4. **Given** waitlist is joined, **When** the lead asks any follow-up question, **Then** the agent continues answering normally and does not restart diagnostic or offer waitlist again.
5. **Given** the lead asks to leave the waitlist, **When** the agent responds, **Then** the lead is marked declined/removed and the assistant does not insist.
6. **Given** the lead updates contact or studio details after joining waitlist, **When** the system saves the update, **Then** the waitlist state remains joined and the new data is visible to the operator.
7. **Given** the lead asks to sign, buy, pay, start now or contract before completing diagnostic in widget or WhatsApp, **When** broad availability is not open, **Then** the agent treats it as qualified high intent, explains the limited-studios context and routes the lead into the waitlist flow instead of checkout.
8. **Given** the lead clicks an "Assinar" or equivalent subscribe CTA on the landing, **When** the chat/WhatsApp flow opens, **Then** the entry is treated as qualified buying intent and routes to the waitlist flow with required details, not to payment.
9. **Given** any signing or buying intent routes to waitlist, **When** the agent explains the next step, **Then** it preserves the current waitlist narrative and must not create a new pre-sale, VIP priority, checkout substitute or apology-heavy framing.

---

### User Story 7 - Human Handoff Pauses The AI For Real (Priority: P1)

As a lead, I want the AI to stop when I ask for a person or when a person replies manually, so I do not get conflicting responses.

**Why this priority**: WhatsApp coexistence requires trust. If the AI responds over a human, the experience breaks.

**Independent Test**: Can be tested by requesting a human and by simulating a manual WhatsApp Business App reply, then sending more user messages.

**Acceptance Scenarios**:

1. **Given** the lead asks for a person, **When** the agent responds, **Then** it confirms a person can assume, saves context, marks human handoff requested and pauses automated replies.
2. **Given** a human has responded manually from WhatsApp Business App, **When** the lead sends another message, **Then** the system records the message but does not call the AI until explicit operator resume.
3. **Given** human handoff is active, **When** the operator views Sales Inbox, **Then** they see summary, lead state, source, last user messages and next action.
4. **Given** the conversation is resumed to AI, **When** the agent replies again, **Then** it acknowledges continuation without pretending it handled the human messages.
5. **Given** manual WhatsApp Business App intervention cannot be detected reliably from provider events, **When** an operator needs to stop automation, **Then** Sales Inbox must provide a manual pause control that prevents AI replies until explicit operator resume.
6. **Given** an outbound human message is identifiable from channel metadata or operator action, **When** it is recorded, **Then** the conversation must enter `human_active` and any queued AI response must be suppressed when possible.

---

### User Story 8 - Same Brain, Channel-Specific Delivery (Priority: P1)

As Taliya, I want widget and WhatsApp to share commercial reasoning while respecting the UX of each channel, so behavior is consistent without making WhatsApp feel like a website widget.

**Why this priority**: The user wants one commercial agent brain, not separate bots. Channel adapters should change delivery, not business truth.

**Independent Test**: Can be tested by running matched scenarios in widget and WhatsApp and validating outcome parity, state, stored facts and message delivery.

**Acceptance Scenarios**:

1. **Given** the same lead asks the same price question in widget and WhatsApp, **When** the agent responds, **Then** pricing truth and commercial policy match.
2. **Given** widget supports buttons/cards, **When** the agent offers plans, diagnostic or demo explanation, **Then** it may use CTAs.
3. **Given** WhatsApp does not have widget CTAs, **When** the agent offers plans or landing context, **Then** it uses short text and approved links instead.
4. **Given** any WhatsApp reply contains multiple ideas, **When** it is delivered, **Then** it is split into short messages, with typing indicator and proportional delay before each message.
5. **Given** any reply in any channel, **When** it is sent, **Then** it must not repeat the lead's message literally.

---

### User Story 9 - Operator Visibility, Cost And Quality Signals (Priority: P2)

As a Taliya operator, I want each lead to show state, source, diagnostic result, waitlist status, handoff status, agent trace and estimated cost, so I can operate and improve the funnel.

**Why this priority**: A better agent only matters if Taliya can trust, debug and act on the leads it creates. This is P2 because the core conversation behavior must be correct first, but records must still support cold, warm, hot, waitlist and handoff operations before production replacement.

**Independent Test**: Can be tested by generating leads from cold, warm, diagnostic, waitlist and human paths and verifying Sales Inbox records.

**Acceptance Scenarios**:

1. **Given** any identifiable lead conversation occurs, including a cold lead, **When** it is persisted, **Then** Sales Inbox shows source, channel, state, priority, next action and safe conversation summary.
2. **Given** diagnostic completes, **When** the lead is stored, **Then** the record includes diagnostic summary, indicated agents, plan to compare and whether the lead validated it.
3. **Given** waitlist is offered, joined, declined or pending details, **When** the operator views the lead, **Then** the exact waitlist state and missing fields are visible.
4. **Given** the agent responds, **When** the trace is saved, **Then** it records triage intent, specialist used, tools/actions, state before/after, guardrail result and token/cost estimate.
5. **Given** abuse, rate limit or low confidence occurs, **When** the system responds, **Then** the event is logged and the operator can see the reason.

---

### User Story 10 - Quality Gates Prove The Agent Feels Human And Commercially Correct (Priority: P1)

As the product owner, I want realistic simulations and qualitative evaluation before production replacement, so we do not ship an agent that passes string tests but feels bad in real conversations.

**Why this priority**: The current agent passed many tests and still felt far from ideal. The new acceptance gate must judge conversation quality, not only exact text.

**Independent Test**: Can be tested by running the required matrix with full transcripts, deterministic assertions and a quality judge score before enabling the new agent in production.

**Acceptance Scenarios**:

1. **Given** implementation is complete locally, **When** the simulation matrix runs, **Then** every P1 route has a full transcript for widget and WhatsApp where applicable.
2. **Given** a direct question appears in a simulation, **When** the transcript is judged, **Then** response-directness is mandatory to pass.
3. **Given** a diagnostic route starts after prior context, **When** the transcript is judged, **Then** repeated questions or early data capture cause failure.
4. **Given** WhatsApp delivery is evaluated, **When** messages are inspected, **Then** long blocks, missing typing, overly instant replies or phone-number requests cause failure.
5. **Given** a quality judge scores naturalness, consultative tone, non-aggressiveness, state continuity and commercial correctness, **When** any P1 scenario falls below the release threshold, **Then** the feature is not ready for production.
6. **Given** any evaluation transcript has a blocking failure, **When** the eval report is produced, **Then** the scenario fails regardless of average score.
7. **Given** a scenario fails or is borderline, **When** product-owner approval is requested, **Then** the failure must be fixed, explicitly waived with rationale, or converted into a spec change before production replacement.

---

### User Story 11 - Real Conversations Do Not Need To Follow The Script (Priority: P1)

As a lead, I may send unclear, mixed, emotional, corrected or out-of-order messages, and I still expect the agent to understand the useful parts, answer what I asked and continue naturally.

**Why this priority**: The new agent must be an AI agent with memory and judgment, not a larger scripted chatbot. Real WhatsApp and widget conversations rarely follow the ideal route.

**Independent Test**: Can be tested by running the chaos/free-form scenario matrix with realistic transcripts and judging semantic interpretation, state continuity, directness, no repetition and safe fallback behavior.

**Acceptance Scenarios**:

1. **Given** the lead sends multiple intents in one message, **When** the agent replies, **Then** it answers the direct question first, extracts useful facts, updates state and asks at most one clear next question.
2. **Given** the lead gives vague or ambiguous information, **When** the next step would be unsafe or likely wrong, **Then** the agent asks one short clarification instead of guessing or restarting.
3. **Given** the lead changes subject mid-flow, **When** the new subject is a valid commercial/product question, **Then** the agent follows the new subject, preserves prior state and returns only when useful.
4. **Given** the lead corrects or contradicts prior information, **When** the agent updates the record, **Then** it confirms naturally if needed and does not overwrite important facts silently.
5. **Given** the lead is irritated, skeptical or feels pushed, **When** the agent responds, **Then** it slows down, answers plainly, removes pressure and offers human help when appropriate.
6. **Given** the lead returns after days or after waitlist join, **When** they ask a new question, **Then** the agent resumes from stored context and does not act like a brand-new conversation.
7. **Given** the lead asks about signing, paying or starting immediately at any point, **When** the system is not broadly available, **Then** the agent routes to the qualified waitlist path and records high buying intent.

### Edge Cases

- WhatsApp profile name is a business name, emoji, single letter, phone number, studio name, "Atendimento", "Pilates", "Oficial" or otherwise not a reliable person name.
- The lead starts with greeting plus pain, greeting plus price question, or greeting plus "quero diagnóstico".
- The lead starts with a direct question without greeting, such as price, plans, demo, product, WhatsApp or human request.
- The lead asks to sign, buy, pay or start now before diagnostic, after pricing, after demo explanation or from a landing subscribe CTA.
- The lead sends a single message containing price, pain, current system, urgency and request to test.
- The lead answers vaguely, ignores the current question, answers out of order or gives multiple facts at once.
- The lead changes subject mid-diagnostic or after joining waitlist.
- The lead corrects or contradicts previously captured data.
- The lead is irritated, skeptical, says the assistant is a bot, or complains about being pushed.
- The lead comes from site/Instagram/Facebook forced message but asks price before answering the agent's follow-up.
- The lead comes from ad diagnostic CTA but then asks "quanto custa?" before confirming diagnostic.
- The lead shares a pain before diagnostic and repeats a different pain during diagnostic; the system must reconcile, not overwrite blindly.
- The lead asks a direct question in the middle of diagnostic.
- The lead refuses to share contact in widget but still wants diagnostic.
- The lead asks to talk to a human before any lead data exists.
- A human sends a manual WhatsApp reply while an AI response is queued.
- The lead asks about guarantees, cancelation, integrations, data privacy or unsupported promises after joining waitlist.
- The lead sends audio, image, document, print or unclear media.
- The lead abuses the chat, repeats messages quickly or tries to prompt-inject/system-prompt-extract.
- The lead returns days later after waitlist joined.
- The same person appears in widget and WhatsApp with matching phone/email or weak matching by name only.
- The conversation becomes inactive, commercially irrelevant, spammy or explicitly opted out.
- The lead uses informal or typo-heavy Portuguese.
- The lead uses English or mixed Portuguese/English.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST route every inbound lead message through a single commercial agent experience shared by widget and WhatsApp while allowing channel-specific delivery behavior.
- **FR-002**: The system MUST maintain an explicit conversation state for each lead using this closed set for the v2 agent: `new_lead`, `open_question`, `product_question`, `price_or_plan`, `diagnostic_offered`, `diagnostic_in_progress`, `diagnostic_completed`, `demo_interest`, `waitlist_offered`, `waitlist_pending_details`, `waitlist_joined`, `human_requested`, `human_active`, `closed`.
- **FR-003**: The system MUST infer the starting context from source and entry message, including direct WhatsApp, site WhatsApp CTA, Instagram/Facebook WhatsApp CTA, ad diagnostic CTA and widget CTA.
- **FR-004**: The system MUST use reliable WhatsApp profile names automatically for greeting and lead persistence, and MUST ignore low-confidence profile names for personal greeting.
- **FR-005**: The system MUST NOT ask for a name in the first cold WhatsApp/widget greeting unless the current action requires persistence and no reliable name exists.
- **FR-006**: The system MUST NOT ask for phone number in WhatsApp because the channel provides it automatically.
- **FR-007**: The system MUST answer direct product, pricing, plans, WhatsApp, demo, guarantee, cancelation and limitation questions before steering to diagnostic, waitlist or data capture.
- **FR-007A**: When a direct question is the first lead message in a new conversation, the system MUST prepend a short natural greeting before answering: "Oi! Tudo bem?" or "Oi, [first name]. Tudo bem?" if a reliable name exists.
- **FR-008**: The system MUST use the approved diagnostic offer policy and present diagnostic as a helpful mini-consultation, not as a form or mandatory gate.
- **FR-009**: The system MUST offer diagnostic only after relevant context, explicit diagnostic CTA, plan recommendation request, "how would it fit my studio" intent, or comparable commercial need.
- **FR-010**: The system MUST run diagnostic adaptively, reusing already known facts and avoiding repeated questions.
- **FR-011**: The diagnostic MUST collect only facts needed to produce a useful recommendation plus contact only where needed by channel; extra lead/studio fields MUST be collected after diagnostic value is delivered and the lead shows interest.
- **FR-012**: The diagnostic MUST produce a concise recommendation with main bottleneck, likely cause, first organization step, indicated agents, plan to compare and validation question.
- **FR-013**: The system MUST offer waitlist only after strong interest such as positive diagnostic validation, positive demo response, qualified buying/testing intent or equivalent high-intent signal.
- **FR-014**: The system MUST keep waitlist conversation open after join, allowing normal questions, detail updates, removal requests and human requests without restarting diagnostic.
- **FR-015**: The system MUST support human handoff where AI responses pause when the lead requests a person or when manual WhatsApp Business App intervention is detected.
- **FR-016**: The system MUST provide an explicit operator-controlled resume path from human-active state back to AI, without losing context; automatic timeout-based resume is out of scope for this release.
- **FR-017**: The system MUST split WhatsApp replies into short messages, show typing before each message and apply delay proportional to message length within configured bounds.
- **FR-018**: The system MUST use official links in WhatsApp where widget would use visual CTAs: landing `https://www.taliya.com.br/pilates`, plans `https://www.taliya.com.br/pilates/planos`, demonstration `https://www.taliya.com.br/pilates/planos/demonstracao`, and privacy `https://www.taliya.com.br/privacidade` when privacy/data questions require it.
- **FR-019**: The system MUST maintain correct PT-BR punctuation and accenting in user-facing Portuguese.
- **FR-020**: The system MUST avoid false enthusiasm, emojis, repeated greetings, repeated user-message echo, repeated name usage and repeated CTA wording.
- **FR-021**: The system MUST provide varied, context-sensitive acknowledgements rather than reusing the same feedback phrase repeatedly.
- **FR-022**: The system MUST preserve a trace of triage decision, specialist selected, actions/tools used, state before/after, guardrail results and estimated token/cost for each meaningful AI turn.
- **FR-023**: The system MUST persist every lead conversation that has an identifiable channel/session or meaningful commercial message, including cold leads, with lead state, diagnostic data when present, waitlist state when present, source, channel, summary, priority and next action to Sales Inbox/Postgres.
- **FR-024**: The system MUST classify and surface cold, warm, hot, waitlist and human-handoff leads in Sales Inbox; cold leads must be visible but must not be marked diagnostic-ready, waitlist-eligible or hot unless later messages justify it.
- **FR-025**: The system MUST enforce commercial guardrails preventing invented pricing, invented availability, unsupported integrations, promised launch dates, guaranteed financial results, hidden pricing and checkout while broad availability is closed or without sufficient confirmation/context.
- **FR-026**: The system MUST enforce abuse/cost guardrails, including rate limits, low-confidence fallbacks, media handling and prompt-injection refusal.
- **FR-027**: The system MUST expose enough evaluation artifacts to validate widget/WhatsApp parity for the same scenario.
- **FR-028**: The system MUST be fully validated in development/staging with realistic simulations before replacing the current production agent.
- **FR-029**: The system MUST include a kill switch or equivalent operational control to disable the new agent without disabling the rest of the landing.
- **FR-030**: The system MUST run the v2 agent as the production path after product-owner approval; partial rollout and shadow-mode comparison are out of scope.
- **FR-031**: The system MUST keep the approved `/pilates` visual/layout direction unchanged; this feature may only affect functional chat/CTA wiring, metadata, tracking or integration behavior.
- **FR-032**: After positive diagnostic validation and waitlist agreement, the system MUST collect missing lead details in this order: reliable person name if absent, studio name, city/state, and widget contact if absent; WhatsApp phone must never be requested.
- **FR-033**: The system MUST treat buying, signing, paying, starting now or clicking a landing "Assinar" CTA as qualified high intent and route the lead to the waitlist flow while broad availability is closed.
- **FR-034**: The system MUST interpret each full lead message semantically, extracting primary intent, secondary intents, useful facts, emotion, urgency, risk and unanswered direct questions before deciding the next response.
- **FR-035**: The system MUST support non-linear conversations, including ambiguous messages, multi-question messages, out-of-order answers, topic changes, corrections and contradictions, without relying on a fixed happy-path script.
- **FR-036**: The system MUST classify lead priority using clear rules for `cold`, `warm`, `hot`, `waitlist_ready`, `human_needed` and `no_action`.
- **FR-037**: The system MUST associate duplicate lead identities safely across widget and WhatsApp using phone or email as strong identifiers, session as a weak identifier and name alone as insufficient for automatic merge.
- **FR-038**: The system MUST support a `closed` conversation state without deleting lead history and MUST reopen or continue if the lead returns later.
- **FR-039**: The system MUST define humanized cost/abuse limit responses for early conversation, diagnostic-in-progress and post-waitlist states, while preserving logs and current lead state.
- **FR-040**: The system MUST handle audio, image, document and print messages without inventing content; when media cannot be interpreted reliably, it must ask for a text summary or offer human help.
- **FR-041**: The system MUST keep post-waitlist conversations fully conversational, including questions about prices, plans, demo, privacy, functionality, competitors, updates, removal and human handoff.
- **FR-042**: A waitlist record MUST be considered actionable only when it has at least one reliable contact path, studio name, city/state, source/channel, main pain or context summary, priority, status and next action; otherwise it remains `waitlist_pending_details`.
- **FR-043**: The waitlist flow MUST preserve the current limited-studios narrative: "Estamos trabalhando com um número pequeno de studios agora. Se fizer sentido, posso colocar seu studio na lista de espera e chamar assim que abrir uma próxima janela." The system MUST NOT introduce checkout, payment, pre-sale, VIP priority or a new waitlist positioning without explicit product approval.
- **FR-044**: The agent architecture MUST be cost-controlled by design, using structured state, compact conversation summaries, focused retrieval/tools and lightweight semantic classification where possible instead of relying on the most expensive model for every turn.
- **FR-045**: The system MAY escalate to a stronger model or deeper validation only for low-confidence, complex, safety-sensitive, evaluation, audit or recovery cases; default production turns MUST stay within the configured cost target when quality gates are met.
- **FR-046**: Response quality MUST come from state, tools, source-of-truth data, guardrails and evals, not from hardcoding scripts or assuming a high-cost model alone will solve conversation quality.
- **FR-047**: The system MUST persist conversation substate in addition to macro state, including asked questions, known facts, pending question, diagnostic step, missing lead fields, last topic, last direct question answered, lead sentiment/irritation level, confidence, last summary and queued/suppressed response status.
- **FR-048**: The diagnostic MUST use a structured schema for both inputs and output; it MUST NOT be considered complete until it has enough evidence for main bottleneck, likely operational cause, first organization step, indicated agents, plan to compare, confidence and validation question.
- **FR-049**: The system MUST use an official product/pricing source of truth for plan names, prices, included agents/routines, links, demo availability, waitlist availability, guarantees/cancelation rules, privacy link and unsupported promises; the agent MUST NOT rely on prompt-only facts for these items.
- **FR-050**: The system MUST expose the official product/pricing source through a controlled read path or tool used by both widget and WhatsApp responses to keep commercial truth consistent by channel.
- **FR-051**: The evaluation process MUST use a 1-5 judge scale by dimension, blocking-failure rules, minimum score thresholds, required scenario rounds and explicit product-owner approval before production replacement.
- **FR-052**: The system MUST support a manual Sales Inbox pause/resume fallback for human handoff when provider metadata cannot reliably identify WhatsApp Business App human intervention.
- **FR-053**: The system MUST define token/cost budgets by conversation type: simple answer, medium qualified lead, diagnostic lead, long/complex lead and evaluation run; budget breaches must be logged with scenario, reason and next action.
- **FR-053A**: The system MUST enforce a hard AI-cost cap of US$0.15 per lead conversation for automatic AI replies. When the cap is reached or projected to be exceeded, the system must stop automatic AI generation, preserve context, log the cap event and send only an approved "we will return soon" message if a reply is still needed.
- **FR-053B**: The evaluation runner MUST enforce an explicit test-run budget with dry-run, max-scenarios, max-real-model-calls and max-estimated-cost controls. A real-model eval run must stop before exceeding the configured budget and must report skipped scenarios separately from failures.
- **FR-054**: The approved waitlist copy in conversation policy MUST take precedence over any alternate example; alternate phrasing is allowed only if it preserves the same wording intent and does not change positioning.
- **FR-055**: WhatsApp delivery MUST use concrete pacing bounds: each outbound message must show typing before send, delay must be proportional to text length, and per-message delay must stay within configured minimum and maximum bounds.
- **FR-056**: The implementation MUST be layered so product knowledge, state/substate persistence, tools, response generation, guardrails, channel delivery and evals can be tested independently before the full agent is enabled.
- **FR-057**: The agent loop MUST follow an explicit sequence for each inbound message: normalize input, load state/substate, retrieve official product knowledge, interpret intent/facts/risk, decide tool actions, validate response, persist state/trace, then deliver through the channel adapter.
- **FR-058**: Every inbound channel event and agent tool action MUST be idempotent using stable message/action identifiers, so retries, rapid messages or duplicate webhooks cannot create duplicate waitlist entries, repeated replies or corrupted state.
- **FR-059**: State and substate updates MUST be atomic for each meaningful turn; out-of-order or concurrent messages must either be merged safely, queued or revalidated before sending a response.
- **FR-060**: Guardrails MUST be layered, with deterministic checks for hard rules where possible, including no WhatsApp phone request, no checkout while closed, no prompt leak, no prompt-only pricing, no response during human-active state and no duplicate merge by name alone.
- **FR-061**: When a guardrail blocks or changes a response, the system MUST log the blocking reason, preserve the lead state and choose a safe fallback instead of silently sending a degraded or contradictory answer.
- **FR-062**: The v2 agent MUST keep its kill switch able to disable automatic replies without disabling lead capture or logging.
- **FR-062A**: The production switch MUST default to v2 automatic replies. Legacy behavior and capture-only logging are explicit rollback/debug modes, not the default path.
- **FR-063**: Widget and WhatsApp MUST use separate channel adapters responsible only for transport, channel metadata, normalization support and delivery behavior; they MUST NOT own commercial reasoning or agent policy.
- **FR-064**: The system MUST use a cost-aware semantic interpretation layer before response generation to extract intent, secondary intents, direct questions, facts, risk, urgency, sentiment and whether stronger-model escalation may be needed.
- **FR-065**: The system MUST use an agent orchestrator to decide the next action from state, substate, semantic interpretation and product knowledge, including whether to answer, ask one clarification, continue diagnostic, offer diagnostic, route to waitlist, call a tool, hand off or escalate.
- **FR-066**: The response generator MUST receive compact state/substate, current message, selected action, official product knowledge when needed and conversation policy; it MUST NOT rely on full raw transcript or prompt memory by default.
- **FR-067**: Stronger-model escalation MUST be an explicit orchestrator decision with logged reason, not an implicit default of the response generator.
- **FR-068**: Channel delivery MUST happen only after guardrail validation and persistence of intended state/trace; WhatsApp splitting, typing and delay belong to the WhatsApp adapter, while widget buttons/cards/CTAs belong to the widget adapter.
- **FR-069**: The evaluation suite MUST test the layers separately and together: adapters, idempotency, state/substate, product knowledge, semantic interpretation, tools, response generation, guardrails, persistence, channel delivery and integrated conversation transcripts.
- **FR-070**: The architecture MUST optimize for high commercial quality with the lowest cost that does not harm directness, naturalness, state continuity, safety, diagnostic usefulness or commercial correctness.
- **FR-071**: n8n and any external automation MAY receive notifications or operator events, but MUST NOT be the source of truth for leads, prices, state, diagnostics, waitlist, payment, agent decisions or product facts. Airtable MUST NOT be used by this feature.
- **FR-072**: Database changes for this feature MUST include migration, verification and rollback instructions before production replacement, because lead state, waitlist and trace data are operationally important.
- **FR-073**: Product-owner approval MUST be recorded as a release-readiness artifact after reviewing representative passing transcripts, all failures, all waivers and cost reports. Approval MUST happen before enabling v2 automatic replies in production.

### Conversation Policy Requirements

- **CP-001**: Taliya's voice MUST be clear, calm, useful, direct and lightly warm; it must be prestativa, not animadora; consultiva, not aggressive; human, not overly intimate.
- **CP-002**: Approved light phrases include "Claro, te ajudo com isso.", "Boa, vamos por partes.", "Entendi.", "Faz sentido.", "Tranquilo.", "Pode ser." and "Vou usar o que você já contou."
- **CP-003**: The agent MUST avoid "que bom te ver por aqui", "incrível", "maravilha", "super", "amei", "ótima ideia", emojis, many exclamation points, and "Para eu te ajudar corretamente..." style phrases.
- **CP-004**: The standard diagnostic offer MUST be: "Se fizer sentido, posso te ajudar com um diagnóstico gratuito rapidinho. A ideia é entender um pouco da rotina do studio e te devolver um caminho mais claro: o que organizar primeiro, quais agentes fariam sentido e qual plano vale comparar. O que você acha?" Equivalent variants are allowed only if they preserve meaning and tone.
- **CP-005**: The site forced WhatsApp message MUST be "Oi, vim pelo site da Taliya e queria entender como ela pode ajudar meu studio de Pilates."
- **CP-006**: The Instagram/Facebook forced WhatsApp message MUST identify the social origin and ask to understand how Taliya works for Pilates studios.
- **CP-007**: The ad diagnostic forced WhatsApp message MUST be "Oi, vim pelo anúncio da Taliya. Quero fazer o diagnóstico gratuito para entender o que organizar primeiro no meu studio."
- **CP-008**: The agent MUST not repeat a previously asked question unless explicitly confirming an apparent contradiction, and that confirmation must be framed naturally.
- **CP-009**: The agent MUST answer direct questions first even when the same message also contains pain, urgency, competitor references, buying intent or diagnostic interest.
- **CP-010**: When the lead asks to sign or buy while the product is not broadly open, the agent MUST avoid checkout language and present the limited-studios waitlist as the next step.
- **CP-011**: When unsure, the agent MUST ask at most one concise clarification question, not a new form-like sequence.
- **CP-012**: After waitlist join, the agent MUST continue answering any reasonable commercial, product, plan, demo, privacy or competitor question without re-offering waitlist or restarting diagnostic.
- **CP-013**: Waitlist copy MUST keep the existing calm narrative and must not sound like an apology, scarcity trick, pre-sale promise, payment workaround or "VIP list".
- **CP-014**: The agent MUST prefer concise, context-aware responses that use stored facts and official product data before spending more tokens on broad re-explanation.

### Key Entities *(include if feature involves data)*

- **Conversation State**: Current stage of the lead conversation, source context, channel policy, known facts, asked questions, paused/human status and closure state.
- **Lead Profile**: Person and studio-level lead data, including reliable name, phone/email, source, channel, studio name, city/state, priority, readiness and next action.
- **Lead Identity Link**: Relationship between widget sessions, WhatsApp conversations, phones, emails and possible duplicates, including confidence and review requirement when automatic merge is unsafe.
- **Diagnostic Record**: Facts collected for recommendation, including student count, pain/intent, current workflow, pain-specific detail, priority, urgency, summary, indicated agents and plan to compare.
- **Waitlist Record**: Waitlist status, joined/declined timestamps, missing details, studio details, contact path and follow-up notes.
- **Product Knowledge Source**: Official commercial data used by the agent, including plans, prices, included routines/agents, URLs, demo status, availability, guarantees/cancelation, privacy link and unsupported claims.
- **Conversation Substate**: Fine-grained memory for asked questions, known facts, pending question, diagnostic step, missing fields, current topic, last answered direct question, sentiment/irritation, confidence and response queue state.
- **Diagnostic Schema**: Structured diagnostic input and output contract with evidence, confidence, recommendation and validation fields.
- **Evaluation Rubric**: Versioned scoring rules, blocking failures, scenario rounds, judge scores, product-owner decisions and waiver/change log.
- **Agent Loop Record**: Normalized input, state loaded, product source version, interpretation result, tool actions, response validation, persistence result, delivery result and any guardrail fallback.
- **Tool Action Record**: Idempotency key, tool name, input, output, status, retry count, side effects, failure reason and linked lead/conversation.
- **Channel Adapter**: Widget or WhatsApp transport component that normalizes channel metadata and delivers validated responses without owning commercial reasoning.
- **Semantic Interpretation Result**: Structured extraction of primary intent, secondary intents, direct questions, facts, urgency, sentiment, risk, confidence and escalation recommendation.
- **Agent Orchestration Decision**: The selected next action, tools to call, state transition, escalation decision, guardrail requirements and response objective for the turn.
- **Response Draft**: Candidate assistant output before guardrail validation and channel delivery, linked to source data and selected action.
- **Agent Trace**: Triage intent, specialist/route selected, actions/tools used, guardrail decisions, state before/after, cost estimate and debug reason.
- **Model Usage Record**: Model/classifier used, escalation reason if any, token usage, estimated cost and whether the turn stayed within the configured cost policy.
- **Handoff Record**: Human request/active/resume status, transcript summary, operator next action and pause reason.
- **Closure Record**: Reason and timestamp for `closed` state, such as opted out, no commercial intent, spam/abuse, human completed, waitlist complete or inactive.
- **Evaluation Transcript**: Scenario input, full channel transcript, expected state changes, deterministic assertions, quality judge score and review notes.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: At least 95% of P1 simulated conversations answer the user's direct question before asking for personal data, diagnostic, waitlist or handoff.
- **SC-002**: At least 95% of WhatsApp greeting scenarios do not ask for name or phone at opening, unless a persistence-required action is already in progress.
- **SC-003**: 100% of WhatsApp scenarios use the channel phone automatically and never ask the lead to type their phone number.
- **SC-004**: At least 95% of diagnostic scenarios avoid repeating a pain, tool, student count or urgency question already answered earlier in the conversation.
- **SC-005**: At least 90% of diagnostic-complete simulations receive a quality score of "useful" or better for recommendation specificity and commercial clarity.
- **SC-006**: 100% of waitlist-joined follow-up scenarios preserve waitlist state and do not restart diagnostic.
- **SC-007**: 100% of human-handoff scenarios pause AI responses until explicit operator resume.
- **SC-008**: At least 95% of WhatsApp multi-idea replies are delivered as short split messages with typing/delay behavior.
- **SC-009**: At least 90% of reviewed transcripts meet the quality threshold for naturalness, non-aggressiveness, directness, state continuity and PT-BR clarity.
- **SC-010**: The average estimated AI cost for a qualified medium lead remains at or below US$0.03 where possible and MUST stay below US$0.05 unless escalation is justified; any lead conversation at or above US$0.15 must block further automatic AI replies.
- **SC-010A**: 100% of cost-cap simulations must preserve lead context, log the cap event and avoid further AI-generated sales responses after the US$0.15 cap, except for the approved "we will return soon" fallback.
- **SC-011**: 100% of identifiable lead conversations, including cold leads, create or update a Sales Inbox record with source, channel, state, priority and next action.
- **SC-012**: The new agent passes all required development/staging simulations and receives explicit product-owner approval before replacing the current production agent.
- **SC-013**: At least 90% of chaos/free-form scenarios pass the quality threshold for semantic interpretation, directness, state continuity, no repetition and safe next action.
- **SC-014**: 100% of strong duplicate identifiers by phone or email are associated correctly, and 100% of weak name-only matches are kept separate or flagged for review rather than merged automatically.
- **SC-015**: 100% of signing/buying/subscribe CTA scenarios route to qualified waitlist flow while broad availability is closed and never initiate checkout.
- **SC-016**: At least 90% of production-intended simulated turns complete without stronger-model escalation while still passing quality gates; all escalations must include a logged reason.
- **SC-017**: 100% of waitlist-offer scenarios preserve the approved limited-studios narrative and do not introduce payment, pre-sale, VIP priority or apology-heavy framing.
- **SC-018**: 100% of P1 eval scenarios must have zero blocking failures; any blocking failure prevents production replacement regardless of average judge score.
- **SC-019**: Every P1 scenario must score at least 4/5 on directness, commercial correctness, state continuity and safety, and at least 4.2/5 average across all rubric dimensions.
- **SC-020**: At least two realistic variants must be evaluated for every P1 scenario route, including one normal route and one free-form/edge variant where applicable; each must include full transcript, state transitions, tool calls and cost estimate.
- **SC-021**: 100% of completed diagnostic simulations must produce all required diagnostic schema fields with evidence from the conversation or an explicit unknown/confidence marker.
- **SC-022**: 100% of plan/price/demo/availability responses must read from the official product knowledge source or trace the exact source version used.
- **SC-023**: 100% of conversations must persist macro state and substate before and after each meaningful AI turn.
- **SC-024**: 100% of human-handoff scenarios must pass either automatic intervention detection or manual Sales Inbox pause fallback.
- **SC-025**: 95% of WhatsApp outbound messages in simulations must respect typing/delay bounds and 100% must show no more than three text chunks per assistant turn unless human-approved.
- **SC-026**: 100% of duplicate webhook/retry simulations must result in no duplicate lead messages, no duplicate waitlist entries and no duplicate outbound replies.
- **SC-027**: 100% of guardrail-blocked simulations must include a logged reason, preserved state and an approved safe fallback response.
- **SC-028**: The feature is not ready for production replacement until product knowledge, state/substate, tools, guardrails, channel delivery and eval runner each have passing layer-specific tests plus passing integrated simulations.
- **SC-029**: 100% of sampled traces must show the full agent loop from channel adapter through semantic interpretation, orchestration decision, tool/source usage, response validation, persistence and channel delivery.
- **SC-030**: In production-intended simulations, at least 90% of turns must use the cost-aware default path without stronger-model escalation while still meeting all P1 quality thresholds.
- **SC-031**: 100% of real-model eval runs must respect the configured run budget and report total estimated cost, real-model call count, skipped scenarios and stop reason.
- **SC-032**: 100% of external automation checks must confirm that Sales Inbox/Postgres remains the lead source of truth and that Airtable is not part of the feature path.
- **SC-033**: Production replacement cannot be marked ready unless migration verification, rollback instructions and product-owner approval are documented.

## Assumptions

- The current Taliya public scope remains one Taliya-owned WhatsApp number and one commercial sales agent for Taliya leads; client/studio WhatsApp connections and the future seven customer agents remain out of scope.
- Existing widget, WhatsApp webhook, Supabase/Postgres storage and Sales Inbox concepts will be reused where possible.
- The approved `/pilates` visual/layout direction is protected and this feature does not redesign the landing.
- Pricing, plan names, plan URLs and product facts have or will have a single commercial source of truth.
- The plan phase must define the technical shape of the product knowledge source, diagnostic schema, conversation substate and evaluation runner without changing the business behavior defined here.
- The plan phase must decompose this feature into independently testable layers to reduce complexity risk; a single big-bang agent implementation is not acceptable for production replacement.
- WhatsApp profile names can be available from provider metadata but must be validated before personal use.
- WhatsApp supports links but not the same visual CTAs as the widget; official links for the v2 agent are `/pilates`, `/pilates/planos`, `/pilates/planos/demonstracao` and `/privacidade`.
- While Taliya is working with a small number of studios, every early signing or buying intent should become a qualified waitlist path rather than a payment/checkout path.
- Cost control is a product requirement: the implementation should improve quality through architecture, state, tools, data and evals first, using stronger models selectively rather than by default.
- The plan phase must preserve the architecture separation between adapters, semantic interpretation, orchestrator, tools, response generator, guardrails, persistence, delivery and evals.
- Human operators may answer in the WhatsApp Business App, so AI pause/resume is mandatory for trust; resume is explicit operator-controlled only.
- The new agent should be built and validated without changing the public `/pilates` layout; production replacement happens only after explicit approval, with no shadow-mode comparison or partial rollout.
- Evaluation must include realistic transcripts and quality judgment, not only keyword assertions.

