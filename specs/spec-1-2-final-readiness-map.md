# Spec 1 + Spec 2 Final Readiness Map

## Purpose

This document is the closing checklist for Spec 1 (`001-niche-landing-system`) and Spec 2 (`002-floating-ai-sales-agent`) before implementation work resumes.

It does not replace the specs. It maps:

- what the current specs promise;
- what already exists in code today;
- what still needs to be implemented later;
- implementation priority;
- likely files/modules to touch.

## Source of Truth

Spec 1 and Spec 2 are the current authority for the landing + AI sales attendant experience.

The source docs under `docs/landing-agentes-pilates/source/` are legacy planning inputs. When they mention "acesso antecipado", validation-first positioning, beta access, or conflict with Spec 1/2, they must be treated as historical context, not implementation authority.

Current commercial direction:

- The landing sells the vertical SaaS for Pilates.
- The `/pilates` layout is accepted and protected; future changes on that route are integration/CTA/schema/tracking fixes only, not visual redesign.
- The preferred conversion path is consultor-first, not direct pricing-first.
- The AI attendant must guide, diagnose, answer objections, recommend plans, route to guided demo, and continue on WhatsApp.
- The studio can subscribe only after a clear buying intent and payment completion.
- Custom AI agents are a separate business line and are not included in public SaaS plans.

## Closing Checklist

