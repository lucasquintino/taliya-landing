# Rodada 4.1G - Vendas E Interessados Web - Plano De Imagens

> Status: aprovado para web v0.1. Imagens 37, 38, 39 e 40 aprovadas como base visual da familia Vendas / Interessados no Taliya CRM.

## Decisao De Arquitetura Visual

A familia Vendas / Interessados usa o mesmo principio de Financeiro: duas superficies irmas, uma visual por etapa e outra em lista para volume, busca e triagem. Elas compartilham a mesma casca operacional, mas nao usam toggle interno Kanban/Lista.

Superficies principais:

1. `/app/vendas` - kanban do pipeline comercial.
2. `/app/vendas/lista` - lista de interessados.
3. `/app/interessados/[id]` - detalhe do interessado herdado do drawer/painel de Vendas.

Decisao de rota:

- `/app/vendas` e a rota principal;
- `/app/interessados` pode ser alias ou redirecionar para `/app/vendas`;
- `/app/interessados/[id]` herda o drawer/painel e pode renderizar o mesmo conteudo em tela expandida;
- cadastro manual acontece por botao/drawer dentro de `/app/vendas`;
- nao criar `/app/interessados/novo` nesta rodada;
- perdidos sao filtro/etapa dentro de Vendas, sem `/app/vendas/perdidos`;
- origem e campo simples do interessado, sem paginas de captura/origens/indicacoes no MVP.

## Casca Padrao Herdada

A familia Vendas nao cria uma casca visual nova. Ela deve reaproveitar os padroes ja aprovados em outras paginas:

- Kanban deve seguir o padrao de operacao por colunas ja aprovado em Financeiro Kanban e Operacao;
- Lista deve seguir o padrao de Movimentacoes do Financeiro: filtro superior, painel esquerdo de filtros rapidos, tabela/lista central e painel direito de detalhe;
- filtros rapidos, filtros superiores, cards, linhas e drawer devem parecer componentes do mesmo sistema, nao componentes novos de Vendas.

Referencias visuais obrigatorias para prompts:

- `33_round-4.1F_financeiro_03_kanban-financeiro.png.png` para densidade, colunas, filtros superiores e comportamento de kanban financeiro;
- `34_round-4.1F_financeiro_04_movimentacoes-filtros-drawer.png.png` para filtro superior, painel esquerdo de filtros rapidos, lista/tabela e painel direito contextual;
- `21_round-4.1B_operacao_01_kanban-geral.png` quando o kanban precisar de filtros rapidos laterais;
- `22_round-4.1B_operacao_02_kanban-com-drawer.png` para estado selecionado com painel contextual.

As imagens de Pipeline e Lista devem respeitar estes blocos:

- App shell lateral aprovado;
- navegacao superior da familia com `Pipeline`, `Lista`, `Experimental`, `Matriculas` e `Historico`;
- titulo `Vendas` e subtitulo operacional curto;
- barra de filtros no topo com busca, dono, etapa/status, origem, proxima acao e botao principal;
- painel esquerdo de filtros rapidos quando a superficie usar lista/tabela ou quando o kanban precisar desse recorte, seguindo o padrao ja aprovado;
- superficie central em kanban ou lista;
- painel direito contextual somente quando um interessado estiver selecionado.

Regra especifica para Vendas Kanban:

- o kanban de `/app/vendas` nao deve usar painel esquerdo;
- filtros rapidos ficam na barra superior como chips/filtros;
- toda a largura disponivel deve ser usada pelas colunas;
- nem todas as etapas precisam aparecer ao mesmo tempo;
- etapas fora da area visivel ficam acessiveis por scroll horizontal, como no Financeiro Kanban.

Regra especifica para Vendas Lista:

- a lista de `/app/vendas/lista` deve usar painel esquerdo de filtros rapidos;
- o painel direito aberto representa estado selecionado, nao carregamento padrao obrigatorio;
- a estrutura deve seguir Movimentacoes do Financeiro.

