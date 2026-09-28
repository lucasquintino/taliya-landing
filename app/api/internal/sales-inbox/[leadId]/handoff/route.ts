import { applyOperatorAction } from "@/lib/landing/ai-attendant/sales-inbox-store";
import { syncTaliyaCommercialRuntimeHandoffState } from "@/lib/landing/ai-attendant/runtime-client";
import { requireSalesInboxAuth } from "../../auth";

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
  const mode = isRecord(body) && body.mode === "resume" ? "resume_ai" : "take_over";
  const { leadId } = await params;
  const result = await applyOperatorAction({
    leadId,
    actorUserId: auth.actorUserId,
    action: mode,
    payload: {
      source: "sales_inbox_handoff_route",
      reason: mode === "resume_ai" ? "operator_resume" : "operator_pause",
    },
  });

  if (!result.ok) return Response.json({ error: result.reason }, { status: 404 });
  const runtimeSync = await syncTaliyaCommercialRuntimeHandoffState({
    actorUserId: auth.actorUserId,
    lead: result.lead,
    mode: mode === "resume_ai" ? "resume" : "pause",
    reason: mode === "resume_ai" ? "operator_resume" : "operator_pause",
  });
  return Response.json({ ...result, runtimeSync });
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
