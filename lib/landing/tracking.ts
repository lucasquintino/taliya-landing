import type { TrackingContext } from "@/data/landing/niches/types";

export type LandingEventName =
  | "page_view_niche"
  | "cta_click"
  | "pain_selected"
  | "agent_selected"
  | "calculator_started"
  | "calculator_result_updated"
  | "form_started"
  | "form_submitted"
  | "landing_viewed"
  | "consultor_cta_clicked"
  | "whatsapp_cta_clicked"
  | "guided_demo_started"
  | "guided_demo_completed"
  | "first_meaningful_chat_message"
  | "plan_asked"
  | "plan_recommended"
  | "plans_page_opened"
  | "checkout_intent"
  | "checkout_link_created"
  | "checkout_sent_by_operator"
  | "payment_confirmed"
  | "onboarding_link_sent"
  | "onboarding_started"
  | "onboarding_completed"
  | "lead_won"
  | "lead_lost"
  | "plans_page_viewed"
  | "plans_comparison_viewed"
  | "plan_cta_clicked"
  | "plan_fit_guidance_clicked"
  | "human_whatsapp_clicked"
  | "faq_item_opened"
  | "faq_doubt_cta_clicked"
  | "assisted_conversion_clicked"
  | "early_access_clicked"
  | "custom_agent_interest_clicked"
  | "custom_agent_diagnostic_started"
  | "custom_agent_diagnostic_submitted"
  | "custom_agent_diagnostic_generated"
  | "custom_agent_diagnostic_cta_clicked"
  | "custom_agent_diagnostic_failed"
  | "human_control_mode_selected"
  | "floating_agent_opened"
  | "floating_agent_closed"
  | "floating_agent_message_delivered"
  | "floating_agent_message_sent"
  | "floating_agent_quick_reply_clicked"
  | "floating_agent_pain_captured"
  | "floating_agent_agent_recommended"
  | "floating_agent_qualification_started"
  | "floating_agent_view_plans_cta"
  | "floating_agent_guided_demo_cta"
  | "floating_agent_plan_recommendation_cta"
  | "floating_agent_checkout_cta"
  | "floating_agent_waitlist_intent"
  | "floating_agent_analysis_handoff"
  | "floating_agent_human_whatsapp_handoff"
  | "floating_agent_diagnostic_handoff"
  | "floating_agent_fallback"
  | "floating_agent_whatsapp_inbound"
  | "floating_agent_whatsapp_reply_sent"
  | "floating_agent_whatsapp_delivery_failed";

export type LandingEvent = TrackingContext & {
  eventName: LandingEventName;
  metadata: Record<string, unknown>;
};

export function trackLandingEvent(
  context: TrackingContext,
  eventName: LandingEventName,
  metadata: Record<string, unknown> = {},
) {
  const payload: LandingEvent = {
    ...context,
    eventName,
    metadata,
  };

  if (typeof window !== "undefined") {
    window.dispatchEvent(new CustomEvent("landing:event", { detail: payload }));
    console.log("[landing:event]", payload);
  }

  return payload;
}
