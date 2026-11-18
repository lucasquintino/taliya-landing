/** Versões apresentadas no cadastro; o servidor confere estas mesmas versões. */
export const legalDocuments = {
  terms: { title: "Termos de Uso", href: "/termos", archiveHref: "/legal/2026-10-26.1/termos.html", version: "2026-10-26.1" },
  privacy: { title: "Política de Privacidade", href: "/privacidade", archiveHref: "/legal/2026-10-27.1/privacidade.html", version: "2026-10-27.1" },
} as const;

/** Validação para o futuro handler autenticado do cadastro. Não persiste aceite. */
export function validateCheckoutLegalAcceptance(input: {
  legalAccepted?: unknown;
  termsVersion?: unknown;
  privacyVersion?: unknown;
}) {
  if (input.legalAccepted !== "true") {
    return { ok: false, error: "Confirme os Termos de Uso e a Política de Privacidade para continuar." } as const;
  }
  if (input.termsVersion !== legalDocuments.terms.version || input.privacyVersion !== legalDocuments.privacy.version) {
    return { ok: false, error: "Os documentos foram atualizados. Recarregue a página e confira antes de continuar." } as const;
  }
  return {
    ok: true,
    termsVersion: legalDocuments.terms.version,
    privacyVersion: legalDocuments.privacy.version,
  } as const;
}
