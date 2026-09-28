# Simulation Review Matrix: Humanized Sales And Waitlist Flow

**Feature**: [spec.md](./spec.md)
**Created**: 2026-05-20
**Purpose**: Define realistic start, middle and end simulations that must be reviewed before implementation is accepted.

## Review Stages

### R0 - Script Review

- Review every P1 scenario in this file before coding.
- Confirm the expected tone does not feel aggressive.
- Confirm waitlist appears only after high intent.
- Confirm widget and WhatsApp differences are intentional.

### R1 - Automated Eval Review

- Convert all P1 scenarios into automated evals.
- Required commands: `npm run lint`, `npx tsc --noEmit`, `npm run build`, affected eval scripts.
- Failure in any P1 scenario blocks release.
- **2026-05-20 result**: Passed. See [implementation-review-2026-05-20.md](./implementation-review-2026-05-20.md).

### R2 - Local API Simulation

- Run local Next server with mock provider where possible.
- Simulate both `/api/landing/ai-attendant` and `/api/landing/ai-attendant/whatsapp`.
- Inspect response text and structured fields.
- **2026-05-20 result**: Passed against `http://localhost:3108` with mock WhatsApp send token.

### R3 - Production-Like WhatsApp Webhook Simulation

- Send signed/mock Meta webhook payloads.
- Confirm storage in `whatsapp_sessions`, `whatsapp_provider_messages`, `whatsapp_message_outbox`, `sales_leads`.
- Confirm duplicate webhook and human takeover behavior still pass.
- **2026-05-20 result**: Passed via `npm run eval:whatsapp-webhook` and `npm run eval:lead-pipeline`; real Meta send was intentionally mocked.

### R4 - Real WhatsApp Number Smoke Review

- Clean the test phone state in database.
- Send real messages from the user's WhatsApp to Taliya.
- Verify:
  - first response asks name;
  - after name, asks pain/intent;
  - after pain/intent, offers diagnostic;
  - no waitlist appears early.
- **Status**: Pending manual real-number smoke after deploy.

### R5 - Product Owner Conversation Review

- Product owner reads transcripts for every P1 scenario marked mandatory below.
- Mark each as pass, fail or needs copy adjustment.
- No public traffic increase until R5 passes.
- **Status**: Pending product-owner transcript review.

## Scenario Format

Each scenario includes:

- channel;
- lead source;
- starting messages;
- expected route;
- expected allowed behavior;
- prohibited behavior;
- storage expectation;
- review notes.

## P1 Start Scenarios

### S001 - WhatsApp Greeting Only

- **Channel**: WhatsApp
- **Lead source**: Direct message to Taliya number
- **Conversation**:
  - Lead: "Oi"
- **Expected**: Agent asks for name in a short human way.
- **Allowed copy**: "Oi, tudo bem? Com quem eu falo?"
- **Prohibited**: diagnostic offer, waitlist, plans, demo, long widget greeting, "Prazer, oi".
- **Storage**: session created, no lead required yet unless current implementation stores early contact.

### S002 - WhatsApp Product Curiosity

- **Channel**: WhatsApp
- **Lead source**: Landing visitor moved to WhatsApp
- **Conversation**:
  - Lead: "Vi o site de voces. O que e a Taliya?"
- **Expected**: Brief acknowledgement and name request before full answer.
- **Allowed copy**: "Claro, te explico sim. Antes: com quem eu falo?"
- **Prohibited**: full pitch before name, waitlist, immediate diagnostic.
- **Storage**: session captures inbound message.

### S003 - WhatsApp Price First

- **Channel**: WhatsApp
- **Conversation**:
  - Lead: "Quanto custa?"
- **Expected**: Acknowledge and ask name.
- **Allowed copy**: "Claro, te explico. Com quem eu falo?"
- **Prohibited**: dumping plans, checkout, waitlist, saying "depende" without moving conversation.

### S004 - WhatsApp Demo First

- **Channel**: WhatsApp
- **Conversation**:
  - Lead: "Tem demo?"
- **Expected**: Acknowledge demo interest and ask name.
- **Prohibited**: sending demo link immediately if demos are not configured, waitlist.

### S005 - Widget Greeting

- **Channel**: Web widget
- **Lead source**: `/pilates`
- **Conversation**:
  - Visitor opens widget or sends "ola"
- **Expected**: Widget may use landing-context opening and can offer common options.
- **Prohibited**: waitlist, checkout, broad availability claim.

### S006 - Widget Price First

- **Channel**: Web widget
- **Lead source**: `/pilates`
- **Conversation**:
  - Visitor: "Quanto custa?"
- **Expected**: Agent answers with configured price framing or plan summary, then asks one qualifying question or offers diagnostic. It must not offer waitlist.
- **Prohibited**: checkout, waitlist, unsupported discount, broad availability claim.

