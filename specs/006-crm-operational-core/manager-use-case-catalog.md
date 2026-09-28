# Draft Catalog - Manager Use Cases

> Status: exploratory draft. This is not final product scope. It is a broad catalog of use cases a Pilates studio manager can follow in Taliya as a CRM with integrated AI agents.

## Short Answer

No, the product does not have only 20 manager use cases.

The previous 20 were macro validation journeys. A more realistic manager-facing catalog has:

```text
132 manager-followable use cases
```

These are not all separate screens and not all separate AI-agent flows. They are practical journeys a manager or team member can follow inside the CRM.

## Counting Rule

A manager use case counts when it has:

- a clear business trigger;
- a user who can start or review it;
- a primary route/surface;
- a decision, action, delegation or recorded outcome;
- possible manual/copilot/autonomous support;
- a CRM record, task, case, approval, audit event or report as output.

It does not need to be a separate AI-agent flow.

## Summary By Area

| Area | Count |
| --- | ---: |
| Setup, access and governance | 13 |
| Daily command center | 10 |
| Inbox, contacts and privacy | 12 |
| Sales and interested people | 16 |
| Agenda and attendance | 17 |
| Finance and student plans | 16 |
| Retention and complaints | 13 |
| Student history and teacher work | 11 |
| Agents, runtime and quotas | 14 |
| Reports, integrations and administration | 10 |
| **Total** | **132** |

## A. Setup, Access And Governance

| ID | Use Case | Primary Routes | Agent/Layer |
| --- | --- | --- | --- |
| MUC-001 | Claim paid workspace after billing confirmation | `/onboarding/claim/[activationId]` | CRM core |
| MUC-002 | Complete studio profile | `/onboarding/studio`, `/app/configuracoes/studio` | CRM core |
| MUC-003 | Finish initial setup checklist | `/onboarding/revisao`, `/app/hoje` | Gestao/F6 |
| MUC-004 | Import initial students, leads, agenda and payments | `/onboarding/importacao`, `/app/importacao` | Gestao/F12 |
| MUC-005 | Resolve import duplicates and conflicts | `/app/dados/duplicidades`, `/app/importacao/[jobId]` | Atendimento/A7, Gestao/F12 |
| MUC-006 | Invite team members | `/app/configuracoes/equipe` | CRM core |
| MUC-007 | Configure roles and permissions | `/app/configuracoes/permissoes` | Gestao/F9, Historico/G11 |
| MUC-008 | Configure WhatsApp and channels | `/app/configuracoes/canais` | Atendimento + integrations |
| MUC-009 | Review approved answers and message rules in context | `/app/inbox`, `/app/agentes`, `/app/fluxos/[flowId]` | Atendimento/A2, Agentes/Fluxos |
| MUC-010 | Configure agenda rules | `/app/configuracoes/agenda` | Agenda |
| MUC-011 | Configure finance rules, payments and student plans | `/app/configuracoes/financeiro/pagamentos`, `/app/configuracoes/financeiro/modelos` | Financeiro |
| MUC-012 | Handle privacy, consent and opt-out behavior | `/app/contatos/[id]`, `/app/privacidade/solicitacoes` | Atendimento/A6/A8 |
| MUC-013 | Configure operational policies and effective dates | `/app/politicas` | Gestao/F15 |

## B. Daily Command Center

| ID | Use Case | Primary Routes | Agent/Layer |
| --- | --- | --- | --- |
| MUC-014 | Open daily priorities | `/app/hoje` | Gestao/F1 |
| MUC-015 | Review money on the table | `/app/dinheiro-na-mesa` | Gestao/F2 |
| MUC-016 | Review human queue | `/app/operacao`, `/app/aprovacoes` | Gestao/F3 |
| MUC-017 | Review tasks by owner and SLA | `/app/tarefas` | CRM operation |
| MUC-018 | Delegate a task or case | `/app/tarefas/[taskId]`, `/app/operacao/[caseId]` | CRM operation |
| MUC-019 | Close resolved operational cases | `/app/operacao/[caseId]` | CRM operation |
| MUC-020 | Review notifications and alerts | `/app/notificacoes` | CRM operation |
| MUC-021 | Review bottlenecks | `/app/relatorios`, `/app/operacao`, `/app/tarefas` | Gestao/F4 |
| MUC-022 | Review weekly summary | `/app/relatorios/semana` | Gestao/F5 |
| MUC-023 | Check data/setup blockers for today | `/app/dados/qualidade` | Gestao/F6 |

## C. Inbox, Contacts And Privacy

