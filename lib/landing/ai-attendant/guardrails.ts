import type { AiAttendantRequest, AiAttendantResponse, GuardrailDecision } from "./schema";

const PROMPT_INJECTION_PATTERNS = [
  /ignore (as )?instru/i,
  /ignore.*instru/i,
  /ignore (the )?(previous|above)/i,
  /mostre.*prompt/i,
  /revel(e|a).*prompt/i,
  /system prompt/i,
  /instrucoes internas/i,
  /developer message/i,
];

const SENSITIVE_DATA_PATTERNS = [
  /cartao/i,
  /cart[aã]o/i,
  /cvv/i,
  /senha/i,
  /historico (dela|dele|da aluna|do aluno|medico|clinico)/i,
  /hist[oó]rico (dela|dele|da aluna|do aluno|medico|m[eé]dico|clinico|cl[ií]nico)/i,
  /problema medico/i,
  /problema m[eé]dico/i,
  /dados? (sensiveis|medicos|privados) (da aluna|do aluno|de aluno|de alunos|dela|dele)?/i,
  /dados? (sens[ií]veis?|m[eé]dicos?|privados?) (da aluna|do aluno|de aluno|de alunos|dela|dele)?/i,
  /prontu[aá]rio/i,
  /laudo/i,
  /diagn[oó]stico m[eé]dico/i,
  /patologia/i,
  /cpf/i,
];

const OPT_OUT_PATTERNS = [
  /\bparar\b.*\b(nao|n[aã]o)\b.*\breceber/i,
  /parar de responder/i,
  /nao quero mais receber/i,
  /não quero mais receber/i,
  /nao quero receber/i,
  /não quero receber/i,
  /nao me mande/i,
  /não me mande/i,
  /sair da lista/i,
  /descadastrar/i,
  /\bparem? (de )?(me )?(mandar|enviar|responder|chamar|contactar|contatar)/i,
  /\bparar (mensagens|respostas automaticas|automacao|automa[cÃ§][aÃ£]o|contato|contacto)/i,
  /stop\b/i,
];

const PROHIBITED_OUTPUT_PATTERNS = [
  /garantimos? resultado/i,
  /resultado garantido/i,
  /\bROI\b/i,
  /ticket m[eé]dio/i,
  /\bMVP\b/i,
  /beta/i,
  /valida[cç][aã]o/i,
  /early access/i,
  /acesso antecipado/i,
];

export function classifyInputGuardrail(request: AiAttendantRequest): GuardrailDecision {
  const text = [request.userMessage, request.quickReplyId].filter(Boolean).join(" ");

  if (request.session.externalContact?.optedOut) {
    return {
      category: "off_topic",
      action: "refuse",
      reason: "WhatsApp contact has opted out.",
      visibleMessage: "Entendi. Nao vou continuar com respostas automaticas por aqui.",
    };
  }

  if (isOptOutText(text)) {
    return {
      category: "off_topic",
      action: "refuse",
      reason: "Visitor asked to stop automated WhatsApp messages.",
      visibleMessage: "Tudo certo, vou parar as respostas automaticas por aqui.",
    };
  }

  if (PROMPT_INJECTION_PATTERNS.some((pattern) => pattern.test(text))) {
    return {
      category: "prompt_injection",
      action: "refuse",
      reason: "Visitor requested internal instructions.",
      visibleMessage:
        "Nao posso ajudar com instrucoes internas. Posso te explicar como os agentes ajudariam no atendimento, agenda, vendas ou financeiro do studio.",
    };
  }

  if (SENSITIVE_DATA_PATTERNS.some((pattern) => pattern.test(text))) {
    return {
      category: "sensitive_data",
      action: "redirect",
      reason: "Visitor included or requested sensitive personal, health or payment details.",
      visibleMessage:
        "Nao preciso desse tipo de dado sensivel para te orientar. Podemos falar da rotina do studio de forma geral: atendimento, agenda, mensalidades, faltas ou historico.",
    };
  }

  return {
    category: "allowed",
    action: "respond",
    reason: "Input is allowed.",
  };
}

export function isOptOutText(text: string) {
  return OPT_OUT_PATTERNS.some((pattern) => pattern.test(text));
}

export function applyOutputGuardrails(response: AiAttendantResponse): AiAttendantResponse {
  const unsafeMessage = response.assistantMessages.find((message) => PROHIBITED_OUTPUT_PATTERNS.some((pattern) => pattern.test(message.content)));
  if (!unsafeMessage) return response;

  return {
    ...response,
    assistantMessages: [
      {
        id: `assistant_guardrail_${Date.now()}`,
        role: "assistant",
        content:
          "Prefiro ser preciso: os agentes podem ajudar a mostrar prioridades e reduzir trabalho manual, mas sem prometer resultado garantido. Quer me contar qual rotina mais pesa hoje?",
        intent: "guardrail",
      },
    ],
    guardrailDecision: {
      category: "unsupported_claim",
      action: "redirect",
      reason: "Assistant output contained prohibited or overpromising language.",
    },
  };
}
