export function classifyWhatsAppProfileName(name?: string) {
  const clean = (name ?? "").trim().replace(/\s+/g, " ");
  if (!clean) return { reliable: false, confidence: "unusable" as const };
  const normalized = normalize(clean);
  if (clean.length < 2 || clean.length > 45) return { reliable: false, confidence: "unusable" as const };
  if (/[^\p{L}\s.'-]/u.test(clean)) return { reliable: false, confidence: "unusable" as const };
  if (clean.split(/\s+/).length > 3) return { reliable: false, confidence: "low" as const };
  if (/^(.)\1*$/.test(normalized) || clean.length === 1) return { reliable: false, confidence: "unusable" as const };
  if (/\b(studio|estudio|pilates|oficial|atendimento|recepcao|recepção|secretaria|clinica|empresa|taliya)\b/.test(normalized)) {
    return { reliable: false, confidence: "low" as const };
  }
  return { reliable: true, confidence: clean.split(/\s+/).length >= 2 ? ("high" as const) : ("medium" as const), firstName: firstName(clean), name: clean };
}

export function firstName(name: string) {
  return name.trim().split(/\s+/)[0] || name;
}

function normalize(value: string) {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}

