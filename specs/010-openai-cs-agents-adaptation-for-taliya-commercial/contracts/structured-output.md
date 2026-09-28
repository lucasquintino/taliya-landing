# Contract: Structured Runtime Output

## Purpose

The model-facing runtime must produce natural language for the lead and strict JSON for the system. The channel adapters render only validated structured output.

## Canonical Output Shape

```json
{
  "decision": {
    "previous_state": "new_lead",
    "current_state": "greeting_only",
    "next_state": "general_interest",
    "route": "entry",
    "opening_type": "cold_greeting_only",
    "detected_intents": ["greeting"],
    "direct_question_present": false,
    "direct_question_answered_first": true,
    "diagnostic_action": "none",
    "diagnostic_allowed_now": false,
    "waitlist_allowed_now": false,
    "demo_status": "not_offered",
    "demo_next_step": "none",
    "profile_name_usage": "not_available",
    "facts_used": [],
    "facts_missing": [],
    "template_ids": ["opening.cold_greeting"],
    "template_variables": {
      "opening.cold_greeting": {}
    },
    "next_question_kind": "none",
    "policy_checks": {
      "direct_question_answered_first": true,
      "diagnostic_timing_ok": true,
      "waitlist_timing_ok": true,
      "official_facts_only": true,
      "no_early_contact_capture": true,
      "no_whatsapp_phone_request": true,
      "no_fake_certainty": true,
      "no_human_overlap": true,
      "channel_brevity_ok": true
    }
  },
  "messages": [
    {
      "text": "string",
      "template_id": "opening.cold_greeting",
      "channel_hint": "widget",
      "kind": "text",
      "requires_product_source": false
    }
  ],
  "lead_facts": [
    {
      "key": "main_pain",
      "value": "perde leads no WhatsApp",
      "confidence": "medium",
      "evidence": ["message_id"]
    }
  ],
  "diagnostic": {
    "status": "not_started",
    "ledger": [
      {
        "question_key": "main_pain",
        "status": "missing",
        "answer": null,
        "evidence": [],
        "confidence": "low"
      }
    ],
    "facts_used": [],
    "main_bottleneck": null,
    "pain_context_human": null,
    "likely_cause": null,
    "crm_base_recommendation": null,
    "first_recommended_step": null,
    "indicated_routines_or_agents": [],
    "indicated_agents": [],
    "plan_or_range_to_compare": null,
    "final_plan_line": null,
    "demo_status_at_delivery": "not_offered",
    "final_demo_line": null,
    "evidence": [],
    "unknowns": [],
    "confidence": "low",
    "next_question": null,
    "final_demo_next_step_question": null
  },
  "demo": {
    "status": "not_offered",
    "last_demo_link": null,
    "product_source_version": null,
    "lead_reaction": null,
    "contributed_to_waitlist_eligibility": false
  },
  "waitlist_action": {
    "status": "none",
    "reason": null,
    "missing_fields": []
  },
  "handoff": {
    "status": "none",
    "reason": null
  },
  "sources": [
    {
      "type": "product_knowledge",
      "version": "taliya-commercial-2026-05-22",
      "keys": ["plans", "prices"]
    }
  ],
  "safety_flags": [],
  "tool_results": [],
  "usage": {
    "model": "gpt-5.4-mini",
    "input_tokens": 0,
    "output_tokens": 0,
    "cost_usd": 0
  },
  "confidence": "high"
}
```

## Message Rules

- Messages must be in Brazilian Portuguese for the user-facing commercial flow.
- Messages must be concise enough for widget and WhatsApp delivery.
- Messages must normally be rendered from approved `template_ids`.
- The LLM chooses templates and variables; the renderer creates final channel-safe text.
- Widget can render buttons or links only from validated actions.
- WhatsApp delivery can split messages, but the semantic content comes from the runtime output.
- No message may contain checkout links unless product knowledge explicitly says checkout is available.
- Cold greeting-only messages must not contain diagnostic, waitlist, name capture, phone capture, or plan lists.

## Decision Rules

