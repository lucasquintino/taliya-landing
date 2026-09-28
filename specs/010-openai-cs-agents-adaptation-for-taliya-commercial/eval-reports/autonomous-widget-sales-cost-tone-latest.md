# autonomous-widget-sales-cost-tone-latest

Generated at: 2026-05-23T02:40:58.230Z

## Executive Summary

- Started: 2026-05-23T02:38:37.146Z
- Finished: 2026-05-23T02:40:58.227Z
- App URL: http://127.0.0.1:3999
- Visual widget: PASS
- Sales Inbox: PASS
- Mapped behavior QA: PASS (0 issue(s))
- Total OpenAI cost observed: US$0.179618
- Average cost per lead: US$0.02566
- Average latency: 5205ms
- P95 latency: 7003ms

## Visual Widget Evidence

- Status: PASS
- Desktop screenshot: specs\010-openai-cs-agents-adaptation-for-taliya-commercial\eval-reports\assets\autonomous-widget-sales-cost-tone-latest\widget-demo-desktop.png
- Mobile screenshot: specs\010-openai-cs-agents-adaptation-for-taliya-commercial\eval-reports\assets\autonomous-widget-sales-cost-tone-latest\widget-demo-mobile.png
- Failures: none

## Sales Inbox Flow Transcript

- Scenario ID: autoval-sales-1779503948154
- Lead ID: lead-autoval-sales-1779503948154
- Turns: 7
- Cost: US$0.06165
- Average latency: 5057ms

Lead 1: quanto custa?
Taliya 1.1: Oi, Ana, tudo bem? Hoje os planos são Base R$ 197/mês, Essencial R$ 497/mês, Avance R$ 897/mês e Completo R$ 1.497/mês.
Taliya 1.2: Se fizer sentido para você, estamos oferecendo um diagnóstico gratuito para o seu studio. Assim você entende se algum dos nossos planos te atenderia. O que você acha?
Runtime 1: http=200; latency=4129ms; cost=US$0.006893; route=product; agent=taliya_commercial_product_agent; templates=product.price_direct, diagnostic.price_hook

Lead 2: quero fazer diagnostico gratuito
Taliya 2.1: Hoje o studio tem mais ou menos quantos alunos ativos ou qual volume de leads por mês?
Runtime 2: http=200; latency=4172ms; cost=US$0.008077; route=diagnostic; agent=taliya_commercial_diagnostic_agent; templates=diagnostic.ask_active_students

Lead 3: tenho 120 alunos, perco interessados no WhatsApp, hoje respondo manualmente, prioridade vendas, urgente agora, quero comparar plano
Taliya 3.1: Pelo contexto, o principal gargalo parece ser atendimento e follow-up no WhatsApp. O primeiro passo seria organizar o fluxo de atendimento e follow-up primeiro.
Taliya 3.2: Para plano, eu compararia Essencial ou Avance, dependendo do peso do atendimento e do follow-up.
Runtime 3: http=200; latency=6715ms; cost=US$0.010875; route=diagnostic; agent=taliya_commercial_diagnostic_agent; templates=diagnostic.deliver

Lead 4: quero contratar, pode me colocar na lista de espera
Taliya 4.1: Estamos trabalhando com um número pequeno de studios agora.
Taliya 4.2: Se fizer sentido, posso colocar seu studio na lista de espera e chamar assim que abrir uma próxima janela.
Runtime 4: http=200; latency=5066ms; cost=US$0.009107; route=waitlist; agent=taliya_commercial_waitlist_agent; templates=waitlist.offer_after_contract_intent

Lead 5: pode colocar o Studio Viva em Vitoria ES
Taliya 5.1: Perfeito, deixei seu studio na lista de espera da Taliya.
Taliya 5.2: Quando abrir uma próxima janela, a equipe chama com o contexto dessa conversa.
Runtime 5: http=200; latency=4915ms; cost=US$0.009409; route=waitlist; agent=taliya_commercial_waitlist_agent; templates=waitlist.joined

Lead 6: quanto custa o Completo?
Taliya 6.1: O Completo fica em R$ 1.497/mês.
Runtime 6: http=200; latency=5913ms; cost=US$0.008815; route=product; agent=taliya_commercial_product_agent; templates=product.price_complete_direct

