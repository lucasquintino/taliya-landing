# Internal Sales Inbox

## Purpose

The Internal Sales Inbox is the SaaS operator's commercial control center for leads who may subscribe to the SaaS.

It exists before the full SaaS product and must not be confused with the future inbox/panel that paying studios may use for their own students, interested students or operational agents.

## Scope

Included:

- leads from the landing web widget;
- leads from the SaaS sales WhatsApp;
- leads asking to see plans;
- leads with checkout/subscription intent;
- leads with checkout link sent;
- leads requesting human assistance;
- leads requesting analysis;
- leads requesting Agente sob medida.

Excluded:

- student conversations for paying studios;
- paying-studio operational inbox;
- CRM sold to studios;
- operational agent management for subscribed studios;
- billing activation or paid entitlement confirmation.

## Source Of Truth Split

The Sales Inbox is the real-time control surface.

Sales Inbox/Postgres is the v1 commercial pipeline/reporting source of truth.

Postgres is the required production persistence layer for the Sales Inbox state, operator actions, message history, merge decisions and sync status. External CRM/spreadsheet sync is disabled for this phase.

Rules:

- The operator uses the Sales Inbox to control conversations and actions.
- n8n may send optional alerts/digests from Sales Inbox events.
- External spreadsheets/CRMs are not the real-time message/reply surface.
- n8n failure must not block the operator from replying or controlling the lead.
- Process-local memory is allowed only in local development and must not be used for production lead control.

## Lead Identity And Merge

Strong merge signals:

- same normalized WhatsApp;
- same normalized email;
- explicit `leadId`;
- explicit `sessionId` carried from widget to WhatsApp.

Weak signals:

- same/similar studio name;
- same source page;
- same browser/IP;
- close timing;
- same selected pain or plan.

Rules:

- Strong signals may auto-merge.
- Weak signals alone must not auto-merge.
- Ambiguous matches must remain separate or require operator review.
- Every merge decision should be recorded as system or operator action.

## Required Statuses

- `ai_active`: AI is handling the lead.
- `handoff_requested`: lead asked for human help or qualifies for operator attention.
- `human_active`: operator took over and AI replies are paused.
- `waiting_customer`: operator replied and waits for the lead.
- `follow_up_scheduled`: operator scheduled a future follow-up.
- `checkout_sent`: trusted checkout link was sent.
- `won`: operator marked the opportunity as won; this is not proof of paid subscription.
- `lost`: lead is not moving forward.
- `do_not_contact`: lead opted out or must not be contacted.

## Required Actions

- `take_over`: pause AI and make operator responsible.
- `send_whatsapp_message`: send a human WhatsApp reply through the server-side provider adapter.
- `send_plan_page`: send configured plans page.
- `send_checkout_link`: send configured checkout link for selected plan.
- `schedule_follow_up`: set next action/follow-up date.
- `resume_ai`: allow AI to respond again.
- `mark_waiting_customer`
- `mark_won`
- `mark_lost`
- `mark_do_not_contact`
- `edit_lead_summary`

## UI Requirements

Minimum v1 surface:

- protected internal route;
- lead list;
- filters by status, priority, channel, conversion path, interested plan and last activity;
- lead detail panel;
- recent messages;
- safe summary;
- contact/studio fields;
- captured pains;
- recommended agents;
- interested plan;
- custom-agent request when applicable;
- next action/follow-up date;
- action buttons;
- WhatsApp reply composer for WhatsApp leads.

## Security

- Internal operator/admin access only.
- Browser must never receive WhatsApp provider credentials.
- Browser must never receive n8n secrets.
- Browser must never receive billing provider secrets.
- Checkout links must come from trusted configuration.
- Operator-typed arbitrary checkout URLs are not allowed in v1.

## AI Pause Rules

- While status is `human_active`, WhatsApp AI replies are paused.
- AI resumes only after `resume_ai` or a later allowed new inbound context.
- `won`, `lost` and `do_not_contact` are terminal for automated replies unless explicit new opt-in/intent exists.

## Billing Boundary

Sales Inbox can send checkout links and mark `checkout_sent`.

Sales Inbox must not mark a subscription as paid or active. Paid status comes only from Spec 3 billing webhooks.

## Optional n8n Automations

Sync fields:

- lead status;
- priority;
- channel(s);
- conversion path;
- selected/interested plan;
- captured pains;
- recommended agents;
- safe summary;
- next action;
- follow-up date;
- won/lost/do-not-contact state;
- last operator action timestamp.

Do not sync by default:

- full raw transcript;
- payment credentials;
- provider secrets;
- internal prompts/guardrails;
- sensitive unnecessary personal data.

## Failure Handling

- WhatsApp send failure: keep operator action visible, mark send failed and allow retry.
- n8n failure: keep inbox action complete, mark external automation status pending/failed and notify/log for retry.
- AI failure: keep Sales Inbox usable and show AI degraded state.
- Missing WhatsApp: allow email/next-action follow-up but disable WhatsApp send.

## Acceptance Criteria

- All SaaS sales leads from web widget and WhatsApp appear in one internal Sales Inbox.
- Widget + WhatsApp activity merges only by strong identifiers.
- Operator can take over a WhatsApp lead and pause AI.
- Operator can send WhatsApp replies through server-side provider.
- Operator can send trusted plan-page and checkout links.
- Operator can mark waiting, follow-up, checkout sent, won, lost and do-not-contact.
- Sales Inbox stores safe fields directly in Postgres and may emit optional n8n events.
- n8n failure does not block operator control.
- Sales Inbox is clearly not the future paying-studio inbox.
