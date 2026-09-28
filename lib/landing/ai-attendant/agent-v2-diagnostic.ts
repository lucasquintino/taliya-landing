import type { AgentV2DiagnosticOutput, AgentV2KnownFacts, AgentV2Substate } from "./agent-v2-types";
import { firstName } from "./agent-v2-identity";

export const diagnosticSteps = [
  "active_students",
  "main_pain",
  "current_workflow",
  "pain_detail",
  "priority",
  "urgency",
] as const;

export type DiagnosticStep = (typeof diagnosticSteps)[number];

export function nextDiagnosticQuestion(substate: AgentV2Substate) {
  const facts = substate.knownFacts;
  const missing = getMissingDiagnosticSteps(facts, substate.askedQuestions);
  const step = missing[0];
  if (!step) return null;

  return {
    step,
    question: questionForStep(step, facts),
  };
}

export function getMissingDiagnosticSteps(facts: AgentV2KnownFacts, askedQuestions: string[] = []): DiagnosticStep[] {
  const missing: DiagnosticStep[] = [];
  if (!facts.activeStudents && !askedQuestions.includes("active_students_unknown")) missing.push("active_students");
  if (!facts.mainPainOrIntent) missing.push("main_pain");
  if (!facts.currentWorkflowOrTool) missing.push("current_workflow");
  if (!facts.painSpecificDetail) missing.push("pain_detail");
  if (!facts.priorityToMakeLighter) missing.push("priority");
  if (!facts.urgency) missing.push("urgency");
  return missing;
}

export function hasEnoughForDiagnostic(facts: AgentV2KnownFacts) {
  const missing = getMissingDiagnosticSteps(facts);
  return missing.length === 0 && Boolean(facts.mainPainOrIntent && facts.currentWorkflowOrTool && facts.painSpecificDetail && facts.priorityToMakeLighter);
}

export function buildDiagnosticOutput(facts: AgentV2KnownFacts): AgentV2DiagnosticOutput {
  const pain = facts.mainPainOrIntent ?? "rotina do studio";
  const workflow = facts.currentWorkflowOrTool ?? "forma atual ainda não informada";
  const priority = facts.priorityToMakeLighter ?? pain;
  const agents = agentsForPain(`${pain} ${priority}`);
  const broad = agents.length >= 3;
  const primaryFlags = dominantPainFlags(pain, priority);

  return {
    mainBottleneck: diagnosticProblemSentence(pain, primaryFlags),
    evidence: [
      facts.activeStudents ? `Studio com cerca de ${facts.activeStudents} alunos ativos.` : "Tamanho do studio ainda não informado.",
      `Hoje isso passa por ${workflow}.`,
      facts.painSpecificDetail ? `Detalhe citado: ${facts.painSpecificDetail}.` : `Prioridade citada: ${priority}.`,
    ],
    likelyOperationalCause: diagnosticCauseSentence(primaryFlags),
    operationalImpact: diagnosticImpactSentence(primaryFlags),
    firstOrganizationStep: diagnosticTaliyaStep(primaryFlags),
    indicatedAgents: agents,
    planOrPlanRangeToCompare: broad ? "Avance ou Completo" : agents.length >= 2 ? "Essencial ou Avance" : "Essencial",
    confidence: facts.mainPainOrIntent && facts.currentWorkflowOrTool && facts.priorityToMakeLighter ? "high" : "medium",
    unknowns: getMissingDiagnosticSteps(facts).map((step) => step),
    validationQuestion: validationQuestion(facts.personName),
  };
}

function dominantPainFlags(pain: string, priority: string) {
  const primary = painFlags(pain);
  const priorityFlags = painFlags(priority);
  if (priorityFlags.isSchedulePain || priorityFlags.isSalesPain || priorityFlags.isWhatsAppPain) {
    return {
      isSchedulePain: priorityFlags.isSchedulePain,
      isSalesPain: priorityFlags.isSalesPain || primary.isSalesPain,
      isWhatsAppPain: priorityFlags.isWhatsAppPain,
    };
  }
  return primary;
}

function painFlags(value: string) {
  return {
    isSchedulePain: /agenda|repos/i.test(value),
    isSalesPain: /vendas|interessados/i.test(value),
    isWhatsAppPain: /whatsapp|atendimento/i.test(value),
  };
}

function diagnosticProblemSentence(
  pain: string,
  flags: { isSchedulePain: boolean; isSalesPain: boolean; isWhatsAppPain: boolean },
) {
  if (countPainFlags(flags) >= 2) return "Pelo que você contou, o problema não está em uma rotina só.";
  if (flags.isSchedulePain) return "Pelo que você contou, o problema não é só reposição.";
  if (flags.isSalesPain) return "Pelo que você contou, o problema não é só vender mais.";
  if (flags.isWhatsAppPain) return "Pelo que você contou, o problema não é só responder WhatsApp.";
  return `Pelo que você contou, o problema principal está em ${pain}.`;
}

