# T012-045 mandatory trace evidence

- Schema: 012.mandatory_trace_evidence_summary.v1
- Source report: `specs\012-taliya-commercial-agent-agents-sdk-migration\evidence\t012-043-real-model-golden-transcripts\20260616T121413Z\report.json`
- Model: `gpt-5.4-mini`
- Paid call status: `attempted_real_openai`
- External trace export enabled: `False`
- Scenario count: `9`
- Total turns: `22`
- Total traces: `21`
- All trace complete: `True`
- Total model operations from source: `33`
- Total cost from source: `$0.087158`

## Required Sections

- `inbound`
- `turn_gate`
- `context_snapshot`
- `turn_situation`
- `sdk_start`
- `sdk_run_items`
- `sdk_final_output`
- `taliya_proposal`
- `action_decision`
- `compiler`
- `validators`
- `repair_or_escalation`
- `render_plan`
- `rendered_messages`
- `state_diff`
- `sales_inbox_projection`
- `delivery`
- `usage_cost`

## Scenario Summary

| Scenario | Trace complete | Turns | Traces | Ops | Cost | Actions |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `final-price-first` | `True` | 1 | 1 | 2 | $0.004206 | answer_direct_product_question |
| `final-price-plus-pain` | `True` | 1 | 1 | 3 | $0.007814 | answer_direct_product_question |
| `final-pain-first` | `True` | 1 | 1 | 2 | $0.004431 | offer_diagnostic_from_pain |
| `final-instagram-interest` | `True` | 1 | 1 | 2 | $0.004432 | answer_source_opening |
| `final-whatsapp-question` | `True` | 1 | 1 | 2 | $0.004188 | answer_whatsapp_scope |
| `step3g-long-conversation` | `True` | 13 | 13 | 16 | $0.048401 | answer_direct_product_question, start_requested_diagnostic, capture_pending_diagnostic_answer, capture_pending_diagnostic_answer, capture_pending_diagnostic_answer, capture_pending_diagnostic_answer, capture_pending_diagnostic_answer, complete_diagnostic, send_demo, answer_price_objection_with_context, offer_or_join_waitlist_if_eligible, answer_question_then_continue_waitlist, handoff_requested |
| `final-waitlist-joined` | `True` | 1 | 1 | 1 | $0.002439 | join_waitlist |
| `final-human-request-silent-after` | `True` | 2 | 1 | 2 | $0.003932 | handoff_requested,  |
| `final-demo-request` | `True` | 1 | 1 | 3 | $0.007316 | send_demo |

## Missing Or Incomplete Trace Checks

- Missing required sections: `{}`
- Missing trace turn indexes: `{}`
- Incomplete trace turn indexes: `{}`

## Local-Only Trace Policy

External/provider trace export remains disabled by D-012-007 and D-012-009. This package is local evidence generated from the approved T012-043 real-model report; it does not activate public delivery, outbox reservation, endpoint cutover, checkout, Sales Inbox UI, multi-tenant behavior, or client/studio WhatsApp connection work.
