# Data Model: Price, Plan And Humanized Agent Experience

## Price Plan Interaction

Represents any lead turn asking about price, plans, comparison, recommendation or buying.

Fields:
- `intent`: price, plans, compare, recommend, buy, objection.
- `channel`: widget or whatsapp.
- `commercialSourceVersion`
- `conversationState`: cold, named, pain_captured, diagnostic_offered, diagnostic_in_progress, diagnostic_completed, demo_discussed, waitlist_offered, human_active.
- `answeredPriceFirst`: whether the agent answered price/plans before steering.
- `recommendationReadiness`: none, pain_hypothesis, diagnostic_complete, operator_confirmed.
- `allowedNextActions`: diagnostic_offer, view_plans, continue_diagnostic, waitlist_offer, human_handoff, no_cta.

Validation:
- Price/plan questions must set `answeredPriceFirst=true`.
- Agent price/plan answers must be traceable to the shared commercial source used by `/pilates/planos` or a documented shared config.
- `recommendationReadiness=none` cannot produce a final plan recommendation.
- `buy` cannot produce checkout unless plan and buying confirmation are both present.

## Real Simulation Run

Represents an acceptance eval run that exercises the real agent/runtime path.

Fields:
- `runId`
- `scenarioCount`
- `usesRealAgentRuntime`
- `modelProvider`
- `usageSummary`
- `estimatedCost`
- `budgetLimit`
- `acceptanceEligible`

Validation:
- Conversation-quality acceptance requires `usesRealAgentRuntime=true`.
- Deterministic mock responses must set `acceptanceEligible=false`.
- Reports must include usage or cost information for review.

## Message Delivery Policy

Represents enforced delivery behavior for automatic assistant messages.

Fields:
- `channel`: widget or whatsapp.
- `messageParts`: ordered assistant message parts.
- `maxPartLength`: configured per channel.
- `typingBeforeEach`: boolean.
- `delayStrategy`: proportional_to_length.
- `noInboundEcho`: boolean.

Validation:
- Every automatic reply must have at least one message part.
- Multi-idea replies should be split into multiple parts.
- No part should exceed the configured maximum unless explicitly marked as a diagnostic report that has already been reviewed.
- The lead's inbound text must not be repeated literally as an assistant part.
- `typingBeforeEach=true` is required for both widget and WhatsApp automatic delivery.

## Usage Limit Policy

Represents cost and abuse controls for automatic AI turns.

Fields:
- `scope`: whatsapp_phone, widget_session, contact_identity or global_daily.
- `limit`: maximum allowed automatic AI turns or cost units.
- `window`: reset window for the configured limit.
- `used`: current usage count or cost estimate.
- `limitReason`: rate_limit, abuse_repeated_messages, global_cap or operator_pause.
- `conversationMoment`: beginning or middle.

Validation:
- Limits must be checked before paid AI generation when possible.
- A limited turn must store the inbound message and limit reason.
- Beginning and middle conversation limits must use different humanized response copy.
- Global caps must stop additional AI spending while preserving operator-visible state.

## Lead Identity

Represents identifiers used to associate widget and WhatsApp leads.

Fields:
- `name`
- `normalizedPhone`
- `normalizedEmail`
- `providerContactId`
- `widgetSessionId`
- `whatsappSessionId`
- `studioName`
- `cityState`
- `mergeConfidence`: strong, suggested, none.

Validation:
- Normalized phone or email creates strong association.
- Name-only matches must not auto-merge.
- Existing histories must be preserved when leads are associated.

## Waitlist Qualification

Represents whether a lead can be marked as joined.

Fields:
- `waitlistStatus`: not_offered, eligible, offered, pending_details, joined, declined, undecided.
- `acceptedAt`
- `personName`
- `contact`
- `studioName`
- `cityState`
- `sourceChannel`
- `primaryPainOrIntent`
- `diagnosticSummary`
- `missingWaitlistFields`
- `nextAction`

Validation:
- `joined` requires explicit acceptance and minimum data.
- Missing minimum data results in `pending_details`.
- `pending_details` must include the exact missing fields needed for operator follow-up.
- WhatsApp phone can satisfy contact if present.

## Lead Priority

Represents operator priority.

Values:
- `cold`: greeting, price-only, research-only, no clear pain.
- `warm`: pain captured, diagnostic offered/started, demo requested, plan question with context.
- `hot`: waitlist joined, diagnostic-positive, demo-positive, buy intent with context, complete studio data.
- `manual`: human request, human active, mid-conversation limit, send error, hot lead with missing required details.

Validation:
- Joined waitlist must be hot.
- Human-active conversations must not be auto-replied.
- Price-only without pain remains cold.

## Funnel Event

Represents a durable commercial event for reporting.

Events:
- conversation_started
- name_captured
- contact_captured
- price_asked
- plans_requested
- recommendation_requested
- diagnostic_offered
- diagnostic_accepted
- diagnostic_completed
- demo_requested
- demo_positive
- waitlist_offered
- waitlist_joined
- waitlist_declined
- human_requested
- human_active
- ai_paused
- rate_limited
- send_error
- conversation_closed

Validation:
- Events are idempotent per conversation step.
- Events include lead/session/channel/stage metadata.
- Events do not depend on external automation success.
- Verification must be possible through a local report, internal API response or database query without Airtable/n8n.

## Conversation Closure State

Represents the operating state of a conversation.

Values:
- `ai_active`
- `waiting_user`
- `cold_closed`
- `waitlist_joined`
- `waitlist_declined`
- `human_active`
- `do_not_contact`
- `error_needs_attention`

Validation:
- Human-active state prevents automatic replies.
- Waitlist joined/declined states are final unless an operator changes them.
- Follow-up templates are out of scope.
- Default closure evaluation is configurable. If no custom config exists, cold leads may become `cold_closed` only after 7 days without reply, while diagnostic-offered or waitlist-offered leads remain `waiting_user` for operator review instead of receiving automated follow-up.
