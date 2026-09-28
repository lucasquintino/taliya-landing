# Design System Web - Rodada 4.1C - Pagina Checklists

> Status: aprovada v0.1. Esta documentacao registra a imagem da rota `/app/checklists`, cobrindo execucoes de rotinas operacionais com detalhe lateral.

## Arquivo

Arquivo aprovado:

`24_round-4.1C_checklists_01_lista-execucao-detalhe.png`

Arquivos locais observados:

- `D:\Downloads\24_round-4.1C_checklists_01_lista-execucao-detalhe.png.png`
- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\24_round-4.1C_checklists_01_lista-execucao-detalhe.png.png`

Nome canonico:

`24_round-4.1C_checklists_01_lista-execucao-detalhe.png`

## Decisao Central

**Checklists** responde:

```text
Quais rotinas operacionais precisam ser executadas, em que ponto estao e o que ainda falta conferir?
```

Checklist nao e tarefa solta.

Checklist e uma rotina padronizada com:

- nome;
- tipo;
- responsavel;
- prazo;
- progresso;
- passos;
- bloqueios;
- historico;
- origem quando aplicavel.

Tarefa e apenas um desdobramento possivel quando um passo do checklist precisa virar trabalho separado com dono, prazo e acompanhamento proprio.

## Rota Coberta

| Rota | Cobertura |
| --- | --- |
| `/app/checklists` | Coberta pela imagem 24. |
| `/app/checklists/[runId]` | Coberta parcialmente pelo painel lateral de detalhe. Pode virar rota/drawer profundo no futuro se necessario. |

## Layout Aprovado

A pagina usa:

- App Shell web aprovado;
- topbar do grupo com `Tarefas`, `Checklists`, `Modelos` e `Historico`;
- `Checklists` ativo;
- titulo `Checklists`;
- subtitulo `Rotinas operacionais do estudio`;
- busca e filtros por tipo, status e responsavel;
- botao principal `Criar checklist`;
- coluna esquerda com filas/tipos de rotina;
- lista central de execucoes;
- painel direito com detalhe da execucao selecionada.

## Blocos Validados

| Bloco | Papel |
| --- | --- |
| Filtros superiores | Encontrar checklists por busca, tipo, status e responsavel. |
| Filas laterais | Separar rotinas por Hoje, Abertura, Fechamento, Agenda, Financeiro, Alunos, Agentes e Setup. |
| Lista central | Mostrar execucoes abertas ou recentes com progresso e proximo passo. |
| Painel direito | Mostrar o checklist selecionado, passos, bloqueio, ultima atividade, comentario e acoes. |
| Paginacao | Permitir volume maior sem transformar a tela em dashboard. |

## Conteudo Minimo Da Lista

Cada execucao de checklist deve mostrar:

- nome do checklist;
- tipo de rotina;
- progresso;
- responsavel;
- prazo;
- status;
- proximo passo;
- ultima atividade.

Exemplos validados na imagem:

- `Abertura do estudio`;
- `Revisao diaria da agenda`;
- `Fechamento do dia`;
- `Setup do agente de agenda`;
- `Onboarding de novo aluno`.

## Painel Direito

O painel direito representa o detalhe da execucao selecionada.

Na imagem aprovada, o exemplo e:

`Abertura do estudio`

Campos validados:

- badge `Checklist`;
- titulo;
- status;
- responsavel;
- prazo;
- progresso;
- passos com checkbox;
- passo pendente/bloqueado com motivo;
- ultima atividade;
- comentario recente;
- acoes.

Regra do painel direito:

- por padrao, `/app/checklists` pode carregar sem execucao selecionada;
- a imagem aprovada mostra uma execucao selecionada, nao o estado inicial obrigatorio;
- o painel direito e contextual e muda conforme o checklist, passo ou execucao clicada;
- todos os modos preservam a ideia central: checklist executa rotina com criterios, evidencias e progresso.

Modos principais do painel de Checklist:

| Item clicado | Painel direito deve mostrar |
| --- | --- |
| Execucao em andamento | Progresso, passos pendentes/concluidos, responsavel, prazo, comentario e acoes de continuar/concluir. |
| Passo bloqueado | Motivo do bloqueio, dependencia, origem canonica, quem pode resolver e opcao de criar tarefa. |
| Checklist atrasado | Tempo de atraso, impacto operacional, passos criticos e acoes de continuar, delegar ou criar tarefa. |
| Checklist concluido | Resumo auditavel, quem concluiu, horario, evidencias e acoes restritas de reabrir quando permitido. |
| Checklist pulado/cancelado | Motivo obrigatorio, aprovacao quando necessaria, impacto e historico. |
| Criar/editar rotina | Campos de template, recorrencia, responsavel, passos obrigatorios e regras de evidencia. |

## Acoes Validadas

| Acao | Regra |
| --- | --- |
| `Continuar` | Retoma a execucao do checklist. |
| `Criar tarefa` | Cria uma tarefa a partir de um passo que precisa de dono/prazo separado. |
| `Concluir` | Finaliza o checklist quando os criterios obrigatorios foram atendidos. |
| `Abrir origem` | Abre a superficie canonica relacionada, quando houver. |

## Relacao Com Tarefas

Checklist e diferente de Tarefa.

| Superficie | Papel |
| --- | --- |
| Checklists | Executar rotinas com varios passos. |
| Tarefas | Executar trabalho humano unitario com dono e prazo. |
| Hoje | Mostrar checklists relevantes do dia como parte da mesa de comando. |
| Operacao | Acompanhar pendencias que precisam andamento por etapa. |

Regra aprovada:

- um checklist pode criar tarefa;
- uma tarefa pode conter subtarefas/checklist interno;
- isso nao transforma toda rotina em tarefa;
- isso nao transforma toda tarefa em checklist.

## Estados Cobertos

- Em andamento;
- Bloqueado;
- Pendente;
- Em revisao;
- parcialmente concluido;
- item pendente dentro da execucao.

Estados futuros nao representados, mas esperados:

- concluido;
- atrasado;
- cancelado;
- reaberto;
- modelo inativo.

## Planos E Modos

| Plano/modo | Comportamento |
| --- | --- |
| 0 agentes | Checklists funcionam manualmente e por regras programaticas. |
| 1 agente | Agente pode sugerir passos apenas no dominio coberto. |
| 3 agentes | Checklists de dominios ativos podem receber sugestoes, pre-preenchimento e alertas. |
| 7 agentes | Todos os dominios podem receber apoio, respeitando permissao, cota, politica e auditoria. |
| Manual | Usuario executa, marca passos, comenta, cria tarefa, conclui e abre origem. |
| Copiloto | Sugere passo, identifica bloqueio, resume pendencia e recomenda proxima acao. |
| Autonomo | Pode marcar passos apenas quando houver evidencia objetiva e politica permitir. |

## O Que Nao Deve Aparecer

- Kanban como visualizacao principal;
- dashboard de KPIs;
- graficos grandes;
- automacao como centro da pagina;
- lista generica de tarefas;
- aprovacoes misturadas como checklists;
- historico profundo substituindo Auditoria.

## Referencias

- `design-system-round-4-1C-tarefas-image-plan.pt-BR.md`
- `hoje-actionable-item-taxonomy.pt-BR.md`
- `drawer-lifecycle-contracts.pt-BR.md`
- `canonical-data-model.pt-BR.md`
