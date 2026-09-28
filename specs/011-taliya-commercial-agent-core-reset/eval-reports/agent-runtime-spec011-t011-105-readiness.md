# agent-runtime-spec011-t011-105-readiness

Release gate: ready_for_paid_batch
Paid OpenAI spend: US$0
Paid batch cap: US$0.36
Paid batch model-call cap: 19

## Expected Paid Batch

- `python scripts\eval-agent-runtime-spec011.py --fixture scripts\fixtures\agent-runtime\spec-011-golden-transcripts.json --scenario-id final-pain-first --max-scenarios 1 --max-model-calls 1 --max-cost-usd 0.03 --report-name agent-runtime-spec011-golden-pain-first-1`
- `python scripts\eval-agent-runtime-spec011.py --fixture scripts\fixtures\agent-runtime\spec-011-golden-transcripts.json --scenario-id step3g-long-conversation --max-scenarios 1 --max-model-calls 14 --max-cost-usd 0.25 --report-name agent-runtime-spec011-golden-long-conversation-17`
- `python scripts\eval-agent-runtime-spec011.py --fixture scripts\fixtures\agent-runtime\spec-011-do-not-do-runtime.json --scenario-id do-not-do-early-phone-capture --scenario-id do-not-do-date-vip-discount --scenario-id do-not-do-client-studio-whatsapp-capture --scenario-id do-not-do-wrong-student-language --max-scenarios 4 --max-model-calls 4 --max-cost-usd 0.08 --report-name agent-runtime-spec011-do-not-do-missing-1`

## PASS readiness records a source fingerprint for paid evidence freshness

```json
{
  "sourceFingerprint": {
    "algorithm": "sha256",
    "digest": "e458fcec6bb36bed281b3b7437582554e9b02d89d958d3bb4f216f95b4ef6987",
    "fileCount": 50,
    "targets": [
      "services/taliya-agent-runtime/app/core/taliya_commercial",
      "services/taliya-agent-runtime/app/main.py",
      "services/taliya-agent-runtime/app/settings.py",
      "services/taliya-agent-runtime/app/runtime/schemas.py",
      "services/taliya-agent-runtime/app/shared/memory",
      "scripts/eval-agent-runtime-spec011.py",
      "scripts/spec011-t011-105-source-fingerprint.mjs",
      "scripts/eval-agent-runtime-spec011-fixture-inventory.mjs",
      "scripts/eval-agent-runtime-spec011-golden-do-not-do.mjs",
      "scripts/eval-agent-runtime-spec011-known-validator-recovery.mjs",
      "scripts/eval-agent-runtime-spec011-mocked-conductor.mjs",
      "scripts/eval-agent-runtime-spec011-public-fallback-quarantine.mjs",
      "scripts/eval-agent-runtime-spec011-rollback.mjs",
      "scripts/eval-agent-runtime-spec011-runner-quarantine.mjs",
      "scripts/eval-agent-runtime-spec011-static-audit.mjs",
      "scripts/eval-agent-runtime-spec011-t011-105-paid-batch.mjs",
      "scripts/eval-agent-runtime-spec011-t011-105-readiness.mjs",
      "scripts/eval-agent-runtime-spec011-t011-105-safety-audit.mjs",
      "scripts/eval-agent-runtime-spec011-unit-contract.mjs",
      "scripts/eval-agent-runtime-spec011-widget-adapter.mjs",
      "scripts/eval-agent-runtime-spec011-t011-105-closure.mjs",
      "scripts/fixtures/agent-runtime/spec-011-golden-transcripts.json",
      "scripts/fixtures/agent-runtime/spec-011-do-not-do-runtime.json"
    ]
  }
}
```

## PASS all readiness commands completed with expected exit status

