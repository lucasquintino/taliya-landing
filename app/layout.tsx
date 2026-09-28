import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Agentes operacionais para studios",
  description:
    "Landings por nicho para apresentar inteligências operacionais.",
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
