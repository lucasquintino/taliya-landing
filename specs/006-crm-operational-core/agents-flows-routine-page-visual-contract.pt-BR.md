# Taliya CRM - Contrato Visual Das Paginas De Rotina De Agentes/Fluxos

Status: contrato visual v0.1.
Data: 2026-05-22.

## Objetivo

Definir exatamente como deve ser a pagina de uma rotina em Agentes/Fluxos.

A imagem aprovada para este modelo e:

```text
54_round-4.1L_agentes_03_rotina-presenca-faltas-aprovado.png
```

Essa imagem mostra apenas a rotina `Presenca e faltas`, mas o mesmo contrato vale para todas as rotinas de todos os agentes.

## Regra Principal

A pagina da rotina responde:

```text
Como esta rotina deve trabalhar e como cada fluxo vai funcionar?
```

Ela nao e:

- dashboard;
- lista de execucoes;
- log tecnico;
- configuracao de integracao;
- configuracao geral do agente;
- builder livre de fluxo.

## Estrutura Fixa Da Pagina

Toda pagina de rotina deve ter:

1. breadcrumb;
2. titulo da rotina;
3. subtitulo curto;
4. chip de status da rotina;
5. bloco `Como essa rotina deve trabalhar?`;
6. seletor `Mais manual`, `Equilibrado`, `Mais autonomo`;
7. cards dos fluxos da rotina;
8. botoes `Simular rotina`, `Ajustar fluxos`, `Revisar para publicar`;
9. painel direito com Agente de Configuracao.

## Comportamento Da Rotina

Texto fixo do bloco:

```text
Como essa rotina deve trabalhar?
Escolha um comportamento para a rotina inteira. A Taliya aplica isso aos fluxos abaixo, e voce pode ajustar qualquer fluxo individualmente.
```

Opcoes:

| Opcao | Texto curto |
|---|---|
| Mais manual | A equipe decide e executa. A Taliya organiza tarefas e rascunhos. |
| Equilibrado | A Taliya executa o simples e chama a equipe nos pontos sensiveis. |
| Mais autonomo | A Taliya conduz o maximo possivel dentro dos limites publicados. |

Padrao visual:

- `Mais autonomo` aparece selecionado quando o plano e o preflight permitem;
- se algum fluxo nao puder subir para o modo maximo, o card do fluxo mostra o motivo;
- ajuste individual de um fluxo nao muda automaticamente os outros fluxos;
- quando houver ajuste individual, a rotina mostra `Personalizada`.

## Modos Dos Fluxos

Labels na UI:

| Label | Significado |
|---|---|
| Manual | Humano conduz; Taliya organiza. |
| Copiloto | Taliya sugere; humano decide. |
| Autonomo | Taliya executa o caso comum dentro dos limites publicados. |
| Autonomo com excecoes | Taliya executa o caso comum e chama equipe quando sai da regra. |
| Autonomo com aprovacao | Taliya prepara a acao, mas so executa apos aprovacao. |

Nao usar na UI:

- `Automatico direto`;
- `Automatico com excecoes`;
- `Automatico com aprovacao`;
- codigos internos como `B1`, `C3`, `D10`.

Os codigos continuam existindo em specs, auditoria e contratos tecnicos.

## Card Do Fluxo

Cada fluxo aparece como um card.

O card deve ter:

- titulo humano do fluxo, sem ID tecnico;
- chip de modo no topo;
- chip de status ao lado do chip de modo;
- explicacao humana do que vai acontecer;
- detalhes operacionais curtos;
- CTA `Ver e ajustar`.

Ordem visual do topo do card:

```text
Nome do fluxo        [Modo] [Status]
```

Exemplo:

```text
Confirmacao de presenca        [Autonomo] [Pronto]
```

Detalhes operacionais possiveis:

- `Gatilho`;
- `Acao`;
- `Chama equipe`;
- `Aprovacao`;
- `Fallback`.

Mostrar apenas os detalhes que importam para aquele fluxo.

## Status Dos Fluxos

Status possiveis:

| Status | Quando usar |
|---|---|
| Pronto | Fluxo pode rodar com a configuracao atual. |
| Precisa aprovacao | Fluxo esta pronto, mas para em aprovacao humana. |
| Pendente | Falta ajuste antes de simular/publicar. |
| Bloqueado | Dependencia impede execucao. |
| Pausado | Usuario, incidente ou sistema pausou o fluxo. |
| Personalizado | Fluxo difere do comportamento escolhido para a rotina. |
| Nao contratado | Plano nao inclui o agente/fluxo. |

