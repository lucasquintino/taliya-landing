import type { NicheLandingConfig } from "@/data/landing/niches/types";

type FooterLink = {
  label: string;
  href: string;
  icon?: "consultor" | "whatsapp" | "email";
};

export function FooterSection({ config }: { config: NicheLandingConfig }) {
  const isPlansPage = config.floatingAgent.label === "Consultor";
  const navigationLinks: FooterLink[] = config.footer.links.filter(
    (link, index, links) => links.findIndex((item) => item.href === link.href) === index,
  );
  const contactLinks: FooterLink[] = [
    { label: isPlansPage ? "Consultor" : "Falar com a Taliya", href: "#vendas", icon: "consultor" },
    {
      label: `WhatsApp ${formatWhatsAppNumber(config.assistedConversion.humanWhatsAppDestination.href)}`,
      href: withWhatsAppMessage(config.assistedConversion.humanWhatsAppDestination.href, config.salesCta.whatsappMessage),
      icon: "whatsapp",
    },
    ...(config.footer.contactEmail
      ? [{ label: config.footer.contactEmail, href: `mailto:${config.footer.contactEmail}`, icon: "email" as const }]
      : []),
  ];
  const legalLinks: FooterLink[] = [
    { label: "Privacidade", href: "/privacidade" },
    { label: "Dados usados", href: "/privacidade#dados" },
    { label: "IA e WhatsApp", href: "/privacidade#ia-whatsapp" },
    { label: "Compartilhamento", href: "/privacidade#compartilhamento" },
    { label: "Seus direitos", href: "/privacidade#direitos" },
  ];
  const linkGroups: Array<{ title: string; links: FooterLink[]; columns?: boolean }> = [
    { title: "Navegação", links: navigationLinks, columns: true },
    { title: "Contato", links: contactLinks },
    { title: "Legal", links: legalLinks },
  ];
  const currentYear = new Date().getFullYear();

  return (
    <footer className="site-footer border-t border-[#20315E] bg-[#101B3A] px-4 pt-10 text-white sm:px-8 lg:px-12">
      <div className="mx-auto max-w-7xl lg:pr-[12rem] xl:pr-[16rem]">
        <div className="grid gap-9 lg:grid-cols-[minmax(18rem,0.8fr)_minmax(0,1.45fr)] lg:items-start xl:grid-cols-[minmax(22rem,0.9fr)_minmax(0,1.55fr)]">
          <div className="max-w-lg">
            <span aria-hidden="true" className="mb-4 block h-1 w-12 rounded-full bg-[#7BE0C8]" />
            <p className="text-2xl font-black tracking-[-0.03em] sm:text-3xl">{config.brand}</p>
            <p className="mt-3 max-w-lg text-sm font-bold leading-6 text-white/68">
              {config.footer.text} {isPlansPage ? "A equipe segue no controle, com contexto claro para decidir o próximo passo." : "Você mantém o controle e decide o próximo passo com o contexto organizado."}
            </p>
          </div>
          <div className="grid gap-7 sm:grid-cols-2 lg:grid-cols-[minmax(15rem,1.1fr)_minmax(13.5rem,0.95fr)_minmax(10.5rem,0.8fr)] xl:gap-8">
            {linkGroups.map((group) => (
              <nav aria-label={group.title} className="grid content-start gap-2" key={group.title}>
                <p className="text-xs font-black uppercase tracking-[0.16em] text-[#7BE0C8]">{group.title}</p>
                <div className={`grid gap-x-5 gap-y-1 ${group.columns ? "grid-cols-2" : ""}`}>
                  {group.links.map((link) => (
                    <a
                      className="inline-flex min-h-10 min-w-0 items-center gap-2 rounded-full px-0 text-sm font-black leading-5 text-white/74 transition hover:text-white focus:outline-none focus:ring-4 focus:ring-[#7BE0C8]/20 lg:min-h-8"
                      href={link.href}
                      key={`${group.title}-${link.href}`}
                      rel={link.href.startsWith("http") ? "noreferrer" : undefined}
                      target={link.href.startsWith("http") ? "_blank" : undefined}
                    >
                      {"icon" in link && link.icon ? <FooterContactIcon icon={link.icon} /> : null}
                      <span className="min-w-0 break-words">{link.label}</span>
                    </a>
                  ))}
                </div>
              </nav>
            ))}
          </div>
        </div>
        <div className="mt-8 border-t border-white/10 pt-5 text-xs font-bold leading-5 text-white/50">
          <p>© {currentYear} Taliya. Todos os direitos reservados.</p>
        </div>
      </div>
    </footer>
  );
}

function withWhatsAppMessage(href: string, message: string) {
  if (!href.includes("wa.me")) return href;

  const [base] = href.split("?");
  return `${base}?text=${encodeURIComponent(message)}`;
}

function formatWhatsAppNumber(href: string) {
  const match = href.match(/wa\.me\/(\d+)/);
  const digits = match?.[1];
  if (!digits || digits.length < 12) return "";

  const country = digits.slice(0, 2);
  const area = digits.slice(2, 4);
  const number = digits.slice(4);
  return `+${country} ${area} ${number.slice(0, 5)}-${number.slice(5)}`;
}

function FooterContactIcon({ icon }: { icon: NonNullable<FooterLink["icon"]> }) {
  if (icon === "email") {
    return (
      <svg aria-hidden="true" className="h-4 w-4 shrink-0 text-[#7BE0C8]" fill="none" viewBox="0 0 24 24">
        <path d="M4.75 6.75h14.5v10.5H4.75V6.75Z" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        <path d="m5.25 7.25 6.75 5.5 6.75-5.5" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
      </svg>
    );
  }

  if (icon === "whatsapp") {
    return (
      <svg aria-hidden="true" className="h-4 w-4 shrink-0 text-[#7BE0C8]" fill="none" viewBox="0 0 24 24">
        <path d="M6.25 18.25 4.75 21l3.15-.95a8 8 0 1 0-2.3-2.3Z" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        <path d="M9 8.85c.2 2.9 2.25 5.05 5.05 5.8l1.3-1.35 2.1.9c-.25 1.75-1.35 2.55-3.05 2.25-3.9-.7-6.8-3.5-7.55-7.35-.3-1.65.5-2.8 2.2-3.05l.9 2.1L9 8.85Z" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
      </svg>
    );
  }

  return (
    <svg aria-hidden="true" className="h-4 w-4 shrink-0 text-[#7BE0C8]" fill="none" viewBox="0 0 24 24">
      <path d="M12 12.25a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Z" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
      <path d="M5.75 19.25c.85-2.55 3.05-4.25 6.25-4.25s5.4 1.7 6.25 4.25" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
    </svg>
  );
}
