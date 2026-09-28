# Design System Web - Rodada 4.1F - Pagina Agenda

> Status: aprovada v0.1. Objetivo: registrar a primeira imagem da familia Agenda / Aulas / Reposicoes, usando `/app/agenda` como calendario operacional do studio.

## Decisao Central

**Agenda** responde:

> O que acontece na agenda do studio esta semana/dia, quais aulas precisam acao, onde ha vaga, conflito, chamada pendente ou reposicao possivel?

Agenda nao e:

- calendario pessoal generico;
- dashboard de indicadores;
- kanban;
- lista de tarefas;
- tela completa de chamada;
- tela completa de reposicoes;
- configuracao estrutural completa de grade/turmas.

Agenda e a superficie operacional para ver aulas reais, abrir uma aula, fazer chamada, encontrar encaixe e tratar conflitos do dia/semana.

## Imagem Aprovada

### 26. Agenda - Calendario Operacional

Status:

**Aprovada v0.1 com observacoes.** Imagem salva no pacote local como `26_round-4.1F_agenda_01_calendario-operacional.png.png`.

Arquivo esperado:

`26_round-4.1F_agenda_01_calendario-operacional.png`

Origem local conhecida:

`D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/26_round-4.1F_agenda_01_calendario-operacional.png.png`

Observacao de numeracao:

A numeracao canonica desta imagem e `26`. A sugestao anterior com prefixo `25` nao deve ser usada.

## Estado Representado

A imagem mostra:

- app shell web aprovado;
- pagina `Agenda`;
- topbar interna com `Agenda`, `Turmas`, `Chamada`, `Reposicoes`, `Historico`;
- modo `Semana` ativo;
- navegacao de periodo com setas, botao `Hoje` e periodo `12-18 maio`;
- filtros por professor, turma, sala e status;
- calendario semanal com aulas de Pilates;
- mini calendario e filtros rapidos na lateral interna;
- aula selecionada no calendario;
- painel direito com detalhe da aula selecionada;
- acoes: abrir aula, fazer chamada, encontrar encaixe e avisar envolvidos;
- copiloto discreto explicando credito de reposicao compativel;
- regra visual de 0 agentes: agenda e chamada continuam operaveis manualmente.

## Blocos Principais

| Zona | Conteudo |
| --- | --- |
| Topo da pagina | Titulo `Agenda`, subtitulo do studio, modo Dia/Semana, periodo, filtros e botao `Criar aula`. |
| Esquerda interna | Mini calendario e filtros rapidos: Hoje, Chamada pendente, Vagas abertas, Conflitos, Reposicoes. |
| Centro | Calendario semanal com cards de aula por horario/dia. |
| Direita | Detalhe da aula selecionada, capacidade, alunos previstos, alerta de reposicao, proximas acoes e copiloto. |

## Regra Do Painel Direito Da Agenda

O painel direito da Agenda e contextual ao card ou alerta selecionado.

- por padrao, `/app/agenda` pode carregar sem painel aberto ou com a proxima aula relevante selecionada em desktop largo;
- a imagem 26 mostra uma aula selecionada, nao o estado inicial obrigatorio;
- o painel muda conforme o item clicado no calendario, filtro rapido ou alerta;
- o painel da Agenda mostra contexto suficiente para agir ou abrir a origem, sem copiar a pagina de Aula, Reposicoes ou Recursos inteira.

Modos principais do painel da Agenda:

| Item clicado | Painel direito deve mostrar |
| --- | --- |
| Aula confirmada | Resumo da aula, ocupacao, professor/recurso se houver, alunos previstos e acoes de abrir aula, avisar turma ou fazer chamada. |
| Aula com chamada pendente | Status da chamada, alunos pendentes, acao principal para abrir aula/chamada e alerta de auditoria. |
| Aula com vaga/reposicao possivel | Vaga, credito compativel, acao de encontrar encaixe e link para Reposicoes. |
| Aula lotada/conflito | Motivo do conflito, impacto, quem resolve e acoes de ajustar, avisar ou criar tarefa. |
| Filtro rapido selecionado | Lista curta de itens do filtro, contadores e primeira acao segura. |
| Recurso/professor indisponivel | Dependencia afetada, aulas impactadas e caminho para ajuste manual. |

## Rotas Cobertas

