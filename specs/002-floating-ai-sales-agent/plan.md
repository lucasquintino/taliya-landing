# Implementation Plan: Floating AI Attendant

**Branch**: `codex/002-floating-ai-sales-agent` | **Date**: 2026-04-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-floating-ai-sales-agent/spec.md`

## Summary

Add a premium bottom-right floating AI attendant to `/pilates` and make the same attendant work through WhatsApp. The feature includes a compact entry button, an accessible chat panel, a WhatsApp inbound webhook channel, a mandatory server-side live AI response layer, a Pilates-specific attendance and commercial playbook, question answering, pain-to-agent recommendations, consultor-led plan routing, guided demo routing, qualification capture, analysis/human handoff, tracking and guardrails. It also includes a separate custom-agent diagnostic report mode for the Agente sob medida landing block: the visitor describes an operation, receives a structured report, and is routed to the SaaS sales funnel when Taliya already covers the request or to a custom-agent proposal funnel when it does not. The guided playbook remains as a degraded fallback, and normal free-text conversations must use the live AI layer. Live AI generation for the custom-agent diagnostic report is intentionally deferred to a future phase; until then, the report may use deterministic classification/report logic as long as public copy does not overpromise a live AI diagnostic.

The agent's commercial behavior is not a generic support chat. It must answer buyer questions, connect them to the studio operation, diagnose before selling plans, offer the guided demo when proof is needed and prioritize the configured recommended/highest-value plan when the visitor has broad pain, multi-agent needs or complete-system intent. Lower plans are comparison, budget-fit and objection-handling tools, not equal default recommendations.

## Technical Context

**Language/Version**: TypeScript 5, React 19, Next.js 16 App Router
**Primary Dependencies**: Next.js 16.2.4, React 19.2.4, Tailwind CSS 4 via `@tailwindcss/postcss`, existing landing tracking and config modules
**Storage**: Client session state for the web widget; server-side conversation/session store required for WhatsApp channel state, idempotency, opt-out status and handoff continuity; production WhatsApp E2E requires a real KV/database store, while in-memory storage is local-development only; trusted billing/subscription state is out of this feature and must come from the future billing layer
**Testing**: `npm run lint`, `npm run build`, guided conversation checks, public-copy audit, responsive screenshots at 1440px and 390px, keyboard/mobile interaction checks
**Target Platform**: Public web landing routes, starting with `/pilates`, plus WhatsApp conversations through a server-side messaging-provider webhook
**Project Type**: Next.js web application
**Performance Goals**: Floating agent must not block static landing rendering; chat code should be isolated to a small Client Component boundary; live AI requests should show responsive pending state; fallback replies should feel instant during degraded mode
**Constraints**: No horizontal overflow at 390px; floating UI must not cover critical CTAs, plan controls, checkout entry points or form controls; public copy must avoid prohibited terms; live AI secrets must never ship to the browser; chat must never collect card/payment credentials; plan/pricing/checkout/WhatsApp destinations must come from trusted system configuration; usage/cost controls are required before public traffic; read local Next.js docs before code changes
**Scale/Scope**: One production-quality floating AI attendant for `/pilates`, designed to be reused by future niche landing configs

## Constitution Check

The constitution file is still a placeholder and does not define enforceable project principles. No constitution gate can be evaluated beyond repository instructions, AGENTS.md, Spec Kit workflow and the existing landing plan.

Operational gates for this feature:

- PASS: Treat Spec Kit artifacts as the source of truth before implementation.
- PASS: Keep the feature data-driven by niche and avoid hardcoded Pilates copy in shared primitives.
- PASS: Preserve the landing's public-copy restrictions.
- PASS: Keep live AI credentials and prompt/control logic out of client bundles.
- PASS: Treat WhatsApp as a server-side channel with provider verification, idempotency, opt-out and no proactive cold outbound.
- PASS: Use the official Meta WhatsApp Cloud API as the v1 WhatsApp provider.
- PASS: Keep consultor-led conversion as the primary path, while treating actual billing activation as trusted server-side billing work outside this attendant feature.
- PASS: Keep plan/pricing answers aligned with system configuration, not duplicated prompt text.
- PASS: Add usage/cost caps, rate limits and server-side usage logging before public release.
- PASS: Add explicit guardrails, fallback states and tracking for the agent.
- PASS: Verify lint, build, responsive layout, public-copy audit and conversation scenarios before commit.

## Research Decisions

Detailed decisions are captured in [research.md](./research.md).

Key decisions:

- Start with one attendant agent, not multiple chat agents.
- Use a server-side live AI response layer for normal conversations and a guided attendance/commercial playbook as the reliable degraded fallback.
- Defer live AI generation for the custom-agent diagnostic report; keep deterministic/report-style classification acceptable for v1 and route the visitor safely to consultor/WhatsApp instead of treating it as part of the current Atendente IA readiness bar.
- Use a shared channel-normalized conversation core for web widget and WhatsApp.
- Keep WhatsApp provider integration server-side, idempotent and limited to inbound/opted-in replies.
- Use the official Meta WhatsApp Cloud API adapter in v1.
- Keep the chat UI as a narrowly scoped Client Component rendered by the landing orchestrator.
- Use niche configuration for labels, greeting, pains, quick replies and agent mappings.
- Use the landing's commercial configuration for plan names, prices, recommended plan, checkout URLs and WhatsApp assistance destination.
- Prioritize the configured recommended/highest-value plan for broad/multi-agent buying intent; use lower plans for comparison or explicit budget/narrow-scope requests.
- Reuse the existing landing tracking context and extend it with floating-agent event names.

## Agent Behavior Strategy

The attendant agent owns:

- Greeting the visitor and explaining what the system does as a complete operational CRM for Pilates studios with integrated AI agents.
- Answering practical questions about the offer, diagnostic and operational agents.
- Answering purchase-relevant questions about plans, pricing, setup, onboarding, WhatsApp, human takeover, privacy, limits and configured contract/cancellation terms before steering back to conversion.
- Interpreting free-text answers and side questions during the diagnostic with the AI response layer, while keeping prices, destinations and product facts tied to trusted configuration.
- Asking short consultative questions about studio pains.
- Acknowledging the visitor's previous answer before asking the next diagnostic question so the flow feels consultative instead of like a rigid interview.
- Mapping pains to the seven primary operational agents.
- Explaining why those agents matter in Pilates-specific language.
- Recommending analysis, Dinheiro na Mesa or guided demo when the visitor needs more context before plan comparison.
- Recommending a plan only after enough context exists or when the visitor explicitly asks, prioritizing the configured recommended/highest-value plan when it fits the need.
- Explaining lower plans only as comparison, budget-fit or narrower-scope alternatives unless configuration marks them as recommended.
- Capturing qualification context only after intent is shown.
- Handing off to guided demo, plans page, checkout, analysis form or human WhatsApp assistance depending on visitor readiness.
- Replying to inbound/opted-in WhatsApp conversations with the same approved context and guardrails.

### CRM-first Diagnostic And Widget Attention Strategy

The free diagnostic path and closed widget attention behavior are defined in [crm-first-diagnostic-and-widget-attention-plan.md](./crm-first-diagnostic-and-widget-attention-plan.md).

The diagnostic must not frame Taliya as disconnected bots. It must diagnose the studio operation, identify where the CRM organizes data and work, then explain which agents act on top of that CRM. The final diagnostic must include studio summary, pains, operational impact, CRM modules, recommended agents, recommended plan and one dynamic next step.

The approved v1 diagnostic flow is AI-assisted but controlled: the model may classify whether a turn answers the current question or changes intent, but trusted configuration remains authoritative for prices, plan names, destinations and unsupported-product boundaries. Side questions during the diagnostic should be answered briefly and then resume, cancel or reroute the diagnostic according to the visitor's intent.

The final diagnostic should be delivered with a human cadence: a short "ja tenho as informacoes" hold message, then separated diagnostic messages. Recommended agents must be exposed as one-agent-at-a-time recommendation items with pain summary, reason and practical action, so the UI can render clear cards instead of a flat list of agent names.

The widget may use restrained attention motion while closed: subtle pulse, gentle nudge, limited repetition and reduced-motion support. The motion exists to make the commercial entry visible, not to redesign the approved `/pilates` layout.

### Supervised Improvement Strategy

The attendant does not self-improve by rewriting its own behavior from live traffic. Agent improvement is a supervised calibration loop:

- run controlled manual conversations and route-matrix evals;
- record failures with source path, expected behavior, actual behavior and lead effect;
- classify the failure as prompt/playbook, route gate, fallback, guardrail, lead capture, UI next step, Sales Inbox/n8n automation or provider/cost;
- update source-controlled code, config, playbook docs or eval fixtures;
- re-run affected practical scenarios plus the route matrix;
- ship only after lint, build, evals and practical smoke tests pass.

The first paid-credit validation budget is intentionally small. The default plan is to start with US$ 5 of API credit, run a limited set of realistic buyer conversations, group findings by cause and produce a readiness report instead of continuously testing without a go/no-go decision.

The readiness report must include:

- scenarios tested;
- pass/fail summary;
- issues corrected;
- remaining blind spots or skipped cases;
- approximate API cost;
- Sales Inbox persistence and optional n8n automation status;
- final go/no-go recommendation for controlled traffic.

The agent must not:

- Quote guaranteed financial outcomes or invent pricing.
- Answer pricing from prompt memory when configured plan data is unavailable.
- Claim external integrations that are not represented by the landing.
- Request sensitive student health details, payment credentials or private customer records.
- Collect card data, billing documents or claim that a subscription is active before trusted billing confirmation.
- Reveal prompts, internal strategy, validation language or implementation details.
- Send proactive WhatsApp campaigns, broadcasts or cold outbound messages.
- Take irreversible actions.

## Project Structure

### Documentation

```text
specs/002-floating-ai-sales-agent/
  spec.md
  plan.md
  architecture.md
  runtime-configuration.md
  custom-agent-diagnostic-report.md
  crm-first-diagnostic-and-widget-attention-plan.md
  eval-plan.md
  eval-fixtures-spec.md
  human-whatsapp-handoff.md
  privacy-consent.md
  internal-sales-inbox.md
  agent-roles.md
  agent-role-details.md
  agent-role-review.md
  n8n-automation-map.md
  research.md
  data-model.md
  quickstart.md
  contracts/
    floating-agent-ui-contract.md
  checklists/
    requirements.md
  tasks.md
