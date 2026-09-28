#!/usr/bin/env node

const targetArg = process.argv.find((arg) => arg.startsWith("--target="));
const target = targetArg?.slice("--target=".length) || process.env.AI_ATTENDANT_EVAL_TARGET;
const salesTokenArg = process.argv.find((arg) => arg.startsWith("--sales-token="));
const salesToken = salesTokenArg?.slice("--sales-token=".length) || process.env.INTERNAL_SALES_INBOX_TOKEN;
const requireSynced = process.argv.includes("--require-synced");

const cases = [
  {
    id: "PIPE-000",
    title: "Cold widget conversation is stored in Sales Inbox",
    message: "Oi",
    expectedConversionPath: "none",
    expectedLeadConversionPath: "cold_lead",
    omitDefaultQualification: true,
    qualificationDraft: {},
    expectedLeadFields: {
      status: "ai_active",
      priority: "cold",
      readiness: "curious",
      conversionPath: "cold_lead",
      waitlistStatus: "not_offered",
    },
  },
  {
    id: "PIPE-001",
    title: "Waitlist offered after positive diagnostic validation",
    message: "Faz sentido, quero entrar quando abrir.",
    expectedConversionPath: "waitlist_intent",
    qualificationDraft: {
      commercialStage: "recommendation_validation",
      waitlistStatus: "not_offered",
      diagnosticStatus: "completed",
      primaryPainOrIntent: "WhatsApp e agenda/repsicoes",
    },
    expectedLeadFields: {
      commercialStage: "waitlist_offered",
      waitlistStatus: "offered",
    },
  },
  {
    id: "PIPE-002",
    title: "Waitlist acceptance stays pending until required details exist",
    message: "Pode colocar.",
    expectedConversionPath: "waitlist_intent",
    qualificationDraft: {
      commercialStage: "waitlist_offered",
      waitlistStatus: "offered",
      diagnosticStatus: "completed",
      primaryPainOrIntent: "Vendas e WhatsApp sem retorno rapido",
      studioName: undefined,
      cityState: undefined,
    },
    expectedLeadFields: {
      commercialStage: "waitlist_pending_details",
      waitlistStatus: "pending_details",
    },
  },
  {
    id: "PIPE-003",
    title: "Waitlist acceptance joins when required details exist",
    message: "Pode colocar.",
    expectedConversionPath: "waitlist_intent",
    qualificationDraft: {
      commercialStage: "waitlist_offered",
      waitlistStatus: "offered",
      diagnosticStatus: "completed",
      primaryPainOrIntent: "Agenda e reposicoes sem controle",
      studioName: "Studio Teste Taliya",
      cityState: "Sao Paulo/SP",
    },
    expectedLeadFields: {
      commercialStage: "waitlist_joined",
      waitlistStatus: "joined",
    },
  },
  {
    id: "PIPE-004",
    title: "Waitlist declined is stored without joining",
    message: "Agora nao, prefiro ver melhor antes.",
    expectedConversionPath: "waitlist_intent",
    qualificationDraft: {
      commercialStage: "waitlist_offered",
      waitlistStatus: "offered",
      diagnosticStatus: "completed",
      primaryPainOrIntent: "WhatsApp e vendas sem retorno",
      studioName: "Studio Teste Taliya",
      cityState: "Sao Paulo/SP",
    },
    expectedLeadFields: {
      commercialStage: "waitlist_declined",
      waitlistStatus: "declined",
    },
  },
];

if (!target || !salesToken) {
  console.error("Usage: npm run eval:lead-pipeline -- --target=https://taliya.com.br --sales-token=TOKEN [--require-synced]");
  process.exit(1);
}

const endpoint = new URL("/api/landing/ai-attendant", target).toString();
const salesInboxEndpoint = new URL("/api/internal/sales-inbox/leads", target).toString();
const runId = `pipeline_${Date.now()}`;
const results = [];

for (const item of cases) {
  const result = await runCase(endpoint, salesInboxEndpoint, item, runId);
  results.push(result);
  const label = result.ok ? "PASS" : "FAIL";
  console.log(`${label} ${item.id}: ${item.title}${result.reason ? ` - ${result.reason}` : ""}`);
}

