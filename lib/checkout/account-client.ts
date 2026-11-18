import type { AccountAccessConfig } from "./account-config";

export function checkoutPhone(value: string): string | null {
  const digits = value.replace(/\D/g, "");
  const national = digits.length === 13 && digits.startsWith("55") ? digits.slice(2) : digits;
  return /^[1-9]\d9\d{8}$/.test(national) ? `+55${national}` : null;
}

async function authPost(config: AccountAccessConfig, path: string, body: object) {
  const response = await fetch(`${config.supabaseUrl}/auth/v1/${path}`, {
    method: "POST", headers: { apikey: config.publishableKey, "content-type": "application/json" },
    body: JSON.stringify(body), signal: AbortSignal.timeout(20000), cache: "no-store",
  });
  if (!response.ok) throw new Error(response.status === 429
    ? "Aguarde um pouco antes de tentar novamente. O limite de envio ou verificação foi atingido."
    : "Não foi possível confirmar o acesso. Confira os dados e tente novamente.");
  return response.json();
}

/** Mesmo contrato de OTP por WhatsApp utilizado no login do aplicativo. */
export async function requestCheckoutCode(config: AccountAccessConfig, phone: string) {
  await authPost(config, "otp", { phone, create_user: true, channel: "whatsapp" });
}

export async function verifyCheckoutCode(config: AccountAccessConfig, phone: string, token: string): Promise<string> {
  const session = await authPost(config, "verify", { phone, token, type: "sms" });
  if (typeof session.access_token !== "string" || !session.access_token) throw new Error("Não foi possível confirmar a sessão. Solicite outro código.");
  // Só o access_token fica na memória da tela; não persistir refresh_token.
  return session.access_token;
}
