"use client";

import { useEffect, useRef, useState, type FormEvent } from "react";
import { checkoutAiNoticeVersion, type AccountAccessConfig } from "../../lib/checkout/account-config";
import { checkoutPhone, requestCheckoutCode, verifyCheckoutCode } from "../../lib/checkout/account-client";
import { validateCheckoutLegalAcceptance } from "../../lib/legal/documents";
import { recordObservedAcquisition } from "../../lib/landing/acquisition";
import { CheckoutLegalAcceptance } from "./CheckoutLegalAcceptance";

export function CheckoutAccountForm({ config }: { config: AccountAccessConfig }) {
  const [stage, setStage] = useState<"contact" | "code" | "complete">("contact");
  const [phone, setPhone] = useState("");
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const [pending, setPending] = useState(false);
  const [wait, setWait] = useState(0);
  const [allowAi, setAllowAi] = useState(false);
  const busy = useRef(false);
  const aiRequest = useRef<string | null>(null);
  useEffect(() => {
    if (wait === 0) return;
    const timer = setTimeout(() => setWait((value) => Math.max(0, value - 1)), 1000);
    return () => clearTimeout(timer);
  }, [wait]);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (busy.current) return;
    const form = new FormData(event.currentTarget);
    setError("");
    busy.current = true; setPending(true);
    try {
      if (stage === "contact") {
        const normalized = checkoutPhone(phone);
        if (!normalized) throw new Error("Informe seu celular com DDD.");
        await requestCheckoutCode(config, normalized);
        setPhone(normalized); setStage("code"); setWait(30);
        // Funnel step only: the phone is never sent with the event.
        void recordObservedAcquisition("signup_code_requested", {});
      } else if (stage === "code") {
        // Aceite decorre deste envio explícito do cadastro, não de visitar a tela
        // ou apenas solicitar o código. Versões continuam conferidas no servidor.
        const chosen = { legalAccepted: "true", termsVersion: String(form.get("termsVersion") ?? ""), privacyVersion: String(form.get("privacyVersion") ?? "") };
        const validated = validateCheckoutLegalAcceptance(chosen);
        if (!validated.ok) throw new Error(validated.error);
        if (!accessToken && !/^\d{6,8}$/.test(code)) throw new Error("Informe o código recebido no WhatsApp.");
        const token = accessToken ?? await verifyCheckoutCode(config, phone, code);
        setAccessToken(token);
        if (allowAi) aiRequest.current ??= crypto.randomUUID();
        const response = await fetch("/api/checkout/account", {
          method: "POST", headers: { "content-type": "application/json", authorization: `Bearer ${token}` },
          body: JSON.stringify({
            ...chosen,
            ...(allowAi && { aiConsent: { requestId: aiRequest.current, noticeVersion: checkoutAiNoticeVersion } }),
          }), signal: AbortSignal.timeout(20000), cache: "no-store",
        });
        const result = await response.json();
        if (!response.ok) {
          if (response.status === 401) setAccessToken(null);
          throw new Error(result.error || "Não foi possível salvar. Tente novamente.");
        }
        if (!result.receipt?.id) throw new Error("O cadastro ainda não foi confirmado. Tente salvar novamente.");
        setAccessToken(null); setCode(""); setStage("complete");
        // Observed in the browser after the server receipt; the account itself is the source of truth.
        void recordObservedAcquisition("signup_completed", {});
      }
    } catch (failure) {
      setError(failure instanceof Error && failure.name !== "TimeoutError" && failure.name !== "TypeError" ? failure.message : "A conexão falhou. Tente novamente; seus dados continuam nesta tela.");
    } finally { busy.current = false; setPending(false); }
  }

  async function resend() {
    if (busy.current || wait > 0) return;
    busy.current = true; setPending(true); setError("");
    try { await requestCheckoutCode(config, phone); setWait(30); setAccessToken(null); setCode(""); }
    catch { setError("Não foi possível reenviar agora. Aguarde um pouco e tente novamente."); }
    finally { busy.current = false; setPending(false); }
  }

  const control = "min-h-12 w-full rounded-lg border border-[#D8E6DC] bg-white px-4 text-base text-[#101B3A] focus:outline-none focus:ring-2 focus:ring-[#0E8F7E]";
  const button = "min-h-12 w-full rounded-full bg-[#101B3A] px-5 py-3 font-bold text-white disabled:opacity-50";
  if (stage === "complete") return (
    <div role="status" className="grid gap-5">
      <h2 className="text-2xl font-bold">Cadastro confirmado</h2>
      <p>Seu acesso foi verificado e o aceite dos documentos foi salvo na sua conta.</p>
      <p>O pagamento ainda não está disponível. Nenhuma assinatura ou cobrança foi iniciada.</p>
      <button className={button} disabled type="button">Pagamento indisponível</button>
    </div>
  );
  return (
    <form className="grid gap-5" onSubmit={submit}>
      {stage === "contact" ? <>
        <p className="text-sm text-[#667085]">Esta etapa confirma sua conta. O pagamento ainda não está disponível neste ambiente.</p>
        <label className="grid gap-2 font-semibold">Celular com DDD
          <input autoComplete="tel" className={control} disabled={pending} inputMode="tel" maxLength={20} name="phone" onChange={(event) => setPhone(event.target.value)} placeholder="27 99999-9999" required type="tel" value={phone} />
        </label>
        <p className="text-sm text-[#667085]">Confirme seu celular por um código no WhatsApp. Se você já tem conta, use o mesmo número do app.</p>
      </> : <>
        <p>Digite o código enviado ao seu WhatsApp, terminado em {phone.slice(-4)}.</p>
        <label className="grid gap-2 font-semibold">Código de acesso
          <input autoComplete="one-time-code" className={control} disabled={pending || Boolean(accessToken)} inputMode="numeric" maxLength={8} minLength={6} name="code" onChange={(event) => setCode(event.target.value.replace(/\D/g, ""))} pattern="[0-9]{6,8}" required={!accessToken} value={code} />
        </label>
      </>}
      {error ? <p className="text-sm text-[#A12A28]" role="alert">{error}</p> : null}
      <CheckoutLegalAcceptance />
      <label className="flex items-start gap-3 text-sm leading-6 text-[#344054]">
        <input className="mt-1 size-4 shrink-0 accent-[#0E8F7E]" type="checkbox" name="aiConsent" checked={allowAi} disabled={pending || Boolean(accessToken)} onChange={(event) => { aiRequest.current = null; setAllowAi(event.target.checked); }} />
        Autorizo a Taliya a enviar minhas mensagens, áudios, arquivos e os dados necessários do meu negócio à OpenAI para responder aos meus pedidos no Copiloto e no WhatsApp.
      </label>
      <button className={button} disabled={pending} type="submit">{pending ? "Aguarde…" : stage === "contact" ? "Receber código" : accessToken ? "Tentar salvar novamente" : "Criar conta"}</button>
      {stage === "code" ? <>
        <button className="min-h-11 text-sm font-bold text-[#0E8F7E] disabled:opacity-50" disabled={pending || wait > 0} onClick={() => void resend()} type="button">{wait > 0 ? `Reenviar código em ${wait}s` : "Reenviar código"}</button>
        <button className="min-h-11 text-sm underline" disabled={pending} onClick={() => { setStage("contact"); setAccessToken(null); setCode(""); setError(""); setAllowAi(false); aiRequest.current = null; }} type="button">Alterar celular</button>
      </> : null}
    </form>
  );
}
