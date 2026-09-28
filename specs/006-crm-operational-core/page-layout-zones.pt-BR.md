# Mapa exato de zonas por pagina - PT-BR

> Status: mapa de layout para transformar os casos de uso em telas. Este documento complementa `page-requirements.pt-BR.md` e foi revisado contra as referencias visuais de CRM por jornada.

## Estrutura padrao do CRM web

Todas as paginas principais devem seguir a mesma logica para o gestor nao se perder:

| Zona | O que fica ali |
| --- | --- |
| Menu lateral esquerdo | As 12 entradas principais: Hoje, Inbox, Alunos, Agenda, Vendas, Financeiro, Retencao, Operacao, Agentes, Uso e cotas, Relatorios, Configuracoes. |
| Topo da pagina | Titulo da area, busca, filtros principais, periodo, status, botao de acao primaria e indicadores curtos. |
| Coluna esquerda interna | Filtros, segmentos, filas, etapas ou calendario pequeno, quando a pagina precisar. |
| Centro | A superficie principal: mapa de jornada, lista priorizada, calendario, pipeline, chamada, perfil ou tabela. |
| Painel direito | Contexto do item selecionado, resumo, historico curto, sugestao da IA, acoes manuais, risco, cota e permissao. |
| Rodape/drawer | Formularios, confirmacoes, aprovacao, detalhes longos, logs e anexos. |

## Padrao de cartao de jornada

Todo cartao de jornada, caso, tarefa, lead, aluno em risco, pagamento ou reposicao deve mostrar:

- pessoa ou turma;
- tipo do caso;
- etapa atual;
- responsavel;
- prazo;
- risco;
- proxima acao;
- modo: manual, copiloto ou autonomo;
- custo/cota quando houver IA, mensagem ou automacao;
- ultimo evento importante.

## Estrutura padrao do app mobile

O app nao deve repetir todas as telas administrativas do web. Ele deve resolver o dia.

| Zona mobile | O que fica ali |
| --- | --- |
| Topo | Titulo curto, busca/filtro, atalho de notificacao e perfil. |
| Corpo | Cartoes verticais de conversas, aulas, tarefas, casos, alunos ou alertas. |
| Detalhe | Tela cheia com resumo, historico curto e acoes. |
| Rodape | Acao principal fixa e navegacao curta. |
| Mais | Configuracoes leves, consultas e paginas menos usadas. |

## Paginas web e onde tudo deve ficar

