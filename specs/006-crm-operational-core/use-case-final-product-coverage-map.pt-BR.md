# Mapa Final De Cobertura Dos 157 Casos - PT-BR

> Status: fonte de verdade v0.1 para fase de produto. Este documento nao cria telas novas; ele remapeia o catalogo historico de 157 casos para a navegacao final aprovada.

## Regra De Leitura

- `Pagina propria`: aparece como rota/pagina do CRM.
- `Contextual`: nao vira item de menu nem pagina propria; aparece como drawer, aba, bloco, filtro, detalhe ou acao dentro de outra pagina.
- `Topbar global`: pagina acessada por icone/menu global, fora da sidebar principal.
- `Pos-MVP`: nao entra no produto inicial.
- Quando documentos antigos divergirem, este mapa prevalece junto com `product-decisions-working-log.pt-BR.md`, `final-navigation-web-app.pt-BR.md`, `web-screen-map.pt-BR.md`, `final-screen-contract-matrix.pt-BR.md` e `final-image-route-status-matrix.pt-BR.md`.

## Resumo

| Grupo | Quantidade historica de casos | Destino final |
| --- | ---: | --- |
| Paginas proprias do MVP | 126 | Permanecem em rotas canonicas, com alguns nomes corrigidos. |
| Contextuais no MVP | 23 | Cobertos sem pagina propria. |
| Topbar global | 2 | Billing/assinatura da Taliya. |
| Pos-MVP | 6 | Segmentos e comunicados. |
| Total | 157 | Coberto v0.1. |

## Matriz Por Superficie Historica

| Superficie historica do catalogo | Casos | Decisao final | Destino canonico |
| --- | ---: | --- | --- |
| Onboarding e configuracao inicial | 6 | Pagina propria pre-CRM | `/onboarding/*`. |
| Hoje | 4 | Pagina propria | `/app/hoje`. |
| Inbox e conversas | 6 | Pagina propria | `/app/inbox`, conversa/drawer contextual. |
| Contatos | 3 | Contextual | Inbox, Alunos, Interessados e validacao de identidade. Sem `/app/contatos`. |
| Qualidade de dados | 2 | Contextual | Onboarding/importacao, Hoje, Tarefas, Aprovacoes e origem do problema. Sem `/app/dados/qualidade`. |
| Alunos e perfil | 1 | Pagina propria | `/app/alunos`, `/app/alunos/[id]`. |
| Historico do aluno | 8 | Contextual | Aba/timeline no perfil do aluno e contexto em aula. Sem `/app/historico`. |
| Professor e notas | 4 | Contextual | Aula, Chamada, Turmas, Agenda e perfil do aluno. Sem `/app/professores`. |
| Agenda | 1 | Pagina propria | `/app/agenda`. |
| Grade, turmas e eventos | 4 | Misto | `/app/grade`, `/app/turmas`; eventos/workshops ficam contextuais em Agenda/Turmas/Aula. |
| Aula e chamada | 7 | Pagina propria/detalhe | `/app/aulas/[id]`, chamada dentro da aula. |
| Reposicoes e lista de espera | 5 | Misto | `/app/reposicoes` para reposicao/creditos/encaixe; lista geral contextual em Vendas/Agenda/Tarefas. |
| Interessados e vendas | 7 | Paginas proprias | `/app/vendas`, `/app/interessados`. |
| Aulas experimentais | 4 | Pagina propria | `/app/aulas-experimentais`. Corrige a rota antiga `/app/experimental`. |
| Matriculas | 2 | Pagina propria | `/app/matriculas`; sem `/app/checkout-alunos`. |
| Vendas e origens | 3 | Contextual dentro de Vendas/Relatorios | Origem, indicacao e captura aparecem em `/app/vendas`, `/app/interessados` e relatorios. |
| Financeiro | 2 | Pagina propria | `/app/financeiro`. |
| Pagamentos e cobrancas | 6 | Pagina propria/subvisao | `/app/financeiro`, `/app/financeiro/kanban`, `/app/financeiro/movimentacoes`. |
| Movimentacoes financeiras | 4 | Pagina propria/subvisao | `/app/financeiro/movimentacoes`. |
| Excecoes financeiras contextuais | 5 | Contextual | Financeiro, Aprovacoes, Tarefas, Operacao e Perfil do aluno. |
| Contratos e documentos financeiros | 2 | Contextual | Financeiro, Matriculas, Aluno e anexos/detalhes. Sem pagina propria. |
| Retencao | 10 | Pagina propria | `/app/retencao`. |
| Cancelamentos e reativacao | 3 | Paginas proprias | `/app/cancelamentos`, `/app/retencao/reativacoes`. |
| Reclamacoes e casos sensiveis | 3 | Pagina propria | `/app/reclamacoes`, detalhe contextual. |
| Jornadas e operacao | 8 | Pagina propria | `/app/operacao`. |
| Tarefas e operacao | 3 | Paginas proprias | `/app/tarefas`, `/app/checklists`. |
| Aprovacoes | 1 | Pagina propria | `/app/aprovacoes`. |
| Agentes e fluxos | 7 | Paginas proprias | `/app/agentes`, `/app/fluxos`, simulacao/execucao contextual. |
| Execucoes e incidentes de agentes | 4 | Misto | `/app/fluxos/execucoes/[runId]`; incidentes contextuais em Operacao/Suporte. |
| Uso, cotas e economia | 3 | Pagina propria | `/app/uso`. |
| Relatorios e exportacoes | 8 | Misto | `/app/relatorios`, `/app/dinheiro-na-mesa`; exportacao e acao local em cada pagina exportavel. |
| Configuracoes | 7 | Pagina propria | `/app/configuracoes` com subareas. |
| Politicas operacionais | 0 no CSV dedicado, presente nos docs de fluxo | Contextual | Configuracoes por area, agentes/fluxos e aprovacao. Sem `/app/politicas`. |
| Recursos, feriados e disponibilidade | 4 | Contextual/configuracao | `/app/configuracoes/agenda`. Sem `/app/recursos`. |
| Segmentos e comunicados | 3 | Pos-MVP | Sem `/app/segmentos` e sem `/app/comunicados` no MVP. |
| Integracoes | 2 | Contextual/configuracao | Configuracoes de canal, pagamentos, agenda, importacao e area afetada. Sem hub `/app/integracoes`. |
| Auditoria | 1 | Contextual | Trilhas dentro das telas, detalhes, aprovacao, execucao e suporte. Sem pagina propria para studio. |
| Privacidade e solicitacoes | 4 | Contextual/suporte | Termos aceitos, consentimentos, opt-out, suporte e aprovacao quando sensivel. Sem pagina propria. |
| Assinatura e billing | 2 | Topbar global | `/app/billing` para plano/assinatura da Taliya, fora da sidebar. |

