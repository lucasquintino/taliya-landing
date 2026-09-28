export function IllustrationPanel({
  title,
  items,
  variant = "studio",
}: {
  title: string;
  items: string[];
  variant?: "studio" | "custom" | "human" | "access";
}) {
  const accent = variant === "custom" ? "#7C5CFF" : variant === "human" ? "#D96B5F" : variant === "access" ? "#FFB21A" : "#0E8F7E";
  return (
    <div className="relative overflow-hidden rounded-[2rem] border border-[#E2DED5] bg-[#FFFDF8] p-6 shadow-[0_24px_70px_rgba(16,27,58,0.10)]">
      <div className="pointer-events-none absolute right-[-110px] top-[-110px] h-56 w-56 rounded-full opacity-15" style={{ backgroundColor: accent }} />
      <div className="relative grid gap-6 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">
        <div>
          <p className="text-xs font-black uppercase tracking-[0.22em]" style={{ color: accent }}>Ilustracao operacional</p>
          <h3 className="mt-3 text-3xl font-black leading-tight tracking-[-0.05em] text-[#101B3A]">{title}</h3>
          <div className="mt-5 grid gap-3">
            {items.map((item) => (
              <p className="rounded-2xl bg-[#F8F5EF] px-4 py-3 text-sm font-bold text-[#344054]" key={item}>{item}</p>
            ))}
          </div>
        </div>
        <div className="relative min-h-[260px] rounded-[1.5rem] bg-[linear-gradient(135deg,#F8F5EF_0%,#FFFFFF_100%)] p-5">
          <div className="absolute bottom-5 left-1/2 h-24 w-44 -translate-x-1/2 rounded-[50%] bg-[#E6E1D8]" />
          <div className="absolute bottom-20 left-[18%] h-28 w-16 rounded-t-full" style={{ backgroundColor: accent }} />
          <div className="absolute bottom-44 left-[22%] h-12 w-12 rounded-full bg-[#FFD8B8]" />
          <div className="absolute bottom-20 right-[16%] h-36 w-36 rounded-[2rem] border border-[#DAD5CC] bg-white p-4 shadow-lg">
            <div className="h-3 w-20 rounded-full bg-[#DAD5CC]" />
            <div className="mt-4 grid gap-2">
              <div className="h-8 rounded-xl" style={{ backgroundColor: `${accent}22` }} />
              <div className="h-8 rounded-xl bg-[#F2F4F7]" />
              <div className="h-8 rounded-xl bg-[#F2F4F7]" />
            </div>
          </div>
          <div className="absolute right-8 top-8 h-16 w-16 rounded-2xl border border-[#DAD5CC] bg-white shadow-md" />
          <div className="absolute left-8 top-12 h-10 w-24 rounded-full" style={{ backgroundColor: `${accent}28` }} />
        </div>
      </div>
    </div>
  );
}
