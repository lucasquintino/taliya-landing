"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import Image from "next/image";
import { agentVisualTokens } from "@/data/landing/agentVisuals";
import type { NicheLandingConfig, ProblemModeId } from "@/data/landing/niches/types";
import { SectionShell } from "../shared/SectionShell";

const agentMeta: Record<string, { token: keyof typeof agentVisualTokens; icon: string }> = {
  Atendimento: { token: "atendimento", icon: "M5 8h14M7 12h8M7 16h5M5 5h14v11H9l-4 3V5z" },
  Agenda: { token: "agenda", icon: "M7 3v3M17 3v3M4.5 8h15M6 5h12a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2ZM8.5 14l2 2 5-5" },
  Vendas: { token: "vendas", icon: "M5 12h14M13 6l6 6-6 6" },
  Financeiro: { token: "financeiro", icon: "M7 8h10M7 12h10M9 16h6M5 5h14v14H5z" },
  Retenção: { token: "retencao", icon: "M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM4 20c1.4-3.2 4.2-5 8-5s6.6 1.8 8 5" },
  Gestão: { token: "gestao", icon: "M4 18h16M7 15v-4M12 15V7M17 15v-6" },
  Histórico: { token: "historico", icon: "M12 8v5l3 2M21 12a9 9 0 1 1-3-6.7" },
};

