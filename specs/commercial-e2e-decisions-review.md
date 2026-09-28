# Commercial E2E Decisions For Review

Date: 2026-05-07

Purpose: capture the decisions needed before implementing the full path from landing/chat/WhatsApp to paid subscription and onboarding.

The launch readiness checklist and implementation sequence are defined in [commercial-e2e-readiness-and-implementation-order.md](./commercial-e2e-readiness-and-implementation-order.md). That file is the cross-spec source of truth for what must be true before the commercial funnel is considered ready.

## 1. Payment Provider

Decision: use Asaas as the v1 billing provider.

Why:

- first commercial market is Brazil;
- plans are priced in BRL;
- buyers expect local methods such as credit card, boleto and Pix;
- checkout/payment credentials must stay server-side;
- paid access must be confirmed by trusted webhooks.

Default payment policy:

- credit card recurring is the preferred automatic subscription path;
- boleto is allowed when configured, but access starts only after payment confirmation;
- Pix can be offered only through the Asaas-supported flow that is actually configured;
- do not promise Pix Automatico or automatic Pix recurrence until it is implemented end-to-end;
- no public free trial;
- annual billing stays hidden until configured.

## 2. Plan Entitlements

Decision: public plans are organized by number of active AI agents: 0, 1, 3 and 7 agents.

The 7-agent plan is the complete-system plan and the main commercial target when the studio has broad operational pain or wants the full SaaS promise. The 0, 1 and 3-agent plans exist to reduce entry friction, fit narrower needs and help with price objections.

Proposed launch names/prices for review:

| Plan | Price | Active AI Agents | Scope | Usage | Setup/Support | Custom Agent |
| --- | ---: | --- | --- | --- | --- | --- |
| Base | R$ 197/mes | 0 agents | 1 studio, 1 user, CRM only | No AI message automation included | Self-guided setup with AI; 24/7 AI support | Separate business |
| 1 Agente | R$ 497/mes | 1 selected primary agent | 1 studio, 2 users, studio's own WhatsApp connected | 1,500 AI messages/month hard cap | Self-guided setup with AI; 24/7 AI support | Separate business |
| 3 Agentes | R$ 897/mes | 3 selected primary agents | 1 studio, 5 users, studio's own WhatsApp connected | 5,000 AI messages/month hard cap | Self-guided setup with AI; 24/7 AI support | Separate business |
| 7 Agentes | R$ 1.497/mes | All seven primary agents | 1 studio, 10 users, studio's own WhatsApp connected | 15,000 AI messages/month hard cap | Self-guided setup with AI; 24/7 AI support | Separate business |

Seven primary agents:

- Atendimento
- Agenda
- Vendas
- Financeiro
- Retencao
- Gestao
- Historico/Evolucao

Important boundaries:

- Base is a CRM-only plan with no active AI agent automation.
- 1 Agente and 3 Agentes let the customer choose from the seven primary agents during onboarding, subject to plan rules.
- 7 Agentes includes the complete set of seven primary agents.
- Agente sob medida is not included in any plan. It is a separate business/opportunity.
- Multi-unit support is not included in launch plans. It belongs to a future Enterprise plan.
- The sales AI uses our own WhatsApp. Paying studios connect and use their own WhatsApp for their agents.
- When usage reaches the plan cap, the customer must upgrade or buy more quota before additional automated AI usage continues.
- Public monthly plans have a 30-day guarantee for the first subscription.
- One invite-only private operational-cost pilot may exist for a specific Pilates studio after the SaaS is ready; it is internal-only, personally handled by the operator and not a public trial.
- No public discounts/coupons in launch; discounts are operator-only if configured.
- V1 nota fiscal is manual on request after trusted payment confirmation.
- V1 Sales Inbox has one internal admin/operator; multi-operator permissions are future scope.
- Human escalation is business-hours by default, with standard response target up to 1 business day and hot-lead same-business-day attempt when possible.

Extra quota model:

- Cota Avulsa +2k: one-time extra quota for temporary spikes.
- Cota Mensal +5k: recurring monthly extra quota for ongoing higher usage.

