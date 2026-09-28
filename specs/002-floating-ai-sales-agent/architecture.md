# Architecture Map: Floating AI Attendant

## Purpose

Map the complete implementation of the AI attendant across frontend, WhatsApp channel, backend/API, AI runtime, guardrails, tracking and conversion handoff.

This feature is not only a floating chat button. It is a real server-side AI attendant available through the landing widget and WhatsApp to answer questions, understand the studio owner's pains, offer a guided demonstration when useful and conduct the visitor toward the right plan/checkout path only after consultative recommendation or explicit informed intent. If the visitor wants a person before subscribing, WhatsApp becomes the assisted-closing channel.

## System Overview

```text
Visitor
  -> FloatingAiAttendant UI
    -> local conversation state
    -> tracking events
    -> POST /api/landing/ai-attendant
      -> request validation
      -> input guardrails
      -> context builder
      -> AI provider call
      -> structured response validation
      -> output guardrails
      -> fallback when needed
    -> chat response rendering
    -> conversion handoff
      -> guided demo destination
      -> plan/checkout destination
      -> analysis form / diagnostic anchor
      -> human WhatsApp assistance
      -> tracking summary
      -> n8n webhook automations

Studio owner on WhatsApp
  -> Messaging provider webhook
    -> POST /api/landing/ai-attendant/whatsapp
      -> provider verification
      -> duplicate message check
      -> channel/session normalization
      -> same AI attendant core as web
      -> provider reply adapter
      -> tracking + n8n webhook automations

Visitor
  -> Agente sob medida diagnostic block
    -> POST /api/landing/custom-agent-diagnostic
      -> request validation
      -> input guardrails
      -> supported-agent/custom-operation classifier
      -> AI provider call with diagnostic-report schema
      -> structured report validation
      -> output guardrails
      -> report rendering
      -> report CTA handoff
        -> consultor with diagnostic context
        -> guided demo when mapped and ready/gated
        -> WhatsApp continuation with diagnostic context
        -> Sales Inbox/Postgres lead storage plus optional n8n alert
```

## Frontend Layer

### Responsibilities

- Render the floating button in the bottom-right corner.
- Open, close and minimize the chat panel.
- Own explicit widget display modes: `minimized_idle`, `minimized_attention`, `minimized_active`, `opening_transition`, `open_desktop`, `open_mobile`, `typing_loading`, `error_fallback` and `handoff_cta`.
- Render message history, quick replies, typing/pending state, recommendations and handoff CTAs.
- Keep every mode visually understandable, premium and aligned to the landing, with clear controls for continue, close, minimize, retry and handoff.
- Keep short-lived client session state.
- Send normal free-text messages to the server-side AI route.
- Use fallback output only when the server returns a fallback response.
- Emit UI and funnel tracking events.
- Pass conversion handoff payload to the guided demo, plans page, checkout path, analysis form/anchor or human WhatsApp handoff.

### Files

```text
components/landing/shared/FloatingAiAttendant.tsx
components/landing/shared/FloatingAiAttendantButton.tsx
components/landing/shared/FloatingAiAttendantPanel.tsx
components/landing/NicheLandingPage.tsx
```

### State Owned By Frontend

- `isOpen`
- `isMinimized`
- `messages`
- `pending`
- `selectedQuickReplyId`
- `selectedPainIds`
- `recommendedAgentIds`
- `qualificationDraft`
- `lastHandoff`
- `pageSignals`

### Frontend Must Not Own

- Provider API keys.
- System prompt.
- Private guardrail rules.
- Final truth for agent recommendations.
- Prompt-injection decisions.
- Unsupported-claim decisions.
- WhatsApp provider credentials or webhook handling.

## Channel Layer

### Purpose

Keep the agent behavior the same across web and WhatsApp while respecting each channel's delivery, identity and safety constraints.

### Supported Channels

- `web`: landing floating widget, short-lived browser session state and optional diagnostic form handoff.
- `whatsapp`: inbound or explicitly opted-in WhatsApp conversation through the official Meta WhatsApp Cloud API provider adapter.

