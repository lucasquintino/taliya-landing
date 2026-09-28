# Feature Specification: Premium Multi-Niche Landing Page System

**Feature Branch**: `codex/001-niche-landing-system`
**Created**: 2026-04-28
**Updated**: 2026-04-30
**Status**: Ready for plan/tasks
**Input**: Build a reusable, data-driven landing page system by niche. The first landing is `/pilates`, selling the vertical SaaS for Pilates studios through a consultative conversion path: the visitor is led first to the consultor/Atendente IA, the consultor diagnoses the studio context, can show a guided demonstration of the real SaaS when the product is ready, and then routes the visitor to the right plan page or trusted checkout path. Quality target is a reference-grade landing that feels more premium, specific, interactive and product-led than Rebookly/Landbot for the Pilates niche.

**Public launch assumption**: this landing goes live only after the SaaS is implemented enough to support the promised product experience, including the real guided demo environment. The landing may be specified before the SaaS is complete, but it must not be publicly launched with fake product behavior.

Commercial E2E launch readiness, go-live blockers and implementation order are defined in [../commercial-e2e-readiness-and-implementation-order.md](../commercial-e2e-readiness-and-implementation-order.md). Spec 1 owns the public landing, plans page, guided-demo surface and CTA integrity required by that cross-spec checklist.

CTA entry behavior, plan/display gates, checkout gates, guided-demo readiness and required consultor context payload are defined in [consultor-entry-matrix.md](./consultor-entry-matrix.md). This matrix is the source of truth for widget, Falar com consultor, Continuar no WhatsApp, plan-interest, guided-demo, custom-agent diagnostic and FAQ doubt CTAs.

The parallel `/pilates` visual/layout pass is considered complete and protected. Future work on the main `/pilates` route must be limited to integration, CTA behavior, tracking, schema/config alignment, accessibility fixes or bug fixes. Do not redesign, reorder, restyle or replace the approved landing layout unless the user explicitly reopens the visual direction. The protected layout contract is recorded in [parallel-layout-handoff.md](./parallel-layout-handoff.md).

## Current Implementation Status

A preliminary implementation already exists on the branch. It is a refactorable baseline, not the final visual source of truth. Existing route, data configuration, calculator utility and tracking utility may be reused when they comply with this specification. Existing monolithic UI structure and visual decisions that conflict with this specification must be replaced through the task plan. The current implementation must not override the required page order, visual direction, componentization, mockup strategy or copy rules defined here.

**Protected `/pilates` layout status**: the current `/pilates` visual/layout direction is accepted as the working visual source of truth. Spec-driven implementation after this point must preserve the layout advances already made. Changes to `components/landing/NicheLandingPage.tsx`, `components/landing/sections/*`, shared landing visuals or `data/landing/niches/pilates.ts` for the main landing should be integration-only unless the user explicitly asks for visual redesign.

## Product Positioning

The product is not a CRM, agenda app, generic automation, chatbot or consulting offer. It is a platform of operational AI agents that monitors studio routines, detects pending work, suggests next actions and keeps humans in control.

Internal campaign phase is now `commercial`. Public copy must never expose validation, beta, MVP, test, founder, incomplete product or similar language. Public offer is a vertical SaaS subscription for Pilates studios, sold through a consultor-first journey. The primary CTA is not a cold jump to plans; it opens the consultor/Atendente IA so the visitor can describe the studio, understand the system and receive the right plan path.

Pricing, plan packaging and subscription routing are part of this landing feature. Actual billing activation, webhook processing, customer portal and entitlement enforcement are part of a separate billing feature, but the public plan offer and visitor path must be fully defined here so the page can sell the SaaS clearly.

Privacy, LGPD and consent requirements for landing forms and WhatsApp assistance are defined in [privacy-consent.md](./privacy-consent.md).

Cross-product security, code safety, data protection, secrets, AI guardrails, webhook safety and future tenant isolation requirements are defined in [../005-security-code-data/spec.md](../005-security-code-data/spec.md).

Primary Pilates message:

- Headline: "Reduza faltas, organize reposicoes e renove planos com agentes de IA para Pilates."
- Central message: "Voce cuida dos alunos. Seus agentes cuidam do resto."

## Pricing & Plan Packaging

The Pilates landing MUST show four public subscription plans organized by number of active AI agents: 0, 1, 3 and 7 agents. Prices are launch defaults and MUST live in trusted niche configuration so they can be changed without editing section markup.

| Plan | Public Price | Best For | Positioning |
| --- | ---: | --- | --- |
| Base | R$ 197/mes | Studios that want CRM without active AI agents yet | CRM-only paid entry plan with no active AI automation. |
| 1 Agente | R$ 497/mes | Studios that want to automate one clear operational pain first | One selected primary agent. |
| 3 Agentes | R$ 897/mes | Studios that want meaningful automation across a few priority routines | Three selected primary agents. |
| 7 Agentes | R$ 1.497/mes | Studios that want the complete system | Recommended complete-system plan with all seven primary agents. |

Launch plan entitlements are defined in [pricing-subscription-flow.md](./pricing-subscription-flow.md). The landing must present the same included-agent scope, WhatsApp scope, onboarding expectation and usage boundary that billing and onboarding enforce.

Annual billing MAY be offered as an optional display toggle with two months free equivalent. If annual billing is not available in the configured checkout provider, the toggle MUST be hidden. Public copy must never imply a discount that is not configured in the trusted pricing model.

Plan cards MUST show plan name, monthly price in BRL, target studio fit, included agent coverage, WhatsApp availability, setup/onboarding expectation, usage boundary/hard cap and trusted next action. On the main landing, plan CTAs must open or continue the consultor path with plan interest context. On the dedicated plans page, checkout CTAs are allowed after the visitor has intentionally reached the comparison/decision surface.

The recommended/default plan for Pilates is `seven_agents`.

## SEO And Discoverability

The landing is a paid-conversion surface first, but it must still be technically ready to capture qualified organic demand for the Pilates niche.

SEO requirements:

- `/pilates` must have a unique title and meta description focused on the literal offer/category, such as AI agents or a system for Pilates studios.
- `/pilates/planos` must have its own title and meta description focused on plans/pricing for the Pilates SaaS.
- Metadata must not promise beta, early access, fake demo, unconfigured discounts or unconfirmed product scope.
- Headings must preserve a clear semantic hierarchy and include Pilates-specific language.
- Open Graph/social metadata must use approved brand/landing assets or safe generated assets, not generic stock-like imagery.
- Canonical URLs must be stable for `/pilates` and `/pilates/planos`.
- The final FAQ set should support high-intent buyer questions and search snippets without bloating the page.
- Descriptive link text should be used for consultor, WhatsApp, plans, guided demo, privacy and final CTA links.

## Consultor-First Conversion Entry Matrix

The landing must support six visible commercial entry paths: the four core consultor paths, the Agente sob medida diagnostic report path and the FAQ doubt CTA. All six may eventually lead to subscription or custom-agent sale, but none should force a cold visitor directly into checkout.

| Entry Path | Visitor Intent Level | First Destination | Required Opening Tone | Primary Job |
| --- | --- | --- | --- | --- |
| Floating widget | Unknown/low-to-medium | Web consultor chat | Neutral, helpful and open | Discover what the visitor wants and route to the right path. |
| Falar com consultor | Medium/high | Web consultor chat | Direct, commercial and consultative | Confirm interest, qualify pain and move toward demo, plan recommendation or WhatsApp. |
| Continuar no WhatsApp | Medium/high | Same consultor brain on WhatsApp | Direct, commercial and continuity-focused | Continue the sale in the buyer's preferred channel and allow human takeover. |
| Demonstracao guiada | Medium/proof-seeking | `/pilates/demonstracao` | Product-led, explanatory and commercial | Show the product working, answer doubts and return context to the consultor. |
| Diagnostico de agente sob medida | Medium/high with custom-operation intent | On-page diagnostic report, then consultor/WhatsApp/demo by classification | Consultative, report-like and commercial | Classify whether Taliya already solves the request, whether it is custom, or whether it is mixed; then route to subscription or custom-agent sales. |
| FAQ: ficou alguma duvida? | Low/medium after reading objections | Web consultor chat | Neutral, helpful and doubt-focused | Answer remaining doubts and route to the normal consultor, demo, plan-comparison or WhatsApp path when intent becomes clear. |

Required first-message rules:

- Floating widget MUST start neutral because the system does not yet know the visitor's intent.
- "Falar com consultor" MUST start with stronger commercial intent, such as acknowledging interest and asking whether the visitor wants help choosing the right plan for the studio.
- "Continuar no WhatsApp" MUST use the same commercial brain as the web consultor and carry source/interest context when available.
- "Demonstracao guiada" MUST introduce the demonstration and make clear the visitor can ask questions or continue with the consultor at any moment.
- "Diagnostico de agente sob medida" MUST NOT open as a chat by default. It must accept free text, generate a structured report and then offer CTAs that carry diagnostic context into the consultor, guided demo or WhatsApp.
- "FAQ: ficou alguma duvida?" MUST reuse the normal widget-style consultor behavior, with `entryPath=widget` and `sourceSection=faq_doubt_cta`, because the visitor may only have a small objection or clarification.

The word "consultor" in public UI may refer to the guided commercial assistant, but the system must not impersonate a named human. If the visitor asks for a human, the path is WhatsApp assisted close with Sales Inbox takeover.

## Custom Agent Diagnostic Report Block

The Agente sob medida block is a second commercial front beside public SaaS subscriptions. It exists for operations not already mapped by the seven primary Taliya agents, such as a future marketing agent, content/campaign agent, partnerships agent or another unmapped operation.

This block must be inspired by the "describe your project and receive a diagnostic/proposal" pattern, but adapted to Taliya's vertical SaaS sales motion. It is not the floating chat and must not feel like another message thread. It is a free-text diagnostic composer that generates a short structured sales report.

Required UI behavior:

1. Show a clear prompt such as "Precisa de um agente que ainda nao existe na Taliya?" or "Quer um agente sob medida para seu studio?".
2. Provide a real textarea for the visitor to describe the operation they want to automate.
3. Provide quick prompt examples for common requests, including one custom request such as marketing and one existing Taliya request such as WhatsApp/reposicoes.
4. Use a primary CTA such as "Gerar diagnostico" or "Gerar diagnostico do agente".
5. Render a report result on the page, not a chat conversation.
6. After the report, show commercial CTAs based on the classification.

The report must classify the request into one of four outcomes:

| Classification | Meaning | Commercial Direction |
| --- | --- | --- |
| `mapped_solution` | The request is already covered by the seven primary Taliya agents or their studio-specific configuration. | Sell the SaaS subscription funnel. |
| `custom_agent` | The request is a new operation outside the seven primary agents. | Sell Agente sob medida as a separate opportunity. |
| `mixed_solution` | Part of the request is covered by Taliya and part is custom. | Sell subscription first or alongside custom-agent discovery. |
| `unclear` | The request is too vague to classify confidently. | Ask for clarifying context and route to consultor/WhatsApp. |

Required report sections:

1. `O que voce quer automatizar`: concise summary of the visitor's request.
2. `Impacto para o studio`: practical effect on time, money, occupancy, response speed, retention or team workload.
3. `Isso ja existe na Taliya?`: clear classification and explanation.
4. `Caminho recomendado`: SaaS plan funnel, custom-agent proposal funnel or mixed path.
5. `Proximo passo`: CTAs that continue the sale.

CTA behavior by classification:

- For `mapped_solution`, CTAs are the same commercial paths as "Quer ver como ficaria no seu studio?", but with diagnostic context: `Falar com consultor`, `Demo guiada` when ready/gated by config and `Continuar pelo WhatsApp`.
- For `custom_agent`, CTAs are `Solicitar proposta de agente sob medida` and `Continuar pelo WhatsApp`. Both open or continue the consultor/WhatsApp with the diagnostic classification and must ask the visitor to explain the operation in more detail before collecting contact.
- For `mixed_solution`, CTAs must include a subscription path for the mapped agents and a custom-agent proposal path for the unmapped part.
- For `unclear`, CTAs must continue to consultor or WhatsApp with the report context and ask for the missing details.

