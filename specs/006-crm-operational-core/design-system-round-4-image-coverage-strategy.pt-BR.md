# Estrategia De Cobertura De Imagens Web - Rodada 4

> Status: v0.1. Objetivo: evitar gerar uma imagem para cada rota quando a rota ja pode ser coberta por uma imagem, padrao de layout, drawer ou componente aprovado.

## Decisao Central

Nao vamos gerar imagens para todas as rotas.

Vamos gerar imagens por **padrao visual-funcional reutilizavel**.

Quando uma imagem mostra drawer ou painel lateral aberto, ela representa um **estado selecionado para documentacao visual**, nao o carregamento padrao da rota. O estado inicial das paginas web deve manter drawer/painel de detalhe fechado ate selecao explicita de item ou acesso direto a detalhe.

Drawers e paineis laterais podem ter varios modos dentro da mesma rota. Uma imagem aprovada com painel aberto normalmente documenta **um modo representativo**, nao todos os modos possiveis daquela pagina.

Regra pratica:

- se os outros modos usam a mesma largura, hierarquia, densidade, acoes base e origem canonica, eles herdam a imagem aprovada e precisam apenas de contrato textual;
- se um modo muda a arquitetura da pagina, cria fluxo visual novo, exige comparacao em massa ou muda a decisao do usuario, ele pode precisar de imagem propria;
- nunca criar uma imagem nova apenas porque o texto do painel muda por status.

Uma rota so precisa de imagem propria quando muda pelo menos um destes pontos:

- superficie principal;
- modelo mental do usuario;
- tipo de interacao dominante;
- densidade/hierarquia;
- painel/drawer de detalhe;
- governanca de risco/cota/permissao;
- estado critico ainda nao coberto por imagem aprovada.

Se uma rota usa o mesmo padrao de outra imagem aprovada, ela deve herdar a cobertura visual e receber apenas contrato textual.

## Tipos De Cobertura

| Tipo | Quando usar | Resultado esperado |
| --- | --- | --- |
| Imagem propria | Pagina tem layout/fluxo novo ou decisao visual importante. | Gerar prompt e imagem aprovada. |
| Herdada | Pagina usa padrao ja aprovado com outro conteudo. | Documentar qual imagem cobre a rota. |
| Drawer/estado | Pagina nao precisa imagem inteira, mas precisa estado de detalhe, modal ou decisao. | Gerar ou documentar drawer/estado especifico. |
| Contrato textual | Rota e variacao simples de lista/tabela/filtro ja coberta. | Nao gerar imagem; registrar regras. |
| Futuro/mobile | Nao pertence ao web atual ou exige design system mobile. | Registrar para rodada futura. |

## Padroes Visuais Ja Aprovados

| Padrao aprovado | Imagem/documento base | Cobre |
| --- | --- | --- |
| App shell web | `16_round-4.1S_app-shell_01_base-web.png` | Moldura de todas as paginas web. |
| Hoje acima da dobra | `17_round-4.1A_hoje_01_acima-da-dobra.png` | Mesa de comando do dia. |
| Hoje com drawer | `18_round-4.1A_hoje_02_resolver-prioridade.png` e contrato de drawers | Detalhe acionavel por tipo vindo do Hoje. |
| Hoje critico/historico | imagens 19/20 ou docs aprovados da familia Hoje | Estado critico e continuidade abaixo da dobra. |
| Operacao kanban | `21_round-4.1B_operacao_01_kanban-geral.png` | Kanban/lista de acompanhamento operacional. |
| Operacao com drawer | `22_round-4.1B_operacao_02_kanban-com-drawer.png` | Drawer por tipo em contexto de acompanhamento. |
| Lista/kanban operacional | referencia `3B.3` + imagem 21 | Tarefas, filas, riscos, pendencias e listas densas similares. |
| Drawer/feedback | referencia `3B.2` + imagem 22 | Detalhes, bloqueios, confirmacoes e acoes contextuais. |
| Aprovacao/decisao | referencia `3B.4` + contrato de drawers | Fila de decisoes e propostas. |
| Cota/plano/governanca | referencia `3B.5` | Planos, limites, permissao, cota e bloqueio por entitlement. |

## Regras Para Decidir Se Gera Nova Imagem

