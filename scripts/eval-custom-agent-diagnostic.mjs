#!/usr/bin/env node

const targetArg = process.argv.find((arg) => arg.startsWith("--target="));
const target = targetArg?.slice("--target=".length) || process.env.CUSTOM_AGENT_DIAGNOSTIC_EVAL_TARGET;

const cases = [
  {
    id: "DIAG-001",
    title: "Mapped WhatsApp and reposicao request",
    description: "Quero responder WhatsApp e organizar reposicoes dos alunos",
    classification: "mapped_solution",
    conversionPath: "custom_agent_diagnostic_mapped",
    mappedAgentIds: ["atendimento", "agenda"],
    forbiddenCtaId: "guided_demo",
  },
  {
    id: "DIAG-002",
    title: "Custom marketing request",
    description: "Quero um agente de marketing para criar campanhas no Instagram",
    classification: "custom_agent",
    conversionPath: "custom_agent_follow_up",
    ctaId: "request_custom_agent_proposal",
  },
  {
    id: "DIAG-003",
    title: "Mixed SaaS and custom request",
    description: "Quero responder WhatsApp, organizar reposicoes e criar campanhas para alunos inativos no Instagram",
    classification: "mixed_solution",
    conversionPath: "mixed_subscription_plus_custom",
    mappedAgentIds: ["atendimento", "agenda", "retencao"],
  },
  {
    id: "DIAG-004",
    title: "Unclear automation request",
    description: "Quero automatizar meu studio",
    classification: "unclear",
    conversionPath: "custom_agent_diagnostic_unclear",
  },
];

if (!target) {
  console.log(`Custom-agent diagnostic harness ready: ${cases.length} cases configured.`);
  for (const item of cases) console.log(`- ${item.id}: ${item.title}`);
  console.log("\nRun against a local app with: npm run eval:custom-diagnostic -- --target=http://localhost:3000");
  process.exit(0);
}

const endpoint = new URL("/api/landing/custom-agent-diagnostic", target).toString();
const results = [];

for (const item of cases) {
  const result = await runCase(endpoint, item);
  results.push(result);
  const label = result.ok ? "PASS" : "FAIL";
  console.log(`${label} ${item.id}: ${item.title}${result.reason ? ` - ${result.reason}` : ""}`);
}

const failed = results.filter((item) => !item.ok);
console.log(`\nCustom-agent diagnostic evals: ${results.length - failed.length}/${results.length} passed.`);

if (failed.length) process.exit(1);

async function runCase(endpoint, item) {
  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      sessionId: `eval_${item.id.toLowerCase()}`,
      niche: "pilates",
      sourcePage: "/pilates",
      sourceSection: "custom_agent_diagnostic",
      campaignStage: "commercial",
      publicOfferMode: "direct_saas_subscription",
      description: item.description,
    }),
  });

  if (!response.ok) return { ok: false, reason: `HTTP ${response.status}` };
  const payload = await response.json();

  if (payload.classification !== item.classification) {
    return { ok: false, reason: `expected classification ${item.classification}, got ${payload.classification}` };
  }
  if (payload.leadEffect?.conversionPath !== item.conversionPath) {
    return { ok: false, reason: `expected conversionPath ${item.conversionPath}, got ${payload.leadEffect?.conversionPath}` };
  }
  if (item.ctaId && !payload.ctas?.some((cta) => cta.id === item.ctaId)) {
    return { ok: false, reason: `missing CTA ${item.ctaId}` };
  }
  if (item.forbiddenCtaId && payload.ctas?.some((cta) => cta.id === item.forbiddenCtaId)) {
    return { ok: false, reason: `unexpected CTA ${item.forbiddenCtaId}` };
  }
  for (const agentId of item.mappedAgentIds ?? []) {
    if (!payload.mappedAgentIds?.includes(agentId)) return { ok: false, reason: `missing mapped agent ${agentId}` };
  }
  if (payload.ctas?.some((cta) => cta.destination === "checkout")) {
    return { ok: false, reason: "diagnostic routed directly to checkout" };
  }

  return { ok: true };
}
