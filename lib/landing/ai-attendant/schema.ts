import type { CampaignStage, PublicOfferMode } from "@/data/landing/niches/types";

export type AiAttendantChannel = "web" | "whatsapp";

export type AiAttendantRole =
  | "receptionist"
  | "product_explainer"
  | "pain_diagnostician"
  | "agent_mapper"
  | "objection_handler"
  | "value_translator"
  | "qualification_collector"
  | "conversion_closer"
  | "handoff_summarizer"
  | "safety_gatekeeper"
  | "context_aware_guide"
  | "fallback_operator";

export type AiAttendantIntent =
  | "answer_question"
  | "pain_detected"
  | "agent_explained"
  | "qualification_started"
  | "view_plans"
  | "guided_demo"
  | "plan_recommendation"
  | "checkout_intent"
  | "analysis_handoff"
  | "human_whatsapp_handoff"
  | "waitlist_intent"
  | "crm_agent_diagnostic"
  | "custom_agent_follow_up"
  | "custom_agent_diagnostic_request"
  | "faq_doubt_cta"
  | "guardrail"
  | "fallback";

export type ConversionPath =
  | "cold_lead"
  | "view_plans"
  | "guided_demo"
  | "plan_recommendation"
  | "checkout_intent"
  | "waitlist_intent"
  | "analysis_request"
  | "human_whatsapp_assist"
  | "crm_agent_diagnostic"
  | "custom_agent_follow_up"
  | "custom_agent_diagnostic_mapped"
  | "mixed_subscription_plus_custom"
  | "custom_agent_diagnostic_unclear";

export type DiagnosticClassification = "mapped_solution" | "custom_agent" | "mixed_solution" | "unclear";

export type DiagnosticContextVariant =
  | "diagnostic_existing_solution"
  | "diagnostic_custom_agent"
  | "diagnostic_mixed_solution"
  | "diagnostic_unclear";

export type CommercialStage =
  | "awaiting_name"
  | "awaiting_pain_or_intent"
  | "diagnostic_offered"
  | "diagnostic_in_progress"
  | "diagnostic_completed"
  | "recommendation_validation"
  | "demo_offered"
  | "demo_seen"
  | "waitlist_eligible"
  | "waitlist_offered"
  | "waitlist_pending_details"
  | "waitlist_joined"
  | "waitlist_declined"
  | "human_handoff";

export type WaitlistStatus = "not_offered" | "eligible" | "offered" | "pending_details" | "joined" | "declined" | "undecided";

export type DiagnosticStatus = "not_started" | "offered" | "in_progress" | "completed" | "declined";

export type DemoStatus = "not_offered" | "offered" | "unavailable" | "viewed_discussed" | "positive" | "negative";

export type ConversationClosureState =
  | "waiting_user"
  | "cold_closed"
  | "waitlist_joined"
  | "waitlist_declined"
  | "human_active"
  | "error_needs_attention";

export type GuardrailCategory =
  | "allowed"
  | "prompt_injection"
  | "unsupported_claim"
  | "sensitive_data"
  | "off_topic"
  | "abuse"
  | "provider_failure"
  | "invalid_model_output"
  | "rate_limited";

export type GuardrailDecision = {
  category: GuardrailCategory;
  action: "respond" | "refuse" | "redirect" | "fallback" | "handoff";
  reason: string;
  visibleMessage?: string;
};

export type AiAttendantMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  intent?: AiAttendantIntent;
  action?: {
    label: string;
    href: string;
  };
};

