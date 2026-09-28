# Feature Specification: OpenAI CS Agents Adaptation For Taliya Commercial

**Feature Branch**: `codex/010-openai-cs-agents-adaptation-for-taliya-commercial`  
**Created**: 2026-05-22  
**Status**: Product-owner final diagnostic/demo/name corrections specified; implementation and transcript approval pending  
**Input**: User wants to replace the current deterministic Taliya commercial agent with an LLM-first architecture that faithfully adapts `openai/openai-cs-agents-demo`. The new runtime must serve the Taliya-owned Pilates commercial widget and WhatsApp number only, preserve the protected `/pilates` layout, reuse existing channel/persistence/Sales Inbox assets, and prepare naming/runtime boundaries for future Taliya agents without implementing multi-tenant studio agents now.

## Corrective Behavior Gate *(mandatory)*

The implementation history showed that the first `010` runtime proved provider integration and several safety checks, but did not yet prove the full commercial behavior expected from the previous `009` policy. The binding behavior source for the corrective implementation is [behavior-contract.md](./behavior-contract.md), which ports the opening, diagnostic, waitlist, voice, name, handoff, and eval policies from `specs/009-taliya-sales-agent-architecture/`.

Final product-owner correction: the new agent must be **LLM-first but template-controlled**. The LLM is the interpreter/director that chooses behavior, state transition, facts, and `template_ids`; approved message templates are the official voice. The old deterministic state machine, regex classifier, template-first orchestrator, and if/else response generator must not be the conversation brain. Conversely, a free-form LLM answer must not bypass templates, product knowledge, validators, Sales Inbox persistence, or channel delivery rules.

The binding contract set for this feature is:

- [behavior-contract.md](./behavior-contract.md): commercial behavior, state policy, voice, diagnostic, waitlist, handoff, safety.
- [conversation-state-contract.md](./conversation-state-contract.md): canonical states, allowed transitions, and state tendencies.
- [message-template-contract.md](./message-template-contract.md): template library policy, template IDs, variables, renderer, and fallback rules.
- [diagnostic-contract.md](./diagnostic-contract.md): mandatory diagnostic questions, fact reuse, no-repeat rule, and completion criteria.
- [sales-inbox-contract.md](./sales-inbox-contract.md): complete lead persistence and operator visibility.
- [product-followup-delta-contract.md](./product-followup-delta-contract.md): missing product explanation, post-diagnostic follow-up, comparison, integration/scope, security/data, out-of-profile, diagnostic-refusal, and conversation-resume behavior.
- [eval-plan.md](./eval-plan.md): quota-aware local and real-OpenAI validation gates.

The final implementation is not production-ready until the behavior contract is implemented and verified with real OpenAI transcripts. Smoke tests, mock tests, and string-only checks are insufficient for final acceptance.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Leads Get An LLM-First Commercial Conversation (Priority: P1)

A Pilates studio lead can message the Taliya widget or the Taliya-owned WhatsApp number with a natural, ambiguous, mixed, or direct message and receive a useful commercial answer that feels like an intelligent sales attendant rather than a scripted chatbot.

**Why this priority**: The main failure of the current v2 is architectural. It passes many tests but behaves like deterministic state machine software. The replacement must prove that the model conducts the conversation.

**Independent Test**: Can be tested by sending realistic free-form widget and WhatsApp messages and verifying that the runtime invokes the LLM-first runner, returns structured output, selects approved template IDs, uses tools for official facts, and avoids deterministic template-only decision logic.

**Acceptance Scenarios**:

1. **Given** a new lead asks "quanto custa e sera que serve para studio pequeno?", **When** the message enters either channel, **Then** the agent answers price/fit directly, uses official product knowledge, and naturally offers the next helpful step without asking for a phone number.
2. **Given** a lead sends a confusing mixed message with price, pain, and urgency, **When** the agent responds, **Then** it answers the direct question first, identifies useful facts, and asks at most one focused follow-up.
3. **Given** the same lead continues out of order, **When** the next turn runs, **Then** the runner uses conversation context and does not require the lead to follow a fixed script.

---

### User Story 2 - Architecture Follows The OpenAI Customer Service Agents Demo (Priority: P1)

The implementation uses the OpenAI Customer Service Agents Demo as a binding architecture reference: agents, triage, tools, handoffs, guardrails, context, memory, runner events, and traceable output are adapted to the Taliya commercial domain.

**Why this priority**: The previous implementation referenced the demo but did not copy the operating pattern. This feature exists to correct that drift.

**Independent Test**: Can be tested by inspecting the new runtime structure and verifying a file-by-file mapping from the reference demo to the Taliya runtime, with LLM-runner decisions replacing deterministic orchestration.

**Acceptance Scenarios**:

1. **Given** the new runtime is inspected, **When** agent definitions are opened, **Then** triage and specialist agents are explicit runtime objects with instructions, model choices, tools, guardrails, and handoffs.
2. **Given** a conversation changes topic, **When** the runner processes the turn, **Then** the current agent and handoff history are persisted and visible in traces.
3. **Given** a tool action such as waitlist or handoff is needed, **When** the model selects the action, **Then** the side effect is executed through an idempotent tool boundary, not by hardcoded conversation flow.

---

### User Story 3 - Price, Plan, Demo, And Availability Answers Use Official Knowledge (Priority: P1)

A lead who asks about price, plans, demo, waitlist, availability, links, cancellation, or checkout receives a direct answer based only on the official product knowledge source.

**Why this priority**: Sales trust depends on not hiding price and not inventing links, checkout availability, or promises.

**Independent Test**: Can be tested with direct and mixed product questions across fresh, diagnostic, waitlist, and handoff-adjacent states.

**Acceptance Scenarios**:

1. **Given** a lead asks "qual o plano e preco?", **When** the agent answers, **Then** the answer includes official plan/price facts and records the product source version used.
2. **Given** a lead asks for checkout while broad availability is closed, **When** the agent responds, **Then** it does not invent checkout and explains the correct demo or waitlist path.
3. **Given** the product knowledge source is missing a requested link, **When** the agent needs that link, **Then** it does not fabricate one and either offers the known page or pauses for human follow-up.

---

### User Story 4 - Diagnostic Is Adaptive And Evidence-Based (Priority: P1)

A lead who shows interest can receive a short, useful diagnostic based on the facts they already shared, with no fake certainty, no repeated questions, and no generic "pelo que voce contou" language when evidence is thin.

**Why this priority**: The diagnostic is the main value bridge between curiosity and waitlist intent. It must feel consultative, not like a scripted form.

**Independent Test**: Can be tested with leads who share rich context, thin context, conflicting context, and no context.

**Acceptance Scenarios**:

1. **Given** a lead has shared pain and current process before formally accepting diagnostic, **When** the diagnostic starts, **Then** those answers are marked as already answered and are not asked again.
2. **Given** a lead has shared almost no facts, **When** a diagnostic is requested, **Then** the agent asks the next mandatory focused question before concluding.
3. **Given** the diagnostic completes, **When** it is stored, **Then** every mandatory diagnostic question is answered by current input, inferred from prior evidence, or marked not applicable; any required unresolved question blocks completed status and remains a next question.

---

### User Story 5 - Waitlist Appears Only After Real Interest (Priority: P1)

A lead is offered the waitlist only after showing clear intent to contract Taliya. This intent can appear directly, or after a diagnostic is delivered and the lead asks about starting, next steps, price/plan to proceed, or being notified.

**Why this priority**: Early waitlist offers feel like rejection or fake scarcity. Waitlist should be a qualified next step.

**Independent Test**: Can be tested with cold, warm, high-intent, diagnostic-positive, diagnostic-negative, and direct-buy conversations.

**Acceptance Scenarios**:

1. **Given** a cold lead only says "oi", **When** the agent responds, **Then** it does not offer waitlist.
2. **Given** a lead asks to contract, start, enter, be notified, or proceed after diagnostic, **When** the agent responds, **Then** it can offer waitlist naturally and collect only missing actionable details.
3. **Given** a lead joins the waitlist, **When** the record is saved, **Then** Sales Inbox shows the waitlist status, priority, contact path, summary, and missing fields.

---

### User Story 6 - Human Handoff Pauses Automation Across Channels (Priority: P1)

When a lead asks for a human, a human replies through WhatsApp Business App, or an operator pauses the lead in Sales Inbox, the AI stops responding and preserves the conversation for human follow-up.

**Why this priority**: WhatsApp coexistence only works if the AI never talks over a human.

**Independent Test**: Can be tested by explicit human requests, manual WhatsApp Business App echoes, Sales Inbox pause/resume actions, and duplicate webhook retries.

**Acceptance Scenarios**:

1. **Given** a lead asks for a human, **When** the turn runs, **Then** a handoff event is persisted and subsequent inbound messages do not receive AI replies while human is active.
2. **Given** a manual WhatsApp Business App response is detected, **When** the next inbound arrives, **Then** automation remains paused.
3. **Given** an operator resumes automation, **When** the next inbound arrives, **Then** the agent can continue from the last safe state with full context.

---

### User Story 7 - Operators Can Inspect Leads, Runs, Tools, Handoffs, And Cost (Priority: P2)

Taliya operators can use Sales Inbox to understand what the agent did, why it did it, what facts it learned, what tools were called, whether guardrails fired, and how much the conversation cost.

**Why this priority**: LLM-first systems need transparency. This is P2 because the lead-facing conversation is the core MVP, but production trust requires these records.

**Independent Test**: Can be tested by creating representative conversations and opening Sales Inbox lead details.

**Acceptance Scenarios**:

1. **Given** a conversation has product, diagnostic, waitlist, and handoff events, **When** an operator opens the lead, **Then** the relevant facts and summaries are visible without reading raw trace JSON.
2. **Given** guardrails or cost caps fired, **When** the lead is inspected, **Then** Sales Inbox shows the reason and recommended operator action.
3. **Given** model usage is recorded, **When** a report is generated, **Then** actual token usage and cost are available per run and per lead.

---

### User Story 8 - Runtime Names And Contracts Support Future Agents Without Implementing Them (Priority: P2)

The new Railway service is named and structured as a generic Taliya agent runtime that can later host configuration and studio operation agents, while the only implemented active agent in this spec is `taliya_commercial`.

**Why this priority**: The platform will later need multiple agents. Naming the runtime too narrowly would create avoidable debt.

**Independent Test**: Can be tested by checking endpoint contracts, table names, source structure, and stored records for generic `agent_key`, `agent_family`, `owner_scope`, and nullable `tenant_id` fields.

**Acceptance Scenarios**:

1. **Given** a request is sent to the runtime, **When** the body includes `agent_key: "taliya_commercial"`, **Then** it routes to the Taliya commercial agent.
2. **Given** a request uses an unknown future agent key, **When** the runtime handles it, **Then** it rejects the request safely without creating partial state.
3. **Given** storage is inspected, **When** agent runtime tables are reviewed, **Then** they are not named `sales_agent_*` or `agent_v2_*`.

---

### User Story 9 - Quality Gates Prove The New Agent Is Better Than The Old One (Priority: P1)

Before the new runtime becomes the official production path, automated and manual gates prove that it is more natural, safer, more useful, and more faithful to the target architecture than the current deterministic implementation.

**Why this priority**: The current implementation passed tests that were too narrow. The replacement must not repeat that mistake.

**Independent Test**: Can be tested by running the required eval suite and reviewing generated transcript reports before production deploy.

**Acceptance Scenarios**:

1. **Given** evals run on direct, ambiguous, diagnostic, waitlist, handoff, and safety scenarios, **When** results are generated, **Then** blocking failures are separated from judge quality scores.
2. **Given** an answer is technically correct but robotic, **When** the quality judge scores it, **Then** it can fail on naturalness or usefulness.
3. **Given** eval cost limits are reached, **When** the report is produced, **Then** skipped scenarios are marked as skipped and do not count as passed.

### Edge Cases

