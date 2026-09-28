# Sales Inbox State Contract

Sales Inbox must make the following states visible enough for an operator to act.

## Required Lead Fields

- `leadId`
- `name`
- `normalizedPhone`
- `normalizedEmail`
- `channel`
- `sourceChannel`
- `sourceDetail`
- `studioName`
- `cityState`
- `primaryPainOrIntent`
- `diagnosticStatus`
- `diagnosticSummary`
- `demoStatus`
- `waitlistStatus`
- `missingWaitlistFields`
- `commercialStage`
- `priority`
- `nextAction`
- `aiPaused`
- `humanActive`
- `lastMessageAt`
- `createdAt`

## Required Message History

For each stored message:
- `id`
- `role`
- `content` or media placeholder
- `channel`
- `createdAt`
- `providerMessageId` when available
- `deliveryStatus` when available

## Priority Rules

- Price-only without pain: `cold`.
- Research-only without pain: `cold`.
- Pain captured: `warm`.
- Diagnostic offered or started: `warm`.
- Diagnostic complete with positive response: `hot`.
- Demo positive: `hot`.
- Waitlist joined: `hot`.
- Human requested: `manual`.
- Human active: `manual`.
- Mid-conversation rate limit: `manual`.
- Send error: `manual`.
- Hot lead missing required waitlist data: `manual`.

## Waitlist Rules

- `not_offered`: no waitlist CTA shown.
- `eligible`: high interest exists but CTA not yet shown.
- `offered`: waitlist CTA shown, no explicit acceptance.
- `pending_details`: accepted but missing required data.
- `joined`: accepted and required data complete.
- `declined`: lead explicitly refused.
- `undecided`: lead uncertain after waitlist-related path.
- `pending_details` must show `missingWaitlistFields` so an operator can see exactly what remains: name, contact, studio name, city/state, source channel, primary pain or diagnostic summary, or explicit acceptance.

## Human Control Rules

- `humanActive=true` prevents AI auto-reply.
- Re-enable must be explicit operator action.
- Inbound messages during human active are stored.
- Human takeover must set `nextAction` for operator visibility.
- Re-enable must record who/what re-enabled AI and when, and the next inbound lead message after re-enable may be answered automatically again.

## Merge Rules

- Strong merge: normalized phone match or normalized email match.
- Suggested match: name + studio/city similarity.
- No automatic merge: name-only match.

## Closure Rules

- `waiting_user`: agent is waiting for reply.
- `cold_closed`: cold lead stopped responding after the default or configured closure window.
- `waitlist_joined`: final waitlist success state.
- `waitlist_declined`: final waitlist refusal state.
- `human_active`: operator owns conversation.
- `error_needs_attention`: operational failure or mid-conversation limit.

Default closure window:
- `waiting_user`: set whenever the agent is waiting for the lead.
- `cold_closed`: allowed only after 7 days without reply for cold leads unless a configurable window overrides it.
- Diagnostic-offered, waitlist-offered and human-active conversations must not be auto-closed by the cold window without operator review.

## Funnel Visibility Rules

- Funnel events must be inspectable by internal report, API response or database query.
- Required verification includes at least event name, lead/session identifier, channel, commercial stage and timestamp.
- Retry/idempotency must prevent duplicate events for the same conversation step.
