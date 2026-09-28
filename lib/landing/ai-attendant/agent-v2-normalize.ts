import type { AiAttendantRequest } from "./schema";
import type { AgentV2NormalizedInput } from "./agent-v2-channel-adapter";
import { normalizeAgentV2Input } from "./agent-v2-channel-adapter";
import { classifyWhatsAppProfileName } from "./agent-v2-identity";

export function normalizeAgentV2Turn(request: AiAttendantRequest): AgentV2NormalizedInput {
  const normalized = normalizeAgentV2Input(request);
  const profileName = request.session.qualificationDraft?.name;
  const classifiedName = request.session.channel === "whatsapp" ? classifyWhatsAppProfileName(profileName) : undefined;
  if (classifiedName?.reliable) {
    normalized.channelMetadata.whatsappProfileName = classifiedName.name;
  }
  return normalized;
}

export function normalizeText(value: string) {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}

