import { absoluteSiteUrl, TALIYA_SITE_ORIGIN } from "@/lib/landing/seo";

export function StructuredData({
  description,
  path,
  title,
}: {
  description: string;
  path: string;
  title: string;
}) {
  const pageUrl = absoluteSiteUrl(path);
  const organizationId = `${TALIYA_SITE_ORIGIN}/#organization`;
  const websiteId = `${TALIYA_SITE_ORIGIN}/#website`;
  const structuredData = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Organization",
        "@id": organizationId,
        name: "Taliya",
        url: `${TALIYA_SITE_ORIGIN}/`,
      },
      {
        "@type": "WebSite",
        "@id": websiteId,
        name: "Taliya",
        url: `${TALIYA_SITE_ORIGIN}/`,
        inLanguage: "pt-BR",
        publisher: { "@id": organizationId },
      },
      {
        "@type": "WebPage",
        "@id": `${pageUrl}#webpage`,
        url: pageUrl,
        name: title,
        description,
        inLanguage: "pt-BR",
        isPartOf: { "@id": websiteId },
        about: { "@id": organizationId },
      },
    ],
  };

  return (
    <script
      dangerouslySetInnerHTML={{
        __html: JSON.stringify(structuredData).replace(/</g, "\\u003c"),
      }}
      type="application/ld+json"
    />
  );
}
