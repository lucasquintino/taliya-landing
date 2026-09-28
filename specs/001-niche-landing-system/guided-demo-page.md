# Guided Demo Page: Pilates SaaS

## Purpose

Define the guided demonstration page for the Pilates vertical SaaS.

Canonical route:

```text
/pilates/demonstracao
```

This page exists so a studio owner can see the real SaaS working before discussing plan price or checkout. It is a trust and education surface that feeds context back into the consultor/Atendente IA. Because the public landing launches only after the SaaS is implemented enough to support the promised product experience, this demo can be part of the public conversion journey once the real demo workspace is ready.

## Product Role

The guided demo page is not onboarding, not a fake landing mockup and not a checkout page.

It must be implemented only after the SaaS product has enough real functionality to demonstrate the promised flows. The guided demo must run on the real SaaS interface/workflows in a controlled demo workspace or sandbox, using approved demo data. It must not be presented as the visitor's own configured studio before subscription/onboarding.

It must:

- show concrete Pilates scenarios inside the real SaaS demo environment with approved demo data;
- show a full product proof flow from studio configuration to agent configuration, live operation, system record and human control;
- demonstrate how agents act across WhatsApp, agenda, financeiro, vendas, retencao, gestao and historico/evolucao;
- include a guided consultor/assistant layer that explains each step and can answer doubts;
- make human control visible;
- support guided progression for a quick demonstration;
- allow manual navigation for visitors who want to inspect each step;
- open or continue the consultor with the selected demo context;
- avoid sending cold visitors straight to plans or checkout as the default action.

## Route Relationship

- `/pilates`: main narrative landing page.
- `/pilates/demonstracao`: guided product demonstration using the real SaaS demo environment.
- `/pilates/planos`: downstream plan comparison page, usually reached after consultor recommendation or explicit plan-comparison intent.
- Floating consultor: primary conversion surface that can open the demo and receive demo completion context.

## Required Page Structure

1. Header
   - Logo/brand.
   - Back link to `/pilates`.
   - Primary CTA: `Falar com consultor`.
   - Secondary CTA: `Continuar no WhatsApp`.

2. Hero
   - H1: `Veja como os agentes atuam em um studio de Pilates`
   - Supporting copy focused on seeing real routines handled before choosing a plan.
   - CTAs:
     - `Iniciar demonstracao`
     - `Falar com consultor`

3. Scenario Selector
   - Faltas e reposicoes.
   - Interessados e aula experimental.
   - Mensalidades e planos vencendo.
   - Alunos inativos.
   - Agenda baguncada.
   - Historico/evolucao do aluno.
   - Agente sob medida.

4. Guided Step-By-Step Demo
   - Step 1: studio setup preview: hours, plans, class rules, absence/replacement rules and responsible team roles.
   - Step 2: agent setup preview: selected agent, knowledge it can use, limits and allowed actions.
   - Step 3: incoming signal or problem.
   - Step 4: agent detects context and checks approved data.
   - Step 5: agent suggests or performs the next safe action.
   - Step 6: human review/control point when needed.
   - Step 7: operational result appears in the system.

5. Product Surface
   - Real SaaS screens/components when the product exists.
   - WhatsApp-style conversation surface connected to the demo workflow.
   - Agent workspace.
   - Agenda/financeiro/history context depending on scenario.
   - Priority panel or next-action queue.

6. Controls
   - Pause.
   - Next.
   - Previous.
   - Restart.
   - Scenario switch.
   - Reduced-motion friendly fallback.

7. Guided Consultor Layer
   - Explains what is happening in the current step.
   - Answers product and plan doubts using the same approved answer policy as the floating consultor.
   - Offers contextual actions: continue demo, ask question, talk on WhatsApp, see recommended plan or return to landing.
   - Must not invent behavior outside what the real SaaS demo environment supports.

8. Consultor Bridge
   - Copy: `Quer ver o que isso mudaria no seu studio?`
   - Primary CTA opens the consultor with selected scenario, selected pain and completed demo steps.
   - Secondary CTA opens configured WhatsApp assistance with the same safe context when available.

## Scenario Data Rules

All scenario content must come from trusted niche configuration, approved demo fixtures and real SaaS demo-workspace capabilities.

The demo must not use:

- private customer data;
- real student health details;
- real payment credentials;
- unsupported product promises;
- static mockups that imply unbuilt SaaS functionality is already real;
- invented plan prices or checkout URLs.

## CTA Behavior

Primary CTA:

```text
Falar com consultor
```

Behavior:

1. Emit `guided_demo_consultor_clicked`.
2. Open/focus the floating consultor.
3. Include:
   - `sourcePage: /pilates/demonstracao`
   - `selectedScenario`
   - `selectedPain`
   - `completedSteps`
   - `niche`
   - `campaignStage`
   - `publicOfferMode`

Secondary CTA:

```text
Continuar no WhatsApp
```

Behavior:

1. Emit `guided_demo_whatsapp_clicked`.
2. Route to configured WhatsApp assistance destination.
3. Include safe summary/context when available.

The page must not make checkout the default final action. Checkout may appear only after the consultor recommends a plan or the visitor intentionally opens the plan comparison path.

## Conversion Strategy

The guided demo must sell by proof, not by pressure.

The required order is:

```text
scenario selected
  -> studio setup preview
  -> agent setup preview
  -> agent operating in the real demo environment
  -> system record/result
  -> human control
  -> consultor summary
  -> recommended next step
```

The recommended next step can be:

- continue with consultor;
- continue on WhatsApp;
- see the recommended plan;
- compare plans;
- checkout only after explicit buying intent or plan confirmation.

## Risk Reducers

The guided demo must make these points easy to answer before the visitor reaches checkout:

- the demo uses the real SaaS demo environment with example data, and the visitor's real studio is configured only after subscription/onboarding;
- the studio's operational agents use the studio's own connected WhatsApp;
- setup/onboarding helps configure studio rules, plans and agents according to the purchased plan;
- humans can review, assume or override where the product requires control;
- usage caps are plan-based and hard capped;
- payment details are handled by the billing provider, not by chat or WhatsApp;
- cancellation, contract, upgrade/downgrade and plan-change terms are shown only when configured.

## Tracking Events

Required:

- `guided_demo_viewed`
- `guided_demo_started`
- `guided_demo_scenario_selected`
- `guided_demo_step_viewed`
- `guided_demo_completed`
- `guided_demo_consultor_clicked`
- `guided_demo_whatsapp_clicked`

All events must include:

- `niche`
- `sourcePage`
- `campaignStage`
- `publicOfferMode`
- `eventName`
- `metadata`

## Acceptance Criteria

- Visitor can start the demo without sharing contact data.
- Visitor can change scenario without losing page state.
- Autoplay can be paused and restarted.
- Mobile view at 390px has no horizontal overflow and controls remain tappable.
- The final CTA opens the consultor with demo context.
- The page never collects payment data and never marks subscription active.
- The page uses the real SaaS demo environment with approved demo data and does not imply the visitor's studio is already configured.
- The demo shows studio setup preview, agent setup preview, agent operation, system record and human control before plan recommendation.
- The guided consultor layer can answer doubts and route to consultor, WhatsApp, plans or checkout according to readiness.
- The page is not launched as a fake/static substitute before the SaaS can support the demonstrated workflows.
