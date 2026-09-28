# Message Template Contract: Taliya Commercial Agent

**Status**: Binding for implementation.  
**Purpose**: Keep the agent LLM-first while making the customer-facing voice controlled, short, and consistent.

## Core Decision

Templates are not the deterministic brain. Templates are the official voice.

The LLM must:

- interpret the lead message;
- choose behavior;
- select one or more `template_ids`;
- fill approved variables;
- propose state updates and facts;
- request tools through structured fields.

The renderer must:

- validate template IDs;
- validate required variables;
- render short messages;
- adapt delivery to widget or WhatsApp;
- block unsafe or unsupported rendered output.

## Template Categories

Required categories:

- `opening.cold_greeting`
- `opening.cold_greeting_named`
- `opening.widget_empty_diagnostic`
- `opening.general_interest`
- `opening.instagram_source`
- `opening.site_cta`
- `opening.diagnostic_cta`
- `product.overview_short`
- `product.price_direct`
- `product.plan_direct`
- `product.plan_fit_with_diagnostic`
- `product.demo_direct`
- `product.whatsapp_direct`
- `product.crm_direct`
- `product.agents_direct`
- `diagnostic.offer_soft`
- `diagnostic.start`
- `diagnostic.start_named`
- `diagnostic.ask_active_students`
- `diagnostic.ask_main_pain`
- `diagnostic.ask_current_process`
- `diagnostic.ask_pain_detail`
- `diagnostic.ask_priority`
- `diagnostic.ask_urgency`
- `diagnostic.partial_progress`
- `diagnostic.deliver`
- `diagnostic.deliver_hold`
- `diagnostic.deliver_context`
- `diagnostic.deliver_crm_base`
- `diagnostic.deliver_operational_step`
- `diagnostic.deliver_agent_recommendation`
- `diagnostic.deliver_plan_recommendation`
- `diagnostic.deliver_demo_not_offered`
- `diagnostic.deliver_demo_already_offered`
- `diagnostic.insufficient_evidence`
- `waitlist.offer_after_contract_intent`
- `waitlist.ask_missing_studio`
- `waitlist.ask_missing_city`
- `waitlist.ask_missing_contact_path`
- `waitlist.joined`
- `waitlist.status_preserved`
- `handoff.acknowledge`
- `handoff.paused`
- `fallback.invalid_json`
- `fallback.provider_timeout`
- `fallback.product_knowledge_missing`
- `fallback.cost_cap`
- `fallback.unmapped_adaptive`
- `fallback.unsupported_media`
- `safety.prompt_injection`
- `safety.out_of_scope`
- `safety.sensitive_data`
- `safety.no_medical_advice`

## Template Record Shape

Each template must define:

- `template_id`;
- category;
- allowed states;
- blocked states;
- channel support: `widget`, `whatsapp`, or `both`;
- required variables;
- optional variables;
- product knowledge requirements;
- max rendered message count;
- max characters per chunk;
- whether buttons are allowed;
- whether official links are allowed;
- acceptance examples;
- rejection examples.

## Rendering Rules

- Assistant turns should normally render 1-3 short messages.
- One message should carry one idea.
- No assistant turn may become a text wall.
- Completed diagnostic delivery is the only approved staged exception. It may render more than 3 short messages across a delivery sequence when the render plan includes typing/delay cadence and each message carries one idea.
- Buttons are allowed only in widget and only for validated actions.
- WhatsApp must use text and official links instead of widget buttons.
- If the LLM chooses a widget-only action for WhatsApp, the renderer must convert it to approved text/link or block it.
- Template variables may be adaptive, but they must not invent product facts, lead facts, dates, guarantees, checkout, or links.

## Diagnostic Template Rules

The final diagnostic must be composed from staged templates instead of one generic two-line summary.

Required final diagnostic stages:

1. `diagnostic.deliver_hold`
2. `diagnostic.deliver_context`
3. `diagnostic.deliver_crm_base`
4. `diagnostic.deliver_operational_step`
5. one `diagnostic.deliver_agent_recommendation` per indicated agent/routine
6. `diagnostic.deliver_plan_recommendation`
7. either `diagnostic.deliver_demo_not_offered` or `diagnostic.deliver_demo_already_offered`

Required variables include:

- `first_name`, optional and only when reliable;
- `pain_context_human`;
- `crm_base_recommendation`;
- `operational_first_step`;
- `agent_name`;
- `agent_fit_phrase`;
- `agent_pain_resolved`;
- `agent_recommendation_reason`;
- `agent_practical_action`;
- `recommended_plan_or_range`;
- `demo_status`.

The rendered final diagnostic must preserve this meaning:

```text
Pelo tamanho, momento do studio e todo o contexto acima, eu recomendaria pra voce o plano [plano_ou_faixa].
```

If demo was not offered:

```text
Temos algumas demonstracoes que mostram o funcionamento na pratica. Quer que eu te mande?
```

If demo was already offered:

```text
Chegou a olhar as demonstracoes? O que voce achou?
```

Rejected final diagnostic patterns:

