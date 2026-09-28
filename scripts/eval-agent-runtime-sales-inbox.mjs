import { assert, readJson, readText, writeReport } from "./eval-agent-runtime-utils.mjs";

const fixtures = readJson("scripts/fixtures/agent-runtime/sales-inbox.json");
const leads = readText("lib/landing/ai-attendant/leads.ts");
const runtimeClient = readText("lib/landing/ai-attendant/runtime-client.ts");
const store = readText("lib/landing/ai-attendant/sales-inbox-store.ts");
const widgetRoute = readText("app/api/landing/ai-attendant/route.ts");
const funnelEvents = readText("lib/landing/ai-attendant/funnel-events.ts");
const api = readText("app/api/internal/sales-inbox/leads/route.ts");
const ui = readText("components/internal/SalesInboxClient.tsx");
const schema = readText("services/taliya-agent-runtime/app/runtime/schemas.py");
const salesContract = readText("specs/010-openai-cs-agents-adaptation-for-taliya-commercial/sales-inbox-contract.md");

const results = [
  assert(fixtures.some((item) => item.agentRuntime?.currentAgent), "Sales Inbox runtime projection fixture is present"),
  assert(runtimeClient.includes("const completedAgentRecommendations = hasCompletedDiagnostic") && runtimeClient.includes("patch.recommendedAgents = completedAgentRecommendations") && runtimeClient.includes("patch.recommendedAgents = undefined"), "runtime adapter only promotes textual agent recommendations after completed diagnostic"),
  assert(runtimeClient.includes("agentRuntimeCrmBaseRecommendation: hasCompletedDiagnostic") && runtimeClient.includes("agentRuntimeAgentRecommendations: completedAgentRecommendations") && runtimeClient.includes("patch.agentRuntimeCrmBaseRecommendation = undefined"), "runtime adapter hides provisional diagnostic recommendation details from Sales Inbox"),
  assert(runtimeClient.indexOf("if (hasCompletedDiagnostic)") < runtimeClient.indexOf("patch.diagnosticSummary = output.diagnostic.main_bottleneck"), "runtime adapter only projects diagnostic summary inside completed-diagnostic block"),
  assert(runtimeClient.includes('const runtimeBuyingTiming = diagnosticAnswerValue(output, "urgency")') && runtimeClient.includes("buyingTiming: runtimeBuyingTiming"), "runtime adapter projects diagnostic urgency answer into Sales Inbox qualification"),
  assert(runtimeClient.includes("didCompletedDiagnosticOfferDemo") && runtimeClient.includes('patch.demoStatus = demoStatus === "not_offered" && completedDiagnosticOfferedDemo ? "offered" : demoStatus'), "runtime adapter records final diagnostic demo invitation as demo offered"),
  assert(leads.includes("agentRuntime?"), "LeadRecord has agentRuntime projection"),
  assert(leads.includes("extractAgentRuntime"), "lead creation extracts runtime metadata"),
  assert(api.includes("agentRuntime: lead.agentRuntime"), "Sales Inbox list API returns agentRuntime"),
  assert(ui.includes("Runtime oficial"), "Sales Inbox UI exposes runtime trace summary"),
  assert(store.includes("runtimeOperatorNextAction"), "Sales Inbox store adds runtime operator next-action flags"),
  assert(store.includes("Custo do runtime atingiu o limite duro"), "cost-cap next action is visible to operators"),
  assert(store.includes("mergeRecommendedAgentIds") && store.includes('lead.diagnosticStatus !== "completed"') && store.includes('lead.commercialStage.startsWith("diagnostic_")'), "Sales Inbox clears premature agent recommendations while diagnostic is still in progress"),
  assert(store.includes("linkRuntimeConversationToLead(next)") && store.includes("UPDATE agent_runtime_conversations") && store.includes("lead_id = $2"), "Sales Inbox links persisted lead identity to the runtime conversation"),
  assert(store.includes("message.conversationId ?? message.channelSessionId ?? lead.channelSessionId"), "Sales Inbox persists a real conversation id for every new transcript message"),
  assert(widgetRoute.includes('eventName: "lead_created"') && widgetRoute.includes("leadId: salesLead.leadId"), "Widget records an explicit lead-created funnel event after persistence"),
  assert(widgetRoute.includes('eventName: "first_message"'), "Widget records the first-message funnel step"),
  assert(funnelEvents.includes('eventName: "widget_opened" | "cta_clicked"') && funnelEvents.includes("ON CONFLICT (idempotency_key) DO NOTHING"), "Landing interaction events are allowlisted and idempotent"),
  assert(leads.includes("templateIds") && leads.includes("diagnosticLedgerStatus"), "LeadRecord persists template IDs and diagnostic ledger status"),
  assert(leads.includes("demoStatus?: string") && leads.includes("finalPlanLine?: string") && leads.includes("finalDemoLine?: string"), "LeadRecord persists demo status and final diagnostic lines"),
  assert(leads.includes("crmBaseRecommendation?: string") && leads.includes("agentRecommendations?: string"), "LeadRecord persists CRM base and per-agent recommendation details"),
  assert(ui.includes("demo runtime:") && ui.includes("plano final:") && ui.includes("demo final:"), "Sales Inbox UI exposes final demo and plan lines"),
  assert(ui.includes("base CRM:") && ui.includes("agentes:"), "Sales Inbox UI exposes CRM base and agent recommendation details"),
  assert(leads.includes("agentRuntimeDemoStatus") && leads.includes("agentRuntimeFinalPlanLine"), "qualification projection reads final diagnostic runtime fields"),
  assert(leads.includes("hasHighUrgencySignal") && leads.includes('qualification.diagnosticStatus === "completed" && hasHighUrgencySignal(qualification)') && leads.includes("calculateLeadUrgency"), "Sales Inbox priority and urgency use completed diagnostic urgency signals"),
  assert(leads.includes("const uniqueMatches = unique(matches)") && leads.includes("if (uniqueMatches.length === 1) return uniqueMatches[0]"), "Sales Inbox avoids collapsing plan ranges into a single recommended plan id"),
  assert(runtimeClient.includes("if (ids.size) return Array.from(ids)") && runtimeClient.indexOf("if (ids.size) return Array.from(ids)") < runtimeClient.indexOf("for (const fact of output.lead_facts"), "runtime adapter prefers structured ledger areas before text fallback for selected pain ids"),
  assert(runtimeClient.includes('const hasCompletedDiagnostic = diagnosticStatus === "completed"') && runtimeClient.includes("patch.recommendedPlan = output.diagnostic.plan_or_range_to_compare") && runtimeClient.includes("patch.recommendedPlan = undefined"), "runtime adapter only promotes plan recommendation after completed diagnostic"),
  assert(runtimeClient.includes('patch.commercialStage = "diagnostic_in_progress"') && runtimeClient.includes("Diagnóstico em andamento; aguardando resposta:"), "runtime adapter projects in-progress diagnostic stage and operator next action"),
  assert(runtimeClient.includes('patch.commercialStage = "diagnostic_offered"') && runtimeClient.includes("Diagnóstico gratuito oferecido; aguardar aceite"), "runtime adapter projects offered diagnostic stage and operator next action"),
  assert(runtimeClient.includes("hasWaitlistAction") && runtimeClient.includes("!hasWaitlistAction"), "runtime adapter avoids overriding waitlist next action after diagnostic completion"),
  assert(runtimeClient.includes('diagnostic?.status !== "completed"') && runtimeClient.includes("return []"), "runtime adapter does not project recommended agents before diagnostic completion"),
  assert(leads.includes('qualification.diagnosticStatus === "completed"') && leads.includes("const recommendedPlan = hasCompletedDiagnostic ? qualification.recommendedPlan : undefined"), "LeadRecord hides provisional plan recommendations until diagnostic completion"),
  assert(leads.includes("waitlistIntentEvidence") && leads.includes("guardrailFlags"), "LeadRecord persists waitlist evidence and guardrail flags"),
  assert(leads.includes("productSourceKeys") && leads.includes("latestProductFollowupIntent"), "LeadRecord persists product-followup source keys and latest intent"),
  assert(leads.includes("postDiagnosticContextUsed") && leads.includes("unsupportedFactRequested"), "LeadRecord persists post-diagnostic context and unsupported fact signal"),
  assert(leads.includes("humanConfirmationOffered") && leads.includes("diagnosticRefusalRespected"), "LeadRecord persists human confirmation and diagnostic-refusal observability"),
  assert(ui.includes("follow-up produto:") && ui.includes("fontes:"), "Sales Inbox UI exposes product-followup intent and source keys"),
  assert(ui.includes("contexto pos-diagnostico:") && ui.includes("fato a confirmar:"), "Sales Inbox UI exposes post-diagnostic context and unsupported fact signal"),
  assert(ui.includes("confirmacao humana:") && ui.includes("recusa diagnostico respeitada:"), "Sales Inbox UI exposes human confirmation and diagnostic-refusal signals"),
  assert(ui.includes("templates:") && ui.includes("ledger:"), "Sales Inbox UI exposes template and ledger runtime fields"),
  assert(schema.includes("previous_state") && schema.includes("next_state"), "runtime schema exposes previous/current/next state for Sales Inbox projection"),
  assert(schema.includes("template_ids") && schema.includes("diagnostic_ledger_status"), "runtime schema exposes template and diagnostic ledger status"),
  assert(salesContract.includes("template IDs rendered"), "Sales Inbox contract requires template IDs"),
  assert(salesContract.includes("diagnostic answer ledger"), "Sales Inbox contract requires diagnostic ledger"),
  assert(salesContract.includes("final plan or range recommendation"), "Sales Inbox contract requires final plan line"),
  assert(salesContract.includes("final demo next-step line"), "Sales Inbox contract requires final demo line"),
];

writeReport("agent-runtime-sales-inbox", results, {
  fixtures: fixtures.map((fixture) => fixture.id),
});