Gerar nova imagem quando:

- a tela tem uma composicao principal ainda nao vista;
- a tela e comercialmente/operacionalmente central;
- a tela tem risco alto de ser mal interpretada sem visual;
- o drawer/modal muda o entendimento da pagina;
- a pagina precisa provar diferenca clara de outra pagina parecida;
- a imagem sera usada como base para varias rotas futuras.

Nao gerar nova imagem quando:

- so muda a lista de objetos;
- so muda filtro/topbar;
- a tela e detalhe de item coberto por drawer;
- a pagina usa a mesma estrutura de kanban/lista/tabela ja aprovada;
- a superficie e rota tecnica ou consulta secundaria;
- o estado e mobile e ainda nao ha design system mobile.

## Matriz Inicial De Cobertura Por Familia

### 4A - Hoje + Operacao

| Pagina/superficie | Status visual | Decisao |
| --- | --- | --- |
| Hoje | Imagens proprias aprovadas | Fechada. |
| Operacao/Pendencias | Imagens proprias 21 e 22 aprovadas | Fechada. |
| Tarefas | Imagem propria aprovada: `23_round-4.1C_tarefas_01_lista-detalhe.png` + drawer compartilhado de Tarefa | Fechada com 1 imagem; `/app/tarefas/[taskId]` herda a mesma cobertura. |
| Checklists | Imagem propria aprovada: `24_round-4.1C_checklists_01_lista-execucao-detalhe.png` | Fechada com 1 imagem; `/app/checklists/[runId]` herda o painel lateral. |
| Aprovacoes | Imagem propria aprovada: `25_round-4.1C_aprovacoes_01_lista-decisao-detalhe.png` | Fechada com 1 imagem; `/app/aprovacoes/[approvalId]` herda o painel lateral. |
| Incidentes no grupo Operacao | Herda tipo de card em Operacao; detalhe fica em Agentes/Execucoes | Sem imagem propria agora. |
| Auditoria/Historico | Herda atividade recente; detalhe fica em Auditoria/Admin | Sem imagem propria agora. |

### 4B - Atendimento + Alunos

| Pagina/superficie | Status visual | Decisao |
| --- | --- | --- |
| Inbox/Conversas | Precisa imagem propria | Layout 3 colunas com conversa e contexto. |
| `/app/inbox` | Imagem propria aprovada: `24_round-4.1D_inbox_01_conversa-aberta.png` | 1 imagem cobre Inbox e `/app/conversas/[id]`; painel direito representa estado selecionado. |
| `/app/conversas/[id]` | Herdada | Usa a imagem 24 com conversa selecionada por URL; sem imagem propria nesta rodada. |
| `/app/envios` e `/app/envios/[sendId]` | Contrato textual | Herda lista densa + detalhe lateral; imagem propria so se falhas/tentativas de envio virarem fluxo visual central. |
| Contatos | Contrato textual | Nao gerar imagem agora; herda lista simples, Inbox e Qualidade de Dados. Sem responsaveis/familia no MVP. |
| Alunos | Imagem propria aprovada: `27_round-4.1E_alunos_01_lista-perfil-resumido.png` | Cobre `/app/alunos`; painel direito representa resumo acionavel, nao perfil completo. |
| Perfil do aluno | Imagem propria aprovada: `28_round-4.1E_aluno-perfil_01_resumo-operacional.png` | Cobre `/app/alunos/[id]` com aba Resumo ativa; demais abas herdam familias especificas. |
| Linha do tempo do aluno | Herdada/contrato textual | Nao precisa imagem agora; herda bloco de linha do tempo da imagem 28 e componentes de Historico/Auditoria. |
| Professor/Notas | Pode herdar Agenda + perfil resumido | Contrato textual suficiente inicialmente. |

### 4C - Agenda

Status da familia: fechada para web v0.1 em `design-system-round-4-1F-agenda-final-audit.pt-BR.md`.

