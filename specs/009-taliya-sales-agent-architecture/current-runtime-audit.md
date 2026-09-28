# Current Runtime Audit

## Existing Agent Entry

- Widget endpoint: `app/api/landing/ai-attendant/route.ts`.
- WhatsApp endpoint: `app/api/landing/ai-attendant/whatsapp/route.ts`.
- Shared runtime entry: `lib/landing/floating-agent.ts`.

## Current Response Path

1. Route validates request payload.
2. `runAiAttendantTurn` builds context, checks rate/kill switch, applies input guardrails.
3. Deterministic commercial rules handle greetings, price/plan, diagnostic and waitlist cases.
4. The provider path calls OpenAI only when deterministic routes do not own the turn.
5. Output guardrails/conversion gates run before returning.

## Persistence

- Sales Inbox source of truth: `sales_leads` plus `sales_lead_messages`.
- WhatsApp sessions/idempotency: `whatsapp_sessions`, `whatsapp_provider_messages`, `whatsapp_message_outbox`.
- Operator actions: `operator_actions`.
- Usage/funnel events: `ai_usage_events`, `ai_funnel_events`.
- Runtime schema bootstrap: `lib/landing/ai-attendant/storage/postgres.ts`.

## Gaps Addressed By Spec 009

- Product facts now get a versioned product knowledge read path.
- Agent v2 state/substate and trace tables are added.
- Cost cap is represented as behavior and trace, not just logging.
- Semantic interpretation and orchestration are explicit modules.
- Widget and WhatsApp still share the same commercial brain, while delivery remains channel-specific.

