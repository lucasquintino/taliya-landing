# Spec 012 Sales Inbox Projection Package

- Schema: 012.sales_inbox_projection_export.v1
- Scenario: t012-046-mocked-sales-inbox-projection
- Proof mode: mocked_no_cost
- Projection complete: True
- Turn count: 4
- Projection count: 3
- Total model operations: 5
- Total cost USD: 0.0

| Turn | Status | Mode | Action | Stage | Diagnostic | Projection |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | delivered | entry | answer_direct_product_question | diagnostic_offered | offered | True |
| 1 | delivered | entry | start_requested_diagnostic | diagnostic_waiting_answer | in_progress | True |
| 2 | delivered | diagnostic | handoff_requested | human_handoff | not_started | True |
| 3 | suppressed | handoff |  |  |  | False |
