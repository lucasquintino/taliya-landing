import Image from "next/image";

export function TaliyaLogo({ label = "Taliya" }: { label?: string }) {
  return (
    <span className="inline-flex min-h-11 shrink-0 items-center" aria-label={label}>
      <Image
        alt=""
        aria-hidden="true"
        className="block shrink-0"
        height="224"
        priority
        src="/taliya-logo.svg"
        style={{ height: "auto", maxWidth: "none", width: 132 }}
        width="1000"
      />
    </span>
  );
}