export type QualificationDraft = {
  name?: string;
  whatsapp?: string;
  email?: string;
  studioName?: string;
  cityState?: string;
  activeStudentsRange?: string;
  biggestPain?: string;
  currentSystem?: string;
  customRoutine?: string;
  contactPreference?: string;
  preferredNextStep?: string;
  diagnosticType?: string;
  diagnosticAskedFields?: string;
  diagnosticCompleted?: string;
  diagnosticCancelled?: string;
  diagnosticAdaptiveAsked?: string;
  studioSizeRange?: string;
  operationalPains?: string;
  crmPainAreas?: string;
  agentPainAreas?: string;
  dailyVisibility?: string;
  replacementComplexity?: string;
  salesFollowupMaturity?: string;
  priorityGoal?: string;
  buyingTiming?: string;
  leadTemperature?: string;
  recommendedCrmModules?: string;
  recommendedAgents?: string;
  recommendedPlan?: string;
  diagnosticSummary?: string;
  diagnosticNextStep?: string;
  contactCaptureStatus?: string;
  commercialStage?: CommercialStage;
  waitlistStatus?: WaitlistStatus;
  waitlistOfferedAt?: string;
  waitlistJoinedAt?: string;
  waitlistDeclinedAt?: string;
  diagnosticStatus?: DiagnosticStatus;
  diagnosticCompletedAt?: string;
  demoStatus?: DemoStatus;
  demoOfferedAt?: string;
  demoSeenAt?: string;
  leadSourceChannel?: "widget" | "whatsapp";
  leadSourceDetail?: string;
  primaryPainOrIntent?: string;
  nextAction?: string;
  studioCity?: string;
  missingWaitlistFields?: string;
  humanActive?: string;
  aiPaused?: string;
  closureState?: ConversationClosureState;
  funnelEvents?: string;
  agentV2State?: string;
  agentV2TraceId?: string;
  agentV2CostEstimateUsd?: string;
  agentV2ProductSourceVersion?: string;
  agentV2Priority?: string;
  agentRuntimeRunId?: string;
  agentRuntimeContractVersion?: string;
  agentRuntimeTraceId?: string;
  agentRuntimeCurrentAgent?: string;
  agentRuntimeCurrentState?: string;
  agentRuntimePreviousState?: string;
  agentRuntimeNextState?: string;
  agentRuntimeRoute?: string;
  agentRuntimeDetectedIntents?: string;
  agentRuntimeTemplateIds?: string;
  agentRuntimeDiagnosticLedgerStatus?: string;
  agentRuntimeDemoStatus?: string;
  agentRuntimeDemoNextStep?: string;
  agentRuntimeFinalPlanLine?: string;
  agentRuntimeFinalDemoLine?: string;
  agentRuntimeCrmBaseRecommendation?: string;
  agentRuntimeAgentRecommendations?: string;
  agentRuntimeGuardrailFlags?: string;
  agentRuntimeWaitlistIntentEvidence?: string;
  agentRuntimeProductSourceKeys?: string;
  agentRuntimeLatestProductFollowupIntent?: string;
  agentRuntimePostDiagnosticContextUsed?: string;
  agentRuntimeUnsupportedFactRequested?: string;
  agentRuntimeHumanConfirmationOffered?: string;
  agentRuntimeDiagnosticRefusalRespected?: string;
  agentRuntimeCostEstimateUsd?: string;
  agentRuntimeProductSourceVersion?: string;
};

export type AiAttendantSession = {
  leadId?: string;
  sessionId: string;
  channel: AiAttendantChannel;
  channelSessionId?: string;
  entryPath?: "widget" | "consultor_cta" | "whatsapp_cta" | "guided_demo" | "plans_page" | "diagnostic_cta" | "custom_agent_diagnostic" | "unknown";
  sourceSection?: string;
  niche: string;
  sourcePage: string;
  campaignStage: CampaignStage;
  publicOfferMode: PublicOfferMode;
  messages: AiAttendantMessage[];
  selectedPainIds?: string[];
  recommendedAgentIds?: string[];
  qualificationDraft?: QualificationDraft;
  externalContact?: {
    type: "whatsapp";
    phone?: string;
    providerContactId?: string;
    providerMessageId?: string;
    phoneNumberId?: string;
    displayPhoneNumber?: string;
    optedOut?: boolean;
  };
};

export type AiAttendantRequest = {
  session: AiAttendantSession;
  userMessage?: string;
  quickReplyId?: string;
  metadata?: Record<string, unknown>;
  pageSignals?: {
    selectedPainId?: string;
    selectedAgentId?: string;
    calculatorEstimate?: number;
    aiRouteIntent?: string;
    aiRouteShouldStartDiagnostic?: string;
  };
};

export type AgentRecommendation = {
  painId: string;
  agentIds: string[];
  painSummary?: string;
  explanation: string;
  exampleAction: string;
  nextQuestion?: string;
};

export type ConversionHandoff = {
  sessionId: string;
  channel: AiAttendantChannel;
  channelSessionId?: string;
  niche: string;
  sourcePage: string;
  campaignStage: CampaignStage;
  publicOfferMode: PublicOfferMode;
  conversionPath: ConversionPath;
  summary: string;
  selectedPainIds: string[];
  recommendedAgentIds: string[];
  qualification: QualificationDraft;
  calculatorEstimate?: number;
  destination: "checkout" | "plan_selection" | "guided_demo" | "analysis_form" | "whatsapp_follow_up" | "custom_agent_follow_up" | "waitlist_follow_up";
  selectedPlanId?: string;
  checkout?: {
    planId?: string;
    url?: string;
  };
  consentContext?: {
    contactPurpose: ConversionPath;
    privacyCopyShown: boolean;
    privacyNoticeUrl?: string;
    whatsappOptIn?: boolean;
    whatsappOptOut?: boolean;
  };
  humanHandoffStatus?: "requested" | "sent_to_whatsapp" | "human_takeover_pending" | "human_takeover_active" | "closed";
  diagnosticClassification?: DiagnosticClassification;
  diagnosticContextVariant?: DiagnosticContextVariant;
};

