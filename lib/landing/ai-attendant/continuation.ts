import type { AiAttendantRequest, AiAttendantResponse, ConversionPath } from "./schema";

const BROAD_ROUTINE_TERMS = /\b(rotina|organizar|melhorar|studio|estudio|pilates|processo|operacao|bagunca|baguncado)\b/i;
const SPECIFIC_PAIN_TERMS = /\b(whatsapp|agenda|agendamento|reposicao|reposicoes|falta|faltas|aluno|alunos|venda|vendas|lead|leads|financeiro|cobranca|cobrancas|renovacao|renovacoes|marketing|instagram)\b/i;
const QUESTION_ENDING = /[?]\s*$/;
const LONG_MESSAGE_LIMIT = 220;
const MAX_SPLIT_PARTS = 3;

const TERMINAL_CTA_PATHS = new Set<ConversionPath>(["checkout_intent", "human_whatsapp_assist", "guided_demo", "view_plans", "waitlist_intent"]);

export function ensureConversationalContinuation(response: AiAttendantResponse, request: AiAttendantRequest): AiAttendantResponse {
  if (response.guardrailDecision.category !== "allowed") return splitLongAssistantMessages(response);
  if (response.conversionPath === "crm_agent_diagnostic") return splitLongAssistantMessages(response);

  const hasTerminalCta = response.conversionPath ? TERMINAL_CTA_PATHS.has(response.conversionPath) : false;
  if (hasTerminalCta && !response.nextQuestion) return splitLongAssistantMessages(response);

  const nextQuestion = normalizeQuestion(response.nextQuestion) ?? continuationQuestionFor(response, request);
  if (!nextQuestion) return splitLongAssistantMessages(response);

  const assistantMessages = [...response.assistantMessages];
  const lastAssistantIndex = findLastAssistantIndex(assistantMessages);
  if (lastAssistantIndex === -1) return splitLongAssistantMessages({ ...response, nextQuestion });

  const lastMessage = assistantMessages[lastAssistantIndex];
  const alreadyContinues = QUESTION_ENDING.test(lastMessage.content.trim());

  if (alreadyContinues || hasTerminalCta) return splitLongAssistantMessages({ ...response, nextQuestion });

  assistantMessages.push({
    ...lastMessage,
    id: `${lastMessage.id}_followup`,
    content: nextQuestion,
  });

  return splitLongAssistantMessages({
    ...response,
    assistantMessages,
    nextQuestion,
  });
}

function findLastAssistantIndex(messages: AiAttendantResponse["assistantMessages"]) {
  for (let index = messages.length - 1; index >= 0; index -= 1) {
    if (messages[index]?.role === "assistant") return index;
  }

  return -1;
}

function continuationQuestionFor(response: AiAttendantResponse, request: AiAttendantRequest) {
  const message = request.userMessage?.trim() ?? "";
  const normalized = normalizeText(message);

  if (isBroadRoutineRequest(normalized)) {
    return "Hoje o que mais pesa na rotina: atendimento no WhatsApp, agenda/reposicoes, vendas ou financeiro?";
  }

  if (response.conversionPath === "view_plans") {
    return "Quer ver os planos agora ou prefere que eu recomende um com base na sua rotina?";
  }

  if (response.conversionPath === "plan_recommendation") {
    return "Quer que eu compare os planos ou prefere me contar quantos alunos e conversas voces tem por semana?";
  }

  if (response.conversionPath === "analysis_request") {
    return "Qual e o ponto que mais trava hoje: atendimento, agenda, vendas ou financeiro?";
  }

  if (response.conversionPath === "custom_agent_follow_up" || response.conversionPath === "mixed_subscription_plus_custom") {
    return "Me conta um pouco mais dessa operacao e o melhor contato para eu te retornar?";
  }

  if (response.recommendedAgentIds.length) {
    return "Quer que eu te mostre como esses agentes funcionariam no seu studio ou prefere ver qual plano faz sentido?";
  }

  return "Hoje voce quer melhorar mais atendimento, agenda/reposicoes, vendas ou financeiro?";
}

function isBroadRoutineRequest(message: string) {
  return BROAD_ROUTINE_TERMS.test(message) && !SPECIFIC_PAIN_TERMS.test(message);
}

function normalizeQuestion(value?: string) {
  const cleanValue = value?.trim();
  if (!cleanValue) return undefined;
  return QUESTION_ENDING.test(cleanValue) ? cleanValue : `${cleanValue}?`;
}

function splitLongAssistantMessages(response: AiAttendantResponse): AiAttendantResponse {
  const assistantMessages = response.assistantMessages.flatMap((message) => {
    if (message.role !== "assistant") return [message];
    const parts = splitLongText(message.content);
    if (parts.length <= 1) return [message];

    return parts.map((content, index) => ({
      ...message,
      id: `${message.id}_part_${index + 1}`,
      content,
    }));
  });

  return {
    ...response,
    assistantMessages,
  };
}

function splitLongText(content: string) {
  const clean = content.trim();
  if (clean.length <= LONG_MESSAGE_LIMIT) return [content];

  const sentences = clean
    .split(/(?<=[.!?])\s+/)
    .map((part) => part.trim())
    .filter(Boolean);

  if (sentences.length < 2) return splitByWords(clean);

  const parts: string[] = [];
  let current = "";

  for (const sentence of sentences) {
    if (current && `${current} ${sentence}`.length > LONG_MESSAGE_LIMIT && parts.length < MAX_SPLIT_PARTS - 1) {
      parts.push(current);
      current = sentence;
      continue;
    }
    current = current ? `${current} ${sentence}` : sentence;
  }

  if (current) parts.push(current);
  return parts.length <= MAX_SPLIT_PARTS ? parts : rebalanceParts(parts);
}

function splitByWords(content: string) {
  const words = content.split(/\s+/).filter(Boolean);
  const parts: string[] = [];
  let current = "";

  for (const word of words) {
    if (current && `${current} ${word}`.length > LONG_MESSAGE_LIMIT && parts.length < MAX_SPLIT_PARTS - 1) {
      parts.push(current);
      current = word;
      continue;
    }
    current = current ? `${current} ${word}` : word;
  }

  if (current) parts.push(current);
  return parts;
}

function rebalanceParts(parts: string[]) {
  const firstTwo = parts.slice(0, MAX_SPLIT_PARTS - 1);
  const last = parts.slice(MAX_SPLIT_PARTS - 1).join(" ");
  return [...firstTwo, last].filter(Boolean);
}

function normalizeText(value: string) {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}