| Rota | Decisao |
| --- | --- |
| `/app/agenda` | Coberta pela imagem 26. |
| `/app/aulas/[id]` | Precisa 1 imagem propria com detalhe da aula e painel/drawer de chamada ativo. |
| `/app/aulas/[id]/chamada` | Nao e rota principal nesta rodada; chamada e acao contextual dentro de `/app/aulas/[id]`. Pode existir no futuro apenas como deep link tecnico. |
| `/app/turmas` | Coberta pela imagem 35. Workspace de estrutura recorrente, lista de turmas e detalhe lateral. |
| `/app/turmas/[id]` | Herda `/app/turmas`: pode abrir detalhe lateral/rota expandida da turma recorrente sem imagem propria separada. |
| `/app/grade` | Coberta pela imagem 36. Visao de grade recorrente/semana-modelo para criar/ver/editar turmas recorrentes. |
| `/app/eventos` | Lista/workspace de eventos e aulas especiais. Herda Turmas/Agenda inicialmente; imagem propria so se eventos virarem modulo forte no produto. |
| `/app/eventos/[eventId]` | Herda detalhe de Evento dentro do padrao Turma/Aula; sem imagem propria nesta rodada. |
| `/app/reposicoes` | Precisa 1 imagem propria para visualizar e resolver o fluxo completo de reposicao e encaixe. |
| `/app/creditos-reposicao` | Nao e pagina principal nesta rodada; credito aparece dentro da reposicao. Pode existir futuramente como consulta/relatorio. |
| `/app/lista-espera` | Nao pertence a Reposicoes nesta rodada; lista de espera geral e superficie separada/futura. |
| `/app/recursos`, `/app/recursos/[resourceId]` | Nao entram como pagina principal nesta rodada. Recurso/sala/equipamento e campo opcional em Agenda, Aula, Grade e Bloqueios. |

## Decisao: Turmas, Grade, Eventos E Bloqueios

### `/app/turmas`

Papel:

- gerenciar turmas recorrentes do studio;
- responder quais turmas existem, em quais horarios, com qual capacidade, quais alunos fixos e quais vagas;
- operar mudancas estruturais com impacto antes de publicar.

Blocos:

- busca e filtros por status, horario, professor opcional, capacidade e vaga;
- lista densa de turmas;
- painel contextual da turma selecionada;
- alunos fixos;
- proximas aulas geradas;
- historico curto de mudancas;
- acoes de criar turma, pausar, encerrar, ajustar horario, mover aluno e avisar turma.

### `/app/turmas/[id]`

Papel:

- detalhe profundo de uma turma recorrente;
- nao e a mesma coisa que `/app/aulas/[id]`: turma e regra recorrente, aula e ocorrencia concreta.

Conteudo:

- resumo da turma;
- horario recorrente;
- capacidade;
- alunos fixos;
- proximas aulas;
- reposicoes/encaixes ligados;
- historico e auditoria;
- mudancas com simulacao de impacto.

Decisao visual:

- sem imagem propria obrigatoria nesta rodada;
- herda o painel/detalhe de `/app/turmas`;
- se acessada por URL direta, renderiza o mesmo conteudo do painel em superficie expandida.

### `/app/grade`

Papel:

- editar a semana-modelo recorrente do studio;
- mostrar o que acontece toda semana, nao o calendario real de uma semana especifica;
- criar, mover, pausar e ajustar turmas/blocos recorrentes;
- permitir bloqueio apenas como acao situacional quando o usuario esta tratando indisponibilidade, feriado, recesso ou horario fechado.

Diferenca para Agenda:

| Rota | Papel |
| --- | --- |
| `/app/agenda` | Operar aulas reais por data, chamada, reposicao, conflito e aviso do dia. |
| `/app/grade` | Configurar a estrutura recorrente que gera aulas futuras. |

Imagem:

- recomendada 1 imagem propria para Turmas/Grade;
- essa imagem deve mostrar `/app/grade` como semana-modelo de turmas recorrentes;
- foco visual: criar/ver/editar turmas recorrentes, capacidade, vagas e horarios;
- bloqueio pode aparecer como estado secundario ou acao contextual discreta, mas nao como botao principal dominante nem como objetivo central da pagina;
- a mesma imagem cobre `/app/turmas` se mostrar lista ou seletor de visualizacao `Lista` / `Grade`.

### `/app/eventos`

Papel:

- gerenciar eventos, workshops, aulas especiais ou turmas temporarias;
- nao substituir Turmas fixas nem Agenda do dia.

