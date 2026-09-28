# Matriz final de superficies, rotas e contratos - PT-BR

> Status: matriz canonica pos-revisao de produto. Esta versao reflete a decisao de sidebar por familias, topbar interna por subitens e varios itens contextuais sem pagina propria.

## Como usar

1. Use `final-navigation-web-app.pt-BR.md` para entender sidebar, topbar interna, topbar global, pre-CRM e backoffice.
2. Use `web-screen-map.pt-BR.md` para saber quais rotas sao paginas proprias, contextuais, topbar global, pos-MVP ou cortadas.
3. Use esta matriz para cobertura funcional por superficie de produto.
4. Use `page-case-coverage.pt-BR.csv` como historico de cobertura dos 157 casos, sabendo que varias "paginas" agora sao contextuais.

## Resumo consolidado

| Item | Total/decisao |
| --- | ---: |
| Entradas de sidebar web | 12 |
| Abas fixas mobile | 5 |
| Casos de uso do catalogo atual | 157 |
| Fluxos finais de agentes | 96 |
| Suporte | Pagina propria via topbar global |
| Billing Taliya | Pagina propria via topbar global/menu de conta |
| Segmentos/Comunicados | Pos-MVP |
| Contatos, auditoria, privacidade, politicas, integracoes e qualidade de dados | Contextuais, sem pagina propria |

## Familias de sidebar

| Familia | Rota inicial | Subitens/topbar | Imagens principais |
| --- | --- | --- | --- |
| Hoje | `/app/hoje` | Filtros leves: Hoje, Semana, Criticos, Minha fila | 17, 18, 19, 20 |
| Inbox | `/app/inbox` | Filtros/chips de conversa | 24 Inbox |
| Alunos | `/app/alunos` | Perfil com abas internas | 27, 28 |
| Agenda | `/app/agenda` | Agenda, Grade, Turmas, Aulas, Reposicoes | 26, 29, 31, 35, 36 |
| Vendas | `/app/vendas` | Pipeline, Interessados, Experimentais, Matriculas | 37, 38, 39, 40 |
| Financeiro | `/app/financeiro` | Visao geral, Kanban, Movimentacoes | 30, 32, 33, 34 |
| Retencao | `/app/retencao` | Riscos, Cancelamentos, Reativacoes, Reclamacoes | 41, 42, 43, 44 |
| Operacao | `/app/operacao` | Jornadas, Tarefas, Checklists, Aprovacoes | 21, 22, 23, 24 Checklists, 25 |
| Agentes | `/app/agentes` | Agentes, Fluxos, Simulacoes, Execucoes | 52, 53, 54, 56, 58, 59, 70 |
| Uso e cotas | `/app/uso` | Visao geral, Extrato | 68, 69 |
| Relatorios | `/app/relatorios` | Relatorios, Dinheiro na Mesa | 45, 46 |
| Configuracoes | `/app/configuracoes` | Studio, Equipe, Permissoes, Agenda, Pagamentos/Financeiro, Canais, Notificacoes | 60, 61, 62, 63, 64 |

## Contrato por superficie propria

