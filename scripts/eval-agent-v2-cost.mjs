import { assert, contains, writeReport } from "./eval-agent-v2-utils.mjs";

const checks = [
  ...contains("lib/landing/ai-attendant/agent-v2-cost-policy.ts", ["hard_cap_blocked", "estimateCostUsd", "hardCapFallbackText"]),
  ...contains("lib/landing/ai-attendant/agent-v2-flags.ts", ["AI_ATTENDANT_V2_HARD_COST_CAP_USD", "0.15"]),
];

writeReport("agent-v2-cost", checks.map((check) => assert(check.found, `cost policy contains ${check.pattern}`)));
