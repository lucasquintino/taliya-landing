# Design System Web - Rodada 4.1A - Plano De Imagens Da Pagina Hoje

> Status: plano v0.1 apos auditoria de foco. Objetivo: definir quantas imagens a pagina Hoje precisa e o que cada uma deve cobrir.

## Decisao

A pagina **Hoje** deve focar apenas no dia atual.

Este plano visual depende da taxonomia funcional definida em
`hoje-actionable-item-taxonomy.pt-BR.md`: Hoje nao e uma lista de tarefas,
e sim uma mesa de comando que agrega itens acionaveis vindos de tarefas,
aprovacoes, conversas, bloqueios, financeiro, agenda, agentes, dados e
notificacoes.

Ela nao deve virar:

- relatorio semanal;
- agenda semanal completa;
- painel de gestao geral;
- lista completa de tarefas;
- console de agentes;
- dashboard de KPIs soltos.

Ela deve responder:

> O que precisa acontecer hoje para o studio nao travar?

## Fronteiras

| Conteudo | Onde fica |
| --- | --- |
| Prioridades do dia | Hoje |
| Checklist e rotina do dia | Hoje |
| Proximas aulas de hoje | Hoje |
| Fila humana de hoje | Hoje como resumo acionavel; detalhe em Operacao/Inbox |
| Bloqueios de hoje | Hoje como resumo acionavel; detalhe na origem |
| Aprovacoes que vencem hoje | Hoje como resumo acionavel; detalhe em Aprovacoes |
| Cota que impacta uma acao de hoje | Hoje como alerta contextual; detalhe em Uso/Cotas |
| Agenda semanal | Agenda |
| Relatorio semanal | Relatorios/Semana |
| Tarefas completas por dono/prazo | Tarefas e Operacao |
| Incidentes e trace detalhado | Operacao/Incidentes |
| Console completo de agentes | Agentes/Fluxos |

## Regra De Origem Dos Itens

Todo item exibido no Hoje precisa ter uma origem canonica.

| Item no Hoje | Origem canonica |
| --- | --- |
| Item do checklist do dia | Checklist |
| Aula de hoje | Agenda/Aula |
| Conversa aguardando humano | Inbox/Conversa |
| Reposicao sem encaixe | Agenda/Reposicoes |
| Bloqueio de professor, sala ou recurso | Agenda/Operacao |
| Tarefa com dono e prazo | Tarefas |
| Aprovacao pendente | Aprovacoes |
| Pagamento, cobranca ou comprovante | Financeiro |
| Cota ou economia | Uso/Cotas |
| Incidente de agente/integracao | Operacao/Incidentes ou Agentes/Execucoes |
| Problema de dados | Qualidade de dados ou perfil do objeto |

O item so vira tarefa quando exige trabalho humano separado, com dono, prazo
e acompanhamento. Caso contrario, ele abre a origem, cria/abre caso
operacional ou abre aprovacao.

## Imagens Necessarias

### 17. Hoje - Acima Da Dobra

Arquivo esperado:

`17_round-4.1A_hoje_01_acima-da-dobra.png`

Objetivo:

Mostrar a visao principal do dia.

Deve conter:

- App Shell aprovado;
- titulo `Hoje`;
- data do dia;
- topbar do grupo Hoje;
- checklist do dia;
- proximas aulas de hoje;
- subcontainers grandes por bloco de acao do dia ocupando a maior parte do canvas;
- nenhum painel direito fixo;
- indicacoes compactas de cota somente dentro da prioridade afetada;
- inicio de gargalos de hoje parcialmente visivel.

Nao deve conter:

- resumo semanal;
- relatorio;
- graficos;
- secoes de agentes pausados como bloco proprio;
- dashboard de KPIs sem acao.
- drawer aberto.

Estrutura recomendada da imagem 1:

- coluna esquerda estreita: checklist do dia e proximas aulas;
- centro em grid de subcontainers:
  - Agora;
  - Fila humana;
  - Tarefas de hoje;
  - Bloqueios de hoje;
  - Dinheiro que exige acao hoje;
  - Aprovacoes de hoje.