### Files

```text
lib/landing/ai-attendant/channels.ts
lib/landing/ai-attendant/session-store.ts
lib/landing/ai-attendant/whatsapp.ts
app/api/landing/ai-attendant/whatsapp/route.ts
```

### Channel Responsibilities

- Normalize every inbound turn into one `AiAttendantRequest`.
- Attach `channel`, `channelSessionId`, provider message IDs and safe contact identifiers.
- Persist WhatsApp conversation state and opt-out state server-side.
- Deduplicate WhatsApp webhooks by provider message ID.
- Enforce channel capability rules before sending a reply.
- Record delivery/failure metadata without exposing provider secrets.

### WhatsApp Boundaries

Production WhatsApp readiness is defined in [whatsapp-e2e-readiness.md](./whatsapp-e2e-readiness.md).

- The system may automatically reply to an inbound WhatsApp conversation when the contact initiated or explicitly opted in.
- The system must not send cold outbound, broadcast, campaign or unrelated follow-up messages in this feature.
- A human or later workflow may follow up only after consent and handoff, and outside the provider service window only through approved Meta templates.
- Opt-out language must stop automated WhatsApp replies for that contact/session.
- V1 uses Meta WhatsApp Cloud API directly. Third-party gateways are out of the default implementation path.
- The adapter must use server-side credentials only and must never expose Meta tokens, app secrets or phone number IDs to the browser.
- Unsupported media/message types must not be passed raw to the model; they are acknowledged safely and routed to text clarification or Sales Inbox when needed.
- Delivery failures/statuses must be recorded as channel metadata and must not break the web widget or Sales Inbox control.

### Session Store Decision

WhatsApp requires server-side persistence because provider retries, opt-out state and multi-turn conversations happen outside the browser.

Production persistence requirements are defined in [persistence-readiness.md](./persistence-readiness.md). The implementation decision is Postgres as the primary durable store, with Redis/KV optional for short-lived counters/locks.

The session store must persist:

- `channelSessionId`
- provider contact ID
- processed provider message IDs
- recent safe conversation history
- opt-in/opt-out state
- selected pains
- recommended agents
- qualification draft
- last reply timestamp
- fallback/guardrail counters

In-memory storage is allowed only for local development because it loses data on restart and cannot deduplicate across server instances.

Production must not use process-local maps for WhatsApp sessions, provider message IDs, opt-out, Sales Inbox leads, operator audit events, AI pause state, Sales Inbox/n8n optional automation sync state, rate limits or usage records.

## Backend/API Layer

### Route

```text
POST /api/landing/ai-attendant
POST /api/landing/custom-agent-diagnostic
POST /api/landing/ai-attendant/whatsapp
```

### Responsibilities

- Accept chat turns from the UI.
- Validate request shape and message length.
- Attach server-trusted defaults for niche, campaign and public offer when possible.
- Run input guardrails before calling the model.
- Build the AI context from approved product config and conversation state.
- Call the AI provider with structured output.
- Validate AI response against the response schema.
- Run output guardrails.
- Return normalized response to the UI.
- Return safe fallback output for provider failure, timeout or invalid model output.
- Verify WhatsApp provider webhooks before accepting inbound WhatsApp messages.
- Persist and retrieve WhatsApp session state before and after each WhatsApp turn.
- Send WhatsApp replies through a provider adapter after output guardrails pass.
- Accept free-text custom-agent diagnostic requests from the landing.
- Classify diagnostic requests as mapped SaaS solution, custom agent, mixed solution or unclear.
- Return a structured report result with CTA context variants rather than chat messages.
- Create/update leads for custom-agent diagnostic outcomes and CTA clicks.

### Files

```text
app/api/landing/ai-attendant/route.ts
app/api/landing/custom-agent-diagnostic/route.ts
lib/landing/ai-attendant/schema.ts
lib/landing/ai-attendant/context.ts
lib/landing/ai-attendant/provider.ts
lib/landing/ai-attendant/guardrails.ts
lib/landing/ai-attendant/fallback.ts
lib/landing/ai-attendant/summarize.ts
lib/landing/ai-attendant/conversion.ts
lib/landing/ai-attendant/channels.ts
lib/landing/ai-attendant/session-store.ts
lib/landing/ai-attendant/whatsapp.ts
```

