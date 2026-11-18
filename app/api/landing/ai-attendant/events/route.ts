import { recordLandingInteractionEvent, type LandingInteractionEventName } from "@/lib/landing/ai-attendant/funnel-events";
import { isInteractionEvent } from "@/lib/landing/acquisition-events";

const allowedEvents = new Set(["widget_opened", "cta_clicked", "page_viewed"]);

export async function POST(request: Request) {
  const origin = request.headers.get("origin");
  if (origin) {
    try {
      const parsed = new URL(origin);
      // Next dev may normalize request.url to localhost while Host retains 127.0.0.1.
      if (!["http:", "https:"].includes(parsed.protocol) || parsed.host !== request.headers.get("host")) return Response.json({ error: "Invalid origin." }, { status: 403 });
    } catch { return Response.json({ error: "Invalid origin." }, { status: 403 }); }
  }
  let body: Record<string, unknown>;
  try {
    const raw = await request.text();
    if (raw.length > 8192) return Response.json({ error: "Event too large." }, { status: 413 });
    const parsed: unknown = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) return Response.json({ error: "Invalid event." }, { status: 400 });
    body = parsed as Record<string, unknown>;
  } catch {
    return Response.json({ error: "Invalid JSON body." }, { status: 400 });
  }

  const eventName = text(body.eventName);
  const occurrenceId = text(body.occurrenceId);
  const sessionId = text(body.sessionId);
  if (!(allowedEvents.has(eventName) || isInteractionEvent(eventName)) || !occurrenceId || !sessionId) {
    return Response.json({ error: "Invalid landing event." }, { status: 400 });
  }

  if ((eventName === "page_viewed" || isInteractionEvent(eventName)) && process.env.NEXT_PUBLIC_TALIYA_ACQUISITION_ENABLED !== "true") return Response.json({ ok: true, state: "not_configured" });
  await recordLandingInteractionEvent({
    eventName: eventName as LandingInteractionEventName,
    occurrenceId,
    sessionId,
    // Only the widget may tie an event to a lead; page views and interactions stay anonymous.
    leadId: eventName === "widget_opened" || eventName === "cta_clicked" ? text(body.leadId) || undefined : undefined,
    channel: eventName === "page_viewed" || isInteractionEvent(eventName) ? "web" : text(body.channel) || "web",
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
