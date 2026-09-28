"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import type { CSSProperties, Touch } from "react";
import { agentVisualTokens } from "@/data/landing/agentVisuals";
import { taliyaFeaturedAgentFlowsByAgent, type TaliyaLandingAgentFlow } from "@/data/landing/agentFlowCatalog";
import type { Agent } from "@/data/landing/niches/types";
import { SectionIntro } from "../shared/SectionIntro";
import { SectionShell } from "../shared/SectionShell";

const SWIPE_COMMIT_PX = 72;
const SWIPE_INTENT_PX = 12;
const SWIPE_MAX_OFFSET_PX = 76;
const SCROLL_OVERFLOW_EPSILON_PX = 4;

type CarouselTouchState = {
  startX: number;
  startY: number;
  offsetX: number;
  intent: "pending" | "horizontal" | "vertical";
};

function scrollElementToTopOnMobile(selector: string) {
  if (typeof window === "undefined") return;
  if (!window.matchMedia("(max-width: 1023px)").matches) return;

  const element = document.querySelector<HTMLElement>(selector);
  if (!element) return;

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const header = document.querySelector<HTMLElement>("header");
  const headerOffset = Math.ceil((header?.getBoundingClientRect().height ?? 64) + 14);
  const alignElement = (behavior: ScrollBehavior) => {
    const top = Math.max(0, window.scrollY + element.getBoundingClientRect().top - headerOffset);
    window.scrollTo({ top, behavior });
  };

  window.requestAnimationFrame(() => {
    alignElement(prefersReducedMotion ? "auto" : "smooth");
    window.setTimeout(() => {
      const distanceFromTarget = element.getBoundingClientRect().top - headerOffset;
      if (Math.abs(distanceFromTarget) > 6) alignElement("auto");
    }, prefersReducedMotion ? 0 : 620);
  });
}

function resetAgentPanelScroll() {
  if (typeof document === "undefined") return;
  document.querySelectorAll<HTMLElement>("#agentes .landing-panel-scroll").forEach((node) => {
    node.scrollTo({ top: 0, behavior: "auto" });
  });
}

const agentExplainers: Record<string, string> = {
  atendimento: "Cadastro, serviços e informações do cliente",
  agenda: "Agendar, remarcar e cancelar",
  vendas: "Avulso, pacote e plano",
  financeiro: "Recebimentos e saldos",
  retencao: "Criar e acompanhar lembretes",
  gestao: "Resumos do dia e do período",
  listagens: "Consultas por cliente, período e situação",
  "historico-evolucao": "Orçamentos e arquivos",
};

const flowNavLabels: Record<string, string> = {
  A1: "Cadastrar cliente",
  A2: "Dados do cliente",
  A3: "Histórico do cliente",
  A5: "Falar com a equipe",
  A10: "Lembrete de retorno",
  B1: "Agendar serviço",
  B2: "Cancelar horário",
  B3: "Atualizar agenda",
  B4: "Horário disponível",
  B5: "Remarcar serviço",
  B12: "Lembrete de agenda",
  C1: "Tipos de serviço",
  C2: "Criar orçamento",
  C4: "Aprovar orçamento",
  C5: "Retomar orçamento",
  C6: "Registrar serviço",
  C7: "Ajustar proposta",
  D1: "Registrar recebimento",
  D2: "Saldo em aberto",
  D3: "Lembrete de cobrança",
  D5: "Recebimentos",
  D6: "Corrigir recebimento",
  D14: "Histórico de recebimentos",
  E1: "Criar lembrete",
  E2: "Ver lembretes",
  E4: "Alterar lembrete",
  E5: "Concluir lembrete",
  E6: "Lembrete ao cliente",
  E7: "Próximo lembrete",
  F1: "Visão do dia",
  F2: "Resumo de recebimentos",
  F3: "Clientes com horário",
  F4: "Serviços prestados",
  F5: "Resumo do período",
  F6: "Orçamentos aguardando resposta",
  F7: "Saldos em aberto",
  F8: "Fechamento do dia",
  G1: "Orçamentos",
  G2: "Guardar arquivo",
  G3: "Documento importante",
  G4: "Versões do orçamento",
  G5: "Documentos do cliente",
  G12: "Histórico do serviço",
};

function agentTokenId(agentId: string) {
  if (agentId === "historico-evolucao") return "historico";
  if (agentId === "listagens") return "gestao";
  return agentId;
}

function agentVisual(agent: Agent) {
  return agentVisualTokens[agentTokenId(agent.id)] ?? {
    accent: agent.accent,
    soft: `${agent.accent}16`,
    activeBg: `${agent.accent}12`,
    label: agent.name,
  };
}

