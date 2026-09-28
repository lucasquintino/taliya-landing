# Auditoria Pos-3C - Cobertura De Rotas, Funcionalidades, Fluxos E Casos

> Status: auditoria v0.1 apos Rodadas 3C.1, 3C.2 e 3C.3. Objetivo: verificar se o design system web de componentes ja e suficiente para montar as rotas e funcionalidades do CRM web.

## Veredito

Para **CRM web**, sim: os componentes aprovados agora sao suficientes para montar as 38 superficies e cobrir os 157 casos de uso em nivel v0.1.

Para **app mobile**, ainda nao: as rodadas atuais sao web. O mobile precisa de design system proprio antes de afirmar cobertura visual completa das telas do app.

Conclusao curta:

```text
Web: suficiente para gerar paginas/rotas v0.1.
Mobile: ainda falta design system mobile.
```

## O Que Mudou Depois Da 3C

A auditoria anterior apontava lacunas grandes em componentes compostos de dominio.

As rodadas 3C fecharam essas lacunas principais:

| Lacuna anterior | Fechamento |
| --- | --- |
| Setup, importacao, duplicidades e qualidade de dados | 3C.1 |
| Perfil, relacoes, consentimento e timeline sensivel | 3C.1 |
| Agenda semanal, turmas, chamada e reposicoes | 3C.2 |
| Documentos, comprovantes, conciliacao e simulacao financeira | 3C.2 |
| Flow builder, simulacao, preflight, trace e incidentes | 3C.3 |
| Auditoria antes/depois, LGPD e grant de suporte | 3C.3 |
| Relatorios, exportacoes, segmentos e comunicados | 3C.3 |

## Cobertura Por Superficie Web

| Superficie | Cobertura de componentes | Observacao |
| --- | --- | --- |
| Onboarding e configuracao inicial | Suficiente | 3C.1 cobre wizard, checklist, importacao, duplicidades e revisao. |
| Hoje | Suficiente | 3A, 3B.2, 3B.3 e 3B.5 cobrem cards, alertas, cotas, tarefas e aprovacoes. |
| Inbox e conversas | Suficiente | 3B.4 cobre inbox, conversa, composer, sugestao, falha e handoff. |
| Contatos | Suficiente | 3C.1 cobre perfil, telefone compartilhado e validacao. Responsaveis/familia/consentimentos nao viram modulos proprios no MVP. |
| Qualidade de dados | Suficiente | 3C.1 cobre conflitos, duplicidades, mapeamento e fila de saneamento. |
| Alunos e perfil | Suficiente | 3C.1 cobre cabecalho, abas, relacoes, timeline sensivel e preferencias. |
| Historico do aluno | Suficiente | 3C.1 cobre timeline sensivel, dado mascarado e pedido de acesso. |
| Professor e notas | Suficiente por composicao | Usa perfil, agenda, timeline, nota, handoff e lista de aulas. |
| Agenda | Suficiente | 3C.2 cobre calendario semanal, aula, capacidade, conflito e filtros. |
| Grade, turmas e eventos | Suficiente por composicao | 3C.2 cobre turma, vagas, lista de espera e recurso; eventos usam mesmos blocos. |
| Aula e chamada | Suficiente | 3C.2 cobre card de aula e roster de chamada. |
| Reposicoes e lista de espera | Suficiente | 3C.2 cobre matcher, candidatos, vagas, reserva e convite. |
| Interessados e vendas | Suficiente | 3B.3, 3B.4 e 3C.1 cobrem pipeline, perfil, conversa e proxima acao. |
| Aulas experimentais | Suficiente por composicao | Usa agenda, aula, interessado, conversa, lembrete e conversao. |
| Matriculas | Suficiente | 3C.1 e 3C.2 cobrem perfil, checklist, documento, pagamento e primeira aula. |
| Vendas e origens | Suficiente | 3B.3 e 3C.3 cobrem relatorios, ranking, origem, segmento e demanda. |
| Financeiro | Suficiente | 3B.3, 3B.5 e 3C.2 cobrem tabela, indicadores, cobrancas e conciliacao. |
| Pagamentos e cobrancas | Suficiente | 3C.2 cobre comprovante, conciliacao, valor/moeda e status. |
| Excecoes financeiras sensiveis | Suficiente por composicao | 3C.2 cobre simulador antes/depois; 3B.2 cobre confirmacao/aprovacao; resolucao acontece por Financeiro, Movimentacoes, Aprovacoes, Tarefas, Aluno ou Operacao. |
| Contratos e documentos financeiros | Suficiente | 3C.2 cobre viewer, assinatura/envio, download e anexo. |
| Retencao | Suficiente | 3B.3 e 3B.4 cobrem risco, timeline, conversa, tarefas e sugestao. |
| Cancelamentos e reativacao | Suficiente por composicao | Usa caso sensivel, plano de salvamento, timeline, aprovacao e comunicacao. |
| Reclamacoes e casos sensiveis | Suficiente | 3B.2, 3B.4 e 3C.3 cobrem severidade, pausa, resposta, auditoria e diff. |
| Jornadas e operacao | Suficiente | 2B, 3A, 3B.3 e 3C.3 cobrem jornada, casos, bloqueios, trace e incidentes. |
| Tarefas e operacao | Suficiente | 3B.3 cobre lista/kanban; 3B.2 cobre estados e confirmacoes. |
| Aprovacoes | Suficiente | 3B.4 e 3C.3 cobrem proposta, risco, antes/depois, custo e decisao. |
| Agentes e fluxos | Suficiente | 3B.4, 3B.5 e 3C.3 cobrem agente, modo, fluxo, simulacao e preflight. |
| Execucoes e incidentes de agentes | Suficiente | 3C.3 cobre trace, custo, erro, incidente e reprocessamento seguro. |
| Uso, cotas e economia | Suficiente | 3B.5 e 3C.3 cobrem cota, limite, custo, trace, economia e pacote. |
| Relatorios e exportacoes | Suficiente | 3B.3 e 3C.3 cobrem graficos, ranking, heatmap, exportacao e job. |
| Configuracoes | Suficiente | 3B.1, 3B.2, 3B.5 e 3C.3 cobrem formularios, politicas, diff e auditoria. |
| Politicas operacionais | Suficiente | 3C.3 cobre politica, modo, preflight, simulacao e publicacao. |
| Recursos, feriados e disponibilidade | Suficiente por composicao | 3C.2 cobre conflito de recurso e impacto; configuracao usa 3B.1/3B.5. |
| Segmentos e comunicados | Suficiente | 3C.3 cobre audiencia, consentimento, preview, custo e aprovacao. |
| Integracoes | Suficiente | 3B.5 cobre conectado/erro; 3C.1/3C.3 cobrem importacao, logs e reprocessamento. |
| Auditoria | Suficiente | 3C.3 cobre diff, log detalhado, ator, objeto, origem, horario e status. |
| Privacidade e solicitacoes | Suficiente | 3C.1 e 3C.3 cobrem consentimento, mascaramento, LGPD e grant. |
| Assinatura e billing | Suficiente | 3B.5 cobre plano, 0 agentes, upgrade, pagamento, fatura e pacote. |

