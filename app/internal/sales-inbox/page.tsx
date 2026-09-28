import type { Metadata } from "next";
import { SalesInboxClient } from "@/components/internal/SalesInboxClient";

export const metadata: Metadata = {
  title: "Sales Inbox | Taliya",
  robots: {
    index: false,
    follow: false,
  },
};

export const dynamic = "force-dynamic";

export default async function SalesInboxPage({
  searchParams,
}: {
  searchParams: Promise<{ token?: string | string[] }>;
}) {
  const expectedToken = process.env.INTERNAL_SALES_INBOX_TOKEN;
  const params = await searchParams;
  const token = Array.isArray(params.token) ? params.token[0] : params.token;

  if (!expectedToken) {
    return <InternalState title="Sales Inbox nao configurado" description="Defina INTERNAL_SALES_INBOX_TOKEN para habilitar o painel interno." />;
  }

  if (token !== expectedToken) {
    return <InternalState title="Acesso restrito" description="Informe um token interno valido para abrir o Sales Inbox." />;
  }

  return <SalesInboxClient token={expectedToken} />;
}

function InternalState({ title, description }: { title: string; description: string }) {
  return (
    <main className="grid min-h-screen place-items-center bg-[#F7F8FA] px-5 text-[#101828]">
      <div className="max-w-md rounded-2xl border border-[#E4E7EC] bg-white p-6 shadow-[0_20px_60px_rgba(16,24,40,0.08)]">
        <p className="text-xs font-bold uppercase tracking-[0.18em] text-[#667085]">Taliya interno</p>
        <h1 className="mt-3 text-2xl font-black">{title}</h1>
        <p className="mt-2 text-sm font-semibold leading-6 text-[#667085]">{description}</p>
      </div>
    </main>
  );
}
