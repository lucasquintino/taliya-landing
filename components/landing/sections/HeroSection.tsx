"use client";

import type { NicheLandingConfig } from "@/data/landing/niches/types";
import { TrackedLink } from "../shared/Header";

function renderHighlighted(headline: string, highlight: string) {
  const parts = headline.split(highlight);
  if (parts.length === 1) return headline;
  return (
    <>
      {parts[0]}
      <span className="bg-[linear-gradient(90deg,#635BFF_0%,#EF3E86_55%,#FFB21A_100%)] bg-clip-text text-transparent">
        {highlight}
      </span>
      {parts.slice(1).join(highlight)}
    </>
  );
}

export function HeroSection({
  config,
  isReady,
  onCta,
}: {
  config: NicheLandingConfig;
  isReady: boolean;
  onCta: (label: string, href: string) => void;
}) {
  return (
    <section
      className={`hero-stage relative isolate flex min-h-[calc(100svh-4.25rem)] items-center justify-center overflow-hidden bg-[#FFFDF8] px-4 py-10 sm:px-8 sm:py-14 lg:px-12 lg:py-16 ${isReady ? "is-ready" : "is-preparing"}`}
      id="top"
    >
      <div className="absolute inset-x-0 top-0 -z-10 h-[720px] bg-[radial-gradient(circle_at_22%_12%,rgba(255,178,26,0.16),transparent_27%),radial-gradient(circle_at_78%_8%,rgba(99,91,255,0.14),transparent_26%),linear-gradient(180deg,#FFFFFF_0%,#FFFDF8_58%,#FAF7F1_100%)]" />
      <div className="mx-auto w-[95vw] max-w-[1520px] lg:w-[80vw]">
        <div className="mx-auto text-center">
          <h1 className="hero-title mx-auto w-full break-words [overflow-wrap:anywhere] font-black text-[#101B3A]">
            {renderHighlighted(config.hero.headline, config.hero.highlight)}
          </h1>
          <p className="hero-message mx-auto mt-7 max-w-3xl text-2xl font-black tracking-[-0.035em] text-[#101B3A] sm:text-3xl">
            {config.hero.centralMessage}
          </p>
          {config.hero.subheadline ? (
            <p className="hero-subheadline mx-auto mt-4 max-w-3xl text-base font-bold leading-7 text-[#667085] sm:text-lg">
              {config.hero.subheadline}
            </p>
          ) : null}
          <div className="hero-actions mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <TrackedLink cta={config.hero.primaryCta} onCta={onCta} size="lg" variant="dark" />
            <TrackedLink cta={config.hero.secondaryCta} onCta={onCta} size="lg" variant="outline" />
          </div>
          {config.hero.proofNotes.length > 0 ? (
            <div className="hero-proof mt-5 flex flex-wrap justify-center gap-2 sm:mt-7 sm:gap-3">
              {config.hero.proofNotes.map((note) => (
                <span className="max-w-full rounded-full border border-[#E6E1D8] bg-white px-3 py-2 text-xs sm:px-4 sm:text-sm font-bold text-[#667085]" key={note}>
                  {note}
                </span>
              ))}
            </div>
          ) : null}
        </div>
      </div>
    </section>
  );
}
