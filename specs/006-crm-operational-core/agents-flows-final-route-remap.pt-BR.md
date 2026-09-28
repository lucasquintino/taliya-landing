# Remapeamento Final Dos 96 Fluxos Para Rotas Canonicas - PT-BR

> Status: fonte de verdade v0.1 para fase de produto. A matriz historica `agents-flows-final-flow-contract-matrix.pt-BR.csv` continua valida para comportamento dos 96 fluxos, mas as rotas antigas em `onde_continua` devem ser interpretadas por este remapeamento.

## Regra De Leitura

- Nao estamos alterando a logica dos 96 fluxos.
- Estamos corrigindo o destino de produto para evitar paginas desnecessarias.
- Quando um fluxo antigo apontar para uma rota removida, a execucao deve aparecer no destino canonico abaixo.

## Resumo

| Item | Status |
| --- | --- |
| Fluxos base | 96 cobertos. |
| Fluxos removidos | 0. |
| Fluxos que continuam com rota propria | Maioria dos fluxos de Hoje, Inbox, Agenda, Alunos, Financeiro, Retencao, Operacao, Agentes, Uso e Relatorios. |
| Fluxos com rota remapeada | Fluxos que citavam Contatos, Dados/Qualidade, Historico, Professor, Lista de espera geral, Experimental antigo, Checkout de alunos, Politicas, Auditoria, Recursos, Eventos, Exportacoes, Privacidade, Segmentos e Comunicados. |

## Regras De Remapeamento

| Rota/superficie historica | Destino canonico |
| --- | --- |
| `/app/contatos`, `/app/contatos/[id]` | Contexto em `/app/inbox`, `/app/alunos/[id]`, `/app/interessados` ou drawer de identidade. |
| `/app/dados/qualidade`, `/app/dados/duplicidades` | Contexto em Hoje, Tarefas, Aprovacoes, Onboarding/importacao ou origem da inconsistencia. |
| `/app/historico`, `/app/historico/documentos`, `/app/historico/permissoes` | Perfil do aluno, aba/timeline/historico permitido, aula/chamada ou permissoes. |
| `/app/professores`, `/app/professores/[id]` | Aula, chamada, turma, agenda ou perfil do aluno. |
| `/app/lista-espera` | Contextual em Vendas/Interessados, Agenda/Turmas, Hoje/Tarefas; se for encaixe com credito/reposicao, usar `/app/reposicoes`. |
| `/app/creditos-reposicao` | `/app/reposicoes`. |
| `/app/experimental` | `/app/aulas-experimentais`. |
| `/app/eventos`, `/app/eventos/[eventId]` | Contexto em Agenda/Turmas/Aula. |
| `/app/checkout-alunos` | `/app/matriculas`, com reflexos em Financeiro, Aprovacoes e Operacao. |
| `/app/financeiro/documentos`, `/app/contratos` | Contexto em Financeiro, Matriculas, Perfil do aluno e anexos/detalhes. |
| `/app/auditoria`, `/app/auditoria/[eventId]` | Trilha contextual dentro da tela de origem, aprovacao, execucao, suporte ou backoffice interno quando for Taliya. |
| `/app/politicas`, `/app/politicas/[policyId]`, `/app/politicas/[policyId]/simular` | Configuracoes por area, Agentes/Fluxos e Aprovacoes. |
| `/app/recursos`, `/app/recursos/[resourceId]` | `/app/configuracoes/agenda`. |
| `/app/segmentos`, `/app/segmentos/[segmentId]` | Pos-MVP. No MVP, usar filtros locais em Vendas, Retencao ou Relatorios quando necessario. |
| `/app/comunicados`, `/app/comunicados/[broadcastId]` | Pos-MVP. No MVP, mensagens aparecem em fluxo/contexto, sem broadcast livre. |
| `/app/exportacoes`, `/app/exportacoes/[jobId]` | Acao local da pagina exportavel com status contextual. |
| `/app/privacidade/solicitacoes`, `/app/privacidade/solicitacoes/[requestId]` | Termos/consentimentos contextuais, Aprovacoes e Suporte. |
| `/app/integracoes` | Configuracao da area especifica: canais, pagamentos, agenda, importacao ou notificacoes. |
| `/app/importacao/[jobId]` | Onboarding/importacao e qualidade contextual. |
| `/app/operacao/incidentes`, `/app/operacao/incidentes/[incidentId]` | Operacao, execucao do fluxo e Suporte quando afetar o studio. |

## Fluxos Afetados Por Dominio

| Dominio | Fluxos afetados | Como ler agora |
| --- | --- | --- |
| Atendimento | A6, A7, A8, A9 | Identidade, consentimento, midia e privacidade aparecem no atendimento, no perfil/contexto da pessoa, em aprovacao ou suporte. Sem pagina Contatos/Dados/Auditoria/Privacidade. |
| Agenda | B4, B6, B7, B12, B13, B14, B16 | Lista geral e eventos sao contextuais; creditos/reposicao vao para Reposicoes; experimental usa Aulas experimentais; correcao sensivel usa Aprovacoes e trilha contextual. |
| Vendas | C2, C3, C8, C10, C11, C12, C15 | Experimental vira Aulas experimentais; checkout de aluno vira Matriculas; lista de espera geral e captura/origem ficam em Vendas/Interessados/Agenda/Tarefas. |
| Financeiro | D8, D11, D12, D13, D14 | Documentos/contratos e auditoria ficam contextuais; relatorio financeiro fica em Relatorios/Financeiro; aprovacoes continuam propria. |
| Retencao | E11 | Historico sensivel aparece no perfil do aluno/contexto do caso, sem rota Historico. |
| Gestao/Governanca | F6, F9, F11, F12, F14, F15 | Qualidade, auditoria, importacao, incidentes e politicas deixam de ser hubs soltos e passam para contexto, configuracoes, execucoes, aprovacao ou suporte. |
| Historico/Evolucao | G1, G2, G3, G5, G6, G7, G8, G9, G11, G12 | Professor e historico nao sao familias de menu; vivem em aula, turma, perfil do aluno, permissoes e aprovacao. |

## Fluxos Que Permanecem Sem Mudanca De Destino

| Dominio | Exemplos |
| --- | --- |
| Hoje/Comando | F1, F2, F3, F4, F5, F7, F8, F10. |
| Inbox e atendimento operacional | A1, A2, A3, A4, A5, A10. |
| Agenda base | B1, B2, B3, B5, B8, B9, B10, B11, B15. |
| Vendas/matricula base | C1, C4, C5, C6, C7, C9, C13, C14. |
| Financeiro base | D1, D2, D3, D4, D5, D6, D7, D9, D10, D15. |
| Retencao base | E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E12, E13. |
| Historico permitido com destino atual | G4, G10. |

## Decisao

Os 96 fluxos estao cobertos para produto. O ajuste necessario era de navegacao, nao de comportamento: rotas antigas viram contexto, subvisao, drawer, aprovacao, suporte ou pos-MVP conforme o corte aprovado.