The diagnostic report must never route directly to checkout. If the request is already covered, it can move into consultor-led plan recommendation, guided demo or plans-page routing according to the existing gates. If the request is custom, it must collect more scope and contact before a human/operator proposes the custom work.

## High-Ticket Sales Strategy

Because the recommended plan can cost more than R$ 1.000/month, the landing must sell through conviction before checkout.

The required persuasion sequence is:

```text
dor percebida
  -> conversa com consultor
  -> diagnostico rapido
  -> prova visual ou demonstracao guiada
  -> plano recomendado
  -> quebra de objeções
  -> assinatura
```

The landing and consultor must make the visitor feel the system understood their studio before asking for a subscription decision. Public copy, CTAs and handoffs should avoid the feeling of "preco antes de contexto".

Plans may be shown when at least one of these is true:

- the visitor explicitly asks to see or compare plans;
- the visitor clicks a plan-related CTA and the consultor opens with plan-interest context;
- the consultor has captured enough pain/context to recommend a plan;
- the guided demo has finished or reached a natural plan-recommendation point;
- the visitor says they are ready to start, sign or buy.

Checkout may be offered when at least one of these is true:

- the visitor confirms the recommended plan;
- the visitor explicitly asks to subscribe now;
- the visitor reaches the plans page and clicks an explicit checkout CTA;
- a human/operator sends a trusted checkout link from the Sales Inbox after assisted close.

Checkout MUST NOT be the default final action of the main landing or guided demo for cold visitors.

## Plans Page

The landing system must provide a dedicated public page for comparing Pilates plans before checkout.

For v1, the canonical plans destination is `/pilates/planos`.

The plans page exists as a downstream decision page, not as the first cold destination from the main landing. The `/pilates` landing may show plan framing or a compact "Planos / Assinatura" teaser, but primary CTAs such as "quero comecar", "ver meu plano ideal" or "falar com consultor" must open the consultor/Atendente IA with plan-interest context. The consultor then routes to `/pilates/planos` when the visitor asks for comparison, has enough context for a recommendation or insists on seeing plans.

The plans page must sell the SaaS, not act as a generic price table. It must make the recommended plan obvious, explain when lower plans fit, show what is included, answer common plan-selection objections and provide a trusted "Assinar" CTA per plan. It should preserve consultor assistance as the main confidence builder for visitors who are not fully decided.

The plans page must be built from the same trusted pricing/plan configuration used by the landing, Atendente IA and billing checkout. It must not duplicate hardcoded prices, checkout URLs or entitlement claims.

Required `/pilates/planos` page structure:

1. Header with return path to `/pilates`.
2. Focused hero: "Escolha o plano para o seu studio de Pilates".
3. Four plan cards: Base, 1 Agente, 3 Agentes and 7 Agentes.
4. Recommended-plan explanation, with 7 Agentes as default unless config changes.
5. Comparison table by included agents, WhatsApp, onboarding/setup, usage boundary and support level.
6. "Qual plano faz sentido para meu studio?" guidance by studio size and pain profile.
7. FAQ with at most 8 high-impact questions about what Taliya does, team replacement, available agents, plan fit, WhatsApp, setup, guarantee/cancellation and custom agents.
8. Secondary CTA for human WhatsApp assistance.
9. Final CTA to sign the recommended plan or return to comparison.

## Guided Demonstration Page

The landing system must provide a guided demonstration page for visitors who want to see the system working before discussing plans.

For v1, the canonical guided-demo destination is `/pilates/demonstracao`.

The guided demo page is a sales-enablement surface, not onboarding, not a fake landing mockup and not a checkout page. It must be built after the SaaS product has enough real functionality to demonstrate the promised flows. The demo must use the real SaaS interface/workflows in a controlled demo workspace or sandbox with approved demo data, show how agents handle Pilates-specific routines and bring the visitor back to the consultor with captured context. It must not imply the visitor's own studio is already configured before subscription/onboarding.

Required `/pilates/demonstracao` page structure:

1. Header with return path to `/pilates` and CTA to continue with the consultor.
2. Focused hero: "Veja como os agentes atuam em um studio de Pilates".
3. Guided scenario selector using the same pain categories as the landing.
4. Guided step-by-step demo for the selected scenario: signal detected, agent reasoning, suggested action, human control point and expected operational result.
5. Real SaaS demo surfaces for WhatsApp conversation, agent workspace, agenda/financeiro/history context and priority panel.
6. Optional timed autoplay with manual controls: pause, next, previous and restart.
7. "O que isso mudaria no seu studio?" bridge that opens the consultor with selected pain/demo context.
8. Final CTA to talk to the consultor; secondary CTA to continue by WhatsApp.

Required guided-demo narrative:

1. Studio setup preview: show example studio profile, hours, plans, class rules, absence/replacement rules and responsible team roles.
2. Agent setup preview: show which agent is being configured, what information it uses and what it is allowed/not allowed to do.
3. Live demo operation: show an incoming WhatsApp/message/event inside the demo workspace, the agent detecting intent and consulting approved studio context.
4. Agent action: show the response, suggestion, schedule/payment/history update or next-action creation.
5. System record: show how the action appears in the operational panel, agenda, financeiro, student history or priority queue.
6. Human control: show where a human can approve, edit, assume or override.
7. Commercial bridge: summarize what the selected scenario would solve and open the consultor with the demo context.

The guided demo must include an on-page consultor/assistant layer or side panel that explains the current step, answers doubts and can route to the next commercial step. This guide uses the same approved commercial rules as the floating consultor, but the demonstrated behavior must stay within what the real SaaS demo environment supports.

Guided demo boundaries:

- It must use the real SaaS demo environment with approved demo content, not private customer data.
- It must not be launched as a fake/static substitute before the SaaS can support the demonstrated workflows.
- It must remain disabled or reroute to consultor/WhatsApp/product explanation while `guidedDemoReady=false`.
- It must not imply the visitor's studio is already configured.
- It must not collect payment data.
- It must not send the visitor straight to checkout as the default action.
- It must track selected scenario, completed steps and consultor handoff context.

## Subscription Flow

Consultor-led subscription is the primary conversion path:

1. Visitor opens `/pilates` and clicks the primary CTA, floating widget, WhatsApp CTA or guided-demo CTA.
2. The consultor/Atendente IA starts a short diagnosis, answers doubts and maps the visitor's pains to the relevant agents.
3. If helpful, the consultor routes the visitor to `/pilates/demonstracao` and preserves the selected pain/context.
4. When the visitor is ready, the consultor recommends a plan and routes to `/pilates/planos` or a trusted checkout/subscription destination.
5. Payment data is collected only by the checkout/billing provider, never by the landing page, chat widget or marketing form.
6. Subscription is considered active only after a trusted server-side billing event confirms payment/subscription status.
7. After activation, onboarding/setup is started by the SaaS/billing product flow, not inferred from the landing click.

Before checkout, the experience must answer the core high-ticket risk reducers when relevant:

- what happens after payment confirmation;
- whether the studio uses its own WhatsApp;
- who helps configure the studio and agents;
- whether a human can assume or approve conversations;
- whether the visitor can change plan later when configured;
- how usage limits/hard caps work;
- whether cancellation/contract terms are configured;
- that payment details are handled only by the billing provider, never inside chat/WhatsApp.

If the visitor asks to see plans without context:

1. The consultor gives a short plan summary from trusted configuration.
2. The consultor asks one concise qualifying question if needed.
3. The consultor can route to `/pilates/planos` with selected/interested plan context.
4. Any final subscription must still happen through the trusted checkout/subscription path.

Temporary pre-billing behavior is allowed only for environments without a live checkout provider: the plan CTA may create a `subscription_intent` or route to a trusted "plan selection" URL, but public UI must make clear the subscription is not active until checkout is completed.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Studio understands the SaaS offer and can subscribe (Priority: P1)

As a Pilates studio owner, I want to open `/pilates`, immediately understand that AI agents can reduce absences, organize make-up classes and renew plans, and start a consultative path that helps me choose the right plan without feeling like I am joining an unfinished product.

**Why this priority**: This is the primary revenue path and the first proof that the vertical SaaS offer is clear, premium and ready to buy.

**Independent Test**: Visit `/pilates` at 1440px and 390px, verify the first viewport is clean and premium, then use the primary CTA to open the consultor with landing context.

**Acceptance Scenarios**:

1. **Given** a visitor opens `/pilates`, **When** the hero loads, **Then** the page shows a clean centered hero with the Pilates headline, a gradient emphasis on the AI agents part, a short subtitle and clear CTAs.
2. **Given** the hero is visible, **When** the visitor scans the first viewport, **Then** it does not include the "Quero que meus agentes cuidem de" selector inside the hero.
3. **Given** the visitor clicks the primary CTA, **When** the consultor opens, **Then** public copy does not mention validation, beta, MVP, test, founder or incomplete product.
4. **Given** the visitor clicks a plan CTA or submits an assisted-conversion form, **When** tracking payload is emitted, **Then** it includes `niche`, `sourcePage`, `campaignStage` and `publicOfferMode`.
5. **Given** the visitor reaches the plans section, **When** they compare offers, **Then** they see Base, 1 Agente, 3 Agentes and 7 Agentes with BRL monthly pricing, clear fit, included agent coverage and one recommended plan.
6. **Given** the visitor selects a plan, **When** the CTA is activated, **Then** the destination uses a trusted configured checkout/subscription URL for that exact plan and does not collect payment details on the landing page.
7. **Given** the visitor asks the consultor to see plans or the consultor has enough context to recommend one, **When** the plans destination opens, **Then** `/pilates/planos` renders the full comparison page with all plan cards visible and the recommended plan visually clear.

---

### User Story 2 - Visitor interacts with operational pains and sees product proof (Priority: P1)

As a Pilates studio owner, I want to choose what I want agents to handle, compare the operation with and without agents, estimate recoverable money and inspect agent workspaces before leaving my data.

**Why this priority**: This is the main product proof. It must make the page feel like a real operational system, not a generic marketing page.

**Independent Test**: Interact with the intent selector, problem comparison toggle, Dinheiro na Mesa calculator and agent selector on desktop and mobile.

**Acceptance Scenarios**:

1. **Given** the block after the hero, **When** it renders, **Then** it is dedicated only to "Quero que meus agentes cuidem de" and presents a polished selector with WhatsApp-style conversation mockups.
2. **Given** a visitor selects a pain, **When** the selection changes, **Then** the conversation mockup updates with Pilates-specific messages, agent detection, suggested action and result.
3. **Given** the "Por que seu studio perde dinheiro sem perceber" block, **When** the visitor switches between `Sem agentes` and `Com agentes`, **Then** the horizontal cards change between loss patterns and agent-assisted outcomes.
4. **Given** the Dinheiro na Mesa calculator, **When** sliders or inputs change, **Then** the monthly estimate and breakdown update live in a strong teal result panel.
5. **Given** the Agents block, **When** the visitor selects one of the seven agents, **Then** only the "Selecione o agente" component is shown and the workspace mockup updates for that agent.

---

### User Story 3 - Visitor sees real product surfaces, guided demo and trust-building visuals (Priority: P1)

As a Pilates studio owner, I want to see high-quality conversations, system screens, guided demonstrations, flows and illustrations so I understand there is a real operational product behind the offer before I discuss a plan.

**Why this priority**: The landing must beat strong benchmarks through product clarity, visual trust and niche specificity.

**Independent Test**: Review all visual proof blocks and confirm each mockup/illustration has a clear job and does not feel generic.

**Acceptance Scenarios**:

1. **Given** conversation mockups appear, **When** they are reviewed, **Then** they include Pilates-specific WhatsApp-style scenarios for absences, make-up classes, payments, inactive students, trial classes and student history.
2. **Given** SaaS/system mockups appear, **When** they are reviewed, **Then** they show agent workspaces, money panels, priority queues, consolidated operations, human approval and custom-agent configuration.
3. **Given** illustration blocks appear, **When** they are reviewed, **Then** they support Pilates-specific context, custom agents, plan subscription, human assistance and human control without looking like generic stock artwork.
4. **Given** external references inform the design, **When** the page is audited, **Then** it is benchmark-level without copying Rebookly, Landbot, Lufisio or any third-party asset, text, logo or identity.
5. **Given** the visitor opens `/pilates/demonstracao`, **When** they choose a pain scenario, **Then** the page runs a guided demo in the real SaaS demo environment and ends by opening the consultor with selected pain/demo context.

---

### User Story 4 - Marketing adds more niches without rebuilding the landing (Priority: P2)

As the project operator, I want to add future pages for physiotherapy, aesthetics, personal training and other niches by configuration while keeping shared sections reusable.

**Why this priority**: Pilates is the first implementation, not the whole product.

**Independent Test**: Add a second niche configuration and route using the same renderer and section components without hardcoding visible niche copy in reusable components.

**Acceptance Scenarios**:

1. **Given** a new niche config exists, **When** its route is rendered, **Then** the same section system can render niche-specific copy, mockups, calculator assumptions, form options and tracking context.
2. **Given** reusable components are audited, **When** visible text is inspected, **Then** Pilates-specific copy is sourced from configuration or section-level props, not embedded in generic components.
3. **Given** future campaign stages change, **When** public offer mode changes, **Then** CTAs, form context and tracking adapt without rebuilding the page structure.

---

### User Story 5 - Implementation remains modular and reviewable (Priority: P2)

As the builder, I want the landing to be componentized so every block can be redesigned, tested and reviewed independently without a giant page file.

**Why this priority**: The visual target is high enough that iteration must be safe and modular.

**Independent Test**: Inspect source structure and confirm the landing renderer delegates to section and shared components.

**Acceptance Scenarios**:

1. **Given** the implementation is inspected, **When** the page renderer is opened, **Then** it acts as an orchestrator rather than containing all section markup inline.
2. **Given** a single section needs redesign, **When** it is edited, **Then** the change is isolated to that section or shared mockup component.
3. **Given** visual assets are audited, **When** conversation screens, flows, SaaS mockups and illustrations are reviewed, **Then** each has a named reusable component or clear section ownership.

## Required Page Order

1. Header
2. Hero enxuta
3. Quero que meus agentes cuidem de
4. Por que seu studio perde dinheiro sem perceber
5. Dinheiro na Mesa
6. Agentes em acao / Selecione o agente
7. Como funciona
8. Tudo que hoje fica espalhado passa a ser acompanhado pelos agentes
9. Feito para a rotina real de um studio de Pilates
10. Agente sob medida / diagnostico de agente sob medida
11. Humano no controle
12. Demonstracao guiada / ver em acao
13. Planos / Assinatura
14. Analise da operacao / WhatsApp humano
15. FAQ
16. CTA final
17. Footer

The previous standalone block "Como os agentes trabalham juntos" is removed. Its useful flow idea may be reused inside other visual proof blocks, but it must not appear as its own section.

## Visual Asset Map

### WhatsApp-style conversation screens

- Hero: optional lightweight conversation proof below the copy, not a full SaaS screen.
- Quero que meus agentes cuidem de: primary interactive conversation mockup with variants for Faltas, Reposicoes, Mensalidades, Alunos inativos, Aulas experimentais, Historico do aluno and Agente sob medida.
- Agentes em acao: agent-specific conversation/task context for Atendimento, Agenda, Vendas, Financeiro, Retencao, Gestao and Historico/Evolucao.
- Humano no controle: suggested message with human review, edit, approve and send actions.
- Autonomous WhatsApp flows are mapped in `autonomous-whatsapp-flows.md` for Atendimento, Agenda, Vendas, Financeiro and Retencao. These flows define trigger, customer action, AI action, phone screen behavior, tools and terminal states for future mockups and SaaS behavior.

### SaaS/system mockups

- Dinheiro na Mesa: primary money panel with controls, estimate, breakdown and actions.
- Agentes em acao: workspace screen per agent.
- Tudo que hoje fica espalhado: consolidated operations panel with WhatsApp, agenda, payments, inactive students, history/evolution and daily priorities.
- Como funciona: mini screens inside a guided flow, not a large system screen.
- Agente sob medida: lightweight custom-agent configuration screen plus a report-style diagnostic result state.
- Humano no controle: approval/review screen.

### Illustrations

- Feito para Pilates: niche-specific Pilates/studio illustration.
- Agente sob medida: modular custom-agent illustration plus mini UI and free-text diagnostic/report composer.
- Humano no controle: human/operator illustration supporting trust.
- Demonstracao guiada: guided real-SaaS demo workflow by pain scenario, launched only after the SaaS supports the demonstrated flows.
- Planos / Assinatura: plan framing that opens/continues the consultor on the main landing; full plan cards live on `/pilates/planos`.
- FAQ/CTA final: optional minimal texture or icon treatment only.

## Functional Requirements *(mandatory)*