| Area | What The Spec Promises | What Exists In Code Today | What Still Needs To Be Implemented Later | Priority | Likely Files |
|------|-------------------------|---------------------------|-------------------------------------------|----------|--------------|
| Commercial positioning | Landing sells the vertical SaaS, not early access or niche validation. | Main landing copy is mostly SaaS-oriented, but legacy source docs still reference early access. | Remove or ignore early-access implementation references when they conflict with Spec 1/2; keep source docs marked as legacy. | P0 | `specs/001-niche-landing-system/spec.md`, `docs/landing-agentes-pilates/source/*`, `data/landing/niches/pilates.ts` |
| Six entry paths | Visitor can enter through normal widget, consultant CTA, WhatsApp CTA, guided demo, custom-agent diagnostic, and FAQ doubt CTA. | Widget, consultant, WhatsApp, plans/guided-demo concepts exist partially. FAQ and custom diagnostic are not fully wired as entry paths. | Normalize all six paths in schema, tracking, UI openers, handoff metadata, and eval cases. | P0 | `lib/landing/ai-attendant/schema.ts`, `components/landing/shared/FloatingAiAttendant.tsx`, `lib/landing/tracking.ts`, `specs/002-floating-ai-sales-agent/conversation-route-matrix.md` |
| FAQ + final CTA | FAQ should have at most 8 high-impact questions and a final "ficou alguma duvida?" CTA that opens the normal agent flow. | FAQ renders all configured questions and has no final CTA. | Select the top 8 FAQ items, add final CTA, track `faq_doubt_cta_clicked`, open widget with FAQ source context. | P0 | `components/landing/sections/FAQSection.tsx`, `data/landing/niches/pilates.ts`, `lib/landing/tracking.ts` |
| Entry schema + tracking | Every conversion entry must preserve origin, section, CTA variant, lead id and handoff context. | Schema/tracking cover older paths and common events, but not all custom diagnostic/FAQ events. | Add missing entry-path enum values, tracking events, handoff fields, and regression fixtures. | P0 | `lib/landing/ai-attendant/schema.ts`, `lib/landing/tracking.ts`, `lib/landing/ai-attendant/route-matrix.ts`, `specs/002-floating-ai-sales-agent/tasks.md` |
| AI attendant behavior | Agent must sell consultor-first, answer objections, recommend the highest-value configured plan when appropriate, and avoid early checkout pressure. | AI/fallback logic exists and route/eval coverage exists, but older direct-checkout behavior was identified previously. | Ensure every plan/subscription request goes through diagnosis/proof/recommendation before checkout gate, unless explicit buying confirmation exists. | P0 | `lib/landing/ai-attendant/*`, `app/api/landing/ai-attendant/route.ts`, `specs/002-floating-ai-sales-agent/agent-roles.md` |
| Sales playbook and objection quality | Agent must handle real buyer objections and still move toward the correct sale. | `commercial-sales-playbook.md` exists with objection coverage and sales metrics. | Add/verify evals for price, receptionist, small studio, distrust of AI, "vou pensar", WhatsApp continuation, agenda-only, setup fear, plan comparison, immediate subscription, custom-agent and unsupported integration. | P0 | `specs/002-floating-ai-sales-agent/commercial-sales-playbook.md`, `specs/002-floating-ai-sales-agent/evals/*`, `lib/landing/ai-attendant/*` |
| Shared commercial configuration | Landing, plans page, agent, WhatsApp and Sales Inbox must use one trusted source for prices, plans, caps and destinations. | Trusted configuration is specified; implementation still needs final cross-check. | Remove duplicate hardcoded plan/price/destination copies and make config changes propagate across all commercial surfaces. | P0 | `data/landing/niches/pilates.ts`, `lib/landing/ai-attendant/*`, `app/pilates/planos/page.tsx`, `app/internal/sales-inbox/*` |
| Widget to WhatsApp continuity | A lead moving from widget to WhatsApp must preserve context or avoid unsafe merge. | Lead identity and merge rules exist in specs; production persistence is still pending. | Carry `leadId`/session/contact continuation into WhatsApp, merge only on strong identifiers and keep uncertain matches operator-reviewable. | P0 | `components/landing/shared/FloatingAiAttendant.tsx`, `app/api/landing/whatsapp/*`, `lib/landing/ai-attendant/sales-inbox-store.ts`, `lib/landing/ai-attendant/lead-sync.ts` |
| Widget UI modes | Widget must have clear display modes: idle, attention, active, opening, open desktop, open mobile, typing, error, handoff. | Floating button/panel exist, but modes are not yet formalized as a clean UI state system. | Implement mode model, responsive behavior, polished visual states, motion, sound, and no visible "IA" labeling when not needed. | P1 | `components/landing/shared/FloatingAiAttendant.tsx`, `components/landing/shared/FloatingAiAttendantPanel.tsx`, `components/landing/shared/FloatingAiAttendant.css` |
| Custom-agent diagnostic | User can type any requested operation; system returns a report, classifies whether existing SaaS agents cover it, and routes to SaaS sale or custom-agent proposal. | Custom-agent config exists, but there is no complete report UI/API flow yet. | Create diagnostic form/report, classifier, CTAs, tracking, Sales Inbox effects, optional n8n alerts, and consultor/WhatsApp variants. | P0 | `components/landing/sections/CustomAgentSection.tsx`, `app/api/landing/custom-agent-diagnostic/route.ts`, `lib/landing/custom-agent-diagnostic/*`, `data/landing/niches/pilates.ts` |
| Custom diagnostic sales quality | Diagnostic result must feel like a report and lead to SaaS sale or custom-agent proposal. | Report spec exists; UI/API implementation is incomplete. | Make report classification, impact, recommended path and CTA variants strong enough to sell, with no direct checkout shortcut. | P0 | `specs/002-floating-ai-sales-agent/custom-agent-diagnostic-report.md`, `components/landing/sections/CustomAgentSection.tsx`, `app/api/landing/custom-agent-diagnostic/route.ts` |
| Protected `/pilates` landing layout | Main landing layout is accepted as the current visual source of truth. | User confirmed the `/pilates` layout has been corrected and should not be redesigned. | Only make integration/CTA/schema/tracking/accessibility/bug-fix changes on `/pilates`; do not reorder, restyle or replace sections without explicit user request. | P0 | `specs/001-niche-landing-system/parallel-layout-handoff.md`, `components/landing/NicheLandingPage.tsx`, `components/landing/sections/*`, `data/landing/niches/pilates.ts` |
| SEO and metadata | Landing and plans page must capture qualified organic demand without legacy early-access positioning. | Metadata needs final implementation audit. | Add/verify title, description, OG, canonical, heading hierarchy, descriptive links and no beta/early-access metadata. | P1 | `app/pilates/page.tsx`, `app/pilates/planos/page.tsx`, `data/landing/niches/pilates.ts`, `specs/001-niche-landing-system/spec.md` |
| Plans and pricing | Public plans are Base, 1 Agente, 3 Agentes and 7 Agentes; 7 Agentes is recommended; no trial; 30-day guarantee. | Plans page/config exists, but needs final cross-check against the latest commercial definitions. | Verify plan names, prices, recommended flag, included agents, CTA copy, no-trial copy, guarantee copy, and quota language. | P1 | `app/pilates/planos/page.tsx`, `components/landing/plans/*`, `data/landing/niches/pilates.ts`, `specs/003-billing-subscriptions-entitlements/*` |
| Checkout boundary | Chat can guide to checkout only after explicit purchase intent; plan activates only after payment confirmation. | Checkout is not fully integrated; current behavior should remain a safe consultor/billing placeholder. | Later integrate Billing Spec with payment confirmation, webhooks, entitlements, and inactive-on-failed-payment behavior. | P2 | `app/api/billing/*`, `lib/billing/*`, `specs/003-billing-subscriptions-entitlements/*` |
| Guided demo | Guided demo must be the real SaaS experience, built after the SaaS exists, and can be offered by all main paths. | Demo route is intentionally not ready; config can gate it. | Keep CTA gated until real SaaS screens exist; later build guided demo with agent support and sales routing. | P2 | `app/pilates/demonstracao/*`, `components/demo/*`, `data/landing/niches/pilates.ts` |
| WhatsApp | WhatsApp is another channel for the same sales agent; Taliya has its own WhatsApp; human can take over. | WhatsApp webhook route and test harness exist, but production env/persistence remain pending. | Configure official WhatsApp provider, durable sessions, idempotency, opt-out, human takeover and Sales Inbox continuity. | P1 | `app/api/landing/whatsapp/*`, `lib/landing/ai-attendant/session-store.ts`, `lib/landing/ai-attendant/sales-inbox-store.ts` |
| Production readiness gate | Real production behavior must not rely on dev memory stores, missing provider envs or placeholder credentials. | Local/dev implementation can exist, but production envs and durable persistence are still pending. | Do not claim production-ready WhatsApp, Sales Inbox, human takeover, billing activation, n8n automation or live AI behavior until durable persistence and official provider envs are configured and verified. | P0 | `specs/002-floating-ai-sales-agent/persistence-readiness.md`, `specs/002-floating-ai-sales-agent/runtime-configuration.md`, `specs/005-security-code-data/spec.md`, production env/config |
| WhatsApp templates | Proactive/out-of-window WhatsApp follow-up must use approved Meta templates. | Template drafts exist in Spec 2. | Submit/approve templates in Meta, connect approved names/categories to runtime config and block unapproved sends. | P2 | `specs/002-floating-ai-sales-agent/whatsapp-template-copy.md`, `lib/landing/whatsapp/*`, `lib/landing/n8n.ts` |
| Sales Inbox | Before real SaaS production, team needs controls over leads that want to subscribe. | Internal Sales Inbox exists as a minimal/process-local implementation. | Persist leads/events durably, add lead status controls, handoff summaries, WhatsApp continuity, and operational filters. | P1 | `app/internal/sales-inbox/*`, `lib/landing/ai-attendant/sales-inbox-store.ts`, `lib/landing/ai-attendant/lead-sync.ts` |
| Human takeover controls | Same-number WhatsApp human takeover must pause AI and be operator-controlled. | Spec and minimal Sales Inbox behavior exist; production durability remains pending. | Enforce `human_active`, `resume_ai`, terminal states, audit events and server-side provider replies in durable storage. | P1 | `app/internal/sales-inbox/*`, `app/api/landing/whatsapp/*`, `lib/landing/ai-attendant/sales-inbox-store.ts` |
| n8n automations | n8n supports optional urgent alerts, digests and follow-up automation, not lead storage or real-time conversation handling. | n8n dispatch helper exists; lead storage is in Sales Inbox/Postgres. | Define production alert/digest workflows, retry behavior and diagnostic-report notification payloads only if needed. | P1 | `lib/landing/ai-attendant/n8n.ts`, `docs/*`, `specs/002-floating-ai-sales-agent/data-model.md` |
| Funnel metrics | Operator must know which paths create conversations, plan intent, checkout intent and wins. | Required metrics are defined in playbook/checklists. | Implement event collection/reporting by entry path, channel, plan interest, diagnostic classification and won/lost outcome. | P1 | `lib/landing/tracking.ts`, `specs/002-floating-ai-sales-agent/commercial-sales-playbook.md`, Sales Inbox analytics and optional n8n dashboards |
| Agent role docs | Role docs must match the current six-path sales strategy and custom diagnostic behavior. | `agent-roles.md` and `agent-role-details.md` had stale four-path assumptions. | Keep them aligned with Spec 2 whenever route matrix or behavior changes. | P1 | `specs/002-floating-ai-sales-agent/agent-roles.md`, `specs/002-floating-ai-sales-agent/agent-role-details.md` |
| QA/E2E | Final QA must validate user paths from landing arrival to qualified conversion or subscription intent. | Lint/build/eval harnesses exist; browser E2E and visual QA are still pending for the final page. | Run full E2E after implementation and layout stabilization: desktop/mobile, widget, FAQ CTA, WhatsApp, diagnostic report, plans and handoff. | P1 | `specs/commercial-e2e-qa-checklist.md`, `tests/*`, `scripts/*`, Browser QA |
| QA evidence package | Launch must preserve evidence that the full flow works. | E2E checklist lists evidence to capture. | Capture screenshots, transcripts, WhatsApp samples, Sales Inbox detail and optional n8n alert payload samples before public launch. | P1 | `tmp/screenshots/*`, `specs/commercial-e2e-qa-checklist.md`, QA artifacts |
| Security, code and data | Cross-cutting security requirements must exist outside individual feature specs. | New Spec 5 defines the security baseline. | Review future landing/SaaS/billing/onboarding implementation against Spec 5 before production. | P0 | `specs/005-security-code-data/spec.md`, future implementation plans |

## Future Implementation Order

1. FAQ and final CTA.
2. Entry paths/tracking/schema for the six paths.
3. Widget UI modes.
4. Custom-agent diagnostic report.
5. `/pilates` integration QA only: CTA wiring, metadata, tracking, route gates and responsive bug checks without redesign.
6. QA E2E.

## Definition Of Ready For Implementation

- Spec 1 and Spec 2 are accepted as the current authority.
- This checklist has no unresolved P0 planning contradiction.
- The `/pilates` layout work is complete and protected; implementation must not perform visual redesign unless explicitly requested.
- Desktop and mobile baseline screenshots for `/pilates` are captured or explicitly confirmed before implementation that can affect landing behavior.
- Production readiness is not claimed until durable persistence and official provider envs are configured and verified.
- Any legacy source doc conflict is resolved in favor of Spec 1/2.
- Implementation tasks can be cut from the checklist above without reopening business strategy.
