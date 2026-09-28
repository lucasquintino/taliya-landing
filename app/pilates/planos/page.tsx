import type { Metadata } from "next";
import { PlansPage } from "@/components/landing/PlansPage";
import { pilatesPlansLanding } from "@/data/landing/niches/pilates";

export const metadata: Metadata = {
  title: "Planos Taliya para studios de Pilates",
  description:
    "Compare Base, Essencial, Avance e Completo para escolher como a Taliya pode cuidar da rotina do seu studio de Pilates.",
  alternates: {
    canonical: "/pilates/planos",
  },
  openGraph: {
    title: "Planos Taliya para studios de Pilates",
    description:
      "Compare Base, Essencial, Avance e Completo para escolher como a Taliya pode cuidar da rotina do seu studio de Pilates.",
    type: "website",
    url: "/pilates/planos",
  },
};

export default async function PilatesPlansRoute({
  searchParams,
}: {
  searchParams: Promise<{ plan?: string | string[] }>;
}) {
  const params = await searchParams;
  const initialPlanId = Array.isArray(params.plan) ? params.plan[0] : params.plan;

  return <PlansPage config={pilatesPlansLanding} initialPlanId={initialPlanId} />;
}
