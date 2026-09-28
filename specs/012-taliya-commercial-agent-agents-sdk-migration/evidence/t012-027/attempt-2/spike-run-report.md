# Spec 012 SDK Spike Run Report

- Proof type: isolated_spike_paid
- Model: gpt-5.4-mini
- Tracing disabled: True
- Paid call status: run
- Total model operations: 42
- Total estimated cost USD: 0.200663
- Aborted: False
- Abort reason: none

| # | Scenario | Status | Ops | Cost USD | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | cold_greeting | failed | 2 | 0.004813 | validator_blocked: sdk_missing_template_plan |
| 2 | pain_first | failed | 3 | 0.007753 | validator_blocked: sdk_missing_template_plan |
| 3 | price_first | failed | 3 | 0.006566 | validator_blocked: sdk_render_preview_failed |
| 4 | price_plus_pain | failed | 3 | 0.006405 | validator_blocked: sdk_template_variable_invalid |
| 5 | diagnostic_start | passed_structural | 3 | 0.006332 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 6 | diagnostic_numeric_120 | failed | 3 | 0.007953 | validator_blocked: sdk_template_variable_invalid, sdk_template_variable_invalid |
| 7 | diagnostic_urgency_final | failed | 3 | 0.038250 | max_turns_exceeded: scenario needed more than the approved 3 model operations; usage charged at worst-case estimate for budget safety. |
| 8 | whatsapp_scope | failed | 2 | 0.006674 | validator_blocked: sdk_render_preview_failed |
| 9 | demo_request | failed | 2 | 0.005216 | validator_blocked: sdk_direct_question_not_answered_first, sdk_missing_template_plan |
| 10 | waitlist_curiosity | failed | 3 | 0.006717 | validator_blocked: sdk_direct_question_not_answered_first |
| 11 | waitlist_contract_intent | failed | 3 | 0.038250 | max_turns_exceeded: scenario needed more than the approved 3 model operations; usage charged at worst-case estimate for budget safety. |
| 12 | human_handoff | failed | 3 | 0.038250 | max_turns_exceeded: scenario needed more than the approved 3 model operations; usage charged at worst-case estimate for budget safety. |
| 13 | do_not_do_497 | failed | 3 | 0.007844 | validator_blocked: sdk_render_preview_failed |
| 14 | do_not_do_checkout_discount_date_vip | passed_structural | 3 | 0.008241 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 15 | delivery_concurrency | passed_structural | 3 | 0.011399 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