export type AiAttendantResponse = {
  assistantMessages: AiAttendantMessage[];
  capturedPainIds: string[];
  recommendedAgentIds: string[];
  recommendations?: AgentRecommendation[];
  nextQuestion?: string;
  conversionPath?: ConversionPath;
  subscription?: {
    planId?: string;
    checkoutUrl?: string;
    ctaLabel: string;
  };
  shouldOfferDiagnostic: boolean;
  qualificationPatch?: QualificationDraft;
  handoff?: ConversionHandoff;
  guardrailDecision: GuardrailDecision;
  diagnosticClassification?: DiagnosticClassification;
  diagnosticContextVariant?: DiagnosticContextVariant;
  diagnosticReportId?: string;
  selectedDiagnosticCtaId?: string;
};

const MAX_MESSAGE_LENGTH = 1200;
const MAX_HISTORY_LENGTH = 16;
let assistantMessageCounter = 0;

export const aiAttendantResponseJsonSchema = {
  type: "object",
  additionalProperties: false,
  required: [
    "assistantMessages",
    "capturedPainIds",
    "recommendedAgentIds",
    "shouldOfferDiagnostic",
    "guardrailDecision",
  ],
  properties: {
    assistantMessages: {
      type: "array",
      minItems: 1,
      maxItems: 3,
      items: {
        type: "object",
        additionalProperties: false,
        required: ["id", "role", "content", "intent"],
        properties: {
          id: { type: "string" },
          role: { type: "string", enum: ["assistant"] },
          content: { type: "string" },
          action: {
            type: "object",
            additionalProperties: false,
            required: ["label", "href"],
            properties: {
              label: { type: "string" },
              href: { type: "string" },
            },
          },
          intent: {
            type: "string",
            enum: [
              "answer_question",
              "pain_detected",
              "agent_explained",
              "qualification_started",
              "view_plans",
              "guided_demo",
              "plan_recommendation",
              "checkout_intent",
              "analysis_handoff",
              "human_whatsapp_handoff",
              "waitlist_intent",
              "crm_agent_diagnostic",
              "custom_agent_follow_up",
              "custom_agent_diagnostic_request",
              "faq_doubt_cta",
              "guardrail",
              "fallback",
            ],
          },
        },
      },
    },
    capturedPainIds: { type: "array", items: { type: "string" } },
    recommendedAgentIds: { type: "array", items: { type: "string" } },
    recommendations: {
      type: "array",
      items: {
        type: "object",
        additionalProperties: false,
        required: ["painId", "agentIds", "explanation", "exampleAction"],
        properties: {
          painId: { type: "string" },
          agentIds: { type: "array", items: { type: "string" } },
          painSummary: { type: "string" },
          explanation: { type: "string" },
          exampleAction: { type: "string" },
          nextQuestion: { type: "string" },
        },
      },
    },
    nextQuestion: { type: "string" },
    conversionPath: {
      type: "string",
      enum: [
        "view_plans",
        "guided_demo",
        "plan_recommendation",
        "checkout_intent",
        "waitlist_intent",
        "analysis_request",
        "human_whatsapp_assist",
        "crm_agent_diagnostic",
        "custom_agent_follow_up",
        "custom_agent_diagnostic_mapped",
        "mixed_subscription_plus_custom",
        "custom_agent_diagnostic_unclear",
      ],
    },
    subscription: {
      type: "object",
      additionalProperties: false,
      required: ["ctaLabel"],
      properties: {
        planId: { type: "string" },
        checkoutUrl: { type: "string" },
        ctaLabel: { type: "string" },
      },
    },
    shouldOfferDiagnostic: { type: "boolean" },
    qualificationPatch: {
      type: "object",
      additionalProperties: { type: "string" },
    },
    guardrailDecision: {
      type: "object",
      additionalProperties: false,
      required: ["category", "action", "reason"],
      properties: {
        category: {
          type: "string",
          enum: [
            "allowed",
            "prompt_injection",
            "unsupported_claim",
            "sensitive_data",
            "off_topic",
            "abuse",
            "provider_failure",
            "invalid_model_output",
            "rate_limited",
          ],
        },
        action: { type: "string", enum: ["respond", "refuse", "redirect", "fallback", "handoff"] },
        reason: { type: "string" },
        visibleMessage: { type: "string" },
      },
    },
    diagnosticClassification: {
      type: "string",
      enum: ["mapped_solution", "custom_agent", "mixed_solution", "unclear"],
    },
    diagnosticContextVariant: {
      type: "string",
      enum: ["diagnostic_existing_solution", "diagnostic_custom_agent", "diagnostic_mixed_solution", "diagnostic_unclear"],
    },
    diagnosticReportId: { type: "string" },
    selectedDiagnosticCtaId: { type: "string" },
  },
} as const;

