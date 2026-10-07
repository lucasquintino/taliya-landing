"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import type { CSSProperties, ReactNode, Touch } from "react";
import { agentVisualTokens } from "@/data/landing/agentVisuals";
import type { Agent, AutonomousFlowMockup, AutonomousFlowStep, HowItWorksTopic, NicheLandingConfig } from "@/data/landing/niches/types";
import { AgendaScreen } from "../copiloto-ui/screens/AgendaScreen";
import type { AgendaEntry, DayOption } from "../copiloto-ui/ui/agenda";
import { SectionIntro } from "../shared/SectionIntro";
import { SectionShell } from "../shared/SectionShell";

const SYNC_STEP_MS = 2000;
const SWIPE_COMMIT_PX = 72;
const SWIPE_INTENT_PX = 12;
const SWIPE_MAX_OFFSET_PX = 76;

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

const agentIcons: Record<string, string> = {
  atendimento: "M5 8h14M7 12h8M7 16h5M5 5h14v11H9l-4 3V5z",
  agenda: "M7 3v3M17 3v3M4.5 8h15M6 5h12a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2ZM8.5 14l2 2 5-5",
  financeiro: "M7 8h10M7 12h10M9 16h6M5 5h14v14H5z",
  vendas: "M5 12h14M13 6l6 6-6 6",
  retencao: "M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM4 20c1.4-3.2 4.2-5 8-5s6.6 1.8 8 5",
  historico: "M12 8v5l3 2M21 12a9 9 0 1 1-3-6.7",
  gestao: "M4 18h16M7 15v-4M12 15V7M17 15v-6",
};

const agentTeamBullets: Record<string, string[]> = {
  atendimento: ["Entende mensagens", "Responde dúvidas simples", "Registra interessados", "Aciona rotina ou humano"],
  agenda: ["Registra faltas", "Anota reposição", "Encaixa alunos", "Avisa responsável"],
  vendas: ["Acompanha interessados", "Marca experimental", "Faz próximo contato", "Cria pré-matrícula"],
  financeiro: ["Monitora vencimentos", "Envia lembretes", "Confere pagamentos", "Renova planos"],
  retencao: ["Detecta alunos sumindo", "Detecta alunos inativos", "Chama de volta", "Marca retorno"],
  gestao: ["Mostra rotina do dia", "Resume a semana", "Aponta gargalos", "Sugere próxima ação"],
  "historico-evolucao": ["Organiza ficha", "Resumo pré-aula", "Registra observações", "Atualiza evolução"],
};

const agentMiniAssets: Record<string, string> = {
  atendimento: "/agents/mini/atendimento.png",
  agenda: "/agents/mini/agenda.png",
  vendas: "/agents/mini/vendas.png",
  financeiro: "/agents/mini/financeiro.png",
  retencao: "/agents/mini/retencao.png",
  gestao: "/agents/mini/gestao.png",
  "historico-evolucao": "/agents/mini/historico-evolucao.png",
};

function Icon({ path }: { path: string }) {
  return (
    <svg aria-hidden="true" className="h-5 w-5" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.1" viewBox="0 0 24 24">
      <path d={path} />
    </svg>
  );
}

function AgentIcon({ agentId }: { agentId: string }) {
  return <Icon path={agentIcons[agentId] ?? agentIcons.atendimento} />;
}

function TopicNavigation({ activeIndex, onSelect, topics }: { activeIndex: number; onSelect: (index: number) => void; topics: HowItWorksTopic[] }) {
  return (
    <aside className="hidden h-full rounded-[2rem] border border-[#E5DED2] bg-white/80 p-3.5 shadow-[0_22px_60px_rgba(16,27,58,0.08)] backdrop-blur xl:p-4 lg:flex lg:flex-col">
      <div className="px-2 pb-3">
        <p className="text-[11px] font-black uppercase tracking-[0.24em] text-[#101B3A]">Navegue pelos tópicos</p>
        <p className="mt-1 text-[0.62rem] font-black uppercase tracking-[0.16em] text-[#98A2B3]">Toque para trocar</p>
      </div>
      <div className="grid min-w-0 flex-1 grid-rows-6 gap-2">
        {topics.map((topic, index) => {
          const isActive = index === activeIndex;
          return (
            <button
              aria-pressed={isActive}
              className={`group relative flex h-full min-h-0 w-full max-w-full items-center gap-3 overflow-hidden rounded-[1.35rem] border px-3 py-3 pr-8 text-left transition duration-200 focus:outline-none focus:ring-4 focus:ring-[#101B3A]/10 ${isActive ? "shadow-[0_12px_24px_rgba(16,27,58,0.10)]" : "border-transparent hover:-translate-y-0.5 hover:bg-[#FFFDF8]"}`}
              key={topic.id}
              onClick={() => onSelect(index)}
              style={isActive ? { backgroundColor: topic.soft, borderColor: topic.accent } : undefined}
              type="button"
            >
              <span className="grid h-11 w-11 shrink-0 place-items-center rounded-full transition group-hover:scale-105" style={{ backgroundColor: isActive ? "#FFFFFF" : topic.soft, color: topic.accent }}>
                <Icon path={topic.icon} />
              </span>
              <span className="flex min-w-0 max-w-full flex-1 flex-col justify-center overflow-hidden">
                <span className="block max-w-full truncate text-[0.95rem] font-black leading-tight tracking-[-0.045em] text-[#101B3A] xl:text-[1.02rem]">{topic.label}</span>
                {isActive && topic.navSubtitle ? (
                  <span className="mt-1.5 block w-full max-w-full truncate whitespace-nowrap text-[0.7rem] font-bold leading-tight text-[#667085] xl:text-[0.72rem]">{topic.navSubtitle}</span>
                ) : null}
              </span>
              <span className="absolute right-3 top-1/2 h-2.5 w-2.5 -translate-y-1/2 rounded-full" style={{ backgroundColor: isActive ? topic.accent : "#CBD2DC" }} />
            </button>
          );
        })}
      </div>
    </aside>
  );
}

function MobileNavigation({ onMove, topic }: { onMove: (direction: 1 | -1) => void; topic: HowItWorksTopic }) {
  return (
    <div className="mobile-topic-nav flex min-h-[4.25rem] min-w-0 items-center rounded-[1.35rem] border border-[#E5DED2] bg-white px-[0.58rem] py-[0.58rem] shadow-[0_16px_35px_rgba(16,27,58,0.08)]">
      <div className="grid w-full grid-cols-[2.35rem_minmax(0,1fr)_2.35rem] items-center justify-items-center gap-[0.45rem]">
        <button aria-label="Tópico anterior" className="grid h-[2.35rem] w-[2.35rem] shrink-0 place-items-center rounded-full border border-[#E2DED5] bg-[#FFFDF8] font-black text-[#101B3A]" onClick={() => onMove(-1)} type="button">&lt;</button>
        <div className="flex min-w-0 w-full flex-col items-center justify-center text-center">
          <p className="mobile-topic-title truncate text-[0.94rem] font-black leading-[1rem] tracking-[-0.03em]" style={{ color: topic.accent }}>{topic.label}</p>
          {topic.navSubtitle ? <p className="mobile-topic-subtitle mt-1 truncate text-[0.67rem] font-bold leading-[0.84rem] text-[#667085]">{topic.navSubtitle}</p> : null}
        </div>
        <button aria-label="Próximo tópico" className="grid h-[2.35rem] w-[2.35rem] shrink-0 place-items-center rounded-full border border-[#E2DED5] bg-[#FFFDF8] font-black text-[#101B3A]" onClick={() => onMove(1)} type="button">&gt;</button>
      </div>
    </div>
  );
}

