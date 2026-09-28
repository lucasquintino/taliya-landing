import type { NicheLandingConfig } from "@/data/landing/niches/types";
import type {
  AiAttendantRequest,
  AiAttendantResponse,
  CommercialStage,
  ConversionHandoff,
  ConversionPath,
  ConversationClosureState,
  DemoStatus,
  DiagnosticStatus,
  QualificationDraft,
  WaitlistStatus,
} from "./schema";

export type LeadStatus =
  | "ai_active"
  | "handoff_requested"
  | "human_active"
  | "waiting_customer"
  | "follow_up_scheduled"
  | "checkout_sent"
  | "won"
  | "lost"
  | "do_not_contact";

export type LeadPriority = "hot" | "warm" | "cold" | "manual";

export type LeadReadiness =
  | "curious"
  | "diagnosing"
  | "proof_needed"
  | "plan_ready"
  | "waitlist_ready"
  | "checkout_ready"
  | "assisted_close"
  | "custom_agent_mapping";

export type LeadRecord = {
  leadId: string;
  sessionId: string;
  channel: "web" | "whatsapp";
  channelSessionId?: string;
  entryPath: string;
  sourceSection?: string;
  sourcePage: string;
  status: LeadStatus;
  priority: LeadPriority;
  urgency: "alta" | "media" | "baixa";
  readiness: LeadReadiness;
  conversionPath: ConversionPath;
  commercialStage: CommercialStage;
  waitlistStatus: WaitlistStatus;
  waitlistOfferedAt?: string;
  waitlistJoinedAt?: string;
  waitlistDeclinedAt?: string;
  diagnosticStatus: DiagnosticStatus;
  diagnosticCompletedAt?: string;
  demoStatus: DemoStatus;
  demoOfferedAt?: string;
  demoSeenAt?: string;
  leadSourceChannel: "widget" | "whatsapp";
  leadSourceDetail?: string;
  primaryPainOrIntent?: string;
  missingWaitlistFields?: string;
  closureState: ConversationClosureState;
  humanActive: boolean;
  lastMessageAt: string;
  selectedPlanId?: string;
  recommendedPlanId: string;
  selectedPainIds: string[];
  recommendedAgentIds: string[];
  qualification: QualificationDraft;
  contact: {
    name?: string;
    whatsapp?: string;
    email?: string;
    providerContactId?: string;
    phoneNumberId?: string;
    displayPhoneNumber?: string;
    normalizedWhatsapp?: string;
  };
  customAgentInterest?: string;
  diagnosticClassification?: string;
  diagnosticContextVariant?: string;
  diagnosticReportId?: string;
  selectedDiagnosticCtaId?: string;
  crmAgentDiagnostic?: {
    diagnosticType?: string;
    studioSizeRange?: string;
    operationalPains?: string;
    crmPainAreas?: string;
    agentPainAreas?: string;
    dailyVisibility?: string;
    replacementComplexity?: string;
    salesFollowupMaturity?: string;
    currentSystem?: string;
    priorityGoal?: string;
    buyingTiming?: string;
    leadTemperature?: string;
    recommendedCrmModules?: string;
    recommendedAgents?: string;
    recommendedPlan?: string;
    diagnosticSummary?: string;
    nextStep?: string;
    contactCaptureStatus?: string;
  };
  agentV2?: {
    macroState?: string;
    traceId?: string;
    productSourceVersion?: string;
    estimatedCostUsd?: number;
    priority?: string;
  };
  agentRuntime?: {
    currentAgent?: string;
    previousState?: string;
    currentState?: string;
    nextState?: string;
    route?: string;
    detectedIntents?: string;
    templateIds?: string;
    diagnosticLedgerStatus?: string;
    demoStatus?: string;
    demoNextStep?: string;
    finalPlanLine?: string;
    finalDemoLine?: string;
    crmBaseRecommendation?: string;
    agentRecommendations?: string;
    guardrailFlags?: string;
    waitlistIntentEvidence?: string;
    productSourceKeys?: string;
    latestProductFollowupIntent?: string;
    postDiagnosticContextUsed?: boolean;
    unsupportedFactRequested?: string;
    humanConfirmationOffered?: boolean;
    diagnosticRefusalRespected?: boolean;
    traceId?: string;
    runId?: string;
    productSourceVersion?: string;
    estimatedCostUsd?: number;
    productSourceWarning?: string;
  };
  summary: string;
  nextAction: string;
  consentContext: ConversionHandoff["consentContext"];
  lastEventName: string;
  idempotencyKey: string;
  merge: {
    strongIdentifiers: string[];
    weakIdentifiers: string[];
    autoMergeAllowed: boolean;
  };
  createdAt: string;
  updatedAt: string;
};

