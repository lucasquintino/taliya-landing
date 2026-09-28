# Data Model: Floating AI Attendant

## FloatingAgentConfig

Represents niche-specific setup for the floating AI attendant.

Fields:

- `enabled`: whether the floating agent appears on the route.
- `label`: visible consultative title, e.g. "Consultor".
- `availability`: visible support text, e.g. "Atendimento 24h".
- `localeSignal`: visual/copy signal for Portuguese/Brazil.
- `avatar`: image path or initials used by the button and chat header.
- `greeting`: first assistant message.
- `quickReplies`: initial guided intents.
- `painOptions`: supported pains the agent can capture.
- `painToAgents`: mapping from pain IDs to primary agent IDs and explanation.
- `qualificationQuestions`: approved questions for name, WhatsApp, studio, location, active students and biggest pain.
- `conversionCtas`: destinations and labels for guided demo, plans page, checkout/subscription intent, analysis/Dinheiro na Mesa and human WhatsApp assistance.
- `guidedDemoAvailability`: whether the real SaaS demo environment is ready to receive visitors.
- `commercialConfigRef`: reference to the trusted system configuration for plans, prices, recommended plan and checkout destinations.
- `commercialGoal`: default sales goal, e.g. selling the configured recommended/highest-value plan for broad or multi-agent needs.
- `fallbackMessages`: safe responses for unsupported, unsafe, off-topic or provider-failure states.

Validation:

- Must not include prohibited public terms.
- Must map every supported pain to at least one primary agent.
- Must keep custom agent as an expansion option, not a primary agent.
- Must not expose unconfigured pricing or unsupported checkout promises.
- Must read pricing, plan recommendations and checkout URLs from trusted system configuration.
- Must not duplicate plan prices in prompt text or component defaults.
- Must not frame lower plans as equal default recommendations when the configured recommended/highest-value plan fits the visitor's need.
- Must offer guided-demo CTA only when `guidedDemoAvailability` confirms the real SaaS demo environment is available.

## CommercialSystemConfig

Represents the trusted business configuration that the landing and AI attendant share.

Fields:

- `campaignStage`
- `publicOfferMode`
- `plans`: configured plan list with IDs, names, prices, recommended flag and checkout destinations
- `humanWhatsAppAssistance`: trusted destination and label
- `analysisDestination`: trusted anchor, route or form state
- `copyBoundaries`: prohibited and preferred public terms

Validation:

- The AI attendant can answer price questions only from this configuration.
- Checkout and WhatsApp destinations must never come from user input, model output or query strings.
- If plan configuration changes, the agent behavior must update without prompt edits.
- The configured recommended/highest-value plan is the default recommendation for broad operational pain, multi-agent needs or complete-system intent.
- Lower plans are comparison, budget-fit or narrow-scope options unless configuration marks them as recommended.

## ConversationSession

Represents one visitor's active chat state.

Fields:

- `sessionId`: anonymous session identifier.
- `channel`: `web` or `whatsapp`.
- `channelSessionId`: optional channel-specific session/contact identifier.
- `entryPath`: `widget`, `consultor_cta`, `whatsapp_cta`, `guided_demo`, `plans_page`, `diagnostic_cta` or `custom_agent_diagnostic`.
- `niche`: landing niche.
- `sourcePage`: route path.
- `campaignStage`: internal campaign stage.
- `publicOfferMode`: visitor-facing offer mode.
- `status`: `minimized`, `open`, `qualifying`, `handoffReady`, `fallback` or `closed`.
- `messages`: ordered `AiAttendantMessage` list.
- `selectedPainIds`: captured pains.
- `recommendedAgentIds`: agents recommended during the conversation.
- `qualification`: optional `QualificationProfile`.
- `handoff`: optional `ConversionHandoff`.
- `conversionPath`: optional `guided_demo`, `view_plans`, `plan_recommendation`, `checkout_intent`, `subscription_intent`, `analysis_request`, `human_whatsapp_assist`, `custom_agent_follow_up`, `crm_agent_diagnostic`, `custom_agent_diagnostic_mapped`, `mixed_subscription_plus_custom` or `custom_agent_diagnostic_unclear`.
- `crmAgentDiagnostic`: optional CRM-first diagnostic state including studio size, pains, daily visibility, replacement complexity, sales follow-up maturity, current system, priority goal, buying timing, lead temperature, recommended CRM modules, recommended agents, recommended plan and next step.
- `commercialGoal`: optional `sell_recommended_plan`, `compare_plans`, `budget_fit` or `assisted_close`.
- `planDisplayGateReason`: optional reason that allowed routing to plans.
- `checkoutGateReason`: optional reason that allowed checkout.
- `guidedDemoContext`: optional selected scenario, selected pain and completed steps.
- `riskReducersCovered`: optional list of risk reducers answered before checkout.
- `interestedPlanId`: optional configured plan discussed or selected during the conversation.
- `externalContact`: optional channel contact context such as WhatsApp phone or provider contact ID.
- `providerMessageIds`: optional set/list used by WhatsApp to prevent duplicate inbound processing.
- `optOutState`: whether the contact opted out of automated WhatsApp replies.
- `lastEventAt`: timestamp for rate-limit and duplicate-event protection.

