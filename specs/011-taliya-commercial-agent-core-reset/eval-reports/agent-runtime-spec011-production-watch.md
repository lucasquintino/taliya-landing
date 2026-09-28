# agent-runtime-spec011-production-watch

Generated at: 2026-05-31T13:38:17.839Z
Release gate: pass_watch_ready_no_production_activation
Passed: 10/10

## PASS machine-readable production watch plan exists with the expected schema and task

```json
{
  "planJson": "specs\\011-taliya-commercial-agent-core-reset\\production-cutover-watch-plan.json",
  "schema": "011.production_watch.v1",
  "task": "T011-099"
}
```

## PASS rollout is explicitly 100 percent, not canary, while final activation remains blocked until Phase 10 approval

```json
{
  "rollout": {
    "mode": "one_hundred_percent",
    "canaryEnabled": false,
    "trafficScope": "all Taliya-owned commercial leads from widget and Taliya-owned WhatsApp after approval",
    "requiresPhase10ApprovalBeforeActivation": true,
    "finalProductionActivationApproved": false,
    "activationDecisionOwner": "lucas_product_owner_with_codex_support",
    "featureFlag": {
      "env": "TALIYA_SPEC011_COMMERCIAL_CORE_ENABLED",
      "enabledValue": "true",
      "rollbackValue": "false",
      "rollbackExpectedDisposition": "operational fallback or retryable spec011_core_disabled; never old TS v2 or Python runner commercial answering",
      "proofTask": "T011-098",
      "proofReport": "specs/011-taliya-commercial-agent-core-reset/eval-reports/agent-runtime-spec011-rollback.json"
    }
  }
}
```

## PASS rollback switch is explicit and points to the proven Spec 011 operational fallback path

```json
{
  "featureFlag": {
    "env": "TALIYA_SPEC011_COMMERCIAL_CORE_ENABLED",
    "enabledValue": "true",
    "rollbackValue": "false",
    "rollbackExpectedDisposition": "operational fallback or retryable spec011_core_disabled; never old TS v2 or Python runner commercial answering",
    "proofTask": "T011-098",
    "proofReport": "specs/011-taliya-commercial-agent-core-reset/eval-reports/agent-runtime-spec011-rollback.json"
  }
}
```

## PASS first-hours watch window covers widget and Taliya-owned WhatsApp with an immediate first check

```json
{
  "watchWindow": {
    "durationMinutes": 240,
    "firstCheckWithinMinutes": 5,
    "defaultCheckCadenceMinutes": 15,
    "channels": [
      "widget",
      "taliya_whatsapp"
    ],
    "trafficScope": "100_percent_taliya_owned_commercial_leads",
    "evidenceFolder": "specs/011-taliya-commercial-agent-core-reset/eval-reports",
    "manualReviewFolder": "specs/011-taliya-commercial-agent-core-reset/manual-review-samples"
  }
}
```

## PASS all required monitors define source, fields, healthy criteria, abort criteria, owner, cadence, and operator action

```json
{
  "missingMonitorIds": [],
  "monitorProblems": []
}
```

## PASS watch plan names every required runtime, trace, delivery, cost, fallback, and Sales Inbox field

```json
{
  "missingWatchFields": []
}
```

## PASS P0 abort criteria cover internal leaks, product facts, numeric grounding, diagnostics, delivery, handoff, Sales Inbox, and false PASS risk

```json
{
  "missingP0AbortIds": []
}
```

## PASS watch readiness links to passing shadow, rollback, quarantine, and no-drift evidence

```json
{
  "missingEvidenceIds": [],
  "badEvidence": []
}
```

## PASS human-readable watch runbook exists and keeps activation blocked without Phase 10 approval

```json
{
  "planMarkdown": "specs\\011-taliya-commercial-agent-core-reset\\production-cutover-watch-plan.md"
}
```

## PASS production watch work produced no protected /pilates, landing visual, floating-agent, or Sales Inbox UI source diff

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
