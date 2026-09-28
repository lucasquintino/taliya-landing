# Feature Specification: Floating AI Attendant

**Feature Branch**: `codex/002-floating-ai-sales-agent`
**Created**: 2026-04-30
**Status**: Ready for plan/tasks
**Input**: Add a floating button in the bottom-right corner that opens an AI attendant for the Pilates landing, and make the same attendant work through WhatsApp conversations. The agent answers questions, talks to studio owners, explains the system, asks about their pains, shows why they need operational AI agents, can route to a guided demonstration of the real SaaS once the product is ready, and conducts the visitor toward the right plan/checkout path only after a consultative recommendation. If the visitor wants to talk to a human before subscribing, the agent routes them to WhatsApp for assisted closing.

Commercial E2E launch readiness, lead identity rules, Sales Inbox go-live requirement and implementation order are defined in [../commercial-e2e-readiness-and-implementation-order.md](../commercial-e2e-readiness-and-implementation-order.md). Spec 2 owns the agent behavior, WhatsApp continuity, lead visibility, human takeover, custom-agent diagnostic report behavior and eval requirements needed by that cross-spec checklist.

Cross-product security, code safety, data protection, secrets, AI guardrails, webhook safety and future tenant isolation requirements are defined in [../005-security-code-data/spec.md](../005-security-code-data/spec.md).

## System Configuration Alignment

The AI attendant MUST always use the current system configuration as the source of truth for plans, pricing, plan-comparison destination, checkout destinations, WhatsApp destinations, offer mode, campaign stage, supported agents, supported pains and public copy boundaries.

The agent MUST NOT hardcode plan names, prices, discounts, plan-comparison URLs, checkout URLs, WhatsApp numbers or offer framing in prompts, components or fallback text. These values must come from trusted configuration shared with the landing system.

For Pilates, the agent must read the same commercial configuration defined by the landing: Base, 1 Agente, 3 Agentes and 7 Agentes plans, with 7 Agentes as the recommended complete-system plan unless configuration changes it. If configuration changes later, the agent behavior must change without prompt rewrites.

All commercial surfaces must share the same trusted configuration source: landing sections, `/pilates/planos`, AI prompts/context, fallback text, WhatsApp replies, Sales Inbox actions, optional n8n automation payloads and future checkout creation. A price, recommended-plan flag, usage cap, plan name or checkout destination must not be duplicated in separate hardcoded copies.

## Commercial Strategy And Answer Coverage

The attendant's primary commercial goal is to sell consultatively, not push a cold visitor straight to plans. It should qualify the studio, answer objections, offer the guided real-SaaS demonstration when proof is needed and available, recommend the configured best-fit plan and then route the visitor to the plan page or trusted checkout path. When the visitor's pains indicate a broad operational need, strong buying intent or desire to activate the complete system, the attendant should frame the configured recommended/highest-value plan as the natural recommendation. Lower plans exist to support comparison, budget-fit and objection handling; they must not be treated as equal default recommendations unless the system configuration marks them as recommended or the visitor clearly asks for a narrower/budget-first option.

### Primary Free Diagnostic Funnel

The free diagnostic is the main sales funnel for the attendant. Price questions, plan requests, demo requests, expensive objections, human handoff requests and "I want to subscribe" messages are not separate cold shortcuts by default. They are commercial signals that the attendant must answer briefly and then use to start or continue the diagnostic unless a diagnostic is already complete.

Before the diagnostic is complete, the attendant must:

- answer the visitor's direct question in simple language;
- avoid dumping plans, checkout links or demo CTAs as the main next step;
- ask for name/contact early once there is minimum interest;
- continue with one short diagnostic question at a time;
- preserve any plan/demo/human/custom intent as context for the final recommendation.

Approved v1 diagnostic behavior:

- The agent is a consultative Taliya sales attendant for Pilates studios. It is not a generic support bot, FAQ bot or early plan comparator. Its primary job is to conduct a short, useful free diagnostic and only then recommend CRM, agents and plan.
- The agent must still answer buyer questions whenever needed. When a question appears before or during the diagnostic, the agent answers it directly, then either resumes the current diagnostic question, pauses/cancels the diagnostic if the visitor asked to stop, or routes to the correct custom/human/commercial path.
- During the diagnostic, free-text answers must be interpreted by the AI response layer instead of relying only on quick replies or local per-answer rules. The system may keep deterministic extraction and trusted configuration for safety, prices and product facts, but the visitor must not be forced to click suggestions to progress.
- The rhythm must feel like a human seller: after the visitor answers, the agent acknowledges or reflects the answer briefly before asking the next question. It must not feel like a rigid interview that immediately fires the next question with no feedback.
- Once enough information exists, the agent must send a short hold message such as "Ok, ja tenho as informacoes necessarias para montar seu diagnostico. Ja te retorno.", then deliver the final diagnostic in separated steps/messages with visible typing/loading cadence where the channel supports it.
- The final diagnostic must be dynamic to the collected context: it identifies the main bottleneck, explains what the Taliya CRM must organize first, recommends the relevant CRM base, then introduces agents and plan after the operational logic is clear.
- Recommended agents must be presented one at a time, each with the pain it resolves, why it was recommended from the diagnostic and how it acts in practice. The UI may render these as structured recommendation cards, but the content contract must preserve pain, reason and practical action.

After the diagnostic is complete, the attendant may show the correct CTA based on readiness: plans, guided demo when available, WhatsApp consultor/human assistance or checkout after an explicit plan confirmation.

The expected decision gate is:

```text
commercial intent detected
  -> diagnostic complete?
    -> no: answer briefly + ask next diagnostic question
    -> yes: offer the best next CTA for that lead
```

The agent must be evaluated as a sales attendant, not only as a Q&A bot. Before launch, the implementation must prove coverage for common buyer directions including: "e caro", "ja tenho secretaria", "meu studio e pequeno", "nao confio em IA", "vou pensar", "manda no WhatsApp", "quero so agenda", "tenho medo de configurar", "quero ver planos", "quero assinar agora", "quero um agente de marketing" and "isso integra com X?". Each answer must follow the approved commercial pattern: answer directly, connect to the studio operation, preserve trust/risk reducers, recommend the correct next step and avoid unsupported promises.

## Entry Intent Matrix

The same agent brain must adapt its opening tone and initial goal according to the entry path.

| Entry Path | Source Metadata | Opening Tone | First Message Goal | Allowed Immediate Next Steps |
| --- | --- | --- | --- | --- |
| Floating widget | `entryPath=widget` | Neutral/helpful | Ask what the visitor wants or offer common options | Explain, diagnose, demo, plans if asked, WhatsApp, custom-agent capture. |
| Falar com consultor | `entryPath=consultor_cta` | Direct/commercial | Acknowledge interest and ask if they want help choosing/acquiring Taliya | Diagnose, recommend demo, recommend plan, WhatsApp, checkout after confirmation. |
| Continuar no WhatsApp | `entryPath=whatsapp_cta` | Direct/commercial/continuity | Continue the sale in WhatsApp with source context | Same as consultor CTA, plus human takeover. |
| Demonstracao guiada | `entryPath=guided_demo` | Product-led/explanatory | Explain the demo step and invite questions | Continue demo, answer doubt, return to consultor, WhatsApp, plans/checkout after recommendation. |
| Diagnostico de agente sob medida | `entryPath=custom_agent_diagnostic` plus `contextVariant` | Report-driven/commercial | Generate a structured diagnostic report, not a chat message thread | Route to SaaS consultor/demo/WhatsApp when already mapped; route to custom-agent proposal consultor/WhatsApp when unmapped. |
| FAQ: ficou alguma duvida? | `entryPath=widget`, `sourceSection=faq_doubt_cta` | Neutral/helpful | Answer the remaining doubt after FAQ reading | Same as widget; may route to demo, plans, WhatsApp or custom-agent capture only after intent is clear. |

Opening behavior:

- Widget entry MUST NOT assume buying intent.
- Consultor CTA entry MAY use stronger commercial copy, but must remain consultative and avoid pressure.
- WhatsApp entry MUST preserve the same answer policy and plan recommendation rules as web.
- Guided demo entry MUST behave like a product guide and commercial assistant, not a generic FAQ bot.
- Custom-agent diagnostic entry MUST preserve the generated report context and use the correct variant: `diagnostic_existing_solution`, `diagnostic_custom_agent`, `diagnostic_mixed_solution` or `diagnostic_unclear`.
- FAQ doubt CTA entry MUST reuse the widget opening logic and must not assume the visitor is ready for checkout.

## Custom Agent Diagnostic Report

The Agente sob medida diagnostic report is defined in [custom-agent-diagnostic-report.md](./custom-agent-diagnostic-report.md).

This is a separate report mode from the floating chat. Live AI generation for this diagnostic is deferred to a future phase. In v1, it may use deterministic/report-style classification as long as it is honest in public copy, preserves the route/schema boundary, and routes the visitor safely to consultor/WhatsApp or the SaaS sales funnel. A future live-AI diagnostic may reuse the same AI provider, guardrails, usage logging, trusted configuration, supported-agent map, Sales Inbox and n8n dispatch, but it must still use a separate route, prompt mode and response schema.

## Widget UI Display Modes

The floating widget must be treated as a conversion component, not only as a button that opens a chat. Its visual states must be deliberately designed so a first-time studio owner understands what it is, what happens after clicking and how to continue without confusion.