function formatPtBrCopy(text: string) {
  return text
    .replace(/\bReposicao\b/g, "Reposição")
    .replace(/\breposicao\b/g, "reposição")
    .replace(/\bReposicoes\b/g, "Reposições")
    .replace(/\breposicoes\b/g, "reposições")
    .replace(/\bRenovacao\b/g, "Renovação")
    .replace(/\brenovacao\b/g, "renovação")
    .replace(/\bAcao\b/g, "Ação")
    .replace(/\bacao\b/g, "ação")
    .replace(/\bAcoes\b/g, "Ações")
    .replace(/\bacoes\b/g, "ações")
    .replace(/\bAprovacao\b/g, "Aprovação")
    .replace(/\baprovacao\b/g, "aprovação")
    .replace(/\bHorario\b/g, "Horário")
    .replace(/\bhorario\b/g, "horário")
    .replace(/\bHorarios\b/g, "Horários")
    .replace(/\bhorarios\b/g, "horários")
    .replace(/\bPossivel\b/g, "Possível")
    .replace(/\bpossivel\b/g, "possível")
    .replace(/\bPublicos\b/g, "Públicos")
    .replace(/\bpublicos\b/g, "públicos")
    .replace(/\bPublico\b/g, "Público")
    .replace(/\bpublico\b/g, "público")
    .replace(/\bNecessarios\b/g, "Necessários")
    .replace(/\bnecessarios\b/g, "necessários")
    .replace(/\bEsta\b(?=\s+(clara|claro|perto|aberta|aberto|pendente|disponível|funcionando|fluindo|ajudando|caro|insatisfeito|ocupado|tudo|identificada|em|perdida)\b)/g, "Está")
    .replace(/\besta\b(?=\s+(clara|claro|perto|aberta|aberto|pendente|disponível|funcionando|fluindo|ajudando|caro|insatisfeito|ocupado|tudo|identificada|em|perdida)\b)/g, "está")
    .replace(/\bEstao\b/g, "Estão")
    .replace(/\bestao\b/g, "estão")
    .replace(/\bJa\b/g, "Já")
    .replace(/\bja\b/g, "já")
    .replace(/\bNao\b/g, "Não")
    .replace(/\bnao\b/g, "não")
    .replace(/\bAlguem\b/g, "Alguém")
    .replace(/\balguem\b/g, "alguém")
    .replace(/\bDuvida\b/g, "Dúvida")
    .replace(/\bduvida\b/g, "dúvida")
    .replace(/\bEndereco\b/g, "Endereço")
    .replace(/\bendereco\b/g, "endereço")
    .replace(/\bInformacao\b/g, "Informação")
    .replace(/\binformacao\b/g, "informação")
    .replace(/\bPropria\b/g, "Própria")
    .replace(/\bpropria\b/g, "própria")
    .replace(/\bProximo\b/g, "Próximo")
    .replace(/\bproximo\b/g, "próximo")
    .replace(/\bProxima\b/g, "Próxima")
    .replace(/\bproxima\b/g, "próxima")
    .replace(/\bRetencao\b/g, "Retenção")
    .replace(/\bretencao\b/g, "retenção")
    .replace(/\bGestao\b/g, "Gestão")
    .replace(/\bgestao\b/g, "gestão")
    .replace(/\bHistorico\b/g, "Histórico")
    .replace(/\bhistorico\b/g, "histórico")
    .replace(/\bPresenca\b/g, "Presença")
    .replace(/\bpresenca\b/g, "presença")
    .replace(/\bAusencia\b/g, "Ausência")
    .replace(/\bausencia\b/g, "ausência")
    .replace(/\bFrequencia\b/g, "Frequência")
    .replace(/\bfrequencia\b/g, "frequência")
    .replace(/\bEvolucao\b/g, "Evolução")
    .replace(/\bevolucao\b/g, "evolução")
    .replace(/\bRestricao\b/g, "Restrição")
    .replace(/\brestricao\b/g, "restrição")
    .replace(/\bObservacao\b/g, "Observação")
    .replace(/\bobservacao\b/g, "observação")
    .replace(/\bSensivel\b/g, "Sensível")
    .replace(/\bsensivel\b/g, "sensível")
    .replace(/\bCredito\b/g, "Crédito")
    .replace(/\bcredito\b/g, "crédito")
    .replace(/\bOpcoes\b/g, "Opções")
    .replace(/\bopcoes\b/g, "opções")
    .replace(/\bMatricula\b/g, "Matrícula")
    .replace(/\bmatricula\b/g, "matrícula")
    .replace(/\bPreco\b/g, "Preço")
    .replace(/\bpreco\b/g, "preço")
    .replace(/\bRecepcao\b/g, "Recepção")
    .replace(/\brecepcao\b/g, "recepção")
    .replace(/\bVe\b/g, "Vê")
    .replace(/\bve\b/g, "vê")
    .replace(/\bResponsavel\b/g, "Responsável")
    .replace(/\bresponsavel\b/g, "responsável")
    .replace(/\bResponsaveis\b/g, "Responsáveis")
    .replace(/\bresponsaveis\b/g, "responsáveis")
    .replace(/\bDecisao\b/g, "Decisão")
    .replace(/\bdecisao\b/g, "decisão")
    .replace(/\bDecisoes\b/g, "Decisões")
    .replace(/\bdecisoes\b/g, "decisões")
    .replace(/\bExcecao\b/g, "Exceção")
    .replace(/\bexcecao\b/g, "exceção")
    .replace(/\bExcecoes\b/g, "Exceções")
    .replace(/\bexcecoes\b/g, "exceções")
    .replace(/\bAutomacao\b/g, "Automação")
    .replace(/\bautomacao\b/g, "automação")
    .replace(/\bOperacao\b/g, "Operação")
    .replace(/\boperacao\b/g, "operação")
    .replace(/\bInformacoes\b/g, "Informações")
    .replace(/\binformacoes\b/g, "informações")
    .replace(/\bCobranca\b/g, "Cobrança")
    .replace(/\bcobranca\b/g, "cobrança")
    .replace(/\bCobrancas\b/g, "Cobranças")
    .replace(/\bcobrancas\b/g, "cobranças")
    .replace(/\bAte\b/g, "Até")
    .replace(/\bate\b/g, "até")
    .replace(/\bMinimo\b/g, "Mínimo")
    .replace(/\bminimo\b/g, "mínimo")
    .replace(/\bRapida\b/g, "Rápida")
    .replace(/\brapida\b/g, "rápida")
    .replace(/\bRapido\b/g, "Rápido")
    .replace(/\brapido\b/g, "rápido")
    .replace(/\bArea\b/g, "Área")
    .replace(/\barea\b/g, "área")
    .replace(/\bSaude\b/g, "Saúde")
    .replace(/\bsaude\b/g, "saúde")
    .replace(/\bLesao\b/g, "Lesão")
    .replace(/\blesao\b/g, "lesão")
    .replace(/\bAvaliacao\b/g, "Avaliação")
    .replace(/\bavaliacao\b/g, "avaliação")
    .replace(/\bRevisao\b/g, "Revisão")
    .replace(/\brevisao\b/g, "revisão")
    .replace(/\bRepeticao\b/g, "Repetição")
    .replace(/\brepeticao\b/g, "repetição")
    .replace(/\bPadrao\b/g, "Padrão")
    .replace(/\bpadrao\b/g, "padrão")
    .replace(/\bDisponivel\b/g, "Disponível")
    .replace(/\bdisponivel\b/g, "disponível")
    .replace(/\bProvavel\b/g, "Provável")
    .replace(/\bprovavel\b/g, "provável")
    .replace(/\bAntecedencia\b/g, "Antecedência")
    .replace(/\bantecedencia\b/g, "antecedência")
    .replace(/\bIntencao\b/g, "Intenção")
    .replace(/\bintencao\b/g, "intenção")
    .replace(/\bVisao\b/g, "Visão")
    .replace(/\bvisao\b/g, "visão")
    .replace(/\bInsatisfacao\b/g, "Insatisfação")
    .replace(/\binsatisfacao\b/g, "insatisfação")
    .replace(/\bPresencas\b/g, "Presenças")
    .replace(/\bpresencas\b/g, "presenças")
    .replace(/\bSilencio\b/g, "Silêncio")
    .replace(/\bsilencio\b/g, "silêncio")
    .replace(/\bCritico\b/g, "Crítico")
    .replace(/\bcritico\b/g, "crítico")
    .replace(/\bMedio\b/g, "Médio")
    .replace(/\bmedio\b/g, "médio")
    .replace(/\bPrevio\b/g, "Prévio")
    .replace(/\bprevio\b/g, "prévio")
    .replace(/\bPrevia\b/g, "Prévia")
    .replace(/\bprevia\b/g, "prévia")
    .replace(/\bUtil\b/g, "Útil")
    .replace(/\butil\b/g, "útil")
    .replace(/\bUnica\b/g, "Única")
    .replace(/\bunica\b/g, "única")
    .replace(/\bE\b(?=\s+(aluno|aluna|elogio|primeira|o|a|sobre|agenda|financeiro|alto|baixa|de|da|do|um|uma)\b)/g, "É")
    .replace(/\be\b(?=\s+(aluno|aluna|elogio|primeira|o|a|sobre|agenda|financeiro|alto|baixa|de|da|do|um|uma)\b)/g, "é")
    .replace(/\bHa\b/g, "Há")
    .replace(/\bha\b/g, "há")
    .replace(/\bSo\b/g, "Só")
    .replace(/\bso\b/g, "só")
    .replace(/\bestão\b/g, "estão");
}

