# Persistence Readiness: Floating AI Attendant

## Purpose

Define what must be persisted before the floating sales attendant, WhatsApp channel and Sales Inbox can be treated as production-ready.

This document intentionally does not define environment variables or provider credentials. Runtime env setup remains a later step.

## Current Implementation State

The current implementation is acceptable for local development and QA, but not for production traffic.

Current volatile stores:

- `lib/landing/ai-attendant/session-store.ts`
  - stores WhatsApp sessions in a process-local `Map`;
  - stores processed provider message IDs in memory;
  - stores opt-out state in memory;
  - stores recent WhatsApp message context in memory.
- `lib/landing/ai-attendant/sales-inbox-store.ts`
  - stores Sales Inbox leads in a process-local `Map`;
  - stores operator audit actions in a process-local array;
  - stores AI pause/takeover state in memory;
  - stores external automation sync status in memory.
- `lib/landing/ai-attendant/usage.ts`
  - stores rate-limit counters in process-local maps;
  - stores usage events in a process-local array.
- `components/landing/shared/FloatingAiAttendant.tsx`
  - stores web-widget continuity in browser `sessionStorage`;
  - this is fine for web UX continuity, but it is not an authoritative backend store.

These stores are reset on deploy, restart, serverless cold start or multi-instance routing. They also cannot guarantee WhatsApp idempotency across instances.

## Production Decision

Use Postgres as the primary production persistence layer for Spec 2.

Postgres owns:

- commercial sales leads;
- Sales Inbox state;
- operator actions and audit events;
- WhatsApp sessions;
- WhatsApp provider message idempotency;
- opt-out state;
- recent safe message history;
- lead merge decisions;
- Sales Inbox/n8n optional automation sync status;
- AI usage events needed for cost/debugging.

Redis/KV is optional for high-frequency short-lived counters:

- per-session rate limiting;
- daily request counters;
- short TTL locks for webhook processing.

If Redis/KV is not available at first launch, Postgres can also own rate-limit counters with TTL/cleanup jobs. The implementation must not rely on process memory for production limits.

## Source Of Truth Split

Postgres:

- real-time operational truth for the Sales Inbox;
- WhatsApp session truth;
- idempotency truth;
- opt-out truth;
- operator audit truth;
- usage/debug truth.

Optional n8n automation:

- v1 commercial reporting/pipeline mirror;
- human-friendly views and lightweight CRM;
- not the real-time reply surface;
- not the source of truth for AI pause, idempotency or operator actions.

Browser `sessionStorage`:

- convenience only for reopening the web chat in the same browser session;
- not trusted for lead identity, checkout state, paid state or WhatsApp state.

## Required Tables

### `ai_attendant_web_sessions`

Purpose: optional server-side record for meaningful web-widget sessions after a conversion signal or contact appears.

Minimum columns:

- `session_id` primary key;
- `niche`;
- `entry_path`;
- `source_page`;
- `campaign_stage`;
- `public_offer_mode`;
- `selected_pain_ids` JSON;
- `recommended_agent_ids` JSON;
- `qualification` JSON;
- `last_conversion_path`;
- `created_at`;
- `updated_at`.

Retention:

- keep lightweight web sessions for 30-90 days unless they become leads;
- delete or anonymize sessions with no lead/contact after retention.

### `whatsapp_sessions`

Purpose: persisted channel state for inbound WhatsApp conversations.

Minimum columns:

- `channel_session_id` primary key;
- `provider`;
- `provider_contact_id` unique;
- `phone_normalized`;
- `status`: `active`, `handoffReady`, `optedOut`, `providerFailed`, `closed`;
- `selected_pain_ids` JSON;
- `recommended_agent_ids` JSON;
- `qualification` JSON;
- `opted_in_at`;
- `opted_out_at`;
- `last_reply_at`;
- `last_event_at`;
- `created_at`;
- `updated_at`.

Required indexes:

- unique `provider_contact_id`;
- index `phone_normalized`;
- index `status`;
- index `updated_at`.

### `whatsapp_provider_messages`

Purpose: exact idempotency for Meta webhook retries.

Minimum columns:

- `provider_message_id` primary key;
- `channel_session_id`;
- `provider_contact_id`;
- `direction`: `inbound` or `outbound`;
- `status`: `received`, `processed`, `replied`, `duplicate`, `failed`;
- `safe_text_preview`;
- `error_code`;
- `created_at`;
- `processed_at`.

Required behavior:

- insert inbound provider message ID before running the AI;
- duplicate insert must skip AI/provider reply;
- outbound send attempts must be linked when available.

### `sales_leads`

Purpose: Sales Inbox real-time lead source.

Minimum columns:

- `lead_id` primary key;
- `primary_session_id`;
- `channel`;
- `entry_path`;
- `source_page`;
- `status`;
- `priority`;
- `urgency`;
- `readiness`;
- `conversion_path`;
- `selected_plan_id`;
- `recommended_plan_id`;
- `selected_pain_ids` JSON;
- `recommended_agent_ids` JSON;
- `qualification` JSON;
- `contact` JSON;
- `safe_summary`;
- `next_action`;
- `consent_context` JSON;
- `merge_context` JSON;
- `ai_paused`;
- `follow_up_at`;
- `last_operator_action_at`;
- `external_sync_status`;
- `created_at`;
- `updated_at`.

