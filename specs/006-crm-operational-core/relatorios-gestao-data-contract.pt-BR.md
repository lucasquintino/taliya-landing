# Contrato De Dados - Relatorios E Gestao - PT-BR

> Status: web v0.1 fechado. Este contrato define como gerar conteudo das paginas de Relatorios/Gestao no MVP sem criar BI avancado nem uma rota `/app/gestao`.

## Principio

Relatorios/Gestao deve ser acionavel.

Cada bloco precisa responder:

- o que o gestor precisa entender;
- de onde vem o dado;
- qual regra simples gera o numero/lista;
- quando o bloco merece atencao;
- qual acao abre a origem operacional;
- o que fica fora do MVP.

Nao criar metricas sem origem. Nao criar graficos apenas decorativos.

## Fontes Disponiveis No MVP

| Fonte | Dados usados |
| --- | --- |
| Financeiro | cobrancas, mensalidades, vencimentos, falhas, promessas, comprovantes, conciliacao, pagamento inicial de matricula. |
| Vendas | interessados, etapa, origem simples, proxima acao, experimental, pre-matricula, perdido. |
| Agenda/Turmas | aulas, turmas, capacidade, alunos fixos, vagas, horarios, chamada, bloqueios aplicados. |
| Reposicoes | pedidos, creditos dentro do fluxo, opcoes, aguardando resposta, reservas, bloqueios. |
| Matriculas | pre-matriculas, dados faltantes, plano escolhido, primeira aula, pagamento inicial quando exigido. |
| Operacao/Tarefas/Aprovacoes | pendencias, tarefas, dono/fila, prazo, bloqueio, aprovacao pendente, origem canonica. |
| Inbox | conversas aguardando humano, falhas de envio, assunto vinculado, dono/fila. |
| Retencao | risco, queda de frequencia, inativos e cancelamentos, quando a familia estiver fechada. |
| Agentes/Uso | execucoes, cota, bloqueios, economia e incidentes, quando a familia estiver fechada. |

## Bloco: Dinheiro Em Aberto

Objetivo:

Mostrar valores que podem virar caixa com acao operacional.

Fonte:

- Financeiro;
- Matriculas, apenas quando pagamento inicial bloquear conversao.

Entram no MVP:

- cobrancas vencidas;
- cobrancas vencendo hoje;
- falhas de pagamento;
- promessas vencendo hoje ou vencidas;
- comprovantes pendentes de validacao;
- pre-matriculas bloqueadas por pagamento inicial obrigatorio.

Nao entram no MVP:

- previsao financeira avancada;
- forecast por churn;
- projecao de meses futuros;
- LTV, CAC ou ROI detalhado.

Regra MVP:

Somar cobrancas abertas com vencimento ate hoje + cobrancas com falha + promessas vencidas/hoje + pagamentos iniciais obrigatorios pendentes.

Estados:

- `normal`: sem atraso critico;
- `atencao`: valor aberto acima do limite configurado ou promessa vencendo hoje;
- `critico`: falha recorrente, atraso acima do limite ou pagamento inicial bloqueando conversao.

Acao principal:

Abrir lista financeira filtrada.

Destino:

- `/app/financeiro/movimentacoes`;
- item especifico em Financeiro quando clicar em linha;
- `/app/matriculas` quando a origem for pagamento inicial de pre-matricula.

## Pagina Especial: Dinheiro Na Mesa

Objetivo:

Reunir oportunidades acionaveis espalhadas pelo CRM que podem virar caixa, conversao, retencao, ocupacao ou experiencia resolvida.

Esta pagina nao e uma extensao visual de Financeiro. Ela nao deve ser uma tabela de movimentacoes nem uma lista de cobrancas.

Fonte:

- Financeiro;
- Matriculas;
- Experimental;
- Vendas;
- Agenda/Turmas;
- Reposicoes;
- Retencao, quando a familia estiver habilitada.

Blocos aprovados para MVP:

| Bloco | Origem canonica | O que entra | Impacto esperado |
| --- | --- | --- | --- |
| Matriculas travadas | Matriculas | pre-matricula bloqueada por pagamento inicial, dado obrigatorio ou primeira aula | conversao |
| Experimentais quentes | Experimental/Vendas | compareceu, perguntou valores, quer plano, pos-aula pendente | conversao |
| Financeiro recuperavel | Financeiro | mensalidade vencida, falha, promessa, comprovante pendente | caixa |
| Vagas com demanda | Agenda/Turmas | vaga util, turma quase cheia, interessados compativeis | ocupacao |
| Reposicoes que evitam perda | Reposicoes | credito vencendo, opcao encontrada, caso sensivel | retencao/experiencia |
| Risco com receita ativa | Retencao/Alunos | queda de frequencia, cancelamento evitavel, aluno ativo em risco | retencao |

