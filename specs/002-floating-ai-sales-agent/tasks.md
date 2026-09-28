# Tasks: Floating AI Attendant

**Input**: Design documents from `/specs/002-floating-ai-sales-agent/`
**Prerequisites**: plan.md, spec.md, research.md, architecture.md, runtime-configuration.md, custom-agent-diagnostic-report.md, eval-plan.md, eval-fixtures-spec.md, human-whatsapp-handoff.md, whatsapp-e2e-readiness.md, internal-sales-inbox.md, privacy-consent.md, data-model.md, contracts/

**Tests**: Required verification is lint, build, public-copy audit, responsive screenshots, keyboard/mobile walkthrough and guided/adversarial conversation checks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare contracts, read required docs and avoid disturbing existing landing changes.

- [X] T001 Confirm working tree status and identify unrelated existing changes with `git status --short`
- [X] T002 Read Next.js local docs for Client Components and Route Handlers in `node_modules/next/dist/docs/`
- [X] T003 Read current landing source of truth in `specs/001-niche-landing-system/spec.md` and `docs/landing-agentes-pilates/source/`
- [X] T004 Review current landing orchestrator in `components/landing/NicheLandingPage.tsx`
- [X] T005 Review existing niche config and type structure in `data/landing/niches/types.ts` and `data/landing/niches/pilates.ts`
- [X] T006 Review existing tracking utility in `lib/landing/tracking.ts`
- [X] T007 Review Front/Back/IA architecture map in `specs/002-floating-ai-sales-agent/architecture.md`
- [X] T008 Review attendant role matrix in `specs/002-floating-ai-sales-agent/agent-roles.md`
- [X] T009 Review implementation-level role details in `specs/002-floating-ai-sales-agent/agent-role-details.md`
- [X] T010 Review role review decisions in `specs/002-floating-ai-sales-agent/agent-role-review.md`
- [X] T011 Review n8n automation map in `specs/002-floating-ai-sales-agent/n8n-automation-map.md`
- [X] T093 Review human WhatsApp handoff rules in `specs/002-floating-ai-sales-agent/human-whatsapp-handoff.md`
- [X] T094 Review privacy/consent requirements in `specs/002-floating-ai-sales-agent/privacy-consent.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Add shared types, configuration, safe conversation primitives and the required live AI route before UI stories.

- [X] T012 Add floating agent config types to `data/landing/niches/types.ts`
- [X] T013 Add Pilates floating agent config, quick replies and pain-to-agent mapping to `data/landing/niches/pilates.ts`
- [X] T086 Add commercial config references for plans, prices, recommended plan, checkout URLs and human WhatsApp assistance destination to `data/landing/niches/types.ts`
- [X] T087 Ensure Pilates floating agent config reads plan/pricing data from the shared system configuration in `data/landing/niches/pilates.ts`
- [X] T014 [P] Create request/response schemas in `lib/landing/ai-attendant/schema.ts`
- [X] T015 [P] Create context builder in `lib/landing/ai-attendant/context.ts`
- [X] T016 [P] Create OpenAI provider wrapper in `lib/landing/ai-attendant/provider.ts`
- [X] T017 [P] Create guardrail classification helpers in `lib/landing/ai-attendant/guardrails.ts`
- [X] T018 [P] Create fallback response helpers in `lib/landing/ai-attendant/fallback.ts`
- [X] T019 [P] Create handoff summary helper in `lib/landing/ai-attendant/summarize.ts`
- [X] T020 [P] Create n8n webhook dispatch helper in `lib/landing/ai-attendant/n8n.ts`
- [X] T021 Create conversation engine helpers in `lib/landing/floating-agent.ts`
- [X] T022 Extend tracking event typing/metadata support in `lib/landing/tracking.ts`
- [X] T023 Create required live AI route boundary in `app/api/landing/ai-attendant/route.ts`
- [X] T024 Add server-side AI request/response validation in `app/api/landing/ai-attendant/route.ts`
- [X] T025 Add baseline guided conversation fixtures in `specs/002-floating-ai-sales-agent/evals/guided-conversations.md`
- [X] T026 Add adversarial conversation fixtures in `specs/002-floating-ai-sales-agent/evals/guardrails.md`
- [X] T027 Add role-specific eval fixtures from `agent-role-details.md` in `specs/002-floating-ai-sales-agent/evals/role-behavior.md`
- [X] T028 Create conversion routing helper in `lib/landing/ai-attendant/conversion.ts`
- [X] T029 Add trusted guided-demo, plans, checkout, analysis and human WhatsApp destination fields to floating agent config in `data/landing/niches/types.ts`
- [X] T030 Add Pilates conversion destinations and CTA labels to `data/landing/niches/pilates.ts`
- [X] T031 Add structured conversion path fields to request/response schemas in `lib/landing/ai-attendant/schema.ts`
- [X] T032 Add conversion eval fixtures for guided demo, plan recommendation, checkout intent, analysis request and human WhatsApp assist in `specs/002-floating-ai-sales-agent/evals/conversion-paths.md`
- [X] T088 Add pricing/config alignment eval fixtures in `specs/002-floating-ai-sales-agent/evals/pricing-config.md`

**Checkpoint**: Data contract, live AI route, playbook, guardrails and tracking vocabulary are ready.

---

## Phase 2b: WhatsApp Channel Foundation (Blocking Prerequisites)

**Purpose**: Add the WhatsApp channel boundary before user-facing stories depend on a single-channel web assumption.

- [X] T033 Create shared channel types and normalization helpers in `lib/landing/ai-attendant/channels.ts`
- [X] T034 Create server-side session/idempotency store abstraction in `lib/landing/ai-attendant/session-store.ts`
- [X] T035 Create official Meta WhatsApp Cloud API provider adapter in `lib/landing/ai-attendant/whatsapp.ts`
- [X] T036 Create WhatsApp inbound webhook route in `app/api/landing/ai-attendant/whatsapp/route.ts`
- [X] T037 Add provider verification using signature, token or shared secret in `app/api/landing/ai-attendant/whatsapp/route.ts`
- [X] T038 Add duplicate inbound message protection by provider message ID in `lib/landing/ai-attendant/session-store.ts`
- [X] T039 Normalize WhatsApp inbound turns into the same AI attendant request contract used by `app/api/landing/ai-attendant/route.ts`
- [X] T040 Add WhatsApp opt-out detection and automated-reply stop behavior in `lib/landing/ai-attendant/guardrails.ts`
- [X] T041 Add channel-aware tracking events for WhatsApp inbound, reply sent and delivery failed in `lib/landing/tracking.ts`
- [X] T042 Add WhatsApp conversation eval fixtures in `specs/002-floating-ai-sales-agent/evals/whatsapp-channel.md`
- [X] T089 Add server-side usage/cost logging schema and helper for AI requests and WhatsApp sends
- [X] T090 Add rate limit, daily cap, timeout and live-AI kill-switch configuration for the attendant routes

**Checkpoint**: Web and WhatsApp can share the same AI attendant core without duplicating the agent brain.

---

## Phase 3: User Story 1 - Visitor Opens The Floating Agent (Priority: P1) MVP

**Goal**: Deliver the visible floating entry and accessible chat shell.

**Independent Test**: Visit `/pilates` at 1440px and 390px, open/close the widget, verify it does not cover critical landing controls or create overflow.

- [X] T043 [P] [US1] Create floating button component in `components/landing/shared/FloatingAiAttendantButton.tsx`
- [X] T044 [P] [US1] Create chat panel shell in `components/landing/shared/FloatingAiAttendantPanel.tsx`
- [X] T045 [US1] Create stateful floating agent container in `components/landing/shared/FloatingAiAttendant.tsx`
- [X] T046 [US1] Render `FloatingAiAttendant` from `components/landing/NicheLandingPage.tsx`
- [X] T047 [US1] Add responsive fixed-position styling and mobile-safe spacing in `app/globals.css` or component classes
- [X] T048 [US1] Verify keyboard open/close, focus return and touch targets in `components/landing/shared/FloatingAiAttendant.tsx`
- [X] T049 [US1] Capture minimized/open screenshots at 1440px and 390px under `tmp/screenshots/`
- [X] T049a Redesign the widget display modes `minimized_idle`, `minimized_attention`, `minimized_active`, `opening_transition`, `open_desktop`, `open_mobile`, `typing_loading`, `error_fallback` and `handoff_cta` so each is visually clear, premium and functional
- [X] T049b Verify the minimized widget is understandable as consultor/atendimento within 5 seconds and does not look like an unexplained phone/chat ad
- [X] T049c Capture desktop, mobile and short-viewport screenshots for every widget display mode after the redesign

**Checkpoint**: The floating agent shell is visible, usable and visually aligned with the reference.

---

## Phase 4: User Story 2 - Agent Answers Questions And Sells Consultatively (Priority: P1)

**Goal**: Make the agent answer doubts, explain the product, ask pains and map pains to operational agents.

**Independent Test**: Run guided and free-text pain prompts and confirm correct agent recommendations.

- [X] T050 [P] [US2] Implement initial greeting and quick reply rendering in `components/landing/shared/FloatingAiAttendantPanel.tsx`
- [X] T051 [US2] Connect quick replies and message submit to `lib/landing/floating-agent.ts`
- [X] T052 [US2] Send normal free-text messages through `app/api/landing/ai-attendant/route.ts` from `components/landing/shared/FloatingAiAttendant.tsx`
- [X] T053 [US2] Implement pain detection and pain-to-agent recommendation metadata handling in `lib/landing/floating-agent.ts`
- [X] T054 [US2] Render recommended agents and next questions in `components/landing/shared/FloatingAiAttendantPanel.tsx`
- [X] T055 [US2] Apply guardrail decisions before and after assistant responses in `components/landing/shared/FloatingAiAttendant.tsx`
- [X] T056 [US2] Verify supported pain prompts from `specs/002-floating-ai-sales-agent/evals/guided-conversations.md`

**Checkpoint**: The agent can sell the system through a guided, Pilates-specific conversation.

---

## Phase 5: User Story 3 - Agent Converts Or Hands Off To The Right Path (Priority: P1)

**Goal**: Convert qualified chat intent into guided demo, plan recommendation, checkout intent, analysis request, human WhatsApp assistance or custom-agent follow-up.

**Independent Test**: Complete guided demo, consultor-led plan recommendation, checkout intent, analysis-intent and human WhatsApp paths; confirm each handoff payload includes conversion path and safe context.

- [X] T057 [P] [US3] Add conversion path decision flow in `lib/landing/floating-agent.ts`
- [X] T058 [US3] Add guided demo, plan recommendation, checkout intent, analysis and human WhatsApp CTA states in `components/landing/shared/FloatingAiAttendantPanel.tsx`
- [X] T059 [US3] Implement conversion handoff callback in `components/landing/shared/FloatingAiAttendant.tsx`
- [X] T060 [US3] Integrate handoff with guided demo destination, plans destination, checkout destination, analysis anchor and WhatsApp assistance destination in `components/landing/NicheLandingPage.tsx`
- [X] T061 [US3] Emit floating-agent tracking events through `lib/landing/tracking.ts`
- [X] T062 [US3] Send analysis, high-intent and human WhatsApp assistance webhooks through `lib/landing/ai-attendant/n8n.ts`
- [X] T063 [US3] Verify handoff payload includes `niche`, `sourcePage`, `campaignStage`, `publicOfferMode`, `channel`, `conversionPath`, selected pain, recommended agents and summary
- [X] T095 Ensure human WhatsApp handoff includes safe summary, trusted destination, selected/interested plan and AI pause/reduced-automation state
- [X] T096 Ensure contact capture explains purpose and links/displays privacy consent copy before submission

**Checkpoint**: The chat diagnoses first, routes to demo/plans/checkout when appropriate and produces qualified assisted-close opportunities when needed.

---

## Phase 6: User Story 4 - Conversation Stays Safe, Accurate And Brand-Aligned (Priority: P2)

**Goal**: Harden the mandatory live AI boundary, safety and fallback behavior without weakening the landing.

**Independent Test**: Run adversarial prompts and provider-failure conditions; verify safe redirects and fallback responses.

- [X] T064 [P] [US4] Implement prompt-injection, unsupported-claim, sensitive-data and off-topic guardrail cases in `lib/landing/ai-attendant/guardrails.ts`
- [X] T065 [US4] Add fallback response states to `lib/landing/floating-agent.ts`
- [X] T066 [US4] Add provider-failure, timeout and missing-credential handling in `app/api/landing/ai-attendant/route.ts`
- [X] T067 [US4] Send safety/fallback webhook through `lib/landing/ai-attendant/n8n.ts` for repeated or severe events
- [X] T068 [US4] Ensure the client uses guided fallback only when the live AI route fails or blocks unsafe input in `components/landing/shared/FloatingAiAttendant.tsx`
- [X] T069 [US4] Verify adversarial prompts from `specs/002-floating-ai-sales-agent/evals/guardrails.md`
- [X] T070 [US4] Audit visible chat copy against prohibited public terms

**Checkpoint**: The agent is safe enough for public landing traffic and resilient when live AI is unavailable.

---

## Final Phase: Polish & Cross-Cutting Verification

**Purpose**: Validate quality gates before commit or PR.

- [X] T071 Run `npm run lint`
- [X] T072 Run `npm run build`
- [X] T073 Run public-copy audit across visible floating-agent strings in `data/landing`, `components/landing`, `app/pilates` and `app/layout.tsx`
- [X] T074 Verify no horizontal body overflow at 390px with the widget minimized and open
- [X] T075 Verify all floating-agent tracking events include landing context and channel
- [X] T076 Verify normal free-text chat requests use the live AI route
- [X] T077 Verify n8n webhook failures do not block chat or conversion handoff
- [X] T078 Verify mobile keyboard behavior and small viewport chat readability
- [X] T079 Verify role-specific evals in `specs/002-floating-ai-sales-agent/evals/role-behavior.md`
- [X] T080 Verify WhatsApp inbound message produces one safe AI attendant reply through the configured provider adapter
- [X] T081 Verify duplicate WhatsApp webhook delivery does not duplicate replies, tracking or n8n handoffs
- [X] T082 Verify WhatsApp opt-out stops automated replies for that contact/session
- [X] T083 Verify checkout CTA uses trusted configured destination, appears only after explicit intent/recommendation and the chat never asks for card/payment data
- [X] T084 Verify human WhatsApp assistance path includes safe assisted-closing summary
- [X] T085 Update `specs/002-floating-ai-sales-agent/checklists/requirements.md` if implementation changes scope
- [X] T091 Verify pricing answers use current system configuration and update when configured plan data changes
- [X] T092 Verify rate limits, daily cap, timeout, usage logging and live-AI degraded mode
- [X] T097 Verify human handoff does not continue selling as if AI were the human closer
- [X] T098 Verify privacy/consent copy appears before contact capture and n8n receives safe summary, not full raw transcript by default

---

## Scope Refresh: Premium Sales And Buyer Q&A

**Purpose**: Capture the latest commercial decision that the attendant must answer buyer questions deeply and sell the configured recommended/highest-value plan as the default fit for broad needs.

- [X] T099 Update server AI context/prompt rules so the agent answers purchase-relevant questions before returning to conversion
- [X] T100 Update conversion/plan recommendation logic so broad or multi-agent needs prioritize the configured recommended/highest-value plan
- [X] T101 Update fallback replies so lower plans are framed as comparison, budget-fit or narrow-scope options, not equal default recommendations
- [X] T102 Add/verify eval coverage for buyer Q&A, recommended/highest-value plan recommendation and lower-plan objection handling
- [X] T103 Verify web widget and WhatsApp produce the same answer policy and plan recommendation for equivalent buyer questions
- [X] T104 Verify visible chat copy does not need repeated AI labeling while privacy/consent transparency remains available before contact capture
- [X] T113 Add plan-comparison intent handling so "ver planos" routes to the configured plans destination
- [X] T114 Add UI action/event for the chat to navigate to `/pilates/planos` without losing chat session after consultor-led or explicit plan-comparison intent
- [X] T115 Verify plan-comparison tracking is separate from checkout/subscription CTA tracking
- [X] T134 Add guided-demo intent handling so "quero ver como funciona" routes to the configured `/pilates/demonstracao` destination
- [X] T135 Add UI action/event for the chat to navigate to `/pilates/demonstracao` without losing chat session
- [X] T136 Verify guided-demo tracking is separate from plan-comparison and checkout intent tracking
- [X] T136a Gate guided-demo CTA visibility/agent routing behind real SaaS demo-environment readiness; before readiness, route to consultor/WhatsApp/product explanation instead of a fake demo
- [X] T137 Add initial entry-path metadata handling for the core widget, consultor CTA, WhatsApp CTA and guided demo paths
- [X] T138 Add opening-message rules for each entry path so the agent does not use one generic greeting everywhere
- [X] T139 Add plan-display gates so `/pilates/planos` is offered only after explicit plan interest, enough context, demo recommendation/completion or visitor insistence
- [X] T140 Add checkout gates so checkout is offered only after explicit buying intent, confirmed recommendation, intentional plans-page action or operator-assisted close
- [X] T141 Add high-ticket sales sequence rules for pain, impact, proof/demo, recommendation, lower-plan comparison, objections/risk reducers and checkout
- [X] T142 Add risk-reducer answer coverage for post-payment next step, studio-owned WhatsApp, setup help, human control, plan changes when configured, usage caps, cancellation/contract when configured and payment-data safety
- [X] T143 Add eval cases for entry-path openings, plan gates, checkout gates, guided-demo completion and high-ticket risk reducers
- [X] T144 Wire `commercial-sales-playbook.md` into prompt/context generation after trusted runtime configuration
- [X] T145 Add eval fixtures for every objection matrix row in `commercial-sales-playbook.md`
- [X] T146 Add lead priority/readiness calculation for hot, warm, cold, curious, diagnosing, proof_needed, plan_ready, checkout_ready, assisted_close and custom_agent_mapping
- [X] T147 Add follow-up eligibility rules so n8n follow-up requires contact permission and stops on opt-out, won, lost or do-not-contact
- [X] T148 Add WhatsApp template readiness checklist and block proactive out-of-window follow-up until approved templates exist
- [X] T149 Add metrics events for the full conversion funnel from landing viewed to onboarding completed and lead won/lost
- [X] T150 Add WhatsApp template drafts from `whatsapp-template-copy.md` to provider setup checklist and verify no proactive follow-up sends without approved template
- [X] T116 Wire `approved-answer-knowledge.md` into the server AI context after trusted runtime configuration
- [X] T117 Add eval cases for unknown buyer questions so the agent says what is not confirmed and routes safely instead of inventing
- [X] T151 Verify approved answers cover price, plan differences, 7 Agentes recommendation, setup, studio-owned WhatsApp, hard caps, 30-day guarantee, cancellation/refund boundary, post-payment next step, payment failure and Agente sob medida
- [X] T152 Add lead identity metadata to every conversion path: `leadId`, `sessionId`, `channel`, `entryPath`, `sourcePage`, selected pains, recommended agents, interested/recommended plan, consent and safe summary
- [X] T153 Verify widget and WhatsApp merge only through strong identifiers: explicit `leadId`, WhatsApp provider contact, normalized WhatsApp, email or explicit session continuation token
- [X] T154 Block production claim of same-number WhatsApp human takeover unless the protected Sales Inbox and operator reply surface are enabled

---

## Scope Refresh: Lead Visibility

**Purpose**: Ensure qualified conversations are visible to the SaaS operator in one lead pipeline instead of disappearing into tracking or alerts.

- [X] T105 Configure Sales Inbox/Postgres as the v1 lead source of truth with the required filters and views
- [X] T106 Add lead storage schema with lead ID, status, priority, channel, conversion path, selected/interested plan, pains, recommended agents, contact fields, summary, next action and consent context
- [X] T107 Store lead records in Sales Inbox/Postgres for guided demo, plan-comparison, analysis, human WhatsApp assistance, custom-agent follow-up, checkout/subscription intent and high-intent contact events
- [X] T108 Add idempotency rules so WhatsApp retries and repeated handoff events update the same lead instead of creating duplicates
- [X] T109 Add daily lead digest and urgent high-intent notifications as secondary alerts, not source of truth
- [X] T110 Verify the operator can open one destination and see all leads filtered by status, priority, channel, conversion path and next action
- [X] T111 Verify Sales Inbox/Postgres remains the durable source for v1 validation
- [X] T112 Add operator notification for optional n8n automation failure without blocking chat/conversion

---

## Scope Refresh: Internal Sales Inbox

**Purpose**: Provide one internal operator control center for all SaaS sales leads who may subscribe, including web widget, WhatsApp, plan-page intent, checkout intent, human handoff and custom-agent follow-up.

- [X] T118 Define Sales Inbox lead conversation schema with statuses `ai_active`, `handoff_requested`, `human_active`, `waiting_customer`, `follow_up_scheduled`, `checkout_sent`, `won`, `lost` and `do_not_contact`
- [X] T119 Define safe merge rules for widget + WhatsApp sessions using WhatsApp, email, explicit `leadId` or explicit `sessionId`, and preventing auto-merge on weak signals only
- [X] T120 Add server-side API to list Sales Inbox leads with safe summary, status, priority, channel, conversion path, interested plan, next action and last activity
- [X] T121 Add server-side API to fetch lead detail with contact, studio, captured pains, recommended agents, custom-agent request, safe summary and recent messages
- [X] T122 Add protected operator action API for `take_over`, `send_whatsapp_message`, `send_plan_page`, `send_checkout_link`, `schedule_follow_up`, `resume_ai`, `mark_waiting_customer`, `mark_won`, `mark_lost`, `mark_do_not_contact` and `edit_lead_summary`
- [X] T123 Ensure operator `send_whatsapp_message` uses the server-side WhatsApp provider adapter and never exposes provider credentials client-side
- [X] T124 Ensure `send_plan_page` and `send_checkout_link` use trusted configured destinations and cannot use model-generated arbitrary URLs
- [X] T125 Pause automated WhatsApp replies while a Sales Inbox lead/session is `human_active`
- [X] T126 Ensure `checkout_sent` and `won` do not mark a lead as paid/subscribed without Spec 3 billing confirmation
- [X] T127 Keep Sales Inbox status/summary/next-action changes in Postgres and emit optional n8n alerts/digests when configured
- [X] T128 Add audit/tracking events for takeover, WhatsApp reply, plan-page send, checkout-link send, resume AI, follow-up, won/lost and do-not-contact actions
- [X] T129 Build minimal protected Sales Inbox UI with list, filters, lead detail, recent messages, action buttons and response composer
- [X] T130 Verify all SaaS sales leads from widget, WhatsApp, plan-page intent, checkout intent, human handoff and custom-agent request appear in the Sales Inbox
- [X] T131 Verify a human can assume and reply on a WhatsApp conversation without duplicate AI replies
- [X] T132 Verify Sales Inbox/n8n optional automation failure records sync failure without blocking operator lead control

---

## Scope Refresh: Supervised Agent Calibration

**Purpose**: Make agent improvement explicit: the sales attendant improves through controlled tests, reviewed changes and evals, not uncontrolled self-learning from live conversations.

- [X] T155 Define the paid-credit validation runbook with budget, scenarios, stop conditions and expected artifacts
- [X] T156 Run supervised buyer conversations for curiosity, product explanation, pains, pricing, objections, plans, checkout, WhatsApp, custom-agent request, unsupported integration, cancellation/guarantee and safety
- [X] T157 Record each failure with entry path, message, expected behavior, actual behavior, lead effect, Sales Inbox effect and cost notes
- [X] T158 Classify failures by prompt/playbook, route gate, fallback, guardrail, lead capture, UI/CTA, Sales Inbox/n8n optional automation or provider/cost
- [X] T159 Apply supervised calibration changes only through source-controlled code, config, playbook docs or eval fixtures
- [X] T160 Re-run affected practical scenarios plus `npm run eval:ai-routes -- --target=http://localhost:3002` after each calibration batch
- [X] T161 Verify no behavior change rewrites plan/pricing, safety rules, checkout gates, lead states or handoff destinations without human review
- [X] T162 Produce a readiness report with scenarios tested, pass/fail summary, corrected issues, remaining blind spots, API cost, lead-sync status and go/no-go for controlled traffic
- [X] T163 Use `agent-readiness-audit-and-100-plan.md` as the readiness source of truth before spending paid OpenAI credits
- [X] T164 Extend route-matrix evals to assert next suggested message, suggested CTA, contact-capture timing, lead effect and live-vs-fallback mode
- [ ] T165 After real demo flows are available, add focused coverage for `chooseNextAction` and `ConversionActions` so the visible next suggestion and CTA cannot drift from the commercial route
- [X] T166 Record Sales Inbox/n8n optional automation dispatch results for web conversion leads in the Sales Inbox sync state
- [X] T167 Run the fixed 20-scenario live AI calibration set under the US$5 validation budget and stop on repeated P0/P1 failure patterns
- [X] T168 Record decision: live AI custom-agent diagnostic is future scope; current Atendente IA 100% readiness excludes it, and deterministic diagnostic/report CTA must not be marketed as live AI diagnosis
- [X] T133 Verify Sales Inbox scope excludes paying-studio student conversations and future SaaS customer inbox behavior

