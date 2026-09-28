# Conversation Route Matrix: Atendente IA

## Purpose

This document turns the commercial strategy into an implementation contract for the web widget and WhatsApp attendant.

The agent must use this matrix after trusted runtime configuration and approved answer knowledge. It is not a prompt by itself; it defines routing, gates, lead effects and eval coverage for the most likely buyer paths.

## Global Rules

- Answer the buyer's direct question before steering to conversion.
- Ask at most one concise qualifying question when context is missing.
- Keep the default motion consultor-led: diagnose, show proof, recommend, then route.
- Do not route cold visitors directly to checkout.
- Do not collect payment data, billing documents, student health details or private student records in chat or WhatsApp.
- Do not invent prices, discounts, integrations, guarantees, timelines, checkout URLs or WhatsApp numbers.
- Read plan names, prices, limits, checkout destinations, WhatsApp destinations and demo readiness from trusted configuration.
- Use the same answer policy on web and WhatsApp.
- Create or update a lead only after meaningful intent, contact capture, plan/demo/checkout interest, human handoff, custom-agent request or high-intent buying signal.

## Response Pattern

Every normal commercial answer should follow this shape:

```text
direct answer
  -> studio-specific implication
  -> one qualifying question when needed
  -> next step allowed by gate
```

For high-ticket close attempts:

```text
pain
  -> impact
  -> proof/demo
  -> recommended plan
  -> risk reducer/objection handling
  -> plans, checkout or WhatsApp assisted close
```

## Entry Routes

| Route ID | Buyer signal | Agent first move | Allowed next step | Lead effect | Eval required |
| --- | --- | --- | --- | --- | --- |
| `entry_widget_neutral` | Opens floating widget | Neutral greeting; ask how to help and offer product, agents, demo, plans or WhatsApp | Continue chat, diagnose, answer question | No lead until meaningful intent/contact | Opening tone eval |
| `entry_consultor_cta` | Clicks `Falar com consultor` | Acknowledge interest; ask whether they want help choosing/acquiring Taliya | Diagnose, recommend demo, recommend plan, WhatsApp, checkout after confirmation | Lead only after meaningful reply/contact/high intent | Entry-path eval |
| `entry_whatsapp_cta` | Clicks `Continuar no WhatsApp` | Continue the same commercial conversation on WhatsApp; preserve source context | Same as consultor plus human takeover when requested | Lead with `channel=whatsapp` when contact/session exists | Web/WhatsApp parity eval |
| `entry_guided_demo` | Starts or returns from guided demo | Explain current demo step; invite questions; preserve scenario/pain/steps | Continue demo, consultor, WhatsApp, plans after recommendation | Lead when demo starts/completes or buyer asks next step | Demo routing eval |
| `entry_crm_agent_diagnostic` | Clicks `Diagnostico gratuito` or `Quer ver como ficaria no seu studio?` | Start the CRM-first diagnostic flow; ask one consultative question at a time and classify buying timing | Final diagnostic, demo, consultor, WhatsApp, plans after recommendation | Lead warm/hot when pain, contact, buying timing or high intent exists; `conversionPath=crm_agent_diagnostic` | CRM-first diagnostic eval |
| `entry_custom_agent_diagnostic_report` | Submits Agente sob medida diagnostic block | Generate a structured report instead of a chat answer; classify mapped/custom/mixed/unclear | Consultor/demo/WhatsApp for mapped SaaS; consultor/WhatsApp custom proposal for custom | Lead after report CTA, custom/mixed classification, contact or high intent | Diagnostic report eval |
| `entry_faq_doubt_cta` | Clicks the final FAQ "ficou alguma duvida?" CTA | Open the normal widget flow with `entryPath=widget` and `sourceSection=faq_doubt_cta`; ask what doubt remains | Continue chat, answer objection, diagnose, demo, plans only if asked/qualified, WhatsApp | No lead until meaningful intent/contact; track FAQ source | FAQ doubt CTA eval |

## Core Discovery Routes