export function createLeadRecord({
  config: _config,
  eventName,
  handoff,
  request,
  response,
}: {
  config: NicheLandingConfig;
  eventName: string;
  handoff: ConversionHandoff;
  request: AiAttendantRequest;
  response: AiAttendantResponse;
}): LeadRecord {
  const now = new Date().toISOString();
  const qualification = {
    ...(request.session.qualificationDraft ?? {}),
    ...(response.qualificationPatch ?? {}),
  };
  const normalizedWhatsapp = normalizePhone(qualification.whatsapp ?? request.session.externalContact?.phone);
  const strongIdentifiers = buildStrongIdentifiers(request, qualification, normalizedWhatsapp);
  const weakIdentifiers = buildWeakIdentifiers(request, qualification, response);
  const conversionPath = handoff.conversionPath;
  const priority = calculateLeadPriority(conversionPath, response, qualification, request);
  const urgency = calculateLeadUrgency(priority, qualification);
  const readiness = calculateLeadReadiness(conversionPath);
  const leadId = request.session.leadId ?? createStableLeadId(strongIdentifiers, request.session.sessionId);
  const commercialState = deriveCommercialState(conversionPath, qualification, request, response);
  const hasCompletedDiagnostic = qualification.diagnosticStatus === "completed";
  const recommendedPlanId = hasCompletedDiagnostic ? planIdFromRecommendation(qualification.recommendedPlan) : undefined;
  void _config;

  return {
    leadId,
    sessionId: request.session.sessionId,
    channel: request.session.channel,
    channelSessionId: request.session.channelSessionId,
    entryPath: request.session.entryPath ?? "unknown",
    sourceSection: request.session.sourceSection,
    sourcePage: request.session.sourcePage,
    status: statusFromConversionPath(conversionPath, request),
    priority,
    urgency,
    readiness,
    conversionPath,
    ...commercialState,
    selectedPlanId: handoff.selectedPlanId ?? response.subscription?.planId ?? recommendedPlanId,
    recommendedPlanId: recommendedPlanId ?? "not_recommended_yet",
    selectedPainIds: unique([...(handoff.selectedPainIds ?? []), ...(response.capturedPainIds ?? [])]),
    recommendedAgentIds: unique([...(handoff.recommendedAgentIds ?? []), ...(response.recommendedAgentIds ?? [])]),
    qualification,
    contact: {
      name: qualification.name,
      whatsapp: qualification.whatsapp ?? request.session.externalContact?.phone,
      email: qualification.email,
      providerContactId: request.session.externalContact?.providerContactId,
      phoneNumberId: request.session.externalContact?.phoneNumberId,
      displayPhoneNumber: request.session.externalContact?.displayPhoneNumber,
      normalizedWhatsapp,
    },
    customAgentInterest:
      conversionPath === "custom_agent_follow_up" || conversionPath === "mixed_subscription_plus_custom"
        ? qualification.customRoutine ?? response.qualificationPatch?.customRoutine ?? handoff.summary
        : undefined,
    diagnosticClassification: response.diagnosticClassification ?? handoff.diagnosticClassification,
    diagnosticContextVariant: response.diagnosticContextVariant ?? handoff.diagnosticContextVariant,
    diagnosticReportId: response.diagnosticReportId,
    selectedDiagnosticCtaId: response.selectedDiagnosticCtaId,
    crmAgentDiagnostic: extractCrmAgentDiagnostic(qualification, conversionPath),
    agentV2: extractAgentV2(qualification) ?? extractAgentRuntimeAsLegacyPanel(qualification),
    agentRuntime: extractAgentRuntime(qualification, response),
    summary: leadSummaryFromQualification(qualification, handoff.summary),
    nextAction: qualification.nextAction ?? nextActionFor(conversionPath, readiness, commercialState.waitlistStatus),
    consentContext: handoff.consentContext,
    lastEventName: eventName,
    idempotencyKey: createIdempotencyKey(request, conversionPath),
    merge: {
      strongIdentifiers,
      weakIdentifiers,
      autoMergeAllowed: strongIdentifiers.length > 0,
    },
    createdAt: now,
    updatedAt: now,
  };
}