Required display modes:

| Mode | Purpose | Required Behavior |
| --- | --- | --- |
| `minimized_idle` | Default bottom-right entry point | Premium compact pill with avatar/call icon, clear consultor label and availability cue; must be understandable without reading surrounding page copy. |
| `minimized_attention` | Soft prompt after visitor spends time or reaches a relevant section | Subtle message cue or pulse only when configured; must not feel like an intrusive popup or cover important controls. |
| `minimized_active` | Visitor has an existing conversation but panel is closed | Shows unread/continuation state clearly so the visitor knows the conversation is preserved. |
| `opening_transition` | Click/tap feedback | Smooth expansion into the panel with no layout jump, no double-open and no blocked scroll artifacts. |
| `open_desktop` | Full desktop chat panel | Clean panel up to the header height, readable messages, clear close/minimize controls, visible input, quick replies and CTA cards without visual clutter. |
| `open_mobile` | Mobile sheet/panel | Fits the viewport, respects safe areas and keyboard, keeps input reachable and does not hide critical browser/page controls. |
| `typing_loading` | AI is generating or handoff is preparing | Shows lightweight typing/loading feedback and disables duplicate sends without freezing the UI. |
| `error_fallback` | AI/provider fails or input is blocked | Shows a calm recoverable message, retry/WhatsApp option when allowed and preserves conversation state. |
| `handoff_cta` | Agent recommends demo, plans, WhatsApp, checkout or custom-agent follow-up | CTA cards/buttons must be visually distinct from normal text, explain the next step and preserve gates/context. |

Visual acceptance rules:

- The minimized widget must not look like an ad, generic chatbot bubble or unexplained phone button.
- The panel must feel aligned with the best sections of the landing, especially "Quero que meus agentes cuidem de", "Por que seu studio perde dinheiro sem perceber" and "Navegue pelos topicos".
- The widget must avoid visual noise: no repeated AI labels, no dense legal/privacy paragraph inside the main chat surface, no competing primary CTAs.
- Every state must be legible at 1440px, 390px and short mobile viewport heights.
- Motion must be smooth and useful, with reduced-motion support.
- Open/minimized/attention/error/loading/handoff states must have screenshot or browser QA before launch.

Required route:

```text
POST /api/landing/custom-agent-diagnostic
```

Required behavior:

- Accept a free-text description of the operation the visitor wants to automate.
- Generate a structured report on the page instead of opening a normal chat by default.
- Classify the request as `mapped_solution`, `custom_agent`, `mixed_solution` or `unclear`.
- For `mapped_solution`, explain that Taliya already covers the request, name the mapped agents and offer the same CTAs as "Quer ver como ficaria no seu studio?": `Falar com consultor`, `Demo guiada` when ready/gated and `Continuar pelo WhatsApp`.
- For `custom_agent`, explain that the request is Agente sob medida, separate from public plans, and offer `Solicitar proposta de agente sob medida` plus `Continuar pelo WhatsApp`.
- For `mixed_solution`, split the SaaS-covered part from the custom part and offer both the SaaS funnel and custom proposal path.
- For `unclear`, ask for more context and route to consultor/WhatsApp without inventing scope.
- Never route directly from the report to checkout.
- Create or update a Sales Inbox lead when the report creates meaningful commercial intent or the visitor clicks a report CTA.

When a report CTA opens the consultor or WhatsApp, the first message must use the report variant:

- `diagnostic_existing_solution`: "this is already covered by Taliya" and continue toward SaaS sale.
- `diagnostic_custom_agent`: ask more about the custom operation, then collect email/cellphone/WhatsApp and say the team will contact them.
- `diagnostic_mixed_solution`: explain the mapped SaaS path and the custom expansion path.
- `diagnostic_unclear`: ask for the missing details before recommending.

Approved commercial answers are defined in [approved-answer-knowledge.md](./approved-answer-knowledge.md). The route-level conversation contract is defined in [conversation-route-matrix.md](./conversation-route-matrix.md). The agent must use trusted system configuration first, then this approved knowledge and route matrix, and must not invent unsupported answers when neither source covers the question.

The agent must answer purchase-relevant questions before steering the visitor back to conversion. This includes doubts about what the system does, which agents are included, plan differences, price, setup, onboarding, WhatsApp behavior, human takeover, configuration per studio, Agente sob medida, integrations, limits, privacy, cancellation/contract terms when configured, what happens after subscribing, whether the system replaces the team and how humans stay in control.

The required conversation pattern is: answer the question directly, connect the answer to the studio's operation, ask one short qualifying question when context is missing, offer the guided demonstration when visual proof would help, frame the recommended/highest-value plan when it is the best fit, then offer the configured plans/checkout path or, if the visitor asks for human help, the WhatsApp assisted-close path. If the information is not in trusted configuration or approved context, the agent must say what it can confirm, avoid inventing details and offer WhatsApp assistance, guided demo or analysis.

The detailed commercial behavior, objection handling, follow-up policy, lead readiness model, Sales Inbox rules, WhatsApp template boundaries, quota policy, terms boundary, fiscal/invoice boundary, guided-demo environment rules and conversion metrics are defined in [commercial-sales-playbook.md](./commercial-sales-playbook.md). The implementation must keep route behavior, next-step gates, lead effects and eval coverage aligned with [conversation-route-matrix.md](./conversation-route-matrix.md).

The same answer policy and commercial strategy must apply on the web widget and WhatsApp. WhatsApp is a continuation channel for the same attendant by default; it becomes human-assisted only when the visitor asks for a person or when an operator takes over.

## Supervised Agent Improvement Plan

The sales attendant must improve through supervised calibration, not uncontrolled self-learning in production.

During validation, the operator and implementation team will run realistic buyer conversations, review failures, group issues by cause and update the approved behavior deliberately. Updates may include the commercial playbook, approved-answer knowledge, route gates, fallback responses, lead-capture rules, UI next-step suggestions, Sales Inbox storage, optional n8n automation payloads and eval fixtures.

The agent must not automatically rewrite its own prompts, rules, prices, plan recommendations, lead status logic, handoff destinations, safety boundaries or fallback behavior based only on live visitor conversations. Every behavior change must be versioned in source-controlled configuration, prompt/context code, docs or eval fixtures, then verified before release.

The improvement loop is:

1. Run controlled manual conversations and automated evals.
2. Capture failures with source path, user intent, expected behavior, actual behavior and lead effect.
3. Classify the issue as prompt/playbook, route gate, safety, fallback, lead capture, UI/CTA, Sales Inbox/n8n automation or provider/cost.
4. Apply a reviewed code/config/docs change.
5. Re-run only the affected practical scenarios plus the route matrix.
6. Promote the change only when lint, build, evals and practical smoke tests pass.

Before traffic is increased beyond controlled validation, the project must produce a readiness report that includes tested scenarios, pass/fail results, issues corrected, remaining blind spots, approximate API cost, lead-sync status and a go/no-go decision.

Widget-to-WhatsApp continuity is required for a serious sales funnel. When the visitor moves from the web widget to WhatsApp, the system must preserve or merge context only through strong identifiers such as `leadId`, WhatsApp number, provider contact ID, email or explicit session continuation token. If the system cannot safely prove identity, it must create a separate lead/conversation or ask for confirmation instead of merging by weak signals.

Sales Inbox is mandatory before production claims of same-number human takeover on WhatsApp. n8n may send secondary alerts/digests, but it is not the lead source of truth or the real-time reply surface.

When the visitor asks to see, compare or understand plans, the agent must not dump them cold into pricing. It must give a short helpful summary, ask one concise qualifying question if context is missing, then route them to the configured public plans destination when they ask, have enough context for a recommendation or insist on comparison. For v1, that destination is the dedicated Pilates plans page at `/pilates/planos`.

When the visitor wants to see the product working, asks for a demo or appears uncertain because the offer is abstract, the agent must route to the configured guided demonstration destination only if the real SaaS demo environment is available. For v1 after SaaS readiness, that destination is `/pilates/demonstracao`. The demo handoff must preserve selected pain, selected agents and conversation context when available. Before the SaaS demo environment exists, the agent must offer consultor/WhatsApp assistance or product explanation instead of pretending a real demo is available.

## Plan And Checkout Gates

The agent may route to `/pilates/planos` only when one of these is true:

- the visitor explicitly asks to see or compare plans;
- the visitor entered through a plan-related CTA and the agent has acknowledged/qualified the intent;
- the agent has captured enough context to recommend a plan;
- the guided demo has reached a recommendation point or completed;
- the visitor insists on seeing plans after a brief answer.

The agent may route to checkout only when one of these is true:

- the visitor says they want to subscribe, start or buy now;
- the visitor confirms the recommended plan;
- the visitor clicks an explicit checkout CTA on `/pilates/planos`;
- an operator sends a trusted checkout link from the Sales Inbox.

Before checkout, the agent must make risk reducers available when relevant: post-payment next step, studio-owned WhatsApp, setup/onboarding help, human control, plan changes when configured, usage caps, cancellation/contract when configured and payment-data safety.

## High-Ticket Sales Conversation Script

For plan recommendations above R$ 1.000/month, the agent should follow this sequence unless the visitor explicitly short-circuits to checkout:

1. Identify the studio's main pain.
2. Connect the pain to operational or financial impact.
3. Show or offer proof through landing context, calculator, product explanation or guided demo.
4. Recommend the plan that fits the pain profile, prioritizing 7 Agentes for broad needs.
5. Explain why lower plans may or may not fit.
6. Answer objections and risk reducers.
7. Offer plans page, WhatsApp human assistance or checkout according to readiness.

## Lead Visibility And Operator Pipeline

The sales attendant must not create qualified conversations that disappear into tracking-only events. Every meaningful conversion signal must be written to one operator-visible lead source of truth.

For v1, the operator-visible lead source of truth is the internal Sales Inbox backed by the configured database. Notifications in WhatsApp, Slack, email, n8n or other channels are allowed only as secondary alerts.

External CRM/spreadsheet sync is explicitly out of scope for this phase. The integration must be designed so the project can add a CRM mirror later without changing the agent brain, WhatsApp transport or Sales Inbox control flow.

Each lead record must include at minimum: contact when provided, studio name when provided, city/state when provided, source channel, conversion path, selected/interested plan, captured pains, recommended agents, custom-agent interest when applicable, qualification completeness, safe conversation summary, status, priority, created/updated timestamps and consent/opt-out context when available.

The operator must be able to see all leads in one place, filter by status/priority/channel/conversion path and identify which leads need human WhatsApp assistance, analysis follow-up, custom-agent follow-up or billing/subscription verification.

## Internal Sales Inbox

Detailed Sales Inbox behavior is defined in [internal-sales-inbox.md](./internal-sales-inbox.md).

Spec 2 must include an internal Sales Inbox before the full SaaS product exists.

The Sales Inbox is the operator control center for the SaaS operator's own commercial leads: studio owners who interact with the landing widget, the SaaS sales WhatsApp, the plans page, assisted conversion paths, custom-agent requests or checkout intent. It is not the future inbox that paying studios will use to manage their students or their own operational agents.

The Sales Inbox owns real-time operational control and is the v1 commercial lead source of truth. External spreadsheets or CRMs are not the real-time reply surface and must not be the only place where the operator controls lead conversations.

The Sales Inbox must let the operator:

- see all commercial leads from web widget and WhatsApp in one internal surface;
- unify web and WhatsApp activity for the same lead when identifiers match safely;
- filter by lead status, priority, channel, conversion path, interested plan, next action and last activity;
- open the full lead context: contact, studio, city/state, captured pains, interested plan, recommended agents, custom-agent request when applicable, safe summary and recent messages;
- assume a lead conversation from the AI;
- pause or resume AI replies for that lead/session;
- reply through the SaaS operator's WhatsApp when the lead is on WhatsApp;
- send configured plan-page and checkout links;
- mark follow-up, waiting customer, checkout sent, won, lost or do-not-contact;
- create/update a next action and follow-up date;
- emit optional n8n alerts/digests for important status changes;
- audit every operator action.

Lead merge rules:

- WhatsApp number match is a strong merge signal.
- Email match is a strong merge signal.
- Explicit `leadId` or `sessionId` carried from the widget to WhatsApp is a strong merge signal.
- Studio name alone is not enough for automatic merge.
- IP/browser fingerprint alone is not enough for automatic merge.
- Ambiguous matches must remain separate or require operator review.

Required Sales Inbox statuses:

- `ai_active`
- `handoff_requested`
- `human_active`
- `waiting_customer`
- `follow_up_scheduled`
- `checkout_sent`
- `won`
- `lost`
- `do_not_contact`

These same operational status values are the canonical lead statuses for the Sales Inbox and any future external CRM mirror. Future external views must be derived from `status`, `conversionPath`, `customAgentInterest` and `nextAction`, not from a separate status lifecycle.

Required operator actions:

- `take_over`
- `send_whatsapp_message`
- `send_plan_page`
- `send_checkout_link`
- `schedule_follow_up`
- `resume_ai`
- `mark_waiting_customer`
- `mark_won`
- `mark_lost`
- `mark_do_not_contact`
- `edit_lead_summary`

Sales Inbox boundaries:

- It is only for the SaaS operator's own leads who may subscribe to the SaaS.
- It is not the CRM/inbox sold to studios.
- It does not manage students or interested students for paying studios.
- It does not activate paid subscriptions; paid state comes only from Spec 3 billing webhooks.
- It does not collect card data, payment credentials or billing documents.
- Browser code must never receive WhatsApp provider credentials, n8n secrets, database credentials or billing secrets.

## Provider Decisions

WhatsApp provider for v1 is the official Meta WhatsApp Cloud API. Third-party providers such as Twilio, Z-API, Evolution API or other gateways are not the default implementation path for this spec.

The WhatsApp adapter remains isolated behind `lib/landing/ai-attendant/whatsapp.ts` so the implementation can be replaced later if needed, but the first production path is Meta Cloud API with server-side webhook verification, provider message idempotency and no browser-side provider calls.

Detailed production WhatsApp E2E readiness, including provider status handling, retry/outbox behavior, service-window/template gating, unsupported message types and live Meta launch blockers, is defined in [whatsapp-e2e-readiness.md](./whatsapp-e2e-readiness.md).

The AI provider remains OpenAI through a server-side abstraction. The planned default model is configured through `AI_ATTENDANT_MODEL`; the model must be overridable by environment/config without changing the conversation rules.

## Human WhatsApp Handoff

Human WhatsApp handoff is defined in [human-whatsapp-handoff.md](./human-whatsapp-handoff.md).

When the visitor asks to talk to a person before subscribing, the agent must create a safe assisted-closing summary, use only trusted WhatsApp destinations from system configuration, emit `floating_agent_human_whatsapp_handoff`, and avoid continuing as if the AI were the human closer.

Because WhatsApp v1 uses the official Meta WhatsApp Cloud API, human takeover on the same WhatsApp AI channel requires an operator reply surface. The Internal Sales Inbox is the commercial lead source of truth and real-time control surface for v1. V1 must provide the Internal Sales Inbox or an approved shared inbox provider before claiming that a human can assume the same WhatsApp conversation.

## Privacy, LGPD And Consent

Privacy and consent requirements are defined in [privacy-consent.md](./privacy-consent.md).

The agent must not pretend to be a named human, must explain why it asks for contact information, avoid unnecessary personal or sensitive data, respect WhatsApp opt-out and send safe summaries rather than full raw transcripts by default. The visible chat UI does not need to label every interaction as AI, but transparency/consent must be available before contact capture and in privacy copy.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Visitor Opens The Floating Agent (Priority: P1)

As a Pilates studio owner visiting `/pilates`, I want to notice a premium floating assistant without it blocking the landing, so I can start a conversation when I have questions or want help understanding the offer.

**Why this priority**: The floating entry point is the conversion surface. It must feel trustworthy, available and aligned with the landing before any conversation can happen.

**Independent Test**: Visit `/pilates` at desktop and mobile widths, confirm the floating button appears in the bottom-right corner, does not cover primary content or form fields, and opens/closes a chat panel by click or tap.

**Acceptance Scenarios**:

1. **Given** a visitor opens `/pilates`, **When** the first viewport is visible, **Then** the page shows a bottom-right floating button with an agent avatar, a consultative label such as "Consultor", availability copy such as "Atendimento 24h", a Brazil/Portuguese signal and a call icon treatment.
2. **Given** the visitor scrolls the page, **When** content moves behind the fixed area, **Then** the floating button remains accessible without hiding important CTAs, calculator controls or form inputs.
3. **Given** the visitor taps the button, **When** the chat opens, **Then** the panel shows an initial greeting, quick intent options and a message input.
4. **Given** the chat is open, **When** the visitor closes it, **Then** the page returns to the compact floating button without losing the current page state.

---

### User Story 2 - Agent Answers Questions And Sells Consultatively (Priority: P1)

As a studio owner, I want the AI attendant to answer my questions, explain the system in plain Pilates-specific language and ask what is painful in my operation, so I understand which agents can help my studio and whether I should subscribe now, request analysis or talk to a human.

**Why this priority**: The feature is valuable only if the conversation answers doubts and sells the actual system, not a generic chatbot or vague automation.

**Independent Test**: Start a conversation, choose at least three different pain paths and verify the agent asks clarifying questions, maps each pain to the correct operational agents and recommends the next step.

**Acceptance Scenarios**:

1. **Given** the chat starts, **When** the visitor asks "o que esse sistema faz?", **Then** the agent explains that Taliya is a complete operational CRM for Pilates studios with AI agents integrated into the CRM, not a generic chatbot or disconnected WhatsApp automation.
2. **Given** the visitor selects or writes a pain such as reposicoes, faltas, mensalidades, alunos inativos, interessados, agenda baguncada or historico do aluno, **When** the agent responds, **Then** it connects that pain first to the CRM area that organizes the work and then to one or more of the seven primary agents: Atendimento, Agenda, Vendas, Financeiro, Retencao, Gestao and Historico/Evolucao.
3. **Given** the visitor gives vague answers, **When** the agent needs more context, **Then** it asks one short consultative question at a time instead of overwhelming the visitor.
4. **Given** the visitor shows buying intent, **When** the agent has enough context, **Then** it recommends the best-fit plan, handles the relevant risk reducers and offers the configured plan/checkout path without sending cold visitors straight to pricing.
5. **Given** the visitor asks a practical buying question about plans, price, setup, WhatsApp, human control, privacy, cancellation, included agents or what happens after subscribing, **When** the agent responds, **Then** it answers from trusted configuration/approved context first and only then guides the visitor to the next conversion step.
6. **Given** the visitor has broad operational needs or wants the complete system, **When** the agent recommends a plan, **Then** it prioritizes the configured recommended/highest-value plan and uses lower plans only as comparison, budget-fit or fallback options.
7. **Given** the visitor asks "quero ver os planos" or "tem uma pagina de planos?", **When** the agent responds, **Then** it gives a short plan-summary answer, asks one qualifying question if context is missing and routes the visitor to the configured public plans destination when appropriate rather than trying to make the chat the only comparison surface.
8. **Given** the visitor asks for a demonstration or says they want to see how it works, **When** the agent responds, **Then** it offers the configured guided demo page and preserves context so the consultor can continue after the demo.
9. **Given** the visitor enters through widget, consultor CTA, WhatsApp CTA, guided demo, custom-agent diagnostic report CTA or FAQ doubt CTA, **When** the first response or report-driven continuation is generated, **Then** the opening tone follows the Entry Intent Matrix for that source.

---

### User Story 3 - Agent Captures Qualification And Hands Off To Conversion (Priority: P1)

As the project operator, I want the agent to collect useful qualification context and pass the visitor to the right conversion path, so conversations become plan recommendations, guided demos, subscriptions or qualified human follow-up opportunities instead of anonymous chat.

**Why this priority**: The agent must help sell and qualify, not only answer questions.

**Independent Test**: Complete a conversation through consultor-led plan recommendation, guided demo, analysis CTA and human WhatsApp CTA, confirming each handoff includes selected pain, agent interest, lead details if provided and landing context.

**Acceptance Scenarios**:

1. **Given** the visitor wants to subscribe, **When** the agent has enough context or the visitor insists on buying, **Then** it sends them to the configured plan/checkout path without asking for card data inside the chat.
2. **Given** the visitor already interacted with landing sections, **When** the chat opens, **Then** the agent can reference non-sensitive page context such as selected pain, selected agent or calculator estimate if available.
3. **Given** the visitor wants analysis before subscribing, **When** lead details are collected, **Then** the agent sends them to the analysis/diagnostic form or prefilled diagnostic state and records a concise conversation summary.
4. **Given** the visitor asks to talk to a human before subscribing, **When** the agent has or requests a safe contact, **Then** it routes the visitor to WhatsApp with a concise summary for assisted closing.
5. **Given** the visitor declines to share contact details, **When** the conversation continues, **Then** the agent still answers product questions and offers guided demo, plan recommendation or analysis CTA without pressure.
6. **Given** the agent captures a meaningful conversion signal, **When** the conversation reaches guided demo, plan-comparison intent, subscription intent, analysis request, human WhatsApp assistance or custom-agent follow-up, **Then** the system creates or updates one lead record in the configured operator-visible lead source of truth.
7. **Given** the operator opens the lead destination, **When** leads from web chat and WhatsApp exist, **Then** all leads appear in one list with status, priority, channel, contact when available, selected/interested plan, captured pains and next action.

---

### User Story 4 - Conversation Stays Safe, Accurate And Brand-Aligned (Priority: P2)

As the project operator, I want the agent to stay inside approved product claims, protect visitor data and handle abuse or irrelevant requests gracefully, so the landing remains trustworthy.

**Why this priority**: An AI attendant can damage trust if it overpromises, leaks internal strategy or accepts adversarial instructions.

**Independent Test**: Run adversarial and edge-case conversations, including prompt-injection attempts, pricing demands, unsupported feature promises, personal data requests and off-topic messages.

**Acceptance Scenarios**:

1. **Given** a visitor asks the agent to ignore instructions, reveal prompts or expose internal project details, **When** the agent responds, **Then** it refuses briefly and returns to helping with studio operations.
2. **Given** a visitor asks for guaranteed financial results, unconfigured pricing, discounts or unsupported integrations, **When** the agent responds, **Then** it avoids false commitments, uses only configured plan information and offers guided demo, analysis, plan recommendation or human WhatsApp assistance.
3. **Given** a visitor shares sensitive health, student or payment details, **When** the agent responds, **Then** it avoids storing or repeating unnecessary sensitive details and redirects to general operational guidance.
4. **Given** the agent cannot answer confidently, **When** it reaches a fallback state, **Then** it offers human WhatsApp follow-up or the analysis form instead of inventing information.
5. **Given** a visitor asks for a feature that is not confirmed in the current product, **When** the agent responds, **Then** it does not promise the feature exists, asks about the operation behind it and separates primary-agent configuration from a true Agente sob medida request.
6. **Given** a visitor requests an operation outside the seven primary agents, such as Marketing, **When** the agent classifies it as Agente sob medida, **Then** it asks for more details, requests email or cellphone/WhatsApp and says the team will contact them.

---

### User Story 5 - Visitor Talks To The Same Agent On WhatsApp (Priority: P1)

As a Pilates studio owner who prefers WhatsApp, I want to talk to the same attendant through WhatsApp, so I can ask questions, describe my operation and request follow-up without depending only on the landing chat.

**Why this priority**: WhatsApp is a primary attendance channel for the target buyer. If the agent only works in the web widget, the implementation misses an important part of the sales and support promise.

**Independent Test**: Send inbound WhatsApp messages through a configured messaging-provider webhook, confirm the backend normalizes the message, uses the same AI attendant behavior as the web chat, replies safely through the provider and emits channel-aware handoff/tracking events.

**Acceptance Scenarios**:

1. **Given** a studio owner starts or continues a WhatsApp conversation, **When** they ask what the system does, **Then** the same attendant explains the operational AI agents using the approved product context.
2. **Given** the owner describes a pain on WhatsApp, **When** the backend receives the inbound message, **Then** it maps the pain to the same seven primary agents and stores the conversation state for future turns.
3. **Given** WhatsApp provider retries the same inbound webhook, **When** the backend receives the duplicate provider message ID, **Then** it does not create duplicate assistant replies or duplicate handoff events.
4. **Given** the owner requests a custom operation such as Marketing on WhatsApp, **When** it is classified as Agente sob medida, **Then** the agent asks for details, confirms email or cellphone/WhatsApp as contact and says the team will contact them.
5. **Given** the owner says they do not want more WhatsApp messages, **When** the agent receives that opt-out intent, **Then** it stops automated replies except for one brief confirmation if allowed by the provider policy.

---

### User Story 6 - Operator Controls Sales Leads In One Inbox (Priority: P1)

As the SaaS operator, I want an internal inbox with all leads who may subscribe to the SaaS, so I can control follow-up, take over conversations, send checkout links and close sales without losing context across widget, WhatsApp and plans-page interactions.

**Why this priority**: The Atendente IA can create buying intent, but the business still needs a reliable human control surface before the full SaaS product exists. Without this inbox, human takeover and lead management depend on scattered tools.

**Independent Test**: Generate leads from web widget, WhatsApp, plans-page intent and custom-agent request; verify they appear in the internal Sales Inbox, can be filtered, can be merged safely, can be taken over by an operator and can emit optional n8n alerts without blocking the lead record.

**Acceptance Scenarios**:

1. **Given** a lead starts in the web widget and later continues on WhatsApp with the same phone or carried `leadId`, **When** the operator opens the Sales Inbox, **Then** one unified lead conversation appears with both channels represented.
2. **Given** a lead asks for a human or reaches high buying intent, **When** the operator opens the Sales Inbox, **Then** the lead appears with priority, interested plan, captured pains, safe summary and next action.
3. **Given** the operator clicks `take_over`, **When** the lead is in a WhatsApp conversation, **Then** AI replies pause for that lead/session and the operator can send WhatsApp messages through the server-side provider adapter.
4. **Given** the operator sends a plans page or checkout link, **When** the action is submitted, **Then** the link comes from trusted configuration and the system records `checkout_sent` or the correct action state without marking the lead as paid.
5. **Given** the operator marks the lead as won, lost, waiting customer, follow-up scheduled or do-not-contact, **When** the action succeeds, **Then** the Sales Inbox updates internal state, emits audit/tracking and sends optional n8n notifications when configured.
6. **Given** n8n is unavailable, **When** the operator updates the Sales Inbox, **Then** the internal inbox remains usable and records the external automation status for retry/notification.

---

### Edge Cases