---

## Scope Refresh: Custom Agent Diagnostic Report

**Purpose**: Add the report-style Agente sob medida diagnostic flow as a separate report mode from the chat, so the landing can sell either the existing SaaS subscription or a custom-agent proposal from one free-text diagnostic block. Live AI generation for this report is future scope.

- [X] T180 Add custom-agent diagnostic request/response schemas for `mapped_solution`, `custom_agent`, `mixed_solution` and `unclear`
- [X] T181 Create `app/api/landing/custom-agent-diagnostic/route.ts` using trusted config, guardrails, usage logging and fallback boundaries; live provider-backed report generation is future scope
- [X] T182 Add diagnostic report context/prompt rules that classify existing Taliya coverage before routing to Agente sob medida
- [X] T183 Add report CTA payloads with `contextVariant`: `diagnostic_existing_solution`, `diagnostic_custom_agent`, `diagnostic_mixed_solution` and `diagnostic_unclear`
- [X] T184 Wire mapped-solution report CTAs to consultor, guided demo when ready/gated and WhatsApp continuation with SaaS sales context
- [X] T185 Wire custom-agent report CTAs to consultor/WhatsApp in proposal mode, asking for more operation details/contact before promising follow-up
- [X] T186 Add Sales Inbox lead fields for diagnostic report ID, classification, context variant, mapped agents, custom operation summary and selected CTA
- [X] T187 Add Sales Inbox lead storage support and optional n8n alerts for `custom_agent_diagnostic_mapped`, `custom_agent_follow_up`, `mixed_subscription_plus_custom` and `custom_agent_diagnostic_unclear`
- [X] T188 Add eval fixtures for mapped request, custom marketing request, mixed request, unclear request, demo gating and no-direct-checkout report behavior
- [X] T189 Verify diagnostic report tracking events include classification, report ID, context variant and safe summary without unnecessary raw text storage
- [X] T190 Add FAQ doubt CTA support so `sourceSection=faq_doubt_cta` opens the normal widget flow with neutral opening, tracks `faq_doubt_cta_clicked` and does not route directly to plans/checkout
- [ ] T191 Future scope: specify and implement live AI custom-agent diagnostic generation with deterministic fallback and dedicated evals before marketing that block as an AI-powered diagnostic

