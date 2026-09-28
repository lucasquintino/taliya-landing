# agent-runtime-spec011-rollback

Generated at: 2026-06-04T14:27:10.247Z
Release gate: pass
Passed: 7/7

## PASS runtime settings expose an explicit Spec 011 commercial core rollback flag

```json
{
  "settingsPath": "services/taliya-agent-runtime/app/settings.py"
}
```

## PASS runtime API returns controlled operational error before running the core when flag is disabled

```json
{
  "mainPath": "services/taliya-agent-runtime/app/main.py",
  "disabledCheckIndex": 10902,
  "runCoreIndex": 11164
}
```

## PASS public runtime client short-circuits to operational fallback before fetch when flag is disabled

```json
{
  "runtimeClientPath": "lib/landing/ai-attendant/runtime-client.ts",
  "clientDisabledCheckIndex": 2701,
  "fetchIndex": 3711
}
```

## PASS rollback path does not import or call the old Python runner

```json
{
  "mainRunnerHits": [],
  "coreRunnerHits": []
}
```

## PASS public widget/WhatsApp paths still cannot reach old TS v2 commercial modules

```json
{
  "forbiddenReachability": [],
  "allowedLegacyOperationalModules": [
    "lib/landing/ai-attendant/agent-v2-idempotency.ts"
  ]
}
```

## PASS rollback behavior is covered by settings, runtime API, widget, and WhatsApp tests

```json
{
  "testSettingsPath": "services/taliya-agent-runtime/tests/test_settings.py",
  "testApiPath": "services/taliya-agent-runtime/tests/test_agent_runs_api.py",
  "widgetAdapterTestPath": "scripts/eval-agent-runtime-spec011-widget-adapter.mjs"
}
```

## PASS rollback implementation produced no protected /pilates, landing visual, floating-agent, or Sales Inbox UI source diff

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