- **FR-001**: The system MUST render `/pilates` as a public Pilates landing page.
- **FR-002**: The system MUST be multi-niche and data-driven, not a single hardcoded Pilates page.
- **FR-003**: The visible Pilates copy SHOULD come from niche configuration except where a section title is intentionally shared.
- **FR-004**: The page MUST follow the required page order defined above.
- **FR-005**: The hero MUST be clean, centered, visually spacious and benchmarked against high-quality Landbot/Rebookly-style heroes.
- **FR-006**: The hero MUST NOT include the "Quero que meus agentes cuidem de" selector.
- **FR-007**: The hero MUST include the Pilates headline, central message, subtitle, CTAs and a light product/conversation proof below the copy if used.
- **FR-008**: The block immediately after the hero MUST be dedicated to "Quero que meus agentes cuidem de".
- **FR-009**: The intent block MUST update a WhatsApp-style conversation mockup for each selected pain.
- **FR-010**: The problem diagnosis block MUST include a two-mode toggle: `Sem agentes` and `Com agentes`.
- **FR-011**: The problem diagnosis block MUST show horizontal cards whose content and visual state change by selected mode.
- **FR-012**: The Dinheiro na Mesa calculator MUST visually follow the approved calculator reference: centered title, controls/sliders on the left and strong teal estimate panel on the right.
- **FR-013**: The Dinheiro na Mesa UI MUST NOT publicly use the term `ROI`.
- **FR-014**: The calculator MUST include the business inputs already defined for active students, monthly fee, absences/cancellations, open classes, overdue payments, expiring plans, inactive students, interested people, trial classes and manual hours.
- **FR-015**: The calculator MUST show a main monthly recoverable-money estimate and a breakdown by the seven primary agents.
- **FR-016**: The Agents block MUST be focused on the `Selecione o agente` component only.
- **FR-017**: The Agents block MUST include exactly seven primary agents: Atendimento, Agenda, Vendas, Financeiro, Retencao, Gestao and Historico/Evolucao.
- **FR-018**: The custom agent offer MUST remain a separate expansion layer, not an eighth primary agent.
- **FR-019**: Vendas and Historico/Evolucao MUST have mockups and copy with equivalent strength to other agents.
- **FR-020**: The standalone "Como os agentes trabalham juntos" section MUST be removed.
- **FR-021**: The "Como funciona" block MUST be redesigned as a premium guided flow, not a generic three-card grid.
- **FR-022**: The page MUST include conversation mockups, SaaS/system mockups and illustrations according to the Visual Asset Map.
- **FR-023**: Public copy MUST use Pilates-specific language such as studio, alunos, turmas, presenca, reposicao, mensalidades, planos vencendo, alunos inativos, historico/evolucao, restricoes and observacoes.
- **FR-024**: Public copy MUST avoid visible terms including lead, follow-up, ticket medio, ROI, dashboard, workflow, founder, beta, MVP, teste, validacao, produto incompleto, early access and acesso antecipado.
- **FR-025**: Public copy SHOULD use terms such as interessado, proximo contato, chamar de volta, mensalidade media por aluno, dinheiro recuperavel, painel, fluxo, assinar plano, falar com humano, analise da operacao and agente sob medida.
- **FR-026**: The primary CTA MUST open or focus the configured consultor/Atendente IA with landing context, not route cold visitors directly to plans or checkout.
- **FR-027**: The landing MUST let the consultor route visitors to analysis/Dinheiro na Mesa, guided demonstration, plans page, checkout or human WhatsApp assistance according to their intent and qualification context.
- **FR-028**: Any checkout or subscription destination MUST come from trusted configuration, not arbitrary user/model-generated URLs.
- **FR-029**: The landing MUST NOT collect card data, payment credentials or billing documents in marketing forms or chat surfaces.
- **FR-030**: The assistance/analysis form MUST capture name, WhatsApp, studio name, city/state, active student count, biggest pain, current system usage, custom-agent routine and preferred next step.
- **FR-031**: The form MUST automatically include `niche`, `sourcePage`, `campaignStage` and `publicOfferMode` in submissions.
- **FR-032**: Tracking events MUST include `niche`, `sourcePage`, `campaignStage`, `publicOfferMode`, `eventName` and `metadata`.
- **FR-033**: Required tracking events are page view, CTA click, plan CTA click, pain selected, agent selected, calculator started, calculator result updated, form started, form submitted, human WhatsApp clicked, custom-agent interest clicked, custom-agent diagnostic submitted/generated/CTA clicked and FAQ doubt CTA clicked.
- **FR-034**: The landing MUST be excellent at 1440px and 390px with no horizontal body overflow.
- **FR-035**: Interactions MUST work by touch on mobile and must not depend on hover.
- **FR-036**: The implementation MUST be modular enough for individual sections, shared mockups and visual components to be iterated independently.
- **FR-037**: The final page MUST feel premium, product-led and specific to Pilates, with visual quality intended to surpass Rebookly/Landbot for this niche without copying their protected identity.
- **FR-038**: Pilates pricing MUST define four public plans in trusted configuration: Base at R$ 197/mes, 1 Agente at R$ 497/mes, 3 Agentes at R$ 897/mes and 7 Agentes at R$ 1.497/mes.
- **FR-039**: The 7 Agentes plan MUST be marked as the recommended/default plan for Pilates unless configuration explicitly changes it.
- **FR-040**: Plan cards MUST show price, target studio fit, included agent coverage, WhatsApp availability, setup/onboarding expectation, usage boundary and CTA. On `/pilates`, plan CTA behavior MUST open/continue the consultor; on `/pilates/planos`, checkout CTAs MAY route to trusted checkout.
- **FR-041**: Plan CTA payloads MUST include `planId`, `planName`, `billingPeriod`, `priceBRL`, `sourceSection`, `niche`, `campaignStage` and `publicOfferMode`.
- **FR-042**: The landing MUST NOT mark a subscription as active, grant access or promise onboarding completion from a CTA click alone.
- **FR-043**: If annual billing is displayed, the annual price/discount MUST come from trusted configuration and MUST be hidden when not configured.
- **FR-044**: Human WhatsApp assistance MUST remain an assisted-close path controlled by the consultor and MUST be framed as help choosing/closing a plan when the visitor wants a human.
- **FR-045**: Assisted-conversion forms MUST show privacy/consent helper text before collecting contact details.
- **FR-046**: The landing MUST link to a privacy notice/policy from the footer or form area before public launch.
- **FR-047**: Form and tracking payloads MUST include conversion purpose/context and SHOULD avoid full raw free-text storage when structured metadata is enough.
- **FR-048**: WhatsApp assistance CTAs MUST make clear that the visitor is choosing to continue by WhatsApp.
- **FR-049**: Landing forms MUST NOT request sensitive student health details or unnecessary personal data.
- **FR-050**: The landing system MUST expose a stable dedicated Pilates plans page at `/pilates/planos`.
- **FR-051**: "Ver planos", "Comparar planos" and plan-related CTAs on the main landing MUST open or continue the consultor with plan-interest context; the consultor may then route to `/pilates/planos` after answering and qualifying.
- **FR-052**: The plans page MUST show the four configured plans, the recommended/default plan, consultor CTAs, explicit checkout CTAs and secondary human WhatsApp assistance CTAs.
- **FR-053**: The plans page MUST reuse the same trusted pricing/plan configuration as the landing, Atendente IA and billing checkout and must not duplicate hardcoded prices.
- **FR-054**: The plans page MUST include a plan comparison table, plan-fit guidance, plan FAQ and post-subscription next-step explanation.
- **FR-055**: The compact plans section on `/pilates`, if present, MUST link to `/pilates/planos` for full comparison.
- **FR-056**: The Base plan MUST be described as CRM without active AI agents, not as an AI-agent automation plan.
- **FR-057**: Public plan copy MUST state or imply that studios use their own connected WhatsApp Business number for their operational agents.
- **FR-057A**: Public landing, plan copy and consultor answers MUST make clear that WhatsApp agents require the studio to have or prepare WhatsApp Business; a personal WhatsApp number MUST NOT be presented as connectable as-is.
- **FR-058**: Public launch plans MUST be scoped to one studio/unit; multi-unit must not be promised before a future Enterprise offer exists.
- **FR-059**: Agente sob medida MUST be presented as a separate business/opportunity, not as included in any public launch plan.
- **FR-060**: The landing system MUST expose a stable guided demonstration page at `/pilates/demonstracao` once the SaaS can support the demonstrated real-product workflows.
- **FR-061**: The guided demo page MUST use the real SaaS demo environment with approved scenario data and show step-by-step agent behavior for Pilates pains without implying the visitor's studio is already configured.
- **FR-062**: The guided demo page MUST provide manual controls and an optional autoplay path without requiring hover-only interaction.
- **FR-063**: The guided demo page MUST end by opening/continuing the consultor with selected pain, selected scenario, completed demo steps and source page context.
- **FR-064**: The guided demo page MUST NOT route straight to checkout as its default final action.
- **FR-065**: The landing MUST implement the six entry paths defined in the Consultor-First Conversion Entry Matrix: floating widget, Falar com consultor, Continuar no WhatsApp, Demonstracao guiada, Diagnostico de agente sob medida and FAQ doubt CTA.
- **FR-066**: Each entry path MUST pass source intent/context to the consultor so the first message and next steps match visitor intent.
- **FR-067**: The landing MUST define plan-display gates so visitors see `/pilates/planos` after explicit plan interest, enough diagnostic context, guided-demo progress/completion or strong buying intent.
- **FR-068**: The landing MUST define checkout gates so checkout is offered only after explicit buying intent, confirmed recommendation, intentional plans-page action or operator-assisted close.
- **FR-069**: The guided demo MUST show the full sales-proof sequence in the real SaaS demo environment: studio setup preview, agent setup preview, operation, agent action, system record, human control and consultor bridge.
- **FR-070**: Before checkout CTAs, the experience MUST make the core risk reducers available: post-payment next step, studio-owned WhatsApp, setup help, human control, plan changes when configured, usage caps, cancellation/contract when configured and payment-data safety.
- **FR-071**: The Agente sob medida block MUST include a real free-text diagnostic composer and MUST NOT present a fake placeholder-only input.
- **FR-072**: Submitting the diagnostic composer MUST generate a structured report result on the page rather than opening a normal chat thread by default.
- **FR-073**: The diagnostic report MUST classify the request as `mapped_solution`, `custom_agent`, `mixed_solution` or `unclear`.
- **FR-074**: If the report classification is `mapped_solution`, the CTAs MUST route to the normal SaaS sales funnel with diagnostic context: consultor, guided demo when ready/gated and WhatsApp continuation.
- **FR-075**: If the report classification is `custom_agent`, the CTAs MUST route to the consultor or WhatsApp in custom-agent proposal mode and ask for operation details/contact before promising a proposal.
- **FR-076**: If the report classification is `mixed_solution`, the UI MUST make clear which part is covered by the SaaS and which part is custom, then offer both SaaS consultor/demo flow and custom-agent proposal follow-up.
- **FR-077**: The diagnostic report MUST NOT route directly to checkout. Checkout remains available only through existing plan/checkout gates after consultor-led recommendation or intentional plans-page action.
- **FR-078**: Diagnostic report tracking MUST include the original source section, classification, mapped agent IDs, custom-agent summary when applicable and selected CTA, while avoiding unnecessary raw free-text storage.
- **FR-079**: The landing FAQ MUST show at most 8 visible high-impact questions and MUST prioritize purchase objections and routing questions over long generic FAQ volume.
- **FR-080**: The landing FAQ MUST end with a "ficou alguma duvida?" CTA that opens/focuses the consultor with `entryPath=widget` and `sourceSection=faq_doubt_cta`, using neutral/helpful opening behavior and no direct checkout route.
- **FR-081**: `/pilates` and `/pilates/planos` MUST define unique SEO metadata, Open Graph metadata and canonical URLs aligned with the current commercial SaaS positioning.
- **FR-082**: Public metadata and headings MUST avoid beta, early access, validation, fake demo or incomplete-product language.
- **FR-083**: SEO copy MUST target qualified Pilates SaaS demand without turning the page into generic SEO filler or weakening the consultor-first sales motion.
- **FR-084**: The final launch QA evidence MUST include desktop/mobile screenshots for `/pilates` and `/pilates/planos`, metadata inspection and confirmation that no visible CTA points to a missing route.

