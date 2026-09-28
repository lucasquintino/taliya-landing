# Planos, agentes e entitlements - PT-BR

> Status: contrato v0.1 de profundidade. Este documento define o que muda quando um studio tem 0, 1, 3 ou 7 agentes ativos.

## Regra central

O numero de agentes muda automacao, copiloto, execucoes, cotas e bloqueios.

O numero de agentes nao muda o fato de que o Taliya e um CRM completo.

```text
0 agentes = CRM completo manual/programatico.
1 agente = CRM completo + 1 dominio com IA ativa.
3 agentes = CRM completo + pacote operacional principal com IA ativa.
7 agentes = CRM completo + suite completa de agentes.
```

## Agentes canonicos

| Agente | Dominio | Onde aparece | Papel |
| --- | --- | --- | --- |
| Atendimento | Inbox, conversas, contatos, responsaveis | Web, app, WhatsApp | Sugerir/responder, classificar, resumir, handoff, opt-out e falha de envio. |
| Agenda | Agenda, turmas, aulas, reposicoes, lista de espera | Web, app, WhatsApp | Sugerir encaixe, avisar, organizar reposicao, detectar conflito e apoiar chamada. |
| Vendas | Interessados, experimental, matricula, origens | Web, app, WhatsApp | Follow-up, qualificacao, lembrete, pos-aula experimental e conversao. |
| Financeiro | Pagamentos, cobrancas, contratos, casos financeiros | Web, app, WhatsApp | Lembrete, rascunho de cobranca, comprovante, promessas e excecoes com trava. |
| Retencao | Risco, primeira semana, cancelamento, reclamacao, reativacao | Web, app, WhatsApp | Detectar risco, sugerir contato, acompanhar retorno e pausar automacao sensivel. |
| Historico/Professor | Historico permitido, notas, handoff, contexto de aula | Web, app | Resumir contexto permitido, lembrar nota, apoiar handoff e revisar pendencias. |
| Gestao/Governanca | Hoje, operacao, agentes, cotas, relatorios, incidentes | Web, app | Priorizar, explicar gargalos, resumir semana, monitorar execucoes/cotas/incidentes. |

## Planos

| Plano | Agentes ativos | CRM | IA/copiloto | Autonomia | Cotas |
| --- | ---: | --- | --- | --- | --- |
| Base | 0 | Completo | Desligado, salvo preview/bloqueado | Nenhuma | Sem consumo de agentes |
| 1 Agente | 1 slot | Completo | Apenas no dominio escolhido | Somente baixo risco daquele dominio | Cota do agente ativo |
| 3 Agentes | 3 slots | Completo | Nos dominios escolhidos | Baixo risco nos dominios ativos | Cota compartilhada/por fluxo |
| 7 Agentes | 7 slots | Completo | Todos os dominios | Baixo risco em todos, sensiveis travados | Cota completa com governanca |

## Slots e bundles

O entitlement deve ser por slot de agente, mas o produto oferece bundles recomendados.

| Plano | Bundle recomendado | Troca permitida |
| --- | --- | --- |
| 1 Agente | Atendimento ou Agenda, escolhido no setup | Sim, com aviso de impacto e cooldown operacional. |
| 3 Agentes | Atendimento + Agenda + Vendas | Sim, mas o produto deve avisar o que perde. |
| 7 Agentes | Todos os agentes canonicos | Nao precisa trocar; todos inclusos. |

## Comportamento com 0 agentes

| Area | O que funciona | O que fica bloqueado |
| --- | --- | --- |
| Hoje | Prioridades programaticas, tarefas, alertas, agenda, financeiro e riscos. | Sugestoes de IA, resumo inteligente pago, execucao autonoma. |
| Inbox | Conversas, resposta manual, tarefas, vinculos e opt-out. | Agente responder, resumir automaticamente, classificar com IA. |
| Agenda/turmas | Calendario, chamada, vagas, reposicao e encaixe programatico. | IA redigir convite, agente convidar automaticamente, resumo inteligente. |
| Vendas | Pipeline, experimental, tarefas, matricula e follow-up manual. | Cadencia automatica, sugestao de objeção, rascunhos de IA. |
| Financeiro | Pagamentos, cobrancas manuais, comprovantes, contratos e excecoes. | Redacao de cobranca por IA, automacao de lembrete pago. |
| Retencao | Risco por regra, tarefas, cancelamento e reativacao manual. | Copiloto de mensagem, resumo de risco com IA, campanha automatizada. |
| Historico/professor | Historico permitido, notas e handoff manual. | Resumo inteligente e lembrete automatico de nota por agente. |
| Gestao/governanca | Cotas zeradas, relatorios normais, auditoria e configuracao. | Relatorio de qualidade de agente e execucoes reais. |

## Comportamento com 1 agente

O studio escolhe 1 agente ativo.

