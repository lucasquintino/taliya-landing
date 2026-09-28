# Multi-View Product Audit - Taliya CRM Web/App

> Status: exploratory audit. This document reviews the current Taliya mapping through multiple visual/product lenses: master table, journeys, objects, swimlanes, screens, heatmap, kanban, mobile, data and agent boundaries.

## Executive Verdict

We are broadly on the right path.

The current direction is coherent:

```text
CRM operacional para studios de Pilates
+ agentes de IA integrados ao sistema
+ WhatsApp as one execution channel
+ manual/copilot/autonomous paths
+ programmatic core before AI
```

But the mapping is not final yet.

The main issue is not missing hundreds of new ideas. The main issue is **normalization**:

- candidate use cases need decision status;
- routes need route-type decisions;
- sensitive flows need exact gates;
- mobile scope needs sharper boundaries;
- some candidate routes/entities are not yet integrated into the main data model;
- some pages may be better as drawers, tabs or filtered case views;
- accepted, optional and merge-review items are still mixed.

## Audit Inputs

Reviewed artifacts:

- `product-master-map.md`
- `product-master-map.csv`
- `journey-metro-map.md`
- `object-action-map.md`
- `execution-swimlanes.md`
- `screen-inventory-tree.md`
- `coverage-heatmap.md`
- `decision-kanban.md`
- `use-case-execution-matrix.md`
- `routes-and-surfaces.md`
- `data-model.md`
- `agent-flow-cardinality-audit.md`
- `complete-manager-use-case-audit.md`

## View 1 - Master Table Audit

### What Looks Right

- 157 candidate manager use cases are now visible in one source.
- The table separates area, object, surface, UI pattern and modes.
- The CSV makes filtering possible.
- Manual/copilot/autonomous thinking is present across the product.

### Problems Found

1. **All rows still have `candidate` status.**
   This is correct while mapping, but not enough for product decisions.

2. **Priority is missing.**
   The table needs P0/P1/P2/out/merge.

3. **Route type is missing.**
   Some rows should be full pages, some drawers, some buttons, some background jobs.

4. **Risk class is missing.**
   Finance, health/history, privacy, batch sends and autonomy need explicit risk level.

5. **Some objects are composite strings.**
   Example: `ClassSession/Waitlist`, `Payment/Case`. Useful for exploration, but the data model needs canonical primary object + related objects.

### Recommended Adjustments

Add columns to the master table:

- `priority`: P0/P1/P2/out/merge;
- `decision`: accepted/candidate/merge/defer/out;
- `route_type`: page/detail/drawer/modal/button/background/report/config;
- `risk`: low/medium/high/blocked;
- `primary_object`;
- `related_objects`;
- `agent_flow_ids`;
- `needs_mobile`: yes/no/partial/approve-only;
- `needs_whatsapp`: none/inbound/outbound/hybrid.

## View 2 - Journey Metro Audit

### What Looks Right

The journey lines are useful and readable:

- lead to student;
- agenda operation;
- student finance;
- retention/trust;
- history/teacher;
- agent runtime/governance;
- daily manager loop.

### Problems Found

Missing or underrepresented metro lines:

1. **Workspace activation and setup journey**
   Claim workspace -> configure studio -> import -> resolve blockers -> configure agents -> first dashboard.

2. **Privacy/LGPD journey**
   Request -> validate identity/permission -> export/delete/anonymize -> audit.

3. **Data quality journey**
   Detect blocker -> fix missing data -> unblock flow -> audit.

4. **Incident recovery journey**
   Bad automation -> pause -> impact -> correction -> prevention -> re-enable.

5. **Policy change journey**
   Change rule -> simulate impact -> approval -> rollout -> audit -> monitor.

### Recommended Additions

Add these metro lines:

- Line 8: Onboarding and setup readiness.
- Line 9: Data quality and unblock automation.
- Line 10: Privacy and support governance.
- Line 11: Automation incident recovery.
- Line 12: Policy/rule lifecycle.

