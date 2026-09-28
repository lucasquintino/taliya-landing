import type { AgentV2Mode } from "./agent-v2-types";

export function getAgentV2Mode(): AgentV2Mode {
  const raw = (process.env.AI_ATTENDANT_V2_MODE ?? "auto").toLowerCase();
  if (raw === "auto" || raw === "capture_only" || raw === "legacy") return raw;
  return "auto";
}

export function isAgentV2Enabled() {
  return getAgentV2Mode() !== "legacy";
}

export function shouldAgentV2ReplyAutomatically() {
  return getAgentV2Mode() === "auto" && !isAgentV2KillSwitchOn();
}

export function isAgentV2CaptureOnly() {
  return getAgentV2Mode() === "capture_only" || isAgentV2KillSwitchOn();
}

export function isAgentV2KillSwitchOn() {
  return process.env.AI_ATTENDANT_V2_KILL_SWITCH === "true" || process.env.AI_ATTENDANT_V2_DISABLED === "true";
}

export function getAgentV2Config() {
  return {
    mode: getAgentV2Mode(),
    killSwitch: isAgentV2KillSwitchOn(),
    hardCostCapUsd: numberEnv("AI_ATTENDANT_V2_HARD_COST_CAP_USD", 0.15),
    reviewCostUsd: numberEnv("AI_ATTENDANT_V2_REVIEW_COST_USD", 0.05),
    highCostUsd: numberEnv("AI_ATTENDANT_V2_HIGH_COST_USD", 0.1),
    defaultModel: process.env.AI_ATTENDANT_MODEL || "gpt-5.4-mini",
    strongerModel: process.env.AI_ATTENDANT_V2_STRONG_MODEL || process.env.AI_ATTENDANT_MODEL || "gpt-5.4-mini",
    enableLegacyFallback: process.env.AI_ATTENDANT_V2_LEGACY_FALLBACK === "true",
  };
}

function numberEnv(key: string, fallback: number) {
  const value = Number(process.env[key]);
  return Number.isFinite(value) && value > 0 ? value : fallback;
}
