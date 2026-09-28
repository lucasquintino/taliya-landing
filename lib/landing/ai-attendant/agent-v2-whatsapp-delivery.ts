export function planWhatsAppChunks(messages: string[]) {
  const splitMessages = messages.flatMap((message) => splitHumanMessage(message, 260)).filter(Boolean).slice(0, 8);
  return splitMessages.map((text) => ({
    text,
    typingDelayMs: Math.min(9000, Math.max(2500, Math.ceil(text.length * 55))),
  }));
}

function splitHumanMessage(content: string, maxLength: number) {
  if (!content || content.length <= maxLength) return content ? [content] : [];
  const paragraphs = content.split(/\n{2,}/).map((item) => item.trim()).filter(Boolean);
  const source = paragraphs.length > 1 ? paragraphs : [content];
  return source.flatMap((item) => splitParagraph(item, maxLength));
}

function splitParagraph(content: string, maxLength: number) {
  if (!content || content.length <= maxLength) return content ? [content] : [];
  const sentences = content.split(/(?<=[.!?])\s+/).map((item) => item.trim()).filter(Boolean);
  const chunks: string[] = [];
  let current = "";
  for (const sentence of sentences.length ? sentences : [content]) {
    if (!current) current = sentence;
    else if (`${current} ${sentence}`.length > maxLength) {
      chunks.push(current);
      current = sentence;
    } else {
      current = `${current} ${sentence}`;
    }
  }
  if (current) chunks.push(current);
  return chunks;
}