export function ProblemDiagnosisSection({
  config,
  selectedMode,
  onSelectMode,
}: {
  config: NicheLandingConfig;
  selectedMode: ProblemModeId;
  onSelectMode: (mode: ProblemModeId) => void;
}) {
  const mode = config.diagnosis.modes.find((item) => item.id === selectedMode) ?? config.diagnosis.modes[0];
  const isGain = mode.tone === "gain";
  const [carouselIndex, setCarouselIndex] = useState(0);
  const [carouselDirection, setCarouselDirection] = useState<1 | -1>(1);
  const [hasScrollRevealed, setHasScrollRevealed] = useState(false);
  const revealAnchorRef = useRef<HTMLDivElement>(null);
  const activeIndex = carouselIndex % mode.cards.length;
  const activeCard = useMemo(() => mode.cards[activeIndex % mode.cards.length], [activeIndex, mode.cards]);
  const activeAgent = agentMeta[activeCard.agent] ?? agentMeta.Atendimento;
  const activeVisual = agentVisualTokens[activeAgent.token];
  const diagnosisImage = isGain ? "/diagnosis/com-agente.png" : "/diagnosis/sem-agente.png";

  useEffect(() => {
    const anchor = revealAnchorRef.current;
    if (!anchor) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry?.isIntersecting) return;
        setHasScrollRevealed(true);
        observer.disconnect();
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.12 },
    );

    observer.observe(anchor);
    return () => observer.disconnect();
  }, []);

  function moveCarousel(direction: 1 | -1) {
    setCarouselDirection(direction);
    setCarouselIndex((current) => (current + direction + mode.cards.length) % mode.cards.length);
  }

  function selectCarouselIndex(nextIndex: number) {
    setCarouselDirection(nextIndex >= activeIndex ? 1 : -1);
    setCarouselIndex(nextIndex);
  }

  return (
    <SectionShell id="diagnostico-operacional" tone="plain">
      <div className="flex flex-col gap-7 lg:flex-row lg:items-start lg:justify-between">
        <div className={`diagnosis-title-block reveal-step max-w-4xl ${hasScrollRevealed ? "is-step-visible" : ""}`} data-mobile-late-reveal data-no-scroll-reveal ref={revealAnchorRef}>
          <h2 className="text-[clamp(2.35rem,5.8vw,4.6rem)] font-light leading-[1.05] tracking-[-0.075em] text-[#101B3A]">
            {config.diagnosis.title}
          </h2>
          <p className="mt-4 max-w-3xl text-lg leading-8 text-[#667085]">{config.diagnosis.subtitle}</p>
        </div>
        <div
          className={`reveal-step reveal-delay-1 ${hasScrollRevealed ? "is-step-visible" : ""} mx-auto w-full max-w-[420px] lg:mx-0 lg:w-auto lg:max-w-none`}
          data-mobile-late-reveal
          data-no-scroll-reveal
        >
          <div
            className={`diagnosis-mode-toggle flex w-full rounded-full border bg-white p-1 shadow-[0_10px_28px_rgba(16,27,58,0.10)] ${
              isGain ? "border-[#0E8F7E]/55" : "border-[#FF8FB0]/70"
            }`}
          >
            {config.diagnosis.modes.map((item) => (
              <button
                className={`flex-1 rounded-full px-5 py-3 text-center text-sm font-black transition focus:outline-none focus:ring-2 lg:flex-none ${
                  item.id === selectedMode
                    ? item.tone === "loss"
                      ? "bg-[#FFB8CF] text-[#8A1538] focus:ring-[#E13B67]"
                      : "bg-[#BEEEDB] text-[#075E4D] focus:ring-[#0E8F7E]"
                    : "text-[#667085] hover:text-[#101B3A]"
                }`}
                key={item.id}
                onClick={() => onSelectMode(item.id)}
                type="button"
              >
                {item.label}
              </button>
            ))}
          </div>
          <p className="mt-2 text-center text-[0.62rem] font-black uppercase tracking-[0.16em] text-[#98A2B3]">Toque para trocar</p>
        </div>
      </div>
      <div className="diagnosis-layout">
        <div
          className={`diagnosis-card-shell reveal-step reveal-delay-2 ${hasScrollRevealed ? "is-step-visible" : ""} flex h-[300px] min-w-0 flex-col justify-between rounded-[2rem] border bg-white p-6 shadow-[0_24px_60px_rgba(16,27,58,0.07)] max-sm:h-[340px] max-sm:p-5 sm:h-[320px] ${
          isGain ? "border-[#0E8F7E]/35" : "border-[#FF5C8A]/55"
          }`}
          data-mobile-late-reveal
          data-no-scroll-reveal
        >
          <div className="flex items-start justify-between gap-4">
            <div className="flex items-center gap-3">
              <span
                className="grid h-11 w-11 shrink-0 place-items-center rounded-full"
                style={{ backgroundColor: activeVisual.soft, color: activeVisual.accent }}
              >
                <svg aria-hidden="true" className="h-5 w-5" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.15" viewBox="0 0 24 24">
                  <path d={activeAgent.icon} />
                </svg>
              </span>
              <div>
                <p className="text-[10px] font-black uppercase tracking-[0.18em] text-[#98A2B3]">Rotina</p>
                <p className="text-base font-black tracking-[-0.03em] text-[#101B3A]">{activeCard.agent}</p>
              </div>
            </div>
            <span className="rounded-full bg-[#F5F0E8] px-3 py-1 text-xs font-black text-[#667085]">
              {activeIndex + 1}/{mode.cards.length}
            </span>
          </div>

          <article
            className="diagnosis-card-content grid min-h-0 flex-1 grid-rows-[2rem_3.5rem] content-center gap-4 py-4"
            data-direction={carouselDirection}
            key={`${mode.id}-${activeIndex}-${activeCard.title}`}
          >
            <h3 className="h-8 truncate whitespace-nowrap text-[clamp(1.35rem,1.8vw,1.7rem)] font-black leading-8 tracking-[-0.045em] text-[#101B3A]">
              {activeCard.title}
            </h3>
            <p className="line-clamp-2 h-14 max-w-[640px] text-base leading-7 text-[#667085]">{activeCard.description}</p>
          </article>

          <div className="diagnosis-card-controls flex items-center justify-between gap-4">
            <div className="diagnosis-card-dots flex gap-0.5">
              {mode.cards.map((card, index) => (
                <button
                  aria-label={`Ir para ${card.agent}`}
                  className="grid h-10 w-10 place-items-center rounded-full transition focus:outline-none focus:ring-4 focus:ring-[#101B3A]/10"
                  key={`${mode.id}-${card.agent}`}
                  onClick={() => selectCarouselIndex(index)}
                  type="button"
                >
                  <span
                    className={`h-2.5 rounded-full transition-all ${
                      index === activeIndex
                        ? isGain
                          ? "w-8 bg-[#0E8F7E]"
                          : "w-8 bg-[#E13B67]"
                        : "w-2.5 bg-[#D8D2C8]"
                    }`}
                  />
                </button>
              ))}
            </div>
            <div className="diagnosis-card-arrows flex items-center gap-2">
              <button
                aria-label="Ver card anterior"
                className="grid h-10 w-10 place-items-center rounded-full border border-[#E2DED5] bg-white text-[#101B3A] shadow-[0_8px_20px_rgba(16,27,58,0.08)] transition hover:-translate-x-0.5 focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] max-sm:h-11 max-sm:w-11"
                onClick={() => moveCarousel(-1)}
                type="button"
              >
                &lt;
              </button>
              <button
                aria-label="Ver próximo card"
                className="grid h-10 w-10 place-items-center rounded-full border border-[#E2DED5] bg-white text-[#101B3A] shadow-[0_8px_20px_rgba(16,27,58,0.08)] transition hover:translate-x-0.5 focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] max-sm:h-11 max-sm:w-11"
                onClick={() => moveCarousel(1)}
                type="button"
              >
                &gt;
              </button>
            </div>
          </div>
        </div>
        <div className={`diagnosis-illustration-slot reveal-step reveal-delay-3 ${hasScrollRevealed ? "is-step-visible" : ""}`} data-mobile-late-reveal>
          <Image
            alt={isGain ? "Ilustração de uma rotina de Pilates organizada com Taliya." : "Ilustração de uma rotina de Pilates caótica sem Taliya."}
            className={`diagnosis-illustration ${
              isGain ? "diagnosis-illustration--gain" : "diagnosis-illustration--loss"
            }`}
            height={760}
            priority={false}
            sizes="(min-width: 1024px) 36vw, 90vw"
            src={diagnosisImage}
            unoptimized
            width={620}
          />
        </div>
      </div>
    </SectionShell>
  );
}
