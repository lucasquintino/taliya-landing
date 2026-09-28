import type { AgentV2ConversationState, AgentV2DirectQuestion, AgentV2Interpretation } from "./agent-v2-types";
import type { AgentV2NormalizedInput } from "./agent-v2-channel-adapter";
import { normalizeText } from "./agent-v2-normalize";

export function interpretLeadMessage(input: AgentV2NormalizedInput, state: AgentV2ConversationState): AgentV2Interpretation {
  const text = input.text ?? "";
  const normalized = normalizeText(text);
  const directQuestions = detectDirectQuestions(normalized);
  if (
    state.substate.lastAnsweredDirectQuestion === "demo" &&
    !directQuestions.includes("demo") &&
    /\b(explica|explicar|me explica|por aqui|na pratica|na pratica)\b/.test(normalized)
  ) {
    directQuestions.push("demo");
  }
  const riskFlags = detectRiskFlags(normalized, input);
  const factsExtracted = extractFacts(text, normalized, state);
  const sentiment = detectSentiment(normalized);
  const secondaryIntents = detectSecondaryIntents(normalized);

  let primaryIntent: AgentV2Interpretation["primaryIntent"] = "unknown";
  if (riskFlags.includes("prompt_injection")) primaryIntent = "prompt_injection";
  else if (riskFlags.includes("abuse")) primaryIntent = "abuse";
  else if (input.media) primaryIntent = "media";
  else if (directQuestions.includes("human")) primaryIntent = "human_request";
  else if (directQuestions.includes("buy")) primaryIntent = "buying_intent";
  else if (isGreetingOnly(normalized)) primaryIntent = "greeting";
  else if (isDiagnosticAccept(normalized, state)) primaryIntent = "diagnostic_accept";
  else if (isWaitlistAccept(normalized, state)) primaryIntent = "waitlist_accept";
  else if (state.macroState === "waitlist_offered" && isNegative(normalized)) primaryIntent = "waitlist_decline";
  else if (state.macroState === "diagnostic_offered" && isPositive(normalized)) primaryIntent = "diagnostic_accept";
  else if (state.macroState === "diagnostic_offered" && isNegative(normalized)) primaryIntent = "diagnostic_decline";
  else if (directQuestions.length) primaryIntent = "direct_question";
  else if (state.macroState === "diagnostic_in_progress") primaryIntent = "diagnostic_answer";
  else if (factsExtracted.mainPainOrIntent || /taliya.*(studio|ficaria|funcionaria|ajudaria)|rotina|agenda|whatsapp|vendas|financeiro/.test(normalized)) primaryIntent = "pain_or_fit";

  const complex = directQuestions.length > 1 || riskFlags.length > 0 || normalized.length > 360 || sentiment === "irritated";

  return {
    primaryIntent,
    secondaryIntents,
    directQuestions,
    factsExtracted,
    sentiment,
    riskFlags,
    confidence: complex ? "medium" : primaryIntent === "unknown" ? "low" : "high",
    needsEscalation: complex && !riskFlags.includes("prompt_injection"),
    escalationReason: complex ? "mixed_or_risky_turn" : undefined,
  };
}

export function detectDirectQuestions(normalized: string): AgentV2DirectQuestion[] {
  const questions: AgentV2DirectQuestion[] = [];
  if (/\b(preco|precos|valor|valores|quanto custa|quanto fica|mensalidade|assinatura)\b/.test(normalized)) questions.push("price");
  if (/\b(planos?|comparativo|comparar)\b/.test(normalized)) questions.push("plans");
  if (/\b(qual plano|plano faz sentido|recomenda.*plano|indica.*plano)\b/.test(normalized)) questions.push("plan_recommendation");
  if (/\b(demo|demonstracao|ver funcionando|mostrar funcionando|explica.*fluxo|explicar.*fluxo|fluxo por aqui|como seria na pratica|como seria na pratica)\b/.test(normalized)) questions.push("demo");
  if (/\b(o que e|o que eh|como funciona|taliya e|taliya eh)\b/.test(normalized)) questions.push("product");
  if (/\b(whatsapp|business app|numero|mensagem)\b/.test(normalized) && /\b(como funciona|integra|integracao|business app|numero|pelo whatsapp|no whatsapp)\b/.test(normalized)) {
    questions.push("whatsapp");
  }
  if (/\b(garantia|cancelar|cancelamento|reembolso|fidelidade|contrato)\b/.test(normalized)) questions.push("guarantee");
  if (/\b(privacidade|lgpd|dados|seguranca|seguro)\b/.test(normalized)) questions.push("privacy");
  if (/\b(nao souber|nao sabe|inventar|erro|falhar)\b/.test(normalized)) questions.push("uncertainty");
  if (/\b(falar com alguem|falar com uma pessoa|humano|atendente|consultor|pessoa real)\b/.test(normalized)) questions.push("human");
  if (/\b(quero assinar|quero comprar|quero contratar|comprar agora|assinar agora|fechar agora|quero pagar|me manda.*link)\b/.test(normalized)) questions.push("buy");
  if (/\b(garante|roi garantido|resultado garantido|integra com)\b/.test(normalized)) questions.push("unsupported_claim");
  return Array.from(new Set(questions));
}

