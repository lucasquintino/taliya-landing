# Quickstart: Price, Plan And Humanized Agent Experience

## Automated Verification

Run from repository root after implementation:

```powershell
npm run eval:price-plan-commercial-matrix -- --target=http://localhost:3999 --sales-token=codex_sales_token --report=reports/price-plan-commercial-matrix.md
npm run eval:message-delivery-matrix -- --target=http://localhost:3999 --sales-token=codex_sales_token --report=reports/message-delivery-matrix.md
npm run eval:commercial-conversation-matrix -- --target=http://localhost:3999 --sales-token=codex_sales_token --report=reports/commercial-conversation-matrix-final.md
npm run eval:ai-sales-humanization -- --target=http://localhost:3999 --sales-token=codex_sales_token
npm run eval:whatsapp-webhook -- --target=http://localhost:3999
npm run eval:lead-pipeline -- --target=http://localhost:3999 --sales-token=codex_sales_token
npx tsc --noEmit
npm run lint
npm run build
```

Conversation-quality evals must call the real agent/runtime path and must include a usage summary in the generated report. Keep scenario count controlled, but do not use deterministic mock responses as the acceptance signal for tone, reasoning, CTA timing or price/plan behavior.

Also run legacy suites and classify failures:

```powershell
npm run eval:ai-routes -- --target=http://localhost:3999
npm run eval:ai-multiturn -- --target=http://localhost:3999
```

Failures caused by price/plans, delivery/humanization, waitlist, merge, handoff or Sales Inbox state must be fixed in this feature. Guardrail failures unrelated to this feature may be reported separately.

Before deploy, verify:
- agent price/plan answers match `/pilates/planos` or the shared commercial config;
- demo-unavailable requests do not invent a demo;
- WhatsApp webhook validation and provider-message idempotency still pass;
- send failures become operator-visible instead of disappearing silently;
- eval reports show usage/cost information for real-runtime conversation tests.

## Widget Manual Test Set

Before each scenario, clear the target widget session/lead.

1. Cold price: "Quanto custa?"
2. Cold plans: "Quero ver planos."
3. Recommendation without diagnostic: "Qual plano faz sentido?"
4. Pain then price: "Meu WhatsApp esta uma bagunca" then "Quanto custa?"
5. Diagnostic in progress then price: start diagnostic, answer one field, ask "quero saber valores primeiro."
6. Diagnostic complete then price/recommendation.
7. Buy without diagnostic: "Quero contratar."
8. Buy after diagnostic positive.
9. Expensive objection: "Achei caro."
10. Demo unavailable: "Quero ver uma demo."
11. Waitlist joined with minimum data.

For each scenario record:
- transcript
- message timing/splitting observations
- final lead state
- Sales Inbox result
- source-of-truth price/plan consistency
- pass/fail

## Post-Deploy WhatsApp Web Manual Test Set

These real-message tests require the deployed public webhook. They run after deploy and block public divulgation or paid lead capture, but they do not block the technical deploy itself.

Use the user's logged-in WhatsApp Web as lead sender. Before each scenario, clear the test phone/session/lead state.

1. Send "Quanto custa?" as first message.
2. Send "Lucas", then "qual valor?"
3. Send "quero ver planos"
4. Send "qual plano faz sentido?"
5. Send pain, then ask price.
6. Send media/audio/image and confirm text-summary fallback.
7. Complete diagnostic and ask price.
8. Complete diagnostic positive and join waitlist.
9. Ask for human and confirm handoff state.
10. Have a human reply from WhatsApp Business App and confirm AI pause.
11. Re-enable AI from the operator action and confirm the next inbound lead message can be answered automatically again.
12. Trigger beginning and mid-conversation rate limits and confirm the different pause messages, stored limit reason and no extra AI spend for the limited turn.

For each scenario validate:
- WhatsApp message split
- typing/delay behavior
- no inbound echo
- DB state
- Sales Inbox state
- missing waitlist fields, when status is `pending_details`
- funnel events/report visibility
- no early waitlist/checkout

## Production Smoke And Post-Deploy Gate

After push/deploy:

- `/pilates` returns 200.
- `/pilates/planos` returns 200.
- WhatsApp webhook GET verify still passes.
- Price question in widget behaves per spec.
- Price question in WhatsApp behaves per spec.
- Sales Inbox shows resulting cold/warm/hot/manual state.
- Human takeover and explicit re-enable behave per spec.
- Funnel events for tested scenarios are visible without Airtable/n8n.
- Send failure and webhook idempotency checks remain operator-visible and non-duplicating.

After the basic production smoke passes, run the Post-Deploy WhatsApp Web Manual Test Set above. Public lead capture starts only after those real WhatsApp transcripts pass.
