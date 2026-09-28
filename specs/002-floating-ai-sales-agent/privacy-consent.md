# Privacy, LGPD And Consent Requirements: Floating AI Attendant

## Purpose

Define privacy and consent requirements for the Atendente IA across web chat and WhatsApp.

This is a product/engineering checklist, not legal advice. Final policy text should be reviewed before launch.

## Data Principles

The attendant should follow privacy-by-design behavior:

- collect only what is needed for the selected path;
- explain why contact data is requested;
- avoid sensitive student health/payment data;
- store summaries and structured IDs instead of full transcripts by default;
- respect WhatsApp opt-out;
- keep provider secrets and private prompts server-side;
- avoid hidden or creepy personalization.

## Web Chat Requirements

- The chat UI does not need to label every interaction as AI, but it must not impersonate a named human.
- AI/privacy transparency must be available before contact capture through privacy/consent copy or a clear supporting link.
- The chat must provide or link to privacy information before collecting contact details.
- The agent must ask contact details only after intent exists: analysis, human assistance, custom-agent follow-up or strong buying interest.
- The agent must explain why it asks for WhatsApp/email.
- The agent must not ask for card data, billing documents, student health records or private student records.
- The chat must not expose full transcripts to n8n by default; send safe summary and structured metadata.

## WhatsApp Requirements

- Automated WhatsApp replies are allowed only for inbound or explicitly opted-in conversations.
- Human handoff must include opt-in/consent status when available.
- Opt-out language must stop automated replies except for one brief confirmation when allowed.
- The system must not send cold outbound, campaigns or broadcast messages in this feature.
- WhatsApp contact identifiers must be stored safely and not exposed to client code.

## Retention And Deletion

- Conversation/session records should have a retention policy before production.
- Safety/usage logs should avoid raw sensitive content.
- The system should support deletion/suppression of conversation records according to the chosen privacy process.

## Agent Behavior

If the visitor shares unnecessary sensitive data, the agent should:

1. avoid repeating it;
2. say it does not need that level of detail;
3. redirect to general operational context;
4. avoid storing it in summaries/handoffs.

## Acceptance Criteria

- Agent asks for contact only after intent exists.
- Agent explains contact purpose.
- Sensitive data prompts are redirected.
- WhatsApp opt-out stops automated replies.
- n8n payloads use safe summaries, not full raw transcripts by default.
- Privacy/consent copy is available before contact capture.
