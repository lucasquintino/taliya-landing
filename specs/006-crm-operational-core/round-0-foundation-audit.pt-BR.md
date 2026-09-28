# Mini-auditoria da Rodada 0 - PT-BR

> Status: Rodada 0 v0.1 criada. Esta auditoria registra o que foi fechado, o que mudou e o que ainda precisa validacao.

## Objetivo da rodada

Criar contratos globais antes de detalhar telas:

- dados;
- ciclo de vida;
- fonte da verdade;
- permissoes;
- botoes;
- estados;
- cotas;
- auditoria;
- politicas;
- falhas de integracao;
- operacao com 0 agentes;
- qualidade de agentes;
- migracao/importacao;
- suporte Taliya;
- metricas;
- mensagens/templates.

## Documentos criados

| Documento | Papel |
| --- | --- |
| `canonical-data-model.pt-BR.md` | Objetos canonicos do CRM. |
| `object-lifecycle-map.pt-BR.md` | Ciclos de vida dos objetos criticos. |
| `source-of-truth-matrix.pt-BR.md` | Fonte da verdade e conflito de dados. |
| `permissions-matrix.pt-BR.md` | Papeis, permissoes e acoes sensiveis. |
| `action-button-taxonomy.pt-BR.md` | Verbos, botoes e confirmacoes. |
| `ui-state-taxonomy.pt-BR.md` | Estados globais e por objeto. |
| `quota-touchpoints.pt-BR.md` | Cotas, limites e downgrade. |
| `audit-touchpoints.pt-BR.md` | Eventos auditaveis. |
| `operational-policy-versioning.pt-BR.md` | Politicas e versoes. |
| `integration-failure-contracts.pt-BR.md` | Falhas e fallback de integracoes. |
| `zero-agent-operating-model.pt-BR.md` | Operacao completa no plano Base. |
| `agent-quality-evaluation.pt-BR.md` | Qualidade, erro e correcao de agentes. |
| `migration-import-plan.pt-BR.md` | Entrada de studios reais. |
| `taliya-internal-ops.pt-BR.md` | Operacao interna e suporte Taliya. |
| `product-success-metrics.pt-BR.md` | Metricas de valor. |
| `notification-template-governance.pt-BR.md` | Mensagens, templates e notificacoes. |
| `functional-architecture.pt-BR.md` | Esqueleto canonico para areas. |
| `screen-specs-detailed.pt-BR.md` | Esqueleto canonico para telas. |
| `open-product-decisions.pt-BR.md` | Decisoes abertas centralizadas. |

## O que ficou fechado como contrato

- Base/0 agentes continua sendo CRM operacional completo.
- Agentes nao podem executar sem entitlement, modo, cota, dados, permissao e politica.
- Suporte Taliya depende de acesso temporario, escopado e auditado.
- Politicas sensiveis precisam de versao, simulacao e snapshot.
- Cota precisa ter alternativa manual e explicacao na UI.
- Fonte da verdade deve evitar sobrescrever dados criticos por importacao/agente.
- Mobile deve resolver rotina, mas configuracao pesada e auditoria longa ficam web-first.

## Lacunas ainda abertas

As lacunas foram registradas em `open-product-decisions.pt-BR.md`.

Principais:

- E14 e G13 como fluxos proprios ou subfluxos;
- multi-unidade;
- provedor financeiro;
- agenda externa;
- limite de dados clinicos/sensiveis;
- retencao de mensagens;
- configuracao avancada no app;
- precos de add-ons;
- relatorios profundos do MVP.

## Risco da proxima rodada

Rodada 1 pode tentar detalhar setup sem decidir demais sobre provedor financeiro, agenda externa e multi-unidade. Para evitar travar:

- assumir uma unidade por studio no MVP, mas manter objeto Unidade preparado;
- permitir importacao simples antes de integracao completa;
- tratar financeiro integrado como futuro quando nao houver provedor definido;
- bloquear agentes ate preflight de dados.

## Criterio para seguir

Rodada 1 pode comecar usando estes contratos. Ela deve atualizar decisoes abertas se encontrar contradicao.