---

## Scope Refresh: Conversation Route Matrix Evals

**Purpose**: Convert the route-level conversation matrix into golden conversations before validating or refining the implemented agent.

- [X] T192 Add route-matrix eval fixtures for entry routes, discovery, pricing, demo, checkout, WhatsApp handoff, custom-agent, risk reducers, failures and lead effects
- [X] T193 Update the eval plan and fixture spec so `conversation-route-matrix.md` is a required pre-launch eval file

---

## Scope Refresh: CRM-first Diagnostic And Widget Attention

**Purpose**: Reframe the diagnostic and widget entry so the public funnel sells Taliya as a complete operational CRM with integrated AI agents, captures buying timing and makes the closed widget more noticeable without redesigning `/pilates`.

- [X] T194 Update all prompt-facing and public-copy source docs that still imply Taliya is not a CRM; the approved rule is CRM operacional completo plus agentes de IA integrados
- [X] T195 Add `crm_agent_diagnostic` entry metadata for the Diagnostico Gratuito CTA, including `entryPath=diagnostic_cta`, `sourceSection=studio_diagnostic`, `leadId` and `sessionId`
- [X] T196 Add diagnostic state fields for name, studio size, pains, daily visibility, replacements, sales follow-up, current system, priority goal, buying timing and contact status
- [X] T197 Implement the diagnostic question flow so the agent asks one short question at a time, extracts multiple answered fields and avoids repeated questions
- [X] T198 Add adaptive follow-up rules for WhatsApp, finance, absences, sales and replacements, with at most one adaptive follow-up before the diagnostic result
- [X] T199 Generate the final diagnostic with studio summary, pains, impact, CRM modules, recommended agents, practical routine, plan recommendation and one dynamic next step
- [X] T200 Extend Sales Inbox lead fields for diagnostic type, CRM pain areas, agent pain areas, buying timing, lead temperature, recommended CRM modules, recommended agents, plan and next step
- [X] T201 Store the new diagnostic fields in Sales Inbox without storing unnecessary raw transcript data
- [X] T202 Add eval fixtures for cold researcher, hot buyer, CRM-only buyer, replacement pain, WhatsApp pain, sales pain, finance pain, broad pain, contact refusal, existing system and human request
- [X] T203 Add closed-widget attention motion: subtle desktop nudge/glow, mobile pulse/badge, max three nudges per session, pause after interaction and `prefers-reduced-motion` support
- [X] T204 Verify desktop and mobile widget attention states with screenshots and confirm they do not cover landing CTAs or change the approved `/pilates` section layout
- [X] T205 Verify the diagnostic CTA wiring preserves the approved `/pilates` visual layout and only changes behavior/metadata/motion
- [X] T205a Add diagnostic-first commercial gate so price, plans, demo, human handoff, objection and checkout intent start/continue the free diagnostic before CTAs