```json
{
  "commands": [
    {
      "id": "node_check_golden_do_not_do",
      "ok": true,
      "allowed": true,
      "exitCode": 0,
      "command": "node --check scripts\\eval-agent-runtime-spec011-golden-do-not-do.mjs",
      "output": ""
    },
    {
      "id": "node_check_paid_batch_runner",
      "ok": true,
      "allowed": true,
      "exitCode": 0,
      "command": "node --check scripts\\eval-agent-runtime-spec011-t011-105-paid-batch.mjs",
      "output": ""
    },
    {
      "id": "node_check_t011_105_safety_audit",
      "ok": true,
      "allowed": true,
      "exitCode": 0,
      "command": "node --check scripts\\eval-agent-runtime-spec011-t011-105-safety-audit.mjs",
      "output": ""
    },
    {
      "id": "node_check_known_validator_recovery",
      "ok": true,
      "allowed": true,
      "exitCode": 0,
      "command": "node --check scripts\\eval-agent-runtime-spec011-known-validator-recovery.mjs",
      "output": ""
    },
    {
      "id": "fixture_inventory_gate",
      "ok": true,
      "allowed": true,
      "exitCode": 0,
      "command": "node scripts\\eval-agent-runtime-spec011-fixture-inventory.mjs",
      "output": "agent-runtime-spec011-fixture-inventory: 8/8 passed\nRelease gate: pass\nReport JSON: C:\\Users\\lucas\\agentes-landing-system\\specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-fixture-inventory.json\nReport MD: C:\\Users\\lucas\\agentes-landing-system\\specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-fixture-inventory.md"
    },
    {
      "id": "known_validator_recovery_gate",
      "ok": true,
      "allowed": true,
      "exitCode": 0,
      "command": "node scripts\\eval-agent-runtime-spec011-known-validator-recovery.mjs",
      "output": "agent-runtime-spec011-known-validator-recovery: 9/9 passed\nRelease gate: pass\nReport JSON: C:\\Users\\lucas\\agentes-landing-system\\specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-known-validator-recovery.json\nReport MD: C:\\Users\\lucas\\agentes-landing-system\\specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-known-validator-recovery.md"
    },
    {
      "id": "t011_105_safety_audit",
      "ok": true,
      "allowed": true,
      "exitCode": 0,
      "command": "node scripts\\eval-agent-runtime-spec011-t011-105-safety-audit.mjs",
      "output": "agent-runtime-spec011-t011-105-safety-audit: 12/12 passed\nRelease gate: pass\nReport JSON: C:\\Users\\lucas\\agentes-landing-system\\specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-t011-105-safety-audit.json\nReport MD: C:\\Users\\lucas\\agentes-landing-system\\specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-t011-105-safety-audit.md"
    },
    {
      "id": "unit_contract_gate",
      "ok": true,
      "allowed": true,
      "exitCode": 0,
      "command": "node scripts\\eval-agent-runtime-spec011-unit-contract.mjs",
      "output": "agent-runtime-spec011-unit-contract: 7/7 passed. Report: C:\\Users\\lucas\\agentes-landing-system\\specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-unit-contract.json"
    },
    {
      "id": "action_coverage_contract_gate",
      "ok": true,
      "allowed": true,
      "exitCode": 0,
      "command": "python -m pytest services\\taliya-agent-runtime\\tests\\test_spec011_action_coverage_contract.py -q",
      "output": "..                                                                       [100%]\r\n2 passed in 0.16s"
    },
    {
      "id": "paid_batch_refuses_without_approval",
      "ok": false,
      "allowed": true,
      "exitCode": 1,
      "command": "node scripts\\eval-agent-runtime-spec011-t011-105-paid-batch.mjs",
      "output": "",
      "error": "Refusing paid OpenAI T011-105 batch without exact approval.\nRequired: --approval-token T011-105-US0.36 --approved-budget-usd 0.36\nNo paid commands were started."
    },
    {
      "id": "paid_batch_refuses_wrong_budget",
      "ok": false,
      "allowed": true,
      "exitCode": 1,
      "command": "node scripts\\eval-agent-runtime-spec011-t011-105-paid-batch.mjs --approval-token T011-105-US0.36 --approved-budget-usd 0.35",
      "output": "",
      "error": "Refusing paid OpenAI T011-105 batch without exact approval.\nRequired: --approval-token T011-105-US0.36 --approved-budget-usd 0.36\nNo paid commands were started."
    },
    {
      "id": "paid_batch_refuses_env_only_approval",
      "ok": false,
      "allowed": true,
      "exitCode": 1,
      "command": "node scripts\\eval-agent-runtime-spec011-t011-105-paid-batch.mjs",
      "output": "",
      "error": "Refusing paid OpenAI T011-105 batch without exact approval.\nRequired: --approval-token T011-105-US0.36 --approved-budget-usd 0.36\nNo paid commands were started."
    },
    {
      "id": "paid_batch_refuses_continue_on_failure",
      "ok": false,
      "allowed": true,
      "exitCode": 1,
      "command": "node scripts\\eval-agent-runtime-spec011-t011-105-paid-batch.mjs --approval-token T011-105-US0.36 --approved-budget-usd 0.36 --continue-on-failure",
      "output": "",
      "error": "Refusing --continue-on-failure for the T011-105 paid batch.\nThis batch must stop after the first paid failure to avoid unnecessary spend.\nNo paid commands were started."
    },
    {
      "id": "focused_t011_105_preflight_pytest",
      "ok": true,
      "allowed": true,
      "exitCode": 0,
      "command": "python -m pytest services\\taliya-agent-runtime\\tests\\test_spec011_mocked_conductor_fixtures.py::test_t011_105_missing_do_not_do_cases_have_local_preflight services\\taliya-agent-runtime\\tests\\test_spec011_widget_runtime_adapter.py::test_runtime_adapter_repairs_pain_first_product_route_without_paid_repair services\\taliya-agent-runtime\\tests\\test_spec011_widget_runtime_adapter.py::test_runtime_adapter_long_conversation_preflight_covers_last_real_gate_failures -q",
      "output": "......                                                                   [100%]\r\n6 passed in 1.35s"
    },
    {
      "id": "mocked_conductor_gate",
      "ok": true,
      "allowed": true,
      "exitCode": 0,
      "command": "node scripts\\eval-agent-runtime-spec011-mocked-conductor.mjs",
      "output": "agent-runtime-spec011-mocked-conductor: 6/6 passed. Report: C:\\Users\\lucas\\agentes-landing-system\\specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-mocked-conductor.json"
    },
    {
      "id": "golden_existing_evidence",
      "ok": false,
      "allowed": true,
      "exitCode": 1,
      "command": "node scripts\\eval-agent-runtime-spec011-golden-do-not-do.mjs --fixture scripts\\fixtures\\agent-runtime\\spec-011-golden-transcripts.json --report specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-full-required-final-matrix-budgeted-1.json --report specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-full-required-remaining-budgeted-1.json --report specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-golden-demo-direct-fixed-1.json --report specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-golden-long-conversation-16.json --name agent-runtime-spec011-t011-105-golden-readiness",
      "output": "agent-runtime-spec011-golden-do-not-do: 7/9 passed\nReport JSON: C:\\Users\\lucas\\agentes-landing-system\\specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-t011-105-golden-readiness.json\nReport MD: C:\\Users\\lucas\\agentes-landing-system\\specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-t011-105-golden-readiness.md",
      "error": ""
    },
    {
      "id": "do_not_do_existing_evidence",
      "ok": false,
      "allowed": true,
      "exitCode": 1,
      "command": "node scripts\\eval-agent-runtime-spec011-golden-do-not-do.mjs --fixture scripts\\fixtures\\agent-runtime\\spec-011-do-not-do-runtime.json --report specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-full-required-final-matrix-budgeted-1.json --report specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-full-required-remaining-budgeted-1.json --report specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-full-required-product-delta-budgeted-1.json --report specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-full-required-product-delta-integration-fixed-1.json --report specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-full-required-product-delta-remaining-budgeted-1.json --report specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-full-required-product-delta-diagnostic-refusal-fixed-1.json --report specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-p0-real-model.json --static-fixture scripts\\fixtures\\agent-runtime\\spec-011-do-not-do-runtime.json --static-report specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-static-audit.json --name agent-runtime-spec011-t011-105-do-not-do-readiness",
      "output": "agent-runtime-spec011-golden-do-not-do: 4/8 passed\nReport JSON: C:\\Users\\lucas\\agentes-landing-system\\specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-t011-105-do-not-do-readiness.json\nReport MD: C:\\Users\\lucas\\agentes-landing-system\\specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-t011-105-do-not-do-readiness.md",
      "error": ""
    },
    {
      "id": "pain_first_paid_plan_dry_run",
      "ok": true,
      "allowed": true,
      "exitCode": 0,
      "command": "python scripts\\eval-agent-runtime-spec011.py --fixture scripts\\fixtures\\agent-runtime\\spec-011-golden-transcripts.json --scenario-id final-pain-first --max-scenarios 1 --max-model-calls 1 --max-cost-usd 0.03 --dry-run --report-name agent-runtime-spec011-t011-105-pain-first-plan",
      "output": "Dry run only. Report JSON: C:\\Users\\lucas\\agentes-landing-system\\specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-t011-105-pain-first-plan-dry-run.json"
    },
    {
      "id": "long_conversation_paid_plan_dry_run",
      "ok": true,
      "allowed": true,
      "exitCode": 0,
      "command": "python scripts\\eval-agent-runtime-spec011.py --fixture scripts\\fixtures\\agent-runtime\\spec-011-golden-transcripts.json --scenario-id step3g-long-conversation --max-scenarios 1 --max-model-calls 14 --max-cost-usd 0.25 --dry-run --report-name agent-runtime-spec011-t011-105-long-conversation-plan",
      "output": "Dry run only. Report JSON: C:\\Users\\lucas\\agentes-landing-system\\specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-t011-105-long-conversation-plan-dry-run.json"
    },
    {
      "id": "do_not_do_paid_plan_dry_run",
      "ok": true,
      "allowed": true,
      "exitCode": 0,
      "command": "python scripts\\eval-agent-runtime-spec011.py --fixture scripts\\fixtures\\agent-runtime\\spec-011-do-not-do-runtime.json --scenario-id do-not-do-early-phone-capture --scenario-id do-not-do-date-vip-discount --scenario-id do-not-do-client-studio-whatsapp-capture --scenario-id do-not-do-wrong-student-language --max-scenarios 4 --max-model-calls 4 --max-cost-usd 0.08 --dry-run --report-name agent-runtime-spec011-t011-105-do-not-do-missing-plan",
      "output": "Dry run only. Report JSON: C:\\Users\\lucas\\agentes-landing-system\\specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-t011-105-do-not-do-missing-plan-dry-run.json"
    }
  ]
}
```

