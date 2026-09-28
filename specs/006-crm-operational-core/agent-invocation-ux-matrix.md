# Draft UX Matrix - How Users Invoke Agents In The CRM

> Status: exploratory draft. This document maps how AI agents are invoked inside Taliya web/app and WhatsApp. It answers whether the system has buttons or entry points that call agents.

## Short Answer

The current specs include agent modes, approvals, simulations and flow execution, but they do not yet explicitly map the UX entry points for "calling" an agent.

This document adds that missing layer.

## Principle

Taliya should not rely on one generic button called "call agent" everywhere.

Instead, agent invocation should happen through four patterns:

1. **Automatic trigger**: configured autonomous flow starts from an event.
2. **Contextual smart action**: user clicks a specific action in context.
3. **Copilot approval**: agent prepares an action and asks for human approval.
4. **Assistant side panel / command bar**: user asks Taliya for help in the current context.

## Invocation Types

| Type | User Mental Model | Example |
| --- | --- | --- |
| Automatic | "Taliya handled this because I configured it." | Presence confirmation sent before class. |
| Contextual button | "Help me with this specific object." | Prepare collection message on overdue payment. |
| Copilot approval | "Taliya suggested something; I decide." | Approve cancellation communication to affected students. |
| Assistant side panel | "I need guidance or explanation here." | Why did this flow stop? What should I do with this student? |
| Bulk/action bar | "Run this on a selected group." | Create follow-up tasks for selected inactive students. |

## Global UI Components

### Contextual Action Menu

Appears on object pages and list rows:

- student;
- interested person;
- conversation;
- class session;
- payment;
- case;
- complaint;
- flow;
- policy.

Label style:

- "Analyze risk";
- "Prepare message";
- "Suggest next action";
- "Summarize";
- "Simulate";
- "Run now";
- "Create task";
- "Ask Taliya".

### Assistant Side Panel

Available in CRM web and possibly app v1 as a lightweight panel.

It should receive current context:

- current route;
- selected object;
- user role;
- tenant;
- active flow/case;
- permissions;
- relevant data snapshot.

It can answer, explain, summarize or draft, but high-risk actions still go through approval.

### Approval Drawer

Used for copiloto mode:

- proposed message;
- proposed data change;
- reason;
- data used;
- cost/quota impact;
- risk flags;
- approve/edit/reject.

### Flow Run Panel

Used after autonomous or manual execution:

- what happened;
- why;
- what was skipped;
- quota used;
- next flow/case/task;
- audit link.

## Route-Level Invocation Matrix

