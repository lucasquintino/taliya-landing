# Mapa web final do Taliya CRM - PT-BR

> Status: mapa web canonico pos-revisao de produto. Este documento reflete as decisoes registradas em `product-decisions-working-log.pt-BR.md` e a navegacao final de `final-navigation-web-app.pt-BR.md`.

## Regra central

Pagina propria nao significa item de sidebar. A sidebar tem 12 familias principais; cada familia pode ter topbar interna, detalhes, drawers e acoes contextuais.

O CRM do studio e separado de:

- pre-CRM: conta, assinatura e onboarding antes do app;
- topbar global: suporte, billing, perfil, alertas e busca;
- backoffice interno Taliya: `/internal/*`.

## Sidebar web

| Sidebar | Rota inicial | Topbar interna |
| --- | --- | --- |
| Hoje | `/app/hoje` | Sem abas estruturais; filtros leves. |
| Inbox | `/app/inbox` | Filtros/chips de conversa. |
| Alunos | `/app/alunos` | Alunos; perfil tem abas internas. |
| Agenda | `/app/agenda` | Agenda, Grade, Turmas, Aulas, Reposicoes. |
| Vendas | `/app/vendas` | Pipeline, Interessados, Experimentais, Matriculas. |
| Financeiro | `/app/financeiro` | Visao geral, Kanban, Movimentacoes. |
| Retencao | `/app/retencao` | Riscos, Cancelamentos, Reativacoes, Reclamacoes. |
| Operacao | `/app/operacao` | Jornadas, Tarefas, Checklists, Aprovacoes. |
| Agentes | `/app/agentes` | Agentes, Fluxos, Simulacoes, Execucoes. |
| Uso e cotas | `/app/uso` | Visao geral, Extrato. |
| Relatorios | `/app/relatorios` | Relatorios, Dinheiro na Mesa. |
| Configuracoes | `/app/configuracoes` | Hub/cards por area. |

## Pre-CRM

| Superficie | Rota/estado | Decisao |
| --- | --- | --- |
| Criar conta basica | A definir no produto publico/autenticacao | Google, Microsoft ou e-mail com link seguro; sem senha na primeira tela. |
| Login | A definir no produto publico/autenticacao | Conta sem assinatura confirmada nao acessa `/app`. |
| Escolher plano | Antes do checkout hospedado | Fora do CRM operacional. |
| Checkout hospedado | Provedor externo | Fora do CRM operacional. |
| Confirmacao de assinatura | Estado de conta pre-CRM | Imagem 75; aparece ao iniciar pagamento seguro e verifica automaticamente. |
| Assinatura pendente/falha | Estado de conta pre-CRM | Imagem 76; permite tentar pagamento novamente, voltar aos planos ou falar com suporte. |
| Assinatura confirmada | Estado de conta pre-CRM | Imagem 77; confirma assinatura ativa e leva para setup guiado. |
| Onboarding/setup | `/onboarding/*` | Comeca somente depois da assinatura confirmada; guiado por agente de configuracao. |

## Paginas proprias do app do studio

