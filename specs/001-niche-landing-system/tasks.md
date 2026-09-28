# Tasks: Premium Multi-Niche Landing Page System

**Input**: Design documents from `/specs/001-niche-landing-system/`
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `pricing-subscription-flow.md`, `privacy-consent.md`, `contracts/ui-contract.md`, `quickstart.md`

**Tests**: No formal test suite requested yet. Required verification is lint, build, copy audit, responsive screenshots and manual interaction walkthrough.

**Organization**: Tasks are grouped by user story so each increment can be reviewed independently.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Restore clean implementation baseline and prepare the project for section-by-section work.

- [X] T001 Confirm working tree excludes unplanned visual edits in `components/landing/NicheLandingPage.tsx`
- [X] T002 Audit existing implementation and classify files/sections as reuse, refactor or replace in `specs/001-niche-landing-system/research.md`
- [X] T003 Preserve reusable baseline pieces from `app/pilates/page.tsx`, `data/landing/niches/pilates.ts`, `lib/landing/money-calculator.ts` and `lib/landing/tracking.ts`
- [X] T004 Review Next.js local docs relevant to App Router, client components and metadata in `node_modules/next/dist/docs/`
- [X] T005 [P] Audit reusable typography, motion and layout patterns in `reference/v0/components/landing/` and capture notes in `specs/001-niche-landing-system/research.md`
- [X] T006 [P] Audit approved external visual references and capture concrete non-copying design cues in `specs/001-niche-landing-system/research.md`
- [X] T007 Update public-copy prohibited-term audit command in `specs/001-niche-landing-system/quickstart.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Componentize before redesigning blocks. No visual story work should begin until this is complete.

- [X] T008 Create shared component directory structure in `components/landing/shared/`
- [X] T009 Create section component directory structure in `components/landing/sections/`
- [X] T010 [P] Extract `Header` to `components/landing/shared/Header.tsx`
- [X] T011 [P] Extract `SectionShell` to `components/landing/shared/SectionShell.tsx`
- [X] T012 [P] Extract `SectionIntro` to `components/landing/shared/SectionIntro.tsx`
- [X] T013 [P] Extract `TrackedLink` to `components/landing/shared/TrackedLink.tsx`
- [X] T014 [P] Extract form primitives to `components/landing/shared/FormField.tsx` and `components/landing/shared/SelectField.tsx`
- [X] T015 Create visual mockup component shells in `components/landing/shared/ConversationMockup.tsx`, `components/landing/shared/SaasPanelMockup.tsx`, `components/landing/shared/FlowDiagram.tsx` and `components/landing/shared/IllustrationPanel.tsx`
- [X] T016 Create initial section files in `components/landing/sections/` for all required page sections
- [X] T017 Refactor `components/landing/NicheLandingPage.tsx` into an orchestrator that imports section components
- [X] T018 Verify existing `/pilates` behavior still builds after componentization with `npm run lint` and `npm run build`

**Checkpoint**: Landing is componentized and ready for visual rebuild.

---

## Phase 3: User Story 1 - Clean Hero and Conversion Entry (Priority: P1) MVP

**Goal**: Deliver a clean, centered, high-quality hero using Pilates copy and no intent selector inside the hero.

**Independent Test**: Visit `/pilates`; first viewport shows centered hero, gradient emphasis, short subtitle, CTAs and optional lightweight proof below copy. The phrase "Quero que meus agentes cuidem de" is absent from the hero.

- [X] T019 [US1] Implement clean centered hero layout in `components/landing/sections/HeroSection.tsx`
- [X] T020 [US1] Add gradient emphasis to the AI agents phrase in `components/landing/sections/HeroSection.tsx`
- [X] T021 [US1] Add lightweight non-dominating conversation/product proof below hero copy in `components/landing/sections/HeroSection.tsx`
- [X] T022 [US1] Ensure hero content is sourced from `data/landing/niches/pilates.ts` or explicit hero props
- [X] T023 [US1] Verify hero at 1440px and 390px with screenshots saved under `tmp/screenshots/`

**Checkpoint**: Hero approved before moving to the next block.

---

## Phase 4: User Story 2 - Interactive Pain, Diagnosis, Calculator and Agent Proof (Priority: P1)

**Goal**: Rebuild the primary interactive product proof blocks with benchmark-level UI.

**Independent Test**: User can interact with intent selector, diagnosis mode toggle, calculator and agent selector independently on desktop and mobile.

- [X] T024 [P] [US2] Implement `WhatsAppConversationMockup` in `components/landing/shared/WhatsAppConversationMockup.tsx`
- [X] T025 [P] [US2] Add conversation variants for all Pilates pains in `data/landing/niches/pilates.ts`
- [X] T026 [US2] Implement "Quero que meus agentes cuidem de" block in `components/landing/sections/IntentSelectorSection.tsx`
- [X] T027 [US2] Ensure intent selection emits `pain_selected` from `components/landing/sections/IntentSelectorSection.tsx`
- [X] T028 [P] [US2] Add problem mode data for `Sem agentes` and `Com agentes` in `data/landing/niches/pilates.ts`
- [X] T029 [US2] Implement diagnosis toggle and cards in `components/landing/sections/ProblemDiagnosisSection.tsx`
- [X] T030 [P] [US2] Implement slider/control primitives for calculator in `components/landing/shared/MoneyPanelMockup.tsx`
- [X] T031 [US2] Redesign Dinheiro na Mesa in `components/landing/sections/MoneyCalculatorSection.tsx`
- [X] T032 [US2] Preserve full calculator logic in `lib/landing/money-calculator.ts` while simplifying visible controls
- [X] T033 [US2] Ensure calculator emits `calculator_started` and `calculator_result_updated` from `components/landing/sections/MoneyCalculatorSection.tsx`
- [X] T034 [P] [US2] Implement `AgentWorkspaceMockup` in `components/landing/shared/AgentWorkspaceMockup.tsx`
- [X] T035 [P] [US2] Add workspace data for all seven agents in `data/landing/niches/pilates.ts`
- [X] T036 [US2] Implement only the `Selecione o agente` component in `components/landing/sections/AgentsDemoSection.tsx`
- [X] T037 [US2] Ensure agent selection emits `agent_selected` from `components/landing/sections/AgentsDemoSection.tsx`
- [X] T038 [US2] Remove standalone agent-workflow section from `components/landing/NicheLandingPage.tsx`
- [X] T039 [US2] Verify all four interactions on desktop and mobile using `specs/001-niche-landing-system/quickstart.md`

**Checkpoint**: Primary product proof blocks approved.

---

## Phase 5: User Story 3 - Visual Product Trust: Screens, Flows and Illustrations (Priority: P1)

**Goal**: Add believable conversation screens, SaaS/system screens, flows and illustrations that make the product feel real and specific.

**Independent Test**: Review each visual proof block and confirm every mockup/illustration has a purpose and a Pilates-specific message.

- [X] T040 [P] [US3] Implement consolidated operations panel in `components/landing/shared/PriorityQueueMockup.tsx`
- [X] T041 [P] [US3] Implement student history/evolution panel in `components/landing/shared/StudentHistoryMockup.tsx`
- [X] T042 [P] [US3] Implement human approval screen in `components/landing/shared/HumanApprovalMockup.tsx`
- [X] T043 [P] [US3] Implement custom-agent builder screen in `components/landing/shared/CustomAgentBuilderMockup.tsx`
- [X] T044 [US3] Redesign `components/landing/sections/HowItWorksSection.tsx` as a premium guided flow
- [X] T045 [US3] Redesign `components/landing/sections/CoverageSection.tsx` around the consolidated operations panel
- [X] T046 [US3] Add Pilates-specific illustration panel to `components/landing/sections/NicheSpecificSection.tsx`
- [X] T047 [US3] Add custom-agent illustration + mini UI in `components/landing/sections/CustomAgentSection.tsx`
- [X] T048 [US3] Add human approval mockup in `components/landing/sections/HumanControlSection.tsx`
- [X] T049 [US3] Add premium plan/subscription illustration/offering treatment in `components/landing/sections/EarlyAccessSection.tsx`
- [X] T050 [US3] Verify visual consistency across conversation, SaaS, flow and illustration components

**Checkpoint**: Visual proof system approved.

---

## Phase 6: User Story 4 - Multi-Niche Reusability (Priority: P2)

**Goal**: Ensure future niches can reuse the landing system without rewriting page structure.

**Independent Test**: Inspect code and optionally add a minimal second niche config to prove the renderer can reuse sections.

- [X] T051 [P] [US4] Normalize landing config types in `data/landing/niches/types.ts` for hero, intent, diagnosis modes, visual assets and agent workspaces
- [X] T052 [US4] Update `data/landing/niches/pilates.ts` to match normalized types
- [X] T053 [US4] Ensure section components consume props/config rather than importing Pilates data directly
- [X] T054 [P] [US4] Add developer notes for adding a second niche in `specs/001-niche-landing-system/quickstart.md`
- [X] T055 [US4] Run a code audit to confirm visible Pilates copy is not hardcoded in shared components

**Checkpoint**: Multi-niche architecture preserved.

---

## Phase 7: User Story 5 - Modular Reviewability (Priority: P2)

**Goal**: Keep the landing maintainable, reviewable and safe to iterate.

**Independent Test**: A reviewer can find and edit any section or visual mockup without touching a giant page file.

- [X] T056 [US5] Reduce `components/landing/NicheLandingPage.tsx` to orchestration only
- [X] T057 [US5] Ensure shared components have focused responsibilities in `components/landing/shared/`
- [X] T058 [US5] Ensure each section owns one page block in `components/landing/sections/`
- [X] T059 [US5] Remove unused legacy helpers from `components/landing/NicheLandingPage.tsx`
- [X] T060 [US5] Run `npm run lint` and `npm run build`

**Checkpoint**: Implementation structure is ready for long-term iteration.

---

## Final Phase: Polish & Cross-Cutting Verification

**Purpose**: Validate quality gates before commit/PR.

- [X] T061 Run prohibited public-copy audit across `data/landing`, `components/landing`, `app/pilates` and `app/layout.tsx`
- [X] T062 Capture 1440px screenshot of `/pilates` in `tmp/screenshots/`
- [X] T063 Capture 390px screenshot of `/pilates` in `tmp/screenshots/`
- [X] T064 Verify no horizontal body overflow at 390px using browser measurement
- [X] T065 Verify all required tracking events include landing context
- [X] T066 Update `specs/001-niche-landing-system/checklists/requirements.md` after implementation review
- [X] T067 Commit completed approved implementation changes with a focused git commit

---

## Commercial Repositioning Phase: Sell The Vertical SaaS Through The Consultor

**Purpose**: Update the completed landing from niche-validation and analysis-first positioning to consultor-led vertical SaaS sales. The main landing must not send cold visitors directly to plans/checkout as the primary action.

- [X] T068 Update Pilates niche config in `data/landing/niches/pilates.ts` from analysis/access-early framing to direct plan/subscription framing
- [X] T069 Update pricing plan types for Base, 1 Agente, 3 Agentes and 7 Agentes in `data/landing/niches/types.ts`
- [X] T070 Update Pilates pricing config in `data/landing/niches/pilates.ts`: Base R$ 197/mes, 1 Agente R$ 497/mes, 3 Agentes R$ 897/mes, 7 Agentes R$ 1.497/mes recommended
- [X] T071 Add trusted plan/subscription CTA destinations to `data/landing/niches/types.ts` and `data/landing/niches/pilates.ts`
- [X] T072 Replace legacy offer-section messaging with plan/subscription messaging or create `PlansSection` in `components/landing/sections/`
- [ ] T073 Ensure plan cards show fit, included agents, WhatsApp availability, setup expectation, usage boundary and consultor-first CTA on `/pilates`
- [X] T074 Replace analysis-first form messaging with analysis/human WhatsApp assisted-conversion messaging in `components/landing/sections/DiagnosisFormSection.tsx` or successor section
- [ ] T075 Update hero and final CTA copy to make consultor-led diagnosis/recommendation the primary action
- [X] T076 Add or update tracking event support for `plan_cta_clicked` with plan payload and `human_whatsapp_clicked` with selected/interested plan in `lib/landing/tracking.ts`
- [X] T077 Verify public copy no longer uses access-early or niche-validation framing
- [X] T078 Verify plan/subscription CTA does not collect card data and routes only to trusted configured destinations
- [X] T079 Verify the landing never marks CTA click/subscription intent as active paid subscription
- [ ] T080 Capture updated 1440px and 390px screenshots after commercial repositioning
- [X] T081 Add privacy/consent helper text to assisted-conversion forms and WhatsApp assistance CTAs
- [X] T082 Add or verify privacy notice/policy link from footer or form area
- [X] T083 Verify forms do not request sensitive student health details or unnecessary personal data
- [X] T084 Verify tracking/form payloads include conversion purpose/context and avoid full raw free-text storage where structured metadata is enough
- [X] T085 Configure stable plans page `/pilates/planos` in the Pilates landing config
- [ ] T086 Ensure hero, final CTA and plan-interest CTAs open/continue the consultor; only explicit plan-comparison or consultor handoffs route to `/pilates/planos`
- [X] T087 Implement `/pilates/planos` page with hero, plan cards, comparison table, fit guidance, FAQ, assisted WhatsApp CTA and final CTA
- [X] T088 Verify `/pilates/planos` shows Base, 1 Agente, 3 Agentes and 7 Agentes with 7 Agentes visually recommended
- [X] T089 Verify `/pilates/planos` uses trusted pricing/checkout configuration and does not hardcode prices or checkout URLs
- [X] T090 Verify `/pilates/planos` at 1440px and 390px with no horizontal overflow
- [X] T091 Verify viewing/comparing plans does not create checkout or active subscription state
- [X] T092 Define stable guided demo page `/pilates/demonstracao` in the Pilates landing config
- [X] T093 Specify `/pilates/demonstracao` content: scenario selector, guided steps, real SaaS demo surfaces, controls and consultor handoff
- [ ] T094 Verify guided demo handoff opens/continues the consultor with selected pain, scenario and completed-step context
- [X] T094a Gate the public guided-demo CTA/page launch until the real SaaS demo environment supports the demonstrated workflows
- [X] T095 Verify `/pilates` does not route cold visitors directly to checkout as its default conversion path
- [X] T096 Define CTA entry metadata for widget, Falar com consultor, Continuar no WhatsApp and Demonstracao guiada
- [ ] T097 Verify each CTA starts the consultor with the correct tone and context
- [ ] T098 Ensure guided demo shows studio setup preview, agent setup preview, live SaaS demo operation, system record, human control and consultor bridge
- [X] T099 Ensure the landing makes high-ticket risk reducers visible or reachable before checkout
- [X] T100 Verify every `/pilates` CTA either opens the consultor/WhatsApp, routes to an existing page, or is gated by trusted readiness config; no CTA may point to 404
- [X] T101 Verify `/pilates/planos` exists before any public plan-comparison destination is enabled
- [X] T102 Verify guided-demo CTAs stay hidden or reroute to consultor/WhatsApp/product explanation while `guidedDemoReady=false`
- [X] T103 Verify the 30-day guarantee, payment-data safety, studio-owned WhatsApp, setup help and usage hard caps are visible or reachable before checkout
- [ ] T104 Preserve the accepted `/pilates` layout and verify only integration points before launch: hero/header/final CTA wiring, consultor-first entry metadata, guided-demo gating, plan-comparison routing, WhatsApp handoff copy, risk reducers and responsive screenshots. Do not redesign, reorder or restyle the landing unless explicitly requested.
- [ ] T105 Specify and implement the Agente sob medida diagnostic composer as a real textarea/report generator, not placeholder-only UI
- [ ] T106 Ensure the diagnostic report renders classifications `mapped_solution`, `custom_agent`, `mixed_solution` and `unclear` with distinct commercial CTAs
- [ ] T107 Ensure `mapped_solution` report CTAs open consultor, guided demo when ready/gated, or WhatsApp with diagnostic context for the normal SaaS subscription funnel
- [ ] T108 Ensure `custom_agent` report CTAs open consultor or WhatsApp in custom-agent proposal mode and ask for more operation details/contact
- [ ] T109 Track diagnostic submit/result/CTA events with source section, classification, mapped agents and safe custom-agent summary
- [ ] T110 Verify the diagnostic report never routes directly to checkout and still respects plan-display, guided-demo and checkout gates
- [ ] T111 Limit the landing FAQ to the 8 canonical high-impact questions defined in the consultor entry matrix
- [ ] T112 Add the final "ficou alguma duvida?" FAQ CTA that opens the consultor with `entryPath=widget` and `sourceSection=faq_doubt_cta`
- [ ] T113 Verify the FAQ doubt CTA starts neutral/helpful and does not route directly to plans or checkout

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1 Setup: starts immediately.
- Phase 2 Foundational: depends on Phase 1 and blocks all visual work.
- Phase 3 US1: depends on Phase 2.
- Phase 4 US2: depends on Phase 2; can start after hero direction is approved if work is split.
- Phase 5 US3: depends on Phase 2 and benefits from US2 visual primitives.
- Phase 6 US4: depends on Phase 2 and should be revisited after US2/US3 data needs are known.
- Phase 7 US5: depends on all section extraction work.
- Final Phase: depends on desired stories being complete.

### Suggested MVP Scope

MVP for the next implementation pass:
1. Phase 1
2. Phase 2
3. Phase 3
4. Phase 4 through T039

Stop after this MVP for user visual review before implementing proof/illustration sections.

### Parallel Opportunities

- T005 and T006 can run in parallel.
- T010-T016 can be split across files once shared boundaries are agreed.
- T024/T025/T028/T030/T034/T035 can run in parallel after foundational extraction.
- T040-T043 can run in parallel because each creates a different visual mockup component.

## Implementation Strategy

1. Do not continue visual patching inside the monolithic page file.
2. Componentize first.
3. Rebuild one block at a time.
4. Capture screenshots after each P1 block.
5. Ask for visual approval at checkpoints.
6. Commit only approved cohesive changes.
