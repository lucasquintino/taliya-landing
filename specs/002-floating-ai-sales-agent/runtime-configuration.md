# Runtime Configuration: Floating AI Attendant

## Purpose

Define the runtime pieces required to run the Atendente IA in production across web widget and WhatsApp.

## Pending Manual Setup Reminder

Before real E2E implementation, the project operator must create and provide the production credentials/configuration below. This is intentionally a manual setup step and can be done later.

OpenAI:

- Create an OpenAI Platform API key.
- Store it as `OPENAI_API_KEY`.
- Optionally choose `AI_ATTENDANT_MODEL`.
- Remember: ChatGPT subscription is not the API key/billing account.

Meta WhatsApp Cloud API:

- Create or use a Meta for Developers app.
- Enable WhatsApp.
- Connect a WhatsApp Business Account.
- Connect/register the production phone number.
- Collect `META_WHATSAPP_ACCESS_TOKEN`.
- Collect `META_WHATSAPP_PHONE_NUMBER_ID`.
- Collect `META_WHATSAPP_BUSINESS_ACCOUNT_ID`.
- Collect `META_WHATSAPP_APP_SECRET`.
- Create a random `META_WHATSAPP_WEBHOOK_VERIFY_TOKEN`.
- Configure the Meta webhook callback URL after the app route exists.
- Configure the internal Sales Inbox access policy before claiming same-number human takeover or full lead control.

Session Store:

- Provision Postgres for production persistence.
- Optionally provision Redis/KV for short-lived rate-limit counters and webhook locks.
- Collect server-side connection credentials.
- In-memory storage is local-only and must not be used for production WhatsApp E2E.

n8n:

- Create analysis handoff webhook.
- Create high-intent webhook.
- Do not create an external lead-upsert webhook for this phase.
- Create custom-agent diagnostic webhook.
- Create urgent lead alert webhook.
- Create operator action sync webhook.
- Create safety/fallback webhook.
- Configure DATABASE_URL/Postgres as the v1 lead source of truth for Sales Inbox.
- Keep external CRM/spreadsheet sync disabled for this phase.
- Store webhook URLs as server env vars.
- Add a shared secret if supported.

## AI Provider

Provider: OpenAI, server-side only.

Required environment:

- `OPENAI_API_KEY`: server-side API key.
- `AI_ATTENDANT_MODEL`: optional override for the planned default model.

Rules:

- The browser never receives the API key.
- Prompt/control logic stays on the server.
- Model can be changed by environment/config without changing role rules.

## WhatsApp Provider

Provider: official Meta WhatsApp Cloud API.

Detailed production E2E behavior, service-window/template rules, delivery status handling and launch blockers are defined in [whatsapp-e2e-readiness.md](./whatsapp-e2e-readiness.md).

Required environment:

- `META_WHATSAPP_ACCESS_TOKEN`
- `META_WHATSAPP_PHONE_NUMBER_ID`
- `META_WHATSAPP_BUSINESS_ACCOUNT_ID`
- `META_WHATSAPP_APP_SECRET`
- `META_WHATSAPP_WEBHOOK_VERIFY_TOKEN`

Rules:

- Webhook verification happens server-side.
- Webhook POST signatures are verified server-side.
- Provider message IDs are used for idempotency.
- Automatic replies are allowed only for inbound or opted-in conversations.
- Proactive or out-of-window WhatsApp follow-up is blocked unless the exact Meta template is approved and enabled.
- Unsupported media/message types are acknowledged safely and are not sent raw to the model.
- Opt-out language stops automated replies.
- Human takeover on the same WhatsApp AI number requires a protected operator reply surface or approved shared inbox.
- While a handoff session is `human_active`, AI replies are paused until explicit resume.
- Provider send failures and later delivery statuses must be tracked without blocking the web widget.

## Internal Sales Inbox

Purpose: allow the operator to control all SaaS sales leads who may subscribe, including leads from the web widget, the SaaS sales WhatsApp, plans-page intent, human handoff, checkout intent and custom-agent requests.

Required configuration:

- `INTERNAL_SALES_INBOX_TOKEN`;
- operator authentication or protected internal access policy;
- server-side permission to list sales lead conversations;
- server-side permission to update lead status and next action;
- server-side permission to send WhatsApp messages through the Meta provider adapter;
- trusted configured plan-page and checkout destinations;
- audit/tracking destination for takeover, reply, checkout-link send, resume and close actions.

Minimum states:

- `ai_active`
- `handoff_requested`
- `human_active`
- `waiting_customer`
- `follow_up_scheduled`
- `checkout_sent`
- `won`
- `lost`
- `do_not_contact`

Rules:

- Sales Inbox is the real-time control surface for our leads.
- Sales Inbox/Postgres is the lead pipeline/reporting destination and real-time control surface.
- Browser code never receives Meta provider credentials.
- Operator replies and status changes must update Sales Inbox state and may emit optional n8n alerts/digests.
- Checkout sent is not paid/subscribed; Spec 3 billing confirmation is required.
- The Sales Inbox is not the future studio/customer inbox and does not manage paying-studio student conversations.

## Session Store

Purpose: persist WhatsApp conversation state outside the browser.

Detailed persistence requirements, required tables and production blockers are defined in [persistence-readiness.md](./persistence-readiness.md).

Must store:

- channel session ID
- provider contact ID
- processed provider message IDs
- recent safe message history
- opt-out state
- selected pains
- recommended agents
- qualification draft
- fallback/guardrail counters
- last reply timestamp

Production options:

- Postgres as the primary persistence layer for Sales Inbox, WhatsApp sessions, idempotency, opt-out, audit and usage/debug records.
- Redis/KV as an optional short-lived counter/lock layer for rate limits and webhook locks.
- Postgres counters if Redis/KV is not available at first launch.

Local-only option:

- In-memory store for development, never production E2E.

## Commercial Configuration

The AI attendant reads, but does not own, commercial configuration.

Required config:

- plan IDs
- plan names
- prices
- recommended plan
- included agents per plan
- user, studio-unit, WhatsApp-channel and AI-message limits per plan
- onboarding/support/custom-agent policy per plan
- checkout/plan-selection URLs
- analysis destination
- human WhatsApp assistance destination
- custom-agent diagnostic enabled flag
- custom-agent diagnostic CTA labels and allowed destinations
- custom-agent diagnostic context variants
- public offer mode
- campaign stage

Rules:

- No hardcoded prices in prompts.
- No model-generated checkout URLs.
- Diagnostic report CTAs use only configured consultor, guided-demo and WhatsApp destinations.
- `guided_demo` from a diagnostic report stays gated by `guidedDemoReady`.
- A custom-agent diagnostic report cannot create checkout links directly.
- If price data is missing, route to human assistance or analysis instead of inventing.

## n8n

Required environment:

- `N8N_WEBHOOK_DIAGNOSTIC_HANDOFF`
- `N8N_WEBHOOK_HIGH_INTENT`
- `N8N_WEBHOOK_LEAD_ALERT`
- `N8N_WEBHOOK_OPERATOR_ACTION`
- `N8N_WEBHOOK_SAFETY_EVENT`
- optional `N8N_WEBHOOK_SECRET`

External n8n setup:

- No external CRM/spreadsheet account is required for v1 validation.
- n8n is optional for alerts, digests and allowed follow-up triggers only.
- Lead creation/update happens in the Sales Inbox database.

Rules:

- n8n runs after structured events.
- n8n is not the chat brain.
- n8n failure must not block chat, checkout CTA or WhatsApp reply.
- If n8n automation fails, log/notify the operator without blocking the visitor.

## Usage And Cost Controls

Required controls:

- max user message length
- max recent history sent to model
- per-session web rate limit
- per-contact WhatsApp rate limit
- daily AI request cap
- provider timeout
- fallback/degraded mode
- live-AI kill switch
- server-side usage event logging

Usage logs should capture:

- channel
- niche
- provider/model
- status
- latency
- token counts when available
- estimated cost when available
- fallback/guardrail category
- idempotency key for WhatsApp

Do not store full raw transcripts by default.