| Pagina/superficie | Status visual | Decisao |
| --- | --- | --- |
| Agenda | Imagem propria aprovada: `26_round-4.1F_agenda_01_calendario-operacional.png` | Calendario semanal operacional com painel de aula selecionada. |
| Turmas | Imagem propria aprovada: `35_round-4.1F_turmas_01_lista-detalhe.png` | `/app/turmas` cobre lista de turmas recorrentes, capacidade, alunos fixos, vagas e painel de turma selecionada. |
| Grade | Imagem propria aprovada: `36_round-4.1F_grade_01_semana-modelo-bloqueio.png` | `/app/grade` cobre semana-modelo recorrente e blocos que geram aulas futuras. A imagem inclui bloqueio aplicado, mas bloqueio e acao situacional/secundaria, nao objetivo central da Grade. |
| `/app/turmas/[id]` | Herdada | Usa detalhe/painel da imagem de Turmas/Grade; rota direta renderiza a mesma estrutura expandida. |
| Eventos | Herdada inicialmente | `/app/eventos` e `/app/eventos/[eventId]` herdam Turmas para estrutura/capacidade e Aula para execucao/chamada. Imagem propria so se eventos/workshops virarem modulo forte. |
| Aula/Chamada | Imagem propria aprovada: `29_round-4.1F_aula_01_detalhe-com-chamada.png` | Uma rota principal `/app/aulas/[id]`; chamada abre como painel/drawer contextual, sem `/app/aulas/[id]/chamada` como pagina separada nesta rodada. |
| Reposicoes | Imagem propria aprovada: `31_round-4.1F_reposicoes_01_fluxo-encaixe.png` | `/app/reposicoes` cobre fluxo completo de reposicao e encaixe; creditos aparecem dentro da reposicao. O painel direito e contextual e muda por item clicado: pendente, com opcao, aguardando resposta, agendada, bloqueada, expirada/cancelada/usada ou novo pedido. Modo manual/copiloto/autonomo e politica do fluxo, nao do aluno. Opcoes resumidas aparecem no painel; agenda completa de vagas abre como estado expandido. Lista de espera geral nao entra nesta pagina. |
| Bloqueios de agenda/feriados/indisponibilidade | Drawer/estado contextual | Sem pagina principal propria. Inicia por acao secundaria em Agenda, Grade, Turma ou Aula; painel/drawer mostra tipo, periodo, escopo, impacto, aviso e publicacao. Recurso/sala/equipamento e opcional. |

### Paineis Contextuais Ja Cobertos

| Pagina | Imagem base | Modos herdados sem nova imagem obrigatoria |
| --- | --- | --- |
| Hoje | `18_round-4.1A_hoje_02_drawer-tarefa.png` + contrato de drawers | Tarefa, aprovacao, bloqueio, fila humana, financeiro, incidente, alerta/cota e problema de dados, conforme tipo real. |
| Operacao | `22_round-4.1B_operacao_02_kanban-com-drawer.png` | Mesmo drawer do tipo real vindo de Hoje/Operacao, mudando apenas contexto de acompanhamento. |
| Tarefas | `23_round-4.1C_tarefas_01_lista-detalhe.png` | Aberta, atrasada, aguardando resposta, bloqueada, com aprovacao vinculada, concluida/cancelada e criar tarefa. |
| Checklists | `24_round-4.1C_checklists_01_lista-execucao-detalhe.png` | Em andamento, passo bloqueado, atrasado, concluido, pulado/cancelado e criar/editar rotina. |
| Aprovacoes | `25_round-4.1C_aprovacoes_01_lista-decisao-detalhe.png` | Pendente, mensagem, financeira/sensivel, aguardando dados, aprovada/rejeitada, expirada/bloqueada. |
| Inbox | `24_round-4.1D_inbox_01_conversa-aberta.png` | Conversa identificada, identidade incerta, opt-out, falha de envio, agente pausado/bloqueado e assunto sensivel. |
| Alunos | `27_round-4.1E_alunos_01_lista-perfil-resumido.png` | Ativo, pendencia financeira, reposicao pendente, dados incompletos, pausado/inativo e risco/alerta. |
| Perfil do aluno | `28_round-4.1E_aluno-perfil_01_resumo-operacional.png` | Resumo, pendencia, tarefa, conversa, financeiro e agenda/reposicao selecionados. |
| Agenda | `26_round-4.1F_agenda_01_calendario-operacional.png` | Aula confirmada, chamada pendente, vaga/reposicao, conflito, filtro rapido e recurso/professor indisponivel. |
| Turmas | `35_round-4.1F_turmas_01_lista-detalhe.png` | Turma ativa, cheia, com vaga, pausada, professor a definir, aluno fixo selecionado, ajuste de horario/capacidade e impacto estrutural. |
| Grade | `36_round-4.1F_grade_01_semana-modelo-bloqueio.png` | Semana-modelo, bloco recorrente selecionado, impacto futuro e bloqueio aplicado como estado situacional. |
| Aula | `29_round-4.1F_aula_01_detalhe-com-chamada.png` | Chamada, detalhe do aluno, reposicao, observacao, conflito, aviso e correcao de chamada. |
| Reposicoes | `31_round-4.1F_reposicoes_01_fluxo-encaixe.png` | Pendente, com opcao, aguardando resposta, agendada/reservada, bloqueada, encerrada e novo pedido. |
| Financeiro | `30_round-4.1F_financeiro_01_visao-geral-filas.png` e drawer planejado `32_round-4.1F_financeiro_02_drawer-cobranca-selecionada.png` | Cobranca, pagamento confirmado, comprovante pendente, falha, promessa e excecao sensivel. |

