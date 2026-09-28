# Product Follow-Up Delta Contract: Taliya Commercial Agent

**Status**: Binding delta for the next implementation pass.
**Scope**: Only gaps not already implemented or protected in the Taliya-owned commercial agent for the `/pilates` widget and Taliya-owned WhatsApp number.
**Non-goal**: Do not reopen approved openings, direct price, price-plus-pain, demo direct, WhatsApp student/app/password, diagnostic script, final diagnostic, waitlist basics, handoff, safety basics, Sales Inbox basics, delivery timing, or `/pilates` visual layout.

## Core Decision

This delta must improve missing product explanation and follow-up behavior without turning the runtime back into a deterministic chatbot.

The model remains the conversation brain:

- The LLM interprets the lead message, state, history, and compact diagnostic memory.
- The LLM chooses normalized intents, route, template ids, and grounded variables.
- Product knowledge supplies official facts.
- Templates supply controlled voice.
- Validators block unsafe, unsupported, ungrounded, or state-inconsistent output.
- Deterministic code may validate, render, persist, retrieve selective facts, and enforce operational boundaries only.

Forbidden implementation pattern:

```text
if text contains "planilha" -> send comparison template
if text contains "LGPD" -> send security template
if text contains "como funciona" -> send fixed answer
if post-diagnostic and text contains "preco" -> send fixed post-diagnostic price branch
```

Required implementation pattern:

```text
LLM receives compact state + selective product knowledge + protected behavior policy
LLM returns structured JSON with intent/template/variables/facts
runtime validates official facts, template permissions, state, and variables
renderer sends channel-safe short messages
memory/Sales Inbox persist the meaningful turn
```

## Protected Behavior That Must Not Change

The following paths are out of scope for behavior redesign. They may receive regression tests, but no new copy or routing should be introduced unless a regression proves a bug.

- `opening.cold_greeting`
- `opening.cold_greeting_named`
- `opening.widget_empty_diagnostic`
- `opening.general_interest`
- `opening.instagram_source`
- `opening.site_cta`
- `opening.diagnostic_cta`
- `product.price_direct`
- `product.price_complete_direct`
- `product.plan_fit_with_diagnostic`
- `product.demo_direct`
- `product.whatsapp_direct`
- all approved diagnostic questions
- final diagnostic staged delivery
- waitlist offer/join basics
- human handoff and pause/resume
- prompt-injection, sensitive-data, unsupported-media, and medical-advice safety basics
- Sales Inbox persistence already covered by existing contract
- widget/WhatsApp delivery timing and chunking already covered by existing delivery contract
- protected `/pilates` visual layout

## Missing Or Partial Coverage To Implement

### 1. Official Product Knowledge: How Taliya Works

Add an official product knowledge key: `how_it_works`.

It must explain, in natural day-to-day language for Pilates studio owners:

- Taliya helps the studio organize day-to-day routine.
- It brings together conversations, students, agenda, replacements, payments/collections, interested leads, and follow-ups.
- The team can see what needs action.
- When the studio WhatsApp Business is connected/configured, agents can support conversations with students and interested leads.
- The team can follow and take over when a human is needed.
- Taliya must not be reduced to a generic chatbot, generic automation, agenda-only app, or technical system explanation.

This key supports:

- "como funciona?"
- "me explica melhor"
- "o que a Taliya faz na pratica?"
- "como seria no meu studio?"
- post-diagnostic "como isso entra no meu caso?"

### 2. Official Product Knowledge: Routine Areas

Add `routine_areas`.

It must explain these areas simply:

- Atendimento: messages and common doubts do not get lost.
- Vendas/interessados: interested leads, trial classes, enrollment next steps, and follow-up.
- Agenda: classes, openings, absences, schedule movements, and fit-ins.
- Reposicoes: replacement requests and pending replacement organization.
- Cobrancas/financeiro: monthly payments, due dates, renewals, and pending payments.
- Acompanhamento dos alunos: students who disappear, miss classes, or need follow-up.
- Gestao/prioridades: what the team should solve first.

