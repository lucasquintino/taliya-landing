import { assert, contains, writeReport } from "./eval-agent-v2-utils.mjs";

const checks = contains("lib/landing/ai-attendant/agent-v2-guardrails.ts", [
  "no_whatsapp_phone_request",
  "no_checkout_while_waitlist_closed",
  "no_prompt_leak",
  "validateToolPlan",
]);

writeReport("agent-v2-guardrails", checks.map((check) => assert(check.found, `guardrail contains ${check.pattern}`)));

