/**
 * Error reporting for the public landing (Sentry project taliya-landing). Errors only: no
 * performance tracing, no session replay, no default PII (IP, cookies, request bodies).
 * The DSN is public by design: browsers send errors with it.
 */
export const sentryDsn =
  "https://5376d68b92883459a769eafb7164a22d@o4512455263387648.ingest.us.sentry.io/4512455281999872";

export const sentryBaseOptions = {
  dsn: sentryDsn,
  sendDefaultPii: false,
  tracesSampleRate: 0,
  // Phone numbers typed in the sign-up form never belong in an error report.
  beforeSend<T extends { message?: string; request?: { data?: unknown; query_string?: unknown } }>(event: T): T {
    if (event.request) { delete event.request.data; delete event.request.query_string; }
    if (event.message) event.message = event.message.replace(/\+?\d[\d\s().-]{7,}\d/g, "[número]");
    return event;
  },
};
