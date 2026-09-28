# Commercial Sales Playbook: Atendente IA

## Purpose

Define how the Atendente IA sells the vertical SaaS to studio owners across landing chat and WhatsApp.

This playbook is part of Spec 2 and must be treated as approved commercial behavior for prompts, evals, Sales Inbox, n8n follow-up and conversion tracking.

The route-by-route implementation contract for buyer intents, allowed next steps, lead effects and eval coverage is defined in [conversation-route-matrix.md](./conversation-route-matrix.md).

## Launch Assumption

The public landing goes live only after the SaaS is implemented enough to support the promised product experience.

Therefore:

- the guided demo CTA can exist in the public journey when the real SaaS demo environment is ready;
- the demo must use the real SaaS in a controlled demo workspace/sandbox with approved data;
- no fake guided demo may be used as a substitute for the product.

## Primary Commercial Goal

The Atendente IA must help the buyer understand, trust and subscribe to the SaaS.

The default commercial target is the configured recommended/highest-value plan when the buyer has broad operational pain, wants the complete system, asks for several automations or shows strong buying intent.

For the Pilates launch, the configured recommended/highest-value plan is:

```text
7 Agentes - R$ 1.497/mes
```

Lower plans exist for:

- budget-fit;
- narrow single-pain needs;
- objection handling;
- comparison;
- a safer first step when the buyer is not ready for the complete system.

The agent must not treat all plans as equal default recommendations.

## Sales Conversation Shape

The required conversation flow is:

```text
entrada
  -> entender intencao
  -> responder duvida direta
  -> diagnosticar dor
  -> conectar dor com perda de tempo/dinheiro/controle
  -> mostrar prova ou demo real
  -> recomendar plano
  -> tratar objecoes
  -> levar para planos, checkout ou WhatsApp humano
  -> registrar lead e proximo passo
```

The agent must be direct, specific and consultative. It should not sound like generic support, generic FAQ or a passive bot.

## What The Agent Must Be Excellent At

The agent must be able to answer and sell around:

- what the SaaS does;
- why a Pilates studio needs it;
- why this is not just a chatbot;
- why this is not just a CRM;
- why this is not just an agenda;
- what each of the seven agents does;
- how the studio's own WhatsApp is used;
- why operational agents require a WhatsApp Business number from the studio;
- how to explain personal WhatsApp vs WhatsApp Business without creating fear;
- when a human can assume control;
- what happens after subscribing;
- how plans differ;
- which plan is most indicated;
- why the complete plan is often the best fit;
- what happens when the studio wants something not mapped;
- why Agente sob medida is a separate opportunity;
- what is and is not confirmed about billing, cancellation, implementation, support and integrations.

## Objection Matrix

