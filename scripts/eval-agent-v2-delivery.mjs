import { assert, contains, readJson, writeReport } from "./eval-agent-v2-utils.mjs";

const fixtures = readJson("scripts/fixtures/agent-v2/channel-parity.json");
const checks = [
  ...contains("lib/landing/ai-attendant/agent-v2-whatsapp-delivery.ts", ["typingDelayMs", "2500", "9000", "260"]),
  ...contains("lib/landing/ai-attendant/agent-v2-widget-delivery.ts", ["attachWidgetActions"]),
  ...contains("lib/landing/ai-attendant/whatsapp.ts", ["sendMetaWhatsAppTypingIndicator", "waitForWhatsAppReplyDelay"]),
];

writeReport("agent-v2-delivery", [
  assert(fixtures.length >= 2, "channel parity fixtures exist"),
  ...checks.map((check) => assert(check.found, `delivery contains ${check.pattern}`)),
]);
