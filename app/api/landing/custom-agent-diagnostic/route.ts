import { createConversionHandoff } from "@/lib/landing/ai-attendant/conversion";
import {
  parseCustomAgentDiagnosticRequest,
  runCustomAgentDiagnostic,
  toPseudoAiRequest,
} from "@/lib/landing/ai-attendant/custom-diagnostic";
import { createLeadRecord } from "@/lib/landing/ai-attendant/leads";
import { dispatchN8nEvent } from "@/lib/landing/ai-attendant/n8n";
import { createAssistantMessage } from "@/lib/landing/ai-attendant/schema";
import type { AiAttendantResponse } from "@/lib/landing/ai-attendant/schema";
import { updateSalesLeadSyncStatus, upsertSalesLead } from "@/lib/landing/ai-attendant/sales-inbox-store";
import { getNicheConfig } from "@/lib/landing/ai-attendant/context";

export async function POST(request: Request) {
  let body: unknown;

  try {
    body = await request.json();
  } catch {
    return Response.json({ error: "Invalid JSON body." }, { status: 400 });
  }

  const parsed = parseCustomAgentDiagnosticRequest(body);
  if (!parsed.ok) {
    return Response.json({ error: parsed.error }, { status: 400 });
  }

  const response = await runCustomAgentDiagnostic(parsed.value);
  const config = getNicheConfig(parsed.value.niche);

  await dispatchN8nEvent("landing_custom_agent_diagnostic", {
    eventName: response.guardrailDecision.category === "allowed" ? "custom_agent_diagnostic_generated" : "custom_agent_diagnostic_failed",
    occurredAt: new Date().toISOString(),
    sessionId: parsed.value.sessionId,
    niche: config.niche,
    sourcePage: parsed.value.sourcePage,
    sourceSection: parsed.value.sourceSection,
    reportId: response.reportId,
    classification: response.classification,
    contextVariant: response.diagnosticContextVariant,
    conversionPath: response.leadEffect.conversionPath,
    mappedAgentIds: response.mappedAgentIds,
    recommendedPlanId: response.recommendedPlanId,
    safeSummary: response.leadEffect.safeSummary,
    guardrailDecision: response.guardrailDecision,
  });

  if (response.leadEffect.shouldCreateOrUpdateLead) {
    const pseudoRequest = toPseudoAiRequest(parsed.value);
    const pseudoResponse = {
      assistantMessages: [createAssistantMessage(response.title, "custom_agent_diagnostic_request")],
      capturedPainIds: [],
      recommendedAgentIds: response.mappedAgentIds,
      conversionPath: response.leadEffect.conversionPath,
      shouldOfferDiagnostic: false,
      guardrailDecision: response.guardrailDecision,
      diagnosticClassification: response.classification,
      diagnosticContextVariant: response.diagnosticContextVariant,
      diagnosticReportId: response.reportId,
      qualificationPatch: response.customAgent
        ? {
            customRoutine: response.customAgent.operationSummary,
          }
        : undefined,
    } satisfies AiAttendantResponse;
    const handoff = createConversionHandoff({
      config,
      conversionPath: response.leadEffect.conversionPath,
      request: pseudoRequest,
      selectedPlanId: response.recommendedPlanId,
      summary: response.leadEffect.safeSummary,
    });
    handoff.diagnosticClassification = response.classification;
    handoff.diagnosticContextVariant = response.diagnosticContextVariant;

    const lead = createLeadRecord({
      config,
      eventName: "custom_agent_diagnostic_generated",
      handoff,
      request: pseudoRequest,
      response: pseudoResponse,
    });
    const salesLead = await upsertSalesLead(lead);

    await updateSalesLeadSyncStatus(salesLead.leadId, "skipped", {
      eventName: "lead_stored_locally",
      reason: "Lead stored in Sales Inbox/Postgres. External CRM lead sync is disabled.",
      reportId: response.reportId,
      classification: response.classification,
      contextVariant: response.diagnosticContextVariant,
    });
  }

  return Response.json(response);
}
