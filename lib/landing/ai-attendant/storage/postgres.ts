import { Pool, type QueryResultRow } from "pg";

let pool: Pool | null = null;
let schemaReady: Promise<void> | null = null;

export function hasPostgresStorage() {
  return Boolean(process.env.DATABASE_URL);
}

export async function postgresQuery<T extends QueryResultRow = QueryResultRow>(text: string, values: unknown[] = []) {
  const client = getPool();
  await ensureAiAttendantSchema();
  return client.query<T>(text, values);
}

export async function ensureAiAttendantSchema() {
  if (!hasPostgresStorage()) return;
  if (!schemaReady) {
    schemaReady = createSchema();
  }
  return schemaReady;
}

function getPool() {
  if (!process.env.DATABASE_URL) {
    throw new Error("DATABASE_URL is not configured.");
  }
  if (!pool) {
    pool = new Pool({
      connectionString: process.env.DATABASE_URL,
      max: Number(process.env.DATABASE_POOL_MAX ?? 5),
      ssl: process.env.DATABASE_SSL === "true" ? { rejectUnauthorized: false } : undefined,
    });
  }
  return pool;
}

async function createSchema() {
  const client = getPool();
  await client.query(`
    CREATE TABLE IF NOT EXISTS whatsapp_sessions (
      channel_session_id text PRIMARY KEY,
      provider text NOT NULL,
      provider_contact_id text NOT NULL UNIQUE,
      phone_normalized text,
      phone_number_id text,
      display_phone_number text,
      status text NOT NULL,
      selected_pain_ids jsonb NOT NULL DEFAULT '[]'::jsonb,
      recommended_agent_ids jsonb NOT NULL DEFAULT '[]'::jsonb,
      qualification jsonb NOT NULL DEFAULT '{}'::jsonb,
      messages jsonb NOT NULL DEFAULT '[]'::jsonb,
      opted_in_at timestamptz,
      opted_out_at timestamptz,
      last_reply_at timestamptz,
      last_event_at timestamptz,
      created_at timestamptz NOT NULL DEFAULT now(),
      updated_at timestamptz NOT NULL DEFAULT now()
    );

    CREATE INDEX IF NOT EXISTS whatsapp_sessions_phone_idx ON whatsapp_sessions(phone_normalized);
    CREATE INDEX IF NOT EXISTS whatsapp_sessions_status_idx ON whatsapp_sessions(status);
    CREATE INDEX IF NOT EXISTS whatsapp_sessions_updated_idx ON whatsapp_sessions(updated_at);

    CREATE TABLE IF NOT EXISTS whatsapp_provider_messages (
      provider_message_id text PRIMARY KEY,
      channel_session_id text NOT NULL,
      provider_contact_id text NOT NULL,
      phone_number_id text,
      direction text NOT NULL,
      status text NOT NULL,
      safe_text_preview text,
      error_code text,
      provider_status text,
      created_at timestamptz NOT NULL DEFAULT now(),
      processed_at timestamptz
    );

    CREATE INDEX IF NOT EXISTS whatsapp_provider_messages_session_idx ON whatsapp_provider_messages(channel_session_id);
    CREATE INDEX IF NOT EXISTS whatsapp_provider_messages_contact_idx ON whatsapp_provider_messages(provider_contact_id);

    CREATE TABLE IF NOT EXISTS whatsapp_message_outbox (
      outbox_id text PRIMARY KEY,
      lead_id text,
      channel_session_id text,
      provider_contact_id text NOT NULL,
      phone_number_id text,
      to_phone text NOT NULL,
      content text NOT NULL,
      reply_to_provider_message_id text,
      idempotency_key text NOT NULL UNIQUE,
      status text NOT NULL,
      provider_message_id text,
      attempt_count integer NOT NULL DEFAULT 0,
      last_error text,
      next_attempt_at timestamptz,
      created_at timestamptz NOT NULL DEFAULT now(),
      updated_at timestamptz NOT NULL DEFAULT now()
    );

    CREATE INDEX IF NOT EXISTS whatsapp_message_outbox_status_idx ON whatsapp_message_outbox(status, next_attempt_at);
    CREATE INDEX IF NOT EXISTS whatsapp_message_outbox_provider_message_idx ON whatsapp_message_outbox(provider_message_id);

    CREATE TABLE IF NOT EXISTS whatsapp_turn_queue (
      queue_id text PRIMARY KEY,
      channel_session_id text NOT NULL,
      provider_contact_id text NOT NULL,
      provider_message_id text NOT NULL UNIQUE,
      phone_number_id text,
      display_phone_number text,
      from_phone text,
      profile_name text,
      text text NOT NULL,
      occurred_at timestamptz NOT NULL,
      status text NOT NULL DEFAULT 'pending',
      batch_id text,
      last_error text,
      created_at timestamptz NOT NULL DEFAULT now(),
      updated_at timestamptz NOT NULL DEFAULT now()
    );

    CREATE INDEX IF NOT EXISTS whatsapp_turn_queue_session_status_idx ON whatsapp_turn_queue(channel_session_id, status, occurred_at);
    CREATE INDEX IF NOT EXISTS whatsapp_turn_queue_contact_status_idx ON whatsapp_turn_queue(provider_contact_id, status, occurred_at);
    CREATE INDEX IF NOT EXISTS whatsapp_turn_queue_batch_idx ON whatsapp_turn_queue(batch_id);
    ALTER TABLE whatsapp_turn_queue ADD COLUMN IF NOT EXISTS profile_name text;

    CREATE TABLE IF NOT EXISTS whatsapp_turn_locks (
      channel_session_id text PRIMARY KEY,
      owner_id text NOT NULL,
      locked_until timestamptz NOT NULL,
      created_at timestamptz NOT NULL DEFAULT now(),
      updated_at timestamptz NOT NULL DEFAULT now()
    );

    CREATE INDEX IF NOT EXISTS whatsapp_turn_locks_until_idx ON whatsapp_turn_locks(locked_until);

    CREATE TABLE IF NOT EXISTS sales_leads (
      lead_id text PRIMARY KEY,
      data jsonb NOT NULL,
      status text NOT NULL,
      priority text NOT NULL,
      channel text NOT NULL,
      conversion_path text NOT NULL,
      selected_plan_id text,
      contact_normalized_whatsapp text,
      contact_email text,
      ai_paused boolean NOT NULL DEFAULT false,
      external_sync_status text NOT NULL DEFAULT 'pending',
      created_at timestamptz NOT NULL DEFAULT now(),
      updated_at timestamptz NOT NULL DEFAULT now()
    );

    ALTER TABLE sales_leads ADD COLUMN IF NOT EXISTS external_sync_status text NOT NULL DEFAULT 'pending';

    CREATE INDEX IF NOT EXISTS sales_leads_status_idx ON sales_leads(status);
    CREATE INDEX IF NOT EXISTS sales_leads_priority_idx ON sales_leads(priority);
    CREATE INDEX IF NOT EXISTS sales_leads_channel_idx ON sales_leads(channel);
    CREATE INDEX IF NOT EXISTS sales_leads_conversion_path_idx ON sales_leads(conversion_path);
    CREATE INDEX IF NOT EXISTS sales_leads_selected_plan_idx ON sales_leads(selected_plan_id);
    CREATE INDEX IF NOT EXISTS sales_leads_contact_whatsapp_idx ON sales_leads(contact_normalized_whatsapp);
    CREATE INDEX IF NOT EXISTS sales_leads_contact_email_idx ON sales_leads(contact_email);
    CREATE INDEX IF NOT EXISTS sales_leads_commercial_stage_json_idx ON sales_leads((data->>'commercialStage'));
    CREATE INDEX IF NOT EXISTS sales_leads_waitlist_status_json_idx ON sales_leads((data->>'waitlistStatus'));
    CREATE INDEX IF NOT EXISTS sales_leads_demo_status_json_idx ON sales_leads((data->>'demoStatus'));
    CREATE INDEX IF NOT EXISTS sales_leads_updated_idx ON sales_leads(updated_at);

    CREATE TABLE IF NOT EXISTS sales_lead_messages (
      message_id text PRIMARY KEY,
      lead_id text NOT NULL,
      channel_session_id text,
      provider_message_id text,
      role text NOT NULL,
      safe_content text NOT NULL,
      created_at timestamptz NOT NULL DEFAULT now()
    );

    CREATE INDEX IF NOT EXISTS sales_lead_messages_lead_idx ON sales_lead_messages(lead_id, created_at DESC);

    CREATE TABLE IF NOT EXISTS operator_actions (
      action_id text PRIMARY KEY,
      lead_id text NOT NULL,
      actor_user_id text NOT NULL,
      action text NOT NULL,
      payload jsonb NOT NULL DEFAULT '{}'::jsonb,
      before_status text NOT NULL,
      after_status text NOT NULL,
      created_at timestamptz NOT NULL DEFAULT now()
    );

    CREATE INDEX IF NOT EXISTS operator_actions_lead_idx ON operator_actions(lead_id, created_at DESC);

    CREATE TABLE IF NOT EXISTS ai_usage_events (
      usage_id text PRIMARY KEY,
      session_id text NOT NULL,
      lead_id text,
      channel text NOT NULL,
      niche text NOT NULL,
      provider text NOT NULL,
      model text,
      status text NOT NULL,
      latency_ms integer,
      input_token_count integer,
      output_token_count integer,
      fallback_or_guardrail_category text,
      idempotency_key text,
      created_at timestamptz NOT NULL DEFAULT now()
    );

    CREATE INDEX IF NOT EXISTS ai_usage_events_session_idx ON ai_usage_events(session_id, created_at DESC);
    CREATE INDEX IF NOT EXISTS ai_usage_events_idempotency_idx ON ai_usage_events(idempotency_key);

    CREATE TABLE IF NOT EXISTS ai_funnel_events (
      event_id text PRIMARY KEY,
      idempotency_key text NOT NULL UNIQUE,
      session_id text NOT NULL,
      lead_id text,
      channel text NOT NULL,
      event_name text NOT NULL,
      commercial_stage text,
      conversion_path text,
      payload jsonb NOT NULL DEFAULT '{}'::jsonb,
      created_at timestamptz NOT NULL DEFAULT now()
    );

    CREATE INDEX IF NOT EXISTS ai_funnel_events_session_idx ON ai_funnel_events(session_id, created_at DESC);
    CREATE INDEX IF NOT EXISTS ai_funnel_events_lead_idx ON ai_funnel_events(lead_id, created_at DESC);
    CREATE INDEX IF NOT EXISTS ai_funnel_events_name_idx ON ai_funnel_events(event_name, created_at DESC);

    CREATE TABLE IF NOT EXISTS rate_limit_counters (
      counter_key text PRIMARY KEY,
      scope text NOT NULL,
      count integer NOT NULL,
      window_start timestamptz NOT NULL,
      expires_at timestamptz NOT NULL,
      updated_at timestamptz NOT NULL DEFAULT now()
    );

    CREATE INDEX IF NOT EXISTS rate_limit_counters_expires_idx ON rate_limit_counters(expires_at);

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

    CREATE TABLE IF NOT EXISTS agent_v2_idempotency (
      idempotency_key text PRIMARY KEY,
      scope text NOT NULL,
      status text NOT NULL,
      created_at timestamptz NOT NULL DEFAULT now(),
      updated_at timestamptz NOT NULL DEFAULT now()
    );

    CREATE INDEX IF NOT EXISTS agent_v2_idempotency_scope_idx ON agent_v2_idempotency(scope, created_at DESC);
  `);
}
