# Parallel Layout Handoff: Spec 1 Pilates Landing

Purpose: preserve the accepted `/pilates` visual pass and define the integration contract that future work must not break.

The `/pilates` layout/front-end visual direction is considered complete. This handoff is now a protection document, not an invitation to redesign the page.

This handoff is only for the main landing route `/pilates`. It does not require changing the already separated `/pilates/planos`, `/privacidade`, Sales Inbox or agent backend unless a future integration task explicitly touches those areas.

## Protected Layout Rule

- Do not redesign `/pilates`.
- Do not reorder the approved landing sections.
- Do not replace the accepted visual style, spacing, hierarchy, colors, cards, mockups, animations or section composition.
- Do not rewrite copy only to match older specs if the current approved layout already expresses the commercial direction.
- Future changes on `/pilates` are allowed only for CTA wiring, entry metadata, tracking, schema/config alignment, accessibility fixes, bug fixes, route gating, responsive breakage fixes or explicit user-requested visual changes.
- If an implementation task appears to require visual changes, pause and treat it as a scope conflict unless the user explicitly reopens the layout.

## Do Not Break

- Main landing must be consultor-first, not pricing-first.
- Cold visitors must not be sent directly to checkout.
- Cold first-viewport CTAs must not go straight to `/pilates/planos`.
- Demo CTAs must not link to `/pilates/demonstracao` while `guidedDemoReady=false`.
- Every visible CTA must either open the consultor, continue to WhatsApp, route to an existing route, or be gated by readiness config.
- No CTA can point to a 404.
- No public copy can imply beta, MVP, validation, fake demo, incomplete product or direct paid activation from a CTA click.
- No chat/form/landing surface can request card data, payment credentials, student health records or private student details.

## Files The Layout Thread Will Likely Touch

- `components/landing/NicheLandingPage.tsx`
- `components/landing/sections/HeroSection.tsx`
- `components/landing/sections/SalesStartSection.tsx`
- `components/landing/sections/FinalCTASection.tsx`
- `components/landing/sections/*`
- `components/landing/shared/Header.tsx`
- `app/globals.css`
- `data/landing/niches/pilates.ts` for copy/config only when needed

## Files This Thread Should Treat As Funnel Contracts

- `specs/001-niche-landing-system/consultor-entry-matrix.md`
- `specs/001-niche-landing-system/plans-page.md`
- `specs/001-niche-landing-system/guided-demo-page.md`
- `specs/002-floating-ai-sales-agent/spec.md`
- `data/landing/niches/types.ts`
- `data/landing/niches/pilates.ts`
- `components/landing/shared/FloatingAiAttendant.tsx`
- `components/landing/shared/FloatingAiAttendantPanel.tsx`

## CTA Contract For `/pilates`

### Hero Primary CTA

Expected label intent:

```text
Ver como ficaria no meu studio
```

Required behavior:

- Open/focus the consultor, or scroll to the consultor CTA section that opens it.
- Pass `sourceSection` equivalent to `hero_primary` or `sales_cta`.
- Use `entryPath=consultor_cta`.
- Do not route directly to `/pilates/planos`.
- Do not route to checkout.

### Header CTA

Expected label intent:

```text
Falar com consultor
```

Required behavior:

- Open/focus consultor or scroll to the consultor section.
- Do not route directly to checkout.
- If it routes by anchor first, the target section must contain the working consultor open button.

### Final CTA

Expected label intent:

```text
Falar com consultor
```

Required behavior:

- Open/focus the consultor with `sourceSection=final_cta`, or preserve an anchor path that immediately offers the consultor.
- The prompt-style visual can remain, but it must not behave like a fake form unless it actually opens the consultor.

### Continuar no WhatsApp

Required behavior:

- Use the configured `assistedConversion.humanWhatsAppDestination`.
- Preserve a safe sales context in the WhatsApp message when possible.
- Track `human_whatsapp_clicked`.
- Do not imply a human has already assumed unless the visitor chooses the WhatsApp path.

