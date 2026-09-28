# Implementation Plan: Price, Plan And Humanized Agent Experience

**Branch**: `008-price-plan-humanized-agent` | **Date**: 2026-05-20 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `specs/008-price-plan-humanized-agent/spec.md`

## Summary

Refine the Taliya commercial agent so widget and WhatsApp answer price/plans first, treat diagnostic as optional recommendation support, keep direct plan comparison available, pace messages like a human conversation, and expose safe operating state for cost limits, human takeover, lead merge, waitlist quality, priority, media, funnel metrics, handoff and closure.

The technical approach is to keep the existing shared agent engine and add explicit behavior gates, delivery policies and eval matrices around it. The protected `/pilates` layout remains untouched.

## Technical Context

**Language/Version**: TypeScript on the existing Next.js project version in this repository  
**Primary Dependencies**: Existing Next.js app, React widget, PostgreSQL/Supabase storage, WhatsApp Cloud API/Dualhook webhook path  
**Storage**: Existing Sales Inbox/Postgres tables and JSON lead payloads  
**Testing**: Existing Node eval scripts plus new matrix scripts for price/plans and message delivery  
**Target Platform**: Vercel-hosted web app and WhatsApp Business webhook integration  
**Project Type**: Web application with API routes, frontend widget and webhook transport  
**Performance Goals**: Agent replies remain fast enough for chat UX while preserving configured typing/delay pacing; eval suite must run locally without paid WhatsApp traffic  
**Constraints**: Do not modify protected `/pilates` visual layout; do not add multi-tenant onboarding; do not connect customer WhatsApp numbers; do not send WhatsApp templates outside the 24-hour window  
**Scale/Scope**: One Taliya landing/widget, one Taliya WhatsApp Business number, one commercial sales agent, Sales Inbox as lead source of truth

## Constitution Check

The project constitution is still placeholder-only, so no enforceable constitutional gates are defined. Project-specific gates from `AGENTS.md` apply:

- Protected `/pilates` layout must not be redesigned, reordered, restyled or visually altered.
- Existing Spec Kit artifacts and docs must remain the source of truth.
- Functional changes must be verified with automated evals and realistic simulations.

Gate result: PASS with the constraint that implementation must not edit `/pilates` layout or visual styling.

## Project Structure

### Documentation (this feature)

```text
specs/008-price-plan-humanized-agent/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── eval-matrix.md
│   └── sales-inbox-state.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
lib/landing/
├── floating-agent.ts
└── ai-attendant/
    ├── commercial-state.ts
    ├── conversion-gates.ts
    ├── sales-cadence.ts
    ├── whatsapp.ts
    ├── leads.ts
    └── session-store.ts

app/api/
├── landing/ai-attendant/route.ts
├── landing/ai-attendant/whatsapp/route.ts
└── internal/sales-inbox/

app/components or existing widget location
└── floating chat delivery/rendering code

scripts/
├── eval-commercial-conversation-matrix.mjs
├── eval-price-plan-commercial-matrix.mjs
├── eval-message-delivery-matrix.mjs
└── safe cleanup helper for test phone/session if needed
```

**Structure Decision**: Extend the existing shared agent, webhook, widget delivery and Sales Inbox paths. Add eval scripts rather than replacing current test harnesses.

## Phase 0 Research Decisions

See [research.md](./research.md).

## Phase 1 Design Artifacts

- [data-model.md](./data-model.md)
- [quickstart.md](./quickstart.md)
- [contracts/eval-matrix.md](./contracts/eval-matrix.md)
- [contracts/sales-inbox-state.md](./contracts/sales-inbox-state.md)

## Implementation Strategy

1. Add/expand eval matrices first so current gaps are reproducible.
2. Adjust price/plan commercial rules while preserving current diagnostic and waitlist gates.
3. Add delivery pacing/splitting rules to widget and verify WhatsApp still sends split replies with typing.
4. Add operational state handling for limits, human takeover/resumption, merge, waitlist quality, priority, media, funnel metrics, handoff and closure.
5. Review Sales Inbox for visibility of all fields and states.
6. Run full automated gates and local/manual widget checks before deploy.
7. After deploy, run WhatsApp Web real-message tests with per-number cleanup before any public lead capture or paid traffic.

Production readiness rule: a smaller internal MVP may validate price/plans and delivery behavior, but real divulgation or paid lead capture requires the operational guardrails in steps 4-7 to be implemented and verified. Real WhatsApp tests require the deployed public webhook and are therefore post-deploy gates.

## Complexity Tracking

No constitution or project-structure violations identified.

## Post-Design Constitution Check

PASS. The plan keeps visual landing changes out of scope and requires eval/manual gates before release.