function extractAgentRuntime(qualification: QualificationDraft, response: AiAttendantResponse): LeadRecord["agentRuntime"] {
  if (!qualification.agentRuntimeTraceId && !qualification.agentRuntimeRunId && !qualification.agentRuntimeCurrentAgent) return undefined;
  const productSourceVersion = qualification.agentRuntimeProductSourceVersion;
  const hasProductLikeIntent =
    response.conversionPath === "view_plans" ||
    response.subscription ||
    response.assistantMessages.some((message) => /\bR\$|plano|preco|preço|demo|demonstra|lista de espera/i.test(message.content));
  return {
    currentAgent: qualification.agentRuntimeCurrentAgent,
    previousState: qualification.agentRuntimePreviousState,
    currentState: qualification.agentRuntimeCurrentState,
    nextState: qualification.agentRuntimeNextState,
    route: qualification.agentRuntimeRoute,
    detectedIntents: qualification.agentRuntimeDetectedIntents,
    templateIds: qualification.agentRuntimeTemplateIds,
    diagnosticLedgerStatus: qualification.agentRuntimeDiagnosticLedgerStatus,
    demoStatus: qualification.agentRuntimeDemoStatus,
    demoNextStep: qualification.agentRuntimeDemoNextStep,
    finalPlanLine: qualification.agentRuntimeFinalPlanLine,
    finalDemoLine: qualification.agentRuntimeFinalDemoLine,
    crmBaseRecommendation: qualification.agentRuntimeCrmBaseRecommendation,
    agentRecommendations: qualification.agentRuntimeAgentRecommendations,
    guardrailFlags: qualification.agentRuntimeGuardrailFlags,
    waitlistIntentEvidence: qualification.agentRuntimeWaitlistIntentEvidence,
    productSourceKeys: qualification.agentRuntimeProductSourceKeys,
    latestProductFollowupIntent: qualification.agentRuntimeLatestProductFollowupIntent,
    postDiagnosticContextUsed: parseBooleanString(qualification.agentRuntimePostDiagnosticContextUsed),
    unsupportedFactRequested: qualification.agentRuntimeUnsupportedFactRequested,
    humanConfirmationOffered: parseBooleanString(qualification.agentRuntimeHumanConfirmationOffered),
    diagnosticRefusalRespected: parseBooleanString(qualification.agentRuntimeDiagnosticRefusalRespected),
    traceId: qualification.agentRuntimeTraceId,
    runId: qualification.agentRuntimeRunId,
    productSourceVersion,
    estimatedCostUsd: Number(qualification.agentRuntimeCostEstimateUsd) || undefined,
    productSourceWarning: hasProductLikeIntent && !productSourceVersion ? "missing_product_source_version" : undefined,
  };
}