Required indexes:

- index `status`;
- index `priority`;
- index `conversion_path`;
- index `selected_plan_id`;
- index `updated_at`;
- index normalized WhatsApp/email extracted from `contact` or stored as dedicated columns.

### `sales_lead_messages`

Purpose: recent operational message history for the Sales Inbox.

Minimum columns:

- `message_id` primary key;
- `lead_id`;
- `channel_session_id`;
- `provider_message_id`;
- `role`: `user`, `assistant`, `operator`, `system`;
- `safe_content`;
- `created_at`.

Rules:

- store only operationally useful messages;
- do not store payment credentials;
- redact sensitive student/private details when detected;
- keep raw full transcript out of optional external automations by default.

### `operator_actions`

Purpose: immutable action log for Sales Inbox controls.

Minimum columns:

- `action_id` primary key;
- `lead_id`;
- `actor_user_id`;
- `action`;
- `payload` JSON;
- `before_status`;
- `after_status`;
- `created_at`.

Required behavior:

- every takeover, reply, checkout link, plan link, status change, summary edit and do-not-contact action must create one record;
- payload must be sanitized before persistence.

### `lead_merge_decisions`

Purpose: record how widget and WhatsApp sessions were merged or kept separate.

Minimum columns:

- `decision_id` primary key;
- `lead_id`;
- `candidate_lead_ids` JSON;
- `candidate_session_ids` JSON;
- `decision`: `merge`, `keep_separate`, `needs_operator_review`;
- `strong_signals` JSON;
- `weak_signals` JSON;
- `reason`;
- `actor`;
- `created_at`.

Rules:

- auto-merge only by strong identifiers: WhatsApp, email, explicit `leadId` or explicit `sessionId`;
- weak identifiers alone never auto-merge.

### `ai_usage_events`

Purpose: cost, latency, fallback and debugging telemetry.

Minimum columns:

- `usage_id` primary key;
- `session_id`;
- `lead_id`;
- `channel`;
- `niche`;
- `provider`;
- `model`;
- `status`;
- `latency_ms`;
- `input_token_count`;
- `output_token_count`;
- `estimated_cost`;
- `fallback_or_guardrail_category`;
- `idempotency_key`;
- `created_at`.

Rules:

- do not store raw prompts or full raw transcripts by default;
- store enough metadata to debug failures and estimate cost.

### `rate_limit_counters`

Purpose: production-safe request caps when Redis/KV is not used.

Minimum columns:

- `counter_key` primary key;
- `scope`: `session`, `whatsapp_contact`, `niche_daily`;
- `count`;
- `window_start`;
- `expires_at`;
- `updated_at`.

Rules:

- counters must work across instances;
- cleanup expired counters.

## Repository/Adapter Boundary

Before production, replace direct process-local maps with storage adapters:

- `WhatsAppSessionStore`
  - `getOrCreate`
  - `registerProviderMessage`
  - `appendMessages`
  - `updateState`
  - `markOptOut`
- `SalesLeadStore`
  - `upsertLead`
  - `listLeads`
  - `getLead`
  - `appendMessage`
  - `updateSyncStatus`
  - `findByWhatsApp`
- `OperatorActionStore`
  - `applyAction`
  - `listActions`
- `UsageStore`
  - `checkRateLimit`
  - `logUsageEvent`

The current in-memory implementations can remain as `dev` adapters. Production must use persistent adapters.

## Production Blockers

Do not claim production-ready WhatsApp, Sales Inbox or same-number human takeover until:

- WhatsApp sessions are persisted outside memory;
- provider message idempotency uses a durable unique key;
- opt-out survives restarts/deploys;
- Sales Inbox leads survive restarts/deploys;
- operator actions are durably audited;
- `human_active` / `aiPaused` survives restarts and is checked before AI replies;
- Sales Inbox/n8n optional automation sync status survives restarts and can be retried;
- rate limits and daily caps work across server instances;
- usage events are persisted or shipped to a durable log/analytics sink;
- backup/export strategy exists for Sales Inbox leads and audit events.

## Recommended Implementation Order

1. Add storage interfaces and keep current memory stores as `dev` implementations.
2. Add Postgres schema/migrations for the required tables.
3. Implement Postgres adapters for Sales Inbox leads, operator actions and lead messages.
4. Implement Postgres adapters for WhatsApp sessions and provider message idempotency.
5. Move opt-out and `aiPaused` checks to persistent reads.
6. Persist usage events and replace process-local rate-limit counters with Redis/KV or Postgres counters.
7. Add integration tests for restart-safe idempotency, opt-out, takeover pause and lead list/detail.
8. Keep Sales Inbox/n8n optional automation as a mirror fed from persisted Sales Inbox state.

## Acceptance Criteria

- Restarting the app does not lose leads, WhatsApp sessions, opt-out state, audit events or AI pause state.
- Replaying the same WhatsApp provider message ID after restart does not send another AI reply.
- A human takeover remains active after restart and blocks AI WhatsApp replies.
- Sales Inbox still lists prior leads after restart.
- Operator actions remain visible in audit after restart.
- n8n failure can be retried because the lead sync state is durable.
- Rate limits apply across multiple app instances.
- No full raw transcript, payment credential or unnecessary sensitive data is persisted by default.
