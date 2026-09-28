# Conversation Route Coverage Matrix: Taliya Commercial Agent

**Status**: Binding planning artifact for spec 010.
**Scope**: Taliya-owned commercial agent only, for the `/pilates` widget and Taliya's own WhatsApp number.
**Out of scope**: `/pilates` visual redesign, customer/studio WhatsApp connections, multi-tenant behavior, and the seven future client/studio agents.

## Purpose

This matrix prevents duplicated behavior while expanding conversation coverage.

The agent already has approved templates, product knowledge, policy, guardrails, persistence, and evals. New coverage must reuse those assets first. New templates, product facts, or structured intents are allowed only when a route is genuinely missing or the current behavior is too weak to be reliable.

The product explanation and follow-up delta is now binding through [product-followup-delta-contract.md](./product-followup-delta-contract.md). Rows marked `do_not_touch` remain protected. Rows marked `partial` or `missing` in the product explanation, post-diagnostic, comparison, integration/scope, security/data, out-of-profile, diagnostic-refusal, and conversation-resume areas are the only routes in scope for the next implementation pass.

## Decision Rules

Use this order before changing behavior:

1. If an existing template and policy already cover the route, do not create anything new.
2. If an existing template covers the route but the wording is weak, adjust the existing template.
3. If the missing piece is an official fact, add it to product knowledge instead of hardcoding it in a prompt or template.
4. If the conversation decision is new, add a structured intent/category for the LLM to choose.
5. If a recurring route needs controlled voice and no existing template fits, create a new template.
6. Never add regex/state-machine shortcuts for commercial understanding such as price, demo, product explanation, comparison, plan fit, pain, diagnostic, waitlist, or mixed-intent messages.

## Status Legend

- `do_not_touch`: approved path; keep behavior stable unless a regression proves a bug.
- `exists`: implemented and adequately covered.
- `partial`: implemented partly, but needs policy, product knowledge, template wording, guardrail, or eval coverage.
- `missing`: not sufficiently represented in policy/product knowledge/templates/evals.
- `watch`: keep under regression because related changes could break it.

## Protected Paths

These paths are approved enough that upcoming work must not redesign or replace them:

| Path | Status | Existing assets | Protection rule |
|------|--------|-----------------|-----------------|
| Cold greeting only | `do_not_touch` | `opening.cold_greeting`, `opening.cold_greeting_named`, cold greeting policy, final behavior matrix | Do not offer diagnostic, waitlist, name capture, phone capture, or product pitch on pure "oi/bom dia". |
| Widget empty opening | `do_not_touch` | `opening.widget_empty_diagnostic`, widget opening policy, widget evals | Preserve the approved soft diagnostic offer and do not ask the first diagnostic question until accepted. |
| Price direct | `do_not_touch` | `product.price_direct`, product knowledge prices, price evals | Always answer official prices directly before steering. |
| Price plus pain | `do_not_touch` | `product.price_direct`, `diagnostic.price_hook_with_context`, mixed-price evals | Answer price first, acknowledge the pain, then offer diagnostic. |
| Price objection | `do_not_touch` | `product.price_objection_value`, behavior policy 7b, real OpenAI stage2 price-objection evals | Keep LLM-detected `price_objection`; do not replace with phrase-by-phrase matching. |
| Demo direct | `do_not_touch` | `product.demo_direct`, official demo link, demo evals | Widget may use CTA/button; WhatsApp must use full official link. Do not trigger waitlist from curiosity alone. |
| WhatsApp student flow | `do_not_touch` | `product.whatsapp_direct`, WhatsApp product question evals | Preserve "student does not need app/password" answer and official demo link. |
| Diagnostic script | `do_not_touch` | diagnostic ledger, diagnostic templates, diagnostic contract, correction evals | Do not change mandatory diagnostic questions/order unless product owner explicitly reopens the diagnostic script. |
| Final diagnostic delivery | `do_not_touch` | staged diagnostic templates, final diagnostic policy, real OpenAI correction evals | Keep staged order: context, base organization, operational step, agents, plan, demo bridge. |
| Waitlist | `do_not_touch` | `waitlist.*`, waitlist policy, waitlist evals | Waitlist requires real contract intent. Do not invent checkout, dates, discounts, or payment links. |
| Human handoff | `do_not_touch` | `handoff.acknowledge`, human pause/resume tools, handoff evals | Human active means no automated AI reply until explicit resume. |
| Prompt injection | `do_not_touch` | `safety.prompt_injection`, input/output guardrails, safety evals | Refuse briefly and never reveal internal rules. |
| Sensitive data | `do_not_touch` | `safety.sensitive_data`, sensitive-data guardrails/evals | Do not repeat CPF/payment/sensitive data and do not use it for signup. |
| Unsupported media | `do_not_touch` | `fallback.unsupported_media`, channel adapter contract, unsupported media evals | Ask for short text summary or offer human path; do not start sales flow from media alone. |
| Sales Inbox persistence | `do_not_touch` | memory store, Sales Inbox contract, Sales Inbox evals | Every meaningful turn must remain fully saved. |
| `/pilates` visual layout | `do_not_touch` | AGENTS protected layout rule, baseline docs | No redesign, reorder, restyle, or visual composition changes. |

