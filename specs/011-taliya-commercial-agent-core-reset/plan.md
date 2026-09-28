# Implementation Plan - Taliya Commercial Agent Core Reset

Status: proposed plan, not approved for implementation yet.

This plan exists so Spec 011 can be implemented later without re-opening the same architecture debate or drifting back into a giant runner. It does not authorize code changes by itself.

## Technical Goal

Replace the current oversized conversational core with a small LLM-first core that preserves the approved Taliya commercial behavior, product knowledge, Spec 006 product truth, templates, diagnostic, Sales Inbox, widget, and Taliya-owned WhatsApp flows.

The implementation should keep reusable infrastructure and replace the conversation brain.

## Architecture Decision

Use the adjusted architecture defined in `architecture.md`:

`Channel Adapter -> Runtime API -> Turn Gate -> Context Builder -> LLM Conductor -> Contract Validators -> Repair Loop -> Template Renderer -> Persistence/Projection -> Delivery/Outbox`

Normal commercial turns use one LLM conductor call. Extra model calls are limited to repair, low-confidence complex diagnostic reasoning, contradictory context, or eval judging.

Implementation must create a new small core beside `runtime/runner.py`; it must not refactor `runner.py` into the new brain. The legacy runner is quarantined as historical reference, fixture source, or controlled rollback reference only.

## Technical Context

- Runtime language: Python FastAPI service under `services/taliya-agent-runtime`.
- Existing frontend/channel adapters: Next/TypeScript under `lib/landing/ai-attendant`.
- Existing Sales Inbox UI/data path: `components/internal/SalesInboxClient.tsx` and `lib/landing/ai-attendant/sales-inbox-store.ts`.
- Existing official product knowledge: `services/taliya-agent-runtime/app/shared/product_knowledge/`.
- Binding product contracts: `specs/006-crm-operational-core/` for pages, access/subscription, setup, operational agents, modes, navigation, and decisions of cut.
- Existing approved templates: `services/taliya-agent-runtime/app/domains/taliya_commercial/templates.py`.
- Existing validators and schemas should be treated as seeds, not final proof.

## Reuse Plan

Reuse:

- Runtime API shell, HMAC, health/config boundaries.
- Product knowledge source.
- Approved message templates after renderer validation is tightened.
- Memory/persistence primitives after projection consistency is checked.
- Widget and Taliya-owned WhatsApp adapters as transport layers.
- Sales Inbox storage/projection as operational surface.

Replace/quarantine:

- `runtime/runner.py` as the commercial brain.
- Commercial regex/token routing helpers.
- Commercial fast paths.
- Old TS v2 conversation fallback for public widget/WhatsApp traffic.

## Implementation Strategy

1. Build regression/eval harness first from `regression-cases.md` and `eval-plan.md`.
2. Prove real bug regressions fail against the current system before fixes.
3. Create new core modules beside the existing runtime.
4. Define strict versioned schemas before writing conductor logic.
5. Implement Turn Gate and Context Builder.
6. Implement the LLM Conductor with logical specialist roles.
7. Implement validators and one-call repair.
8. Refactor rendering to be mechanical and validation-driven.
9. Persist mandatory trace, runtime events, and Sales Inbox projection from validated state.
10. Capture or confirm `/pilates` desktop/mobile baseline before widget cutover work.
11. Run the new core in shadow mode before it can reply to leads.
12. Cut widget/Taliya WhatsApp to the new core behind a controlled flag.
13. Quarantine legacy runner paths and block old TS fallback.
14. Prove rollback does not re-enable the old deterministic commercial brain as public responder.
15. Run eval gates, no-drift baseline check, rollback check, and product-owner transcript review before full production cutover.
16. Activate the new core for 100% of production traffic with first-hours emergency monitoring and an immediate rollback switch.

## Complexity Gates

Implementation must stop for review if:

- A new module starts owning more than one pipeline responsibility.
- A file approaches roughly 700 lines without a clear split.
- A helper both interprets commercial meaning and produces customer-facing text.
- A deterministic rule routes or answers a commercial turn.
- A renderer default invents semantic content.
- A template variable acts as a hidden full-response field.
- Adapter/Sales Inbox inferred data is promoted to reliable memory without source/confidence.
- An eval can PASS without transcript, decision JSON, validators, model usage, and Sales Inbox projection.
- A real bug fix lacks a red failing test against the current system.
- Commercial logic is added to `runner.py` or old TS v2 public paths.
- Product facts are introduced in prompts, templates, tests, or fallbacks instead of official product knowledge or Spec 006-derived sources.
- Mandatory trace is missing.
- Shadow mode, rollback proof, or first-hours emergency monitoring is skipped before production activation.
- Cost optimization removes model usage from normal commercial turns.

## Protected Areas

Do not change:

- `/pilates` layout, styling, copy, section order, animations, mockups, or visual composition.
- The approved `/pilates` desktop/mobile baseline; widget cutover work must prove no visual/layout drift.
- Multi-tenant model.
- Client/studio WhatsApp integrations.
- Checkout/payment flows.
- Sales Inbox visual design unless separately approved.
- Design System/component library work.
- Client-studio operational CRM agents.
- Demo/video production assets.

## Open Decisions Before Coding

Implementation must wait for confirmation of the decisions listed in `spec.md`, especially:

- One-conductor default versus full multi-agent handoff graph.
- Implementation details for new core beside `runner.py`; in-place `runner.py` refactor is rejected.
- Repair-call budget.
- Diagnostic "CRM base" customer-facing wording.
- Minimum real-model eval suite and budget.
- Shadow-mode sample size.
- Full production cutover, abort criteria, and rollback plan.
- Whether semantic quality verification uses judge, manual review, or both.