## View 3 - Object Action Map Audit

### What Looks Right

The object-first view is probably the most useful for discovering real screens and buttons.

It correctly maps actions around:

- Contact;
- Conversation;
- InterestedPerson;
- Student;
- ClassSession;
- MakeUpCredit;
- WaitlistEntry;
- Payment;
- StudentPlan;
- ComplaintCase;
- FlowConfiguration;
- FlowRun;
- PolicyVersion;
- DataQualityIssue;
- Approval.

### Problems Found

Important objects are missing from the object map:

- ClassGroup;
- Teacher/UserAccount/Membership;
- Resource;
- ClosureCalendar;
- Broadcast;
- SegmentDefinition;
- PaymentAgreement;
- RefundDisputeCase;
- PrivacyRequest;
- SupportAccessGrant;
- ExportJob;
- IntegrationLog;
- AuditEvent.

### Recommended Additions

Add object sections for:

- `ClassGroup`: grade, capacity, teacher, recurrence, room/resource, waitlist.
- `Teacher/Membership`: availability, permissions, class context, notes.
- `Resource`: room/equipment capacity, outage, availability.
- `SegmentDefinition`: create segment, eligibility, bulk approval.
- `Broadcast`: audience, template, approval, send status.
- `PrivacyRequest`: validate, export, delete/anonymize, audit.
- `SupportAccessGrant`: approve, scope, expire, audit.
- `ExportJob`: generate, download, audit.
- `IntegrationLog`: inspect, retry, incident.

## View 4 - Execution Swimlane Audit

### What Looks Right

The swimlanes correctly establish:

- programmatic CRM first;
- AI for draft/explanation/interpretation;
- approval before risky execution;
- audit/usage as persistent outputs;
- WhatsApp as one participant, not the whole system.

### Problems Found

Missing swimlane patterns:

1. **Bulk/campaign flow**
   Segment -> eligibility -> quota -> approval -> send -> monitor.

2. **Data correction/merge flow**
   Suggest duplicate -> human review -> merge -> audit -> re-index/update context.

3. **Privacy/LGPD flow**
   Request -> identity/permission -> export/delete/anonymize -> audit.

4. **Mobile quick action flow**
   Push/alert -> mobile approval -> execution -> audit.

5. **Provider failure/retry flow**
   Webhook failure -> idempotency -> retry/skip -> integration log -> case.

### Recommended Additions

Add five more swimlane templates for:

- bulk actions;
- data correction;
- privacy request;
- mobile approval;
- integration retry.

## View 5 - Screen Inventory Audit

### What Looks Right

The screen tree captures the product breadth well:

- public;
- auth/onboarding;
- app shell;
- inbox;
- students/history;
- agenda;
- sales;
- finance;
- retention;
- operations;
- management/reports;
- agents/runtime;
- usage/billing;
- data/integrations/governance;
- settings;
- policies;
- mobile app.

### Problems Found

#### Missing Detail Routes

These likely need detail routes if accepted:

- `/app/eventos/[eventId]`
- `/app/segmentos/[segmentId]`
- `/app/comunicados/[broadcastId]`
- `/app/checklists/[runId]`
- detalhes/drawers em `/app/financeiro/movimentacoes/[id]` para acordos, estornos e disputas
- `/app/exportacoes/[jobId]`
- `/app/privacidade/solicitacoes/[requestId]`
- `/app/suporte/acessos/[grantId]`
- `/app/recursos`
- `/app/recursos/[resourceId]`
- `/app/professores/[teacherId]`

#### Route Sprawl Risk

Some routes may not need top-level pages:

- excecoes financeiras, acordos, estornos e alteracoes de plano como tipos/filtros dentro de `/app/financeiro/movimentacoes`

These are consolidated into the `Movimentacoes` experience with filters, drawers, approvals and tasks.

Similarly:

- `/app/retencao/reativacoes`
- `/app/segmentos`
- `/app/comunicados`

May need a shared `BulkAction/Campaign` concept.

