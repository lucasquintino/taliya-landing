# Implementation Plan: Premium Multi-Niche Landing Page System

**Branch**: `codex/001-niche-landing-system` | **Date**: 2026-04-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-niche-landing-system/spec.md`

## Summary

Treat the existing implementation as a baseline/prototype to be refactored. Reuse stable foundations only: route wiring, data-driven config, calculator utility and tracking utility. Do not preserve existing visual layout or monolithic component structure when it conflicts with the updated spec. Build a premium, reusable multi-niche landing system with `/pilates` as the first route. The page must be data-driven, componentized, and visually benchmarked against Rebookly/Landbot-level quality while remaining original and Pilates-specific. The landing's job is now commercial: sell the vertical SaaS for each niche through a consultor-first journey, show clear plan packaging and BRL pricing, use a guided real-SaaS demo as proof once the SaaS is ready, and route high-intent visitors to plans/checkout only after consultor recommendation or explicit informed intent.

## Technical Context

**Language/Version**: TypeScript 5, React 19, Next.js 16 App Router
**Primary Dependencies**: Next.js 16.2.4, React 19.2.4, Tailwind CSS 4 via `@tailwindcss/postcss`
**Storage**: N/A for current frontend-only landing; assisted-conversion form can log locally until destination is selected; subscription intent may be represented in tracking/context only; subscription/billing state is outside this feature
**Testing**: `npm run lint`, `npm run build`, Chrome screenshot checks at 1440px and 390px, copy audit via `rg`
**Target Platform**: Web, static/prerendered public landing routes
**Project Type**: Next.js web application
**Performance Goals**: Static route output; interactions remain lightweight; avoid large image assets until final illustration strategy is chosen
**Constraints**: No horizontal body overflow at 390px; touch-first mobile interactions; public copy must avoid prohibited terms; plan/checkout URLs and prices must come from trusted config; the landing must not collect card/payment data; a CTA click must never be treated as active subscription; this Next.js version requires reading local docs before API changes
**Scale/Scope**: One production-quality `/pilates` landing now; architecture must support future niche routes by configuration

## Constitution Check

The constitution file is still a placeholder and does not define enforceable project principles. No constitution gate can be evaluated beyond the repository instructions and AGENTS.md rules.

Operational gates for this feature:

- PASS: Keep Spec Kit artifacts as source of truth before implementation.
- PASS: Preserve data-driven multi-niche architecture.
- PASS: Do not expose internal validation language in public copy.
- PASS: Treat consultor-led SaaS subscription as the primary conversion path for each niche.
- PASS: Define plan packaging and launch pricing in the landing spec/config before implementation.
- PASS: Keep full billing, payment webhooks and entitlements out of this landing spec.
- PASS: Componentize before the next visual rebuild.
- PASS: Run `npm run lint`, `npm run build`, responsive screenshots and copy audit before commit.

## Design Direction

Target: premium operational SaaS landing for Pilates, with a clean Landbot-style hero and Rebookly-like product rhythm, but original visual identity.

Core decisions:

- Hero is clean, centered and concise. It does not include the intent selector.
- Block 2 is the first interactive product component: "Quero que meus agentes cuidem de".
- Diagnosis block uses a two-mode segmented control: `Sem agentes` and `Com agentes`.
- Dinheiro na Mesa follows the approved calculator reference: controls/sliders left, strong teal estimate panel right.
- Agents block focuses only on `Selecione o agente` with a changing workspace mockup.
- The previous standalone "Como os agentes trabalham juntos" section is removed.
- "Como funciona" becomes a premium guided flow, not a generic card grid.
- Visual proof requires WhatsApp-style conversations, SaaS/system screens, flows and illustrations.
- Consultor-first diagnosis is the primary conversion pattern; plan/checkout CTAs are downstream once the visitor has context.
- `/pilates/demonstracao` is the guided automated demo route for visitors who need to see the product before plan discussion.
- Plan cards show four Pilates launch offers by active AI agent count: Base R$ 197/mes, 1 Agente R$ 497/mes, 3 Agentes R$ 897/mes and 7 Agentes R$ 1.497/mes as recommended.
- Analysis/Dinheiro na Mesa and human WhatsApp assistance are secondary conversion patterns.
- Access-early framing is no longer the public offer.
- `reference/v0` should be mined for typography, animation, component rhythm and useful UI patterns, then adapted into the componentized architecture.

## Pricing & Subscription Decisions

Landing-owned decisions:

- Pricing data is configuration-owned per niche, not hardcoded in section markup.
- Pilates launch plans are `base`, `one_agent`, `three_agents` and `seven_agents`.
- `seven_agents` is the default recommended plan.
- Every plan has monthly BRL price, optional annual display fields, included-agent list, WhatsApp availability, setup/onboarding expectation, usage boundary, checkout URL and human-assistance URL/context.
- Main landing plan-interest CTAs open/continue the consultor with selected plan context.
- Decision-page checkout CTAs emit `plan_cta_clicked` before navigation.
- Human help from the plans section emits `human_whatsapp_clicked` and includes selected/interested plan when available.

Billing-owned decisions for a separate feature spec:

- Provider selection and account setup.
- Checkout session creation if checkout cannot be represented by static trusted URLs.
- Customer, tenant and subscription mapping.
- Webhook signature verification, idempotency and subscription activation.
- Entitlement enforcement, failed payment handling, cancellation, upgrade, downgrade, invoices, taxes, coupons and customer portal.

Until the billing feature exists, the consultor or plans page may route to trusted checkout/plan-selection URLs or capture a subscription intent, but the landing must not grant access or claim payment/subscription completion.

## Visual Components Strategy

Shared visual components to create:

- `ConversationMockup`
- `WhatsAppConversationMockup`
- `AgentBuilderMockup`
- `SaasPanelMockup`
- `MoneyPanelMockup`
- `AgentWorkspaceMockup`
- `PriorityQueueMockup`
- `StudentHistoryMockup`
- `HumanApprovalMockup`
- `CustomAgentBuilderMockup`
- `FlowDiagram`
- `IllustrationPanel`

These components must receive data through props/config and avoid hardcoded Pilates copy unless explicitly section-owned.

## Project Structure

### Documentation

```text
specs/001-niche-landing-system/
  spec.md
  plan.md
  research.md
  data-model.md
  pricing-subscription-flow.md
  privacy-consent.md
  guided-demo-page.md
  plans-page.md
  quickstart.md
  contracts/
    ui-contract.md
  checklists/
    requirements.md
  tasks.md