| Superficie | Rota principal | Blocos obrigatorios | Acoes essenciais | Estados essenciais | Observacao |
| --- | --- | --- | --- | --- | --- |
| Conta basica | Pre-CRM | Google, Microsoft, e-mail com link seguro, login com e-mail/senha | criar conta, entrar | assinatura ausente, conta criada | Nao libera CRM antes da assinatura confirmada. |
| Escolha de plano/checkout Taliya | Pre-CRM + provedor externo | plano, valor, cupom, checkout hospedado, status de confirmacao, recuperacao e setup guiado | escolher plano, revisar, iniciar pagamento, tentar novamente, comecar setup, agendar ajuda | revisao, verificando, pendente, aprovado, falha | Fora do CRM operacional; imagens 74, 75, 76 e 77 aprovadas. |
| Onboarding/setup | `/onboarding/*` | studio, equipe, canais, planos, alunos, turmas, agenda, pagamento, revisao, agente de configuracao | continuar, salvar, revisar, publicar | incompleto, pronto, pendente | Usa shell proprio, sem sidebar operacional; comeca pela 77. |
| Hoje | `/app/hoje` | prioridades, aulas, dinheiro, tarefas, aprovacoes, alertas, cotas | abrir origem, aprovar, delegar, resolver | sem pendencia, critico, bloqueado | Hoje nao substitui Operacao. |
| Inbox/conversas | `/app/inbox` | lista, conversa, contexto, vinculo, sugestao, falhas | responder, assumir, criar tarefa, abrir aluno/interessado | novo, aguardando humano, falha, opt-out | Contatos sao contextuais. |
| Alunos | `/app/alunos` | lista, filtros, status, resumo lateral | abrir perfil, conversar, tarefa, agendar | ativo, pausado, inadimplente, risco | Sem pagina propria de Contatos. |
| Perfil do aluno | `/app/alunos/[id]` | resumo, agenda, financeiro, historico, tarefas, conversas | nota, tarefa, abrir cobranca, abrir aula, conversar | sensivel restrito, risco, pendencia | Historico/professor/documentos contextuais. |
| Agenda | `/app/agenda` | calendario, aulas, conflitos, capacidade, filtros | abrir aula, criar aula, ajustar horario | vaga, lotado, conflito, feriado | Eventos/workshops contextuais. |
| Grade | `/app/grade` | semana modelo, bloqueios, turmas, disponibilidade | ajustar grade, simular impacto | indisponivel, conflito, publicado | Feriados/recursos em Configuracoes de Agenda. |
| Turmas | `/app/turmas` | lista, capacidade, professor, alunos, demanda | criar/editar turma, abrir aula, ver demanda | lotada, vaga, conflito | Lista de espera geral contextual. |
| Aula/Chamada | `/app/aulas/[id]` | alunos, presenca, faltas, observacoes, creditos | fazer chamada, corrigir, abrir reposicao, nota | chamada pendente, falta, no-show | Professor/notas contextuais. |
| Reposicoes | `/app/reposicoes` | pedidos, creditos, vagas, candidatos, conflitos | encontrar encaixe, reservar, convidar, consumir credito | sem vaga, conflito, aguardando resposta, vencido | Sem `/app/creditos-reposicao`; sem lista de espera geral. |
| Vendas/Pipeline | `/app/vendas` | etapas, origem, proxima acao, dono, conversa | qualificar, mover, follow-up, converter | novo, quente, sem resposta, sem vaga | Sem Segmentos/Comunicados. |
| Interessados | `/app/interessados` | lista, perfil resumido, origem, status | abrir conversa, qualificar, agendar experimental | novo, sem vaga, perdido, pronto | Contato contextual. |
| Aulas experimentais | `/app/aulas-experimentais` | aulas, interessado, status, pos-aula | confirmar, remarcar, marcar compareceu/faltou, matricular | agendada, faltou, converter | Rota canonica substitui `/app/experimental`. |
| Matriculas | `/app/matriculas` | checklist, dados, plano, primeira aula, pagamento inicial | validar, cobrar, converter, tarefa | faltando, aguardando pagamento, pronto | Sem `/app/checkout-alunos`. |
| Financeiro | `/app/financeiro` | filas, KPIs, prioridades, cobranca selecionada | abrir cobranca, lembrar, confirmar, tarefa | aberto, atraso, falha, conciliacao | Financeiro dos alunos, nao Billing Taliya. |
| Financeiro Kanban | `/app/financeiro/kanban` | etapas, cards, responsaveis, proxima acao | mover, lembrar, promessa, aprovacao | a vencer, atraso, promessa, resolvido | Subitem de Financeiro. |
| Movimentacoes financeiras | `/app/financeiro/movimentacoes` | tabela, filtros, comprovantes, ajustes | confirmar, conciliar, exportar, tarefa | pago, aberto, falhou, disputa | Documentos/comprovantes contextuais. |
| Retencao | `/app/retencao` | riscos, frequencia, inativos, sinais | tarefa, mensagem, caso, acompanhar | risco baixo/medio/alto | Pagina propria. |
| Cancelamentos | `/app/cancelamentos` | pedidos, motivos, salvamento, pausa | registrar, salvar, converter pausa | aberto, salvamento, cancelado | Pagina propria. |
| Reativacoes | `/app/retencao/reativacoes` | ex-alunos, elegibilidade, oportunidade | iniciar retorno, reservar vaga validada | elegivel, nao contatar, reativado | Pagina propria. |
| Reclamacoes | `/app/reclamacoes` | severidade, dono, prazo, resposta | classificar, pausar automacao, escalar, resolver | severo, aguardando, resolvido | Pagina propria. |
| Operacao/Jornadas | `/app/operacao` | jornadas, casos, bloqueios, alertas | abrir caso, atribuir, mover, corrigir | aberto, bloqueado, aguardando, resolvido | Central profunda; Hoje so resume. |
| Tarefas | `/app/tarefas` | fila, dono, prazo, origem, caso | assumir, delegar, concluir, reagendar | atrasada, sem dono, aguardando | Subitem de Operacao. |
| Checklists | `/app/checklists` | rotinas recorrentes, execucoes, responsaveis, historico | iniciar, concluir, atribuir, abrir tarefa | pendente, em execucao, atrasado | Pagina propria dentro de Operacao. |
| Aprovacoes | `/app/aprovacoes` | proposta, antes/depois, risco, impacto, motivo | aprovar, editar, rejeitar, pedir dados | pendente, expirada, aprovada, rejeitada | Pagina propria dentro de Operacao. |
| Agentes | `/app/agentes` | catalogo, slots, agentes ativos, status | abrir agente, ativar/pausar quando permitido | ativo, nao configurado, bloqueado | Subitem de Agentes. |
| Fluxos | `/app/fluxos`, `/app/fluxos/[flowId]` | rotina, fluxo, modo, regras, fallback | editar, simular, preparar publicacao | rascunho, pronto, ativo, pausado | Politicas de agente ficam aqui. |
| Simulacoes | `/app/fluxos/[flowId]/simular` | cenarios, resultado, celular/preview, limites | testar/simular, ajustar, publicar | seguro, bloqueado, precisa ajuste | Imagem 58 usa linguagem final de simulacao. |
| Publicacao de rotina | Contextual em Fluxos | preflight, impacto, o que sera ativado | publicar, revisar, cancelar | pronto, bloqueado, publicado | Imagem 59; nao precisa aba propria. |
| Execucao de fluxo | `/app/fluxos/execucoes/[runId]` | resumo, linha do tempo, regras, continuidade | abrir origem, criar tarefa, explicar | sucesso, falha, excecao | Recibo operacional, nao log tecnico. |
| Uso e cotas | `/app/uso` | consumo, cota, origem, alertas, economia | abrir extrato, abrir fluxo, ver alternativa | 70%, 90%, 100%, bloqueado | Add-ons ficam em Billing. |
| Extrato de uso | `/app/uso/extrato` | lancamentos, origem, agente, fluxo, status | filtrar, abrir origem | estimado, confirmado, falhou | Subitem de Uso. |
| Relatorios | `/app/relatorios` | indicadores, filtros, origem, exportacao local | filtrar, abrir origem, exportar | sem dados, carregando, pronto | Exportacao e acao local. |
| Dinheiro na Mesa | `/app/dinheiro-na-mesa` | oportunidades, origem, impacto, proxima acao | abrir oportunidade, criar tarefa, abrir origem | oportunidade, sem dono, resolvido | Pagina propria. |
| Configuracoes | `/app/configuracoes` | hub/cards por area | abrir card, editar area | incompleto, salvo, pendente | Sem politicas/integracoes/privacidade como paginas proprias. |
| Config. permissoes | `/app/configuracoes/permissoes` | papeis, equipe, acessos sensiveis | convidar, alterar papel, remover | convite pendente, ativo | Pagina propria de configuracao. |
| Config. pagamentos/financeiro | `/app/configuracoes/pagamentos` | meios, regras simples, baixa manual, modelos | salvar, testar, revisar impacto | pendente, salvo, falha | Pagamentos do studio para alunos, nao Billing Taliya. |
| Config. agenda | `/app/configuracoes/agenda` | feriados, bloqueios, disponibilidade, reposicao | salvar regra, criar excecao | impacto pendente, salvo | Recursos/feriados/disponibilidade aqui. |
| Config. notificacoes/canais | `/app/configuracoes/notificacoes` | canais, notificacoes, horarios, mensagens internas | salvar, testar canal | desconectado, salvo, falha | Integracoes tecnicas embutidas. |
| Suporte Taliya | `/app/suporte` | tickets, status, suporte 24/7, grants, historico | abrir ticket, falar com suporte, autorizar/revogar grant | aberto, respondido, acesso ativo | Topbar global; nao e Inbox dos alunos. |
| Billing Taliya | `/app/billing` | plano, assinatura, status, fatura, add-ons | atualizar pagamento, ver faturas, add-on, suporte | ativo, falha, vencido | Topbar global/menu de conta; separado do Financeiro. |
| Faturas Taliya | `/app/billing/invoices` | fatura atual, historico, status | ver fatura, resolver pagamento | paga, pendente, falhou | Dentro de Billing. |
| Add-ons Taliya | `/app/billing/add-ons` | add-ons ativos, pacotes, mais agentes | comprar/solicitar, abrir suporte | ativo, vazio, pendente | Dentro de Billing. |

