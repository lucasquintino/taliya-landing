import { isInteractionEvent } from './acquisition-events';
/** Shared with the widget. Observation only: this identifier never authenticates an account. */
let volatileSession: string | undefined;
const pageOccurrences = new Map<string, string>();
export function acquisitionId() {
 return typeof crypto !== 'undefined' && 'randomUUID' in crypto ? crypto.randomUUID().replaceAll('-', '') : `${Date.now().toString(36)}_${Math.random().toString(36).slice(2)}`;
}
export function readOrCreateLandingSessionId() {
 if (typeof window === 'undefined') return undefined;
 try {
  const stored = window.sessionStorage.getItem('taliya:landing-session');
  if (stored && /^[-A-Za-z0-9_:]{1,128}$/.test(stored)) return stored;
  volatileSession ??= `landing_${acquisitionId()}`;
  window.sessionStorage.setItem('taliya:landing-session', volatileSession);
 } catch { /* A blocked storage does not break navigation or the conversation. */ }
 return volatileSession ??= `landing_${acquisitionId()}`;
}
export function readAcquisitionMetadata() {
 if (typeof window === 'undefined') return {};
 const params = new URLSearchParams(window.location.search);
 const value = (key: string) => { const raw = params.get(key); return raw?.trim() && raw.length <= 200 && !/[\x00-\x1f\x7f]/.test(raw) ? raw : undefined; };
 let referrer: string | undefined;
 try { if (document.referrer) referrer = new URL(document.referrer).origin; } catch { /* Not an origin. */ }
 return { anonymousSessionId: readOrCreateLandingSessionId(), referrer, utmSource: value('utm_source'), utmMedium: value('utm_medium'), utmCampaign: value('utm_campaign'), utmContent: value('utm_content'), utmTerm: value('utm_term') };
}
const pageEvents = new Set(['page_view_niche', 'landing_viewed', 'plans_page_viewed', 'page_opened']);
const ctaEvents = new Set(['cta_click', 'plan_cta_clicked', 'human_whatsapp_clicked', 'whatsapp_cta_clicked', 'consultor_cta_clicked', 'faq_doubt_cta_clicked', 'assisted_conversion_clicked']);
export async function recordObservedAcquisition(eventName: string, metadata: Record<string, unknown>) {
 if (process.env.NEXT_PUBLIC_TALIYA_ACQUISITION_ENABLED !== 'true' || typeof window === 'undefined') return;
 const pageView = pageEvents.has(eventName); const interaction = isInteractionEvent(eventName);
 if (!pageView && !interaction && !ctaEvents.has(eventName)) return;
 try {
  const path = window.location.pathname;
  // One occurrence per rendered path/document, including React StrictMode's repeated Effect and
  // the page's own view event next to the layout-wide one: the second sender is skipped.
  if (pageView) { if (pageOccurrences.has(path)) return; pageOccurrences.set(path, acquisitionId()); }
  const acquisition = readAcquisitionMetadata();
  await fetch('/api/landing/ai-attendant/events', { method: 'POST', headers: { 'content-type': 'application/json' }, keepalive: true,
   body: JSON.stringify({ eventName: pageView ? 'page_viewed' : interaction ? eventName : 'cta_clicked', occurrenceId: pageView ? pageOccurrences.get(path) : acquisitionId(), sessionId: acquisition.anonymousSessionId, channel: 'web', sourcePage: path,
    sourceSection: typeof metadata.sourceSection === 'string' ? metadata.sourceSection.slice(0, 200) : undefined,
    metadata: { ...acquisition, ctaId: pageView || interaction ? undefined : eventName } }) });
 } catch { /* Telemetry failure never blocks the user's action; no unbounded retries. */ }
}
