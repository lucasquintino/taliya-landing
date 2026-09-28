import { assert, readText, writeReport } from "./eval-agent-runtime-utils.mjs";

const registry = readText("services/taliya-agent-runtime/app/runtime/registry.py");
const schemas = readText("services/taliya-agent-runtime/app/runtime/schemas.py");
const migration = readText("services/taliya-agent-runtime/migrations/001_agent_runtime_tables.sql");
const readme = readText("services/taliya-agent-runtime/README.md");
const rollout = readText("specs/010-openai-cs-agents-adaptation-for-taliya-commercial/rollout-and-deploy.md");

const forbiddenTablePattern = /\b(create table if not exists|create table)\s+(sales_agent_|agent_v2_)/i;
const results = [
  assert(registry.includes('agent_key="taliya_commercial"'), "taliya_commercial remains the only active implemented key"),
  assert(registry.includes('"taliya_configuration"'), "future Taliya configuration key is reserved"),
  assert(registry.includes('"studio_lead_capture"') && registry.includes('"studio_retention"'), "future studio operation keys are reserved"),
  assert(schemas.includes("agent_family") && schemas.includes("owner_scope") && schemas.includes("tenant_id"), "schemas expose generic scope fields"),
  assert(migration.includes("agent_family text not null"), "migration persists agent_family"),
  assert(migration.includes("owner_scope text not null"), "migration persists owner_scope"),
  assert(migration.includes("tenant_id text"), "migration persists nullable tenant_id"),
  assert(!forbiddenTablePattern.test(migration), "migration creates no sales_agent_* or agent_v2_* tables"),
  assert(readme.includes("Future agent boundaries"), "README documents future agent boundaries"),
  assert(rollout.includes("Out of scope for this spec"), "rollout docs state future agents are out of scope"),
];

writeReport("agent-runtime-naming", results);
