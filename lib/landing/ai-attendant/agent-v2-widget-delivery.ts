import type { AiAttendantResponse } from "./schema";
import type { ProductKnowledge } from "./product-knowledge-source";

export function attachWidgetActions(response: AiAttendantResponse, product: ProductKnowledge): AiAttendantResponse {
  if (response.conversionPath !== "view_plans" && response.conversionPath !== "guided_demo") return response;
  return {
    ...response,
    subscription: response.conversionPath === "view_plans"
      ? { planId: "seven_agents", ctaLabel: "Ver comparativo", checkoutUrl: product.links.plans }
      : { planId: "seven_agents", ctaLabel: "Ver demonstracao", checkoutUrl: product.links.demonstration },
  };
}

