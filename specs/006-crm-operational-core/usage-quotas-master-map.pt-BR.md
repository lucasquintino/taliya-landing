# Taliya CRM - Mapa Mestre De Uso E Cotas

Status: mapa mestre v1.
Data: 2026-05-25.

## Objetivo

Definir Uso/Cotas como a camada que mostra consumo real, previsao, alertas, economia e bloqueios de automacao paga.

Uso/Cotas nao e:

- Billing Taliya;
- pagina de compra de add-on;
- configuracao de fluxo;
- relatorio financeiro;
- log tecnico de integracao;
- auditoria completa.

Uso/Cotas responde:

- quanto o studio consumiu neste ciclo?
- quanto ainda resta?
- qual origem consumiu mais?
- algum fluxo foi downgradado, bloqueado ou virou tarefa?
- estamos perto de 70%, 90% ou 100%?
- o que continua manual quando a cota acaba?
- onde ver o detalhe de cada lancamento?

## Decisao MVP

Uso/Cotas tera **2 paginas**:

1. `/app/uso`
   - visao geral de consumo, cotas, alertas e economia.
2. `/app/uso/extrato`
   - extrato detalhado e auditavel dos lancamentos de uso.

## Rotas Absorvidas Ou Removidas

| Rota antiga | Decisao MVP | Onde fica |
|---|---|---|
| `/app/uso/cotas` | Removida como pagina propria | Dentro de `/app/uso` |
| `/app/uso/custos` | Removida como pagina propria | Origem do consumo em `/app/uso` e `/app/uso/extrato` |
| `/app/uso/alertas` | Removida como pagina propria | Dentro de `/app/uso` |
| `/app/uso/pacotes` | Removida | Add-ons ficam em `/app/billing/add-ons` |
| `/app/uso/regras-economia` | Removida como pagina propria | Comportamento de economia fica em `/app/uso` |
| `/app/uso/limites-fluxo` | Removida | Limites ficam em Agentes/Fluxos |
| `/app/uso/limites-fluxo/[flowId]` | Removida | Limite do fluxo fica na pagina do fluxo |

## 1. `/app/uso` - Visao Geral

### Para Que Serve

Mostrar rapidamente se o studio esta operando dentro da cota, perto de limite ou com automacoes degradadas.

### Imagem Aprovada

Referencia visual aprovada:

- `68_round-4.1O_uso_01_visao-geral-aprovado.png`

Estado representado na imagem:

- plano 7 agentes;
- 15.000 mensagens/mes;
- 6.300 usadas;
- 8.700 restantes;
- 42% usado;
- status `Normal`;
- proximo alerta em 70%;
- nenhuma automacao pausada por cota;
- nenhum downgrade ativo.

Ajustes obrigatorios para implementacao:

- `Ver extrato` e o CTA principal no estado normal.
- `Ver add-ons` aparece como acao secundaria no estado normal e so ganha destaque quando houver alerta alto, cota esgotada ou add-on recomendado.
- O icone do card principal deve comunicar uso/cota de forma neutra, sem parecer que a cota e apenas de chat.
- O painel do Agente de Suporte Taliya deve dizer `Plano, faturas e add-ons ficam em Billing`, nao `pacotes`.

### O Que Tem

- cota contratada do ciclo;
- cota usada;
- cota restante;
- percentual usado;
- previsao ate o fim do ciclo;
- status:
  - `Normal`;
  - `Alerta 70%`;
  - `Economia 90%`;
  - `Cota esgotada`;
  - `Add-on extra ativo`;
- principais origens de consumo:
  - IA;
  - WhatsApp service;
  - WhatsApp utility;
  - WhatsApp marketing;
  - batch job;
  - midia;
  - historico;
- consumo por agente/area, de forma resumida;
- alertas 70/90/100;
- lista curta de downgrades/bloqueios recentes;
- explicacao do que continua manual;
- CTA `Ver extrato`;
- CTA `Ver add-ons`, quando precisar de add-on;
- CTA para abrir fluxo afetado, quando o bloqueio vier de fluxo.

### O Que Nao Tem

- contratacao completa de add-on;
- plano contratado e fatura completa;
- configuracao fina de fluxo;
- tabela gigante de eventos;
- logs tecnicos;
- billing interno;
- grafico pesado;
- configuracao de todos os limites dos 96 fluxos.

### Regras

- Billing define o direito contratado.
- Uso/Cotas mostra o consumo e a consequencia operacional.
- Agentes/Fluxos define limite e comportamento por fluxo.
- Manual CRM continua funcionando quando cota acaba.
- Em uso normal, a pagina nao deve empurrar compra de add-on como acao principal.
- Quando bater 90% ou 100%, a pagina pode destacar `Ver add-ons` ou `Abrir chamado`, conforme o estado de billing.

