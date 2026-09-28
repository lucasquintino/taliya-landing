# Taliya CRM Operational Core - Implementation Slices

> Objective: split the CRM + app + agent runtime into delivery slices that preserve the product thesis: Taliya is a complete vertical CRM for Pilates studios; AI agents are optional integrated operators.

## Slice 0 - Product Contract And Naming Alignment

### Goal
Remove ambiguity between older landing language and the current product decision.

### Scope
- Canonical product statement: "Taliya is a vertical operational CRM for Pilates studios with integrated AI agents."
- Base plan supports 0 active AI agents.
- Public pages may sell the agent value, but the app product must not be modeled as "only an agent panel".
- Existing internal sales inbox remains Taliya's own commercial inbox, not the tenant CRM inbox.

### Documents/Areas
- `specs/001-niche-landing-system/spec.md`
- `specs/002-floating-ai-sales-agent/*`
- New CRM spec package under `specs/006-crm-operational-core/`

### Acceptance Criteria
- Product docs distinguish "public lead funnel", "internal Taliya sales operation", and "tenant CRM product".
- Any future implementation plan treats agents as a module, not the root app.
- Base-plan user journey works without provisioning an AI agent.

## Slice 1 - Tenant Foundation, Auth, Roles, And Workspace Claim

### Goal
Let a studio owner claim and configure a workspace before using CRM modules.

### Route Scope
- `/login`
- `/onboarding/claim/[activationId]`
- `/onboarding/studio`
- `/onboarding/importacao`
- `/onboarding/agentes`
- `/onboarding/revisao`
- `/app/configuracoes/equipe`
- `/app/configuracoes/permissoes`

### Data Scope
- Tenant
- UserAccount
- Membership
- StudioProfile
- AuditEvent

### Acceptance Criteria
- A manager can create/claim a studio workspace.
- Roles exist for owner, manager, receptionist, teacher, financial user, and external accountant.
- All tenant-scoped records include tenant isolation.
- Audit events capture important configuration changes.

## Slice 2 - CRM Base: Contacts, Students, Interested People, Tasks, And Inbox

### Goal
Ship a usable CRM with no AI agents.

### Route Scope
- `/app`
- `/app/inbox`
- `/app/conversas/[id]`
- `/app/contatos`
- `/app/contatos/[id]`
- `/app/alunos`
- `/app/alunos/[id]`
- `/app/interessados`
- `/app/interessados/[id]`
- `/app/tarefas`
- `/app/tarefas/[taskId]`

### Data Scope
- Contact
- ResponsibleParty
- Student
- InterestedPerson
- Conversation
- Message
- Task
- StudentHistoryEvent

### Acceptance Criteria
- Staff can register contacts, students, guardians/responsibles, and interested people.
- Staff can manually send/respond through CRM conversation records where integrations are active.
- Staff can create and complete tasks.
- Every important manual action can be recovered in a student's timeline.
- Product is useful on Base plan with 0 active agents.

## Slice 3 - Agenda, Classes, Attendance, Repositions, And Waitlist

### Goal
Cover the operational routine of a Pilates studio.

### Route Scope
- `/app/agenda`
- `/app/grade`
- `/app/turmas`
- `/app/turmas/[id]`
- `/app/aulas/[id]`
- `/app/aulas/[id]/chamada`
- `/app/reposicoes`
- `/app/creditos-reposicao`
- `/app/lista-espera`

### Data Scope
- StudioPlan
- ClassGroup
- ClassSession
- AttendanceRecord
- MakeUpCredit
- WaitlistEntry
- Teacher membership links

### Acceptance Criteria
- Manager can configure capacity, days, teachers, and recurring classes.
- Reception/teacher can mark attendance and absence.
- System creates and consumes make-up credits.
- Waitlist can be used to fill available spots.
- Manual operation works before any autonomous automation is enabled.

## Slice 4 - Finance Core And Student Plans

### Goal
Make CRM operationally complete for billing and financial follow-up.

### Route Scope
- `/app/financeiro`
- `/app/financeiro/kanban`
- `/app/financeiro/movimentacoes`
- `/app/financeiro/movimentacoes/[id]`
- `/app/financeiro/documentos`

### Data Scope
- StudentPlan
- Payment
- Charge
- Contract
- DocumentRecord
- OperationCase
- Approval

### Acceptance Criteria
- Staff can see paid, open, overdue, disputed, and cancelled charges.
- Financial exceptions require explicit handling.
- Contract and plan changes are auditable.
- Overdue follow-up can run manually first, then copiloto/autonomous later.

## Slice 5 - Operation Cases, Approvals, Sends, And Flow Runs

### Goal
Create the runtime layer needed by both manual workflows and AI-assisted workflows.

### Route Scope
- `/app/operacao`
- `/app/operacao/[caseId]`
- `/app/aprovacoes`
- `/app/aprovacoes/[approvalId]`
- `/app/fluxos/execucoes/[runId]`
- `/app/envios`
- `/app/envios/[sendId]`
- `/app/auditoria`
- `/app/auditoria/[eventId]`

