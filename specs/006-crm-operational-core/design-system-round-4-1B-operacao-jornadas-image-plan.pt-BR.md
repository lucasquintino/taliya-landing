# Design System Web - Rodada 4.1B - Plano De Imagens Da Pagina Operacao

> Status: plano v0.2 apos simplificacao de produto. Objetivo: definir apenas as imagens necessarias para representar Operacao como um kanban operacional simples, sem criar complexidade de casos/jornadas profundas.

## Decisao Central

**Hoje** responde:

> O que precisa da minha atencao agora?

**Operacao** responde:

> Em que etapa estao as pendencias operacionais que ainda precisam acompanhamento?

Operacao nao deve ser:

- uma copia do Hoje;
- um dashboard generico;
- uma nova camada obrigatoria de caso operacional;
- uma lista completa de tarefas;
- uma fila completa de aprovacoes;
- um console de agentes;
- um mapa complexo de jornadas.

Operacao deve ser um **kanban operacional de pendencias acompanhadas**.

Cada card do kanban representa **1 item operacional unitario**. A pagina pode ter filtros, contadores e atividade recente agregada, mas o card em si nao deve agrupar varias conversas, varios alunos, varias reposicoes ou varias tarefas.

## Regra De Produto

Um item entra em Operacao quando precisa ser acompanhado ate resolver, mas continua tendo uma origem canonica.

Exemplos:

- uma reposicao sem encaixe vem de Agenda/Reposicoes;
- uma conversa aguardando humano vem de Inbox;
- um comprovante pendente vem de Financeiro;
- um telefone invalido vem de Dados/Contato;
- uma aprovacao pendente vem de Aprovacoes;
- um incidente de WhatsApp ou agente vem de Incidentes/Execucoes;
- uma tarefa atrasada vem de Tarefas.

Operacao mostra o andamento e a proxima acao, mas nao vira dona de todos os dados.

## Diferenca Entre Hoje, Operacao E Origens

| Superficie | Pergunta que responde | Papel |
| --- | --- | --- |
| Hoje | O que importa agora? | Mesa de comando do dia, priorizacao e acao imediata. |
| Operacao | O que ainda esta aberto e em que etapa esta? | Kanban de acompanhamento operacional. |
| Tarefas | Qual trabalho humano tenho que fazer? | Unidade de trabalho com dono e prazo. |
| Aprovacoes | Que decisao precisa ser tomada? | Fila de decisao com antes/depois, risco e auditoria. |
| Origem | Onde o dado mora e muda? | Agenda, Inbox, Financeiro, Dados, Uso/Cotas, Agentes etc. |

## Colunas Do Kanban

Usar 5 colunas simples:

| Coluna | Significado |
| --- | --- |
| Novo | Pendencia detectada, ainda nao assumida. |
| Assumido | Alguem ou uma fila ja esta cuidando. |
| Aguardando | Depende de aluno, responsavel, professor, pagamento, aprovacao ou provedor. |
| Bloqueado | Nao avanca por dado, permissao, cota, integracao, recurso ou regra. |
| Resolvido | Resultado registrado ou origem resolvida. |

## Tipos De Card

Um card de Operacao pode representar tipos diferentes, sempre com tipo real visivel:

- tarefa;
- bloqueio;
- aprovacao;
- conversa;
- financeiro;
- dados;
- agenda/reposicao;
- incidente;
- cota/uso;
- comunicado operacional.

O card nao precisa virar "caso" por padrao. Agrupar em caso pode existir no futuro como acao manual/avancada, mas nao e o conceito principal desta pagina.

Regra visual importante:

- nao criar cards agregados como "4 alunos", "3 conversas" ou "5 pagamentos";
- se houver muitos itens parecidos, usar contador/filtro no topo, mas manter cada card como item unico;
- cards de aprovacao devem parecer decisoes aguardando decisor, nao tarefas assumidas comuns;
- a coluna `Resolvido` deve aparecer mais leve, com poucos cards, para nao competir com o trabalho aberto.

## Rotas Do Grupo Operacao Para Imagens

As rotas principais do grupo Operacao ja estao mapeadas em documentos existentes, mas nem todas precisam de imagem nesta rodada.