## 2. `/app/uso/extrato` - Extrato

### Para Que Serve

Mostrar cada lancamento de uso de forma rastreavel.

### Imagem Aprovada

Referencia visual aprovada:

- `69_round-4.1O_uso_02_extrato-aprovado.png`

Estado representado na imagem:

- ciclo atual;
- 42% usado;
- 15.000 mensagens/mes;
- filtros por periodo, agente, origem e status;
- tabela de lancamentos com `Quando`, `Origem`, `Agente / fluxo`, `Caso`, `Uso`, `Status` e `Acao`;
- painel lateral com Agente de Suporte Taliya.

Ajustes obrigatorios para implementacao:

- O chip de cota deve usar icone neutro de uso/cota, nao icone que faca parecer consumo apenas de chat.
- O status deve ser padronizado como `Estimado`, nao `Estimada`.
- A coluna `Origem` deve aceitar, no contrato, `IA`, `WhatsApp`, `Sistema`, `Batch`, `Midia` e `Historico`.
- `Abrir execucao` leva para `/app/fluxos/execucoes/[runId]`.
- `Abrir conversa`, `Abrir caso`, `Abrir cobranca` e `Abrir aprovacao` levam para os objetos operacionais correspondentes.
- A pagina nao deve mostrar payload bruto, custo interno do provedor nem detalhes tecnicos de integracao.

### O Que Tem

- lista/tabela de lancamentos;
- filtros simples:
  - periodo;
  - agente;
  - fluxo;
  - origem;
  - status;
- data/hora;
- origem do consumo;
- agente/fluxo;
- objeto/caso relacionado;
- quantidade consumida;
- status:
  - consumido;
  - estimado;
  - bloqueado;
  - downgradado;
  - reprocessado;
- idempotency key ou referencia tecnica segura, se necessario;
- link para execucao, conversa, fluxo, aprovacao ou caso relacionado.

### Origens Permitidas

- `IA`;
- `WhatsApp`;
- `Sistema`;
- `Batch`;
- `Midia`;
- `Historico`.

### Acoes Permitidas

| Acao | Destino |
|---|---|
| `Abrir execucao` | `/app/fluxos/execucoes/[runId]` |
| `Abrir conversa` | conversa operacional relacionada |
| `Abrir caso` | caso operacional relacionado |
| `Abrir cobranca` | cobranca do aluno relacionada |
| `Abrir aprovacao` | aprovacao relacionada |
| `Abrir fluxo` | pagina do fluxo relacionado |

### O Que Nao Tem

- payload tecnico bruto;
- custo interno sensivel de provedor;
- configuracao de billing;
- contratacao de add-on;
- ajuste de limite de fluxo.

## Thresholds

| Uso | Comportamento |
|---|---|
| 0-69% | Fluxos rodam conforme configuracao. |
| 70% | Alerta preventivo e previsao ate o fim do ciclo. |
| 90% | Modo economia: baixa prioridade vira tarefa, aprovacao ou copiloto. |
| 100% | Automacao paga para. CRM manual continua. |
| Add-on ativo | Fluxos elegiveis retomam conforme regras publicadas. |

## Relacao Com Outras Familias

| Familia | Papel |
|---|---|
| Billing Taliya | Define plano, cota contratada, add-ons e faturas. |
| Billing Add-ons | Compra/solicitacao de add-on de uso. |
| Agentes/Fluxos | Define limite, estimativa e fallback por fluxo. |
| Execucoes | Mostra cota daquela execucao. |
| Hoje | Mostra alerta critico acionavel. |
| Aprovacoes | Mostra custo previsto antes de aprovar acao. |
| Auditoria | Guarda eventos sensiveis e mudancas. |

## Imagens Necessarias

Precisam de imagem propria:

1. `/app/uso`
   - visao geral de consumo, previsao, origem, alertas e downgrades.
   - imagem aprovada: `68_round-4.1O_uso_01_visao-geral-aprovado.png`.
2. `/app/uso/extrato`
   - tabela/lista de lancamentos de uso.
   - imagem aprovada: `69_round-4.1O_uso_02_extrato-aprovado.png`.

Nao gerar imagem propria para:

- cotas separadas;
- custos separados;
- alertas separados;
- add-ons;
- regras de economia;
- limites por fluxo.

## Decisao Final

Uso/Cotas fica enxuto no MVP.

A familia existe para explicar consumo e consequencia operacional, nao para duplicar Billing, Agentes/Fluxos ou Auditoria.