### 4D - Vendas + Retencao

| Pagina/superficie | Status visual | Decisao |
| --- | --- | --- |
| Vendas/Interessados - Kanban | Imagem propria aprovada: `37_round-4.1G_vendas_01_pipeline-kanban.png` | Pipeline de vendas tem modelo mental proprio, mas herda a casca visual de Financeiro Kanban/Operacao. Cobre `/app/vendas`; sem painel esquerdo; filtros rapidos ficam na barra superior; etapas extras usam scroll horizontal. Cadastro manual entra como drawer/botao no pipeline, sem `/app/interessados/novo`. Perdidos vira filtro/status, nao pagina propria. Sem toggle interno Kanban/Lista. |
| Vendas/Interessados - Lista | Imagem propria aprovada: `38_round-4.1G_vendas_02_lista-interessados.png` | Visao lista/tabela no estilo Movimentacoes do Financeiro, com barra de filtros, painel esquerdo de filtros rapidos, lista central e painel direito contextual. Cobre `/app/vendas/lista`, `/app/interessados` e ajuda `/app/interessados/[id]` a herdar o drawer/painel. Sem toggle interno Kanban/Lista. |
| Experimental | Imagem propria aprovada: `39_round-4.1G_experimental_01_lista-acompanhamento.png` | Conecta Vendas com Agenda: entra quando um interessado tem aula experimental real vinculada; acompanha confirmacao, falta, remarcacao, pos-aula e conversao; sai para Matriculas, Perdido ou nova remarcacao. Nao substitui Agenda, Inbox ou Vendas. |
| Matriculas | Imagem propria aprovada: `40_round-4.1G_matriculas_01_checklist-conversao.png` | Checklist simples de conversao em aluno, sem checkout separado. Cobre `/app/matriculas`; conversao so habilita com checklist obrigatorio completo; primeira aula vem da Agenda; pagamento inicial pode ser item obrigatorio conforme politica do studio. Metodos de pagamento exibidos em Matriculas sao herdados de Configuracoes/Financeiro e filtrados por permissao, politica e integracao. Matriculas pode acionar cobranca inicial, mas Financeiro e a fonte da verdade para cobranca, conciliacao, comprovante, falha, promessa, desconto, estorno e auditoria. Sem `/app/checkout-alunos` como pagina propria nesta rodada. |
| Retencao | Imagem propria aprovada: `41_round-4.1H_retencao_01_riscos-lista-drawer.png` | Painel/fila de risco com drawer de aluno selecionado; ajustes finais documentados em `design-system-round-4-1H-retencao-image-plan.pt-BR.md`. |
| Cancelamentos | Imagem propria aprovada: `42_round-4.1H_cancelamentos_01_fila-salvamento-drawer.png` | Fila de pedidos de saida, pausa e salvamento com drawer de decisao humana; confirmar cancelamento exige confirmacao forte e automacoes pausadas. |
| Reativacao | Imagem propria aprovada: `43_round-4.1H_reativacoes_01_ex-alunos-retorno.png` | Fila de ex-alunos, pausados e inativos elegiveis para retorno; nao e venda nova nem cancelamento ativo. Reserva de vaga exige validacao e `Nao contatar` bloqueia mensagens. |
| Reclamacoes/Casos sensiveis | Imagem propria aprovada: `44_round-4.1H_reclamacoes_01_fila-caso-sensivel-drawer.png` | Fila de reclamacoes com severidade, automacao pausada, plano de resolucao, resposta revisada e escalonamento humano. Estado severo extra so se acesso restrito/escalonamento mudar muito a tela. |
| Comunicados | Pos-MVP | Nao pertence ao pipeline principal de Vendas e nao entra como imagem desta familia. Deve virar agente/superficie separada pos-MVP, com contrato proprio. |