### Custom Agent Diagnostic Report Contract

Detailed behavior is defined in [custom-agent-diagnostic-report.md](./custom-agent-diagnostic-report.md).

The diagnostic route is not a chat route. It receives one free-text operation description and returns a structured report:

```ts
type CustomAgentDiagnosticResponse = {
  reportId: string
  classification: 'mapped_solution' | 'custom_agent' | 'mixed_solution' | 'unclear'
  confidence: 'high' | 'medium' | 'low'
  sections: Array<{
    id: 'request_summary' | 'studio_impact' | 'taliya_fit' | 'recommended_path' | 'next_step'
    title: string
    body: string
  }>
  mappedAgentIds: Array<'atendimento' | 'agenda' | 'vendas' | 'financeiro' | 'retencao' | 'gestao' | 'historico_evolucao'>
  customAgent?: {
    label: string
    operationSummary: string
    missingScopeQuestions: string[]
  }
  recommendedPlanId?: string
  ctas: Array<{
    id: 'talk_to_consultor' | 'guided_demo' | 'continue_whatsapp' | 'request_custom_agent_proposal'
    destination: 'open_consultor' | 'configured_guided_demo' | 'configured_whatsapp'
    contextVariant: 'diagnostic_existing_solution' | 'diagnostic_custom_agent' | 'diagnostic_mixed_solution' | 'diagnostic_unclear'
  }>
}
```

Rules:

- `mapped_solution` routes to consultor/demo/WhatsApp using the normal SaaS funnel.
- `custom_agent` routes to consultor/WhatsApp in proposal mode and asks for operation scope/contact.
- `mixed_solution` separates SaaS-covered work from custom work.
- `unclear` asks for more detail.
- No diagnostic report can route directly to checkout.

### Request Contract

```ts
type AiAttendantRequest = {
  session: {
    sessionId: string
    channel: 'web' | 'whatsapp'
    channelSessionId?: string
    niche: string
    sourcePage: string
    campaignStage: string
    publicOfferMode: string
    messages: Array<{
      role: 'user' | 'assistant'
      content: string
    }>
    selectedPainIds?: string[]
    recommendedAgentIds?: string[]
    qualificationDraft?: Record<string, string>
    externalContact?: {
      type: 'whatsapp'
      phone?: string
      providerContactId?: string
      optedOut?: boolean
    }
  }
  userMessage?: string
  quickReplyId?: string
  pageSignals?: {
    selectedPainId?: string
    selectedAgentId?: string
    calculatorEstimate?: number
  }
}
```

### WhatsApp Webhook Contract

Provider-specific payloads must be converted into this internal shape before the AI attendant core runs:

```ts
type WhatsAppInboundTurn = {
  provider: string
  providerMessageId: string
  providerContactId: string
  fromPhone?: string
  text: string
  occurredAt: string
  rawSignatureVerified: boolean
}
```

The route must acknowledge the provider according to provider requirements after persisting the inbound turn and must either send the reply within the request or enqueue a safe provider-send operation.

### Response Contract