---

## Scope Refresh: AI-first Diagnostic Calibration

**Purpose**: Reflect the approved v1 agent proposal after manual production testing: the agent is a consultative Taliya seller, the free diagnostic is the main funnel, AI interprets free-text answers and side questions, and final agent recommendations stay structured and useful.

- [X] T228 Add AI-based diagnostic turn routing so side questions, price/plan questions, human requests, diagnostic cancellation and custom-agent requests are interpreted during the diagnostic instead of handled only by local case rules
- [X] T229 Verify free-text diagnostic answers advance the current field without requiring quick-reply suggestions or repeating the same question
- [X] T230 Calibrate diagnostic cadence so the agent acknowledges or reflects the visitor's answer before asking the next diagnostic question
- [X] T231 Deliver the final diagnostic in separated steps after a short hold/typing message instead of dumping plan and agents immediately
- [X] T232 Make final plan recommendation dynamic from the diagnostic context and keep plan discussion after CRM base and agent logic
- [X] T233 Render recommended agents one at a time with pain summary, recommendation reason and practical action, and add eval coverage so the cards cannot regress to a flat/partial list

---

## Production Readiness: Persistence

**Purpose**: Replace local/dev memory stores with durable persistence before production WhatsApp, Sales Inbox or same-number human takeover.