## Key Entities

- **Niche Landing**: A configured public landing page for a business niche.
- **Campaign Stage**: Internal phase controlling strategy, currently `commercial`.
- **Public Offer Mode**: Visitor-facing offer, currently direct vertical SaaS subscription.
- **Pain Option**: Selectable operational pain connected to conversation mockups and tracking.
- **Problem Mode**: `Sem agentes` or `Com agentes` mode for the diagnosis block.
- **Agent**: One of the seven operational agents.
- **Conversation Mockup**: WhatsApp-style product proof screen for a scenario or agent.
- **SaaS/System Mockup**: Product screen showing panels, workspaces, priorities, money estimates or approvals.
- **Guided Demo Page**: Dedicated `/pilates/demonstracao` surface that demonstrates approved product scenarios through the real SaaS demo environment and hands context back to the consultor.
- **Illustration Panel**: Non-generic illustration supporting a section's message.
- **Money Calculator Input**: Numeric business input used for Dinheiro na Mesa.
- **Subscription CTA**: Trusted configured plan or checkout destination for a niche.
- **Pricing Plan**: Public plan offer with BRL price, included agents, usage boundary, onboarding expectation, billing period options and trusted checkout destination.
- **Plans Page**: Dedicated public route `/pilates/planos` where visitors compare plans before checkout.
- **Subscription Intent**: A selected plan and landing context captured before checkout completion; not proof of an active subscription.
- **Assisted Conversion Submission**: Form data plus automatic context for analysis, human WhatsApp assistance or custom-agent follow-up.
- **Custom Agent Diagnostic Report**: A report-style result generated from a free-text custom-agent request, classifying whether the request is already covered by Taliya, requires Agente sob medida, is mixed or is unclear, then routing to the correct commercial path.
- **Tracking Event**: Frontend event payload with standard landing context.

