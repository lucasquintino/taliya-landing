# Taliya Agent - Inventario de Regras

Data: 2026-05-14

Base: `docs/taliya-agent-proposta-simplificacao.md`

## Matriz

| Arquivo | Regra/area | Acao | Motivo |
| --- | --- | --- | --- |
| `crm-diagnostic.ts` | Fluxo deterministico do diagnostico gratuito | manter | Ja e o nucleo mais previsivel do funil principal. |
| `crm-diagnostic.ts` | Interpretacao de respostas livres por etapa | manter | Resolve o problema de repetir perguntas e depender de sugestoes. |
| `context.ts` | Instrucao "responder duvida sem perder o rumo" | simplificar | Deve virar a regra central do prompt, sem varias regras comerciais concorrentes. |
| `context.ts` | Uso de `plan_recommendation` antes do diagnostico | simplificar | Hoje ainda permite recomendacao com "dor clara" ou "multiplas rotinas"; a proposta pede diagnostico antes de plano. |
| `sales-cadence.ts` | Objeções e duvidas humanas | manter | Protege tom consultivo e respostas a recepcionista, IA, integracao e preco. |
| `sales-cadence.ts` | Atalho de "sistema completo" para 7 Agentes | simplificar | Fala de plano cedo demais e duplica bloqueios de `conversion-gates.ts`. |
| `sales-cadence.ts` | Atalho de planos/comparativo antes do diagnostico | simplificar | Deve responder em alto nivel e puxar diagnostico, sem abrir conversao. |
| `sales-cadence.ts` | Atalho de dor conhecida + plano | simplificar | Pode indicar direcao de escopo, mas nao deve definir plano antes do diagnostico. |
| `conversion-gates.ts` | Bloqueio de checkout sem confirmacao | manter | Gate de seguranca comercial. |
| `conversion-gates.ts` | Demo indisponivel | manter | Evita prometer demo real quando nao existe. |
| `conversion-gates.ts` | Diagnostico antes de conversao fria | manter | Alinha com funil principal. |
| `conversion-gates.ts` | Regras que apenas removem `conversionPath` mas preservam copy de plano cedo | simplificar | O gate bloqueia o path, mas a mensagem ainda pode soar como recomendacao prematura. |
| `fallback.ts` | Guardrails e indisponibilidade | manter | Necessario para seguranca e resiliencia. |
| `fallback.ts` | Fallback de sistema completo e plano recomendado | simplificar | Deve voltar ao diagnostico, nao virar vendedor paralelo. |
| `fallback.ts` | Fallback de preco/planos | simplificar | Deve responder preco em alto nivel e pedir contexto. |
| `continuation.ts` | Acabamento quando falta pergunta | manter pequeno | Util, mas nao pode adicionar pergunta em respostas finais ou diagnostico. |
| `eval-ai-multiturn.mjs` | Expectativas de checkout/handoff cedo | atualizar eval | Algumas expectativas antigas conflitam com diagnostico antes de conversao. |
| `eval-ai-sales-humanization.mjs` | HUM-006 checkout imediato apos diagnostico incompleto | atualizar eval | Deve aceitar diagnostico/plan comparison antes de checkout quando faltam campos. |

## Decisao de implementacao

Implementar agora apenas:

1. alinhar `context.ts`;
2. trocar atalhos prematuros de plano em `sales-cadence.ts` por respostas consultivas;
3. alinhar fallback de plano/preco/sistema completo;
4. impedir `continuation.ts` de anexar perguntas em diagnostico final;
5. atualizar evals somente onde a expectativa antiga conflita com a proposta aprovada.
