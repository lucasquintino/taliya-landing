export function FormField({
  label,
  name,
  required,
  type = "text",
}: {
  label: string;
  name: string;
  required?: boolean;
  type?: string;
}) {
  return (
    <label className="grid min-w-0 gap-2">
      <span className="text-sm font-black text-[#344054]">{label}</span>
      <input
        className="min-h-12 w-full min-w-0 rounded-2xl border border-[#DDD8CF] bg-[#FBF8F2] px-4 py-3 text-[#101B3A] outline-none transition focus:border-[#0E8F7E] focus:ring-4 focus:ring-[#0E8F7E]/15"
        name={name}
        required={required}
        type={type}
      />
    </label>
  );
}
