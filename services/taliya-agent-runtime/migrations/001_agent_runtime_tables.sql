-- Generic runtime tables for Taliya agent families.
-- Do not apply to production without explicit user confirmation.

create table if not exists agent_runtime_agents (
  agent_key text primary key,
  agent_family text not null,
  owner_scope text not null,
  tenant_id text,
  enabled boolean not null default false,
  description text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists agent_runtime_conversations (
  id text primary key,
  agent_key text not null references agent_runtime_agents(agent_key),
  agent_family text not null,
  owner_scope text not null,
  lead_id text,
  tenant_id text,
  channel text not null,
  source text,
  current_agent_name text,
  human_status text not null default 'none',
  compact_summary text,
  product_source_version text,
  cost_usd numeric(12, 6) not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists agent_runtime_messages (
  id bigserial primary key,
  conversation_id text not null references agent_runtime_conversations(id),
  run_id text,
  role text not null,
  channel text not null,
  channel_message_id text,
  idempotency_key text,
  text text,
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

drop index if exists agent_runtime_messages_idempotency_idx;

create unique index if not exists agent_runtime_messages_idempotency_idx
  on agent_runtime_messages(idempotency_key);

create table if not exists agent_runtime_runs (
  id text primary key,
  conversation_id text not null references agent_runtime_conversations(id),
  agent_key text not null,
  agent_family text not null,
  owner_scope text not null,
  tenant_id text,
  current_agent_name text,
  status text not null,
  trace_id text not null,
  input jsonb not null default '{}'::jsonb,
  output jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists agent_runtime_state (
  conversation_id text primary key references agent_runtime_conversations(id),
  agent_key text not null,
  agent_family text not null,
  owner_scope text not null,
  tenant_id text,
  current_agent_name text not null,
  input_items jsonb not null default '[]'::jsonb,
  lead_facts jsonb not null default '[]'::jsonb,
  diagnostic jsonb,
  waitlist jsonb,
  human_status text not null default 'none',
  compact_summary text,
  runtime_meta jsonb not null default '{}'::jsonb,
  product_source_version text,
  cost_usd numeric(12, 6) not null default 0,
  updated_at timestamptz not null default now()
);

create table if not exists agent_runtime_tool_calls (
  id bigserial primary key,
  conversation_id text not null,
  run_id text,
  agent_key text not null,
  agent_family text not null,
  owner_scope text not null,
  tenant_id text,
  tool_name text not null,
  idempotency_key text not null,
  input jsonb not null default '{}'::jsonb,
  output jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  unique (idempotency_key)
);

create table if not exists agent_runtime_handoffs (
  id bigserial primary key,
  conversation_id text not null,
  run_id text,
  agent_key text not null,
  agent_family text not null,
  owner_scope text not null,
  tenant_id text,
  source_agent text,
  target_agent text,
  handoff_type text not null,
  reason text,
  status text not null,
  created_at timestamptz not null default now()
);

create table if not exists agent_runtime_guardrail_events (
  id bigserial primary key,
  conversation_id text not null,
  run_id text,
  agent_key text not null,
  agent_family text not null,
  owner_scope text not null,
  tenant_id text,
  name text not null,
  phase text not null,
  status text not null,
  reason text,
  blocked boolean not null default false,
  repaired boolean not null default false,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists agent_runtime_model_usage (
  id bigserial primary key,
  conversation_id text not null,
  run_id text not null,
  agent_key text not null,
  agent_family text not null,
  owner_scope text not null,
  tenant_id text,
  model text,
  input_tokens integer not null default 0,
  output_tokens integer not null default 0,
  cost_usd numeric(12, 6) not null default 0,
  created_at timestamptz not null default now()
);

create table if not exists agent_runtime_product_sources (
  source_key text primary key,
  scope text not null,
  version text not null,
  payload jsonb not null,
  last_reviewed_at timestamptz not null,
  created_at timestamptz not null default now()
);

create table if not exists agent_runtime_idempotency (
  request_id text primary key,
  response jsonb,
  status text not null default 'completed',
  created_at timestamptz not null default now(),
  expires_at timestamptz
);
