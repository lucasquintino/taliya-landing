# Rodada 4.1I - Relatorios E Gestao Web - Plano De Imagens

> Status: familia fechada para web v0.1 com imagens 45 e 46 aprovadas. Esta familia usa a rota principal `Relatorios`; "gestao" e a funcao da familia, nao uma rota nova.

## Decisao De Escopo

Nao criar `/app/gestao` nesta rodada.

Gestao fica dentro da familia **Relatorios / Exportacoes**, ja existente nos mapas do produto.

Rotas ja mapeadas para o MVP:

- `/app/relatorios`;
- `/app/relatorios/semana`;
- `/app/relatorios/financeiro`;
- `/app/relatorios/vendas`;
- `/app/relatorios/risco`;
- `/app/relatorios/agentes`;
- `/app/relatorios/ocupacao`;
- `/app/dinheiro-na-mesa`;
- `/app/exportacoes`;
- `/app/exportacoes/[jobId]`.

`Gargalos` e `Capacidade` nao sao rotas dedicadas no MVP. Eles aparecem como blocos/leituras dentro de Relatorios e abrem as origens operacionais com filtros aplicados.

## Papel Da Familia

Relatorios/Gestao responde:

> O que o gestor precisa entender, decidir ou abrir para agir, sem entrar em cada modulo operacional?

Esta familia nao substitui:

- Hoje, que comanda o dia;
- Operacao, que resolve travas e pendencias;
- Financeiro, que opera cobrancas e pagamentos;
- Vendas, que opera interessados;
- Agenda, que opera aulas e capacidade diaria;
- Retencao, que opera risco e cancelamento;
- Configuracoes, que muda regras.

## Principio Visual

Relatorios nao podem virar dashboard generico.

Cada bloco deve ter:

- origem do dado;
- periodo;
- leitura curta;
- impacto;
- acao ou aprofundamento;
- link para abrir a fonte operacional.

Graficos podem existir, mas devem servir a decisao. Evitar tela apenas com KPIs decorativos.

## Superficies E Cobertura

| Superficie | Decisao visual | Motivo |
| --- | --- | --- |
| `/app/relatorios` | Imagem propria aprovada | Hub de gestao; define modelo mental da familia. |
| `/app/dinheiro-na-mesa` | Imagem propria aprovada | Superficie acionavel de oportunidades por origem; mostra caixa, conversao, retencao e ocupacao sem virar Financeiro. |
| Gargalos | Bloco herdado no MVP | Proximo demais de Hoje/Operacao; no MVP, o bloco em Relatorios abre Operacao/Tarefas/Aprovacoes/Inbox com filtros aplicados. |
| Capacidade | Bloco herdado no MVP | Proximo demais de Agenda/Turmas/Grade/Reposicoes; no MVP, o bloco de Ocupacao abre as origens com filtros aplicados. |
| `/app/relatorios/financeiro` | Herdada | Aprofunda Financeiro; herda imagens 30/33/34 e componentes de relatorio. |
| `/app/relatorios/vendas` | Herdada | Aprofunda Vendas; herda imagens 37/38/39/40. |
| `/app/relatorios/risco` | Herdada | Aprofunda Retencao; herda imagens da familia Retencao. |
| `/app/relatorios/ocupacao` | Herdada | Aprofunda Agenda/Turmas/Grade. |
| `/app/relatorios/agentes` | Adiar | Depende da familia Agentes/Uso. |
| `/app/exportacoes` | Contrato textual inicialmente | Lista/job de exportacao pode herdar tabela + detalhe lateral. |
| `/app/exportacoes/[jobId]` | Herdada | Detalhe de job pode herdar painel/tabela de exportacoes. |

## Imagens Recomendadas Inicialmente

| Imagem | Nome | Objetivo |
| --- | --- | --- |
| 1 | `45_round-4.1I_relatorios_01_visao-gestao.png` | Hub de Relatorios/Gestao com blocos acionaveis e links para origem. |
| 2 | `46_round-4.1I_dinheiro-na-mesa_01_oportunidades-por-origem.png` | Mesa de oportunidades acionaveis agrupadas por origem, com drawer contextual. |
| 3 | `47_round-4.1I_gargalos_01_travas-recorrentes.png` | Nao gerar no MVP; herda Relatorios + Operacao. |
| 4 | `48_round-4.1I_capacidade_01_ocupacao-demanda.png` | Nao gerar no MVP; herda Relatorios + Agenda/Turmas/Grade/Reposicoes. |

