-- Additive production migration for taliya-commercial-ops.v1.
-- Server-side Postgres/service-role access remains available. Browser roles
-- have no direct access to operational lead, message, runtime or funnel data.

ALTER TABLE public.agent_runtime_conversations
  ADD COLUMN IF NOT EXISTS channel_conversation_id text,
  ADD COLUMN IF NOT EXISTS entry_intent text;

ALTER TABLE public.agent_runtime_model_usage
  ADD COLUMN IF NOT EXISTS model_operations integer NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS cached_input_tokens integer NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS cache_write_input_tokens integer NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS reasoning_tokens integer NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS repairs integer NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS latency_ms numeric(12, 3),
  ADD COLUMN IF NOT EXISTS provider text,
  ADD COLUMN IF NOT EXISTS status text NOT NULL DEFAULT 'succeeded';

CREATE UNIQUE INDEX IF NOT EXISTS agent_runtime_model_usage_run_idx
  ON public.agent_runtime_model_usage(run_id);

ALTER TABLE public.sales_leads
  ADD COLUMN IF NOT EXISTS contract_version text;

ALTER TABLE public.sales_lead_messages
  ADD COLUMN IF NOT EXISTS conversation_id text,
  ADD COLUMN IF NOT EXISTS channel text,
  ADD COLUMN IF NOT EXISTS direction text,
  ADD COLUMN IF NOT EXISTS message_type text NOT NULL DEFAULT 'text',
  ADD COLUMN IF NOT EXISTS delivery_status text,
  ADD COLUMN IF NOT EXISTS run_id text,
  ADD COLUMN IF NOT EXISTS trace_id text,
  ADD COLUMN IF NOT EXISTS safety_flags jsonb NOT NULL DEFAULT '[]'::jsonb,
  ADD COLUMN IF NOT EXISTS is_sensitive boolean NOT NULL DEFAULT false,
  ADD COLUMN IF NOT EXISTS unsupported_media boolean NOT NULL DEFAULT false,
  ADD COLUMN IF NOT EXISTS is_problematic boolean NOT NULL DEFAULT false,
  ADD COLUMN IF NOT EXISTS metadata jsonb NOT NULL DEFAULT '{}'::jsonb;

UPDATE public.sales_lead_messages
SET conversation_id = channel_session_id
WHERE conversation_id IS NULL AND channel_session_id IS NOT NULL;

UPDATE public.sales_lead_messages AS message
SET channel = lead.channel,
    direction = CASE WHEN message.role = 'assistant' THEN 'outbound' ELSE 'inbound' END,
    delivery_status = CASE WHEN message.role = 'assistant' THEN 'unknown' ELSE 'received' END
FROM public.sales_leads AS lead
WHERE lead.lead_id = message.lead_id
  AND (message.channel IS NULL OR message.direction IS NULL OR message.delivery_status IS NULL);

CREATE INDEX IF NOT EXISTS sales_lead_messages_conversation_idx
  ON public.sales_lead_messages(conversation_id, created_at, message_id);
CREATE INDEX IF NOT EXISTS sales_lead_messages_run_idx
  ON public.sales_lead_messages(run_id) WHERE run_id IS NOT NULL;

ALTER TABLE public.ai_funnel_events
  ADD COLUMN IF NOT EXISTS anonymous_session_id text,
  ADD COLUMN IF NOT EXISTS message_id text,
  ADD COLUMN IF NOT EXISTS run_id text,
  ADD COLUMN IF NOT EXISTS trace_id text,
  ADD COLUMN IF NOT EXISTS page_path text,
  ADD COLUMN IF NOT EXISTS source_section text,
  ADD COLUMN IF NOT EXISTS cta_id text,
  ADD COLUMN IF NOT EXISTS referrer text,
  ADD COLUMN IF NOT EXISTS utm_source text,
  ADD COLUMN IF NOT EXISTS utm_medium text,
  ADD COLUMN IF NOT EXISTS utm_campaign text,
  ADD COLUMN IF NOT EXISTS utm_content text,
  ADD COLUMN IF NOT EXISTS utm_term text;

CREATE INDEX IF NOT EXISTS ai_funnel_events_session_time_idx
  ON public.ai_funnel_events(session_id, created_at, event_id);
CREATE INDEX IF NOT EXISTS ai_funnel_events_lead_time_idx
  ON public.ai_funnel_events(lead_id, created_at, event_id)
  WHERE lead_id IS NOT NULL;

ALTER TABLE public.whatsapp_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.whatsapp_provider_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.whatsapp_message_outbox ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.whatsapp_turn_queue ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.whatsapp_turn_locks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sales_leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sales_lead_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.operator_actions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ai_usage_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ai_funnel_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.rate_limit_counters ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_v2_conversation_states ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_v2_traces ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_v2_idempotency ENABLE ROW LEVEL SECURITY;

REVOKE ALL PRIVILEGES ON TABLE
  public.whatsapp_sessions,
  public.whatsapp_provider_messages,
  public.whatsapp_message_outbox,
  public.whatsapp_turn_queue,
  public.whatsapp_turn_locks,
  public.sales_leads,
  public.sales_lead_messages,
  public.operator_actions,
  public.ai_usage_events,
  public.ai_funnel_events,
  public.rate_limit_counters,
  public.agent_v2_conversation_states,
  public.agent_v2_traces,
  public.agent_v2_idempotency
FROM anon, authenticated;

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public
  REVOKE SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER
  ON TABLES FROM anon, authenticated;