## Coverage Matrix

| Route / lead direction | Status | Existing assets to reuse | Gap | Required action | Eval coverage needed |
|------------------------|--------|--------------------------|-----|-----------------|----------------------|
| Pure greeting: "oi", "bom dia", "tudo bem" | `do_not_touch` | `opening.cold_greeting`, `opening.cold_greeting_named`, `is_cold_greeting_only`, final/real OpenAI evals | None for current scope | Regression only | Existing final behavior + low-budget validation |
| Widget opens without typed message | `do_not_touch` | `opening.widget_empty_diagnostic`, widget pending context handling | None for current scope | Regression only | Existing widget-empty + pending acceptance evals |
| Widget diagnostic offer accepted with "sim/pode/quero" | `watch` | contextual widget shortcut, diagnostic ledger, `diagnostic.ask_active_students` | Must keep LLM/contextual interpretation and avoid brittle phrase handling | Regression only unless new failures appear | Existing stage2 widget acceptance eval |
| Site CTA / "faz sentido para meu studio" | `exists` | `opening.site_cta`, site CTA policy | Copy is approved enough; only watch for product-explanation overlap | Do not duplicate; reuse site CTA template | Existing site CTA eval |
| Instagram/Facebook/source opening | `exists` | `opening.instagram_source`, behavior policy 5a/5b | Current behavior now offers diagnostic softly; keep short | Do not create a new social template unless copy changes are explicitly requested | Existing stage2 Instagram eval |
| General "quero saber mais" | `partial` | `opening.general_interest`, `product.overview_short`, `opening.instagram_source` | Needs clearer rule for when to explain product vs ask broad help vs offer diagnostic | Add policy and product knowledge; likely reuse existing templates | New "quero saber mais" variants across widget/WhatsApp |
| "O que é a Taliya?" | `partial` | `product.overview_short`, `opening.general_interest` | Product knowledge lacks official `overview`; answer may be too thin | Add `overview` product knowledge and improve existing overview template if needed | New product explanation eval |
| "Como funciona?" / "me explica melhor" | `partial` | `product.overview_short`, `product.agents_direct`, `opening.general_interest` | Needs practical explanation of workflow without leading with CRM | Add `how_it_works` and `routine_areas` product knowledge; add LLM policy | New how-it-works eval |
| "É CRM ou IA?" | `partial` | `product.crm_direct`, `product.overview_short` | `product.crm_direct` starts with CRM and may be too technical | Adjust existing template or add variables; do not create parallel route unless needed | New CRM/IA explanation eval |
| "Como ajuda meu studio?" | `partial` | `diagnostic.offer_soft`, `product.overview_short` | Needs bridge from product explanation to diagnostic without forcing | Add policy: answer first, then offer diagnostic if useful | New usefulness/product-fit eval |
| Agenda/reposições product question | `partial` | diagnostic pain policy, `diagnostic.offer_soft`, final diagnostic routines | Covered as pain/diagnostic, not as product explanation | Add product knowledge for routine areas; reuse diagnostic offer | New routine-area eval |
| Cobranças/financeiro product question | `partial` | `product.agents_direct`, diagnostic final agents | Product knowledge has plan agent names but weak customer-facing explanation | Add routine-area knowledge; reuse product/diagnostic templates | New finance routine eval |
| Atendimento/vendas product question | `partial` | `product.agents_direct`, `diagnostic.offer_soft`, price+pain handling | Covered through pain and diagnostic, but explanation could be better | Add routine-area knowledge; no new runtime branch | New atendimento/vendas eval |
| WhatsApp student/app/password | `do_not_touch` | `product.whatsapp_direct` | None for approved path | Regression only | Existing WhatsApp product eval |
| WhatsApp of Taliya commercial agent | `partial` | WhatsApp adapter/runtime docs, current channel behavior | Need clear product knowledge distinction: Taliya's own WhatsApp vs future studio WhatsApps | Add `whatsapp_scope`; do not promise customer WhatsApp setup | New WhatsApp scope eval |
| "Conecta meu WhatsApp?" | `partial` | `unsupported_claims`, product plan `whatsapp_availability`, fallback missing knowledge | Existing product knowledge can imply studio WhatsApp connection, conflicting with current scope | Add explicit integration scope guardrail and official wording | New customer WhatsApp connection eval |
| "Integra com Instagram?" | `missing` | `unsupported_claims`, `fallback.product_knowledge_missing` | No specific official integration-scope response | Add `integration_scope` product knowledge and eval | New integration eval |
| "Tem disparo em massa?" | `missing` | `unsupported_claims`, safety/product fallback | No specific guardrail/copy | Add unsupported-claim policy; answer only official facts | New mass messaging eval |
| "Integra com meu sistema atual?" | `missing` | `fallback.product_knowledge_missing`, `unsupported_claims` | No official answer path | Add `integration_scope` product knowledge | New integration-current-system eval |
| Uses spreadsheet/caderno/WhatsApp manual | `partial` | diagnostic ledger current process, facts extraction, price-objection value context | Works as diagnostic fact, not as product comparison answer | Add comparison product knowledge; probably new or adjusted template | New spreadsheet comparison eval |
| Uses CRM/generic system | `partial` | `product.crm_direct`, current_process fact extraction | Needs non-technical comparison and no fake replacement promise | Add `comparison_management_system` knowledge and policy | New CRM comparison eval |
| Uses Tecnofit/Next Fit/competitor | `missing` | current_process fact extraction catches `tecnofit`; no policy/template | Need non-attack, no feature invention, no "replace now" claim | Add competitor-neutral policy and product knowledge | New competitor comparison eval |
| Price direct | `do_not_touch` | `product.price_direct` | None | Regression only | Existing price evals |
| Complete plan price | `do_not_touch` | `product.price_complete_direct` | None | Regression only | Existing post-waitlist complete-price eval |
| Plan fit thin context | `do_not_touch` | `product.plan_fit_with_diagnostic` | None for current approved copy | Regression only | Existing plan-fit evals |
| Plan fit with rich context | `watch` | diagnostic ledger, `diagnostic.deliver_plan_recommendation` | Must not guess beyond facts; may need richer evals | Add eval only if coverage is thin | Existing diagnostic complete + possible new rich plan-fit eval |
| Price objection | `do_not_touch` | `product.price_objection_value` | None for current scope | Regression only | Existing stage2 price-objection eval |
| "Não tenho tempo agora" | `missing` | `fallback.unmapped_adaptive` could respond, but too generic | Needs low-pressure objection handling | Add `general_objection` intent/policy; maybe new template | New general objection eval |
| "Vou pensar" | `missing` | None specific | Needs de-escalation and optional useful next step | Add general objection policy/template | New objection eval |
| "Preciso falar com sócio/equipe" | `missing` | None specific | Needs natural response, no pressure, maybe offer demo/diagnostic summary | Add general objection policy/template | New stakeholder objection eval |
| "Minha equipe não vai usar" | `missing` | None specific | Needs practical, non-defensive answer | Add general objection policy and possibly product knowledge | New team adoption objection eval |
| "Parece complicado" | `missing` | None specific | Needs simple reassurance without fake onboarding promise | Add objection + implementation scope knowledge | New complexity objection eval |
| "Não quero IA falando com aluno" | `partial` | `product.whatsapp_direct`, behavior policy, guardrails | Need distinguish control/handoff/limits without inventing product guarantees | Add trust/product policy and official facts | New AI concern eval |
| "Você é robô?" / irritated lead | `partial` | final irritated eval, handoff option | Existing eval is broad; behavior not explicitly specified | Add policy: be direct, short, offer human if needed | New irritated/robot eval |
| "Só me manda o preço, sem diagnóstico" | `missing` | price direct, direct-question policy | Need respect refusal and not force diagnostic hook | Add policy/eval for diagnostic refusal on direct price | New no-diagnostic-price eval |
| "Não quero diagnóstico" | `partial` | `refuse_diagnostic` contextual shortcut, final irritated route | Needs broader coverage and no repeated diagnostic | Add eval; reuse existing refusal path if possible | New diagnostic refusal eval |
| "Quero contratar" before diagnostic | `do_not_touch` | waitlist policy, `waitlist.offer_after_contract_intent` | None for current path | Regression only | Existing buy intent eval |
| "Quero contratar" after diagnostic | `watch` | diagnostic delivered state, waitlist policy | Covered by state contract; needs real-world transcript coverage | Add targeted eval if missing | New post-diagnostic contract eval |
| "Me manda link de pagamento/checkout" | `do_not_touch` | checkout unavailable knowledge, output guardrails, waitlist | None | Regression only | Existing checkout eval |
| "Quando posso começar?" | `partial` | availability + waitlist_status product knowledge | Needs natural direct answer without fake date | Add `availability_and_onboarding` knowledge/policy | New availability eval |
| "Vocês configuram?" / onboarding | `missing` | None specific | No official onboarding wording | Add official knowledge or route to human if unknown | New onboarding eval |
| "É seguro?" | `partial` | `privacy_or_data_notes`, privacy link, sensitive-data guardrail | Current knowledge is too thin for a useful trust answer | Add `security_and_data` official facts; no unsupported certifications | New security eval |
| "Tem LGPD?" | `missing` | privacy link only | Need official wording or human fallback | Add knowledge if true/available; otherwise fallback to human confirmation | New LGPD eval |
| "Vocês leem as conversas?" | `missing` | privacy notes too generic | Needs official policy; avoid inventing data handling | Add security/data knowledge or block with human confirmation | New data access eval |
| "A IA pode responder errado?" | `partial` | behavior policy says do not invent; some runtime copy exists | Needs official customer-facing explanation | Add trust policy; no new flow if existing template can be reused | New AI-error eval |
| Lead is a Pilates student | `missing` | `safety.out_of_scope` | Need not qualify as studio lead; redirect politely | Add `out_of_profile` policy/template or adjust safety template | New student eval |
| Lead is teacher/autonomous instructor | `missing` | `safety.out_of_scope` | Needs qualify context without forcing studio diagnostic | Add out-of-profile knowledge/policy | New teacher eval |
| Lead is gym/clinic/non-Pilates | `missing` | `safety.out_of_scope` | Needs scope explanation; avoid fake fit | Add out-of-profile policy | New non-Pilates business eval |
| Studio not opened yet | `missing` | none specific | Needs qualify gently; diagnostic may be different or not appropriate | Add out-of-profile/early-stage policy | New not-opened eval |
| Returning "oi" with existing state | `partial` | compact previous state, conversation state contract | Need make sure it does not reset incorrectly | Add resume policy/eval | New returning greeting eval |
| "Pode continuar" | `missing` | previous state memory exists | Needs resume from diagnostic/waitlist/demo state | Add `conversation_resume` intent and eval | New continue eval |
| "Qual era mesmo o plano?" | `missing` | previous diagnostic, product knowledge | Needs use memory/recommendation if available | Add resume/product follow-up eval | New plan recall eval |
| "Alguma novidade da lista?" | `partial` | waitlist status preserved, post-waitlist eval | Current post-waitlist eval is price-specific | Add waitlist status follow-up eval | New waitlist follow-up eval |
| Message broken into multiple turns | `partial` | memory state, diagnostic ledger, lead facts | Existing diagnostics cover some multi-turn; not broad enough | Add long/broken-message eval | New broken-message eval |
| Audio/image/file | `do_not_touch` | unsupported media fallback | None for current support boundary | Regression only | Existing unsupported media eval |
| Prompt injection | `do_not_touch` | safety prompt injection | None | Regression only | Existing safety eval |
| Sensitive data | `do_not_touch` | safety sensitive data | None | Regression only | Existing sensitive data eval |
| Human request | `do_not_touch` | handoff agent/tools | None | Regression only | Existing handoff eval |
| Sales Inbox completeness | `do_not_touch` | memory store, sales-inbox contract/evals | New routes must continue saving facts/intents/usage | Extend eval only for new routes | Existing Sales Inbox eval + new route rows |

