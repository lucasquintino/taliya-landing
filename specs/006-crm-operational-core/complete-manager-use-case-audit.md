# Complete Draft Audit - Manager Use Cases, Modes And Gaps

> Status: exploratory draft. This audit reviews manager-followable use cases for Taliya as a CRM with integrated AI agents. Use cases may be CRM-only, agent-assisted, manual, copilot or autonomous.

## Executive Verdict

The current `manager-use-case-catalog.md` is a strong baseline, but it should not be called complete yet.

Current state:

```text
132 cataloged manager use cases
+ 25 missing or under-modeled candidate use cases found in this audit
= 157 candidate manager use cases
```

Important distinction:

- **96 candidate AI-agent flows** describe what agents can do.
- **132 current manager use cases** describe how a manager can operate the current CRM/agent draft.
- **157 audited candidate manager use cases** is the broader working universe if manual, copilot and autonomous actions all count.

This does not mean v1 must ship 157 screens. Many are subflows, routes inside existing modules or later-stage workflows.

## Audit Rules

A use case counts when a manager or team member can:

- start it, review it or receive it as work;
- use a CRM route or mobile surface;
- make a decision, approve, delegate, correct, send, configure or close;
- produce a record, case, task, approval, audit event, report, message, schedule change, payment state or policy version.

A use case may be:

- unrelated to agents;
- agent-detected but human-executed;
- agent-prepared and human-approved;
- fully autonomous inside rules;
- manual-only for safety or product reasons.

## Mode Definitions Used In This Audit

| Mode | Meaning | Manager Experience |
| --- | --- | --- |
| Manual | Human performs the action; Taliya records and organizes it. | Task, form, case, note, status update, audit. |
| Copilot | Taliya prepares recommendation/action/message and waits for review. | Approval queue, editable proposal, impact preview. |
| Autonomous | Taliya executes inside configured limits. | Notification, execution log, audit, quota usage, exception if blocked. |

## Current 132 Use Cases - Mode Audit

This is a recommended default-mode distribution for the already cataloged 132 use cases. Individual tenants can configure more conservative behavior.

| Area | Count | Manual-first | Copilot-first | Autonomous-eligible |
| --- | ---: | ---: | ---: | ---: |
| Setup, access and governance | 13 | 9 | 4 | 0 |
| Daily command center | 10 | 5 | 2 | 3 |
| Inbox, contacts and privacy | 12 | 5 | 4 | 3 |
| Sales and interested people | 16 | 4 | 5 | 7 |
| Agenda and attendance | 17 | 5 | 5 | 7 |
| Finance and student plans | 16 | 7 | 5 | 4 |
| Retention and complaints | 13 | 5 | 5 | 3 |
| Student history and teacher work | 11 | 4 | 5 | 2 |
| Agents, runtime and quotas | 14 | 5 | 6 | 3 |
| Reports, integrations and administration | 10 | 4 | 2 | 4 |
| **Total** | **132** | **53** | **43** | **36** |

Interpretation:

- The product is not "autonomous by default".
- A serious CRM with agents needs a lot of manual and copilot paths.
- Autonomous behavior is strongest in reminders, classification, summaries, simple routing, low-risk follow-up, data-quality detection and usage alerts.

## Safety Mode Rules

### Always Manual Or Human-Confirmed

- health/clinical advice;
- refund, chargeback, discount, courtesy, block/release;
- student plan cancellation when money/contract/agenda are affected;
- data deletion/anonymization;
- role/permission changes;
- sensitive history sharing;
- complaint resolution with reputation risk;
- policy changes that affect students;
- external communication in batch when cost/reputation risk exists.

### Copilot By Default

- campaign or batch send;
- complaint response draft;
- cancellation-risk response;
- plan change impact;
- debt/payment agreement;
- policy impact simulation;
- import/merge decisions;
- sharing student history;
- automation incident correction;
- cross-object data correction.

### Autonomous-Eligible

- presence confirmation;
- allowed FAQ;
- simple lead classification;
- simple follow-up within cadence;
- trial reminders;
- due reminders within policy;
- Pix/link resend when safe;
- low-risk satisfaction check;
- weekly/daily summaries;
- data-quality detection;
- usage/quota alerts;
- flow run logging.