### Data Scope
- OperationCase
- Task
- Approval
- SendAttempt
- FlowRun
- AuditEvent
- IntegrationLog

### Acceptance Criteria
- Any automated or manual operational item can become a case.
- Cases can require approval before sending, changing schedule, charging, or closing a student action.
- Failed messages/payments/integrations are visible and recoverable.
- Flow execution history is inspectable without reading logs.

## Slice 6 - Usage, Quotas, Economy Rules, And Billing Entitlements

### Goal
Prevent runaway cost, explain limits clearly, and support plan/package upgrades.

### Route Scope
- `/app/uso`
- `/app/uso/cotas`
- `/app/uso/custos`
- `/app/uso/extrato`
- `/app/uso/alertas`
- `/app/uso/pacotes`
- `/app/uso/regras-economia`
- `/app/uso/limites-fluxo`
- `/app/uso/limites-fluxo/[flowId]`
- `/app/billing`
- `/app/billing/add-ons`
- `/app/billing/invoices`

### Data Scope
- QuotaLedgerEntry
- Plan entitlements
- Add-on packages
- FlowConfiguration
- AgentConfiguration
- AuditEvent

### Acceptance Criteria
- Base plan has 0 agent quota and still allows CRM usage.
- Agent plans expose message/credit/automation quotas.
- Users see usage by channel, flow, agent, and cost origin.
- At 70%, 90%, and 100%, the system changes behavior according to product rules.
- Economy mode can pause low-priority autonomous flows while preserving critical CRM operation.

## Slice 7 - Retention, History, Quality, And Management Cockpit

### Goal
Give the manager visibility over studio health beyond day-to-day task execution.

### Route Scope
- `/app/retencao`
- `/app/retencao/riscos`
- `/app/cancelamentos`
- `/app/retencao/reativacoes`
- `/app/reclamacoes`
- `/app/alunos/[id]/linha-do-tempo`
- `/app/historico/documentos`
- `/app/professores`
- `/app/professores/[teacherId]`
- `/app/dinheiro-na-mesa`
- `Gargalos` as filtered reports/origin links, no dedicated MVP route
- `Capacidade` as occupancy indicators and filtered agenda origins, no dedicated MVP route
- `/app/relatorios`

### Data Scope
- StudentHistoryEvent
- DocumentRecord
- AttendanceRecord
- Payment
- OperationCase
- Teacher-scoped observations

### Acceptance Criteria
- Manager can identify money at risk, retention risk, schedule capacity, and unresolved operational bottlenecks.
- Teacher observations can be captured without exposing private financial data.
- Reports are sourced from CRM records, not landing/demo data.

## Slice 8 - Agents, Flow Configuration, Simulation, And Autonomy Controls

### Goal
Integrate AI agents as configurable operators after CRM foundations exist.

### Route Scope
- `/app/agentes`
- `/app/agentes/[agentId]`
- `/app/agentes/[agentId]/fluxos`
- `/app/fluxos`
- `/app/fluxos/[flowId]`
- `/app/fluxos/[flowId]/simular`
- `/app/fluxos/execucoes/[runId]`

### Data Scope
- AgentConfiguration
- FlowConfiguration
- FlowRun
- Approval
- QuotaLedgerEntry
- IntegrationLog

### Acceptance Criteria
- Each strong candidate agent flow can be configured as manual, copiloto, or autonomous where allowed. The current working catalog is 96 strong candidate flows, with E14/G13 still optional as standalone flows.
- Simulation shows what would happen before enabling autonomous mode.
- Guardrails, approval thresholds, quiet hours, and quota limits are configurable.
- AI agents cannot bypass tenant permissions, quotas, approvals, or business rules.

## Slice 9 - Mobile App For Field Operation

### Goal
Support the daily operating surface for owners, reception, and teachers on mobile.

### App Surface Scope
- App home/today
- Inbox/conversation detail
- Tasks
- Student profile
- Attendance
- Make-up credits
- Interested person detail
- Approvals
- Usage alerts
- Settings-light

### Acceptance Criteria
- Teacher can handle attendance and observations quickly.
- Reception can respond to conversations and tasks from mobile.
- Manager can approve sensitive actions and monitor usage.
- Mobile app does not need every admin setup screen from web v1.

## Suggested Delivery Order

1. Slice 0: Product contract.
2. Slice 1: Tenant/auth/roles.
3. Slice 2: Base CRM.
4. Slice 3: Agenda.
5. Slice 4: Finance.
6. Slice 5: Runtime layer.
7. Slice 6: Quotas and billing entitlements.
8. Slice 8: Agents and flow simulation.
9. Slice 7: Management/retention.
10. Slice 9: Mobile app.

## Non-Negotiable Gates

- No autonomous workflow before tenant isolation, audit log, quota enforcement, and approval model exist.
- No AI send before conversation ownership, opt-out/permission, quiet hours, and send failure handling exist.
- No billing or quota promise before entitlements are represented in data.
- No route should depend on the current `/internal/sales-inbox` as tenant CRM infrastructure.
- No `/pilates` visual/layout change is required for these implementation slices.
