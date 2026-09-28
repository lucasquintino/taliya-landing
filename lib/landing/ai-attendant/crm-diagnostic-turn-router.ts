import type { QualificationDraft } from "./schema";
import { callAiJson } from "./ai-json";

export type DiagnosticTurnIntent =
  | "answer_current_question"
  | "diagnostic_cancel"
  | "price_or_plan"
  | "custom_agent_request"
  | "product_question"
  | "human_request"
  | "unsupported_integration"
  | "other_side_question"
  | "unclear";

export type DiagnosticTurnRoute = {
  intent: DiagnosticTurnIntent;
  shouldContinueDiagnostic: boolean;
  confidence: number;
  reason: string;
  sideAnswer?: string;
};

type DiagnosticTurnRouteInput = {
  userMessage: string;
  currentField?: string;
  currentQuestion?: string;
  currentDraft: QualificationDraft;
};

const diagnosticTurnRouteSchema = {
  type: "object",
  additionalProperties: false,
  required: ["intent", "shouldContinueDiagnostic", "confidence", "reason"],
  properties: {
    intent: {
      type: "string",
      enum: [
        "answer_current_question",
        "diagnostic_cancel",
        "price_or_plan",
        "custom_agent_request",
        "product_question",
        "human_request",
        "unsupported_integration",
        "other_side_question",
        "unclear",
      ],
    },
    shouldContinueDiagnostic: { type: "boolean" },
    confidence: { type: "number" },
    reason: { type: "string" },
    sideAnswer: { type: "string" },
  },
} as const;

export async function classifyDiagnosticTurnRoute(input: DiagnosticTurnRouteInput): Promise<DiagnosticTurnRoute | undefined> {
  const message = input.userMessage.trim();
  if (!message || !input.currentField) return undefined;

  const result = await callAiJson<DiagnosticTurnRoute>({
    name: "crm_diagnostic_turn_route",
    schema: diagnosticTurnRouteSchema,
    timeoutMs: 6000,
    system: [
      "Voce roteia uma mensagem enviada durante um diagnostico comercial da Taliya para studios de Pilates.",
      "Nao responda como chat final; classifique a intencao do turno.",
      "A decisao principal: a mensagem responde a pergunta atual do diagnostico ou mudou de assunto?",
      "Use answer_current_question quando a pessoa respondeu a pergunta atual, mesmo com texto livre, curto, informal ou incompleto.",
      "Use price_or_plan para duvidas sobre valores, preco, planos, assinatura ou comparativo.",
      "Use custom_agent_request quando a pessoa pedir algo fora do time principal da Taliya, como marketing, Instagram, campanhas, trafego, conteudo, parcerias, estoque, RH ou qualquer agente/processo sob medida.",
      "Use diagnostic_cancel quando a pessoa disser que nao quer continuar o diagnostico.",
      "Use human_request quando pedir uma pessoa, consultor ou WhatsApp humano.",
      "Use unsupported_integration para integracao/sistema externo nao confirmado.",
      "Use product_question ou other_side_question para duvidas laterais que devem ser respondidas antes de retomar.",
      "shouldContinueDiagnostic=true apenas quando a conversa deve retomar a pergunta atual depois da resposta lateral. Para custom_agent_request ou diagnostic_cancel, use false.",
      "sideAnswer deve ser uma resposta curta e segura quando a intencao nao for answer_current_question. Nao invente recurso, preco novo, integracao ou promessa.",
    ].join("\n"),
    user: {
      userMessage: input.userMessage,
      currentField: input.currentField,
      currentQuestion: input.currentQuestion,
      currentDraft: input.currentDraft,
    },
  });

  if (!result.ok) return undefined;
  return normalizeRoute(result.value);
}

function normalizeRoute(input: DiagnosticTurnRoute): DiagnosticTurnRoute {
  const intent = isDiagnosticTurnIntent(input.intent) ? input.intent : "unclear";
  return {
    intent,
    shouldContinueDiagnostic: Boolean(input.shouldContinueDiagnostic),
    confidence: typeof input.confidence === "number" ? Math.max(0, Math.min(1, input.confidence)) : 0,
    reason: typeof input.reason === "string" ? input.reason.slice(0, 180) : "classified diagnostic turn",
    sideAnswer: typeof input.sideAnswer === "string" ? input.sideAnswer.trim().slice(0, 260) : undefined,
  };
}

function isDiagnosticTurnIntent(input: unknown): input is DiagnosticTurnIntent {
  return (
    input === "answer_current_question" ||
    input === "diagnostic_cancel" ||
    input === "price_or_plan" ||
    input === "custom_agent_request" ||
    input === "product_question" ||
    input === "human_request" ||
    input === "unsupported_integration" ||
    input === "other_side_question" ||
    input === "unclear"
  );
}