### S007 - Widget Demo First

- **Channel**: Web widget
- **Lead source**: `/pilates`
- **Conversation**:
  - Visitor: "Quero ver uma demo"
- **Expected**: If demo is configured, agent routes to demo; if not, agent explains the demo is not ready and offers diagnostic or concise product explanation. It must not offer waitlist unless later high intent occurs.
- **Prohibited**: fake demo, waitlist before demo-positive signal, checkout.

### S008 - Widget Diagnostic Positive

- **Channel**: Web widget
- **Lead source**: `/pilates`
- **Conversation**:
  - Diagnostic recommendation delivered.
  - Visitor: "Faz sentido"
- **Expected**: Agent may offer the waitlist narrative because this is a positive response after diagnostic.
- **Prohibited**: checkout, immediate availability claim, promising date.

### S009 - Widget Diagnostic Negative

- **Channel**: Web widget
- **Lead source**: `/pilates`
- **Conversation**:
  - Diagnostic recommendation delivered.
  - Visitor: "Nao sei se e pra mim"
- **Expected**: Agent offers demo/clarification or asks what did not fit. It must not offer waitlist.
- **Prohibited**: waitlist, pressure, repeating the same recommendation unchanged.

## P1 Middle Scenarios

### S101 - Name Then Pain/Intent

- **Channel**: WhatsApp
- **Conversation**:
  - Agent: asks name
  - Lead: "Lucas"
- **Expected**: Agent says "Prazer, Lucas" and asks pain/intent.
- **Allowed copy**: "Prazer, Lucas. Me conta: o que te fez procurar a Taliya agora?"
- **Prohibited**: waitlist, plans, demo, diagnostic offer before pain/intent.

### S102 - Name And Intent In Same Message

- **Channel**: WhatsApp
- **Conversation**:
  - Lead: "Sou a Marina, quero saber valores"
- **Expected**: Agent extracts name and intent, then asks minimum pain/context before diagnostic or plans.
- **Prohibited**: treating "valores" as enough for waitlist or checkout.

### S103 - Pain Then Diagnostic Offer

- **Channel**: WhatsApp
- **Conversation**:
  - Lead has given name.
  - Agent asks pain/intent.
  - Lead: "Minhas reposicoes sao uma bagunca"
- **Expected**: Agent acknowledges pain and offers free diagnostic.
- **Allowed copy**: "Entendi. A gente esta oferecendo um diagnostico gratuito para studios de Pilates para mapear isso com calma antes de falar em plano. Quer fazer por aqui?"
- **Prohibited**: waitlist, price dump, demo before diagnostic unless lead refuses diagnostic.

### S104 - Refuses Diagnostic

- **Channel**: WhatsApp or widget
- **Conversation**:
  - Agent offers diagnostic.
  - Lead: "Nao, quero so tirar uma duvida"
- **Expected**: Agent respects and answers the doubt path.
- **Prohibited**: forcing diagnostic or waitlist.

### S105 - Early Contract Request

- **Channel**: WhatsApp
- **Conversation**:
  - Lead has name but little/no context.
  - Lead: "Quero contratar"
- **Expected**: Agent does not offer waitlist cold; asks for minimum context or proposes diagnostic.
- **Prohibited**: waitlist without context, checkout, saying product is open for immediate onboarding.

### S106 - Refuses Name But Asks Direct Question

- **Channel**: WhatsApp
- **Conversation**:
  - Agent asks name.
  - Lead: "Prefiro nao falar, so quero saber se funciona no WhatsApp"
- **Expected**: Agent answers briefly and says it can help better with a name later. It must not block the conversation.
- **Prohibited**: refusing to answer, waitlist, diagnostic offer before any pain/intent.

### S107 - Ambiguous Yes After Diagnostic

- **Channel**: WhatsApp or widget
- **Conversation**:
  - Diagnostic recommendation delivered.
  - Agent asks whether the recommendation makes sense or whether the lead wants to see next step.
  - Lead: "sim"
- **Expected**: If immediate context clearly asks whether it makes sense, agent can offer waitlist; if context is ambiguous, agent asks one clarifying question before waitlist.
- **Prohibited**: always treating "sim" as waitlist consent.

## P1 End Scenarios

### S201 - Diagnostic Complete, Positive Response

- **Channel**: WhatsApp or widget
- **Conversation**:
  - Diagnostic completed and recommendation delivered.
  - Agent asks whether it makes sense.
  - Lead: "Faz sentido, quero seguir"
- **Expected**: Agent offers waitlist with approved narrative.
- **Allowed copy**: "Boa. Hoje estamos trabalhando com um numero pequeno de studios. Se fizer sentido para voce, posso colocar seu studio numa lista de espera e chamamos assim que possivel."
- **Prohibited**: checkout, promise of date, "beta" framing, saying open onboarding is available.
- **Storage**: lead waitlist status becomes `offered`, not `joined`.

