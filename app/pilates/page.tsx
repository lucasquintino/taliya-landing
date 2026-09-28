import type { Metadata } from "next";
import { NicheLandingPage } from "@/components/landing/NicheLandingPage";
import { pilatesLanding } from "@/data/landing/niches/pilates";

export const metadata: Metadata = {
  title: pilatesLanding.metadata.title,
  description: pilatesLanding.metadata.description,
  alternates: {
    canonical: pilatesLanding.route,
  },
  openGraph: {
    title: pilatesLanding.metadata.title,
    description: pilatesLanding.metadata.description,
    type: "website",
    url: pilatesLanding.route,
  },
};

export default function PilatesPage() {
  return <NicheLandingPage config={pilatesLanding} />;
}
