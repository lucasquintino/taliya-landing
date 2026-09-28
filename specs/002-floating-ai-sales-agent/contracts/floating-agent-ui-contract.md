# Floating AI Attendant UI And Conversation Contract

## Purpose

Define the contract between niche configuration, floating attendant UI, WhatsApp channel, conversation engine, required live AI route and landing tracking.

## Component Contract

### FloatingAiAttendant

Inputs:

- `config: FloatingAgentConfig`
- `landingContext: { niche, sourcePage, campaignStage, publicOfferMode }`
- `pageSignals?: { selectedPainId?, selectedAgentId?, calculatorEstimate? }`
- `onHandoff(payload: ConversionHandoff): void`
- `onTrack(event: FloatingAgentTrackingEvent): void`

Behavior:

- Renders the compact floating button when minimized.
- Opens the chat panel without page navigation.
- Keeps message state isolated from the rest of the landing.
- Emits tracking for open, close, quick replies, messages, recommendations, qualification, guided demo CTA, plan recommendation CTA, checkout CTA and handoff.
- Calls `onHandoff` only after the visitor chooses guided demo, plan comparison, checkout after recommendation, CRM-first diagnostic next step, analysis, human WhatsApp assistance or custom-agent follow-up.
- For human WhatsApp assistance, calls `onHandoff` with a safe assisted-closing summary and trusted destination from config.

## Widget Display Mode Contract

The widget UI must expose deliberate display modes instead of one generic button/panel pair:

| Mode | UI Responsibility |
| --- | --- |
| `minimized_idle` | Default compact entry with clear consultor label, avatar/call icon, availability cue and premium styling. |
| `minimized_attention` | Optional subtle prompt/nudge configured by page context or time on page. |
| `minimized_active` | Minimized state after a conversation exists, with unread/continuation affordance. |
| `opening_transition` | Smooth state change from button to panel with no flicker or duplicate open. |
| `open_desktop` | Desktop panel with header, message list, quick replies, CTA area, input and close/minimize controls. |
| `open_mobile` | Mobile-safe panel/sheet with reachable input, safe-area spacing and keyboard resilience. |
| `typing_loading` | Typing/loading state that prevents duplicate sends while keeping the UI responsive. |
| `error_fallback` | Recoverable provider/guardrail failure state with retry or allowed next step. |
| `handoff_cta` | Structured CTA state for demo, plans, WhatsApp, checkout or custom-agent follow-up. |

Display mode rules:

- The minimized widget must communicate "consultor/atendimento" clearly; it must not be an unexplained phone icon.
- The minimized widget may use restrained attention motion only while closed: subtle desktop nudge/glow, mobile pulse/badge, max three nudges per session, pause after interaction and `prefers-reduced-motion` support.
- The open panel must not show dense legal/privacy paragraphs in the main conversation surface.
- CTA cards/buttons must have clear hierarchy and must not compete with the message input.
- The panel height must respect the page header boundary and short mobile viewport constraints.
- Every mode must have hover/focus/pressed/disabled/loading/error states where relevant.
- Reduced-motion users must receive a non-animated but still clear transition.

Accessibility requirements:

- Button has an accessible name.
- Panel behaves like a dialog-like region with clear close/minimize controls.
- Keyboard users can open, type, send, select quick replies and close.
- Message updates are announced politely.
- Focus is managed when opening and closing.

## Conversation Engine Contract

### Input

```ts
type AiAttendantTurnInput = {
  session: ConversationSession
  channel: 'web' | 'whatsapp'
  userMessage?: string
  quickReplyId?: string
  pageSignals?: {
    selectedPainId?: string
    selectedAgentId?: string
    calculatorEstimate?: number
  }
}
```

### Output

```ts
type AiAttendantTurnOutput = {
  session: ConversationSession
  assistantMessages: AiAttendantMessage[]
  recommendations?: AgentRecommendation[]
  guardrailDecision?: GuardrailDecision
  trackingEvents: FloatingAgentTrackingEvent[]
  handoff?: ConversionHandoff
}
```

Rules:

- One user turn may produce one or two short assistant messages, not long essays.
- Normal free-text user turns must be sent through the server-side AI route.
- If a pain is detected, return recommendations for relevant agents.
- If the visitor asks to subscribe, confirm/recommend the plan when needed and move session toward trusted checkout CTA without collecting payment data in chat.
- If the visitor asks for analysis or human assistance, move session toward qualification and handoff.
- If input is unsafe or off-topic, return a guardrail response and do not call live AI.
- If live AI fails, return a fallback message and preserve the session.

## Required Server Route Contract

Route:

```text
POST /api/landing/ai-attendant
```

Request:

```json
{
  "session": {
    "sessionId": "anon_123",
    "channel": "web",
    "niche": "pilates",
    "sourcePage": "/pilates",
    "campaignStage": "commercial",
    "publicOfferMode": "direct_saas_subscription",
    "messages": []
  },
  "userMessage": "Tenho muitas reposicoes baguncadas",
  "pageSignals": {
    "selectedPainId": "reposicoes",
    "selectedAgentId": "agenda",
    "calculatorEstimate": 4200
  }
}
```

Response:

```json
{
  "assistantMessages": [
    {
      "id": "msg_456",
      "role": "assistant",
      "content": "Reposicoes baguncadas normalmente envolvem Atendimento e Agenda. O Atendimento entende o pedido no WhatsApp e a Agenda sugere horarios possiveis.",
      "intent": "select_pain"
    }
  ],
  "recommendations": [
    {
      "painId": "reposicoes",
      "agentIds": ["atendimento", "agenda"],
      "explanation": "Atendimento entende o pedido e Agenda organiza os encaixes.",
      "exampleAction": "Sugerir dois horarios de reposicao sem troca manual de mensagens.",
      "nextQuestion": "Hoje quem confere se o aluno ainda tem direito a reposicao?"
    }
  ],
  "guardrailDecision": {
    "category": "allowed",
    "action": "respond",
    "reason": "Supported pain"
  }
}
```

Checkout intent response example:

```json
{
  "assistantMessages": [
    {
      "id": "msg_subscribe",
      "role": "assistant",
      "content": "Pelo que voce descreveu, faz sentido comecar pelo plano que coloca Atendimento e Agenda para organizar mensagens e reposicoes. Posso te levar para a assinatura agora.",
      "intent": "checkout_intent"
    }
  ],
  "conversionPath": "checkout_intent",
  "subscription": {
    "planId": "seven_agents",
    "checkoutUrl": "/pilates/assinar?plan=seven_agents",
    "ctaLabel": "Assinar plano"
  },
  "guardrailDecision": {
    "category": "allowed",
    "action": "respond",
    "reason": "High buying intent"
  }
}
```

Error/fallback response:

```json
{
  "assistantMessages": [
    {
      "id": "msg_fallback",
      "role": "assistant",
      "content": "Consigo te ajudar pelo caminho guiado. Qual rotina mais pesa hoje: faltas, reposicoes, mensalidades ou alunos inativos?",
      "intent": "fallback"
    }
  ],
  "guardrailDecision": {
    "category": "provider_failure",
    "action": "fallback",
    "reason": "Live response unavailable"
  }
}
```

Security and privacy:

- The route must validate request shape and message length.
- The route must not accept arbitrary system instructions from the browser.
- Provider secrets stay server-side.
- Sensitive details should be redacted or not sent to the provider unless necessary.
- Checkout URLs and plan IDs must come from trusted configuration, not model-generated arbitrary URLs.
- Plan names, prices, recommended plan and checkout URLs must come from trusted system configuration shared with the landing.
- If price configuration is missing, the route must not invent a price; it should offer analysis or human WhatsApp assistance.
- The chat must not collect card data or treat client-reported checkout state as subscription activation.
- The chat UI does not need to label every interaction as AI, but it must not impersonate a named human.
- AI/privacy transparency must be available before contact capture.
- Contact capture must explain purpose and show/link privacy consent copy before submission.
- n8n/handoff payloads use safe summaries and structured metadata by default, not full raw transcripts.

## WhatsApp Channel Contract

Route:

```text
POST /api/landing/ai-attendant/whatsapp
```

Provider-specific webhook payloads are not passed directly into the agent. The route must verify the provider request and normalize the inbound message into this internal shape:

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

The normalized AI request uses the same server-side route/core contract:

```json
{
  "session": {
    "sessionId": "wa_session_123",
    "channel": "whatsapp",
    "channelSessionId": "wa_contact_456",
    "niche": "pilates",
    "sourcePage": "whatsapp",
    "campaignStage": "commercial",
    "publicOfferMode": "direct_saas_subscription",
    "messages": [],
    "externalContact": {
      "type": "whatsapp",
      "phone": "+55 11 99999-9999",
      "providerContactId": "wa_contact_456",
      "optedOut": false
    }
  },
  "userMessage": "Quero um agente de marketing para meu studio"
}
```

Required behavior:

- Use the official Meta WhatsApp Cloud API adapter in v1.
- Verify provider signature, token or shared secret before processing.
- Deduplicate by `providerMessageId` before calling the AI layer.
- Persist WhatsApp session state before sending a reply.
- Reuse the same AI context, guardrails, pain mapping, qualification and handoff rules as the web widget.
- Send automatic replies only for inbound or explicitly opted-in conversations.
- Stop automated replies when the contact opts out.
- Record provider delivery failure without breaking the web widget.

WhatsApp replies must use a provider adapter, not direct model/browser calls:

```ts
type WhatsAppReplyAction = {
  provider: string
  channelSessionId: string
  replyToProviderMessageId: string
  content: string
  idempotencyKey: string
}
```

