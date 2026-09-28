# agent-runtime-spec011-runner-quarantine

Generated at: 2026-06-04T14:27:21.496Z
Release gate: pass
Passed: 5/5

## PASS runtime API shell does not import or call runtime/runner.py

```json
{
  "mainRunnerImportHits": []
}
```

## PASS Spec 011 core package does not import or call runtime/runner.py

```json
{
  "coreRunnerImportHits": []
}
```

## PASS legacy /v1/agent-runs rejects Taliya commercial turns instead of calling the old runner

```json
{
  "legacyEndpointQuarantineHits": [
    {
      "path": "services/taliya-agent-runtime/app/main.py",
      "line": 231,
      "text": "\"legacy_commercial_runner_quarantined\","
    },
    {
      "path": "services/taliya-agent-runtime/app/main.py",
      "line": 232,
      "text": "\"Taliya commercial turns must use /v1/taliya-commercial/turn.\","
    }
  ]
}
```

## PASS legacy /v1/agent-runs keeps only zero-token runtime_control handoff operations

```json
{
  "operationalControlHits": [
    {
      "path": "services/taliya-agent-runtime/app/main.py",
      "line": 43,
      "text": "def _runtime_control(payload: AgentRunRequest) -> dict[str, Any] | None:"
    },
    {
      "path": "services/taliya-agent-runtime/app/main.py",
      "line": 44,
      "text": "control = payload.metadata.get(\"runtime_control\")"
    },
    {
      "path": "services/taliya-agent-runtime/app/main.py",
      "line": 65,
      "text": "async def _apply_taliya_runtime_control("
    },
    {
      "path": "services/taliya-agent-runtime/app/main.py",
      "line": 101,
      "text": "safety_flags=[f\"runtime_control:{action}\"],"
    },
    {
      "path": "services/taliya-agent-runtime/app/main.py",
      "line": 151,
      "text": "\"source\": \"runtime_control\","
    },
    {
      "path": "services/taliya-agent-runtime/app/main.py",
      "line": 228,
      "text": "control = _runtime_control(payload)"
    },
    {
      "path": "services/taliya-agent-runtime/app/main.py",
      "line": 235,
      "text": "result = await _apply_taliya_runtime_control(payload, control)"
    },
    {
      "path": "services/taliya-agent-runtime/app/main.py",
      "line": 48,
      "text": "if action not in {\"pause_human\", \"resume_human\"}:"
    },
    {
      "path": "services/taliya-agent-runtime/app/main.py",
      "line": 74,
      "text": "paused = action == \"pause_human\""
    },
    {
      "path": "services/taliya-agent-runtime/app/main.py",
      "line": 48,
      "text": "if action not in {\"pause_human\", \"resume_human\"}:"
    },
    {
      "path": "services/taliya-agent-runtime/app/main.py",
      "line": 102,
      "text": "usage=Usage(model=None, input_tokens=0, output_tokens=0, cost_usd=0),"
    }
  ]
}
```

## PASS public commercial runtime client does not post turns to /v1/agent-runs

```json
{
  "runtimeClientLegacyTurnHits": []
}
```