```ts
type AiAttendantResponse = {
  assistantMessages: Array<{
    id: string
    role: 'assistant'
    content: string
    intent:
      | 'answer_question'
      | 'pain_detected'
      | 'agent_explained'
      | 'qualification_started'
      | 'guided_demo'
      | 'view_plans'
      | 'plan_recommendation'
      | 'checkout_intent'
      | 'analysis_handoff'
      | 'human_whatsapp_handoff'
      | 'diagnostic_handoff'
      | 'guardrail'
      | 'fallback'
  }>
  capturedPainIds: string[]
  recommendedAgentIds: Array<
    | 'atendimento'
    | 'agenda'
    | 'vendas'
    | 'financeiro'
    | 'retencao'
    | 'gestao'
    | 'historico_evolucao'
  >
  nextQuestion?: string
  conversionPath?:
    | 'guided_demo'
    | 'view_plans'
    | 'plan_recommendation'
    | 'checkout_intent'
    | 'subscription_intent'
    | 'analysis_request'
    | 'human_whatsapp_assist'
    | 'custom_agent_follow_up'
    | 'custom_agent_diagnostic_mapped'
    | 'mixed_subscription_plus_custom'
    | 'custom_agent_diagnostic_unclear'
  subscription?: {
    planId?: string
    checkoutUrl?: string
    ctaLabel: string
  }
  shouldOfferDiagnostic: boolean
  qualificationPatch?: Record<string, string>
  handoff?: ConversionHandoff
  guardrailDecision: {
    category:
      | 'allowed'
      | 'prompt_injection'
      | 'unsupported_claim'
      | 'sensitive_data'
      | 'off_topic'
      | 'abuse'
      | 'provider_failure'
      | 'invalid_model_output'
    action: 'respond' | 'refuse' | 'redirect' | 'fallback' | 'handoff'
    reason: string
  }
  channelActions?: Array<
    | { type: 'send_whatsapp_reply'; providerMessageId: string; status: 'sent' | 'queued' | 'failed'; reason?: string }
    | { type: 'store_session'; status: 'stored' | 'failed'; reason?: string }
  >
}
```

## AI Runtime Layer

### Provider Choice

Use OpenAI through the server-side provider abstraction.

Recommended baseline:

```text
OpenAI Responses API
model: gpt-5.4-mini
structured output: JSON schema / Zod
```

Use `gpt-5.5` only when we intentionally want higher reasoning quality for more complex qualification or objection handling.

### Commercial Configuration Source

The AI runtime must not hardcode plan names, prices, discounts, checkout URLs or WhatsApp assistance destinations.

On each turn, the context builder reads the current trusted system configuration and includes only approved commercial facts:

- available plans;
- configured monthly/annual prices when present;
- recommended plan;
- configured checkout or plan-selection URLs;
- human WhatsApp assistance destination;
- analysis/Dinheiro na Mesa destination;
- public offer mode and campaign stage.

If a value is missing from configuration, the agent says it can help the visitor choose a path or speak with a human, but it does not invent the missing value.

### Files

```text
lib/landing/ai-attendant/provider.ts
```

### Provider Responsibilities

- Read `OPENAI_API_KEY` server-side.
- Set the selected model.
- Send approved context and recent conversation history.
- Request structured output.
- Enforce timeout.
- Convert provider errors into normalized failure codes.
- Never expose raw provider responses to the client.

### Why Not Direct Browser Calls

The browser must never call the model provider directly because it would expose credentials, bypass guardrails and make prompt/control logic public.

## Agent Context Layer

### Files

```text
lib/landing/ai-attendant/context.ts
data/landing/niches/pilates.ts
data/landing/niches/types.ts
```

### Context Included In Each AI Turn

- Role: Atendente IA commercial assistant.
- Goal: answer questions, explain the system, diagnose the studio and conduct the visitor toward guided demo, plan recommendation, checkout, analysis or assisted human close.
- Product positioning: operational AI agents for Pilates studios.
- What the product is not: generic CRM, standalone agenda app, generic chatbot, generic automation or consulting. The approved product framing is operational CRM plus integrated AI agents.
- Seven primary agents and their jobs.
- Agente sob medida only for operations outside the seven primary agent domains; studio-specific rules inside those domains are configuration of the primary agent.
- Supported pains and pain-to-agent mapping.
- Approved CTAs: guided demo, plan recommendation, plans page, checkout after recommendation/explicit intent, analysis/Dinheiro na Mesa and human WhatsApp assistance when requested.
- Public-copy restrictions.
- Conversation history, shortened to recent turns.
- Page signals such as selected pain, selected agent and calculator estimate.
- Channel context such as `web` or `whatsapp`, but only safe contact identifiers and opt-in/opt-out state.