## Custom Agent Diagnostic Report Contract

Route:

```text
POST /api/landing/custom-agent-diagnostic
```

This route supports the Agente sob medida landing block. It is a report generator, not the chat route.

Request:

```json
{
  "sessionId": "anon_123",
  "niche": "pilates",
  "sourcePage": "/pilates",
  "sourceSection": "custom_agent_diagnostic",
  "campaignStage": "commercial",
  "publicOfferMode": "direct_saas_subscription",
  "description": "Quero um agente de marketing que crie campanhas para alunos inativos"
}
```

Response:

```json
{
  "reportId": "diag_123",
  "classification": "custom_agent",
  "confidence": "high",
  "title": "Diagnostico de agente sob medida",
  "sections": [
    {
      "id": "request_summary",
      "title": "O que voce quer automatizar",
      "body": "Voce quer um agente voltado a marketing e campanhas para alunos inativos."
    },
    {
      "id": "taliya_fit",
      "title": "Isso ja existe na Taliya?",
      "body": "A Taliya ja cobre retencao e alunos inativos, mas um agente especifico de marketing entra como Agente sob medida."
    }
  ],
  "mappedAgentIds": ["retencao"],
  "customAgent": {
    "label": "Agente de Marketing",
    "operationSummary": "Campanhas e comunicacao para alunos inativos",
    "missingScopeQuestions": [
      "Quais canais o agente deve usar?",
      "Ele apenas sugere campanhas ou tambem publica/envia?"
    ]
  },
  "ctas": [
    {
      "id": "request_custom_agent_proposal",
      "label": "Solicitar proposta de agente sob medida",
      "destination": "open_consultor",
      "contextVariant": "diagnostic_custom_agent"
    },
    {
      "id": "continue_whatsapp",
      "label": "Continuar pelo WhatsApp",
      "destination": "configured_whatsapp",
      "contextVariant": "diagnostic_custom_agent"
    }
  ],
  "leadEffect": {
    "shouldCreateOrUpdateLead": true,
    "conversionPath": "custom_agent_follow_up",
    "priority": "media",
    "safeSummary": "Visitante quer agente de marketing sob medida para campanhas de alunos inativos."
  }
}
```

Rules:

- `mapped_solution` report CTAs use `diagnostic_existing_solution` and route to consultor, guided demo when ready/gated or WhatsApp with SaaS sales context.
- `custom_agent` report CTAs use `diagnostic_custom_agent` and route to consultor/WhatsApp to collect more scope and contact.
- `mixed_solution` report CTAs use `diagnostic_mixed_solution` and offer both SaaS and custom proposal paths.
- `unclear` report CTAs use `diagnostic_unclear` and ask for missing details.
- No report CTA can route straight to checkout.

## Tracking Contract

Every event uses the existing landing context shape:

```ts
type FloatingAgentTrackingEvent = {
  niche: string
  sourcePage: string
  campaignStage: string
  publicOfferMode: string
  eventName:
    | 'floating_agent_opened'
    | 'floating_agent_closed'
    | 'floating_agent_message_sent'
    | 'floating_agent_quick_reply_clicked'
    | 'floating_agent_pain_captured'
    | 'floating_agent_agent_recommended'
    | 'floating_agent_qualification_started'
    | 'floating_agent_guided_demo_cta'
    | 'floating_agent_plan_recommendation_cta'
    | 'floating_agent_checkout_cta'
    | 'floating_agent_analysis_handoff'
    | 'floating_agent_human_whatsapp_handoff'
    | 'floating_agent_diagnostic_handoff'
    | 'floating_agent_fallback'
    | 'floating_agent_whatsapp_inbound'
    | 'floating_agent_whatsapp_reply_sent'
    | 'floating_agent_whatsapp_delivery_failed'
    | 'custom_agent_diagnostic_started'
    | 'custom_agent_diagnostic_submitted'
    | 'custom_agent_diagnostic_generated'
    | 'custom_agent_diagnostic_cta_clicked'
    | 'custom_agent_diagnostic_failed'
    | 'faq_doubt_cta_clicked'
  metadata: Record<string, unknown>
}
```

Metadata rules:

- Include IDs, categories and counts rather than full raw conversation transcripts by default.
- Include selected pain and recommended agents when available.
- Include handoff destination and qualification completeness for analysis or human assistance handoff.
- Include `sourceSection=faq_doubt_cta` when the visitor opens the agent from the final FAQ CTA.
- Include conversion path for subscription, analysis, human WhatsApp assistance or custom-agent follow-up.
- Include `channel` in metadata or event context.
- Include provider message IDs for WhatsApp idempotency and delivery tracking.
- Include diagnostic report classification, report ID, context variant and mapped agents when the event comes from the custom-agent diagnostic report.
