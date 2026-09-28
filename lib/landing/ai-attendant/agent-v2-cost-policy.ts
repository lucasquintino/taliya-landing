import type { AgentV2ModelUsage, AgentV2OrchestrationDecision, AgentV2Substate } from "./agent-v2-types";
import { getAgentV2Config } from "./agent-v2-flags";

export function estimateTurnUsage({
  input,
  output,
  category,
  operation = "generation",
  model,
  escalationReason,
}: {
  input: string;
  output?: string;
  category: AgentV2OrchestrationDecision["costBudgetCategory"];
  operation?: AgentV2ModelUsage["operation"];
  model?: string;
  escalationReason?: string;
}): AgentV2ModelUsage {
  const config = getAgentV2Config();
  const inputTokens = estimateTokens(input);
  const outputTokens = estimateTokens(output ?? "");
  const selectedModel = model ?? config.defaultModel;
  const estimatedCostUsd = estimateCostUsd(selectedModel, inputTokens, outputTokens);

  return {
    operation,
    model: selectedModel,
    inputTokens,
    outputTokens,
    estimatedCostUsd,
    budgetCategory: category,
    escalationReason,
  };
}

export function getCostCapStatus(cost: number): AgentV2Substate["cost"]["capStatus"] {
  const config = getAgentV2Config();
  if (cost >= config.hardCostCapUsd) return "hard_cap_blocked";
  if (cost >= config.highCostUsd) return "high";
  if (cost >= config.reviewCostUsd) return "review";
  return "ok";
}

export function shouldBlockForCost(substate: AgentV2Substate, projectedTurnCost = 0) {
  const total = substate.cost.estimatedConversationCostUsd + projectedTurnCost;
  return total >= getAgentV2Config().hardCostCapUsd;
}

export function hardCapFallbackText() {
  return "Vou deixar o que você já contou salvo por aqui.\n\nPara não te responder de qualquer jeito, vamos retornar assim que possível.";
}

export function estimateTokens(text: string) {
  return Math.ceil((text || "").length / 4);
}

function estimateCostUsd(model: string, inputTokens: number, outputTokens: number) {
  const normalized = model.toLowerCase();
  const inputPerMillion = normalized.includes("mini") ? 0.25 : 1.25;
  const outputPerMillion = normalized.includes("mini") ? 2 : 10;
  return Number(((inputTokens * inputPerMillion + outputTokens * outputPerMillion) / 1_000_000).toFixed(6));
}