```

### Source Code

```text
app/
  page.tsx
  pilates/
    page.tsx
    demonstracao/
      page.tsx
    planos/
      page.tsx

components/
  landing/
    NicheLandingPage.tsx
    PlansPage.tsx
    sections/
      HeroSection.tsx
      IntentSelectorSection.tsx
      ProblemDiagnosisSection.tsx
      MoneyCalculatorSection.tsx
      AgentsDemoSection.tsx
      HowItWorksSection.tsx
      CoverageSection.tsx
      NicheSpecificSection.tsx
      CustomAgentSection.tsx
      HumanControlSection.tsx
      PlansSection.tsx
      AssistedConversionSection.tsx
      FAQSection.tsx
      FinalCTASection.tsx
      FooterSection.tsx
    shared/
      Header.tsx
      SectionShell.tsx
      SectionIntro.tsx
      TrackedLink.tsx
      ConversationMockup.tsx
      WhatsAppConversationMockup.tsx
      AgentBuilderMockup.tsx
      SaasPanelMockup.tsx
      MoneyPanelMockup.tsx
      AgentWorkspaceMockup.tsx
      PriorityQueueMockup.tsx
      StudentHistoryMockup.tsx
      HumanApprovalMockup.tsx
      CustomAgentBuilderMockup.tsx
      FlowDiagram.tsx
      IllustrationPanel.tsx
      FormField.tsx
      SelectField.tsx

data/
  landing/
    niches/
      types.ts
      pilates.ts

lib/
  landing/
    money-calculator.ts
    tracking.ts
```

**Structure Decision**: Next.js App Router with data/config in `data/landing`, pure utilities in `lib/landing`, route-level pages in `app`, and componentized landing UI under `components/landing/sections` and `components/landing/shared`.

## Implementation Phases

### Phase 0: Reference Audit

- Review `reference/v0` for typography, motion, spacing, section rhythm and reusable interaction ideas.
- Review approved screenshots for hero, intent selector, diagnosis toggle and calculator direction.
- Capture decisions in `research.md` before implementation.

### Phase 1: Foundation Refactor

- Audit current implementation and label each piece as reuse, refactor or replace.
- Reuse data/calculator/tracking where compatible.
- Replace visual sections that conflict with the new spec.
- Extract the existing large `NicheLandingPage.tsx` into section and shared components.
- Keep behavior unchanged except for removing dead/obsolete standalone flow section when implementing the new spec.
- Ensure `NicheLandingPage` becomes an orchestrator.

### Phase 2: P1 Visual Rebuild

- Rebuild HeroSection.
- Rebuild IntentSelectorSection.
- Rebuild ProblemDiagnosisSection.
- Rebuild MoneyCalculatorSection.
- Rebuild AgentsDemoSection.

### Phase 3: Trust/Proof Sections

- Rebuild HowItWorksSection.
- Add SaaS consolidated panel for coverage.
- Add illustration panels for Pilates-specific proof, custom agent, human control and plan subscription.

### Phase 4: Commercial Conversion + QA

- Replace access-early/analysis-first messaging with consultor-first commercial messaging.
- Add trusted consultor, guided-demo, plan/subscription and WhatsApp CTA destinations from niche config.
- Add configured pricing and plan cards for Base, 1 Agente, 3 Agentes and 7 Agentes.
- Mark 7 Agentes as recommended and make consultor-led recommendation the dominant action.
- Refine analysis/human WhatsApp assistance section, FAQ, final CTA and footer.
- Ensure no chat/form surface collects payment details.
- Ensure CTA clicks do not imply an active paid subscription.
- Add privacy/consent helper text for forms and WhatsApp assistance CTAs according to `privacy-consent.md`.
- Run lint/build/copy audit.
- Capture desktop and mobile screenshots.
- Commit only after visual checkpoints are approved.

## Complexity Tracking

No constitution violations recorded. Complexity is justified by quality target: the landing must be reusable, premium, highly visual and independently maintainable by section.