## Cobertura Por Tipo De Fluxo

| Tipo de fluxo | Cobertura | Componentes principais |
| --- | --- | --- |
| Manual | Coberto | botoes, formularios, tabelas, listas, calendario, drawers, confirmacoes. |
| Copiloto | Coberto | painel de copiloto, sugestao, resumo, aprovacao, editar/rejeitar. |
| Autonomo | Coberto | builder, modo por fluxo, preflight, execucao, trace, pausa, incidente. |
| Bloqueado por plano | Coberto | card de plano, permissao/bloqueio, 0 agentes, upgrade, fallback manual. |
| Bloqueado por cota | Coberto | cota, limite, uso, economia, pacote, fallback manual. |
| Acao sensivel | Coberto | confirmacao, antes/depois, risco, auditoria, permissao e diff. |
| Falha de integracao | Coberto | erro, reconectar, retry, incidente, log e reprocessamento seguro. |
| Dado incompleto | Coberto | fila de conflitos, mapeamento, duplicidade, dado mascarado e pedido de acesso. |

## Casos De Uso

Os 157 casos de uso ficam cobertos em nivel de componente web porque cada pagina dona tem pelo menos:

- container/shell;
- lista, tabela, calendario, kanban, jornada ou perfil;
- acao primaria manual;
- estados vazio/loading/erro/sem permissao/bloqueado;
- confirmacao quando sensivel;
- cota/plano quando agente participa;
- auditoria quando a acao altera algo relevante;
- fallback manual quando IA/agente nao pode agir.

Nao ha, nesta auditoria, um caso de uso web que esteja bloqueado por ausencia total de componente.

## Pontos Que Ainda Merecem Refinamento Futuro

Estes itens nao bloqueiam as rotas web v0.1, mas podem merecer rodadas pequenas depois que as paginas reais revelarem necessidade:

1. **Busca global / command palette**
   - Ja ha busca avancada e topbar, mas falta uma prancha especifica de resultado global agrupado e acoes rapidas.

2. **Notification center**
   - Ja ha alertas, toasts e Hoje, mas falta uma prancha especifica de central de notificacoes com agrupamento por urgencia.

3. **Editor profundo de templates**
   - Segmentos/comunicados e composer existem, mas pode faltar editor com variaveis, preview multi-canal e validacao.

4. **Matriz de ferramentas permitidas por agente**
   - 3C.3 cobre fluxo, politica e preflight, mas uma matriz visual tool-by-tool pode ser necessaria para governanca avancada.

5. **Recorrencia**
   - Agenda, calendario e financeiro cobrem base; regras recorrentes complexas podem precisar de componente proprio.

Esses itens sao refinamentos, nao bloqueios.

## Mobile

As rotas e casos mobile estao mapeados nos documentos de produto, mas os componentes visuais atuais sao web.

Portanto, para app mobile ainda faltam:

- mobile shell;
- bottom tabs;
- cards de Hoje;
- lista mobile;
- bottom sheet;
- action sheet;
- swipe actions;
- mobile chat;
- mobile agenda/turma/chamada;
- mobile aprovacao;
- mobile configuracao de agente;
- mobile cota/alerta;
- mobile forms e filtros.

Nao usar os componentes web como resposta final para mobile. Eles podem inspirar, mas mobile precisa rodadas proprias.

## Decisao Recomendada

Para web:

```text
Prosseguir para Rodada 4 - Paginas Web Por Familia.
```

Para mobile:

```text
Abrir Rodada 5 - Design System Mobile antes de gerar telas do app.
```

## Conclusao

Depois das Rodadas 3C:

- componentes web genericos: cobertos;
- componentes web compostos de dominio: cobertos em v0.1;
- rotas web: cobertas para montagem funcional;
- fluxos manual/copiloto/autonomo: cobertos para representacao visual;
- casos de uso web: cobertos por componentes e composicao;
- mobile: ainda nao coberto visualmente.

Veredito final:

```text
O design system web agora e suficiente para montar as rotas e funcionalidades web v0.1.
Ainda falta design system mobile para dizer que web + app estao 100%.
```