## PASS paid batch runner refuses missing or wrong approval before any paid command can start

```json
{
  "paidBatchRefusalCommands": [
    {
      "id": "paid_batch_refuses_without_approval",
      "ok": false,
      "allowed": true,
      "exitCode": 1,
      "command": "node scripts\\eval-agent-runtime-spec011-t011-105-paid-batch.mjs",
      "output": "",
      "error": "Refusing paid OpenAI T011-105 batch without exact approval.\nRequired: --approval-token T011-105-US0.36 --approved-budget-usd 0.36\nNo paid commands were started."
    },
    {
      "id": "paid_batch_refuses_wrong_budget",
      "ok": false,
      "allowed": true,
      "exitCode": 1,
      "command": "node scripts\\eval-agent-runtime-spec011-t011-105-paid-batch.mjs --approval-token T011-105-US0.36 --approved-budget-usd 0.35",
      "output": "",
      "error": "Refusing paid OpenAI T011-105 batch without exact approval.\nRequired: --approval-token T011-105-US0.36 --approved-budget-usd 0.36\nNo paid commands were started."
    },
    {
      "id": "paid_batch_refuses_env_only_approval",
      "ok": false,
      "allowed": true,
      "exitCode": 1,
      "command": "node scripts\\eval-agent-runtime-spec011-t011-105-paid-batch.mjs",
      "output": "",
      "error": "Refusing paid OpenAI T011-105 batch without exact approval.\nRequired: --approval-token T011-105-US0.36 --approved-budget-usd 0.36\nNo paid commands were started."
    },
    {
      "id": "paid_batch_refuses_continue_on_failure",
      "ok": false,
      "allowed": true,
      "exitCode": 1,
      "command": "node scripts\\eval-agent-runtime-spec011-t011-105-paid-batch.mjs --approval-token T011-105-US0.36 --approved-budget-usd 0.36 --continue-on-failure",
      "output": "",
      "error": "Refusing --continue-on-failure for the T011-105 paid batch.\nThis batch must stop after the first paid failure to avoid unnecessary spend.\nNo paid commands were started."
    }
  ]
}
```

