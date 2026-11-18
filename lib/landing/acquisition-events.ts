/**
 * Landing interactions kept in the commercial database (ai_funnel_events), besides page views and
 * CTA clicks. Names only: no free text, phone, message or answer is ever attached to them.
 * Shared by the browser sender and the events route so both accept the same list.
 */
export const interactionEventNames = [
  "pain_selected",
  "agent_selected",
  "faq_item_opened",
  "custom_agent_diagnostic_started",
  "custom_agent_diagnostic_submitted",
  "custom_agent_diagnostic_generated",
  "custom_agent_diagnostic_failed",
  "signup_code_requested",
  "signup_completed",
] as const;
export type InteractionEventName = (typeof interactionEventNames)[number];
export const isInteractionEvent = (name: string): name is InteractionEventName =>
  (interactionEventNames as readonly string[]).includes(name);
