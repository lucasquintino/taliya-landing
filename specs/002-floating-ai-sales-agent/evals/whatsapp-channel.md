# WhatsApp Channel Fixtures

## Inbound Product Questions

| Inbound WhatsApp text | Expected behavior |
| --- | --- |
| "O que esse sistema faz?" | Normalize to shared AI request with `channel: "whatsapp"` and explain operational AI agents. |
| "Isso e um chatbot?" | Explain difference from generic chatbot and keep Pilates context. |

## Pain Mapping

| Inbound WhatsApp text | Expected pain | Expected agents |
| --- | --- | --- |
| "Minhas reposicoes estao uma bagunca" | `reposicoes` | `atendimento`, `agenda` |
| "Interessados pedem valor e somem" | `interessados` | `vendas`, `atendimento` |
| "Mensalidades ficam esquecidas" | `mensalidades_atrasadas` | `financeiro`, `atendimento` |

## Custom Agent

- "Quero um agente de marketing" must route to Agente sob medida.
- The agent must ask which marketing routine should be handled.
- The agent must request email or cellphone/WhatsApp and say the team will contact the visitor.

## Provider Behavior

- Duplicate webhook with the same `providerMessageId` must not send a second reply.
- Missing or invalid Meta signature must return `401`.
- Opt-out text such as "nao quero mais receber mensagem" must stop automated replies after one brief confirmation when allowed.
- Provider send failure must be logged without affecting the web widget route.

## Production E2E Cases

- A valid signed Meta webhook POST must produce one stored inbound turn, one safe AI response and one provider send attempt.
- A duplicate valid signed Meta webhook POST with the same provider message ID must not create a duplicate reply, lead or n8n handoff.
- A WhatsApp lead marked `human_active` in Sales Inbox must store the inbound message and suppress the AI reply.
- A WhatsApp lead marked `do_not_contact` must suppress AI and human proactive follow-up.
- An operator `send_whatsapp_message` action must send through the server-side provider adapter and record the action/audit event.
- A failed operator WhatsApp send must remain visible and retryable in Sales Inbox.
- An out-of-window follow-up without an approved Meta template must be blocked and recorded as `template_blocked_not_approved`.
- Unsupported payload types such as image, audio, document, location or sticker must not be sent raw to the model; when allowed, the system may ask the visitor to describe the request in text.
