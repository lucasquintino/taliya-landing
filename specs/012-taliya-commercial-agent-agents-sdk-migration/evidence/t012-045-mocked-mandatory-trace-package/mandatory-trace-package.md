# Spec 012 Mandatory Trace Package

- Schema: 012.action_trace_export.v1
- Scenario: t012-045-mocked-mandatory-trace-full-funnel
- Proof mode: mocked_no_cost
- Trace complete: True
- External trace export enabled: False
- Turn count: 5
- Trace count: 4
- Total model operations: 6
- Total cost USD: 0.0

| Turn | Status | Mode | Action | Templates | Trace required | Trace present |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | delivered | entry | answer_direct_product_question | product.price_direct, diagnostic.price_hook | True | True |
| 1 | delivered | entry | start_requested_diagnostic | diagnostic.start, diagnostic.ask_active_students | True | True |
| 2 | delivered | diagnostic | capture_pending_diagnostic_answer | diagnostic.partial_progress, diagnostic.ask_main_pain | True | True |
| 3 | delivered | diagnostic | handoff_requested | handoff.acknowledge | True | True |
| 4 | suppressed | handoff |  |  | False | False |
