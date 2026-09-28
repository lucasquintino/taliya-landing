import type { HumanControlMode, NicheLandingConfig } from "@/data/landing/niches/types";
import { HumanApprovalMockup } from "../shared/HumanApprovalMockup";
import { SectionIntro } from "../shared/SectionIntro";
import { SectionShell } from "../shared/SectionShell";

export function HumanControlSection({
  config,
  selectedMode,
  onSelectMode,
}: {
  config: NicheLandingConfig;
  selectedMode: HumanControlMode;
  onSelectMode: (modeId: string) => void;
}) {
  return (
    <SectionShell id="controle-humano" tone="warm">
      <div className="grid gap-8 lg:grid-cols-[0.82fr_1.18fr] lg:items-center">
        <div>
          <SectionIntro eyebrow="Humano no controle" title={config.humanControl.title} subtitle={config.humanControl.subtitle} />
          <div className="mt-7 flex flex-wrap gap-2 rounded-[1.6rem] border border-[#E2DED5] bg-white p-2 shadow-sm">
            {config.humanControl.modes.map((mode) => {
              const selected = selectedMode.id === mode.id;
              return (
                <button
                  className={`interactive-hit min-h-12 flex-1 rounded-[1.2rem] px-4 py-3 text-sm font-black transition focus:outline-none focus:ring-4 focus:ring-[#0E8F7E]/15 ${
                    selected ? "bg-[#101B3A] text-white shadow-[0_14px_30px_rgba(16,27,58,0.18)]" : "bg-[#FBF8F2] text-[#667085] hover:text-[#101B3A]"
                  }`}
                  key={mode.id}
                  onClick={() => onSelectMode(mode.id)}
                  type="button"
                >
                  {mode.label}
                </button>
              );
            })}
          </div>
          <div className="mt-5 grid gap-3">
            {selectedMode.actions.map((point) => (
              <div className="rounded-2xl border border-[#E2DED5] bg-white px-5 py-4 text-base font-black text-[#344054]" key={point}>
                {point}
              </div>
            ))}
          </div>
        </div>
        <HumanApprovalMockup mode={selectedMode} />
      </div>
    </SectionShell>
  );
}