Conteudo:

- lista de eventos;
- data/horario;
- capacidade;
- inscricoes;
- status;
- comunicacao;
- chamada quando o evento acontecer.

Decisao visual:

- nao precisa imagem propria agora;
- herda Turmas para estrutura/capacidade e Aula para execucao/chamada;
- gerar imagem propria so se eventos/workshops virarem um modulo comercial importante.

### `/app/eventos/[eventId]`

Papel:

- detalhe de evento/aula especial;
- mostra inscricoes, capacidade, lista de espera do evento, comunicacoes e chamada.

Decisao visual:

- sem imagem propria nesta rodada;
- herda detalhe de Turma/Aula.

## Bloqueios De Agenda

O studio precisa conseguir iniciar indisponibilidade, feriado, recesso e bloqueio de horario sem depender de uma pagina de Recursos.

Objeto canonico:

`Bloqueio de agenda`

Tipos:

- feriado;
- recesso;
- fechamento pontual do studio;
- professor indisponivel;
- horario bloqueado;
- sala/equipamento/recurso indisponivel, quando o studio usa esse controle.

Onde inicia:

- acao secundaria `Bloquear horario` em `/app/agenda`, ao selecionar um horario, aula ou conflito;
- menu de mais acoes em `/app/grade`, ao selecionar um bloco/horario recorrente;
- menu de mais acoes em `/app/turmas/[id]`, quando o bloqueio afeta aquela turma;
- opcionalmente a partir de uma aula/turma afetada;
- nao deve competir com `Criar turma`, `Editar bloco` ou `Simular impacto` como acao primaria da Grade.

Campos minimos:

- tipo;
- periodo;
- recorrencia, se houver;
- escopo: studio inteiro, turma, professor, horario ou recurso opcional;
- motivo;
- impacto simulado;
- plano de aviso;
- politica de compensacao/reposicao quando aplicavel.

Controle de compensacao no drawer:

- o drawer do bloqueio deve ter uma secao `Compensacao`;
- essa secao mostra a politica padrao aplicada pelo studio antes da publicacao;
- a decisao de gerar ou nao credito de reposicao fica no drawer do bloqueio, como consequencia do impacto, nao como funcao solta da Grade;
- opcoes esperadas: `Seguir politica do studio`, `Gerar credito de reposicao`, `Nao gerar credito`, `Revisar aluno por aluno`;
- se `Seguir politica do studio` estiver ativo, o drawer deve explicar a regra, por exemplo: `Feriado previsto nao gera credito`;
- se `Gerar credito de reposicao` estiver ativo, o drawer deve mostrar alunos afetados, creditos previstos, validade e origem `Bloqueio de agenda`;
- se `Revisar aluno por aluno` estiver ativo, o drawer deve listar os alunos afetados com consequencia individual: `gera credito`, `nao gera credito` ou `revisar`;
- a decisao pode exigir permissao ou aprovacao quando mudar regra financeira/contratual sensivel.

Comportamento:

- antes de publicar, o sistema mostra aulas, alunos, professores e reposicoes afetados;
- usuario decide entre cancelar, reagendar, gerar credito, nao gerar credito, revisar aluno por aluno, criar tarefas, avisar envolvidos ou apenas bloquear novas aulas;
- creditos gerados por bloqueio aparecem depois em `/app/reposicoes` com origem, validade, politica e aula afetada;
- copiloto pode resumir impacto e redigir aviso;
- copiloto pode explicar consequencia de compensacao, mas nao decide compensacao sensivel sozinho;
- autonomo so envia avisos ou cria tarefas quando politica, consentimento, cota, template e risco permitirem; nao altera compensacao sensivel sozinho;
- sem agentes, tudo funciona manualmente e por simulacao programatica.

Decisao sobre `/app/recursos`:

- nao criar pagina principal de Recursos agora;
- recurso/sala/equipamento continua opcional;
- se o studio nao usa recursos, a UI deve falar em `Bloqueios` e `Indisponibilidade`, nao em recurso;
- catalogo de recursos pode existir futuramente em Configuracoes, mas nao e necessario para operar feriados, recessos e bloqueios de horario.

## Imagens Aprovadas: Turmas E Grade

### 35. Turmas - Lista E Detalhe

Imagem aprovada:

`35_round-4.1F_turmas_01_lista-detalhe.png`

Arquivo local esperado:

`D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/35_round-4.1F_turmas_01_lista-detalhe.png.png`

Status:

aprovada v0.1

Objetivo:

Mostrar `/app/turmas` como workspace de turmas recorrentes, com lista densa, filtros e painel lateral da turma selecionada.

Cobertura:

- rota `/app/turmas`;
- rota `/app/turmas/[id]` por heranca do painel/detalhe;
- turmas recorrentes com horario, capacidade, professor opcional, alunos fixos, vagas, proxima aula, status e ultima mudanca;
- painel lateral de turma selecionada com alunos fixos, proximas aulas, historico, impacto e acoes estruturais.

Observacoes da aprovacao:

- a imagem comunica bem composicao recorrente, sem virar Agenda ou Aula;
- `Recurso/equipamento` aparece como opcional e discreto;
- drawer/painel representa estado selecionado, nao carregamento padrao;
- outros modos do painel de turma herdam a mesma estrutura: cheia, com vaga, pausada, professor a definir, aluno fixo selecionado ou mudanca pendente.

### 36. Grade - Semana-Modelo

Imagem aprovada:

`36_round-4.1F_grade_01_semana-modelo-bloqueio.png`

Arquivo local esperado:

`D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/36_round-4.1F_grade_01_semana-modelo-bloqueio.png.png`

Status:

aprovada v0.1 com ressalva funcional

Objetivo:

Mostrar `/app/grade` como semana-modelo recorrente do studio, usada para criar, ver e editar turmas/blocos recorrentes que geram aulas futuras.

Cobertura:

- rota `/app/grade`;
- grade recorrente sem datas reais;
- blocos recorrentes por dia/horario;
- capacidade, alunos fixos, vagas, professor opcional e recurso opcional;
- painel lateral de bloco recorrente selecionado;
- impacto de alteracao futura em alunos e aulas geradas;
- bloqueio aplicado como exemplo de excecao situacional na grade.

Ressalva funcional obrigatoria:

- Grade nao e uma pagina de bloqueios;
- `Criar bloqueio` nao deve ser acao primaria dominante da Grade;
- bloqueio aparece como estado aplicado ou acao situacional/secundaria, acionada por menu/contexto;
- o foco da Grade continua sendo criar/ver/editar turmas recorrentes, horarios, capacidade, vagas e blocos recorrentes.

## Observacoes Da Aprovacao

Pontos aceitos sem regenerar a imagem:

- mini calendario mostra `maio 2024`; em prompts futuros e implementacao, usar ano/periodo consistente com o contexto do produto;
- painel direito tem `X`; tratar como controle de recolher painel, nao modal/drawer sobreposto;
- `Chamada` na topbar deve ser entendida como atalho/filtro para aulas com chamada, nao necessariamente rota raiz principal;
- muitos cards aparecem como `confirmada`; proximas imagens devem variar melhor entre chamada pendente, vaga aberta, lotado, conflito, reposicao e cancelada/ajuste.

## Modos De Visualizacao

Agenda deve suportar:

- `Dia`;
- `Semana`;
- navegacao anterior/proximo;
- botao `Hoje`;
- seletor/periodo visivel;
- filtros por professor, turma, sala/recurso e status.

`Mes` nao e modo principal nesta rodada. Pode existir futuramente como consulta, mas a operacao real do studio acontece em dia/semana.

## Manual, Copiloto E Autonomo

| Modo | Comportamento |
| --- | --- |
| 0 agentes | Agenda, chamada, abertura de aula, encaixe e aviso manual continuam funcionando. |
| Manual | Usuario abre aula, faz chamada, altera permitido, encontra encaixe e avisa envolvidos. |
| Programatico | CRM calcula vagas, capacidade, conflitos, chamada pendente e candidatos de reposicao sem IA. |
| Copiloto | Explica conflito, sugere encaixe, redige convite e resume impacto. |
| Autonomo | Apenas envia convite/lembrete seguro quando politica, consentimento, cota, template e risco permitirem. Nao altera agenda sensivel sozinho. |

## O Que Nao Deve Aparecer

- dashboard com graficos;
- kanban;
- conversa de WhatsApp como foco principal;
- financeiro completo;
- historico sensivel completo;
- tela de configuracao estrutural completa;
- IA alterando agenda sozinha;
- modal/drawer cobrindo o calendario como estado principal.

## Proximo Passo Da Familia

Depois da Agenda, a imagem seguinte aprovada e:

`29_round-4.1F_aula_01_detalhe-com-chamada.png`

Motivo:

Chamada e execucao de aula usam interacao diferente do calendario, mas nao precisam de rota separada. A aula e a superficie principal; a chamada abre como painel/drawer contextual com roster de alunos, presenca, falta, no-show, observacao, credito de reposicao e auditoria.

## Contrato Da Pagina Aula

Rota principal:

`/app/aulas/[id]`

Decisao:

- usar uma unica rota web para detalhe da aula;
- nao criar `/app/aulas/[id]/chamada` como pagina separada nesta rodada;
- `Fazer chamada` abre painel/drawer lateral dentro da pagina da aula;
- a pagina da aula pode abrir outros drawers contextuais, como detalhe do aluno, reposicao, observacao, conflito ou aviso;
- a imagem 29 mostra a aula aberta com o painel/drawer de chamada ativo.

Pergunta que a pagina responde:

> O que esta acontecendo nesta aula especifica e quais acoes precisam ser tomadas nela?

Blocos da pagina:

| Zona | Conteudo |
| --- | --- |
| Topo | Aula, data/horario, turma, professor quando houver, sala/equipamento/recurso quando houver, status da chamada e acoes principais. |
| Centro | Resumo da aula, alunos esperados, capacidade, reposicoes vinculadas, observacoes e eventos curtos. |
| Lateral/drawer de chamada | Lista de alunos com controles de presenca, falta avisada, no-show, observacao e consequencia. |
| Outros drawers contextuais | Detalhe do aluno, reposicao, conflito, observacao, aviso ou correcao de chamada. |

## Regras De Dados Da Aula

Professor:

- professor nao e obrigatoriamente fixo;
- pode existir professor atribuido por aula;
- pode aparecer como `A definir`;
- pode mudar por substituicao;
- a UI nao deve tratar professor fixo como premissa universal da turma.

Sala/equipamento/recurso:

- sao opcionais;
- studios podem nao usar sala, equipamento ou recurso como controle formal;
- quando nao existirem, nao devem ocupar area central da interface;
- quando existirem, podem aparecer como metadado discreto da aula e como origem de conflito.

Capacidade:

- capacidade e o limite operacional da aula/turma naquele horario;
- alunos esperados devem bater com a capacidade, salvo quando a tela mostrar conflito explicito;
- reposicao encaixada conta na ocupacao da aula;
- se esperados > capacidade, o estado deve aparecer como excesso/conflito, por exemplo `5/4`.

Drawers da aula:

| Drawer | Papel |
| --- | --- |
| Chamada | Marcar presenca, falta avisada, no-show, observacao curta e consequencia imediata. |
| Detalhe do aluno | Mostrar contexto permitido do aluno selecionado sem transformar a aula em perfil completo. |
| Reposicao | Criar/usar credito, reservar vaga e ver conflito de encaixe. |
| Observacao | Registrar observacao da aula ou do aluno. |
| Conflito | Explicar excesso, professor ausente, recurso indisponivel ou politica bloqueante. |
| Aviso | Preparar mensagem para turma/aluno/responsavel quando permitido. |

Regra do drawer de chamada:

- deve ser transacional e rapido;
- nao deve concentrar todo o contexto do aluno;
- contexto detalhado do aluno deve abrir no drawer de detalhe do aluno;
- botao principal e `Salvar chamada`;
- consequencias aparecem curtas junto ao aluno: `gera credito`, `nao gera credito`, `reposicao usada`, `requer revisao`.

Estados que a imagem 29 deve mostrar:

- chamada em andamento;
- aluno presente;
- falta avisada que gera credito;
- no-show;
- aluno pendente;
- aluno encaixado por reposicao;
- observacao operacional;
- capacidade coerente com alunos esperados, ou conflito explicito se exceder;
- professor como atribuicao da aula, nao premissa fixa;
- sala/equipamento/recurso como opcional/discreto;
- copiloto discreto explicando consequencia, sem marcar chamada sozinho.

Regra:

- chamada e uma acao humana/auditavel;
- IA pode sugerir consequencia ou redigir aviso;
- autonomia nao marca presenca sozinha;
- correcao de chamada gera auditoria.

## Imagem Aprovada - Aula

### 29. Aula - Detalhe Com Chamada

Status:

**Aprovada v0.1.** Imagem salva no pacote local como `29_round-4.1F_aula_01_detalhe-com-chamada.png.png`.

