# agent-runtime-spec011-legacy-reference-quarantine

Generated at: 2026-05-31T12:14:44.221Z
Release gate: pass
Passed: 5/5

## PASS all tests importing the legacy runner are explicitly marked as legacy_runner_reference

```json
{
  "runnerImportTests": [
    {
      "file": "services/taliya-agent-runtime/tests/test_diagnostic.py",
      "marked": true
    },
    {
      "file": "services/taliya-agent-runtime/tests/test_handoffs.py",
      "marked": true
    },
    {
      "file": "services/taliya-agent-runtime/tests/test_human_handoff.py",
      "marked": true
    },
    {
      "file": "services/taliya-agent-runtime/tests/test_llm_output_repair.py",
      "marked": true
    },
    {
      "file": "services/taliya-agent-runtime/tests/test_model_usage.py",
      "marked": true
    },
    {
      "file": "services/taliya-agent-runtime/tests/test_product_knowledge.py",
      "marked": true
    },
    {
      "file": "services/taliya-agent-runtime/tests/test_runner_events.py",
      "marked": true
    },
    {
      "file": "services/taliya-agent-runtime/tests/test_runtime_behavior_regressions.py",
      "marked": true
    },
    {
      "file": "services/taliya-agent-runtime/tests/test_waitlist_tool.py",
      "marked": true
    },
    {
      "file": "services/taliya-agent-runtime/tests/test_widget_opening_policy.py",
      "marked": true
    }
  ],
  "unmarkedRunnerImportTests": []
}
```

## PASS pytest marker registry documents legacy runner reference tests

```json
{
  "markerPath": "services/taliya-agent-runtime/pyproject.toml"
}
```

## PASS runtime README names Spec 011 as active endpoint and quarantines /v1/agent-runs

```json
{
  "readmePath": "services/taliya-agent-runtime/README.md"
}
```

## PASS real OpenAI production-path eval posts to the Spec 011 endpoint, not /v1/agent-runs

```json
{
  "realOpenAiLegacyEndpointHits": []
}
```

## PASS legacy behavior eval is labeled as reference-only and not production-path evidence

```json
{
  "legacyEvalPath": "scripts/eval-agent-runtime-legacy-behavior.py"
}
```