function extractAgentRuntimeAsLegacyPanel(qualification: QualificationDraft): LeadRecord["agentV2"] {
  if (!qualification.agentRuntimeTraceId && !qualification.agentRuntimeCurrentAgent) return undefined;
  return {
    macroState: qualification.agentRuntimeCurrentAgent,
    traceId: qualification.agentRuntimeTraceId,
    productSourceVersion: qualification.agentRuntimeProductSourceVersion,
    estimatedCostUsd: Number(qualification.agentRuntimeCostEstimateUsd) || undefined,
    priority: undefined,
  };
}

function parseBooleanString(value?: string) {
  if (value === "true") return true;
  if (value === "false") return false;
  return undefined;
}

function extractAgentV2(qualification: QualificationDraft): LeadRecord["agentV2"] {
  if (!qualification.agentV2State && !qualification.agentV2TraceId && !qualification.agentV2CostEstimateUsd) return undefined;
  let macroState: string | undefined;
  try {
    const parsed = qualification.agentV2State ? JSON.parse(qualification.agentV2State) : undefined;
    macroState = typeof parsed?.macroState === "string" ? parsed.macroState : undefined;
  } catch {
    macroState = undefined;
  }
  return {
    macroState,
    traceId: qualification.agentV2TraceId,
    productSourceVersion: qualification.agentV2ProductSourceVersion,
    estimatedCostUsd: Number(qualification.agentV2CostEstimateUsd) || undefined,
    priority: qualification.agentV2Priority,
  };
}

function calculateLeadPriority(
  conversionPath: ConversionPath,
  response: AiAttendantResponse,
  qualification: QualificationDraft,
  request: AiAttendantRequest,
): LeadPriority {
  if (conversionPath === "human_whatsapp_assist" || qualification.humanActive === "true" || qualification.humanActive === "requested") return "manual";
  if (qualification.closureState === "error_needs_attention") return "manual";
  if (conversionPath === "cold_lead") return "cold";
  if (conversionPath === "waitlist_intent") return qualification.waitlistStatus === "joined" ? "hot" : "warm";
  if (conversionPath === "crm_agent_diagnostic") {
    if (qualification.leadTemperature === "hot") return "hot";
    if (qualification.diagnosticStatus === "completed" && hasHighUrgencySignal(qualification)) return "hot";
    if (
      qualification.leadTemperature === "warm" ||
      hasContact(request) ||
      qualification.diagnosticStatus === "completed" ||
      response.capturedPainIds.length ||
      response.recommendedAgentIds.length
    ) {
      return "warm";
    }
    return "cold";
  }
  if (conversionPath === "checkout_intent") return "hot";
  if (conversionPath === "plan_recommendation") return "hot";
  if (conversionPath === "custom_agent_follow_up" && (qualification.whatsapp || qualification.email || qualification.contactPreference)) return "hot";
  if (conversionPath === "mixed_subscription_plus_custom") return "hot";
  if (
    conversionPath === "guided_demo" ||
    conversionPath === "view_plans" ||
    conversionPath === "analysis_request" ||
    conversionPath === "custom_agent_follow_up" ||
    conversionPath === "custom_agent_diagnostic_mapped"
  ) {
    return "warm";
  }
  if (response.recommendedAgentIds.length || qualification.whatsapp || qualification.email) return "warm";
  return "cold";
}

function calculateLeadUrgency(priority: LeadPriority, qualification: QualificationDraft): LeadRecord["urgency"] {
  if (hasHighUrgencySignal(qualification)) return "alta";
  if (priority === "manual" || priority === "hot") return "alta";
  if (priority === "warm") return "media";
  return "baixa";
}

function hasHighUrgencySignal(qualification: QualificationDraft) {
  const normalized = normalizeText(
    [
      qualification.buyingTiming,
      qualification.leadTemperature,
      qualification.diagnosticSummary,
      qualification.priorityGoal,
      qualification.nextAction,
    ]
      .filter(Boolean)
      .join(" "),
  );
  return /\b(agora|urgente|urgencia|esse mes|este mes|perdendo|perder|dinheiro|prejuizo)\b/.test(normalized);
}

