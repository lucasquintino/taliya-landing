# Draft Audit - Do The Agent Flows Produce A CRM With Integrated AI Agents?

> Status: exploratory draft. This document evaluates the current 91 + candidate AI-agent flows from the viewpoint of a Pilates studio manager buying Taliya. It asks whether the flow catalog is enough to produce a CRM with integrated AI agents.

## Short Answer

The current catalog is enough to define the **agent behavior layer**, but it is not enough by itself to define the whole CRM product.

With the current direction:

```text
91 existing agent flows
+ 5 strong additions
= 96 likely AI-agent flows
```

Taliya can become:

```text
a CRM with integrated AI agents
```

but only if the agent flows sit on top of a real CRM foundation:

- tenant and user accounts;
- contacts, students, responsible parties and interested people;
- agenda, attendance, make-up credits and waitlist;
- student plans, payments, contracts and financial exceptions;
- conversations, tasks, cases, approvals and audit logs;
- usage quotas, flow configuration and flow execution history;
- integrations such as WhatsApp, billing/payment, imports and files.

Without that foundation, the 96 flows become an automation map, not a usable CRM.

## Studio Manager Test

The manager does not think:

```text
Which agent flow is running?
```

She thinks:

```text
What needs attention today?
Which students are at risk?
Who owes money?
Which trials can convert?
Which classes are full or empty?
Which conversations need a human?
What did the system do?
Can I trust it?
What happens if I change a rule?
```

Therefore, the product must answer two levels at once:

1. CRM level: records, screens, state, history, search, filters, permissions, reports.
2. Agent level: detect, suggest, execute, hand off, explain, audit, respect quotas.

## What The 96 Agent Flows Cover Well

### Atendimento

The flow set covers the front door well:

- new messages;
- existing student requests;
- FAQs and allowed answers;
- opt-out;
- family/responsible handling;
- privacy;
- media and duplicate identity;
- SLA and handoff.

Manager outcome:

The studio can stop losing WhatsApp context and route conversations more reliably.

CRM dependency:

Requires contacts, conversations, responsible-party permissions, inbox, task queue, message logs and opt-out state.

### Agenda

The flow set covers the heart of Pilates operation:

- attendance confirmation;
- absence;
- no-show;
- make-up;
- waitlist;
- open slot recovery;
- trial availability;
- fixed schedule changes;
- studio-side cancellation;
- grid adjustments;
- first class;
- workshops.

Manager outcome:

The studio can reduce empty spots, forgotten make-ups and manual schedule confusion.

CRM dependency:

Requires calendar, class groups, class sessions, attendance records, credits, waitlist, capacity rules and teacher/class context.

### Vendas

With C15 added, the flow set covers sales better:

- WhatsApp lead intake;
- multichannel lead intake;
- pricing;
- trial scheduling;
- follow-up;
- objections;
- pre-enrollment;
- referrals;
- checkout abandonment;
- no-slot demand;
- lead-to-student conversion;
- upsell.

Manager outcome:

The studio can track interested people from first contact to enrollment without relying only on memory or WhatsApp.

CRM dependency:

Requires lead pipeline, source attribution, stages, owner assignment, trial records, conversion records and lost-reason tracking.

### Financeiro

With D15 added, the flow set covers student-facing finance:

- due reminders;
- overdue payment;
- Pix/link;
- payment confirmation;
- failed payment;
- receipts/invoices;
- renewal;
- pause/freezing;
- contract/terms;
- block/release;
- financial exceptions;
- effective plan ending/change.

Manager outcome:

The studio can collect better and avoid financial actions happening without context.

CRM dependency:

Requires student plans, payments, charges, contracts, policy snapshots, approval queue, reconciliation and audit.

### Retencao

With E13 added, the flow set covers the main churn risks:

- frequency drop;
- inactive student;
- return;
- cancellation risk;
- ex-student reactivation;
- satisfaction;
- complaint recovery;
- return after pause;
- risk profile;
- post-cancellation;
- engagement milestone;
- sensitive personal/health event;
- risk segmentation.

Manager outcome:

The studio can detect and act before churn becomes invisible.

CRM dependency:

Requires timeline, attendance patterns, payment status, complaint cases, risk scoring, segmentation, consent and follow-up status.

### Gestao

With F14 and F15 added, the flow set becomes much safer:

- daily priorities;
- money on the table;
- human queue;
- bottlenecks;
- weekly summary;
- data quality;
- quotas/limits;
- agent performance;
- permissions/audit;
- capacity planning;
- integration failures;
- import/migration;
- flow testing;
- automation incident review;
- policy/rule change governance.

Manager outcome:

The owner can see what the system is doing and where intervention is needed.

CRM dependency:

Requires operation cases, task queues, approvals, flow runs, audit events, quotas, integration logs and data-quality screens.

### Historico/Evolucao

The current set covers internal student context well:

- context before class;
- teacher notes;
- restrictions/care;
- goals/evolution;
- context for agents;
- documents/anamnesis;
- correction;
- teacher handoff;
- teacher reminders;
- safe context sharing;
- visibility permissions;
- unified timeline.