State transitions:

- `minimized` -> `open` when the visitor opens the widget.
- `open` -> `qualifying` when the visitor shows analysis, human assistance or custom-agent follow-up intent.
- `qualifying` -> `handoffReady` when required qualification is captured or skipped.
- Any active state -> `fallback` when the agent cannot continue safely.
- Any active state -> `closed` when the visitor closes the panel.
- Any WhatsApp active state -> `closed` or `optedOut` when the contact asks to stop receiving messages.

Validation:

- `entryPath` must be present when the session starts from a landing CTA or guided demo.
- `entryPath=widget` must use a neutral opening.
- `entryPath=consultor_cta` or `entryPath=whatsapp_cta` may use direct commercial copy.
- `entryPath=guided_demo` must preserve demo context when available.
- `entryPath=diagnostic_cta` must start the CRM-first diagnostic flow, not the Agente sob medida report mode.
- `entryPath=widget` with `sourceSection=faq_doubt_cta` must use the normal neutral widget opening while acknowledging the visitor may have a remaining FAQ doubt.
- `entryPath=custom_agent_diagnostic` must preserve diagnostic report context and route by classification.
- `checkoutGateReason` must exist before checkout is offered.
- `planDisplayGateReason` must exist before plans are proactively routed.

## CustomAgentDiagnosticReport

Represents the one-shot report generated by the Agente sob medida landing block.

Fields:

- `reportId`: stable diagnostic report ID.
- `sessionId`: visitor/session ID when available.
- `niche`: landing niche.
- `sourcePage`: route path.
- `sourceSection`: `custom_agent_diagnostic` or `final_diagnostic_cta`.
- `description`: visitor-provided operation description, stored only where retention policy allows.
- `classification`: `mapped_solution`, `custom_agent`, `mixed_solution` or `unclear`.
- `confidence`: `high`, `medium` or `low`.
- `sections`: structured visitor-facing report sections.
- `mappedAgentIds`: existing Taliya agents that cover the request when applicable.
- `customAgent`: optional label, operation summary and missing scope questions.
- `recommendedPlanId`: configured plan recommendation when the request is already covered and enough context exists.
- `ctas`: report CTAs with destination and diagnostic context variant.
- `leadEffect`: conversion path, priority and safe summary for Sales Inbox/n8n.
- `guardrailDecision`: safety classification.
- `createdAt`: timestamp.

Validation:

- Must not route directly to checkout.
- Must classify mapped existing operations as SaaS funnel, not Agente sob medida.
- Must classify unmapped operations as custom-agent proposal funnel, not a public-plan entitlement.
- Must not include unconfigured prices, unsupported integrations, unsupported timelines or arbitrary URLs.
- Must not store unnecessary raw text in analytics, n8n or Sales Inbox summaries when a safe summary is enough.

## DiagnosticContextVariant

Represents the opening mode used when a report CTA opens consultor or WhatsApp.

Values:

- `diagnostic_existing_solution`: the report found Taliya already covers the request.
- `diagnostic_custom_agent`: the report found an unmapped custom-agent opportunity.
- `diagnostic_mixed_solution`: the report found both mapped SaaS work and custom work.
- `diagnostic_unclear`: the report needs more detail before recommending.

Validation:

- Existing-solution variants may offer consultor, guided demo when ready/gated and WhatsApp continuation.
- Custom-agent variants must ask for operation details before asking contact.
- Mixed variants must not imply Agente sob medida is included in public plans.
- Unclear variants must ask for clarification before recommending a plan or custom proposal.

