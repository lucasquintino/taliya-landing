import type { NicheLandingConfig } from "@/data/landing/niches/types";
import type { QualificationDraft } from "./schema";
import { callAiJson } from "./ai-json";

type FinalDiagnosticInput = {
  config: NicheLandingConfig;
  draft: QualificationDraft;
  painIds: string[];
  crmModules: string[];
  agentIds: string[];
  planName: string;
  fallbackMessages: string[];
};

const finalSchema = {
  type: "object",
  additionalProperties: false,
  required: ["messages"],
  properties: {
    messages: {
      type: "array",
      minItems: 4,
      maxItems: 6,
      items: { type: "string" },
    },
  },
} as const;

export async function generateFinalDiagnosticMessages(input: FinalDiagnosticInput): Promise<string[] | undefined> {
  const result = await callAiJson<{ messages?: unknown }>({
    name: "crm_final_diagnostic_messages",
    schema: finalSchema,
    timeoutMs: 10000,
    system: [
      "Voce gera o diagnostico final consultivo da Taliya para um studio de Pilates.",
      "Escreva em portugues do Brasil, natural, curto e comercial sem agressividade.",
      "Use apenas os dados fornecidos. Nao invente preco, recurso, integracao, prazo ou resultado financeiro garantido.",
      "Ordem obrigatoria:",
      "1. mensagem curta: ok, ja tenho as informacoes necessarias e vou montar o diagnostico.",
      "2. gargalo principal e base da rotina primeiro.",
      "3. recomendacao dinamica da base Taliya e plano por ultimo.",
      "4. transicao curta dizendo que os agentes indicados aparecem abaixo, um por vez.",
      "Nao liste agentes individualmente nas mensagens: a interface renderiza os cards de agentes logo abaixo com nome, dor, motivo e atuacao pratica.",
      "A recomendacao deve dizer rotina primeiro, agentes depois, plano por ultimo.",
      "Nao cite campos internos ou enums como 80_a_149, visao_condicional, complexidade alta ou leadTemperature.",
      "Cada mensagem deve caber bem em chat: ate 240 caracteres quando possivel. Nao use markdown pesado.",
    ].join("\n"),
    user: {
      draft: input.draft,
      painIds: input.painIds,
      crmModules: input.crmModules,
      agentIds: input.agentIds,
      planName: input.planName,
      availablePlans: input.config.subscription.plans.map((plan) => ({
        id: plan.id,
        name: plan.name,
        price: plan.monthlyPriceLabel,
      })),
      availableAgents: input.config.agents.map((agent) => ({
        id: agent.id,
        name: agent.name,
        role: agent.role,
      })),
    },
  });

  if (!result.ok || !Array.isArray(result.value.messages)) return undefined;
  const messages = result.value.messages
    .filter((message): message is string => typeof message === "string")
    .map((message) => message.trim())
    .filter(Boolean)
    .slice(0, 6);

  const joinedMessages = messages.join(" ");
  if (
    messages.length < 4 ||
    messages.some((message) => message.length > 280) ||
    violatesFinalRules(joinedMessages) ||
    (input.agentIds.length > 0 && !normalizeText(joinedMessages).includes("agentes indicados"))
  ) {
    return undefined;
  }
  return messages;
}

function violatesFinalRules(text: string) {
  const normalized = normalizeText(text);
  return /(garantido|garantia de resultado|aumentar faturamento garantido|integra com qualquer|sem erro|100%|agente indicado:|dor que resolve:|atuacao pratica:|80_a_149|30_a_79|150_mais|visao_condicional|complexidade alta|leadtemperature)/i.test(normalized);
}

function normalizeText(text: string) {
  return text
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}