### 4E - Financeiro + Documentos

| Pagina/superficie | Status visual | Decisao |
| --- | --- | --- |
| Financeiro - visao geral | Aprovada/documentada | `30_round-4.1F_financeiro_01_visao-geral-filas.png`: pagina principal com filtros de periodo, prioridades financeiras e filas. |
| Financeiro - drawer de cobranca | Aprovada/documentada | `32_round-4.1F_financeiro_02_drawer-cobranca-selecionada.png`: mesma pagina com item financeiro selecionado e acoes seguras. |
| Financeiro - kanban | Aprovada/documentada | `33_round-4.1F_financeiro_03_kanban-financeiro.png`, operacao por estagio em `/app/financeiro/kanban`. |
| Financeiro - movimentacoes/tabela | Aprovada/documentada | `34_round-4.1F_financeiro_04_movimentacoes-filtros-drawer.png`, tabela completa em `/app/financeiro/movimentacoes`, com mensalidade, cobranca, parcela, pagamento, conciliacao, falha, promessa, estorno, desconto, ajuste e comprovante. |
| Excecoes financeiras sensiveis | Sem imagem propria no MVP | Resolver visualmente por Financeiro, Kanban, Movimentacoes, Aprovacoes, Tarefas, Aluno ou Operacao. Nao gerar rota/imagem `Casos financeiros`. |
| Documentos financeiros | Herdada | `/app/financeiro/documentos` usa documentos `3C.2`, tabela `3B.3`, drawer `3B.2` e auditoria `3C.3`; sem imagem propria no MVP. |

### 4F - Agentes + Uso

| Pagina/superficie | Status visual | Decisao |
| --- | --- | --- |
| Agentes/Fluxos | Precisa imagem propria | Configuracao, modo e builder sao unicos. |
| Execucoes/Incidentes | Precisa imagem propria | Trace, erro, fallback e reprocessamento seguro sao unicos. |
| Uso/Cotas | Precisa imagem propria | Governanca de custo/cota tem modelo proprio. |

### 4G - Relatorios + Admin

| Pagina/superficie | Status visual | Decisao |
| --- | --- | --- |
| Relatorios/Gestao | Imagem propria aprovada: `45_round-4.1I_relatorios_01_visao-gestao.png` | `/app/relatorios` e o hub de gestao, sem criar `/app/gestao`; mostra blocos acionaveis com origem, periodo, impacto e acao, sem virar dashboard generico. `/app/relatorios/semana` herda esta imagem e aprofunda o resumo semanal por contrato textual. |
| Dinheiro na mesa | Imagem propria aprovada: `46_round-4.1I_dinheiro-na-mesa_01_oportunidades-por-origem.png` | `/app/dinheiro-na-mesa` e uma mesa de oportunidades por origem, nao uma tabela financeira. Cobre blocos de Matriculas, Experimental, Financeiro recuperavel, Vagas, Reposicoes e Risco; drawer e contextual e acoes financeiras aparecem somente quando aplicaveis. |
| Gargalos | Bloco herdado no MVP | Nao recebe rota/imagem propria agora para nao duplicar Hoje/Operacao. O bloco em Relatorios abre Operacao, Tarefas, Aprovacoes, Inbox ou origem canonica com filtros aplicados. |
| Capacidade | Bloco herdado no MVP | Nao recebe rota/imagem propria agora para nao duplicar Agenda/Turmas/Grade/Reposicoes. O bloco de Ocupacao abre as origens com filtros aplicados. |
| Exportacoes | Contrato textual no MVP | `/app/exportacoes` e `/app/exportacoes/[jobId]` herdam tabela/job + detalhe lateral; imagem propria so se exportacao recorrente/agendada virar fluxo central. |
| Configuracoes | Herda forms + governanca | Sem imagem propria obrigatoria inicialmente. |
| Politicas | Pode precisar imagem propria | Recomendada se simular/publicar politica for central. |
| Segmentos/Comunicados | Pos-MVP | Fora do MVP atual; quando entrar, tratar como agente/superficie propria de Comunicacao. |
| Integracoes | Herda sistema/logs/importacao | Contrato textual inicialmente. |
| Auditoria | Herda diff/log `3C.3` | Contrato textual inicialmente. |
| Privacidade | Herda LGPD/grant `3C.3` | Contrato textual inicialmente. |
| Suporte | Imagem propria aprovada: `47_round-4.1J_suporte_01_central-studio-taliya.png` | `/app/suporte` cobre central studio ↔ Taliya com agente de suporte 24/7, tickets, status de servicos, grants e detalhe lateral. Nao e Inbox nem atendimento aos alunos; agente de suporte nao conta como agente operacional do studio. |
| Billing | Herda plano/cota `3B.5` | Contrato textual inicialmente. |