const failed = results.filter((result) => !result.ok);
console.log(`\nLead pipeline E2E: ${results.length - failed.length}/${results.length} passed.`);
if (requireSynced) console.log("Sync mode: requiring Sales Inbox external sync status=synced.");
if (failed.length) process.exit(1);

async function runCase(endpointUrl, salesInboxUrl, item, runPrefix) {
  const sessionId = `${runPrefix}_${item.id.toLowerCase()}`;
  const response = await fetch(endpointUrl, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      session: {
        sessionId,
        channel: "web",
        entryPath: "consultor_cta",
        niche: "pilates",
        sourcePage: "/pilates",
        campaignStage: "commercial",
        publicOfferMode: "direct_saas_subscription",
        messages: [],
        qualificationDraft: {
          ...(item.omitDefaultQualification
            ? {}
            : {
                name: `Lead Teste ${item.id}`,
                whatsapp: "+5511999999999",
                email: `lead-${item.id.toLowerCase()}@example.com`,
                studioName: "Studio Teste Taliya",
                cityState: "Sao Paulo/SP",
              }),
          ...(item.qualificationDraft ?? {}),
          ...(item.expectedLeadConversionPath === "cold_lead" || item.expectedConversionPath === "custom_agent_follow_up"
            ? {}
            : {
                diagnosticType: "crm_agent_diagnostic",
                diagnosticCompleted: "true",
                activeStudentsRange: "80_a_149",
                operationalPains: "atendimento, agenda/reposicoes, vendas, financeiro",
                dailyVisibility: "sem_visao",
                buyingTiming: "agora",
                leadTemperature: "hot",
                recommendedPlan: "seven_agents",
              }),
        },
      },
      userMessage: item.message,
      pageSignals: {
        selectedPainId: "atendimento_agenda_financeiro",
        calculatorEstimate: 6500,
      },
    }),
  });

  if (!response.ok) return { ok: false, reason: `AI route HTTP ${response.status}` };
  const payload = await response.json();
  if ((payload.conversionPath ?? "none") !== item.expectedConversionPath) {
    return { ok: false, reason: `expected ${item.expectedConversionPath}, got ${payload.conversionPath ?? "none"}` };
  }

  const leadLookup = await findLead(salesInboxUrl, sessionId, item.expectedLeadConversionPath ?? item.expectedConversionPath);
  if (!leadLookup.ok) return leadLookup;
  const lead = leadLookup.lead;
  if (!lead) return { ok: false, reason: "Sales Inbox lead not found" };
  const syncStatus = lead.externalSyncStatus;
  if (requireSynced && syncStatus !== "synced") {
    return { ok: false, reason: `expected synced external sync status, got ${syncStatus}` };
  }
  if (!requireSynced && !["pending", "synced", "skipped"].includes(syncStatus)) {
    return { ok: false, reason: `expected pending/synced/skipped external sync status, got ${syncStatus}` };
  }
  for (const [key, value] of Object.entries(item.expectedLeadFields ?? {})) {
    if (lead[key] !== value) return { ok: false, reason: `expected lead.${key}=${value}, got ${lead[key]}` };
  }

  return { ok: true };
}

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function findLead(salesInboxUrl, sessionId, conversionPath) {
  let lastStatus = "";

  for (let attempt = 0; attempt < 8; attempt += 1) {
    await wait(attempt === 0 ? 500 : 750);
    const leadResponse = await fetch(salesInboxUrl, {
      headers: { "x-internal-sales-token": salesToken },
    });
    if (!leadResponse.ok) return { ok: false, reason: `Sales Inbox HTTP ${leadResponse.status}` };

    const body = await leadResponse.json();
    const leads = Array.isArray(body.leads) ? body.leads : [];
    const lead = leads.find((candidate) => candidate.sessionId === sessionId && candidate.conversionPath === conversionPath);
    if (lead) return { ok: true, lead };
    lastStatus = `${leads.length} leads checked`;
  }

  return { ok: false, reason: `Sales Inbox lead not found (${lastStatus})` };
}
