# agent-runtime-spec011-static-audit

Generated at: 2026-06-04T14:27:21.375Z
Release gate: pass
Passed: 8/8

## PASS active runtime API and Spec 011 core do not import/call runtime/runner.py for commercial answering

```json
{
  "activeRunnerHits": []
}
```

## PASS public widget/WhatsApp entrypoints use Spec 011 endpoint and cannot reach old TS v2 commercial fallback

```json
{
  "forbiddenReachability": [],
  "endpointOk": true,
  "runtimeClientLegacyHintHits": [],
  "requestBodyLegacyHints": [],
  "allowedLegacyOperationalModules": [
    "lib/landing/ai-attendant/agent-v2-idempotency.ts"
  ]
}
```

## PASS runtime adapter keeps commercial understanding inside conduct_turn before validation/render/state updates

```json
{
  "conductIndex": 4036,
  "validateIndex": 5222,
  "renderIndex": 6702,
  "stateDiffIndex": 6855,
  "runtimeAdapterCommercialBranchHits": [],
  "runtimeAdapterMessageTextHits": []
}
```

## PASS public conversion path is derived from runtime structured output, not user-text regex routing

```json
{
  "conversionPathTextParsingHits": []
}
```

## PASS active production-path prompts/templates/fallbacks do not hardcode product facts outside official product knowledge or Spec 006

```json
{
  "activeProductFactHits": [],
  "legacyReferenceProductFactHits": [
    {
      "path": "services/taliya-agent-runtime/app/runtime/runner.py",
      "line": 3071,
      "text": "\"Hoje os planos sao Base R$ 197/mes, Essencial R$ 497/mes, Avance R$ 897/mes e Completo R$ 1.497/mes.\",",
      "classification": "legacy_reference_not_active_path"
    },
    {
      "path": "services/taliya-agent-runtime/app/runtime/runner.py",
      "line": 3202,
      "text": "\"O Completo fica em R$ 1.497/mes.\",",
      "classification": "legacy_reference_not_active_path"
    },
    {
      "path": "services/taliya-agent-runtime/app/runtime/runner.py",
      "line": 3249,
      "text": "\"Claro. Hoje os planos da Taliya para studios de Pilates comecam em R$ 197/mes no Base, \"",
      "classification": "legacy_reference_not_active_path"
    },
    {
      "path": "services/taliya-agent-runtime/app/runtime/runner.py",
      "line": 3250,
      "text": "\"R$ 497/mes no Essencial, R$ 897/mes no Avance e R$ 1.497/mes no Completo. \"",
      "classification": "legacy_reference_not_active_path"
    },
    {
      "path": "services/taliya-agent-runtime/app/runtime/runner.py",
      "line": 3259,
      "text": "\"Os planos oficiais sao Base, Essencial, Avance e Completo. Posso te explicar a diferenca por faixa e, se voce me disser a rotina que mais pesa hoje, eu comparo sem inventar link de pagamento.\"",
      "classification": "legacy_reference_not_active_path"
    },
    {
      "path": "services/taliya-agent-runtime/app/runtime/runner.py",
      "line": 3888,
      "text": "if entry_intent == \"waitlist_intent\" and normalized.startswith(\"quero assinar o plano \") and \"checkout seguro\" in normalized:",
      "classification": "legacy_reference_not_active_path"
    },
    {
      "path": "services/taliya-agent-runtime/app/domains/taliya_commercial/templates.py",
      "line": 112,
      "text": "body=(\"Hoje os planos são Base R$ 197/mês, Essencial R$ 497/mês, Avance R$ 897/mês e Completo R$ 1.497/mês.\",),",
      "classification": "legacy_reference_not_active_path"
    },
    {
      "path": "services/taliya-agent-runtime/app/domains/taliya_commercial/templates.py",
      "line": 119,
      "text": "body=(\"O Completo fica em R$ 1.497/mês.\",),",
      "classification": "legacy_reference_not_active_path"
    },
    {
      "path": "services/taliya-agent-runtime/app/domains/taliya_commercial/behavior_policy.py",
      "line": 94,
      "text": "7a. When the lead asks price, list the official plan names and prices: Base R$ 197/mes, Essencial R$ 497/mes, Avance R$ 897/mes, and Completo R$ 1.497/mes. Do not answer only a range or one plan price unless the lead asked about that specif",
      "classification": "legacy_reference_not_active_path"
    },
    {
      "path": "lib/landing/ai-attendant/agent-v2-response-generator.ts",
      "line": 415,
      "text": "messages.push(\"Hoje a Taliya tem quatro faixas de plano, começando em R$ 197/mês.\");",
      "classification": "legacy_reference_not_active_path"
    }
  ]
}
```

## PASS generic whole-response fields are blocked by guards and absent from active renderer/template/runtime output surfaces

```json
{
  "genericWholeResponseActiveHits": [],
  "genericWholeResponseGuardHits": [
    {
      "path": "services/taliya-agent-runtime/app/core/taliya_commercial/schemas.py",
      "line": 324,
      "text": "\"message_text\","
    },
    {
      "path": "services/taliya-agent-runtime/app/core/taliya_commercial/schemas.py",
      "line": 325,
      "text": "\"freeform_response\","
    },
    {
      "path": "services/taliya-agent-runtime/app/core/taliya_commercial/schemas.py",
      "line": 326,
      "text": "\"assistant_reply\","
    },
    {
      "path": "services/taliya-agent-runtime/app/core/taliya_commercial/failed_path_guards.py",
      "line": 38,
      "text": "\"assistant_reply\","
    },
    {
      "path": "services/taliya-agent-runtime/app/core/taliya_commercial/failed_path_guards.py",
      "line": 39,
      "text": "\"freeform_response\","
    },
    {
      "path": "services/taliya-agent-runtime/app/core/taliya_commercial/failed_path_guards.py",
      "line": 41,
      "text": "\"message_text\","
    }
  ]
}
```

## PASS active renderer/template registry do not invent semantic defaults for missing commercial variables

```json
{
  "rendererDefaultHits": []
}
```

## PASS static audit work produced no protected /pilates, landing visual, floating-agent, or Sales Inbox UI source diff

```json
{
  "protectedDiff": [],
  "protectedPaths": [
    "app/pilates",
    "components/landing",
    "data/landing",
    "lib/landing/floating-agent.ts",
    "components/internal/SalesInboxClient.tsx"
  ]
}
```