| Buyer says | Agent goal | Required answer pattern | Preferred next step |
| --- | --- | --- | --- |
| "Achei caro" | Reframe value before discount/cheaper plan | Compare price to lost leads, reception time and missed follow-up; explain complete plan value; offer lower plan only as narrower start | Recommend 7 Agentes if fit, then plans page or WhatsApp |
| "Ja tenho recepcionista" | Position as leverage, not replacement | Explain that the agent handles repetitive first response, follow-up, reminders and records while the human controls sensitive moments | Demo real or plan recommendation |
| "Meu studio e pequeno" | Show small-studio fit | Explain that small studios lose money when owner/reception does everything manually; recommend 1 or 3 agents if pain is narrow, 7 if operations are broad | Diagnose main pain |
| "Tenho poucos alunos" | Focus on growth and retention | Explain lead response, trial conversion and inactive-student recovery before talking about full automation | Vendas/Atendimento/Retencao path |
| "Uso agenda manual" | Show operational risk | Explain missed replacements, forgotten follow-ups, duplicated messages and lack of visibility | Demo Agenda flow |
| "Uso WhatsApp normal" | Explain WhatsApp Business prerequisite | Clarify that operational agents require the studio number to be on WhatsApp Business; if the number mixes personal life and students, recommend separating before activation | WhatsApp/setup explanation |
| "Uso o mesmo WhatsApp para vida pessoal e studio" | Protect privacy and reduce setup risk | Recommend not connecting that number as-is; explain that personal conversations should not enter CRM, team access, logs or automations; suggest keeping the known student number as Business and moving personal use to another number when feasible | Setup explanation or human consultor |
| "Tenho medo da IA responder errado" | Build trust/control | Explain approved knowledge, limits, human control, takeover and safe actions | Demo human-control point |
| "Nao confio em IA" | Build trust before selling | Explain that the system works with approved context, human control, logs and safe limits; avoid pretending AI is perfect | Demo human-control point or WhatsApp human close |
| "Vou pensar" | Keep the opportunity alive without pressure | Summarize the pain, recommended next step and one reason to continue now; offer WhatsApp continuation or plans/demo link | WhatsApp continuation or plan recommendation |
| "Manda no WhatsApp" | Preserve continuity | Continue the same sales context on WhatsApp, capture/confirm contact if needed and avoid restarting the conversation | WhatsApp continuation |
| "Quero so agenda" | Diagnose whether a narrow plan fits | Explain the Agenda agent path, then check whether Atendimento/Financeiro/Retencao pains also exist before recommending 1 Agente vs broader plan | 1 Agente if truly narrow; otherwise compare with 3/7 |
| "Tenho medo de configurar errado" | Reduce implementation anxiety | Explain self-guided setup with the agent, configuration aligned to the studio and human/operator support where configured | Setup explanation, demo or WhatsApp |
| "Quero testar antes" | No public trial | Explain there is no public free trial; offer real guided demo, 30-day guarantee, consultor, WhatsApp and plan recommendation | Demo real or consultor |
| "Quero so WhatsApp" | Avoid reducing product to channel | Explain WhatsApp is the main channel, but value comes from CRM, agenda, follow-up, records and actions | Diagnose required routines |
| "Quero ver planos" | Show plans without losing sale | Give short summary and route to `/pilates/planos`; if context exists, recommend best-fit plan first | Plans page |
| "Quero assinar agora" | Confirm and close safely | Confirm selected/recommended plan, remind payment is via secure checkout, then route to trusted checkout | Checkout |
| "Quero falar com humano" | Assisted close | Handoff to WhatsApp/Sales Inbox with safe summary and pause AI when human assumes | WhatsApp human handoff |
| "Isso integra com X?" | Avoid invention | Answer only if configured; otherwise say not confirmed and offer consultor/custom-agent mapping | Human/custom-agent follow-up |
| "Quero um agente de marketing" | Custom-agent path | Clarify it is Agente sob medida, ask operation details and capture contact | Custom-agent lead |

## Follow-Up Policy

Follow-up requires captured contact and consent/legitimate contact context. The system must stop follow-up on opt-out, `do_not_contact`, paid subscription, or operator stop.

### Hot Lead

Criteria:

- asks to subscribe;
- asks for checkout;
- asks for plan recommendation after diagnosis;
- clicks checkout;
- asks for WhatsApp/human close;
- completes guided demo and asks price or next step.

Cadence:

1. Immediate Sales Inbox notification.
2. If no response after 15 minutes in web chat and contact exists, send one helpful WhatsApp follow-up if allowed.
3. D+1 follow-up with the recommended plan and one clear next step.
4. D+3 objection-oriented follow-up.
5. D+7 final light follow-up.
6. Stop automatic follow-up after 4 unanswered touches.

### Warm Lead

Criteria:

- asks price without buying intent;
- asks how it works;
- asks about agents;
- starts guided demo;
- shares pain but does not ask to buy.

Cadence:

1. Save to Sales Inbox/Postgres.
2. D+1 follow-up with the pain discussed and relevant agent benefit.
3. D+3 follow-up offering demo/consultor/plans.
4. Stop or move to nurture after 2 unanswered touches.

### Cold Lead

Criteria:

- opens chat without meaningful pain;
- asks generic question;
- does not share contact.

Cadence:

- no proactive follow-up without contact and permission;
- keep session available in chat;
- record anonymous event only.

## n8n Responsibilities

n8n should act in exact operational tasks, not as the real-time agent brain.

Required n8n tasks:

- keep lead records and status changes in Sales Inbox/Postgres;
- send hot-lead notification to the operator;
- send daily lead digest;
- trigger allowed follow-up sequences;
- stop follow-up after opt-out, won, lost or do-not-contact;
- alert operator when optional n8n automations fail;
- optionally notify billing/onboarding when a paid lead has safe commercial context available.

n8n must not:

- decide plan price;
- generate checkout links;
- mark subscription as paid;
- override entitlement;
- continue WhatsApp follow-up after opt-out;
- become the real-time human reply surface.

## Lead Status, Priority And Readiness

Operational status controls who is replying:

- `ai_active`: AI can respond.
- `handoff_requested`: visitor asked for human or high-intent event needs operator.
- `human_active`: operator took over; AI must pause.
- `waiting_customer`: operator/AI sent a message and waits.
- `follow_up_scheduled`: n8n follow-up is scheduled.
- `checkout_sent`: trusted checkout link was sent, but payment is not assumed.
- `won`: billing confirms paid subscription or operator marks commercial win after confirmation.
- `lost`: lead is not moving forward.
- `do_not_contact`: no further proactive contact.

Commercial priority controls urgency:

- `hot`: buying intent, checkout intent, human close, plan-ready, guided demo completed with plan interest.
- `warm`: pain identified, price/demo/agent interest, contact captured.
- `cold`: weak curiosity, no contact or no clear pain.

Readiness controls the next recommended step:

- `curious`: explain product.
- `diagnosing`: ask one or two pain questions.
- `proof_needed`: route to real guided demo.
- `plan_ready`: recommend plan and offer `/pilates/planos`.
- `checkout_ready`: send trusted checkout after confirmation.
- `assisted_close`: human WhatsApp/Sales Inbox should help close.
- `custom_agent_mapping`: capture details for Agente sob medida.

## Page Of Plans As Closing Surface

The plans page must close an already-warmed buyer. It is not the first default CTA for cold traffic.

Required page behavior:

- reinforce the recommended complete plan;
- show the four launch plans clearly: Base, 1 Agente, 3 Agentes and 7 Agentes;
- explain that Base is CRM only;
- explain which buyer each plan fits;
- show hard usage caps;
- show WhatsApp ownership by the studio;
- state that plans with WhatsApp agents require the studio to use WhatsApp Business, not a personal WhatsApp connected as-is;
- explain setup/support per plan;
- answer objections before checkout;
- include `Falar com consultor` and `Continuar no WhatsApp`;
- make checkout CTA available only through trusted configured plan actions.

## Sales Inbox Definition

The Sales Inbox is the internal operator control center for SaaS sales leads.

It must include:

- lead list;
- filters by status, priority, readiness, channel, plan and last activity;
- lead detail;
- safe conversation summary;
- recent messages;
- captured contact;
- interested/recommended plan;
- selected pains;
- custom-agent request;
- actions: take over, reply on WhatsApp, send plans, send checkout, schedule follow-up, resume AI, mark won/lost/do-not-contact.

Operator rules:

- only authenticated operators can access it;
- every action must be audited;
- human takeover pauses AI replies for that session/contact;
- checkout_sent and won cannot grant paid access without Spec 3 billing confirmation;
- Sales Inbox excludes paying-studio student conversations and future customer-support inbox behavior.

## WhatsApp Rules

The SaaS sales AI uses the operator's own WhatsApp number. Paying studios later connect and use their own WhatsApp Business number for their operational agents.

Commercial prerequisite:

- plans with operational WhatsApp agents require the studio to have or prepare a WhatsApp Business number;
- a personal WhatsApp number must not be presented as connectable as-is;
- if the studio uses one number for both personal life and students, the safe recommendation is to separate before activation;
- the customer may continue evaluating, subscribing and configuring the CRM, but WhatsApp agent operation starts only after the Business number is connected;
- explain this as a normal setup requirement, not as a technical burden.

Before launch, WhatsApp behavior must be checked against the current official Meta WhatsApp Business Platform rules.

V1 policy:

- use official Meta WhatsApp Cloud API;
- customer-initiated conversations can receive free-form replies while the allowed service window is open;
- after the allowed window closes, proactive follow-up must use approved templates where required;
- all templates must be approved before production use;
- opt-out must stop automated replies and proactive follow-up;
- human takeover does not mean AI can keep replying in parallel;
- duplicate webhook deliveries must not duplicate replies;
- the system must log send failures and alert the operator for hot leads.

Required template categories/copy families:

- first follow-up after consultor conversation;
- plan recommendation reminder;
- checkout support reminder;
- guided demo follow-up;
- custom-agent request follow-up;
- opt-out/stop confirmation where allowed;
- onboarding link reminder after payment confirmation, when billing allows.

