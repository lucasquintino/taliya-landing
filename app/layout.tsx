import type { Metadata, Viewport } from "next";
import { pilatesLanding } from "@/data/landing/niches/pilates";
import { TALIYA_SITE_ORIGIN } from "@/lib/landing/seo";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL(TALIYA_SITE_ORIGIN),
  title: pilatesLanding.metadata.title,
  description: pilatesLanding.metadata.description,
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR" className="h-full scroll-smooth antialiased">
      <body className="flex min-h-full flex-col">{children}</body>
    </html>
  );
}
