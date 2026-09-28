import type { NicheLandingConfig } from "@/data/landing/niches/types";
import { SectionIntro } from "../shared/SectionIntro";
import { SectionShell } from "../shared/SectionShell";

export function FAQSection({
  config,
  onContactSupport,
}: {
  config: NicheLandingConfig;
  onContactSupport: () => void;
}) {
  const visibleFaq = config.faq;

  return (
    <SectionShell id="faq" tone="white" className="is-visible" contentClassName="max-w-[1180px]">
      <SectionIntro
        eyebrow="FAQ"
        title="Dúvidas antes de começar?"
        subtitle="Entenda os canais, o que fica registrado e os limites da proposta."
      />
      <div className="mt-10 grid gap-3 md:grid-cols-2">
        {visibleFaq.map((item) => (
          <details
            className="group rounded-[1.25rem] border border-[#E2DED5] bg-white p-5 shadow-sm transition hover:border-[#0E8F7E]/35 hover:shadow-md"
            key={item.question}
          >
            <summary className="flex cursor-pointer list-none items-start justify-between gap-4 text-base font-black leading-6 text-[#101B3A] marker:hidden sm:text-lg">
              <span>{item.question}</span>
              <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-[#EAF7F3] text-lg leading-none text-[#0E8F7E] transition group-open:rotate-45">
                +
              </span>
            </summary>
            <p className="mt-4 leading-7 text-[#667085]">{item.answer}</p>
          </details>
        ))}
      </div>
      <div className="mt-8 rounded-[1.4rem] border border-[#D9EEE8] bg-[#F3FBF8] p-5 shadow-sm sm:flex sm:items-center sm:justify-between sm:gap-5">
        <div>
          <p className="text-sm font-black uppercase tracking-[0.16em] text-[#0E8F7E]">Ficou alguma dúvida?</p>
          <p className="mt-2 max-w-2xl text-base font-bold leading-7 text-[#344054]">
            Quer saber como a Taliya pode se encaixar na sua rotina? Conte um pouco sobre o seu negócio.
          </p>
        </div>
        <a
          className="interactive-hit mt-4 inline-flex min-h-12 w-full items-center justify-center rounded-full bg-[#101B3A] px-5 text-sm font-black text-white transition hover:bg-[#18264F] focus:outline-none focus:ring-4 focus:ring-[#FFB21A]/20 sm:mt-0 sm:w-auto"
          href={`mailto:${config.footer.contactEmail}`}
          onClick={onContactSupport}
        >
          Falar com a equipe
        </a>
      </div>
    </SectionShell>
  );
}