Decisao pratica:

- imagem 45 aprovada como base do hub `/app/relatorios`;
- imagem 46 aprovada para `/app/dinheiro-na-mesa`, porque a rota precisa provar que nao e uma lista financeira;
- nao gerar 47 e 48 no MVP: `Gargalos` e `Capacidade` ficam cobertos por heranca visual e filtros nas origens;
- nao gerar imagem propria para `/app/relatorios/semana`, `/app/exportacoes` ou `/app/exportacoes/[jobId]` no MVP;
- nao gerar imagem separada para relatorios especificos se eles apenas aprofundarem familias ja aprovadas.

## Fechamento Web V0.1

As duas imagens suficientes para Relatorios/Gestao no MVP sao:

- `45_round-4.1I_relatorios_01_visao-gestao.png`;
- `46_round-4.1I_dinheiro-na-mesa_01_oportunidades-por-origem.png`.

Elas cobrem os dois trabalhos principais da familia:

- leitura gerencial entre frentes;
- oportunidades acionaveis que cruzam origens.

O que fica sem imagem propria no MVP:

- Gargalos como rota dedicada, por proximidade com Hoje/Operacao;
- Capacidade como rota dedicada, por proximidade com Agenda/Turmas/Grade/Reposicoes;
- `/app/relatorios/semana`, por ser aprofundamento textual do resumo semanal;
- `/app/exportacoes` e `/app/exportacoes/[jobId]`, por herdarem lista/tabela + painel lateral;
- relatorios especificos de Financeiro, Vendas, Risco e Ocupacao, por herdarem as familias donas;
- `/app/relatorios/agentes`, por depender da familia Agentes/Uso.

Qualquer nova imagem nesta familia so deve ser aberta se aparecer uma interacao nova que nao possa herdar esses padroes.

## Decisao Sobre Gargalos E Capacidade

`Gargalos` nao recebe rota nem imagem propria no MVP.

Motivo:

- se aproxima demais de Hoje e Operacao;
- poderia virar uma segunda lista de problemas;
- o bloco `Gargalos` em `/app/relatorios` ja explica a leitura gerencial;
- a resolucao real deve acontecer em Operacao, Tarefas, Aprovacoes, Inbox ou na origem canonica.

Comportamento aprovado:

- `Abrir gargalos` abre a origem com filtro aplicado, como `bloqueadas`, `sem dono`, `aguardando humano`, `aprovacao pendente`, `dados bloqueando fluxo` ou `falha de envio`;
- uma rota propria so deve voltar a ser considerada pos-MVP se houver analise recorrente real, como tendencia por semana, tempo medio parado, gargalo por fila ou sobrecarga de equipe.

`Capacidade` nao recebe rota nem imagem propria no MVP.

Motivo:

- se aproxima demais de Agenda, Turmas, Grade e Reposicoes;
- ocupacao, vagas, bloqueios e demanda ja aparecem nas superficies operacionais aprovadas;
- o bloco `Ocupacao` em `/app/relatorios` ja basta para leitura gerencial inicial.

Comportamento aprovado:

- `Ver ocupacao` abre Turmas, Agenda, Grade ou Reposicoes com filtros aplicados;
- exemplos de filtros: `com vagas`, `lotadas`, `demanda sem vaga`, `reposicoes aguardando encaixe`, `horarios vazios`, `bloqueios com impacto`;
- uma rota propria so deve voltar a ser considerada pos-MVP se houver planejamento analitico de capacidade que nao caiba nas origens.

## Auditoria Visual Da Imagem 45

Imagem aprovada:

`45_round-4.1I_relatorios_01_visao-gestao.png`

Decisoes registradas:

- cobre `/app/relatorios`;
- confirma que nao existe `/app/gestao`;
- cada bloco mostra origem, periodo, impacto e acao;
- `Dinheiro em aberto`, `Vendas em andamento`, `Ocupacao`, `Gargalos`, `Risco`, `Resumo semanal`, `Exportacoes` e `Copiloto` estao bem representados;
- bloco `Risco` depende da familia Retencao estar habilitada; pode ser omitido ou aparecer limitado se a permissao/plano nao cobrir;
- bloco `Copiloto` so aparece quando houver agente/slot/cota habilitado; com 0 agentes, a pagina continua funcionando sem ele;
- `Agendar relatorio` depende de plano/feature de exportacao agendada; caso contrario fica indisponivel ou vira exportacao manual;
- Dinheiro virou pagina propria na imagem 46; Gargalos e Capacidade ficam herdadas no MVP para evitar duplicar Operacao e Agenda.

## Auditoria Visual Da Imagem 46

Imagem aprovada:

`46_round-4.1I_dinheiro-na-mesa_01_oportunidades-por-origem.png`

Decisoes registradas:

- cobre `/app/dinheiro-na-mesa`;
- a pagina e uma mesa de oportunidades por origem, nao uma tabela financeira;
- blocos principais aprovados: `Matriculas travadas`, `Experimentais quentes`, `Financeiro recuperavel`, `Vagas com demanda`, `Reposicoes que evitam perda` e `Risco com receita ativa`;
- cada bloco mostra origem canonica, impacto, status e proxima acao;
- valores monetarios aparecem quando existem, mas a rota tambem aceita impacto qualitativo como `conversao`, `retencao`, `ocupacao` e `experiencia`;
- reposicoes entram como retencao/experiencia/continuidade, nao como cobranca;
- vagas com demanda entram como oportunidade de ocupacao e nao como financeiro direto;
- o painel direito representa um item selecionado e deve ficar fechado no carregamento padrao da rota;
- o painel direito e contextual: acoes como `Abrir cobranca` ou `Enviar Pix` so aparecem quando existe origem financeira/cobranca aplicavel;
- `Criar tarefa` e acao auxiliar, nao o caminho principal da pagina;
- o caminho principal deve abrir a origem operacional: Matriculas, Experimental, Financeiro, Agenda/Turmas, Reposicoes ou Retencao;
- a rota funciona com 0 agentes; Copiloto apenas sugere prioridade, mensagem ou proxima acao; Autonomo so executa acoes seguras quando politica, plano, permissao e cota permitirem.

Correcao de implementacao:

- a URL canonica da rota e `/app/dinheiro-na-mesa`; qualquer referencia visual com `/app/app/dinheiro-na-mesa` deve ser tratada como erro de geracao de imagem, nao como rota real.

## Relacao Com Paginas Ja Aprovadas

Relatorios/Gestao deve abrir origem operacional:

- dinheiro em aberto abre Financeiro;
- interessado quente abre Vendas;
- experimental sem pos-aula abre Experimental;
- risco abre Retencao;
- ocupacao/vaga abre Agenda/Turmas/Grade;
- gargalo operacional abre Operacao/Tarefas/Aprovacoes;
- exportacao abre Exportacoes.

Exportacoes:

- `/app/exportacoes` lista jobs recentes com tipo, status, solicitante, filtros, data, validade do arquivo e acao de baixar/reprocessar quando aplicavel;
- `/app/exportacoes/[jobId]` mostra parametros, status, erro quando falhar, historico de processamento e acoes de baixar, reprocessar, criar nova com mesmos filtros ou cancelar quando ainda estiver processando;
- exportacao agendada ou recorrente fica dependente de plano/feature e nao precisa imagem propria nesta rodada.

## Manual, Copiloto E Autonomo

| Modo | Comportamento |
| --- | --- |
| 0 agentes | Relatorios funcionam com dados do CRM e filtros manuais. |
| Manual | Gestor filtra, abre origem, exporta e acompanha indicadores. |
| Programatico | Sistema calcula totais, comparacoes, tendencias simples, gargalos e listas. |
| Copiloto | Resume leitura, explica mudanca e sugere onde abrir primeiro. |
| Autonomo | Nao toma decisoes de gestao nem exporta sozinho; no maximo prepara resumo ou tarefa segura quando permitido. |

## O Que Nao Deve Aparecer

- `/app/gestao` como rota nova;
- dashboard executivo generico;
- hero, landing page ou cards decorativos;
- graficos sem acao;
- metricas sem origem;
- exportacao automatica sem confirmacao humana;
- mudanca de regra operacional dentro de Relatorios.
