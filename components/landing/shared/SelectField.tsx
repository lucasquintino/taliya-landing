export function SelectField({
  label,
  name,
  options,
  required,
}: {
  label: string;
  name: string;
  options: string[];
  required?: boolean;
}) {
  return (
    <label className="grid min-w-0 gap-2">
      <span className="text-sm font-black text-[#344054]">{label}</span>
      <select
        className="min-h-12 w-full min-w-0 rounded-2xl border border-[#DDD8CF] bg-[#FBF8F2] px-4 py-3 text-[#101B3A] outline-none transition focus:border-[#0E8F7E] focus:ring-4 focus:ring-[#0E8F7E]/15"
        defaultValue=""
        name={name}
        required={required}
      >
        <option disabled value="">
          Selecione uma opcao
        </option>
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </label>
  );
}
