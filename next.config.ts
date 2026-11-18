import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  allowedDevOrigins: ["127.0.0.1", "192.168.1.4", "192.168.10.199"],
  devIndicators: false,
  async redirects() {
    return [
      { source: "/pilates/demonstracao", destination: "/#como-funciona", permanent: true },
    ];
  },
  async headers() {
    return [{ source: "/excluir-conta/:path*", headers: [
      { key: "Referrer-Policy", value: "no-referrer" },
      { key: "Cache-Control", value: "no-store" },
      { key: "X-Content-Type-Options", value: "nosniff" },
      { key: "X-Robots-Tag", value: "noindex, nofollow" },
    ] }];
  },
  async rewrites() {
    return [
      { source: "/excluir-conta", destination: "/excluir-conta/index.html" },
      {
        source: "/internal",
        destination: "https://taliya-internal.vercel.app/internal",
      },
      {
        source: "/internal/:path*",
        destination: "https://taliya-internal.vercel.app/internal/:path*",
      },
    ];
  },
  turbopack: {
    root: process.cwd(),
    resolveAlias: {
      "react-native": "react-native-web",
    },
  },
};

export default nextConfig;