function buildFallbackFlow(agent: Agent): TaliyaLandingAgentFlow {
  return {
    id: `${agent.id}-principal`,
    code: agent.id.slice(0, 2).toUpperCase(),
    title: agent.role,
    displayTitle: agent.role,
    summary: agent.result,
    mode: "copiloto",
    channel: "hibrido",
    channels: ["App", "WhatsApp"],
    trigger: agent.pain,
    checks: [],
    action: agent.action,
    message: agent.workspace.conversation.lines.at(-1)?.text ?? agent.result,
    result: agent.result,
    when: agent.pain,
    does: agent.action,
    outcome: agent.result,
    whenBullets: [agent.pain],
    doesBullets: [agent.action],
    outcomeBullets: [agent.result],
    inside: [],
  };
}

function AgentNavigation({
  agents,
  onSelectAgent,
  selectedAgent,
}: {
  agents: Agent[];
  onSelectAgent: (agentId: string) => void;
  selectedAgent: Agent;
}) {
  return (
    <aside className="hidden h-full w-full min-w-0 max-w-full overflow-hidden rounded-[2rem] border border-[#E5DED2] bg-white/84 p-3.5 shadow-[0_22px_60px_rgba(16,27,58,0.08)] backdrop-blur xl:p-4 lg:flex lg:flex-col">
      <div className="px-2 pb-3">
        <p className="text-[11px] font-black uppercase tracking-[0.24em] text-[#101B3A]">Frentes</p>
        <p className="mt-1 text-[0.62rem] font-black uppercase tracking-[0.16em] text-[#98A2B3]">Toque para trocar</p>
      </div>

      <div
        className="-mb-8 flex max-w-full gap-2 overflow-x-auto pb-8 lg:mb-0 lg:grid lg:min-w-0 lg:flex-1 lg:grid-rows-8 lg:overflow-visible lg:pb-0"
        style={{ scrollbarWidth: "none" }}
      >
        {agents.map((agent) => {
          const isActive = agent.id === selectedAgent.id;
          const visual = agentVisual(agent);
          return (
            <button
              aria-pressed={isActive}
              className={`agent-nav-item group flex min-h-[4.85rem] w-[14rem] shrink-0 items-center gap-3.5 overflow-hidden rounded-[1.2rem] border px-4 py-3 text-left transition duration-200 focus:outline-none focus:ring-4 focus:ring-[#101B3A]/10 lg:h-full lg:min-h-0 lg:w-full ${isActive ? "is-active shadow-[0_8px_18px_rgba(16,27,58,0.10)]" : "border-transparent hover:bg-[#FFFDF8]"}`}
              data-agent-nav-id={agent.id}
              key={agent.id}
              onClick={() => onSelectAgent(agent.id)}
              style={isActive ? { backgroundColor: visual.activeBg, borderColor: visual.accent } : undefined}
              type="button"
            >
              <span className="min-w-0 flex-1 overflow-hidden">
                <span className="block truncate text-lg font-black leading-tight tracking-[-0.03em] text-[#101B3A]">{agent.name}</span>
                <span
                  className="mt-1 block max-w-full truncate whitespace-nowrap text-[0.8rem] font-extrabold leading-4"
                  style={{ color: isActive ? visual.accent : "#8A90A6" }}
                >
                  {agentExplainers[agent.id] ?? agent.role}
                </span>
              </span>
              <span className="agent-active-dot h-5 w-5 shrink-0 rounded-full" style={{ backgroundColor: isActive ? visual.accent : "#AEB7C2", opacity: isActive ? 1 : 0.62 }} />
            </button>
          );
        })}
      </div>
    </aside>
  );
}