| Pagina | Topo | Esquerda interna | Centro | Direita | Mobile |
| --- | --- | --- | --- | --- | --- |
| Onboarding e configuracao inicial | Progresso do setup e proximo passo | Checklist de etapas | Formulario da etapa atual | Ajuda contextual e impacto do que falta | Nao entra no app |
| Hoje | Data, busca, filtros de prioridade e indicadores do dia | Fila curta por urgencia | Cartoes do dia: aulas, dinheiro, atendimento, riscos e bloqueios | Detalhe do cartao selecionado com acao manual/copiloto | Tela inicial do app com cartoes do dia |
| Inbox e conversas | Busca, canal, status, responsavel e botao nova conversa | Lista de conversas por prioridade | Conversa selecionada | Perfil, historico, resumo, sugestao de resposta e botoes assumir/delegar | Lista de conversas e detalhe em tela cheia |
| Contatos | Busca, filtros e novo contato | Segmentos e duplicidades | Lista de contatos e telefones compartilhados | Detalhe do contato, preferencia, bloqueio e vinculos operacionais | Consulta parcial a partir do aluno/conversa; sem responsaveis/familia/consentimentos como modulos proprios |
| Qualidade de dados | Tipo de problema, impacto e status | Filas de duplicidade, incompletos e bloqueios | Lista de problemas com impacto operacional | Antes/depois, sugestao de correcao, risco e objetos afetados | Aprovacao/consulta para corrigir bloqueios |
| Alunos e perfil do aluno | Busca, status, plano e risco | Lista/segmentos de alunos | Perfil do aluno com agenda, plano, pagamentos e tarefas | Proximas acoes, riscos, conversa e historico curto | Perfil resumido e acoes principais |
| Historico do aluno | Aluno, permissao e periodo | Tipos de registro | Linha do tempo sensivel | Detalhe do registro, quem pode ver e anexos | Consulta restrita quando permitido |
| Professor e notas | Professor, dia e aulas | Lista de aulas do professor | Cartoes de alunos da aula e notas pendentes | Contexto permitido e handoff | Tela do professor para notas e lembretes |
| Agenda | Dia/semana, professor, turma e status | Mini calendario e filtros | Calendario operacional | Aula selecionada, capacidade, conflitos e acoes | Agenda do dia e semana |
| Grade, turmas e eventos | Periodo, unidade e criar turma/evento | Turmas, professores e recursos | Grade semanal editavel | Impacto de mudanca e simulacao | Consulta e ajustes simples |
| Aula e chamada | Aula, horario, professor e status | Alunos esperados | Chamada com presenca, faltas e observacoes | Contexto do aluno e consequencias da falta | Chamada completa no app |
| Reposicoes e lista de espera | Vagas, creditos, periodo e prioridade | Filtros por horario/turma | Fila de pedidos e vagas disponiveis | Candidatos para encaixe e convite | Cartoes para aprovar/resolver encaixe |
| Interessados e vendas | Busca, etapa, origem e temperatura | Etapas do funil | Pipeline por cartoes de lead | Detalhe do lead, conversa, objeções e proxima acao | Consulta e follow-up principal |
| Aulas experimentais | Dia, status e professor | Lista por status | Agenda comercial e cartoes de experimental | Detalhe, lembrete, pos-aula e conversao | Acoes de lembrete, remarcacao e pos-aula |
| Matriculas | Status de pre-matricula e pendencias | Checklist de dados | Lista de matriculas em andamento | Pendencias, contrato, pagamento e primeira aula | Consulta e aprovacao simples |
| Vendas e origens | Periodo, origem e conversao | Origens e segmentos | Painel de fontes, indicacoes e demanda sem vaga | Detalhe da origem e acoes de segmento | Consulta |
| Financeiro | Mes, recebido, previsto, atraso e falhas | Filtros de status | Visao de caixa e filas financeiras | Item financeiro selecionado e acao segura | Resumo e alertas importantes |
| Movimentacoes financeiras | Periodo, vencimento, status e canal | Filtros por atraso, forma, tipo, comprovante, conciliacao e excecao | Lista completa de movimentacoes | Detalhe, comprovante, conversa, lembrete, aprovacao e auditoria | Fila parcial de cobranca |
| Excecoes financeiras sensiveis | Herdado da rota de origem | Sem pagina propria | Sem central propria no MVP | Drawer/aprovacao/tarefa com impacto, motivo e auditoria | Aprovacoes e consulta contextual |
| Contratos e documentos financeiros | Busca, status e tipo | Tipos de documento | Lista de contratos/recibos | Detalhe, assinatura, envio e anexo | Consulta |
| Retencao | Risco, periodo e grupo de alunos | Segmentos de risco | Cartoes de alunos em risco, inativos e primeira semana | Plano de acao, mensagem sugerida e tarefa manual | Cartoes de risco prioritario |
| Cancelamentos e reativacao | Status, motivo e elegibilidade | Segmentos de cancelamento | Jornada de salvamento, cancelamento e reativacao | Detalhe, motivo, historico e proxima tentativa | Consulta e acoes essenciais |
| Reclamacoes e casos sensiveis | Severidade, prazo e responsavel | Fila por risco | Cartoes de reclamacao/caso sensivel | Plano de resposta, pausa de automacao e auditoria | Aprovacao e acompanhamento |
| Jornadas e operacao | Status, area, responsavel e etapa | Etapas e filtros por tipo | Mapa de jornadas com cartoes conectados por etapa | Caso selecionado, historico curto, sugestao e acoes | Cartoes de jornada prioritarios |
| Tarefas e operacao | Responsavel, prazo e prioridade | Donos e status | Lista priorizada de tarefas | Detalhe da tarefa, origem e comentarios | Minhas tarefas e tarefas do dia |
| Aprovacoes | Risco, origem e prazo | Tipos de aprovacao | Fila de aprovacoes com antes/depois | Mensagem, impacto, custo/cota e botoes aprovar/editar/rejeitar | Aprovacao rapida com detalhe |
| Agentes e fluxos | Agente, modo, status e plano | Lista de agentes e fluxos | Cartoes de fluxo com modo manual/copiloto/autonomo | Regras, simulacao, limites e ultima execucao | Consulta e pausas rapidas |
| Execucoes e incidentes de agentes | Periodo, status, agente e custo | Filtros de erro | Lista de execucoes e incidentes | Explicacao, ferramenta usada, correcao e reexecucao segura | Alertas e consulta |
| Uso, cotas e economia | Cota usada, restante e previsao | Tipos de consumo | Grafico simples e lista de consumo por area/fluxo | Acoes de economia, pacote extra e bloqueios | Consulta de cota e alertas |
| Relatorios e exportacoes | Periodo, area e exportar | Tipos de relatorio | Paineis enxutos e tabelas de apoio | Filtros salvos, explicacao e links para casos | Consulta |
| Configuracoes | Busca, area e salvar | Menu de configuracoes | Formulario da secao selecionada | Impacto, testes e auditoria | Nao prioritario no app |
| Politicas operacionais | Politica, versao e vigencia | Tipos de politica | Editor de regras em linguagem simples | Simulacao de impacto e historico de versoes | Nao prioritario no app |
| Recursos, feriados e disponibilidade | Periodo, recurso e professor | Recursos e fechamentos | Calendario de disponibilidade | Impacto em aulas e avisos necessarios | Consulta e alerta |
| Segmentos e comunicados | Publico, canal e status | Segmentos salvos | Construtor de publico e comunicados | Elegibilidade, consentimento, custo e aprovacao | Aprovacao/consulta |
| Integracoes | Status dos conectores | Lista de integracoes | Cartoes de WhatsApp, pagamentos e importacao | Logs curtos, teste e reprocessamento | Nao prioritario no app |
| Auditoria | Periodo, usuario, objeto e risco | Filtros | Lista de eventos | Antes/depois e origem da alteracao | Consulta sensivel |
| Privacidade e solicitacoes | Status, tipo e prazo | Tipos de solicitacao | Fila LGPD, opt-out e consentimentos | Validacao, execucao e auditoria | Aprovacao sensivel |
| Assinatura e billing | Plano, status e fatura | Produtos e add-ons | Plano atual, faturas e pacotes | Upgrade, pacote, falha e historico | Consulta |

## Ajuste de linguagem para produto

Na interface em PT-BR, evitar termos tecnicos quando existir alternativa clara:

| Evitar | Usar |
| --- | --- |
| Workflow | Fluxo |
| Execution | Execucao ou atividade |
| Run | Rodada |
| Payload | Dados recebidos |
| Tool call | Acao executada |
| Agent trace | Historico do agente |
| Escalation | Encaminhamento |
| Exception | Excecao ou caso especial |
| SLA | Prazo combinado |
| Segment | Grupo |

## Decisao final desta rodada

Nao adicionar novas paginas agora.

O caminho mais forte e ajustar a forma das paginas existentes para o padrao de jornada das referencias. A cobertura continua:

- 12 menus principais;
- 38 paginas/superficies;
- 157 casos de uso cobertos;
- app mobile focado no dia a dia;
- IA embutida em contexto, sem obrigar o gestor a usar agente.