| ID | Use Case | Primary Routes | Agent/Layer |
| --- | --- | --- | --- |
| MUC-024 | Handle a new WhatsApp conversation | `/app/inbox`, `/app/conversas/[id]` | Atendimento/A1 |
| MUC-025 | Handle an existing student request | `/app/conversas/[id]`, `/app/alunos/[id]` | Atendimento/A3 |
| MUC-026 | Answer allowed FAQ or create missing-answer task | `/app/inbox`, `/app/tarefas/[taskId]` | Atendimento/A2 |
| MUC-027 | Human takeover and response | `/app/conversas/[id]`, `/app/operacao/[caseId]` | Atendimento/A5 |
| MUC-028 | Register opt-out or communication preference | `/app/contatos/[id]`, `/app/privacidade/solicitacoes` when formal | Atendimento/A6 |
| MUC-029 | Handle shared-phone or identity-ambiguous message | `/app/contatos`, `/app/inbox` | Atendimento/A9 |
| MUC-030 | Update contact data safely | `/app/contatos/[id]` | Atendimento/A8 |
| MUC-031 | Validate contact identity before sensitive action | `/app/contatos/[id]`, `/app/alunos/[id]` | Atendimento/A9, Historico/G11 |
| MUC-032 | Classify media, proof, document or audio | `/app/conversas/[id]`, `/app/envios` | Atendimento/A7 |
| MUC-033 | Resolve contact/student duplicate | `/app/dados/duplicidades` | Atendimento/A7 |
| MUC-034 | Handle privacy/data request | `/app/operacao/[caseId]`, `/app/auditoria` | Atendimento/A8 |
| MUC-035 | Reopen stale conversation or SLA breach | `/app/inbox`, `/app/tarefas` | Atendimento/A10 |

## D. Sales And Interested People

| ID | Use Case | Primary Routes | Agent/Layer |
| --- | --- | --- | --- |
| MUC-036 | Capture multichannel lead | `/app/vendas/captura` | Vendas/C15 |
| MUC-037 | Register walk-in or manual lead | `/app/interessados/novo` | Vendas/C15 |
| MUC-038 | Review lead sources and attribution | `/app/vendas/origens` | Vendas/C8/C15 |
| MUC-039 | Qualify interested person | `/app/interessados/[id]` | Vendas/C8 |
| MUC-040 | Answer price and plan question | `/app/inbox`, `/app/vendas`, `/app/configuracoes/financeiro/modelos` | Vendas/C1 |
| MUC-041 | Schedule trial class | `/app/experimental`, `/app/agenda` | Vendas/C2, Agenda/B7 |
| MUC-042 | Send trial reminder | `/app/experimental`, `/app/envios` | Vendas/C3 |
| MUC-043 | Handle trial no-show or reschedule | `/app/experimental`, `/app/interessados/[id]` | Agenda/B12 |
| MUC-044 | Follow up after trial class | `/app/interessados/[id]`, `/app/vendas` | Vendas/C4 |
| MUC-045 | Run commercial follow-up cadence | `/app/vendas`, `/app/tarefas` | Vendas/C5 |
| MUC-046 | Handle objection without unsafe discounting | `/app/conversas/[id]`, `/app/aprovacoes` | Vendas/C7 |
| MUC-047 | Create pre-enrollment | `/app/matriculas` | Vendas/C6 |
| MUC-048 | Track student checkout abandonment | `/app/checkout-alunos` | Vendas/C11 |
| MUC-049 | Register referral and benefit review | `/app/indicacoes` | Vendas/C10 |
| MUC-050 | Manage demand with no available slot | `/app/vendas`, `/app/lista-espera`, `/app/agenda`, `/app/reposicoes` | Vendas/C12 |
| MUC-051 | Convert interested person into student | `/app/matriculas`, `/app/alunos/[id]` | Vendas/C13 |

## E. Agenda And Attendance