function Dots({
  activeIndex,
  dragDirection,
  onSelect,
  topic,
  total,
}: {
  activeIndex: number;
  dragDirection: 1 | -1 | null;
  onSelect: (index: number) => void;
  topic: HowItWorksTopic;
  total: number;
}) {
  const label = dragDirection === null ? "Arraste na horizontal para trocar" : dragDirection > 0 ? "Solte para ver o próximo tópico" : "Solte para voltar ao tópico anterior";

  return (
    <div className="mt-4 min-w-0 rounded-[1.35rem] border border-[#E5DED2] bg-white/75 px-4 py-3 shadow-[0_14px_30px_rgba(16,27,58,0.06)] lg:hidden">
      <p className={`text-center text-[0.72rem] font-black uppercase tracking-[0.16em] transition-colors ${dragDirection === null ? "text-[#98A2B3]" : "text-[#101B3A]"}`}>{label}</p>
      <div className="mt-1 flex justify-center gap-0.5">
        {Array.from({ length: total }).map((_, index) => (
          <button
            aria-label={`Ir para tópico ${index + 1}`}
            className="grid h-10 w-10 place-items-center rounded-full transition focus:outline-none focus:ring-4 focus:ring-[#101B3A]/10"
            key={index}
            onClick={() => onSelect(index)}
            type="button"
          >
            <span
              className={`h-2.5 rounded-full transition-all ${index === activeIndex ? "w-8" : "w-2.5 bg-[#D8D2C8]"}`}
              style={index === activeIndex ? { backgroundColor: topic.accent } : undefined}
            />
          </button>
        ))}
      </div>
    </div>
  );
}

