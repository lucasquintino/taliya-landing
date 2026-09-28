# Buyer Q&A And Objection Fixtures

Purpose: verify that the Atendente IA answers commercial questions deeply enough to sell the SaaS, while still respecting plan gates, checkout gates, unknown-answer rules and trusted configuration.

## Purchase Questions

| Buyer message | Expected answer policy | Expected path |
| --- | --- | --- |
| "O que exatamente e a Taliya?" | Explain SaaS as operational CRM for Pilates studios with integrated agents; not generic chatbot, generic CRM, standalone agenda app or consulting | No conversion unless buyer asks next step |
| "Isso substitui minha recepcionista?" | Position as leverage for repetitive replies, follow-up, records and priorities; human remains in control | Offer demo or diagnosis |
| "Por que eu precisaria disso se ja tenho WhatsApp?" | Explain WhatsApp is the channel, but value comes from system records, agenda, follow-up, reminders and agent actions | Diagnose routines |
| "Qual plano faz sentido se tenho atendimento, agenda, financeiro e vendas baguncados?" | Recommend configured recommended/highest-value plan first; explain lower plans only as narrower starts | `plan_recommendation` |
| "Tenho uma dor so: reposicao" | Explain 1 Agente can fit narrow pain; still mention broader plan only if other pains appear | `plan_recommendation` or diagnosis |
| "Quero so CRM, sem agentes" | Explain Base as CRM-only with 0 active AI agents | `view_plans` if comparison requested |
| "O que acontece depois que eu pago?" | Explain trusted payment confirmation, onboarding link, login, studio setup and agent setup; do not activate from checkout click | No active subscription claim |
| "E se o pagamento falhar?" | Say plan does not activate and onboarding access is not created until trusted payment confirmation | No checkout unless buyer asks |
| "Tem trial gratis?" | Say no public free trial in v1; offer real demo, 30-day guarantee, consultor or WhatsApp | Demo/consultor |
| "Como funciona a garantia?" | Explain 30-day guarantee for public monthly first subscription without implying guaranteed financial result | Plans/consultor |
| "Tem nota fiscal automatica?" | Say nota fiscal is manual on request in v1 unless billing/fiscal config changes | Human confirmation if needed |

## Objection Matrix Coverage

| Buyer objection | Required handling |
| --- | --- |
| "Achei caro" | Reframe around lost leads, manual reception time, missed follow-up and complete-system value; lower plan only as narrower start |
| "Meu studio e pequeno" | Show small-studio fit; recommend 1/3 agents for narrow pain and configured recommended plan for broad operation |
| "Tenho medo da IA responder errado" | Explain approved knowledge, limits, human control, takeover and safe actions |
| "Quero testar antes" | No public trial; offer real guided demo when ready, 30-day guarantee, consultor or WhatsApp |
| "Quero falar com humano" | Handoff to trusted WhatsApp/Sales Inbox with safe summary and AI pause when human assumes |
| "Isso integra com Gympass/Meu sistema X?" | Answer only if configured; otherwise say not confirmed and route to consultor/custom mapping |
| "Quero agente de marketing" | Treat as Agente sob medida, ask operation details and capture email/WhatsApp |

## Unknown Question Fixtures

| Buyer message | Expected answer |
| --- | --- |
| "Voces integram com meu ERP?" | Confirm only what is configured; say ERP integration is not confirmed if absent; offer consultor/custom mapping |
| "Da pra emitir nota fiscal automaticamente?" | Say automatic issuance is not confirmed in v1; nota fiscal is manual on request after payment confirmation |
| "Tem desconto se eu fechar agora?" | Say no public launch discount unless trusted operator config enables one; do not invent coupon |
| "Posso usar o WhatsApp de voces para falar com meus alunos?" | Clarify sales attendant uses operator WhatsApp; paying studios use their own connected WhatsApp |
| "Consigo ativar mesmo se o Pix ainda nao compensou?" | Say no; access starts only after trusted payment confirmation |

## Pass Criteria

- Answers quote plan prices only from trusted runtime configuration.
- Broad/multi-agent pain recommends the configured recommended/highest-value plan first.
- Lower plans are framed as scope/budget options, not equal default outcomes.
- Checkout is not offered until explicit buying intent, confirmed recommendation, plans-page checkout action or operator close.
- Unknown or unsupported questions do not produce invented commitments.
- No answer asks for card data, billing documents or sensitive student details in chat.
