import type { GuidedStep } from "@/data/landing/niches/types";
import { BrowserFrame } from "./SaasPanelMockup";

export function FlowDiagram({ steps }: { steps: GuidedStep[] }) {
  return (
    <div className="grid gap-5 lg:grid-cols-[0.86fr_1.14fr] lg:items-start">
      <div className="relative grid gap-4">
        <div className="absolute bottom-8 left-6 top-8 hidden w-px bg-[#DAD5CC] sm:block" />
        {steps.map((step, index) => (
          <div className={`reveal-step reveal-delay-${Math.min(index + 1, 6)} relative flex gap-4 rounded-[1.5rem] border border-[#E2DED5] bg-white p-5 shadow-sm`} key={step.title}>
            <div className="z-10 grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-[#101B3A] text-sm font-black text-white">
              0{index + 1}
            </div>
            <div>
              <h3 className="text-xl font-black tracking-[-0.03em] text-[#101B3A]">{step.title}</h3>
              <p className="mt-2 text-sm leading-6 text-[#667085]">{step.description}</p>
            </div>
          </div>
        ))}
      </div>
      <BrowserFrame title="Fluxo assistido">
        <div className="grid gap-4 bg-[#FBF8F2] p-5 sm:grid-cols-2 sm:p-6">
          {steps.map((step, index) => (
            <div className={`reveal-step reveal-delay-${Math.min(index + 2, 7)} rounded-[1.5rem] border border-[#E6E1D8] bg-white p-4`} key={step.screenTitle}>
              <p className="text-xs font-black uppercase tracking-[0.16em] text-[#0E8F7E]">Etapa 0{index + 1}</p>
              <h4 className="mt-2 text-lg font-black text-[#101B3A]">{step.screenTitle}</h4>
              <div className="mt-4 grid gap-2">
                {step.screenItems.map((item) => (
                  <span className="rounded-xl bg-[#F2F4F7] px-3 py-2 text-sm font-bold text-[#344054]" key={item}>{item}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </BrowserFrame>
    </div>
  );
}
