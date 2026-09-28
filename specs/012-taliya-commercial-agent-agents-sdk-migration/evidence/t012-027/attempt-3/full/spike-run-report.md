# Spec 012 SDK Spike Run Report

- Proof type: isolated_spike_paid
- Model: gpt-5.4-mini
- Tracing disabled: True
- Paid call status: run
- Total model operations: 30
- Total estimated cost USD: 0.081956
- Aborted: False
- Abort reason: none

| # | Scenario | Status | Ops | Cost USD | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | cold_greeting | passed_structural | 2 | 0.005112 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 2 | pain_first | passed_structural | 2 | 0.004768 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 3 | price_first | passed_structural | 2 | 0.007157 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 4 | price_plus_pain | failed | 2 | 0.006658 | validator_blocked: sdk_direct_question_not_answered_first |
| 5 | diagnostic_start | passed_structural | 2 | 0.005285 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 6 | diagnostic_numeric_120 | passed_structural | 2 | 0.006494 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 7 | diagnostic_urgency_final | failed | 2 | 0.007995 | validator_blocked: sdk_render_preview_failed |
| 8 | whatsapp_scope | passed_structural | 2 | 0.006038 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 9 | demo_request | passed_structural | 2 | 0.005214 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 10 | waitlist_curiosity | failed | 2 | 0.006407 | validator_blocked: sdk_direct_question_not_answered_first |
| 11 | waitlist_contract_intent | passed_structural | 2 | 0.004378 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 12 | human_handoff | passed_structural | 2 | 0.003107 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 13 | do_not_do_497 | passed_structural | 2 | 0.005117 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 14 | do_not_do_checkout_discount_date_vip | failed | 2 | 0.004397 | validator_blocked: sdk_render_preview_failed |
| 15 | delivery_concurrency | failed | 2 | 0.003829 | validator_blocked: sdk_direct_question_not_answered_first |
