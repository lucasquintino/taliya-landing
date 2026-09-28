# T012-046 Sales Inbox projection evidence

- Schema: 012.sales_inbox_projection_evidence_summary.v1
- Source report: `specs\012-taliya-commercial-agent-agents-sdk-migration\evidence\t012-043-real-model-golden-transcripts\20260616T121413Z\report.json`
- Model: `gpt-5.4-mini`
- Paid call status: `attempted_real_openai`
- Scenario count: `9`
- Total turns: `22`
- Total projections: `21`
- All projection complete: `True`
- Sales Inbox UI changed: `False`
- Persistence commit changed: `False`
- Total model operations from source: `33`
- Total cost from source: `$0.087158`

## Required Fields

- `conversation_id`
- `lead_id`
- `commercial_stage`
- `diagnostic_status`
- `fields`

## Required Nested Fields

- `fields.template_ids`
- `fields.validator_status`
- `fields.source_labels`

## Scenario Summary

| Scenario | Projection complete | Turns | Projections | Ops | Cost | Stages |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `final-price-first` | `True` | 1 | 1 | 2 | $0.004206 | diagnostic_offered |
| `final-price-plus-pain` | `True` | 1 | 1 | 3 | $0.007814 | diagnostic_offered |
| `final-pain-first` | `True` | 1 | 1 | 2 | $0.004431 | diagnostic_offered |
| `final-instagram-interest` | `True` | 1 | 1 | 2 | $0.004432 | general_interest |
| `final-whatsapp-question` | `True` | 1 | 1 | 2 | $0.004188 | diagnostic_offered |
| `step3g-long-conversation` | `True` | 13 | 13 | 16 | $0.048401 | diagnostic_offered, diagnostic_waiting_answer, diagnostic_waiting_answer, diagnostic_waiting_answer, diagnostic_waiting_answer, diagnostic_waiting_answer, diagnostic_waiting_answer, diagnostic_delivered, demo_reaction_pending, post_diagnostic_questions, waitlist_offered, waitlist_pending_data, human_handoff |
| `final-waitlist-joined` | `True` | 1 | 1 | 1 | $0.002439 | waitlist_joined |
| `final-human-request-silent-after` | `True` | 2 | 1 | 2 | $0.003932 | human_handoff |
| `final-demo-request` | `True` | 1 | 1 | 3 | $0.007316 | demo_reaction_pending |

## Aggregates

- Commercial stages: `{'diagnostic_offered': 5, 'general_interest': 1, 'diagnostic_waiting_answer': 6, 'diagnostic_delivered': 1, 'demo_reaction_pending': 2, 'post_diagnostic_questions': 1, 'waitlist_offered': 1, 'waitlist_pending_data': 1, 'human_handoff': 2, 'waitlist_joined': 1}`
- Waitlist statuses: `{'none': 17, 'offered': 3, 'joined': 1}`
- Operator next actions: `{'none': 13, 'review_completed_diagnostic': 5, 'human_follow_up': 2, 'monitor_waitlist': 1}`

## Missing Projection Checks

- Missing required fields: `{}`
- Missing projection turn indexes: `{}`

## Scope Boundary

This is a local evidence export from validated turn projections. It does not change Sales Inbox UI, persistence commit behavior, public delivery, endpoint cutover, `/pilates`, checkout, multi-tenant behavior, or client/studio WhatsApp connection work.