- The model API times out or returns invalid structured output.
- Product knowledge is unavailable, stale, or missing a requested fact.
- The lead sends audio, image, document, sticker, or empty text.
- The lead sends prompt injection, asks for system prompt, or tries to override tools.
- The lead asks for price and human help in the same message.
- The lead asks multiple unrelated questions in one message.
- The lead answered a diagnostic question before the diagnostic formally started.
- The lead gives a studio name or WhatsApp profile name that is not a real person name.
- The lead asks to contract before any diagnostic is delivered.
- The lead asks to contract immediately after diagnostic is delivered.
- Duplicate WhatsApp webhooks arrive after a response was already sent.
- A human handoff becomes active while an AI response is queued.
- A conversation hits the automatic cost cap.
- A lead uses widget and WhatsApp with only weak identity evidence.
- A future `agent_key` is accidentally sent before the agent exists.
- The `/pilates` page is touched by integration wiring and could regress visually.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The new runtime MUST replace the current deterministic v2 as the official production conversation path for the Taliya-owned commercial widget and WhatsApp number.
- **FR-002**: The runtime MUST be LLM-first: normal user turns must be handled by an agent runner and model decision, except for explicit operational fallbacks such as human pause, invalid request, unsupported media, API outage, or disabled automation.
- **FR-003**: The architecture MUST faithfully adapt the structure of `openai/openai-cs-agents-demo`, including agent definitions, triage, tools, handoffs, guardrails, context, memory, runner events, and traceable structured output.
- **FR-004**: The implementation MUST include a documented reference map from the OpenAI demo files to the Taliya runtime files.
- **FR-005**: The runtime service MUST be named generically as `taliya-agent-runtime`, not as a single sales-agent service.
- **FR-006**: The active agent key for this feature MUST be `taliya_commercial`.
- **FR-007**: The runtime MUST expose a generic agent-run contract that routes by `agent_key`.
- **FR-008**: Unknown or disabled agent keys MUST be rejected safely and must not create partial side effects.
- **FR-009**: The runtime MUST be prepared for future agent families through naming and storage fields, but MUST NOT implement multi-tenant studio agents in this feature.
- **FR-010**: The feature MUST NOT connect WhatsApp numbers owned by client studios.
- **FR-011**: The feature MUST NOT implement the seven future studio operation agents.
- **FR-012**: The feature MUST NOT redesign, reorder, restyle, or replace the protected `/pilates` landing layout.
- **FR-013**: Before implementation changes that can affect landing behavior, a desktop and mobile `/pilates` baseline MUST be captured or confirmed.
- **FR-014**: Next.js route/runtime code changes MUST follow the local Next.js docs under `node_modules/next/dist/docs/` before editing.
- **FR-015**: Next/Vercel MUST remain responsible for the existing landing, widget endpoint, WhatsApp webhook endpoint, and Sales Inbox UI.
- **FR-016**: The new Python runtime MUST be deployed as a separate Railway service.
- **FR-017**: Requests from Next to the runtime MUST be authenticated with HMAC over timestamp and raw request body.
- **FR-018**: The runtime MUST reject stale timestamps, invalid signatures, malformed bodies, and body/signature mismatches.
- **FR-019**: The runtime MUST expose a health endpoint for deploy and monitoring checks.
- **FR-020**: The runtime MUST return structured JSON for every successful turn.
- **FR-021**: The structured response MUST include conversation id, lead id when known, current agent, current state, next state, template ids, template variables, rendered message plan, facts, diagnostic checklist, actions, sources, safety flags, usage, and trace identifiers.
- **FR-022**: The runtime MUST validate model output before any channel delivery occurs.
- **FR-023**: The model MUST NOT be allowed to directly perform side effects outside approved tools.
- **FR-024**: Product knowledge MUST be the only source for prices, plan names, links, demo status, availability, checkout status, waitlist status, and commercial promises.
- **FR-025**: Price and plan answers MUST be direct and must not hide official information.
- **FR-026**: If the official product knowledge does not contain a requested fact, the agent MUST not invent it.
- **FR-027**: Product answers MUST persist the product source version used.
- **FR-028**: The agent MUST answer direct questions before steering to diagnostic, waitlist, or lead qualification.
- **FR-029**: The agent MUST handle open-ended, ambiguous, confusing, mixed, and out-of-order messages without requiring an explicit scripted flow.
- **FR-030**: The diagnostic flow MUST use facts volunteered by the lead before asking new questions.
- **FR-031**: The diagnostic MUST not conclude until every mandatory diagnostic question in [diagnostic-contract.md](./diagnostic-contract.md) is answered by current input, inferred from prior conversation evidence, or marked not applicable; required unresolved questions MUST produce a follow-up question or partial orientation, not a completed diagnostic.
- **FR-032**: Diagnostic records MUST include evidence, unknowns, confidence, recommendation, and next step.
- **FR-033**: The agent MUST offer the free diagnostic naturally and only when relevant to the conversation.
- **FR-034**: The agent MUST offer waitlist only after clear intent to contract, whether direct or after diagnostic delivery and follow-up buying/next-step intent.
- **FR-034A**: The diagnostic final delivery MUST be staged and MUST follow the order defined in [diagnostic-contract.md](./diagnostic-contract.md): pain/context, CRM base, operational step, agents/routines, dynamic plan recommendation, and dynamic demo bridge.
- **FR-034B**: The runtime MUST persist demo state and use it to choose the final diagnostic demo line: offer demonstrations if not previously offered, or ask whether the lead looked at them if already offered.
- **FR-034C**: The runtime MUST ask for a person name only at qualified moments when no reliable name exists, must never ask for a name on a cold greeting, and must not block value delivery when the lead skips the name.
- **FR-034D**: Diagnostic question turns MUST include a short grounded acknowledgement before the next question, including before the first diagnostic question when the lead explicitly requests the diagnostic.
- **FR-035**: Waitlist side effects MUST be idempotent.
- **FR-036**: Waitlist records MUST include contact path, source/channel, main pain or context, diagnostic summary when available, priority, missing fields, and joined date.
- **FR-037**: The agent MUST not ask WhatsApp leads for their phone number.
- **FR-038**: Widget leads MAY be asked for contact details only after value is delivered or when required for a requested follow-up.
- **FR-039**: The agent MUST pause automation when a lead requests a human.
- **FR-040**: The agent MUST pause automation when a manual WhatsApp Business App response is detected.
- **FR-041**: Sales Inbox pause/resume actions MUST control the runtime across widget and WhatsApp.
- **FR-042**: While human handoff is active, inbound messages MUST be recorded but MUST NOT receive AI replies.
- **FR-043**: The runtime MUST record the minimum operational observability needed for this behavior release: run id, current agent, current state, template IDs, handoffs, side-effect tool summaries, guardrail events, model usage when available, final output, delivery results, and error class. Full durable runtime replay/tracing can be completed after behavior correctness.
- **FR-044**: The runtime MUST record actual token usage and cost when available from the model provider.
- **FR-045**: Automatic AI generation MUST stop at or above the configured per-lead cost cap and mark the lead for human follow-up.
- **FR-046**: Approved message templates MUST be the official voice for mapped and semi-mapped commercial behaviors; the LLM MUST choose `template_ids` and variables, while validators and renderers control final delivery.
- **FR-047**: The current deterministic interpreter, orchestrator, and response generator MUST be removed from the official production path.
- **FR-048**: The old deterministic runtime MUST NOT remain as a conversational rollback path.
- **FR-049**: Operational fallback MAY pause automation, send a short safe error, or route to human, depending on channel.
- **FR-050**: Existing WhatsApp/Dualhook/Meta webhook behavior, idempotency, typing, delay, and delivery status behavior SHOULD be reused.
- **FR-051**: Existing widget behavior SHOULD be reused without visual redesign.
- **FR-052**: Existing Sales Inbox lead and message persistence SHOULD be reused and extended instead of replaced wholesale.
- **FR-053**: New runtime tables and contracts MUST use generic names such as `agent_runtime_*`, not `agent_v2_*` or `sales_agent_*`.
- **FR-054**: Stored runtime records MUST include `agent_key`, `agent_family`, `owner_scope`, `channel`, and nullable `tenant_id`.
- **FR-055**: For this feature, `agent_key` MUST be `taliya_commercial`, `agent_family` MUST be `taliya`, `owner_scope` MUST be `taliya`, and `tenant_id` MUST be null.
- **FR-056**: Evals MUST include deterministic invariants, multi-turn transcript scenarios, and LLM judge scoring.
- **FR-057**: Evals MUST fail robotic, evasive, generic, or unsupported answers even if they contain expected keywords.
- **FR-058**: Evals MUST separate blocking safety failures from quality score failures.
- **FR-059**: Manual widget and real WhatsApp tests MUST be documented before public lead capture or paid traffic.
- **FR-060**: The final production gate MUST approve the new runtime as the single official production agent.
- **FR-061**: Runtime traces, model context projections, logs, and Sales Inbox projections MUST redact secrets, system prompts, API keys, signatures, and raw provider payload fields that are not needed for operations.
- **FR-062**: `behavior-contract.md` MUST be treated as a binding implementation contract, not optional guidance.
- **FR-063**: The commercial runtime MUST expose the logical topology `taliya_commercial_triage` plus `entry`, `product`, `diagnostic`, `waitlist`, and `handoff` specialist roles.
- **FR-064**: The specialist topology MUST NOT require six model calls per normal turn; normal turns SHOULD use one default-model operation unless repair, escalation, or eval judging is required.
- **FR-065**: Structured model output MUST include previous/current/next state, route, opening type, detected intents, direct-question status, diagnostic action, diagnostic eligibility, waitlist eligibility, profile-name usage, template IDs, template variables, facts used, facts missing, diagnostic ledger status, next question kind, and policy checks.
- **FR-066**: Cold greeting-only openings such as "oi", "ola", and "bom dia" MUST receive only a natural greeting and broad help question; they MUST NOT trigger diagnostic, waitlist, name request, phone request, or plan list.
- **FR-067**: Source openings from widget, site CTA, Instagram/Facebook, and diagnostic CTA MUST follow the distinct opening behaviors defined in `behavior-contract.md`.
- **FR-068**: The diagnostic MUST be offered when the lead shares pain, asks for plan fit, asks how Taliya would work for their studio, or asks for diagnostic, after any direct question has been answered.
- **FR-069**: The diagnostic MUST NOT be offered on cold greeting-only turns, unresolved direct questions, human requests, irritation/de-escalation turns, or immediately after waitlist join without a new diagnostic request.
- **FR-070**: Only real person names MAY be saved as lead names. WhatsApp profile names must be treated as unverified until they look like a real person name or are confirmed by the lead; studio names, brands, handles, phone numbers, emojis, and generic strings MUST NOT be saved as person names.
- **FR-071**: Output validators MUST enforce the behavior contract before channel delivery and may trigger one repair attempt before safe fallback or human handoff.
- **FR-072**: The final eval gate MUST include the opening and diagnostic-first scenario matrix from `behavior-contract.md` with real OpenAI provider calls and saved transcripts.
- **FR-073**: Cost reports MUST use a current provider pricing table before they are used for release decisions.
- **FR-074**: The runtime MUST implement the canonical conversation states and allowed/tendency transitions in [conversation-state-contract.md](./conversation-state-contract.md).
- **FR-075**: State transitions MUST guide the journey but MUST NOT replace LLM interpretation as the conversation brain.
- **FR-076**: The renderer MUST split assistant turns into short channel-safe messages for both widget and WhatsApp.
- **FR-077**: Widget delivery MAY include validated buttons or quick replies; WhatsApp delivery MUST use text and official links instead of widget-only buttons.
- **FR-078**: Both widget and WhatsApp delivery MUST respect typing/delay/chunk rules from [message-template-contract.md](./message-template-contract.md) and [contracts/channel-adapters.md](./contracts/channel-adapters.md).
- **FR-079**: The runtime MUST enforce a one-question-at-a-time diagnostic progression unless the lead explicitly requests a form-style list.
- **FR-080**: The runtime MUST maintain a diagnostic answer ledger so questions answered outside the formal diagnostic are not repeated.
- **FR-081**: The runtime MUST implement JSON/schema repair once for invalid model output; if repair fails, it MUST use a safe operational fallback without advancing commercial state.
- **FR-082**: The runtime MUST enforce idempotency for inbound provider retries, outbound replies, transcript writes, diagnostic writes, waitlist joins, and handoff events.
- **FR-083**: The runtime MUST process rapid consecutive lead messages in order per conversation or otherwise prevent stale replies from being delivered after newer context is known.
- **FR-084**: Human handoff MUST pause automation across widget, WhatsApp, and Sales Inbox until explicit resume.
- **FR-085**: Product knowledge MUST be versioned and every sensitive product answer MUST persist the version and keys used.
- **FR-086**: Out-of-scope and safety cases MUST be handled with short safe replies, no medical advice, no prompt leakage, no invented services, and a return to Taliya/diagnostic only when relevant.
- **FR-087**: Sales Inbox MUST persist the complete lead, facts, diagnostic ledger, waitlist state, transcript, handoff state, guardrails, product source version, template IDs, model/cost signal, and next operator action described in [sales-inbox-contract.md](./sales-inbox-contract.md).
- **FR-088**: The implementation MUST include zero-cost tests for templates, renderer, validators, state transitions, diagnostic no-repeat, waitlist timing, Sales Inbox completeness, handoff, idempotency, and channel delivery before any broad real-OpenAI matrix run.
- **FR-089**: Real OpenAI evals MUST be quota-aware and support max scenario count, max cost, max model calls, dry-run mode, and stop-on-first-failure.
- **FR-090**: The final release gate MUST include product-owner review of complete transcripts for the mapped behavior matrix.
- **FR-091**: The product explanation and follow-up delta in [product-followup-delta-contract.md](./product-followup-delta-contract.md) MUST be implemented without reopening protected behavior that already exists and is approved.
- **FR-092**: The runtime MUST answer "como funciona?", "me explica melhor", "como seria no meu studio?", and related questions as product questions, not as openings.
- **FR-093**: The product knowledge source MUST include official keys for `how_it_works`, `routine_areas`, `whatsapp_scope`, `integration_scope`, `comparison_spreadsheet`, `comparison_management_system`, `security_and_data`, `availability_and_onboarding`, and `out_of_profile`.
- **FR-094**: The runtime MUST retrieve those new product knowledge keys selectively by topic and MUST NOT add all new facts to every prompt.
- **FR-095**: The runtime MUST include compact `post_diagnostic_context` in the LLM payload after diagnostic delivery, populated only from saved diagnostic/demo/waitlist state.
- **FR-096**: Post-diagnostic follow-up MUST use saved diagnostic context, MUST NOT restart diagnostic, and MUST NOT ask again for facts already answered.
- **FR-097**: The runtime MUST support `product_how_it_works`, `comparison_current_tool`, `integration_scope_question`, `trust_security_question`, `out_of_profile`, `conversation_resume`, `general_objection`, and `diagnostic_refusal` as LLM-selected normalized intents.
- **FR-098**: The implementation MUST NOT add deterministic commercial regex/state-machine shortcuts for product explanation, comparison, integration, security, out-of-profile, diagnostic refusal, general objection, or post-diagnostic follow-up.
- **FR-099**: The runtime MUST add and validate the missing templates `product.how_it_works_direct`, `product.comparison_current_tool`, `product.integration_scope_direct`, `product.security_data_direct`, and `product.out_of_profile_redirect`.
- **FR-100**: Customer-facing lay-lead output MUST NOT use "CRM" as the main explanation or persuasion device in openings, price objections, "como funciona", or comparison responses unless the lead directly asked about CRM.
- **FR-101**: Integration and WhatsApp-scope answers MUST distinguish Taliya's commercial WhatsApp from the studio WhatsApp Business product requirement and MUST NOT promise automatic setup, Instagram/current-system integration, mass messaging, migration, checkout, or payment links without official facts.
- **FR-102**: Security/data answers MUST be conservative, MUST NOT request sensitive data, and MUST NOT invent LGPD, certification, encryption, audit, privacy, or data-access claims.
- **FR-103**: Out-of-profile leads MUST be qualified gently and MUST NOT be forced into a studio diagnostic or treated as buyers when they are students.
- **FR-104**: Diagnostic refusal MUST be respected; the agent MUST answer the direct question and MUST NOT immediately offer diagnostic again in the same turn.
- **FR-105**: Protected-route regressions MUST prove approved openings, price direct, price-plus-pain, demo direct, WhatsApp direct, diagnostic, waitlist, handoff, safety, Sales Inbox, and delivery shape did not degrade after the delta.
- **FR-106**: Customer-facing product explanation, comparison, objection, diagnostic-refusal, and post-diagnostic follow-up MUST use Pilates-studio-owner language and MUST avoid technical SaaS language unless the lead used the technical term first.
- **FR-107**: Commercial product-followup routes MUST include LLM/model-usage evidence in eval reports unless the turn is an explicitly allowed operational, safety, or cold-empty zero-cost exception.

