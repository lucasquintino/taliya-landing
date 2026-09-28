# Data Model: OpenAI CS Agents Adaptation For Taliya Commercial

## Overview

The new runtime introduces generic `agent_runtime_*` entities that can support future agents while only implementing `taliya_commercial` now. Existing Sales Inbox lead and message records remain operationally useful and should be extended through projections instead of replaced wholesale.

## Entity: Agent Definition

Represents a registered agent inside the runtime.

Fields:

- `agent_key`: stable key, initially `taliya_commercial`
- `agent_family`: `taliya`, `taliya_configuration`, `studio_operations`
- `display_name`
- `owner_scope`: `taliya` or `studio`
- `tenant_id`: null for Taliya-owned agents
- `enabled`
- `default_model`
- `strong_model`
- `tools`
- `guardrails`
- `handoffs`
- `created_at`
- `updated_at`

Rules:

- This feature registers only `taliya_commercial` as active.
- Unknown agent keys are rejected before any side effect.
- Future agent keys may be reserved in docs but not implemented.

## Entity: Agent Runtime Conversation

Represents a durable conversation between a lead and an agent on one channel.

Fields:

- `id`
- `agent_key`
- `agent_family`
- `owner_scope`
- `tenant_id`
- `lead_id`
- `channel`: `widget` or `whatsapp`
- `channel_conversation_id`
- `current_agent_name`
- `current_state`
- `previous_state`
- `next_state`
- `human_status`: `none`, `requested`, `active`, `resumed`
- `last_summary`
- `last_inbound_at`
- `last_outbound_at`
- `created_at`
- `updated_at`

Rules:

- `tenant_id` is null for `taliya_commercial`.
- Human-active conversations record inbound messages but do not generate AI replies.
- Current agent is updated from runner output after every successful turn.
- Current state must follow [conversation-state-contract.md](./conversation-state-contract.md).

## Entity: Agent Runtime Message

Represents inbound, outbound, human, system, tool, or guardrail messages.

Fields:

- `id`
- `conversation_id`
- `lead_id`
- `agent_key`
- `direction`: `inbound`, `outbound`, `human`, `system`, `tool`
- `channel`
- `channel_message_id`
- `idempotency_key`
- `text`
- `message_type`: `text`, `image`, `audio`, `document`, `unsupported`, `unknown`
- `raw_payload_ref`
- `delivery_status`
- `created_at`

Rules:

- Duplicate idempotency keys do not create duplicate outbound replies.
- Unsupported media cannot be used as diagnostic evidence unless transcribed or summarized by the user.

## Entity: Agent Runtime Run

Represents one execution of the agent runtime for one inbound event.

Fields:

- `id`
- `conversation_id`
- `lead_id`
- `agent_key`
- `channel`
- `input_message_id`
- `current_agent_before`
- `current_agent_after`
- `status`: `succeeded`, `failed`, `blocked`, `human_paused`, `cost_capped`
- `structured_output`
- `template_ids`
- `render_plan`
- `trace_id`
- `error_code`
- `created_at`
- `completed_at`

Rules:

- A run can complete without user-facing output when human pause or guardrail block applies.
- Invalid structured output is a failed run and must not be delivered.
- Invalid structured output may be repaired once; if repair fails, state must not advance.

## Entity: Agent Runtime State

Stores typed memory needed by the runner and Sales Inbox.

Fields:

- `conversation_id`
- `agent_key`
- `input_items`
- `context`
- `lead_facts`
- `diagnostic`
- `diagnostic_ledger`
- `waitlist`
- `demo`
- `human_status`
- `budget`
- `last_decision`
- `last_route`
- `last_opening_type`
- `asked_questions`
- `answered_direct_questions`
- `profile_name_status`
- `last_safe_state`
- `compact_summary`
- `product_source_version`
- `updated_at`

Rules:

- `input_items` follow the runner-compatible history shape.
- Context excludes secrets and private system prompts from public projections.
- Compact summary is used for cost control when the transcript grows.
- `last_decision` stores the structured behavior decision required by `behavior-contract.md`, including previous/current/next state, route, opening type, intents, direct-question status, diagnostic action, waitlist eligibility, profile-name usage, template IDs, facts used, next question kind, and policy checks.
- `asked_questions` prevents repeated diagnostic or qualification questions when the answer is already known.
- `diagnostic_ledger` is the authority for whether a diagnostic question has already been answered outside the formal diagnostic flow.
- `demo` stores whether demo was not offered, offered, viewed/asked, or reacted positive so diagnostic closing and waitlist eligibility can be validated.

## Entity: Conversation State

Represents the current commercial journey state.

Fields:

- `conversation_id`
- `previous_state`
- `current_state`
- `next_state`
- `transition_reason`
- `transition_evidence`
- `high_impact_transition`
- `validator_status`
- `updated_at`

Rules:

- State values and transitions must follow [conversation-state-contract.md](./conversation-state-contract.md).
- State guides the journey but does not replace LLM interpretation.
- High-impact transitions require validator approval before delivery or side effects.

## Entity: Message Template

Represents an approved official message block.

Fields:

- `template_id`
- `category`
- `allowed_states`
- `blocked_states`
- `supported_channels`
- `required_variables`
- `optional_variables`
- `product_source_requirements`
- `max_message_count`
- `max_chunk_length`
- `buttons_allowed`
- `official_links_allowed`

Rules:

- Templates are the official voice for mapped and semi-mapped behavior.
- The LLM selects template IDs and variables; the renderer creates final messages.
- Template variables must be grounded in lead facts or product knowledge.

## Entity: Template Render Plan

Represents the final channel-specific delivery plan.

Fields:

- `run_id`
- `conversation_id`
- `channel`
- `template_ids`
- `chunks`
- `buttons`
- `links`
- `typing_plan`
- `delay_plan`
- `validator_status`

Rules:

- Widget may render validated buttons or quick replies.
- WhatsApp must use text or official links instead of widget-only buttons.
- Both channels must avoid text walls and respect short-message delivery.

## Entity: Lead Facts

Represents structured facts learned from the lead.

Fields:

- `lead_id`
- `conversation_id`
- `agent_key`
- `person_name`
- `person_name_status`: `none`, `unverified`, `verified`, `rejected`
- `unverified_profile_name`
- `studio_name`
- `city`
- `state`
- `contact_path`
- `student_count`
- `current_tools`
- `main_pain`
- `priority`
- `urgency`
- `buying_intent`
- `demo_status`
- `demo_reaction`
- `confidence`
- `evidence_messages`

Rules:

- Name alone is weak identity evidence.
- WhatsApp phone and email are strong identity evidence.
- Only real person names may be stored as person names.
- WhatsApp profile names are unverified unless confirmed by the lead.
- Studio names, brands, handles, phone numbers, emojis, and generic strings must not be saved as person names.
- The agent must not ask for WhatsApp phone from WhatsApp leads.

## Entity: Product Knowledge Source

Versioned commercial truth.

Fields:

- `source_key`
- `version`
- `scope`: `taliya_commercial`
- `plans`
- `prices`
- `links`
- `demo_status`
- `waitlist_status`
- `checkout_status`
- `availability`
- `unsupported_claims`
- `last_reviewed_at`

Rules:

- Price, plan, link, demo, availability, waitlist, and checkout claims must trace to this source.
- Missing facts must produce honest uncertainty or human follow-up, not invention.

## Entity: Tool Call

Represents one model-selected tool invocation.

Fields:

- `id`
- `run_id`
- `conversation_id`
- `lead_id`
- `agent_key`
- `tool_name`
- `input`
- `output`
- `status`: `pending`, `succeeded`, `failed`, `skipped`
- `idempotency_key`
- `retry_count`
- `failure_reason`
- `created_at`
- `completed_at`

