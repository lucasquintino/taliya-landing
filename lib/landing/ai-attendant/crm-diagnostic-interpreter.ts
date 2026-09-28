import type { QualificationDraft } from "./schema";
import { callAiJson } from "./ai-json";

type InterpreterInput = {
  userMessage: string;
  currentField?: string;
  currentQuestion?: string;
  currentDraft: QualificationDraft;
};

export type CrmDiagnosticInterpretation = {
  intent: DiagnosticTurnIntent;
  shouldContinueDiagnostic: boolean;
  patch?: Partial<QualificationDraft>;
  feedback?: string;
  sideAnswer?: string;
  confidence: number;
  reason: string;
};

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

const interpretationSchema = {
  type: "object",
  additionalProperties: false,
  required: ["intent", "shouldContinueDiagnostic", "understood", "confidence", "reason", "patch"],
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
    understood: { type: "boolean" },
    confidence: { type: "number" },
    reason: { type: "string" },
    feedback: { type: "string" },
    sideAnswer: { type: "string" },
    patch: {
      type: "object",
      additionalProperties: { type: "string" },
      properties: {
        name: { type: "string" },
        whatsapp: { type: "string" },
        email: { type: "string" },
        activeStudentsRange: { type: "string" },
        studioSizeRange: { type: "string" },
        operationalPains: { type: "string" },
        dailyVisibility: { type: "string" },
        replacementComplexity: { type: "string" },
        salesFollowupMaturity: { type: "string" },
        currentSystem: { type: "string" },
        priorityGoal: { type: "string" },
        buyingTiming: { type: "string" },
        contactCaptureStatus: { type: "string" },
      },
    },
  },
} as const;

export async function interpretCrmDiagnosticAnswer(input: InterpreterInput): Promise<CrmDiagnosticInterpretation | undefined> {
  if (!shouldUseInterpreter(input)) return undefined;

  const result = await callAiJson<Record<string, unknown>>({
    name: "crm_diagnostic_answer_interpretation",
    schema: interpretationSchema,
    timeoutMs: 8000,
    system: [
      "Voce interpreta respostas livres de um diagnostico consultivo da Taliya para studios de Pilates.",
      "A tarefa e classificar o turno, entender a resposta, extrair dados e escrever um feedback curto e humano. Nao faca a proxima pergunta.",
      "Use answer_current_question quando a pessoa respondeu a pergunta atual, mesmo com texto livre, curto, informal ou incompleto.",
      "Use price_or_plan para duvidas sobre valores, preco, planos, assinatura ou comparativo.",
      "Use custom_agent_request quando a pessoa pedir algo fora do time principal da Taliya, como marketing, Instagram, campanhas, trafego, conteudo, parcerias, estoque, RH ou qualquer agente/processo sob medida.",
      "Use diagnostic_cancel quando a pessoa disser que nao quer continuar o diagnostico.",
      "Use human_request quando pedir uma pessoa, consultor ou WhatsApp humano.",
      "Use unsupported_integration para integracao/sistema externo nao confirmado.",
      "Use product_question ou other_side_question para duvidas laterais que devem ser respondidas antes de retomar.",
      "shouldContinueDiagnostic=true apenas quando a conversa deve retomar a pergunta atual depois da resposta lateral. Para custom_agent_request ou diagnostic_cancel, use false.",
      "Se a pessoa fugir do script com uma duvida de preco, demo, integracao, recepcionista ou medo de IA, preencha sideAnswer com uma resposta curta e segura e tambem extraia o que for possivel.",
      "Nao dependa de opcoes sugeridas. Respostas como 'depende do meu tempo', 'mais ou menos', 'tenho num caderno', 'minha recepcionista ve', 'uso planilha e WhatsApp' devem ser interpretadas.",
      "Preencha apenas campos que a mensagem realmente respondeu. Nao invente dados.",
      "feedback deve ter uma frase curta, natural e relacionada ao que a pessoa disse. Sem parecer template.",
      "Valores esperados:",
      "activeStudentsRange/studioSizeRange: ate_30, 30_a_79, 80_a_149, 150_mais.",
      "operationalPains: lista curta separada por virgula, usando termos como whatsapp, agenda/reposicoes, faltas, vendas, financeiro, acompanhamento, gestao, historico/evolucao.",
      "dailyVisibility: tem_visao, visao_manual, visao_condicional ou sem_visao. Use visao_condicional quando a visao depende de tempo, pessoa especifica, correria ou so acontece as vezes.",
      "replacementComplexity: alta ou baixa.",
      "salesFollowupMaturity: fraco, manual ou organizado.",
      "currentSystem: planilha, whatsapp, manual, whatsapp_e_manual ou sistema.",
      "buyingTiming: agora ou pesquisando.",
      "contactCaptureStatus: captured ou refused.",
    ].join("\n"),
    user: {
      currentField: input.currentField,
      currentQuestion: input.currentQuestion,
      userMessage: input.userMessage,
      currentDraft: compactDraft(input.currentDraft),
    },
  });

  if (!result.ok || !isRecord(result.value)) return undefined;
  const intent = normalizeIntent(result.value.intent);
  if (intent === "answer_current_question" && result.value.understood !== true) return undefined;
  const confidence = typeof result.value.confidence === "number" ? result.value.confidence : 0;
  if (confidence < 0.45) return undefined;
  const patch = isRecord(result.value.patch) ? normalizePatch(result.value.patch) : {};

  return {
    intent,
    shouldContinueDiagnostic: Boolean(result.value.shouldContinueDiagnostic),
    patch,
    feedback: typeof result.value.feedback === "string" ? result.value.feedback.trim().slice(0, 220) : undefined,
    sideAnswer: typeof result.value.sideAnswer === "string" ? result.value.sideAnswer.trim().slice(0, 280) : undefined,
    confidence,
    reason: typeof result.value.reason === "string" ? result.value.reason.slice(0, 180) : "interpreted diagnostic turn",
  };
}