function MobileAgentNavigation({
  activeIndex,
  onMove,
  selectedAgent,
  total,
}: {
  activeIndex: number;
  onMove: (direction: 1 | -1) => void;
  selectedAgent: Agent;
  total: number;
}) {
  const visual = agentVisual(selectedAgent);

  return (
    <div className="mobile-agent-nav flex min-h-[4.25rem] items-center rounded-[1.35rem] border border-[#E5DED2] bg-white px-[0.58rem] py-[0.58rem] shadow-[0_16px_35px_rgba(16,27,58,0.08)] lg:hidden">
      <div className="grid w-full grid-cols-[2.35rem_minmax(0,1fr)_2.35rem] items-center justify-items-center gap-[0.45rem]">
        <button aria-label="Frente anterior" className="grid h-[2.35rem] w-[2.35rem] shrink-0 place-items-center rounded-full border border-[#E2DED5] bg-[#FFFDF8] font-black text-[#101B3A]" onClick={() => onMove(-1)} type="button">
          &lt;
        </button>
        <div className="flex min-w-0 w-full items-center justify-center gap-[0.58rem] text-center">
          <div className="min-w-0">
            <p className="truncate text-[0.94rem] font-black leading-[1rem] tracking-[-0.03em]" style={{ color: visual.accent }}>
              {selectedAgent.name}
            </p>
            <p className="truncate text-[0.67rem] font-bold leading-[0.84rem] text-[#667085]">{agentExplainers[selectedAgent.id] ?? selectedAgent.role}</p>
            <p className="mt-0.5 text-[0.58rem] font-black uppercase leading-none tracking-[0.12em] text-[#98A2B3]">Frente {activeIndex + 1} de {total}</p>
          </div>
        </div>
        <button aria-label="Próxima frente" className="grid h-[2.35rem] w-[2.35rem] shrink-0 place-items-center rounded-full border border-[#E2DED5] bg-[#FFFDF8] font-black text-[#101B3A]" onClick={() => onMove(1)} type="button">
          &gt;
        </button>
      </div>
    </div>
  );
}

function AgentDots({
  activeIndex,
  agents,
  dragDirection,
  onSelect,
  selectedAgent,
}: {
  activeIndex: number;
  agents: Agent[];
  dragDirection: 1 | -1 | null;
  onSelect: (agentId: string) => void;
  selectedAgent: Agent;
}) {
  const visual = agentVisual(selectedAgent);
  const label = dragDirection === null ? "Arraste na horizontal para trocar" : dragDirection > 0 ? "Solte para ver a próxima frente" : "Solte para voltar à frente anterior";

  return (
    <div className="mt-4 rounded-[1.35rem] border border-[#E5DED2] bg-white/75 px-4 py-3 shadow-[0_14px_30px_rgba(16,27,58,0.06)] lg:hidden">
      <p className={`text-center text-[0.72rem] font-black uppercase tracking-[0.16em] transition-colors ${dragDirection === null ? "text-[#98A2B3]" : "text-[#101B3A]"}`}>{label}</p>
      <div className="mt-1 flex justify-center gap-0.5">
        {agents.map((agent, index) => (
          <button
            aria-label={`Ir para frente ${agent.name}`}
            className="grid h-10 w-10 place-items-center rounded-full transition focus:outline-none focus:ring-4 focus:ring-[#101B3A]/10"
            key={agent.id}
            onClick={() => onSelect(agent.id)}
            type="button"
          >
            <span
              className={`h-2.5 rounded-full transition-all ${index === activeIndex ? "w-8" : "w-2.5 bg-[#D8D2C8]"}`}
              style={index === activeIndex ? { backgroundColor: visual.accent } : undefined}
            />
          </button>
        ))}
      </div>
    </div>
  );
}