Arquivo esperado:

`29_round-4.1F_aula_01_detalhe-com-chamada.png`

Origem local conhecida:

`D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/29_round-4.1F_aula_01_detalhe-com-chamada.png.png`

Observacao de numeracao:

A numeracao canonica desta imagem e `29`. A sugestao anterior com prefixo `27` nao deve ser usada.

Objetivo:

Mostrar `/app/aulas/[id]` como detalhe de aula com o drawer de chamada aberto, sem criar rota separada para chamada.

Estado representado:

- aula `Terca 17h - Reformer Intermediario`;
- professor tratado como `Professor da aula`, nao professor fixo universal;
- equipamento/recurso opcional e discreto;
- capacidade coerente com alunos esperados: `5/6`;
- lista de alunos esperados no corpo da aula;
- drawer de chamada aberto com status por aluno;
- consequencias curtas: `gera credito`, `nao gera credito`, `reposicao usada`;
- copiloto discreto explicando consequencia;
- chamada auditavel e salva por humano.

Observacoes da aprovacao:

- `Fazer chamada` aparece como botao ativo; em implementacao pode virar `Chamada aberta` ou `Chamada em andamento`;
- `Salvar aula` salva dados/observacoes da aula;
- `Salvar chamada` salva presenca, falta, no-show e consequencias da chamada;
- detalhe completo do aluno deve abrir outro drawer, acionado ao clicar no aluno;
- o drawer de chamada permanece transacional e nao deve virar perfil do aluno.

## Contrato Da Pagina Reposicoes

Rota principal:

`/app/reposicoes`

Decisao:

- `/app/reposicoes` deve ser suficiente para visualizar e resolver todo o fluxo de reposicao e encaixe;
- nao misturar lista de espera geral na pagina de reposicoes;
- nao criar pagina visual separada de creditos de reposicao nesta rodada;
- creditos aparecem dentro do fluxo da reposicao, como direito/validade/status do aluno;
- encaixe e parte da reposicao, pois resolve onde o aluno vai repor;
- modo `manual`, `copiloto` ou `autonomo` e configuracao do fluxo/regra de reposicao do studio, nao configuracao individual por aluno.

Pergunta que a pagina responde:

> Quais alunos precisam repor aula, em que etapa esta cada reposicao, e qual horario pode ser encaixado com seguranca?

Reposicao contem:

- aluno;
- aula original perdida;
- motivo/origem da falta;
- elegibilidade a reposicao;
- credito/direito gerado quando houver;
- validade;
- preferencias de horario;
- opcoes de encaixe;
- convite/resposta;
- aula de destino;
- status da reposicao.

Estados principais:

- pendente;
- buscando horario;
- opcao encontrada;
- convidado;
- aguardando resposta;
- agendada/reservada;
- usada;
- expirada;
- cancelada;
- bloqueada por regra.

Blocos esperados:

| Zona | Conteudo |
| --- | --- |
| Topo | Titulo `Reposicoes`, busca, filtros por status, validade, turma/horario e botao `Novo pedido`. |
| Centro | Lista de reposicoes com aluno, aula original, validade, status, proxima acao, origem e estado operacional. |
| Direita | Detalhe da reposicao selecionada com credito, preferencias, algumas opcoes de horario, conflito e acoes. |

Regra do painel direito:

- por padrao, o painel direito pode estar fechado ate o usuario selecionar uma reposicao;
- a imagem aprovada mostra um estado selecionado, nao necessariamente o carregamento inicial da rota;
- o painel direito e contextual e muda conforme o item clicado;
- ele nao e sempre um painel de encaixe: encaixe e apenas um dos modos possiveis;
- o painel deve manter a mesma largura, densidade, hierarquia e padrao de acoes dos drawers aprovados de Hoje, Operacao, Tarefas, Inbox e Aula.

Modos principais do painel direito em `/app/reposicoes`:

| Item clicado | Painel direito deve mostrar |
| --- | --- |
| Reposicao pendente | Direito/credito, motivo, validade, preferencias, proxima acao e botao para buscar horario. |
| Reposicao com opcao encontrada | Opcoes resumidas de encaixe, compatibilidade, sugestao de convite, `Reservar vaga`, `Enviar convite` e `Ver agenda de vagas`. |
| Reposicao aguardando resposta | Convite enviado, canal/conversa, prazo de resposta, historico curto e acoes de cobrar retorno, alterar opcao ou cancelar. |
| Reposicao agendada/reservada | Aula de destino, status da reserva, consumo previsto do credito, acoes de abrir aula, remarcar ou cancelar. |
| Reposicao bloqueada | Regra/politica que bloqueou, risco, quem pode resolver, acao manual permitida e ausencia de acao autonoma. |
| Reposicao expirada/cancelada/usada | Resumo auditavel, origem, destino quando houver, motivo de encerramento e acoes restritas. |
| Pedido novo/manual | Formulario curto para criar reposicao com aluno, aula original, motivo, validade/politica e preferencia. |

Regra de autonomia do fluxo:

- o studio configura o fluxo de reposicao como `manual`, `copiloto` ou `autonomo`;
- essa configuracao vale para o processo e pode variar por politica, plano, permissao, cota, risco e tipo de acao;
- o aluno nunca e configurado como manual/copiloto/autonomo;
- cada reposicao pode exibir um estado operacional derivado: `manual`, `copiloto sugeriu`, `autonomo disponivel`, `autonomo bloqueado` ou `revisao humana`;
- o estado operacional explica o que o sistema pode fazer naquele caso, sem virar atributo do aluno.

Opcoes de encaixe:

- o painel lateral mostra apenas algumas opcoes recomendadas, suficientes para decisao rapida;
- cada opcao deve mostrar horario, turma/aula, vaga disponivel, compatibilidade e alerta simples quando houver regra;
- deve existir acao `Ver agenda de vagas` ou `Escolher na agenda`;
- essa acao abre uma agenda de vagas usando o mesmo modelo visual da pagina Agenda, com dia/semana, filtros e aulas com vagas compativeis;
- na agenda expandida, o usuario seleciona a aula de destino e volta para a reposicao com a opcao escolhida;
- essa agenda de vagas e um estado expandido/overlay/drawer amplo da rota `/app/reposicoes`, nao uma nova pagina obrigatoria nesta rodada.

Acoes principais:

- encontrar horario;
- reservar encaixe;
- escolher na agenda de vagas;
- enviar convite;
- marcar como agendada;
- consumir/usar credito;
- cancelar reposicao;
- criar tarefa;
- abrir conversa;
- abrir aula original;
- abrir aula de destino.

O que nao entra nesta pagina:

- lista de espera geral de alunos/interessados aguardando vaga fixa;
- dashboard de ocupacao;
- auditoria completa de todos os creditos;
- configuracao de autonomia por aluno;
- gestao estrutural de grade/turmas;
- financeiro completo;
- pipeline de vendas/interessados.

Imagem aprovada:

`31_round-4.1F_reposicoes_01_fluxo-encaixe.png`

Arquivo local:

`D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/31_round-4.1F_reposicoes_01_fluxo-encaixe.png.png`

Status:

aprovada v0.1

Objetivo da imagem:

Mostrar a pagina `/app/reposicoes` como lista de reposicoes + detalhe da reposicao selecionada, com opcoes de encaixe e acoes para resolver.

Cobertura da imagem:

- rota `/app/reposicoes`;
- lista de reposicoes com status, validade, origem, preferencia, proxima acao e estado operacional;
- detalhe lateral da reposicao selecionada;
- opcoes resumidas de encaixe;
- sugestao de convite;
- acoes para reservar vaga, enviar convite, criar tarefa, abrir conversa, abrir aula original e cancelar;
- comportamento com 0 agentes, copiloto e autonomia disponivel/bloqueada.

Observacoes da aprovacao:

- a imagem usa coluna/tag de modo como estado operacional da reposicao conforme a politica do fluxo, nao como preferencia do aluno;
- modo `manual`, `copiloto` ou `autonomo` continua sendo configuracao do fluxo de reposicao do studio;
- o painel lateral mostra poucas opcoes de encaixe; a implementacao deve manter um caminho claro para abrir a agenda completa de vagas;
- autonomia so pode enviar convite seguro, reservar temporariamente ou sugerir acao quando politica, consentimento, cota e risco permitirem;
- `Reservar vaga` significa pre-reserva operacional segura, nao consumo definitivo de credito em caso ambiguo;
- o nome `30_round-4.1F_reposicoes_01_fluxo-encaixe.png` nao deve ser usado para Reposicoes, pois o indice 30 ja foi usado em outra familia.
