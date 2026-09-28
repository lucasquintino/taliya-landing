export function SectionShell({
  children,
  id,
  tone = "plain",
  className = "",
  contentClassName = "",
}: {
  children: React.ReactNode;
  id: string;
  tone?: "plain" | "warm" | "dark" | "white";
  className?: string;
  contentClassName?: string;
}) {
  const toneClass =
    tone === "dark"
      ? "bg-[#101B3A] text-white"
      : tone === "warm"
        ? "bg-[#F5F0E8] text-[#101B3A]"
        : tone === "white"
          ? "bg-[#FFFDF8] text-[#101B3A]"
          : "bg-[#FAF7F1] text-[#101B3A]";

  return (
    <section className={`reveal-on-scroll scroll-mt-36 min-h-[calc(100svh-4.25rem)] px-4 py-14 sm:scroll-mt-32 sm:px-8 sm:py-16 lg:flex lg:scroll-mt-28 lg:items-center lg:justify-center lg:px-12 lg:py-16 ${toneClass} ${className}`} id={id}>
      <div className={`reveal-section-content mx-auto min-w-0 w-full max-w-[1600px] lg:w-[calc(100vw-8rem)] ${contentClassName}`}>{children}</div>
    </section>
  );
}