function FlowNavigation({
  accent,
  flows,
  mode = "panel",
  onSelectFlow,
  selectedFlow,
}: {
  accent: string;
  flows: TaliyaLandingAgentFlow[];
  mode?: "panel" | "mobileSticky";
  onSelectFlow: (flowId: string, direction?: 1 | -1) => void;
  selectedFlow: TaliyaLandingAgentFlow;
}) {
  const flowTrackRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const track = flowTrackRef.current;
    const activeButton = track?.querySelector<HTMLButtonElement>(".agent-flow-tab.is-active");
    if (!track || !activeButton || track.scrollWidth <= track.clientWidth) return;

    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const activeCenter = activeButton.offsetLeft - track.offsetLeft + activeButton.offsetWidth / 2;
    const targetLeft = activeCenter - track.clientWidth / 2;
    track.scrollTo({ left: Math.max(0, targetLeft), behavior: prefersReducedMotion ? "auto" : "smooth" });
  }, [selectedFlow.id]);

  function moveFlow(direction: 1 | -1) {
    const selectedIndex = flows.findIndex((flowItem) => flowItem.id === selectedFlow.id);
    const nextIndex = (selectedIndex + direction + flows.length) % flows.length;
    const nextFlow = flows[nextIndex] ?? flows[0];
    if (nextFlow) onSelectFlow(nextFlow.id, direction);
  }

  return (
    <nav
      aria-label="Exemplos desta frente"
      className={`agent-flow-nav relative min-h-[4rem] min-w-0 max-w-full items-center overflow-hidden border-b border-[#E8E1D6] px-[0.58rem] py-[0.35rem] ${
        mode === "mobileSticky" ? "mobile-agent-flow-nav flex lg:hidden" : "hidden lg:flex"
      }`}
    >
      <button aria-label="Fluxo anterior" className="agent-flow-arrow absolute left-[0.58rem] top-1/2 z-10 grid h-10 w-10 -translate-y-1/2 place-items-center rounded-full border border-[#E2DED5] bg-white font-black text-[#101B3A] shadow-[0_8px_18px_rgba(16,27,58,0.05)] focus:outline-none focus:ring-4 focus:ring-[#101B3A]/10 lg:hidden" onClick={() => moveFlow(-1)} type="button">
        &lt;
      </button>
      <button aria-label="Próximo fluxo" className="agent-flow-arrow absolute right-[0.58rem] top-1/2 z-10 grid h-10 w-10 -translate-y-1/2 place-items-center rounded-full border border-[#E2DED5] bg-white font-black text-[#101B3A] shadow-[0_8px_18px_rgba(16,27,58,0.05)] focus:outline-none focus:ring-4 focus:ring-[#101B3A]/10 lg:hidden" onClick={() => moveFlow(1)} type="button">
        &gt;
      </button>
      <div className="agent-flow-viewport flex h-full min-w-0 w-full flex-1 items-center px-[2.8rem] lg:px-0">
        <div
          className="agent-flow-track -mb-8 flex min-w-0 max-w-full items-center justify-start gap-2 overflow-x-auto pb-8 max-lg:mb-0 max-lg:h-full max-lg:w-full max-lg:justify-center max-lg:overflow-visible max-lg:pb-0 lg:mb-0 lg:flex-nowrap lg:justify-start lg:overflow-visible lg:pb-0"
          ref={flowTrackRef}
          style={{ scrollbarWidth: "none" }}
        >
          {flows.map((flowItem, index) => {
            const isActive = flowItem.id === selectedFlow.id;
            return (
              <button
                aria-pressed={isActive}
                className={`agent-flow-tab min-h-[2.35rem] max-w-[14rem] shrink-0 items-center rounded-[0.85rem] border px-[0.78rem] py-[0.48rem] text-left transition focus:outline-none focus:ring-4 focus:ring-[#101B3A]/10 ${
                  isActive ? "is-active flex max-lg:w-full max-lg:max-w-none max-lg:justify-center max-lg:text-center" : "flex max-lg:hidden"
                }`}
                key={flowItem.id}
                onClick={() => {
                  const selectedIndex = flows.findIndex((item) => item.id === selectedFlow.id);
                  const nextIndex = flows.findIndex((item) => item.id === flowItem.id);
                  onSelectFlow(flowItem.id, nextIndex >= selectedIndex ? 1 : -1);
                }}
                style={{
                  backgroundColor: isActive ? accent : "#FFFFFF",
                  borderColor: isActive ? accent : "#E2DED5",
                  color: isActive ? "#FFFFFF" : "#101B3A",
                  marginLeft: 0,
                  marginRight: 0,
                }}
                type="button"
              >
                <span className="agent-flow-tab-name truncate text-sm font-black leading-tight tracking-[-0.035em]">{flowNavLabels[flowItem.code] ?? flowItem.displayTitle}</span>
                {isActive ? <span className="agent-flow-tab-count ml-2 hidden shrink-0 text-[0.62rem] font-black uppercase tracking-[0.12em] opacity-75 max-lg:block">Fluxo {index + 1} de {flows.length}</span> : null}
              </button>
            );
          })}
        </div>
      </div>
    </nav>
  );
}

function ChannelChips({ channels }: { channels: TaliyaLandingAgentFlow["channels"] }) {
  return (
    <div className="agent-channel-chips flex flex-wrap items-center gap-2">
      {channels.map((channel) => (
        <span className="rounded-full bg-[#ECFFF8] px-3 py-1.5 text-xs font-black text-[#087A61]" key={channel}>
          {channel}
        </span>
      ))}
    </div>
  );
}

