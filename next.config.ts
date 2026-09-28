import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  allowedDevOrigins: ["127.0.0.1", "192.168.1.4", "192.168.10.199"],
  devIndicators: false,
  async redirects() {
    return [
      { source: "/pilates", destination: "/", permanent: true },
      { source: "/pilates/planos", destination: "/#planos", permanent: true },
      { source: "/pilates/planos/:path*", destination: "/#como-funciona", permanent: true },
      { source: "/pilates/demonstracao", destination: "/#como-funciona", permanent: true },
    ];
  },
  async rewrites() {
    return [
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