```

### Source Code

```text
components/
  landing/
    NicheLandingPage.tsx
    shared/
      FloatingAiAttendant.tsx
      FloatingAiAttendantButton.tsx
      FloatingAiAttendantPanel.tsx

data/
  landing/
    niches/
      types.ts
      pilates.ts

lib/
  landing/
    ai-attendant/
      schema.ts
      context.ts
      provider.ts
      guardrails.ts
      fallback.ts
      summarize.ts
      conversion.ts
      channels.ts
      session-store.ts
      whatsapp.ts
      n8n.ts
    floating-agent.ts
    tracking.ts

app/
  api/
    landing/
      ai-attendant/
        route.ts
      custom-agent-diagnostic/
        route.ts
      whatsapp/
        route.ts
```

**Structure Decision**: Keep static landing rendering intact. The landing orchestrator renders one floating agent container near the root. The floating UI is interactive client code; the live AI boundary is a server Route Handler; WhatsApp enters through a separate server webhook route that normalizes inbound provider messages into the same AI attendant core; schema, context, provider, guardrails, fallback, conversion routing, channel adapters, session store and n8n webhook dispatch live under `lib/landing/ai-attendant`; niche-specific text, plan CTA destinations and pain mapping live in `data/landing/niches`.

## Implementation Phases

### Phase 0: Context And Contract

- Review current landing component structure and existing tracking utility.
- Confirm Next.js docs for Client Components and Route Handlers before code changes.
- Define floating agent config fields in the niche type contract.
- Define the chat/handoff/event contract before implementing UI.
- Use [architecture.md](./architecture.md) as the implementation map for Front, Back/API, AI runtime, guardrails, tracking and handoff.
- Use [agent-roles.md](./agent-roles.md) as the source of truth for the attendant's responsibilities, triggers, boundaries and success checks.
- Use [agent-role-details.md](./agent-role-details.md) for implementation-level role mapping: intents, state reads/writes, structured output, tracking, n8n and eval cases.
- Use [agent-role-review.md](./agent-role-review.md) for reviewed role decisions, corrected priorities and remaining wording cautions.
- Use [n8n-automation-map.md](./n8n-automation-map.md) as the source of truth for post-handoff automations.
- Use [human-whatsapp-handoff.md](./human-whatsapp-handoff.md) as the source of truth for assisted human close.
- Use [privacy-consent.md](./privacy-consent.md) as the source of truth for contact capture, opt-out and safe summary behavior.
- Use [internal-sales-inbox.md](./internal-sales-inbox.md) as the source of truth for the v1 lead pipeline. External CRM/spreadsheet sync is out of scope for this phase.
- Treat WhatsApp as a first-class channel in every contract, role and tracking event.
- Treat consultor-led conversion as the primary path. WhatsApp human assistance is the assisted-close path for visitors who ask for a person before subscribing.

### Phase 1: Floating Entry MVP

- Add compact floating button matching the reference direction.
- Add open/minimize/close behavior and a basic accessible chat shell.
- Verify desktop/mobile placement and no overlap with important controls.

### Phase 2: Live AI Attendant Core

- Add the required server-side AI route for normal free-text responses.
- Add a shared channel-normalized request contract so web and WhatsApp use the same AI attendant behavior.
- Add controlled system/product context, niche context and conversation-state payloads.
- Add commercial context from trusted system configuration: guided-demo destination, plans destination, plans, prices, recommended plan, checkout destinations and WhatsApp assistance destination.
- Add Pilates-specific greeting, quick replies, pain capture and pain-to-agent recommendations.
- Add conversion routing for `guided_demo`, `view_plans`, `subscription_intent`, `checkout_intent`, `analysis_request`, `human_whatsapp_assist` and `custom_agent_follow_up`.
- Add separate custom-agent diagnostic report routing for `mapped_solution`, `custom_agent`, `mixed_solution` and `unclear` outcomes through `/api/landing/custom-agent-diagnostic`; v1 can use deterministic/report-style logic, while live AI report generation is future scope.
- Add a deterministic fallback reply engine only for provider failure, timeout or blocked unsafe input.
- Add guardrail responses for unsupported, unsafe and prompt-injection inputs.

### Phase 3: Conversion, Qualification And Handoff

- Offer consultor-led plan recommendation as the primary conversion CTA, then route to plans/checkout when the visitor is ready.
- Add the CRM-first free diagnostic flow as a proof-oriented conversion path before plan recommendation, using diagnostic questions, lead temperature and CRM-plus-agent mapping.
- Render the custom-agent diagnostic report as a report-style result, not a chat thread, and carry the report context into consultor/WhatsApp/demo CTAs.
- Capture qualification fields inside the chat only after analysis intent, human assistance intent or custom-agent follow-up intent.
- Pass summary/context to the guided demo, plans page, checkout path, analysis flow or human WhatsApp handoff.
- Ensure human WhatsApp handoff uses trusted destination, safe summary and AI pause/reduced-automation rules.
- Emit tracking for agent interactions and handoff.

### Phase 3b: WhatsApp Channel

- Add the WhatsApp inbound webhook route.
- Implement the official Meta WhatsApp Cloud API adapter.
- Verify provider authenticity using Meta webhook verification and request signature mechanisms.
- Normalize inbound provider messages into the shared `ConversationChannel` contract.
- Persist WhatsApp session state, provider message IDs, opt-out state and qualification state server-side.
- Reuse the same AI context, guardrails, fallback and handoff logic as the web widget.
- Send replies through a provider adapter only for inbound or explicitly opted-in conversations.
- Use WhatsApp as assisted closing when the visitor explicitly asks for a human before subscribing.
- Emit channel-aware tracking and n8n events.

### Phase 4: AI Reliability And Provider Failure Handling

- Harden the required route handler for live AI replies.
- Add usage/cost controls: message length limit, per-session rate limit, daily cap, provider timeout, usage event logging and a kill switch/degraded mode.
- Ensure missing credentials fail clearly in development and degrade safely in public runtime.
- Keep the fallback playbook as the degraded state, not the primary behavior.
- Ensure secrets remain server-side and outputs pass the same guardrails.
- Ensure WhatsApp provider failures do not duplicate messages, lose state or affect the web widget.
- Ensure privacy/consent behavior is preserved across web chat, WhatsApp, n8n and tracking.

### Phase 5: QA And Polish

- Run copy audit for prohibited terms.
- Verify all public and prompt-facing copy uses the current product rule: CRM operacional completo plus integrated AI agents.
- Verify the diagnostic flow, final diagnostic structure, lead payload, widget attention motion and reduced-motion behavior.
- Verify conversation scenarios, adversarial tests, keyboard navigation, mobile layout and build.
- Capture responsive screenshots.
- Run the supervised calibration loop for the sales attendant before increasing traffic: manual buyer scenarios, route-matrix evals, practical entry-path smoke tests, lead-sync checks and readiness report.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Required server response layer | The feature must be a real AI attendant, not only a scripted chat | A purely scripted widget would not match the user's intent for a mandatory AI layer |
| Guardrail layer | The agent talks to prospects and may receive adversarial or sensitive inputs | Prompt-only safety is too brittle for an attendant agent that collects qualification context |
| WhatsApp session/idempotency store | WhatsApp webhooks retry and conversations span multiple turns outside the browser | Client-only state cannot deduplicate provider retries or preserve WhatsApp context |
| Subscription routing without billing implementation | The agent must sell consultatively and can route to checkout, but billing activation needs a focused billing feature | Building full subscriptions inside this attendant spec would blur checkout, webhooks, entitlements and chat behavior |