| Tela | Se o agente cobre a area | Se o agente nao cobre a area |
| --- | --- | --- |
| Hoje | Cards mostram sugestoes/execucoes daquele dominio. | Cards continuam manuais/programaticos. |
| Inbox | Ativo se agente = Atendimento. | Sem IA ativa; mostra upgrade/selecionar agente. |
| Agenda | Ativo se agente = Agenda. | Encaixe programatico continua; sem IA. |
| Vendas | Ativo se agente = Vendas. | Pipeline manual/programatico. |
| Financeiro | Ativo se agente = Financeiro, com travas fortes. | Financeiro manual/programatico. |
| Retencao | Ativo se agente = Retencao. | Risco por regra e tarefas manuais. |
| Historico/professor | Ativo se agente = Historico/Professor. | Notas e contexto manual. |
| Operacao/relatorios | Ativo se agente = Gestao/Governanca. | Operacao manual/programatica. |

### Exemplo: 1 agente de Agenda

- Reposicao pode ter sugestao de mensagem.
- Turma com vaga pode acionar "Encontrar encaixe" programatico e "Pedir sugestao" com IA.
- Convite automatico so se o fluxo estiver em autonomo permitido.
- Atendimento, vendas e financeiro seguem sem IA ativa.

## Comportamento com 3 agentes

Bundle recomendado: Atendimento + Agenda + Vendas.

| Area | Resultado esperado |
| --- | --- |
| Atendimento | WhatsApp/inbox com sugestao, resumo, classificacao e handoff. |
| Agenda | Vagas, reposicoes, lembretes e conflitos com copiloto/autonomia segura. |
| Vendas | Follow-up, experimental, pos-aula e matricula com copiloto. |
| Financeiro | Manual/programatico, salvo upgrade/troca de slot. |
| Retencao | Manual/programatico, salvo upgrade/troca de slot. |
| Historico/professor | Manual/programatico, salvo upgrade/troca de slot. |
| Gestao/governanca | Relatorios normais; qualidade de agentes limitada aos 3 ativos. |

## Comportamento com 7 agentes

Todos os dominios ficam ativos.

| Area | Resultado esperado | Trava |
| --- | --- | --- |
| Atendimento | Copiloto e autonomia segura em respostas permitidas. | Identidade, opt-out, humano aguardando e tom sensivel. |
| Agenda | Copiloto/autonomia em lembretes, reposicao e encaixe seguro. | Regras de reposicao, consentimento, conflito e cota. |
| Vendas | Cadencia comercial, experimental e pos-aula com automacao segura. | Opt-out, limite de tentativas e objeção sensivel. |
| Financeiro | Lembretes e rascunhos com controle. | Acordo, desconto, estorno e disputa sempre humanos. |
| Retencao | Risco, primeira semana, retorno e reativacao assistidos. | Cancelamento/reclamacao pausam automacao. |
| Historico/Professor | Resumo permitido, lembrete de nota e handoff. | Dado sensivel bruto bloqueado. |
| Gestao/Governanca | Priorizacao, relatorios de agentes, incidentes e cota. | Suporte, billing, LGPD e permissao sempre auditados. |

## Estados de interface por entitlement

| Estado | Quando aparece | Acao visivel |
| --- | --- | --- |
| Sem agentes ativos | Plano Base ou todos pausados. | Operar manualmente, configurar preview, ver planos. |
| Bloqueado por plano | Tela/acao pertence a agente nao incluso. | Ver motivo, trocar agente quando permitido, upgrade. |
| Agente incluso nao configurado | Slot existe, mas falta setup. | Configurar, testar, manter manual. |
| Agente ativo | Fluxo publicado e preflight OK. | Pausar, simular, ver execucoes, editar limite. |
| Agente pausado | Usuario pausou ou incidente/cota pausou. | Retomar, ver motivo, corrigir bloqueio. |
| Cota 70% | Uso alto. | Alertar e sugerir economia. |
| Cota 90% | Economia ativada. | Converter baixa prioridade em tarefa/aprovacao. |
| Cota 100% | Automacao paga bloqueada. | Caminho manual, pacote/upgrade quando permitido. |

## Regras de downgrade/upgrade

| Mudanca | Comportamento |
| --- | --- |
| 7 -> 3 | Agentes fora dos 3 slots ficam pausados; execucoes historicas continuam consultaveis. |
| 3 -> 1 | Apenas 1 agente segue ativo; os outros viram bloqueados por plano. |
| 1 -> 0 | Agente pausa; CRM segue manual; historico/auditoria permanecem. |
| 0 -> 1/3/7 | Setup guiado mostra agentes novos, cotas, riscos e simulacao antes de ativar. |
| Trocar agente de slot | Mostrar fluxos que serao pausados e areas que ficarao sem IA. |

## Regras tecnicas de metering

- Uso de IA deve gerar lancamento de cota idempotente.
- Cliente nao decide entitlement; backend/billing decide.
- Toda execucao registra tenant, agente, fluxo, origem, custo estimado, status e idempotency key.
- Retentativa nao pode cobrar/contar duas vezes se for a mesma execucao logica.
- Cota deve ser visivel no Hoje, Agentes, Execucoes, Uso/cotas, Aprovacoes e Billing.

## Aceite de produto

Uma tela esta correta quando:

- o CRM ainda funciona no plano 0 agentes;
- a acao com agente fica bloqueada por plano quando o agente nao esta incluso;
- o usuario entende qual agente cobre aquela area;
- o caminho manual aparece antes de upgrade;
- cota, permissao, auditoria e fallback aparecem quando a acao usa IA.