function diagnosticCauseSentence(flags: { isSchedulePain: boolean; isSalesPain: boolean; isWhatsAppPain: boolean }) {
  if (countPainFlags(flags) >= 2) return "O risco é atendimento, agenda e interessados dependerem de mensagens soltas, planilha e memória da equipe.";
  if (flags.isSchedulePain) return "O risco é a rotina depender de caderno, memória e mensagens soltas.";
  if (flags.isSalesPain) return "O risco é cada interessado depender de alguém lembrar quem chamou, quem respondeu e qual é o próximo passo.";
  if (flags.isWhatsAppPain) return "O risco é o WhatsApp virar o lugar onde tudo acontece, mas quase nada fica organizado para a equipe acompanhar.";
  return "O risco é a rotina ficar espalhada entre conversa, agenda, anotação e memória da equipe.";
}

function diagnosticImpactSentence(flags: { isSchedulePain: boolean; isSalesPain: boolean; isWhatsAppPain: boolean }) {
  if (countPainFlags(flags) >= 2) return "Isso faz interessado esfriar, reposição atrasar e pendência importante sumir no meio da rotina.";
  if (flags.isSchedulePain) return "Isso faz o studio perder horário, atrasar retorno e deixar aluno esperando.";
  if (flags.isSalesPain) return "Isso faz interessado esfriar, aula experimental ficar sem retorno e oportunidade boa sumir no meio das mensagens.";
  if (flags.isWhatsAppPain) return "Isso gera demora, retrabalho e resposta sem contexto quando outra pessoa precisa assumir.";
  return "Isso aumenta retrabalho, deixa pendências invisíveis e faz decisões simples dependerem de quem lembrou de conferir.";
}

function diagnosticTaliyaStep(flags: { isSchedulePain: boolean; isSalesPain: boolean; isWhatsAppPain: boolean }) {
  if (countPainFlags(flags) >= 2) return "A Taliya ajudaria conectando atendimento, agenda, interessados, histórico e próximos passos em uma base única.";
  if (flags.isSchedulePain) return "A Taliya ajudaria organizando agenda, faltas, reposições, histórico e próximos passos em um lugar só.";
  if (flags.isSalesPain) return "A Taliya ajudaria colocando interessados, conversas, origem e próximos passos em um fluxo mais claro.";
  if (flags.isWhatsAppPain) return "A Taliya ajudaria conectando atendimento, histórico, pendências e rotina do aluno em um lugar só.";
  return "A Taliya ajudaria organizando alunos, conversas, agenda, financeiro e prioridades do dia em uma base única.";
}

function countPainFlags(flags: { isSchedulePain: boolean; isSalesPain: boolean; isWhatsAppPain: boolean }) {
  return [flags.isSchedulePain, flags.isSalesPain, flags.isWhatsAppPain].filter(Boolean).length;
}

function validationQuestion(name?: string) {
  return name ? `Então, ${firstName(name)}... isso conversa com o que você precisa resolver agora?` : "Então... isso conversa com o que você precisa resolver agora?";
}

function questionForStep(step: DiagnosticStep, facts: AgentV2KnownFacts) {
  if (step === "active_students") return "Hoje seu studio tem mais ou menos quantos alunos ativos?";
  if (step === "main_pain") return "Qual parte mais pesa hoje: WhatsApp, agenda/reposições, vendas, financeiro ou acompanhamento dos alunos?";
  if (step === "current_workflow") return "Hoje isso fica em algum sistema ou mais em WhatsApp, planilha e caderno?";
  if (step === "pain_detail") {
    if (/vendas|interessados/i.test(facts.mainPainOrIntent ?? "")) return "Quando alguém chama querendo conhecer o studio, vocês conseguem acompanhar até virar aluno?";
    if (/agenda|repos/i.test(facts.mainPainOrIntent ?? "")) return "As reposições ficam claras para a equipe ou dependem de conversa e memória?";
    if (/whatsapp|atendimento/i.test(facts.mainPainOrIntent ?? "")) return "O que mais pesa no WhatsApp: volume de mensagens, pedidos repetidos ou demora no retorno?";
    return "Hoje você consegue ver facilmente o que precisa ser resolvido no dia?";
  }
  if (step === "priority") return "Pensando na rotina do studio, qual tarefa você mais gostaria de deixar mais leve primeiro?";
  return "Vocês estão buscando resolver isso agora ou só pesquisando por enquanto?";
}

function agentsForPain(value: string) {
  const normalized = value
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
  const agents: string[] = [];
  if (/\b(whatsapp|atendimento|mensagem|responder)\b/.test(normalized)) agents.push("Atendimento");
  if (/\b(agenda|repos|faltas|horario)\b/.test(normalized)) agents.push("Agenda");
  if (/\b(vendas|interessados|experimental|matricula)\b/.test(normalized)) agents.push("Vendas");
  if (/\b(financeiro|mensalidade|cobranca|renovacao)\b/.test(normalized)) agents.push("Financeiro");
  if (/\b(gestao|prioridade|visao|rotina|dia)\b/.test(normalized)) agents.push("Gestao");
  return agents.length ? Array.from(new Set(agents)) : ["Atendimento", "Gestao"];
}
