CREATE TABLE IF NOT EXISTS agent_v2_conversation_states (
  conversation_id text PRIMARY KEY,
  lead_id text,
  channel text NOT NULL,
  macro_state text NOT NULL,
  priority text NOT NULL,
  human_status text NOT NULL,
  payload jsonb NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS agent_v2_conversation_states_lead_idx ON agent_v2_conversation_states(lead_id);
CREATE INDEX IF NOT EXISTS agent_v2_conversation_states_macro_idx ON agent_v2_conversation_states(macro_state);
CREATE INDEX IF NOT EXISTS agent_v2_conversation_states_updated_idx ON agent_v2_conversation_states(updated_at);

CREATE TABLE IF NOT EXISTS agent_v2_traces (
  trace_id text PRIMARY KEY,
  lead_id text,
  conversation_id text NOT NULL,
  turn_id text NOT NULL,
  channel text NOT NULL,
  product_source_version text,
  payload jsonb NOT NULL,
  cost_estimate_usd numeric(10,6) NOT NULL DEFAULT 0,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS agent_v2_traces_lead_idx ON agent_v2_traces(lead_id, created_at DESC);
CREATE INDEX IF NOT EXISTS agent_v2_traces_conversation_idx ON agent_v2_traces(conversation_id, created_at DESC);

CREATE TABLE IF NOT EXISTS agent_v2_tool_actions (
  action_id text PRIMARY KEY,
  idempotency_key text NOT NULL UNIQUE,
  conversation_id text NOT NULL,
  lead_id text,
  tool_name text NOT NULL,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  result jsonb NOT NULL DEFAULT '{}'::jsonb,
  status text NOT NULL,
  failure_reason text,
  retry_count integer NOT NULL DEFAULT 0,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS agent_v2_tool_actions_conversation_idx ON agent_v2_tool_actions(conversation_id, created_at DESC);
CREATE INDEX IF NOT EXISTS agent_v2_tool_actions_lead_idx ON agent_v2_tool_actions(lead_id, created_at DESC);

CREATE TABLE IF NOT EXISTS agent_v2_model_usage (
  usage_id text PRIMARY KEY,
  trace_id text,
  lead_id text,
  conversation_id text NOT NULL,
  operation text NOT NULL,
  model text NOT NULL,
  input_tokens integer,
  output_tokens integer,
  estimated_cost_usd numeric(10,6) NOT NULL DEFAULT 0,
  budget_category text NOT NULL,
  escalation_reason text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS agent_v2_model_usage_lead_idx ON agent_v2_model_usage(lead_id, created_at DESC);
CREATE INDEX IF NOT EXISTS agent_v2_model_usage_trace_idx ON agent_v2_model_usage(trace_id);

CREATE TABLE IF NOT EXISTS agent_v2_product_source_versions (
  version text PRIMARY KEY,
  payload jsonb NOT NULL,
  active boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS agent_v2_idempotency (
  idempotency_key text PRIMARY KEY,
  scope text NOT NULL,
  status text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS agent_v2_idempotency_scope_idx ON agent_v2_idempotency(scope, created_at DESC);

