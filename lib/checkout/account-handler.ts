import { checkoutAiNoticeVersion, type AccountAccessConfig } from "./account-config";
import { validateCheckoutLegalAcceptance } from "../legal/documents";

const responseHeaders = { "Cache-Control": "no-store", "Referrer-Policy": "no-referrer" };
function reply(body: object, status = 200) { return Response.json(body, { status, headers: responseHeaders }); }

/** A autoridade da conta, sessão e data continua no RPC do backend do app. */
export async function saveCheckoutAccount(request: Request, config: AccountAccessConfig | null, transport: typeof fetch = fetch): Promise<Response> {
  if (!config) return reply({ error: "O cadastro está temporariamente indisponível." }, 503);
  if (request.method !== "POST") return reply({ error: "Método não permitido." }, 405);
  if (request.headers.get("origin") !== new URL(request.url).origin) return reply({ error: "Origem inválida." }, 403);
  const authorization = request.headers.get("authorization") ?? "";
  if (!/^Bearer [A-Za-z0-9._~-]{20,8192}$/.test(authorization)) return reply({ error: "Confirme o código para continuar." }, 401);
  if (!request.headers.get("content-type")?.startsWith("application/json")) return reply({ error: "Solicitação inválida." }, 400);
  let body: Record<string, unknown>;
  try {
    const raw = await request.text();
    if (raw.length > 4096) return reply({ error: "Solicitação inválida." }, 400);
    const parsed: unknown = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) return reply({ error: "Solicitação inválida." }, 400);
    body = parsed as Record<string, unknown>;
    if (Object.keys(body).some((key) => !["legalAccepted", "termsVersion", "privacyVersion", "aiConsent"].includes(key))) return reply({ error: "Solicitação inválida." }, 400);
  } catch { return reply({ error: "Solicitação inválida." }, 400); }
  const validated = validateCheckoutLegalAcceptance(body);
  if (!validated.ok) return reply({ error: validated.error }, 400);
  let consentRequest: string | undefined;
  if (body.aiConsent !== undefined) {
    const choice = body.aiConsent as Record<string, unknown> | null;
    if (!choice || typeof choice !== "object" || Object.keys(choice).length !== 2 ||
      choice.noticeVersion !== checkoutAiNoticeVersion || typeof choice.requestId !== "string" ||
      !/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(choice.requestId)) {
      return reply({ error: "Confira a autorização de IA e tente novamente." }, 400);
    }
    consentRequest = choice.requestId.toLowerCase();
  }
  const signal = AbortSignal.timeout(15000);
  const headers = { apikey: config.publishableKey, authorization, "content-type": "application/json" };
  try {
    const result = await transport(`${config.supabaseUrl}/rest/v1/rpc/account_legal_accept`, {
      method: "POST", headers,
      body: JSON.stringify({ p_terms_version: validated.termsVersion, p_privacy_version: validated.privacyVersion, p_accepted: true }),
      signal, cache: "no-store",
    });
    if (!result.ok) return reply({ error: result.status === 401 || result.status === 403
      ? "Sua sessão expirou ou não foi confirmada. Solicite outro código."
      : "Não foi possível confirmar o cadastro. Tente salvar novamente; seu aceite não será duplicado." }, result.status === 401 || result.status === 403 ? 401 : 503);
    const receipt = await result.json();
    if (typeof receipt?.id !== "string" || typeof receipt?.accepted_at !== "string" || receipt.terms_version !== validated.termsVersion || receipt.privacy_version !== validated.privacyVersion) {
      return reply({ error: "Não foi possível confirmar o cadastro. Tente salvar novamente." }, 503);
    }
    if (consentRequest) {
      const consent = await transport(`${config.supabaseUrl}/rest/v1/rpc/ai_consent_decide`, {
        method: "POST", headers, signal, cache: "no-store",
        body: JSON.stringify({ p_request_id: consentRequest, p_notice_version: checkoutAiNoticeVersion, p_allowed: true }),
      });
      if (consent.status === 401 || consent.status === 403)
        return reply({ error: "Sua sessão expirou. Solicite outro código." }, 401);
      if (!consent.ok) return reply({ error: "Não foi possível confirmar a autorização de IA. Tente salvar novamente." }, 503);
      const decision = await consent.json();
      if (decision?.allowed !== true || decision.notice_version !== checkoutAiNoticeVersion || typeof decision.decided_at !== "string") {
        return reply({ error: "A autorização de IA ainda não foi confirmada." }, 503);
      }
    }
    return reply({ receipt });
  } catch { return reply({ error: "Não foi possível confirmar o cadastro. Tente salvar novamente; seu aceite não será duplicado." }, 503); }
}