| Familia | Pagina | Rota principal | Imagem canonica | Observacao |
| --- | --- | --- | --- | --- |
| Hoje | Hoje | `/app/hoje` | 17, 18, 19, 20 | Mesa de comando; abre origens em outras familias. |
| Inbox | Inbox/conversas | `/app/inbox` | 24 Inbox | Conversas e atendimento; conversa pode abrir como detalhe. |
| Alunos | Alunos | `/app/alunos` | 27 | Lista operacional. |
| Alunos | Perfil do aluno | `/app/alunos/[id]` | 28 | Inclui historico, agenda, financeiro, tarefas e conversas contextuais. |
| Agenda | Agenda | `/app/agenda` | 26 | Calendario operacional. |
| Agenda | Grade | `/app/grade` | 36 | Semana modelo, bloqueios e regras visiveis. |
| Agenda | Turmas | `/app/turmas` | 35 | Lista/detalhe de turmas. |
| Agenda | Aula/Chamada | `/app/aulas/[id]` | 29 | Chamada pode ser painel/drawer dentro da aula. |
| Agenda | Reposicoes | `/app/reposicoes` | 31 | Creditos dentro do fluxo; lista de espera geral fora. |
| Vendas | Pipeline | `/app/vendas` | 37 | Kanban comercial. |
| Vendas | Interessados | `/app/interessados` | 38 | Lista de leads/interessados. |
| Vendas | Aulas experimentais | `/app/aulas-experimentais` | 39 | Acompanhamento de experimentais. |
| Vendas | Matriculas | `/app/matriculas` | 40 | Checklist de conversao; sem checkout separado. |
| Financeiro | Financeiro visao geral | `/app/financeiro` | 30, 32 | Filas, prioridades e detalhe de cobranca. |
| Financeiro | Kanban financeiro | `/app/financeiro/kanban` | 33 | Operacao por etapa. |
| Financeiro | Movimentacoes | `/app/financeiro/movimentacoes` | 34 | Tabela/consulta de pagamentos, cobrancas e ajustes. |
| Retencao | Retencao/riscos | `/app/retencao` | 41 | Riscos e oportunidades de salvar alunos. |
| Retencao | Cancelamentos | `/app/cancelamentos` | 42 | Fila de salvamento/cancelamento. |
| Retencao | Reativacoes | `/app/retencao/reativacoes` | 43 | Ex-alunos e retorno. |
| Retencao | Reclamacoes | `/app/reclamacoes` | 44 | Casos sensiveis. |
| Operacao | Jornadas/casos | `/app/operacao` | 21, 22 | Central profunda de trabalho operacional. |
| Operacao | Tarefas | `/app/tarefas` | 23 | Fila de tarefas. |
| Operacao | Checklists | `/app/checklists` | 24 Checklists | Rotinas recorrentes do studio. |
| Operacao | Aprovacoes | `/app/aprovacoes` | 25 | Fila transversal de decisoes sensiveis. |
| Agentes | Agentes | `/app/agentes` | 52, 53 | Catalogo e detalhe. |
| Agentes | Fluxos | `/app/fluxos`, `/app/fluxos/[flowId]` | 54, 56 | Rotinas/fluxos e configuracao. |
| Agentes | Simulacoes | `/app/fluxos/[flowId]/simular` | 58 | Simular antes de publicar. |
| Agentes | Execucoes | `/app/fluxos/execucoes/[runId]` | 70 | Recibo operacional de execucao real. |
| Uso e cotas | Uso e cotas | `/app/uso` | 68 | Consumo, alertas e economia. |
| Uso e cotas | Extrato | `/app/uso/extrato` | 69 | Ledger/extrato de uso. |
| Relatorios | Relatorios | `/app/relatorios` | 45 | Paineis e indicadores. |
| Relatorios | Dinheiro na Mesa | `/app/dinheiro-na-mesa` | 46 | Oportunidades acionaveis. |
| Configuracoes | Hub configuracoes | `/app/configuracoes` | 60 | Hub de configuracoes pos-go-live. |
| Configuracoes | Equipe/permissoes | `/app/configuracoes/permissoes` | 61 | Papeis e permissoes. |
| Configuracoes | Pagamentos/financeiro | `/app/configuracoes/pagamentos` | 62 | Pagamentos e regras financeiras. |
| Configuracoes | Agenda | `/app/configuracoes/agenda` | 63 | Agenda, feriados, bloqueios, disponibilidade e reposicoes. |
| Configuracoes | Notificacoes/canais | `/app/configuracoes/notificacoes` | 64 | Canais, notificacoes e mensagens internas. |

## Topbar global: paginas proprias fora da sidebar

| Area | Rota | Imagem canonica | Como acessar |
| --- | --- | --- | --- |
| Suporte Taliya | `/app/suporte` | 47 | Topbar global/icone de suporte. |
| Assinatura Taliya | `/app/billing` | 65 | Chip de plano/menu de conta/topbar global. |
| Faturas Taliya | `/app/billing/invoices` | 66 | Dentro de Billing. |
| Add-ons Taliya | `/app/billing/add-ons` | 67 | Dentro de Billing ou CTA de cota/add-on. |

