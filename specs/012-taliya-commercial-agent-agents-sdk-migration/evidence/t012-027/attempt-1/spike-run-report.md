# Spec 012 SDK Spike Run Report

- Proof type: isolated_spike_paid
- Model: gpt-5.4-mini
- Tracing disabled: True
- Paid call status: run
- Total model operations: 39
- Total estimated cost USD: 0.080724
- Aborted: False
- Abort reason: none

| # | Scenario | Status | Ops | Cost USD | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | cold_greeting | failed | 2 | 0.004786 | validator_blocked: sdk_missing_template_plan |
| 2 | pain_first | failed | 2 | 0.005842 | validator_blocked: sdk_missing_template_plan |
| 3 | price_first | failed | 3 | 0.006352 | validator_blocked: sdk_direct_question_not_answered_first, sdk_missing_template_plan |
| 4 | price_plus_pain | failed | 3 | 0.007422 | validator_blocked: sdk_direct_question_not_answered_first, sdk_missing_template_plan |
| 5 | diagnostic_start | failed | 2 | 0.003447 | validator_blocked: sdk_missing_template_plan |
| 6 | diagnostic_numeric_120 | failed | 3 | 0.005621 | validator_blocked: sdk_missing_answer_obligation, sdk_missing_template_plan |
| 7 | diagnostic_urgency_final | failed | 3 | 0.005093 | validator_blocked: sdk_missing_template_plan |
| 8 | whatsapp_scope | failed | 3 | 0.006508 | validator_blocked: sdk_missing_template_plan |
| 9 | demo_request | failed | 2 | 0.004010 | validator_blocked: sdk_missing_answer_obligation, sdk_missing_template_plan |
| 10 | waitlist_curiosity | failed | 2 | 0.006438 | validator_blocked: sdk_direct_question_not_answered_first |
| 11 | waitlist_contract_intent | failed | 3 | 0.005658 | validator_blocked: sdk_missing_answer_obligation, sdk_missing_template_plan |
| 12 | human_handoff | failed | 3 | 0.005813 | validator_blocked: sdk_missing_answer_obligation, sdk_missing_template_plan |
| 13 | do_not_do_497 | failed | 3 | 0.004085 | validator_blocked: sdk_direct_question_not_answered_first, sdk_missing_template_plan |
| 14 | do_not_do_checkout_discount_date_vip | failed | 2 | 0.005005 | validator_blocked: sdk_direct_question_not_answered_first, sdk_missing_template_plan |
| 15 | delivery_concurrency | failed | 3 | 0.004644 | validator_blocked: sdk_direct_question_not_answered_first, sdk_missing_template_plan |
