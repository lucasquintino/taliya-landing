# Research: Premium Multi-Niche Landing Page System

## Decision: Use a clean centered hero inspired by Landbot/Rebookly patterns

**Rationale**: The current side-by-side hero felt heavy. The approved direction is headline-first, centered, short subtitle, subtle CTAs and product proof below. This gives the first viewport clarity and confidence.

**Alternatives considered**: Split hero with large interactive panel beside copy. Rejected because it made the hero feel crowded and put the intent selector in the wrong place.

## Decision: Move the intent selector into its own block immediately after the hero

**Rationale**: The selector is important, but it should be the first product interaction after the visitor understands the offer. This matches the user's latest direction and keeps the hero clean.

**Alternatives considered**: Keep selector in hero. Rejected because it conflicts with the new hero benchmark.

## Decision: Use a mode toggle for the diagnosis block

**Rationale**: `Sem agentes` vs `Com agentes` is clearer than the current before/after tabs. It creates immediate contrast and makes the agent value legible.

**Alternatives considered**: Static cards or accordion. Rejected because it is less interactive and less benchmark-level.

## Decision: Redesign Dinheiro na Mesa as a calculator panel with sliders and a teal estimate card

**Rationale**: The approved screenshot has strong conversion clarity: controls left, result right, value large, breakdown below. This is more memorable than a grid of inputs.

**Alternatives considered**: Keep all numeric inputs as basic fields. Rejected because it feels utilitarian and not premium enough.

## Decision: Agents block becomes only `Selecione o agente`

**Rationale**: A focused selector plus workspace mockup is easier to understand and closer to product proof. Extra grids dilute the section.

**Alternatives considered**: Cards plus agent tabs plus mockup. Rejected due to visual noise.

## Decision: Include conversation screens, SaaS/system screens, flows and illustrations

**Rationale**: To beat the references, the page must show a believable product world. Conversations explain agent behavior; SaaS mockups prove there is a system; flows explain operations; illustrations create warmth and vertical specificity.

**Alternatives considered**: Mostly text/cards. Rejected because it feels generic and below target quality.

## Decision: Mine `reference/v0`, but do not use it as source of truth

**Rationale**: v0 may contain useful typography, animation and patterns. The final implementation must still follow this spec, plan and the data-driven architecture.

**Alternatives considered**: Ignore v0 or copy it directly. Both rejected: ignoring wastes useful work; copying risks architecture drift and generic visuals.

## Implementation Audit - 2026-04-29

Current pass replaced the prototype UI with a componentized, data-driven implementation.

Reuse:
- `/pilates` route wiring and metadata pattern.
- `data/landing/niches/pilates.ts` as the niche configuration source.
- `lib/landing/money-calculator.ts` for the calculator model.
- `lib/landing/tracking.ts` for landing event payloads.

Refactor:
- `NicheLandingPage.tsx` is now an orchestrator with state and tracking only.
- Landing content types now include conversation mockups, problem modes, agent workspaces, guided flow steps and visual proof data.

Replace:
- Monolithic visual sections were replaced by files in `components/landing/sections/`.
- Inline helper UI was replaced by files in `components/landing/shared/`.
- The standalone agent-workflow block was removed from the rendered page.

Reference cues applied without copying:
- Clean headline-first hero with centered hierarchy.
- Rebookly/Landbot-like selector rhythm, adapted to Pilates and separated from the hero.
- Calculator with controls on the left and a strong teal money panel on the right.
- Product proof through WhatsApp-style conversations, SaaS panels, approval screens and simple bespoke illustrations.

Validation notes:
- `npm run lint` passed.
- `npm run build` passed.
- Production server returned HTTP 200 for `/pilates`.
- Desktop full-page screenshot captured at `tmp/screenshots/pilates-desktop-full.png`.
- Tablet/mobile-style screenshot captured at `tmp/screenshots/pilates-tablet-long.png`.
- 390px CDP layout measurement returned no horizontal overflow.
- Public-copy prohibited-term audit returned no matches for visible landing source files.