- [X] T206 Add persistence readiness contract in `specs/002-floating-ai-sales-agent/persistence-readiness.md`
- [ ] T207 Add storage interfaces for WhatsApp sessions, Sales Inbox leads, operator actions and usage/rate limits
- [ ] T208 Keep current process-local stores only as explicit local-development adapters
- [ ] T209 Add Postgres schema/migrations for WhatsApp sessions, provider message idempotency, Sales Inbox leads, lead messages, operator actions, merge decisions, usage events and rate-limit counters
- [ ] T210 Implement Postgres adapter for Sales Inbox leads, lead messages, operator actions and sync status
- [ ] T211 Implement Postgres adapter for WhatsApp sessions, opt-out and provider message idempotency
- [ ] T212 Persist `human_active` / `aiPaused` state and enforce it before any WhatsApp AI reply
- [ ] T213 Replace process-local rate-limit counters with Redis/KV or Postgres counters that work across instances
- [ ] T214 Persist or ship AI usage events to durable storage/logging without raw full transcripts by default
- [ ] T215 Add restart-safety tests for WhatsApp idempotency, opt-out, human takeover, Sales Inbox lead listing and operator audit history

---

## Production Readiness: WhatsApp E2E

**Purpose**: Turn the local WhatsApp webhook/adapter into a production-safe Meta WhatsApp Cloud API channel for the same Atendente IA and Sales Inbox takeover flow.

