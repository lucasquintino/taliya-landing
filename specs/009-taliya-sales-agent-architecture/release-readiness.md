# Release Readiness - Agent V2

Status: implemented as the default v2 production path.

## What Is Implemented

- Agent v2 loop with layered interpretation, orchestration, tool execution, guardrails, response generation, state persistence and trace recording.
- Shared brain for widget and WhatsApp, with channel-specific delivery.
- Official product knowledge source for plans, prices and links.
- Diagnostic flow with substate, known facts, no repeated questions and concrete output.
- Waitlist flow after validated interest or buying intent.
- Post-waitlist questions without restarting diagnostic/list flow.
- Human handoff pause path and Sales Inbox handoff endpoint.
- Cost tracking, estimated cost per turn and hard-cap fallback.
- Postgres migration/runbook for durable v2 tables.
- Sales Inbox v2 visibility: macro state, priority, trace id, product source version and estimated cost.
- Airtable remains unused as source of truth; external automations are treated as optional dispatch only.

## Validation Summary

- `npm run lint`: pass
- `npm run build`: pass
- `npm run eval:agent-v2:layers`: pass
- `npm run eval:agent-v2:matrix`: 62/62 pass
- `npm run eval:agent-v2:runtime`: 29/29 pass
- Sales Inbox runtime probe: pass, sanitized report in `eval-reports/sales-inbox-runtime.json`
- Legacy 008 regression harnesses were run. Harness-only scripts loaded successfully; target-based legacy matrices still contain expected conflicts with spec 009 behavior, mainly old name-first assumptions, old demo-unavailable copy, and older waitlist/demo branching expectations.

## Production Behavior

Production now runs the v2 agent by default when `AI_ATTENDANT_V2_MODE` is unset. Keep these checks current:

1. Apply/verify `scripts/sql/003_taliya_agent_v2_architecture.sql` in Supabase.
2. Confirm Vercel envs from `docs/landing-agentes-pilates/source/taliya-agent-v2-env.md`.
3. Confirm Dualhook webhook override and Meta verification.
4. Run the WhatsApp post-deploy test plan after each production deploy that changes WhatsApp behavior.

## Rollback

- Immediate behavioral rollback: set `AI_ATTENDANT_V2_MODE=legacy`.
- Emergency stop: set `AI_ATTENDANT_V2_KILL_SWITCH=true`.
- WhatsApp-specific operational stop: use Sales Inbox handoff/takeover or WhatsApp Business App manual reply.
- Database rollback: follow `migration-runbook.md`; do not drop trace/state tables until exports are no longer needed.

## Remaining Real-World Risk

- Real Meta/WhatsApp send, typing and delay require post-deploy validation with the actual token.
- Manual WhatsApp Business App echo behavior can vary by Meta payload; fallback operator pause exists through Sales Inbox.
- The deterministic interpreter handles the mapped scenarios, but real conversations can still be ambiguous; traces and Sales Inbox review are required during the first live days.
- Current cost estimates are conservative approximations; production token usage should be reviewed after the first real leads.
