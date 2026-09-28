# Design System Web - Rodada 4.1C - Pagina Tarefas

> Status: aprovada v0.1. Esta pagina foi fechada com 1 imagem porque usa lista densa + detalhe lateral e herda o contrato compartilhado de drawer do tipo Tarefa.

## Decisao Central

**Tarefas** responde:

> Quem precisa fazer o que, ate quando, e de onde veio essa tarefa?

Tarefas nao e:

- Hoje;
- Operacao;
- Aprovacoes;
- kanban principal;
- dashboard;
- fila de decisoes;
- lista de pendencias de varios tipos.

Tarefas e a superficie de **trabalho humano real**, com dono, prazo, status, origem e conclusao.

## Relacao Com Outras Paginas

| Superficie | Papel |
| --- | --- |
| Hoje | Prioriza o que precisa atencao agora. |
| Operacao | Acompanha pendencias operacionais por etapa. |
| Tarefas | Lista trabalho humano com dono e prazo. |
| Aprovacoes | Decide propostas/acoes sensiveis. |
| Origem | Guarda e altera o dado real. |

## Layout Aprovado

Tarefas usa:

- App Shell aprovado;
- topbar do grupo com `Tarefas` ativo;
- filtros por dono, prazo, origem, status e prioridade;
- botao `Criar tarefa`;
- coluna esquerda com filas;
- lista/tabela densa no centro;
- painel lateral com detalhe da tarefa selecionada.

Estado padrao:

- `/app/tarefas` carrega com lista e filtros, sem painel/drawer de detalhe aberto;
- o painel lateral abre apos selecionar uma tarefa, criar uma tarefa ou acessar `/app/tarefas/[taskId]`;
- a imagem 23 mostra tarefa selecionada para documentar o detalhe, nao o estado inicial obrigatorio.

Nao usar kanban como visualizacao principal. Kanban pode existir como visualizacao futura/opcional, mas a pagina base e lista densa.

## Imagem Aprovada

### 23. Tarefas - Lista E Detalhe

Status:

**Aprovada v0.1.** Imagem salva no pacote local como `23_round-4.1C_tarefas_01_lista-detalhe.png.png`.

Arquivo esperado:

`23_round-4.1C_tarefas_01_lista-detalhe.png`

Origem local conhecida:

`D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/23_round-4.1C_tarefas_01_lista-detalhe.png.png`

Objetivo:

Mostrar `/app/tarefas` como lista densa de trabalho humano, com uma tarefa selecionada e painel lateral de detalhe.

Estado representado:

- tarefa selecionada: `Confirmar reposicao da Ana`;
- origem canonica: Agenda/Reposicoes;
- dono/fila: Recepcao;
- prazo: Hoje;
- checklist/subtarefas;
- comentarios;
- historico curto;
- copiloto discreto;
- acoes manuais.

## Drawer Compartilhado

O painel lateral da imagem 23 usa o **mesmo contrato de drawer do tipo Tarefa** definido em `drawer-lifecycle-contracts.pt-BR.md`.

Esse drawer deve ser o mesmo quando uma tarefa for aberta a partir de:

- Hoje;
- Operacao;
- Tarefas;
- origem canonica;
- busca global.

A diferenca entre paginas e somente o contexto:

- em Hoje, o drawer explica por que a tarefa subiu hoje;
- em Operacao, explica em que etapa/acompanhamento a tarefa esta;
- em Tarefas, mostra a execucao direta do trabalho humano.

O tipo real continua sendo `Tarefa`; portanto, blocos e acoes devem ser consistentes.

Regra do painel lateral:

- por padrao, `/app/tarefas` pode carregar sem tarefa selecionada;
- a imagem 23 mostra um estado selecionado, nao o estado inicial obrigatorio;
- o painel lateral muda conforme a tarefa clicada, mantendo o mesmo contrato base de Tarefa;
- variacoes de origem, prazo, status, bloqueio, aprovacao vinculada ou checklist vinculado nao exigem nova imagem propria nesta rodada.

