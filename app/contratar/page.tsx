import type { Metadata } from "next";
import Link from "next/link";
import { CheckoutAccountForm } from "@/components/checkout/CheckoutAccountForm";
import { accountAccessConfig } from "@/lib/checkout/account-config";
export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Criar conta | Taliya", robots: { index: false, follow: false } };
export default function CheckoutPage() {
  const config = accountAccessConfig();
  return <main className="min-h-screen bg-[#F7F3EA] px-5 py-8 text-[#101B3A] sm:py-12">
    <div className="mx-auto max-w-md">
      <Link className="inline-flex min-h-11 items-center font-bold text-[#0E8F7E] underline" href="/#planos">Voltar</Link>
      <section className="mt-5 rounded-lg border border-[#D8E6DC] bg-[#FFFDF8] p-5 sm:p-8">
        <h1 className="mb-6 text-3xl font-black tracking-[-0.04em]">Criar sua conta</h1>
        {config ? <CheckoutAccountForm config={config} /> : <p>O cadastro está temporariamente indisponível. Entre em contato pelo e-mail contato@taliya.com.br.</p>}
      </section>
    </div>
  </main>;
}