export function parseAiAttendantRequest(input: unknown): { ok: true; value: AiAttendantRequest } | { ok: false; error: string } {
  if (!isRecord(input)) return { ok: false, error: "Request body must be an object." };
  if (!isRecord(input.session)) return { ok: false, error: "Missing session." };

  const session = input.session;
  const userMessage = typeof input.userMessage === "string" ? input.userMessage.trim() : undefined;
  const quickReplyId = typeof input.quickReplyId === "string" ? input.quickReplyId.trim() : undefined;

  if (!userMessage && !quickReplyId) return { ok: false, error: "Message or quick reply is required." };
  if (userMessage && userMessage.length > MAX_MESSAGE_LENGTH) return { ok: false, error: "Message is too long." };
  if (typeof session.sessionId !== "string" || !session.sessionId) return { ok: false, error: "Invalid session id." };
  if (session.channel !== "web" && session.channel !== "whatsapp") return { ok: false, error: "Invalid channel." };
  if (typeof session.niche !== "string" || !session.niche) return { ok: false, error: "Invalid niche." };
  if (typeof session.sourcePage !== "string" || !session.sourcePage) return { ok: false, error: "Invalid source page." };

  return {
    ok: true,
    value: {
      session: {
        leadId: typeof session.leadId === "string" ? session.leadId : undefined,
        sessionId: session.sessionId,
        channel: session.channel,
        channelSessionId: typeof session.channelSessionId === "string" ? session.channelSessionId : undefined,
        entryPath: parseEntryPath(session.entryPath),
        sourceSection: typeof session.sourceSection === "string" ? session.sourceSection.slice(0, 80) : undefined,
        niche: session.niche,
        sourcePage: session.sourcePage,
        campaignStage: session.campaignStage === "commercial" ? "commercial" : "commercial",
        publicOfferMode: session.publicOfferMode === "direct_saas_subscription" ? "direct_saas_subscription" : "direct_saas_subscription",
        messages: parseMessages(session.messages).slice(-MAX_HISTORY_LENGTH),
        selectedPainIds: parseStringArray(session.selectedPainIds),
        recommendedAgentIds: parseStringArray(session.recommendedAgentIds),
        qualificationDraft: isRecord(session.qualificationDraft) ? mapStringRecord(session.qualificationDraft) : undefined,
        externalContact: parseExternalContact(session.externalContact),
      },
      userMessage,
      quickReplyId,
      pageSignals: parsePageSignals(input.pageSignals),
    },
  };
}

function parseEntryPath(input: unknown): AiAttendantSession["entryPath"] {
  if (
    input === "widget" ||
    input === "consultor_cta" ||
    input === "whatsapp_cta" ||
    input === "guided_demo" ||
    input === "plans_page" ||
    input === "diagnostic_cta" ||
    input === "custom_agent_diagnostic" ||
    input === "unknown"
  ) {
    return input;
  }

  return undefined;
}

