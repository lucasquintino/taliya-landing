# Context Builder Manual Validation - T011-040

Date: 2026-05-30

Scope: isolated Spec 011 Context Builder. Product knowledge retrieval, Spec 006 summaries, deeper reliability policy, and context snapshot persistence remain `T011-041` through `T011-045`.

Manual simulation summary:

- Latest inbound message is copied into `TurnContext.inbound`.
- Compact memory includes the persisted summary.
- Diagnostic ledger is copied from runtime state and preserves missing `urgency`.
- Waitlist, demo, and handoff state are copied from runtime state.
- Recent transcript combines persisted state items and message events.
- Channel/source metadata becomes non-renderable context facts.
- Product knowledge remains empty until the retrieval stages.

Observed output:

```text
turn=turn_manual_ctx; channel=whatsapp; inbound_id=wamid_manual
memory=[{'kind': 'summary', 'value': 'Lead quer organizar agenda e reposicoes.'}]
ledger=['active_students_or_size:answered', 'urgency:missing']
waitlist={'status': 'none'}; demo={'status': 'offered'}; handoff={'status': 'none', 'reason': None}
facts=[('source', 'channel_metadata', 'internal', False), ('entry_intent', 'channel_metadata', 'internal', False), ('channel_conversation_id', 'channel_metadata', 'internal', False), ('page_path', 'channel_metadata', 'internal', False), ('utm_source', 'channel_metadata', 'internal', False), ('profile_name', 'channel_metadata', 'channel_provided', False), ('whatsapp_phone', 'channel_metadata', 'channel_provided', False)]
recent_count=4; last=Mensagem anterior
product_knowledge_count=0
```

Manual conclusion:

- The builder assembles typed context without making commercial route, diagnostic, price, plan, demo, or waitlist decisions.
- It does not branch on message content; two different commercial messages keep the same memory/state context except for the inbound text itself.
- Internal/source metadata is available to the future LLM conductor as context, but is not customer-renderable.
- This is not a production cutover and does not yet validate product truth retrieval.
