# Contract: Memory Store

## Purpose

Persist runner-compatible conversation memory and operational projections without depending on the old deterministic v2 state model.

## Target Table Families

Use generic names for any runtime tables created by this feature or later runtime hardening:

- `agent_runtime_conversations`
- `agent_runtime_messages`
- `agent_runtime_runs`
- `agent_runtime_state`
- `agent_runtime_tool_calls`
- `agent_runtime_handoffs`
- `agent_runtime_guardrail_events`
- `agent_runtime_model_usage`
- `agent_runtime_product_sources`
- `agent_runtime_idempotency`

Do not create new primary tables named `agent_v2_*` or `sales_agent_*`.

Immediate behavior-release requirement:

- Sales Inbox lead completeness, transcript durability, diagnostic ledger, waitlist state, handoff state, idempotency, product source versions, and minimum runtime observability must work now.
- Full durable runtime replay/tracing can be completed later as long as the fields needed by the behavior release are not lost.

## Common Columns

Runtime tables should include where applicable:

- `agent_key`
- `agent_family`
- `owner_scope`
- `tenant_id`
- `lead_id`
- `conversation_id`
- `created_at`
- `updated_at`

For this feature:

```text
agent_key = taliya_commercial
agent_family = taliya
owner_scope = taliya
tenant_id = null
```

## Conversation Memory

Persist:

- runner input history or compacted equivalent
- current agent name
- current conversation state
- template ids and render plan summary
- lead facts
- diagnostic state and diagnostic ledger
- demo state and demo engagement evidence
- waitlist state
- human status
- product source version
- compact summary
- cost budget state

Do not persist:

- API keys
- HMAC secrets
- request signatures
- system prompts
- raw provider payload fields that are not required for debugging or audit
- unredacted sensitive media payloads

## Sales Inbox Projection

Sales Inbox should show:

- lead identity and channel
- priority and next action
- current agent
- human status
- diagnostic summary
- CRM base recommendation, final plan line, final demo line, and demo status
- waitlist status
- key facts
- latest messages
- guardrail/cost warnings
- trace summary link or panel

Sales Inbox must not show secrets, system prompts, HMAC signatures, or raw provider payloads.

## Idempotency

Idempotency keys are required for:

- inbound channel events
- runtime runs
- side-effecting tools
- waitlist joins
- handoff status changes
- outbound WhatsApp sends

Duplicate events must return or reference the existing result instead of creating duplicate replies.

## Migration Policy

- Existing lead/message/Sales Inbox data may remain.
- New runtime state should be written to generic runtime tables.
- The old deterministic runtime state must not be the source of truth for new official conversations.