### Context Excluded From AI

- API keys and secrets.
- Internal repository details.
- Internal validation strategy.
- Raw full tracking logs.
- Sensitive student health/payment details.
- Payment credentials, card data, billing documents and untrusted client-side payment state.
- Raw provider webhook payloads unless specifically required for debugging and safely redacted.

## Guardrails Layer

### Input Guardrails

Run before provider call.

Block or redirect:

- prompt injection;
- requests to reveal system prompt or internal instructions;
- very long messages;
- off-topic requests;
- abusive content;
- sensitive student health/payment details.

### Output Guardrails

Run after provider call.

Block, repair or fallback when the model:

- promises guaranteed financial results;
- invents exact price, integration or delivery timeline;
- exposes prohibited public terms;
- recommends agents outside the seven primary agents;
- asks for sensitive data;
- returns invalid structured output;
- gives a long, generic or non-Pilates answer.

## Usage And Cost Control Layer

The attendant must meter and control usage before public traffic.

### Required Controls

- Maximum user message length.
- Maximum recent history sent to the AI provider.
- Per-session rate limit for web.
- Per-contact rate limit for WhatsApp.
- Daily AI request cap for the landing/niche.
- Provider request timeout.
- Fallback/degraded mode when limits are exceeded.
- Server-side usage event per AI call and WhatsApp send attempt.
- Kill switch to disable live AI while leaving guided fallback/CTA paths available.

### Usage Events

Record safe server-side usage metadata:

- `sessionId`
- `channel`
- `niche`
- provider/model
- request status
- latency
- input/output token counts when available
- estimated cost when available
- fallback/guardrail category
- idempotency key for WhatsApp retries

Do not store full raw transcripts in usage logs by default.

### Files

```text
lib/landing/ai-attendant/guardrails.ts
lib/landing/ai-attendant/fallback.ts
```

## Fallback Layer

Fallback is not the main agent. It is degraded behavior.

Use fallback only when:

- provider key is missing in runtime;
- provider request times out;
- provider returns an error;
- model output fails schema validation;
- guardrails block the input or output.

Fallback response should:

- stay short;
- return to supported studio pains;
- offer quick replies;
- preserve the guided demo, plan recommendation, checkout, analysis or human assistance CTA;
- emit `floating_agent_fallback`.

## Tracking Layer

### Files

```text
lib/landing/tracking.ts
components/landing/shared/FloatingAiAttendant.tsx
app/api/landing/ai-attendant/route.ts
app/api/landing/ai-attendant/whatsapp/route.ts
```

### Frontend Events

- `floating_agent_opened`
- `floating_agent_closed`
- `floating_agent_message_sent`
- `floating_agent_quick_reply_clicked`
- `floating_agent_diagnostic_handoff`

### Server/Agent Events

- `floating_agent_pain_captured`
- `floating_agent_agent_recommended`
- `floating_agent_qualification_started`
- `floating_agent_guided_demo_cta`
- `floating_agent_plan_recommendation_cta`
- `floating_agent_checkout_cta`
- `floating_agent_analysis_handoff`
- `floating_agent_human_whatsapp_handoff`
- `floating_agent_fallback`
- `floating_agent_whatsapp_inbound`
- `floating_agent_whatsapp_reply_sent`
- `floating_agent_whatsapp_delivery_failed`
- `custom_agent_diagnostic_started`
- `custom_agent_diagnostic_submitted`
- `custom_agent_diagnostic_generated`
- `custom_agent_diagnostic_cta_clicked`
- `custom_agent_diagnostic_failed`

### Tracking Rules

- Every event includes `niche`, `sourcePage`, `campaignStage` and `publicOfferMode`.
- Every event includes `channel`.
- Metadata uses IDs/categories, not full raw transcripts by default.
- Fallback and guardrail events include category and action.
- WhatsApp metadata uses provider message IDs and safe contact identifiers, not full raw provider payloads.
- Custom-agent diagnostic metadata includes report classification, context variant, mapped agent IDs and safe summary, not full raw text by default.