This key supports product explanation, objections, comparison, and post-diagnostic answers.

### 3. Official Product Knowledge: WhatsApp Scope

Add `whatsapp_scope`.

It must distinguish:

- This commercial conversation runs on Taliya's own widget and Taliya's own WhatsApp number.
- For the product agents to act on students' WhatsApp conversations, the studio needs WhatsApp Business connected/configured.
- The student does not need to download an app or create a password.
- The student talks through WhatsApp.
- Taliya helps register/organize the routine and notify the team when attention is needed.
- The studio team can follow and take over when needed.
- The agent must not promise to connect/configure the customer's WhatsApp automatically inside this commercial chat.

This key supports:

- "preciso ter WhatsApp Business?"
- "conecta meu WhatsApp?"
- "e no WhatsApp, como funciona?"
- "aluno precisa baixar app?"
- "e no meu numero ou no de voces?"

### 4. Official Product Knowledge: Integration Scope

Add `integration_scope`.

It must define safe boundaries:

- Do not promise Instagram integration.
- Do not promise integration with the lead's current system.
- Do not promise mass messaging.
- Do not promise checkout or payment link while checkout is unavailable.
- Do not promise automatic migration.
- If a specific integration is not officially known, answer the limit and offer human confirmation.

This key supports:

- "integra com Instagram?"
- "integra com Tecnofit?"
- "integra com meu sistema?"
- "tem disparo em massa?"
- "conecta tudo automaticamente?"

### 5. Official Product Knowledge: Comparison With Current Tools

Add `comparison_spreadsheet`.

It must state:

- Spreadsheet, notebook, and manual WhatsApp can work while the routine is small/simple.
- Problems usually appear when messages, replacements, interested leads, payments, and follow-ups become spread out.
- Taliya's practical difference is organizing the routine and helping the team act on what needs attention.
- Do not shame the current process.
- Do not claim Taliya replaces everything before understanding the case.

Add `comparison_management_system`.

It must state:

- If the current system solves part of the routine, acknowledge that.
- Taliya should be compared by how it organizes the studio routine and how AI agents support actions.
- Do not attack Tecnofit, Next Fit, or any competitor.
- Do not invent feature parity.
- Do not promise migration or integration without confirmation.

### 6. Official Product Knowledge: Security And Data

Add `security_and_data`.

It must state:

- The chat should not request sensitive data.
- Do not ask for CPF, payment data, medical data, or sensitive student information.
- Privacy, security, LGPD, certifications, encryption, or access-to-conversation claims require official facts.
- If a detail is not official, do not invent it; offer human confirmation.

### 7. Official Product Knowledge: Availability And Onboarding

Add or strengthen `availability_and_onboarding`.

It must state:

- Taliya is working with a small number of studios.
- There is no open checkout for immediate broad entry.
- Do not promise an exact date.
- Do not promise a guaranteed opening window.
- Waitlist is the current commercial path when there is real intent to start/contract.
- Setup/implementation details should be confirmed by the team when the lead wants to advance.
- Do not promise automatic WhatsApp, system, or data setup without validation.

### 8. Official Product Knowledge: Out Of Profile

Add `out_of_profile`.

It must state:

- Taliya is currently intended mainly for Pilates studios.
- If the person is a student, autonomous teacher, gym, clinic, non-Pilates business, or not-yet-open studio, qualify gently.
- Do not force studio diagnostic.
- Do not treat a student as a buyer.
- Do not promise fit for another niche.

## New Templates

Create only these new templates unless implementation evidence proves one is unnecessary or an existing template covers it better.

### `product.how_it_works_direct`

Purpose: product explanation for "como funciona?" and related questions. This is not an opening template.

Body:

```text
Funciona assim: a Taliya ajuda o studio a organizar o que acontece no dia a dia.

Ela junta conversas, alunos, agenda, reposicoes, cobrancas, interessados e acompanhamentos para a equipe enxergar melhor o que precisa de acao.

Quando o WhatsApp Business do studio esta conectado, os agentes podem apoiar conversas com alunos e interessados, sempre com a equipe podendo acompanhar e assumir quando precisar.

{contextual_next_step}
```

Required variable:

- `contextual_next_step`

Allowed `contextual_next_step` meanings:

No diagnostic done:

```text
Se fizer sentido para voce, estamos oferecendo um diagnostico gratuito para entender como isso encaixaria na rotina do seu studio. O que voce acha?
```

No diagnostic done, but with pain/context:

```text
Se fizer sentido para voce, estamos oferecendo um diagnostico gratuito para o seu studio. Assim podemos entender como a Taliya encaixaria na sua rotina e por onde comecar. O que voce acha?
```

Diagnostic in progress:

```text
Isso conversa diretamente com o diagnostico que estamos fazendo. Vou usar suas respostas para te devolver onde a Taliya entraria primeiro na rotina.
```

Diagnostic delivered:

```text
Pelo diagnostico que fizemos, isso entraria primeiro em {recommended_area}. Posso te mandar uma demonstracao para voce ver esse funcionamento na pratica.
```

Demo already offered:

```text
Chegou a olhar a demonstracao? Ela ajuda a visualizar esse funcionamento na pratica.
```

Waitlist joined:

```text
Seu studio continua registrado na lista de espera. Enquanto isso, posso te explicar qualquer parte do funcionamento com mais calma.
```

Validation:

- `recommended_area` must be grounded in saved diagnostic output.
- The template must not be selected as a cold opening.
- The template must not use "CRM" for a lay lead.
- The template must not offer waitlist unless the structured decision separately validates clear contract intent.

### `product.comparison_current_tool`

Purpose: comparison with spreadsheet, notebook, manual WhatsApp, current system, or competitor.

Body:

```text
Se o que voces usam hoje resolve parte da rotina, faz sentido manter o que funciona.

A diferenca da Taliya e ajudar a organizar o que costuma ficar espalhado: conversas, agenda, reposicoes, cobrancas, interessados e acompanhamento dos alunos.

Para comparar sem chute, vale olhar onde a rotina do seu studio mais perde tempo hoje.
```

Optional variable:

- `current_tool_context`, only when explicitly mentioned by the lead.

Validation:

- Do not mention a competitor unless the lead mentioned it.
- Do not promise migration.
- Do not promise integration.
- Do not attack the current tool.
- Offer diagnostic only when the LLM selects that next step and the state allows it.

### `product.integration_scope_direct`

Purpose: integration, WhatsApp setup, Instagram, current system, and mass-message scope questions.

Body:

```text
Para os agentes atuarem no WhatsApp dos alunos, o studio precisa ter WhatsApp Business conectado/configurado.

Sobre integracoes especificas, eu prefiro nao prometer sem confirmar com a equipe.

Posso te explicar o caminho geral ou deixar esse ponto para alguem validar com voce.
```

Optional variable:

- `integration_topic`, grounded in the lead message.

Validation:

- Do not promise a specific integration.
- Do not promise automatic WhatsApp setup.
- Do not promise mass messaging.
- Do not promise checkout or payment link.

### `product.security_data_direct`

Purpose: security, privacy, LGPD, data, and AI-error concern questions.

Body:

```text
E um ponto importante.

Por aqui, eu nao preciso que voce mande dados sensiveis do studio ou dos alunos.

Sobre seguranca, privacidade ou LGPD, eu prefiro seguir so informacoes oficiais. Se faltar algum detalhe, deixo para a equipe confirmar com precisao.
```

Validation:

- Do not invent LGPD, certifications, encryption claims, audits, or guarantees.
- Do not request sensitive data.
- Offer human confirmation if official facts are missing.

