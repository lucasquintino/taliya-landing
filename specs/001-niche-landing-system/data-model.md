# Data Model: Premium Multi-Niche Landing Page System

## NicheLanding

Fields:
- `niche`: stable slug, e.g. `pilates`
- `route`: public route, e.g. `/pilates`
- `brand`: visitor-facing brand name
- `metadata`: title and description
- `tracking`: TrackingContext
- `hero`: hero content
- `intentSelector`: pain options and conversation variants
- `problemDiagnosis`: mode cards for `Sem agentes` and `Com agentes`
- `calculator`: inputs, defaults, labels and assumptions
- `agents`: seven primary agents
- `visualAssets`: conversation, SaaS mockup and illustration mapping
- `pricingPlans`: public plan packaging, prices and recommended plan
- `entryPaths`: CTA entry-path metadata for widget, consultor CTA, WhatsApp CTA, guided demo, custom-agent diagnostic and FAQ doubt CTA
- `guidedDemo`: guided real-SaaS demonstration page configuration
- `planDisplayGates`: conditions that allow routing to `/pilates/planos`
- `checkoutGates`: conditions that allow checkout to be offered
- `riskReducers`: high-ticket reassurance points that must be visible or reachable before checkout
- `plansPage`: dedicated plan-comparison page configuration
- `subscription`: plan/subscription CTA destinations, labels and flow metadata
- `assistedConversion`: analysis and human WhatsApp assistance form fields/options
- `faq`: objections and answers

Validation:
- `niche` and `route` are required.
- `/pilates` config must include all required sections.
- Public copy must avoid prohibited terms.

## TrackingContext

Fields:
- `niche`
- `sourcePage`
- `campaignStage`
- `publicOfferMode`
- `internalGoal`

Validation:
- Current Pilates campaign uses `campaignStage: "commercial"` internally.
- Public UI uses consultor-led SaaS subscription framing.

## EntryPath

Fields:
- `id`: `widget`, `consultor_cta`, `whatsapp_cta`, `guided_demo`, `custom_agent_diagnostic` or `faq_doubt_cta`
- `label`
- `sourceSection`
- `intentLevel`
- `openingTone`
- `firstMessageGoal`
- `allowedNextSteps`
- `trackingMetadata`

Validation:
- `/pilates` must define all six entry paths.
- Entry path metadata must be passed to the consultor/Atendente IA.
- Widget entry must not assume purchase intent.
- Consultor and WhatsApp entries may use stronger commercial copy without pressure.
- Guided demo entry must preserve selected scenario and completed-step context when available.
- Custom-agent diagnostic entry must preserve report classification and context variant.
- FAQ doubt CTA may reuse `entryPath=widget`, but must pass `sourceSection=faq_doubt_cta`.

## GuidedDemo

Fields:
- `route`: canonical route, e.g. `/pilates/demonstracao`
- `title`
- `scenarios`
- `steps`: studio setup preview, agent setup preview, live demo operation, agent action, system record, human control and consultor bridge
- `demoEnvironment`: real SaaS demo workspace/sandbox reference
- `controls`: pause, next, previous, restart and scenario switch
- `consultorLayer`
- `handoffContext`

Validation:
- Must use the real SaaS demo environment with approved demo data.
- Must not be launched as a fake/static substitute before the SaaS supports the demonstrated workflows.
- Must not imply the visitor's real studio is already configured.
- Must not make checkout the default final action.
- Must hand selected scenario, selected pain and completed steps back to the consultor.

## PlanDisplayGate

Fields:
- `reason`: explicit plan request, plan-related CTA, enough diagnosis, guided-demo recommendation/completion, visitor insistence or strong buying intent
- `requiredContext`
- `destination`: trusted plans route
- `trackingEvent`

Validation:
- `/pilates/planos` should not be the default first destination for cold visitors.
- Plan display gate metadata must not determine price or entitlement.

## CheckoutGate

Fields:
- `reason`: explicit buy intent, confirmed recommendation, plans-page checkout CTA or operator-assisted close
- `requiredContext`
- `trustedCheckoutSource`
- `trackingEvent`

Validation:
- Checkout must not be offered as the default final action of `/pilates` or `/pilates/demonstracao`.
- Checkout destination must come from trusted configuration or server-side billing checkout creation.
- Checkout gate metadata must never be proof of paid access.

## RiskReducer

Fields:
- `id`
- `question`
- `approvedAnswer`
- `requiredBeforeCheckoutWhenRelevant`

Required risk reducers:
- post-payment next step
- studio-owned WhatsApp
- setup/onboarding help
- human control
- plan changes when configured
- hard usage caps
- cancellation/contract when configured
- payment-data safety

## PainOption

Fields:
- `id`
- `chip`
- `title`
- `description`
- `conversation`
- `result`

Relationships:
- Used by IntentSelectorSection and conversation mockups.
- Selection emits `pain_selected`.

## ProblemMode

Fields:
- `mode`: `sem_agentes` or `com_agentes`
- `label`: public toggle label
- `cards`: list of problem/outcome cards
- `accent`: visual treatment

