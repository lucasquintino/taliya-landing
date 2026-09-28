# agent-runtime-spec011-report-contract

Generated at: 2026-06-01T00:16:41.901Z
Release gate: pass
Passed: 7/7

## PASS report belongs to Spec 011

```json
{
  "expected": "011-taliya-commercial-agent-core-reset",
  "actual": "011-taliya-commercial-agent-core-reset"
}
```

## PASS report has explicit release gate

```json
{
  "releaseGate": "pass"
}
```

## PASS report includes scenarios

```json
{
  "scenarioCount": 1
}
```

## PASS scenario product-delta-integration-scope has identity

```json
{
  "id": "product-delta-integration-scope",
  "title": "Integration scope should not overpromise Instagram or current-system setup"
}
```

## PASS scenario product-delta-integration-scope lists checks

```json
{
  "checks": [
    "integration_scope_safe",
    "product_followup_source_keys",
    "no_crm_lay_copy",
    "owner_language_no_technical",
    "llm_usage_required",
    "template_ids_present",
    "whatsapp_max_three_chunks"
  ]
}
```

## PASS scenario product-delta-integration-scope records failures array

```json
{
  "failures": []
}
```

## PASS scenario product-delta-integration-scope turn 1 has mandatory Spec 011 artifacts

```json
{
  "missing": [],
  "artifacts": {
    "trace_id": true,
    "context_snapshot": true,
    "conductor_json": true,
    "decision_json": true,
    "rendered_messages": true,
    "validator_results": true,
    "repair_attempts": true,
    "model_usage": true,
    "runtime_state": true,
    "sales_inbox_projection": true,
    "delivery_events": true,
    "trace_complete": true
  }
}
```
