import type { Metadata } from "next";
import { NicheLandingPage } from "@/components/landing/NicheLandingPage";
import { StructuredData } from "@/components/landing/shared/StructuredData";
import { pilatesLanding } from "@/data/landing/niches/pilates";
import { absoluteSiteUrl } from "@/lib/landing/seo";

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
    url: absoluteSiteUrl("/"),
  },
  twitter: {
    card: "summary",
    title: pilatesLanding.metadata.title,
    description: pilatesLanding.metadata.description,
  },
};

export default function Home() {
  return (
    <>
      <StructuredData
        description={pilatesLanding.metadata.description}
        path="/"
        title={pilatesLanding.metadata.title}
      />
      <NicheLandingPage config={pilatesLanding} />
    </>
  );
}
