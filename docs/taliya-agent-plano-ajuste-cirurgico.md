# Taliya Agent - Plano Concreto de Ajuste Cirurgico

Data: 2026-05-14

Documento base: `docs/taliya-agent-proposta-simplificacao.md`

## Objetivo

Ajustar apenas o necessario para deixar o agente mais simples, previsivel e alinhado com a proposta aprovada:

> Responder a duvida sem perder o rumo.

Nao e uma reescrita do agente. O trabalho deve preservar o diagnostico que ja esta funcionando e remover apenas complexidade que esteja duplicando, disputando ou atrapalhando o fluxo.

## Resultado Esperado

Ao final, o agente deve:

- responder duvidas do cliente primeiro;
- voltar para o diagnostico de forma natural;
- conduzir uma pergunta por vez;
- interpretar respostas livres sem depender de sugestoes;
- nao recomendar plano antes do diagnostico;
- entregar diagnostico final em etapas;
- recomendar CRM primeiro, agentes depois e plano por ultimo;
- manter checkout, demo, WhatsApp, seguranca e promessas falsas protegidos por gates claros.

## Escopo

Arquivos principais:

- `lib/landing/ai-attendant/context.ts`
- `lib/landing/ai-attendant/crm-diagnostic.ts`
- `lib/landing/ai-attendant/sales-cadence.ts`
- `lib/landing/ai-attendant/conversion-gates.ts`
- `lib/landing/ai-attendant/fallback.ts`
- `lib/landing/ai-attendant/continuation.ts`
- scripts/evals relacionados ao agente, se algum comportamento antigo estiver desalinhado com a proposta aprovada

Fora de escopo:

- redesign da landing `/pilates`;
- mudancas visuais na landing aprovada;
- reescrita completa do agente;
- mudancas em lead pipeline, n8n, external CRM/spreadsheet, checkout ou billing sem necessidade direta;
- mexer nas mudancas pendentes de `specs/006-crm-operational-core`.

## Ordem de Execucao

### Fase 1 - Inventario de Regras

Objetivo:

Mapear regras existentes que influenciam conversa, diagnostico e conversao.

Arquivos:

- `context.ts`
- `sales-cadence.ts`
- `conversion-gates.ts`
- `fallback.ts`
- `continuation.ts`
- `crm-diagnostic.ts`

Saida esperada:

Uma matriz curta com cada regra relevante classificada como:

- manter;
- simplificar;
- remover;
- mover para `crm-diagnostic.ts`;
- atualizar eval;
- investigar com roteiro real.

Criterios de aceite:

- nenhuma alteracao de runtime nessa fase;
- regras de seguranca/privacidade/checkout ficam marcadas como manter por padrao;
- regras que apenas corrigem sintomas comerciais antigos ficam marcadas como candidatas, nao removidas automaticamente.

### Fase 2 - Alinhar Prompt e Contexto

Objetivo:

Fazer o modelo receber uma instrucao mais simples e coerente com a proposta aprovada.

Arquivo principal:

- `lib/landing/ai-attendant/context.ts`

Ajustes provaveis:

- reduzir repeticao de instrucoes comerciais;
- explicitar a regra central: responder a duvida sem perder o rumo;
- reforcar que o diagnostico gratuito e o funil principal;
- reforcar que duvidas devem ser respondidas antes da proxima pergunta;
- deixar `conversionPath` mais restrito a momentos realmente maduros;
- remover instrucoes que incentivem recomendacao de plano cedo demais.

Criterios de aceite:

- pergunta simples de preco responde preco em alto nivel e volta para diagnostico;
- pergunta "o que e a Taliya?" responde claro e volta para contexto do studio;
- pergunta de integracao nao inventa;
- pergunta de recepcionista/IA/seguranca responde antes de diagnosticar;
- nao quebra o fluxo deterministico do diagnostico.

Testes minimos:

- `npm run lint`
- `npm run build`
- `npm run eval:ai-routes -- --target=http://localhost:3010`
- roteiros manuais:
  - "Quanto custa?"
  - "O que exatamente e a Taliya?"
  - "Tenho medo da IA responder errado."
  - "Integra com o sistema X?"

### Fase 3 - Reduzir Disputa Entre Cadencia e Gates

Objetivo:

Evitar que `sales-cadence.ts` e `conversion-gates.ts` fiquem corrigindo a mesma coisa de formas diferentes.

Arquivos:

- `lib/landing/ai-attendant/sales-cadence.ts`
- `lib/landing/ai-attendant/conversion-gates.ts`

Direcao:

- `sales-cadence.ts` deve cuidar de tom humano e cadencia comercial.
- `conversion-gates.ts` deve cuidar de permissao de conversao.
- nenhum dos dois deve recriar o diagnostico inteiro se `crm-diagnostic.ts` ja e a fonte principal.

Manter em `conversion-gates.ts`:

- bloquear checkout sem confirmacao clara;
- bloquear demo quando demo nao esta pronta;
- evitar plano/checkout antes do diagnostico quando contexto e frio;
- garantir contato quando houver handoff que precisa de retorno;
- proteger custom agent e integracoes incertas.

Manter em `sales-cadence.ts`:

- evitar tom agressivo;
- transformar atalhos de venda em conversa consultiva;
- responder objecoes de forma humana;
- impedir "empurrar assinatura" cedo demais.

Candidatos a simplificacao:

- regras repetidas de plano cedo demais nos dois arquivos;
- mensagens que falam de comparativo/plano antes do diagnostico;
- regras que tentam inferir diagnostico fora de `crm-diagnostic.ts`;
- excecoes criadas para um caso especifico que hoje ja e coberto pelo fluxo principal.

Criterios de aceite:

- pedido amplo com varias dores nao vira `plan_recommendation` antes do diagnostico;
- pedido direto de planos recebe explicacao curta e volta para diagnostico;
- pedido de checkout so avanca depois de plano recomendado e confirmado;
- duvida comercial nao fica presa em pergunta sem responder.

Testes minimos:

- `npm run eval:ai-routes -- --target=http://localhost:3010`
- `npm run eval:ai-sales-humanization -- --target=http://localhost:3010`
- `npm run eval:ai-multiturn -- --target=http://localhost:3010`

Observacao:

Falhas antigas dos evals devem ser analisadas antes de alterar comportamento. Se o eval espera checkout/handoff cedo e isso conflita com a proposta aprovada, marcar como `atualizar eval`, nao forcar o agente a voltar ao comportamento antigo.

### Fase 4 - Alinhar Fallback

Objetivo:

Garantir que fallback nao vire um vendedor paralelo com regras antigas.

Arquivo:

- `lib/landing/ai-attendant/fallback.ts`

Ajustes provaveis:

- respostas de preco, plano e sistema completo devem responder e voltar para diagnostico;
- fallback nao deve recomendar plano completo antes do diagnostico;
- fallback deve preservar honestidade sobre demo, integracoes e funcionalidades nao confirmadas;
- fallback deve ser curto, util e seguro.

Criterios de aceite:

- com provider indisponivel, o agente ainda conduz diagnostico sem pular para plano;
- respostas fallback nao contradizem `context.ts` nem `crm-diagnostic.ts`;
- fallback mantem tom consultivo.

Testes minimos:

- rodar roteiros com mock/fallback se houver flag local disponivel;
- `npm run eval:ai-routes -- --target=http://localhost:3010`

### Fase 5 - Ajustar Continuacao

Objetivo:

Manter `continuation.ts` como acabamento, nao como motor do fluxo.

Arquivo:

- `lib/landing/ai-attendant/continuation.ts`

Ajustes provaveis:

- impedir pergunta duplicada quando a resposta ja tem `nextQuestion`;
- evitar adicionar CTA/pergunta depois de diagnostico final bem formado;
- manter apenas continuacoes neutras para respostas secas.

Criterios de aceite:

- diagnostico nao recebe pergunta duplicada;
- respostas de duvida terminam com uma pergunta natural;
- respostas finais com CTA claro nao ganham frase extra desnecessaria.

### Fase 6 - Evals e Roteiros Reais

Objetivo:

Separar regressao real de expectativa antiga.

Roteiros obrigatorios:

1. Diagnostico com resposta livre:
   - "Meu nome e Lucas"
   - "Meu WhatsApp e 27996991427"
   - "50"
   - "n consigo vender bem meu studio"
   - "consigo sim, por meio de anotacoes no caderno"
   - "geralmente sim, mas toma tempo"
   - "uso mais caderno e whatsapp"
   - "quero vender melhor sem perder interessado"
   - "depois"

2. Duvida antes de diagnostico:
   - "Quanto custa?"
   - "O que exatamente e a Taliya?"
   - "Ja tenho recepcionista. Por que eu precisaria disso?"
   - "Tenho medo da IA responder errado."
   - "Integra com o sistema X?"

3. Conversao madura:
   - completar diagnostico;
   - pedir para comparar planos;
   - pedir link apenas depois de recomendacao.

Comandos:

```bash
npx tsc --noEmit
npm run lint
npm run build
npm run eval:ai-routes -- --target=http://localhost:3010
npm run eval:ai-sales-humanization -- --target=http://localhost:3010
npm run eval:ai-multiturn -- --target=http://localhost:3010
```

Criterios de aceite:

- `tsc`, lint e build passam;
- route matrix deve passar ou ter falha justificada por expectativa antiga;
- humanization e multiturn devem melhorar ou ter lista clara de falhas restantes;
- roteiro real do usuario nao repete perguntas e nao pula diagnostico;
- nenhuma mudanca em `/pilates` visual.

## Plano de Commits

Preferir commits pequenos:

1. `Document agent simplification plan`
2. `Align AI attendant context with diagnostic proposal`
3. `Simplify sales cadence and conversion gates`
4. `Align fallback and continuation behavior`
5. `Update agent eval expectations`

Se uma fase ficar pequena, pode juntar. Se tocar comportamento sensivel, manter separado.

## Riscos

- Remover regra que ainda protegia checkout cedo.
- Deixar o modelo responder duvidas mas esquecer de voltar ao diagnostico.
- Atualizar eval errado para mascarar regressao real.
- Duplicar perguntas entre `crm-diagnostic.ts` e `continuation.ts`.
- Fallback antigo contradizer fluxo novo quando provider falhar.

## Sequencia Recomendada Agora

1. Criar matriz de regras por arquivo.
2. Revisar matriz com o usuario.
3. Implementar Fase 2 primeiro (`context.ts`), por ser menor e de menor risco.
4. Rodar roteiros reais.
5. So entao simplificar `sales-cadence.ts` e `conversion-gates.ts`.