| ID | Use Case | Primary Routes | Agent/Layer |
| --- | --- | --- | --- |
| MUC-052 | Create or adjust weekly grade | `/app/grade` | Agenda/B11 |
| MUC-053 | Create class group | `/app/turmas` | Agenda/B11 |
| MUC-054 | Review calendar/day schedule | `/app/agenda` | Agenda |
| MUC-055 | Open class session | `/app/aulas/[id]` | Agenda |
| MUC-056 | Take attendance | `/app/aulas/[id]/chamada` | Agenda/B3/B14 |
| MUC-057 | Confirm presence before class | `/app/agenda`, `/app/envios` | Agenda/B1 |
| MUC-058 | Register absence with notice | `/app/reposicoes`, `/app/aulas/[id]` | Agenda/B2 |
| MUC-059 | Handle no-show | `/app/aulas/[id]`, `/app/retencao` | Agenda/B3 |
| MUC-060 | Handle make-up request | `/app/reposicoes` | Agenda/B5 |
| MUC-061 | Manage make-up credit ledger | `/app/creditos-reposicao` | Agenda/B13 |
| MUC-062 | Recover open slot | `/app/lista-espera`, `/app/reposicoes` | Agenda/B4 |
| MUC-063 | Manage waitlist | `/app/lista-espera` | Agenda/B6 |
| MUC-064 | Change fixed student schedule | `/app/alunos/[id]`, `/app/agenda` | Agenda/B8 |
| MUC-065 | Cancel or alter class by studio | `/app/aulas/[id]`, `/app/aprovacoes` | Agenda/B9 |
| MUC-066 | Resolve capacity or overbooking conflict | `/app/turmas/[id]`, `/app/agenda`, `/app/operacao/[caseId]` | Agenda/B10 |
| MUC-067 | Prepare first class checklist | `/app/aulas/[id]`, `/app/alunos/[id]` | Agenda/B15 |
| MUC-068 | Create and manage workshop/special class | `/app/eventos` | Agenda/B16 |

## F. Finance And Student Plans

| ID | Use Case | Primary Routes | Agent/Layer |
| --- | --- | --- | --- |
| MUC-069 | Create or update student plan | `/app/alunos/[id]`, `/app/financeiro/movimentacoes` | Financeiro |
| MUC-070 | Review finance overview | `/app/financeiro` | Financeiro |
| MUC-071 | Send due reminder | `/app/financeiro/movimentacoes` | Financeiro/D1 |
| MUC-072 | Handle overdue payment | `/app/financeiro/movimentacoes/[id]` | Financeiro/D2 |
| MUC-073 | Send Pix/payment link | `/app/financeiro/movimentacoes`, `/app/envios` | Financeiro/D3 |
| MUC-074 | Confirm payment | `/app/financeiro/movimentacoes/[id]` | Financeiro/D4 |
| MUC-075 | Reconcile unmatched payment | `/app/financeiro/movimentacoes` | Financeiro/D10 |
| MUC-076 | Handle failed payment | `/app/financeiro/movimentacoes/[id]` | Financeiro/D7 |
| MUC-077 | Send receipt or invoice document | `/app/financeiro/documentos` | Financeiro/D8 |
| MUC-078 | Manage contract/terms | `/app/contratos`, `/app/contratos/[id]` | Financeiro/D11 |
| MUC-079 | Review financial exception | `/app/financeiro/movimentacoes` | Financeiro/D6 |
| MUC-080 | Pause/freeze student plan | `/app/financeiro/movimentacoes` | Financeiro/D9/D15 |
| MUC-081 | Block or release student access | `/app/financeiro/movimentacoes` | Financeiro/D12 |
| MUC-082 | Register credit/courtesy | `/app/financeiro/movimentacoes` | Financeiro/D13 |
| MUC-083 | Execute effective plan change or ending | `/app/financeiro/movimentacoes` | Financeiro/D15 |
| MUC-084 | Review monthly financial close | `/app/relatorios/financeiro` | Financeiro/D14 |

## G. Retention And Complaints

| ID | Use Case | Primary Routes | Agent/Layer |
| --- | --- | --- | --- |
| MUC-085 | Review retention dashboard | `/app/retencao` | Retencao |
| MUC-086 | Act on frequency drop | `/app/retencao/riscos`, `/app/alunos/[id]` | Retencao/E1 |
| MUC-087 | Act on inactive student | `/app/retencao/riscos` | Retencao/E2 |
| MUC-088 | Handle student return | `/app/retencao`, `/app/agenda` | Retencao/E3 |
| MUC-089 | Handle cancellation risk | `/app/cancelamentos`, `/app/operacao/[caseId]` | Retencao/E4 |
| MUC-090 | Process post-cancellation | `/app/cancelamentos` | Retencao/E9 |
| MUC-091 | Run ex-student reactivation | `/app/retencao/reativacoes` | Retencao/E5 |
| MUC-092 | Process satisfaction feedback | `/app/reclamacoes` when sensitive; `/app/retencao` when preventive | Retencao/E6 |
| MUC-093 | Open complaint case | `/app/reclamacoes` | Retencao/E13 |
| MUC-094 | Resolve complaint and recover trust | `/app/reclamacoes/[caseId]` | Retencao/E13 |
| MUC-095 | Handle return after pause | `/app/retencao`, `/app/agenda` | Retencao/E7 |
| MUC-096 | Review risk segmentation | `/app/retencao/riscos` | Retencao/E8/E12 |
| MUC-097 | Handle sensitive health/personal event | `/app/operacao/[caseId]`, `/app/historico` | Retencao/E11, Historico/G3 |

## H. Student History And Teacher Work