| Route ID | Buyer signal | Intent/readiness | Agent response contract | Allowed next step | Lead/status effect | Eval required |
| --- | --- | --- | --- | --- | --- | --- |
| `ask_product_basic` | "O que e isso?", "como funciona?" | `curious` | Explain Taliya as an operational CRM for Pilates with integrated AI agents; clarify it is not just chatbot/agenda/WhatsApp automation | Ask main pain or offer diagnostic/demo/product explanation | No lead unless contact/high intent | Product answer eval |
| `describe_pain_known` | Mentions faltas, reposicoes, agenda, vendas, financeiro, retencao, gestao or historico | `diagnosing` | Name the CRM area that organizes the work, then the matching agent(s); connect pain to time/money/control and ask one sizing/context question | Recommend diagnostic, agent bundle, demo, plans if ready | Lead if pain is meaningful; `status=ai_active`; priority warm if specific | CRM+agent pain mapping eval |
| `describe_broad_pain` | Multiple pains or "quero organizar tudo" | `plan_ready` | Explain this is broad operational need; frame complete-system value | Recommend configured highest-value plan, usually 7 Agentes | Lead warm/hot depending buying intent; recommended plan set | 7 Agentes recommendation eval |
| `ask_agent_specific` | "O que o agente de agenda faz?" | `curious` or `diagnosing` | Explain only configured capabilities; connect to Pilates routine; ask whether this is the main bottleneck | Demo relevant scenario or recommend plan if context exists | No lead unless meaningful intent | Agent detail eval |
| `ask_is_it_chatbot` | "Isso e so chatbot?" | `objection` | Clarify product combines CRM, agenda/routines, records, actions, WhatsApp and human control | Ask which routine they want to remove from manual work | No lead unless continued intent | Differentiation eval |
| `ask_replace_team` | "Vai substituir recepcionista?" | `objection` | Position as leverage for repetitive work; human controls sensitive moments | Demo/human-control proof or diagnose routine | Warm if pain expressed | Objection eval |

## Plans And Pricing Routes

| Route ID | Buyer signal | Intent/readiness | Agent response contract | Allowed next step | Lead/status effect | Eval required |
| --- | --- | --- | --- | --- | --- | --- |
| `ask_price_no_context` | "Quanto custa?" with no pain/context | `curious` | Give short configured plan range/summary if available; ask one qualifying question before recommending | Offer `/pilates/planos` only if buyer asks/insists | Lead warm only if they continue or provide contact | Pricing gate eval |
| `ask_view_plans` | "Quero ver planos", "tem pagina de planos?" | `plan_ready` if explicit | Briefly summarize Base, 1, 3 and 7; if no context ask one question; route to configured plans page when appropriate | `/pilates/planos`, consultor continues | Create/update lead; `conversionPath=view_plans`; status `ai_active` | Plan page routing eval |
| `ask_best_plan` | "Qual plano pra mim?" | `diagnosing` or `plan_ready` | Ask one key context question if missing; otherwise recommend best-fit plan from config | Plans page, demo, WhatsApp or checkout if confirmed | Lead with `recommendedPlanId`; warm/hot | Recommendation eval |
| `broad_need_plan` | Wants many automations or full system | `plan_ready` | Recommend configured complete plan; explain why lower plans are narrower starts | Plans page or checkout after confirmation | Lead hot if buying signal; `recommendedPlanId=seven_agents` by config | Highest-value eval |
| `budget_or_small_start` | "Achei caro", "quero comecar barato" | `objection` | Reframe value; offer lower plan only as narrower start, not equal default | Compare plans or WhatsApp consultor | Lead warm; next action objection follow-up | Lower-plan framing eval |
| `base_plan_interest` | Wants CRM only/no agents | `plan_ready` narrow | Explain Base has zero active AI agents; suitable for CRM-only start | Plans page or consultor | Lead warm; interestedPlanId=base | Base scope eval |
| `ask_trial_free` | "Tem teste gratis?", "trial?" | `objection` | State no public trial; offer real guided demo when ready and 30-day guarantee | Demo, consultor, WhatsApp, plans | Lead warm if contact/continued intent | No-trial eval |
| `ask_discount_coupon` | "Tem desconto?", "cupom?" | `objection` | Do not offer discount unless trusted config allows; explain current offer safely | Plans/WhatsApp if they need human confirmation | Lead warm | Discount boundary eval |

## Demo And Proof Routes