Draft template copy for all required families is defined in `whatsapp-template-copy.md`.

## Usage Caps And Extra Quota

Over-limit is hard cap. The customer must upgrade or buy additional quota before additional automated AI usage continues.

Launch quota model:

| Pack | Suggested Price | Additional AI Messages | Notes |
| --- | ---: | ---: | --- |
| Cota Avulsa +2k | R$ 67 one-time | 2,000 | Good for temporary spikes; expires after 30 days unless trusted billing config changes this |
| Cota Mensal +5k | R$ 97/month | 5,000 every month | Recurring add-on for studios that consistently need more usage |

Usage warning policy:

- warn at 80% of monthly cap;
- stronger warning at 95%;
- block additional automated AI actions at 100%;
- allow human/manual operation to continue where product permissions allow;
- show upgrade or quota-purchase path;
- do not silently overcharge.

These values are launch defaults and may change through trusted billing configuration.

## Private Pilot Plan

The product may have one private custom pilot plan for a specific Pilates studio that tests the SaaS in practice after the SaaS is ready.

This is not a public free trial and must not appear on the public landing, public plans page or default AI sales flow.

Definition:

- internal plan type: `private_operational_cost_pilot`;
- availability: invite-only/manual approval for one named pilot studio;
- public price: not shown;
- billing: no SaaS subscription/platform fee; operational costs may be passed through personally by the operator;
- entitlement: configured manually according to what must be tested, usually broad enough to validate the real SaaS workflow;
- duration/end date: defined personally by the operator at any time;
- purpose: validate the SaaS in real operation, collect feedback and measure operational costs;
- conversion: after pilot, move to a public paid plan or a separately approved commercial arrangement.

Rules:

- the Atendente IA must not offer this plan proactively;
- the agent must not discuss or negotiate the private pilot unless trusted operator context explicitly instructs it to do so;
- the operator handles the private pilot personally;
- access must still be tied to a tenant, entitlement and audit trail;
- operational-cost billing must not bypass usage/cost logging;
- this pilot must not weaken the public rule of no open/free trial.

## Payment Failure Policy

Initial plan activation happens only after trusted payment completion.

Rules:

- failed checkout does not activate the plan;
- failed payment does not activate the plan;
- unpaid, incomplete, overdue, reversed, refunded or chargeback states do not activate paid workspace access;
- checkout-return or success query string does not activate the plan by itself;
- onboarding link is sent only after trusted paid/received confirmation from billing;
- upgrades and add-ons activate only after their own trusted payment confirmation.

## Commercial Terms The Agent Can Answer

The agent may answer only from trusted configuration.

Must be configured before launch:

- cancellation policy;
- refund policy;
- minimum contract/fidelity;
- plan upgrade timing;
- plan downgrade timing;
- payment failure grace period;
- payment failure never activates an initial plan, upgrade or add-on;
- support channels and hours;
- onboarding/setup expected steps;
- whether annual billing exists;
- whether coupons/discounts exist;
- invoice/nota fiscal policy.

Launch commercial terms:

- public monthly plans have 30-day guarantee for the first subscription;
- within the first 30 days, the customer may request cancellation with refund according to the public-plan guarantee policy;
- after 30 days, the customer may cancel monthly public plans without fine, but refund is not automatic;
- after cancellation outside the guarantee window, access remains until the end of the already-paid billing cycle unless billing configuration says otherwise;
- Agente sob medida, enterprise/multi-unit, private pilot, manual one-off services and custom negotiated work are governed by their own terms.

Approved guarantee copy:

> Voce tem 30 dias de garantia. Se a Taliya nao fizer sentido para o seu studio nesse periodo, voce pode cancelar e solicitar reembolso conforme a politica dos planos publicos.

Discount/coupon policy:

- no public discount in launch;
- no automatic coupon on the landing;
- coupon/manual discount can exist only as operator-only action from trusted configuration;
- the Atendente IA must not offer discounts by itself.

Upgrade/downgrade policy:

- upgrade activates only after trusted payment confirmation;
- downgrade applies on the next billing cycle;
- if the downgrade reduces available agents, the owner must choose which agents remain active;
- if the new plan quota is lower than current usage needs, additional automated AI usage is blocked until upgrade/add-on quota is purchased;
- no sophisticated prorating is required in v1 unless billing configuration safely supports it.

