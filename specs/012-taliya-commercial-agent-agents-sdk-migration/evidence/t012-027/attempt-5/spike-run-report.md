# Spec 012 SDK Spike Run Report

- Proof type: isolated_spike_paid
- Model: gpt-5.4-mini
- Tracing disabled: True
- Paid call status: run
- Total model operations: 36
- Total estimated cost USD: 0.096869
- Aborted: False
- Abort reason: none

| # | Scenario | Status | Ops | Cost USD | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | cold_greeting | passed_structural | 2 | 0.005387 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 2 | pain_first | passed_structural | 2 | 0.005341 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 3 | price_first | passed_structural | 3 | 0.006868 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 4 | price_plus_pain | passed_structural | 2 | 0.007017 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 5 | diagnostic_start | passed_structural | 2 | 0.005538 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 6 | diagnostic_numeric_120 | passed_structural | 2 | 0.006590 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 7 | diagnostic_urgency_final | failed | 3 | 0.015282 | validator_blocked: sdk_render_preview_failed |
| 8 | whatsapp_scope | passed_structural | 3 | 0.009268 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 9 | demo_request | passed_structural | 3 | 0.006130 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 10 | waitlist_curiosity | failed | 3 | 0.004480 | max_turns_exceeded: scenario needed more than the approved 3 model operations; partial run items recorded for diagnosis. |
| 11 | waitlist_contract_intent | passed_structural | 2 | 0.003909 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 12 | human_handoff | passed_structural | 2 | 0.005556 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 13 | do_not_do_497 | passed_structural | 3 | 0.004446 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 14 | do_not_do_checkout_discount_date_vip | passed_structural | 2 | 0.005609 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 15 | delivery_concurrency | passed_structural | 2 | 0.005448 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
