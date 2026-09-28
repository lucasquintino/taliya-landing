# n8n Automation Map

## Current Decision

Sales Inbox/Postgres is the v1 source of truth for all SaaS sales leads. n8n is optional and must not be required for lead creation, lead update, WhatsApp replies, human takeover or operator actions.

## Allowed n8n Responsibilities

n8n may receive best-effort server-side events for:

- urgent hot-lead alerts;
- daily or periodic commercial digests;
- safety/fallback notifications;
- custom-agent diagnostic notifications;
- allowed follow-up reminders when the lead has contact/permission and is not opted out;
- operator-action notifications for internal awareness.

## Forbidden n8n Responsibilities In This Phase

n8n must not:

- own the lead database;
- receive a required lead-upsert webhook;
- decide prices, plans, checkout URLs or payment status;
- bypass WhatsApp opt-out, human pause, 24h window or template approval;
- mark a subscription as paid or active;
- store full raw transcripts by default.

## Runtime Events

The app may dispatch these optional events when the matching env var is configured:

- `landing_ai_attendant_high_intent`
- `landing_ai_attendant_analysis_handoff`
- `landing_ai_attendant_lead_alert`
- `landing_ai_attendant_operator_action`
- `landing_ai_attendant_safety_event`
- `landing_custom_agent_diagnostic`

There is no lead-upsert event in the current runtime contract.

## Failure Rule

If n8n is missing, slow or failing, the chat, WhatsApp webhook, Sales Inbox lead storage and operator actions must continue. The system records `externalSyncStatus` as skipped, pending or failed according to the local action context.