Cada subcontainer deve ter poucos cards acionaveis, com titulo curto, status, responsavel/prazo quando fizer sentido e atalho para abrir origem.
Os cards da imagem 1 nao exibem botoes de acao internos. Eles apenas indicam que sao selecionaveis. As acoes aparecem somente apos clique, no drawer/painel da imagem 2.

Todos os blocos da imagem 1 devem ter drawer especifico mapeado: Agora,
Checklist do dia, Aulas de hoje, Fila humana, Bloqueios de hoje, Tarefas de
hoje, Aprovacoes de hoje e Dinheiro hoje.

### 18. Hoje - Drawer De Tarefa

Arquivo esperado:

`18_round-4.1A_hoje_02_drawer-tarefa.png`

Objetivo:

Mostrar o que acontece quando o gestor decide agir em uma prioridade do dia
que ja e uma **tarefa humana**.

Deve conter:

- tarefa selecionada no bloco `Tarefas de hoje`;
- drawer/painel lateral aberto apos selecao da tarefa;
- tipo real exibido como `Tarefa`;
- origem do problema;
- dono ou fila;
- prazo;
- prioridade;
- objeto afetado;
- checklist/subpassos quando existir;
- comentarios ou ultima atividade;
- botoes manuais: abrir conversa, concluir com resultado estruturado, reagendar, delegar, abrir origem;
- sugestao do copiloto se aplicavel;
- cota/permissao apenas se a tarefa envolver mensagem, agente ou acao sensivel.

Exemplo aprovado:

- tarefa: `Confirmar reposicao com Ana Paula`;
- origem canonica: `Agenda / Reposicoes`;
- criacao: `Criada por regra do CRM as 09:12`;
- acao principal: `Abrir conversa`;
- conclusao: `Concluir` deve abrir resultado estruturado.

Nao deve sugerir que esse drawer serve para todos os tipos do Hoje. Agora,
Checklist do dia, Aulas de hoje, Fila humana, bloqueio, aprovacao,
financeiro, alerta/cota, incidente e problema de dados tem drawers
especificos definidos em `hoje-actionable-item-taxonomy.pt-BR.md`.

### 19. Hoje - Estado Critico Do Dia

Arquivo esperado:

`19_round-4.1A_hoje_03_estado-critico-do-dia.png`

Objetivo:

Mostrar a pagina quando o dia esta sob risco operacional.

Deve conter pelo menos tres tipos de problema:

- fila humana acima do normal;
- bloqueio de agenda/recurso/professor;
- cota 90% ou 100% impactando automacao;
- aprovacao urgente vencendo hoje;
- dinheiro que bloqueia aula ou exige acao hoje.

Deve deixar claro:

- o que esta bloqueado;
- o que ainda pode ser feito manualmente;
- o que o agente nao pode executar;
- quais acoes resolvem o dia.

### 20. Hoje - Historico De Hoje

Arquivo esperado:

`20_round-4.1A_hoje_04_historico-de-hoje.png`

Objetivo:

Mostrar a area abaixo da dobra da pagina Hoje.

Deve conter:

- scroll leve da pagina Hoje, com parte da primeira dobra ainda visivel;
- apenas um novo container principal abaixo da dobra;
- container `Historico de hoje` ocupando praticamente toda a largura util;
- timeline/lista cronologica do que ja foi resolvido, alterado, executado ou decidido hoje;
- itens com horario, tipo, origem, ator, resultado e link discreto para origem.

Nao deve duplicar os blocos de acao da primeira dobra. Historico responde
`o que ja aconteceu hoje`, enquanto os blocos acima respondem `o que ainda
precisa de acao hoje`.

## Quantidade Final

Para a pagina Hoje, a cobertura recomendada e de **4 imagens**:

1. acima da dobra;
2. drawer de tarefa;
3. estado critico do dia;
4. historico de hoje abaixo da dobra.

As quatro imagens cobrem a primeira dobra, um drawer real, pressao operacional
e a memoria operacional abaixo da dobra.
