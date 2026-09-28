# Spec 012 SDK Spike Run Report

- Proof type: isolated_spike_paid
- Model: gpt-5.4-mini
- Tracing disabled: True
- Paid call status: run
- Total model operations: 8
- Total estimated cost USD: 0.055582
- Aborted: False
- Abort reason: none

| # | Scenario | Status | Ops | Cost USD | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | cold_greeting | passed_structural | 2 | 0.005352 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 3 | price_first | passed_structural | 3 | 0.011980 | Structured proposal validated and approved templates rendered. Conversational-quality pass/fail still requires the manual review described in the approval packet. |
| 7 | diagnostic_urgency_final | failed | 3 | 0.038250 | max_turns_exceeded: scenario needed more than the approved 3 model operations; usage charged at worst-case estimate for budget safety. |
