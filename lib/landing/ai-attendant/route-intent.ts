import type { AiAttendantRequest } from "./schema";
import { callAiJson } from "./ai-json";

export type AiRouteIntent =
  | "diagnostic_request"
  | "diagnostic_continue"
  | "price_or_plan"
  | "product_question"
  | "demo_request"
  | "human_request"
  | "objection"
  | "custom_agent_request"
  | "buying_intent"
  | "off_topic"
  | "general";

export type AiRouteDecision = {
  intent: AiRouteIntent;
  shouldStartDiagnostic: boolean;
  confidence: number;
  reason: string;
};

const routeSchema = {
  type: "object",
  additionalProperties: false,
  required: ["intent", "shouldStartDiagnostic", "confidence", "reason"],
  properties: {
    intent: {
      type: "string",
      enum: [
        "diagnostic_request",
        "diagnostic_continue",
        "price_or_plan",
        "product_question",
        "demo_request",
        "human_request",
        "objection",
        "custom_agent_request",
        "buying_intent",
        "off_topic",
        "general",
      ],
    },
    shouldStartDiagnostic: { type: "boolean" },
    confidence: { type: "number" },
    reason: { type: "string" },
  },
} as const;

export async function classifyAiRoute(request: AiAttendantRequest): Promise<AiRouteDecision> {
  const deterministic = deterministicRoute(request);
  if (deterministic) return deterministic;

  const result = await callAiJson<AiRouteDecision>({
    name: "ai_attendant_route_intent",
    schema: routeSchema,
    timeoutMs: 5000,
    system: [
      "Voce roteia mensagens de um atendimento comercial da Taliya para studios de Pilates.",
      "Classifique a mensagem atual. Nao responda ao cliente.",
      "Regra mais importante: diagnostico so comeca quando a pessoa pede explicitamente diagnostico, raio-x, mapear o studio/rotina, ou quando ja esta em diagnostico.",
      "Perguntas como 'qual o valor', 'quanto custa', 'tem demo', 'como funciona', 'integra com X', 'quero falar com humano' NAO iniciam diagnostico.",
      "Nessas perguntas, shouldStartDiagnostic deve ser false. O atendimento pode sugerir diagnostico depois, mas nao deve coletar nome/WhatsApp automaticamente.",
      "Se a pessoa disser claramente 'quero fazer diagnostico gratuito', 'quero diagnostico', 'faz o raio-x', 'mapear meu studio', shouldStartDiagnostic=true.",
    ].join("\n"),
    user: {
      userMessage: request.userMessage,
      quickReplyId: request.quickReplyId,
      entryPath: request.session.entryPath,
      qualificationDraft: compactQualificationDraft(request.session.qualificationDraft),
      recentMessages: request.session.messages.slice(-4).map((message) => ({
        role: message.role,
        content: message.content,
        intent: message.intent,
      })),
    },
  });

  if (!result.ok) return fallbackRoute(request);
  return normalizeDecision(result.value);
}

export function diagnosticIsExplicitlyStarted(request: AiAttendantRequest, route: AiRouteDecision) {
  if (request.session.qualificationDraft?.diagnosticCancelled === "true" && request.quickReplyId !== "start_crm_diagnostic") return false;
  return route.shouldStartDiagnostic || route.intent === "diagnostic_continue";
}

function deterministicRoute(request: AiAttendantRequest): AiRouteDecision | undefined {
  if (
    request.session.qualificationDraft?.diagnosticType === "crm_agent_diagnostic" &&
    request.session.qualificationDraft.diagnosticCompleted !== "true" &&
    request.session.qualificationDraft.diagnosticCancelled !== "true"
  ) {
    return {
      intent: "diagnostic_continue",
      shouldStartDiagnostic: true,
      confidence: 1,
      reason: "diagnostic already active",
    };
  }
  if (request.quickReplyId === "start_crm_diagnostic" || request.session.entryPath === "diagnostic_cta") {
    return {
      intent: "diagnostic_request",
      shouldStartDiagnostic: true,
      confidence: 1,
      reason: "explicit diagnostic entry",
    };
  }
  if (
    request.session.qualificationDraft?.diagnosticStatus === "offered" &&
    request.session.qualificationDraft.diagnosticCompleted !== "true" &&
    isDiagnosticOfferAccepted(request)
  ) {
    return {
      intent: "diagnostic_request",
      shouldStartDiagnostic: true,
      confidence: 1,
      reason: "accepted previously offered diagnostic",
    };
  }
  return undefined;
}

function isDiagnosticOfferAccepted(request: AiAttendantRequest) {
  const current = normalize(request.userMessage ?? "");
  if (!isPositiveIntent(current)) return false;
  if (/\b(diagnostico|diagnosticar|raio[-\s]?x|mapear)\b/.test(current)) return true;

  const recentAssistantText = normalize(
    request.session.messages
      .slice(-4)
      .filter((message) => message.role === "assistant")
      .map((message) => message.content)
      .join(" "),
  );

  return /\bdiagnostico gratuito|faca um diagnostico|fazer um diagnostico\b/.test(recentAssistantText);
}

function isPositiveIntent(normalized: string) {
  return /\b(sim|faz sentido|gostei|boa|perfeito|quero|pode|vamos|tenho interesse|curti|legal|avancar|seguir|pode fazer|faca|faz)\b/.test(normalized);
}

function fallbackRoute(request: AiAttendantRequest): AiRouteDecision {
  const text = normalize([request.userMessage, request.quickReplyId].filter(Boolean).join(" "));
  const explicitDiagnostic = /\b(diagnostico|diagnositco|diagnostico gratuito|diagnositco gratuito|raio[-\s]?x|mapear meu studio|mapear minha rotina|diagnosticar)\b/.test(text);
  if (explicitDiagnostic) {
    return {
      intent: "diagnostic_request",
      shouldStartDiagnostic: true,
      confidence: 0.7,
      reason: "fallback explicit diagnostic wording",
    };
  }
  return {
    intent: "general",
    shouldStartDiagnostic: false,
    confidence: 0.5,
    reason: "fallback non-diagnostic route",
  };
}

function compactQualificationDraft(draft: AiAttendantRequest["session"]["qualificationDraft"]) {
  if (!draft) return {};
  return {
    diagnosticType: draft.diagnosticType,
    diagnosticCompleted: draft.diagnosticCompleted,
    diagnosticCancelled: draft.diagnosticCancelled,
    diagnosticAskedFields: draft.diagnosticAskedFields,
    operationalPains: draft.operationalPains,
    contactCaptureStatus: draft.contactCaptureStatus,
    recommendedPlan: draft.recommendedPlan,
  };
}

function normalizeDecision(input: AiRouteDecision): AiRouteDecision {
  const intent = isRouteIntent(input.intent) ? input.intent : "general";
  return {
    intent,
    shouldStartDiagnostic: Boolean(input.shouldStartDiagnostic) && (intent === "diagnostic_request" || intent === "diagnostic_continue"),
    confidence: typeof input.confidence === "number" ? Math.max(0, Math.min(1, input.confidence)) : 0,
    reason: typeof input.reason === "string" ? input.reason.slice(0, 180) : "route classified",
  };
}

function isRouteIntent(input: unknown): input is AiRouteIntent {
  return (
    input === "diagnostic_request" ||
    input === "diagnostic_continue" ||
    input === "price_or_plan" ||
    input === "product_question" ||
    input === "demo_request" ||
    input === "human_request" ||
    input === "objection" ||
    input === "custom_agent_request" ||
    input === "buying_intent" ||
    input === "off_topic" ||
    input === "general"
  );
}

function normalize(value: string) {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}