Lead 7: quero falar com humano
Taliya 7.1: Claro. Vou deixar uma pessoa assumir daqui.
Taliya 7.2: Também deixo o contexto salvo para você não precisar repetir tudo.
Runtime 7: http=200; latency=4488ms; cost=US$0.008474; route=handoff; agent=taliya_commercial_handoff_agent; templates=handoff.acknowledge


## Sales Inbox Evidence

- Lead ID: lead-autoval-sales-1779503948154
- API status: list=200, detail=200
- Lead status: handoff_requested
- Conversion path: human_whatsapp_assist
- Waitlist status: joined
- Diagnostic status: completed
- Human active: true
- AI paused: false
- Messages saved: 26
- Runtime trace: trace_03e61c071152421fadb3f4d6596ea426
- Runtime cost: 0.008474

- user: quanto custa?
- user: quanto custa?
- assistant: Oi, Ana, tudo bem? Hoje os planos são Base R$ 197/mês, Essencial R$ 497/mês, Avance R$ 897/mês e Completo R$ 1.497/mês.
- assistant: Se fizer sentido para você, estamos oferecendo um diagnóstico gratuito para o seu studio. Assim você entende se algum dos nossos planos te atenderia. O que você acha?
- user: quero fazer diagnostico gratuito
- user: quero fazer diagnostico gratuito
- assistant: Hoje o studio tem mais ou menos quantos alunos ativos ou qual volume de leads por mês?
- user: tenho 120 alunos, perco interessados no WhatsApp, hoje respondo manualmente, prioridade vendas, urgente agora, quero comparar plano
- user: tenho 120 alunos, perco interessados no WhatsApp, hoje respondo manualmente, prioridade vendas, urgente agora, quero comparar plano
- assistant: Pelo contexto, o principal gargalo parece ser atendimento e follow-up no WhatsApp. O primeiro passo seria organizar o fluxo de atendimento e follow-up primeiro.
- assistant: Para plano, eu compararia Essencial ou Avance, dependendo do peso do atendimento e do follow-up.
- user: quero contratar, pode me colocar na lista de espera
- user: quero contratar, pode me colocar na lista de espera
- assistant: Estamos trabalhando com um número pequeno de studios agora.
- assistant: Se fizer sentido, posso colocar seu studio na lista de espera e chamar assim que abrir uma próxima janela.
- user: pode colocar o Studio Viva em Vitoria ES
- user: pode colocar o Studio Viva em Vitoria ES
- assistant: Perfeito, deixei seu studio na lista de espera da Taliya.
- assistant: Quando abrir uma próxima janela, a equipe chama com o contexto dessa conversa.
- user: quanto custa o Completo?
- user: quanto custa o Completo?
- assistant: O Completo fica em R$ 1.497/mês.
- user: quero falar com humano
- user: quero falar com humano
- assistant: Claro. Vou deixar uma pessoa assumir daqui.
- assistant: Também deixo o contexto salvo para você não precisar repetir tudo.

## Cost And Latency

- Scenarios: 7
- Turns: 21
- Total cost: US$0.179618
- Average cost per turn: US$0.008553
- Average cost per lead: US$0.02566
- Max turn cost: US$0.011599
- Average latency: 5205ms
- P95 latency: 7003ms
- Max latency: 7385ms
- Most expensive turn: autoval-long-1779503984318 turn 5, US$0.011599

## Transcript: Price short lead

- Scenario ID: autoval-price-1779503984318
- Lead ID: lead-autoval-price-1779503984318
- Turns: 1
- Cost: US$0.007645
- Average latency: 5602ms

Lead 1: quanto custa?
Taliya 1.1: Oi, Ana, tudo bem? Hoje os planos são Base R$ 197/mês, Essencial R$ 497/mês, Avance R$ 897/mês e Completo R$ 1.497/mês.
Taliya 1.2: Se fizer sentido para você, estamos oferecendo um diagnóstico gratuito para o seu studio. Assim você entende se algum dos nossos planos te atenderia. O que você acha?
Runtime 1: http=200; latency=5602ms; cost=US$0.007645; route=product; agent=taliya_commercial_product_agent; templates=product.price_direct, diagnostic.price_hook


## Transcript: Demo lead