- [X] T216 Add WhatsApp E2E readiness contract in `specs/002-floating-ai-sales-agent/whatsapp-e2e-readiness.md`
- [X] T217 Add a Meta webhook E2E test harness for GET challenge, valid signed POST, invalid signature and unsupported payloads
- [X] T218 Verify signed inbound WhatsApp text produces exactly one stored inbound turn, one AI response, one provider send attempt and one usage/tracking event
- [X] T218a Verify duplicate signed inbound WhatsApp text is ignored within the active process-local session store
- [ ] T219 Verify duplicate provider message IDs do not duplicate replies, leads, n8n events or usage events across process restarts
- [ ] T220 Add durable provider delivery/status handling for sent, delivered, read, failed and deleted WhatsApp statuses
- [ ] T221 Add an outbox/retry model for failed AI and operator WhatsApp sends with idempotency keys and retry exhaustion state
- [ ] T222 Enforce WhatsApp service-window/template gating before proactive or out-of-window follow-up sends
- [ ] T223 Connect approved Meta template configuration to `whatsapp-template-copy.md` internal names and block unapproved templates
- [X] T224 Add unsupported WhatsApp media/message-type handling without passing raw payloads to the model
- [ ] T225 Verify Sales Inbox `take_over`, `human_active`, `resume_ai`, `won`, `lost` and `do_not_contact` states suppress or allow AI replies exactly as specified
- [ ] T226 Verify operator `send_whatsapp_message` uses server-side credentials, records audit, records provider result and stays retryable on failure
- [ ] T227 Run a live Meta E2E smoke test with real app/test number/webhook URL through AI reply, human takeover, operator reply, opt-out and n8n lead sync

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1 Setup: starts immediately.
- Phase 2 Foundational: depends on setup and blocks user stories.
- Phase 2b WhatsApp Channel Foundation: depends on foundational schemas and blocks WhatsApp verification.
- Phase 3 US1: depends on foundational config/types.
- Phase 4 US2: depends on US1 shell and foundational conversation helpers.
- Phase 5 US3: depends on US2 conversation state.
- Phase 6 US4: guardrails can start after foundational helpers; route hardening depends on the mandatory route created in Phase 2 and WhatsApp opt-out behavior from Phase 2b.
- Final Phase: depends on desired stories being complete.