## Product Knowledge Additions Needed

Do not hardcode these in templates or runtime. Add them as official product knowledge keys and retrieve them only when relevant.

| Key | Required content | Used by |
|-----|------------------|---------|
| `overview` | Short plain-language definition of Taliya without leading with CRM. | Product explanation, social/site openings |
| `how_it_works` | Practical explanation of how Taliya helps the studio routine day to day. | "Como funciona?", "me explica melhor" |
| `routine_areas` | Agenda, reposições, cobranças, gestão, atendimento, acompanhamento; what each means in simple language. | Product explanation, diagnostic bridge |
| `comparison_spreadsheet` | How to compare Taliya with spreadsheet/caderno/WhatsApp manual without shaming current process. | Spreadsheet/manual comparisons |
| `comparison_management_system` | Neutral comparison with CRM/management systems/competitors; no attacks, no invented feature parity. | Tecnofit/Next Fit/current system |
| `security_and_data` | Official facts about data/privacy/security that can be safely stated. | Security/LGPD/data questions |
| `whatsapp_scope` | Distinguish Taliya's own WhatsApp commercial agent from future/customer studio WhatsApp capabilities. | WhatsApp/integration questions |
| `integration_scope` | What integrations cannot be promised now, including Instagram, existing systems, mass messaging, and customer WhatsApp setup. | Integration questions |
| `availability_and_onboarding` | Availability, waitlist, setup/onboarding limits, and when human confirmation is needed. | "When can I start?", "do you configure?" |
| `out_of_profile` | Current ICP/scope and how to respond to students, teachers, clinics, gyms, or not-yet-open studios. | Out-of-profile leads |