## Conclusao De Cobertura

Os 157 casos continuam cobertos. A diferenca e que o produto final nao transforma todo caso em pagina propria. O corte aprovado reduz ruido de navegacao e concentra o studio nas familias que ele usa no dia a dia.

## Paginas Que Nao Devem Ser Criadas Para Cobrir Casos

| Nao criar | Motivo |
| --- | --- |
| `/app/contatos` | Contato e entidade de suporte ao atendimento/aluno/interessado. |
| `/app/dados/qualidade` | Problema deve aparecer no ponto onde impede uma acao. |
| `/app/historico` | Historico pertence ao perfil do aluno e ao contexto de aula. |
| `/app/professores` | Professor/notas e contexto operacional, nao modulo de gestao separado no MVP. |
| `/app/lista-espera` | Lista geral e contextual; reposicao tem pagina propria quando envolve encaixe/credito. |
| `/app/checkout-alunos` | Matricula, Financeiro, Aprovacoes e Operacao cobrem o fluxo. |
| `/app/politicas` | Politicas sao configuracoes/predefinicoes por area. |
| `/app/recursos` | Recurso, feriado e disponibilidade ficam em Configuracoes de Agenda. |
| `/app/exportacoes` | Exportacao e acao local da pagina exportavel. |
| `/app/integracoes` | Integracao fica na configuracao da area. |
| `/app/auditoria` | Auditoria aparece como historico/trilha contextual. |
| `/app/privacidade/solicitacoes` | Termos, consentimentos e suporte cobrem o uso real do studio. |
| `/app/segmentos` | Pos-MVP. |
| `/app/comunicados` | Pos-MVP. |

## Lacunas Reais Restantes

| Lacuna | Status | Proximo passo |
| --- | --- | --- |
| Imagem da conta basica pre-assinatura | Parcial | Signup 72 e signin 73 salvas; ajustes visuais finos pendentes. |
| Imagem do checkout/assinatura da Taliya | Coberta | Revisao 74, confirmacao 75, recuperacao 76 e confirmacao/setup 77 aprovadas. |
| Imagem do bloqueio ate assinatura confirmada | Coberta | 75 bloqueia enquanto verifica, 76 recupera falha e 77 leva ao setup guiado apos confirmar. |
| Contrato visual final de mobile | Fora do fechamento atual | Voltar depois do web/app shell estar consolidado. |
