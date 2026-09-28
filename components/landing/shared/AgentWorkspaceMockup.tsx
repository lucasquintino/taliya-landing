import type { Agent } from "@/data/landing/niches/types";
import { SaasPanelMockup } from "./SaasPanelMockup";

export function AgentWorkspaceMockup({ agent }: { agent: Agent }) {
  return (
    <div className="grid gap-5">
      <SaasPanelMockup
        title={agent.workspace.title}
        metric={agent.workspace.primaryMetric}
        label={agent.workspace.primaryMetricLabel}
        items={agent.workspace.queue}
      />
    </div>
  );
}
