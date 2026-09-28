import { recordLandingInteractionEvent } from "@/lib/landing/ai-attendant/funnel-events";

const allowedEvents = new Set(["widget_opened", "cta_clicked"]);

export async function POST(request: Request) {
  let body: Record<string, unknown>;
  try {
    body = await request.json() as Record<string, unknown>;
  } catch {
    return Response.json({ error: "Invalid JSON body." }, { status: 400 });
  }

  const eventName = text(body.eventName);
  const occurrenceId = text(body.occurrenceId);
  const sessionId = text(body.sessionId);
  if (!allowedEvents.has(eventName) || !occurrenceId || !sessionId) {
    return Response.json({ error: "Invalid landing event." }, { status: 400 });
  }

  await recordLandingInteractionEvent({
    eventName: eventName as "widget_opened" | "cta_clicked",
    occurrenceId,
    sessionId,
    leadId: text(body.leadId) || undefined,
    channel: text(body.channel) || "web",
    sourcePage: text(body.sourcePage) || undefined,
    sourceSection: text(body.sourceSection) || undefined,
    metadata: record(body.metadata),
  });

  return Response.json({ ok: true });
}

function text(value: unknown) {
  return typeof value === "string" && value.trim() ? value.trim().slice(0, 500) : "";
}

function record(value: unknown): Record<string, unknown> {
  return value && typeof value === "object" && !Array.isArray(value)
    ? value as Record<string, unknown>
    : {};
}