## Coverage Verdict By Area

### Setup, Access And Governance

Current coverage is good for workspace claim, profile, import, roles, channels, templates, agenda/finance/privacy rules and policies.

Missing or under-modeled:

- holidays/recess/closures;
- rooms/equipment/resources;
- teacher availability rules;
- custom tags/segments/fields;
- role notification preferences.

Verdict:

Good CRM foundation, but operational setup needs a few more studio-specific controls.

### Daily Command Center

Current coverage is good for daily priorities, money on the table, tasks, approvals, notifications, bottlenecks, weekly summary and data blockers.

Missing or under-modeled:

- daily opening/closing checklist;
- class-day announcements/broadcasts;
- resource/teacher disruptions as manager work.

Verdict:

Good for agent-driven priorities. Needs a practical checklist layer for the human routine.

### Inbox, Contacts And Privacy

Current coverage is strong for conversations, handoff, opt-out, groups, contact updates, responsible validation, media, duplicates and privacy/data requests.

Missing or under-modeled:

- LGPD execution path for export/delete/anonymize;
- blocked/unsafe contact handling;
- support access authorization when Taliya staff helps a tenant.

Verdict:

Strong for v1, but compliance execution must be more explicit.

### Sales And Interested People

Current coverage is strong after C15: multichannel capture, walk-in/manual lead, source attribution, qualification, pricing, trial, follow-up, objection, pre-enrollment, checkout, referral, no-slot demand and conversion.

Missing or under-modeled:

- campaign/list creation as manager work;
- segment creation for later bulk actions;
- source ROI exists, but campaign-to-source quality could be made sharper.

Verdict:

Strong enough for v1 sales CRM. Additional marketing sophistication can be P1/P2.

### Agenda And Attendance

Current coverage is strong: grade, classes, attendance, confirmation, absence, no-show, make-up, credits, open slot, waitlist, fixed schedule, studio cancellation, capacity, first class and workshops.

Missing or under-modeled:

- holidays/recess impact;
- room/equipment/resource availability;
- teacher availability/substitution as system work;
- bulk class announcements not tied to cancellation.

Verdict:

Strong for agenda operation. Pilates-specific resource controls need a decision: include in CRM v1 or defer.

### Finance And Student Plans

Current coverage is strong for student-facing receivables: plans, overview, reminders, overdue, Pix/link, confirmation, reconciliation, failed payment, receipts, contracts, exceptions, pause, block, courtesy, plan change and monthly close.

Missing or under-modeled:

- partial payment/payment promise;
- debt renegotiation/installment agreement;
- refund/chargeback/dispute case;
- accountant/fiscal export;
- cashflow forecast from student receivables.

Verdict:

Strong for collection and student plan operations. Not a full ERP/accounting product, and that boundary should be explicit.

### Retention And Complaints

Current coverage is strong: retention dashboard, frequency drop, inactive, return, cancellation risk, post-cancel, reactivation, satisfaction, complaint, pause return, risk segmentation and sensitive event.

Missing or under-modeled:

- first-week new student journey;
- milestone/engagement celebration as manager-visible case;
- complaint escalation level and pause rules.

Verdict:

Strong for churn and relationship work. First-week journey is probably worth adding as P1.

### Student History And Teacher Work

Current coverage is strong for teacher context, observations, restrictions, objectives, documents, correction, handoff, reminders, safe sharing, permissions and timeline.

Missing or under-modeled:

- anamnese/emergency-contact gate;
- periodic student evaluation/review cycle.

Verdict:

Strong for internal context. Intake gating deserves validation because it affects safety and first-class readiness.

### Agents, Runtime And Quotas

Current coverage is strong for configuring agents/flows, simulation, pause/activate, execution, approvals, performance, incidents, policy change, data blockers, quota and economy rules.

Missing or under-modeled:

- regression simulation after policy changes;
- autonomy-change review history;
- cross-flow blast-radius view when one rule changes.

Verdict:

Good draft. The product should avoid enabling autonomy before simulation/audit/rollback exists.

