# Storage Contract: Humanized Sales And Waitlist Flow

The implementation keeps the current Supabase/Postgres `sales_leads.data` JSON object as the durable source for the new commercial state. This avoids a broad table rewrite while preserving operator visibility through the Sales Inbox API.

## Lead Fields

- `commercialStage`: current funnel stage, such as `awaiting_name`, `diagnostic_offered`, `recommendation_validation`, `waitlist_offered`, `waitlist_pending_details` or `waitlist_joined`.
- `waitlistStatus`: `not_offered`, `eligible`, `offered`, `pending_details`, `joined`, `declined` or `undecided`.
- `waitlistOfferedAt`, `waitlistJoinedAt`, `waitlistDeclinedAt`: timestamps for waitlist transitions.
- `diagnosticStatus`, `diagnosticCompletedAt`: diagnostic progression.
- `demoStatus`, `demoOfferedAt`, `demoSeenAt`: demo branch progression.
- `leadSourceChannel`, `leadSourceDetail`: stable origin metadata for widget or WhatsApp.
- `primaryPainOrIntent`: short safe summary of why the lead is talking to Taliya.
- `nextAction`: operator-readable next step.

## Indexing

The migration `scripts/sql/002_ai_attendant_commercial_stage_waitlist.sql` adds expression indexes for:

- `commercialStage`
- `waitlistStatus`
- `demoStatus`
- `diagnosticStatus`

## Waitlist Rule

`waitlistStatus=joined` is valid only after explicit lead agreement and required details are available. If details are missing, the lead remains `pending_details`.
