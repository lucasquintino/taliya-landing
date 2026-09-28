# Handoff para nova conversa Codex - Taliya Landing + Agente

Data do handoff: 2026-05-14  
Repo: `C:\Users\lucas\agentes-landing-system`  
Branch atual de produção: `master`  
Último commit enviado: `f258be6 Fix diagnostic widget entry flow`

## Como retomar sem começar do zero

Na nova conversa, começar lendo nesta ordem:

1. `AGENTS.md`
2. `docs/conversation-handoff-2026-05-14.md`
3. `specs/002-floating-ai-sales-agent/spec.md`
4. `specs/002-floating-ai-sales-agent/plan.md`
5. `specs/002-floating-ai-sales-agent/tasks.md`
6. `specs/001-niche-landing-system/spec.md`
7. `docs/taliya-agent-flow-test-scenarios.md`
8. `docs/taliya-agent-flow-validation-matrix.md`
9. `docs/taliya-agent-flow-deep-map.md`
10. `docs/landing-agentes-pilates/source/README.md`

Regra mais importante: a frente visual/layout da `/pilates` está aprovada. Não redesenhar a landing. Mudanças futuras nela devem ser apenas integração, CTA, schema, tracking, acessibilidade, bugs responsivos ou wiring do agente.

## Estado atual em produção

Domínio e deploy:

- `taliya.com.br` está apontado para Vercel.
- Cloudflare está no meio como DNS/proxy.
- Vercel validou `taliya.com.br` e `www.taliya.com.br`.
- Deploy recente publicado a partir do commit `f258be6`.

Agente/widget:

- O widget flutuante existe na landing `/pilates`.
- Desktop deve mostrar o widget em modo pill completo.
- Mobile deve mostrar somente o ícone/mensagem compacto.
- Chat abre com botão de fechar.
- O agente usa OpenAI quando `OPENAI_API_KEY` está configurada.
- A chave antiga vazou em conversa e já foi trocada pelo usuário.
- O fluxo determinístico de diagnóstico CRM/agentes existe em `lib/landing/ai-attendant/crm-diagnostic.ts`.
- O diagnóstico gratuito virou o funil principal do agente.

Lead pipeline:

- Existe n8n Cloud em `taliyan8n.app.n8n.cloud`.
- Workflow existente: `Taliya - Lead Upsert`.
- Webhook usado: `https://taliyan8n.app.n8n.cloud/webhook/taliya/lead-upsert`.
- Airtable base foi criada e integrada via n8n para receber leads.
- Não colocar segredos no repo. Usar Vercel envs.

Última validação feita:

- `npm run lint` passou.
- `npx tsc --noEmit` passou.
- `npm run build` passou.
- Teste local API do diagnóstico passou.
- Teste em produção confirmou que a nova versão já estava ativa.

## Últimas correções feitas

Commit `f258be6 Fix diagnostic widget entry flow`:

- O widget abre com duas mensagens:
  - `Oi. Estou aqui pra te acompanhar e responder duvidas sobre a Taliya.`
  - `Se fizer sentido pra voce, podemos fazer um diagnostico gratuito do seu studio. O que voce acha?`
- Sugestão inicial: `Quero fazer diagnostico gratuito`.
- Se o usuário clicar/escrever algo que remeta a diagnóstico, força `start_crm_diagnostic`.
- Clicar em `Fazer diagnóstico gratuito` na landing envia uma mensagem real ao chat.
- Corrigido bug em que `Quero fazer diagnostico gratuito` virava nome/dor/objetivo do lead.
- Ajustada animação do widget para não sumir depois da primeira cutucada.
- Ajustada sugestão dinâmica para acompanhar melhor a pergunta atual do diagnóstico.

## Arquivos principais do agente

Frontend/widget:

- `components/landing/shared/FloatingAiAttendant.tsx`
- `components/landing/shared/FloatingAiAttendantButton.tsx`
- `components/landing/shared/FloatingAiAttendantPanel.tsx`
- `components/landing/NicheLandingPage.tsx`
- `app/globals.css`

Backend/agente:

- `app/api/landing/ai-attendant/route.ts`
- `app/api/landing/ai-attendant/whatsapp/route.ts`
- `lib/landing/floating-agent.ts`
- `lib/landing/ai-attendant/provider.ts`
- `lib/landing/ai-attendant/crm-diagnostic.ts`
- `lib/landing/ai-attendant/conversion-gates.ts`
- `lib/landing/ai-attendant/sales-cadence.ts`
- `lib/landing/ai-attendant/leads.ts`
- `lib/landing/ai-attendant/n8n.ts`
- `lib/landing/ai-attendant/sales-inbox-store.ts`

Config comercial:

- `data/landing/niches/pilates.ts`
- `data/landing/niches/types.ts`

Página de planos:

- `app/pilates/planos`
- Ainda precisa de uma rodada futura de copy/polish, mas não era a prioridade final desta conversa.

## Decisões de negócio já travadas

Landing:

- A landing `/pilates` não é mais só validação de nicho. Ela vende o SaaS vertical Taliya para studios de Pilates.
- Estratégia principal: não jogar o lead direto em planos caros.
- O caminho preferido é diagnóstico gratuito → recomendação → demo/planos/WhatsApp/assinatura.
- O botão `Falar com consultor`, o widget e o WhatsApp devem alimentar o mesmo funil comercial.

Planos:

- Organização por número de agentes: Base sem agentes, 1 agente, 3 agentes, 7 agentes.
- Plano Base = CRM sem agentes.
- 7 agentes é o plano recomendado/completo, salvo se config mudar.
- Agente sob medida não entra em nenhum plano.
- Over-limit não deixa estourar cota: upgrade ou compra de cota.
- WhatsApp do studio será o próprio WhatsApp do studio.
- O agente vendedor da Taliya usa o WhatsApp próprio da Taliya.
- Sem multi-unidade no começo.
- Sem trial gratuito.
- Cancelamento/reembolso: 30 dias de garantia.
- Setup: self-guided com agente de IA.
- Suporte: 24/7 com agente de IA.
- Implantação: poucos minutos para todos.
- Existe caso especial de piloto privado gratuito para um studio de Pilates, cobrando apenas custo operacional, tratado pessoalmente pelo usuário.

Agente do site:

- Deve conversar como vendedor humano, com cadência.
- Não deve ser agressivo.
- Não deve despejar preço/plano cedo.
- Deve cumprimentar, se apresentar, perguntar com quem fala e conduzir por etapas.
- Função principal agora: oferecer/fazer diagnóstico gratuito.
- Deve responder dúvidas, objeções e caminhos paralelos, mas puxar de volta para diagnóstico quando fizer sentido.
- Deve pedir contato cedo quando houver mínimo interesse.
- Deve registrar lead.
- Deve preservar intenção do usuário: planos, demo, humano, WhatsApp, agente sob medida, preço, objeção etc.

Perguntas do diagnóstico gratuito:

- Nome: `Boa. Antes de eu montar o diagnóstico: com quem eu falo?`
- Contato: pedir WhatsApp ou email para salvar o diagnóstico, permitindo continuar se preferir.
- Tamanho: quantos alunos ativos aproximadamente.
- Dores: pergunta abrangente sobre WhatsApp, agenda/reposições, vendas, financeiro, acompanhamento/gestão.
- Visão do dia: `Hoje você consegue ver facilmente o que precisa ser resolvido no dia?`
- Reposições: se aparecem como dor, perguntar se são fáceis ou viram troca de mensagem.
- Vendas: se aparecem como dor, perguntar se conseguem acompanhar interessado até virar aluno.
- Sistema atual: perguntar se fica em sistema ou WhatsApp/planilha/caderno.
- Objetivo: o que tiraria da mão primeiro este mês.
- Temperatura: se estão buscando resolver agora ou só pesquisando.

Diagnóstico final esperado:

- Identificar dores reais do studio.
- Explicar como o CRM Taliya organiza a operação.
- Explicar quais agentes resolvem aquelas dores.
- Recomendar o plano compatível.
- Só então mostrar CTAs adequados: ver planos, demo guiada quando existir, continuar no WhatsApp/humano, ou assinatura após confirmação clara.

## Pontos pendentes importantes

P0/P1 para próxima conversa:

1. Rodar teste manual completo do widget em produção:
   - abrir pelo widget normal;
   - clicar na sugestão `Quero fazer diagnostico gratuito`;
   - clicar no CTA `Fazer diagnóstico gratuito` antes de abrir chat;
   - abrir chat antes e depois clicar no CTA;
   - confirmar que o roteiro não duplica mensagens nem entra em loop.
2. Validar visual da animação do widget em produção:
   - desktop largo;
   - desktop com DPR 1.25;
   - mobile;
   - confirmar que ele cutuca sem sumir.
3. Calibrar o texto do agente com conversas reais:
   - tom humano;
   - mensagens curtas;
   - sem termos técnicos;
   - sem pressão de venda precoce;
   - resposta direta + gancho para diagnóstico.
4. Validar que lead vai para Airtable/n8n em cenário real:
   - diagnóstico completo;
   - pedido de WhatsApp;
   - pedido de humano;
   - lead quente.
5. Revisar página `/pilates/planos` futuramente:
   - menos poluição;
   - cards vendendo melhor;
   - incluir CRM web, Taliya App, WhatsApp, sistema e 7 agentes;
   - CTAs focados em assinatura e demo;
   - apenas um lugar para voltar ao consultor;
   - seção de agente sob medida igual home.

## Ajustes mapeados pelo usuário antes da migração

Esses pontos foram encontrados em teste real do widget/agente e devem ser tratados na próxima conversa antes de considerar o diagnóstico 100%.

### Widget e animação

- A animação do widget não pode aumentar largura/altura do componente e depois voltar ao tamanho normal.
- A animação deve ser fluida e sutil: pulso, pequeno pulo, badge de notificação ou cutucada visual.
- O widget não pode sumir nem reentrar de forma estranha depois da animação.
- Validar em desktop normal, desktop com DPR 1.25 e mobile.

### Interpretação das respostas do diagnóstico

- O agente repetiu a pergunta `Hoje você consegue ver facilmente o que precisa ser resolvido no dia?` mesmo depois de respostas como:
  - `tenho tudo num caderno anotado`
  - `sim`
  - `nao`
- O agente só avançou quando o usuário clicou na sugestão pronta. Isso está errado.
- O agente deve interpretar respostas livres equivalentes, não depender apenas de sugestões/quick replies.
- Essa regra vale para todas as perguntas do diagnóstico.

Também ocorreu bug na pergunta:

```text
Quais partes mais dão trabalho hoje: WhatsApp, agenda/reposições, vendas, financeiro ou acompanhamento dos alunos?
```

Resposta do usuário:

```text
n consigo vender bem meu studio
```

Resultado errado:

- O agente repetiu a mesma pergunta.
- Mesmo repetindo a resposta, ficou preso nessa etapa.

Resultado esperado:

- Interpretar como dor de vendas/interessados.
- Marcar dor correspondente.
- Humanizar a resposta.
- Avançar para a próxima pergunta do diagnóstico.

### Sugestões de próxima mensagem

- Na pergunta `Pra deixar esse diagnóstico salvo para você, Lucas, me passa um WhatsApp ou email? Se preferir, eu continuo mesmo assim, tudo bem?`, a sugestão apareceu como `Responder meu nome`. Está errado.
- Para pergunta de contato, sugestão deve ser algo como `Deixar meu WhatsApp` ou preencher input com `Meu WhatsApp é `.
- Na pergunta sobre dores, a sugestão estava sugerindo deixar WhatsApp, o que não condiz com a etapa.
- A sugestão deve sempre acompanhar a pergunta atual e o estado real do diagnóstico.

### Ritmo e humanização

- O ritmo atual está apressado.
- As mensagens podem ter delay maior.
- O fluxo está parecendo entrevista mecânica: agente pergunta, usuário responde, agente já joga outra pergunta.
- O comportamento esperado:
  1. agente faz uma pergunta;
  2. usuário responde;
  3. agente manda uma primeira mensagem curta reconhecendo a resposta de forma humana;
  4. depois emenda com outra mensagem curta contendo a próxima pergunta.
- Exemplo de padrão:
  - Usuário: `n consigo vender bem meu studio`
  - Agente msg 1: `Entendi. Quando a venda fica solta, muita gente interessada acaba esfriando antes de marcar uma aula.`
  - Agente msg 2: `Hoje você consegue ver facilmente o que precisa resolver no dia?`