### Reports, Integrations And Administration

Current coverage is good for billing, invoices, integrations, logs, audit, reports, finance/sales/capacity/source ROI.

Missing or under-modeled:

- full CRM export/backup;
- support access approval;
- archived record management.

Verdict:

Good for product operations. Needs governance/admin hardening before production.

## 25 Missing Or Under-Modeled Candidate Use Cases

These are candidate additions to review before updating the official catalog.

| ID | Candidate Use Case | Default Mode | Priority | Primary Routes Needed | Agent/Layer |
| --- | --- | --- | --- | --- | --- |
| AUD-001 | Configure holidays, recess and closure dates | Manual/Copilot | P0 | `/app/configuracoes/agenda`, `/app/politicas` | CRM + Gestao/F15 |
| AUD-002 | Configure rooms, equipment and resource capacity | Manual | P1 | `/app/configuracoes/recursos`, `/app/agenda` | CRM + Agenda |
| AUD-003 | Configure teacher availability/substitution rules | Manual | P2 | `/app/configuracoes/equipe`, `/app/configuracoes/agenda` | CRM + Agenda |
| AUD-004 | Configure custom tags, segments and fields | Manual | P1 | `/app/configuracoes/campos`, `/app/segmentos` | CRM core |
| AUD-005 | Configure role notification preferences | Manual | P1 | `/app/configuracoes/notificacoes` | CRM core |
| AUD-006 | Run daily opening/closing checklist | Manual/Copilot | P1 | `/app/checklists`, `/app/hoje` | Gestao |
| AUD-007 | Handle teacher availability or substitution issue | Manual/Copilot | P2 | `/app/operacao/[caseId]`, `/app/agenda` | Agenda/Gestao |
| AUD-008 | Handle room/equipment outage impact | Copilot | P1 | `/app/agenda`, `/app/operacao/[caseId]` | Agenda/Gestao |
| AUD-009 | Handle holiday/recess class impact | Copilot | P1 | `/app/politicas/[policyId]/simular`, `/app/agenda` | Agenda/Gestao |
| AUD-010 | Send class/student broadcast not tied to cancellation | Copilot | P1 | `/app/comunicados`, `/app/aprovacoes` | Atendimento/Gestao |
| AUD-011 | Register partial payment or payment promise | Manual/Copilot | P0 | `/app/financeiro/movimentacoes/[id]` | Financeiro |
| AUD-012 | Renegotiate overdue balance/installment agreement | Manual/Copilot | P2 | `/app/financeiro/movimentacoes`, `/app/aprovacoes` | Financeiro |
| AUD-013 | Handle refund, chargeback or payment dispute | Manual | P1 | `/app/financeiro/movimentacoes`, `/app/operacao/[caseId]` | Financeiro |
| AUD-014 | Export financial/accounting handoff | Manual | P2 | `/app/exportacoes`, `/app/relatorios/financeiro` | Financeiro |
| AUD-015 | Review cashflow forecast from student receivables | Autonomous/Copilot | P2 | `/app/relatorios/financeiro`, `/app/dinheiro-na-mesa` | Financeiro/Gestao |
| AUD-016 | Review student milestone/engagement celebration | Autonomous/Copilot | P2 | `/app/retencao`, `/app/alunos/[id]` | Retencao/E10 |
| AUD-017 | Follow first-week new student journey | Copilot/Autonomous | P1 | `/app/alunos/[id]`, `/app/retencao` | Retencao/E14 candidate |
| AUD-018 | Enforce anamnese, consent and emergency-contact gate | Manual/Copilot | P1 | `/app/historico/documentos`, `/app/dados/qualidade` | Historico/G13 candidate |
| AUD-019 | Schedule periodic student evaluation/review | Manual/Copilot | P2 | `/app/historico`, `/app/tarefas` | Historico |
| AUD-020 | Escalate sensitive complaint to owner and pause automations | Manual/Copilot | P0 | `/app/reclamacoes/[caseId]`, `/app/operacao` | Retencao/E13 |
| AUD-021 | Export full CRM data or backup | Manual | P2 | `/app/exportacoes` | Admin |
| AUD-022 | Execute LGPD export/delete/anonymize request | Manual | P1 | `/app/privacidade/solicitacoes`, `/app/auditoria` | Atendimento/A8 + Security |
| AUD-023 | Approve Taliya support access to tenant workspace | Manual | P1 | `/app/suporte/acessos`, `/app/auditoria` | Security/Gestao |
| AUD-024 | Archive/reactivate student, lead or contact record | Manual | P0 | `/app/alunos`, `/app/interessados`, `/app/contatos` | CRM core |
| AUD-025 | Create segment and review bulk action eligibility | Copilot | P1 | `/app/segmentos`, `/app/aprovacoes` | Vendas/Retencao/Gestao |

