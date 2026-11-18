export type AccountAccessConfig = { supabaseUrl: string; publishableKey: string };

export const checkoutAiNoticeVersion = "openai-2026-10-23";

/** Somente configuração pública do mesmo Auth do app; nunca service_role. */
export function accountAccessConfig(env: Record<string, string | undefined> = process.env): AccountAccessConfig | null {
  if (env.TALIYA_ACCOUNT_CHECKOUT_ENABLED !== "true") return null;
  const supabaseUrl = env.TALIYA_ACCOUNT_SUPABASE_URL?.replace(/\/$/, "");
  const publishableKey = env.TALIYA_ACCOUNT_SUPABASE_PUBLISHABLE_KEY;
  if (!supabaseUrl || !publishableKey) return null;
  try {
    const url = new URL(supabaseUrl);
    if (url.username || url.password || url.pathname !== "/" || url.search || url.hash) return null;
    const local = env.NODE_ENV !== "production" && ["localhost", "127.0.0.1"].includes(url.hostname);
    if (url.protocol !== "https:" && !(local && url.protocol === "http:")) return null;
    if (!publishableKey.startsWith("sb_publishable_")) {
      const payload = JSON.parse(Buffer.from(publishableKey.split(".")[1] ?? "", "base64url").toString("utf8"));
      if (payload.role !== "anon") return null;
    }
    return { supabaseUrl, publishableKey };
  } catch { return null; }
}
