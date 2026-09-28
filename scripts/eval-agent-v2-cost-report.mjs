import { createBudgetFromEnv, writeReport, assert } from "./eval-agent-v2-utils.mjs";

const budget = createBudgetFromEnv();
writeReport("agent-v2-cost-report", [
  assert(budget.maxEstimatedCostUsd <= 5, "eval budget has explicit max estimated cost", budget),
  assert(budget.maxRealModelCalls >= 0, "eval budget tracks max real model calls", budget),
], { budget });