function calculateLeadReadiness(conversionPath: ConversionPath): LeadReadiness {
  if (conversionPath === "cold_lead") return "curious";
  if (conversionPath === "checkout_intent") return "checkout_ready";
  if (conversionPath === "waitlist_intent") return "waitlist_ready";
  if (conversionPath === "human_whatsapp_assist") return "assisted_close";
  if (conversionPath === "plan_recommendation" || conversionPath === "view_plans") return "plan_ready";
  if (conversionPath === "crm_agent_diagnostic") return "plan_ready";
  if (conversionPath === "custom_agent_diagnostic_mapped") return "plan_ready";
  if (conversionPath === "guided_demo") return "proof_needed";
  if (conversionPath === "custom_agent_follow_up" || conversionPath === "mixed_subscription_plus_custom") return "custom_agent_mapping";
  if (conversionPath === "analysis_request") return "diagnosing";
  return "curious";
}

function statusFromConversionPath(conversionPath: ConversionPath, request: AiAttendantRequest): LeadStatus {
  if (conversionPath === "waitlist_intent") return "waiting_customer";
  if (conversionPath === "human_whatsapp_assist") return "handoff_requested";
  if (conversionPath === "custom_agent_follow_up" || conversionPath === "mixed_subscription_plus_custom") return hasContact(request) ? "handoff_requested" : "ai_active";
  return "ai_active";
}

function deriveCommercialState(
  conversionPath: ConversionPath,
  qualification: QualificationDraft,
  request: AiAttendantRequest,
  response: AiAttendantResponse,
): Pick<
  LeadRecord,
  | "commercialStage"
  | "waitlistStatus"
  | "waitlistOfferedAt"
  | "waitlistJoinedAt"
  | "waitlistDeclinedAt"
  | "diagnosticStatus"
  | "diagnosticCompletedAt"
  | "demoStatus"
  | "demoOfferedAt"
  | "demoSeenAt"
  | "leadSourceChannel"
  | "leadSourceDetail"
  | "primaryPainOrIntent"
  | "missingWaitlistFields"
  | "closureState"
  | "humanActive"
  | "lastMessageAt"
> {
  const waitlistStatus = normalizeWaitlistStatus(qualification.waitlistStatus, conversionPath);
  return {
    commercialStage: normalizeCommercialStage(qualification.commercialStage, conversionPath, response),
    waitlistStatus,
    waitlistOfferedAt: qualification.waitlistOfferedAt,
    waitlistJoinedAt: qualification.waitlistJoinedAt,
    waitlistDeclinedAt: qualification.waitlistDeclinedAt,
    diagnosticStatus: normalizeDiagnosticStatus(qualification.diagnosticStatus, qualification),
    diagnosticCompletedAt: qualification.diagnosticCompletedAt,
    demoStatus: normalizeDemoStatus(qualification.demoStatus),
    demoOfferedAt: qualification.demoOfferedAt,
    demoSeenAt: qualification.demoSeenAt,
    leadSourceChannel: qualification.leadSourceChannel ?? (request.session.channel === "whatsapp" ? "whatsapp" : "widget"),
    leadSourceDetail:
      qualification.leadSourceDetail ??
      [request.session.entryPath, request.session.sourceSection, request.session.sourcePage].filter(Boolean).join(":").slice(0, 180),
    primaryPainOrIntent: firstNonEmpty([
      qualification.primaryPainOrIntent,
      qualification.operationalPains,
      qualification.biggestPain,
      qualification.priorityGoal,
      response.capturedPainIds.join(", "),
    ]),
    missingWaitlistFields: qualification.missingWaitlistFields,
    closureState: deriveClosureState(conversionPath, qualification, response),
    humanActive: qualification.humanActive === "true" || qualification.humanActive === "requested" || conversionPath === "human_whatsapp_assist",
    lastMessageAt: new Date().toISOString(),
  };
}

