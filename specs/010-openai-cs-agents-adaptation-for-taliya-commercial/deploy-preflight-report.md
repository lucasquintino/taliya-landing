# Deploy Preflight Report

Date: 2026-05-23

Status: **local/runtime preflight passed; external production deploy blocked by missing deploy credentials/project linking**.

This report reflects the latest validation after the final Taliya commercial agent corrections, production Postgres migration, and local end-to-end smokes. No Railway, Vercel, Meta, Dualhook, or live WhatsApp production deploy was completed from this workspace because the required deploy CLIs/tokens/project metadata are not available in the current environment.

## Checked Items

| Item | Result | Evidence |
| --- | --- | --- |
| Runtime Python tests | PASS | `python -m pytest services/taliya-agent-runtime/tests -q`: `121 passed` |
| Next lint | PASS | `npm run lint` |
| Next production build | PASS | `npm run build` compiled, typechecked, and generated routes successfully |
| Zero-cost gates | PASS | `node scripts/eval-agent-runtime-zero-cost-gates.mjs`: `6/6 passed` |
| Real OpenAI correction matrix | PASS | `python scripts/eval-agent-runtime-real-openai.py --fixture scripts/fixtures/agent-runtime/real-openai-final-corrections.json --report-name agent-runtime-real-openai-final-corrections-latest`: `8/8 passed` |
| Widget visual smoke | PASS | Desktop/mobile screenshots under `test-results/taliya-widget-smoke/`; demo CTA rendered as widget action with `https://www.taliya.com.br/pilates/planos/demonstracao` |
| Sales Inbox local smoke with real Postgres/OpenAI | PASS | Latest smoke session `prod_widget_smoke_lead_20260523135540`, lead `lead_j5f1qa`: one lead per session, diagnostic saved, waitlist joined, contact/studio/city saved, 23 recent messages, handoff paused |
| Production Postgres migration | PASS | `services/taliya-agent-runtime/migrations/001_agent_runtime_tables.sql` applied to configured Postgres/Supabase; idempotency unique index corrected and reapplied |
| Runtime config guard | PASS | Production validation blocks incomplete provider/API key/database/HMAC config |
| Docker/Railway static config | PASS | `services/taliya-agent-runtime/Dockerfile` and `railway.toml` are present |
| Railway deploy | BLOCKED | `railway` CLI missing and no `RAILWAY_TOKEN`/project link available |
| Vercel deploy | BLOCKED | `vercel` CLI missing, no `VERCEL_TOKEN`, and no `.vercel/project.json` link available |
| Live WhatsApp smoke | BLOCKED | Requires deployed public URL and Meta/Dualhook production webhook configuration |

## Production Env Vars Required

### Railway Runtime

```text
OPENAI_API_KEY
DATABASE_URL
TALIYA_AGENT_RUNTIME_HMAC_SECRET
TALIYA_AGENT_RUNTIME_HMAC_MAX_SKEW_SECONDS=300
TALIYA_AGENT_PROVIDER=openai
TALIYA_AGENT_MODEL=gpt-5.4-mini
TALIYA_AGENT_GUARDRAIL_MODEL=gpt-4.1-mini
TALIYA_AGENT_STRONG_MODEL=gpt-5.2
TALIYA_AGENT_HARD_COST_CAP_USD=0.15
TALIYA_AGENT_REVIEW_COST_USD=0.05
TALIYA_AGENT_HIGH_COST_USD=0.10
TALIYA_AGENT_RUNTIME_ENV=production
```

### Vercel/Next

```text
TALIYA_AGENT_RUNTIME_URL=https://<railway-service>.up.railway.app
TALIYA_AGENT_RUNTIME_HMAC_SECRET=<same-secret-as-runtime>
TALIYA_AGENT_RUNTIME_TIMEOUT_MS=60000
TALIYA_AGENT_RUNTIME_AGENT_KEY=taliya_commercial
DATABASE_URL
INTERNAL_SALES_INBOX_TOKEN
META_WHATSAPP_ACCESS_TOKEN
DUALHOOK_WEBHOOK_SECRET
```

## Current Deploy Blockers

- Install/login or provide non-interactive credentials for Railway.
- Link or create the Railway project/service for `services/taliya-agent-runtime`.
- Install/login or provide non-interactive credentials for Vercel.
- Link the Vercel project for the Next app.
- Deploy the runtime first and copy the Railway public URL into Vercel as `TALIYA_AGENT_RUNTIME_URL`.
- Configure the same `TALIYA_AGENT_RUNTIME_HMAC_SECRET` on Railway and Vercel.
- Configure Meta/Dualhook webhook callback to the deployed Next WhatsApp route.
- Run a live WhatsApp smoke after deploy.

## Latest Local Smoke Transcript Summary

Session `prod_widget_smoke_lead_20260523135540`:

1. Lead: `quero fazer diagnostico gratuito`
   Taliya started diagnostic with a short confirmation and first question.
2. Lead: `Lucas`
   Taliya stored the real name and continued the pending diagnostic question.
3. Lead gave 80 students, spreadsheet, agenda/repositions pain, urgent timing.
   Taliya acknowledged the fact and asked priority without repeating already answered fields.
4. Lead asked to organize repositions and compare plan.
   Taliya delivered diagnostic, CRM-first recommendation, indicated Agenda/Atendimento, plan range, and demo next step.
5. Lead explicitly asked to join waitlist with studio, city, WhatsApp.
   Taliya joined waitlist and preserved details.
6. Lead asked for human.
   Taliya acknowledged handoff; Sales Inbox operator takeover paused the AI.

## Conclusion

The codebase is locally ready for an external production cutover, and the production database schema has been applied. The actual Railway/Vercel/WhatsApp production deploy remains blocked by deployment credentials, project linking, public runtime URL setup, and live webhook validation.