function shouldUseInterpreter(input: InterpreterInput) {
  if (!input.userMessage.trim()) return false;
  if (!input.currentField) return false;
  return input.userMessage.trim().length >= 2;
}

function compactDraft(draft: QualificationDraft) {
  return {
    name: draft.name,
    contactCaptureStatus: draft.contactCaptureStatus,
    activeStudentsRange: draft.activeStudentsRange,
    studioSizeRange: draft.studioSizeRange,
    operationalPains: draft.operationalPains,
    dailyVisibility: draft.dailyVisibility,
    replacementComplexity: draft.replacementComplexity,
    salesFollowupMaturity: draft.salesFollowupMaturity,
    currentSystem: draft.currentSystem,
    priorityGoal: draft.priorityGoal,
    buyingTiming: draft.buyingTiming,
    diagnosticAskedFields: draft.diagnosticAskedFields,
  };
}

function normalizeIntent(input: unknown): DiagnosticTurnIntent {
  return isDiagnosticTurnIntent(input) ? input : "unclear";
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

function normalizePatch(input: Record<string, unknown>): Partial<QualificationDraft> {
  const patch: Partial<QualificationDraft> = {};
  copyString(input, patch, "name", 80);
  copyString(input, patch, "whatsapp", 40);
  copyString(input, patch, "email", 120);
  copyAllowed(input, patch, "activeStudentsRange", ["ate_30", "30_a_79", "80_a_149", "150_mais"]);
  copyAllowed(input, patch, "studioSizeRange", ["ate_30", "30_a_79", "80_a_149", "150_mais"]);
  copyString(input, patch, "operationalPains", 240);
  copyAllowed(input, patch, "dailyVisibility", ["tem_visao", "visao_manual", "visao_condicional", "sem_visao"]);
  copyAllowed(input, patch, "replacementComplexity", ["alta", "baixa"]);
  copyAllowed(input, patch, "salesFollowupMaturity", ["fraco", "manual", "organizado"]);
  copyAllowed(input, patch, "currentSystem", ["planilha", "whatsapp", "manual", "whatsapp_e_manual", "sistema"]);
  copyString(input, patch, "priorityGoal", 180);
  copyAllowed(input, patch, "buyingTiming", ["agora", "pesquisando"]);
  copyAllowed(input, patch, "contactCaptureStatus", ["captured", "refused"]);
  return patch;
}

function copyString<K extends keyof QualificationDraft>(input: Record<string, unknown>, patch: Partial<QualificationDraft>, key: K, maxLength: number) {
  if (typeof input[key] !== "string") return;
  const value = input[key].trim().slice(0, maxLength);
  if (value) {
    (patch as Record<keyof QualificationDraft, unknown>)[key] = value;
  }
}

function copyAllowed<K extends keyof QualificationDraft>(input: Record<string, unknown>, patch: Partial<QualificationDraft>, key: K, allowed: string[]) {
  if (typeof input[key] !== "string") return;
  const value = input[key].trim();
  if (allowed.includes(value)) {
    (patch as Record<keyof QualificationDraft, unknown>)[key] = value;
  }
}

function isRecord(input: unknown): input is Record<string, unknown> {
  return typeof input === "object" && input !== null;
}
