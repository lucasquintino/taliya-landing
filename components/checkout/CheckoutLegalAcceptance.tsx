import { legalDocuments } from "../../lib/legal/documents";

/** Aceite dentro do cadastro; os links abrem a versão exata apresentada. */
export function CheckoutLegalAcceptance() {
  const linkClass = "font-bold text-[#0E8F7E] underline underline-offset-4 focus:outline-none focus:ring-4 focus:ring-[#0E8F7E]/16";
  return (
    <div className="grid gap-2 text-sm leading-6 text-[#344054]">
        <p>
          Ao criar sua conta, você concorda com os{" "}
          <a className={linkClass} href={legalDocuments.terms.archiveHref} target="_blank" rel="noopener noreferrer">Termos de Uso</a>
          {" e a "}
          <a className={linkClass} href={legalDocuments.privacy.archiveHref} target="_blank" rel="noopener noreferrer">Política de Privacidade</a>.
        </p>
      <input name="termsVersion" type="hidden" value={legalDocuments.terms.version} />
      <input name="privacyVersion" type="hidden" value={legalDocuments.privacy.version} />
    </div>
  );
}
