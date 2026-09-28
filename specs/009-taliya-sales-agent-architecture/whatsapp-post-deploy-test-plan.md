# WhatsApp Post-Deploy Test Plan

Run after production deploy. `AI_ATTENDANT_V2_MODE` can remain unset because v2 is the default production path.

## Preflight

- Confirm Vercel envs: `META_WHATSAPP_ACCESS_TOKEN`, `META_WHATSAPP_PHONE_NUMBER_ID`, `META_WHATSAPP_WEBHOOK_VERIFY_TOKEN`, `INTERNAL_SALES_INBOX_TOKEN`. `AI_ATTENDANT_V2_MODE` is optional and defaults to v2 auto.
- Confirm Dualhook webhook override points to `https://www.taliya.com.br/api/landing/ai-attendant/whatsapp`.
- Confirm GET verification still returns Meta challenge.
- Confirm Sales Inbox opens and shows v2 fields.

## Test 1 - First Direct Question

Message from personal WhatsApp:

> Quanto custa a Taliya?

Expected:

- First reply is split: greeting first, answer second.
- If WhatsApp profile name is reliable, greeting uses first name.
- Price/plan information is answered before diagnostic.
- No checkout/payment link is sent.
- Sales Inbox shows channel `whatsapp`, `price_or_plan`, trace id and cost.

## Test 2 - Diagnostic Flow

Messages:

1. Quero fazer diagnostico gratuito
2. 96
3. Vendas e interessados
4. Hoje uso WhatsApp e planilha
5. Perco interessados por demora no retorno
6. Quero aliviar WhatsApp e agenda primeiro
7. faz sentido
8. pode ser
9. Studio do Lucas, Vitoria

Expected:

- WhatsApp does not ask for phone.
- Questions are not repeated.
- Diagnostic includes bottleneck, cause, first step, indicated agents and plan/range.
- Waitlist is offered only after positive validation.
- Final lead is waitlist joined or pending only for studio/city if missing.

## Test 3 - Post-Waitlist Question

After joined:

> quanto custa depois?

Expected:

- Agent answers price/plans.
- Agent confirms the studio remains on the waitlist.
- It does not restart diagnostic or ask waitlist details again.

## Test 4 - Human Takeover

From WhatsApp Business App, manually reply to the same lead.

Expected:

- Inbound echo is recorded.
- AI is paused/human active.
- Next lead message is recorded but no automatic AI reply is sent.
- Sales Inbox shows human/handoff status.

## Test 5 - Unsupported Media

Send an image/audio.

Expected:

- Agent asks for a short text description or offers human help.
- No hallucinated interpretation of media.

## Rollback

Set `AI_ATTENDANT_V2_MODE=legacy` or `AI_ATTENDANT_V2_KILL_SWITCH=true`, redeploy/restart if required, then repeat one WhatsApp message to confirm legacy path or no v2 auto response.