| Route ID | Buyer signal | Intent/readiness | Agent response contract | Allowed next step | Lead/status effect | Eval required |
| --- | --- | --- | --- | --- | --- | --- |
| `ask_demo_ready` | "Quero ver funcionando", "demo" and `guidedDemoReady=true` | `proof_needed` | Offer real SaaS guided demo; explain it uses approved demo data and is not their configured studio | `/pilates/demonstracao` with context | Lead with `conversionPath=guided_demo`; warm | Demo-ready eval |
| `ask_demo_not_ready` | Demo requested while `guidedDemoReady=false` | `proof_needed` | Do not fake demo; offer product explanation, consultor or WhatsApp | Consultor/WhatsApp/product explanation | Lead warm if contact/intent | Demo gate eval |
| `demo_completed_plan_interest` | Completed demo and asks price/next step | `plan_ready` | Summarize observed scenario, recommend best-fit plan, offer plans page | Plans page; checkout only after confirmation | Lead hot; `guidedDemoCompleted=true` | Demo completion eval |
| `demo_completed_hesitation` | Completed demo but uncertain | `proof_needed` | Ask what felt unclear; answer objection; offer WhatsApp consultor | WhatsApp/consultor, continue Q&A | Lead warm; nextAction follow-up if contact | Demo objection eval |

## Checkout And Subscription Routes

| Route ID | Buyer signal | Intent/readiness | Agent response contract | Allowed next step | Lead/status effect | Eval required |
| --- | --- | --- | --- | --- | --- | --- |
| `buy_now_no_plan` | "Quero assinar" without plan/context | `checkout_ready` after confirmation | Confirm fit/recommend plan first; remind checkout is secure; do not collect payment data | Trusted checkout only after plan confirmation | Lead hot; `conversionPath=plan_recommendation` until plan is confirmed | Checkout gate eval |
| `buy_now_recommended` | Confirms recommended plan | `checkout_ready` | Confirm selected plan, risk reducers if relevant, route to trusted checkout | Trusted checkout destination from config | Lead hot; status may become `checkout_sent` when link sent | Trusted URL eval |
| `plans_page_checkout_click` | Clicks checkout CTA on `/pilates/planos` | `checkout_ready` | Treat as explicit plan selection; use server-side billing route when Spec 3 exists | Checkout creation route | Lead hot; never paid/subscribed from click | Billing boundary eval |
| `payment_data_in_chat` | Sends card/CVV/payment credentials | unsafe | Refuse to collect; tell them payment happens only in secure provider checkout; do not repeat/store details | Trusted checkout or human assistance | Safety event; avoid raw transcript | Sensitive-data eval |
| `after_subscribing` | "O que acontece depois que eu assino?" | `curious` or `checkout_ready` | Explain billing confirmation, onboarding link, account/studio setup, agent setup; no activation from redirect | Checkout if ready or plans/demo | Lead warm/hot by intent | Post-payment eval |
| `payment_failed` | "Paguei mas falhou", "Pix nao confirmou" | support boundary | Explain failed/incomplete payment does not activate plan; billing confirmation is required | Human/Sales Inbox or retry checkout when configured | Lead hot; nextAction billing verification | Payment failure eval |

## WhatsApp And Human Handoff Routes

| Route ID | Buyer signal | Intent/readiness | Agent response contract | Allowed next step | Lead/status effect | Eval required |
| --- | --- | --- | --- | --- | --- | --- |
| `continue_whatsapp` | Wants WhatsApp continuation | `assisted_close` or `warm` | Explain same attendant can continue on WhatsApp; preserve summary/context | Configured WhatsApp destination | Lead with WhatsApp/session when available | WhatsApp continuity eval |
| `ask_human` | "Quero falar com humano" | `assisted_close` | Ask contact if missing; create safe summary; route to trusted WhatsApp/Sales Inbox | Human WhatsApp handoff | Lead `handoff_requested`; hot if buying intent | Human handoff eval |
| `operator_takeover` | Operator takes over | `human_active` | AI pauses WhatsApp replies; web may answer general product questions without pretending to be human closer | Human reply via Sales Inbox | Status `human_active`; audit event | Takeover pause eval |
| `resume_ai` | Operator resumes AI | `ai_active` | Continue with same approved answer policy and safe summary | AI replies allowed on next inbound | Status `ai_active`; audit event | Resume eval |
| `opt_out` | "Parar", "nao me manda msg" | terminal | Confirm opt-out when allowed; stop proactive and automated replies as required | None unless new opt-in later | Status `do_not_contact`; no follow-up | Opt-out eval |

## Custom-Agent And Unsupported Routes