### `product.out_of_profile_redirect`

Purpose: students, autonomous teachers, gyms, clinics, non-Pilates businesses, and not-yet-open studios.

Body:

```text
Hoje a Taliya e pensada principalmente para studios de Pilates.

Se voce e aluno, professor autonomo ou esta falando de outro tipo de negocio, me conta rapidinho o contexto para eu nao te orientar errado.
```

Validation:

- Do not offer diagnostic automatically.
- Do not treat a student as a buyer.
- Do not promise fit for another niche.

## New Or Strengthened Structured Intents

The LLM may choose these intents. Runtime must validate them, not infer them through commercial regex.

- `product_how_it_works`
- `comparison_current_tool`
- `integration_scope_question`
- `trust_security_question`
- `out_of_profile`
- `conversation_resume`
- `general_objection`
- `diagnostic_refusal`

## Post-Diagnostic Consultative Mode

The conversation state already includes `diagnostic_delivered` and `post_diagnostic_questions`. This delta strengthens what must happen there.

After diagnostic delivery:

- Do not restart the diagnostic.
- Do not treat the lead as a new conversation.
- Do not ask again for facts already answered.
- Use the saved diagnostic as the main commercial context.
- Answer direct questions first.
- Use demo as the natural next step when useful.
- Offer waitlist only with clear intent to start/contract/advance.
- Preserve waitlist status without repeating status on every product answer.
- Do not invent dates, checkout, setup promises, links, or availability.

Add compact LLM payload:

```text
post_diagnostic_context:
- pain_context_human
- likely_cause
- first_recommended_step
- recommended_area
- indicated_agents
- recommended_plan_or_range
- demo_status
- waitlist_status
- unknowns
```

Rules:

- Include only after diagnostic has been delivered.
- Populate only from saved diagnostic/waitlist/demo state.
- Do not invent missing fields.
- Use this context to continue the sales conversation, not to regenerate the diagnostic.

## General Objections Policy

Do not create separate deterministic branches for each objection.

The LLM should handle:

- "vou pensar"
- "nao tenho tempo agora"
- "preciso falar com minha socia"
- "minha equipe nao vai usar"
- "parece complicado"
- "nao quero IA falando com aluno"
- "nao sei se faz sentido"

Expected behavior:

- acknowledge without pressure;
- answer the concern in simple studio-owner language;
- use saved diagnostic context if available;
- offer demo when it helps the decision;
- offer diagnostic only when useful and allowed;
- respect diagnostic refusal;
- hand off when the lead asks for a person.

Create `product.general_objection_response` only if evaluation proves LLM+policy is inconsistent.

## Diagnostic Refusal Policy

If the lead refuses diagnostic or asks for a direct answer only:

- respect it;
- answer the direct question;
- do not offer diagnostic again in the same turn;
- continue helping with product questions;
- offer diagnostic again only if the lead later asks for a recommendation or shows openness to context.

Examples:

- "nao quero diagnostico"
- "so me fala o preco"
- "sem perguntas agora"
- "responde direto"

## Selective Product Knowledge Retrieval

Do not increase every turn's payload. Retrieve only relevant keys:

For "como funciona":

- `how_it_works`
- `routine_areas`
- `whatsapp_scope`

For WhatsApp/integration:

- `whatsapp_scope`
- `integration_scope`
- `unsupported_claims`

For comparison:

- `comparison_spreadsheet`
- `comparison_management_system`
- `routine_areas`

For security/data:

- `security_and_data`
- `privacy_or_data_notes`

For availability/onboarding:

- `availability_and_onboarding`
- `availability`
- `waitlist_status`
- `checkout_status`

For post-diagnostic follow-up:

- saved diagnostic compact context;
- `plans` and `prices` only when price/plan is relevant;
- `demo_status` and `links` only when demo is relevant;
- `waitlist_status` and `checkout_status` only when availability/next-step is relevant;
- `how_it_works` and `routine_areas` only when product explanation is relevant.

## "CRM" Word Control

Customer-facing output must not use "CRM" as the main explanation or persuasion device for lay leads.

Allowed:

- the lead directly asks "e CRM?", "tem CRM?", or similar;
- the selected template is `product.crm_direct`;
- internal diagnostic/data fields, Sales Inbox metadata, and docs.

Blocked:

- openings;
- price objection value explanations;
- "como funciona" explanation for lay leads;
- comparison with current tools unless the lead used "CRM";
- generic persuasion.

## Owner-Language Control

Customer-facing output for lay Pilates studio owners must explain the product in day-to-day studio language, not technical SaaS language.

Avoid these terms unless the lead used them first or the selected official answer requires a direct clarification:

- pipeline;
- lead scoring;
- automacao;
- integracao, except when the lead asks about a specific integration;
- status, except when describing what the team can see in simple terms;
- fluxo operacional;
- arquitetura;
- stack;
- webhook, API, Meta, Dualhook, HMAC, SDK, or runtime.

Preferred language:

- conversas;
- alunos;
- interessados;
- agenda;
- reposicoes;
- cobrancas;
- acompanhamento;
- rotina;
- o que precisa de acao;
- equipe acompanha e assume quando precisar.

Validation:

- Owner-language violations fail product explanation, comparison, price-objection, diagnostic-refusal, and post-diagnostic follow-up evals.
- Internal fields, logs, Sales Inbox metadata, and engineering docs may still use technical terms.

## LLM Evidence And Cost Budget

The new product-followup routes must preserve the LLM-first architecture while keeping cost controlled.

LLM evidence required:

- `product_how_it_works`;
- `comparison_current_tool`;
- `integration_scope_question`;
- `trust_security_question`;
- `general_objection`;
- `conversation_resume`;
- post-diagnostic product, price, demo, plan, and objection follow-up;
- any mixed-intent or ambiguous commercial message.

For those routes, reports must include model usage, selected intent, selected template id, product knowledge keys used, and whether any deterministic operational gate ran before the LLM.

Allowed zero-cost exceptions remain limited to operational/safety/cold-empty cases already defined by the LLM-first rule, such as widget empty opening, pure cold greeting, idempotency, active human handoff, unsupported media, sensitive data, and prompt-injection handling.

Cost and latency budget:

- Use the latest approved protected-route eval report as the baseline before this delta.
- Protected routes must remain within the configured cost and latency bands.
- A protected route average cost or latency increase above 10% must be treated as a regression unless the transcript quality improvement is explicitly accepted in `product-owner-transcript-review.md`.
- New routes must use selective product knowledge retrieval and stay inside configured model-call and spend caps.
- Low or zero cost on a commercial route is suspicious unless it is one of the allowed zero-cost exceptions above.

## Required New Evals

### How It Works

Scenarios:

- "como funciona?"
- "me explica melhor"
- "como seria no meu studio?"
- "como funciona no WhatsApp?"
- after diagnostic delivered: "como funciona no meu caso?"
- after demo offered: "como funciona?"
- after waitlist joined: "como funciona?"

Pass criteria:

- answer is product explanation, not an opening;
- no "CRM" for lay lead;
- explains routine plainly;
- mentions WhatsApp Business when WhatsApp is relevant;
- CTA/next step matches state;
- post-diagnostic path does not restart diagnostic.

### Post-Diagnostic Consultative Follow-Up

Scenarios:

- diagnostic delivered -> "qual plano mesmo?"
- diagnostic delivered -> "quanto fica?"
- diagnostic delivered -> "como funciona no meu caso?"
- diagnostic delivered -> "me manda demo"
- diagnostic delivered -> "achei caro"
- diagnostic delivered -> "vou pensar"
- diagnostic delivered -> "quero comecar"
- diagnostic delivered -> "pode continuar"

