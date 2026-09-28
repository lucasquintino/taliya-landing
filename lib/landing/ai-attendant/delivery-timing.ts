export function widgetFirstResponseDelay(apiLatencyMs: number, isDiagnosticFinal = false) {
  if (apiLatencyMs <= 2000) return isDiagnosticFinal ? 900 : 700;
  if (apiLatencyMs <= 5000) return isDiagnosticFinal ? 500 : 350;
  return isDiagnosticFinal ? 200 : 80;
}

export function widgetNextResponseDelay(apiLatencyMs: number, contentLength: number, index: number, isDiagnosticFinal = false) {
  const lengthDelay = Math.min(500, Math.ceil(Math.max(0, contentLength) / 80) * 120);
  const diagnosticExtra = isDiagnosticFinal ? Math.max(0, 240 - index * 80) : 0;

  if (apiLatencyMs <= 2000) return clampDelay(900 + lengthDelay + diagnosticExtra, 900, isDiagnosticFinal ? 1450 : 1200);
  if (apiLatencyMs <= 5000) return clampDelay(600 + lengthDelay + diagnosticExtra, 600, isDiagnosticFinal ? 1100 : 900);
  return clampDelay(400 + Math.min(260, lengthDelay) + Math.min(120, diagnosticExtra), 400, isDiagnosticFinal ? 850 : 700);
}

export function whatsappReplyDelayMs(content: string, index: number) {
  const cleanLength = Math.max(0, content.trim().length);
  const isUrgent = /\b(humano|pausar|erro|falha|parar)\b/i.test(content);
  const isVeryShort = cleanLength <= 48;
  const fastTypingDelay = Math.ceil(cleanLength * 18);

  if (isUrgent) {
    return index === 0 ? clampDelay(500 + fastTypingDelay, 500, 1200) : clampDelay(650 + fastTypingDelay, 700, 1500);
  }

  if (isVeryShort) {
    return index === 0 ? clampDelay(550 + fastTypingDelay, 700, 1400) : clampDelay(750 + fastTypingDelay, 900, 1700);
  }

  if (index === 0) return clampDelay(650 + fastTypingDelay, 1000, 3600);
  return clampDelay(800 + fastTypingDelay, 1600, 6500);
}

function clampDelay(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, Math.round(value)));
}
