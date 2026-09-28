import type { NicheLandingConfig } from "@/data/landing/niches/types";
import { IllustrationPanel } from "../shared/IllustrationPanel";
import { SectionShell } from "../shared/SectionShell";
import { StudentHistoryMockup } from "../shared/StudentHistoryMockup";

export function NicheSpecificSection({ config }: { config: NicheLandingConfig }) {
  return (
    <SectionShell id="pilates-real" tone="plain">
      <div className="grid gap-8 lg:grid-cols-[0.95fr_1.05fr] lg:items-center">
        <IllustrationPanel title={config.nicheSpecific.title} items={config.nicheSpecific.items} variant="studio" />
        <div>
          <p className="text-xs font-black uppercase tracking-[0.24em] text-[#0E8F7E]">Pilates de verdade</p>
          <h2 className="mt-4 text-[clamp(2.3rem,5vw,4.4rem)] font-black leading-[1] tracking-[-0.07em] text-[#101B3A]">
            {config.nicheSpecific.title}
          </h2>
          <p className="mt-5 text-lg leading-8 text-[#667085]">{config.nicheSpecific.description}</p>
          <div className="mt-8">
            <StudentHistoryMockup />
          </div>
        </div>
      </div>
    </SectionShell>
  );
}