### 4K - Taliya Interno / Backoffice

Status da familia: contrato criado em `taliya-internal-backoffice-contract.pt-BR.md`.

| Pagina/superficie | Status visual | Decisao |
| --- | --- | --- |
| `/internal` | Imagem propria aprovada: `48_round-4.1K_internal_01_visao-operacional.png` | Mesa operacional interna da Taliya; modelo mental diferente do CRM do studio. Mostra leads Taliya, tenants, tickets, grants, incidentes, billing/entitlements e copiloto interno limitado. |
| `/internal/tenants` | Imagem propria aprovada: `49_round-4.1K_internal_02_tenants-lista-detalhe.png` | Lista de clientes/studios, status, plano, tickets, grants, incidentes e billing. A imagem tem correcao documentada: nao usar checkboxes por linha como padrao; selecao e por clique em linha e painel lateral. |
| `/internal/tenants/[tenantId]` | Imagem propria aprovada: `50_round-4.1K_internal_03_tenant-detalhe-usuarios-grants.png` | Visao 360 de tenant com usuarios, entitlements, uso, suporte, grants e auditoria. A imagem tem correcao documentada: numeros antes dos blocos sao artefato visual e nao fazem parte obrigatoria do padrao. |
| `/internal/leads` | Herdada inicialmente | Pode herdar Vendas/Pipeline e Vendas/Lista, desde que fique claro que sao leads da Taliya, nao do studio. |
| `/internal/support` | Herdada inicialmente | Herda Suporte 47 + lista/detalhe, mas no lado interno da Taliya. |
| `/internal/support/grants` | Herdada/estado sensivel | Herda grants, auditoria e detalhe; imagem propria so se decisao de grant ficar visualmente central. |
| `/internal/incidents` | Herdada inicialmente | Herda Operacao/Incidentes e logs. |
| `/internal/billing` | Herdada futuramente | Herda Uso/Cotas/Billing quando a familia Agentes/Uso/Cotas for fechada. |
| `/internal/audit` | Herdada | Herda auditoria/log/diff. |

Imagens recomendadas:

- `48_round-4.1K_internal_01_visao-operacional.png`;
- `49_round-4.1K_internal_02_tenants-lista-detalhe.png`;
- `50_round-4.1K_internal_03_tenant-detalhe-usuarios-grants.png`.

## Resultado Pratico

Em vez de gerar imagem para todas as 38 superficies, a meta inicial deve ser gerar apenas as paginas que criam padroes novos.

Estimativa inicial:

- ja aprovadas: App shell, Hoje, Operacao;
- proximas imagens realmente provaveis: Aprovacoes, Inbox/Conversas, Alunos/Perfil, Agenda, Aula/Chamada, Vendas, Retencao, Financeiro, Agentes/Fluxos, Execucoes/Incidentes, Uso/Cotas, Relatorios;
- demais rotas herdam padroes ou ficam com contrato textual ate aparecer necessidade.

Essa estrategia deve ser revisada apos cada familia fechada.