- "Pelo contexto, o principal gargalo parece..."
- "Para plano, eu compararia..."
- using "Isso faz sentido para o momento do seu studio?" as the standard final close
- plan before CRM/operational recommendation
- waitlist offer before demo or clear contract intent

## Diagnostic Question Feedback Templates

Diagnostic question templates must support an optional preceding feedback/reflection message. The renderer may render feedback plus the next question in the same assistant turn, but it must keep them as separate short messages.

Required feedback variable:

- `answer_feedback`, grounded in the lead's previous answer.

If the model/runtime cannot produce grounded feedback, it should use a short neutral orientation only once at diagnostic start, not generic filler after every question.

## Unmapped Case Policy

If no mapped template fits:

- LLM may choose `fallback.unmapped_adaptive`;
- output must remain short;
- no side effect is allowed unless separately validated;
- no product claim is allowed without product knowledge;
- at most one clarification question is allowed;
- return to diagnostic only if relevant and allowed by state;
- low confidence should ask clarification or hand off.

## Delivery Rules By Channel

Widget:

- render short bubbles;
- use buttons/quick replies for clear next actions;
- use a validated demo CTA/button when the template/action is official and the channel is widget;
- keep the existing visual direction untouched;
- do not add explanatory in-app text about how the agent works.

WhatsApp:

- split into short chunks;
- attempt typing/delay for each chunk;
- use text or official links instead of buttons;
- avoid more than 3 chunks per assistant turn unless an operator explicitly approves;
- completed diagnostic staged delivery is an approved exception to the 3 chunk limit only when each chunk is short and delay/typing cadence is present;
- demo CTAs must be rendered as official full links, never buttons;
- never ask for the WhatsApp phone number.

## Validator Requirements

Before delivery, validators must check:

- selected template exists;
- template is allowed in current state;
- required variables are present;
- variable values are grounded in lead facts or product knowledge;
- rendered text follows brevity limits;
- rendered text does not include blocked phrases;
- rendered text does not violate channel rules;
- rendered text does not contradict selected state/action;
- waitlist templates only appear after clear contract intent;
- diagnostic completion template only appears after diagnostic ledger completion.
- diagnostic completion stages appear in the required order.
- final diagnostic plan recommendation uses `diagnostic.deliver_plan_recommendation` and an official product knowledge plan/range.
- final diagnostic demo line matches persisted demo status.
- diagnostic question turns include feedback before the first question when the lead explicitly requested diagnostic and before each next question after a previous answer.

## Product Explanation And Follow-Up Delta Templates

The next implementation pass must add only the missing templates defined in [product-followup-delta-contract.md](./product-followup-delta-contract.md). Existing approved openings, diagnostic templates, direct price templates, demo direct, WhatsApp direct, waitlist, handoff, and safety templates are protected.

### New Required Templates

- `product.how_it_works_direct`
- `product.comparison_current_tool`
- `product.integration_scope_direct`
- `product.security_data_direct`
- `product.out_of_profile_redirect`

Do not create `product.general_objection_response` unless evals prove that LLM+policy remains inconsistent for general objections.

### Template Selection Rules

- The LLM chooses these templates through structured output.
- Runtime code validates template id, state, channel, product knowledge, and variables.
- Runtime code must not select these templates through commercial phrase matching.
- These templates must use official product knowledge keys and grounded variables.
- These templates must render as short widget/WhatsApp chunks; no text wall is allowed.

### Protected Copy Rules

- Approved openings must not be rewritten to solve product explanation.
- `product.how_it_works_direct` is a product answer, not an opening.
- "CRM" must not appear in lay lead product explanation, price objection, openings, or comparison unless the lead directly asked about CRM.
- Lay lead copy must avoid technical SaaS terms such as pipeline, lead scoring, automacao, arquitetura, stack, webhook, API, Meta, Dualhook, SDK, and runtime unless the lead used the term first. Prefer studio-owner language: conversas, alunos, interessados, agenda, reposicoes, cobrancas, acompanhamento, rotina, equipe, and o que precisa de acao.
- WhatsApp setup and integration language must not promise automatic setup, mass messaging, checkout, payment links, Instagram integration, current-system integration, or migration.
- Security/data language must not invent LGPD, certification, encryption, audit, data-retention, or privacy guarantees.

### New Variable Grounding Rules

`product.how_it_works_direct`:

- `contextual_next_step` must follow one of the approved meanings in the delta contract or be repaired.
- `recommended_area`, if present, must be grounded in saved diagnostic output.
- post-diagnostic wording must not restart diagnostic.

`product.comparison_current_tool`:

- `current_tool_context`, if present, must be grounded in the lead message or saved facts.
- competitor names may be used only when the lead mentioned them.

`product.integration_scope_direct`:

- `integration_topic`, if present, must be grounded in the lead message.
- unsupported integration promises must be blocked.

`product.security_data_direct`:

- all security/privacy claims must be grounded in `security_and_data` or `privacy_or_data_notes`.
- missing official details should route to human confirmation or safe fallback.

`product.out_of_profile_redirect`:

- must qualify gently;
- must not offer diagnostic automatically;
- must not treat students as buyers.
