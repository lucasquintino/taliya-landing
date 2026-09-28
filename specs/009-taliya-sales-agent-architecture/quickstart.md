# Quickstart: Taliya Sales Agent Architecture

## 1. Read Required Context

Before implementation, read:

- `AGENTS.md`
- `node_modules/next/dist/docs/` relevant route/runtime docs before editing Next.js API routes
- `specs/009-taliya-sales-agent-architecture/spec.md`
- `specs/009-taliya-sales-agent-architecture/conversation-policy.md`
- `specs/009-taliya-sales-agent-architecture/scenario-matrix.md`
- `specs/002-floating-ai-sales-agent/spec.md`
- `specs/002-floating-ai-sales-agent/tasks.md`
- `specs/001-niche-landing-system/spec.md`
- docs under `docs/landing-agentes-pilates/source/`

## 2. Protected Landing Rule

Do not redesign, reorder, restyle or visually alter `/pilates`. Functional CTA wiring, chat behavior, metadata, accessibility fixes and integration fixes are allowed only when they preserve the approved layout.

Before changes that could affect landing behavior, capture or confirm desktop and mobile `/pilates` baseline.

## 3. Environment

Expected existing env groups:

- OpenAI: `OPENAI_API_KEY`, optional `AI_ATTENDANT_MODEL`
- Database: existing Supabase/Postgres env vars used by the app
- WhatsApp/Dualhook/Meta: existing verify token, access token, phone number id and allowed phone number id/connection env vars
- Safety flags: existing or new kill switch for AI replies, while preserving capture/logging
- Agent v2 switch: v2 automatic replies by default; legacy/capture-only are explicit rollback or debug modes
- Eval budget: max scenarios, max real-model calls and max estimated cost for realistic eval runs

Local mock path:

- `AI_ATTENDANT_PROVIDER=mock` or current mock envs may be used for non-real-model tests.
- Realistic evals should use real model calls when validating quality before production replacement.

## 4. Implementation Order

1. Add official product knowledge source and read tool.
2. Add v2 conversation state/substate types and persistence compatibility.
3. Add channel adapter contracts for widget and WhatsApp.
4. Add normalization and idempotency for inbound events and tool actions.
5. Add semantic interpretation layer.
6. Add orchestrator decision layer.
7. Add internal tools for facts, diagnostic, waitlist, handoff, trace and cost cap.
8. Add response generator constrained by selected action and product source.
9. Add deterministic guardrails.
10. Add channel delivery behavior, including WhatsApp typing/delay/splitting.
11. Update Sales Inbox to display cold/warm/hot/waitlist/handoff/trace/cost fields.
12. Add layer-specific tests.
13. Add integrated realistic evals and reports.

## 5. Local Commands

Use existing project scripts where applicable:

```bash
npm run lint
npm run eval:ai-routes
npm run eval:ai-multiturn
npm run eval:ai-sales-humanization
npm run eval:lead-pipeline
npm run eval:custom-diagnostic
npm run eval:whatsapp-webhook
npm run eval:commercial-conversation-matrix
npm run eval:price-plan-commercial-matrix
npm run eval:message-delivery-matrix
npm run cleanup:ai-test-data
```

New or updated eval scripts should produce:

- full transcripts
- state transitions
- tool/source usage
- guardrail results
- cost estimates
- quality judge scores
- blocking failures

## 6. Manual Test Timing

Widget manual tests can be run locally and after deploy.

Real WhatsApp manual tests happen after deploy because the live webhook, provider metadata, typing indicator and Business App coexistence cannot be fully proven locally.

## 7. Production Gate

The v2 agent is the intended production path. Before or after deploys that touch agent behavior, verify:

- product knowledge tests pass
- state/substate tests pass
- idempotency tests pass
- tool action tests pass
- guardrail tests pass
- channel delivery tests pass
- integrated transcript evals pass
- Sales Inbox visibility checks pass
- product owner reviews representative transcripts and approves

No shadow mode or partial rollout is required.

Before production replacement:

- verify database migration applied successfully;
- document rollback path;
- confirm n8n/Airtable are not source of truth;
- record product-owner approval with eval reports and manual-test reports.
