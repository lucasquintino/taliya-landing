export function BrowserFrame({ children, title = "Painel da Taliya" }: { children: React.ReactNode; title?: string }) {
  return (
    <div className="mockup-float overflow-hidden rounded-[2rem] border border-[#E2DED5] bg-white shadow-[0_24px_70px_rgba(16,27,58,0.12)]">
      <div className="flex h-14 items-center justify-between border-b border-[#E9E4DA] bg-[#FBF8F2] px-5">
        <div className="flex items-center gap-2">
          <span className="window-dot h-3 w-3 rounded-full bg-[#F97066]" />
          <span className="window-dot h-3 w-3 rounded-full bg-[#FDB022]" style={{ animationDelay: "120ms" }} />
          <span className="window-dot h-3 w-3 rounded-full bg-[#12B76A]" style={{ animationDelay: "240ms" }} />
        </div>
        <p className="hidden text-xs font-black uppercase tracking-[0.16em] text-[#667085] sm:block">{title}</p>
        <span className="h-7 w-20 rounded-full bg-[#E9E5FF]" />
      </div>
      {children}
    </div>
  );
}

export function SaasPanelMockup({
  title,
  metric,
  label,
  items,
}: {
  title: string;
  metric: string;
  label: string;
  items: { label: string; value: string; tone?: "neutral" | "warning" | "success" | "accent" }[];
}) {
  const toneClass = {
    neutral: "bg-[#F2F4F7] text-[#344054]",
    warning: "bg-[#FFF3E0] text-[#B54708]",
    success: "bg-[#E7F8F1] text-[#087A61]",
    accent: "bg-[#EBE7FF] text-[#4937A8]",
  };

  return (
    <BrowserFrame title={title}>
      <div className="bg-[linear-gradient(180deg,#FFFFFF_0%,#F8F5EF_100%)] p-5 sm:p-6">
        <div className="rounded-[1.5rem] bg-[#101B3A] p-5 text-white">
          <p className="text-xs font-black uppercase tracking-[0.18em] text-[#7BE0C8]">{title}</p>
          <p className="metric-pop mt-4 text-5xl font-black tracking-[-0.07em]">{metric}</p>
          <p className="mt-2 text-sm text-white/65">{label}</p>
        </div>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          {items.map((item, index) => (
            <div className="panel-row interactive-hit rounded-2xl border border-[#E6E1D8] bg-white p-4" key={item.label} style={{ animationDelay: `${index * 70}ms` }}>
              <p className="text-sm font-bold text-[#667085]">{item.label}</p>
              <span className={`mt-3 inline-flex rounded-full px-3 py-1.5 text-xs font-black ${toneClass[item.tone ?? "neutral"]}`}>
                {item.value}
              </span>
            </div>
          ))}
        </div>
      </div>
    </BrowserFrame>
  );
}