export function normalizeAiAttendantResponse(input: unknown): AiAttendantResponse | null {
  if (!isRecord(input)) return null;
  const assistantMessages = Array.isArray(input.assistantMessages)
    ? input.assistantMessages
        .filter(isRecord)
        .map((message, index) => ({
          id: typeof message.id === "string" ? message.id : `assistant_${Date.now()}_${index}`,
          role: "assistant" as const,
          content: typeof message.content === "string" ? message.content.slice(0, 900) : "",
          intent: isIntent(message.intent) ? message.intent : "answer_question",
          action: parseMessageAction(message.action),
        }))
        .filter((message) => message.content)
        .slice(0, 3)
    : [];

  if (!assistantMessages.length) return null;

  const guardrailDecision = isRecord(input.guardrailDecision)
    ? {
        category: isGuardrailCategory(input.guardrailDecision.category) ? input.guardrailDecision.category : "allowed",
        action: isGuardrailAction(input.guardrailDecision.action) ? input.guardrailDecision.action : "respond",
        reason: typeof input.guardrailDecision.reason === "string" ? input.guardrailDecision.reason : "Model response",
        visibleMessage: typeof input.guardrailDecision.visibleMessage === "string" ? input.guardrailDecision.visibleMessage : undefined,
      }
    : ({ category: "allowed", action: "respond", reason: "Model response" } satisfies GuardrailDecision);

  return {
    assistantMessages,
    capturedPainIds: parseStringArray(input.capturedPainIds),
    recommendedAgentIds: parseStringArray(input.recommendedAgentIds),
    recommendations: parseRecommendations(input.recommendations),
    nextQuestion: typeof input.nextQuestion === "string" ? input.nextQuestion : undefined,
    conversionPath: isConversionPath(input.conversionPath) ? input.conversionPath : undefined,
    subscription: parseSubscription(input.subscription),
    shouldOfferDiagnostic: Boolean(input.shouldOfferDiagnostic),
    qualificationPatch: isRecord(input.qualificationPatch) ? mapStringRecord(input.qualificationPatch) : undefined,
    guardrailDecision,
    diagnosticClassification: isDiagnosticClassification(input.diagnosticClassification) ? input.diagnosticClassification : undefined,
    diagnosticContextVariant: isDiagnosticContextVariant(input.diagnosticContextVariant) ? input.diagnosticContextVariant : undefined,
    diagnosticReportId: typeof input.diagnosticReportId === "string" ? input.diagnosticReportId.slice(0, 80) : undefined,
    selectedDiagnosticCtaId: typeof input.selectedDiagnosticCtaId === "string" ? input.selectedDiagnosticCtaId.slice(0, 80) : undefined,
  };
}

export function createAssistantMessage(content: string, intent: AiAttendantIntent = "answer_question"): AiAttendantMessage {
  assistantMessageCounter = (assistantMessageCounter + 1) % 100000;
  return {
    id: `assistant_${Date.now()}_${assistantMessageCounter}`,
    role: "assistant",
    content,
    intent,
  };
}

export function createAssistantActionMessage(
  content: string,
  intent: AiAttendantIntent,
  action: { label: string; href: string },
): AiAttendantMessage {
  return {
    ...createAssistantMessage(content, intent),
    action,
  };
}

function parseMessages(input: unknown): AiAttendantMessage[] {
  if (!Array.isArray(input)) return [];
  return input.filter(isRecord).flatMap((message, index) => {
    if (message.role !== "user" && message.role !== "assistant") return [];
    if (typeof message.content !== "string" || !message.content.trim()) return [];
    return [
      {
        id: typeof message.id === "string" ? message.id : `${message.role}_${index}`,
        role: message.role,
        content: message.content.trim().slice(0, MAX_MESSAGE_LENGTH),
        intent: isIntent(message.intent) ? message.intent : undefined,
        action: parseMessageAction(message.action),
      },
    ];
  });
}