Rules:

- Side-effecting tools require idempotency keys.
- Tool output must be concise and safe to pass back into model context.

## Entity: Handoff Event

Represents agent-to-agent or agent-to-human handoff.

Fields:

- `id`
- `run_id`
- `conversation_id`
- `lead_id`
- `agent_key`
- `from_agent`
- `to_agent`
- `handoff_type`: `agent`, `human`
- `reason`
- `status`: `requested`, `accepted`, `active`, `resumed`, `cancelled`
- `created_at`

Rules:

- Human handoff makes automation pause until explicit resume.
- Agent handoffs update `current_agent_name`.

## Entity: Guardrail Event

Represents input/output guardrail result.

Fields:

- `id`
- `run_id`
- `conversation_id`
- `agent_key`
- `guardrail_name`
- `phase`: `input`, `tool`, `output`, `delivery`
- `status`: `passed`, `blocked`, `repaired`, `escalated`
- `reason`
- `evidence`
- `created_at`

Rules:

- Output guardrails run before channel delivery.
- Product-source violations are blocking failures.

## Entity: Diagnostic Record

Represents a useful commercial diagnostic.

Fields:

- `id`
- `conversation_id`
- `lead_id`
- `agent_key`
- `ledger`
- `facts_used`
- `main_bottleneck`
- `evidence`
- `likely_operational_cause`
- `first_organization_step`
- `crm_base_recommendation`
- `indicated_agents`: list of objects with `agent_name`, `pain_resolved`, `recommendation_reason`, and `practical_action`
- `recommended_plan_or_range`
- `final_plan_line`
- `demo_status_at_delivery`
- `final_demo_line`
- `confidence`: `high`, `medium`, `low`
- `unknowns`
- `validation_question`: optional internal or follow-up validation field; it must not replace `final_demo_line` and must not render as the standard completed-diagnostic close.
- `lead_validation`: `yes`, `no`, `unclear`
- `created_at`

Rules:

- Do not complete until all mandatory diagnostic ledger questions are answered, inferred from prior messages, or explicitly not applicable.
- Required unresolved diagnostic questions block completion and should produce a next question or clearly partial orientation instead of a completed diagnostic.
- Do not repeat a diagnostic question already answered with sufficient evidence.
- Do not pretend the lead shared facts that are not present.
- Render final diagnostic in staged order: pain/context, CRM base, operational step, agents/routines, plan, demo.
- The final plan line must use the approved dynamic "Pelo tamanho, momento..." meaning.
- The final demo line must match demo state.
- Do not use `validation_question` to append "Isso faz sentido..." or another generic validation close after the approved dynamic demo bridge.

## Entity: Demo Engagement

Represents demo offer, link/CTA rendering, and lead reaction.

Fields:

- `lead_id`
- `conversation_id`
- `agent_key`
- `status`: `not_offered`, `offered`, `viewed_or_asked`, `reacted_positive`
- `offered_at`
- `last_demo_link`
- `product_source_version`
- `channel_rendering`: `widget_cta`, `whatsapp_link`, `text_only`
- `lead_reaction`
- `reaction_evidence`
- `contributed_to_waitlist_eligibility`
- `updated_at`

Rules:

- Demo state controls the final diagnostic demo line.
- Demo curiosity alone cannot make waitlist eligible.
- Positive demo reaction contributes to waitlist eligibility only with clear next-step or contract intent.

## Entity: Waitlist Record

Represents qualified waitlist state.

Fields:

- `lead_id`
- `conversation_id`
- `agent_key`
- `status`: `not_offered`, `offered`, `pending_details`, `joined`, `declined`, `removed`
- `joined_at`
- `contact_path`
- `studio_name`
- `city`
- `state`
- `main_pain_summary`
- `diagnostic_summary`
- `plan_or_range`
- `priority`
- `contract_intent_evidence`
- `missing_fields`

Rules:

- Waitlist is not a checkout.
- Waitlist join must be idempotent.
- Waitlist can be offered only after clear intent to contract Taliya.

## Entity: Sales Inbox Projection

Represents the operator-facing lead record derived from runtime output.

Fields:

- identity fields from [sales-inbox-contract.md](./sales-inbox-contract.md)
- conversation fields from [sales-inbox-contract.md](./sales-inbox-contract.md)
- lead facts
- diagnostic ledger and result
- waitlist status and intent evidence
- product knowledge version and keys
- runtime/cost fields
- operator next action

Rules:

- Every meaningful turn must update this projection.
- Passing conversation evals without Sales Inbox completeness is not acceptable.

## Entity: Model Usage Record

Tracks model usage and cost.

Fields:

- `id`
- `run_id`
- `conversation_id`
- `agent_key`
- `operation`: `runner`, `guardrail`, `summary`, `judge`, `recovery`
- `model`
- `input_tokens`
- `output_tokens`
- `cached_input_tokens`
- `cost_usd`
- `budget_before`
- `budget_after`
- `cap_status`: `ok`, `review`, `hard_cap_blocked`
- `created_at`

Rules:

- Use provider-reported token usage when available.
- Heuristics can fill gaps only when clearly marked.

## Entity: Evaluation Scenario

Represents a reusable test scenario.

Fields:

- `scenario_id`
- `priority`
- `channel`
- `source`
- `messages`
- `expected_invariants`
- `judge_rubric`
- `blocking_failures`

## Entity: Evaluation Run

Represents one eval execution.

Fields:

- `run_id`
- `agent_key`
- `scenarios`
- `transcripts`
- `tool_calls`
- `handoffs`
- `guardrails`
- `usage`
- `judge_scores`
- `blocking_failures`
- `skipped_scenarios`
- `approved`
- `created_at`

Rules:

- Skipped scenarios cannot count as passed.
- Blocking failures fail the run regardless of judge average.

## Product-Followup Delta Data Additions

These additions support [product-followup-delta-contract.md](./product-followup-delta-contract.md) without changing the approved diagnostic, waitlist, handoff, or Sales Inbox core entities.

### Entity: Product Knowledge Fact Group

Add official fact groups to the existing product knowledge source:

- `how_it_works`
- `routine_areas`
- `whatsapp_scope`
- `integration_scope`
- `comparison_spreadsheet`
- `comparison_management_system`
- `security_and_data`
- `availability_and_onboarding`
- `out_of_profile`

Rules:

- Each group must be versioned with the product knowledge source.
- Missing groups must appear in `missing_facts` rather than being invented by the LLM.
- Runtime retrieval must be selective by topic.

### Entity: Post Diagnostic Context

Compact projection of a completed diagnostic for follow-up conversation.

Fields:

- `pain_context_human`
- `likely_cause`
- `first_recommended_step`
- `recommended_area`
- `indicated_agents`
- `recommended_plan_or_range`
- `demo_status`
- `waitlist_status`
- `unknowns`

Rules:

- Include only after diagnostic delivery.
- Populate only from saved diagnostic, demo, and waitlist state.
- Do not generate or infer new diagnostic facts for this projection.
- Use as LLM context for follow-up, not as a replacement for product knowledge.

### Entity: Product Follow-Up Signal

Optional operator-visible signal persisted for new product-followup routes.

Fields:

- `intent`: `product_how_it_works`, `comparison_current_tool`, `integration_scope_question`, `trust_security_question`, `out_of_profile`, `conversation_resume`, `general_objection`, or `diagnostic_refusal`
- `template_ids`
- `product_knowledge_keys`
- `grounded_facts`
- `guardrail_flags`
- `post_diagnostic_context_used`
- `created_at`

Rules:

- This signal must not duplicate the full transcript.
- It exists to make Sales Inbox and eval reports explain why a route was chosen.
- It must not store sensitive data beyond existing redaction rules.
