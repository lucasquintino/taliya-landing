import type { AiAttendantChannel, AiAttendantRequest, AiAttendantResponse, QualificationDraft } from "./schema";

export type AgentV2Mode = "legacy" | "capture_only" | "auto";

export type AgentV2MacroState =
  | "new_lead"
  | "open_question"
  | "product_question"
  | "price_or_plan"
  | "diagnostic_offered"
  | "diagnostic_in_progress"
  | "diagnostic_completed"
  | "demo_interest"
  | "waitlist_offered"
  | "waitlist_pending_details"
  | "waitlist_joined"
  | "human_requested"
  | "human_active"
  | "closed";

export type AgentV2Sentiment = "neutral" | "curious" | "urgent" | "skeptical" | "irritated";
export type AgentV2Confidence = "high" | "medium" | "low";
export type AgentV2Priority = "cold" | "warm" | "hot" | "waitlist_ready" | "human_needed" | "no_action";

export type AgentV2KnownFacts = {
  personName?: string;
  personNameConfidence?: "high" | "medium" | "low" | "unusable";
  whatsappPhone?: string;
  email?: string;
  studioName?: string;
  cityState?: string;
  activeStudents?: string;
  mainPainOrIntent?: string;
  currentWorkflowOrTool?: string;
  painSpecificDetail?: string;
  priorityToMakeLighter?: string;
  urgency?: "now" | "comparing" | "researching" | "unknown";
  source?: "direct" | "site" | "instagram" | "facebook" | "ad" | "unknown";
  entryIntent?: string;
};

export type AgentV2DiagnosticOutput = {
  mainBottleneck: string;
  evidence: string[];
  likelyOperationalCause: string;
  operationalImpact: string;
  firstOrganizationStep: string;
  indicatedAgents: string[];
  planOrPlanRangeToCompare: string;
  confidence: AgentV2Confidence;
  unknowns: string[];
  validationQuestion: string;
};

export type AgentV2Substate = {
  askedQuestions: string[];
  knownFacts: AgentV2KnownFacts;
  pendingQuestion: string | null;
  diagnosticStep: string | null;
  missingFields: string[];
  lastTopic: string | null;
  lastAnsweredDirectQuestion: string | null;
  sentiment: AgentV2Sentiment;
  confidence: AgentV2Confidence;
  lastSummary: string | null;
  queuedResponseStatus: "none" | "queued" | "suppressed" | "revalidate_required";
  cost: {
    estimatedConversationCostUsd: number;
    capStatus: "ok" | "review" | "high" | "hard_cap_blocked";
  };
};

export type AgentV2ConversationState = {
  version: "agent-v2";
  leadId?: string;
  conversationId: string;
  channel: "widget" | "whatsapp";
  macroState: AgentV2MacroState;
  substate: AgentV2Substate;
  priority: AgentV2Priority;
  humanStatus: "none" | "requested" | "active" | "resumed";
  productSourceVersion?: string;
  updatedAt: string;
};

export type AgentV2DirectQuestion =
  | "price"
  | "plans"
  | "plan_recommendation"
  | "demo"
  | "product"
  | "whatsapp"
  | "guarantee"
  | "privacy"
  | "uncertainty"
  | "human"
  | "buy"
  | "unsupported_claim";

export type AgentV2Interpretation = {
  primaryIntent:
    | "greeting"
    | "direct_question"
    | "pain_or_fit"
    | "diagnostic_accept"
    | "diagnostic_decline"
    | "diagnostic_answer"
    | "waitlist_accept"
    | "waitlist_decline"
    | "buying_intent"
    | "human_request"
    | "media"
    | "abuse"
    | "prompt_injection"
    | "unknown";
  secondaryIntents: string[];
  directQuestions: AgentV2DirectQuestion[];
  factsExtracted: Partial<AgentV2KnownFacts>;
  sentiment: AgentV2Sentiment;
  riskFlags: string[];
  confidence: AgentV2Confidence;
  needsEscalation: boolean;
  escalationReason?: string;
};

export type AgentV2Action =
  | "legacy_fallback"
  | "opening"
  | "answer_direct"
  | "offer_diagnostic"
  | "continue_diagnostic"
  | "deliver_diagnostic"
  | "offer_waitlist"
  | "collect_waitlist_details"
  | "confirm_waitlist_joined"
  | "answer_post_waitlist"
  | "capture_name"
  | "handoff_human"
  | "pause_no_reply"
  | "cost_cap_fallback"
  | "unsupported_media"
  | "safe_refusal";

export type AgentV2OrchestrationDecision = {
  selectedAction: AgentV2Action;
  stateTransition: AgentV2MacroState;
  responseObjective: string;
  toolActions: Array<{
    toolName: string;
    payload: Record<string, unknown>;
  }>;
  modelClass: "default" | "stronger";
  escalationReason?: string;
  costBudgetCategory:
    | "simple_answer"
    | "medium_qualified_lead"
    | "diagnostic_lead"
    | "long_complex_lead"
    | "evaluation_run";
};

export type AgentV2ToolRecord = {
  toolName: string;
  idempotencyKey: string;
  status: "pending" | "succeeded" | "failed" | "skipped";
  output?: Record<string, unknown>;
  failureReason?: string;
};

export type AgentV2ModelUsage = {
  operation: "interpretation" | "generation" | "judge" | "summary" | "recovery";
  model: string;
  inputTokens?: number;
  outputTokens?: number;
  estimatedCostUsd: number;
  budgetCategory: AgentV2OrchestrationDecision["costBudgetCategory"];
  escalationReason?: string;
};

export type AgentV2Trace = {
  id: string;
  leadId?: string;
  conversationId: string;
  turnId: string;
  channel: AiAttendantChannel;
  normalizedInput: unknown;
  stateBefore?: AgentV2ConversationState;
  productSourceVersion?: string;
  semanticInterpretation?: AgentV2Interpretation;
  orchestrationDecision?: AgentV2OrchestrationDecision;
  toolActions: AgentV2ToolRecord[];
  guardrailResult: {
    status: "passed" | "blocked" | "modified";
    reasons: string[];
  };
  responseDraft?: unknown;
  validatedResponse?: unknown;
  stateAfter?: AgentV2ConversationState;
  deliveryResult?: unknown;
  modelUsage: AgentV2ModelUsage[];
  costEstimateUsd: number;
  fallbackReason?: string;
  createdAt: string;
};

export type AgentV2LoopInput = {
  request: AiAttendantRequest;
  legacyTurn: (request: AiAttendantRequest) => Promise<AiAttendantResponse>;
};

export type AgentV2PersistedEnvelope = {
  macroState?: AgentV2MacroState;
  substate?: AgentV2Substate;
  traceId?: string;
  costEstimateUsd?: number;
};

export type AgentV2ResponseWithMeta = AiAttendantResponse & {
  qualificationPatch?: QualificationDraft & {
    agentV2State?: string;
    agentV2TraceId?: string;
    agentV2CostEstimateUsd?: string;
  };
};
