# agent-runtime-spec011-public-fallback-quarantine

Generated at: 2026-06-04T14:27:21.615Z
Release gate: pass
Passed: 4/4

## PASS public widget/WhatsApp paths cannot reach old TS v2 commercial fallback modules

```json
{
  "forbiddenReachability": [],
  "allowedLegacyOperationalModules": [
    "lib/landing/ai-attendant/agent-v2-idempotency.ts"
  ]
}
```

## PASS runtime client public turn path has no legacy commercial payload builder or hints

```json
{
  "runtimeLegacyPayloadHits": []
}
```

## PASS runtime client still strips legacy commercial hints from supplied metadata

```json
{
  "runtimeStripHits": [
    {
      "line": 21,
      "text": "template_ids?: string[];"
    },
    {
      "line": 34,
      "text": "template_id?: string | null;"
    },
    {
      "line": 279,
      "text": "delete transport.client_pending_context;"
    },
    {
      "line": 280,
      "text": "delete transport.commercial_route;"
    },
    {
      "line": 281,
      "text": "delete transport.template_id;"
    },
    {
      "line": 294,
      "text": "const stagedDiagnosticDelivery = output.decision?.template_ids?.some((templateId) => templateId.startsWith(\"diagnostic.deliver_\")) ?? false;"
    },
    {
      "line": 406,
      "text": "agentRuntimeTemplateIds: output.decision?.template_ids?.join(\", \") || output.messages?.map((message) => message.template_id).filter(Boolean).join(\", \"),"
    },
    {
      "line": 687,
      "text": "const templateIds = output.decision?.template_ids ?? [];"
    },
    {
      "line": 752,
      "text": "const templateIds = output.decision?.template_ids ?? [];"
    }
  ]
}
```

## PASS runtime client commercial turn endpoint is fixed to the Spec 011 API

```json
{}
```
