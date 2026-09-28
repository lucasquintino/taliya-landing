# Mapa Mestre Final De Produto - PT-BR

> Status: resumo executivo v0.1 da fase de produto. Use este documento para entender o estado final sem precisar reler todas as rodadas.

## Produto

Taliya CRM e um CRM operacional para studios de Pilates com agentes de IA integrados ao sistema. O WhatsApp e canal; o CRM e o sistema operacional.

O produto inicial nao e um conjunto de paginas soltas. Ele e organizado por familias de trabalho do studio: Hoje, Inbox, Alunos, Agenda, Vendas, Financeiro, Retencao, Operacao, Agentes, Uso, Relatorios e Configuracoes.

## Navegacao Final

### Sidebar

| Ordem | Familia | Rota |
| ---: | --- | --- |
| 1 | Hoje | `/app/hoje` |
| 2 | Inbox | `/app/inbox` |
| 3 | Alunos | `/app/alunos` |
| 4 | Agenda | `/app/agenda` |
| 5 | Vendas | `/app/vendas` |
| 6 | Financeiro | `/app/financeiro` |
| 7 | Retencao | `/app/retencao` |
| 8 | Operacao | `/app/operacao` |
| 9 | Agentes | `/app/agentes` |
| 10 | Uso e cotas | `/app/uso` |
| 11 | Relatorios | `/app/relatorios` |
| 12 | Configuracoes | `/app/configuracoes` |

### Topbar Interna

A topbar interna mostra subitens da familia selecionada. Ela evita uma sidebar gigante e mantem contexto claro para o gestor.

| Familia | Subitens |
| --- | --- |
| Hoje | Hoje, Semana, Criticos, Minha fila. |
| Inbox | Todos, Nao lidos, Aguardando, Com IA, Com humano, Erros. |
| Alunos | Lista; perfil com Resumo, Agenda, Financeiro, Historico, Tarefas, Conversas. |
| Agenda | Agenda, Grade, Turmas, Aulas, Reposicoes. |
| Vendas | Pipeline, Interessados, Aulas experimentais, Matriculas. |
| Financeiro | Visao geral, Kanban, Movimentacoes. |
| Retencao | Riscos, Cancelamentos, Reativacoes, Reclamacoes. |
| Operacao | Jornadas, Tarefas, Checklists, Aprovacoes. |
| Agentes | Agentes, Fluxos, Simulacoes, Execucoes. |
| Uso | Visao geral, Extrato. |
| Relatorios | Relatorios, Dinheiro na Mesa. |
| Configuracoes | Studio, Equipe, Permissoes, Agenda, Pagamentos/Financeiro, Canais, Notificacoes. |

### Topbar Global

Busca, alertas, uso/cota, suporte, plano/assinatura e perfil/conta ficam globais. Suporte e Billing nao entram na sidebar.

## Paginas Proprias Do MVP

| Grupo | Paginas |
| --- | --- |
| Pre-CRM | Criar conta basica, checkout externo, aguardo de assinatura, onboarding/setup. |
| Comando | Hoje. |
| Atendimento | Inbox. |
| Alunos | Alunos, Perfil do aluno. |
| Agenda | Agenda, Grade, Turmas, Aula, Reposicoes. |
| Vendas | Vendas, Interessados, Aulas experimentais, Matriculas. |
| Financeiro | Financeiro, Kanban, Movimentacoes. |
| Retencao | Retencao, Cancelamentos, Reativacoes, Reclamacoes. |
| Operacao | Operacao, Tarefas, Checklists, Aprovacoes. |
| Agentes | Agentes, Fluxos, Simulacoes, Execucoes. |
| Gestao | Uso e cotas, Relatorios, Dinheiro na Mesa, Configuracoes. |
| Global | Suporte, Billing/Assinatura. |
| Interno Taliya | Backoffice interno separado em `/internal/*`. |

## Itens Contextuais Do MVP

| Item | Onde aparece |
| --- | --- |
| Contatos | Inbox, Alunos, Interessados, identidade/telefone compartilhado. |
| Qualidade de dados | Origem do problema, Hoje, Tarefas, Aprovacoes, Onboarding/importacao. |
| Historico do aluno | Perfil do aluno e contexto de aula. |
| Professor/notas | Aula, Chamada, Turmas, Agenda e perfil. |
| Lista de espera geral | Vendas/Interessados, Agenda/Turmas, Hoje/Tarefas. |
| Creditos de reposicao | Reposicoes. |
| Checkout de alunos | Matriculas, Financeiro, Aprovacoes, Operacao. |
| Politicas operacionais | Configuracoes por area, agentes/fluxos, aprovacao. |
| Recursos/feriados/disponibilidade | Configuracoes de Agenda. |
| Exportacoes | Acao local em cada pagina exportavel. |
| Integracoes | Configuracao de canais, pagamentos, agenda, importacao e notificacoes. |
| Auditoria | Historico/trilha contextual. |
| Privacidade | Termos, consentimentos, opt-out, aprovacao e suporte. |

## Pos-MVP

| Item | Decisao |
| --- | --- |
| Segmentos | Produto futuro/separado. |
| Comunicados/broadcast livre | Produto futuro/separado. |
| Lista de espera geral como pagina autonoma | Produto futuro se o uso real justificar. |
| Mobile profundo | Depois do web/app shell consolidado. |

## Cobertura

| Area | Resultado |
| --- | --- |
| Imagens | Mapeadas por rota/familia em `final-image-route-status-matrix.pt-BR.md`. |
| Paginas | Mapeadas em `web-screen-map.pt-BR.md` e `final-screen-contract-matrix.pt-BR.md`. |
| 157 casos | Cobertos em `use-case-final-product-coverage-map.pt-BR.md`. |
| 96 fluxos | Cobertos em `agents-flows-final-route-remap.pt-BR.md`; remapeamento corrige rotas antigas sem mudar comportamento. |
| Decisoes de corte | Registradas em `product-decisions-working-log.pt-BR.md`. |

## O Que Falta Antes De Implementar

| Falta | Motivo |
| --- | --- |
| Revisar imagens necessarias para conta basica, checkout/assinatura e bloqueio ate assinatura confirmada | Esta decisao nasceu na revisao atual e ainda nao tem imagem propria. |
| Decidir se o pacote de imagens finais deve ser complementado ou se algumas telas herdam padrao existente | Evita gerar imagem desnecessaria. |
| Congelar o pacote de docs que sera usado como briefing de implementacao | Evita que documentos historicos antigos voltem a guiar rotas removidas. |

## Nao Falta Para Produto V0.1

| Item | Status |
| --- | --- |
| Sidebar/topbar | Fechadas. |
| Suporte | Pagina propria via topbar global. |
| Billing Taliya | Pagina propria via topbar global; financeiro dos alunos separado. |
| Aprovacoes | Pagina propria. |
| Checklists | Pagina propria. |
| Aulas experimentais | Pagina propria. |
| Matriculas | Pagina propria sem checkout separado de aluno. |
| Retencao/cancelamentos/reativacoes/reclamacoes | Paginas proprias. |
| Relatorios/Dinheiro na Mesa | Paginas proprias. |