## PASS known critical validator errors have no-500 recovery proof before paid rerun

```json
{
  "summary": {
    "total": 9,
    "passed": 9,
    "failed": 0,
    "coveredValidatorCodes": [
      "demo_direct_question_flags_missing",
      "diagnostic_final_demo_stage_missing",
      "diagnostic_final_staged_order_invalid",
      "diagnostic_next_question_invalid",
      "diagnostic_next_question_not_missing",
      "diagnostic_start_must_ask_active_students",
      "diagnostic_urgency_answer_not_captured",
      "pain_first_diagnostic_offer_must_use_diagnostic_route",
      "pain_first_must_offer_diagnostic",
      "price_question_missing_diagnostic_hook",
      "price_question_missing_diagnostic_offer",
      "price_question_missing_price_answer",
      "sales_inbox_diagnostic_status_mismatch",
      "stale_demo_direct_without_current_request",
      "unsupported_schema_version"
    ]
  },
  "releaseGate": "pass",
  "report": "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-known-validator-recovery.json"
}
```

## PASS T011-105 paid-batch safety audit passed all no-cost guard checks

```json
{
  "summary": {
    "total": 12,
    "passed": 12,
    "failed": 0
  },
  "releaseGate": "pass",
  "report": "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-t011-105-safety-audit.json"
}
```