Regra MVP:

Gerar oportunidades a partir de eventos ja registrados e listar apenas itens com proxima acao clara. A pagina deve preferir acao na origem operacional antes de criar tarefa.

Campos minimos por oportunidade:

- pessoa, turma ou oportunidade;
- origem canonica;
- impacto (`caixa`, `conversao`, `retencao`, `ocupacao` ou `experiencia`);
- valor estimado quando existir;
- status atual;
- proxima acao;
- dono/fila;
- prazo ou urgencia.

Valor estimado:

- pode ser valor monetario real quando existe cobranca, pagamento inicial, mensalidade ou promessa;
- pode ser recorrencia estimada, como `R$ 420/mes`, quando a oportunidade e conversao;
- pode ser impacto qualitativo quando nao ha dinheiro direto, como reposicao que evita perda ou vaga que melhora ocupacao.

Drawer contextual:

- abre apenas apos selecionar uma oportunidade;
- exibe origem, impacto, motivo do bloqueio, historico curto, sugestao do Copiloto quando habilitado e acoes permitidas;
- `Enviar Pix`, `Abrir cobranca` e acoes financeiras aparecem apenas quando existe metodo/cobranca aplicavel;
- `Abrir conversa`, `Abrir matricula`, `Abrir aula`, `Abrir reposicao`, `Abrir aluno` ou `Abrir retencao` aparecem conforme origem;
- `Marcar sem acao` exige motivo e deve registrar auditoria;
- `Criar tarefa` e auxiliar, nao substitui resolver pela origem.

Manual, Copiloto e Autonomo:

- com 0 agentes, a pagina funciona como lista de oportunidades e atalhos manuais;
- no modo manual, usuario decide e executa;
- no modo Copiloto, o sistema sugere prioridade, mensagem e proxima acao;
- no modo Autonomo, so acoes seguras e permitidas podem ser preparadas/executadas, respeitando politica, permissao, plano, cota e risco;
- o modo nao e configurado por aluno individual, e sim pelo fluxo/politica do studio.

Destino:

- `/app/matriculas`;
- `/app/experimental`;
- `/app/vendas`;
- `/app/financeiro/movimentacoes`;
- `/app/agenda`;
- `/app/turmas`;
- `/app/reposicoes`;
- `/app/retencao`, quando ativo.

## Bloco: Vendas Em Andamento

Objetivo:

Mostrar oportunidades comerciais que precisam de proxima acao para virar aluno.

Fonte:

- Vendas;
- Experimental;
- Matriculas.

Entram no MVP:

- interessados sem resposta;
- interessados quentes;
- experimentais hoje/amanha;
- pos-aula sem follow-up;
- pre-matriculas pendentes;
- perdas recentes com motivo.

Nao entram no MVP:

- ROI por campanha;
- funil customizavel;
- analise avancada de origem;
- segmentos comerciais.

Regra MVP:

Contar interessados ativos por etapa/status e listar os itens com proxima acao vencida, hoje ou sem dono.

Estados:

- `normal`: sem proxima acao vencida;
- `atencao`: interessados sem resposta ou pos-aula pendente;
- `critico`: oportunidade quente sem dono, experimental sem follow-up ou pre-matricula bloqueada.

Acao principal:

Abrir origem comercial.

Destino:

- `/app/vendas`;
- `/app/vendas/lista`;
- `/app/experimental`;
- `/app/matriculas`;
- `/app/interessados/[id]` quando existir rota direta.

## Bloco: Ocupacao

Objetivo:

Mostrar como a agenda e as turmas estao sendo usadas: cheio, vazio, vagas e demanda reprimida.

Fonte:

- Agenda;
- Turmas;
- Grade;
- Reposicoes.

Entram no MVP:

- turmas lotadas;
- turmas com vagas;
- horarios vazios recorrentes;
- aulas com capacidade baixa;
- demanda sem vaga;
- reposicoes aguardando encaixe por falta de vaga.

Nao entram no MVP:

- previsao automatica de abrir nova turma;
- simulacao avancada de receita por capacidade;
- otimizacao automatica de grade.