## Success Criteria *(mandatory)*

- **SC-001**: A first-time visitor understands the Pilates-specific SaaS offer and primary value within the first viewport.
- **SC-002**: The hero visually matches the approved clean benchmark direction and does not include the intent selector.
- **SC-003**: The block after the hero is clearly the first interactive selector: "Quero que meus agentes cuidem de".
- **SC-004**: The diagnosis block toggles cleanly between `Sem agentes` and `Com agentes` with updated cards.
- **SC-005**: The Dinheiro na Mesa block looks like a premium calculator and updates live.
- **SC-006**: The Agents block is centered on selecting one of the seven agents and viewing its workspace/mockup.
- **SC-007**: Visual audit confirms high-quality conversation screens, SaaS mockups, flows and illustrations across required sections.
- **SC-008**: A copy audit finds none of the prohibited public terms in visible landing content.
- **SC-009**: A responsive audit at 1440px and 390px confirms no horizontal body overflow and usable touch interactions.
- **SC-010**: Adding another niche can reuse the renderer, section components, visual components, tracking, calculator and subscription CTA model without duplicating Pilates page structure.
- **SC-011**: A high-intent visitor can open the consultor from the first viewport and receive a plan/checkout path after answering concise qualification questions.
- **SC-012**: A visitor who wants help before subscribing can choose guided demo, analysis or human WhatsApp assistance without confusing those paths with active subscription.
- **SC-013**: A visitor can compare the four Pilates plans and identify the recommended plan after reaching the plans page through consultor-led or explicit plan-comparison intent.
- **SC-014**: Selecting any plan routes only to a trusted configured destination and never asks for payment details inside the landing page.
- **SC-015**: A QA audit confirms no UI state, tracking event or form submission treats a plan CTA click as a paid/active subscription.
- **SC-016**: Assisted-conversion forms and WhatsApp CTAs show clear privacy/consent framing before contact capture or channel handoff.
- **SC-017**: A visitor can reach `/pilates/planos` from the consultor or explicit plan-comparison path, then compare plans without asking a human.
- **SC-018**: The `/pilates/planos` page uses the same configured plan data as `/pilates` and the checkout route.
- **SC-019**: A visitor can open `/pilates/demonstracao`, complete an automated scenario and return to the consultor with demo context preserved.
- **SC-020**: A QA walkthrough confirms each of the six entry paths starts with the correct tone and can reach demo, plans, WhatsApp, custom-agent proposal or checkout through the correct gates.
- **SC-021**: A high-ticket sales walkthrough confirms the visitor can move through pain, diagnosis, proof/demo, recommendation, objections and checkout without being sent cold to pricing.
- **SC-022**: A visitor can type an unmapped operation such as "agente de marketing" into the custom-agent diagnostic composer, receive a report classified as `custom_agent` and continue to consultor/WhatsApp with custom-agent proposal context.
- **SC-023**: A visitor can type a mapped operation such as "responder WhatsApp e organizar reposicoes", receive a report classified as `mapped_solution` and continue to consultor, guided demo or WhatsApp with SaaS sales context.
- **SC-024**: A visitor can type a mixed request and see which parts are covered by Taliya versus Agente sob medida without being sent directly to checkout.
- **SC-025**: A visitor can read a shortened FAQ with at most 8 questions, click "ficou alguma duvida?" and open the consultor with neutral widget-style behavior.
- **SC-026**: A metadata audit confirms `/pilates` and `/pilates/planos` have unique title, description, Open Graph/canonical metadata and no legacy early-access positioning.
- **SC-027**: Launch evidence includes screenshots and CTA route checks proving the landing, plans page, FAQ CTA, consultor CTAs and WhatsApp CTAs are functional on desktop and mobile.

## Assumptions

- The first implementation may still route to configured plan/checkout URLs rather than implementing billing inside the landing feature, but plan names, prices and CTAs must already be represented in configuration.
- Full checkout, billing webhooks, subscriptions, entitlements, failed payment, invoices, taxes, coupons, proration and customer portal behavior belong in a separate billing feature spec.
- Assistance form submissions may initially log locally until a backend/CRM destination is chosen.
- External references are inspiration only; final design must be original.
- `reference/v0` is a visual and interaction reference to mine for typography, motion and useful patterns, not a source of truth.
