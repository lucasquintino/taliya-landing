import * as Sentry from "@sentry/nextjs";
import { sentryBaseOptions } from "@/lib/observability/sentry-options";

// Only the public site reports: previews and local runs stay silent.
const isProduction = typeof window !== "undefined" && /(^|\.)taliya\.com\.br$/.test(window.location.hostname);

Sentry.init({ ...sentryBaseOptions, enabled: isProduction, environment: "production" });

export const onRouterTransitionStart = Sentry.captureRouterTransitionStart;
