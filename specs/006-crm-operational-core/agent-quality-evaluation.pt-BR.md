# Qualidade e avaliacao dos agentes - PT-BR

> Status: Rodada 0 v0.1. Este documento define como medir se agentes estao ajudando ou criando risco.

## Regra central

Agente nao pode ser caixa-preta. Toda execucao relevante deve ter motivo, modo, confianca, resultado, custo e possibilidade de correcao.

## Indicadores por agente/fluxo

| Indicador | Pergunta |
| --- | --- |
| Taxa de resolucao | Quantos casos o fluxo resolveu sem reabrir? |
| Taxa de aprovacao | Quantas sugestoes foram aprovadas sem edicao? |
| Taxa de edicao | Quantas sugestoes precisaram ajuste humano? |
| Taxa de rejeicao | Quantas sugestoes foram recusadas? |
| Reabertura | Quantos casos voltaram depois de resolvidos? |
| Incidentes | Quantas execucoes geraram erro operacional? |
| Bloqueios | Quantas pararam por dado, permissao, cota ou integracao? |
| Tempo economizado | Quanto trabalho manual foi evitado ou preparado? |
| Custo por resolucao | Quanto consumiu para resolver cada tipo de caso? |
| Risco evitado | Quantas acoes foram corretamente bloqueadas/escaladas? |

## Avaliacao humana

Em sugestoes/aprovacoes, permitir marcar:

- util;
- precisou ajuste;
- errado;
- arriscado;
- faltou dado;
- tom inadequado;
- resolveu.

## Classificacao de falha

| Tipo | Exemplo | Tratamento |
| --- | --- | --- |
| Dado ruim | aluno duplicado, telefone compartilhado. | Qualidade de dados. |
| Regra ruim | politica de reposicao errada. | Politica versionada. |
| Prompt/IA | resposta mal escrita ou interpretacao errada. | Ajuste supervisionado/eval. |
| Integracao | WhatsApp/pagamento falhou. | Incidente/log. |
| Permissao | agente tentou acao proibida. | Bloqueio e revisao de guardrail. |
| Cota | fluxo parou ou downgradou. | Uso/cotas/economia. |
| Produto | tela/fluxo nao suporta caso real. | Decisao aberta/ajuste de escopo. |

## Telas

| Tela | Deve mostrar |
| --- | --- |
| Execucao de agente | entrada, decisao, modo, custo, resultado, erro, proxima acao. |
| Incidente | impacto, causa, correcao, prevencao, reprocessamento. |
| Relatorio de agentes | metricas por agente/fluxo/periodo. |
| Aprovacoes | antes/depois, confianca, motivo e feedback. |
| Agentes/fluxos | desempenho recente e alertas. |
| Mobile Agentes/alertas | falhas, bloqueios, pausar emergencia. |

## Ciclo de melhoria supervisionada

```text
execucao
  -> avaliacao/feedback
  -> classificacao da falha
  -> ajuste em politica/configuracao/template/eval
  -> simulacao
  -> publicacao versionada
```

## O que nao pode acontecer

- agente alterar suas proprias regras em producao;
- prompt decidir permissao, billing ou seguranca sozinho;
- erro sumir sem incidente ou feedback;
- metrica de sucesso contar apenas volume, sem qualidade.

## Aceite

Toda ficha de tela com agente deve dizer onde o usuario ve:

- o que o agente fez;
- por que fez;
- quanto custou;
- se deu certo;
- como corrigir;
- como pausar;
- como avaliar.