function normalizeCommercialStage(
  input: QualificationDraft["commercialStage"],
  conversionPath: ConversionPath,
  response: AiAttendantResponse,
): CommercialStage {
  if (isCommercialStage(input)) return input;
  if (conversionPath === "cold_lead") return "awaiting_pain_or_intent";
  if (conversionPath === "waitlist_intent") return response.qualificationPatch?.waitlistStatus === "joined" ? "waitlist_joined" : "waitlist_offered";
  if (conversionPath === "crm_agent_diagnostic") return "recommendation_validation";
  if (conversionPath === "guided_demo") return "demo_offered";
  if (conversionPath === "human_whatsapp_assist") return "human_handoff";
  return "diagnostic_completed";
}

function normalizeWaitlistStatus(input: QualificationDraft["waitlistStatus"], conversionPath: ConversionPath): WaitlistStatus {
  if (isWaitlistStatus(input)) return input;
  return conversionPath === "waitlist_intent" ? "offered" : "not_offered";
}

function normalizeDiagnosticStatus(input: QualificationDraft["diagnosticStatus"], qualification: QualificationDraft): DiagnosticStatus {
  if (isDiagnosticStatus(input)) return input;
  if (qualification.diagnosticCompleted === "true") return "completed";
  if (qualification.diagnosticType === "crm_agent_diagnostic") return "in_progress";
  return "not_started";
}

function normalizeDemoStatus(input: QualificationDraft["demoStatus"]): DemoStatus {
  return isDemoStatus(input) ? input : "not_offered";
}

function deriveClosureState(
  conversionPath: ConversionPath,
  qualification: QualificationDraft,
  response: AiAttendantResponse,
): ConversationClosureState {
  if (qualification.closureState) return qualification.closureState;
  if (qualification.waitlistStatus === "joined") return "waitlist_joined";
  if (qualification.waitlistStatus === "declined") return "waitlist_declined";
  if (conversionPath === "human_whatsapp_assist" || qualification.humanActive === "true" || qualification.humanActive === "requested") return "human_active";
  if (response.guardrailDecision.category === "rate_limited") return "error_needs_attention";
  return "waiting_user";
}

function isCommercialStage(input: unknown): input is CommercialStage {
  return (
    input === "awaiting_name" ||
    input === "awaiting_pain_or_intent" ||
    input === "diagnostic_offered" ||
    input === "diagnostic_in_progress" ||
    input === "diagnostic_completed" ||
    input === "recommendation_validation" ||
    input === "demo_offered" ||
    input === "demo_seen" ||
    input === "waitlist_eligible" ||
    input === "waitlist_offered" ||
    input === "waitlist_pending_details" ||
    input === "waitlist_joined" ||
    input === "waitlist_declined" ||
    input === "human_handoff"
  );
}

function isWaitlistStatus(input: unknown): input is WaitlistStatus {
  return (
    input === "not_offered" ||
    input === "eligible" ||
    input === "offered" ||
    input === "pending_details" ||
    input === "joined" ||
    input === "declined" ||
    input === "undecided"
  );
}

function isDiagnosticStatus(input: unknown): input is DiagnosticStatus {
  return input === "not_started" || input === "offered" || input === "in_progress" || input === "completed" || input === "declined";
}

function isDemoStatus(input: unknown): input is DemoStatus {
  return input === "not_offered" || input === "offered" || input === "unavailable" || input === "viewed_discussed" || input === "positive" || input === "negative";
}

