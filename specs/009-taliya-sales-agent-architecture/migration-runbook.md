# Migration Runbook: Agent V2

## Apply

1. Apply `scripts/sql/001_ai_attendant_whatsapp_sales_inbox.sql` if the environment is new.
2. Apply `scripts/sql/002_ai_attendant_commercial_stage_waitlist.sql` if it has not been applied.
3. Apply `scripts/sql/003_taliya_agent_v2_architecture.sql`.
4. Leave `AI_ATTENDANT_V2_MODE` unset for the default v2 production path, or set `AI_ATTENDANT_V2_MODE=auto` explicitly.

## Verify

Run these checks in Supabase SQL editor:

```sql
select to_regclass('agent_v2_conversation_states') is not null as has_states;
select to_regclass('agent_v2_traces') is not null as has_traces;
select to_regclass('agent_v2_idempotency') is not null as has_idempotency;
select count(*) from sales_leads;
```

Then run a local or staging widget turn with v2 enabled and confirm `agent_v2_traces` receives rows.

## Rollback

To disable behavior immediately, set:

```txt
AI_ATTENDANT_V2_MODE=legacy
AI_ATTENDANT_V2_KILL_SWITCH=true
```

The tables can remain in place. If a destructive rollback is explicitly approved later:

```sql
drop table if exists agent_v2_model_usage;
drop table if exists agent_v2_tool_actions;
drop table if exists agent_v2_traces;
drop table if exists agent_v2_conversation_states;
drop table if exists agent_v2_product_source_versions;
drop table if exists agent_v2_idempotency;
```

Do not drop `sales_leads`, `sales_lead_messages`, `whatsapp_sessions`, `whatsapp_provider_messages`, `operator_actions` or `ai_usage_events`.