function useScrollableArea<T extends HTMLElement>(items: unknown[]) {
  const ref = useRef<T>(null);
  const [hasOverflow, setHasOverflow] = useState(false);
  const [canScrollMore, setCanScrollMore] = useState(false);

  useEffect(() => {
    const node = ref.current;
    if (!node) return;

    const updateOverflow = () => {
      const nextHasOverflow = node.scrollHeight > node.clientHeight + SCROLL_OVERFLOW_EPSILON_PX;
      setHasOverflow(nextHasOverflow);
      setCanScrollMore(nextHasOverflow && node.scrollTop + node.clientHeight < node.scrollHeight - SCROLL_OVERFLOW_EPSILON_PX);
    };

    updateOverflow();
    const rafId = window.requestAnimationFrame(updateOverflow);
    const settleTimers = [120, 420, 860].map((delay) => window.setTimeout(updateOverflow, delay));

    const resizeObserver = new ResizeObserver(updateOverflow);
    resizeObserver.observe(node);

    const mutationObserver = new MutationObserver(updateOverflow);
    mutationObserver.observe(node, { childList: true, subtree: true, characterData: true });

    window.addEventListener("resize", updateOverflow);

    return () => {
      resizeObserver.disconnect();
      mutationObserver.disconnect();
      window.cancelAnimationFrame(rafId);
      settleTimers.forEach((timer) => window.clearTimeout(timer));
      window.removeEventListener("resize", updateOverflow);
    };
  }, [items]);

  return { canScrollMore, hasOverflow, onScroll: () => {
    const node = ref.current;
    if (!node) return;
    setCanScrollMore(node.scrollHeight > node.clientHeight + SCROLL_OVERFLOW_EPSILON_PX && node.scrollTop + node.clientHeight < node.scrollHeight - SCROLL_OVERFLOW_EPSILON_PX);
  }, ref };
}

