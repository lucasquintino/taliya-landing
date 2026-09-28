import type { LeadRecord, LeadStatus } from "./leads";

export type FollowUpEligibility =
  | {
      allowed: true;
      reason: "hot_lead_with_contact" | "warm_lead_with_contact" | "scheduled_by_operator";
      maxTouches: number;
      cadence: string[];
    }
  | {
      allowed: false;
      reason:
        | "missing_contact"
        | "opted_out"
        | "terminal_status"
        | "cold_without_permission"
        | "unsupported_channel";
    };

const terminalStatuses: LeadStatus[] = ["won", "lost", "do_not_contact"];

export function getFollowUpEligibility(lead: LeadRecord): FollowUpEligibility {
  if (terminalStatuses.includes(lead.status)) return { allowed: false, reason: "terminal_status" };
  if (lead.consentContext?.whatsappOptOut) return { allowed: false, reason: "opted_out" };

  const hasContact = Boolean(lead.contact.normalizedWhatsapp || lead.contact.whatsapp || lead.contact.email);
  if (!hasContact) return { allowed: false, reason: "missing_contact" };

  if (lead.priority === "hot") {
    return {
      allowed: true,
      reason: "hot_lead_with_contact",
      maxTouches: 4,
      cadence: ["immediate_operator_notification", "15m_if_allowed", "D+1", "D+3", "D+7_final"],
    };
  }

  if (lead.priority === "warm") {
    return {
      allowed: true,
      reason: "warm_lead_with_contact",
      maxTouches: 2,
      cadence: ["D+1", "D+3"],
    };
  }

  return { allowed: false, reason: "cold_without_permission" };
}