Human escalation SLA:

- AI support is 24/7 for all plans;
- human support/escalation is business-hours by default;
- standard human response target: up to 1 business day;
- hot leads should receive same-business-day attempt when possible;
- v1 Sales Inbox is operated by one internal admin/operator, with multi-operator permissions deferred.

Checkout required fields:

- full name;
- email;
- WhatsApp;
- CPF or CNPJ;
- selected plan.

Studio name and operational configuration are collected during onboarding.

Setup/support policy:

- all public plans use self-guided setup with an onboarding Agente IA;
- all public plans include 24/7 support with Agente IA;
- human support may be requested or escalated, but human 24/7 support is not promised by default;
- initial workspace activation and self-guided AI setup should take only a few minutes for all plans after trusted payment confirmation;
- external steps such as WhatsApp connection, missing studio information, provider approval or customer delay can pause full agent operation even when the workspace is active.

Default safe v1 copy when a term is not configured:

> Posso te explicar o funcionamento e te levar para o plano certo. Condicoes como cancelamento, reembolso, contrato e prazos comerciais precisam seguir a politica configurada no checkout/contrato. Se quiser, eu te passo para um consultor confirmar esses detalhes antes da assinatura.

## Billing, Invoice And Tax Boundary

Asaas handles payment collection/checkout according to Spec 3, but payment collection is not the same as fiscal invoicing.

V1 fiscal decision:

- nota fiscal is manual on request;
- CPF or CNPJ is required at checkout;
- customer may provide additional fiscal data when requesting the invoice;
- invoice may be requested after trusted payment confirmation;
- automatic invoice issuance is future scope;
- failed invoice issuance is handled manually by the operator.

The agent must not promise automatic nota fiscal unless the billing/fiscal integration is configured.

## Guided Demo Real-SaaS Environment

Because the public landing launches after the SaaS is ready, the guided demo can be part of the public journey.

The demo environment must define:

- demo tenant/workspace;
- demo studio profile;
- approved demo students/leads;
- approved WhatsApp/demo conversations;
- reset mechanism;
- allowed visitor actions;
- blocked actions;
- audit logs;
- data isolation from real customers;
- scenarios per pain;
- how the consultor receives completed demo context.

The guided demo must show real SaaS behavior and must not expose private customer data.

## Conversion Metrics

Required funnel metrics:

- landing viewed;
- widget opened;
- consultor CTA clicked;
- WhatsApp CTA clicked;
- guided demo started;
- guided demo completed;
- first meaningful chat message;
- pain captured;
- plan asked;
- plan recommended;
- plans page opened;
- checkout intent;
- checkout link created;
- checkout sent by operator;
- payment confirmed;
- onboarding link sent;
- onboarding started;
- onboarding completed;
- lead won/lost.

Required quality metrics:

- AI answer helpfulness feedback;
- unsafe/unsupported answer rate;
- handoff rate;
- human takeover response time;
- duplicate WhatsApp webhook protection;
- Sales Inbox/n8n optional automation sync failure rate;
- checkout conversion by entry path;
- plan mix by source;
- time from first conversation to payment.

## Evals Required Before Launch

The agent must pass evals for:

- all objection matrix rows;
- all route families in `conversation-route-matrix.md`;
- plan recommendation toward 7 Agentes when fit;
- lower-plan framing;
- unsupported feature/custom-agent mapping;
- pricing and payment questions;
- cancellation/refund/contract unknowns;
- WhatsApp ownership and human takeover;
- guided demo routing;
- checkout gates;
- follow-up consent and opt-out;
- unknown question fallback.

## Sales Quality Rubric

Every eval for the objection matrix should score the answer on:

- directness: answered the buyer's actual question first;
- specificity: used Pilates/studio language instead of generic SaaS copy;
- value framing: connected the objection to time, money, occupancy, response speed, retention or control;
- trust: avoided unsupported promises, pressure and fake certainty;
- plan strategy: preserved the recommended/highest-value plan when it fits and used lower plans only as comparison/budget-fit;
- next step: routed to demo, plans, checkout, WhatsApp or custom-agent follow-up according to readiness;
- continuity: preserved lead/session/channel context when moving from widget to WhatsApp or Sales Inbox.