function DetailRow({
  accent,
  items,
  label,
  tone = "plain",
}: {
  accent: string;
  items: string[];
  label: string;
  tone?: "plain" | "accent";
}) {
  const isAccent = tone === "accent";
  const { canScrollMore, hasOverflow, onScroll, ref } = useScrollableArea<HTMLUListElement>(items);

  return (
    <section
      className={`agent-detail-row ${isAccent ? "agent-result-row" : ""} grid gap-2.5 border-t px-4 py-2.5 first:border-t-0 sm:grid-cols-[9.5rem_minmax(0,1fr)] sm:gap-4 sm:px-5 sm:py-2.5 xl:grid-cols-[10.5rem_minmax(0,1fr)] ${
        isAccent ? "bg-[#101B3A] text-white" : "bg-white text-[#101B3A]"
      }`}
      style={{ borderColor: isAccent ? "#101B3A" : "#E8E1D6" }}
    >
      <div className="flex items-center gap-2 sm:items-start">
        <span className="mt-0.5 hidden h-2.5 w-2.5 shrink-0 rounded-full sm:block" style={{ backgroundColor: isAccent ? accent : "#D0D5DD" }} />
        <p className="text-[10px] font-black uppercase tracking-[0.17em]" style={{ color: isAccent ? "#7BE0C8" : "#98A2B3" }}>
          {label}
        </p>
      </div>
      <div className={`agent-scroll-frame ${hasOverflow ? "is-scrollable" : ""} ${canScrollMore ? "can-scroll-more" : ""} ${hasOverflow && !canScrollMore ? "is-at-end" : ""}`}>
        <ul className={`agent-detail-list agent-scroll-area grid gap-1.5 ${hasOverflow ? "is-scrollable" : ""} ${canScrollMore ? "can-scroll-more" : "is-at-end"}`} onScroll={onScroll} ref={ref}>
          {items.map((item) => (
            <li className={`agent-detail-item flex gap-2.5 text-sm font-bold leading-[1.15rem] ${isAccent ? "text-white" : "text-[#101B3A]"}`} key={item}>
              <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full" style={{ backgroundColor: isAccent ? accent : "#B7C0CC" }} />
              <span>{formatPtBrCopy(item)}</span>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

function InsideFlowPaths({ accent, paths }: { accent: string; paths: TaliyaLandingAgentFlow["inside"] }) {
  const { canScrollMore, hasOverflow, onScroll, ref } = useScrollableArea<HTMLDivElement>(paths);

  if (!paths.length) return null;

  return (
    <section className="agent-paths-layer border-t border-[#E8E1D6] bg-[#FFFDF8] px-4 py-2.5 sm:px-5">
      <div className="grid gap-2.5 sm:grid-cols-[9.5rem_minmax(0,1fr)] sm:gap-4 xl:grid-cols-[10.5rem_minmax(0,1fr)]">
        <div className="flex items-center gap-2 sm:items-start">
          <span className="mt-0.5 hidden h-2.5 w-2.5 shrink-0 rounded-full sm:block" style={{ backgroundColor: accent }} />
          <p className="agent-paths-label text-[10px] font-black uppercase tracking-[0.17em] text-[#98A2B3]">Possíveis caminhos</p>
        </div>

        <div className={`agent-scroll-frame ${hasOverflow ? "is-scrollable" : ""} ${canScrollMore ? "can-scroll-more" : ""} ${hasOverflow && !canScrollMore ? "is-at-end" : ""}`}>
          <div className={`agent-paths-list agent-scroll-area grid gap-1.5 pl-0 ${hasOverflow ? "is-scrollable" : ""} ${canScrollMore ? "can-scroll-more" : "is-at-end"}`} data-path-count={paths.length} onScroll={onScroll} ref={ref}>
            {paths.map((path) => (
              <article
                className="agent-path-card-aligned min-w-0 rounded-[0.4rem] border py-1.5 pr-3"
                key={path.title}
                style={{ backgroundColor: "#FFFBF2", borderColor: "#EFE7DA", paddingLeft: "var(--agent-path-card-pad, 1.35rem)" }}
              >
                <p className="agent-path-copy min-w-0 text-sm font-bold leading-[1.15rem] text-[#667085]">
                  <span className="font-black text-[#101B3A]">{formatPtBrCopy(path.title)}: </span>
                  <span>{formatPtBrCopy(path.text)}</span>
                </p>
              </article>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function AgentMainPanel({
  accent,
  agentDirection,
  agentId,
  flowDirection,
  flows,
  onSelectFlow,
  selectedFlow,
}: {
  accent: string;
  agentDirection: 1 | -1;
  agentId: string;
  flowDirection: 1 | -1;
  flows: TaliyaLandingAgentFlow[];
  onSelectFlow: (flowId: string, direction?: 1 | -1) => void;
  selectedFlow: TaliyaLandingAgentFlow;
}) {
  return (
    <article
      className="agent-main-panel relative flex min-h-0 w-full min-w-0 max-w-full flex-col overflow-hidden rounded-[2.25rem] border border-[#E5DED2] bg-[#FFFDF8] shadow-[0_30px_80px_rgba(16,27,58,0.10)] lg:h-full"
      data-agent-direction={agentDirection}
      key={`agent-panel-${agentId}`}
    >
      <div className="pointer-events-none absolute -right-24 -top-24 h-64 w-64 rounded-full opacity-15 blur-3xl" style={{ backgroundColor: accent }} />
      <FlowNavigation accent={accent} flows={flows} onSelectFlow={onSelectFlow} selectedFlow={selectedFlow} />

      <div className="landing-panel-scroll relative flex min-h-0 flex-1 flex-col overflow-y-auto px-4 pb-32 pt-2 sm:px-5 sm:pb-32 sm:pt-2 lg:px-5 lg:pb-5 lg:pt-1 xl:px-6 xl:pb-6 xl:pt-1">
        <div className="agent-flow-content" data-flow-direction={flowDirection} key={`${agentId}-${selectedFlow.id}`}>
          <div className="agent-flow-heading border-b border-[#E8E1D6] pb-3">
            <div className="min-w-0">
              <div className="min-w-0">
                <div className="agent-flow-title-row flex min-w-0 flex-wrap items-center gap-2">
                  <h2 className="min-w-0 text-[clamp(1.65rem,2.7vw,2.75rem)] font-black leading-none tracking-[-0.07em] text-[#101B3A]" data-no-scroll-reveal>{formatPtBrCopy(selectedFlow.displayTitle)}</h2>
                  <ChannelChips channels={selectedFlow.channels} />
                </div>
                <p className="agent-flow-summary mt-2 max-w-full text-[0.86rem] font-bold leading-5 text-[#667085] lg:text-[0.9rem]" data-no-scroll-reveal>{formatPtBrCopy(selectedFlow.summary)}</p>
              </div>
            </div>
          </div>

          <div className="agent-flow-card mt-3 min-h-0 overflow-hidden rounded-[0.75rem] border border-[#E8E1D6] bg-white shadow-[0_18px_48px_rgba(16,27,58,0.06)]">
            <DetailRow accent={accent} items={selectedFlow.whenBullets} label="Quando acontece" />
            <DetailRow accent={accent} items={selectedFlow.doesBullets} label="A Taliya faz" />
            <InsideFlowPaths accent={accent} paths={selectedFlow.inside} />
            <DetailRow accent={accent} items={selectedFlow.outcomeBullets} label="Resultado" tone="accent" />
          </div>
        </div>
      </div>
    </article>
  );
}

export function AgentsDemoSection({
  agents,
  intro,
  selectedAgent,
  onSelectAgent,
}: {
  agents: Agent[];
  intro: {
    eyebrow: string;
    title: string;
    subtitle: string;
  };
  selectedAgent: Agent;
  onSelectAgent: (agentId: string) => void;
}) {
  const [touchState, setTouchState] = useState<CarouselTouchState | null>(null);
  const [transitionDirection, setTransitionDirection] = useState<1 | -1>(1);
  const [flowDirection, setFlowDirection] = useState<1 | -1>(1);
  const flows = useMemo(
    () =>
      taliyaFeaturedAgentFlowsByAgent[selectedAgent.id] ??
      (selectedAgent.operationalFlows?.length
        ? selectedAgent.operationalFlows.map(
            (flowItem) =>
              ({
                ...buildFallbackFlow(selectedAgent),
                ...flowItem,
                displayTitle: flowItem.title,
                channels: flowItem.channel === "hibrido" ? ["App", "WhatsApp"] : flowItem.channel === "sistema" ? ["App"] : ["WhatsApp"],
                when: flowItem.trigger,
                does: flowItem.action,
                outcome: flowItem.result,
                whenBullets: [flowItem.trigger],
                doesBullets: [flowItem.action],
                outcomeBullets: [flowItem.result],
                inside: [],
              }) satisfies TaliyaLandingAgentFlow,
          )
        : [buildFallbackFlow(selectedAgent)]),
    [selectedAgent],
  );
  const [selectedFlowState, setSelectedFlowState] = useState({ agentId: selectedAgent.id, flowId: flows[0]?.id ?? "" });
  const activeFlowId = selectedFlowState.agentId === selectedAgent.id ? selectedFlowState.flowId : flows[0]?.id;
  const selectedFlow = flows.find((flowItem) => flowItem.id === activeFlowId) ?? flows[0];
  const selectedVisual = agentVisual(selectedAgent);
  const accent = selectedVisual.accent;
  const activeAgentIndex = Math.max(0, agents.findIndex((agent) => agent.id === selectedAgent.id));
  const dragOffset = touchState?.intent === "horizontal" ? touchState.offsetX : 0;
  const dragDirection = Math.abs(dragOffset) >= SWIPE_COMMIT_PX ? (dragOffset < 0 ? 1 : -1) : null;

  function moveAgent(direction: 1 | -1) {
    if (!agents.length) return;
    setTransitionDirection(direction);
    setFlowDirection(direction);
    const nextIndex = (activeAgentIndex + direction + agents.length) % agents.length;
    const nextAgent = agents[nextIndex] ?? agents[0];
    if (nextAgent) onSelectAgent(nextAgent.id);
    resetAgentPanelScroll();
    scrollElementToTopOnMobile("#agentes .mobile-agent-nav");
  }

  function selectAgent(agentId: string) {
    const nextIndex = agents.findIndex((agent) => agent.id === agentId);
    const direction = nextIndex >= activeAgentIndex ? 1 : -1;
    setTransitionDirection(direction);
    setFlowDirection(direction);
    onSelectAgent(agentId);
    resetAgentPanelScroll();
    scrollElementToTopOnMobile("#agentes .mobile-agent-nav");
  }

  function selectFlow(flowId: string, direction?: 1 | -1) {
    const currentIndex = flows.findIndex((flowItem) => flowItem.id === selectedFlow.id);
    const nextIndex = flows.findIndex((flowItem) => flowItem.id === flowId);
    setFlowDirection(direction ?? (nextIndex >= currentIndex ? 1 : -1));
    setSelectedFlowState({ agentId: selectedAgent.id, flowId });
    resetAgentPanelScroll();
    scrollElementToTopOnMobile("#agentes .mobile-agent-flow-nav");
  }

  function handleAgentCarouselTouchStart(touch: Touch) {
    setTouchState({ startX: touch.clientX, startY: touch.clientY, offsetX: 0, intent: "pending" });
  }

  function handleAgentCarouselTouchMove(touch: Touch) {
    setTouchState((current) => {
      if (!current || current.intent === "vertical") return current;

      const deltaX = touch.clientX - current.startX;
      const deltaY = touch.clientY - current.startY;
      const absX = Math.abs(deltaX);
      const absY = Math.abs(deltaY);

      if (current.intent === "pending" && absY > SWIPE_INTENT_PX && absY > absX * 1.15) {
        return { ...current, intent: "vertical", offsetX: 0 };
      }

      if (current.intent === "pending" && (absX < SWIPE_INTENT_PX || absX < absY * 1.25)) {
        return current;
      }

      return {
        ...current,
        intent: "horizontal",
        offsetX: Math.max(-SWIPE_MAX_OFFSET_PX, Math.min(SWIPE_MAX_OFFSET_PX, deltaX)),
      };
    });
  }

  function handleAgentCarouselTouchEnd() {
    if (!touchState || touchState.intent !== "horizontal") {
      setTouchState(null);
      return;
    }

    const delta = touchState.offsetX;
    setTouchState(null);
    if (Math.abs(delta) < SWIPE_COMMIT_PX) return;
    moveAgent(delta < 0 ? 1 : -1);
  }

  return (
    <SectionShell id="agentes" tone="white" className="landing-take-section landing-roomy-section scroll-mt-36" contentClassName="py-2">
      <div className="landing-one-line-title agents-one-line-title reveal-step mx-auto mb-10 max-w-none lg:mb-16">
        <SectionIntro align="center" eyebrow={intro.eyebrow} title={intro.title} subtitle={intro.subtitle} />
      </div>
      <div className="agents-demo-shell grid min-w-0 gap-5">
        <div className="landing-mobile-sticky-nav landing-mobile-agent-selector reveal-step min-w-0 lg:sticky lg:top-24 lg:h-full lg:self-start">
          <AgentNavigation agents={agents} onSelectAgent={selectAgent} selectedAgent={selectedAgent} />
          <div className="landing-mobile-agent-sticky-stack lg:hidden">
            <MobileAgentNavigation activeIndex={activeAgentIndex} onMove={moveAgent} selectedAgent={selectedAgent} total={agents.length} />
            <FlowNavigation accent={accent} flows={flows} mode="mobileSticky" onSelectFlow={selectFlow} selectedFlow={selectedFlow} />
          </div>
        </div>

        <div
          className="reveal-step reveal-delay-1 min-w-0 lg:min-h-0"
          onTouchCancel={() => setTouchState(null)}
          onTouchEnd={handleAgentCarouselTouchEnd}
          onTouchMove={(event) => {
            const touch = event.touches[0];
            if (touch) handleAgentCarouselTouchMove(touch);
          }}
          onTouchStart={(event) => {
            const touch = event.touches[0];
            if (touch) handleAgentCarouselTouchStart(touch);
          }}
        >
          <div
            className={`topic-carousel-slide mobile-swipe-slide lg:h-full ${touchState?.intent === "horizontal" ? "is-dragging" : ""}`}
            data-agent-nav-id={`panel-${selectedAgent.id}`}
            data-direction={transitionDirection}
            key={selectedAgent.id}
            style={{ "--carousel-drag-x": `${dragOffset}px` } as CSSProperties}
          >
            <AgentMainPanel
              accent={accent}
              agentDirection={transitionDirection}
              agentId={selectedAgent.id}
              flowDirection={flowDirection}
              flows={flows}
              onSelectFlow={selectFlow}
              selectedFlow={selectedFlow}
            />
          </div>
          <AgentDots activeIndex={activeAgentIndex} agents={agents} dragDirection={dragDirection} onSelect={selectAgent} selectedAgent={selectedAgent} />
        </div>
      </div>
    </SectionShell>
  );
}