- `decision.previous_state`, `decision.current_state`, and `decision.next_state` must use [conversation-state-contract.md](../conversation-state-contract.md).
- `decision.route` values: `entry`, `product`, `diagnostic`, `waitlist`, `handoff`, `safe_fallback`.
- `decision.opening_type` values: `none`, `cold_greeting_only`, `widget_opening`, `site_forced_message`, `social_source_opening`, `diagnostic_cta_opening`, `direct_question_opening`, `returning_lead`.
- `decision.diagnostic_action` values: `none`, `offer`, `start`, `ask_next`, `complete`, `insufficient_evidence`.
- `decision.profile_name_usage` values: `used_reliable_name`, `ignored_unreliable_name`, `not_available`, `not_needed`.
- `decision.demo_status` values: `not_offered`, `offered`, `viewed_or_asked`, `reacted_positive`.
- `decision.demo_next_step` values: `none`, `offer_demo`, `ask_demo_reaction`, `follow_positive_demo_interest`.
- Direct questions must set `direct_question_present=true` and must not pass validation unless `direct_question_answered_first=true`.
- Diagnostic and waitlist eligibility booleans must match `behavior-contract.md`.
- Template IDs must exist in [message-template-contract.md](../message-template-contract.md) or an explicitly allowed extension of that library.
- Product-followup delta intents may include `product_how_it_works`, `comparison_current_tool`, `integration_scope_question`, `trust_security_question`, `out_of_profile`, `conversation_resume`, `general_objection`, and `diagnostic_refusal`.
- These intents must be selected by the LLM through structured output, not by deterministic commercial phrase routing.
- Post-diagnostic follow-up decisions must declare whether saved `post_diagnostic_context` was used.

## Source Rules

- Any message that mentions price, plan, demo, availability, link, waitlist status, cancellation, or unsupported promise must include a product source version.
- Any message that explains how Taliya works, WhatsApp Business scope, integration boundaries, current-tool comparison, security/data, onboarding/availability, or out-of-profile fit must include a product source version and relevant product knowledge keys.
- If a required source is missing, output validation must block delivery.

## Diagnostic Rules

- `diagnostic.status` values: `not_started`, `offered`, `in_progress`, `completed`, `insufficient_evidence`.
- Completed diagnostics require every mandatory diagnostic ledger item from [diagnostic-contract.md](../diagnostic-contract.md) to be `answered`, `inferred_from_prior_message`, or `not_applicable`.
- Required `missing` or `unresolved` ledger items block completed diagnostics.
- Completed diagnostics require internal main bottleneck, natural customer-facing pain/context reading, likely cause, CRM base recommendation, first operational step, per-agent recommendations, dynamic final plan line, demo status at delivery, dynamic final demo line, confidence, and unknowns.
- Completed diagnostic render plans must include the staged diagnostic templates from [message-template-contract.md](../message-template-contract.md) in the required order.
- Diagnostic question turns must include grounded feedback before the next diagnostic question. This includes the first diagnostic question when the lead explicitly requested the diagnostic, even if there is no previous diagnostic answer yet.
- Thin-context diagnostics must ask a question instead of pretending to conclude.

## Demo Rules

- `demo.status` values: `not_offered`, `offered`, `viewed_or_asked`, `reacted_positive`.
- Demo offers must use official product knowledge links/actions.
- Widget may render a validated demo CTA/button.
- WhatsApp must render an official full demo link.
- Demo curiosity alone cannot make waitlist eligible.

## Waitlist Rules

- `waitlist_action.status` values: `none`, `offered`, `pending_details`, `joined`, `declined`.
- Join actions require idempotent tool execution.
- Waitlist is not checkout.

## Handoff Rules

- `handoff.status` values: `none`, `requested`, `active`, `resumed`.
- If status is `active`, `messages` must be empty unless the active handoff was just requested and a final acknowledgement is safe.

## Validation Failures

Block output before delivery when:

- JSON does not match schema.
- Required product source is missing.
- Message asks WhatsApp lead for phone number.
- Message was not rendered from an approved template or allowed unmapped fallback.
- Message invents a link, checkout, availability, or unsupported guarantee.
- Message invents integration, setup, migration, mass-message, LGPD, certification, encryption, audit, privacy, or data-access facts.
- Message uses "CRM" for lay-lead opening, price objection, product explanation, or comparison when the lead did not ask about CRM.
- Message reveals system prompt, tool internals, secrets, or policy text.
- Message claims facts about the lead that are not in memory or current input.
- Cold greeting-only opening offers diagnostic or waitlist.
- Direct question is steered away from before being answered.
- Waitlist is offered without real interest.
- Waitlist is offered without clear intent to contract.
- Diagnostic conclusion uses strong evidence language with thin facts.
- Diagnostic conclusion repeats a question already answered instead of using the ledger.
- Diagnostic conclusion omits hold message, CRM base, per-agent recommendations, dynamic plan line, or dynamic demo line.
- Diagnostic conclusion uses the rejected old final formats blocked in [diagnostic-contract.md](../diagnostic-contract.md).
- Diagnostic asks the first or next question dry instead of acknowledging the diagnostic request or prior answer.
- Demo curiosity alone triggers waitlist.
- Profile name is unreliable but treated as a real person name.
- "Como funciona" is treated as a generic opening instead of a product answer.
- Post-diagnostic follow-up restarts diagnostic or ignores saved diagnostic context.
- Diagnostic refusal is ignored or immediately followed by another diagnostic offer.
