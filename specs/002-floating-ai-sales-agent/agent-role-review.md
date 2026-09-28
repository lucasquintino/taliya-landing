# Agent Role Review: Floating AI Attendant

## Purpose

Review the 12 roles after the latest product decisions:

- Atendente IA answers questions and sells.
- Live AI layer is mandatory.
- The seven primary agents have per-studio configuration.
- Agente sob medida is only for operations outside the seven mapped domains, such as Marketing.
- When Agente sob medida is identified, the attendant asks for more details, asks email or cellphone/WhatsApp and says the team will contact the visitor.
- The same attendant must work in the web widget and WhatsApp.
- Consultor-led conversion is now the primary path; the visitor is not sent cold to plans.
- The consultor may route to the guided demo, plans page or checkout after diagnosis, explicit plan-comparison intent or strong buying intent.
- If the visitor wants a human before subscribing, WhatsApp is the assisted-closing path.
- The agent's commercial default is to sell the configured recommended/highest-value plan when the studio has broad pain, multi-agent needs or complete-system intent.
- Lower plans support comparison, budget-fit and objection handling; they are not equal default recommendations unless configuration or visitor intent says so.
- The agent must answer purchase-relevant questions before steering back to conversion.
- The agent must not make the plan page the default first destination from the landing.

## Review Summary

| Role | Status | Decision |
|------|--------|----------|
| 1. Receptionist | Approved with caution | Must not ask contact at first message |
| 2. Product Explainer | Approved | Explains system, not generic chatbot/CRM |
| 3. Pain Diagnostician | Approved with scope note | Must classify pain without turning custom rules into Agente sob medida |
| 4. Agent Mapper | Approved after correction | Primary-agent configuration stays inside primary agents |
| 5. Objection Handler | Approved after correction | Handles unsupported features and Marketing/custom-agent requests |
| 6. Value Translator | Approved | Must avoid guaranteed financial outcomes |
| 7. Qualification Collector | Approved after correction | For Agente sob medida, collects operation summary plus email/cellphone/WhatsApp |
| 8. Conversion Closer | Approved after adjustment | Diagnoses first, offers demo/plans/checkout when appropriate and prioritizes configured recommended/highest-value plan when fit |
| 9. Handoff Summarizer | Approved | Summarizes safe context for form/n8n |
| 10. Safety Gatekeeper | Approved | Must override every other role when risk appears |
| 11. Context-Aware Guide | Approved | Uses page signals without sounding invasive |
| 12. Fallback Operator | Approved | Degraded state only; not replacement for live AI |

## Channel Review

Approved with guardrails.

- Web widget and WhatsApp share the same 12-role agent brain.
- WhatsApp changes delivery mechanics, identity, session persistence and opt-out handling; it does not create a separate sales agent.
- WhatsApp automatic replies are allowed only inside inbound or explicitly opted-in conversations.
- Proactive campaigns, broadcasts and cold outbound are out of scope.
- n8n remains post-handoff automation and must not become the real-time WhatsApp chat brain.
- WhatsApp human assistance is allowed when requested by the visitor before subscribing.
- WhatsApp uses the same answer policy and plan recommendation rules as the web widget.

## Key Corrections Made

### Priority Order

Objection handling now runs before pain mapping. This avoids wrong behavior such as mapping an already-known pain when the visitor actually asked about price, setup, integrations or unsupported functionality.

### Agente Sob Medida Boundary

The review confirms:

- Studio-specific rules inside Atendimento, Agenda, Vendas, Financeiro, Retencao, Gestao or Historico/Evolucao are configuration of those agents.
- Agente sob medida applies only to a new operation outside those seven domains.
- Marketing is the canonical example of Agente sob medida.

### Contact Capture For Agente Sob Medida

When the request is truly Agente sob medida, the agent must:

1. Ask what operation the visitor wants.
2. Capture a short summary.
3. Ask whether they prefer email or cellphone/WhatsApp.
4. Say the team will contact them.
5. Trigger n8n only after contact/intent exists.

## Role-by-Role Review

### 1. Receptionist

Approved.

Risk:

- Asking for WhatsApp too early would feel pushy.

Rule:

- First message must welcome, explain options and offer quick replies.

### 2. Product Explainer

Approved.

Risk:

- Calling the product CRM, chatbot or generic automation.

Rule:

- Explain as operational AI agents for studio routines.

### 3. Pain Diagnostician

Approved with scope note.

Risk:

- Treating every specific rule as Agente sob medida.

Rule:

- If the pain belongs to a primary agent domain, it stays there as configurable behavior.

### 4. Agent Mapper

Approved after correction.

Risk:

- Recommending all agents or inventing a new primary agent.

Rule:

- Map to one to three primary agents unless the operation is truly outside the seven domains.

### 5. Objection Handler

Approved after correction.

Risk:

- Promising unsupported features or exact price/timeline.
- Dodging buyer questions and pushing CTA before the visitor feels answered.
- Recommending a lower plan too early and weakening the premium sale.

Rule:

- For unsupported features, separate "primary-agent configuration" from "Agente sob medida".
- Answer purchase-relevant questions directly from trusted configuration or approved context, then return to the next conversion step.
- When plan fit is broad or multi-agent, frame the configured recommended/highest-value plan before lower plans.

### 6. Value Translator

Approved.

Risk:

- Overpromising financial result.

Rule:

- Use cautious language and tie value to operational clarity, time, occupancy and follow-up.

### 7. Qualification Collector

Approved after correction.

Risk:

- Asking too many fields or asking contact before intent.

Rule:

- For normal diagnostic flow, collect one field at a time after intent.
- For Agente sob medida, collect requested operation and contact preference.

### 8. Conversion Closer

Approved after adjustment.

Risk:

- Pushing analysis when the visitor is ready to subscribe would slow conversion.
- Sending a cold visitor straight to plans would weaken the consultative sale.
- Asking for payment/card data in chat would be unsafe.

Rule:

- Offer plan recommendation first, then checkout for high buying intent or confirmed recommended plan.
- Offer guided demo when the visitor needs to see the product before discussing price.
- Recommend the configured recommended/highest-value plan for broad pain, multi-agent need or complete-system intent.
- Use lower plans only for explicit budget/narrow-scope intent, missing higher-plan configuration or comparison after the recommended plan has been framed.
- Offer human WhatsApp assistance when the visitor asks to talk to a person before subscribing.
- Keep "analise da operacao", "raio-x do studio" or "Dinheiro na Mesa" for visitors who need more context.
- Never collect payment/card data in chat or WhatsApp.

### 9. Handoff Summarizer

Approved.

Risk:

- Sending full raw transcript or sensitive details to n8n.

Rule:

- Summarize safely with IDs, categories and missing fields.

### 10. Safety Gatekeeper

Approved.

Risk:

- Treating guardrails as prompt-only.

Rule:

- Guardrails must run before and after the model and can override the model-selected role.

### 11. Context-Aware Guide

Approved.

Risk:

- Sounding like hidden surveillance.

Rule:

- Reference page context naturally and only when captured.

### 12. Fallback Operator

Approved.

Risk:

- Letting fallback become the main chat.

Rule:

- Fallback only for provider failure, timeout, invalid output or guardrail block.

## Remaining Open Wording Decision

The implementation should decide whether the analysis CTA copy says:

- "Diagnostico"
- "Analise da Operacao"
- "Raio-X do Studio"
- "Analise Dinheiro na Mesa"

Recommendation: use "Assinar plano" for direct conversion, "Falar com humano no WhatsApp" for assisted close and "Analise da Operacao" or "Raio-X do Studio" for consultative analysis.
