create index if not exists agent_runtime_conversations_agent_key_idx
  on public.agent_runtime_conversations (agent_key);

create index if not exists agent_runtime_messages_conversation_id_idx
  on public.agent_runtime_messages (conversation_id);

create index if not exists agent_runtime_runs_conversation_id_idx
  on public.agent_runtime_runs (conversation_id);