## Route Gaps Found

The current route map is close, but these routes should be considered if the candidate use cases are accepted:

| Route | Needed For |
| --- | --- |
| `/app/configuracoes/recursos` | Rooms, equipment and resource capacity. |
| `/app/configuracoes/campos` | Custom fields/tags. |
| `/app/configuracoes/notificacoes` | Role notification preferences. |
| `/app/checklists` | Daily opening/closing checklist. |
| `/app/comunicados` | Broadcasts not tied to one existing flow. |
| Tipos em `/app/financeiro/movimentacoes` | Partial payments, renegotiation, refunds, chargebacks and disputes. |
| `/app/exportacoes` | CRM/financial export and backup. |
| `/app/privacidade/solicitacoes` | LGPD operational request handling. |
| `/app/suporte/acessos` | Audited support access approval. |
| `/app/segmentos` | Segment creation and bulk eligibility review. |

## Data Model Gaps Found

If the candidate use cases are accepted, the model needs new or explicit entities:

| Entity | Needed For |
| --- | --- |
| `PolicyVersion` | Rule/policy effective dates, rollout and rollback. |
| `Resource` | Rooms, equipment, capacity and availability. |
| `ClosureCalendar` | Holidays, recess and closure impact. |
| `NotificationPreference` | Role/user notification routing. |
| `ChecklistRun` | Daily/opening/closing manager routines. |
| `PaymentAgreement` | Partial payment, promise and renegotiation. |
| `RefundDisputeCase` | Refunds, disputes and chargebacks. |
| `PrivacyRequest` | LGPD export/delete/anonymize handling. |
| `SupportAccessGrant` | Audited Taliya support access. |
| `SegmentDefinition` | Segment and bulk action eligibility. |
| `RecordArchiveState` | Archive/reactivation of contacts, leads and students. |

## What Should Not Become Taliya V1 Scope

These are real studio-manager concerns, but they would push Taliya toward ERP/HR/accounting too early:

- full payroll;
- employee timesheets;
- supplier accounts payable;
- inventory purchasing;
- tax calculation/advisory;
- complete accounting ledger;
- complex commission engine;
- multi-unit enterprise consolidation;
- full marketing automation platform;
- clinical prescription or medical advice.

They can appear as notes, reports, exports or future integrations, but should not drive the first CRM scope.

## Completeness Verdict

### Is 132 complete?

No.

It is a strong baseline, but this audit found 25 additional candidate manager use cases.

### Is 157 final?

Also no.

It is the current full working universe after this audit. It should be validated with product decisions and then split into:

- accepted P0/P1;
- accepted later;
- merged into existing use cases;
- explicitly out of scope.

### Do all 157 need agents?

No.

Many are CRM-only or manual-first. That is correct because Taliya must work as a CRM even with 0 agents.

### Can actions be manual, copiloto or autonomous?

Yes. The system should model the same operational object with different execution modes:

```text
signal -> case/task/flow -> manual action OR copilot approval OR autonomous execution -> audit/result
```

## Recommended Next Step

Round 2 has now produced a full 157-case classification pass in `rodada-2-classificacao-157.pt-BR.md`.

Before implementation, review that classification and confirm:

1. accept for detailed design;
2. accept with lean depth;
3. merge into existing MUC;
4. keep as a case/gate but not a standalone agent flow.

After that, update:

- `manager-use-case-catalog.md`;
- `routes-and-surfaces.md`;
- `data-model.md`;
- `implementation-slices.md`.
