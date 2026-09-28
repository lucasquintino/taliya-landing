import { assert, readText, writeReport } from "./eval-agent-v2-utils.mjs";

const policy = readText("specs/009-taliya-sales-agent-architecture/conversation-policy.md");
const failures = ["direct question", "WhatsApp phone", "checkout", "human handoff", "prompt"];

writeReport("agent-v2-blocking-failures", failures.map((failure) => assert(policy.toLowerCase().includes(failure.toLowerCase()), `blocking policy mentions ${failure}`)));

