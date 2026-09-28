# Rollout And Deploy

## Decision

The new LLM-first runtime is the official production replacement. There is no active production user base depending on the current deterministic runtime, so gradual rollout modes are not part of this plan.

## Execution Authority

Implementation can proceed autonomously for repository files, local migrations, local tests, fixtures, evals, and non-production verification.

Stop and request explicit user confirmation immediately before:

- applying a migration to a production database;
- deploying the Railway runtime to production;
- deploying the Next/Vercel integration to production;
- changing live WhatsApp/Meta/Dualhook production configuration;
- running live WhatsApp production tests that send real messages.

## Deployment Topology

```text
Vercel
|-- Next.js app
|-- /pilates
|-- widget endpoint
|-- WhatsApp webhook endpoint
`-- Sales Inbox

Railway
`-- taliya-agent-runtime
    |-- Python agent runtime
    |-- OpenAI Agents SDK pattern
    |-- generic /v1/agent-runs endpoint
    `-- taliya_commercial active agent

Postgres
|-- existing Sales Inbox/lead records
`-- generic agent_runtime_* records
```

## Cost Expectations

Expected fixed cost:

- Railway Hobby as the initial service plan unless production traffic later requires a larger plan.

Expected variable cost:

- OpenAI model usage per lead.
- Existing Vercel/Postgres/WhatsApp provider costs remain outside this feature unless already paid.

The runtime must measure actual token usage and cost when provider data is available.

## Required Environment Variables

### Vercel/Next

```text
TALIYA_AGENT_RUNTIME_URL
TALIYA_AGENT_RUNTIME_HMAC_SECRET
TALIYA_AGENT_RUNTIME_TIMEOUT_MS=60000
TALIYA_AGENT_RUNTIME_AGENT_KEY=taliya_commercial
```

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

## Cost Targets

Initial operating targets:

- Normal lead target: at or below US$0.05.
- Review threshold: US$0.10.
- Hard automatic AI cap: default US$0.15 per lead conversation.
- Hard cap can be raised up to US$0.30 only after explicit product-owner approval if quality requires it.

These are product budget targets. The runtime must record provider-reported usage and calculate actual cost from the configured model pricing table.

## Production Cutover

Required sequence:

1. Complete final product-owner diagnostic/demo/name correction tasks T206-T226.
2. Run zero-cost gates.
3. Run quota-limited real OpenAI smoke.
4. Run the full mapped behavior matrix.
5. Validate Sales Inbox completeness.
6. Product owner approves representative transcripts.
7. Request explicit user confirmation for production migration/deploy actions.
8. Deploy Railway runtime.
9. Configure Vercel env vars.
10. Deploy Next integration.
11. Run real WhatsApp smoke tests.
12. Mark `taliya_commercial` as official production path.

## Fallback Policy

Allowed:

- pause automation
- send short operational message
- mark for human follow-up
- suppress response when human is active

Disallowed:

- using old deterministic v2 as conversational rollback
- silently answering with stale product facts
- inventing product facts when runtime or product source fails

## Future Agents

Railway runtime may later host:

- `taliya_configuration`
- `studio_lead_capture`
- `studio_scheduling`
- `studio_reactivation`
- `studio_billing`
- `studio_support`
- `studio_retention`
- `studio_reporting`

These are reserved names only. They are not implemented by this spec.

## Out of scope for this spec

The reserved future keys do not create multi-tenant behavior, client-owned WhatsApp connections, studio customer data access, billing actions, schedule changes, or the seven studio operation agents. Those capabilities require separate specs, tenant isolation, tool permissions, evals, production migrations, and explicit deploy approval.