Modos principais do painel de Tarefa:

| Item clicado | Painel lateral deve mostrar |
| --- | --- |
| Tarefa aberta | Dono, prazo, origem, checklist/subtarefas, comentarios, historico curto e acoes de assumir, concluir, delegar ou comentar. |
| Tarefa atrasada | Motivo do atraso, impacto, dono atual, proxima acao segura e opcoes de reagendar, delegar ou escalar. |
| Tarefa aguardando resposta | Canal/origem, ultima tentativa, prazo de retorno e acoes de cobrar retorno, criar lembrete ou encerrar com motivo. |
| Tarefa bloqueada | Bloqueio, origem canonica, quem pode remover, acao manual permitida e ausencia de automacao quando houver risco. |
| Tarefa com aprovacao vinculada | Decisao pendente, impacto, link para aprovacao e acoes limitadas ate decisao. |
| Tarefa concluida/cancelada | Resumo auditavel, quem concluiu/cancelou, evidencias e acoes restritas de reabrir quando permitido. |
| Criar tarefa | Formulario curto com titulo, dono/fila, prazo, origem opcional, prioridade e checklist/subtarefas se necessario. |

## Conteudo Minimo Da Lista

Cada linha deve mostrar:

- titulo da tarefa;
- dono/fila;
- prazo;
- status;
- origem canonica;
- prioridade;
- ultima atividade;
- modo: manual, copiloto, autonomo bloqueado ou sem IA.

## Estados Cobertos

- Aberta;
- Em andamento;
- Aguardando;
- Atrasada;
- Sem dono;
- Concluida.

## Planos E Modos

| Plano/modo | Comportamento |
| --- | --- |
| 0 agentes | Tarefas funcionam manualmente e por regra programatica. |
| 1 agente | Copiloto atua se o dominio da tarefa estiver coberto pelo agente ativo. |
| 3 agentes | Copiloto/autonomia segura podem aparecer nos dominios ativos. |
| 7 agentes | Todos os dominios podem ter apoio, respeitando permissao, cota, politica e risco. |
| Manual | Criar, assumir, concluir, delegar, reagendar, comentar e abrir origem. |
| Copiloto | Sugere prioridade, checklist, resumo, comentario e proxima acao. |
| Autonomo | Pode criar tarefa segura e concluir apenas com evidencia objetiva; nao conclui julgamento humano sensivel. |

## O Que Nao Deve Aparecer

- kanban como visualizacao principal;
- aprovacoes tratadas como tarefas;
- cards agregados;
- dashboard de indicadores;
- IA como acao principal;
- detalhe profundo de Operacao;
- copia completa da origem dentro do painel.

## Cobertura

Uma imagem e suficiente para fechar Tarefas nesta rodada porque:

- a lista densa esta clara;
- o painel lateral usa contrato compartilhado de drawer;
- estados e modos aparecem na propria lista;
- criacao/edicao profunda pode usar drawer/modal ja coberto por `3B.2`.

## Cobertura Da Rota De Detalhe

Rota:

`/app/tarefas/[taskId]`

Decisao:

Nao precisa imagem propria nesta rodada.

A rota de detalhe da tarefa herda:

- imagem `23_round-4.1C_tarefas_01_lista-detalhe.png`;
- contrato compartilhado do drawer de tipo `Tarefa`;
- componentes de drawer/painel `3B.2`;
- lista/timeline/comentarios `3B.3`;
- estados e ciclos definidos em `drawer-lifecycle-contracts.pt-BR.md`.

Quando acessada por URL direta, a rota pode renderizar o mesmo conteudo do drawer em uma superficie expandida, mantendo os mesmos campos, acoes e regras.

So deve ganhar imagem propria no futuro se adicionar comportamento novo, como:

- editor avancado;
- anexos longos;
- dependencias complexas;
- comentarios em thread;
- historico/auditoria longa;
- automacoes especificas de tarefa.

Mobile fica para rodada propria: lista de tarefas com filtros em chips/bottom sheet e detalhe em tela cheia ou bottom sheet.
