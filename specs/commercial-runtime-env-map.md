# Commercial Runtime Env Map

Date: 2026-05-07

Purpose: list the runtime configuration needed for Spec 1 and Spec 2. Values are not stored here.

## Required For Local Web Consultor

| Env var | Required | Owner | Used by | Notes |
| --- | --- | --- | --- | --- |
| `OPENAI_API_KEY` | Yes for real AI | Operator/OpenAI | server AI provider | ChatGPT subscription is not enough; this must be an OpenAI Platform API key |
| `AI_ATTENDANT_MODEL` | Optional | Operator | server AI provider | Defaults in code if absent |
| `AI_ATTENDANT_DISABLED` | Optional | Operator | AI kill switch | `1` or `true` disables live AI and forces degraded behavior |
| `AI_ATTENDANT_WEB_RATE_LIMIT_PER_MINUTE` | Optional | Operator | usage guard | Default exists in code |
| `AI_ATTENDANT_DAILY_REQUEST_CAP` | Optional | Operator | usage guard | Default exists in code |

## Required For WhatsApp

| Env var | Required | Owner | Used by | Notes |
| --- | --- | --- | --- | --- |
| `META_WHATSAPP_ACCESS_TOKEN` | Yes for sending | Meta | WhatsApp adapter | Server-side only |
| `META_WHATSAPP_PHONE_NUMBER_ID` | Yes for sending | Meta | WhatsApp adapter | Server-side only |
| `META_WHATSAPP_BUSINESS_ACCOUNT_ID` | Setup | Meta | provider/admin setup | Currently documented for setup; not directly used by code yet |
| `META_WHATSAPP_APP_SECRET` | Yes for webhook POST | Meta | webhook signature verification | Missing secret blocks verified inbound POST |
| `META_WHATSAPP_WEBHOOK_VERIFY_TOKEN` | Yes for webhook GET | Operator/Meta | webhook challenge verification | Random token configured in Meta app and app env |
| `AI_ATTENDANT_WHATSAPP_RATE_LIMIT_PER_MINUTE` | Optional | Operator | usage guard | Default exists in code |

## Required For Sales Inbox

| Env var | Required | Owner | Used by | Notes |
| --- | --- | --- | --- | --- |
| `INTERNAL_SALES_INBOX_TOKEN` | Yes | Operator | `/internal/sales-inbox` and internal APIs | Temporary protected access token for v1 |

Access pattern:

```text
/internal/sales-inbox?token=INTERNAL_SALES_INBOX_TOKEN
```

API calls can also use:

```text
Authorization: Bearer INTERNAL_SALES_INBOX_TOKEN
```

or:

```text
x-internal-sales-token: INTERNAL_SALES_INBOX_TOKEN
```

## Required For n8n

| Env var | Required | Owner | Used by | Notes |
| --- | --- | --- | --- | --- |
| `N8N_WEBHOOK_DIAGNOSTIC_HANDOFF` | Recommended | n8n | analysis handoff | Best-effort; failure must not block chat |
| `N8N_WEBHOOK_HIGH_INTENT` | Recommended | n8n | high-intent conversion event | Best-effort |
| `N8N_WEBHOOK_LEAD_ALERT` | Recommended | n8n | urgent lead alerts | Secondary alert, not source of truth |
| `N8N_WEBHOOK_OPERATOR_ACTION` | Recommended | n8n | Sales Inbox action sync | Sync safe status/summary/next-action |
| `N8N_WEBHOOK_SAFETY_EVENT` | Recommended | n8n | guardrail/fallback alerts | Best-effort |
| `N8N_WEBHOOK_SECRET` | Optional | n8n/operator | webhook sender | Sent as `x-webhook-secret` when configured |

## Required Inside n8n, Not The App Browser

| Credential | Required | Owner | Notes |
| --- | --- | --- | --- |
| Notification destination | Optional | n8n/operator | Email/Slack/WhatsApp alert destination |

## Not Needed Yet

These belong to later reviewed specs after the real SaaS spec exists:

- billing provider secrets;
- subscription webhook secrets;
- tenant database credentials for real SaaS app;
- mobile app push credentials;
- paying-studio WhatsApp credentials;
- onboarding magic link/OTP provider credentials.

## Local Minimum Modes

### Docs/UI Only

No env vars required. Static pages can render.

### Web Consultor Real AI

Required:

```text
OPENAI_API_KEY
```

Recommended:

```text
AI_ATTENDANT_MODEL
INTERNAL_SALES_INBOX_TOKEN
```

### WhatsApp E2E

Required:

```text
OPENAI_API_KEY
META_WHATSAPP_ACCESS_TOKEN
META_WHATSAPP_PHONE_NUMBER_ID
META_WHATSAPP_APP_SECRET
META_WHATSAPP_WEBHOOK_VERIFY_TOKEN
INTERNAL_SALES_INBOX_TOKEN
```

### Lead Pipeline E2E

Required:

```text
N8N_WEBHOOK_HIGH_INTENT
N8N_WEBHOOK_OPERATOR_ACTION
```

Recommended:

```text
N8N_WEBHOOK_LEAD_ALERT
N8N_WEBHOOK_DIAGNOSTIC_HANDOFF
N8N_WEBHOOK_SAFETY_EVENT
N8N_WEBHOOK_SECRET
```

## Safety Rules

- Never expose OpenAI, Meta, n8n, database or future billing secrets to browser code.
- n8n failures must not block chat, WhatsApp reply, Sales Inbox control or plan/demo CTA rendering.
- Sales Inbox/Postgres is the pipeline/reporting source of truth and real-time control surface.
- Checkout/payment envs must not be added until Spec 3 is reviewed against the real SaaS spec.
