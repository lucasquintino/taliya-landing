# Taliya Agent - Proposta e Simplificacao Cirurgica

Data: 2026-05-14

## Objetivo

Este documento recapitula a proposta atual do agente da Taliya e organiza uma revisao de complexidade sem "terra arrasada".

A intencao nao e reescrever o agente do zero. A intencao e preservar o que ja funciona, tirar regras redundantes quando elas atrapalham, e deixar o fluxo principal mais previsivel.

## Proposta do Agente

O agente e um vendedor consultivo da Taliya para studios de Pilates.

Ele nao e suporte generico, chatbot passivo de FAQ, nem comparador de planos logo de cara.

O objetivo principal e conduzir um diagnostico gratuito curto, humano e util, para entender a rotina do studio e so depois recomendar CRM, agentes e plano.

Ao mesmo tempo, ele deve conseguir tirar duvidas do cliente sempre que necessario. Quando a pessoa pergunta algo, o agente responde com clareza primeiro, sem fugir da pergunta. Depois conecta a resposta com a rotina do studio e, se fizer sentido, volta suavemente para o diagnostico.

Regra central:

> Responder a duvida sem perder o rumo.

## Comportamento Esperado

1. Recebe a pessoa de forma natural.
2. Se a pessoa trouxe uma duvida, responde primeiro.
3. Conecta a resposta com a realidade de um studio de Pilates.
4. Oferece ou continua o diagnostico gratuito como caminho principal.
5. Faz uma pergunta por vez.
6. Reconhece a resposta antes de fazer a proxima pergunta.
7. Interpreta respostas livres, sem depender de sugestoes clicaveis.
8. Coleta nome e contato de forma leve, sem travar se a pessoa preferir continuar sem contato.
9. Entende tamanho do studio, dores, visao do dia, sistema atual, prioridade e momento.
10. Faz perguntas adaptativas apenas quando a dor pede.
11. Antes do resultado, sinaliza que ja tem informacoes suficientes e demora um pouco.
12. Entrega o diagnostico final em etapas.
13. Recomenda CRM primeiro, agentes depois, plano por ultimo.
14. Lista agentes indicados um por vez, explicando dor, motivo e atuacao pratica.
15. So depois do diagnostico oferece comparar planos, continuar pelo WhatsApp, demo ou proximo passo comercial.

## Regras Essenciais

- Responder duvidas do cliente primeiro.
- Voltar para o diagnostico sem soar mecanico ou insistente.
- Nao empurrar plano antes do diagnostico.
- Nao abrir checkout antes de um plano recomendado e confirmado.
- Nao repetir pergunta quando a resposta livre ja foi interpretada.
- Uma pergunta por vez.
- Toda pergunta importante deve ter um reconhecimento anterior quando houver resposta do cliente.
- Nao inventar integracao, garantia, suporte, resultado ou funcionalidade.
- Quando houver incerteza tecnica, dizer que precisa confirmar.
- Diagnostico final deve parecer pensado, nao instantaneo.

## Fluxo Base

### 1. Entrada

O agente abre com recepcao simples e convite para diagnostico gratuito.

Se a pessoa ja chega perguntando algo, ele responde a duvida e usa a resposta como ponte para o diagnostico.

### 2. Diagnostico

Campos principais:

- Nome.
- WhatsApp ou email, opcional.
- Quantidade aproximada de alunos ativos.
- Partes que mais dao trabalho.
- Visao do que precisa ser resolvido no dia.
- Perguntas adaptativas por dor:
  - reposicoes/faltas;
  - vendas/interessados;
  - financeiro;
  - acompanhamento/retencao;
  - historico/evolucao.
- Sistema atual.
- Prioridade principal.
- Momento: resolver agora ou pesquisando.

### 3. Resultado

O resultado deve sair em etapas:

1. "Ok, ja tenho as informacoes necessarias para montar seu diagnostico. Ja te retorno."
2. Gargalo principal.
3. Base de CRM recomendada.
4. Agentes indicados.
5. Proximo passo.

### 4. Recomendacao

Ordem correta:

1. Primeiro: o que precisa ser organizado no CRM.
2. Depois: quais agentes ajudam.
3. Por ultimo: qual plano comparar.

O plano nao deve aparecer como a resposta principal antes de explicar a operacao.

## Principio de Simplificacao

Antes de remover qualquer regra, perguntar:

- Essa regra protege contra um risco real atual?
- Essa regra duplica uma regra mais central?
- Essa regra esta corrigindo sintoma de outro modulo?
- Essa regra faz o agente parecer mais humano ou mais travado?
- Essa regra ainda combina com "responder a duvida sem perder o rumo"?

