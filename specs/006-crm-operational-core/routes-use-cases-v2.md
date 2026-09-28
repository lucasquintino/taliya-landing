# Draft V2 - Routes, Screens And Use Cases

> Status: exploratory draft. This version uses the current product direction: Taliya is a CRM operational layer with integrated AI agents. The agent catalog is currently 96 candidate flows, with E14/G13 still optional.

## Product Shape

The app should not be organized only by agents.

It should be organized by how a studio manager works:

1. today and priorities;
2. conversations and contacts;
3. students and history;
4. agenda and attendance;
5. sales and interested people;
6. finance and plans;
7. retention and complaints;
8. operations, tasks and approvals;
9. agents, flows, simulation and execution logs;
10. usage, quotas, integrations and audit;
11. settings and policies.

Agents appear inside these surfaces as:

- suggestions;
- autonomous runs;
- copilots awaiting approval;
- flow configuration;
- execution history;
- quota/cost explanation;
- incident/correction records.

## Route Principles

### 1. CRM Routes Are Not Agent Routes

Examples:

- `/app/alunos`
- `/app/agenda`
- `/app/financeiro`
- `/app/interessados`
- `/app/inbox`

These must exist even on Base plan with 0 agents.

### 2. Agent Routes Configure And Explain Automation

Examples:

- `/app/agentes`
- `/app/fluxos`
- `/app/fluxos/[flowId]`
- `/app/fluxos/[flowId]/simular`
- `/app/fluxos/execucoes/[runId]`

These should not be the only way to use the product.

### 3. Operational Routes Are The Bridge

Examples:

- `/app/operacao`
- `/app/tarefas`
- `/app/aprovacoes`
- `/app/envios`
- `/app/auditoria`
- `/app/dados/qualidade`

This is where manual, copiloto and autonomous modes meet.

## Recommended Web Navigation V1

### Primary Sidebar

| Nav | Primary Route | Why It Exists |
| --- | --- | --- |
| Hoje | `/app/hoje` | Manager starts from priorities, not from a module list. |
| Inbox | `/app/inbox` | Central place for WhatsApp/conversation work. |
| Alunos | `/app/alunos` | Core CRM record. |
| Agenda | `/app/agenda` | Pilates operational center. |
| Vendas | `/app/vendas` | Pipeline, interested people, trials and conversion. |
| Financeiro | `/app/financeiro` | Payments, plans, charges and exceptions. |
| Retencao | `/app/retencao` | Risk, complaints, cancellations and reactivation. |
| Operacao | `/app/operacao` | Cases, tasks, approvals, incidents. |
| Agentes | `/app/agentes` | Configure, simulate and observe agents. |
| Relatorios | `/app/relatorios` | Business visibility. |
| Configuracoes | `/app/configuracoes` | Post-go-live CRM settings hub: Studio, Equipe, Permissoes, Canais, Planos e modelos, Pagamentos e financeiro, Agenda and Notificacoes. |

### Secondary Always-Available Surfaces

| Surface | Routes |
| --- | --- |
| Tasks | `/app/tarefas`, `/app/tarefas/[taskId]` |
| Approvals | `/app/aprovacoes`, `/app/aprovacoes/[approvalId]` |
| Notifications | `/app/notificacoes` |
| Usage | `/app/uso`, `/app/uso/extrato` |
| Audit | `/app/auditoria`, `/app/auditoria/[eventId]` |
| Data Quality | `/app/dados/qualidade`, `/app/dados/duplicidades` |

## New Route Additions From The 5 Accepted Agent Gaps

### C15 - Entrada Multicanal De Lead

Routes:

- `/app/vendas/captura`
- `/app/vendas/origens`
- `/app/interessados/novo`
- `/app/interessados/[id]`

Use case:

An interested person arrives from Instagram, site form, referral, walk-in or manual import. The system creates/deduplicates the lead, registers source, assigns owner, suggests next action and routes to trial, pricing, follow-up or waitlist.

### D15 - Encerramento Ou Alteracao Efetiva De Plano

Routes:

- `/app/financeiro/movimentacoes`
- `/app/financeiro/movimentacoes/[id]`
- `/app/alunos/[id]`
- `/app/cancelamentos`

Use case:

A student changes frequency, pauses, downgrades, upgrades or cancels. The system validates contract/payment/credits/agenda impact, proposes effective date, creates approval when needed and records final state.

### E13 - Reclamacao E Recuperacao De Confianca

Routes:

- `/app/reclamacoes`
- `/app/reclamacoes/[caseId]`
- `/app/retencao`
- `/app/inbox`

Use case:

A student or responsible complains. The system classifies severity, pauses inappropriate automation, assigns owner, tracks SLA, records resolution and schedules recovery follow-up.

### F14 - Incidente De Automacao E Correcao Operacional

Routes:

- `/app/operacao/incidentes`
- `/app/operacao/incidentes/[incidentId]`
- `/app/fluxos/execucoes/[runId]`
- `/app/auditoria/[eventId]`
- `/app/dados/qualidade`

Use case:

An agent technically completed an action but the business outcome was wrong: wrong message, wrong student, wrong charge, wrong booking, stale data or bad rule. The system opens incident, shows impact, pauses affected flow, creates correction tasks and records prevention.

### F15 - Mudanca De Politica Ou Regra Operacional

Routes:

- `/app/politicas`
- `/app/politicas/[policyId]`
- `/app/politicas/[policyId]/simular`
- `/app/fluxos/[flowId]`

Use case:

The studio changes make-up validity, absence deadline, price policy, cancellation policy, send window, campaign rule or autonomy boundary. The system versions the policy, simulates impact, asks approval and schedules rollout.

## Optional Route Pressure From E14/G13

These do not require new top-level routes yet.

### E14 - Primeira Semana Do Novo Aluno

Can live inside:

- `/app/alunos/[id]`
- `/app/retencao`
- `/app/tarefas`
- `/app/agenda`

Only create a dedicated student onboarding surface if this becomes a large product surface. Until then, keep it inside student profile, retention checklist and tasks instead of adding a new route.

### G13 - Gate De Anamnese, Consentimento E Contato De Emergencia

Can live inside:

- `/app/historico/documentos`
- `/app/alunos/[id]`
- `/app/dados/qualidade`
- `/app/privacidade/solicitacoes` when it becomes a formal privacy request

Only create a dedicated route if intake gating becomes central to the product.

## Macro Use Case Catalog V2

This section lists macro validation journeys, not the complete manager use-case catalog. The broader manager catalog is in [manager-use-case-catalog.md](./manager-use-case-catalog.md).

### UC-001 - Owner Claims Workspace

Routes:

- `/onboarding/claim/[activationId]`
- `/onboarding/studio`
- `/onboarding/revisao`
- `/app/hoje`

Outcome:

Owner creates the workspace and reaches the first usable CRM dashboard.

### UC-002 - Studio Runs Base Plan Without Agents

Routes:

- `/app/hoje`
- `/app/alunos`
- `/app/agenda`
- `/app/inbox`
- `/app/tarefas`
- `/app/financeiro`

Outcome:

The studio can manage CRM records and manual tasks with 0 active agents.

### UC-003 - Configure Agent Plan

Routes:

- `/app/agentes`
- `/app/agentes/[agentId]`
- `/app/fluxos`
- `/app/fluxos/[flowId]`
- `/app/fluxos/[flowId]/simular`

Outcome:

Owner configures included agents, modes, limits, approval rules, templates and simulation before activation.

### UC-004 - Daily Manager Review

Routes:

- `/app/hoje`
- `/app/operacao`
- `/app/tarefas`
- `/app/aprovacoes`
- `/app/dinheiro-na-mesa`

Outcome:

Manager sees what needs attention today across agenda, sales, finance, retention, data quality and agent handoffs.

### UC-005 - Manual Conversation Handling

Routes:

- `/app/inbox`
- `/app/conversas/[id]`
- `/app/contatos/[id]`
- `/app/tarefas/[taskId]`

Outcome:

Staff handles a conversation manually while the CRM still records context, task, outcome and next action.

### UC-006 - Copilot Approval

Routes:

- `/app/aprovacoes`
- `/app/aprovacoes/[approvalId]`
- `/app/fluxos/execucoes/[runId]`
- `/app/envios/[sendId]`

Outcome:

Agent prepares message/action, human reviews, edits, approves or rejects, and the system records decision.

### UC-007 - Autonomous Flow Runs Safely

Routes:

- `/app/fluxos/execucoes/[runId]`
- `/app/auditoria/[eventId]`
- `/app/uso/extrato`

Outcome:

Agent acts inside configured rules, consumes quota, logs result and exposes explanation after the fact.

### UC-008 - New WhatsApp Lead

Routes:

- `/app/inbox`
- `/app/interessados/[id]`
- `/app/vendas`
- `/app/experimental`

Outcome:

Lead is identified, qualified, routed and followed up.

### UC-009 - Multichannel Lead

Routes:

- `/app/vendas/captura`
- `/app/vendas/origens`
- `/app/interessados/novo`
- `/app/interessados/[id]`

Outcome:

Lead from Instagram/site/referral/walk-in enters the same CRM pipeline and agent logic.

### UC-010 - Trial Class To Student

Routes:

- `/app/experimental`
- `/app/matriculas`
- `/app/alunos/[id]`
- `/app/configuracoes/financeiro/modelos`
- `/app/financeiro/documentos`

Outcome:

Interested person becomes student, with plan, schedule, contract, first class and follow-up connected.

### UC-011 - Attendance And Make-Up

Routes:

- `/app/agenda`
- `/app/aulas/[id]/chamada`
- `/app/reposicoes`
- `/app/creditos-reposicao`
- `/app/lista-espera`

Outcome:

Presence, absence, credits, make-ups and open slots are handled without losing history.

### UC-012 - Overdue Payment

Routes:

- `/app/financeiro`
- `/app/financeiro/movimentacoes`
- `/app/financeiro/movimentacoes/[id]`
- `/app/aprovacoes/[approvalId]`

Outcome:

Payment reminder or collection is sent manually, in copilot or autonomously depending on rules.

### UC-013 - Effective Plan Change

Routes:

- `/app/financeiro/movimentacoes`
- `/app/financeiro/movimentacoes/[id]`
- `/app/alunos/[id]`
- `/app/agenda`

Outcome:

Plan pause, cancellation, upgrade, downgrade or frequency change is executed with financial and agenda impact controlled.

### UC-014 - Cancellation Risk

Routes:

- `/app/retencao`
- `/app/cancelamentos`
- `/app/inbox`
- `/app/operacao/[caseId]`

Outcome:

Risk is detected, human takes over when needed and cancellation outcome is recorded.

### UC-015 - Complaint Recovery

Routes:

- `/app/reclamacoes`
- `/app/reclamacoes/[caseId]`
- `/app/retencao`

Outcome:

Complaint has owner, SLA, resolution and post-resolution recovery follow-up.

### UC-016 - Teacher Note And Student History

Routes:

- `/app/professores`
- `/app/aulas/[id]`
- `/app/alunos/[id]/linha-do-tempo`
- `/app/historico`

Outcome:

Teacher context is saved and visible according to permissions.

### UC-017 - Quota Reaches Limit

Routes:

- `/app/uso`
- `/app/uso/extrato`

Outcome:

System explains usage, activates economy behavior and blocks or downgrades low-priority automation. Cotas, alertas and economy behavior are shown inside `/app/uso`; the detailed ledger stays in `/app/uso/extrato`.

### UC-018 - Automation Incident

Routes:

- `/app/operacao/incidentes`
- `/app/operacao/incidentes/[incidentId]`
- `/app/fluxos/execucoes/[runId]`
- `/app/dados/qualidade`

Outcome:

Wrong automated action is reviewed, corrected and prevented from recurring.

### UC-019 - Policy Change

Routes:

- `/app/politicas`
- `/app/politicas/[policyId]`
- `/app/politicas/[policyId]/simular`

Outcome:

Operational rule changes are versioned, simulated, approved and rolled out safely.

### UC-020 - Data Quality Blocks Automation

Routes:

- `/app/dados/qualidade`
- `/app/dados/duplicidades`
- `/app/importacao/[jobId]`
- `/app/tarefas`

Outcome:

Missing/conflicting data becomes visible work instead of invisible agent failure.

## MVP Route Cut

### Web P0

Required to have a credible CRM with agents:

- `/app/hoje`
- `/app/inbox`
- `/app/alunos`
- `/app/agenda`
- `/app/vendas`
- `/app/interessados`
- `/app/financeiro`
- `/app/retencao`
- `/app/operacao`
- `/app/tarefas`
- `/app/aprovacoes`
- `/app/agentes`
- `/app/fluxos`
- `/app/uso`
- `/app/configuracoes/studio`
- `/app/configuracoes/equipe`
- `/app/configuracoes/permissoes`
- `/app/configuracoes/canais`
- `/app/configuracoes/financeiro/modelos`
- `/app/configuracoes/financeiro/pagamentos`
- `/app/configuracoes/agenda`
- `/app/configuracoes/notificacoes`

### Web P1

Needed for the 96-flow system to feel safe:

- `/app/reclamacoes`
- `/app/financeiro/movimentacoes`
- `/app/operacao/incidentes`
- `/app/politicas`
- `/app/dados/qualidade`
- `/app/dados/duplicidades`
- `/app/fluxos/[flowId]/simular`
- `/app/fluxos/execucoes/[runId]`
- `/app/auditoria`

### Mobile V1

Mobile should focus on action, not heavy setup:

- Today;
- Inbox;
- Agenda/chamada;
- Students;
- Tasks;
- Approvals;
- Complaints/sensitive cases;
- Finance essentials;
- Student notes/history;
- Notifications.

## Product Verdict

The current route map is directionally right, but it needed the five accepted agent gaps represented as product surfaces.

With the additions above, the screen/route plan now supports:

- Base CRM with 0 agents;
- manual operation;
- copilot approvals;
- autonomous runs;
- agent configuration and simulation;
- quotas and economy;
- audit and incident correction;
- policy/rule governance;
- 96 candidate AI-agent flows.

This is enough for a serious CRM-with-agents draft. The next missing artifact is a full flow-by-flow use case catalog if we want one use case per canonical agent flow.
