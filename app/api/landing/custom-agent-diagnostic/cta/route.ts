import { createConversionHandoff } from "@/lib/landing/ai-attendant/conversion";
import { toPseudoAiRequest, type CustomAgentDiagnosticRequest } from "@/lib/landing/ai-attendant/custom-diagnostic";
import { createLeadRecord } from "@/lib/landing/ai-attendant/leads";
import { dispatchN8nEvent } from "@/lib/landing/ai-attendant/n8n";
import { createAssistantMessage, type AiAttendantResponse, type ConversionPath, type DiagnosticClassification, type DiagnosticContextVariant } from "@/lib/landing/ai-attendant/schema";
import { updateSalesLeadSyncStatus, upsertSalesLead } from "@/lib/landing/ai-attendant/sales-inbox-store";
import { getNicheConfig } from "@/lib/landing/ai-attendant/context";

export async function POST(request: Request) {
  let body: unknown;

  try {
    body = await request.json();
  } catch {
    return Response.json({ error: "Invalid JSON body." }, { status: 400 });
  }

  if (!isRecord(body)) return Response.json({ error: "Request body must be an object." }, { status: 400 });

  const reportId = stringValue(body.reportId);
  const selectedCtaId = stringValue(body.selectedCtaId);
  const sessionId = stringValue(body.sessionId);
  const niche = stringValue(body.niche) || "pilates";
  const sourcePage = stringValue(body.sourcePage) || "/";
  const classification = parseClassification(body.classification);
  const contextVariant = parseContextVariant(body.contextVariant);
  const conversionPath = parseConversionPath(body.conversionPath);
  const safeSummary = stringValue(body.safeSummary) || "Diagnostic CTA selected.";

  if (!reportId || !selectedCtaId || !sessionId || !classification || !contextVariant || !conversionPath) {
    return Response.json({ error: "Invalid diagnostic CTA payload." }, { status: 400 });
  }

  const config = getNicheConfig(niche);
  const pseudoRequest = toPseudoAiRequest({
    sessionId,
    niche,
    sourcePage,
    sourceSection: "final_diagnostic_cta",
    campaignStage: "commercial",
    publicOfferMode: "direct_saas_subscription",
    description: safeSummary,
  } satisfies CustomAgentDiagnosticRequest);
  const pseudoResponse = {
    assistantMessages: [createAssistantMessage(`CTA selecionado: ${selectedCtaId}`, "custom_agent_diagnostic_request")],
    capturedPainIds: [],
    recommendedAgentIds: parseStringArray(body.mappedAgentIds),
    conversionPath,
    shouldOfferDiagnostic: false,
    guardrailDecision: {
      category: "allowed",
      action: "respond",
      reason: "Diagnostic CTA selected.",
    },
    diagnosticClassification: classification,
    diagnosticContextVariant: contextVariant,
    diagnosticReportId: reportId,
    selectedDiagnosticCtaId: selectedCtaId,
    qualificationPatch: isRecord(body.customAgent)
      ? {
          customRoutine: stringValue(body.customAgent.operationSummary),
        }
      : undefined,
  } satisfies AiAttendantResponse;
  const handoff = createConversionHandoff({
    config,
    conversionPath,
    request: pseudoRequest,
    summary: safeSummary,
  });
  handoff.diagnosticClassification = classification;
  handoff.diagnosticContextVariant = contextVariant;

  const lead = createLeadRecord({
    config,
    eventName: "custom_agent_diagnostic_cta_clicked",
    handoff,
    request: pseudoRequest,
    response: pseudoResponse,
  });
  const salesLead = await upsertSalesLead(lead);

  await dispatchN8nEvent("landing_custom_agent_diagnostic", {
    eventName: "custom_agent_diagnostic_cta_clicked",
    occurredAt: new Date().toISOString(),
    sessionId,
    niche: config.niche,
    sourcePage,
    sourceSection: "final_diagnostic_cta",
    reportId,
    selectedCtaId,
    classification,
    contextVariant,
    conversionPath,
    mappedAgentIds: parseStringArray(body.mappedAgentIds),
    safeSummary,
  });

  await updateSalesLeadSyncStatus(salesLead.leadId, "skipped", {
    eventName: "lead_stored_locally",
    reason: "Lead stored in Sales Inbox/Postgres. External CRM lead sync is disabled.",
    reportId,
    selectedCtaId,
  });

  return Response.json({ ok: true, leadId: salesLead.leadId });
}

function parseClassification(input: unknown): DiagnosticClassification | undefined {
  if (input === "mapped_solution" || input === "custom_agent" || input === "mixed_solution" || input === "unclear") return input;
  return undefined;
}

function parseContextVariant(input: unknown): DiagnosticContextVariant | undefined {
  if (
    input === "diagnostic_existing_solution" ||
    input === "diagnostic_custom_agent" ||
    input === "diagnostic_mixed_solution" ||
    input === "diagnostic_unclear"
  ) {
    return input;
  }
  return undefined;
}

function parseConversionPath(input: unknown): ConversionPath | undefined {
  if (
    input === "custom_agent_diagnostic_mapped" ||
    input === "custom_agent_follow_up" ||
    input === "mixed_subscription_plus_custom" ||
    input === "custom_agent_diagnostic_unclear"
  ) {
    return input;
  }
  return undefined;
}

function parseStringArray(input: unknown) {
  return Array.isArray(input) ? input.filter((item): item is string => typeof item === "string") : [];
}

function stringValue(input: unknown) {
  return typeof input === "string" ? input.slice(0, 1200) : undefined;
}

function isRecord(input: unknown): input is Record<string, unknown> {
  return typeof input === "object" && input !== null;
}