| Surface | Primary Agent Entry Points | Invocation Pattern |
| --- | --- | --- |
| `/app/hoje` | Analyze priorities, explain today, create tasks, start high-value actions | Assistant panel, contextual buttons, automatic summary |
| `/app/inbox` | Summarize conversation, prepare reply, classify intent, handoff, pause automation | Contextual buttons, assistant panel, copilot approval |
| `/app/conversas/[id]` | Prepare response, summarize, identify contact, route to flow, resume/pause AI | Contextual buttons, copilot approval |
| `/app/contatos/[id]` | Merge suggestion, update preference, validate permission, summarize contact | Contextual buttons, copilot |
| `/app/alunos/[id]` | Analyze risk, summarize timeline, suggest next action, prepare message | Contextual buttons, assistant panel |
| `/app/alunos/[id]/linha-do-tempo` | Summarize history, detect conflicts, share safe context | Contextual buttons, copilot approval |
| `/app/agenda` | Confirm presence, find conflicts, recover slots, suggest changes | Contextual buttons, automatic triggers |
| `/app/aulas/[id]` | Prepare class context, detect no-shows, ask for teacher notes | Automatic, contextual buttons |
| `/app/aulas/[id]/chamada` | Correct attendance, create make-up, detect no-show risk | Contextual buttons, copilot |
| `/app/reposicoes` | Suggest eligible slots, validate credit, prepare options | Contextual buttons, automatic |
| `/app/lista-espera` | Select candidates, prepare invite, fill open slot | Contextual buttons, copilot/autonomous |
| `/app/vendas` | Prioritize leads, suggest follow-up, detect stalled opportunities | Automatic, assistant panel |
| `/app/vendas/captura` | Deduplicate lead, classify source, assign owner, route next action | Contextual buttons, automatic |
| `/app/interessados/[id]` | Qualify, suggest reply, schedule trial, convert to student | Contextual buttons, copilot |
| `/app/experimental` | Send reminders, handle no-show, follow up after trial | Automatic, contextual buttons |
| `/app/financeiro` | Explain financial priorities, surface overdue risk | Assistant panel, automatic summary |
| `/app/financeiro/movimentacoes/[id]` | Prepare reminder, reconcile, explain divergence, send link, simulate plan-impact change | Contextual buttons, copilot/autonomous |
| `/app/financeiro/movimentacoes` | Run collection cadence, review reconciliation, prepare batch reminders and create review tasks | Bulk action, copilot/autonomous |
| `/app/retencao` | Prioritize risk, suggest recovery action, segment students | Assistant panel, automatic |
| `/app/reclamacoes/[caseId]` | Summarize complaint, suggest response, recovery plan, pause automation | Contextual buttons, copilot |
| `/app/cancelamentos` | Summarize cancellation risk, prepare save plan, handoff | Contextual buttons, copilot/manual |
| `/app/historico` | Summarize context, detect sensitive data, suggest teacher note | Contextual buttons, assistant panel |
| `/app/historico/documentos` | Classify document, extract safe fields, flag missing intake | Contextual buttons, copilot |
| `/app/professores` | Prepare class context, remind notes, handoff between teachers | Automatic, contextual buttons |
| `/app/operacao/[caseId]` | Summarize case, suggest next action, delegate, close with audit | Contextual buttons, assistant panel |
| `/app/aprovacoes/[approvalId]` | Explain proposal, edit message, approve/reject | Approval drawer |
| `/app/fluxos/[flowId]` | Configure, explain, simulate, activate, pause, run now | Contextual buttons |
| `/app/fluxos/[flowId]/simular` | Test examples, compare modes, show risk gates | Simulation action |
| `/app/fluxos/execucoes/[runId]` | Explain run, debug failure, create incident | Flow run panel, contextual buttons |
| `/app/operacao/incidentes/[incidentId]` | Find cause, propose correction, prevent recurrence | Contextual buttons, copilot |
| `/app/politicas/[policyId]` | Simulate policy impact, draft rollout, schedule effective date | Contextual buttons, copilot |
| `/app/dados/qualidade` | Fix blockers, suggest merges, create tasks | Contextual buttons, bulk action |
| `/app/uso` | Explain quota, suggest economy settings, identify costly flows | Assistant panel, contextual buttons |
| `configuracao especifica da integracao` | Explain failure, retry safely, create incident | Contextual buttons |

## Examples By Screen

### Student Profile

Buttons:

- Analyze risk;
- Summarize timeline;
- Suggest next action;
- Prepare message;
- Create retention task;
- Ask Taliya.

Blocked actions:

- sharing sensitive history without approval;
- clinical advice;
- financial exception without permission.

### Conversation Detail

Buttons:

- Summarize conversation;
- Prepare reply;
- Identify contact;
- Route to flow;
- Human takeover;
- Pause/resume AI.

Autonomous triggers:

- allowed FAQ;
- simple classification;
- opt-out detection;
- SLA task creation.

### Payment Detail

Buttons:

- Prepare cobranÃ§a;
- Send Pix/link;
- Explain divergence;
- Create financial exception;
- Mark as manual review.

Copilot required:

- debt negotiation;
- refund/dispute;
- block/release;
- high-risk overdue message.

### Flow Detail

Buttons:

- Simulate;
- Activate;
- Pause;
- Run now;
- View executions;
- Explain config.

Guardrails:

- "Run now" still checks entitlement, quota, required data, consent, risk and send window.

## Mobile App Invocation

Mobile should favor quick, bounded agent actions:

- summarize conversation;
- prepare reply;
- approve/reject;
- create task;
- mark attendance;
- add teacher note;
- review alert;
- pause automation;
- ask Taliya about current object.

Heavy configuration should stay web-first:

- configuring flow rules;
- setting quotas;
- editing policies;
- connecting integrations;
- bulk actions.

## What This Adds To Existing Docs

Existing docs already cover:

- manual/copilot/autonomous mode;
- approvals;
- flow simulation;
- flow execution history;
- routes.

This document adds:

- where the user clicks;
- what button/action invokes an agent;
- when no click is needed because it is automatic;
- when a proposal goes to approval;
- how assistant/command behavior should stay context-aware.

## Product Rule

Do not make the AI feel like a separate chatbot pasted into the CRM.

The agent should feel embedded in the object the user is already handling:

```text
student -> smart actions about that student
payment -> smart actions about that payment
class -> smart actions about that class
conversation -> smart actions about that conversation
flow -> simulation/config/execution actions for that flow
```
