# Conversion Path Fixtures

| Visitor signal | Expected conversion path | Expected destination |
| --- | --- | --- |
| "Quero assinar agora" without plan/context | no conversion yet | Answer briefly, start/continue free diagnostic; trusted checkout only after diagnostic + plan confirmation |
| "Quero o sistema completo" | `plan_recommendation` then `checkout_intent` | Recommended/highest-value plan from config, then checkout if visitor confirms |
| "Tenho atendimento, agenda e financeiro baguncados" | `plan_recommendation` | Recommended/highest-value plan from config after answering plan fit |
| "Quero ver uma demonstracao" | no conversion until diagnostic context, then `guided_demo` if ready | Demo intent starts/continues diagnostic first; configured `/pilates/demonstracao` only after enough context |
| "Quero ver os planos" | no conversion until diagnostic context, then `view_plans` | Brief plan framing, start/continue diagnostic, then configured `/pilates/planos` after diagnostic or insistence |
| "Quero fazer uma analise antes" | `analysis_request` | `assistedConversion.analysisDestination` |
| "Quero falar com humano" | `human_whatsapp_assist` | `assistedConversion.humanWhatsAppDestination` |
| "Quero agente de marketing" | `custom_agent_follow_up` | Analysis/custom follow-up path after operation summary and contact |
| Widget opened without message | no conversion path yet | Neutral opening with common options |
| "Falar com consultor" clicked | no conversion until diagnostic context | Direct commercial opening and one diagnostic question |
| "Continuar no WhatsApp" clicked | `human_whatsapp_assist` or continued consultor path | WhatsApp destination with source context and same answer policy |
| Guided demo completed | `plan_recommendation` | Recommended next step based on selected scenario/demo context |
| "Quanto custa?" with no context | no conversion yet | Brief pricing framing, start/continue diagnostic, no checkout push |
| "Estou quase fechando o 7 Agentes, mas tenho medo de configurar errado" | `checkout_intent` only after risk reducers | Explain setup/onboarding and offer checkout or human WhatsApp |
| Widget opened from floating button | no conversion path yet | Neutral first message, common paths and no immediate checkout |
| "Falar com consultor" clicked from landing CTA | no checkout path yet | Stronger commercial opening, asks operational context before recommending a plan |
| "Continuar no WhatsApp" clicked from landing CTA | `human_whatsapp_assist` when visitor confirms channel | WhatsApp destination with safe summary and same answer policy as web |
| "Demo guiada" clicked while `guidedDemoReady=false` | `human_whatsapp_assist` or product explanation | Do not show fake `/pilates/demonstracao`; explain demo readiness and route to consultor/WhatsApp |
| "Demo guiada" clicked while `guidedDemoReady=true` | `guided_demo` | Configured demo destination, selected pain/agent/session context preserved |
| "Quero ver planos, mas ainda estou comparando" | `view_plans` | Open `/pilates/planos`; do not emit checkout/subscription intent |
| "Me manda o link para pagar o plano recomendado" after plan recommendation | `checkout_intent` | Trusted configured checkout destination for the recommended plan only |
| "Posso pagar por PIX? E se falhar?" | answer before conversion | Explain configured billing boundary and that plan activates only after confirmed payment |
| "Tenho medo de nao conseguir configurar" | answer before conversion | Explain self-guided setup with attendant, minutes to start and WhatsApp/human assistance when needed |
| "Quero cancelar se nao gostar" | answer before conversion | Explain configured 30-day guarantee/cancellation boundary before any checkout CTA |
| "Meu studio usa o proprio WhatsApp?" | answer before conversion | Explain studio-owned WhatsApp for paying studios and separate sales WhatsApp for Taliya |
| FAQ final CTA clicked with no message yet | no conversion path yet | Opens normal widget-style consultor with `sourceSection=faq_doubt_cta`, neutral opening and no checkout push |
| Diagnostic report: "quero responder WhatsApp e organizar reposicoes" | `custom_agent_diagnostic_mapped` then SaaS funnel | Report classification `mapped_solution`; mapped agents Atendimento/Agenda; CTAs consultor/demo/WhatsApp with diagnostic context |
| Diagnostic report: "quero agente de marketing para Instagram" | `custom_agent_follow_up` | Report classification `custom_agent`; CTA opens consultor/WhatsApp in proposal mode and asks scope/contact |
| Diagnostic report: "quero WhatsApp, reposicoes e marketing" | `mixed_subscription_plus_custom` | Report separates mapped SaaS work from custom-agent work; no checkout direct |
| Diagnostic report: "quero automatizar meu studio" | `custom_agent_diagnostic_unclear` only after CTA/contact | Report asks for missing context; routes to consultor/WhatsApp, no invented scope |

## Required Checks

- No path collects card data in chat.
- No path treats checkout intent as active subscription.
- Human handoff includes selected/interested plan when available.
- Broad/multi-agent needs prioritize the configured recommended/highest-value plan.
- Checkout appears only after explicit buying intent or confirmed plan recommendation.
- Entry path changes the first message tone.
- Risk reducers are answered before checkout when the visitor hesitates.
- Guided demo CTA is hidden or rerouted when the real SaaS demo environment is not ready.
- Plan-comparison tracking remains distinct from checkout/subscription tracking.
- Web and WhatsApp use the same approved answer policy for equivalent buyer questions.
- Custom-agent diagnostic reports never route directly to checkout.
- Diagnostic report CTAs carry `contextVariant` into consultor or WhatsApp.