Nao deve aparecer:

- toggle interno `Kanban / Lista`;
- abas duplicadas dentro da area de filtros;
- atividade recente abaixo da superficie principal;
- dashboard generico ou cards de metrica;
- controle de campanhas, origens avancadas, segmentos ou indicacoes.

A navegacao entre Pipeline e Lista acontece pela barra superior da familia ou pela rota, nao por um controle dentro da pagina.

## Papel Da Pagina

Vendas responde:

> Quem esta interessado, em que etapa esta, qual a proxima acao, quem e o dono e o que precisa acontecer para virar aluno?

Vendas nao e:

- Inbox;
- Agenda;
- Matriculas;
- Checkout;
- Comunicados;
- central de marketing/origens;
- dashboard generico.

## Visao Kanban

Rota:

`/app/vendas`

Papel:

- operar o funil por etapa;
- mover interessados entre etapas;
- priorizar proximas acoes;
- abrir detalhe do interessado;
- agendar experimental;
- iniciar matricula quando estiver pronto.

Etapas sugeridas:

- Novo;
- Conversando;
- Experimental;
- Pos-aula;
- Matricula.

`Sem resposta`, `Sem vaga` e `Perdido` sao filtros rapidos/status de trabalho, nao precisam virar colunas permanentes do kanban.

Cada card deve mostrar:

- nome;
- origem simples;
- objetivo/interesse;
- horario desejado;
- ultima conversa;
- proxima acao;
- dono/fila;
- badge de status quando relevante;
- badge de modo somente quando houver diferenca operacional: manual, copiloto sugeriu, autonomo bloqueado, aguardando humano.

O kanban deve ter poucos cards visiveis por coluna e colunas com largura respiravel. A prioridade visual e entender a etapa e a proxima acao, nao mostrar todos os dados do interessado no card.

Filtros rapidos no kanban:

- Todos;
- Meus interessados;
- Sem resposta;
- Sem vaga;
- Experimental hoje;
- Prontos para matricula;
- Perdidos.

Esses filtros aparecem na barra superior, nao em painel lateral.

## Visao Lista

Rota:

`/app/vendas/lista`

Papel:

- trabalhar volume;
- buscar interessado rapidamente;
- filtrar por dono, etapa, origem, proxima acao, sem resposta, sem vaga, perdido e experimental;
- ordenar por prazo/proxima acao;
- revisar muitos leads sem trocar de coluna.

Colunas sugeridas:

- interessado;
- etapa/status;
- proxima acao;
- horario desejado;
- dono/fila;
- ultima conversa.

Origem, canal e modo podem aparecer como badges secundarios dentro da linha quando forem relevantes, mas nao devem transformar a lista em uma tabela pesada.

## Drawer/Painel Do Interessado

O mesmo painel deve ser usado no Kanban, na Lista e em `/app/interessados/[id]`.

Por padrao, a pagina pode carregar sem painel aberto. Imagens com painel aberto representam estado selecionado.

Modos principais do painel:

| Item clicado | Painel deve mostrar |
| --- | --- |
| Interessado novo | Dados basicos, origem simples, canal, primeira proxima acao e qualificacao inicial. |
| Qualificado/quente | Objetivo, horario desejado, objecao, nivel de interesse, proxima acao, conversa recente e acoes de follow-up. |
| Experimental agendada | Aula experimental vinculada, horario, status do lembrete, acao para abrir Experimental/Agenda e remarcar. |
| Pos-aula | Resultado da aula teste, feedback, objecao, proxima acao e acao de iniciar matricula. |
| Pre-matricula | Checklist resumido de dados, plano escolhido, primeira aula, pagamento inicial quando exigido e acao para abrir Matriculas. |
| Sem resposta | Ultima tentativa, limite de cadencia, canal permitido e acoes de tentar novamente, criar tarefa ou marcar perdido. |
| Sem vaga | Horario desejado, alternativas, tarefa de retorno ou lista futura; nao marcar perdido automaticamente. |
| Perdido | Motivo de perda, data, responsavel, possibilidade de reativar e historico comercial. |

