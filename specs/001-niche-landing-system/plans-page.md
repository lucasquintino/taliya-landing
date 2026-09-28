# Plans Page: Pilates SaaS

## Purpose

Define the dedicated plans page for the Pilates vertical SaaS.

Canonical route:

```text
/pilates/planos
```

This page exists so the visitor can compare plans with confidence before checkout after consultor recommendation or explicit plan-comparison intent. The main landing should not push cold visitors straight here as the primary action; it should open the consultor first.

## Product Role

The plans page is not a generic pricing table. It is the downstream buying-decision page for the SaaS.

It must:

- make plan differences obvious;
- make the recommended plan easy to choose;
- explain when a lower plan fits;
- support selling the higher-value plan when the studio has broad operational needs;
- answer common objections before checkout;
- preserve checkout as an available action for visitors who reached the page intentionally;
- keep consultor/WhatsApp assistance as the main confidence builder for visitors who still need help.

## Route Relationship

- `/pilates`: main narrative landing page.
- `/pilates#planos`: optional compact pricing band inside the landing.
- `/pilates/demonstracao`: guided real-SaaS product demonstration before plan discussion.
- `/pilates/planos`: canonical full plan comparison page reached after consultor recommendation or explicit plan-comparison intent.
- Billing checkout route: server-side checkout creation after the visitor chooses a specific plan.

## Required Page Structure

1. Header
   - Logo/brand.
   - Back link to `/pilates`.
   - Primary CTA to consultor with current plan context.
   - Secondary CTA for WhatsApp assistance.

2. Hero
   - H1: `Escolha o plano para o seu studio de Pilates`
   - Supporting copy focused on choosing the right level of operational agent coverage.
   - CTAs:
     - `Ver comparativo`
     - `Falar com consultor`
     - `Assinar plano recomendado`

3. Plan Cards
   - Base.
   - 1 Agente.
   - 3 Agentes.
   - 7 Agentes as recommended/default unless config changes.
   - Each card includes price, best-fit studio profile, included agent coverage, WhatsApp availability, setup/onboarding expectation, usage boundary, primary consultor CTA and secondary checkout CTA. Checkout CTA remains allowed here because the visitor intentionally reached the decision page.

4. Comparison Table
   - Rows:
     - Atendimento.
     - Agenda.
     - Vendas.
     - Financeiro.
     - Retencao.
     - Gestao.
     - Historico/Evolucao.
     - WhatsApp channel.
     - Setup/onboarding.
     - Usage boundary/hard cap.
     - Support/human assistance.
     - Agente sob medida.
   - Columns:
     - Base.
     - 1 Agente.
     - 3 Agentes.
     - 7 Agentes.

5. Plan Fit Guidance
   - `Escolha Base se...`
   - `Escolha 1 Agente se...`
   - `Escolha 3 Agentes se...`
   - `Escolha 7 Agentes se...`
   - 7 Agentes should remain the natural recommendation for studios that want the full system.

6. Objection FAQ
   - What happens after subscribing?
   - Does it replace my team?
   - Does it work on WhatsApp?
   - Can I change plan later?
   - Can I cancel?
   - Do I need to configure everything alone?
   - What if I need an agent outside these seven?
   - Is payment handled safely?
   - What happens when I hit my usage cap?
   - How does nota fiscal/invoice work when configured?

7. Assisted Close
   - Secondary band for visitors who still need help choosing.
   - CTA: `Falar com consultor`
   - Must include selected/interested plan context when available.

8. Final CTA
   - Consultor CTA with recommended-plan context.
   - Secondary recommended-plan checkout CTA.
   - Link back to comparison.

## Pricing Rules

All plan data must come from trusted niche/commercial configuration.

The page must not hardcode:

- prices;
- discounts;
- checkout URLs;
- included-agent claims;
- recommended plan;
- annual billing claims.

Public default plans:

| Plan | Default price | Default role |
|------|---------------|--------------|
| Base | R$ 197/mes | CRM-only, 0-agent entry plan |
| 1 Agente | R$ 497/mes | Narrow first-automation plan |
| 3 Agentes | R$ 897/mes | Multi-agent growth plan |
| 7 Agentes | R$ 1.497/mes | Recommended complete-system plan |

## Launch Comparison Content

Default comparison values:

| Row | Base | 1 Agente | 3 Agentes | 7 Agentes |
| --- | --- | --- | --- | --- |
| Active AI agents | 0 | 1 selected agent | 3 selected agents | All seven primary agents |
| Atendimento | Not active | Available as selected agent | Available as selected agent | Included |
| Agenda | Not active | Available as selected agent | Available as selected agent | Included |
| Vendas | Not active | Available as selected agent | Available as selected agent | Included |
| Financeiro | Not active | Available as selected agent | Available as selected agent | Included |
| Retencao | Not active | Available as selected agent | Available as selected agent | Included |
| Gestao | Not active | Available as selected agent | Available as selected agent | Included |
| Historico/Evolucao | Not active | Available as selected agent | Available as selected agent | Included |
| Studio scope | 1 studio/unit | 1 studio/unit | 1 studio/unit | 1 studio/unit |
| Team users | 1 | Up to 2 | Up to 5 | Up to 10 |
| WhatsApp channels | No automated WhatsApp agent | Studio's own WhatsApp connected | Studio's own WhatsApp connected | Studio's own WhatsApp connected |
| Usage boundary | No AI message automation | 1,500 AI messages/month hard cap | 5,000 AI messages/month hard cap | 15,000 AI messages/month hard cap |
| Setup | Self-guided with AI | Self-guided with AI | Self-guided with AI | Self-guided with AI |
| Support | 24/7 AI support | 24/7 AI support | 24/7 AI support | 24/7 AI support |
| Agente sob medida | Separate business | Separate business | Separate business | Separate business |

The public plans page must not show private operational-cost pilot plans.

Public UI may translate caps into friendlier plan language, but the comparison must not imply unlimited use, multi-unit support or included custom-agent development.

## CTA Behavior

Primary plan CTA:

```text
Falar com consultor sobre [planName]
```

Behavior:

1. Emit `plan_consultor_clicked`.
2. Open/focus the consultor with selected/interested plan context.
3. Include source metadata:
   - `source: plans_consultor`
   - `sourcePage: /pilates/planos`
   - `sourceSection`
   - `planId`
   - `billingPeriod`

Secondary checkout CTA:

```text
Assinar [planName]
```

Behavior:

1. Emit `plan_cta_clicked`.
2. Call or route to server-side checkout creation from Spec 3.
3. Include source metadata:
   - `source: landing_plans`
   - `sourcePage: /pilates/planos`
   - `sourceSection`
   - `planId`
   - `billingPeriod`
4. Never collect card data in the page.
5. Never mark subscription active from click alone.

WhatsApp CTA:

```text
Falar no WhatsApp
```

Behavior:

1. Emit `human_whatsapp_clicked`.
2. Include selected/interested plan when available.
3. Route to configured WhatsApp assistance destination.

## Tracking Events

Required:

- `plans_page_viewed`
- `plans_comparison_viewed`
- `plan_cta_clicked`
- `plan_period_toggled` if annual billing is enabled
- `human_whatsapp_clicked`
- `faq_item_opened`
- `plan_fit_guidance_clicked` if guidance is interactive

All events must include:

- `niche`
- `sourcePage`
- `campaignStage`
- `publicOfferMode`
- `eventName`
- `metadata`

## Agent Integration

When the floating sales attendant detects `view_plans`, it must:

1. answer briefly;
2. ask one concise qualifying question if the visitor has not shared enough context;
3. mention that the full comparison is available;
4. route to `/pilates/planos` when the visitor asks, has enough context for a recommendation or insists on seeing plans;
5. preserve chat session state;
6. not treat the request as checkout/subscription intent.

## Billing Boundary

Viewing the page or comparing plans does not start checkout.

Checkout starts only when the visitor clicks a specific plan subscription CTA.

Active access starts only after trusted billing webhook confirmation from Spec 3.

## Responsive Requirements

- At 390px, cards may stack but the recommended plan must remain obvious.
- Comparison table must not cause horizontal body overflow.
- On mobile, comparison may use segmented plan tabs or grouped accordions.
- CTAs must remain tappable and not overlap the floating attendant.

## Acceptance Criteria

- Visitor can understand plan differences after reaching the page intentionally.
- 7 Agentes is visually recommended by default unless config changes.
- Base, 1 Agente and 3 Agentes remain credible options, not disabled decoys.
- The page prioritizes consultor assistance but routes to checkout after explicit plan selection.
- The page never collects payment data.
- The page uses trusted config for all plan/pricing/checkout data.
- The floating attendant can route to the page and preserve chat context after consultor-led or explicit plan-comparison intent.
