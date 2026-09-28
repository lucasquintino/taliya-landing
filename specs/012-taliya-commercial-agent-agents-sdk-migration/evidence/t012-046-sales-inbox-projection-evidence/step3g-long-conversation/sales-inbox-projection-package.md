# Spec 012 Sales Inbox Projection Package

- Schema: 012.sales_inbox_projection_export.v1
- Scenario: step3g-long-conversation
- Proof mode: real_model_t012_043_approved_9_of_9
- Projection complete: True
- Turn count: 13
- Projection count: 13
- Total model operations: 16
- Total cost USD: 0.048401

| Turn | Status | Mode | Action | Stage | Diagnostic | Projection |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | delivered | entry | answer_direct_product_question | diagnostic_offered | offered | True |
| 1 | delivered | entry | start_requested_diagnostic | diagnostic_waiting_answer | in_progress | True |
| 2 | delivered | diagnostic | capture_pending_diagnostic_answer | diagnostic_waiting_answer | in_progress | True |
| 3 | delivered | diagnostic | capture_pending_diagnostic_answer | diagnostic_waiting_answer | in_progress | True |
| 4 | delivered | diagnostic | capture_pending_diagnostic_answer | diagnostic_waiting_answer | in_progress | True |
| 5 | delivered | diagnostic | capture_pending_diagnostic_answer | diagnostic_waiting_answer | in_progress | True |
| 6 | delivered | diagnostic | capture_pending_diagnostic_answer | diagnostic_waiting_answer | in_progress | True |
| 7 | delivered | diagnostic | complete_diagnostic | diagnostic_delivered | completed | True |
| 8 | delivered | post_diagnostic | send_demo | demo_reaction_pending | completed | True |
| 9 | delivered | post_diagnostic | answer_price_objection_with_context | post_diagnostic_questions | completed | True |
| 10 | delivered | post_diagnostic | offer_or_join_waitlist_if_eligible | waitlist_offered | completed | True |
| 11 | delivered | waitlist | answer_question_then_continue_waitlist | waitlist_pending_data | completed | True |
| 12 | delivered | waitlist | handoff_requested | human_handoff | completed | True |
