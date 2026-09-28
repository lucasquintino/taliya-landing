import { assert, contains, writeReport } from "./eval-agent-v2-utils.mjs";

const checks = [
  ...contains("lib/landing/ai-attendant/agent-v2-idempotency.ts", ["reserveAgentV2IdempotencyKey", "ON CONFLICT", "duplicate"]),
  ...contains("lib/landing/ai-attendant/agent-v2-loop.ts", ["duplicate_inbound", "completeAgentV2IdempotencyKey"]),
];

writeReport("agent-v2-idempotency", checks.map((check) => assert(check.found, `idempotency contains ${check.pattern}`)));

