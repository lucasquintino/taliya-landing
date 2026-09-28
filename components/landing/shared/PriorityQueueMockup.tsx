export function PriorityQueueMockup({
  items,
}: {
  items: { label: string; value: string; tone?: "neutral" | "warning" | "success" | "accent" }[];
}) {
  const columns = ["Sinal", "Rotina", "Prioridade"];
  return (
    <div className="overflow-hidden rounded-[2rem] border border-[#E2DED5] bg-white shadow-[0_24px_70px_rgba(16,27,58,0.10)]">
      <div className="border-b border-[#E9E4DA] bg-[#101B3A] p-5 text-white">
        <p className="text-xs font-black uppercase tracking-[0.22em] text-[#7BE0C8]">Painel operacional</p>
        <h3 className="mt-2 text-3xl font-black tracking-[-0.05em]">Prioridades de hoje</h3>
      </div>
      <div className="grid grid-cols-3 border-b border-[#E9E4DA] bg-[#FBF8F2] px-4 py-3 text-xs font-black uppercase tracking-[0.12em] text-[#667085]">
        {columns.map((column) => <span key={column}>{column}</span>)}
      </div>
      <div className="divide-y divide-[#E9E4DA]">
        {items.map((item, index) => (
          <div className={`reveal-step reveal-delay-${Math.min(index + 1, 7)} grid grid-cols-3 items-center gap-3 px-4 py-4 text-sm`} key={item.label}>
            <span className="font-black text-[#101B3A]">{item.label}</span>
            <span className="text-[#667085]">{index % 2 === 0 ? "Agenda" : "Gestão"}</span>
            <span className="justify-self-start rounded-full bg-[#E7F8F1] px-3 py-1.5 text-xs font-black text-[#087A61]">{item.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
