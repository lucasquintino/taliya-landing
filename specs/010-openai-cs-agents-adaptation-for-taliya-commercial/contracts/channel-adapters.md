# Contract: Channel Adapters

## Overview

Next.js remains the channel boundary. Channel adapters normalize inbound events, call the Railway runtime, validate response status, persist delivery results, and render/send messages.

## Widget Adapter

Existing boundary:

- `app/api/landing/ai-attendant/route.ts`
- `components/landing/shared/FloatingAiAttendant.tsx`

Responsibilities:

- preserve existing `/pilates` visual layout
- manage widget session id
- pass page path, source, entry intent, UTM metadata
- call `POST /v1/agent-runs` with HMAC
- render validated runtime messages
- render only validated widget actions/links
- render validated quick replies/buttons when available
- render validated demo CTA/button when the runtime selects an official demo action
- preserve short-message delivery with widget typing/delay behavior
- persist lead/message results through existing stores

Must not:

- decide commercial intent through state machine
- select commercial behavior without the runtime
- invent product facts
- bypass runtime guardrails
- redesign landing sections or widget visuals

## WhatsApp Adapter

Existing boundary:

- `app/api/landing/ai-attendant/whatsapp/route.ts`
- `lib/landing/ai-attendant/whatsapp.ts`

Responsibilities:

- preserve Meta/Dualhook GET verification
- validate allowed phone number/connection
- normalize inbound text and provider metadata
- identify unsupported media
- detect manual WhatsApp Business App echoes when possible
- deduplicate provider retries
- call `POST /v1/agent-runs` with HMAC
- send validated messages through Cloud API
- attempt typing indicators and proportional delays
- convert widget-only buttons into approved text or official links
- render demo CTA as an official full link when the runtime selects a demo action
- log statuses and delivery errors

Must not:

- ask for the user's WhatsApp phone number
- decide diagnostic/waitlist/handoff logic
- respond while human handoff is active
- create duplicate replies for duplicate webhooks
- use the old deterministic runtime as fallback

## Delivery Rules

Widget:

- Can render up to the validated message list.
- Can show validated quick replies, buttons, or links.
- Must preserve short bubbles and avoid text walls.
- Must respect typing/delay behavior where supported by the existing widget.
- Must not introduce new visual design for `/pilates`.

WhatsApp:

- Target max 3 chunks per assistant turn unless explicitly approved.
- Target chunk length under 320 characters.
- Attempt typing before every chunk.
- Delay between chunks should feel human but remain bounded.
- Use official links/text instead of widget buttons.
- Completed diagnostic staged delivery is an explicitly approved exception to the normal 3 chunk target, as long as each chunk is short and the typing/delay plan is present.
- Demo links must be absolute official URLs, not relative paths.
- Delivery failure must be logged without retry storms.

## Operational Fallbacks

Allowed fallback cases:

- runtime unavailable
- model provider timeout
- invalid structured output after repair
- product knowledge unavailable for a required fact
- cost cap reached
- human handoff active

Allowed fallback actions:

- no reply and mark for human
- short safe operational message
- pause automation

Disallowed fallback:

- old deterministic sales conversation engine
