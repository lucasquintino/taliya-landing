# UI Contract: Premium Multi-Niche Landing Page System

## Page Contract

Route `/pilates` renders the Pilates NicheLanding configuration through the shared landing renderer.

Route `/pilates/planos` renders the dedicated Pilates plans page using the same configured pricing and subscription data.

Required order:
1. Header
2. HeroSection
3. IntentSelectorSection
4. ProblemDiagnosisSection
5. MoneyCalculatorSection
6. AgentsDemoSection
7. HowItWorksSection
8. CoverageSection
9. NicheSpecificSection
10. CustomAgentSection
11. HumanControlSection
12. PlansSection
13. AssistedConversionSection
14. FAQSection
15. FinalCTASection
16. FooterSection

## Interaction Contract

- Hero CTA click emits `cta_click`.
- Intent selection emits `pain_selected` and updates conversation mockup.
- Diagnosis mode toggle updates cards without page navigation.
- Calculator first interaction emits `calculator_started`.
- Calculator changes emit `calculator_result_updated`.
- Agent selection emits `agent_selected` and updates workspace mockup.
- Plan/subscription CTA emits `plan_cta_clicked` with `planId`, `planName`, `billingPeriod`, `priceBRL`, `sourceSection`, `niche`, `campaignStage` and `publicOfferMode`.
- Assisted conversion form focus emits `form_started` once.
- Assisted conversion form submit emits `form_submitted` with automatic context.
- Human WhatsApp CTA emits `human_whatsapp_clicked` and includes selected/interested plan when the click comes from a plan card.
- Custom-agent CTA emits `custom_agent_interest_clicked`.
- Custom-agent diagnostic submit emits `custom_agent_diagnostic_submitted`.
- Custom-agent diagnostic result emits `custom_agent_diagnostic_generated` with classification and safe summary.
- Custom-agent diagnostic CTA emits `custom_agent_diagnostic_cta_clicked` with classification, context variant and destination.
- Plans page view emits `plans_page_viewed`.
- Plans comparison section emits `plans_comparison_viewed` when visible or opened.
- Plans page FAQ open emits `faq_item_opened`.
- Landing FAQ item open emits `faq_item_opened` with `sourceSection=faq`.
- Landing FAQ final doubt CTA emits `faq_doubt_cta_clicked` and opens the floating consultor with `entryPath=widget` and `sourceSection=faq_doubt_cta`.

## Pricing Contract

PlansSection and `/pilates/planos` receive configured pricing data and render four Pilates plans:

1. Base: R$ 197/mes, 0 active AI agents.
2. 1 Agente: R$ 497/mes, 1 selected primary agent.
3. 3 Agentes: R$ 897/mes, 3 selected primary agents.
4. 7 Agentes: R$ 1.497/mes and marked as recommended, all seven primary agents.

Each plan card renders:

- plan name and price
- who it is for
- included agent coverage
- WhatsApp availability
- setup/onboarding expectation
- usage boundary/hard cap
- consultor-first CTA
- secondary human assistance CTA

Annual pricing may render only when configured for all fields required by the pricing model.

Plan URLs must come from trusted niche configuration. The UI must not render arbitrary checkout URLs from user input, model output, query strings or form payloads.

## Plans Page Contract

`/pilates/planos` renders:

- focused page hero;
- four plan cards;
- recommended-plan explanation;
- comparison table;
- plan-fit guidance;
- plan FAQ;
- secondary human WhatsApp assistance;
- final recommended-plan CTA.

The page must be reachable from `/pilates`, floating attendant plan-comparison actions and direct URL access.

On mobile, the comparison table may become tabs or accordions, but it must not create horizontal body overflow.

Viewing/comparing plans must not call checkout. Checkout starts only from explicit plan CTA click.

## Landing FAQ Contract

The `/pilates` landing FAQ renders at most 8 visible high-impact questions:

1. O que a Taliya faz?
2. Isso substitui minha equipe?
3. Quais agentes existem?
4. Qual plano faz sentido para meu studio?
5. Como funciona o WhatsApp?
6. Como e o setup?
7. Tem garantia ou cancelamento?
8. E se eu precisar de um agente sob medida?

The FAQ must end with a "ficou alguma duvida?" CTA. This CTA must reuse the normal floating widget consultor behavior, pass `sourceSection=faq_doubt_cta`, and must not assume the visitor wants checkout.

## Subscription Flow Contract

Direct path:

1. User selects a plan.
2. UI emits `plan_cta_clicked`.
3. UI navigates to the trusted checkout/subscription URL for that plan.
4. UI does not collect payment data and does not show active subscription state.

Assisted path:

1. User clicks "falar com humano" or chooses analysis.
2. UI emits the relevant event with selected/interested plan when available.
3. UI opens trusted WhatsApp/handoff path or submits assisted-conversion form.
4. Final purchase still happens through trusted subscription/checkout.

Custom-agent diagnostic path:

1. User describes an operation in the Agente sob medida diagnostic textarea.
2. UI sends the description to the Spec 2 diagnostic report route.
3. UI renders a structured report with classification `mapped_solution`, `custom_agent`, `mixed_solution` or `unclear`.
4. If classification is `mapped_solution`, CTAs open consultor, guided demo when ready/gated or WhatsApp with existing-solution diagnostic context.
5. If classification is `custom_agent`, CTAs open consultor or WhatsApp with custom-agent proposal context.
6. If classification is `mixed_solution`, CTAs preserve both the SaaS-covered and custom-agent context.
7. The diagnostic path does not navigate directly to checkout.

## Visual Contract

- Hero does not include the intent selector.
- Intent selector is the first block after hero.
- Diagnosis block uses `Sem agentes` and `Com agentes` modes.
- Dinheiro na Mesa uses a controls + estimate panel composition.
- Agents block only contains the agent selector/workspace pattern.
- Consultor-led diagnosis/recommendation is the primary conversion path; plans/subscription is the downstream decision section.
- 7 Agentes is visually recommended without making other plans look disabled.
- Analysis and human WhatsApp assistance are secondary conversion paths.
- Agente sob medida diagnostic is a report-style sales block, not a second chat UI.
- Standalone agent-workflow section is absent.
- Public UI uses "painel" instead of the prohibited public term "dashboard".
