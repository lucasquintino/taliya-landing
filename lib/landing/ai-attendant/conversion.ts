import type { NicheLandingConfig, PricingPlan } from "@/data/landing/niches/types";
import type { AiAttendantRequest, ConversionHandoff, ConversionPath } from "./schema";

export function getRecommendedPlan(config: NicheLandingConfig): PricingPlan | undefined {
  return config.subscription.plans.find((plan) => plan.id === config.subscription.recommendedPlanId) ?? config.subscription.plans.find((plan) => plan.recommended);
}

export function getSubscriptionTarget(config: NicheLandingConfig) {
  const plan = getRecommendedPlan(config);
  return {
    planId: plan?.id,
    checkoutUrl: plan?.primaryCta.href ?? config.subscription.fallbackPlanSelection.href,
    ctaLabel: config.floatingAgent.conversionCtas.checkoutIntent.label,
  };
}

export function getPlanComparisonTarget(config: NicheLandingConfig) {
  return {
    url: config.floatingAgent.planComparisonDestination.href,
    ctaLabel: config.floatingAgent.planComparisonDestination.label,
  };
}

export function getGuidedDemoTarget(config: NicheLandingConfig) {
  return {
    url: config.floatingAgent.guidedDemoDestination.href,
    ctaLabel: config.floatingAgent.guidedDemoDestination.label,
    ready: config.floatingAgent.guidedDemoReady,
  };
}

export function createConversionHandoff({
  config,
  conversionPath,
  request,
  selectedPlanId,
  summary,
}: {
  config: NicheLandingConfig;
  conversionPath: ConversionPath;
  request: AiAttendantRequest;
  selectedPlanId?: string;
  summary: string;
}): ConversionHandoff {
  const subscriptionTarget = getSubscriptionTarget(config);
  const destination = getHandoffDestination(conversionPath);

  return {
    sessionId: request.session.sessionId,
    channel: request.session.channel,
    channelSessionId: request.session.channelSessionId,
    niche: config.niche,
    sourcePage: request.session.sourcePage,
    campaignStage: config.tracking.campaignStage,
    publicOfferMode: config.tracking.publicOfferMode,
    conversionPath,
    summary,
    selectedPainIds: request.session.selectedPainIds ?? [],
    recommendedAgentIds: request.session.recommendedAgentIds ?? [],
    qualification: request.session.qualificationDraft ?? {},
    calculatorEstimate: request.pageSignals?.calculatorEstimate,
    destination,
    selectedPlanId: selectedPlanId ?? (conversionPath === "plan_recommendation" || conversionPath === "checkout_intent" ? subscriptionTarget.planId : undefined),
    checkout:
      conversionPath === "checkout_intent"
        ? {
            planId: subscriptionTarget.planId,
            url: subscriptionTarget.checkoutUrl,
          }
        : undefined,
    consentContext: {
      contactPurpose: conversionPath,
      privacyCopyShown: true,
      privacyNoticeUrl: config.assistedConversion.privacyNotice.href,
      whatsappOptIn: request.session.channel === "whatsapp" || conversionPath === "human_whatsapp_assist",
      whatsappOptOut: Boolean(request.session.externalContact?.optedOut),
    },
    humanHandoffStatus: conversionPath === "human_whatsapp_assist" ? "requested" : undefined,
  };
}

function getHandoffDestination(conversionPath: ConversionPath): ConversionHandoff["destination"] {
  if (conversionPath === "cold_lead") return "analysis_form";
  if (conversionPath === "checkout_intent") return "checkout";
  if (conversionPath === "waitlist_intent") return "waitlist_follow_up";
  if (conversionPath === "view_plans" || conversionPath === "plan_recommendation" || conversionPath === "crm_agent_diagnostic") return "plan_selection";
  if (conversionPath === "custom_agent_diagnostic_mapped") return "plan_selection";
  if (conversionPath === "guided_demo") return "guided_demo";
  if (conversionPath === "human_whatsapp_assist") return "whatsapp_follow_up";
  if (conversionPath === "custom_agent_follow_up" || conversionPath === "mixed_subscription_plus_custom") return "custom_agent_follow_up";
  return "analysis_form";
}
