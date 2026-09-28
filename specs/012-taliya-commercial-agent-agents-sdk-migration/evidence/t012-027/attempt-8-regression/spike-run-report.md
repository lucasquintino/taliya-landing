# Spec 012 SDK Spike Run Report

- Proof type: isolated_spike_paid
- Model: gpt-5.4-mini
- Tracing disabled: True
- Paid call status: run
- Total model operations: 40
- Total estimated cost USD: 0.097174
- Aborted: False
- Abort reason: none

| # | Scenario | Status | Ops | Cost USD | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | cold_greeting | passed_structural | 2 | 0.005127 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 2 | pain_first | passed_structural | 3 | 0.004502 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 3 | price_first | failed | 3 | 0.007592 | validator_blocked: sdk_render_preview_failed |
| 4 | price_plus_pain | passed_structural | 3 | 0.008395 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 5 | diagnostic_start | passed_structural | 3 | 0.006532 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 6 | diagnostic_numeric_120 | passed_structural | 2 | 0.004625 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 7 | diagnostic_urgency_final | passed_structural | 3 | 0.014194 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 8 | whatsapp_scope | failed | 3 | 0.006767 | validator_blocked: sdk_render_preview_failed |
| 9 | demo_request | failed | 4 | 0.005924 | validator_blocked: sdk_render_preview_failed |
| 10 | waitlist_curiosity | passed_structural | 2 | 0.005463 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 11 | waitlist_contract_intent | passed_structural | 2 | 0.006195 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 12 | human_handoff | passed_structural | 2 | 0.004093 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 13 | do_not_do_497 | passed_structural | 3 | 0.005889 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 14 | do_not_do_checkout_discount_date_vip | passed_structural | 3 | 0.008102 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 15 | delivery_concurrency | passed_structural | 2 | 0.003774 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