## ConversationChannel

Represents the channel-specific envelope around the same AI attendant core.

Fields:

- `channel`: `web` or `whatsapp`.
- `capabilities`: supported actions such as `renderQuickReplies`, `sendTextReply`, `handoffToForm` or `handoffToFollowUp`.
- `sessionKey`: stable key for the channel session.
- `replyPolicy`: whether automatic replies are allowed for this turn.
- `source`: `landing_widget` or messaging provider name.

Validation:

- Web sessions may remain client-local until handoff.
- WhatsApp sessions must be persisted server-side before an assistant reply is sent.
- WhatsApp automatic replies are allowed only for inbound or explicitly opted-in conversations.
- Proactive campaigns, broadcasts and cold outbound are not valid channel actions in v1.
- Production WhatsApp sessions must not use in-memory storage.

## WhatsAppConversation

Represents a persisted WhatsApp conversation owned by the backend.

Fields:

- `channelSessionId`: stable backend session ID.
- `provider`: configured WhatsApp messaging provider.
- `providerContactId`: provider contact identifier.
- `phone`: normalized or safely stored phone number when available.
- `status`: `active`, `handoffReady`, `optedOut`, `providerFailed` or `closed`.
- `lastProviderMessageId`: most recent inbound provider message ID.
- `processedProviderMessageIds`: IDs already processed for idempotency.
- `messages`: recent safe conversation history used for context.
- `qualification`: optional `QualificationProfile`.
- `selectedPainIds`: captured pains.
- `recommendedAgentIds`: recommended agents.
- `optedInAt`: timestamp if explicit opt-in exists.
- `optedOutAt`: timestamp if the contact asks to stop.
- `lastReplyAt`: timestamp for rate limiting.

Validation:

- Duplicate provider message IDs must not produce duplicate assistant replies.
- Opted-out conversations must not receive automated follow-up replies.
- Raw provider payloads should not be persisted unless redacted and required for debugging.
- Provider for v1 is Meta WhatsApp Cloud API.

## AiAttendantMessage

Represents a user or assistant message.

Fields:

- `id`: message identifier.
- `channel`: optional channel where the message happened.
- `providerMessageId`: optional WhatsApp provider message ID for inbound/outbound delivery tracking.
- `role`: `user`, `assistant` or `system`.
- `content`: visible message text.
- `createdAt`: timestamp.
- `intent`: optional detected intent such as `explain_product`, `select_pain`, `ask_pricing`, `guided_demo`, `view_plans`, `plan_recommendation`, `checkout_intent`, `analysis_interest`, `human_whatsapp_assist`, `unsafe_request`.
- `quickReplies`: optional next choices.
- `guardrailDecision`: optional safety classification.

Validation:

- Assistant content must use approved product claims.
- User messages should be trimmed and length-limited.
- Sensitive details should not be echoed back unless necessary for the visitor's immediate understanding.

## QualificationProfile

Represents business context the visitor voluntarily provides.

Fields:

- `name`: visitor name.
- `whatsapp`: contact phone or WhatsApp.
- `studioName`: studio name.
- `cityState`: city and state.
- `activeStudentsRange`: range, not exact requirement.
- `biggestPain`: captured pain.
- `currentSystem`: optional current system usage.
- `customRoutine`: optional routine they want an agent to handle.
- `contactPreference`: optional email or cellphone/WhatsApp preference for custom-agent follow-up.
- `preferredNextStep`: guided demo, plan comparison, checkout after recommendation, analysis, WhatsApp follow-up or continue chat.
- `preferredConversionPath`: guided demo, plan comparison, checkout/subscription intent, analysis request, human WhatsApp assistance, custom-agent follow-up or continue chat.

Validation:

- Must not require sensitive student health details.
- Must not require payment credentials.
- WhatsApp format should be friendly and tolerant, not blocking useful leads with overly strict masks.

## AgentRecommendation

Represents how the AI attendant connects a visitor pain to the product.

Fields:

- `painId`: captured pain.
- `agentIds`: one or more primary agents.
- `explanation`: short visitor-facing explanation.
- `exampleAction`: concrete action the agent would help with.
- `nextQuestion`: consultative follow-up question.

Validation:

- Agent IDs must be one of the seven primary agents.
- Explanation must stay Pilates-specific.
- No unsupported guarantees.