Manager outcome:

The studio can preserve student context instead of scattering it across teachers and WhatsApp.

CRM dependency:

Requires student history, documents, permissions, teacher views, timeline filters and sensitive-data audit.

## What Is Still Missing If The Goal Is A CRM With Agents

These are not necessarily more agent flows. They are product foundations without which the flows cannot be trusted.

### 1. CRM Object Model Must Be Real

The agent flows need durable objects to read/write:

- Contact;
- ResponsibleParty;
- Student;
- InterestedPerson;
- ClassGroup;
- ClassSession;
- AttendanceRecord;
- MakeUpCredit;
- WaitlistEntry;
- StudentPlan;
- Payment;
- Contract;
- Conversation;
- Message;
- OperationCase;
- Task;
- Approval;
- FlowRun;
- QuotaLedgerEntry;
- AuditEvent.

If these are missing, agents will only chat or suggest actions without being operational.

### 2. Operation Case Layer Is Essential

Many flows cannot end as "message sent".

They need cases:

- complaint;
- overdue payment;
- schedule exception;
- missing setup data;
- cancellation risk;
- financial exception;
- automation incident;
- policy change;
- data conflict;
- privacy request.

Without cases, the manager cannot track unresolved work.

### 3. Manual Mode Must Be First-Class

The Base plan has 0 agents. Also, even paid agent plans need manual fallback.

That means every important flow needs a manual path:

- create task;
- assign responsible;
- record decision;
- log outcome;
- close case;
- convert into copilot/autonomous later.

If manual mode is weak, the CRM becomes dependent on automation and the Base plan feels empty.

### 4. Copilot And Autonomous Need Different UI

A manager needs to see:

- what the agent detected;
- why it thinks that;
- what data it used;
- what action it proposes;
- what will be sent externally;
- cost/quota impact;
- what happens if approved;
- what happens if rejected.

Without this, "copilot" is just a magic suggestion box.

### 5. Quotas Must Be Attached To Actions, Not Just Plans

The system must know cost by:

- flow;
- agent;
- tenant;
- channel;
- message category;
- AI usage;
- media;
- batch job;
- history/context retrieval.

If quotas are only a billing screen, the manager cannot understand why automation stopped or got expensive.

### 6. Flow Simulation Must Exist Before Autonomy

Before activating autonomous behavior, the manager needs to simulate:

- new lead;
- absence;
- make-up request;
- overdue payment;
- complaint;
- plan cancellation;
- opt-out;
- low quota;
- missing data;
- external send failure.

Without simulation, activating autonomy will feel risky.

### 7. Agent Observability Must Be Productized

A manager needs answers:

- What did the agent do?
- Why did it do that?
- What did it not do because of a rule?
- Where did it hand off?
- What failed?
- What cost credits?
- Which flows are blocked by missing data?

This requires flow run history, audit, integration logs, and case timelines.

### 8. Data Quality Must Be A Workspace, Not A Background Detail

The agents depend on clean data:

- duplicate contacts;
- student without plan;
- class without capacity;
- teacher missing;
- payment without status;
- WhatsApp not linked;
- responsible not authorized;
- anamnesis missing;
- rule not configured.

If data quality is not visible, agents will fail in ways that look like product bugs.

## Are More Agent Flows Still Missing?

After applying the stricter counting rule, I would not add many more now.

Current recommendation:

```text
Canonical candidate count: 96
Possible expanded count: 98
```

Strong additions accepted:

- C15 Entrada Multicanal De Lead;
- D15 Encerramento Ou Alteracao Efetiva De Plano;
- E13 Reclamacao E Recuperacao De Confianca;
- F14 Incidente De Automacao E Correcao Operacional;
- F15 Mudanca De Politica Ou Regra Operacional.

Optional:

- E14 Primeira Semana Do Novo Aluno;
- G13 Gate De Anamnese, Consentimento E Contato De Emergencia.

The bigger missing work is not adding many more agent flows. It is making sure the CRM foundation and runtime can support these flows.

## Manager Verdict

From a studio manager perspective:

### If Taliya ships only the 96 flow catalog

It is not a CRM yet.

It is a strong automation blueprint.

### If Taliya ships CRM records + operation cases + tasks + approvals + agenda + finance + conversations + flow runtime

Then yes, it becomes:

```text
a CRM operational for Pilates studios with AI agents integrated into the system
```

### If Taliya ships CRM screens without agent runtime

It becomes a CRM, but not the differentiated agent product.

### If Taliya ships agents without CRM records

It becomes a chatbot/automation layer, not the product we want.

## Practical Product Decision

Use this structure:

1. **CRM Core**: contacts, students, interested people, agenda, plans, payments, conversations, tasks and history.
2. **Operation Layer**: cases, approvals, audit, quotas, data quality and integrations.
3. **Agent Flow Layer**: 96 candidate flows, with E14/G13 still under validation.

The flows are close enough to start designing the agent system.

The CRM is not complete unless the supporting product surfaces and objects are also part of the implementation plan.