Pass criteria:

- uses saved diagnostic context;
- does not repeat diagnostic;
- does not ask already answered questions;
- answers direct question first;
- uses demo at the right time;
- waitlist only with clear intent;
- no invented price, date, checkout, setup promise, or link.

### Comparison

Scenarios:

- "uso planilha hoje"
- "faco tudo pelo WhatsApp"
- "uso caderno"
- "ja tenho sistema"
- "uso Tecnofit"
- "uso Next Fit"
- "isso e so uma agenda?"

Pass criteria:

- does not attack current tool;
- does not promise migration/integration;
- explains practical difference;
- offers diagnostic only when useful;
- no "CRM" for lay lead unless the lead used it.

### WhatsApp And Integration Scope

Scenarios:

- "preciso ter WhatsApp Business?"
- "voces conectam meu WhatsApp?"
- "e no meu numero ou no de voces?"
- "integra com Instagram?"
- "tem disparo em massa?"
- "integra com meu sistema?"
- "aluno precisa baixar app?"

Pass criteria:

- distinguishes Taliya commercial WhatsApp from studio WhatsApp Business product use;
- explains no app/password for student when relevant;
- does not promise integration or setup;
- offers human confirmation when needed.

### Security And Data

Scenarios:

- "e seguro?"
- "tem LGPD?"
- "voces leem as conversas?"
- "posso mandar dados dos alunos?"
- "a IA pode responder errado?"

Pass criteria:

- no invented certification or guarantee;
- no sensitive-data request;
- uses official product knowledge;
- offers human confirmation when official facts are missing.

### Out Of Profile

Scenarios:

- "sou aluno"
- "sou professor autonomo"
- "tenho uma academia"
- "tenho uma clinica"
- "ainda vou abrir meu studio"

Pass criteria:

- does not force diagnostic;
- qualifies gently;
- does not promise fit;
- does not treat student as buyer.

### Diagnostic Refusal

Scenarios:

- "nao quero diagnostico"
- "so me fala o preco"
- "sem perguntas agora"
- "responde direto"

Pass criteria:

- respects refusal;
- answers the question;
- does not immediately offer diagnostic again;
- remains commercially helpful.

## Regression Evals Required

Before approval, prove that protected behavior did not regress:

- approved openings unchanged;
- openings do not use "CRM";
- direct price still answers official prices;
- price plus pain still answers price first and offers diagnostic naturally;
- diagnostic script unchanged;
- final diagnostic unchanged;
- waitlist timing unchanged;
- handoff unchanged;
- safety unchanged;
- Sales Inbox still saves meaningful turns.

## Acceptance Criteria

The delta is complete only when:

- All new product knowledge keys exist and are retrieved selectively.
- New templates exist and are validated.
- LLM chooses new intents/templates through structured output.
- No commercial understanding is moved into regex/state-machine shortcuts.
- Post-diagnostic turns use saved diagnostic memory and do not restart the diagnostic.
- "Como funciona" works before, during, and after diagnostic without being treated as an opening.
- Price-objection and lay product explanation do not use "CRM".
- Customer-facing product explanation, comparison, objection, and post-diagnostic follow-up avoid technical SaaS language unless the lead used it first.
- New commercial product-followup routes include real LLM evidence, except for explicitly allowed operational zero-cost exceptions.
- Integration and WhatsApp scope are clear without overpromising.
- Security/data answers are conservative and official-fact based.
- Diagnostic refusal is respected.
- New routes save useful facts/intents/state for Sales Inbox.
- Existing protected routes pass regression.
- Protected-route cost and latency remain inside configured bands and do not regress by more than 10% versus the latest approved baseline unless explicitly accepted in product-owner review.
- New routes use selective knowledge and stay inside configured cost caps.
- Reports include transcripts, costs, and a product-owner-readable review.