| Route ID | Buyer signal | Intent/readiness | Agent response contract | Allowed next step | Lead/status effect | Eval required |
| --- | --- | --- | --- | --- | --- | --- |
| `primary_agent_configuration` | Wants special rule inside Atendimento, Agenda, Vendas, Financeiro, Retencao, Gestao or Historico | `diagnosing` | Explain this is likely studio-specific configuration of an existing primary agent; ask exact rule/process | Consultor, demo, plan recommendation | Lead warm; selected agents updated | Config-vs-custom eval |
| `custom_marketing_agent` | Wants marketing, ads, content, partnerships or unmapped operation | `custom_agent_mapping` | Say it is Agente sob medida, separate from public plans; ask operation details and contact | Custom-agent follow-up | Lead with `conversionPath=custom_agent_follow_up`; status `handoff_requested` if contact exists | Custom-agent eval |
| `unknown_integration` | "Integra com X?" not configured | `unknown` | State what is confirmed; say integration is not confirmed if absent from config; offer mapping/consultor | WhatsApp/human/custom mapping | Lead if high intent/contact | Unknown integration eval |
| `unsupported_claim_request` | Asks agent to promise unsupported result | guardrail | Refuse guarantee; explain limits and available proof/risk reducers | Demo/consultor | Safety/guardrail event if severe | Unsupported-claim eval |

## Custom-Agent Diagnostic Report Routes

These routes apply to `POST /api/landing/custom-agent-diagnostic`, not to a normal chat turn.

| Route ID | Free-text diagnostic signal | Classification | Report contract | CTAs | Lead/status effect | Eval required |
| --- | --- | --- | --- | --- | --- | --- |
| `diagnostic_existing_solution` | Visitor describes WhatsApp atendimento, reposicoes, agenda, financeiro, vendas, retencao, gestao or historico work | `mapped_solution` | Say Taliya already covers it; name mapped agents; explain impact; recommend SaaS funnel | Falar com consultor, Demo guiada when ready/gated, Continuar pelo WhatsApp | Lead after CTA or high intent; conversion can continue to `plan_recommendation` | Existing-solution diagnostic eval |
| `diagnostic_custom_agent` | Visitor asks for marketing, content, ads, partnerships, HR, inventory or another unmapped operation | `custom_agent` | Say it is Agente sob medida; separate from public plans; list missing scope questions | Solicitar proposta de agente sob medida, Continuar pelo WhatsApp | Lead with `conversionPath=custom_agent_follow_up`; status `handoff_requested` when contact exists | Custom diagnostic eval |
| `diagnostic_mixed_solution` | Visitor combines mapped SaaS work with unmapped custom operation | `mixed_solution` | Split covered agents from custom operation; sell SaaS path and custom discovery as separate | Consultor/demo/WhatsApp for SaaS plus custom proposal CTA | Lead with `conversionPath=mixed_subscription_plus_custom`; custom summary stored | Mixed diagnostic eval |
| `diagnostic_unclear` | Visitor is vague, e.g. "quero automatizar meu studio" | `unclear` | State what can be inferred; ask for missing detail; avoid inventing scope | Falar com consultor, Continuar pelo WhatsApp | Lead only after CTA/contact/high intent; conversionPath `custom_agent_diagnostic_unclear` | Unclear diagnostic eval |

Report route global rules:

- It returns report sections, not assistant chat bubbles.
- It never routes directly to checkout.
- It reads mapped agents, plans, demo readiness and destinations from trusted configuration.
- It carries `contextVariant` into consultor/WhatsApp so the next opening is not generic.
- It creates safe summaries for Sales Inbox/Sales Inbox/n8n optional automation instead of storing raw free text by default.

## Risk Reducer Routes

| Route ID | Buyer signal | Agent response contract | Allowed next step | Lead effect | Eval required |
| --- | --- | --- | --- | --- | --- |
| `guarantee_refund` | Asks guarantee/cancel/refund | Answer from trusted terms; public monthly plans have 30-day guarantee; avoid legal overpromise | Plans/checkout if ready; human if unsure | Lead warm/hot by intent | Guarantee eval |
| `setup_fear` | Afraid to configure wrong | Explain self-guided setup with AI support, starts in minutes after confirmed payment; external provider/customer delay may affect full operation | Demo, WhatsApp, checkout if confirmed | Warm/hot | Setup eval |
| `whatsapp_ownership` | Asks whose WhatsApp is used | Sales attendant uses operator WhatsApp; paying studios use their own connected WhatsApp for operational agents | Plans/demo/consultor | Warm if buying context | WhatsApp ownership eval |
| `ai_wrong_answer_fear` | Afraid AI will answer wrong | Explain approved knowledge, limits, human control/takeover/review where product allows | Human-control demo or consultor | Warm | Safety/control eval |
| `usage_cap` | Asks limits or over-limit | Explain hard caps; upgrade or buy extra quota; no silent overcharge | Plans/add-on info when configured | Warm/hot | Usage cap eval |
| `invoice_tax` | Asks nota fiscal | Explain manual on request in v1 after trusted payment confirmation unless config changes | Human/billing path if needed | Warm/hot | Fiscal boundary eval |