## Structured Intents To Allow

The LLM may use these normalized intents when appropriate. Runtime should validate and retrieve facts; it should not decide these by commercial regex.

| Intent | Meaning | Expected behavior |
|--------|---------|-------------------|
| `product_explanation` | Lead asks what Taliya is or how it works. | Explain simply, connect to routine, offer diagnostic only if useful. |
| `comparison_current_tool` | Lead compares Taliya with spreadsheet, WhatsApp manual, CRM, Tecnofit, Next Fit, or current system. | Compare neutrally, avoid attacking, avoid fake feature parity, offer diagnostic if relevant. |
| `general_objection` | Lead hesitates for time, team, complexity, partner approval, or similar. | Acknowledge, reduce pressure, answer concern, ask at most one useful next step. |
| `trust_security_question` | Lead asks about safety, data, LGPD, privacy, or AI mistakes. | Use only official product knowledge or offer human confirmation. |
| `integration_scope_question` | Lead asks about WhatsApp connection, Instagram, mass messages, or external systems. | Answer current scope and avoid unsupported promises. |
| `out_of_profile` | Lead may not be a Pilates studio decision-maker. | Qualify politely or redirect; do not force diagnostic. |
| `conversation_resume` | Lead asks to continue or recall prior recommendation/state. | Use memory and previous state; do not restart as new lead. |
| `implementation_availability_question` | Lead asks when/how they can start or how setup works. | Use availability/onboarding knowledge; waitlist only with real contract intent. |

