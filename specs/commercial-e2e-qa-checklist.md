# Commercial E2E QA Checklist

Date: 2026-05-07

Purpose: one practical QA script for Spec 1 and Spec 2 after the parallel `/pilates` layout work finishes. Spec 3 and Spec 4 are intentionally excluded from implementation QA for now because billing/onboarding will be reviewed after the real SaaS spec is created.

## Scope

Included:

- `/pilates`
- `/pilates/planos`
- `/privacidade`
- web consultor/widget
- WhatsApp channel boundary
- Sales Inbox
- Sales Inbox lead storage and optional n8n alert behavior
- demo gate while `guidedDemoReady=false`

Excluded for now:

- real SaaS app pages
- mobile app
- billing checkout activation
- post-payment onboarding
- real `/pilates/demonstracao` implementation

## Preflight

- [ ] `npm run lint` passes.
- [ ] `npm run build` passes.
- [ ] `/pilates` returns 200.
- [ ] `/pilates/planos` returns 200.
- [ ] `/privacidade` returns 200.
- [ ] No visible CTA points to a missing route.
- [ ] `guidedDemoReady=false` in the landing config until the real SaaS demo exists.
- [ ] Public copy does not mention beta, MVP, validation, fake demo, incomplete product or direct paid activation from CTA click.

## Landing CTA QA

| Test | Expected result |
| --- | --- |
| Open `/pilates` at 1440px | No horizontal overflow; layout looks complete after visual pass |
| Open `/pilates` at 390px | No horizontal overflow; CTAs remain tappable |
| Click hero primary CTA | Opens/focuses consultor or lands on a working consultor CTA |
| Click header CTA | Opens/focuses consultor or lands on a working consultor CTA |
| Click final CTA | Opens/focuses consultor with final CTA context |
| Click WhatsApp CTA | Opens configured WhatsApp destination with safe sales message |
| Search for plan CTAs on `/pilates` | Cold visitor is not sent directly to checkout |
| Search for demo CTAs on `/pilates` | No cold link to `/pilates/demonstracao` while `guidedDemoReady=false` |

## Consultor/Web Widget QA

| Scenario | Expected result |
| --- | --- |
| Open floating widget | Neutral opening; no checkout CTA |
| Inspect widget display modes | Minimized, attention, active, opening, desktop open, mobile open, loading, error and handoff states are visually clear and polished |
| Click Falar com consultor | Stronger commercial opening; asks context before plan |
| Ask "quanto custa?" | Answers from configured plans and can route to `/pilates/planos`; does not treat as checkout |
| Ask "quero assinar agora" | Confirms/recommends plan and offers trusted checkout path only after explicit intent |
| Ask "quero ver demo" while `guidedDemoReady=false` | Explains demo readiness and routes to consultor/WhatsApp/product explanation |
| Ask "tenho medo de configurar errado" | Explains setup/self-guided help before checkout |
| Ask "tem garantia?" | Explains 30-day guarantee from approved context |
| Ask "posso usar meu WhatsApp?" | Explains studio-owned WhatsApp for paying studios |
| Ask "quero agente de marketing" | Maps as Agente sob medida; asks details/contact and says team will follow up |
| Ask for card/payment in chat | Refuses to collect payment data and routes to secure provider path |

## Custom-Agent Diagnostic Report QA

| Scenario | Expected result |
| --- | --- |
| Submit diagnostic with "quero responder WhatsApp e organizar reposicoes" | Report classifies `mapped_solution`, names Atendimento/Agenda and offers consultor/demo/WhatsApp CTAs with diagnostic context |
| Submit diagnostic with "quero agente de marketing para Instagram" | Report classifies `custom_agent`, explains separate proposal path and offers custom proposal/WhatsApp CTAs |
| Submit diagnostic with mixed SaaS + marketing request | Report separates mapped SaaS agents from custom-agent work and does not imply custom work is included in plans |
| Submit vague diagnostic "quero automatizar meu studio" | Report classifies `unclear`, asks for missing context and offers consultor/WhatsApp continuation |
| Click diagnostic `Solicitar proposta de agente sob medida` | Opens consultor or WhatsApp in custom-agent proposal mode and asks for more operation details/contact |
| Click diagnostic mapped-solution `Falar com consultor` | Opens consultor with "Taliya already covers this" variant and continues SaaS sales funnel |
| Inspect diagnostic report CTAs | No CTA routes directly to checkout |

## Plans Page QA