- Scenario ID: autoval-demo-1779503984318
- Lead ID: lead-autoval-demo-1779503984318
- Turns: 1
- Cost: US$0.006796
- Average latency: 3720ms

Lead 1: quero ver uma demonstracao
Taliya 1.1: Oi, Ana, tudo bem?
Taliya 1.2: Ver demonstração [action: Ver demonstração -> https://www.taliya.com.br/pilates/planos/demonstracao]
Taliya 1.3: Conte mais sobre os problemas do seu studio, posso te indicar uma demonstração que resolva algo seu.
Runtime 1: http=200; latency=3720ms; cost=US$0.006796; route=product; agent=taliya_commercial_product_agent; templates=product.demo_direct


## Transcript: Pain-first lead

- Scenario ID: autoval-pain-1779503984318
- Lead ID: lead-autoval-pain-1779503984318
- Turns: 1
- Cost: US$0.007687
- Average latency: 4655ms

Lead 1: perco interessados no WhatsApp porque a equipe demora para responder
Taliya 1.1: Oi, Ana, tudo bem? Entendi: o gargalo parece estar nos interessados que chegam pelo WhatsApp e demoram a receber retorno.
Taliya 1.2: Posso fazer um diagnóstico gratuito com poucas perguntas e te devolver o que organizar primeiro, quais agentes fariam sentido e qual plano vale comparar.
Taliya 1.3: O que você acha?
Runtime 1: http=200; latency=4655ms; cost=US$0.007687; route=diagnostic; agent=taliya_commercial_diagnostic_agent; templates=diagnostic.offer_soft


## Transcript: Plan fit lead

- Scenario ID: autoval-plan-1779503984318
- Lead ID: lead-autoval-plan-1779503984318
- Turns: 1
- Cost: US$0.00811
- Average latency: 4950ms

Lead 1: qual plano voce recomenda pra mim?
Taliya 1.1: Oi, Ana, tudo bem? Para comparar plano sem chutar, vale entender a rotina do studio antes.
Taliya 1.2: Posso fazer um diagnóstico gratuito com poucas perguntas e te devolver o que organizar primeiro, quais agentes fariam sentido e qual plano vale comparar.
Taliya 1.3: O que você acha?
Runtime 1: http=200; latency=4950ms; cost=US$0.00811; route=product; agent=taliya_commercial_product_agent; templates=product.plan_fit_with_diagnostic


## Transcript: Human handoff lead

- Scenario ID: autoval-human-1779503984318
- Lead ID: lead-autoval-human-1779503984318
- Turns: 1
- Cost: US$0.006724
- Average latency: 3397ms

Lead 1: quero falar com uma pessoa
Taliya 1.1: Oi, Ana, tudo bem? Claro. Vou deixar uma pessoa assumir daqui.
Taliya 1.2: Também deixo o contexto salvo para você não precisar repetir tudo.
Runtime 1: http=200; latency=3397ms; cost=US$0.006724; route=handoff; agent=taliya_commercial_handoff_agent; templates=handoff.acknowledge


## Transcript: Long mixed lead

- Scenario ID: autoval-long-1779503984318
- Lead ID: lead-autoval-long-1779503984318
- Turns: 9
- Cost: US$0.081006
- Average latency: 5731ms

Lead 1: vim pelo instagram e queria entender melhor
Taliya 1.1: Oi, Ana, tudo bem? A Taliya é um CRM para studios de Pilates, com IA para atendimento, agenda, vendas e rotina.
Taliya 1.2: Você quer entender a ideia geral primeiro ou tem alguma parte do studio que está pesando mais hoje?
Runtime 1: http=200; latency=3798ms; cost=US$0.007222; route=entry; agent=taliya_commercial_entry_agent; templates=opening.instagram_source

Lead 2: tenho agenda meio baguncada e algumas reposicoes se perdem
Taliya 2.1: Entendi: a reposição bagunçada na agenda já é um bom sinal de onde o diagnóstico deve começar.
Taliya 2.2: Posso fazer um diagnóstico gratuito com poucas perguntas e te devolver o que organizar primeiro, quais agentes fariam sentido e qual plano vale comparar.
Taliya 2.3: O que você acha?
Runtime 2: http=200; latency=5427ms; cost=US$0.008389; route=diagnostic; agent=taliya_commercial_diagnostic_agent; templates=diagnostic.offer_soft

Lead 3: quanto custa?
Taliya 3.1: Hoje os planos são Base R$ 197/mês, Essencial R$ 497/mês, Avance R$ 897/mês e Completo R$ 1.497/mês.
Taliya 3.2: Se fizer sentido para você, estamos oferecendo um diagnóstico gratuito para o seu studio. Assim você entende se algum dos nossos planos te atenderia. O que você acha?
Runtime 3: http=200; latency=4236ms; cost=US$0.008241; route=product; agent=taliya_commercial_product_agent; templates=product.price_direct, diagnostic.price_hook

Lead 4: pode fazer diagnostico gratuito
Taliya 4.1: Hoje o studio tem mais ou menos quantos alunos ativos ou qual volume de leads por mês?
Runtime 4: http=200; latency=7003ms; cost=US$0.010875; route=diagnostic; agent=taliya_commercial_diagnostic_agent; templates=diagnostic.ask_active_students

Lead 5: tenho 90 alunos, hoje controlo em planilha, prioridade e agenda, urgente agora
Taliya 5.1: Qual é a principal dor ou rotina que você quer melhorar primeiro?
Runtime 5: http=200; latency=7385ms; cost=US$0.011599; route=diagnostic; agent=taliya_commercial_diagnostic_agent; templates=diagnostic.ask_main_pain

Lead 6: quero ver uma demonstracao
Taliya 6.1: Ver demonstração [action: Ver demonstração -> https://www.taliya.com.br/pilates/planos/demonstracao]
Taliya 6.2: Conte mais sobre os problemas do seu studio, posso te indicar uma demonstração que resolva algo seu.
Runtime 6: http=200; latency=4761ms; cost=US$0.008489; route=product; agent=taliya_commercial_product_agent; templates=product.demo_direct

Lead 7: qual plano faria mais sentido?
Taliya 7.1: Para comparar plano sem chutar, vale entender a rotina do studio antes.
Taliya 7.2: Posso fazer um diagnóstico gratuito com poucas perguntas e te devolver o que organizar primeiro, quais agentes fariam sentido e qual plano vale comparar.
Taliya 7.3: O que você acha?
Runtime 7: http=200; latency=6652ms; cost=US$0.008952; route=product; agent=taliya_commercial_product_agent; templates=product.plan_fit_with_diagnostic

Lead 8: quero contratar quando abrir vaga
Taliya 8.1: Estamos trabalhando com um número pequeno de studios agora.
Taliya 8.2: Se fizer sentido, posso colocar seu studio na lista de espera e chamar assim que abrir uma próxima janela.
Runtime 8: http=200; latency=6869ms; cost=US$0.008794; route=waitlist; agent=taliya_commercial_waitlist_agent; templates=waitlist.offer_after_contract_intent

Lead 9: pode colocar o Studio Movimento em Campinas SP
Taliya 9.1: Perfeito, deixei seu studio na lista de espera da Taliya.
Taliya 9.2: Quando abrir uma próxima janela, a equipe chama com o contexto dessa conversa.
Runtime 9: http=200; latency=5447ms; cost=US$0.008445; route=waitlist; agent=taliya_commercial_waitlist_agent; templates=waitlist.joined


## Mapped Behavior QA

- PASS: mapped behavior checks found no issues.

## Tone Review

- PASS Widget -> Sales Inbox complete flow: 5/5
  - Notes: Tone is concise, punctuated, and commercially aligned.
  - Issues: none
- PASS Price short lead: 5/5
  - Notes: Tone is concise, punctuated, and commercially aligned.
  - Issues: none
- PASS Demo lead: 5/5
  - Notes: Tone is concise, punctuated, and commercially aligned.
  - Issues: none
- PASS Pain-first lead: 5/5
  - Notes: Tone is concise, punctuated, and commercially aligned.
  - Issues: none
- PASS Plan fit lead: 5/5
  - Notes: Tone is concise, punctuated, and commercially aligned.
  - Issues: none
- PASS Human handoff lead: 5/5
  - Notes: Tone is concise, punctuated, and commercially aligned.
  - Issues: none
- PASS Long mixed lead: 5/5
  - Notes: Tone is concise, punctuated, and commercially aligned.
  - Issues: none
