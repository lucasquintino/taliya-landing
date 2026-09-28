import type { NicheLandingConfig } from "@/data/landing/niches/types";
import { SectionShell } from "../shared/SectionShell";

export function SalesStartSection({
  config,
  onOpenAgent,
  onCta,
}: {
  config: NicheLandingConfig;
  onOpenAgent: () => void;
  onCta: (label: string, href: string) => void;
}) {
  const revealDelays = ["reveal-delay-1", "reveal-delay-2", "reveal-delay-3", "reveal-delay-4"];

  return (
    <>
      <SectionShell id="comecar" tone="white" className="!min-h-0 !py-10 sm:!py-12 lg:!items-center lg:!py-14 [@media(min-width:1024px)_and_(max-height:720px)]:!py-8" contentClassName="py-0">
        <div>
          <div className="mx-auto w-full text-center">
            <p className="text-xs font-black uppercase tracking-[0.24em] text-[#0E8F7E]">{config.salesSetup.eyebrow}</p>
            <h2 className="mt-4 text-[clamp(2.35rem,4.7vw,4.8rem)] font-black leading-[0.95] tracking-[-0.06em] text-[#101B3A]">
              {config.salesSetup.title}
            </h2>
            {config.salesSetup.subtitle ? (
              <p className="mx-auto mt-5 max-w-3xl text-lg font-bold leading-8 text-[#667085]">{config.salesSetup.subtitle}</p>
            ) : null}
          </div>

          <div className="sales-start-steps-grid mt-12 grid gap-5 md:grid-cols-2 xl:grid-cols-4">
            {config.salesSetup.steps.map((step, index) => (
              <article
                className={`sales-start-step reveal-step grid min-h-[22rem] grid-rows-[5.6rem_4.25rem_1fr] items-start rounded-[30px] border border-[#E2DED5] bg-white p-6 text-center shadow-[0_18px_45px_rgba(16,27,58,0.06)] sm:p-7 ${revealDelays[index] ?? ""}`}
                data-no-scroll-reveal
                key={step.title}
              >
                <span className="mx-auto grid h-16 w-16 place-items-center rounded-full bg-[#2FB7BE] text-2xl font-black text-white shadow-[0_18px_34px_rgba(47,183,190,0.28)]">
                  {index + 1}
                </span>
                <h3 className="mx-auto flex max-w-full items-center justify-center text-balance text-[1.35rem] font-black leading-7 tracking-[-0.04em] text-[#101B3A] xl:text-2xl">
                  {step.title}
                </h3>
                <p className="mx-auto max-w-[17rem] text-base font-medium leading-7 text-[#667085]">{step.description}</p>
              </article>
            ))}
          </div>

          {config.salesSetup.reassurance ? (
            <p className="mx-auto mt-8 max-w-3xl text-center text-sm font-black leading-6 text-[#667085]">{config.salesSetup.reassurance}</p>
          ) : null}
        </div>
      </SectionShell>

      <SectionShell id="vendas" tone="plain" className="!min-h-0 !py-10 sm:!py-12 lg:!items-center lg:!py-14" contentClassName="py-0">
        <div className="mx-auto max-w-6xl text-center">
          <h2 className="mx-auto max-w-5xl text-[clamp(3rem,6vw,6rem)] font-black leading-[0.92] tracking-[-0.075em] text-[#080A0F]">
            {config.salesCta.title}
          </h2>
          <p className="mx-auto mt-5 max-w-3xl text-lg font-bold leading-8 text-[#667085]">{config.salesCta.subtitle}</p>

          <div className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <button
              className="interactive-hit inline-flex min-h-16 w-full items-center justify-center gap-2 rounded-full bg-[#101B3A] px-8 text-base font-black leading-5 text-white shadow-[0_18px_42px_rgba(16,27,58,0.20)] transition hover:bg-[#17254B] focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] focus:ring-offset-2 sm:w-auto sm:min-w-[18rem] lg:min-w-[21rem] lg:px-10 lg:text-lg"
              onClick={onOpenAgent}
              type="button"
            >
              <span>{config.salesCta.primaryCta}</span>
              <span aria-hidden="true" className="shrink-0">→</span>
            </button>
            <a
              className="interactive-hit inline-flex min-h-16 w-full items-center justify-center gap-2 rounded-full border border-[#E2DED5] bg-white px-8 text-base font-black leading-5 text-[#101B3A] shadow-[0_14px_32px_rgba(16,27,58,0.08)] transition hover:border-[#0E8F7E]/40 focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] focus:ring-offset-2 sm:w-auto sm:min-w-[18rem] lg:min-w-[21rem] lg:px-10 lg:text-lg"
              href={config.hero.secondaryCta.href}
              onClick={() => onCta(config.salesCta.secondaryCta, config.hero.secondaryCta.href)}
            >
              <span>{config.salesCta.secondaryCta}</span>
              <span aria-hidden="true" className="shrink-0">→</span>
            </a>
          </div>

          <p className="mx-auto mt-5 max-w-2xl text-sm font-bold leading-6 text-[#667085]">{config.salesCta.microcopy}</p>
        </div>
      </SectionShell>
    </>
  );
}
