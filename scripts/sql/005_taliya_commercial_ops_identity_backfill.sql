begin;

do $$
begin
  if exists (
    select 1
    from public.sales_leads
    where data->>'sessionId' is not null
    group by data->>'sessionId'
    having count(*) > 1
  ) then
    raise exception 'Backfill abortado: sessionId duplicado em sales_leads.';
  end if;
end
$$;

update public.agent_runtime_conversations as conversation
set lead_id = lead.lead_id,
    updated_at = now()
from public.sales_leads as lead
where lead.data->>'sessionId' = conversation.id
  and conversation.lead_id is null;

update public.sales_lead_messages as message
set channel_session_id = lead.data->>'sessionId',
    conversation_id = lead.data->>'sessionId'
from public.sales_leads as lead
join public.agent_runtime_conversations as conversation
  on conversation.id = lead.data->>'sessionId'
where message.lead_id = lead.lead_id
  and message.channel_session_id is null
  and message.conversation_id is null;

commit;