Se a regra protege seguranca, privacidade, checkout, dados sensiveis ou promessas falsas, tende a ficar.

Se a regra existe apenas para empurrar ou bloquear CTA em muitos cenarios parecidos, pode virar candidata a simplificacao.

## Auditoria Leve do Codigo Atual

### `lib/landing/ai-attendant/crm-diagnostic.ts`

Papel atual:

- Deve ser o nucleo deterministico do diagnostico gratuito.
- Hoje ja contem a maior parte do fluxo aprovado: perguntas, extracao de respostas livres, feedback, perfil, diagnostico final e agentes recomendados.

Tendencia:

- Manter como fonte principal do fluxo de diagnostico.
- Simplificar aos poucos apenas se houver duplicacao clara.
- Evitar espalhar logica de diagnostico para outros arquivos.

### `lib/landing/ai-attendant/context.ts`

Papel atual:

- Instrui o modelo quando o fluxo nao cai no diagnostico deterministico.
- Define tom, regras comerciais e uso de `conversionPath`.

Tendencia:

- Atualizar para refletir a proposta final do agente em linguagem curta.
- Remover instrucoes redundantes se elas ja estiverem garantidas por codigo deterministico.
- Manter regras de duvidas, honestidade e nao inventar informacao.

### `lib/landing/ai-attendant/sales-cadence.ts`

Papel atual:

- Tenta deixar a venda mais humana e evitar atalhos agressivos.
- Tambem contem muitas correcoes de rota comercial.

Risco:

- Pode disputar com `crm-diagnostic.ts` e `conversion-gates.ts`.
- Pode estar segurando comportamentos antigos de plano/checkout.

Tendencia:

- Revisar caso a caso.
- Manter protecoes claras de cadencia humana.
- Remover ou reduzir regras que tentam recompor o diagnostico fora do nucleo principal.

### `lib/landing/ai-attendant/conversion-gates.ts`

Papel atual:

- Protege conversoes: planos, checkout, demo, WhatsApp, contato e diagnostico antes de conversao.

Risco:

- E o arquivo mais propenso a virar acumulador de excecoes.
- Muitas regras aqui podem significar que o fluxo anterior esta emitindo `conversionPath` cedo demais.

Tendencia:

- Manter gates de seguranca e negocio:
  - sem checkout antes de confirmacao;
  - sem demo se demo nao esta pronta;
  - sem plano antes do diagnostico quando o contexto e frio;
  - sem contato forçado.
- Simplificar gates que apenas corrigem saidas antigas do modelo.

### `lib/landing/ai-attendant/fallback.ts`

Papel atual:

- Respostas deterministicas quando IA falha ou quando alguns atalhos sao detectados.

Risco:

- Pode conter respostas comerciais antigas que recomendam plano antes da proposta atual.

Tendencia:

- Manter fallback de seguranca e disponibilidade.
- Alinhar respostas comerciais com o diagnostico gratuito.
- Evitar que fallback vire um segundo vendedor paralelo.

### `lib/landing/ai-attendant/continuation.ts`

Papel atual:

- Garante que a resposta nao termine seca e tente continuar a conversa.

Risco:

- Pode adicionar perguntas em cima de respostas que ja tinham proximo passo adequado.

Tendencia:

- Manter pequeno.
- Garantir que nao duplique pergunta do diagnostico.
- Usar apenas como acabamento, nao como regra central.

## O Que Nao Fazer Agora

- Nao redesenhar `/pilates`.
- Nao trocar o funil principal.
- Nao apagar arquivos grandes por impulso.
- Nao reescrever o agente inteiro.
- Nao mudar integrações, lead pipeline ou checkout sem necessidade.
- Nao atualizar evals para "passar" se eles ainda representam um risco real.

## Proximo Passo Recomendado

1. Revisar este documento e ajustar a proposta ate ficar 100% alinhada.
2. Fazer uma matriz curta por arquivo:
   - manter;
   - simplificar;
   - remover;
   - mover para `crm-diagnostic.ts`;
   - atualizar eval.
3. So depois escolher uma fatia pequena de implementacao.

Fatia sugerida para a primeira implementacao, se aprovada:

- Atualizar `context.ts` para refletir a proposta final.
- Auditar `sales-cadence.ts` e `conversion-gates.ts` procurando regras que duplicam o diagnostico.
- Rodar os roteiros reais do usuario e os evals antes/depois.
