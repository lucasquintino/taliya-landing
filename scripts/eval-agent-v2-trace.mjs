import { assert, contains, writeReport } from "./eval-agent-v2-utils.mjs";

const checks = [
  ...contains("lib/landing/ai-attendant/agent-v2-trace-store.ts", ["recordAgentV2Trace", "agent_v2_traces", "product_source_version"]),
  ...contains("lib/landing/ai-attendant/agent-v2-loop.ts", ["semanticInterpretation", "orchestrationDecision", "deliveryResult"]),
];

writeReport("agent-v2-trace", checks.map((check) => assert(check.found, `trace path contains ${check.pattern}`)));

