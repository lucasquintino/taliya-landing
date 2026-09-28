# T012-051 simulated shadow comparison

- Schema: `012.simulated_shadow_comparison.v1`
- Comparison mode: `simulated_no_real_leads`
- Real lead traffic used: `False`
- Public activation: `False`
- Paid OpenAI calls for this task: `0`
- Source golden pass: `9/9`
- Trace all complete: `True`
- Projection all complete: `True`
- Manual review status: `pending_manual_review`
- Compared scenarios: `9`
- All compared scenarios passed: `True`

## What Was Compared

- Approved real-model golden transcript status from T012-043.
- Manual transcript package presence and pending product-owner decision from T012-047.
- Mandatory trace completeness from T012-045.
- Sales Inbox projection completeness from T012-046.
- Simulated shadow runtime invariant from T012-050: local evidence exists while public delivery is suppressed.

## Scenario Results

| Scenario | Golden | Manual package | Trace | Projection | Turns | Actions |
| --- | --- | --- | --- | --- | ---: | --- |
| `final-price-first` | `True` | `True` | `True` | `True` | 1 | answer_direct_product_question |
| `final-price-plus-pain` | `True` | `True` | `True` | `True` | 1 | answer_direct_product_question |
| `final-pain-first` | `True` | `True` | `True` | `True` | 1 | offer_diagnostic_from_pain |
| `final-instagram-interest` | `True` | `True` | `True` | `True` | 1 | answer_source_opening |
| `final-whatsapp-question` | `True` | `True` | `True` | `True` | 1 | answer_whatsapp_scope |
| `step3g-long-conversation` | `True` | `True` | `True` | `True` | 13 | answer_direct_product_question, start_requested_diagnostic, capture_pending_diagnostic_answer, capture_pending_diagnostic_answer, capture_pending_diagnostic_answer, capture_pending_diagnostic_answer, capture_pending_diagnostic_answer, complete_diagnostic, send_demo, answer_price_objection_with_context, offer_or_join_waitlist_if_eligible, answer_question_then_continue_waitlist, handoff_requested |
| `final-waitlist-joined` | `True` | `True` | `True` | `True` | 1 | join_waitlist |
| `final-human-request-silent-after` | `True` | `True` | `True` | `True` | 2 | handoff_requested,  |
| `final-demo-request` | `True` | `True` | `True` | `True` | 1 | send_demo |

## Failure Summary

- Failures: `[]`

## Scope Boundary

This comparison uses approved local evidence and simulated shadow invariants only. It does not use real lead traffic, activate public delivery, run paid OpenAI calls, change `/pilates`, change Sales Inbox UI, add checkout, alter multi-tenant behavior, or connect client/studio WhatsApp.
