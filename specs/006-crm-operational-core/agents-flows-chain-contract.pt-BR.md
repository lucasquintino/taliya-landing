# Taliya CRM - Contrato De Encadeamento Entre Fluxos

Status: contrato funcional v0.1.
Data: 2026-05-22.

## Objetivo

Explicar como um fluxo pode continuar em outro fluxo, rotina ou area do CRM sem misturar configuracoes.

Este contrato corrige a ambiguidade vista em `Falta com aviso`: o fluxo nao deve configurar profundamente reposicao, mas pode encaminhar a operacao para a rotina de reposicoes.

## Regra Principal

Fluxos podem emendar em outros fluxos.

Mas um fluxo nao configura o outro.

Ele apenas entrega uma continuacao operacional:

- evento;
- tarefa;
- aprovacao;
- caso;
- item de fila;
- execucao de outro fluxo;
- registro para auditoria.

O fluxo seguinte usa as proprias configuracoes, modo, teto, preflight, cota, permissoes, fallback e auditoria.

## Por Que Isso Importa

Sem essa regra, a tela de um fluxo vira um painel gigante tentando configurar o sistema inteiro.

Exemplo ruim:

```text
Falta com aviso configura destino da reposicao, prioridade de vaga, credito, lista de espera e regra de encaixe.
```

Exemplo correto:

```text
Falta com aviso registra a falta e define o proximo passo.
Se o proximo passo for reposicao, a operacao continua na rotina Vagas, reposicoes e lista de espera.
A logica de vaga, credito e prioridade fica nessa rotina.
```

## Tipos De Continuidade

### 1. Termina Aqui

O fluxo conclui a acao e registra auditoria.

Exemplo:

```text
Duvidas permitidas responde a pergunta e encerra a execucao.
```

### 2. Continua Como Tarefa Humana

O fluxo cria tarefa, caso ou aprovacao para uma pessoa.

Exemplo:

```text
Correcao de presenca prepara a alteracao e cria aprovacao para o admin.
```

### 3. Emenda Em Outro Fluxo

O fluxo cria uma entrada para outro fluxo cuidar da proxima etapa.

Exemplo:

```text
Falta com aviso -> Reposicao/remarcacao
```

### 4. Chama Outra Area

O fluxo nao dispara necessariamente outro fluxo, mas envia o caso para outra area operacional.

Exemplo:

```text
Retorno apos pausa -> Agenda
```

### 5. Pausa E Abre Incidente

O fluxo para por falha, risco, cota, integracao ou permissao e abre um item de controle.

Exemplo:

```text
Falhas/webhooks -> Incidente de automacao
```

## O Que O Studio Configura

O studio configura apenas a decisao local daquele fluxo.

Exemplos:

| Fluxo | Ajuste local correto | Nao configurar aqui |
|---|---|---|
| Falta com aviso | Proximo passo apos falta | Regra completa de reposicao |
| Demanda sem vaga | Proximo passo sem vaga | Prioridade completa da lista de espera |
| Retorno apos pausa | Quando chamar Agenda | Grade, vaga ou encaixe |
| Recibo/nota | Quando abrir tarefa | Fallback tecnico inteiro |
| Falha pagamento | Quando abrir caso | Retry tecnico do provedor |

## O Que A UI Deve Mostrar

Toda pagina de fluxo deve explicar o encadeamento dentro do `Fim`:

```text
Fim
```

Essa parte aparece quando o fluxo entrega a operacao para outro fluxo, rotina ou area.

Exemplo:

```text
Fim
Se a falta for registrada, a Taliya cria uma tarefa de reposicao.
A rotina Vagas, reposicoes e lista de espera decide vaga, credito, prioridade e remarcacao.
```

Essa area precisa deixar claro que:

- o fluxo atual terminou sua parte;
- o proximo passo nao e configurado profundamente aqui;
- o destino usa as proprias regras.

Nao deve virar configuracao extensa.

## Como Renderizar Na Pagina De Fluxo

Ordem recomendada:

1. modo do fluxo;
2. `Como funciona neste modo`, dividido em `Inicio`, `Meio` e `Fim`;
3. `Ajustes deste fluxo`;
4. acoes de testar/salvar/voltar.

Nao colocar consequencias dentro de `Segue sozinho quando`.

`Segue sozinho quando` deve ter apenas condicoes para o fluxo atual seguir.

Encadeamento e consequencia, portanto fica no `Fim`.

## Exemplo: Falta Com Aviso

Fluxo atual:

```text
Falta com aviso
```

No bloco `Como funciona neste modo`, `Segue sozinho quando` deve mostrar apenas:

```text
aluno foi identificado
aula existe na agenda
aviso chegou ate o prazo configurado
falta ainda nao foi registrada
mensagem usa template aprovado
```

Depois, no `Fim`:

```text
Se a falta for registrada, a Taliya cria uma tarefa de reposicao.
A rotina Vagas, reposicoes e lista de espera decide vaga, credito, prioridade e remarcacao conforme as proprias regras.
```

Ajuste local:

```text
Proximo passo apos falta: Criar tarefa de reposicao
```

Nao configurar neste fluxo:

- prioridade da lista;
- regra de credito;
- limite de convites;
- vaga compativel;
- remarcacao detalhada.

## Exemplos Principais De Encadeamento

| Origem | Continua em | Tipo | Regra |
|---|---|---|---|
| Falta com aviso | Reposicao/remarcacao | Outro fluxo/rotina | Registra falta e entrega reposicao para a rotina de reposicoes. |
| No-show | Retencao preventiva | Outra rotina | Se recorrente ou sensivel, cria caso para retencao. |
| Demanda sem vaga | Lista de espera | Outro fluxo/rotina | Vendas registra interesse; Agenda controla vaga e prioridade. |
| Aula experimental | Disponibilidade experimental | Outro fluxo/rotina | Vendas qualifica; Agenda oferece horarios permitidos. |
| Pagamento atrasado | Excecoes financeiras | Outra rotina | Financeiro simples cobra; excecao financeira pede aprovacao. |
| Retorno apos pausa | Agenda | Outra area/rotina | Retencao aciona Agenda para vaga/horario. |
| Reclamacao e recuperacao | Operacao/incidentes ou aprovacao | Controle/operacao | Retencao pausa automacoes e cria caso sensivel. |
| Falhas/webhooks | Incidente de automacao | Control plane distribuido | Integracao falha e governanca investiga. |
| Restricao/cuidado | Historico protegido | Outra rotina | Aula/contexto pode abrir revisao protegida. |
| Contexto antes aula | Observacao pos-aula | Fluxo posterior | Resumo antes da aula pode gerar lembrete de observacao depois. |

## Relacao Com Simulacao

Simulacao deve mostrar o encadeamento real.

Para cada cenario, a simulacao precisa dizer:

- onde o fluxo comeca;
- o que ele faz;
- se termina ali;
- se chama humano;
- se emenda em outro fluxo;
- qual regra do proximo fluxo assume dali em diante.

## Relacao Com Auditoria

Toda emenda entre fluxos registra:

- fluxo de origem;
- motivo da continuidade;
- destino;
- dados entregues;
- usuario ou agente que publicou a regra;
- versao da configuracao;
- cota consumida ate aquele ponto;
- proxima execucao ou tarefa criada.

## Regra De Produto

Encadeamento deve ser visivel, mas nao pesado.

O dono precisa entender:

```text
Este fluxo faz X.
Depois ele continua em Y.
Y tem suas proprias regras.
```

Isso evita duas confusoes:

1. achar que cada fluxo e isolado;
2. achar que um fluxo configura o produto inteiro.