- The floating button must not cover the mobile diagnostic form submit button, cookie/banner areas if added later, or sticky page CTAs.
- The chat must keep messages readable when the viewport height is small or the mobile keyboard is open.
- The agent must use a live server-side AI response layer for normal conversations; if the provider fails temporarily, the visitor still sees a useful guided fallback instead of a broken chat.
- The agent must rate-limit repeated submissions or very fast messages to avoid spammy tracking and lead records.
- The agent must not use prohibited public terms from the landing spec, including "beta", "MVP", "validacao", "lead", "ROI", "ticket medio", "dashboard" or "workflow".
- WhatsApp webhook retries must be idempotent by provider message ID.
- WhatsApp delivery failures must be tracked without breaking the web widget.
- WhatsApp replies must be limited to inbound or explicitly opted-in conversations; no proactive broadcasts or cold outbound messages are part of this feature.
- The agent must not collect card data, payment credentials or billing documents inside the chat or WhatsApp.
- Checkout failure, cancellation or abandoned checkout must not be treated as an active subscription by the agent.
- The visible chat does not need to repeatedly say the visitor is talking to AI, but the agent must not impersonate a named human and must keep AI/privacy transparency available before contact capture.
- The agent must not collect contact details before there is intent for analysis, human assistance, custom-agent follow-up or strong buying interest.
- Sales Inbox ambiguous lead matches must not auto-merge based only on studio name, IP, browser or similar weak signals.
- Sales Inbox operator messages must never expose provider secrets or send arbitrary model-generated checkout URLs.
- Sales Inbox `won` status must not be treated as paid subscription unless Spec 3 billing webhook confirms payment.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST render a fixed bottom-right floating agent button on `/pilates`.
- **FR-002**: The floating entry MUST remain visually aligned with the provided reference: avatar, black compact pill, consultative label such as "Consultor", "Atendimento 24h", Portuguese/Brazil signal and call action.
- **FR-003**: The floating entry MUST be responsive, touch-friendly and accessible by keyboard.
- **FR-004**: The floating entry MUST open a chat panel without navigating away from the current landing section.
- **FR-005**: The chat panel MUST support a greeting, quick replies, message history, text input, close action and minimized state.
- **FR-005A**: The widget UI MUST define and implement the display modes `minimized_idle`, `minimized_attention`, `minimized_active`, `opening_transition`, `open_desktop`, `open_mobile`, `typing_loading`, `error_fallback` and `handoff_cta`.
- **FR-005B**: Each widget display mode MUST make its purpose clear to a first-time visitor and MUST preserve state, context and accessibility when switching modes.
- **FR-005C**: The widget visual design MUST be revisited before launch so minimized, open, loading, error and handoff states look premium, legible and aligned with the strongest landing sections.
- **FR-005D**: The closed widget MAY use restrained attention motion, but it MUST limit nudges per session, pause after interaction, avoid automatic sound or aggressive shake and respect `prefers-reduced-motion`.
- **FR-006**: The chat MUST send normal free-text visitor messages to a live server-side AI response layer.
- **FR-007**: The AI response layer MUST receive controlled product context, landing context, conversation state, guardrail rules and approved niche-specific agent mapping.
- **FR-008**: The AI response layer MUST keep provider credentials, system instructions and private control logic on the server.
- **FR-009**: The AI response layer MUST return structured response metadata including detected intent, captured pain, recommended agents, qualification state, guardrail decision and optional handoff.
- **FR-010**: The agent MUST explain the product as a complete operational CRM for Pilates studios with AI agents integrated into the CRM, not as a generic chatbot, generic automation, consulting service or disconnected WhatsApp bot.
- **FR-011**: The agent MUST answer visitor questions and ask consultative questions about the studio owner's pains before pushing subscription, analysis or human assistance.
- **FR-012**: The agent MUST map visitor pains to the seven primary agents: Atendimento, Agenda, Vendas, Financeiro, Retencao, Gestao and Historico/Evolucao.
- **FR-012A**: The agent MUST map visitor pains to both CRM areas and AI agents; it MUST explain that the CRM organizes the operational data/work and the agents act on top of that context.
- **FR-012B**: The Diagnostico Gratuito flow MUST ask consultative questions about studio size, operational pains, daily visibility, replacements, sales follow-up, current system, priority goal, buying timing and contact preference, then produce a CRM-plus-agent diagnostic with one dynamic next step.
- **FR-012C**: During the Diagnostico Gratuito flow, the AI response layer MUST classify whether each visitor turn answers the current question, asks a side question, asks for price/plans, requests a custom-agent path, requests a human, cancels the diagnostic or is unclear; this classification MUST prevent repeated questions when the visitor gives a valid free-text answer.
- **FR-012D**: Every normal diagnostic answer MUST receive a short contextual acknowledgement or feedback before the next diagnostic question, unless the visitor asked to cancel, switch paths or receive an immediate safety/guardrail response.
- **FR-012E**: The final diagnostic MUST be delivered in separated chat steps after a hold/typing moment, and each recommended agent MUST include a pain summary, recommendation reason and practical action. The final plan recommendation MUST come after the CRM base and agent logic, not before them.
- **FR-013**: The agent MUST keep Agente sob medida as an expansion option, not as an eighth primary agent.
- **FR-014**: The agent MUST offer plan recommendation before checkout when buying intent is high enough, and MUST NOT use checkout as the default first step for cold visitors.
- **FR-015**: The agent MUST offer guided demo, analysis/Dinheiro na Mesa or WhatsApp assistance as consultative alternatives when the visitor is not ready to subscribe.
- **FR-016**: The agent MUST capture qualification fields only after intent is shown or human assistance is requested: name, WhatsApp, studio name, city/state, active student range, biggest pain and preferred next step.
- **FR-017**: The agent MUST attach landing context to the conversion handoff: `niche`, `sourcePage`, selected pain, selected agent, calculator estimate if available, conversation summary, public offer mode and selected conversion path.
- **FR-018**: The agent MUST emit tracking events for open, close, message sent, quick reply clicked, pain captured, agent recommended, qualification started, guided demo CTA, plan recommendation CTA, checkout CTA, analysis handoff, human WhatsApp handoff and fallback.
- **FR-019**: The agent MUST include `niche`, `sourcePage`, `campaignStage`, `publicOfferMode`, `channel`, `eventName` and `metadata` in every tracking event.
- **FR-020**: The agent MUST refuse prompt-injection requests, requests to reveal internal instructions and requests unrelated to the studio attendance/commercial context.
- **FR-021**: The agent MUST avoid unsupported promises about guaranteed revenue, exact implementation timelines, unconfigured pricing, unauthorized discounts, medical advice, legal advice or payment handling.
- **FR-022**: The agent MUST not collect or request sensitive student health details, full payment credentials, card data, billing documents or private customer records.
- **FR-023**: The chat MUST have a guided fallback conversation path only for AI provider failure, timeout or blocked unsafe input; fallback MUST NOT replace the live AI response layer for normal operation.
- **FR-024**: The visible copy MUST remain Pilates-specific and follow the same public-copy restrictions as the main landing.
- **FR-025**: The feature SHOULD be configurable by niche so future landing routes can reuse the floating agent with different avatar, copy, pains, agent mapping and conversion destinations.
- **FR-026**: When asked for unsupported or unconfirmed functionality, the agent MUST NOT claim it exists; it MUST clarify the underlying operation and determine whether it is configuration inside one of the seven primary agents or a true Agente sob medida request for an unmapped operation.
- **FR-027**: When a chat request is classified as Agente sob medida, the agent MUST capture a short operation summary, ask for email or cellphone/WhatsApp and explain that the team will contact the visitor.
- **FR-027A**: The system MUST provide a separate custom-agent diagnostic report mode for the landing's Agente sob medida block, using a dedicated route and response schema rather than the normal chat response schema.
- **FR-027B**: The custom-agent diagnostic report MUST classify requests as `mapped_solution`, `custom_agent`, `mixed_solution` or `unclear`.
- **FR-027C**: For `mapped_solution`, the diagnostic report MUST route to the normal SaaS sales funnel with diagnostic context and CTAs for consultor, guided demo when ready/gated and WhatsApp continuation.
- **FR-027D**: For `custom_agent`, the diagnostic report MUST route to consultor or WhatsApp in custom-agent proposal mode and ask for more operation details before collecting contact or promising follow-up.
- **FR-027E**: For `mixed_solution`, the diagnostic report MUST separate the mapped SaaS part from the custom-agent part and must not imply the custom part is included in public plans.
- **FR-027F**: The custom-agent diagnostic report MUST NOT route directly to checkout; checkout is still governed by plan/checkout gates after consultor-led recommendation or intentional plans-page action.
- **FR-028**: The same AI attendant MUST support two conversation channels in v1: the landing web widget and WhatsApp.
- **FR-029**: The backend MUST normalize all inbound channel turns into one shared conversation contract with `channel`, `sessionId`, `externalContact`, message history, landing context when available and qualification state.
- **FR-030**: WhatsApp inbound messages MUST enter through a server-side webhook route, not through browser-side provider calls.
- **FR-031**: WhatsApp webhook handling MUST validate provider authenticity using the available provider signature, token or shared secret mechanism.
- **FR-032**: WhatsApp webhook handling MUST be idempotent by provider message ID and MUST NOT send duplicate assistant replies for duplicate webhook deliveries.
- **FR-033**: WhatsApp conversations MUST use a server-side session store so pain, qualification, opt-out state and handoff context survive across turns.
- **FR-034**: WhatsApp automatic replies MUST only occur inside an inbound or explicitly opted-in conversation. Proactive campaigns, broadcast messages and cold outbound messages are out of scope for this feature.
- **FR-035**: WhatsApp replies MUST pass the same input guardrails, AI context, output guardrails, fallback behavior, tracking and n8n handoff rules as the web widget.
- **FR-036**: WhatsApp channel events MUST include `channel: "whatsapp"`, provider message IDs, delivery/failure metadata when available and safe contact identifiers.
- **FR-037**: If the WhatsApp provider is unavailable, the system MUST record a safe failure event and avoid losing the conversation state; the web widget must remain unaffected.
- **FR-038**: When a visitor asks to subscribe, the agent MUST route them to a configured checkout or plan-selection destination and MUST NOT claim subscription activation until a trusted billing flow confirms it.
- **FR-039**: When a visitor asks to talk to a human before subscribing, the agent MUST route them to WhatsApp for assisted closing and include a safe summary of pain, recommended agents and intent.
- **FR-040**: The agent MUST distinguish guided demo, plan-comparison intent, subscription intent, analysis request, human WhatsApp assistance, custom-agent follow-up and custom-agent diagnostic report outcomes as separate conversion paths in structured response metadata.
- **FR-041**: The agent MUST read plan names, prices, recommended plan, checkout destinations and WhatsApp assistance destinations from trusted system configuration and MUST NOT duplicate those values in prompts or component text.
- **FR-042**: When asked about price, the agent MUST answer from configured plan data when available; if pricing is missing from configuration, it MUST say it can route the visitor to human WhatsApp assistance or analysis instead of inventing prices.
- **FR-043**: WhatsApp v1 MUST use the official Meta WhatsApp Cloud API provider adapter.
- **FR-044**: The system MUST include usage/cost controls for AI and WhatsApp traffic: message length limits, per-session rate limits, daily caps, provider timeout, fallback behavior and server-side logging of usage events.
- **FR-045**: The implementation MUST include eval fixtures before public release for supported pain mapping, plan/pricing answers, consultor-led plan recommendation, guided demo, human WhatsApp assistance, Agente sob medida, WhatsApp idempotency, opt-out and guardrails.
- **FR-046**: The WhatsApp session/idempotency store MUST be server-side and production-capable; in-memory storage is allowed only for local development and must not be used for production E2E.
- **FR-047**: Human WhatsApp handoff MUST follow `human-whatsapp-handoff.md`, including safe summary, trusted destination, handoff tracking and AI pause/reduced-automation rules.
- **FR-048**: The agent MUST NOT impersonate a named human attendant and MUST keep AI/privacy transparency available through consent/privacy copy before contact capture.
- **FR-049**: The agent MUST provide or link to privacy/consent information before collecting contact details.
- **FR-050**: The agent MUST explain why contact data is requested and MUST ask for it only after minimum commercial interest exists, such as a stated pain, diagnostic request, analysis request, human assistance request, WhatsApp continuation, custom-agent follow-up, plan/pricing/demo interest or strong buying intent.
- **FR-051**: n8n and tracking payloads MUST use safe summaries and structured metadata by default, not full raw transcripts.
- **FR-052**: WhatsApp opt-out and consent state MUST be included in handoff/session metadata when available.
- **FR-053**: The agent MUST treat the configured recommended/highest-value plan as the default commercial recommendation for broad operational pain, complete-system interest or high buying intent.
- **FR-054**: The agent MUST NOT recommend a lower plan first unless the visitor explicitly asks for the cheapest/narrowest option, the configured recommended plan is unavailable, or the visitor's stated need only fits a lower plan.
- **FR-055**: The agent MUST use lower plans as comparison, objection handling, budget-fit or fallback options that support the sale of the recommended/highest-value plan, not as equal default outcomes.
- **FR-056**: The agent MUST answer purchase-relevant questions about plans, pricing, setup, onboarding, WhatsApp, human takeover, included agents, Agente sob medida, integrations, limits, privacy, cancellation/contract terms when configured and post-subscription steps using trusted configuration or approved product context.
- **FR-057**: When the agent cannot answer a purchase-relevant question from trusted configuration or approved context, it MUST say what is not confirmed, avoid inventing, and route to guided demo, plan recommendation, analysis or WhatsApp assistance according to visitor intent.
- **FR-058**: Web widget and WhatsApp conversations MUST share the same answer policy, commercial strategy, plan recommendation rules and guardrails.
- **FR-059**: The visible chat UI MUST NOT be required to label every message as AI, but the agent MUST NOT impersonate a named human and MUST expose privacy/consent context before collecting contact.
- **FR-060**: The system MUST create or update an operator-visible lead record for every guided demo handoff, plan-comparison intent, analysis request, human WhatsApp assistance request, custom-agent follow-up request, provided contact, high-intent price/how-to-start interaction or subscription intent.
- **FR-061**: The system MUST define exactly one primary lead source of truth for v1: the internal Sales Inbox backed by the configured database.
- **FR-062**: Lead notifications, daily digests and alerts MUST NOT be treated as the lead source of truth.
- **FR-063**: Lead records MUST include channel, source page, conversion path, selected/interested plan, captured pains, recommended agents, qualification fields when provided, safe summary, status, priority and consent/opt-out metadata when available.
- **FR-064**: The operator MUST be able to view all leads in one place and filter or identify leads by status, priority, channel and next action.
- **FR-065**: Lead records MUST be created/updated using idempotency keys so WhatsApp retries or repeated webhook deliveries do not duplicate leads.
- **FR-066**: External CRM/spreadsheet sync MUST NOT be required for v1 lead capture or operator control.
- **FR-067**: Optional n8n automation MUST run server-side only; the browser MUST NOT call n8n directly or receive n8n credentials.
- **FR-068**: The Sales Inbox database MUST store cold leads, qualified leads, hot leads, waitlist interest, contact data, conversation summaries and operator state needed for follow-up.
- **FR-069**: Lead storage MUST minimize duplicates by using stable identifiers such as leadId, sessionId, WhatsApp number, provider contact id and email.
- **FR-070**: If optional n8n automations fail, the system MUST preserve chat/conversion behavior, keep the Sales Inbox usable and record the external automation status.
- **FR-071**: The agent MUST support a `view_plans`/plan-comparison intent that first answers and qualifies, then routes visitors to the configured public plans destination when appropriate.
- **FR-072**: For v1, the configured public plans destination SHOULD be `/pilates/planos`; the agent MUST use configuration rather than hardcoded URLs.
- **FR-073**: When routing to the plans destination, the agent SHOULD provide a concise summary of Base, 1 Agente, 3 Agentes and 7 Agentes, highlight the configured recommended complete-system plan when relevant, include captured context and avoid long plan tables inside chat.
- **FR-074**: Plan-comparison routing MUST emit tracking/lead metadata distinct from checkout/subscription intent, so "viewed plans" is not treated as active subscription intent.
- **FR-075**: The web widget MUST be able to navigate to the plans page without losing the chat session.
- **FR-075A**: The agent MUST support a `guided_demo` intent that routes visitors to the configured guided demonstration destination and preserves selected pain, selected agent and conversation context when available.
- **FR-101**: The agent MUST receive and use `entryPath` metadata for widget, consultor CTA, WhatsApp CTA, guided demo and custom diagnostic entries, and MUST preserve `sourceSection=faq_doubt_cta` when the normal widget flow starts from the FAQ CTA.
- **FR-102**: The first response MUST follow the Entry Intent Matrix and MUST NOT use the same opening message for every entry path.
- **FR-103**: The agent MUST enforce plan-display gates before routing to `/pilates/planos`.
- **FR-104**: The agent MUST enforce checkout gates before offering checkout.
- **FR-105**: For recommendations above R$ 1.000/month, the agent SHOULD follow the high-ticket sales sequence: pain, impact, proof/demo, recommended plan, lower-plan comparison, objections/risk reducers and then plans/checkout.
- **FR-106**: Before checkout handoff, the agent MUST make available answers for post-payment next step, studio-owned WhatsApp Business, setup/onboarding help, human control, plan changes when configured, usage caps, cancellation/contract when configured and payment-data safety.
- **FR-106A**: When asked about WhatsApp setup, personal WhatsApp, WhatsApp Business or same-number personal/studio use, the agent MUST explain that operational WhatsApp agents require the studio to have or prepare a WhatsApp Business number, and MUST recommend separating personal and studio conversations before activation when the same number is used for both.
- **FR-107**: The guided-demo agent/guide MUST explain demo steps, answer product doubts and route to consultor, WhatsApp, plans or checkout according to readiness while keeping demo actions deterministic.
- **FR-108**: The agent MUST follow the approved objection matrix, follow-up policy, lead priority/readiness model and commercial boundaries defined in `commercial-sales-playbook.md`.
- **FR-109**: The system MUST include eval coverage for the objection matrix, follow-up consent, WhatsApp ownership, plan recommendation, checkout gates, unsupported feature handling, commercial terms fallback and fiscal/invoice fallback before public launch.
- **FR-076**: The AI context MUST include the approved answer knowledge file as product/commercial context after trusted runtime configuration.
- **FR-077**: When trusted configuration and approved answer knowledge do not cover a buyer question, the agent MUST avoid inventing and route to the correct next step.
- **FR-078**: Human takeover on the same WhatsApp AI number MUST use a protected operator reply surface or approved shared inbox; external spreadsheets are insufficient for real-time takeover.
- **FR-079**: The operator reply surface MUST support handoff session list, safe context, recent messages, pause AI, send human reply, resume AI and close/won/lost/do-not-contact states.
- **FR-080**: While a WhatsApp session is marked `human_active`, the AI MUST NOT send automated replies unless the operator explicitly resumes AI or a later allowed inbound context restarts automation.
- **FR-081**: Operator WhatsApp replies MUST be sent through the server-side WhatsApp provider adapter and MUST NOT expose provider credentials to the browser.
- **FR-082**: Operator takeover, reply, resume and close actions MUST emit audit/tracking events and update the operator-visible lead pipeline in the Sales Inbox, with optional n8n alert/digest events when configured.
- **FR-083**: The system MUST provide an internal Sales Inbox for the SaaS operator's own commercial leads before claiming full human takeover support.
- **FR-084**: The Sales Inbox MUST include leads from web widget, WhatsApp, guided-demo intent, plans-page intent, subscription intent, analysis request, human assistance request, custom-agent follow-up and custom-agent diagnostic report CTA/result paths.
- **FR-085**: The Sales Inbox MUST distinguish its scope from the future paying-studio inbox; it manages SaaS sales leads only, not students or interested students of paying studios.
- **FR-086**: The Sales Inbox MUST use a server-side conversation/lead store for real-time state and lead follow-up.
- **FR-087**: The Sales Inbox MUST remain the v1 commercial lead source of truth for reporting/pipeline and the real-time message/reply surface.
- **FR-088**: The Sales Inbox MUST support safe lead merge by WhatsApp number, email, explicit `leadId` or explicit `sessionId` and MUST NOT auto-merge based only on studio name, IP or browser fingerprint.
- **FR-089**: The Sales Inbox MUST support lead statuses `ai_active`, `handoff_requested`, `human_active`, `waiting_customer`, `follow_up_scheduled`, `checkout_sent`, `won`, `lost` and `do_not_contact`.
- **FR-090**: The Sales Inbox MUST allow filtering by status, priority, channel, conversion path, interested plan, next action and last activity.
- **FR-091**: The Sales Inbox lead detail MUST show contact, studio, city/state, captured pains, interested plan, recommended agents, custom-agent request when applicable, safe summary, consent/opt-out context and recent messages.
- **FR-092**: The Sales Inbox MUST support operator actions `take_over`, `send_whatsapp_message`, `send_plan_page`, `send_checkout_link`, `schedule_follow_up`, `resume_ai`, `mark_waiting_customer`, `mark_won`, `mark_lost`, `mark_do_not_contact` and `edit_lead_summary`.
- **FR-093**: `send_plan_page` and `send_checkout_link` MUST use trusted configured destinations and MUST NOT accept arbitrary model-generated or operator-typed checkout URLs.
- **FR-094**: `send_checkout_link` and `checkout_sent` MUST NOT mark the lead as paid or subscribed; paid subscription state can come only from Spec 3 billing confirmation.
- **FR-095**: `take_over` MUST pause automated WhatsApp AI replies for that lead/session until the operator resumes AI or the conversation reaches a terminal state.
- **FR-096**: Sales Inbox operator actions MUST be authenticated/authorized for internal operator/admin access only.
- **FR-097**: Browser code for the Sales Inbox MUST NOT receive WhatsApp provider credentials, n8n secrets, database credentials, OpenAI keys or billing secrets.
- **FR-098**: Every Sales Inbox operator action MUST create an audit event with actor, action, lead/session, timestamp, before/after status when applicable and safe metadata.
- **FR-099**: Sales Inbox status changes MAY emit safe n8n alerts/digests when configured, and n8n failure MUST NOT block the operator from continuing the real-time conversation.
- **FR-100**: Sales Inbox must store only the messages and summaries needed for operation, must not store payment credentials and must avoid sending full raw transcripts to external automations by default.
- **FR-110**: All commercial surfaces MUST use one trusted configuration source for plan names, prices, recommended plan, usage caps, checkout destinations and WhatsApp destinations.
- **FR-111**: The agent MUST include eval coverage for the core sales objection set: price concern, existing receptionist, small studio, distrust of AI, "vou pensar", WhatsApp continuation, agenda-only request, setup fear, plan comparison, immediate subscription, custom-agent request and unsupported integration.
- **FR-111A**: The agent MUST improve only through supervised, source-controlled calibration. It MUST NOT automatically rewrite its own prompts, route gates, safety rules, prices, plan recommendations or lead-state logic from live conversations without human review and passing evals.
- **FR-111B**: Every agent-behavior calibration round MUST produce or update eval fixtures, practical QA notes or a readiness report covering tested paths, corrected failures, remaining blind spots and go/no-go status before broader traffic.
- **FR-112**: Widget-to-WhatsApp continuation MUST preserve `leadId`/session context when available and MUST merge leads only through strong identifiers.
- **FR-113**: If widget-to-WhatsApp identity is uncertain, the system MUST avoid automatic merge and keep the operator-visible lead context reviewable.
- **FR-114**: Human takeover behavior MUST be enforced server-side: `human_active` pauses WhatsApp AI replies, `resume_ai` explicitly resumes them and terminal states prevent automatic restart.
- **FR-115**: WhatsApp proactive or out-of-window follow-up MUST use approved Meta templates from `whatsapp-template-copy.md`; unapproved, rejected, paused or missing templates MUST block the send and create a Sales Inbox event.
- **FR-116**: Funnel metrics MUST distinguish at minimum widget opened, consultor CTA, WhatsApp CTA, guided demo started/completed, meaningful message, pain captured, plan asked, plan recommended, plans page opened, checkout intent, checkout link sent, payment confirmed, onboarding started/completed and lead won/lost.
- **FR-117**: The custom-agent diagnostic report MUST be treated as a sales artifact: it must produce a report-quality result, classify the opportunity, explain business impact and always offer the next commercial step without routing directly to checkout.
- **FR-118**: Before launch, QA evidence MUST include a sample web consultor transcript, sample WhatsApp webhook response, sample Sales Inbox lead detail, optional n8n alert payload when configured and screenshots for all widget modes.