### Geração do diagnóstico final

- O diagnóstico final deve parecer que levou tempo para ser montado.
- Quando o agente tiver as informações necessárias, deve dizer algo como:

```text
Ok, já tenho as informações necessárias para montar seu diagnóstico. Já te retorno.
```

- Depois disso, deve haver um delay maior.
- O diagnóstico deve sair por etapas, não tudo seco de uma vez.

Mensagem final 1 aprovada pelo usuário como boa:

```text
Pelo que você contou, o gargalo principal está em WhatsApp, reposições, faltas, vendas e interessados e gestão do dia. Antes de pensar em agente, a Taliya precisa organizar isso no CRM: alunos, conversas, agenda, financeiro e prioridades do dia no mesmo lugar.
```

Mensagem final 2 teve partes boas, mas precisa melhorar:

```text
Minha recomendação é começar olhando cadastro de alunos, histórico de conversas, agenda e presença, pipeline de interessados e painel do dia. Em cima disso, os agentes mais úteis seriam Atendimento, Agenda, Vendas e Gestão. Na prática, o CRM mostra prioridades e os agentes ajudam a agir. Pelo tamanho e momento do studio, eu compararia o 7 Agentes com calma, sem pular direto para assinatura. Quer que eu te mostre os planos já com essa recomendação?
```

Feedback do usuário:

- A recomendação precisa ser dinâmica conforme o diagnóstico.
- A parte depois de `Em cima disso...` ficou boa.
- Evitar recomendação genérica ou sempre empurrar o mesmo plano sem explicar o porquê.

### Agentes indicados no diagnóstico

- A seção/listagem `Agentes indicados` está feia e pouco funcional.
- Em vez de um bloco genérico, deve listar os agentes indicados um por vez.
- Para cada agente indicado, explicar:
  - qual dor ele resolve;
  - por que ele foi recomendado para aquele studio;
  - como ele atua na prática.
- Exemplo esperado:
  - `Atendimento`: resolve WhatsApp bagunçado e dúvidas repetidas.
  - `Agenda`: resolve reposições, faltas e encaixes.
  - `Vendas`: resolve perda de interessados e follow-up fraco.
  - `Gestão`: resolve falta de clareza do que precisa ser feito no dia.

## Estado do worktree

Depois do commit `f258be6`, ainda existem muitas alterações não commitadas em `specs/006-crm-operational-core/*`. Elas são da outra frente de conversa/sistema real.

Na próxima conversa:

- Não reverter essas mudanças.
- Não misturar essas mudanças com commits da landing/agente.
- Antes de commitar algo, usar `git status --short`.
- Se trabalhar na landing/agente, stagear apenas arquivos tocados nessa frente.

## Comandos úteis

Rodar local:

```powershell
npm run dev
```

Build/validação:

```powershell
npm run lint
npx tsc --noEmit
npm run build
```

Evals existentes:

```powershell
npm run eval:ai-routes
npm run eval:ai-multiturn
npm run eval:ai-sales-humanization
npm run eval:lead-pipeline
npm run eval:custom-diagnostic
npm run eval:whatsapp-webhook
```

## Prompt recomendado para abrir a nova conversa

Use este texto:

```text
Estamos migrando de uma conversa longa. Leia primeiro:
- AGENTS.md
- docs/conversation-handoff-2026-05-14.md
- specs/002-floating-ai-sales-agent/spec.md
- specs/002-floating-ai-sales-agent/plan.md
- specs/002-floating-ai-sales-agent/tasks.md
- specs/001-niche-landing-system/spec.md
- docs/taliya-agent-flow-test-scenarios.md
- docs/taliya-agent-flow-validation-matrix.md

Contexto: a landing /pilates está visualmente aprovada e protegida. Não redesenhar. O funil principal do widget/agente é diagnóstico gratuito consultivo, com tom humano e sem agressividade. O último commit em produção é f258be6. Existem muitas mudanças não commitadas em specs/006 da outra frente; não reverter nem misturar.

Primeira tarefa: confirmar o estado atual do widget/agente em produção e continuar a partir dos P0/P1 listados no handoff, sem começar do zero.
```
