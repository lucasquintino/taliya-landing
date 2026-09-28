# Spec 012 Mandatory Trace Package

- Schema: 012.action_trace_export.v1
- Scenario: step3g-long-conversation
- Proof mode: real_model_t012_043_approved_9_of_9
- Trace complete: True
- External trace export enabled: False
- Turn count: 13
- Trace count: 13
- Total model operations: 16
- Total cost USD: 0.048401

| Turn | Status | Mode | Action | Templates | Trace required | Trace present |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | delivered | entry | answer_direct_product_question | product.price_direct, diagnostic.price_hook | True | True |
| 1 | delivered | entry | start_requested_diagnostic | diagnostic.start, diagnostic.ask_active_students | True | True |
| 2 | delivered | diagnostic | capture_pending_diagnostic_answer | diagnostic.ask_main_pain | True | True |
| 3 | delivered | diagnostic | capture_pending_diagnostic_answer | diagnostic.ask_pain_detail | True | True |
| 4 | delivered | diagnostic | capture_pending_diagnostic_answer | diagnostic.ask_current_process | True | True |
| 5 | delivered | diagnostic | capture_pending_diagnostic_answer | diagnostic.ask_priority | True | True |
| 6 | delivered | diagnostic | capture_pending_diagnostic_answer | diagnostic.ask_urgency | True | True |
| 7 | delivered | diagnostic | complete_diagnostic | diagnostic.deliver_hold, diagnostic.deliver_context, diagnostic.deliver_crm_base, diagnostic.deliver_operational_step, diagnostic.deliver_agent_recommendation, diagnostic.deliver_plan_recommendation, diagnostic.deliver_demo_not_offered | True | True |
| 8 | delivered | post_diagnostic | send_demo | product.demo_direct | True | True |
| 9 | delivered | post_diagnostic | answer_price_objection_with_context | product.price_objection_value | True | True |
| 10 | delivered | post_diagnostic | offer_or_join_waitlist_if_eligible | waitlist.offer_after_contract_intent | True | True |
| 11 | delivered | waitlist | answer_question_then_continue_waitlist | waitlist.current_path_explained, waitlist.ask_missing_contact_path | True | True |
| 12 | delivered | waitlist | handoff_requested | handoff.acknowledge | True | True |