## Template Reuse Plan

| Existing template | Reuse / adjustment rule |
|-------------------|-------------------------|
| `opening.general_interest` | Reuse for broad "quero saber mais"; adjust only if product explanation remains too thin after knowledge additions. |
| `opening.instagram_source` | Reuse for Instagram/Facebook/source openings; do not create social variants now. |
| `opening.site_cta` | Reuse for landing CTA handoff; do not start diagnostic question immediately. |
| `product.overview_short` | Primary candidate for "what is/how works"; may need stronger wording and product knowledge key alignment. |
| `product.crm_direct` | Adjust or constrain; avoid leading with CRM for lay leads. |
| `product.agents_direct` | Reuse for "what agents exist/do"; do not implement seven client agents now. |
| `product.whatsapp_direct` | Reuse only for student/WhatsApp product explanation, not for promising customer WhatsApp connection. |
| `product.price_objection_value` | Keep as approved price-objection template. |
| `fallback.product_knowledge_missing` | Reuse when official fact is missing or needs human confirmation. |
| `safety.out_of_scope` | Candidate for out-of-profile adjustment; do not overuse for qualified but adjacent leads. |
| `waitlist.*` | Reuse only after real contract intent. |
| `handoff.acknowledge` | Reuse for human request; no new handoff copy needed. |