## Agente De Configuracao

O painel direito aparece em paginas de rotina, ajuste, simulacao e publicacao.

Na pagina da rotina, ele deve:

- explicar o comportamento escolhido;
- explicar por que cada fluxo esta naquele modo;
- responder onde a equipe entra;
- responder o que falta para publicar;
- oferecer simulacao de exemplo.

Mensagem base:

```text
Essa rotina esta em Mais autonomo. Cada fluxo mostra o que a Taliya faz, quando chama a equipe e onde exige aprovacao.
```

Perguntas rapidas base:

- `O que muda no Equilibrado?`
- `Por que este fluxo pede aprovacao?`
- `Onde a equipe e chamada?`
- `Simular um caso desta rotina`

## Rotinas E Cards De Fluxo

As rotinas abaixo usam a mesma pagina visual. O que muda e o titulo, subtitulo e os cards de fluxo.

### Atendimento

| Rotina | Rota | Subtitulo | Cards de fluxo |
|---|---|---|---|
| Conversas e triagem | `/app/agentes/atendimento/rotinas/conversas-e-triagem` | Organiza conversas, duvidas permitidas, fora de escopo e chamadas humanas. | Nova conversa; Duvidas permitidas; Aluno existente; Fora do escopo; Chamada humana; Ciclo de vida/SLA |
| Identidade e privacidade | `/app/agentes/atendimento/rotinas/identidade-e-privacidade` | Protege consentimento, identidade, midias, privacidade e telefone compartilhado. | Consentimento/opt-out; Identidade/midias; Privacidade/dados; Telefone compartilhado e identidade |

### Agenda

| Rotina | Rota | Subtitulo | Cards de fluxo |
|---|---|---|---|
| Presenca e faltas | `/app/agentes/agenda/rotinas/presenca-e-faltas` | Confirma presenca, trata faltas avisadas, no-shows e correcoes. | Confirmacao de presenca; Falta com aviso; No-show; Correcao de presenca |
| Vagas, reposicoes e lista de espera | `/app/agentes/agenda/rotinas/vagas-reposicoes-lista-espera` | Organiza vagas abertas, remarcacoes, creditos e lista de espera. | Recuperar vaga aberta; Reposicao/remarcacao; Lista de espera; Creditos de reposicao |
| Grade e capacidade | `/app/agentes/agenda/rotinas/grade-e-capacidade` | Ajuda com horario fixo, cancelamento pelo studio, conflitos e ajustes de grade. | Mudanca de horario fixo; Cancelamento pelo studio; Conflito de capacidade; Ajuste de grade |
| Primeira aula e aulas especiais | `/app/agentes/agenda/rotinas/primeira-aula-aulas-especiais` | Acompanha primeira aula, workshops e eventos especiais. | Primeira aula; Aula especial/workshop |
| Agenda experimental | `/app/agentes/agenda/rotinas/agenda-experimental` | Organiza disponibilidade para experimental e no-show de experimental. | Disponibilidade experimental; Experimental no-show |

### Vendas

| Rotina | Rota | Subtitulo | Cards de fluxo |
|---|---|---|---|
| Captura e qualificacao | `/app/agentes/vendas/rotinas/captura-e-qualificacao` | Organiza entrada de leads, origem, qualificacao, perdas e indicacoes. | Entrada multicanal de lead; Origem/qualificacao; Perda comercial; Indicacao |
| Experimental e acompanhamento | `/app/agentes/vendas/rotinas/experimental-e-acompanhamento` | Acompanha aula experimental, lembretes, pos-aula, follow-up e demanda sem vaga. | Aula experimental; Lembrete experimental; Pos-aula experimental; Follow-up comercial; Demanda sem vaga |
| Conversao e matricula | `/app/agentes/vendas/rotinas/conversao-e-matricula` | Apoia valores, pre-matricula, objecoes, checkout e conversao em aluno. | Valores e planos; Pre-matricula; Objecoes; Checkout/abandono; Interessado para aluno; Upsell/upgrade |

### Financeiro

