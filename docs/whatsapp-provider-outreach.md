# WhatsApp Provider Outreach - Taliya CRM

## Goal

Find 2-3 WhatsApp providers for Taliya CRM POC, prioritizing:

- Official WhatsApp Business Platform access.
- WhatsApp Business App + Cloud API coexistence on the same studio number.
- Embedded Signup for multi-tenant SaaS onboarding.
- API/webhooks without forcing studios to use the provider's inbox as the main CRM.
- Low fixed cost per connected studio number.
- Clear pricing in BRL or USD for SaaS plans around R$497, R$897, and R$1.497/month.

## Providers To Contact

| Priority | Provider | Why contact | Contact / signup |
| --- | --- | --- | --- |
| P0 | 360dialog | Best documented API-first coexistence and partner platform baseline. | https://www.360dialog.com/contact |
| P0 | Gupshup | Strongest economic hypothesis if coexistence is supported for ISVs. | https://www.gupshup.ai/en/partners |
| P0 | Zenvia | Brazilian provider with documented WhatsApp Coexistence and local billing/support. | https://www.zenvia.com/precos/ |
| P1 | Huggy | Brazilian official Meta partner, documented coexistence, but likely inbox-first. | https://www.huggy.io/whatsapp |
| P1 | seven.io | Documents WhatsApp Coexistence, Embedded Signup, API, and webhooks. | https://help.seven.io/whatsapp |
| P1 | WATI | Documents coexistence, but likely platform/inbox-first. Useful price pressure. | https://www.wati.io/coexistence/ |
| P2 | Blip | Strong Brazil/Meta player, but needs confirmation on coexistence with existing Business App numbers. | https://www.blip.ai/fale-conosco |
| P2 | Infobip | Enterprise CPaaS with API and Brazil presence, pricing likely custom. | https://www.infobip.com/pt/contato |
| P2 | Sinch | Large CPaaS, possible but likely enterprise/custom pricing. | https://sinch.com/apis/messaging/whatsapp/ |
| P2 | Twilio | Excellent API, but coexistence with existing Business App number appears weak/unclear. | https://www.twilio.com/en-us/whatsapp |
| P2 | Bird | API/platform option, but needs coexistence and pricing confirmation. | https://bird.com/pricing/ |
| P2 | Vonage | API-first and potentially cheap, but existing Business App coexistence needs confirmation. | https://www.vonage.com/communications-apis/messages/pricing/ |
| P2 | CM.com | CPaaS option, but needs coexistence and partner model confirmation. | https://www.cm.com/whatsapp-business/ |

## Message - Portuguese Providers

Subject: WhatsApp Coexistence + API para CRM SaaS multi-tenant

Ola, time.

Estamos avaliando provedores oficiais de WhatsApp para o Taliya, um CRM SaaS para studios de Pilates no Brasil.

Nosso caso de uso:

- Cada studio conecta o seu proprio numero do WhatsApp Business.
- O studio deve continuar usando o WhatsApp Business App normalmente no celular.
- O Taliya precisa operar via API/webhooks no mesmo numero, em coexistencia oficial WhatsApp Business App + Cloud API.
- O onboarding ideal e Embedded Signup/self-service dentro do Taliya.
- Nao queremos que o cliente precise operar uma inbox/CRM de terceiros. A experiencia principal deve ficar dentro do Taliya.
- Precisamos suportar varios studios, cada um com seu proprio numero/WABA.

Podem confirmar, objetivamente:

1. Voces suportam WhatsApp Business App + Cloud API Coexistence no mesmo numero?
2. Esse fluxo funciona para numeros ja usados no WhatsApp Business App no Brasil?
3. Voces oferecem Embedded Signup ou fluxo equivalente para SaaS multi-tenant?
4. O Taliya pode receber todos os webhooks de inbound, status e mensagens enviadas manualmente pelo app?
5. Mensagens enviadas pela API aparecem no WhatsApp Business App?
6. Mensagens enviadas manualmente pelo app aparecem via webhook/API para o Taliya?
7. O cliente precisa usar a inbox/plataforma de voces ou podemos usar somente API/webhooks?
8. Existe API para criar/listar templates, status de aprovacao, health do numero e desconexao?
9. Qual o custo por numero conectado, setup, mensalidade minima, mensagens, templates e markup sobre tarifas Meta?
10. Existe plano/condicao para ISV/SaaS com dezenas ou centenas de clientes pequenos?

Contexto de preco: nossos planos sao aproximadamente R$497, R$897 e R$1.497 por mes. Precisamos entender se o custo por numero/mensagem permite operar studios pequenos sem margem negativa.

Se fizer sentido, queremos iniciar uma POC com 1 numero real de WhatsApp Business App e validar coexistencia + webhooks + envio via API.

Obrigado.

## Message - Global Providers

Subject: WhatsApp Business App Coexistence + API for multi-tenant SaaS CRM

Hi team,

We are evaluating official WhatsApp providers for Taliya, a CRM SaaS for Pilates studios in Brazil.

Our use case:

- Each studio connects its own WhatsApp Business number.
- The studio must continue using the WhatsApp Business App on their phone.
- Taliya needs to use API/webhooks on the same number through official WhatsApp Business App + Cloud API Coexistence.
- The ideal onboarding flow is Embedded Signup/self-service inside Taliya.
- We do not want customers to operate from a third-party inbox/CRM. The main experience must stay inside Taliya.
- We need to support multiple tenants, each with its own phone number/WABA.

Could you please confirm, explicitly:

1. Do you support WhatsApp Business App + Cloud API Coexistence on the same phone number?
2. Does this work for existing WhatsApp Business App numbers in Brazil?
3. Do you provide Embedded Signup or an equivalent flow for multi-tenant SaaS/ISV onboarding?
4. Can Taliya receive all webhooks for inbound messages, message status, and messages manually sent from the Business App?
5. Do API-sent messages appear in the WhatsApp Business App?
6. Do manually sent Business App messages appear through webhook/API to Taliya?
7. Can we use only API/webhooks, without requiring customers to use your inbox/platform?
8. Do you provide API access for template CRUD/status, phone number health, WABA/number management, and disconnect flows?
9. What are the exact costs per connected number, setup, monthly minimums, messages, templates, and markup over Meta fees?
10. Do you offer ISV/SaaS pricing for dozens or hundreds of small business customers?

Pricing context: our plans are around R$497, R$897, and R$1,497/month. We need to understand whether per-number and per-message costs work for small studios without killing SaaS margins.

If this is supported, we want to start a POC with one real WhatsApp Business App number and validate coexistence + webhooks + API sending.

Thanks.

## Response Scorecard

| Provider | Coexistence explicit | Existing BR Business App number | Embedded Signup | Multi-tenant SaaS/ISV | API-only allowed | App echoes to webhook | API echoes to app | Cost per number | Markup over Meta | Setup/minimum | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 360dialog | Yes | Likely; confirm BR geo eligibility | Yes | Yes | Yes | Yes | Yes | Per-channel fee + partner plan if using Partner Platform | Public page says zero Meta markup | Partner plan starts at $600/month / EUR500 + per-channel fee | Strong technical fit; POC priority, commercial risk for early MVP |
| Gupshup |  |  |  |  |  |  |  |  |  |  |  |
| Zenvia |  |  |  |  |  |  |  |  |  |  |  |
| Huggy |  |  |  |  |  |  |  |  |  |  |  |
| seven.io |  |  |  |  |  |  |  |  |  |  |  |
| WATI |  |  |  |  |  |  |  |  |  |  |  |
| Blip |  |  |  |  |  |  |  |  |  |  |  |
| Infobip |  |  |  |  |  |  |  |  |  |  |  |
| Sinch |  |  |  |  |  |  |  |  |  |  |  |
| Twilio |  |  |  |  |  |  |  |  |  |  |  |
| Bird |  |  |  |  |  |  |  |  |  |  |  |
| Vonage |  |  |  |  |  |  |  |  |  |  |  |
| CM.com |  |  |  |  |  |  |  |  |  |  |  |

## Decision Rules

- Reject if they cannot confirm official WhatsApp Business App + Cloud API coexistence.
- Reject if the studio must stop using WhatsApp Business App on the phone.
- Reject if the customer must operate primarily inside the provider's inbox/CRM.
- Prefer no fixed monthly fee per number, or fixed fee low enough for the R$497 plan.
- Prefer providers that support partner/ISV onboarding and tenant management through API.
- For MVP, accept manual provider dashboard steps only if the runtime integration is API/webhook-first.

## 360dialog Response Notes

360dialog support routed Taliya to the Partner Onboarding team, which is the correct path for a multi-client SaaS/ISV use case.

Useful public confirmations:

- Partner Platform is positioned for SaaS, ISVs, and resellers with multi-customer architecture.
- Partner page states unlimited WhatsApp Business Accounts through one API and zero markup on Meta fees.
- Integrated onboarding is described as client onboarding directly through the platform.
- Partner documentation confirms Partner API for programmatic management of WABAs and phone numbers.
- Coexistence documentation confirms existing WhatsApp Business App numbers can be onboarded to Cloud API while maintaining mobile app access and message history.
- Coexistence documentation confirms message echoes:
  - API-sent messages appear in the WhatsApp Business App.
  - App-sent messages appear in Cloud API conversation history.

Commercial concern:

- Partner Plan is a monthly platform fee at organisation level: Growth $600/month / EUR500/month, Premium $1,200/month / EUR1,000/month.
- Coexistence still requires normal 360dialog account/subscription and Cloud API fees.
- This may be too heavy before Taliya has enough paying studios, unless they offer startup/POC terms or Taliya starts with single-account API before Partner Platform.

Next ask to Partner Onboarding:

- Can Taliya start with a low-cost POC before committing to the $600/month Partner Plan?
- What is the exact per-channel fee for Brazil coexistence numbers?
- Is Brazil fully supported for WhatsApp Business App coexistence onboarding?
- Can Taliya use Embedded Signup and Partner API without exposing 360dialog UI to studios?
