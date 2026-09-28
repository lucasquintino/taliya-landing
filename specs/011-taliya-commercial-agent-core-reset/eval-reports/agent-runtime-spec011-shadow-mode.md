# agent-runtime-spec011-shadow-mode

Generated at: 2026-05-31T13:09:20.322Z
Release gate: pass
Passed: 7/7

## PASS runtime response has an explicit delivery_control envelope

```json
{
  "runtimeSchemasPath": "services/taliya-agent-runtime/app/runtime/schemas.py"
}
```

## PASS shadow mode is explicit metadata control, not inferred from commercial text

```json
{
  "runtimeAdapterPath": "services/taliya-agent-runtime/app/core/taliya_commercial/runtime_adapter.py"
}
```

## PASS shadow mode suppresses public delivery while preserving rendered trace material

```json
{
  "runtimeAdapterPath": "services/taliya-agent-runtime/app/core/taliya_commercial/runtime_adapter.py"
}
```

## PASS shadow mode records model usage, trace, runtime diff, and Sales Inbox projection as evidence

```json
{
  "runtimeAdapterPath": "services/taliya-agent-runtime/app/core/taliya_commercial/runtime_adapter.py"
}
```

## PASS shadow persistence does not mutate live runtime state

```json
{
  "runtimeAdapterPath": "services/taliya-agent-runtime/app/core/taliya_commercial/runtime_adapter.py"
}
```

## PASS shadow mode does not call the old Python runner

```json
{
  "runnerHits": []
}
```

## PASS shadow mode has widget, WhatsApp, API envelope, and normal-mode separation tests

```json
{
  "shadowTestPath": "services/taliya-agent-runtime/tests/test_spec011_shadow_mode.py"
}
```
