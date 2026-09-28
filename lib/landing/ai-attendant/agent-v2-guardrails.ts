import type { AiAttendantRequest, AiAttendantResponse } from "./schema";
import type { AgentV2OrchestrationDecision } from "./agent-v2-types";

export function validateAgentV2Response({
  request,
  response,
  decision,
}: {
  request: AiAttendantRequest;
  response: AiAttendantResponse;
  decision: AgentV2OrchestrationDecision;
}) {
  const reasons: string[] = [];
  const text = response.assistantMessages.map((message) => message.content).join("\n\n").toLowerCase();

  if (request.session.channel === "whatsapp" && isAskingForWhatsAppContact(text)) {
    reasons.push("no_whatsapp_phone_request");
  }
  if (/\b(checkout|cartao|pagar agora|link de pagamento|assinar agora pelo link)\b/.test(normalize(text))) {
    reasons.push("no_checkout_while_waitlist_closed");
  }
  if (/\b(system prompt|developer message|instrucoes internas|prompt interno)\b/.test(text)) {
    reasons.push("no_prompt_leak");
  }
  if (decision.selectedAction === "answer_direct" && decision.responseObjective.includes("direta") && response.assistantMessages.length === 0) {
    reasons.push("direct_question_not_answered");
  }

  if (!reasons.length) {
    return { status: "passed" as const, reasons: [] as string[], response };
  }

  return {
    status: "modified" as const,
    reasons,
    response: {
      ...response,
      assistantMessages: [
        {
          id: `assistant_guardrail_${Date.now()}`,
          role: "assistant" as const,
          content: safeFallbackForReasons(reasons),
          intent: "guardrail" as const,
        },
      ],
      guardrailDecision: {
        category: "allowed" as const,
        action: "respond" as const,
        reason: `Agent v2 guardrail modified response: ${reasons.join(",")}`,
      },
    },
  };
}

export function validateToolPlan(decision: AgentV2OrchestrationDecision) {
  const reasons: string[] = [];
  if (decision.selectedAction === "offer_waitlist" && decision.toolActions.some((action) => action.toolName === "sendCheckout")) {
    reasons.push("checkout_tool_blocked");
  }
  return { ok: reasons.length === 0, reasons };
}

function safeFallbackForReasons(reasons: string[]) {
  if (reasons.includes("no_whatsapp_phone_request")) {
    return "Vou usar o contato deste canal mesmo. Para seguir, me diga só o detalhe que falta sobre o studio.";
  }
  if (reasons.includes("no_checkout_while_waitlist_closed")) {
    return "Estamos trabalhando com um número pequeno de studios agora. Se fizer sentido, posso colocar seu studio na lista de espera e chamar assim que abrir uma próxima janela.";
  }
  return "Para não te responder de qualquer jeito, vou deixar isso salvo e seguimos com uma pessoa se precisar.";
}

function isAskingForWhatsAppContact(text: string) {
  const normalized = normalize(text);
  return (
    /\b(me passa|manda|envia|informa|qual e|qual eh|qual seria).{0,36}\b(seu|teu|contato|numero|telefone|whatsapp|email)\b/.test(normalized) ||
    /\b(whatsapp|telefone|numero|email).{0,24}\b(para|pra).{0,24}\b(chamar|contato|retornar)\b/.test(normalized)
  );
}

function normalize(value: string) {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}