### S202 - Diagnostic Complete, Negative Response

- **Channel**: WhatsApp or widget
- **Conversation**:
  - Recommendation delivered.
  - Lead: "Nao sei se faz sentido"
- **Expected**: Agent does not offer waitlist; offers demo, asks what did not fit or answers doubts.
- **Prohibited**: waitlist, pressure, repeating same recommendation.

### S203 - Diagnostic Complete, Wants Demo

- **Channel**: Widget or WhatsApp
- **Conversation**:
  - Lead: "Quero ver na pratica"
- **Expected**: If demo is ready, route to demo; if not ready, explain calmly and continue with example or human help.
- **Prohibited**: fake demo claim, waitlist before positive post-demo signal unless lead explicitly asks to advance without demo.

### S203B - Demo Not Available

- **Channel**: Widget or WhatsApp
- **Conversation**:
  - Lead: "Quero ver uma demo"
  - Demo-ready state is false.
- **Expected**: Agent does not pretend demo exists. It explains calmly and offers diagnostic/product explanation or human help.
- **Prohibited**: fake demo link, waitlist before positive high-intent signal.

### S204 - Demo Seen, Positive Response

- **Channel**: Widget or WhatsApp
- **Conversation**:
  - Demo seen or discussed.
  - Lead: "Gostei, quero seguir"
- **Expected**: Agent offers waitlist with approved narrative.
- **Storage**: demo status positive and waitlist offered/joined state.

### S205 - Demo Seen, Negative Response

- **Channel**: Widget or WhatsApp
- **Conversation**:
  - Lead: "Nao era isso"
- **Expected**: Agent asks what did not fit: routine shown, agent type or moment of studio.
- **Prohibited**: waitlist, checkout, arguing with lead.

### S206 - Waitlist Accepted

- **Channel**: Widget or WhatsApp
- **Conversation**:
  - Agent offers waitlist.
  - Lead: "Pode colocar"
- **Expected**: Agent confirms and collects any missing required waitlist fields.
- **Storage**: If required fields are complete, `waitlistStatus=joined`, timestamp, source channel, safe summary, next action "chamar assim que possivel". If required fields are missing, `waitlistStatus=pending_details`.

### S207 - Waitlist Declined

- **Channel**: Widget or WhatsApp
- **Conversation**:
  - Agent offers waitlist.
  - Lead: "Nao agora"
- **Expected**: Agent respects, offers to answer doubts or keep context.
- **Storage**: `waitlistStatus=declined` or equivalent, no joined timestamp.

### S208 - Pending Details After Waitlist Acceptance

- **Channel**: Widget or WhatsApp
- **Conversation**:
  - Agent offers waitlist.
  - Lead: "Pode colocar"
  - Person name exists but studio name or city is missing.
- **Expected**: Agent asks only for missing fields and does not claim the studio is already fully on the list until fields are complete.
- **Storage**: `waitlistStatus=pending_details`.

### S209 - Details Completed After Pending

- **Channel**: Widget or WhatsApp
- **Conversation**:
  - Lead provides missing studio name/city/WhatsApp after pending details.
- **Expected**: Agent confirms the studio is on the list and uses the approved "chamamos assim que possivel" narrative without promising date.
- **Storage**: `waitlistStatus=joined`, `waitlistJoinedAt` set.

## Review Result Template

Use this table during R5. All rows below are mandatory for R5.

| Scenario | Channel | Pass/Fail | Issue Type | Notes | Fix Required |
| --- | --- | --- | --- | --- | --- |
| S001 | WhatsApp |  |  |  |  |
| S002 | WhatsApp |  |  |  |  |
| S003 | WhatsApp |  |  |  |  |
| S004 | WhatsApp |  |  |  |  |
| S005 | Widget |  |  |  |  |
| S006 | Widget |  |  |  |  |
| S007 | Widget |  |  |  |  |
| S008 | Widget |  |  |  |  |
| S009 | Widget |  |  |  |  |
| S101 | WhatsApp |  |  |  |  |
| S102 | WhatsApp |  |  |  |  |
| S103 | WhatsApp |  |  |  |  |
| S104 | Both |  |  |  |  |
| S105 | WhatsApp |  |  |  |  |
| S106 | WhatsApp |  |  |  |  |
| S107 | Both |  |  |  |  |
| S201 | Both |  |  |  |  |
| S202 | Both |  |  |  |  |
| S203 | Both |  |  |  |  |
| S203B | Both |  |  |  |  |
| S204 | Both |  |  |  |  |
| S205 | Both |  |  |  |  |
| S206 | Both |  |  |  |  |
| S207 | Both |  |  |  |  |
| S208 | Both |  |  |  |  |
| S209 | Both |  |  |  |  |
