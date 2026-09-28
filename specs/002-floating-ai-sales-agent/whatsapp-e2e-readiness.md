# WhatsApp E2E Readiness: Floating AI Attendant

## Purpose

Define the production end-to-end behavior for the SaaS sales WhatsApp channel.

This document complements `human-whatsapp-handoff.md`, `runtime-configuration.md`, `persistence-readiness.md` and `whatsapp-template-copy.md`. It exists so the WhatsApp channel is not only a local webhook demo, but a production-safe sales channel using the same Atendente IA behavior as the landing widget.

## Scope

Included:

- inbound WhatsApp conversations with the SaaS operator's own sales number;
- same AI attendant answer policy used by the web widget;
- Meta WhatsApp Cloud API webhook verification;
- message idempotency;
- opt-out handling;
- handoff to the Internal Sales Inbox;
- human takeover on the same number;
- operator replies through the server-side provider adapter;
- Sales Inbox/n8n optional automation lead sync as asynchronous pipeline/reporting;
- approved WhatsApp templates for proactive or out-of-window follow-up.

Excluded:

- cold outbound prospecting;
- broadcast campaigns;
- unofficial WhatsApp gateways;
- studio/customer student conversations;
- the future inbox sold to paying studios;
- automatic billing activation or subscription entitlement.

## Current Implementation State

Already implemented for local/dev validation:

- `GET /api/landing/ai-attendant/whatsapp` verifies the Meta webhook challenge with the configured verify token.
- `POST /api/landing/ai-attendant/whatsapp` validates `x-hub-signature-256` with `META_WHATSAPP_APP_SECRET`.
- inbound text/button/interactive replies are normalized into the shared `AiAttendantRequest`.
- provider message IDs are deduplicated before an AI reply is sent.
- the WhatsApp channel uses the same `runAiAttendantTurn` engine as the web widget.
- opt-out language can mark a WhatsApp session as opted out.
- Sales Inbox state can pause AI replies when the lead is `human_active`, `do_not_contact` or `aiPaused`.
- operator replies use the server-side Meta WhatsApp adapter.
- n8n may receive high-intent, safety, urgent-alert and operator-action events when configured.

Not production-ready yet:

- WhatsApp sessions, idempotency and Sales Inbox state are still local memory until the persistence tasks are implemented.
- provider delivery status webhooks are not yet consumed as a first-class event stream.
- failed WhatsApp sends do not yet have a durable retry/outbox queue.
- out-of-window proactive messages must remain blocked until approved templates are configured in Meta.
- message types other than supported text/button/interactive replies need an explicit user-safe response policy.
- live E2E testing with a real Meta app, test number, webhook URL and production-like secrets is still pending.

## End-To-End Inbound Flow

1. Meta sends webhook verification to `GET /api/landing/ai-attendant/whatsapp`.
2. The route validates `hub.mode`, `hub.verify_token` and `hub.challenge`.
3. Meta sends inbound message events to `POST /api/landing/ai-attendant/whatsapp`.
4. The route reads the raw body before parsing JSON.
5. The route validates `x-hub-signature-256` with `META_WHATSAPP_APP_SECRET`.
6. Unsupported payloads are acknowledged safely without running the AI.
7. Supported inbound text/button/interactive messages become `WhatsAppInboundTurn`.
8. Provider message ID is registered before any reply attempt.
9. Duplicate provider message IDs return success/ignored behavior without sending a second reply.
10. The system checks session opt-out and Sales Inbox terminal/human states.
11. If `human_active`, `aiPaused` or `do_not_contact`, the inbound user message is stored and no AI reply is sent.
12. Otherwise the turn is normalized into the shared AI attendant request.
13. The agent answers using trusted product/config context and the same commercial rules as the web widget.
14. The route stores safe recent messages, selected pains, recommended agents and qualification patch.
15. Opt-out intent marks the session and lead as `do_not_contact` when applicable.
16. A safe WhatsApp text reply is sent through the Meta provider adapter when allowed.
17. Usage/tracking metadata is logged without raw full transcript storage by default.
18. Conversion or guardrail events are emitted to n8n asynchronously.
19. Lead storage and urgent alert events update Sales Inbox visibility.
20. The webhook returns a provider-safe JSON acknowledgement.

## Human Takeover Flow

Human takeover on the same WhatsApp number requires the Internal Sales Inbox.

Required behavior:

- the operator clicks `take_over`;
- Sales Inbox sets the lead to `human_active` and `aiPaused=true`;
- future inbound WhatsApp messages are stored but do not trigger AI replies;
- the operator sends WhatsApp replies through the protected server route;
- the browser never receives Meta credentials;
- operator actions create audit records and n8n sync events;
- `resume_ai` is required before automated replies can continue;
- `won`, `lost` and `do_not_contact` remain terminal for automation unless a later explicit allowed inbound context restarts the relationship.

## WhatsApp Conversation Window And Templates

Rules:

- Free-form automated replies are allowed only inside an inbound/opted-in WhatsApp conversation where provider policy allows it.
- The system must not send proactive or out-of-window sales follow-up unless the exact template is approved and enabled in Meta.
- Template drafts live in `whatsapp-template-copy.md`.
- n8n or the operator may request a template send only after eligibility checks.
- Template failure, rejection, paused status or missing approval must block the proactive send and keep the lead visible in Sales Inbox.
- Each template attempt must use an idempotency key based on lead, template, trigger and cycle.

Minimum template eligibility checks:

- contact is not opted out;
- lead is not `do_not_contact`, `lost` or already paid/won for that follow-up purpose;
- template exists in the approved provider configuration;
- template category and language match the approved Meta setup;
- variables are filled only from safe fields;
- service-window status is checked before deciding free-form vs template.

## Unsupported WhatsApp Message Types

V1 supports text, button text and interactive button replies.

For images, audio, documents, location, stickers or unknown payloads:

- acknowledge the webhook safely;
- do not send the media or raw payload to the model;
- store minimal safe metadata when persistence is available;
- optionally send a short text asking the visitor to describe the request in words if the service window allows;
- route to Sales Inbox if the unsupported type appears during human handoff or checkout-ready conversations.

The agent must not claim it viewed or understood unsupported media unless a future media-processing capability is explicitly implemented.

## Delivery Status And Retry Policy

Production must distinguish:

- inbound accepted;
- AI turn generated;
- provider send requested;
- provider send accepted;
- provider delivery status received;
- send failed;
- retry queued;
- retry exhausted.

Required behavior:

- immediate Meta send failures return/log `floating_agent_whatsapp_delivery_failed`.
- failed operator sends remain visible in Sales Inbox and can be retried.
- provider status webhooks should update the message/send record when Meta later reports delivered, read, failed or deleted statuses.
- retries must use an outbox/idempotency key so the same logical reply is not duplicated.
- Sales Inbox/n8n optional automation sync failure must not block WhatsApp conversation control.

## Security And Guardrails

Production requirements:

- reject invalid/missing Meta signatures.
- keep Meta tokens, app secret and phone number ID server-side only.
- do not accept browser-originated WhatsApp provider sends outside the protected Sales Inbox API.
- do not store raw full transcripts by default.
- redact or avoid unnecessary sensitive student/payment data.
- honor opt-out immediately.
- never collect card data or payment credentials in WhatsApp.
- use trusted configured plan, checkout and plan-page links only.
- do not let n8n bypass opt-out, template approval, human pause or provider idempotency.

## Required Production Tests

Before public WhatsApp E2E launch:

- verify Meta webhook challenge with the real callback URL;
- reject invalid signature POST requests;
- accept a valid signed inbound text message;
- ignore duplicate provider message IDs without a second reply;
- map equivalent web and WhatsApp pain prompts to the same agents;
- preserve multi-turn WhatsApp context after process restart;
- stop automation after opt-out and after `do_not_contact`;
- suppress AI replies while Sales Inbox lead is `human_active`;
- allow operator reply through the server-side provider adapter;
- record failed operator sends and allow retry;
- block out-of-window proactive follow-up without an approved template;
- send an approved template only after eligibility checks;
- handle unsupported media without passing raw payload to the model;
- verify Sales Inbox/n8n optional automation failure does not block WhatsApp replies or Sales Inbox control.

## Production Blockers

The WhatsApp channel must not be considered production-ready until these are complete:

1. Durable Postgres persistence for WhatsApp sessions, idempotency, opt-out, Sales Inbox leads, messages and operator actions.
2. Strict Meta signature verification in the deployed route with real app secret.
3. Real Meta app, WhatsApp Business Account, phone number, webhook URL and access token configured.
4. Provider status webhook handling or an equivalent durable delivery/failure event model.
5. Retry/outbox behavior for failed provider sends.
6. Approved templates for every proactive/out-of-window follow-up branch that will be enabled.
7. Sales Inbox authentication and operator policy enabled before same-number human takeover is claimed.
8. Live E2E test from a real WhatsApp contact through AI reply, human takeover, operator reply, opt-out and n8n lead sync.
