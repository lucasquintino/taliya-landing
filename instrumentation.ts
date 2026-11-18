import * as Sentry from "@sentry/nextjs";
import { sentryBaseOptions } from "@/lib/observability/sentry-options";

export async function register() {
  // VERCEL_ENV is set by Vercel on every deployment; previews and local runs stay silent.
  Sentry.init({ ...sentryBaseOptions, enabled: process.env.VERCEL_ENV === "production", environment: process.env.VERCEL_ENV ?? "local" });
}

export const onRequestError = Sentry.captureRequestError;
