# Use Cases: Taliya CRM Operational Core

## UC-001: Owner Claims Workspace After Payment

Actor: studio owner.

Preconditions:

- trusted billing confirmation exists;
- tenant activation exists;
- owner can authenticate by magic link or OTP.

Flow:

1. Owner opens activation link.
2. System authenticates owner.
3. System creates or links tenant.
4. System assigns owner membership.
5. Owner starts onboarding.

Success:

- owner reaches `/onboarding/studio`;
- active entitlement is visible;
- no access is created from checkout return or chat intent alone.

## UC-002: Base Plan Studio Runs CRM Without Agents

Actor: owner or operations user.

Preconditions:

- tenant has `base` entitlement;
- zero active agents;
- CRM records exist or can be created manually.

Flow:

1. User opens `/app/hoje`.
2. User sees agenda, tasks, payments, interested people and student risks.
3. User opens a task.
4. User updates the relevant record manually.
5. System records audit and timeline events.

Success:

- no active agent automation runs;
- tasks and records still work;
- unavailable agent actions are locked or upsell-gated.

## UC-003: Import Studio Data

Actor: owner/admin.

Flow:

1. User opens `/app/importacao`.
2. User uploads or maps students, contacts, agenda, plans and payments.
3. System creates import job.
4. User reviews duplicates and missing data.
5. System blocks dependent automations until required data is fixed.

Routes:

- `/app/importacao`
- `/app/importacao/[jobId]`
- `/app/dados/qualidade`
- `/app/dados/duplicidades`

## UC-004: Handle New WhatsApp Conversation Manually

Actors: operations user, contact.

Mode: manual.

Flow:

1. New message appears in `/app/inbox`.
2. System creates conversation and operation case.
3. System creates task because flow is manual or unavailable.
4. User opens `/app/conversas/[id]`.
5. User identifies contact as interested or student.
6. User replies and updates record.

Success:

- contact is not lost;
- all changes are visible in CRM;
- no unauthorized automation sends a message.

## UC-005: Confirm Presence Autonomously

Actors: agent runtime, student.

Mode: autonomous.

Flow:

1. B1 starts from configured confirmation window.
2. System checks class, student, opt-out, send window and quota.
3. System sends confirmation message.
4. Student confirms or reports absence.
5. Attendance record updates.
6. If absent, flow transitions to B2.

Routes:

- `/app/fluxos/execucoes/[runId]`
- `/app/envios/[sendId]`
- `/app/aulas/[id]/chamada`
- `/app/operacao/[caseId]`

## UC-006: Make-Up Request With Missing Data

Mode: autonomous or copilot.

Flow:

1. Student asks for make-up class.
2. System cannot find eligible credit.
3. System asks one safe clarification or creates task.
4. Team reviews in `/app/tarefas/[taskId]`.
5. If exception is requested, approval or human handoff is required.

Success:

- automation does not invent a credit;
- case remains visible;
- team can resolve manually.

## UC-007: Overdue Payment In Copilot Mode

Actor: finance user.

Flow:

1. D2 detects overdue payment.
2. System creates flow execution and proposed reminder.
3. Approval appears in `/app/aprovacoes`.
4. Finance user approves, edits or rejects.
5. Approved send becomes `/app/envios/[sendId]`.
6. Payment status and usage ledger update.

Success:

- no sensitive financial action happens without configured approval;
- message uses approved template and configured payment destination.

## UC-008: Financial Exception Requires Manual Human Decision

Examples:

- discount;
- refund;
- courtesy;
- pause/trancamento;
- block/unblock access.

Flow:

1. Request enters inbox or finance.
2. System identifies D6, D9, D12 or D13.
3. Automation pauses.
4. Case is assigned to finance/owner.
5. Decision is logged in audit.

Routes:

- `/app/financeiro/movimentacoes`
- `/app/tarefas/[taskId]`
- `/app/auditoria/[eventId]`

## UC-009: Interested Person Becomes Student

Flow:

1. Interested person asks values or trial class.
2. Vendas records stage and next action.
3. Trial is booked or pre-enrollment starts.
4. Payment/contract/schedule are confirmed.
5. System converts interested person to student.
6. Agenda, Financeiro and Historico receive setup tasks.

Routes:

- `/app/interessados/[id]`
- `/app/experimental`
- `/app/matriculas`
- `/app/alunos/[id]`
- `/app/aulas/[id]`
- `/app/financeiro`

## UC-010: Student At Risk Of Cancellation

Flow:

1. System detects low frequency or explicit cancellation signal.
2. Retention case opens.
3. If cancellation/health/anger appears, human handoff is required.
4. Owner sees context and next action.
5. Follow-up or final cancellation is recorded.

Routes:

- `/app/retencao`
- `/app/cancelamentos`
- `/app/alunos/[id]`
- `/app/tarefas/[taskId]`

## UC-011: Teacher Records Post-Class Observation

Actor: teacher.

Flow:

1. Teacher opens class or student.
2. Teacher records note by text or voice.
3. System stores history event with proper visibility.
4. If note indicates risk, a retention task is created.
5. If note includes sensitive restriction, visibility is restricted.

Routes:

- `/app/professores`
- `/app/aulas/[id]`
- `/app/historico`
- `/app/alunos/[id]/linha-do-tempo`

## UC-012: Owner Reviews Daily Operation

Actor: owner.

Flow:

1. Owner opens `/app/hoje`.
2. Owner sees priorities, cases, tasks, approvals, failed sends, quota alerts and bottlenecks.
3. Owner opens `/app/operacao`.
4. Owner filters by waiting team, blocked, running, overdue or high priority.
5. Owner resolves or delegates cases.

Success:

- no important case disappears inside an agent-specific page;
- owner can run the day from one surface.

## UC-013: Quota Reaches 90 Percent

Flow:

1. Usage ledger reaches configured threshold.
2. System creates alert.
3. Low-priority flows shift to task/copilot.
4. Campaigns and expensive sends require approval.
5. Owner can buy extra quota or adjust economy rules.

Routes:

- `/app/uso/alertas`
- `/app/uso/cotas`
- `/app/uso/pacotes`
- `/app/uso/regras-economia`

## UC-014: Flow Simulation Before Activation

Actor: owner/admin.

Flow:

1. User opens flow config.
2. User edits mode, templates, windows, limits and handoff.
3. User runs simulation.
4. System tests success, missing data, exception, cost and transition.
5. Flow can activate only if gates pass.

Routes:

- `/app/fluxos/[flowId]`
- `/app/fluxos/[flowId]/simular`
- `/app/dados/qualidade`

## UC-015: WhatsApp Send Fails

Flow:

1. Send attempt fails through provider.
2. System creates integration log and operation case.
3. Case appears in `/app/operacao`.
4. Team can retry, send manually or mark resolved.
5. Idempotency prevents duplicate sends.

Routes:

- `/app/envios/[sendId]`
- `configuracao especifica da integracao`
- `/app/operacao/[caseId]`