| Topbar/superficie | Rota mapeada | Status para imagens |
| --- | --- | --- |
| Pendencias | `/app/operacao` | Sim, coberta pelas imagens 21 e 22 desta rodada. |
| Tarefas | `/app/tarefas`, `/app/tarefas/[taskId]` | Mapeada; imagem propria fica em rodada de Tarefas se necessario. |
| Checklists | `/app/checklists`, `/app/checklists/[runId]` | Mapeada; pode aparecer como origem/filtro, nao precisa imagem nesta rodada. |
| Aprovacoes | `/app/aprovacoes`, `/app/aprovacoes/[approvalId]` | Mapeada; imagem propria fica em rodada de Aprovacoes se necessario. |
| Incidentes | `/app/operacao/incidentes`, `/app/operacao/incidentes/[incidentId]` | Mapeada; nesta rodada aparece apenas como tipo de card. Detalhe profundo fica para Agentes/Execucoes/Incidentes. |
| Auditoria/Historico | `/app/auditoria`, `/app/auditoria/[eventId]` | Mapeada como superficie restrita; nesta rodada aparece so como atividade recente/historico curto. |

Portanto, para esta rodada, a rota visual principal e `/app/operacao`. As demais rotas ja existem como superficies, mas nao precisam ser geradas agora.

## Conteudo Minimo Do Card

Cada card deve mostrar:

- titulo curto;
- tipo real;
- origem canonica;
- dono ou fila;
- prazo ou janela critica quando existir;
- status/coluna;
- impacto curto;
- proxima acao.

Badges opcionais:

- bloqueado;
- aguardando aprovacao;
- cota;
- sem dono;
- risco alto;
- manual;
- copiloto;
- autonomo bloqueado.

## Sidebar/Drawer Por Tipo De Item

Ao clicar em um card, Operacao abre um sidebar/drawer lateral com uma **estrutura base comum**, mas o conteudo e as acoes mudam conforme o tipo real do item.

Estado padrao da pagina:

- `/app/operacao` carrega com o kanban visivel e nenhum drawer aberto;
- o drawer abre somente apos selecionar um card, usar uma acao de detalhe ou acessar uma rota direta de item;
- a imagem 22 mostra o estado selecionado para explicar o detalhe, nao o estado inicial da pagina.

Os drawers por tipo devem ser compartilhados entre **Hoje** e **Operacao**. Se um item do Hoje e um item de Operacao tem o mesmo tipo real, o drawer deve usar a mesma estrutura, os mesmos blocos principais e as mesmas acoes permitidas.

A diferenca entre as paginas e apenas o contexto de entrada:

- em Hoje, o drawer explica por que o item entrou na mesa de comando do dia;
- em Operacao, o drawer explica em que etapa a pendencia esta e por que precisa acompanhamento;
- o contrato do tipo continua o mesmo.

Estrutura base comum para todos:

- titulo do item;
- tipo real;
- origem canonica;
- dono ou fila;
- status atual;
- impacto;
- prazo/janela critica quando existir;
- motivo de estar em Operacao;
- proxima acao recomendada;
- historico curto;
- acoes permitidas;
- permissao, cota, politica ou bloqueio quando aplicavel.

Variacoes por tipo:

| Tipo de item | O sidebar deve enfatizar | Acoes principais esperadas |
| --- | --- | --- |
| Tarefa | dono, prazo, checklist/subpassos, comentario recente e origem. | abrir origem, assumir, delegar, concluir, reagendar. |
| Bloqueio | causa, objeto travado, impacto, dependencias e caminho para destravar. | abrir origem, assumir, criar tarefa, pedir aprovacao, mover status. |
| Aprovacao | proposta, antes/depois, risco, decisor, prazo e auditoria futura. | abrir aprovacao, aprovar/editar/rejeitar quando permitido, pedir dados. |
| Conversa | contato, responsavel/aluno, ultima mensagem, tempo em espera e motivo do handoff. | abrir conversa, assumir, responder, criar tarefa. |
| Financeiro | pagamento/cobranca, valor/status, comprovante, impacto e politica financeira. | abrir financeiro, validar, cobrar, criar tarefa, pedir aprovacao. |
| Dados | campo com problema, objeto afetado, impacto, confianca e origem do dado. | abrir cadastro, corrigir dado, pedir revisao, criar tarefa. |
| Agenda/Reposicao | aula/turma/aluno, vaga, prazo do credito, conflito e alternativas. | abrir agenda/reposicoes, reservar, criar tarefa, pedir aprovacao. |
| Incidente | canal/fluxo afetado, erro resumido, impacto, fallback e seguranca de reprocessamento. | abrir incidente, pausar fluxo, criar tarefa, reprocessar se seguro. |
| Cota/Uso | limite, consumo, fluxo afetado, downgrade e caminho manual. | abrir uso/cotas, ajustar economia, criar tarefa, pausar baixa prioridade. |

Regra:

- o visual do sidebar deve ser consistente;
- o conteudo deve ser especifico do tipo;
- a acao primaria deve respeitar a origem canonica;
- nao usar um drawer unico generico para todos os tipos;
- nao exibir acoes que nao fazem sentido para o tipo real do item.

## Imagens Necessarias

### 21. Operacao - Kanban Geral

Status:

**Aprovada v0.1.** Imagem salva no pacote local como `21_round-4.1B_operacao_01_kanban-geral.png.png`.

Arquivo esperado:

`21_round-4.1B_operacao_01_kanban-geral.png`

Origem local conhecida:

`D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/21_round-4.1B_operacao_01_kanban-geral.png.png`

Objetivo:

Mostrar a pagina principal `/app/operacao` como kanban operacional simples, com pendencias acompanhadas por etapa.

Estado representado:

- operacao ativa, com cards reais espalhados nas 5 colunas;
- nenhum drawer aberto;
- foco em acompanhamento, nao em urgencia do dia;
- mistura de origens: Agenda, Inbox, Financeiro, Dados, Aprovacoes, Incidentes e Tarefas.

Blocos principais:

- App Shell aprovado;
- grupo lateral `Operacao` ativo;
- topbar do grupo Operacao com `Pendencias`, `Tarefas`, `Aprovacoes`, `Incidentes`, `Historico` ou equivalente;
- topo com titulo `Operacao`, busca e filtros por origem, dono, tipo, status e bloqueio;
- coluna lateral interna com filtros compactos: minhas pendencias, sem dono, bloqueadas, aguardando resposta, cota/agente;
- centro com kanban de 5 colunas: `Novo`, `Assumido`, `Aguardando`, `Bloqueado`, `Resolvido`;
- cards com tipo real e origem canonica;
- area inferior parcialmente visivel com atividade recente ou pendencias resolvidas.

Exemplos de cards unitarios na imagem:

- `Reposicao da Ana sem encaixe` | Agenda | Bloqueio | Recepcao;
- `Comprovante da Marina para validar` | Financeiro | Tarefa | Financeiro;
- `Conversa da Julia aguardando humano` | Inbox | Conversa | Atendimento;
- `Telefone do responsavel invalido` | Dados | Bloqueio | Recepcao;
- `Aprovar mensagem de cobranca` | Aprovacoes | Decisao | Gestora;
- `WhatsApp com falha de envio` | Incidentes | Incidente | Sistema;
- `Confirmar substituto aula 18h` | Agenda | Tarefa | Coordenacao.

Regras especificas para esta imagem:

- reduzir a coluna `Resolvido` para poucos cards, no maximo 2 ou 3;
- reforcar badges de origem nos cards: `Agenda`, `Inbox`, `Financeiro`, `Dados`, `Aprovacoes`, `Sistema`;
- nao colocar card de aprovacao na coluna `Assumido` como tarefa comum; usar `Novo` ou `Aguardando`, com badge de decisao.

Componentes usados:

- App Shell `4.1S`;
- cards e containers `3A`;
- kanban/lista/atividade `3B.3`;
- filtros `3B.1`;
- badges/alertas `3B.2`;
- comunicacao/aprovacao/copiloto `3B.4`;
- cota/permissao/plano `3B.5`.

Comportamento manual/copiloto/autonomo:

- manual sempre disponivel: abrir origem, assumir, delegar, criar tarefa, pedir aprovacao e marcar resolvido quando permitido;
- copiloto pode resumir, priorizar e sugerir proxima acao;
- autonomo aparece apenas em cards seguros, como tarefa interna ou fallback permitido;
- se plano Base/0 agentes, a pagina continua funcionando com cards manuais/programaticos;
- se cota/plano bloqueia automacao, o card mostra caminho manual.

Relacao com tarefas, aprovacoes, bloqueios, incidentes e origem canonica:

- tarefa continua sendo tarefa e pode abrir Tarefas;
- aprovacao continua sendo aprovacao e abre Aprovacoes;
- bloqueio mostra causa e origem;
- incidente aparece como pendencia operacional, mas detalhe profundo fica em Incidentes/Execucoes;
- origem canonica fica visivel em todo card e e o destino principal para alterar dados.

O que nao deve aparecer:

- mapa complexo de jornadas;
- cards conectados por linhas;
- dashboard de KPI;
- grafico decorativo;
- lista completa de tarefas;
- fila completa de aprovacoes;
- cards que agrupam varios itens;
- console de agentes;
- explicacao textual ensinando o usuario a usar a pagina;
- promessa de resolver tudo com IA.

### 22. Operacao - Kanban Com Drawer De Item

Status:

**Aprovada v0.1.** Imagem salva no pacote local como `22_round-4.1B_operacao_02_kanban-com-drawer.png`.

Arquivo esperado:

`22_round-4.1B_operacao_02_kanban-com-drawer.png`

Origem local conhecida:

`D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/22_round-4.1B_operacao_02_kanban-com-drawer.png`

Objetivo:

Mostrar a mesma pagina com um card selecionado e drawer/painel lateral aberto, explicando como o usuario resolve sem criar uma entidade complexa.

Estado representado:

- card selecionado: `Reposicao da Ana sem encaixe`;
- coluna atual: `Bloqueado` ou `Novo`;
- origem canonica: Agenda/Reposicoes;
- drawer aberto com detalhe operacional e acoes.

Blocos principais:

- App Shell aprovado;
- kanban ao fundo com o card selecionado destacado;
- drawer/painel lateral com:
  - titulo do item;
  - tipo real: Bloqueio de agenda;
  - origem canonica: Agenda/Reposicoes;
  - impacto: Ana precisa repor ate sexta; turma atual sem vaga;
  - dono/fila: Recepcao;
  - prazo/janela critica;
  - motivo de estar em Operacao;
  - proxima acao recomendada;
  - historico curto;
  - itens vinculados simples, se existirem;
  - permissao/cota quando afetar acao com agente ou mensagem.

Acoes principais no drawer:

- abrir origem;
- assumir;
- delegar;
- criar tarefa;
- pedir aprovacao;
- marcar resolvido;
- mover status.

Componentes usados:

- drawer/painel `3B.2`;
- kanban `3B.3`;
- filtros `3B.1`;
- aprovacao/comunicacao `3B.4` quando houver sugestao;
- cota/permissao `3B.5`;
- timeline curta/atividade `3B.3`.

Comportamento manual/copiloto/autonomo:

- manual: usuario pode abrir origem, assumir, delegar, criar tarefa, pedir aprovacao e marcar resolvido se a origem permitir;
- copiloto: mostra resumo curto e sugestao de proxima acao, sem tomar decisao sensivel;
- autonomo: se houver, apenas como fallback seguro ou tarefa interna;
- no plano Base, o drawer continua completo sem sugestao de automacao.

Relacao com tarefas, aprovacoes, bloqueios, incidentes e origem canonica:

- se o usuario clicar `Criar tarefa`, nasce uma tarefa real em Tarefas;
- se clicar `Pedir aprovacao`, nasce uma aprovacao real em Aprovacoes;
- `Abrir origem` leva para Agenda/Reposicoes;
- `Marcar resolvido` so deve estar ativo quando a pendencia puder ser encerrada sem alterar dado sensivel fora da origem;
- o drawer nao duplica a tela Agenda inteira, so mostra contexto suficiente para decidir o proximo passo.

O que nao deve aparecer:

- pagina de detalhe separada de caso profundo;
- timeline longa;
- varios subcasos;
- botao de IA como acao primaria dominante;
- acao sensivel sem permissao/aprovacao;
- copia completa de Agenda, Financeiro ou Inbox dentro do drawer.
- card agrupando varios alunos ou varias pendencias.

## Contratos Funcionais Ainda Faltantes

Com a decisao de simplificar Operacao para kanban operacional, nao ha bloqueio funcional para gerar as duas imagens.

O ponto a atualizar em rodada posterior e harmonizar documentos antigos que ainda falam em "mapa de jornadas" ou "caso operacional profundo" como metafora principal. Para as imagens da Rodada 4.1B, este documento v0.2 vence.

## Regras Para Prompts Futuros

Quando os prompts forem escritos, eles devem:

- usar `16_round-4.1S_app-shell_01_base-web.png` como base obrigatoria;
- manter o estilo aprovado: CRM premium, operacional, denso, minimalista e claro;
- manter sidebar/topbar do shell;
- tratar Operacao como kanban de acompanhamento, nao como dashboard;
- preservar origem canonica em todos os cards;
- mostrar tipos reais, nao transformar tudo em tarefa;
- nao criar caso operacional complexo por padrao;
- usar exemplos cotidianos de studio de Pilates;
- mostrar IA como apoio discreto, nao como centro da pagina;
- manter caminho manual completo.

## Quantidade Final

Para a pagina Operacao, a cobertura recomendada agora e de **2 imagens**:

1. `21_round-4.1B_operacao_01_kanban-geral.png`;
2. `22_round-4.1B_operacao_02_kanban-com-drawer.png`.

Essas duas imagens bastam para fechar o conceito visual e funcional da pagina antes de escrever prompts.
