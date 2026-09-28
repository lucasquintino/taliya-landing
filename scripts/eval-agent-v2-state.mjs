import { assert, contains, writeReport } from "./eval-agent-v2-utils.mjs";

const checks = contains("lib/landing/ai-attendant/agent-v2-types.ts", [
  "diagnostic_in_progress",
  "waitlist_joined",
  "human_active",
  "askedQuestions",
  "knownFacts",
  "pendingQuestion",
  "cost:",
]);

writeReport("agent-v2-state", checks.map((check) => assert(check.found, `state contract contains ${check.pattern}`)));

