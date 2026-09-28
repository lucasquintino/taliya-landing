# Taliya Agent Runtime Environment

This replaces the old v2 runtime flags as the official production path for the Taliya commercial agent.

## Next.js Channel Adapter

- `TALIYA_AGENT_RUNTIME_URL`: Railway runtime base URL, for example `https://<service>.up.railway.app`
- `TALIYA_AGENT_RUNTIME_HMAC_SECRET`: shared HMAC secret used by Next.js and the Python runtime
- `TALIYA_AGENT_RUNTIME_TIMEOUT_MS`: default `60000`
- `TALIYA_AGENT_RUNTIME_AGENT_KEY`: default `taliya_commercial`

The Next.js adapter must not fall back to the old deterministic conversation engine for normal production turns. If the runtime is unavailable, it may send a short operational fallback or pause for human handling.

## Python Runtime

- `TALIYA_AGENT_RUNTIME_ENV`: `local`, `staging`, or `production`
- `TALIYA_AGENT_RUNTIME_HMAC_SECRET`: same secret configured in Next.js
- `TALIYA_AGENT_PROVIDER`: `openai` in production, `mock` only for local tests/evals
- `OPENAI_API_KEY`: required when `TALIYA_AGENT_PROVIDER=openai`
- `TALIYA_AGENT_MODEL`: default production target `gpt-5.6-luna`
- `TALIYA_AGENT_GUARDRAIL_MODEL`: default `gpt-4.1-mini`
- `TALIYA_AGENT_STRONG_MODEL`: optional escalation model, recommended `gpt-5.2`
- `TALIYA_AGENT_HARD_COST_CAP_USD`: default `0.15`
- `TALIYA_AGENT_REVIEW_COST_USD`: default `0.05`
- `TALIYA_AGENT_HIGH_COST_USD`: default `0.10`
- `TALIYA_SIMPLE_OPENING_TRIAGE_ENABLED`: default `true`. This enables a small LLM-only first-message triage for strictly simple openings such as direct price, direct demo, or thin diagnostic requests. It is not the conversation brain: it must fall back to the full commercial agent for any context, pain, numbers, plan-fit, WhatsApp implementation, buying intent, ambiguity, previous state, invalid output, timeout, or low confidence. Set to `false` only as an operational kill switch.
- `DATABASE_URL`: Postgres connection string for `agent_runtime_*` tables

In production, the commercial endpoint uses the Spec 012 action-first Agents SDK
runtime directly.

The action-first agents use `reasoning.effort=none` for predictable latency and
cost on this conversational workload. The active model remains an environment
setting so an operator can roll back by restoring the previously validated model
and redeploying the service. This is an operational model switch, not a public
fallback to the removed legacy conversation engine.

For GPT-5.6, usage accounting must include ordinary input, cache-read input,
cache-write input, and output. Cache writes are billed at 1.25 times the Luna
uncached input rate and are included in the per-conversation hard cost cap.

When `TALIYA_AGENT_RUNTIME_ENV=production`, the runtime healthcheck fails with `503` until these production requirements are met:

- `TALIYA_AGENT_PROVIDER=openai`
- `OPENAI_API_KEY` is configured
- `DATABASE_URL` is configured
- `TALIYA_AGENT_RUNTIME_HMAC_SECRET` is not `dev-secret` and is long enough for production use
- `TALIYA_AGENT_MODEL` is configured

## Real OpenAI Evaluation

Run the real provider gate before treating the agent as conversation-ready:

```powershell
npm run eval:agent-runtime:real-openai
```

This runner refuses mock behavior, loads `OPENAI_API_KEY` from `.env.local` when present, forces `TALIYA_AGENT_PROVIDER=openai`, and writes complete transcripts to:

```text
specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/agent-runtime-real-openai-latest.md
```

By default it uses in-memory runtime state to avoid writing local eval traffic into the configured database. Set `AGENT_RUNTIME_REAL_EVAL_USE_DATABASE=1` only when intentionally testing persistence.

## Production Stops

Stop and ask for separate confirmation before:

- running migrations against a real production database
- changing Meta/Dualhook/WhatsApp production config
- enabling external trace export containing lead text
