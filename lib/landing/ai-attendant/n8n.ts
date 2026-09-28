type N8nEventName =
  | "landing_ai_attendant_analysis_handoff"
  | "landing_ai_attendant_high_intent"
  | "landing_ai_attendant_lead_alert"
  | "landing_ai_attendant_operator_action"
  | "landing_ai_attendant_safety_event"
  | "landing_custom_agent_diagnostic";

export type N8nDispatchResult =
  | {
      status: "sent" | "synced";
      statusCode: number;
      responseStatus?: string;
    }
  | {
      status: "skipped";
      reason: string;
    }
  | {
      status: "failed";
      statusCode?: number;
      reason?: string;
      responseStatus?: string;
    };

const WEBHOOK_ENV: Record<N8nEventName, string> = {
  landing_ai_attendant_analysis_handoff: "N8N_WEBHOOK_DIAGNOSTIC_HANDOFF",
  landing_ai_attendant_high_intent: "N8N_WEBHOOK_HIGH_INTENT",
  landing_ai_attendant_lead_alert: "N8N_WEBHOOK_LEAD_ALERT",
  landing_ai_attendant_operator_action: "N8N_WEBHOOK_OPERATOR_ACTION",
  landing_ai_attendant_safety_event: "N8N_WEBHOOK_SAFETY_EVENT",
  landing_custom_agent_diagnostic: "N8N_WEBHOOK_CUSTOM_AGENT_DIAGNOSTIC",
};

export async function dispatchN8nEvent(eventName: N8nEventName, payload: Record<string, unknown>): Promise<N8nDispatchResult> {
  const url = process.env[WEBHOOK_ENV[eventName]];
  if (!url) {
    return { status: "skipped" as const, reason: "Webhook URL is not configured." };
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 2500);

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        ...(process.env.N8N_WEBHOOK_SECRET ? { "x-webhook-secret": process.env.N8N_WEBHOOK_SECRET } : {}),
      },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });

    const body = await readWebhookResponse(response);
    if (!response.ok) {
      return {
        status: "failed",
        statusCode: response.status,
        responseStatus: body.status,
        reason: body.error,
      };
    }

    return {
      status: body.synced ? "synced" : "sent",
      statusCode: response.status,
      responseStatus: body.status,
    };
  } catch (error) {
    return {
      status: "failed" as const,
      reason: error instanceof Error ? error.message : "Unknown n8n error.",
    };
  } finally {
    clearTimeout(timeout);
  }
}

export function salesInboxSyncStatusFromN8nResult(result: N8nDispatchResult) {
  if (result.status === "synced") return "synced";
  if (result.status === "sent") return "pending";
  if (result.status === "skipped") return "skipped";
  return "failed";
}

async function readWebhookResponse(response: Response) {
  const contentType = response.headers.get("content-type") ?? "";
  if (!contentType.includes("application/json")) return {};

  try {
    const body = (await response.json()) as Record<string, unknown>;
    const status = typeof body.status === "string" ? body.status : undefined;
    const error = typeof body.error === "string" ? body.error.slice(0, 300) : undefined;
    return {
      status,
      error,
      synced: status === "synced" || status === "created" || status === "updated",
    };
  } catch {
    return {};
  }
}