## Manual, Copiloto E Autonomo

| Modo | Comportamento |
| --- | --- |
| 0 agentes | Pipeline, lista, follow-up manual, cadastro, agendamento de experimental e inicio de matricula funcionam manualmente. |
| Manual | Usuario move etapa, responde, cria follow-up, agenda experimental, marca perdido e inicia matricula. |
| Programatico | CRM calcula prazos, sem resposta, etapa, dono, experimental vinculada e pendencias simples. |
| Copiloto | Sugere qualificacao, resposta, objecao, proxima acao e resumo da conversa. |
| Autonomo | Apenas follow-up/lembrete/resposta simples quando politica, canal configurado, template, cota, janela e risco permitirem. Nao promete desconto, preco especial, vaga ou contrato sozinho. |

## Imagens Necessarias

| Imagem | Nome | Objetivo |
| --- | --- | --- |
| 1 | `37_round-4.1G_vendas_01_pipeline-kanban.png` | Kanban principal do pipeline de interessados, sem toggle Kanban/Lista, sem painel esquerdo e com scroll horizontal. |
| 2 | `38_round-4.1G_vendas_02_lista-interessados.png` | Lista de interessados para busca, filtros e volume, com painel esquerdo de filtros rapidos e painel direito contextual. |
| 3 | `39_round-4.1G_experimental_01_lista-acompanhamento.png` | Lista operacional de aulas experimentais, conectada a Vendas e Agenda, com painel direito contextual. |
| 4 | `40_round-4.1G_matriculas_01_checklist-conversao.png` | Fila/checklist de pre-matriculas para converter interessados em alunos com seguranca. |

Decisao:

- imagem 37 mostra o pipeline sem painel direito aberto;
- imagem 38 mostra a lista com painel direito aberto para interessado selecionado;
- imagem 39 mostra Experimental como fila comercial-operacional, nao como calendario;
- imagem 40 mostra Matriculas como checklist de conversao, nao como checkout financeiro;
- cada imagem reutiliza a casca aprovada correspondente: Financeiro Kanban para Pipeline e Movimentacoes do Financeiro para Lista;
- nao gerar imagem separada para `/app/interessados/[id]` nesta rodada.

## Auditoria Visual Final

Imagem 37 - Pipeline/Kanban:

- aprovada como referencia de `/app/vendas`;
- filtros rapidos ficam na barra superior;
- nao ha painel esquerdo;
- colunas ocupam a largura da tela;
- etapas extras podem ficar fora da dobra horizontal;
- o scroll horizontal e comportamento esperado;
- `Perdido`, `Sem resposta` e `Sem vaga` podem aparecer como filtro/status e nao precisam ser colunas centrais sempre visiveis;
- sem painel direito no estado base.

Imagem 38 - Lista:

- aprovada como referencia de `/app/vendas/lista`;
- usa painel esquerdo de filtros rapidos;
- usa tabela/lista central enxuta;
- painel direito aberto representa interessado selecionado;
- o carregamento padrao pode manter o painel fechado ate selecao;
- herda o padrao de Movimentacoes do Financeiro.

Imagem 39 - Experimental:

- aprovada como referencia de `/app/experimental`;
- usa lista/tabela com filtros superiores e painel esquerdo de filtros rapidos;
- painel direito aberto representa uma aula experimental selecionada;
- mostra a ponte com Agenda sem virar calendario;
- mostra a ponte com Vendas sem virar pipeline;
- a acao `Agendar experimental` deve abrir fluxo de escolha de horario na Agenda ou componente de agenda, nunca criar horario solto;
- `Aula experimental` pode ser turma/tipo/equipamento opcional; nao assumir professor fixo, sala fixa ou recurso obrigatorio para todo studio;
- variacoes de status herdam a mesma estrutura textual.

Imagem 40 - Matriculas:

- aprovada como referencia de `/app/matriculas`;
- usa lista/tabela com filtros superiores e painel esquerdo de filtros rapidos;
- painel direito aberto representa uma pre-matricula selecionada;
- mostra checklist de conversao com progresso;
- `Converter em aluno` so habilita quando o checklist obrigatorio estiver completo;
- se faltar dado obrigatorio, a acao principal deve ser pedir/validar dado, e converter fica desabilitado ou secundario;
- pagamento inicial e relevante no checklist quando a politica do studio exigir pagamento antes da conversao;
- Matriculas pode mostrar resumo do pagamento inicial e acionar `Gerar cobranca`, `Enviar Pix/link`, `Abrir cobranca` ou `Marcar pagamento manual` quando permitido;
- Financeiro continua sendo a fonte da verdade da cobranca, conciliacao, comprovante, falha, estorno, promessa, desconto e auditoria;
- contrato, cobranca detalhada, assinatura e documentos completos nao moram nesta pagina;
- se o studio exigir pagamento/contrato antes da conversao, Matriculas mostra bloqueio/pendencia e abre Financeiro, Documentos ou Aprovacoes;
- primeira aula deve ser escolhida pela Agenda/componente de agenda, nao como texto livre solto;
- variacoes de pendencia herdam a mesma estrutura textual.

Cobertura:

- `/app/vendas` coberto pela imagem 37;
- `/app/vendas/lista` coberto pela imagem 38;
- `/app/interessados` pode redirecionar/herdar `/app/vendas`;
- `/app/interessados/[id]` herda o painel de interessado da imagem 38 em tela expandida ou rota direta;
- `/app/experimental` coberto pela imagem 39;
- `/app/matriculas` coberto pela imagem 40;
- variacoes de painel por etapa herdam a mesma estrutura e ficam documentadas por contrato textual.

## Relacao Com Experimental, Matriculas E Checkout

Experimental:

- nasce a partir de Vendas quando o interessado agenda aula teste;
- cria aula/evento real na Agenda com tipo `experimental`;
- `/app/experimental` acompanha lembrete, falta, remarcacao, pos-aula e conversao.

### Ciclo De Entrada E Saida Do Experimental

Um item entra em `/app/experimental` quando existe um interessado vinculado a uma aula experimental real.

Entradas:

- em Vendas, usuario clica em `Agendar experimental`, escolhe horario real usando Agenda/componente de agenda, e o interessado passa para etapa `Experimental`;
- em Agenda, usuario cria uma aula/evento do tipo `Experimental` e vincula um interessado;
- em Inbox, uma conversa pode acionar `Agendar experimental`; ao escolher horario, o vinculo com Agenda cria o item em Experimental.

O item nao deve ser criado como tarefa solta. O objeto pratico e:

`Interessado + Aula Experimental + Status + Proxima acao`.

Status principais:

- Agendada;
- Confirmar presenca;
- Confirmada;
- Compareceu;
- Faltou;
- Remarcar;
- Pos-aula;
- Pronta para matricula;
- Perdida;
- Convertida.

Saidas:

- `Iniciar matricula` envia para `/app/matriculas` e deixa Experimental como convertido ou fora dos filtros ativos;
- `Marcar perdido` encerra a tentativa e mantem historico em Vendas;
- `Remarcar` mantem o item em Experimental com nova aula vinculada;
- `Faltou` pode virar Remarcar ou Perdida;
- `Compareceu` vira Pos-aula ate converter, seguir em follow-up ou perder.

Fluxo simples:

`Interessado em Vendas -> agenda aula experimental -> entra em Experimental -> confirma presenca -> aula acontece -> compareceu/faltou -> pos-aula/remarcar/perdido -> matricula ou encerramento`.

Matriculas:

- acompanha pre-matriculas e pendencias antes de virar aluno;
- e uma fila/checklist de conversao.

Regras de Matriculas:

- uma pre-matricula entra em `/app/matriculas` a partir de Vendas, Experimental ou criacao manual pela recepcao;
- o objeto pratico e `Interessado + Checklist de conversao + Plano escolhido + Primeira aula + Pagamento inicial quando exigido + Status`;
- converter em aluno cria/atualiza o aluno em `/app/alunos/[id]`, preservando origem, historico e vinculos comerciais;
- conversao so deve ficar disponivel quando dados minimos, contato, plano, primeira aula obrigatoria e pagamento inicial obrigatorio estiverem resolvidos;
- pendencias financeiras, contrato ou assinatura sao bloqueios vinculados, mas sua resolucao profunda fica em Financeiro/Documentos/Aprovacoes;
- a primeira aula vem da Agenda ou de um seletor baseado na Agenda.

Pagamento em Matriculas:

- se o studio nao exige pagamento antes de virar aluno, o item `Pagamento inicial` pode aparecer como `Nao obrigatorio agora` ou nao aparecer;
- se o studio exige pagamento antes da conversao, `Pagamento inicial` vira item obrigatorio e bloqueia `Converter em aluno` ate confirmacao;
- Matriculas pode iniciar ou acionar a cobranca de entrada, mas nao substitui Financeiro;
- estados de pagamento relevantes no checklist: `Nao obrigatorio`, `Pendente`, `Link enviado`, `Pago`, `Falhou`, `Prometido`, `Aguardando aprovacao`;
- `Pagamento prometido` so libera conversao se politica/permissao permitirem; caso contrario vira bloqueio ou aprovacao;
- desconto, valor especial ou condicao diferente exigem aprovacao antes de gerar/confirmar cobranca;
- pagamento falhou abre cobranca existente ou permite reenviar link, sempre mantendo Financeiro como fonte da verdade.

Metodos de pagamento em Matriculas:

- os metodos sao configurados pelo studio em Configuracoes/Financeiro;
- Matriculas apenas herda e filtra os metodos disponiveis para pagamento inicial;
- exemplos: Pix, cartao de credito, cartao de debito, dinheiro, transferencia, boleto, link de pagamento e pagamento manual/externo;
- cada metodo pode definir se aparece em matricula, mensalidade ou ambos;
- cada metodo pode exigir confirmacao manual, integracao automatica, permissao, aprovacao, taxa ou parcelamento;
- a tela nunca deve oferecer metodo que o studio nao habilitou para aquele caso;
- usuario sem permissao nao pode registrar pagamento manual;
- agente autonomo pode enviar link/Pix permitido, mas nao pode marcar pagamento manual sozinho.

Auditoria do fluxo Interessado -> Aluno:

- Interessado nasce em Vendas/Inbox/cadastro manual com origem, canal, etapa e proxima acao;
- Experimental e opcional e so existe quando ha aula experimental real vinculada a Agenda;
- Matriculas comeca quando alguem aciona `Iniciar matricula`;
- Pre-matricula resolve dados, plano, inicio, primeira aula e pagamento inicial quando exigido;
- Financeiro confirma pagamento e mantem auditoria;
- `Converter em aluno` cria/atualiza `/app/alunos/[id]` preservando origem, historico comercial, conversas, experimental, plano, primeira aula e cobranca vinculada;
- depois da conversao, o acompanhamento sai de Vendas/Matriculas e passa para Alunos, Agenda e Financeiro.

Checkout:

- nao criar `/app/checkout-alunos` como pagina propria no MVP;
- o fluxo guiado de conversao acontece dentro de `/app/matriculas`;
- quando houver pagamento inicial, Matriculas aciona cobranca, mas Financeiro continua fonte da verdade;
- quando houver contrato/assinatura/documento obrigatorio, Matriculas mostra bloqueio e abre Documentos/Aprovacoes;
- se no futuro o checkout ficar grande demais, pode virar rota propria em rodada posterior.

Comunicados:

- nao pertencem ao pipeline principal de Vendas;
- nao entram como imagem ou rota desta familia no MVP;
- ficam para agente/superficie separada pos-MVP, com contrato proprio.