| Rotina | Rota | Subtitulo | Cards de fluxo |
|---|---|---|---|
| Lembretes e pagamentos | `/app/agentes/financeiro/rotinas/lembretes-e-pagamentos` | Organiza lembretes, atrasos, links, falhas, recibos e conciliacao. | Lembrete de vencimento; Pagamento atrasado; Pix/link; Falha de pagamento; Recibo/nota; Conciliacao interna |
| Ciclo do plano do aluno | `/app/agentes/financeiro/rotinas/ciclo-do-plano-do-aluno` | Apoia renovacao, pausa, trancamento e encerramento ou alteracao de plano. | Renovacao de plano; Pausa/trancamento; Encerramento ou alteracao efetiva de plano |
| Excecoes e documentos financeiros | `/app/agentes/financeiro/rotinas/excecoes-documentos-financeiros` | Trata comprovantes, excecoes, contratos, bloqueios, creditos e fechamento mensal. | Confirmacao de pagamento; Excecoes financeiras; Contrato/termos; Bloqueio/liberacao; Creditos/cortesias; Fechamento mensal |

### Retencao

| Rotina | Rota | Subtitulo | Cards de fluxo |
|---|---|---|---|
| Retencao preventiva | `/app/agentes/retencao/rotinas/retencao-preventiva` | Detecta queda de frequencia, inatividade, retorno, satisfacao e marcos de engajamento. | Queda de frequencia; Aluno inativo; Retorno; Satisfacao; Retorno apos pausa; Marco de engajamento |
| Casos sensiveis | `/app/agentes/retencao/rotinas/casos-sensiveis` | Protege cancelamento, reclamacao, reativacao, saude/evento pessoal e risco por perfil. | Risco de cancelamento; Reativacao de ex-aluno; Risco por perfil; Pos-cancelamento; Saude/evento pessoal; Segmentacao de risco; Reclamacao e recuperacao de confianca |

### Gestao/Governanca

| Rotina | Rota | Subtitulo | Cards de fluxo |
|---|---|---|---|
| Comando operacional | `/app/agentes/gestao-governanca/rotinas/comando-operacional` | Prioriza dia, dinheiro na mesa, fila humana, gargalos, resumo semanal e qualidade de dados. | Prioridades do dia; Dinheiro na mesa; Fila humana; Gargalos; Resumo semanal; Qualidade de dados; Capacidade/crescimento |
| Governanca de agentes | `/app/agentes/gestao-governanca/rotinas/governanca-de-agentes` | Monitora creditos, limites, performance, permissoes, auditoria, testes e incidentes. | Creditos/limites; Performance; Permissoes/auditoria; Teste de fluxo; Incidente de automacao e correcao operacional; Mudanca de politica ou regra operacional |
| Integracoes e importacao | `/app/agentes/gestao-governanca/rotinas/integracoes-e-importacao` | Acompanha falhas, webhooks, importacao e migracao. | Falhas/webhooks; Importacao/migracao |

### Historico/Evolucao

| Rotina | Rota | Subtitulo | Cards de fluxo |
|---|---|---|---|
| Aula com contexto | `/app/agentes/historico-professor/rotinas/aula-com-contexto` | Apoia contexto antes da aula, observacoes, evolucao, repasse e linha do tempo. | Contexto antes da aula; Observacao pos-aula; Objetivo/evolucao; Repasse entre professores; Lembrete professor; Linha do tempo |
| Historico protegido | `/app/agentes/historico-professor/rotinas/historico-protegido` | Protege restricoes, documentos, correcao de historico, compartilhamento e permissoes. | Restricao/cuidado; Contexto para agente; Documentos/anamnese; Correcao de historico; Compartilhar contexto; Permissao historico |

## Como Preencher Explicacao E Detalhes Dos Cards

Para cada fluxo, a explicacao e os detalhes vêm da ficha do fluxo no contrato final:

- `agents-flows-final-flow-page-contract.pt-BR.md`
- `agents-flows-final-flow-contract-matrix.pt-BR.csv`

Se houver conflito com mapas antigos de modo, perfil ou ajuste, a matriz final vence.

Regra:

- a explicacao humana deve dizer o que a Taliya faz na pratica;
- `Gatilho` vem do evento que inicia o fluxo;
- `Acao` vem da acao principal do fluxo;
- `Chama equipe` aparece quando o modo e `Autonomo com excecoes`;
- `Aprovacao` aparece quando o modo e `Autonomo com aprovacao`;
- `Fallback` aparece quando existe degradacao importante;
- status fica ao lado do modo.

Este contrato evita gerar uma imagem separada para cada rotina sem perder clareza do que cada pagina deve conter.