| Test | Expected result |
| --- | --- |
| Open `/pilates/planos` at 1440px | No horizontal overflow |
| Open `/pilates/planos` at 390px | No horizontal overflow |
| Inspect plans | Shows Base, 1 Agente, 3 Agentes, 7 Agentes |
| Inspect recommendation | 7 Agentes visually recommended |
| Inspect Base | CRM only, 0 active AI agents |
| Inspect each plan | Shows fit, included agents, WhatsApp scope, setup expectation and usage boundary |
| Click consultor on a plan | Opens consultor with selected plan context |
| Click WhatsApp assistance | Opens trusted WhatsApp destination |
| Click checkout CTA | Tracks intent/gate; does not mark paid/subscribed |
| Read FAQ/risk reducers | Shows guarantee, payment-data safety, setup help, WhatsApp ownership and hard caps |
| Inspect landing FAQ | Shows no more than 8 high-impact questions |
| Click "ficou alguma duvida?" FAQ CTA | Opens the consultor with widget-style neutral opening and `sourceSection=faq_doubt_cta` |

## WhatsApp QA

| Test | Expected result |
| --- | --- |
| Inbound valid WhatsApp message | Webhook verifies provider and sends one AI reply |
| Duplicate provider message ID | No duplicate reply or duplicate lead |
| User says stop/opt-out | Automated replies stop |
| Equivalent buyer question from web and WhatsApp | Same answer policy and plan recommendation |
| Human takeover active | AI does not auto-reply until operator resumes |
| Missing Meta credentials in dev | Send is skipped/degraded safely without exposing secrets |

## Sales Inbox QA

| Test | Expected result |
| --- | --- |
| Open `/internal/sales-inbox` without token | Access blocked/config state |
| Open with valid token | Lead list and detail load |
| Filter by status | Results filter correctly |
| Filter by priority | Results filter correctly |
| Filter by channel | Results filter correctly |
| Filter by conversion path | Results filter correctly |
| Filter by next action | Results filter correctly |
| Take over a WhatsApp lead | Status becomes `human_active`; AI paused |
| Send WhatsApp message | Uses server-side Meta adapter; browser receives no provider credentials |
| Send plan page | Uses trusted `/pilates/planos` destination |
| Send checkout link | Uses trusted configured plan destination; does not mark paid |
| Mark won/lost/do-not-contact | Creates audit event and updates status |

## Sales Inbox/n8n QA

| Test | Expected result |
| --- | --- |
| Lead storage | Sales Inbox creates or updates one durable lead record |
| Hot lead event | n8n receives urgent alert as secondary notification |
| Operator action | n8n receives safe operator action sync |
| n8n webhook unavailable | Chat and Sales Inbox still work; external sync status records skipped/failed |
| External CRM disabled | No lead upsert webhook is required for the funnel to work |
| Stored lead content | Safe summary/status fields only; no payment credentials |

## Lead Identity QA

Strong merge identifiers:

- explicit `leadId`
- WhatsApp provider contact ID
- normalized WhatsApp number
- verified/provided email
- explicit session continuation token

Checks:

- [ ] Same WhatsApp contact updates one lead.
- [ ] Duplicate WhatsApp retry does not create a second lead.
- [ ] Same studio name alone does not auto-merge.
- [ ] Same pain/plan alone does not auto-merge.
- [ ] Widget to WhatsApp continuation can merge only when a strong identifier exists.

## Launch Blockers

Any one of these blocks public launch:

- `/pilates` has a 404 CTA.
- Cold CTA sends directly to checkout.
- Cold CTA sends directly to `/pilates/planos` as the primary path.
- Demo CTA links to `/pilates/demonstracao` while `guidedDemoReady=false`.
- 7 Agentes is not the recommended plan in visible/commercial behavior.
- Chat collects card/payment data.
- Sales Inbox is inaccessible while same-number human takeover is promised.
- n8n failure blocks chat, WhatsApp or operator control.
- Lead records are not visible to the operator.
- Public copy implies beta, validation, fake demo or incomplete product.

## Evidence To Capture

- `tmp/screenshots/pilates-commercial-desktop.png`
- `tmp/screenshots/pilates-commercial-mobile.png`
- `tmp/screenshots/pilates-planos-desktop.png`
- `tmp/screenshots/pilates-planos-mobile.png`
- lint output
- build output
- sample web consultor transcript
- sample WhatsApp webhook response
- sample Sales Inbox lead detail
- sample Sales Inbox lead detail and optional n8n alert payload
