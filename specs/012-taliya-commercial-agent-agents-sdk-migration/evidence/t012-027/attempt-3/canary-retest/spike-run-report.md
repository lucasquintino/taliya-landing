# Spec 012 SDK Spike Run Report

- Proof type: isolated_spike_paid
- Model: gpt-5.4-mini
- Tracing disabled: True
- Paid call status: run
- Total model operations: 3
- Total estimated cost USD: 0.038250
- Aborted: False
- Abort reason: none

| # | Scenario | Status | Ops | Cost USD | Reason |
| --- | --- | --- | --- | --- | --- |
| 7 | diagnostic_urgency_final | failed | 3 | 0.038250 | max_turns_exceeded: scenario needed more than the approved 3 model operations; usage charged at worst-case estimate for budget safety. |
