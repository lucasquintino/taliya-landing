import type { AiAttendantRequest, CommercialStage, QualificationDraft } from "./schema";
import type { AgentV2ConversationState, AgentV2MacroState, AgentV2Substate } from "./agent-v2-types";
import { getCostCapStatus } from "./agent-v2-cost-policy";

export function createDefaultSubstate(request: AiAttendantRequest): AgentV2Substate {
  const draft = request.session.qualificationDraft ?? {};
  const parsed = parseStoredV2State(draft);
  if (parsed?.substate) return parsed.substate;

  return {
    askedQuestions: parseCsv(draft.diagnosticAskedFields),
    knownFacts: {
      personName: draft.name,
      personNameConfidence: draft.name ? "high" : undefined,
      whatsappPhone: request.session.externalContact?.phone ?? draft.whatsapp,
      email: draft.email,
      studioName: draft.studioName,
      cityState: draft.cityState ?? draft.studioCity,
      activeStudents: draft.studioSizeRange ?? draft.activeStudentsRange,
      mainPainOrIntent: draft.primaryPainOrIntent ?? draft.operationalPains ?? draft.biggestPain,
      currentWorkflowOrTool: draft.currentSystem,
      painSpecificDetail: draft.salesFollowupMaturity ?? draft.replacementComplexity ?? draft.dailyVisibility,
      priorityToMakeLighter: draft.priorityGoal,
      urgency: mapBuyingTiming(draft.buyingTiming),
      entryIntent: request.session.entryPath,
    },
    pendingQuestion: null,
    diagnosticStep: null,
    missingFields: [],
    lastTopic: draft.primaryPainOrIntent ?? null,
    lastAnsweredDirectQuestion: null,
    sentiment: "neutral",
    confidence: "medium",
    lastSummary: draft.diagnosticSummary ?? null,
    queuedResponseStatus: "none",
    cost: {
      estimatedConversationCostUsd: Number(draft.agentV2CostEstimateUsd ?? 0) || 0,
      capStatus: getCostCapStatus(Number(draft.agentV2CostEstimateUsd ?? 0) || 0),
    },
  };
}

export function mapCommercialStageToV2(input?: CommercialStage): AgentV2MacroState {
  if (input === "diagnostic_offered") return "diagnostic_offered";
  if (input === "diagnostic_in_progress") return "diagnostic_in_progress";
  if (input === "diagnostic_completed" || input === "recommendation_validation") return "diagnostic_completed";
  if (input === "demo_offered" || input === "demo_seen") return "demo_interest";
  if (input === "waitlist_offered" || input === "waitlist_eligible") return "waitlist_offered";
  if (input === "waitlist_pending_details") return "waitlist_pending_details";
  if (input === "waitlist_joined") return "waitlist_joined";
  if (input === "human_handoff") return "human_requested";
  return "new_lead";
}

export function buildInitialV2State(request: AiAttendantRequest): AgentV2ConversationState {
  const draft = request.session.qualificationDraft ?? {};
  const stored = parseStoredV2State(draft);
  if (stored?.macroState && stored.substate) {
    return {
      version: "agent-v2",
      leadId: request.session.leadId,
      conversationId: conversationIdForRequest(request),
      channel: request.session.channel === "whatsapp" ? "whatsapp" : "widget",
      macroState: stored.macroState,
      substate: stored.substate,
      priority: "cold",
      humanStatus: draft.aiPaused === "true" || draft.humanActive === "true" ? "active" : "none",
      updatedAt: new Date().toISOString(),
    };
  }

  const macroState =
    draft.aiPaused === "true" || draft.humanActive === "true"
      ? "human_active"
      : draft.waitlistStatus === "joined"
        ? "waitlist_joined"
        : mapCommercialStageToV2(draft.commercialStage);

  return {
    version: "agent-v2",
    leadId: request.session.leadId,
    conversationId: conversationIdForRequest(request),
    channel: request.session.channel === "whatsapp" ? "whatsapp" : "widget",
    macroState,
    substate: createDefaultSubstate(request),
    priority: "cold",
    humanStatus: macroState === "human_active" ? "active" : "none",
    updatedAt: new Date().toISOString(),
  };
}

export function serializeV2State(state: AgentV2ConversationState) {
  return JSON.stringify({
    macroState: state.macroState,
    substate: state.substate,
    updatedAt: state.updatedAt,
  });
}

export function parseStoredV2State(draft?: QualificationDraft) {
  if (!draft?.agentV2State) return undefined;
  try {
    const parsed = JSON.parse(draft.agentV2State) as {
      macroState?: AgentV2MacroState;
      substate?: AgentV2Substate;
    };
    if (!parsed.macroState || !parsed.substate) return undefined;
    return parsed;
  } catch {
    return undefined;
  }
}

export function conversationIdForRequest(request: AiAttendantRequest) {
  return request.session.channelSessionId ?? request.session.externalContact?.providerContactId ?? request.session.sessionId;
}

function mapBuyingTiming(value?: string): AgentV2Substate["knownFacts"]["urgency"] {
  const normalized = (value ?? "").toLowerCase();
  if (/agora|resolver|urgente|sim/.test(normalized)) return "now";
  if (/compar/.test(normalized)) return "comparing";
  if (/pesquis/.test(normalized)) return "researching";
  return undefined;
}

function parseCsv(value?: string) {
  return value ? value.split(",").map((item) => item.trim()).filter(Boolean) : [];
}