### Parallel Opportunities

- T010 through T015 can run in parallel after types are defined because they own separate server modules.
- T028 through T032 can run after config and schemas are stable because they define conversion routing.
- T033 through T036 can run in parallel after schemas are stable because they own separate channel modules.
- T043 and T044 can run in parallel because they own separate UI files.
- T050 and T053 can run in parallel if the message contract is stable.
- T057 and T061 can run in parallel with clear ownership between conversation flow and tracking utility.
- T064 and T066 can run in parallel because guardrails and provider-failure handling are separate files.

## Implementation Strategy

### MVP First

1. Complete Phase 1 and Phase 2.
2. Complete Phase 2b so the channel contract is not retrofitted after web-only assumptions land.
3. Complete Phase 3 to ship the floating entry and empty chat shell.
4. Complete Phase 4 to make the agent useful for selling and pain mapping.
5. Complete Phase 5 to make consultor-led conversion the primary path and WhatsApp human assistance the assisted-close path.
6. Stop for visual/conversation review only after live AI route integration is working.

### Incremental Delivery

1. Floating UI shell.
2. WhatsApp channel webhook/session/idempotency boundary.
3. Guided attendance and commercial conversation.
4. Guided demo, plan recommendation, checkout intent, analysis and human WhatsApp handoff.
5. Guardrails and fallback hardening.
6. Provider-failure hardening for the mandatory server-backed AI route and WhatsApp provider.

### Notes

- Keep shared components reusable by future niche configs.
- Do not hardcode visible Pilates copy in generic floating-agent components.
- Do not let live AI provider failure break the static landing experience.
- Commit planning artifacts before implementation once approved.