Suporte e Billing sao paginas proprias, mas nao sao familias operacionais da sidebar.

## Backoffice interno Taliya

| Area | Rota | Imagem canonica | Decisao |
| --- | --- | --- | --- |
| Operacao interna | `/internal` | 48 | Fora do app do studio. |
| Tenants | `/internal/tenants` | 49 | Fora do app do studio. |
| Tenant detalhe | `/internal/tenants/[tenantId]` | 50 | Fora do app do studio. |
| Sales inbox interno | `/internal/sales-inbox` | Sem imagem do CRM operacional | Operacao comercial da propria Taliya; nao e Inbox do studio. |

## Contextuais, sem pagina propria

| Item | Onde vive |
| --- | --- |
| Contatos | Alunos, Interessados, Inbox/Conversas, Matriculas, busca e seletores. |
| Qualidade de dados | Onboarding/importacao, Alunos, Agenda, Financeiro, Aprovacoes, Hoje e Tarefas. |
| Historico do aluno | Perfil do aluno e origens relacionadas. |
| Professor e notas | Aula/Chamada, Perfil do Aluno, Turmas e Agenda. |
| Contratos/documentos financeiros | Financeiro, Matriculas, Perfil do Aluno e historico contextual. |
| Excecoes financeiras | Financeiro, Aprovacoes, Tarefas, Aluno e Operacao. |
| Recursos/feriados/disponibilidade | Configuracoes de Agenda e contexto de Agenda/Turmas/Aula. |
| Exportacoes | Acao local em cada pagina exportavel. |
| Integracoes | Configuracoes da area correspondente e alertas contextuais. |
| Auditoria | Historico/contexto da acao; sem central para o studio. |
| Privacidade/solicitacoes | Termos, consentimentos contextuais e Suporte para excecoes. |
| Politicas operacionais | Configuracoes/pre-definicoes por area e Agentes/Fluxos. |
| Lista de espera geral | Vendas/Interessados, Agenda/Turmas, Hoje/Tarefas e conversas. |
| Creditos de reposicao | Reposicoes. |
| Checkout de alunos | Matriculas, Financeiro, Aprovacoes e Operacao. |
| Eventos/workshops | Agenda, Turmas e Aula. |

## Pos-MVP / produto futuro

| Item | Decisao |
| --- | --- |
| Segmentos | Pos-MVP/produto futuro. |
| Comunicados/campanhas | Pos-MVP/produto futuro. |
| Marketing amplo | Fora do produto atual. |

## Rotas que nao devem ser criadas como pagina propria agora

| Rota/tema | Decisao |
| --- | --- |
| `/app/contatos` | Contextual. |
| `/app/dados/qualidade` | Contextual. |
| `/app/historico` | Contextual no perfil do aluno. |
| `/app/professores` | Contextual em aula/turma/aluno. |
| `/app/financeiro/documentos` | Contextual em Financeiro/Aluno/Matriculas. |
| `/app/eventos` | Contextual em Agenda/Turmas/Aula. |
| `/app/creditos-reposicao` | Dentro de Reposicoes. |
| `/app/lista-espera` | Contextual; sem pagina propria. |
| `/app/checkout-alunos` | Dentro de Matriculas/Financeiro/Aprovacoes/Operacao. |
| `/app/politicas` | Configuracoes/pre-definicoes por area. |
| `/app/exportacoes` | Acao local de cada pagina exportavel. |
| `/app/integracoes` | Configuracoes por area. |
| `/app/auditoria` | Historico contextual. |
| `/app/privacidade/solicitacoes` | Termos/consentimentos contextuais e Suporte. |
| `/app/segmentos` | Pos-MVP. |
| `/app/comunicados` | Pos-MVP. |
| `/app/gestao` | Nao criar; usar Relatorios e Dinheiro na Mesa. |
