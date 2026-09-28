import { runTaliyaCommercialRuntimeTurn } from "@/lib/landing/ai-attendant/runtime-client";
import type { AiAttendantRequest, AiAttendantResponse } from "@/lib/landing/ai-attendant/schema";

export async function runAiAttendantTurn(request: AiAttendantRequest): Promise<AiAttendantResponse> {
  return runTaliyaCommercialRuntimeTurn(request);
}