## Superficies contextuais ou removidas como pagina propria

| Superficie antiga | Decisao atual | Onde aparece |
| --- | --- | --- |
| Contatos | Sem pagina propria | Alunos, Interessados, Inbox, Matriculas, busca. |
| Qualidade de dados | Sem pagina propria | Onboarding/importacao, Hoje, Tarefas, Aprovacoes, origem do dado. |
| Historico do aluno | Sem pagina propria | Perfil do aluno. |
| Professor e notas | Sem pagina propria | Aula/Chamada, Perfil do Aluno, Turmas, Agenda. |
| Contratos e documentos financeiros | Sem pagina propria | Financeiro, Matriculas, Perfil do Aluno. |
| Recursos, feriados e disponibilidade | Sem pagina propria | Configuracoes de Agenda. |
| Exportacoes | Sem pagina propria | Acao local em cada pagina exportavel. |
| Integracoes | Sem pagina propria | Configuracoes da area correspondente. |
| Auditoria | Sem pagina propria para studio | Historico contextual e suporte quando necessario. |
| Privacidade e solicitacoes | Sem pagina propria | Termos/consentimentos contextuais e Suporte. |
| Politicas operacionais | Sem pagina propria | Configuracoes/pre-definicoes por area e Agentes/Fluxos. |
| Segmentos e comunicados | Pos-MVP | Fora do produto atual. |
| Lista de espera geral | Sem pagina propria | Vendas/Interessados, Agenda/Turmas, Hoje/Tarefas, conversas. |
| Creditos de reposicao | Sem pagina propria | Reposicoes. |
| Checkout de alunos | Sem pagina propria | Matriculas, Financeiro, Aprovacoes, Operacao. |
| Eventos/workshops | Sem pagina propria | Agenda, Turmas, Aula. |
| Gestao | Nao criar rota propria | Relatorios e Dinheiro na Mesa. |

## Regra final por modo de agente

| Modo | Onde aparece | Limite |
| --- | --- | --- |
| Manual | Todas as areas criticas. | Usuario executa e sistema registra. |
| Copiloto | Sugestoes, resumos, priorizacao, rascunhos e preparacao. | Usuario revisa antes de acao externa ou sensivel. |
| Autonomo | Fluxos permitidos de baixo risco ou com excecoes. | Exige permissao, cota, configuracao publicada, auditoria e fallback. |