## Required New Templates For Product-Followup Delta

These templates are required by [product-followup-delta-contract.md](./product-followup-delta-contract.md) unless implementation evidence proves an existing approved template fully covers the route without weakening quality. They remain voice/rendering blocks; the LLM chooses them through structured output.

| Template | Reason to create | Required safeguards |
|----------|------------------|---------------------|
| `product.how_it_works_direct` | "Como funciona?" is a product question that can occur before, during, or after diagnostic and needs state-aware controlled voice. | Not an opening; no lay-lead "CRM"; contextual next step must match state. |
| `product.comparison_current_tool` | Recurring comparison with spreadsheet/current system needs controlled non-attacking copy. | No competitor attack, migration promise, or integration promise. |
| `product.security_data_direct` | Security/LGPD/data questions need conservative answer grounded in official facts. | No invented LGPD, certification, encryption, audit, or privacy guarantees. |
| `product.integration_scope_direct` | Integration and WhatsApp scope need precise non-promise wording. | No automatic WhatsApp setup, Instagram/current-system integration, mass messaging, checkout, or migration promises. |
| `product.out_of_profile_redirect` | Student/teacher/non-studio leads need softer redirect than generic out-of-scope. | Qualify gently; do not force diagnostic; do not treat students as buyers. |

Do not create `product.general_objection_response` or `product.resume_context` in the first pass. General objections and resume should be handled through LLM+policy+memory first. Create templates for them only if eval evidence proves inconsistent quality.

## Evals To Add Later

These are not part of stage 1/2 implementation, but this matrix defines the required coverage.

- Product explanation: "como funciona?", "o que é a Taliya?", "é CRM ou IA?", "como ajuda meu studio?"
- Comparison: "uso planilha", "uso Tecnofit", "uso Next Fit", "já tenho sistema", "uso WhatsApp Business mesmo"
- General objections: "não tenho tempo", "vou pensar", "preciso falar com meu sócio", "minha equipe não vai usar", "parece complicado", "não quero IA falando com aluno"
- Trust/security: "é seguro?", "tem LGPD?", "vocês leem as conversas?", "a IA pode responder errado?"
- Integrations: "conecta meu WhatsApp?", "integra com Instagram?", "tem disparo em massa?", "integra com meu sistema?"
- Out of profile: "sou aluno", "sou professor autônomo", "tenho clínica", "tenho academia", "ainda não abri meu studio"
- Resume/follow-up: "pode continuar", "qual era mesmo o plano?", "alguma novidade da lista?", "só me manda o preço sem diagnóstico"

## Acceptance Criteria For Future Work

Future implementation against this matrix is acceptable only if:

- No protected path regresses.
- New coverage reuses existing templates/policy/product knowledge where possible.
- Any new template has a documented reason in this matrix.
- Any new product claim is sourced from product knowledge.
- Commercial understanding remains LLM-first.
- New behavior has local evals and selected real OpenAI transcripts.
- Cost and latency are measured before/after.
- Sales Inbox remains complete for new routes.