### Key Entities *(include if feature involves data)*

- **Agent Definition**: Registered runtime agent with key, family, instructions, tools, guardrails, model policy, and enabled status.
- **Agent Run**: One execution of the runtime for one inbound event, including input, agent selection, output, tool calls, guardrails, usage, and trace id.
- **Runtime Conversation**: Persistent conversation state across widget or WhatsApp for a lead and agent key.
- **Runtime Message**: Inbound, outbound, system, human, or tool-related message associated with a conversation.
- **Runtime State**: Structured memory including current agent, lead facts, diagnostic state, waitlist state, human status, summary, and budget.
- **Conversation State**: Canonical commercial journey state with allowed transitions and tendency rules.
- **Message Template**: Approved official response block selected by LLM via `template_id` and rendered by channel-specific renderer.
- **Template Render Plan**: Ordered short-message delivery plan with channel-specific actions, buttons or links, chunking, typing, and delay metadata.
- **Diagnostic Answer Ledger**: Per-question record of answered, inferred, missing, or unresolved diagnostic inputs with evidence references.
- **Tool Call**: Idempotent model-selected action such as reading product knowledge, saving facts, marking waitlist, or pausing for human.
- **Handoff Event**: Agent-to-agent or agent-to-human transfer with reason, status, source, and resume behavior.
- **Guardrail Event**: Input or output policy result, including prompt-injection, unsupported claim, price/link validation, human pause, and safety checks.
- **Product Knowledge Source**: Versioned official source for commercial facts, plans, prices, links, availability, and unsupported claims.
- **Diagnostic Record**: Evidence-based diagnostic output generated from lead facts and persisted with confidence and unknowns.
- **Waitlist Record**: Qualified waitlist status and actionable follow-up fields.
- **Model Usage Record**: Actual or provider-reported token and cost record for each model operation.
- **Evaluation Run**: Versioned eval execution with scenario results, transcripts, judge scores, blocking failures, and spend.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In representative evals, at least 95% of normal lead turns invoke the LLM-first runtime for interpretation and template selection rather than a deterministic decision path.
- **SC-002**: 100% of price, plan, demo, availability, and checkout answers cite a persisted product source version.
- **SC-003**: 0 eval-approved transcripts contain invented checkout links, invented demo links, invented availability, or unsupported promises.
- **SC-004**: At least 90% of direct question scenarios are judged as answering the direct question before steering.
- **SC-005**: At least 85% of diagnostic scenarios score 4 out of 5 or higher for usefulness, evidence, and non-generic recommendation.
- **SC-006**: 0 diagnostic pass cases use strong evidence language when fewer than two relevant lead facts are known.
- **SC-007**: 100% of human handoff scenarios pause automation until explicit resume.
- **SC-008**: 100% of duplicate webhook scenarios avoid duplicate replies and duplicate side effects.
- **SC-009**: 100% of waitlist join scenarios persist status, source, contact path, priority, and summary.
- **SC-010**: 90% of qualified lead conversations remain under the configured target cost band, and 100% stop automatic replies at the hard cap.
- **SC-011**: Sales Inbox exposes lead summary, current agent, facts, diagnostic, waitlist, handoff, guardrail, and cost information for all representative test leads.
- **SC-012**: Protected `/pilates` desktop and mobile visual baselines show no intentional redesign after integration.
- **SC-013**: Real WhatsApp smoke tests pass for inbound text, duplicate webhook retry, manual human reply pause, AI resume, typing/delay, and status logging.
- **SC-014**: Product owner review approves representative transcripts before public lead capture or paid traffic.
- **SC-015**: 100% of trace/log redaction tests pass for API keys, HMAC secrets, signatures, system prompts, and raw provider payload fields.
- **SC-016**: 100% of mapped opening scenarios in `behavior-contract.md` pass their blocking invariants with real OpenAI transcripts.
- **SC-017**: 0 eval-approved cold greeting transcripts offer diagnostic, waitlist, name capture, phone capture, or plan lists.
- **SC-018**: 100% of direct question first-message scenarios answer the direct question before diagnostic, waitlist, or lead qualification.
- **SC-019**: 100% of real-provider eval reports include route, specialist role, policy checks, model usage, estimated cost, and full visible transcript.
- **SC-020**: P1 behavior scenarios average at least 4.2 out of 5 on the quality judge rubric, no mapped P1 scenario scores below 4.0, and no blocking failures remain.
- **SC-021**: 100% of mapped commercial behaviors return approved `template_ids` or an allowed unmapped safe fallback category.
- **SC-022**: 100% of widget and WhatsApp approved transcripts respect short-message delivery limits, with no text-wall assistant turn.
- **SC-023**: 100% of completed diagnostic scenarios have every mandatory question answered, inferred from prior evidence, or marked not applicable; scenarios with required unresolved answers must not be marked completed.
- **SC-024**: 100% of scenarios where a diagnostic fact was answered before diagnostic starts do not repeat that same question.
- **SC-025**: 100% of waitlist-offer pass scenarios contain clear intent to contract, either direct, after diagnostic delivery plus next-step intent, or after positive demo reaction plus next-step intent.
- **SC-026**: 0 approved scenarios save studio names, brands, handles, numbers, or generic strings as verified person names.
- **SC-027**: 100% of invalid JSON/model-output scenarios either repair once successfully or use safe fallback without unintended state advancement.
- **SC-028**: 100% of rapid-message and duplicate-webhook scenarios avoid duplicate replies, duplicated transcript entries, duplicated waitlist joins, and stale responses.
- **SC-029**: 100% of Sales Inbox completeness scenarios persist all required fields from [sales-inbox-contract.md](./sales-inbox-contract.md).
- **SC-030**: 100% of completed diagnostic pass scenarios include hold message, staged delivery, CRM-first recommendation, agent-by-agent explanation, required dynamic plan line, and correct dynamic demo line.
- **SC-031**: 0 approved transcripts use the old final diagnostic formats "Pelo contexto, o principal gargalo parece", "Para plano, eu compararia", or "Isso faz sentido para o momento do seu studio?" as the standard final close.
- **SC-032**: 100% of direct diagnostic request and diagnostic-in-progress scenarios include grounded feedback before the first/next diagnostic question.
- **SC-033**: 100% of demo-history branch scenarios choose the correct final diagnostic demo line and persist demo status in Sales Inbox.
- **SC-034**: 100% of name-timing scenarios follow the WhatsApp/widget rules: reliable WhatsApp name can be used, unreliable names are ignored, widget/cold greetings do not ask name, and qualified diagnostic entry may ask name without blocking value.
- **SC-035**: Real OpenAI eval execution never exceeds the configured max scenario, max model-call, or max cost limits.
- **SC-036**: 100% of "como funciona" pass scenarios are treated as product answers, not openings, and adapt their next step to the current state.
- **SC-037**: 100% of post-diagnostic follow-up pass scenarios use saved diagnostic context and do not restart diagnostic or repeat already answered diagnostic questions.
- **SC-038**: 0 approved lay-lead transcripts use "CRM" in openings, price objections, product explanation, or comparison unless the lead directly asked about CRM.
- **SC-039**: 100% of comparison pass scenarios avoid attacking current tools, avoid unsupported migration/integration promises, and explain practical difference in studio-owner language.
- **SC-040**: 100% of WhatsApp/integration-scope pass scenarios distinguish Taliya's commercial WhatsApp from studio WhatsApp Business product use and avoid unsupported setup/integration/mass-message promises.
- **SC-041**: 100% of security/data pass scenarios avoid invented LGPD/certification/encryption/audit/privacy claims and do not request sensitive data.
- **SC-042**: 100% of out-of-profile pass scenarios qualify gently without forcing diagnostic or treating students as buyers.
- **SC-043**: 100% of diagnostic-refusal pass scenarios respect refusal, answer the direct question, and do not immediately offer diagnostic again.
- **SC-044**: Protected-route cost and latency remain inside configured bands and do not regress by more than 10% versus the latest approved baseline unless explicitly accepted in product-owner review.
- **SC-045**: 0 approved lay-lead product explanation, comparison, objection, diagnostic-refusal, or post-diagnostic transcripts use technical SaaS language unless the lead used that term first.
- **SC-046**: 100% of approved commercial product-followup eval reports include LLM/model-usage evidence, except explicitly allowed operational, safety, or cold-empty zero-cost exceptions.