function nextActionFor(conversionPath: ConversionPath, readiness: LeadReadiness, waitlistStatus?: WaitlistStatus) {
  if (conversionPath === "cold_lead") return "Lead frio iniciou conversa; acompanhar se demonstrar dor, diagnóstico, demo ou lista de espera.";
  if (conversionPath === "waitlist_intent") {
    if (waitlistStatus === "joined") return "Studio entrou na lista de espera; chamar quando houver próxima janela.";
    if (waitlistStatus === "pending_details") return "Coletar dados pendentes para confirmar lista de espera.";
    if (waitlistStatus === "declined") return "Tratar dúvidas sem insistir na lista de espera.";
    return "Aguardar aceite explícito para entrar na lista de espera.";
  }
  if (conversionPath === "crm_agent_diagnostic") return "Usar diagnóstico gratuito para comparar planos e conduzir para demo ou assinatura.";
  if (readiness === "checkout_ready") return "Confirmar plano e enviar checkout seguro quando billing estiver habilitado.";
  if (readiness === "assisted_close") return "Assumir conversa no WhatsApp/Sales Inbox e continuar fechamento.";
  if (readiness === "waitlist_ready") return "Studio na lista de espera; chamar quando abrir a próxima janela.";
  if (readiness === "plan_ready") return "Reforçar recomendação, enviar comparativo e tratar objeções.";
  if (readiness === "proof_needed") return "Levar para demo real quando disponível ou explicar o fluxo com contexto.";
  if (readiness === "custom_agent_mapping") return "Coletar detalhes da operação sob medida e contato.";
  if (conversionPath === "custom_agent_diagnostic_mapped") return "Continuar venda consultiva da Taliya a partir do diagnóstico.";
  if (conversionPath === "custom_agent_diagnostic_unclear") return "Pedir detalhes da operação antes de recomendar plano ou agente sob medida.";
  if (conversionPath === "analysis_request") return "Fazer diagnóstico comercial e recomendar próximo passo.";
  return "Responder dúvidas e descobrir dor principal.";
}

function extractCrmAgentDiagnostic(qualification: QualificationDraft, conversionPath: ConversionPath): LeadRecord["crmAgentDiagnostic"] {
  if (conversionPath !== "crm_agent_diagnostic" && qualification.diagnosticType !== "crm_agent_diagnostic") return undefined;
  const hasCompletedDiagnostic = qualification.diagnosticStatus === "completed";

  return {
    diagnosticType: qualification.diagnosticType,
    studioSizeRange: qualification.studioSizeRange ?? qualification.activeStudentsRange,
    operationalPains: qualification.operationalPains ?? qualification.biggestPain ?? qualification.primaryPainOrIntent,
    crmPainAreas: qualification.crmPainAreas,
    agentPainAreas: qualification.agentPainAreas,
    dailyVisibility: qualification.dailyVisibility,
    replacementComplexity: qualification.replacementComplexity,
    salesFollowupMaturity: qualification.salesFollowupMaturity,
    currentSystem: qualification.currentSystem,
    priorityGoal: qualification.priorityGoal,
    buyingTiming: qualification.buyingTiming,
    leadTemperature: qualification.leadTemperature,
    recommendedCrmModules: qualification.recommendedCrmModules,
    recommendedAgents: qualification.recommendedAgents,
    recommendedPlan: hasCompletedDiagnostic ? qualification.recommendedPlan : undefined,
    diagnosticSummary: qualification.diagnosticSummary,
    nextStep: qualification.diagnosticNextStep,
    contactCaptureStatus: qualification.contactCaptureStatus,
  };
}

function leadSummaryFromQualification(qualification: QualificationDraft, fallback: string) {
  const hasCompletedDiagnostic = qualification.diagnosticStatus === "completed";
  const recommendedPlan = hasCompletedDiagnostic ? qualification.recommendedPlan : undefined;
  if (qualification.diagnosticSummary || qualification.primaryPainOrIntent || qualification.recommendedAgents || recommendedPlan) {
    return [
      qualification.diagnosticSummary ?? qualification.primaryPainOrIntent,
      qualification.currentSystem ? `Hoje usa: ${qualification.currentSystem}` : undefined,
      qualification.priorityGoal ? `Prioridade: ${qualification.priorityGoal}` : undefined,
      qualification.recommendedAgents ? `Agentes: ${qualification.recommendedAgents}` : undefined,
      recommendedPlan ? `Plano para comparar: ${recommendedPlan}` : undefined,
      qualification.waitlistStatus === "joined" ? "Entrou na lista de espera." : undefined,
    ]
      .filter(Boolean)
      .join(" ");
  }
  return fallback;
}

