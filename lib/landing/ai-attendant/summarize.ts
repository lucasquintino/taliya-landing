import type { AiAttendantRequest } from "./schema";

export function summarizeConversation(request: AiAttendantRequest): string {
  const lastUserMessages = request.session.messages
    .filter((message) => message.role === "user")
    .slice(-3)
    .map((message) => message.content);
  const pains = request.session.selectedPainIds?.length ? `Dores: ${request.session.selectedPainIds.join(", ")}.` : "Dores ainda não confirmadas.";
  const agents = request.session.recommendedAgentIds?.length ? `Agentes recomendados: ${request.session.recommendedAgentIds.join(", ")}.` : "Agentes ainda não confirmados.";
  const latest = lastUserMessages.length ? `Contexto recente: ${lastUserMessages.join(" | ").slice(0, 400)}.` : "Sem histórico recente suficiente.";

  return `${pains} ${agents} ${latest}`;
}