function extractFacts(raw: string, normalized: string, state: AgentV2ConversationState): AgentV2Interpretation["factsExtracted"] {
  const facts: AgentV2Interpretation["factsExtracted"] = {};
  const email = raw.match(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i)?.[0];
  if (email) facts.email = email;
  if (!state.substate.knownFacts.personName && isLikelyStandaloneName(raw, normalized, state)) facts.personName = raw.trim();
  const phoneDigits = raw.replace(/\D/g, "");
  if (phoneDigits.length >= 10 && phoneDigits.length <= 13) facts.whatsappPhone = phoneDigits;
  const students = normalized.match(/\b(\d{2,4})\s*(alunos?|clientes?)\b/)?.[1] ?? normalized.match(/\btenho\s+(\d{2,4})\b/)?.[1];
  if (students) facts.activeStudents = students;
  if (/\b(planilha|excel|caderno|papel|manual)\b/.test(normalized)) facts.currentWorkflowOrTool = "planilha/caderno/manual";
  if (/\b(tecnofit|nextfit|google agenda|sistema)\b/.test(normalized)) facts.currentWorkflowOrTool = raw.slice(0, 180);
  if (/\b(agora|urgente|resolver agora|preciso resolver)\b/.test(normalized)) facts.urgency = "now";
  else if (/\b(comparando|comparar)\b/.test(normalized)) facts.urgency = "comparing";
  else if (/\b(pesquisando|pesquisar|vendo ainda|vou pensar)\b/.test(normalized)) facts.urgency = "researching";

  const pain = detectPain(normalized);
  if (pain && (!state.substate.diagnosticStep || state.substate.diagnosticStep === "main_pain")) facts.mainPainOrIntent = pain;

  const studioCity = raw.match(/\b(?:em|de)\s+([\p{L}\s.'-]{3,40})(?:$|[,.;])/iu)?.[1];
  if (studioCity) facts.cityState = studioCity.trim();
  const studio = raw.match(/\b(?:nome do studio|studio chama|studio se chama|studio:|estudio:)\s*([\p{L}\d\s.'-]{2,60})(?:$|[,.;])/iu)?.[1];
  if (studio) facts.studioName = `Studio ${studio.trim().replace(/^studio\s+/i, "")}`;
  applyContextualAnswer(raw, normalized, state, facts);
  return facts;
}

function applyContextualAnswer(
  raw: string,
  normalized: string,
  state: AgentV2ConversationState,
  facts: AgentV2Interpretation["factsExtracted"],
) {
  const answer = raw.trim().slice(0, 180);
  if (!answer) return;

  if (state.macroState === "waitlist_pending_details") {
    const missing = new Set(state.substate.missingFields);
    const parts = answer.split(",").map((part) => part.trim()).filter(Boolean);
    if (missing.has("studio") && missing.has("cidade") && parts.length >= 2) {
      facts.studioName ??= parts[0];
      facts.cityState ??= parts.slice(1).join(", ");
    } else if (missing.has("studio") && !facts.studioName) {
      facts.studioName = answer;
    } else if (missing.has("cidade") && !facts.cityState) {
      facts.cityState = answer;
    }
  }

  const step = state.substate.diagnosticStep;
  if (!step) return;

  if (step === "active_students" && !facts.activeStudents) {
    const numeric = normalized.match(/^\d{1,4}$/)?.[0];
    if (numeric) facts.activeStudents = numeric;
  }
  if (step === "main_pain" && !facts.mainPainOrIntent) {
    facts.mainPainOrIntent = answer;
  }
  if (step === "current_workflow" && !facts.currentWorkflowOrTool) {
    facts.currentWorkflowOrTool = answer;
  }
  if (step === "pain_detail" && !facts.painSpecificDetail) {
    facts.painSpecificDetail = answer;
  }
  if (step === "priority" && !facts.priorityToMakeLighter) {
    facts.priorityToMakeLighter = answer;
  }
  if (step === "urgency" && !facts.urgency) {
    if (/\b(agora|resolver|sim|faz sentido|se fizer sentido)\b/.test(normalized)) facts.urgency = "now";
    else if (/\b(comparando|comparar)\b/.test(normalized)) facts.urgency = "comparing";
    else if (/\b(pesquisando|pensando|vendo)\b/.test(normalized)) facts.urgency = "researching";
    else facts.urgency = "unknown";
  }
}

function detectPain(normalized: string) {
  const pains: string[] = [];
  if (/\b(vendas|interessados|aula experimental|matricula|retorno)\b/.test(normalized)) pains.push("vendas e interessados");
  if (/\b(whatsapp|mensagem|atendimento|responder|demora)\b/.test(normalized)) pains.push("atendimento no WhatsApp");
  if (/\b(reposicao|reposicoes|faltas|agenda|horario|encaixe)\b/.test(normalized)) pains.push("agenda, faltas e reposicoes");
  if (/\b(financeiro|cobranca|mensalidade|renovacao|atraso)\b/.test(normalized)) pains.push("financeiro e renovacoes");
  if (/\b(gestao|organizar|rotina|visao do dia|prioridade)\b/.test(normalized)) pains.push("organizacao da rotina do studio");
  if (pains.length) return Array.from(new Set(pains)).join(", ");
  if (/\b(caderno|planilha|manual|papel)\b/.test(normalized)) return "rotina manual em caderno ou planilha";
  return undefined;
}

function isDiagnosticAccept(normalized: string, state: AgentV2ConversationState) {
  if (/\bdiagnostico\b/.test(normalized) && (isPositive(normalized) || /^diagnostico$/.test(normalized))) return true;
  const pending = normalizeText(state.substate.pendingQuestion ?? "");
  const justOfferedRecommendation =
    state.macroState === "price_or_plan" &&
    (state.substate.lastAnsweredDirectQuestion === "plan_recommendation" || /\bdiagnostico\b/.test(pending));
  const justOfferedDemoOrPriceDiagnostic =
    (state.macroState === "price_or_plan" || state.macroState === "demo_interest" || state.macroState === "product_question") &&
    /\bdiagnostico|recomendar|recomendacao\b/.test(pending);
  return isPositive(normalized) && (state.macroState === "diagnostic_offered" || justOfferedRecommendation || justOfferedDemoOrPriceDiagnostic);
}

function isWaitlistAccept(normalized: string, state: AgentV2ConversationState) {
  if (state.macroState === "waitlist_offered" && isPositive(normalized)) return true;
  if (state.macroState === "diagnostic_completed" && /\b(coloca|colocar|lista|espera|pode ser|pode sim|quero|sim)\b/.test(normalized)) return true;
  if (state.macroState === "waitlist_offered" && looksLikeWaitlistDetails(normalized)) return true;
  return false;
}

function looksLikeWaitlistDetails(normalized: string) {
  return /\b(studio|estudio|stúdio)\b/.test(normalized) || /,/.test(normalized) || /\b(vitoria|vitória|vila velha|serra|cariacica)\b/.test(normalized);
}

function isLikelyStandaloneName(raw: string, normalized: string, state: AgentV2ConversationState) {
  const text = raw.trim();
  if (!text || text.length < 2 || text.length > 50) return false;
  if (!/^[\p{L}][\p{L}\s.'-]*$/u.test(text)) return false;
  if (state.macroState !== "open_question" && state.macroState !== "new_lead") return false;
  if (state.substate.pendingQuestion && !/em que posso te ajudar|com quem eu falo|qual seu nome/i.test(state.substate.pendingQuestion)) return false;
  if (/\b(oi|ola|olá|opa|bom dia|boa tarde|boa noite|agenda|reposicao|reposicoes|whatsapp|planos?|preco|valor|demo|diagnostico|vendas|financeiro|studio|pilates|alunos?|caderno|planilha|sim|nao|ok|pode|quero|preciso)\b/.test(normalized)) return false;
  return text.split(/\s+/).length <= 3;
}

function detectRiskFlags(normalized: string, input: AgentV2NormalizedInput) {
  const flags: string[] = [];
  if (/\b(ignore|ignora).{0,40}\b(regras|prompt|instrucao|sistema)|prompt|system message|developer message/.test(normalized)) flags.push("prompt_injection");
  if (/\b(cpf|cartao|cvv|senha|token)\b/.test(normalized)) flags.push("sensitive_data");
  if (/\b(idiota|burro|merda|porra|caralho)\b/.test(normalized)) flags.push("abuse");
  if (input.media) flags.push("unsupported_media");
  return flags;
}

function detectSentiment(normalized: string) {
  if (/\b(urgente|agora|preciso resolver|rapido)\b/.test(normalized)) return "urgent";
  if (/\b(duvida|nao sei|talvez|desconfi|medo|receio)\b/.test(normalized)) return "skeptical";
  if (/\b(chato|bot|robotico|responde direto|irritante)\b/.test(normalized)) return "irritated";
  if (/\b(curioso|queria entender|saber mais)\b/.test(normalized)) return "curious";
  return "neutral";
}

function detectSecondaryIntents(normalized: string) {
  const intents: string[] = [];
  if (/\b(diagnostico|diagnóstico)\b/.test(normalized)) intents.push("diagnostic");
  if (/\b(lista de espera|espera)\b/.test(normalized)) intents.push("waitlist");
  if (/\b(demo|demonstracao)\b/.test(normalized)) intents.push("demo");
  if (/\b(planos?|preco|valor)\b/.test(normalized)) intents.push("pricing");
  return intents;
}

function isGreetingOnly(normalized: string) {
  return /^(oi|ola|opa|bom dia|boa tarde|boa noite|e ai|ei|hello|hi)[\s!.?]*$/.test(normalized.trim());
}

function isPositive(normalized: string) {
  return /\b(sim|pode|faz sentido|gostei|vamos|quero|coloca|pode colocar|perfeito|ok|fechado)\b/.test(normalized);
}

function isNegative(normalized: string) {
  return /\b(nao|nao quero|talvez|vou pensar|agora nao|nao faz sentido)\b/.test(normalized);
}
