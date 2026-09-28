# Rodada 8 - Auditoria de cobertura cruzada - PT-BR

> Status: v0.1. Esta rodada cruza as Rodadas 1-7 com rotas, telas, casos, fluxos de agente, cotas, auditoria, permissoes, mobile, operacao sem agentes e decisoes abertas.

## Resultado curto

As Rodadas 1-7 agora tem arquitetura funcional v0.1 e especificacao profunda v0.1. Nao encontrei uma area principal sem dona.

O produto ainda nao deve ser chamado de 100% final porque existem decisoes abertas conscientes em `open-product-decisions.pt-BR.md`, principalmente sobre agenda externa, dados sensiveis, retencao de mensagens, politica de reposicao, formula de encaixe, pipeline, pre-matricula, contratos, LGPD, qualidade minima para autonomia e suporte interno.

## Fontes usadas na cobertura

| Cobertura | Fonte canonica atual |
| --- | --- |
| Rotas web/mobile | `web-screen-map.pt-BR.md`, `mobile-screen-map.pt-BR.md`, Rodadas 1-7. |
| Casos candidatos | `product-master-map-v2.pt-BR.md`, `page-case-coverage.pt-BR.csv`. |
| Fluxos de agente | `flow-coverage-matrix.md`, `agent-flow-cardinality-audit.md`, `agent-invocation-ux-matrix.md`. |
| Objetos | `canonical-data-model.pt-BR.md`. |
| Ciclo de vida | `object-lifecycle-map.pt-BR.md`. |
| Fonte da verdade | `source-of-truth-matrix.pt-BR.md`. |
| Permissoes | `permissions-matrix.pt-BR.md`. |
| Cotas | `quota-touchpoints.pt-BR.md`, Rodada 7. |
| Auditoria | `audit-touchpoints.pt-BR.md`, Rodada 7. |
| Operacao sem agentes | `zero-agent-operating-model.pt-BR.md`, Rodadas 1-7. |
| Mensagens | `notification-template-governance.pt-BR.md`. |
| Suporte Taliya | `taliya-internal-ops.pt-BR.md`, Rodada 7. |

## Status por area

| Rodada | Area | Status da cobertura | Observacao |
| --- | --- | --- | --- |
| 1 | Ativacao/setup | Coberta v0.1 | App tambem cobre setup essencial. |
| 2 | Operacao diaria | Coberta v0.1 | Hoje, tarefas, aprovacoes, casos e notificacoes tem papeis claros. |
| 3 | Atendimento/alunos/historico | Coberta v0.1 | Decisoes sensiveis de historico seguem abertas. |
| 4 | Agenda/turmas/aulas/reposicoes | Coberta v0.1 | Encaixe programatico foi explicitado. |
| 5 | Vendas/matricula/comunicados | Coberta v0.1 | Pipeline e pre-matricula precisam decisao final. |
| 6 | Financeiro/retencao/sensiveis | Coberta v0.1 | Autonomia bloqueada para acoes sensiveis. |
| 7 | Agentes/cotas/governanca | Coberta v0.1 | Falta threshold final de qualidade/autonomia. |

## Checks de cobertura

| Check | Resultado |
| --- | --- |
| Toda area funcional tem arquitetura | OK em `functional-architecture.pt-BR.md`. |
| Toda area tem telas web/mobile | OK em `screen-specs-detailed.pt-BR.md` e Rodadas 1-7. |
| Todo caminho critico tem alternativa sem agentes | OK em Rodadas 1-7; reforcado pelo modelo 0 agentes. |
| Toda acao sensivel cita permissao/auditoria | OK em Rodadas 3, 6 e 7; revisar microcopy depois. |
| Cotas aparecem onde IA/WhatsApp/agente consome | OK em Rodadas 1-7; precos finais seguem abertos. |
| Mobile cobre dia a dia | OK para setup essencial, Hoje, atendimento, agenda, professor, vendas rapidas, financeiro essencial, retencao, agentes e cotas. |
| Web cobre configuracao profunda | OK para configuracoes, politicas, agentes, relatorios, auditoria, integracoes e billing. |
| Fluxos de agente tem superficie | OK no nivel de matriz existente; precisa export final all-row em Rodada 10 se o catalogo mudar. |
| Casos de uso tem pagina dona | OK usando `page-case-coverage.pt-BR.csv`; excecoes sensiveis apontam para aprovacao, tarefa, aluno, financeiro ou operacao, sem exigir pagina propria. |
| Integracoes tem comportamento de falha | OK em contratos globais e Rodada 7; provedores reais seguem abertos. |
| Suporte Taliya tem autorizacao | OK em Rodada 7 e privacidade; escopo final segue aberto. |

## Lacunas que nao sao bug, sao decisoes abertas

| Tema | Decisao aberta relacionada |
| --- | --- |
| Agenda externa/provedor calendario | D005 |
| Dados clinicos/sensiveis | D006 |
| Retencao de mensagens | D007 |
| Configuracao avancada no app | D008 |
| Relatorios profundos do MVP | D012 |
| Formula de prioridade do Hoje | D013 |
| Tipos canonicos de caso | D015 |
| Identidade em telefone compartilhado | D016 |
| Historico para professor | D017 |
| Reposicao e encaixe | D020, D021 |
| Pipeline/pre-matricula/cadencia | D024, D025, D026 |
| Contratos, retencao, LGPD | D028, D029, D031 |
| Qualidade/autonomia/reprocessamento/suporte | D032, D033, D034, D035 |

## Ajustes recomendados antes de chamar de 100%

1. Fechar as decisoes que afetam desenho de tela: D013, D014, D015, D016, D017, D020, D021, D024, D025, D029, D032.
2. Gerar uma exportacao final das rotas/telas a partir das Rodadas 1-7.
3. Rodar simulacoes reais da Rodada 9 em manual, copiloto, autonomo e 0 agentes.
4. Atualizar o pacote de prompts so depois das simulacoes.

## Criterio de aceite da Rodada 8

Rodada 8 esta pronta para v0.1 porque:

- nao ha area funcional sem documento;
- nao ha bloco central sem rota/tela;
- nao ha caminho critico exclusivamente dependente de agente;
- riscos restantes estao em decisoes abertas visiveis;
- proximas rodadas podem testar o produto por simulacao em vez de discutir abstratamente.