#### Overlap Risk

Potential overlaps:

- `/app/historico` vs `/app/alunos/[id]/linha-do-tempo`
- `/app/relatorios/agentes` vs `/app/agentes/[agentId]`
- `/app/dados/qualidade` vs setup checklist
- `/app/politicas` vs `/app/configuracoes/politicas`

These can still coexist, but their responsibilities must be sharper.

### Recommended Adjustments

Do not remove yet. Instead classify each route as:

- primary nav;
- object detail;
- subpage/tab;
- drawer/modal;
- filtered case list;
- report;
- config;
- background job detail.

## View 6 - Heatmap Audit

### What Looks Right

The heatmap correctly identifies high-risk zones:

- Finance;
- History/Teacher;
- Agents/Runtime;
- Data quality;
- Mobile scope;
- Gates.

### Problems Found

The heatmap is useful but still too coarse.

Need a second-level heatmap for:

- autonomy gates;
- mobile support;
- route maturity;
- data model maturity;
- permission sensitivity.

### Recommended Red Flags

Treat these as blockers before implementation:

1. Financial exception gates.
2. Sensitive history permissions.
3. Autonomy gates.
4. Consent/opt-out enforcement.
5. Quota/cost enforcement.
6. Policy versioning.
7. Audit for high-risk changes.
8. Support access controls.

## View 7 - Decision Kanban Audit

### What Looks Right

The kanban is the right tool to prevent circular discussion.

It captures:

- product shape;
- 96-flow baseline;
- B17 not standalone;
- programmatic before AI;
- docs still exploratory;
- MVP not final.

### Problems Found

Some items need to move from "not decided" to stronger decision categories:

- Support access approval should be required before production, even if UI depth is TBD.
- Financial exception gates should be a P0 blocker, not just detail.
- Sensitive history permissions should be a P0 blocker.
- Autonomy gates should be a P0 blocker.

### Recommended Adjustments

Add a kanban column:

```text
Must Decide Before Implementation
```

Items:

- permissions/RBAC;
- finance gates;
- history visibility;
- quota enforcement;
- approval model;
- audit model;
- support access model;
- data deletion/export policy.

## View 8 - Mobile Audit

### What Looks Right

Mobile is correctly framed as action-oriented:

- Today;
- Inbox;
- Agenda/class;
- Attendance;
- Student;
- Tasks;
- Approvals;
- Payment essentials;
- Complaint/case;
- Notes;
- Notifications.

### Problems Found

Mobile risks becoming too broad if every web concept gets a mobile screen.

Mobile should avoid:

- full agent configuration;
- full flow simulation;
- policy editing;
- integration setup;
- custom fields;
- exports;
- heavy reports.

### Recommended Mobile Model

Classify each mobile capability as:

- full action;
- approve-only;
- read-only;
- notification only;
- web-only.

High-value mobile actions:

- approve/reject;
- reply/prep reply;
- mark attendance;
- add note;
- view student;
- resolve task;
- pause automation;
- review alert;
- handle complaint.

## View 9 - Agent Flow Audit

### What Looks Right

96 candidate flows is a better working number than 91.

Accepted additions still make sense:

- C15 Multichannel lead intake;
- D15 Effective plan change/end;
- E13 Complaint and trust recovery;
- F14 Automation incident;
- F15 Policy/rule change.

### Problems Found

E14 and G13 are still ambiguous:

- E14 First-week new student is clearly a manager use case, but may or may not need standalone agent-flow status.
- G13 Intake/anamnesis/emergency gate is clearly a product need, but may be a data-quality/history gate instead of standalone agent flow.

### Recommendation

Keep E14/G13 as:

```text
accepted candidate use cases
optional standalone agent flows
```

Do not force them into the 96 until flow cards prove they need standalone configuration.

## View 10 - Data Model Audit

### What Looks Right

The base model has the right spine:

- tenant;
- users/memberships;
- contacts/students/leads;
- agenda;
- payments/contracts;
- conversations/messages;
- cases/tasks/approvals;
- flow config/runs;
- quota/audit/integration logs.

### Problems Found

The later audits introduced candidate entities not yet integrated:

- `PolicyVersion`;
- `Resource`;
- `ClosureCalendar`;
- `NotificationPreference`;
- `ChecklistRun`;
- `PaymentAgreement`;
- `RefundDisputeCase`;
- `PrivacyRequest`;
- `SupportAccessGrant`;
- `SegmentDefinition`;
- `Broadcast`;
- `ExportJob`;
- `RecordArchiveState`.

### Recommendation

Do not add all blindly.

Split into:

#### Should Likely Add

- PolicyVersion;
- PrivacyRequest;
- SupportAccessGrant;
- SegmentDefinition;
- PaymentAgreement;
- Resource if resources stay in scope;
- ChecklistRun if checklists stay in scope.

#### Could Be Modeled As OperationCase Types

- RefundDisputeCase;
- Broadcast;
- RecordArchiveState;
- Closure impact;
- Teacher substitution issue.

#### Could Be Job/Log Types

- ExportJob;
- Integration retry;
- report generation.

## Add / Adjust / Remove Summary

### Add

- Workspace/setup journey metro line.
- Data quality journey metro line.
- Privacy/LGPD journey metro line.
- Automation incident recovery journey line.
- Detail routes for accepted candidate objects.
- Route type classification.
- Priority/decision columns in master table.
- Risk class and mobile depth columns.
- Additional swimlanes for bulk, privacy, merge, mobile approval and provider retry.
- Data model review for PolicyVersion, PrivacyRequest, SupportAccessGrant, SegmentDefinition and PaymentAgreement.

### Adjust

- Treat 157 as candidate universe, not final scope.
- Treat E14/G13 as accepted use cases but optional standalone agent flows.
- Treat financial exception, history visibility and autonomy gates as P0 blockers.
- Normalize finance case routes to avoid too many top-level finance submodules.
- Separate `/app/politicas` from `/app/configuracoes/politicas`:
  - config = rules/settings;
  - policies = versioned operational changes and simulation.
- Separate `/app/historico` from student timeline:
  - student timeline = per-student event history;
  - historico workspace = teacher/history operations across students.

### Remove Or Keep Out

- Do not re-add B17 as standalone agent flow in current framing.
- Do not add a generic global "call agent" button as primary UX.
- Do not turn payroll, supplier AP, inventory purchase, tax advisory or clinical advice into MVP product scope.
- Do not make every candidate route a primary nav item.

## Priority Decisions To Make Next

Before adding more flows, make these decisions:

1. Are resources/rooms/equipment first-class CRM objects?
2. Are daily checklists first-class screens or Today widgets?
3. Are broadcasts/campaigns a module, or filtered actions inside Retention/Sales?
4. Are finance exceptions separate pages or one Finance Cases workspace?
5. Does mobile support finance actions beyond review/approve?
6. Do E14 and G13 become standalone agent flows or remain use cases/gates?
7. Which of the 157 are accepted, merged, deferred or out?

## Final Audit Verdict

We are on the right path.

The product model is now much clearer than before:

```text
CRM records and operations
  -> contextual actions
  -> programmatic core
  -> AI assistance where useful
  -> manual/copilot/autonomous execution
  -> audit, quota and safety gates
```

The biggest risk is no longer "we forgot the whole product".

The biggest risk is now:

```text
turning every candidate into a top-level screen before deciding route type, priority and risk.
```

The next broad-map artifact was created as:

```text
product-master-map-v2
```

with extra columns:

- priority;
- decision;
- route type;
- risk;
- mobile depth;
- primary object;
- related objects;
- agent flow ids.

After Round 1, the next best artifact is no longer another broad map. It is a decision pass over the 157 candidate rows:

```text
accepted / merged / deferred / out
```

That pass should decide route depth, autonomy boundary and mobile depth for each candidate before implementation planning.