Regra MVP:

Calcular ocupacao como alunos previstos ou fixos dividido pela capacidade configurada da aula/turma, quando capacidade existir. Quando studio nao usa capacidade formal, mostrar apenas vagas conhecidas e demanda sem vaga.

Estados:

- `normal`: ocupacao equilibrada;
- `atencao`: turma cheia com demanda, ou horario vazio recorrente;
- `critico`: demanda sem vaga acumulada ou bloqueio afetando varias aulas.

Acao principal:

Abrir Agenda/Turmas/Reposicoes.

Destino:

- `/app/agenda`;
- `/app/turmas`;
- `/app/grade`;
- `/app/reposicoes`;
- uma rota analitica de capacidade apenas se existir no pos-MVP.

Decisao visual MVP:

Capacidade nao tem rota nem imagem propria no MVP. A leitura de ocupacao fica no bloco de Relatorios e a acao abre Agenda, Turmas, Grade ou Reposicoes com filtros aplicados.

## Bloco: Gargalos

Objetivo:

Mostrar travas recorrentes ou acumuladas que impedem o CRM de andar.

Fonte:

- Operacao;
- Tarefas;
- Aprovacoes;
- Inbox;
- Dados/qualidade;
- Agentes/Uso quando disponivel.

Entram no MVP:

- itens sem dono;
- aguardando humano;
- tarefas atrasadas;
- aprovacoes pendentes;
- dados faltando bloqueando fluxo;
- falhas de envio;
- automacao/cota bloqueada, quando a familia Agentes/Uso estiver disponivel.

Nao entram no MVP:

- analise estatistica profunda de gargalo;
- previsao de gargalo futuro;
- recomendacao automatica de reorganizacao de equipe.

Regra MVP:

Listar e contar pendencias abertas por motivo de bloqueio, dono/fila e origem canonica.

Estados:

- `normal`: poucos bloqueios e dentro do prazo;
- `atencao`: acumulado por fila, dono ou origem;
- `critico`: bloqueio com impacto financeiro, aluno ou agenda.

Acao principal:

Abrir origem operacional.

Destino:

- `/app/operacao`;
- `/app/tarefas`;
- `/app/aprovacoes`;
- `/app/inbox`;
- origem canonica do item.

Decisao visual MVP:

Gargalos nao tem rota nem imagem propria no MVP. A leitura de gargalo fica no bloco de Relatorios e a resolucao abre Operacao, Tarefas, Aprovacoes, Inbox ou a origem canonica com filtros aplicados.

## Bloco: Risco

Objetivo:

Mostrar alunos que podem cancelar, reduzir frequencia ou exigir acao de retencao.

Fonte:

- Retencao;
- Alunos;
- Agenda/chamada;
- Financeiro.

Entram no MVP quando Retencao estiver fechada:

- queda de frequencia;
- aluno inativo;
- inadimplencia com risco;
- cancelamento solicitado;
- primeira semana critica;
- reclamacao/satisfacao baixa, se existir.

Nao entram no MVP desta familia:

- score preditivo opaco;
- automacao de salvamento sem humano;
- segmentacao avancada.

Regra MVP:

Herdar os indicadores e estados definidos na familia Retencao.

Estados:

- `baixo`;
- `medio`;
- `alto`;
- `critico`.

Acao principal:

Abrir Retencao ou aluno.

Destino:

- `/app/retencao`;
- `/app/alunos/[id]`;
- `/app/cancelamentos`, se a rota estiver ativa na familia Retencao.

## Bloco: Agentes

Objetivo:

Mostrar qualidade, bloqueios, incidentes e consumo dos agentes.

Status no MVP:

Adiar ate a familia Agentes/Uso estar fechada.

Fonte futura:

- Agentes;
- Execucoes;
- Incidentes;
- Uso/cotas.

Nao entra na primeira imagem de Relatorios se a familia Agentes ainda nao estiver fechada.

## Bloco: Resumo Semanal

Objetivo:

Dar ao gestor uma leitura curta do que mudou na semana.

Fonte:

- agregacao simples dos blocos de dinheiro, vendas, ocupacao, gargalos e risco.

Entram no MVP:

- melhorou;
- piorou;
- exige atencao;
- principais origens para abrir.

Nao entram no MVP:

- narrativa longa gerada por IA obrigatoria;
- comparacao complexa por coorte;
- previsao mensal.

Regra MVP:

Comparar periodo atual com periodo anterior usando contagens e totais simples. Se nao houver periodo anterior suficiente, mostrar apenas estado atual.

Acao principal:

Abrir relatorio ou origem.

Destino:

- `/app/relatorios/semana`;
- fontes operacionais dos blocos.

Decisao visual MVP:

`/app/relatorios/semana` nao precisa imagem propria nesta rodada. Herda a leitura de cards/blocos da imagem 45 e aprofunda o resumo semanal em texto, contagens simples e links para origem.

## Bloco: Exportacoes

Objetivo:

Permitir que o gestor gere ou acompanhe arquivos de relatorio, contabilidade, financeiro ou backup.

Fonte:

- Jobs de exportacao;
- filtros salvos;
- auditoria.

Entram no MVP:

- exportacao solicitada;
- em processamento;
- pronta;
- falhou;
- solicitante;
- filtros usados;
- data de expiracao do arquivo.

Nao entram no MVP:

- exportacoes recorrentes sofisticadas;
- BI customizavel;
- envio automatico externo sem confirmacao.

Regra MVP:

Listar jobs recentes e permitir abrir detalhe.

Acao principal:

Abrir exportacao.

Destino:

- `/app/exportacoes`;
- `/app/exportacoes/[jobId]`.

Contrato minimo de `/app/exportacoes`:

- tipo de exportacao;
- status (`processando`, `pronta`, `falhou`, `expirada`, `cancelada`);
- solicitante;
- origem/familia;
- filtros usados;
- data de solicitacao;
- validade do arquivo;
- acao principal contextual.

Contrato minimo de `/app/exportacoes/[jobId]`:

- parametros e filtros usados;
- status atual;
- historico de processamento;
- erro legivel quando falhar;
- arquivo e validade quando pronto;
- auditoria de solicitacao e download;
- acoes: `Baixar`, `Reprocessar`, `Criar nova com mesmos filtros`, `Copiar link interno` e `Cancelar` quando ainda estiver processando.

Decisao visual MVP:

Exportacoes nao precisa imagem propria nesta rodada. Herda tabela/lista densa + painel lateral de detalhe. Exportacao recorrente/agendada so deve ganhar imagem propria se virar fluxo central depois.

## Paginas E Dados Necessarios

| Pagina | Blocos principais | Complexidade MVP | Imagem |
| --- | --- | --- | --- |
| `/app/relatorios` | dinheiro, vendas, ocupacao, gargalos, risco, exportacoes | Media | Imagem aprovada 45. |
| `/app/relatorios/semana` | resumo semanal por blocos e origem | Baixa/media, herda Relatorios | Sem imagem propria no MVP. |
| `/app/dinheiro-na-mesa` | oportunidades por origem: matriculas, experimental, financeiro, vagas, reposicoes e risco | Media | Imagem aprovada 46. |
| Gargalos | bloqueios por origem/dono/fila | Baixa/media, herda Operacao | Sem rota/imagem propria no MVP. |
| Capacidade | ocupacao, vagas, demanda sem vaga | Baixa/media, herda Agenda/Turmas | Sem rota/imagem propria no MVP. |
| `/app/relatorios/financeiro` | financeiro aprofundado | Baixa, herda Financeiro | Nao agora. |
| `/app/relatorios/vendas` | vendas aprofundado | Baixa, herda Vendas | Nao agora. |
| `/app/relatorios/risco` | risco aprofundado | Depende de Retencao | Nao agora. |
| `/app/relatorios/ocupacao` | ocupacao aprofundada | Media, herda Agenda/Turmas | Nao agora. |
| `/app/relatorios/agentes` | agentes/uso | Depende de Agentes/Uso | Adiar. |
| `/app/exportacoes` | jobs de exportacao | Baixa/media, herda tabela/detalhe | Sem imagem propria no MVP. |
| `/app/exportacoes/[jobId]` | detalhe de job de exportacao | Baixa, herda painel lateral | Sem imagem propria no MVP. |

## Criterio Para Entrar No MVP

Um bloco entra no MVP se:

- usa dados que o CRM ja registra;
- tem acao clara;
- abre uma origem operacional;
- nao depende de predicao ou BI avancado;
- funciona com 0 agentes.

Um bloco fica pos-MVP se:

- depende de score preditivo;
- depende de agente ainda nao mapeado;
- exige configuracao analitica customizada;
- exige forecast sofisticado;
- nao tem acao clara.
