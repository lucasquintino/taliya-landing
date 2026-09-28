# agent-runtime-spec011-mocked-conductor

Generated at: 2026-06-04T14:27:21.741Z
Release gate: pass
Passed: 6/6

## Fixture Matrix

- valid_adapter: mocked valid conductor decision renders, persists live state, records model usage, and exposes shadow trace/projection evidence
- repairable_adapter: mocked repairable JSON decision reaches validator, sends precise errors to one repair call, then renders and persists the repaired decision
- repaired_trace_projection: mocked repaired decision builds rendered messages, runtime-state diff, Sales Inbox projection, and mandatory trace with repair metadata
- invalid_provider_output: free-form/non-JSON provider output fails with the conductor error and maps only to approved safe fallback disposition
- blocked_validator: blocked validator result skips repair and maps to handoff disposition without commercial copy
- failed_repair: failed repair maps to handoff disposition without deterministic commercial answer
- t011_105_missing_do_not_do_preflight: the four do-not-do scenarios still missing real-model evidence have local structured-JSON preflight coverage for validators, renderer, model usage, and Sales Inbox projection

## PASS required mocked conductor fixture files exist

```json
{
  "missingFixtureFiles": [],
  "requiredFixtureFiles": [
    "services/taliya-agent-runtime/tests/test_spec011_mocked_conductor_fixtures.py",
    "services/taliya-agent-runtime/tests/test_spec011_conductor_template_plan.py",
    "services/taliya-agent-runtime/tests/test_spec011_repair_loop.py",
    "services/taliya-agent-runtime/tests/test_spec011_safe_fallback.py",
    "services/taliya-agent-runtime/tests/test_spec011_widget_runtime_adapter.py",
    "services/taliya-agent-runtime/tests/test_spec011_shadow_mode.py"
  ]
}
```

## PASS mocked conductor fixture matrix passes

```json
{
  "passedCount": 85,
  "command": {
    "id": "mocked_conductor_fixture_pytest",
    "ok": true,
    "command": "python -m pytest tests\\test_spec011_mocked_conductor_fixtures.py tests\\test_spec011_conductor_template_plan.py tests\\test_spec011_repair_loop.py tests\\test_spec011_safe_fallback.py -q",
    "cwd": "services\\taliya-agent-runtime",
    "output": "........................................................................ [ 84%]\r\n.............                                                            [100%]\r\n85 passed in 3.19s"
  },
  "fixtureMatrix": [
    {
      "id": "valid_adapter",
      "proof": "mocked valid conductor decision renders, persists live state, records model usage, and exposes shadow trace/projection evidence"
    },
    {
      "id": "repairable_adapter",
      "proof": "mocked repairable JSON decision reaches validator, sends precise errors to one repair call, then renders and persists the repaired decision"
    },
    {
      "id": "repaired_trace_projection",
      "proof": "mocked repaired decision builds rendered messages, runtime-state diff, Sales Inbox projection, and mandatory trace with repair metadata"
    },
    {
      "id": "invalid_provider_output",
      "proof": "free-form/non-JSON provider output fails with the conductor error and maps only to approved safe fallback disposition"
    },
    {
      "id": "blocked_validator",
      "proof": "blocked validator result skips repair and maps to handoff disposition without commercial copy"
    },
    {
      "id": "failed_repair",
      "proof": "failed repair maps to handoff disposition without deterministic commercial answer"
    },
    {
      "id": "t011_105_missing_do_not_do_preflight",
      "proof": "the four do-not-do scenarios still missing real-model evidence have local structured-JSON preflight coverage for validators, renderer, model usage, and Sales Inbox projection"
    }
  ]
}
```

## PASS adapter and shadow mocked fixture boundaries pass

```json
{
  "passedCount": 24,
  "command": {
    "id": "adapter_shadow_fixture_pytest",
    "ok": true,
    "command": "python -m pytest tests\\test_spec011_widget_runtime_adapter.py tests\\test_spec011_shadow_mode.py -q",
    "cwd": "services\\taliya-agent-runtime",
    "output": "........................                                                 [100%]\r\n24 passed in 2.13s"
  }
}
```

## PASS mocked conductor fixture code passes ruff

```json
{
  "command": {
    "id": "mocked_conductor_ruff",
    "ok": true,
    "command": "python -m ruff check app/core/taliya_commercial/conductor.py tests/test_spec011_mocked_conductor_fixtures.py tests/test_spec011_conductor_template_plan.py",
    "cwd": "services\\taliya-agent-runtime",
    "output": "All checks passed!"
  }
}
```

## PASS LLM-first static, runner quarantine, and public fallback guards pass

```json
{
  "commands": [
    {
      "id": "static_audit",
      "ok": true,
      "command": "node scripts\\eval-agent-runtime-spec011-static-audit.mjs",
      "cwd": ".",
      "output": "agent-runtime-spec011-static-audit: 8/8 passed. Report: C:\\Users\\lucas\\agentes-landing-system\\specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-static-audit.json"
    },
    {
      "id": "runner_quarantine",
      "ok": true,
      "command": "node scripts\\eval-agent-runtime-spec011-runner-quarantine.mjs",
      "cwd": ".",
      "output": "agent-runtime-spec011-runner-quarantine: 5/5 passed. Report: C:\\Users\\lucas\\agentes-landing-system\\specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-runner-quarantine.json"
    },
    {
      "id": "public_fallback_quarantine",
      "ok": true,
      "command": "node scripts\\eval-agent-runtime-spec011-public-fallback-quarantine.mjs",
      "cwd": ".",
      "output": "agent-runtime-spec011-public-fallback-quarantine: 4/4 passed. Report: C:\\Users\\lucas\\agentes-landing-system\\specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-public-fallback-quarantine.json"
    }
  ]
}
```

## PASS mocked conductor gate produced no protected /pilates, landing visual, floating-agent, or Sales Inbox UI source diff

```json
{
  "protectedDiff": {
    "id": "protected_source_diff",
    "ok": true,
    "command": "git -c safe.directory=C:/Users/lucas/agentes-landing-system diff --name-only -- app/pilates components/landing data/landing lib/landing/floating-agent.ts components/internal/SalesInboxClient.tsx",
    "cwd": ".",
    "output": "",
    "files": []
  },
  "protectedPaths": [
    "app/pilates",
    "components/landing",
    "data/landing",
    "lib/landing/floating-agent.ts",
    "components/internal/SalesInboxClient.tsx"
  ]
}
```
