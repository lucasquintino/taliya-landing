import type { NicheLandingConfig } from "@/data/landing/niches/types";
import { PriorityQueueMockup } from "../shared/PriorityQueueMockup";
import { SectionIntro } from "../shared/SectionIntro";
import { SectionShell } from "../shared/SectionShell";

export function CoverageSection({ config }: { config: NicheLandingConfig }) {
  return (
    <SectionShell id="cobertura" tone="white">
      <div className="grid gap-10 lg:grid-cols-[0.82fr_1.18fr] lg:items-center">
        <div className="reveal-step">
          <SectionIntro eyebrow="Operação conectada" title={config.coverage.title} subtitle={config.coverage.subtitle} />
        </div>
        <div className="reveal-step reveal-delay-2">
          <PriorityQueueMockup items={config.coverage.items} />
        </div>
      </div>
    </SectionShell>
  );
}
