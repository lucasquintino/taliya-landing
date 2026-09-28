# Contratos tecnicos de produto - PT-BR

> Status: contrato v0.1 para implementacao futura. Fecha dados/API, RBAC, billing, cotas e auditoria no nivel necessario para nao inventar backend depois.

## Contrato de dados por tela

Toda tela deve consumir um view model do servidor, nao payload cru.

```text
ScreenViewModel
- tenant
- user
- role
- surface
- route
- primaryObject
- blocks[]
- actions[]
- states[]
- permissions
- entitlement
- quota
- auditHints
- fallbackActions
```

## Campos obrigatorios de uma acao

```text
ActionContract
- id
- label
- type: manual | copilot | autonomous | sensitive | navigation | billing
- objectType
- objectId
- requiredPermission
- requiredAgent
- requiredPlan
- quotaImpact
- riskLevel
- confirmationRequired
- auditEvent
- fallbackAction
- idempotencyKeyRequired
```

## RBAC v0.1

| Papel | Pode por padrao | Bloqueado por padrao |
| --- | --- | --- |
| Dono | Tudo do tenant, billing, grants, permissoes, agentes e exportacoes. | Acesso interno Taliya sem grant. |
| Admin | Configuracoes, agentes, agenda, equipe, operacao. | Billing sensivel se nao autorizado. |
| Recepcao/operacao | Inbox, agenda, tarefas, alunos basicos, vendas operacionais. | Financeiro sensivel, LGPD, permissao, billing. |
| Professor | Aulas, chamada, contexto permitido, notas e handoff. | Financeiro, conversa completa, dados sensiveis. |
| Financeiro | Pagamentos, cobrancas, contratos, casos financeiros. | Historico sensivel de saude e config de agentes. |
| Suporte Taliya | Somente via grant escopado. | Qualquer acesso sem grant, impersonacao invisivel. |

## Acoes que sempre exigem confirmacao

- envio externo para aluno/responsavel;
- alterar permissao/papel;
- publicar politica;
- ativar autonomia;
- estorno, desconto, acordo ou excecao financeira;
- cancelamento/reclamacao;
- exportar dados;
- apagar/anonimizar dado;
- conceder acesso de suporte;
- comprar pacote ou alterar plano.

## Billing e entitlements

| Objeto | Fonte da verdade | Regra |
| --- | --- | --- |
| Plano Taliya | Billing/backend Taliya | Cliente apenas exibe. |
| Agentes inclusos | Entitlement server-side | UI nao libera por conta propria. |
| Cota | Usage ledger agregado | Sempre reconciliavel. |
| Add-on/pacote | Billing/backend Taliya | Compra altera entitlement apos evento confiavel. |
| Fatura | Billing/backend Taliya | CRM nao cria status financeiro do plano por conta propria. |

## Eventos de cota

```text
UsageEvent
- tenantId
- agentId
- flowId
- runId
- sourceSurface
- sourceObjectType
- sourceObjectId
- quantity
- unit
- estimatedCost
- status
- idempotencyKey
- createdAt
```

Regras:

- todo uso de IA gera evento idempotente;
- reprocessamento seguro reutiliza ou referencia o evento original;
- falha pode registrar custo se houve chamada real;
- cota 100% bloqueia automacao paga antes de chamar provedor quando possivel.

## Eventos de auditoria

```text
AuditEvent
- tenantId
- actorType
- actorId
- surface
- actionId
- objectType
- objectId
- before
- after
- reason
- riskLevel
- ip/device when available
- createdAt
```

Eventos obrigatorios:

- ativar/pausar agente;
- mudar modo de fluxo;
- publicar/rollback de politica;
- envio externo;
- aprovacao/rejeicao;
- alteracao financeira;
- alteracao de permissao;
- LGPD/exportacao/anonimizacao;
- grant de suporte;
- compra/upgrade/downgrade;
- reprocessamento de execucao.

## APIs conceituais

| Area | Endpoints conceituais |
| --- | --- |
| Entitlements | `GET /entitlements`, `POST /agent-slots/:id/swap`, `POST /plans/checkout` |
| Agentes | `GET /agents`, `POST /flows/:id/simulate`, `POST /flows/:id/publish`, `POST /flows/:id/pause` |
| Execucoes | `GET /runs`, `GET /runs/:id`, `POST /runs/:id/reprocess` |
| Uso/cotas | `GET /usage/summary`, `GET /usage/ledger`, `POST /usage/economy-rules` |
| Auditoria | `GET /audit-events`, `GET /audit-events/:id` |
| Aprovacoes | `GET /approvals`, `POST /approvals/:id/approve`, `POST /approvals/:id/reject` |

## Aceite tecnico

- Nenhum entitlement depende de estado do cliente.
- Nenhuma acao sensivel executa sem permissao server-side.
- Nenhuma chamada de IA cobrada ocorre sem checar cota quando possivel.
- Todo evento de uso e auditoria e idempotente ou tem chave de correlacao.
- Toda tela consegue renderizar sem agente ativo.