## ConversionHandoff

Represents context passed from the chat or diagnostic report to the guided demo, plans page, checkout path, analysis flow, human WhatsApp assistance or custom-agent follow-up.

Fields:

- `sessionId`: source conversation.
- `channel`: `web` or `whatsapp`.
- `channelSessionId`: optional channel session/contact identifier.
- `conversionPath`: `guided_demo`, `view_plans`, `plan_recommendation`, `checkout_intent`, `subscription_intent`, `analysis_request`, `human_whatsapp_assist`, `custom_agent_follow_up`, `custom_agent_diagnostic_mapped`, `mixed_subscription_plus_custom` or `custom_agent_diagnostic_unclear`.
- `entryPath`: source entry path for the conversation or handoff.
- `summary`: concise conversation summary.
- `selectedPainIds`: pains discussed.
- `recommendedAgentIds`: agents recommended.
- `recommendedPlanId`: configured plan recommended by the consultor when available.
- `planDisplayGateReason`: reason plans were allowed.
- `checkoutGateReason`: reason checkout was allowed.
- `guidedDemoContext`: selected demo scenario, selected pain and completed steps when available.
- `diagnosticReportId`: optional report identifier when the handoff came from the Agente sob medida diagnostic block.
- `diagnosticClassification`: optional `mapped_solution`, `custom_agent`, `mixed_solution` or `unclear`.
- `diagnosticContextVariant`: optional `diagnostic_existing_solution`, `diagnostic_custom_agent`, `diagnostic_mixed_solution` or `diagnostic_unclear`.
- `diagnosticSelectedCta`: optional CTA selected from the diagnostic report.
- `customAgentSummary`: optional safe summary of the unmapped/custom operation.
- `mappedAgentIds`: optional agent IDs the report identified as already covered by Taliya.
- `sourceSection`: optional source section such as `faq_doubt_cta` when the handoff started from a contextual CTA.
- `riskReducersCovered`: risk reducers already answered.
- `qualification`: captured profile.
- `calculatorEstimate`: optional value from landing calculator.
- `destination`: checkout, plan selection, analysis form anchor, form state or follow-up channel.
- `checkout`: optional trusted checkout or plan-selection destination.
- `selectedPlanId`: selected or interested plan when available.
- `consentContext`: optional consent/opt-in state when available.
- `humanHandoffStatus`: optional `requested`, `sent_to_whatsapp`, `human_takeover_pending`, `human_takeover_active` or `closed`.
- `createdAt`: timestamp.

Validation:

- Must include `niche`, `sourcePage`, `campaignStage` and `publicOfferMode` through the session context.
- Must not include sensitive unnecessary data.
- Must not include payment credentials, card data or client-asserted subscription state.
- Must not allow checkout handoff without `checkoutGateReason`.
- Must not allow a diagnostic report CTA to route directly to checkout.
- Plan/demo/checkout metadata may help tracking and onboarding context, but must not determine billing price, entitlement or paid access.
- Human WhatsApp handoff must use safe summaries rather than full raw transcripts by default.

## ConsentContext

Represents privacy/consent state relevant to contact capture or WhatsApp handoff.

Fields:

- `contactPurpose`: guided demo follow-up, plan recommendation, checkout support, analysis, human WhatsApp assistance or custom-agent follow-up.
- `privacyCopyShown`: whether privacy/consent copy was shown before contact capture.
- `privacyNoticeUrl`: optional configured policy URL.
- `whatsappOptIn`: whether the visitor initiated or agreed to WhatsApp contact when known.
- `whatsappOptOut`: whether the contact opted out.
- `capturedAt`: timestamp.

Validation:

- Contact details should not be requested before a valid purpose exists.
- Opt-out must stop automated WhatsApp replies.
- Consent context does not override billing, legal or payment requirements.

## LeadRecord

Represents one operator-visible sales opportunity created from the web chat, WhatsApp, guided demo, plan-comparison intent, analysis request, human WhatsApp assistance request, custom-agent follow-up or checkout/subscription intent.

Fields:

- `leadId`: stable lead identifier.
- `sessionId`: source conversation session.
- `channel`: web or whatsapp.
- `channelSessionId`: optional channel contact/session identifier.
- `sourcePage`: landing route or WhatsApp source.
- `status`: ai_active, handoff_requested, human_active, waiting_customer, follow_up_scheduled, checkout_sent, won, lost or do_not_contact.
- `priority`: alta, media or baixa.
- `conversionPath`: guided_demo, view_plans, plan_recommendation, checkout_intent, subscription_intent, analysis_request, human_whatsapp_assist, custom_agent_follow_up or high_intent.
- `selectedPlanId`: selected or interested configured plan when available.
- `selectedPainIds`: captured pains.
- `recommendedAgentIds`: recommended agents.
- `qualification`: captured profile fields when provided.
- `customAgentInterest`: safe summary of the requested unmapped operation when applicable.
- `summary`: concise safe summary.
- `nextAction`: operator-facing next step.
- `consentContext`: consent/opt-in/opt-out state when available.
- `lastEventName`: last event that updated the record.
- `idempotencyKey`: key used to prevent duplicate records.
- `createdAt`
- `updatedAt`

Validation:

- The operator must be able to view all lead records in one configured source of truth.
- Sales Inbox status is canonical; optional external mirrors must derive from this same status taxonomy instead of using a separate pipeline status list.
- Custom-agent interest must be represented by `conversionPath`, `customAgentInterest` and `nextAction`, not by a separate lead status.
- Checkout/subscription intent does not equal subscribed status; trusted billing confirmation is required.
- Duplicate WhatsApp webhooks or repeated handoff events must update the same lead rather than create duplicates.
- Lead records must not store raw full transcripts by default.
- Sensitive student health/payment data must not be stored in lead summaries.

## InternalSalesInbox

Represents the protected operator surface used to control the SaaS operator's own commercial leads before the full SaaS product exists.

Fields:

- `inboxId`
- `name`
- `scope`: `saas_sales_leads`
- `allowedOperatorRoleIds`
- `defaultFilters`
- `createdAt`
- `updatedAt`

Validation:

- Scope is only SaaS sales leads, not paying-studio student conversations.
- Must require authenticated internal operator/admin access.
- Must not expose provider or integration secrets to the browser.

## SalesLeadConversation

Represents the real-time internal conversation/control record shown in the Sales Inbox.

Fields:

- `leadId`: stable sales lead identifier.
- `primarySessionId`: primary web or WhatsApp session.
- `webSessionIds`: associated widget sessions.
- `whatsappSessionIds`: associated WhatsApp sessions.
- `normalizedWhatsapp`: safe normalized WhatsApp when available.
- `email`: normalized email when available.
- `studioName`: studio name when available.
- `status`: `ai_active`, `handoff_requested`, `human_active`, `waiting_customer`, `follow_up_scheduled`, `checkout_sent`, `won`, `lost` or `do_not_contact`.
- `priority`: alta, media or baixa.
- `channels`: web, whatsapp or both.
- `sourcePages`: landing/plans pages involved.
- `conversionPaths`: guided_demo, view_plans, plan_recommendation, checkout_intent, subscription_intent, analysis_request, human_whatsapp_assist, custom_agent_follow_up or high_intent.
- `interestedPlanId`: configured plan when available.
- `selectedPainIds`
- `recommendedAgentIds`
- `qualification`
- `customAgentInterest`
- `safeSummary`
- `recentMessages`: recent operational messages needed by the operator.
- `nextAction`
- `followUpAt`
- `aiPaused`: whether AI replies are paused for the lead/session.
- `lastActivityAt`
- `externalSyncStatus`: synced, pending, failed or skipped for optional external automations.
- `createdAt`
- `updatedAt`

Validation:

- The Sales Inbox is the real-time control surface and reporting/pipeline destination for v1.
- `won` does not mean paid subscription unless Spec 3 confirms billing status separately.
- Message history should be limited to operationally useful recent messages and safe summaries.
- Payment credentials and billing documents must never be stored.

## LeadMergeDecision

Represents how multiple channel sessions are joined or kept separate.

Fields:

- `decisionId`
- `candidateLeadIds`
- `candidateSessionIds`
- `decision`: merge, keep_separate or needs_operator_review
- `reason`
- `strongSignals`: whatsapp, email, leadId, sessionId
- `weakSignals`: studioName, sourcePage, browser, timing
- `actor`: system or operator
- `createdAt`

Validation:

- WhatsApp match, email match, explicit `leadId` and explicit `sessionId` are strong signals.
- Studio name, IP, browser fingerprint or timing alone must not auto-merge.
- Ambiguous matches must require operator review or remain separate.

