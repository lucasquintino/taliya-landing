export function SectionIntro({
  eyebrow,
  title,
  subtitle,
  align = "left",
  dark = false,
}: {
  eyebrow: string;
  title: string;
  subtitle: string;
  align?: "left" | "center";
  dark?: boolean;
}) {
  return (
    <div className={align === "center" ? "mx-auto max-w-3xl text-center" : "max-w-3xl"}>
      <p className={`text-xs font-black uppercase tracking-[0.28em] ${dark ? "text-[#7BE0C8]" : "text-[#0E8F7E]"}`}>
        {eyebrow}
      </p>
      <h2 className={`mt-4 text-[clamp(2.25rem,5vw,4.6rem)] font-black leading-[0.98] tracking-[-0.07em] ${dark ? "text-white" : "text-[#101B3A]"}`}>
        {title}
      </h2>
      {subtitle ? (
        <p className={`mt-5 text-base leading-8 sm:text-lg ${dark ? "text-white/68" : "text-[#667085]"}`}>
          {subtitle}
        </p>
      ) : null}
    </div>
  );
}
