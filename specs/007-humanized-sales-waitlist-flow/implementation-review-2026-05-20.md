# Implementation Review - 2026-05-20

## Scope Completed

- Shared AI attendant engine kept for widget and WhatsApp.
- WhatsApp cold-start policy now asks name before pitch, diagnostic, demo, plans or waitlist.
- After known name, the agent asks pain/intent before offering the diagnostic.
- Diagnostic completion asks for recommendation validation instead of jumping to checkout.
- Waitlist is offered only after high intent: positive post-diagnostic or positive post-demo.
- Waitlist `offered`, `pending_details`, `joined` and `declined` states are stored separately.
- Sales Inbox lead list exposes commercial stage, waitlist status, diagnostic status, demo status, source and pain/intent fields.
- WhatsApp webhook keeps duplicate protection, 24h window guard and Business App human takeover pause.
- Demo-ready state confirmed as `guidedDemoReady: false` in `data/landing/niches/pilates.ts`; the agent must not claim a real demo is available.
- Required waitlist fields implemented as: person name, studio name, city/state, WhatsApp/contact and pain/intent summary/source.

## Implementation Discoveries Reflected

- Checkout and plan recommendation needed a stricter diagnostic-first gate. The route matrix caught pre-diagnostic checkout-adjacent paths returning `plan_recommendation`; the gate now returns to diagnostic instead.
- Waitlist decline should still be auditable. Declines now create/update a `waitlist_intent` lead with `waitlistStatus=declined` instead of disappearing as chat-only text.
- Webhook evals needed reply text visibility to assert WhatsApp opening quality. The webhook result now includes a short `replyPreview` for test/debug responses.
- Lead pipeline evals were updated from the older checkout/plans lead contract to the current waitlist contract.

## Automated Results

- `npm run lint`: pass.
- `npx tsc --noEmit`: pass.
- `npm run build`: pass.
- `npm run eval:ai-sales-humanization -- --target=http://localhost:3108 --sales-token=codex_internal_sales_token`: 24/24 pass.
- `npm run eval:whatsapp-webhook -- --target=http://localhost:3108`: 8/8 pass.
- `npm run eval:lead-pipeline -- --target=http://localhost:3108 --sales-token=codex_internal_sales_token`: 4/4 pass.
- `npm run eval:ai-routes -- --target=http://localhost:3108 --sales-token=codex_internal_sales_token`: 25/25 pass, 5 skipped by harness rules.

## Local/Production-Like Simulation Notes

- Tests ran against `next start` on `http://localhost:3108`.
- WhatsApp send path used `META_WHATSAPP_ACCESS_TOKEN=mock` to avoid sending real Meta messages.
- Webhook signature, GET verify token, unsupported media, duplicate inbound, human Business App echo pause and outside-24h handling passed.
- Sales Inbox checks used `INTERNAL_SALES_INBOX_TOKEN=codex_internal_sales_token`.

## Pending Manual Gates

- R4 real WhatsApp number smoke review remains manual: send fresh messages to the Taliya number after deploy and confirm name -> pain/intent -> diagnostic, with no early waitlist.
- R5 product owner transcript review remains manual: read representative transcripts for P1 scenarios and approve tone/copy.
