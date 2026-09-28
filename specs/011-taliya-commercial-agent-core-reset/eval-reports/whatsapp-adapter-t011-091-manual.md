# T011-091 WhatsApp Adapter Manual Validation

Passed: true

Scope: adapter-level proof only. This loaded the real `lib/landing/ai-attendant/runtime-client.ts` through TypeScript transpilation in the Node REPL and inspected the WhatsApp endpoint/body that the Taliya-owned WhatsApp path sends to the runtime. It is not production delivery proof.

```json
{
  "endpoint": "/v1/taliya-commercial/turn",
  "channel": "whatsapp",
  "source": "taliya_whatsapp",
  "conversationId": "wa_conv_5511999990000",
  "channelConversationId": "wa_conv_5511999990000",
  "channelMessageId": "wamid.HBgMNTUxMTk5OTk5MDAwMA",
  "idempotencyKey": "whatsapp:wamid.HBgMNTUxMTk5OTk5MDAwMA",
  "phone": "+5511999990000",
  "metadataProvider": "whatsapp",
  "noClientPendingContext": true,
  "noCommercialRoute": true,
  "noTemplateId": true
}
```

Remaining production proof stays in later Spec 011 tasks: shadow mode, rollback proof, real-model evals, trace/projection export, and first-hours monitoring.