## OperatorAction

Represents an authenticated internal action taken from the Sales Inbox.

Fields:

- `actionId`
- `leadId`
- `sessionId`
- `actorUserId`
- `action`: `take_over`, `send_whatsapp_message`, `send_plan_page`, `send_checkout_link`, `schedule_follow_up`, `resume_ai`, `mark_waiting_customer`, `mark_won`, `mark_lost`, `mark_do_not_contact` or `edit_lead_summary`.
- `payload`: safe action-specific metadata.
- `beforeStatus`
- `afterStatus`
- `createdAt`

Validation:

- Requires internal operator/admin authorization.
- WhatsApp sends must go through the server-side provider adapter.
- Plan-page and checkout links must come from trusted configuration.
- Checkout sent does not activate or confirm payment.

## OperatorAuditEvent

Represents the immutable audit trail for Sales Inbox control.

Fields:

- `auditId`
- `leadId`
- `actorUserId`
- `action`
- `before`
- `after`
- `safeMetadata`
- `createdAt`

Validation:

- Required for takeover, reply, resume AI, checkout link send, status changes, summary edits and do-not-contact.
- Must not include provider secrets, payment credentials or full raw transcripts by default.

## SubscriptionHandoff

Represents a high-intent visitor being routed to plan selection or checkout.

Fields:

- `planId`: optional configured plan identifier.
- `checkoutUrl`: trusted checkout or plan-selection URL.
- `ctaLabel`: approved CTA label.
- `sourceSessionId`: source conversation session.
- `selectedPainIds`: pains discussed before the visitor chose to subscribe.
- `recommendedAgentIds`: agents recommended before checkout.

Validation:

- The URL must come from trusted configuration, not model-generated text.
- The agent must not claim access is active until trusted billing confirmation exists.
- The agent must never ask for card details inside chat or WhatsApp.

## GuardrailDecision

Represents the safety classification for a user message or generated reply.

Fields:

- `category`: `allowed`, `prompt_injection`, `unsupported_claim`, `sensitive_data`, `off_topic`, `abuse`, `provider_failure`.
- `action`: `respond`, `refuse`, `redirect`, `fallback` or `handoff`.
- `reason`: short internal reason.
- `visibleMessage`: approved visitor-facing response when needed.

Validation:

- Refusals should be brief and return to studio operations when possible.
- Prompt-injection and internal-detail requests must never expose instructions.

## FloatingAgentTrackingEvent

Represents analytics emitted by the widget.

Fields:

- `niche`
- `sourcePage`
- `campaignStage`
- `publicOfferMode`
- `channel`
- `eventName`
- `metadata`

Required event names:

- `floating_agent_opened`
- `floating_agent_closed`
- `floating_agent_message_sent`
- `floating_agent_quick_reply_clicked`
- `floating_agent_pain_captured`
- `floating_agent_agent_recommended`
- `floating_agent_qualification_started`
- `floating_agent_guided_demo_cta`
- `floating_agent_plan_recommendation_cta`
- `floating_agent_checkout_cta`
- `floating_agent_analysis_handoff`
- `floating_agent_human_whatsapp_handoff`
- `floating_agent_diagnostic_handoff`
- `floating_agent_fallback`
- `floating_agent_whatsapp_inbound`
- `floating_agent_whatsapp_reply_sent`
- `floating_agent_whatsapp_delivery_failed`

Validation:

- Every event must include landing context.
- Every event must include channel.
- Metadata must avoid full sensitive message dumps.
- WhatsApp metadata should use provider message IDs and safe contact identifiers rather than full raw payloads.

## AiUsageEvent

Represents server-side usage/cost telemetry for the AI attendant.

Fields:

- `id`
- `sessionId`
- `channel`
- `niche`
- `provider`
- `model`
- `status`: success, fallback, guardrail_blocked, timeout, provider_error or rate_limited
- `inputTokenCount`: when provider returns it
- `outputTokenCount`: when provider returns it
- `estimatedCost`: when calculable
- `latencyMs`
- `idempotencyKey`: required for WhatsApp retries
- `createdAt`

Validation:

- Must be created server-side.
- Must not rely on client counters.
- Must not store full raw transcripts by default.
- Retries must be idempotent so usage is not double-counted.