## n8n Automation Layer

n8n is a post-handoff automation layer, not the chat brain.

Detailed responsibilities live in [n8n-automation-map.md](./n8n-automation-map.md).

Use n8n for:

- conversion handoff ingestion from web or WhatsApp;
- lead record creation/update;
- high-intent alerts;
- internal follow-up tasks;
- daily lead digest;
- safety/fallback alerts when needed.

Do not use n8n for:

- real-time chat responses;
- primary conversation state;
- WhatsApp webhook idempotency;
- live AI provider calls for every message;
- primary guardrails.

## Conversion Handoff Layer

### Trigger

The agent creates a handoff when:

- visitor asks for a demo or wants to see the product working;
- visitor asks to see/compare plans;
- visitor asks to subscribe or how to start now;
- visitor asks for diagnostic;
- visitor asks to talk to a human before subscribing;
- visitor asks how to start;
- visitor provides enough qualification context;
- visitor clicks a conversion CTA inside the chat.
- visitor generates or clicks a CTA from a custom-agent diagnostic report.

### Payload

```ts
type ConversionHandoff = {
  sessionId: string
  channel: 'web' | 'whatsapp'
  channelSessionId?: string
  niche: string
  sourcePage: string
  campaignStage: string
  publicOfferMode: string
  conversionPath:
    | 'guided_demo'
    | 'view_plans'
    | 'plan_recommendation'
    | 'checkout_intent'
    | 'subscription_intent'
    | 'analysis_request'
    | 'human_whatsapp_assist'
    | 'custom_agent_follow_up'
  summary: string
  selectedPainIds: string[]
  recommendedAgentIds: string[]
  qualification: {
    name?: string
    whatsapp?: string
    studioName?: string
    cityState?: string
    activeStudentsRange?: string
    biggestPain?: string
    currentSystem?: string
    customRoutine?: string
  }
  calculatorEstimate?: number
  destination:
    | 'checkout'
    | 'plan_selection'
    | 'diagnostic_form'
    | 'whatsapp_follow_up'
    | 'custom_agent_follow_up'
  checkout?: {
    planId?: string
    url?: string
  }
}
```

### Payment Boundary

The attendant may route a visitor to plan selection or checkout, but it must not:

- collect card data or payment credentials;
- trust client-reported payment state;
- say the subscription is active before trusted billing confirmation;
- grant product access or entitlements.

Full checkout, payment webhooks, entitlement activation, upgrades, downgrades, cancellation and failed-payment handling belong in a focused billing/subscription feature spec.

## Implementation Order

1. Define config/types for the attendant.
2. Create server schema, channel contract and web route.
3. Build context, provider, guardrails and fallback.
4. Build floating UI shell.
5. Connect UI to route.
6. Add WhatsApp webhook route, provider adapter, idempotency and session store.
7. Render recommendations and guided demo / plan recommendation / checkout / analysis / human WhatsApp handoff states.
8. Add channel-aware tracking.
9. Add n8n webhook sender for handoff/high-intent/safety events.
10. Add eval fixtures and run manual scenarios for both channels.

## Non-Goals For V1

- Sending proactive WhatsApp broadcasts, campaigns or cold outbound messages.
- Multi-tenant authentication.
- Billing or paid usage metering.
- Implementing payment checkout, billing webhooks, invoices, entitlements or customer portal inside the attendant feature.
- Multi-agent orchestration inside the attendant.
- Voice calls.
- Full CRM/agenda integrations.

## Open Decisions

- Exact OpenAI model default can be set in implementation via `AI_ATTENDANT_MODEL`, with `gpt-5.4-mini` as the planned default.
- WhatsApp provider decision is closed for v1: official Meta WhatsApp Cloud API.
- The production persistence backend decision is Postgres as primary durable storage, with Redis/KV optional for short-lived counters/locks. It cannot be browser-only or in-memory state.
- The exact production cost caps must be selected before public traffic, but the implementation must include rate limit, daily cap, timeout, fallback and usage logging hooks.