| ID | Use Case | Primary Routes | Agent/Layer |
| --- | --- | --- | --- |
| MUC-098 | Teacher opens class context | `/app/professores`, `/app/aulas/[id]` | Historico/G1 |
| MUC-099 | Add post-class observation | `/app/aulas/[id]`, `/app/historico` | Historico/G2 |
| MUC-100 | Register restriction/care | `/app/historico`, `/app/alunos/[id]` | Historico/G3 |
| MUC-101 | Review objective/evolution | `/app/alunos/[id]/linha-do-tempo` | Historico/G4 |
| MUC-102 | Store document/anamnesis | `/app/historico/documentos` | Historico/G6 |
| MUC-103 | Correct history event | `/app/historico`, `/app/auditoria` | Historico/G7 |
| MUC-104 | Handoff between teachers | `/app/professores`, `/app/tarefas` | Historico/G8 |
| MUC-105 | Remind teacher to add note | `/app/tarefas`, `/app/professores` | Historico/G9 |
| MUC-106 | Share safe context with student | `/app/aprovacoes`, `/app/conversas/[id]` | Historico/G10 |
| MUC-107 | Review history visibility permissions | `/app/historico/permissoes` | Historico/G11 |
| MUC-108 | Review unified student timeline | `/app/alunos/[id]/linha-do-tempo` | Historico/G12 |

## I. Agents, Runtime And Quotas

| ID | Use Case | Primary Routes | Agent/Layer |
| --- | --- | --- | --- |
| MUC-109 | Configure included agents by plan | `/app/agentes` | Agent runtime |
| MUC-110 | Configure an agent | `/app/agentes/[agentId]` | Agent runtime |
| MUC-111 | Configure a flow | `/app/fluxos/[flowId]` | Agent runtime |
| MUC-112 | Simulate flow before activation | `/app/fluxos/[flowId]/simular` | Gestao/F13 |
| MUC-113 | Activate or pause flow | `/app/fluxos/[flowId]` | Agent runtime |
| MUC-114 | Review flow execution | `/app/fluxos/execucoes/[runId]` | Agent observability |
| MUC-115 | Approve or reject copilot action | `/app/aprovacoes/[approvalId]` | Operation layer |
| MUC-116 | Review agent performance | `/app/relatorios/agentes` | Gestao/F8 |
| MUC-117 | Investigate automation incident | `/app/operacao/incidentes/[incidentId]` | Gestao/F14 |
| MUC-118 | Change operational rule/policy | `/app/politicas/[policyId]` | Gestao/F15 |
| MUC-119 | Resolve flow blocked by missing data | `/app/dados/qualidade` | Gestao/F6 |
| MUC-120 | Review quota and usage | `/app/uso`, `/app/uso/cotas` | Gestao/F7 |
| MUC-121 | Configure economy rules | `/app/uso/regras-economia` | Gestao/F7 |
| MUC-122 | Buy or request extra quota pack | `/app/uso/pacotes` | Billing/usage |

## J. Reports, Integrations And Administration

| ID | Use Case | Primary Routes | Agent/Layer |
| --- | --- | --- | --- |
| MUC-123 | Manage Taliya subscription | `/app/billing` | Billing |
| MUC-124 | View Taliya invoices | `/app/billing/invoices` | Billing |
| MUC-125 | Review integrations | `configuracao especifica da integracao` | System |
| MUC-126 | Investigate integration logs | `configuracao especifica da integracao` | Gestao/F11 |
| MUC-127 | Review audit event | `/app/auditoria/[eventId]` | Security/governance |
| MUC-128 | Export or review reports hub | `/app/relatorios` | Reports |
| MUC-129 | Review financial report | `/app/relatorios/financeiro` | Financeiro |
| MUC-130 | Review sales report | `/app/relatorios/vendas` | Vendas |
| MUC-131 | Review capacity/occupancy report | `/app/relatorios/ocupacao` | Agenda/Gestao |
| MUC-132 | Review source ROI and commercial quality | `/app/vendas/origens`, `/app/relatorios/vendas` | Vendas/C8/C15 |

## What This Means For Product Scope

The manager journey catalog is larger than the agent-flow catalog:

- **96 candidate AI-agent flows** describe what agents can do.
- **132 manager use cases** describe how a studio manager can operate the CRM around those agents.

This is expected.

A single agent flow can support many manager use cases. A single manager use case can involve multiple agent flows.

## Recommended Next Step

Convert this catalog into three delivery cuts:

1. **P0 Manager MVP**: the minimum use cases required for Base CRM + one active agent.
2. **P1 Full Agent System**: use cases required for the 96-flow system to be safe and useful.
3. **P2 Expansion**: reporting, optimization, advanced governance and optional flows.
