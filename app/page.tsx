import type { Metadata } from "next";
import { NicheLandingPage } from "@/components/landing/NicheLandingPage";
import { pilatesLanding } from "@/data/landing/niches/pilates";

export const metadata: Metadata = {
  title: pilatesLanding.metadata.title,
  description: pilatesLanding.metadata.description,
  alternates: {
    canonical: "/",
  },
  openGraph: {
    title: pilatesLanding.metadata.title,
    description: pilatesLanding.metadata.description,
    type: "website",
    url: "/",
  },
};

export default function Home() {
  return <NicheLandingPage config={pilatesLanding} />;
}
