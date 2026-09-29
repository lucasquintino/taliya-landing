import type { MetadataRoute } from "next";
import { absoluteSiteUrl } from "@/lib/landing/seo";

export default function robots(): MetadataRoute.Robots {
  const publicRules = {
    allow: "/",
    disallow: "/internal",
  };

  return {
    rules: [
      { userAgent: "*", ...publicRules },
      { userAgent: "OAI-SearchBot", ...publicRules },
      { userAgent: "GPTBot", ...publicRules },
    ],
    sitemap: absoluteSiteUrl("/sitemap.xml"),
  };
}