Relationships:
- Used by ProblemDiagnosisSection.

## MoneyCalculatorInput

Fields:
- active students
- average monthly fee
- weekly absences/cancellations
- weekly open classes
- monthly overdue payments
- plans expiring in 30 days
- inactive students in 30 days
- monthly interested people
- trial classes without closing
- manual hours per week

Relationships:
- Used by MoneyCalculatorSection and `lib/landing/money-calculator.ts`.

## Agent

Fields:
- `id`
- `name`
- `pain`
- `action`
- `workspaceMockup`
- `conversationMockup`
- `result`
- `accent`

Validation:
- Pilates must include exactly Atendimento, Agenda, Vendas, Financeiro, Retencao, Gestao, Historico/Evolucao.
- Agente sob medida is not included in this list.

## VisualAsset

Fields:
- `type`: conversation, saas_screen, flow, illustration
- `section`
- `variant`
- `contentSource`
- `purpose`

Relationships:
- Supports Hero, IntentSelector, MoneyCalculator, AgentsDemo, HowItWorks, Coverage, NicheSpecific, CustomAgent, HumanControl and Plans.

## SubscriptionCTA

Fields:
- `planId`
- `planName`
- `billingPeriod`: monthly or annual
- `priceBRL`
- `ctaLabel`
- `trustedCheckoutUrl` or trusted plan-selection URL
- `sourceSection`
- tracking context fields

Validation:
- URL must come from trusted niche configuration.
- Must not collect card data inside the landing form.
- Subscription activation is not inferred from CTA click.
- CTA payload must never be used as proof of paid status.

## PlansPage

Fields:
- `route`: canonical route, e.g. `/pilates/planos`
- `title`
- `subtitle`
- `heroCtas`
- `comparisonRows`
- `fitGuidance`
- `faq`
- `recommendedPlanExplanation`
- `secondaryHumanAssistanceCta`
- `finalCta`

Relationships:
- Uses the same `pricingPlans` and `subscription` configuration as `/pilates`.
- Receives plan-comparison traffic from the consultor-led flow, explicit plan-comparison intent and guided-demo recommendation/completion.
- Sends explicit plan selections to the trusted checkout flow.

Validation:
- Route must be stable and configured.
- Must not duplicate hardcoded prices or checkout URLs.
- Must not create checkout for view-only comparison.
- Must not mark a subscription active from plan comparison or CTA click.

## PricingPlan

Fields:
- `id`: `base`, `one_agent`, `three_agents` or `seven_agents`
- `name`
- `monthlyPriceBRL`
- `annualPriceBRL` when annual billing is configured
- `annualDiscountLabel` when annual billing is configured
- `isRecommended`
- `bestFor`
- `positioning`
- `includedAgents`
- `whatsappAvailability`
- `setupExpectation`
- `usageBoundary`
- `primaryCta`
- `secondaryHumanCta`
- `trustedCheckoutUrl`

Validation:
- Pilates must include exactly four public plans: Base R$ 197/mes, 1 Agente R$ 497/mes, 3 Agentes R$ 897/mes and 7 Agentes R$ 1.497/mes.
- Only one plan should be marked recommended; Pilates default is `seven_agents`.
- Annual billing fields are optional, but if any annual discount is shown all annual fields must be configured.
- Prices must come from trusted configuration, not component text.
- Plan display must not imply active subscription before checkout confirmation.

## SubscriptionIntent

Fields:
- `planId`
- `billingPeriod`
- `priceBRL`
- `niche`
- `sourcePage`
- `sourceSection`
- `campaignStage`
- `publicOfferMode`
- `createdAt`

Validation:
- Represents interest or checkout navigation only.
- Does not grant access, onboarding, entitlements or active subscription state.
- If persisted later, must be superseded by trusted billing events.

## AssistedConversionSubmission

Fields:
- name
- WhatsApp
- studio name
- city/state
- active students
- biggest pain
- current system usage
- custom routine
- preferred next step: analysis, human WhatsApp assistance or custom-agent follow-up
- selected or interested plan when available
- tracking context fields

Validation:
- Required user fields cannot be empty.
- Automatic context fields are always included.

## CustomAgentDiagnosticBlock

Fields:

- `title`
- `subtitle`
- `textareaPlaceholder`
- `examplePrompts`
- `submitCta`
- `reportResult`
- `mappedSolutionCtas`
- `customAgentCtas`
- `mixedSolutionCtas`
- `unclearCtas`

Relationships:

- Uses the same seven primary agent configuration as the landing and Atendente IA.
- Uses the same guided-demo readiness and WhatsApp destination configuration as the consultor.
- Sends report-generation requests to the Spec 2 custom-agent diagnostic route.
- Carries report context into consultor, guided demo or WhatsApp CTAs.

Validation:

- Must use a real textarea/input, not placeholder-only UI.
- Must render a structured report result, not a normal chat thread.
- Must classify as `mapped_solution`, `custom_agent`, `mixed_solution` or `unclear`.
- Must not route directly to checkout.
- Must not imply Agente sob medida is included in public plans.
- Must track classification and CTA selection without unnecessary raw-text storage.
