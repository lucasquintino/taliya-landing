# T012-055 - Public Activation Direct Path

Date: 2026-06-16

## Status

Completed.

Approved by the user's instruction to remove the extra paid-approval flag,
remove docs that mention it, and put the agent live. Public runtime smoke passed
on 2026-06-16 after Supabase was restored and the runtime schema was applied.

## What Changed

Removed the extra paid-approval runtime flag. Production activation no longer
depends on that extra flag.

In production, `/v1/taliya-commercial/turn` routes to the Spec 012 action-first
SDK runtime directly. Local/test contexts may still enable the action-first path
for mocked/injected-model tests with `TALIYA_SPEC012_ACTION_FIRST_ENABLED`, but
production no longer needs an extra paid-approval switch.

## Activation Behavior

When the runtime is configured as production:

```text
TALIYA_AGENT_RUNTIME_ENV=production
TALIYA_AGENT_PROVIDER=openai
```

the commercial endpoint uses the Spec 012 action-first SDK path.

The runtime still requires production safety settings through `/healthz`:

- `OPENAI_API_KEY`
- `DATABASE_URL`
- non-default `TALIYA_AGENT_RUNTIME_HMAC_SECRET`
- `TALIYA_AGENT_MODEL`

The per-conversation cost cap remains:

```text
TALIYA_AGENT_HARD_COST_CAP_USD=0.15
```

## Deployment And Supabase Verification

- Railway service: `taliya-agent-runtime`
- Production URL: `https://taliya-agent-runtime-production.up.railway.app`
- Deployment id observed online: `16d42cc7-0f3b-47a8-917b-43466f8a358b`
- Health check: `GET /healthz` returned
  `{"ok":true,"service":"taliya-agent-runtime","environment":"production"}`.
- Supabase project: `Taliya` / `pxvabrsngfhebytdqxth`
- Supabase status from connector: `ACTIVE_HEALTHY`
- Database SQL check succeeded as `postgres`.
- Runtime schema migration applied through the Supabase connector:
  `agent_runtime_tables`.
- Runtime hardening migration applied through the Supabase connector:
  `agent_runtime_enable_rls`.
- Confirmed 11 `agent_runtime_*` tables exist.
- Confirmed RLS is enabled on the runtime tables with no public policies.

The earlier production smoke blocker was the paused/quota-affected Supabase
project and missing runtime schema. After the project was restored, the existing
`DATABASE_URL` connected successfully and saw all runtime tables.

## What Did Not Change

- No `/pilates` visual/layout/copy change.
- No Sales Inbox UI change.
- No checkout.
- No multi-tenant.
- No client/studio WhatsApp.
- No external/provider trace export with lead text.
- No old deterministic commercial brain fallback.

## Rollback

Immediate operational rollback remains:

```text
TALIYA_SPEC012_ACTION_FIRST_ENABLED=false
```

for non-production contexts, or switching production off the Spec 012 runtime
deployment/config if needed.

If Spec 012 is disabled and the Spec 011 commercial core is also disabled, the
endpoint returns a controlled `spec011_core_disabled` error instead of silently
using the old commercial brain.

## Anti-Determinism Review

This is an activation/routing change only.

It does not add raw lead-text routing, regex commercial understanding,
template-first shortcuts, SDK free-form direct delivery, or SDK tool commits
during reasoning. The LLM remains the commercial brain through the action-first
Agents SDK pipeline.

## Paid-Call Status

This change enables the production runtime to call OpenAI when production is
configured with provider `openai`.

Paid runtime verification completed:

- Endpoint: `POST /v1/taliya-commercial/turn`
- Request id: `req_spec012_public_smoke_1781620949`
- Conversation id: `conv_spec012_public_smoke_1781620949`
- Lead message: `Oi, quanto custa a Taliya?`
- HTTP status: `200`
- Runtime status: `succeeded`
- Current agent: `taliya_triage_agent`
- Model: `gpt-5.4-mini`
- Recorded cost: `$0.0041955`
- Persisted in Supabase:
  - `agent_runtime_conversations.cost_usd = 0.004196`
  - `agent_runtime_state.cost_usd = 0.004196`

Assistant response chunks:

```text
Oi, tudo bem?

Base: R$ 197/mês. Essencial: R$ 497/mês. Avance: R$ 897/mês. Completo: R$ 1.497/mês.
```

```text
Se fizer sentido para você, estamos oferecendo um diagnóstico gratuito para o seu studio. Assim você entende se algum dos nossos planos te atenderia.

Com poucas perguntas, eu entendo a rotina do studio e te devolvo o que organizar primeiro, quais agentes fariam sentido e qual plano vale comparar.
```

```text
O que você acha?
```
