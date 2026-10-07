import type { CTA, NicheLandingConfig } from "@/data/landing/niches/types";
import { TaliyaLogo } from "./TaliyaLogo";

export function Header({
  config,
  onCta,
  activeSection,
  scrollProgress,
}: {
  config: NicheLandingConfig;
  onCta: (label: string, href: string) => void;
  activeSection: string;
  scrollProgress: number;
}) {
  return (
    <header className="sticky top-0 z-40 border-b border-[#E9E4DA]/80 bg-[#FFFDF8]/88 px-4 py-3 backdrop-blur-xl sm:px-8 lg:px-12">
      <div
        className="absolute bottom-0 left-0 h-0.5 bg-[#0E8F7E] transition-[width] duration-150 ease-out"
        style={{ width: `${scrollProgress}%` }}
      />
      <div className="mx-auto flex w-full max-w-[1600px] items-center justify-between gap-3 lg:w-[calc(100vw-8rem)]">
        <a className="interactive-hit flex shrink-0 items-center text-[#101B3A]" href="#top">
          <TaliyaLogo label={config.brand} />
        </a>
        <nav className="hidden items-center gap-1 text-sm font-bold text-[#667085] xl:flex">
          {config.header.links.map((link) => {
            const sectionId = link.href.replace("#", "");
            const active = activeSection === sectionId;
            return (
              <a
                className={`interactive-hit rounded-full px-3 py-2 transition ${
                  active ? "bg-[#E7F8F1] text-[#0E8F7E]" : "hover:bg-[#F5F0E8] hover:text-[#101B3A]"
                }`}
                href={link.href}
                key={link.href}
              >
                {link.label}
              </a>
            );
          })}
        </nav>
        <a
          className="interactive-hit inline-flex shrink-0 items-center justify-center rounded-full bg-[#101B3A] px-3 py-3 text-xs font-black text-white shadow-[0_18px_45px_rgba(16,27,58,0.20)] transition hover:bg-[#17254B] focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] focus:ring-offset-2 sm:px-4 sm:text-sm"
          href={config.header.cta.href}
          onClick={() => onCta(config.header.cta.label, config.header.cta.href)}
        >
          <span className="hidden sm:inline">{config.header.cta.label}</span>
          <span className="sm:hidden">{config.header.cta.label}</span>
          <span aria-hidden="true" className="ml-2 hidden sm:inline">→</span>
        </a>
      </div>
    </header>
  );
}

export function TrackedLink({
  cta,
  onCta,
  size = "md",
  variant = "dark",
  className = "",
}: {
  cta: CTA;
  onCta: (label: string, href: string) => void;
  size?: "sm" | "md" | "lg";
  variant?: "dark" | "light" | "outline" | "gold";
  className?: string;
}) {
  const sizeClass =
    size === "sm"
      ? "px-4 py-3 text-xs sm:text-sm"
      : size === "lg"
        ? "px-5 py-4 text-sm sm:px-7 sm:text-base"
        : "px-5 py-3.5 text-sm";

  const variantClass =
    variant === "light"
      ? "bg-white text-[#101B3A] shadow-[0_18px_45px_rgba(16,27,58,0.12)] hover:bg-[#F8F5EF]"
      : variant === "outline"
        ? "border border-[#DAD5CC] bg-white/70 text-[#101B3A] hover:border-[#101B3A]"
        : variant === "gold"
          ? "bg-[#FFB21A] text-[#101B3A] shadow-[0_16px_35px_rgba(255,178,26,0.24)] hover:bg-[#F8A800]"
          : "bg-[#101B3A] text-white shadow-[0_18px_45px_rgba(16,27,58,0.20)] hover:bg-[#17254B]";

  return (
    <a
      className={`interactive-hit group inline-flex max-w-full items-center justify-center rounded-full text-center font-black transition focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] focus:ring-offset-2 ${sizeClass} ${variantClass} ${className}`}
      href={cta.href}
      onClick={() => onCta(cta.label, cta.href)}
    >
      <span className="truncate">{cta.label}</span>
      <span aria-hidden="true" className="ml-2 shrink-0 transition-transform group-hover:translate-x-1">→</span>
    </a>
  );
}
