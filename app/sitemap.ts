import type { MetadataRoute } from "next";
import { absoluteSiteUrl } from "@/lib/landing/seo";

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: absoluteSiteUrl("/") },
    { url: absoluteSiteUrl("/privacidade") },
  ];
}