function parseMessageAction(input: unknown): AiAttendantMessage["action"] {
  if (!isRecord(input)) return undefined;
  if (typeof input.label !== "string" || typeof input.href !== "string") return undefined;
  const label = input.label.trim().slice(0, 80);
  const href = input.href.trim();
  if (!label || !/^https?:\/\//.test(href)) return undefined;
  return { label, href };
}

function parsePageSignals(input: unknown): AiAttendantRequest["pageSignals"] {
  if (!isRecord(input)) return undefined;
  return {
    selectedPainId: typeof input.selectedPainId === "string" ? input.selectedPainId : undefined,
    selectedAgentId: typeof input.selectedAgentId === "string" ? input.selectedAgentId : undefined,
    calculatorEstimate: typeof input.calculatorEstimate === "number" ? input.calculatorEstimate : undefined,
    aiRouteIntent: typeof input.aiRouteIntent === "string" ? input.aiRouteIntent : undefined,
    aiRouteShouldStartDiagnostic: typeof input.aiRouteShouldStartDiagnostic === "string" ? input.aiRouteShouldStartDiagnostic : undefined,
  };
}

function parseExternalContact(input: unknown): AiAttendantSession["externalContact"] {
  if (!isRecord(input) || input.type !== "whatsapp") return undefined;
  return {
    type: "whatsapp",
    phone: typeof input.phone === "string" ? input.phone : undefined,
    providerContactId: typeof input.providerContactId === "string" ? input.providerContactId : undefined,
    providerMessageId: typeof input.providerMessageId === "string" ? input.providerMessageId : undefined,
    phoneNumberId: typeof input.phoneNumberId === "string" ? input.phoneNumberId : undefined,
    displayPhoneNumber: typeof input.displayPhoneNumber === "string" ? input.displayPhoneNumber : undefined,
    optedOut: Boolean(input.optedOut),
  };
}

function parseRecommendations(input: unknown): AgentRecommendation[] | undefined {
  if (!Array.isArray(input)) return undefined;
  const recommendations = input.filter(isRecord).flatMap((item) => {
    if (typeof item.painId !== "string" || typeof item.explanation !== "string" || typeof item.exampleAction !== "string") return [];
    return [
      {
        painId: item.painId,
        agentIds: parseStringArray(item.agentIds),
        painSummary: typeof item.painSummary === "string" ? item.painSummary : undefined,
        explanation: item.explanation,
        exampleAction: item.exampleAction,
        nextQuestion: typeof item.nextQuestion === "string" ? item.nextQuestion : undefined,
      },
    ];
  });
  return recommendations.length ? recommendations : undefined;
}

function parseSubscription(input: unknown): AiAttendantResponse["subscription"] {
  if (!isRecord(input) || typeof input.ctaLabel !== "string") return undefined;
  return {
    planId: typeof input.planId === "string" ? input.planId : undefined,
    checkoutUrl: typeof input.checkoutUrl === "string" ? input.checkoutUrl : undefined,
    ctaLabel: input.ctaLabel,
  };
}

function parseStringArray(input: unknown): string[] {
  return Array.isArray(input) ? input.filter((item): item is string => typeof item === "string") : [];
}

function mapStringRecord(input: Record<string, unknown>): Record<string, string> {
  return Object.fromEntries(Object.entries(input).filter((entry): entry is [string, string] => typeof entry[1] === "string"));
}

function isRecord(input: unknown): input is Record<string, unknown> {
  return typeof input === "object" && input !== null;
}

function isIntent(input: unknown): input is AiAttendantIntent {
  return (
    input === "answer_question" ||
    input === "pain_detected" ||
    input === "agent_explained" ||
    input === "qualification_started" ||
    input === "view_plans" ||
    input === "guided_demo" ||
    input === "plan_recommendation" ||
    input === "checkout_intent" ||
    input === "analysis_handoff" ||
    input === "human_whatsapp_handoff" ||
    input === "waitlist_intent" ||
    input === "crm_agent_diagnostic" ||
    input === "custom_agent_follow_up" ||
    input === "custom_agent_diagnostic_request" ||
    input === "faq_doubt_cta" ||
    input === "guardrail" ||
    input === "fallback"
  );
}

function isConversionPath(input: unknown): input is ConversionPath {
  return (
    input === "view_plans" ||
    input === "guided_demo" ||
    input === "plan_recommendation" ||
    input === "checkout_intent" ||
    input === "waitlist_intent" ||
    input === "analysis_request" ||
    input === "human_whatsapp_assist" ||
    input === "crm_agent_diagnostic" ||
    input === "custom_agent_follow_up" ||
    input === "custom_agent_diagnostic_mapped" ||
    input === "mixed_subscription_plus_custom" ||
    input === "custom_agent_diagnostic_unclear"
  );
}

function isDiagnosticClassification(input: unknown): input is DiagnosticClassification {
  return input === "mapped_solution" || input === "custom_agent" || input === "mixed_solution" || input === "unclear";
}

function isDiagnosticContextVariant(input: unknown): input is DiagnosticContextVariant {
  return (
    input === "diagnostic_existing_solution" ||
    input === "diagnostic_custom_agent" ||
    input === "diagnostic_mixed_solution" ||
    input === "diagnostic_unclear"
  );
}

function isGuardrailCategory(input: unknown): input is GuardrailCategory {
  return (
    input === "allowed" ||
    input === "prompt_injection" ||
    input === "unsupported_claim" ||
    input === "sensitive_data" ||
    input === "off_topic" ||
    input === "abuse" ||
    input === "provider_failure" ||
    input === "invalid_model_output" ||
    input === "rate_limited"
  );
}

function isGuardrailAction(input: unknown): input is GuardrailDecision["action"] {
  return input === "respond" || input === "refuse" || input === "redirect" || input === "fallback" || input === "handoff";
}