## PASS full local unit/contract gate passed before paid evidence can be accepted

```json
{
  "summary": {
    "total": 7,
    "passed": 7,
    "failed": 0
  },
  "releaseGate": "pass",
  "report": "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-unit-contract.json"
}
```

## PASS golden existing evidence has exactly the expected paid-evidence gaps

```json
{
  "summary": {
    "total": 9,
    "passed": 7,
    "failed": 2,
    "runtimeCases": 9,
    "staticCases": 0,
    "estimatedCostUsd": 0.424509
  },
  "failures": [
    "final-pain-first",
    "step3g-long-conversation"
  ],
  "expectedGoldenMissing": [
    "final-pain-first",
    "step3g-long-conversation"
  ],
  "report": "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-t011-105-golden-readiness.json"
}
```

## PASS do-not-do existing evidence has exactly the expected four paid-evidence gaps

```json
{
  "summary": {
    "total": 8,
    "passed": 4,
    "failed": 4,
    "runtimeCases": 8,
    "staticCases": 0,
    "estimatedCostUsd": 0.056464
  },
  "failures": [
    "do-not-do-client-studio-whatsapp-capture",
    "do-not-do-date-vip-discount",
    "do-not-do-early-phone-capture",
    "do-not-do-wrong-student-language"
  ],
  "expectedDoNotDoMissing": [
    "do-not-do-client-studio-whatsapp-capture",
    "do-not-do-date-vip-discount",
    "do-not-do-early-phone-capture",
    "do-not-do-wrong-student-language"
  ],
  "report": "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-t011-105-do-not-do-readiness.json"
}
```

## PASS pain-first paid rerun plan is capped and targets only the missing golden pain-first scenario

```json
{
  "dryRun": {
    "feature": "011-taliya-commercial-agent-core-reset",
    "name": "agent-runtime-spec011-t011-105-pain-first-plan",
    "dryRun": true,
    "selectedScenarioCount": 1,
    "estimatedModelCalls": 1,
    "maxModelCalls": 1,
    "maxCostUsd": 0.03,
    "scenarioIds": [
      "final-pain-first"
    ]
  },
  "report": "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-t011-105-pain-first-plan-dry-run.json"
}
```

## PASS long-conversation paid rerun plan is capped and targets only the missing golden scenario

```json
{
  "dryRun": {
    "feature": "011-taliya-commercial-agent-core-reset",
    "name": "agent-runtime-spec011-t011-105-long-conversation-plan",
    "dryRun": true,
    "selectedScenarioCount": 1,
    "estimatedModelCalls": 14,
    "maxModelCalls": 14,
    "maxCostUsd": 0.25,
    "scenarioIds": [
      "step3g-long-conversation"
    ]
  },
  "report": "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-t011-105-long-conversation-plan-dry-run.json"
}
```

## PASS do-not-do paid rerun plan is capped and targets only the missing forbidden-behavior scenarios

```json
{
  "dryRun": {
    "feature": "011-taliya-commercial-agent-core-reset",
    "name": "agent-runtime-spec011-t011-105-do-not-do-missing-plan",
    "dryRun": true,
    "selectedScenarioCount": 4,
    "estimatedModelCalls": 4,
    "maxModelCalls": 4,
    "maxCostUsd": 0.08,
    "scenarioIds": [
      "do-not-do-early-phone-capture",
      "do-not-do-date-vip-discount",
      "do-not-do-client-studio-whatsapp-capture",
      "do-not-do-wrong-student-language"
    ]
  },
  "report": "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-t011-105-do-not-do-missing-plan-dry-run.json"
}
```

## PASS combined paid batch stays within the approved-request ceiling

```json
{
  "totalCapUsd": 0.36,
  "totalEstimatedModelCalls": 19
}
```

## PASS readiness gate produced no protected /pilates, landing visual, floating-agent, or Sales Inbox UI source diff

```json
{
  "protectedDiff": {
    "id": "protected_source_diff",
    "ok": true,
    "allowed": true,
    "exitCode": 0,
    "command": "git -c safe.directory=C:/Users/lucas/agentes-landing-system diff --name-only -- app/pilates components/landing data/landing lib/landing/floating-agent.ts components/internal/SalesInboxClient.tsx",
    "output": "",
    "files": []
  }
}
```