### Key Entities

- **Floating Agent Config**: Niche-specific configuration for label, avatar, availability text, greeting, quick replies, pain-to-agent mapping and CTA destinations.
- **Commercial System Config**: Trusted shared configuration for plans, prices, recommended plan, checkout destinations, WhatsApp assistance destinations, campaign stage and public offer mode.
- **Conversation Session**: A visitor's chat state, including open/minimized state, messages, selected intents, captured qualification and landing context.
- **Conversation Channel**: The normalized channel where a turn happened, either `web` or `whatsapp`, with channel-specific identifiers and capabilities.
- **WhatsApp Conversation**: A server-side channel session keyed by provider/contact identifiers, opt-in/opt-out state, recent messages, delivery metadata and qualification context.
- **AI Attendant Message**: A user or assistant message with role, timestamp, content, optional quick replies, intent and safety classification.
- **Qualification Profile**: The business context captured from the visitor, including studio name, WhatsApp, location, active student range, biggest pain and desired next step.
- **Agent Recommendation**: Mapping from a captured pain to one or more operational agents plus a short explanation and suggested action.
- **Analysis Handoff**: The payload that transfers qualified context from chat to analysis form or follow-up channel.
- **Subscription Handoff**: The payload or link that sends a high-intent visitor to plan selection or trusted checkout.
- **Guided Demo Handoff**: The payload or link that sends a visitor to `/pilates/demonstracao` with selected pain, selected agent and conversation context, then returns that context to the consultor.
- **Assisted WhatsApp Handoff**: The safe summary and contact context used when the visitor wants a human to help them decide before subscribing.
- **Custom Agent Diagnostic Report**: A report-style sales result generated from a free-text operation request, classifying whether Taliya already covers it, whether it is Agente sob medida, whether it is mixed or whether more detail is needed. Live AI generation for this report is future scope; v1 may use deterministic/report-style logic.
- **Diagnostic Context Variant**: Metadata passed from a diagnostic report CTA into consultor or WhatsApp so the next message starts with the correct sales path: existing SaaS solution, custom-agent proposal, mixed path or unclear request.
- **Lead Record**: Operator-visible record representing a qualified or high-intent studio prospect, including contact when available, status, priority, channel, conversion path, selected/interested plan, captured pains, recommended agents, safe summary and next action.
- **Lead Source Of Truth**: The single configured destination where the operator sees and manages all sales leads for v1. For this spec, it is the internal Sales Inbox backed by the configured database. It must not be only analytics events, transient notifications or an external spreadsheet.
- **Internal Sales Inbox**: Protected operator surface for controlling the SaaS operator's own commercial leads across widget, WhatsApp, plans-page intent and checkout follow-up. It is not the inbox sold to paying studios.
- **Sales Lead Conversation**: Server-side conversation/control record that joins lead identity, channel sessions, recent messages, AI state, operator state, interested plan, next action and sync status.
- **Lead Merge Decision**: Decision record describing whether web and WhatsApp activity should be joined, based on strong identifiers such as WhatsApp, email, `leadId` or `sessionId`, or left separate for operator review.
- **Operator Action**: Authenticated internal action taken in the Sales Inbox, such as takeover, WhatsApp reply, plan-page link, checkout link, follow-up scheduling, won/lost marking or do-not-contact.
- **Operator Audit Event**: Server-side audit record for Sales Inbox actions, including actor, action, lead/session, before/after state and safe metadata.
- **Guardrail Decision**: The classification and action taken for unsafe, unsupported, off-topic or prompt-injection inputs.
- **Tracking Event**: A structured event emitted by the floating agent with landing context and interaction metadata.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: At 1440px and 390px, the floating button is visible, tappable and does not create horizontal overflow or cover critical landing controls.
- **SC-002**: A first-time visitor can open the agent and understand its purpose within 5 seconds.
- **SC-002A**: A QA pass confirms every widget display mode is visually understandable, polished and functional on desktop, mobile and short viewport heights.
- **SC-002B**: A QA pass confirms closed-widget attention motion is visible but restrained, stops after the session limit or user interaction and is disabled under reduced-motion preference.
- **SC-003**: In test conversations, 90% of supported pain prompts are mapped to the correct primary agent or agent combination.
- **SC-003A**: In diagnostic conversations, the final diagnostic identifies CRM areas and agents for the visitor's pains, captures buying timing when provided and recommends one coherent next step.
- **SC-003B**: Diagnostic evals include free-text answers, ambiguous answers and side questions during the diagnostic, and confirm the agent progresses without requiring quick-reply suggestions or repeating the same question.
- **SC-003C**: Diagnostic evals confirm the final recommendation cards list each indicated agent one at a time with pain summary, reason for recommendation and practical action.
- **SC-004**: A visitor can move from initial chat open to a recommended plan/checkout path in under 2 minutes when they choose a guided path and provide enough context.
- **SC-005**: 100% of tracking events emitted by the agent include landing context fields and channel.
- **SC-006**: Adversarial tests for prompt leakage, false guarantees and sensitive-data collection are refused or safely redirected.
- **SC-007**: The public-copy audit finds none of the prohibited terms in visible floating-agent copy.
- **SC-008**: Normal free-text conversations use the server-side AI response layer, while provider failure scenarios produce a safe fallback instead of a broken chat.
- **SC-009**: A WhatsApp inbound message can receive a safe AI attendant reply through the configured provider in under 10 seconds in normal conditions.
- **SC-010**: Duplicate WhatsApp webhook deliveries produce exactly one assistant reply and one set of tracking/handoff events.
- **SC-011**: Web widget and WhatsApp conversations produce the same pain-to-agent mapping for the same supported pain prompts.
- **SC-012**: Opt-out language on WhatsApp stops automated follow-up replies for that contact/session.
- **SC-013**: A visitor who asks to talk to a human before subscribing is routed to WhatsApp with a safe assisted-closing summary.
- **SC-014**: The agent never asks for card data or treats a checkout attempt as an active subscription without trusted billing confirmation.
- **SC-015**: Changing configured plan price, recommended plan or checkout destination updates the agent response and CTA behavior without editing prompts or visible component copy.
- **SC-016**: Usage/cost tests confirm repeated fast messages are rate-limited, provider timeouts fall back safely and usage events are logged server-side.
- **SC-017**: The eval fixture set covers all supported pains, all conversion paths, price questions, unsupported/custom-agent requests, WhatsApp duplicate webhooks and opt-out language.
- **SC-018**: A human WhatsApp handoff produces a safe summary, uses a trusted configured destination and does not keep selling as if AI were the human closer.
- **SC-019**: Contact capture flows explain purpose and expose privacy/consent copy before the visitor submits contact details.
- **SC-020**: In evals, broad-pain and complete-system conversations recommend the configured recommended/highest-value plan before lower plans.
- **SC-021**: In evals, lower-plan suggestions appear only for explicit budget/narrow-scope requests, missing recommended-plan configuration or comparison/objection handling.
- **SC-022**: In evals, purchase-relevant questions are answered directly from trusted configuration/approved context before the agent offers subscription, analysis or WhatsApp assistance.
- **SC-023**: Web and WhatsApp produce the same plan recommendation and answer policy for equivalent buyer questions.
- **SC-024**: 100% of guided demo handoff, plan-comparison intent, analysis, human WhatsApp assistance, custom-agent follow-up, subscription intent and provided-contact conversations create or update one lead record in the configured lead source of truth.
- **SC-025**: Duplicate WhatsApp webhook deliveries do not create duplicate lead records.
- **SC-026**: The operator can open one configured destination and see all leads with status, priority, channel, conversion path and next action.
- **SC-027**: The Sales Inbox contains the required lead fields and filters for all leads, high-priority leads, WhatsApp assistance, custom-agent follow-up, subscription intent, waitlist interest and won/lost status.
- **SC-028**: Optional n8n automation failure does not break the web chat, WhatsApp reply flow, guided demo CTA, plan/checkout CTA or analysis CTA.
- **SC-029**: A visitor asking to see plans receives a short consultative answer, can be routed to the configured plans destination and can return to chat without losing context.
- **SC-030**: Plan-comparison events are tracked separately from checkout/subscription CTA events.
- **SC-030A**: A visitor asking for a demo can open the configured guided demonstration page and return to the consultor with selected demo context preserved.
- **SC-036**: Entry-path tests confirm widget, consultor CTA, WhatsApp CTA, guided demo, custom-agent diagnostic and FAQ doubt CTA each produce the correct opening tone, first goal and context payload.
- **SC-037**: Plan-routing tests confirm `/pilates/planos` is offered only after explicit plan interest, enough context, demo recommendation/completion or visitor insistence.
- **SC-038**: Checkout-routing tests confirm checkout is offered only after explicit buying intent, confirmed recommendation, intentional plans-page action or operator-assisted close.
- **SC-039**: High-ticket evals confirm the agent handles pain, impact, proof/demo, recommendation, lower-plan comparison, objections and risk reducers before checkout.
- **SC-031**: The operator can open the internal Sales Inbox and see all commercial leads from web widget and WhatsApp with status, priority, interested plan, channel and next action.
- **SC-032**: A lead that starts in the widget and continues on WhatsApp with matching WhatsApp, email, `leadId` or `sessionId` appears as one unified Sales Inbox conversation.
- **SC-033**: Operator takeover pauses WhatsApp AI replies for that lead/session and allows a human WhatsApp reply through the server-side provider adapter.
- **SC-034**: Sending a plan-page or checkout link from the Sales Inbox uses trusted configuration and does not mark the lead as paid.
- **SC-035**: Sales Inbox status changes create audit events and optional n8n notifications; n8n failure is recorded without blocking the operator conversation.
- **SC-040**: A free-text custom-agent diagnostic request for an existing operation, such as WhatsApp atendimento plus reposicoes, returns a report classified as `mapped_solution`, maps to the correct Taliya agents and offers consultor/demo/WhatsApp CTAs with diagnostic context.
- **SC-041**: A free-text custom-agent diagnostic request for an unmapped operation, such as marketing campaigns, returns a report classified as `custom_agent`, asks for operation scope/contact through consultor or WhatsApp and creates or updates a custom-agent lead.
- **SC-042**: A mixed diagnostic request separates SaaS-covered work from custom-agent work and does not imply Agente sob medida is included in public plans.
- **SC-043**: No custom-agent diagnostic report CTA routes directly to checkout; all checkout paths still pass through existing plan/checkout gates.
- **SC-044**: Changing a configured price, recommended plan or checkout destination updates landing, plans page, agent answers, WhatsApp answers and Sales Inbox link actions without prompt or component copy rewrites.
- **SC-045**: Evals confirm the agent handles every core objection in FR-111 with direct answer, studio-specific value framing and correct next-step routing.
- **SC-046**: A lead that starts in the widget and continues on WhatsApp with a strong identifier appears as one unified Sales Inbox conversation; without a strong identifier it remains separate or requires operator review.
- **SC-046A**: Every calibration change is traceable to a source-controlled prompt/config/code/doc/eval update and passes the affected practical scenarios plus the route matrix before release.
- **SC-046B**: A validation readiness report exists before controlled traffic, documenting scenarios tested, API cost estimate, lead-sync result, corrected issues, skipped/blocked cases and final go/no-go decision.
- **SC-047**: A human takeover test confirms WhatsApp AI replies stop during `human_active`, resume only after explicit operator action and never continue in parallel with the human closer.
- **SC-048**: Out-of-window WhatsApp follow-up is blocked unless the exact approved Meta template is configured and the lead is eligible.
- **SC-049**: Funnel metrics can show conversion performance by entry path, plan interest, channel, diagnostic classification and won/lost outcome.
- **SC-050**: Launch QA evidence includes web transcript, WhatsApp webhook sample, Sales Inbox lead detail, optional n8n payload when configured and widget-mode screenshots.

## Assumptions

- The first version is for `/pilates`, but configuration must support future niches.
- The first version requires a live AI backend for normal free-text responses.
- Live AI generation for the custom-agent diagnostic report is not required for the current Atendente IA launch readiness. It is future scope and must be specified/evaluated separately before public copy markets that block as an AI-powered diagnostic.
- Live AI provider failure must not block the landing, subscription CTA or analysis CTA, but it should be treated as a degraded state and tracked.
- WhatsApp is a first-version channel for replies to inbound or explicitly opted-in conversations. Proactive campaigns, cold outbound and broadcast messaging are not part of this feature.
- WhatsApp requires a configured messaging provider and a server-side session/idempotency store before production use.
- The site will have a plan subscription path, but the landing's primary conversion motion is consultor-led. Pricing and plan details must come from the same trusted configuration used by the landing. If pricing/plan details are not configured yet, the agent may describe only approved plan framing and route to guided demo, analysis or human WhatsApp assistance.
- Full billing, entitlement activation and payment webhooks should be handled by a focused billing/subscription spec; this feature only routes high-intent visitors to the trusted subscription path.
- The existing landing tracking utility remains the canonical event surface unless the implementation plan identifies a necessary extension.
