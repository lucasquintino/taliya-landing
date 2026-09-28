import type { LeadPriority, LeadStatus } from "@/lib/landing/ai-attendant/leads";
import { listSalesLeads } from "@/lib/landing/ai-attendant/sales-inbox-store";
import { requireSalesInboxAuth } from "../auth";

export async function GET(request: Request) {
  const auth = requireSalesInboxAuth(request);
  if (!auth.ok) return auth.response;

  const url = new URL(request.url);
  const leads = await listSalesLeads({
    status: parseLeadStatus(optionalParam(url, "status")),
    priority: parseLeadPriority(optionalParam(url, "priority")),
    channel: parseChannel(optionalParam(url, "channel")),
    conversionPath: optionalParam(url, "conversionPath"),
    selectedPlanId: optionalParam(url, "selectedPlanId"),
    nextAction: optionalParam(url, "nextAction"),
  });

  return Response.json({
    leads: leads.map((lead) => ({
      leadId: lead.leadId,
      sessionId: lead.sessionId,
      status: lead.status,
      priority: lead.priority,
      urgency: lead.urgency,
      readiness: lead.readiness,
      channel: lead.channel,
      sourceSection: lead.sourceSection,
      sourcePage: lead.sourcePage,
      conversionPath: lead.conversionPath,
      commercialStage: lead.commercialStage,
      waitlistStatus: lead.waitlistStatus,
      waitlistOfferedAt: lead.waitlistOfferedAt,
      waitlistJoinedAt: lead.waitlistJoinedAt,
      waitlistDeclinedAt: lead.waitlistDeclinedAt,
      diagnosticStatus: lead.diagnosticStatus,
      diagnosticCompletedAt: lead.diagnosticCompletedAt,
      demoStatus: lead.demoStatus,
      demoOfferedAt: lead.demoOfferedAt,
      demoSeenAt: lead.demoSeenAt,
      leadSourceChannel: lead.leadSourceChannel,
      leadSourceDetail: lead.leadSourceDetail,
      primaryPainOrIntent: lead.primaryPainOrIntent,
      missingWaitlistFields: lead.missingWaitlistFields,
      closureState: lead.closureState,
      humanActive: lead.humanActive,
      lastMessageAt: lead.lastMessageAt,
      selectedPlanId: lead.selectedPlanId,
      recommendedPlanId: lead.recommendedPlanId,
      selectedPainIds: lead.selectedPainIds,
      recommendedAgentIds: lead.recommendedAgentIds,
      contact: lead.contact,
      summary: lead.summary,
      nextAction: lead.nextAction,
      diagnosticClassification: lead.diagnosticClassification,
      diagnosticContextVariant: lead.diagnosticContextVariant,
      diagnosticReportId: lead.diagnosticReportId,
      selectedDiagnosticCtaId: lead.selectedDiagnosticCtaId,
      crmAgentDiagnostic: lead.crmAgentDiagnostic,
      agentRuntime: lead.agentRuntime,
      agentV2: lead.agentV2,
      aiPaused: lead.aiPaused,
      externalSyncStatus: lead.externalSyncStatus,
      updatedAt: lead.updatedAt,
    })),
  });
}

function optionalParam(url: URL, key: string) {
  return url.searchParams.get(key) ?? undefined;
}

function parseLeadStatus(input?: string): LeadStatus | undefined {
  if (
    input === "ai_active" ||
    input === "handoff_requested" ||
    input === "human_active" ||
    input === "waiting_customer" ||
    input === "follow_up_scheduled" ||
    input === "checkout_sent" ||
    input === "won" ||
    input === "lost" ||
    input === "do_not_contact"
  ) {
    return input;
  }
  return undefined;
}

function parseLeadPriority(input?: string): LeadPriority | undefined {
  if (input === "hot" || input === "warm" || input === "cold" || input === "manual") return input;
  return undefined;
}

function parseChannel(input?: string): "web" | "whatsapp" | undefined {
  if (input === "web" || input === "whatsapp") return input;
  return undefined;
}