Checkout required fields:

- full name;
- email;
- WhatsApp;
- CPF ou CNPJ;
- selected plan.

## 3. Payment Before Account

Decision: the buyer pays first, then creates/claims the SaaS workspace.

Flow:

1. Visitor arrives through widget, Falar com consultor, WhatsApp, guided demo, Agente sob medida diagnostic report or FAQ doubt CTA.
2. Consultor diagnoses, answers doubts, offers guided demo when useful and recommends the best-fit plan.
3. Visitor reaches `/pilates/planos`, checkout after confirmed recommendation, or operator-assisted close from Sales Inbox.
4. Server creates trusted Asaas checkout/payment/subscription only when a checkout gate exists.
5. Visitor pays.
6. Asaas webhook confirms first paid/received payment.
7. Billing creates customer, subscription, entitlement and pending tenant activation.
8. Owner receives onboarding link by email and, when available, WhatsApp.
9. Owner authenticates with magic link/OTP.
10. Owner claims or creates the studio workspace.
11. Onboarding configures profile and included agents, optionally using safe consultor/demo context as prefill.

Rejected paths:

- no workspace from checkout-started;
- no workspace from checkout-return URL;
- no workspace from chat intent;
- no workspace from Sales Inbox lead status;
- no workspace from unpaid/trialing/incomplete billing state.
- no checkout from cold `/pilates` CTA without valid checkout gate.

## 4. Human Takeover On WhatsApp

Decision: Sales Inbox/Postgres is the lead pipeline and real-time reply surface for SaaS sales leads.

Because WhatsApp v1 uses Meta WhatsApp Cloud API, human takeover on the same AI WhatsApp number requires a protected operator reply surface or approved shared inbox. V1 default is the internal Sales Inbox for all SaaS sales leads.

Minimum Sales Inbox behavior:

- list SaaS sales leads from widget, WhatsApp, guided-demo intent/completion, plans-page intent, checkout intent and custom-agent requests;
- show safe context, recent messages, interested plan, status and next action;
- operator can take over;
- AI pauses while session is `human_active`;
- operator sends replies through server-side WhatsApp adapter;
- operator can send trusted plan-page and checkout links;
- operator can schedule follow-up, resume AI, mark waiting customer, checkout sent, won/lost or do-not-contact;
- n8n can send optional alerts/digests, but does not own lead storage.

State machine:

- `ai_active`
- `handoff_requested`
- `human_active`
- `waiting_customer`
- `follow_up_scheduled`
- `checkout_sent`
- `won`
- `lost`
- `do_not_contact`

## 5. Approved Agent Knowledge

Decision: the Atendente IA must answer from trusted config plus approved knowledge.

Source order:

1. runtime system configuration;
2. approved answer knowledge file;
3. safe fallback/handoff.

The agent must not invent:

- price;
- discount;
- contract/cancellation terms;
- implementation timeline;
- integration support;
- legal/tax promises;
- guaranteed financial result;
- payment status.

## 6. Additional Commercial Operating Decisions

Decision: the detailed SaaS sales behavior is defined in Spec 2 `commercial-sales-playbook.md`.

Now defined:

- commercial objection matrix;
- sales follow-up cadence;
- lead status, priority and readiness;
- n8n responsibilities;
- Sales Inbox operating rules;
- WhatsApp template/follow-up boundary;
- launch quota pack defaults;
- commercial terms boundary;
- billing/fiscal invoice boundary;
- guided demo real-SaaS environment rules;
- private operational-cost pilot boundary under personal operator control;
- all required WhatsApp template drafts in Spec 2 `whatsapp-template-copy.md`;
- funnel and quality metrics;
- required launch evals.

## 7. What Still Needs Final Business Approval Before Paid Launch

- Final add-on quota prices for Cota Avulsa +2k and Cota Mensal +5k.
- Cancellation, refund and minimum-contract wording.
- Final WhatsApp template approval in Meta/WhatsApp provider.
