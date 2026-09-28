# T012-059 Luna production switch attempt 1

## Result

The first production switch was stopped and rolled back. The Luna deployment
itself reached `SUCCESS`, but the approved public production smoke could not
reach the agent because the runtime database was unavailable before model
execution.

## Deployment evidence

- Service: `taliya-agent-runtime`.
- Environment: `production`.
- Luna switch deployment: `7cf61829-aaec-4fdb-b444-d062f2de0873`.
- Health after switch: `ok=true`, model `gpt-5.6-luna`, OpenAI `2.44.0`,
  Agents SDK `0.18.0`.
- Public smoke session: `t012059_luna_prod_smoke_1785893861`.
- Public smoke message: `como funciona no WhatsApp?`.
- Public result: operational fallback with guardrail category
  `provider_failure` and reason `runtime_database_unavailable`.
- Runtime HTTP result: `503 Service Unavailable` from
  `/v1/taliya-commercial/turn`.

## Root-cause evidence

Railway logs show the Supabase transaction pooler returning:

`FATAL: (ENOTFOUND) tenant/user postgres.pxvabrsngfhebytdqxth not found`

The configured `DATABASE_URL` exists and targets the expected Supabase pooler
host on port `6543`. Supabase project `pxvabrsngfhebytdqxth` reported
`INACTIVE`, and a direct SQL probe timed out. The failure therefore occurred
during the runtime's first database/idempotency read, before the commercial
agent or OpenAI model could run.

## Cost and rollback

The failed response contained no model usage or cost record. No OpenAI spend is
confirmed for this production attempt, so the T012-057 budget ledger remains
unchanged.

The stop condition triggered an immediate model rollback. Railway deployment
`fb31d45d-245f-4d72-97ce-1f581766575a` reached `SUCCESS`, and production health
again reported `gpt-5.4-mini` with the pinned SDK versions.

The existing Supabase project was then requested for restoration. No schema,
table, product behavior, public landing layout, or legacy commercial brain was
changed. T012-059 remains open until database connectivity is proven without
an OpenAI call and a fresh controlled Luna smoke passes.
