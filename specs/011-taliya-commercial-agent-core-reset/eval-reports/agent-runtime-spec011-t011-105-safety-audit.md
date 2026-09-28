# agent-runtime-spec011-t011-105-safety-audit

Release gate: pass
Paid OpenAI spend: US$0
Passed: 12/12

## PASS paid batch requires exact CLI approval token and budget before paid work

```json
{
  "approvalIndex": 10353,
  "firstCommandIndex": 10658,
  "firstPaidCommandIndex": 11957,
  "approvalBeforeCommands": true
}
```

## PASS paid batch cannot use environment-only approval and validates before any command starts

```json
{
  "approvalIndex": 10353,
  "firstCommandIndex": 10658,
  "firstPaidCommandIndex": 11957,
  "processEnvHits": 0
}
```

## PASS paid batch refuses continue-on-failure and has explicit stop gates after each paid block

```json
{
  "paidCommandIds": [
    "paid_pain_first",
    "paid_long_conversation",
    "paid_do_not_do_missing"
  ]
}
```

## PASS paid batch has exactly three paid commands with per-scenario caps

```json
{
  "paidCommandCount": 3,
  "requiredScenarioIds": [
    "final-pain-first",
    "step3g-long-conversation",
    "do-not-do-early-phone-capture",
    "do-not-do-date-vip-discount",
    "do-not-do-client-studio-whatsapp-capture",
    "do-not-do-wrong-student-language"
  ]
}
```

## PASS paid batch rejects stale scenario and aggregation reports during the batch

```json
{
  "freshnessCheckCount": 6
}
```

## PASS paid batch rejects source/gate drift before continuing across paid phases

```json
{
  "sourceStabilityCheckCount": 7
}
```

## PASS paid batch can only pass with all commands green, three paid commands, and cost within budget

```json
{
  "passGateExcerptPresent": true
}
```

## PASS closure requires fresh evidence, matching batch/scenario cost, and approved budget/model-call envelope

```json
{
  "closureFreshnessChecks": 3,
  "closureCostChecks": 5
}
```

## PASS closure preserves protected /pilates, floating-agent, and Sales Inbox UI source diff gate

```json
{
  "protectedPathCount": 6
}
```

## PASS golden/do-not-do aggregation reports carry generatedAt timestamps for freshness checks

```json
{
  "generatedAtHits": 1
}
```

## PASS readiness requires known critical validator recovery before paid reruns

```json
{
  "coveredValidatorCodeHits": [
    "pain_first_must_offer_diagnostic",
    "diagnostic_urgency_answer_not_captured",
    "diagnostic_next_question_invalid",
    "diagnostic_next_question_not_missing",
    "diagnostic_final_demo_stage_missing",
    "diagnostic_final_staged_order_invalid",
    "price_question_missing_price_answer",
    "price_question_missing_diagnostic_hook",
    "price_question_missing_diagnostic_offer",
    "demo_direct_question_flags_missing",
    "sales_inbox_diagnostic_status_mismatch"
  ],
  "readinessGatePresent": true
}
```

## PASS readiness proves no-cost approval refusals and the US$0.36 / 19-call paid ceiling

```json
{
  "refusalChecks": [
    "paid_batch_refuses_without_approval",
    "paid_batch_refuses_wrong_budget",
    "paid_batch_refuses_env_only_approval",
    "paid_batch_refuses_continue_on_failure"
  ]
}
```
