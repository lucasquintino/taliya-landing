# Data Model: Taliya Sales Agent Architecture

## Overview

The implementation should extend the existing Sales Inbox/Postgres model instead of replacing it wholesale. Existing lead, message and commercial-stage fields may remain for compatibility, but the new agent requires versioned v2 state, substate, trace, cost and tool-action records.

## Entity: Lead Profile

Represents a person/studio lead across widget and WhatsApp.

Fields:

- `id`
- `primary_channel`: `widget` or `whatsapp`
- `source`: `direct`, `site`, `instagram`, `facebook`, `ad`, `unknown`
- `person_name`
- `person_name_confidence`: `high`, `medium`, `low`, `unusable`
- `whatsapp_phone`
- `email`
- `studio_name`
- `city`
- `state`
- `priority`: `cold`, `warm`, `hot`, `waitlist_ready`, `human_needed`, `no_action`
- `next_action`
- `summary`
- `created_at`
- `updated_at`

Validation:

- WhatsApp phone is a strong identifier.
- Email is a strong identifier.
- Name alone must never merge records automatically.
- Cold identifiable leads must still be visible in Sales Inbox.

## Entity: Lead Identity Link

Links channel identities without unsafe merging.

Fields:

- `id`
- `lead_id`
- `identifier_type`: `whatsapp_phone`, `email`, `widget_session`, `studio_name`, `possible_duplicate`
- `identifier_value_hash` or safe value when appropriate
- `confidence`: `strong`, `possible`, `weak`
- `review_required`
- `created_at`

Rules:

- Merge/associate automatically only on strong phone/email evidence.
- Flag possible duplicates for review when evidence is plausible but weak.

## Entity: Conversation

Represents the ongoing thread for a lead in a channel.

Fields:

- `id`
- `lead_id`
- `channel`: `widget`, `whatsapp`
- `channel_connection_id`
- `phone_number_id` for WhatsApp
- `widget_session_id`
- `source`
- `macro_state`
- `substate`
- `human_status`: `none`, `requested`, `active`, `resumed`
- `closure_reason`
- `last_inbound_at`
- `last_outbound_at`
- `created_at`
- `updated_at`

Macro states:

- `new_lead`
- `open_question`
- `product_question`
- `price_or_plan`
- `diagnostic_offered`
- `diagnostic_in_progress`
- `diagnostic_completed`
- `demo_interest`
- `waitlist_offered`
- `waitlist_pending_details`
- `waitlist_joined`
- `human_requested`
- `human_active`
- `closed`

Substate shape:

- `askedQuestions`: string keys
- `knownFacts`: structured lead and studio facts
- `pendingQuestion`: current open question key or null
- `diagnosticStep`: current diagnostic step or null
- `missingFields`: required fields still missing
- `lastTopic`
- `lastAnsweredDirectQuestion`
- `sentiment`: `neutral`, `curious`, `urgent`, `skeptical`, `irritated`
- `confidence`: `high`, `medium`, `low`
- `lastSummary`
- `queuedResponseStatus`: `none`, `queued`, `suppressed`, `revalidate_required`
- `cost`: accumulated estimated cost and cap status

Rules:

- Persist macro state and substate before and after every meaningful AI turn.
- State updates that change waitlist, human handoff or diagnostic completion must be atomic.

## Entity: Message

Represents inbound/outbound channel messages.

Fields:

- `id`
- `conversation_id`
- `lead_id`
- `direction`: `inbound`, `outbound`, `system`, `human`
- `channel_message_id`
- `idempotency_key`
- `text`
- `message_type`: `text`, `audio`, `image`, `document`, `unknown`
- `raw_payload_ref` or safe JSON payload
- `delivery_status`
- `created_at`

Rules:

- Duplicate webhook/event ids must not create duplicate messages or duplicate replies.
- Unsupported media cannot satisfy diagnostic questions without reliable text.

## Entity: Product Knowledge Source

Versioned commercial truth used by the agent.

Fields:

- `version`
- `plans`
- `prices`
- `includedRoutines`
- `planComparisonNotes`
- `links`
- `demoStatus`
- `waitlistAvailability`
- `guaranteeCancellationPolicy`
- `privacyPolicy`
- `unsupportedClaims`
- `updated_at`

Rules:

- Price/plan/demo/availability answers must trace the source version.
- If unavailable, the agent must not invent.

## Entity: Diagnostic Record

Structured diagnosis and recommendation.

Input fields:

- `activeStudents` or explicit unknown
- `mainPainOrIntent`
- `currentWorkflowOrTool`
- `painSpecificDetail`
- `priorityToMakeLighter`
- `urgency`
- `knownContactPath`

Output fields:

- `mainBottleneck`
- `evidence`
- `likelyOperationalCause`
- `firstOrganizationStep`
- `indicatedAgents`
- `planOrPlanRangeToCompare`
- `confidence`: `high`, `medium`, `low`
- `unknowns`
- `validationQuestion`
- `validatedByLead`: `yes`, `no`, `unclear`

Rules:

- Do not complete if output would be generic.
- Use evidence from the lead messages or mark unknowns.
- Do not ask studio/city until after value and waitlist agreement unless volunteered.

## Entity: Waitlist Record

Represents waitlist status and readiness.

Fields:

- `lead_id`
- `conversation_id`
- `status`: `not_offered`, `offered`, `pending_details`, `joined`, `declined`, `removed`
- `joined_at`
- `declined_at`
- `studio_name`
- `city`
- `state`
- `contact_path`
- `main_pain_summary`
- `diagnostic_summary`
- `plan_or_range`
- `priority`
- `next_action`
- `missing_fields`

Actionable waitlist requirements:

- contact path
- studio name
- city/state
- source and channel
- main pain/context summary
- diagnostic summary or equivalent high-intent context
- likely plan/range when available
- priority
- joined date

## Entity: Semantic Interpretation Result

Structured understanding for each lead message.

Fields:

- `primaryIntent`
- `secondaryIntents`
- `directQuestions`
- `factsExtracted`
- `urgency`
- `sentiment`
- `riskFlags`
- `confidence`
- `needsEscalation`
- `escalationReason`

Rules:

- Must read the whole message before action selection.
- Direct questions must be answered before steering.

## Entity: Orchestration Decision

Agent decision for the next turn.

Fields:

- `selectedAction`
- `stateTransition`
- `toolActions`
- `responseObjective`
- `guardrailRequirements`
- `modelClass`: `default`, `stronger`
- `escalationReason`
- `costBudgetCategory`

## Entity: Tool Action Record

Idempotent side-effect/action record.

Fields:

- `idempotency_key`
- `tool_name`
- `input`
- `output`
- `status`: `pending`, `succeeded`, `failed`, `skipped`
- `retry_count`
- `failure_reason`
- `conversation_id`
- `lead_id`
- `created_at`

Rules:

- Retrying a tool with the same idempotency key must not duplicate side effects.

## Entity: Agent Trace

Debug and audit record for every meaningful turn.

Fields:

- `normalizedInput`
- `stateBefore`
- `productSourceVersion`
- `semanticInterpretation`
- `orchestrationDecision`
- `toolActions`
- `guardrailResult`
- `responseDraft`
- `validatedResponse`
- `stateAfter`
- `deliveryResult`
- `modelUsage`
- `costEstimate`
- `fallbackReason`

## Entity: Model Usage Record

Tracks model/cost.

Fields:

- `model`
- `operation`: `interpretation`, `generation`, `judge`, `summary`, `recovery`
- `input_tokens`
- `output_tokens`
- `estimated_cost_usd`
- `conversation_cost_before`
- `conversation_cost_after`
- `budget_category`
- `cap_status`: `ok`, `review`, `high`, `hard_cap_blocked`

Cost categories:

- simple answer: target under US$0.005
- medium qualified lead: target up to US$0.03, review above US$0.05
- diagnostic lead: target up to US$0.05 when possible, review above US$0.08
- long/complex lead: target below US$0.10
- hard cap: block automatic AI at or above US$0.15

## Entity: Evaluation Transcript

Versioned eval artifact.

Fields:

- `scenario_id`
- `variant_id`
- `channel`
- `source`
- `transcript`
- `stateTransitions`
- `toolCalls`
- `productSourceVersion`
- `costEstimate`
- `rubricScores`
- `blockingFailures`
- `reviewNotes`
- `approvedBy`
- `approvedAt`

## Entity: Evaluation Run Budget

Controls realistic eval spend.

Fields:

- `run_id`
- `dry_run`
- `max_scenarios`
- `max_real_model_calls`
- `max_estimated_cost_usd`
- `real_model_call_count`
- `estimated_cost_usd`
- `stop_reason`
- `skipped_scenarios`

Rules:

- Skipped scenarios are not failures, but they cannot count as passed.
- A production-readiness report must include the budget and stop reason.

## Entity: Release Approval Record

Records explicit product-owner approval before production replacement.

Fields:

- `feature`
- `approved_by`
- `approved_at`
- `eval_report_ids`
- `manual_test_report_ids`
- `known_waivers`
- `migration_verified`
- `rollback_documented`
- `production_switch`

Rules:

- Approval is required before enabling v2 automatic replies in production.

## State Transition Notes

- Cold greeting moves `new_lead` to `open_question`.
- Direct price/plan question moves to `price_or_plan` but may return to prior state after answer.
- Diagnostic offer moves to `diagnostic_offered`.
- Accepted diagnostic moves to `diagnostic_in_progress`.
- Completed diagnostic moves to `diagnostic_completed`.
- Positive validation after diagnostic moves to `waitlist_offered`.
- Waitlist agreement with missing details moves to `waitlist_pending_details`.
- Complete waitlist details moves to `waitlist_joined`.
- Human request moves to `human_requested`, then `human_active`.
- Explicit operator resume leaves `human_active` and restores the last safe macro state.
- Cost hard cap preserves state, marks human follow-up and blocks further automatic AI replies.