## Failure And Safety Routes

| Route ID | Buyer signal/system condition | Agent/system response contract | Allowed next step | Lead effect | Eval required |
| --- | --- | --- | --- | --- | --- |
| `live_ai_failed` | OpenAI timeout/provider error | Use safe degraded fallback; do not break widget; no invented data | Retry later, WhatsApp, consultor | Track fallback; lead only if existing intent | Provider failure eval |
| `n8n_automation_failed` | Optional n8n automation fails | Chat/WhatsApp/Sales Inbox continue; mark external sync pending/failed and notify/log | Continue conversation | Do not lose local lead state | Sync failure eval |
| `duplicate_whatsapp_webhook` | Same provider message delivered twice | Process once; no duplicate reply, event or lead | None | Idempotency recorded | Idempotency eval |
| `weak_lead_match` | Same studio name/pain only | Do not auto-merge; keep separate or flag possible duplicate | Operator review | No unsafe merge | Lead merge eval |
| `prompt_injection` | Asks for prompt/secrets/policy bypass | Refuse and redirect to product help | Continue safe conversation | Safety event if needed | Guardrail eval |
| `off_topic` | Irrelevant non-commercial question | Briefly redirect to Taliya/Pilates SaaS | Continue or close | No lead | Off-topic eval |
| `sensitive_student_data` | Shares student health/private details | Do not repeat; say not needed; redirect to general operational context | Continue safely | Avoid raw transcript/sync | LGPD eval |

## Lead Effects Contract

| Conversion path | When created | Default status | Priority guidance | Required metadata |
| --- | --- | --- | --- | --- |
| `guided_demo` | Demo requested/started/completed | `ai_active` | warm; hot after completion + price/plan intent | scenario, selectedPainIds, completed steps |
| `view_plans` | Buyer asks/insists on plans or consultor recommends comparison | `ai_active` | warm | interestedPlanId/recommendedPlanId when known |
| `plan_recommendation` | Agent recommends a configured plan | `ai_active` | warm/hot by buying signal | recommendedPlanId, reason, selected pains |
| `checkout_intent` | Buyer asks to subscribe/pay/start or clicks checkout | `ai_active` or `checkout_sent` when link is sent | hot | selectedPlanId/recommendedPlanId, checkoutGateReason |
| `subscription_intent` | Buyer says they intend to subscribe but checkout not sent | `ai_active` | hot | selectedPlanId if known, risk reducers covered |
| `human_whatsapp_assist` | Buyer asks for human/WhatsApp assisted close | `handoff_requested` | hot if buying intent, warm otherwise | safe summary, contact/WhatsApp when available |
| `custom_agent_follow_up` | Buyer asks for unmapped operation | `handoff_requested` when contact exists, else `ai_active` | hot if contact exists; warm otherwise | operation, goal, tools/channels, expected outcome |
| `custom_agent_diagnostic_mapped` | Diagnostic report says Taliya already covers the request and buyer clicks CTA/high intent | `ai_active` | warm/hot by buying signal | reportId, classification, mapped agents, contextVariant |
| `mixed_subscription_plus_custom` | Diagnostic report contains both mapped SaaS work and custom-agent work | `ai_active` or `handoff_requested` | hot if contact or plan intent exists; warm otherwise | reportId, mapped agents, custom operation, contextVariant |
| `custom_agent_diagnostic_unclear` | Diagnostic report is vague but buyer clicks CTA or provides contact | `ai_active` | low/warm | reportId, missing details, contextVariant |
| `analysis_request` | Buyer asks for diagnostic/analysis | `ai_active` | warm/hot by contact and pain | selectedPainIds, qualification, safe summary |
| `high_intent` | Price/how-to-start/contact/checkout signals | `ai_active` or current operational status | hot | intent signal, safe summary, nextAction |

## Eval Coverage Checklist

Before public launch, evals must cover:

- every entry route;
- every plan/pricing route;
- guided demo ready and not-ready branches;
- checkout gates and payment-data refusal;
- human WhatsApp handoff and operator takeover pause;
- custom-agent vs primary-agent configuration distinction;
- all risk reducer routes;
- provider, Sales Inbox/n8n optional automation and duplicate WhatsApp failure paths;
- web and WhatsApp parity for equivalent buyer questions;
- no cold route to checkout;
- no model-generated checkout or WhatsApp URL.