function planIdFromRecommendation(value?: string) {
  const normalized = normalizeText(value ?? "");
  if (!normalized) return undefined;
  const matches = [
    /\bbase\b/.test(normalized) ? "base" : undefined,
    /\bessencial\b/.test(normalized) ? "one_agent" : undefined,
    /\bavance\b/.test(normalized) ? "three_agents" : undefined,
    /\bcompleto\b|\b7 agentes\b|\bseven_agents\b/.test(normalized) ? "seven_agents" : undefined,
  ].filter((planId): planId is string => Boolean(planId));
  const uniqueMatches = unique(matches);
  if (uniqueMatches.length === 1) return uniqueMatches[0];
  return undefined;
}

function normalizeText(value: string) {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}

function buildStrongIdentifiers(request: AiAttendantRequest, qualification: QualificationDraft, normalizedWhatsapp?: string) {
  return unique(
    [
      request.session.leadId ? `lead:${request.session.leadId}` : undefined,
      request.session.channelSessionId ? `channelSession:${request.session.channelSessionId}` : undefined,
      request.session.externalContact?.providerContactId ? `providerContact:${request.session.externalContact.providerContactId}` : undefined,
      normalizedWhatsapp ? `whatsapp:${normalizedWhatsapp}` : undefined,
      qualification.email ? `email:${normalizeEmail(qualification.email)}` : undefined,
      request.session.sessionId ? `session:${request.session.sessionId}` : undefined,
    ].filter(Boolean) as string[],
  );
}

function buildWeakIdentifiers(request: AiAttendantRequest, qualification: QualificationDraft, response: AiAttendantResponse) {
  return unique(
    [
      qualification.studioName ? `studio:${qualification.studioName.trim().toLowerCase()}` : undefined,
      qualification.cityState ? `cityState:${qualification.cityState.trim().toLowerCase()}` : undefined,
      request.session.sourcePage ? `sourcePage:${request.session.sourcePage}` : undefined,
      response.capturedPainIds.length ? `pains:${response.capturedPainIds.sort().join(",")}` : undefined,
    ].filter(Boolean) as string[],
  );
}

function createStableLeadId(strongIdentifiers: string[], sessionId: string) {
  const source = strongIdentifiers.find((id) => !id.startsWith("session:")) ?? `session:${sessionId}`;
  return `lead_${hashString(source)}`;
}

function createIdempotencyKey(request: AiAttendantRequest, conversionPath: ConversionPath) {
  const channelKey = request.session.externalContact?.providerContactId ?? request.session.channelSessionId ?? request.session.sessionId;
  return `${request.session.channel}:${channelKey}:${conversionPath}`;
}


function normalizePhone(phone?: string) {
  if (!phone) return undefined;
  const digits = phone.replace(/\D/g, "");
  if (!digits) return undefined;
  return digits.startsWith("55") ? `+${digits}` : `+55${digits}`;
}

function normalizeEmail(email: string) {
  return email.trim().toLowerCase();
}

function unique(values: string[]) {
  return Array.from(new Set(values.filter(Boolean)));
}

function hasContact(request: AiAttendantRequest) {
  const qualification = request.session.qualificationDraft;
  return Boolean(
    qualification?.whatsapp ||
      qualification?.email ||
      qualification?.contactPreference ||
      request.session.externalContact?.phone ||
      request.session.externalContact?.providerContactId,
  );
}

function firstNonEmpty(values: Array<string | undefined>) {
  return values.find((value) => typeof value === "string" && value.trim())?.trim();
}

function hashString(value: string) {
  let hash = 0;
  for (let index = 0; index < value.length; index += 1) {
    hash = (hash << 5) - hash + value.charCodeAt(index);
    hash |= 0;
  }
  return Math.abs(hash).toString(36);
}