## Assumptions

- The Taliya commercial agent is for Taliya's own Pilates SaaS leads only.
- The current business context is that Taliya is a CRM SaaS for Pilates studios; older docs that say otherwise are legacy and must not override this spec.
- The Taliya-owned WhatsApp Business number remains the only WhatsApp number in scope for this feature.
- No studio/customer WhatsApp numbers are connected in this feature.
- Future configuration and studio operation agents will be planned separately.
- Railway is available for hosting the Python runtime.
- The existing Vercel/Next deployment remains the public app deployment.
- A stable Postgres `DATABASE_URL` is available or will be provisioned before production.
- `/pilates/planos` is the official plans page unless product owner updates the source.
- `/pilates/planos/demonstracao` is the approved official demo/commercial link unless product owner updates the source later.
- Waitlist is an internal recorded action, not a public invented checkout link.
- New `agent_runtime_*` migrations may be created and should not depend on `agent_v2_*` as the primary runtime schema.
- The old deterministic agent path may remain temporarily as unused legacy code during transition, but must not remain reachable as the official production conversation path.
- The immediate focus is perfecting agent behavior and Sales Inbox lead completeness; full durable runtime replay/tracing infrastructure can be completed later as long as the minimum observability and idempotency requirements in this spec are met now.
- Implementation may proceed autonomously for local files, tests, fixtures, and non-production verification.
- Any real production migration, Railway deployment, Vercel deployment, or live WhatsApp production action requires explicit user confirmation immediately before execution.
