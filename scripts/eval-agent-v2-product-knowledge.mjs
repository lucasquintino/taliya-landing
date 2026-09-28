import { assert, contains, writeReport } from "./eval-agent-v2-utils.mjs";

const checks = [
  ...contains("lib/landing/ai-attendant/product-knowledge-source.ts", [
    "version:",
    "plans:",
    "links:",
    "https://www.taliya.com.br/pilates/planos",
    "limited_studios_waitlist",
    "unsupportedClaims",
  ]),
];

writeReport("agent-v2-product-knowledge", checks.map((check) => assert(check.found, `product source contains ${check.pattern}`)));

