# Custom Agent Diagnostic Report

## Purpose

Define the report-style diagnostic flow used by the Agente sob medida block on the landing.

This flow is not the floating chat. It is a one-shot diagnostic/report generator that receives a free-text description, classifies whether the request is already covered by Taliya or requires a custom agent, and then routes the visitor into the correct commercial funnel.

Live AI generation for this diagnostic report is future scope. In v1, deterministic/report-style classification is acceptable as long as public copy does not promise a live AI diagnostic and the report remains commercially useful, honest and lead-safe.

The business goal is always a sale:

- sell the SaaS subscription when Taliya already covers the request;
- sell Agente sob medida when the request is outside the mapped SaaS agents;
- sell the SaaS first or alongside a custom discovery when the request is mixed.

## Relationship To The Main Attendant

The report generator may later reuse the same server-side AI provider, guardrails, usage logging, trusted configuration, supported-agent map, n8n dispatch and Sales Inbox lead store as the Atendente IA.

It must not reuse the same free-form chat prompt or response schema without a mode boundary. While live AI report generation is deferred, the deterministic v1 must still keep this route/schema separation so the future AI version can be added without changing the sales funnel contract.

Required separation:

| Area | Atendente IA Chat | Custom Agent Diagnostic Report |
| --- | --- | --- |
| UX | Multi-turn chat | Free-text input plus structured report |
| Route | `/api/landing/ai-attendant` | `/api/landing/custom-agent-diagnostic` |
| Response | Chat messages and conversion metadata | Report sections, classification and CTAs |
| Primary goal | Consultor-led SaaS sale | Classify custom request and route to SaaS or custom-agent sale |
| CTA behavior | Conversation actions | Report CTAs with diagnostic context |

## Request Contract

```ts
type CustomAgentDiagnosticRequest = {
  sessionId: string
  niche: string
  sourcePage: string
  sourceSection: "custom_agent_diagnostic" | "final_diagnostic_cta"
  campaignStage: string
  publicOfferMode: string
  description: string
  pageSignals?: {
    selectedPainId?: string
    selectedAgentId?: string
    calculatorEstimate?: number
  }
}
```

Validation:

- `description` is required and length-limited.
- The browser cannot pass system instructions, arbitrary model options, checkout URLs or WhatsApp destinations.
- The route reads plans, agents, demo readiness, WhatsApp destination and checkout/plan destinations from trusted configuration.
- Sensitive student health data, payment credentials and private customer records are rejected or redacted.

## Response Contract

```ts
type CustomAgentDiagnosticResponse = {
  reportId: string
  classification: "mapped_solution" | "custom_agent" | "mixed_solution" | "unclear"
  confidence: "high" | "medium" | "low"
  title: string
  sections: Array<{
    id: "request_summary" | "studio_impact" | "taliya_fit" | "recommended_path" | "next_step"
    title: string
    body: string
  }>
  mappedAgentIds: Array<
    | "atendimento"
    | "agenda"
    | "vendas"
    | "financeiro"
    | "retencao"
    | "gestao"
    | "historico_evolucao"
  >
  customAgent?: {
    label: string
    operationSummary: string
    missingScopeQuestions: string[]
  }
  recommendedPlanId?: string
  ctas: Array<{
    id:
      | "talk_to_consultor"
      | "guided_demo"
      | "continue_whatsapp"
      | "request_custom_agent_proposal"
    label: string
    destination:
      | "open_consultor"
      | "configured_guided_demo"
      | "configured_whatsapp"
    contextVariant:
      | "diagnostic_existing_solution"
      | "diagnostic_custom_agent"
      | "diagnostic_mixed_solution"
      | "diagnostic_unclear"
  }>
  leadEffect: {
    shouldCreateOrUpdateLead: boolean
    conversionPath:
      | "custom_agent_diagnostic_mapped"
      | "custom_agent_follow_up"
      | "mixed_subscription_plus_custom"
      | "custom_agent_diagnostic_unclear"
    priority: "alta" | "media" | "baixa"
    safeSummary: string
  }
  guardrailDecision: {
    category:
      | "allowed"
      | "prompt_injection"
      | "unsupported_claim"
      | "sensitive_data"
      | "off_topic"
      | "provider_failure"
      | "invalid_model_output"
    action: "respond" | "refuse" | "redirect" | "fallback" | "handoff"
    reason: string
  }
}
```

## Classification Rules

### `mapped_solution`

Use when the request is already solved by one or more of the seven primary agents or by per-studio configuration inside those agents.

Examples:

- "Quero responder alunos no WhatsApp"
- "Quero organizar reposicoes"
- "Quero cobrar mensalidades atrasadas"
- "Quero acompanhar alunos inativos"
- "Quero saber qual plano faz sentido para 120 alunos"

Required report behavior:

- Say that Taliya already covers the request.
- Name the mapped agents.
- Explain the operational impact.
- Recommend consultor-led SaaS funnel.
- Offer CTAs: `Falar com consultor`, `Demo guiada` when ready/gated and `Continuar pelo WhatsApp`.
- Do not sell Agente sob medida as the primary path.

### `custom_agent`

Use when the request is an operation outside the seven mapped domains.

Examples:

- "Quero um agente de marketing"
- "Quero um agente que publique no Instagram"
- "Quero agente para parcerias"
- "Quero agente de estoque"
- "Quero agente para RH interno"

Required report behavior:

- Say that it is Agente sob medida and separate from public plans.
- Summarize the custom operation.
- Ask what the agent should do, where it operates, whether it suggests or executes, which tools/channels are involved and who approves.
- Offer CTAs: `Solicitar proposta de agente sob medida` and `Continuar pelo WhatsApp`.
- The CTA opens consultor/WhatsApp with `contextVariant=diagnostic_custom_agent`.
- The consultor asks for more scope first, then asks for email or cellphone/WhatsApp and says the team will contact the visitor.

### `mixed_solution`

Use when the request includes both mapped SaaS work and an unmapped custom operation.

Example:

- "Quero responder WhatsApp, organizar reposicoes e criar campanhas para alunos inativos no Instagram"

Required report behavior:

- Split the mapped part and the custom part.
- Sell the mapped Taliya agents as the immediate SaaS path.
- Present the custom agent as an expansion/opportunity.
- Offer CTAs for consultor/demo/WhatsApp plus custom-agent proposal.
- Do not imply the custom agent is included in public plans.

### `unclear`

Use when the request is too vague.

Required report behavior:

- Say what can be inferred.
- Ask for the missing context.
- Offer consultor/WhatsApp continuation.
- Do not invent a custom-agent scope.

## CTA Context Variants

### `diagnostic_existing_solution`

Used for `mapped_solution`.

The consultor opening should acknowledge that the diagnostic found an existing Taliya path and continue toward SaaS sale:

```text
Vi seu diagnostico e a boa noticia e que isso ja esta coberto pela Taliya. Pelo que voce descreveu, eu olharia primeiro [agentes]. Quer que eu te mostre o caminho mais indicado para seu studio?
```

Allowed next steps:

- guided demo when ready;
- plan recommendation;
- plans page after gate;
- WhatsApp assisted close;
- checkout only after existing gates.

### `diagnostic_custom_agent`

Used for `custom_agent`.

The consultor opening should ask for custom scope:

```text
Vi seu diagnostico. Esse pedido parece entrar como Agente sob medida, porque nao e um dos agentes operacionais ja mapeados na Taliya. Para montar uma proposta, preciso entender melhor: o agente faria so sugestoes ou tambem executaria acoes por voce?
```

Allowed next steps:

- ask operation scope;
- collect email or cellphone/WhatsApp;
- create/update custom-agent lead;
- operator follow-up;
- WhatsApp continuation.

### `diagnostic_mixed_solution`

Used for `mixed_solution`.

The consultor should sell the mapped SaaS path while preserving custom-agent discovery:

```text
Seu diagnostico tem duas partes: uma ja coberta pela Taliya e outra que entra como Agente sob medida. Eu comecaria resolvendo [mapped agents] e mapearia [custom operation] como expansao. Quer seguir por esse caminho?
```

### `diagnostic_unclear`

Used for `unclear`.

The consultor should ask a clarifying question before recommending anything.

## Lead And Sales Inbox Effects

Every generated report should create or update a lead when at least one of these is true:

- classification is `custom_agent` or `mixed_solution`;
- visitor clicks any report CTA;
- report detects mapped agents and recommends a plan;
- visitor provides contact;
- description contains high-intent buying language.

Sales Inbox lead detail must show:

- report classification;
- report ID;
- original source section;
- mapped agents;
- recommended plan when available;
- custom-agent operation summary when applicable;
- missing scope questions;
- selected CTA;
- safe report summary.

## Tracking Events

Required events:

- `custom_agent_diagnostic_started`
- `custom_agent_diagnostic_submitted`
- `custom_agent_diagnostic_generated`
- `custom_agent_diagnostic_cta_clicked`
- `custom_agent_diagnostic_failed`

Metadata must include:

- `classification`;
- `sourceSection`;
- `mappedAgentIds`;
- `recommendedPlanId` when available;
- `contextVariant`;
- `conversionPath`;
- `reportId`;
- safe summary or category, not full raw text by default.

## Sales Inbox/n8n optional automation Effects

Sales Inbox/Postgres stores or updates the lead after report generation or CTA click. n8n may receive optional alert/digest events when configured.

For `mapped_solution`, the lead uses conversion path `custom_agent_diagnostic_mapped` or continues into `plan_recommendation` once the consultor recommends a plan.

For `custom_agent`, the lead uses conversion path `custom_agent_follow_up`.

For `mixed_solution`, the lead uses conversion path `mixed_subscription_plus_custom`.

For `unclear`, the lead uses conversion path `custom_agent_diagnostic_unclear` only after CTA click/contact/high intent.

## Evals

Before release, evals must verify:

- mapped request routes to existing Taliya agents and SaaS funnel;
- marketing/custom request routes to Agente sob medida and asks for scope/contact;
- mixed request separates mapped and custom parts;
- vague request asks for clarification;
- no report routes directly to checkout;
- demo CTA respects `guidedDemoReady`;
- report output never invents unsupported agents, integrations, prices or timelines;
- report CTAs carry context into consultor/WhatsApp.
