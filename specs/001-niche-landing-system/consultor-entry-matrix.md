# Consultor Entry Matrix: Pilates Landing

This document defines the public CTA contract for Spec 1. Visual implementation may change, but every CTA must preserve these entry semantics.

## Entry Paths

| Entry | Source section | `entryPath` | First goal | Allowed immediate destination |
| --- | --- | --- | --- | --- |
| Floating widget | `widget` | `widget` | Ask how to help and discover buyer intent | Chat only |
| Falar com consultor | `sales_cta`, `hero_primary`, `final_cta` | `consultor_cta` | Start a stronger commercial conversation and diagnose the studio before plan/checkout | Chat; WhatsApp only if visitor chooses |
| Continuar no WhatsApp | `sales_whatsapp`, `plans_whatsapp`, `demo_whatsapp` | `whatsapp_cta` | Continue assisted close in WhatsApp with safe context | Configured WhatsApp destination |
| Ver planos / Comparar planos | `plans_interest`, `plans_page`, `consultor_plan_recommendation` | `plans_page` | Answer/qualify first, then route to `/pilates/planos` when allowed | Consultor first; `/pilates/planos` only after gate |
| Demonstração guiada | `guided_demo` | `guided_demo` | Show proof through the real SaaS demo when ready | `/pilates/demonstracao` only if `guidedDemoReady=true`; otherwise consultor/WhatsApp/product explanation |
| Diagnostico de agente sob medida | `custom_agent_diagnostic` | `custom_agent_diagnostic` | Generate a structured report and classify whether the request is mapped, custom, mixed or unclear | On-page report first; then consultor, WhatsApp or guided demo with diagnostic context |
| FAQ: ficou alguma duvida? | `faq_doubt_cta` | `widget` | Answer the remaining doubt after the visitor read objections/risk reducers | Chat only, reusing the normal widget-style opening with FAQ source context |

## Plan Display Gate

`/pilates/planos` can be offered when at least one is true:

- visitor explicitly asks to see/compare plans;
- consultor has enough context to recommend a plan;
- visitor completed or progressed through the real guided demo;
- visitor has strong buying intent and wants to decide between plans;
- visitor insists on seeing prices after receiving a short consultative answer.

Cold first-viewport CTAs must not send the visitor directly to `/pilates/planos` as the default path.

## Checkout Gate

Checkout can be offered only when at least one is true:

- visitor explicitly says they want to sign/subscribe/pay;
- visitor confirms a recommended plan;
- visitor intentionally clicks a checkout CTA on `/pilates/planos`;
- operator sends a trusted checkout link through the Sales Inbox assisted close.

Checkout URL must come from trusted plan configuration or the future billing route. User input, query strings and model output must never generate checkout URLs.

## Guided Demo Gate

`guidedDemoReady=false` means:

- hide public demo CTAs or reroute them to consultor/WhatsApp/product explanation;
- do not link cold visitors to `/pilates/demonstracao`;
- do not imply a fake/static mockup is the real SaaS demo.

`guidedDemoReady=true` is allowed only when the real SaaS demo environment can show:

- studio setup preview;
- agent setup preview;
- live operation in approved demo data;
- system record/result;
- human control point;
- consultor bridge with selected scenario, pain and completed steps.

## Required Context Payload

Every consultor-opening CTA should pass what is available:

- `sourceSection`;
- `entryPath`;
- `sourcePage`;
- `selectedPainId`;
- `selectedAgentId`;
- `calculatorEstimateBRL`;
- `interestedPlanId`;
- `guidedDemoScenario`;
- `guidedDemoCompleted`;
- `diagnosticReportId`;
- `diagnosticClassification`;
- `diagnosticContextVariant`;
- `diagnosticSelectedCta`;
- `customAgentSummary`;
- `mappedAgentIds`;
- `faqQuestionId`;
- `faqCtaContext`;
- `leadId` or `sessionId` when available.

## FAQ Doubt CTA

The FAQ section must contain at most 8 visible questions. The canonical questions are:

1. O que a Taliya faz?
2. Isso substitui minha equipe?
3. Quais agentes existem?
4. Qual plano faz sentido para meu studio?
5. Como funciona o WhatsApp?
6. Como e o setup?
7. Tem garantia ou cancelamento?
8. E se eu precisar de um agente sob medida?

After the questions, the section must show a final CTA equivalent to "Ficou alguma duvida?". This CTA opens the same web consultor used by the floating widget, passes `sourceSection=faq_doubt_cta`, and starts neutral/helpful instead of assuming checkout intent.

## Risk Reducers Before Checkout

Before checkout is public, the landing/plans/consultor path must make these answers visible or reachable:

- 30-day guarantee for public monthly plans;
- payment data is handled only by the secure billing provider;
- paying studios use their own connected WhatsApp for operational agents;
- setup is self-guided with the consultor/agent and starts in a few minutes after confirmed payment;
- humans can control, review or assume conversations where the product allows;
- AI message usage is hard capped by plan;
- plan changes/cancellation/refund terms appear only from configured terms.
