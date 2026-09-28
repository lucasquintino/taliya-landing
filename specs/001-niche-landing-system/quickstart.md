# Quickstart: Premium Multi-Niche Landing Page System

## Local Verification

1. Install dependencies if needed: `npm install`
2. Build: `npm run build`
3. Start production server: `npm run start -- --hostname 127.0.0.1 --port 3000`
4. Open `/pilates`: `http://127.0.0.1:3000/pilates`
5. Open `/pilates/planos`: `http://127.0.0.1:3000/pilates/planos`

## Required Checks Before Commit

- `npm run lint`
- `npm run build`
- Open `/pilates` at 1440px desktop.
- Open `/pilates` at 390px mobile.
- Open `/pilates/planos` at 1440px desktop.
- Open `/pilates/planos` at 390px mobile.
- Confirm no horizontal body overflow.
- Confirm public copy does not contain prohibited terms.
- Confirm all required events log payloads with landing context.
- Confirm plan names, BRL prices and checkout destinations come from trusted configuration.
- Confirm no UI state treats plan CTA click as active subscription.
- Confirm assisted-conversion forms and WhatsApp assistance CTAs include privacy/consent framing.
- Confirm privacy notice/policy link is reachable from footer or form area.
- Capture screenshots after major visual changes.

## Manual Walkthrough

1. Hero: verify clean centered hero and no intent selector.
2. Intent selector: select at least two pains and verify conversation mockup changes.
3. Diagnosis: toggle `Sem agentes` and `Com agentes`.
4. Dinheiro na Mesa: move controls and verify estimate updates.
5. Agents: select all seven agents and verify workspace changes.
6. Plans: verify Base R$ 197/mes, 1 Agente R$ 497/mes, 3 Agentes R$ 897/mes and 7 Agentes R$ 1.497/mes, with 7 Agentes as recommended.
7. Plans page: open `/pilates/planos`, verify hero, plan cards, comparison table, fit guidance, FAQ and assisted WhatsApp CTA.
8. Plan CTA: click each primary plan/subscription CTA and verify it uses the trusted configured destination for that plan.
9. Subscription boundary: verify the landing/plans page does not collect card data and does not show paid/active subscription state after a CTA click.
10. Assisted conversion: focus form, submit with valid values and verify automatic context fields plus selected/interested plan when available.
11. Human WhatsApp: click the human assistance CTA and verify tracking/context.

## Existing Implementation Policy

The current codebase contains an earlier implementation. Treat it as a baseline/prototype. Reuse route setup, data config, calculator and tracking when compatible. Replace monolithic UI and outdated visual decisions according to `spec.md` and `tasks.md`.

## Commercial Positioning Check

- The landing sells the vertical SaaS for the niche, not niche validation.
- Primary CTAs point to plan/subscription paths.
- Public pricing shows the configured Pilates launch plans and does not rely on hardcoded section text.
- 7 Agentes is the recommended plan unless the niche config changes that decision.
- `/pilates/planos` is the canonical full plan comparison page.
- `/pilates` can show compact plan cards, but full comparison CTAs route to `/pilates/planos`.
- Analysis/Dinheiro na Mesa and human WhatsApp assistance are secondary paths.
- Public copy does not use "acesso antecipado", "early access", "validacao", "beta", "MVP" or incomplete-product language.
- No marketing form asks for card data, payment credentials or billing documents.
- No form asks for sensitive student health details or unnecessary personal data.
- Contact capture explains purpose and links/shows privacy consent information.
- Checkout/payment completion, subscription activation, entitlements and customer portal are not implemented by this landing spec.