function ConceptVisual({ topic }: { topic: HowItWorksTopic }) {
  const [activeStep, setActiveStep] = useState(0);
  const steps = [
    { label: "Pedir", text: "Diga o que precisa por voz ou texto, pelo app ou WhatsApp." },
    { label: "Entender", text: "A Taliya interpreta o seu pedido." },
    { label: "Responder", text: "Retorna com a informação ou ação concluída." },
    { label: "Organizar", text: "Deixa os registros e atualizações organizados no app." },
  ];
  const currentStep = steps[activeStep] ?? steps[0];

  return (
    <div className="concept-visual grid h-full content-center gap-3">
      <div className="concept-visual-definition how-topic-visual-part relative overflow-hidden rounded-[1.55rem] border border-[#E5DED2] bg-white p-4 shadow-[0_16px_36px_rgba(16,27,58,0.06)]">
        <span className="absolute -right-10 -top-12 h-28 w-28 rounded-full" style={{ backgroundColor: topic.soft }} />
        <p className="relative text-xs font-black uppercase tracking-[0.18em]" style={{ color: topic.accent }}>Do seu pedido à rotina organizada</p>
        <p className="relative mt-2 max-w-3xl text-lg font-black leading-6 tracking-[-0.045em] text-[#101B3A]">
          Você fala ou escreve o que precisa. A Taliya entende o pedido e consulta os registros do seu negócio.
        </p>
      </div>
      <div className="concept-visual-comparison grid gap-3 md:grid-cols-[0.95fr_1.05fr]">
        <div className="how-topic-mini-card relative overflow-hidden rounded-[1.35rem] border border-[#F0A7BE] bg-white p-4 shadow-[0_18px_42px_rgba(225,59,103,0.08)]">
          <span className="absolute -right-6 -top-6 h-24 w-24 rounded-full bg-[#FFE6EF]" />
          <p className="relative text-xs font-black uppercase tracking-[0.2em] text-[#E13B67]">WhatsApp</p>
          <h3 className="relative mt-3 text-[2rem] font-black leading-[0.9] tracking-[-0.08em] text-[#101B3A]">Converse.</h3>
          <p className="relative mt-3 text-sm font-bold leading-5 text-[#667085]">Fale com a Taliya por mensagem ou áudio.</p>
        </div>
        <div className="how-topic-mini-card relative overflow-hidden rounded-[1.35rem] border border-[#D5DCE8] bg-white p-4 shadow-[0_18px_42px_rgba(16,27,58,0.08)]">
          <span className="absolute -right-6 -top-6 h-24 w-24 rounded-full bg-[#EEF1F6]" />
          <p className="relative text-xs font-black uppercase tracking-[0.2em] text-[#536071]">App</p>
          <h3 className="relative mt-3 text-[2rem] font-black leading-[0.9] tracking-[-0.08em] text-[#101B3A]">Acompanhe.</h3>
          <p className="relative mt-3 text-sm font-bold leading-5 text-[#667085]">Consulte seus clientes, serviços, agenda e registros.</p>
        </div>
      </div>
      <div className="concept-visual-taliya how-topic-visual-part relative overflow-hidden rounded-[1.55rem] border p-4 shadow-[0_22px_52px_rgba(16,27,58,0.12)]" style={{ borderColor: topic.accent, backgroundColor: topic.soft }}>
        <span className="absolute -right-8 -top-8 h-28 w-28 rounded-full bg-white/80" />
        <div className="relative grid gap-4 md:grid-cols-[minmax(0,0.62fr)_minmax(0,1.38fr)] md:items-center">
          <div>
            <p className="text-xs font-black uppercase tracking-[0.2em]" style={{ color: topic.accent }}>Taliya</p>
            <h3 className="mt-3 text-[2.25rem] font-black leading-[0.9] tracking-[-0.08em] text-[#101B3A]">Integra.</h3>
            <p className="mt-3 text-sm font-bold leading-5 text-[#667085]">Você pede, a Taliya entende, responde e deixa tudo organizado no app.</p>
          </div>
          <div className="how-topic-visual-part rounded-[1.25rem] border border-white/80 bg-white/72 p-3 shadow-sm">
            <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
              {steps.map((step, index) => {
                const isActive = index === activeStep;
                return (
                  <button
                    aria-pressed={isActive}
                    className={`concept-step-button how-topic-interactive flex h-[5.55rem] min-w-10 flex-col items-center justify-center rounded-2xl px-1.5 py-2.5 text-center outline-none transition-colors focus:ring-4 focus:ring-[#101B3A]/10 ${isActive ? "bg-[#101B3A] text-white shadow-[0_10px_20px_rgba(16,27,58,0.14)]" : "bg-[#F8F5EF] text-[#101B3A] hover:bg-white"}`}
                    key={step.label}
                    onClick={() => setActiveStep(index)}
                    onMouseEnter={() => setActiveStep(index)}
                    type="button"
                  >
                    <span className="mx-auto grid h-8 w-8 place-items-center rounded-full text-xs font-black" style={{ backgroundColor: isActive ? "#FFFFFF" : topic.accent, color: isActive ? topic.accent : "#FFFFFF" }}>{index + 1}</span>
                    <span className="mt-2 block max-w-full text-center text-[0.68rem] font-black leading-tight sm:text-[0.66rem] xl:text-[0.72rem]">{step.label}</span>
                  </button>
                );
              })}
            </div>
            <p className="how-topic-interactive mt-2 flex min-h-[2.25rem] items-center justify-center rounded-2xl bg-white px-3 py-2 text-center text-xs font-black leading-4 text-[#101B3A]">
              {currentStep.text}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

function focusAgentInSection(agentId: string) {
  const section = document.getElementById("agentes");
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  section?.scrollIntoView({ behavior: prefersReducedMotion ? "auto" : "smooth", block: "start" });
  window.history.replaceState(null, "", "#agentes");

  window.setTimeout(() => {
    const target = Array.from(document.querySelectorAll<HTMLElement>(`[data-agent-nav-id="${agentId}"]`)).find((node) => node.offsetParent !== null);
    if (target) {
      target.focus({ preventScroll: true });
      return;
    }

    section?.setAttribute("tabindex", "-1");
    section?.focus({ preventScroll: true });
  }, prefersReducedMotion ? 0 : 420);
}

function TeamVisual({ agents, onSelectAgent }: { agents: Agent[]; onSelectAgent: (agentId: string) => void }) {
  return (
    <div className="grid gap-2 sm:grid-cols-2">
      {agents.map((agent) => {
        const visual = agentVisualTokens[agent.id] ?? { accent: agent.accent, soft: "#F2F4F7" };
        const miniAgentSrc = agentMiniAssets[agent.id];
        return (
          <a
            className="agent-team-card group relative grid min-h-[6.55rem] grid-cols-[4.5rem_minmax(0,1fr)] gap-2.5 overflow-hidden rounded-[1.2rem] border border-[#E5DED2] bg-white p-2.5 shadow-[0_10px_24px_rgba(16,27,58,0.06)] transition hover:-translate-y-1 hover:shadow-[0_16px_34px_rgba(16,27,58,0.10)] focus:outline-none focus:ring-4 focus:ring-[#101B3A]/10"
            href="#agentes"
            key={agent.id}
            onClick={(event) => {
              event.preventDefault();
              onSelectAgent(agent.id);
              focusAgentInSection(agent.id);
            }}
            style={{ "--agent-accent": visual.accent } as React.CSSProperties}
          >
            <span className="pointer-events-none absolute inset-y-3 left-0 w-1 rounded-r-full bg-[var(--agent-accent)] opacity-0 transition group-hover:opacity-100 group-focus-visible:opacity-100" />
            <span className="absolute right-2.5 top-2.5 z-10 grid h-7 w-7 translate-x-1 place-items-center rounded-full bg-[#101B3A] text-sm font-black text-white opacity-0 transition group-hover:translate-x-0 group-hover:opacity-100 group-focus-visible:translate-x-0 group-focus-visible:opacity-100" aria-hidden="true">
              &gt;
            </span>
            <span className="relative flex h-full min-h-[4.75rem] w-[4.5rem] shrink-0 items-end justify-center overflow-visible rounded-[1rem] transition group-hover:scale-105" style={{ color: visual.accent }}>
              {miniAgentSrc ? (
                // Intentionally using a raw PNG path to preserve transparent assets without Next image optimization/WebP conversion.
                // eslint-disable-next-line @next/next/no-img-element
                <img
                  alt={`Mini agente ${agent.name}`}
                  className="h-[5.75rem] w-[4.2rem] object-contain object-bottom"
                  decoding="async"
                  loading="lazy"
                  src={miniAgentSrc}
                />
              ) : (
                <AgentIcon agentId={agent.id} />
              )}
            </span>
            <span className="min-w-0">
              <span className="block text-sm font-black tracking-[-0.04em] text-[#101B3A]">{agent.name}</span>
              <span className="mt-1.5 grid gap-0.5">
                {(agentTeamBullets[agent.id] ?? [agent.action]).slice(0, 4).map((bullet) => (
                  <span className="agent-team-bullet flex items-center gap-2 text-[0.68rem] font-bold leading-[0.9rem] text-[#667085]" key={bullet}>
                    <span className="h-1.5 w-1.5 shrink-0 rounded-full" style={{ backgroundColor: visual.accent }} />
                    <span className="truncate">{bullet}</span>
                  </span>
                ))}
              </span>
            </span>
          </a>
        );
      })}
    </div>
  );
}

function ProductCardsVisual({ cards, onSelectAgent }: { cards: NonNullable<HowItWorksTopic["productCards"]>; onSelectAgent: (agentId: string) => void }) {
  return (
    <div className="grid gap-2.5 sm:grid-cols-2">
      {cards.map((card) => {
        const visual = agentVisualTokens[card.agentId] ?? { accent: "#008C8C" };
        return (
          <a
            className="product-feature-card group relative grid min-h-[8rem] grid-cols-1 overflow-hidden rounded-[1.2rem] border border-[#E5DED2] bg-white p-3 shadow-[0_10px_24px_rgba(16,27,58,0.06)] transition hover:-translate-y-1 hover:shadow-[0_16px_34px_rgba(16,27,58,0.10)] focus:outline-none focus:ring-4 focus:ring-[#101B3A]/10"
            href="#agentes"
            key={card.id}
            onClick={(event) => {
              event.preventDefault();
              onSelectAgent(card.agentId);
              focusAgentInSection(card.agentId);
            }}
            style={{ "--agent-accent": visual.accent } as React.CSSProperties}
          >
            <span className="min-w-0">
              <span className="block text-sm font-black tracking-[-0.04em] text-[#101B3A]">{card.title}</span>
              <span className="mt-1.5 grid gap-1">
                {card.bullets.map((bullet) => (
                  <span className="flex items-start gap-2 text-[0.68rem] font-bold leading-[0.95rem] text-[#667085]" key={bullet}>
                    <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full" style={{ backgroundColor: visual.accent }} />
                    <span>{bullet}</span>
                  </span>
                ))}
              </span>
            </span>
            <span className="absolute right-2 top-2 z-10 grid h-6 w-6 translate-x-1 place-items-center rounded-full bg-[#101B3A] text-xs font-black text-white opacity-0 transition group-hover:translate-x-0 group-hover:opacity-100 group-focus-visible:translate-x-0 group-focus-visible:opacity-100" aria-hidden="true">
              &gt;
            </span>
          </a>
        );
      })}
    </div>
  );
}

function PilatesFocusVisual() {
  const [allowsMotion, setAllowsMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    const updateMotionPreference = () => setAllowsMotion(!mediaQuery.matches);

    updateMotionPreference();
    mediaQuery.addEventListener("change", updateMotionPreference);
    return () => mediaQuery.removeEventListener("change", updateMotionPreference);
  }, []);

  return (
    <div className="grid h-full content-center">
      <div className="how-topic-visual-part relative overflow-hidden rounded-[1.9rem] border border-[#E8D8C4] bg-[#FEFDF8] p-3 shadow-[0_22px_52px_rgba(138,92,46,0.13)]">
        <div className="pointer-events-none absolute -left-16 -top-16 h-44 w-44 rounded-full bg-[#FFF1DF] blur-2xl" />
        <div className="pointer-events-none absolute -bottom-14 -right-12 h-48 w-48 rounded-full bg-[#E8D8C4]/45 blur-2xl" />
        <div className="how-topic-visual-part relative flex items-center justify-between gap-3 px-2 pb-2">
          <span className="rounded-full bg-white px-3 py-1.5 text-[10px] font-black uppercase tracking-[0.16em] text-[#8A5C2E] shadow-sm">Rotina em andamento</span>
          <span className="rounded-full bg-[#101B3A] px-3 py-1.5 text-[10px] font-black uppercase tracking-[0.16em] text-white">Taliya em ação</span>
        </div>
        <div className="how-topic-visual-part relative aspect-[620/348] w-full overflow-hidden rounded-[1.45rem] sm:min-h-[20rem] xl:min-h-[22rem]">
          {allowsMotion ? (
            <video
              aria-hidden="true"
              autoPlay
              className="absolute inset-0 h-full w-full object-contain object-center mix-blend-multiply"
              loop
              muted
              playsInline
              poster="/illustrations/pilates-studio-poster.webp"
              preload="metadata"
            >
              <source src="/illustrations/pilates-studio-loop.webm" type="video/webm" />
              <source src="/illustrations/pilates-studio-loop.mp4" type="video/mp4" />
            </video>
          ) : (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              alt="Profissional atendendo enquanto a Taliya ajuda a organizar a rotina pelo WhatsApp e pelo app"
              className="absolute inset-0 h-full w-full object-contain object-center mix-blend-multiply"
              decoding="async"
              loading="lazy"
              src="/illustrations/pilates-studio-poster.webp"
            />
          )}
        </div>
        <div className="how-topic-visual-part relative mt-3 rounded-[1.3rem] border border-[#E8D8C4] bg-white/86 px-4 py-3 text-center shadow-[0_12px_28px_rgba(138,92,46,0.08)]">
          <p className="text-[clamp(1rem,1.25vw,1.2rem)] font-black leading-snug tracking-[-0.045em] text-[#101B3A]">
            A Taliya ajuda a organizar sua rotina e a preparar seu trabalho.
          </p>
        </div>
      </div>
    </div>
  );
}

function SettingsVisual({ topic }: { topic: HowItWorksTopic }) {
  const rows = topic.groups ?? [];

  return (
    <div className="settings-visual relative flex h-full flex-col overflow-visible rounded-[1.65rem] border border-[#E7D7B7] bg-white p-4 shadow-[0_22px_52px_rgba(16,27,58,0.10)]">
      <div className="settings-visual-header how-topic-visual-part relative flex items-center justify-between gap-3 border-b border-[#EFE3CC] pb-3.5">
        <div>
          <p className="text-[10px] font-black uppercase tracking-[0.18em]" style={{ color: topic.accent }}>{topic.eyebrow}</p>
          <p className="mt-1 text-lg font-black tracking-[-0.055em] text-[#101B3A]">Comece pelo básico</p>
        </div>
        <span className="rounded-full bg-[#101B3A] px-3 py-1.5 text-[10px] font-black uppercase tracking-[0.14em] text-white">opcional</span>
      </div>

      <div className="settings-visual-grid relative mt-3 grid gap-3 md:grid-cols-2">
        {rows.slice(0, 2).map((row, index) => (
          <div className="settings-visual-card how-topic-visual-part min-h-[13.4rem] rounded-[1.35rem] border border-[#EFE3CC] bg-[#FFFDF8] p-4" key={row.title}>
            <div className="flex items-start gap-3">
              <span className="grid h-10 w-10 shrink-0 place-items-center rounded-full text-sm font-black text-white" style={{ backgroundColor: topic.accent }}>{index + 1}</span>
              <div className="min-w-0">
                <p className="settings-visual-card-title text-[1.28rem] font-black uppercase leading-6 tracking-[-0.06em] text-[#101B3A]">{row.title}</p>
                {row.description ? <p className="settings-visual-card-copy mt-2 text-xs font-bold leading-4 text-[#667085]">{row.description}</p> : null}
              </div>
            </div>
            <ul className="mt-4 grid gap-2.5">
              {row.items.map((item) => (
                <li className="flex items-start gap-2 text-xs font-bold leading-5 text-[#667085]" key={item}>
                  <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full" style={{ backgroundColor: topic.accent }} />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      <div className="settings-visual-footer how-topic-visual-part relative mt-auto flex items-center gap-3 rounded-[1.2rem] border border-[#EAD7B2] bg-[#FFF8EA] px-4 py-3 text-xs font-black leading-5 text-[#5F4300]">
        <span className="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-[#101B3A] text-[10px] text-white">i</span>
        <span>Esta configuração é opcional. Se preferir, faça depois durante uma conversa com a Taliya.</span>
      </div>
    </div>
  );
}

function stepClass(step: AutonomousFlowStep) {
  if (step.type === "process") return "whatsapp-process-pill mx-auto flex max-w-[90%] items-center gap-1.5 rounded-full border border-[#E8D59D] bg-[#FFF8DF] px-2.5 py-1.5 text-[8px] font-black uppercase tracking-[0.07em] text-[#7A5600]";
  if (step.type === "notification") return "whatsapp-notification-card mx-auto max-w-[90%] rounded-[0.95rem] border border-[#CCE8DF] bg-[#ECFFF8] px-3 py-2 text-[9px] font-bold leading-3 text-[#0B6F61]";
  if (step.type === "switch") return "mx-auto max-w-[78%] rounded-full bg-white/85 px-3 py-1.5 text-center text-[9px] font-black text-[#667085]";
  if (step.actor === "student") return "mr-auto max-w-[80%] rounded-[0.95rem] rounded-bl-sm bg-white px-2.5 py-2 text-[10px] font-medium leading-3 text-[#111B21] shadow-sm";
  return "ml-auto max-w-[80%] rounded-[0.95rem] rounded-br-sm bg-[#D9FDD3] px-2.5 py-2 text-[10px] font-medium leading-3 text-[#111B21] shadow-sm";
}

function StepText({ step }: { step: AutonomousFlowStep }) {
  if (step.type === "process") return <><span className="text-[8px] font-black">IA</span><span>{step.text}</span></>;
  if (step.type === "notification") return <><p className="mb-0.5 text-[7px] font-black uppercase tracking-[0.12em] text-[#0E8F7E]">Sistema atualizado</p>{step.text}</>;
  if (step.type === "switch") return <span>{step.text}</span>;
  return <>{step.speaker ? <p className="mb-0.5 text-[9px] font-bold text-[#667781]">{step.speaker}</p> : null}{step.text}</>;
}

type AgendaDemoStage = "waiting" | "scheduled" | "rescheduled" | "cancelled" | "reminder";

function getAgendaDemoStage(visibleSteps: number): AgendaDemoStage {
  if (visibleSteps >= 10) return "reminder";
  if (visibleSteps >= 6) return "cancelled";
  if (visibleSteps >= 4) return "rescheduled";
  if (visibleSteps >= 2) return "scheduled";
  return "waiting";
}

function getLiveFlowIndex(visibleSteps: number) {
  if (visibleSteps >= 8) return 3;
  if (visibleSteps >= 6) return 2;
  if (visibleSteps >= 2) return 1;
  return 0;
}

function PhoneFrame({ children, compact = false }: { children: ReactNode; compact?: boolean }) {
  return (
    <div className={`mockup-float relative mx-auto w-full ${compact ? "channels-phone-frame max-w-none sm:max-w-[330px] xl:max-w-[348px] 2xl:max-w-[364px]" : "max-w-[322px] 2xl:max-w-[342px]"}`}>
      <div className={`relative rounded-[2.55rem] border border-black/20 bg-[#222] p-2 shadow-[0_26px_58px_rgba(16,27,58,0.20)] ${compact ? "channels-phone-shell phone-shell-compact h-[25.5rem] sm:h-[540px] xl:h-[560px] 2xl:h-[584px]" : "h-[558px] 2xl:h-[590px]"}`}>
        <div className="relative h-full overflow-hidden rounded-[1.9rem] border border-white/10 bg-[#0B141A]">
          <div className="absolute left-1/2 top-2 z-30 h-6 w-24 -translate-x-1/2 rounded-full bg-[#1D1F22] shadow-inner" />
          {children}
        </div>
      </div>
    </div>
  );
}

function CopilotoAgendaPhone({ stage, topic }: { stage: AgendaDemoStage; topic: HowItWorksTopic }) {
  const updates: Record<Exclude<AgendaDemoStage, "waiting">, { title: string; notification: string; item: string; time: string; date: string; kind: "service" | "reminder" }> = {
    scheduled: {
      title: "Horário marcado",
      notification: "Marina · atendimento · terça, às 14h.",
      item: "Atendimento · Marina",
      time: "14h · Horário confirmado",
      date: "Terça-feira, 15 de setembro",
      kind: "service",
    },
    rescheduled: {
      title: "Horário atualizado",
      notification: "Marina · atendimento · quarta, às 10h.",
      item: "Atendimento · Marina",
      time: "10h · Horário remarcado",
      date: "Quarta-feira, 16 de setembro",
      kind: "service",
    },
    cancelled: {
      title: "Horário cancelado",
      notification: "Marina · horário cancelado.",
      item: "",
      time: "",
      date: "",
      kind: "service",
    },
    reminder: {
      title: "Lembrete criado",
      notification: "Combinar uma nova data com Marina.",
      item: "Combinar uma nova data",
      time: "9h · Lembrete para Marina",
      date: "Segunda-feira, 14 de setembro",
      kind: "reminder",
    },
  };
  const update = stage === "waiting" ? null : updates[stage];
  const showScheduleEntry = stage === "scheduled" || stage === "rescheduled";
  const showReminderEntry = stage === "reminder";
  const dateId = stage === "scheduled" ? "2026-09-15" : stage === "rescheduled" ? "2026-09-16" : "2026-09-14";
  const days: DayOption[] = update && (showScheduleEntry || showReminderEntry)
    ? [{ id: dateId, weekday: stage === "scheduled" ? "Terça-feira" : stage === "rescheduled" ? "Quarta-feira" : "Segunda-feira", dayNumber: stage === "scheduled" ? "15" : stage === "rescheduled" ? "16" : "14", fullDate: update.date }]
    : [];
  const entries: AgendaEntry[] = showScheduleEntry && update
    ? [{ id: "marina-atendimento", kind: "timed", dateId, title: update.item, detail: update.time, startMinute: stage === "scheduled" ? 14 * 60 : 10 * 60, endMinute: stage === "scheduled" ? 15 * 60 : 11 * 60 }]
    : showReminderEntry && update
      ? [{ id: "marina-lembrete", kind: "due", dateId, dueMinute: 9 * 60, title: update.item, detail: "Lembrete para Marina" }]
      : [];
  return (
    <PhoneFrame compact>
      <div className="relative h-full w-full overflow-hidden bg-[#F4F8FA]">
        <div className="absolute left-0 top-0 h-[235%] w-[235%] origin-top-left scale-[0.425]">
          <div aria-label="Agenda do Copiloto" className="relative h-full overflow-hidden bg-[#F4F8FA] text-[#14182F]">
            <AgendaScreen
              days={days}
              entries={entries}
              selectedDateId={dateId}
            />
          </div>
        </div>
        {update ? (
          <>
            <div aria-live="polite" className="taliya-app-notifications pointer-events-none absolute left-2 right-2 top-[2rem] z-50 grid gap-1">
              <div className="taliya-app-notification-card how-topic-visual-part is-substep-visible rounded-[0.82rem] border border-[#DCE2EA] bg-white/95 px-2 py-1.5 shadow-[0_10px_24px_rgba(16,27,58,0.16)] backdrop-blur" key={`notification-${stage}`}>
                <div className="flex items-start gap-2">
                  <span className="grid h-4 w-4 shrink-0 place-items-center rounded-full text-[0.58rem] font-black text-white" style={{ backgroundColor: topic.accent }}>✓</span>
                  <span className="min-w-0">
                    <span className="taliya-app-notification-title block truncate text-[0.58rem] font-black uppercase tracking-[0.1em]" style={{ color: topic.accent }}>{update.title}</span>
                    <span className="taliya-app-notification-text block truncate text-[0.62rem] font-bold leading-3 text-[#657089]">{update.notification}</span>
                  </span>
                </div>
              </div>
            </div>
          </>
        ) : null}
      </div>
    </PhoneFrame>
  );
}

function WhatsAppClassPhone({
  flow,
  onTimelineChange,
  steps,
  timelineReady,
  timelineSteps,
  topic,
  visibleSteps,
}: {
  flow?: AutonomousFlowMockup;
  onTimelineChange: (stepCount: number) => void;
  steps: AutonomousFlowStep[];
  timelineReady: boolean;
  timelineSteps: number;
  topic: HowItWorksTopic;
  visibleSteps: number;
}) {
  const chatScrollRef = useRef<HTMLDivElement>(null);
  const visibleFlowSteps = useMemo(() => steps.slice(0, visibleSteps), [steps, visibleSteps]);
  const timelineFlowSteps = useMemo(() => steps.slice(0, timelineSteps), [steps, timelineSteps]);
  const activeContactName = useMemo(() => {
    const latestSwitch = timelineFlowSteps.findLast((step) => step.type === "switch");
    if (!latestSwitch) return flow?.contactName ?? "Pedro";
    const match = latestSwitch.text.match(/com\s+(.+)$/i);
    return match?.[1] ?? flow?.contactName ?? "Pedro";
  }, [flow?.contactName, timelineFlowSteps]);
  const initials = activeContactName.slice(0, 1).toUpperCase();

  useEffect(() => {
    const chatScroll = chatScrollRef.current;
    if (!chatScroll) return;
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    chatScroll.scrollTo({ top: chatScroll.scrollHeight, behavior: prefersReducedMotion ? "auto" : "smooth" });
  }, [visibleSteps]);

  function handleTimelineScroll() {
    const chatScroll = chatScrollRef.current;
    if (!chatScroll || !timelineReady) return;

    const stepNodes = Array.from(chatScroll.querySelectorAll<HTMLElement>("[data-flow-step-index]"));
    if (!stepNodes.length) return;

    const isAtBottom = chatScroll.scrollTop + chatScroll.clientHeight >= chatScroll.scrollHeight - 8;
    if (isAtBottom) {
      onTimelineChange(steps.length || 1);
      return;
    }

    const timelineLine = chatScroll.scrollTop + chatScroll.clientHeight * 0.52;
    const activeNode = stepNodes.reduce((current, node) => {
      return node.offsetTop <= timelineLine ? node : current;
    }, stepNodes[0]);
    const nextStep = Number(activeNode.dataset.flowStepIndex ?? 0) + 1;

    if (Number.isFinite(nextStep)) {
      onTimelineChange(Math.min(Math.max(nextStep, 1), steps.length || 1));
    }
  }

  return (
    <PhoneFrame compact>
      <div className="flex h-full flex-col bg-[#F0E9DF]">
        <div className="flex h-10 shrink-0 items-center justify-between bg-[#0B141A] px-5 pt-2 text-[10px] font-black text-white">
          <span>12:30</span>
          <span className="flex items-center gap-1.5"><span className="h-2 w-3 rounded-sm border border-white/70" /><span className="h-2 w-3 rounded-sm border border-white/70 bg-white/80" /></span>
        </div>
        <div className="flex shrink-0 items-center gap-2 bg-[#075E54] px-3 py-2 text-white">
          <span className="text-lg leading-none">&lt;</span>
          <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-white/95 text-[11px] font-black ring-2 ring-white/70" style={{ color: topic.accent }}>{initials}</span>
          <div className="min-w-0 flex-1">
            <p className="truncate text-[13px] font-black">{activeContactName}</p>
            <p className="truncate text-[10px] text-white/75">Assistente do seu negócio</p>
          </div>
          <span className="h-2 w-2 rounded-full bg-white/80" />
          <span className="h-2 w-2 rounded-full bg-white/80" />
        </div>
        <div ref={chatScrollRef} className="whatsapp-chat-bg min-h-0 flex-1 space-y-2 overflow-y-auto p-2.5 scroll-smooth" onScroll={handleTimelineScroll}>
          <div className="sticky top-0 z-10 mx-auto w-fit rounded-full bg-[#D9EAF4]/90 px-3 py-1 text-[10px] font-bold text-[#5B6B73] backdrop-blur">HOJE</div>
          {visibleFlowSteps.map((step, index) => <div className={`chat-line ${stepClass(step)}`} data-flow-step-index={index} key={`${step.type}-${index}`}><StepText step={step} /></div>)}
          {visibleSteps < steps.length ? <div className="typing-pill mr-auto flex w-fit items-center rounded-[1rem] rounded-bl-sm bg-white px-3.5 py-3 shadow-sm"><span /><span /><span /></div> : null}
        </div>
        <div className="flex shrink-0 items-center gap-2 bg-[#F0E9DF] px-2.5 py-2">
          <div className="grid h-7 w-7 place-items-center rounded-full bg-white text-[10px] font-black text-[#667781]">:)</div>
          <div className="flex min-h-8 flex-1 items-center rounded-full bg-white px-3 text-[11px] font-semibold text-[#8696A0] shadow-inner">Mensagem ou áudio</div>
          <div className="grid h-8 w-8 place-items-center rounded-full text-white" style={{ backgroundColor: topic.accent }}>&gt;</div>
        </div>
        <div className="flex h-6 shrink-0 items-center justify-center bg-[#F0E9DF]"><div className="h-1 w-24 rounded-full bg-black/80" /></div>
      </div>
    </PhoneFrame>
  );
}

function LiveFlowBanner({ topic, visibleSteps }: { topic: HowItWorksTopic; visibleSteps: number }) {
  const activeIndex = getLiveFlowIndex(visibleSteps);
  const steps = [
    "Você pede um horário",
    "Taliya entende e responde",
    "Agenda atualizada",
    "Você acompanha no app",
  ];

  return (
    <div className="live-flow-banner relative px-1 py-1">
      <div className="grid gap-1.5 min-[1400px]:grid-cols-[1fr_auto_1fr_auto_1fr_auto_1fr] min-[1400px]:items-center">
        {steps.map((step, index) => {
          const isDone = index < activeIndex;
          const isCurrent = index === activeIndex;
          const isLit = isDone || isCurrent;
          return (
            <div className="contents" key={step}>
              <div
                className={`live-flow-step flex min-h-[2.15rem] items-center gap-2 rounded-[0.95rem] border px-2.5 py-1.5 text-[0.66rem] font-black leading-tight transition ${isCurrent ? "live-flow-current" : ""}`}
                style={{
                  backgroundColor: isLit ? topic.soft : "#FFFFFF",
                  borderColor: isLit ? topic.accent : "#EEE7DD",
                  color: isLit ? topic.accent : "#667085",
                  boxShadow: isCurrent ? `0 0 0 3px ${topic.soft}, 0 10px 18px rgba(16,27,58,0.07)` : "none",
                }}
              >
                <span
                  className="grid h-5 w-5 shrink-0 place-items-center rounded-full text-[0.6rem] font-black"
                  style={{ backgroundColor: isLit ? topic.accent : "#F1EDE6", color: isLit ? "#FFFFFF" : "#98A2B3" }}
                >
                  {isDone ? "✓" : index + 1}
                </span>
                <span>{step}</span>
              </div>
              {index < steps.length - 1 ? <span className="hidden text-center text-lg font-black text-[#CFC8BC] min-[1400px]:block">→</span> : null}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function ChannelsVisual({ flow, topic }: { flow?: AutonomousFlowMockup; topic: HowItWorksTopic }) {
  const steps = useMemo(() => flow?.steps ?? [], [flow]);
  const getInitialStepCount = () => {
    if (typeof window === "undefined") return 1;
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches ? steps.length || 1 : 1;
  };
  const [visibleSteps, setVisibleSteps] = useState(getInitialStepCount);
  const [timelineSteps, setTimelineSteps] = useState(getInitialStepCount);
  const appStage = getAgendaDemoStage(visibleSteps);
  const timelineReady = Boolean(steps.length) && visibleSteps >= steps.length;

  useEffect(() => {
    if (steps.length <= 1) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if (visibleSteps >= steps.length) return;
    const timeout = window.setTimeout(() => {
      const nextStep = Math.min(visibleSteps + 1, steps.length);
      setVisibleSteps(nextStep);
      setTimelineSteps(nextStep);
    }, SYNC_STEP_MS);
    return () => window.clearTimeout(timeout);
  }, [steps.length, visibleSteps]);

  return (
    <div className="channels-visual-stack grid min-w-0 gap-2">
      <LiveFlowBanner topic={topic} visibleSteps={visibleSteps} />
      <div className="channels-phone-grid grid min-w-0 grid-cols-[minmax(0,1fr)_minmax(0,1fr)] items-start justify-items-stretch gap-0 sm:justify-items-center sm:gap-3 xl:gap-4">
        <div className="channels-phone-column grid w-full min-w-0 justify-items-center gap-1.5">
          <p className="text-[0.68rem] font-black uppercase tracking-[0.18em] text-[#98A2B3]">Converse com a Taliya</p>
          <WhatsAppClassPhone
            flow={flow}
            onTimelineChange={setTimelineSteps}
            steps={steps}
            timelineReady={timelineReady}
            timelineSteps={timelineSteps}
            topic={topic}
            visibleSteps={visibleSteps}
          />
        </div>
        <div className="channels-phone-column grid w-full min-w-0 justify-items-center gap-1.5">
          <p className="text-[0.68rem] font-black uppercase tracking-[0.18em] text-[#98A2B3]">Seu negócio no app</p>
          <CopilotoAgendaPhone stage={appStage} topic={topic} />
        </div>
      </div>
    </div>
  );
}

type AutomationModeKey = "manual" | "copiloto";
type AutomationRoutineKey = "clientes" | "servicos" | "agenda" | "recebimentos" | "documentos" | "lembretes" | "resumos" | "listagens";

const modeScenes: Record<
  AutomationModeKey,
  {
    label: string;
    shortLabel: string;
    title: string;
    description: string;
    badgeTone: "amber" | "purple";
  }
> = {
  manual: {
    label: "Manual",
    shortLabel: "Pelo app",
    title: "Organize sua rotina direto pelo app.",
    description: "Cadastre e consulte clientes, serviços, horários, recebimentos e documentos no app.",
    badgeTone: "amber",
  },
  copiloto: {
    label: "Copiloto",
    shortLabel: "App + WhatsApp",
    title: "Peça pelo WhatsApp. Acompanhe pelo app.",
    description: "Envie texto ou áudio para a Taliya organizar o pedido e deixar os registros disponíveis no app.",
    badgeTone: "purple",
  },
};

const modeToneStyles = {
  amber: {
    accent: "#C8890A",
    soft: "#FFF4D8",
    border: "#E8C986",
    badge: "bg-[#FFF4D8] text-[#8A5C00] border-[#E8C986]",
  },
  purple: {
    accent: "#6F4E7C",
    soft: "#F0E8F4",
    border: "#D9C4E2",
    badge: "bg-[#F0E8F4] text-[#6F4E7C] border-[#D9C4E2]",
  },
};

const routineStories: Record<
  AutomationRoutineKey,
  {
    label: string;
    modes: Record<AutomationModeKey, { result: string; steps: string[] }>;
  }
> = {
  clientes: {
    label: "Clientes",
    modes: {
      manual: {
        steps: ["Abra Clientes no app", "Busque pelo nome", "Consulte contato e histórico", "Atualize os dados"],
        result: "Os dados e registros do cliente ficam reunidos no app.",
      },
      copiloto: {
        steps: ["Pergunte pelo cliente", "A Taliya localiza o cadastro", "Veja os dados disponíveis", "Consulte o histórico no app"],
        result: "Você encontra o contexto do cliente na conversa e no app.",
      },
    },
  },
  servicos: {
    label: "Serviços",
    modes: {
      manual: {
        steps: ["Abra Serviços no app", "Escolha avulso, pacote ou plano", "Inclua valores e detalhes", "Salve para consultar ou orçar"],
        result: "Os formatos e detalhes dos serviços ficam organizados no app.",
      },
      copiloto: {
        steps: ["Conte o que você oferece", "A Taliya organiza os dados", "Defina avulso, pacote ou plano", "Revise os detalhes no app"],
        result: "A lista de serviços fica pronta para você revisar e usar em orçamentos.",
      },
    },
  },
  agenda: {
    label: "Agenda",
    modes: {
      manual: {
        steps: ["Abra a agenda no app", "Escolha cliente e serviço", "Marque, remarque ou cancele", "Confira os horários"],
        result: "Os horários e suas alterações ficam registrados na agenda.",
      },
      copiloto: {
        steps: ["Peça para marcar ou alterar", "Informe cliente e serviço", "A Taliya organiza o horário", "Acompanhe a agenda no app"],
        result: "O registro do horário fica disponível para você acompanhar no app.",
      },
    },
  },
  recebimentos: {
    label: "Recebimentos",
    modes: {
      manual: {
        steps: ["Abra o serviço no app", "Registre o valor recebido", "Vincule ao cliente", "Crie lembrete se precisar"],
        result: "Recebimentos e lembretes ficam registrados para acompanhamento.",
      },
      copiloto: {
        steps: ["Informe o valor recebido", "A Taliya registra o pagamento", "Peça lembrete de cobrança", "Consulte os registros no app"],
        result: "O pagamento informado e o lembrete ficam organizados no app.",
      },
    },
  },
  documentos: {
    label: "Documentos",
    modes: {
      manual: {
        steps: ["Abra Documentos no app", "Crie ou atualize um orçamento", "Anexe contrato ou arquivo", "Consulte pelo cliente"],
        result: "Orçamentos e arquivos ficam ligados ao cliente para consulta.",
      },
      copiloto: {
        steps: ["Peça para criar um orçamento", "Informe serviço e valores", "A Taliya prepara o documento", "Revise e acompanhe no app"],
        result: "O orçamento fica organizado para você revisar e acompanhar.",
      },
    },
  },
  lembretes: {
    label: "Lembretes",
    modes: {
      manual: {
        steps: ["Abra Lembretes no app", "Escolha cliente ou serviço", "Defina quando lembrar", "Consulte o próximo passo"],
        result: "O lembrete fica ligado ao contexto para você retomar na data escolhida.",
      },
      copiloto: {
        steps: ["Peça um lembrete por texto ou áudio", "Diga se é cobrança ou retorno", "Informe quando lembrar", "Acompanhe pelo app"],
        result: "O lembrete fica registrado com o cliente e o motivo informado.",
      },
    },
  },
  resumos: {
    label: "Resumos",
    modes: {
      manual: {
        steps: ["Abra Resumos no app", "Escolha o período", "Consulte horários e lembretes", "Confira serviços e recebimentos"],
        result: "O resumo reúne informações registradas para o período escolhido.",
      },
      copiloto: {
        steps: ["Peça um resumo do período", "A Taliya reúne os registros", "Inclui horários e lembretes", "Consulte a resposta no app"],
        result: "O resumo considera os dados registrados, como serviços e recebimentos informados.",
      },
    },
  },
  listagens: {
    label: "Listagens",
    modes: {
      manual: {
        steps: ["Abra Listagens no app", "Escolha o tipo de consulta", "Filtre cliente ou período", "Confira os registros"],
        result: "Você consulta horários, serviços, orçamentos e recebimentos registrados.",
      },
      copiloto: {
        steps: ["Peça uma lista pelo WhatsApp", "Diga o tipo e o período", "A Taliya reúne os registros", "Acompanhe a resposta no app"],
        result: "A lista mostra os dados encontrados para a consulta que você pediu.",
      },
    },
  },
};

function ModesVisual() {
  const modeKeys = ["manual", "copiloto"] as const;
  const routineKeys = ["clientes", "servicos", "agenda", "recebimentos", "documentos", "lembretes", "resumos", "listagens"] as const;
  const [activeMode, setActiveMode] = useState<AutomationModeKey>("manual");
  const [activeRoutine, setActiveRoutine] = useState<AutomationRoutineKey>("agenda");
  const [isRoutineMenuOpen, setIsRoutineMenuOpen] = useState(false);
  const scene = modeScenes[activeMode];
  const routine = routineStories[activeRoutine];
  const routineMode = routine.modes[activeMode];
  const tone = modeToneStyles[scene.badgeTone];

  return (
    <div className="modes-visual relative grid h-full min-h-0 content-center gap-4">
        <div className="how-topic-visual-part rounded-[1.55rem] border p-4 shadow-[0_16px_34px_rgba(16,27,58,0.05)]" style={{ backgroundColor: tone.soft, borderColor: tone.border }}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="text-[0.62rem] font-black uppercase tracking-[0.2em] text-[#98A2B3]">1. Modo de uso</p>
              <h3 className="mt-1 text-[1.32rem] font-black leading-none tracking-[-0.06em] text-[#101B3A]">Como você prefere usar a Taliya?</h3>
            </div>
            <span className={`shrink-0 rounded-full border px-2.5 py-1 text-[0.62rem] font-black uppercase tracking-[0.12em] ${tone.badge}`}>{scene.shortLabel}</span>
          </div>

          <div className="how-topic-interactive mt-4 grid grid-cols-2 rounded-full border p-1" style={{ backgroundColor: tone.soft, borderColor: tone.border }}>
            {modeKeys.map((mode) => {
              const isActive = activeMode === mode;

              return (
                <button
                  aria-pressed={isActive}
                  className="rounded-full px-2 py-2.5 text-[0.72rem] font-black transition focus:outline-none focus:ring-4 focus:ring-[#101B3A]/10"
                  key={mode}
                  onClick={() => setActiveMode(mode)}
                  style={{
                    backgroundColor: isActive ? tone.accent : "rgba(255,255,255,0.58)",
                    boxShadow: isActive ? "0 10px 20px rgba(16,27,58,0.16)" : "none",
                    color: isActive ? "#FFFFFF" : "#667085",
                  }}
                  type="button"
                >
                  {modeScenes[mode].label}
                </button>
              );
            })}
          </div>

          <div className="how-topic-visual-part mt-4 rounded-[1.15rem] border border-white/70 bg-white/75 px-3.5 py-3">
            <p className="text-[1.12rem] font-black leading-none tracking-[-0.055em] text-[#101B3A]">{scene.title}</p>
            <p className="mt-1.5 text-[0.78rem] font-bold leading-4 text-[#667085]">{scene.description}</p>
          </div>

        </div>

        <div className="how-topic-visual-part rounded-[1.55rem] border border-[#EEE7DD] bg-[#FFFDF8] p-4 shadow-[0_16px_34px_rgba(16,27,58,0.05)]">
          <div>
            <div className="relative max-w-[20rem]">
              <p className="text-[0.62rem] font-black uppercase tracking-[0.2em] text-[#98A2B3]">2. Frente do negócio</p>
              <button
                aria-expanded={isRoutineMenuOpen}
                className="mt-1 flex w-full items-center justify-between gap-3 border-b-2 pb-1.5 text-left text-[1.34rem] font-black leading-none tracking-[-0.06em] focus:outline-none focus:ring-4 focus:ring-[#101B3A]/10"
                onClick={() => setIsRoutineMenuOpen((current) => !current)}
                style={{ borderColor: tone.accent, color: tone.accent }}
                type="button"
              >
                <span>{routine.label}</span>
                <svg aria-hidden="true" className="h-4 w-4 shrink-0" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.4" viewBox="0 0 24 24">
                  <path d={isRoutineMenuOpen ? "M18 15l-6-6-6 6" : "M6 9l6 6 6-6"} />
                </svg>
              </button>
              {isRoutineMenuOpen ? (
                <div className="absolute left-0 top-full z-20 mt-0 w-full border border-t-0 border-[#E5DED2] bg-white shadow-[0_18px_42px_rgba(16,27,58,0.13)]">
                  {routineKeys.map((routineKey) => (
                    <button
                      className="block w-full px-3.5 py-2.5 text-left text-[1.05rem] font-black leading-tight tracking-[-0.055em] transition hover:bg-[#FFF8E8]"
                      key={routineKey}
                      onClick={() => {
                        setActiveRoutine(routineKey);
                        setIsRoutineMenuOpen(false);
                      }}
                      style={{
                        backgroundColor: activeRoutine === routineKey ? "#FFFDF8" : "#FFFFFF",
                        color: tone.accent,
                      }}
                      type="button"
                    >
                      {routineStories[routineKey].label}
                    </button>
                  ))}
                </div>
              ) : null}
            </div>
          </div>

          <div className="mt-4 grid gap-2.5 sm:grid-cols-2">
            {routineMode.steps.map((step, index) => (
              <div className="how-topic-mini-card grid min-h-[3.15rem] grid-cols-[1.8rem_minmax(0,1fr)] items-center gap-2 rounded-[1rem] border border-[#EEE7DD] bg-white px-2.5 py-2" key={step}>
                <span className="grid h-7 w-7 place-items-center rounded-full text-[0.7rem] font-black text-white" style={{ backgroundColor: tone.accent }}>{index + 1}</span>
                <span className="text-[0.72rem] font-black leading-[0.9rem] text-[#101B3A]">{step}</span>
              </div>
            ))}
          </div>

          <div className="how-topic-visual-part mt-3 rounded-[1rem] px-3.5 py-2.5 text-[0.78rem] font-black leading-4 text-[#101B3A]" style={{ backgroundColor: tone.soft, border: `1px solid ${tone.border}` }}>
            Resultado: {routineMode.result}
          </div>
        </div>
    </div>
  );
}

function TopicVisual({ agents, flow, onSelectAgent, topic }: { agents: Agent[]; flow?: AutonomousFlowMockup; onSelectAgent: (agentId: string) => void; topic: HowItWorksTopic }) {
  if (topic.visual === "agents-explained") return <ConceptVisual topic={topic} />;
  if (topic.visual === "pilates-focus") return <PilatesFocusVisual />;
  if (topic.visual === "agent-team") return topic.productCards ? <ProductCardsVisual cards={topic.productCards} onSelectAgent={onSelectAgent} /> : <TeamVisual agents={agents} onSelectAgent={onSelectAgent} />;
  if (topic.visual === "settings") return <SettingsVisual topic={topic} />;
  if (topic.visual === "channels") return <ChannelsVisual flow={flow} topic={topic} />;
  return <ModesVisual />;
}

function TopicPanel({ agents, flow, onSelectAgent, topic }: { agents: Agent[]; flow?: AutonomousFlowMockup; onSelectAgent: (agentId: string) => void; topic: HowItWorksTopic }) {
  const hasWideVisual = topic.visual === "modes";

  if (topic.visual === "channels") {
    return (
      <article className="relative min-w-0 overflow-hidden rounded-[2.5rem] border border-[#E5DED2] bg-[#FFFDF8] p-5 shadow-[0_30px_80px_rgba(16,27,58,0.10)] sm:p-7 lg:h-full lg:max-h-full lg:min-h-0 lg:p-6 xl:p-7">
        <div className="pointer-events-none absolute -right-24 -top-24 h-64 w-64 rounded-full opacity-20 blur-3xl" style={{ backgroundColor: topic.accent }} />
        <div className="channels-topic-layout relative grid h-full min-h-0 gap-4">
          <div className="channels-topic-copy min-w-0">
            <h2 className="max-w-xl text-[clamp(2rem,2.75vw,3.25rem)] font-black leading-[0.94] tracking-[-0.085em] text-[#101B3A]">{topic.title}</h2>
            <p className="mt-3 max-w-xl text-sm font-semibold leading-6 text-[#667085] xl:text-[0.95rem] xl:leading-6">{topic.description}</p>
            <div className="mt-4 grid gap-2">
              {topic.points.map((point) => <div className="how-topic-bullet flex items-start gap-3 rounded-2xl border border-[#EEE7DD] bg-white/78 px-3.5 py-2 text-xs font-bold leading-5 text-[#344054] xl:text-[0.82rem]" key={point}><span className="mt-1.5 h-2 w-2 shrink-0 rounded-full" style={{ backgroundColor: topic.accent }} /><span>{point}</span></div>)}
            </div>
          </div>
          <div className="channels-topic-visual min-w-0 min-h-0"><TopicVisual agents={agents} flow={flow} onSelectAgent={onSelectAgent} topic={topic} /></div>
        </div>
      </article>
    );
  }

  return (
    <article className="relative min-w-0 overflow-hidden rounded-[2.5rem] border border-[#E5DED2] bg-[#FFFDF8] p-5 shadow-[0_30px_80px_rgba(16,27,58,0.10)] sm:p-7 lg:h-full lg:max-h-full lg:min-h-0 lg:p-6 xl:p-7">
      <div className="pointer-events-none absolute -right-24 -top-24 h-64 w-64 rounded-full opacity-20 blur-3xl" style={{ backgroundColor: topic.accent }} />
      <div className={`relative grid h-full min-h-0 gap-6 lg:items-center ${hasWideVisual ? "lg:grid-cols-[minmax(0,0.45fr)_minmax(0,0.55fr)] xl:gap-7" : "lg:grid-cols-[minmax(0,0.47fr)_minmax(0,0.53fr)] xl:gap-8"}`}>
        <div className="min-w-0">
          <h2 className="max-w-xl text-[clamp(2rem,2.85vw,3.35rem)] font-black leading-[0.94] tracking-[-0.085em] text-[#101B3A]">{topic.title}</h2>
          <p className="mt-3 max-w-xl text-sm font-semibold leading-6 text-[#667085] xl:text-[0.95rem] xl:leading-6">{topic.description}</p>
          <div className="mt-4 grid gap-2">
            {topic.points.map((point) => <div className="how-topic-bullet flex items-start gap-3 rounded-2xl border border-[#EEE7DD] bg-white/78 px-3.5 py-2 text-xs font-bold leading-5 text-[#344054] xl:text-[0.82rem]" key={point}><span className="mt-1.5 h-2 w-2 shrink-0 rounded-full" style={{ backgroundColor: topic.accent }} /><span>{point}</span></div>)}
          </div>
        </div>
        <div className="min-w-0"><TopicVisual agents={agents} flow={flow} onSelectAgent={onSelectAgent} topic={topic} /></div>
      </div>
    </article>
  );
}

export function HowItWorksSection({ config, onSelectAgent }: { config: NicheLandingConfig; onSelectAgent: (agentId: string) => void }) {
  const [activeIndex, setActiveIndex] = useState(0);
  const [touchState, setTouchState] = useState<CarouselTouchState | null>(null);
  const [transitionDirection, setTransitionDirection] = useState<1 | -1>(1);
  const topics = config.howItWorks.topics;
  const activeTopic = topics[activeIndex] ?? topics[0];
  const flow = activeTopic.demoPainId ? config.pains.find((pain) => pain.id === activeTopic.demoPainId)?.autonomousFlow : undefined;
  const dragOffset = touchState?.intent === "horizontal" ? touchState.offsetX : 0;
  const dragDirection = Math.abs(dragOffset) >= SWIPE_COMMIT_PX ? (dragOffset < 0 ? 1 : -1) : null;

  function moveTopic(direction: 1 | -1) {
    setTransitionDirection(direction);
    setActiveIndex((current) => (current + direction + topics.length) % topics.length);
    scrollElementToTopOnMobile("#como-funciona .mobile-topic-nav");
  }

  function selectTopic(nextIndex: number) {
    setTransitionDirection(nextIndex >= activeIndex ? 1 : -1);
    setActiveIndex(nextIndex);
    scrollElementToTopOnMobile("#como-funciona .mobile-topic-nav");
  }

  function handleCarouselTouchStart(touch: Touch) {
    setTouchState({ startX: touch.clientX, startY: touch.clientY, offsetX: 0, intent: "pending" });
  }

  function handleCarouselTouchMove(touch: Touch) {
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

  function handleCarouselTouchEnd() {
    if (!touchState || touchState.intent !== "horizontal") {
      setTouchState(null);
      return;
    }

    const delta = touchState.offsetX;
    setTouchState(null);
    if (Math.abs(delta) < SWIPE_COMMIT_PX) return;
    moveTopic(delta < 0 ? 1 : -1);
  }

  return (
    <SectionShell id="como-funciona" tone="warm" className="landing-take-section landing-roomy-section" contentClassName="py-2">
      <div className="landing-one-line-title reveal-step mx-auto mb-10 max-w-4xl lg:mb-16">
        <SectionIntro align="center" eyebrow="Como funciona" title={config.howItWorks.title} subtitle={config.howItWorks.subtitle} />
      </div>
    <div className="how-it-works-stage grid min-w-0 gap-5 lg:grid-cols-[18rem_minmax(0,1fr)] lg:items-stretch xl:grid-cols-[20.5rem_minmax(0,1fr)]">
        <div className="reveal-step min-w-0 lg:sticky lg:top-24 lg:h-full lg:self-start">
          <TopicNavigation activeIndex={activeIndex} onSelect={selectTopic} topics={topics} />
        </div>
        <div className="landing-mobile-sticky-nav landing-mobile-topic-selector reveal-step min-w-0 lg:hidden">
          <MobileNavigation onMove={moveTopic} topic={activeTopic} />
        </div>
        <div
          className="reveal-step reveal-delay-2 min-w-0 lg:min-h-0"
          onTouchCancel={() => setTouchState(null)}
          onTouchEnd={handleCarouselTouchEnd}
          onTouchMove={(event) => {
            const touch = event.touches[0];
            if (touch) handleCarouselTouchMove(touch);
          }}
          onTouchStart={(event) => {
            const touch = event.touches[0];
            if (touch) handleCarouselTouchStart(touch);
          }}
        >
          <div
            className={`topic-carousel-slide mobile-swipe-slide min-w-0 lg:h-full ${touchState?.intent === "horizontal" ? "is-dragging" : ""}`}
            data-direction={transitionDirection}
            key={activeTopic.id}
            style={{ "--carousel-drag-x": `${dragOffset}px` } as CSSProperties}
          >
            <TopicPanel agents={config.agents} flow={flow} onSelectAgent={onSelectAgent} topic={activeTopic} />
          </div>
          <Dots activeIndex={activeIndex} dragDirection={dragDirection} onSelect={selectTopic} topic={activeTopic} total={topics.length} />
        </div>
      </div>
    </SectionShell>
  );
}