### Ver planos / Comparar planos

Allowed only when:

- visitor explicitly asks for plans;
- the consultor recommends or qualifies the visitor;
- visitor insists on seeing prices;
- visitor reaches the dedicated `/pilates/planos` page intentionally.

If a visual plan teaser exists on `/pilates`, its primary CTA should open consultor with plan interest context. Full comparison belongs on `/pilates/planos`.

### Demonstracao Guiada

Current config:

```text
guidedDemoReady=false
```

Required behavior now:

- hide the CTA, or
- open consultor with `entryPath=guided_demo`, or
- route to WhatsApp/product explanation.

Forbidden now:

- linking cold visitors to `/pilates/demonstracao`;
- showing a fake/static demo as if it were the real SaaS.

## Risk Reducers That Must Be Visible Or Reachable Before Checkout

These can appear in FAQ, plans teaser, consultor answers, final CTA microcopy or `/pilates/planos` links:

- 30-day guarantee for public monthly plans.
- Payment details are handled only by the secure payment provider.
- The paying studio uses its own connected WhatsApp for operational agents.
- Setup is self-guided with consultor/agent help and starts in a few minutes after confirmed payment.
- Humans can control, review, pause or assume when needed.
- AI messages are hard capped by plan; no surprise over-limit usage.
- Base plan is CRM only with zero active AI agents.
- Agente sob medida is separate and not included in public plans.

## Remaining Spec 1 Tasks Owned By The Layout Thread

- T073: If `/pilates` shows plan cards or a plan teaser, ensure cards show fit, included agents, WhatsApp availability, setup expectation, usage boundary and consultor-first CTA.
- T075: Make hero and final CTA copy/action clearly consultor-led.
- T080: Capture final 1440px and 390px screenshots after commercial repositioning.
- T086: Ensure hero, final CTA and plan-interest CTAs open/continue consultor.
- T097: Verify every CTA starts the consultor with correct tone/context.
- T104: After the parallel layout review is complete, revisit CTAs, demo gates, WhatsApp copy, risk reducers and screenshots before launch.

## Remaining Spec 1 Tasks Not Owned By The Layout Thread Yet

- T094: Verify guided demo handoff opens/continues the consultor with selected pain, scenario and completed-step context. This waits for the real demo implementation.
- T098: Ensure guided demo shows studio setup preview, agent setup preview, live SaaS demo operation, system record, human control and consultor bridge. This waits for the real SaaS demo environment.

## Final QA Checklist For `/pilates`

Run after the visual pass:

1. Open `/pilates` at 1440px.
2. Open `/pilates` at 390px.
3. Confirm no horizontal overflow.
4. Click hero primary CTA and confirm consultor opens or the page lands on a working consultor CTA.
5. Click header CTA and confirm consultor path.
6. Click final CTA and confirm consultor path.
7. Click WhatsApp CTA and confirm configured WhatsApp destination.
8. Search all visible CTAs and confirm none point to `/pilates/demonstracao` while `guidedDemoReady=false`.
9. Confirm no default CTA sends a cold visitor straight to checkout.
10. Confirm risk reducers are visible or reachable before checkout.
11. Confirm `/pilates/planos` still returns 200.
12. Confirm `/privacidade` still returns 200.
13. Run `npm run lint`.
14. Run `npm run build`.

Suggested screenshots:

- `tmp/screenshots/pilates-commercial-desktop.png`
- `tmp/screenshots/pilates-commercial-mobile.png`

## Acceptance Summary

The layout pass is successful when `/pilates` looks final, but the commercial behavior still follows this path:

```text
visitor arrives
  -> understands promise/pains/proof
  -> opens consultor or WhatsApp
  -> consultor diagnoses
  -> consultor routes to demo/plans/checkout only when gated
  -> risk reducers are answerable before checkout
```
