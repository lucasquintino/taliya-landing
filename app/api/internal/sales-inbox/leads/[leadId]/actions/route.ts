import { pilatesLanding } from "@/data/landing/niches/pilates";
import { dispatchN8nEvent, salesInboxSyncStatusFromN8nResult } from "@/lib/landing/ai-attendant/n8n";
import {
  appendSalesLeadMessage,
  applyOperatorAction,
  getSalesLead,
  isValidOperatorAction,
  updateSalesLeadSyncStatus,
} from "@/lib/landing/ai-attendant/sales-inbox-store";
import { syncTaliyaCommercialRuntimeHandoffState } from "@/lib/landing/ai-attendant/runtime-client";
import { isWithinWhatsAppCustomerServiceWindow, sendMetaWhatsAppText } from "@/lib/landing/ai-attendant/whatsapp";
import { requireSalesInboxAuth } from "../../../auth";

export async function POST(
  request: Request,
  {
    params,
  }: {
    params: Promise<{ leadId: string }>;
  },
) {
  const auth = requireSalesInboxAuth(request);
  if (!auth.ok) return auth.response;

  const body = await safeJson(request);
  if (!isRecord(body) || typeof body.action !== "string" || !isValidOperatorAction(body.action)) {
    return Response.json({ error: "Invalid action." }, { status: 400 });
  }

  const payload = isRecord(body.payload) ? body.payload : {};
  const trustedPayload = withTrustedActionPayload(body.action, payload);
  if (!trustedPayload.ok) return Response.json({ error: trustedPayload.reason }, { status: 400 });

  const { leadId } = await params;

  if (body.action === "send_whatsapp_message") {
    const lead = await getSalesLead(leadId);
    if (!lead) return Response.json({ error: "lead_not_found" }, { status: 404 });

    const content = typeof trustedPayload.payload.message === "string" ? trustedPayload.payload.message.trim() : "";
    const to = lead.contact.providerContactId ?? lead.contact.normalizedWhatsapp ?? lead.contact.whatsapp;
    if (!content) return Response.json({ error: "Mensagem obrigatoria." }, { status: 400 });
    if (!to) return Response.json({ error: "Lead sem WhatsApp/provider contact." }, { status: 400 });
    if (!isWithinWhatsAppCustomerServiceWindow(lead.updatedAt)) {
      return Response.json(
        {
          error: "outside_customer_service_window_template_required",
          reason: "Envio livre pelo WhatsApp exige janela de atendimento de 24h. Templates aprovados ainda nao estao habilitados neste fluxo.",
        },
        { status: 409 },
      );
    }

    const clientIdempotencyKey = typeof trustedPayload.payload.idempotencyKey === "string" ? trustedPayload.payload.idempotencyKey : undefined;
    const sendResult = await sendMetaWhatsAppText({
      content,
      to,
      phoneNumberId: lead.contact.phoneNumberId,
      idempotencyKey: clientIdempotencyKey ?? `operator:${leadId}:${hashString(`${auth.actorUserId}:${content}:${lead.updatedAt}`)}`,
      leadId,
      channelSessionId: lead.channelSessionId,
      providerContactId: lead.contact.providerContactId,
    });
    if (!sendResult.ok) {
      return Response.json({ error: sendResult.reason }, { status: 502 });
    }

    await appendSalesLeadMessage(leadId, {
      id: sendResult.providerMessageId ?? `operator_${Date.now()}`,
      role: "assistant",
      content,
    });
  }

  const result = await applyOperatorAction({
    leadId,
    actorUserId: auth.actorUserId,
    action: body.action,
    payload: trustedPayload.payload,
  });

  if (!result.ok) return Response.json({ error: result.reason }, { status: 404 });
  const runtimeSync =
    body.action === "take_over" || body.action === "resume_ai"
      ? await syncTaliyaCommercialRuntimeHandoffState({
          actorUserId: auth.actorUserId,
          lead: result.lead,
          mode: body.action === "resume_ai" ? "resume" : "pause",
          reason: body.action === "resume_ai" ? "operator_resume" : "operator_pause",
        })
      : undefined;

  const operatorSyncResult = await dispatchN8nEvent("landing_ai_attendant_operator_action", {
    eventName: "sales_inbox_operator_action",
    occurredAt: new Date().toISOString(),
    lead: {
      leadId: result.lead.leadId,
      status: result.lead.status,
      priority: result.lead.priority,
      readiness: result.lead.readiness,
      channel: result.lead.channel,
      conversionPath: result.lead.conversionPath,
      selectedPlanId: result.lead.selectedPlanId,
      nextAction: result.lead.nextAction,
      summary: result.lead.summary,
    },
    action: result.action,
  });
  const syncResult = operatorSyncResult;

  await updateSalesLeadSyncStatus(result.lead.leadId, salesInboxSyncStatusFromN8nResult(syncResult), {
    eventName: "sales_inbox_operator_action",
    n8nStatus: syncResult.status,
    n8nReason: "reason" in syncResult ? syncResult.reason : undefined,
    n8nStatusCode: "statusCode" in syncResult ? syncResult.statusCode : undefined,
    operatorActionStatus: operatorSyncResult.status,
    leadStorage: "sales_inbox_postgres",
  });

  return Response.json({ ...result, sync: syncResult, operatorSync: operatorSyncResult, runtimeSync });
}

async function safeJson(request: Request) {
  try {
    return await request.json();
  } catch {
    return null;
  }
}

function isRecord(input: unknown): input is Record<string, unknown> {
  return typeof input === "object" && input !== null;
}

function hashString(value: string) {
  let hash = 0;
  for (let index = 0; index < value.length; index += 1) {
    hash = (hash << 5) - hash + value.charCodeAt(index);
    hash |= 0;
  }
  return Math.abs(hash).toString(36);
}

function withTrustedActionPayload(action: string, payload: Record<string, unknown>) {
  if (action === "send_whatsapp_message") {
    const message = typeof payload.message === "string" ? payload.message.trim().slice(0, 3800) : "";
    const idempotencyKey = typeof payload.idempotencyKey === "string" ? payload.idempotencyKey.trim().slice(0, 160) : undefined;
    if (!message) return { ok: false as const, reason: "Mensagem obrigatoria." };
    return {
      ok: true as const,
      payload: {
        message,
        idempotencyKey,
        provider: "meta_whatsapp_cloud_api",
      },
    };
  }

  if (action === "send_plan_page") {
    return {
      ok: true as const,
      payload: {
        ...payload,
        url: pilatesLanding.floatingAgent.planComparisonDestination.href,
        label: pilatesLanding.floatingAgent.planComparisonDestination.label,
      },
    };
  }

  if (action === "send_checkout_link") {
    const planId = typeof payload.planId === "string" ? payload.planId : pilatesLanding.subscription.recommendedPlanId;
    const plan = pilatesLanding.subscription.plans.find((item) => item.id === planId);
    if (!plan) return { ok: false as const, reason: "Invalid configured plan." };

    return {
      ok: true as const,
      payload: {
        ...payload,
        planId: plan.id,
        url: plan.primaryCta.href,
        label: plan.primaryCta.label,
        billingActivationBoundary: "payment_confirmation_required",
      },
    };
  }

  return { ok: true as const, payload };
}
