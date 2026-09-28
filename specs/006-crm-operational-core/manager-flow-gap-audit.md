# Draft Audit - Are The 91 Flows Enough For A Pilates Studio Manager?

> Status: exploratory draft. This document does not decide final product scope. It tests whether the current 91 agent flows are enough when seen through the eyes of a studio manager buying Taliya as a CRM/operational system.

## Short Answer

No.

The 91 flows are a strong map for the **agent-assisted operational MVP**, but they should not be treated as the complete map of every possible CRM/product path.

They cover many recurring interactions around WhatsApp, agenda, sales, payments, retention, management summaries, and student history. However, a Pilates studio manager also has work that is:

- administrative, not conversational;
- recurring, but not always agent-driven;
- related to staff, equipment, compliance, expenses, and internal policies;
- needed before automation can safely work;
- needed after automation produces a recommendation.

Therefore, the current 91 flows are better described as:

```text
The initial agent-operation flow map for Taliya.
```

Not:

```text
The complete CRM/business-process map for every studio operation.
```

## Audit Lens

Persona:

- studio owner/manager;
- runs a Pilates studio with reception, teachers, students, interested people, recurring schedules, make-up classes, monthly payments, WhatsApp, contracts, and operational exceptions;
- wants fewer missed opportunities, fewer manual follow-ups, better control of agenda/finance/retention, and less dependence on memory.

Daily question:

```text
What do I need to know, decide, delegate, collect, fix, approve, or document to keep the studio healthy?
```

## What The 91 Flows Cover Well

### 1. Conversation Intake And Triage

Covered by A1-A10.

Strong coverage:

- new WhatsApp conversations;
- allowed questions;
- existing student requests;
- out-of-scope messages;
- handoff to human;
- opt-out and consent;
- identity, duplicates, and media;
- privacy and preferences;
- groups/family/responsibles;
- conversation lifecycle and SLA.

Assessment:

This is solid for the communication layer. It is not yet a full CRM case-management catalog, but it covers most front-door situations.

### 2. Agenda Operations

Covered by B1-B16.

Strong coverage:

- presence confirmation;
- absence with notice;
- no-show;
- open slot recovery;
- make-up/rebooking;
- waitlist;
- experimental class availability;
- fixed schedule changes;
- studio-side cancellation;
- capacity conflicts;
- grid adjustments;
- first class;
- workshop/special class.

Assessment:

This is the strongest part of the map. It is close to a real Pilates operation. Gaps remain around teacher operations, equipment maintenance, room/resource setup, and incident handling.

### 3. Sales

Covered by C1-C14.

Strong coverage:

- prices/plans;
- experimental class;
- reminders;
- post-experimental follow-up;
- objections;
- pre-enrollment;
- lead source;
- lost lead;
- referral;
- checkout abandonment;
- no available slot;
- lead-to-student conversion;
- upsell.

Assessment:

Good for direct lead conversion. Less complete for marketing operations, campaign performance, inbound sources beyond WhatsApp, manual pipeline governance, and source ROI.

### 4. Student Billing

Covered by D1-D14.

Strong coverage:

- payment reminders;
- overdue payment;
- Pix/link;
- payment confirmation;
- plan renewal;
- financial exceptions;
- failed payment;
- receipt/invoice request;
- pause/freeze;
- reconciliation;
- contract/terms;
- block/release;
- credits/courtesies;
- monthly close.

Assessment:

Good for **student receivables**. Not complete for the whole financial life of the studio: expenses, payroll, supplier bills, cashflow, taxes/accounting exports, commission, and profitability are not first-class flows.

### 5. Retention

Covered by E1-E12.

Strong coverage:

- frequency drop;
- inactive student;
- return;
- cancellation risk;
- ex-student reactivation;
- satisfaction;
- return after pause;
- risk profile;
- post-cancellation;
- engagement milestone;
- health/personal event;
- risk segmentation.

Assessment:

Strong retention map. Missing deeper customer-success routines such as structured renewal meetings, goal review cycles with manager, complaint resolution lifecycle, and formal save-offer governance.

### 6. Management And Agent Operations

Covered by F1-F13.

Strong coverage:

- daily priorities;
- money on the table;
- human queue;
- recurring bottlenecks;
- weekly summary;
- data/setup quality;
- credits/limits;
- performance by agent/responsible;
- permissions/audit;
- capacity/growth;
- failures/webhooks;
- import/migration;
- flow testing.

Assessment:

Good as an AI-operation control plane. Less complete as an owner business cockpit. It does not yet fully cover staff management, expenses, profitability, inventory/equipment, service quality process, or strategic planning.

### 7. Student History And Evolution

Covered by G1-G12.

Strong coverage:

- context before class;
- post-class observation;
- restriction/care;
- objective/evolution;
- context for agents;
- documents/anamnesis;
- history correction;
- teacher handoff;
- teacher reminders;
- safe context sharing;
- history permission;
- unified timeline.

Assessment:

Very important and well mapped. Missing possible formal flows around assessment scheduling, consent renewal, incident reports, emergency contact verification, and periodic student review.

## Concrete Manager Simulation

### Scenario 1 - Monday Morning

The manager opens Taliya and asks:

- Who is missing today?
- Which classes are full or empty?
- Which trials are booked?
- Which payments are late?
- Which teachers are absent or overloaded?
- Is any room/equipment unavailable?
- Which students need attention?
- Which setup/data problems block automation?

Covered:

- priorities, agenda, payments, retention, setup quality.

Partial or missing:

- teacher availability/shift management;
- equipment/room maintenance;
- staff workload;
- daily opening checklist;
- internal operational checklist unrelated to agents.

Candidate missing flows:

- H1 Daily Opening Checklist.
- H2 Teacher Availability And Substitution.
- H3 Room/Equipment Availability And Maintenance.
- H4 Staff Workload And Coverage.

### Scenario 2 - New Student Starts

The manager needs:

- lead converted;
- payment/contract confirmed;
- first class scheduled;
- anamnesis collected;
- emergency contact validated;
- restrictions visible to teacher;
- welcome orientation sent;
- teacher notified;
- first-week follow-up scheduled.

Covered:

- C13, D11, B15, G6, G3, G1/G8.

Partial or missing:

- emergency contact validation as explicit flow;
- first-week success path;
- consent/health intake completion gate;
- structured onboarding checklist for the student, not only tenant onboarding.

Candidate missing flows:

- H5 New Student Operational Onboarding.
- H6 Emergency Contact And Responsible Validation.
- H7 First-Week Success Follow-Up.
- H8 Health Intake Completion Gate.

### Scenario 3 - Teacher Calls In Sick

The manager needs:

- identify affected classes;
- find substitute;
- decide cancel/reschedule;
- notify students;
- adjust credits;
- record teacher absence;
- maybe calculate payment impact.

Covered:

- B9 studio-side cancellation;
- B11 grid adjustment;
- G8 teacher handoff.

Partial or missing:

- substitute teacher search/assignment;
- teacher absence record;
- payroll/commission impact;
- teacher availability calendar.

Candidate missing flows:

- H2 Teacher Availability And Substitution.
- H9 Teacher Absence And Payroll Impact.

### Scenario 4 - Equipment Breaks

The manager needs:

- mark equipment/room unavailable;
- identify affected classes;
- prevent new bookings;
- schedule maintenance;
- notify staff/students if needed;
- track supplier/repair status.

Covered:

- B9 and B10 mention room/equipment unavailable.

Partial or missing:

- equipment inventory;
- maintenance task;
- supplier interaction;
- recurring safety inspection;
- resource-level availability.

Candidate missing flows:

- H3 Room/Equipment Availability And Maintenance.
- H10 Equipment Safety Inspection.
- H11 Supplier/Maintenance Follow-Up.

### Scenario 5 - Month-End Business Review

The manager needs:

- receivables;
- overdue amounts;
- cancellations;
- new students;
- churn;
- occupancy;
- teacher costs;
- rent/expenses;
- marketing spend;
- profit estimate;
- taxes/accounting handoff.

Covered:

- D14 monthly close;
- F2 money on the table;
- F5 weekly summary;
- F8 performance;
- F10 capacity/growth.

Partial or missing:

- accounts payable;
- expense tracking;
- payroll/commission;
- profit/cashflow;
- accountant export;
- marketing ROI.

Candidate missing flows:

- H12 Accounts Payable And Studio Expenses.
- H13 Payroll/Commission Review.
- H14 Cashflow And Profitability Snapshot.
- H15 Accountant Export / Fiscal Handoff.
- H16 Marketing Spend And Source ROI.

### Scenario 6 - Parent/Responsible Complains

The manager needs:

- know whether the responsible is authorized;
- capture complaint;
- route to manager/teacher;
- pause automation;
- record resolution;
- follow up after resolution.

Covered:

- A9 responsibles/groups;
- A5 handoff;
- E6 satisfaction;
- E4 cancellation risk.

Partial or missing:

- complaint ticket lifecycle;
- root cause category;
- resolution SLA;
- post-resolution check.

Candidate missing flows:

- H17 Complaint Case Lifecycle.
- H18 Post-Resolution Satisfaction Check.

### Scenario 7 - Studio Changes Policy

The manager changes:

- absence notice deadline;
- make-up validity;
- price table;
- cancellation policy;
- teacher access;
- campaign permissions.

Covered:

- F9 permissions/audit;
- F13 flow testing;
- F6 setup quality;
- B13 credits;
- C1 pricing;
- D11 terms.

Partial or missing:

- policy versioning;
- effective date;
- impact simulation;
- student communication plan;
- rollback.

Candidate missing flows:

- H19 Policy Versioning And Effective Date.
- H20 Policy Change Impact Simulation.
- H21 Policy Communication Rollout.

### Scenario 8 - Lead Comes From Instagram, Site Form, Referral Or Walk-In

The manager needs:

- capture source;
- deduplicate;
- assign owner;
- track campaign;
- convert to experimental;
- compare source quality.

Covered:

- C8 origin/qualification;
- C10 referral;
- A1 new conversation.

Partial or missing:

- non-WhatsApp inbound forms;
- Instagram/DM source handling;
- manual walk-in lead registration;
- campaign attribution and ROI.

Candidate missing flows:

- H22 Multi-Source Lead Capture.
- H23 Walk-In Lead Registration.
- H16 Marketing Spend And Source ROI.

### Scenario 9 - Data Is Wrong But Automation Already Acted

The manager needs:

- see what happened;
- correct student/agenda/payment data;
- reverse wrong action if possible;
- notify affected person;
- prevent repeat.

Covered:

- B14 correction/audit;
- G7 history correction;
- F11 failures/webhooks;
- F9 audit;
- D10 reconciliation.

Partial or missing:

- cross-object rollback;
- customer-visible correction message;
- root-cause analysis after wrong automation.

Candidate missing flows:

- H24 Operational Correction And Recovery.
- H25 Automation Incident Review.

## Candidate Missing Flow Families

These are not final product decisions. They are candidate gaps discovered by simulating real manager work.

| Candidate | Flow | Why It May Matter |
| --- | --- | --- |
| H1 | Daily Opening Checklist | Manager needs a non-agent daily control routine. |
| H2 | Teacher Availability And Substitution | Teacher absence is common and impacts agenda. |
| H3 | Room/Equipment Availability And Maintenance | Pilates depends on rooms/apparatus capacity. |
| H4 | Staff Workload And Coverage | Owner needs to know if reception/teachers are overloaded. |
| H5 | New Student Operational Onboarding | Lead-to-student is not enough; first week has its own checklist. |
| H6 | Emergency Contact And Responsible Validation | Critical for safety and permissions. |
| H7 | First-Week Success Follow-Up | Reduces early churn after first purchase. |
| H8 | Health Intake Completion Gate | Student should not start certain routines without required intake. |
| H9 | Teacher Absence And Payroll Impact | Connects substitution and internal finance. |
| H10 | Equipment Safety Inspection | Safety/quality routine for apparatus-based studios. |
| H11 | Supplier/Maintenance Follow-Up | Repairs and vendors create operational tasks. |
| H12 | Accounts Payable And Studio Expenses | Current finance map focuses on student receivables. |
| H13 | Payroll/Commission Review | Teacher cost is central to studio economics. |
| H14 | Cashflow And Profitability Snapshot | Owner needs business health beyond money receivable. |
| H15 | Accountant Export / Fiscal Handoff | Month-end admin is real manager work. |
| H16 | Marketing Spend And Source ROI | Sales source exists, but spend/ROI does not. |
| H17 | Complaint Case Lifecycle | Complaints need lifecycle, owner, SLA and resolution. |
| H18 | Post-Resolution Satisfaction Check | Closing a complaint is not the same as recovering trust. |
| H19 | Policy Versioning And Effective Date | Rule changes need versioning and future dates. |
| H20 | Policy Change Impact Simulation | Manager should see who is affected before changing policy. |
| H21 | Policy Communication Rollout | Policy changes often require controlled communication. |
| H22 | Multi-Source Lead Capture | Leads may come from site, Instagram, referral, walk-in or manual entry. |
| H23 | Walk-In Lead Registration | Pilates studios still receive in-person leads. |
| H24 | Operational Correction And Recovery | Wrong data/action needs rollback or visible recovery. |
| H25 | Automation Incident Review | Autonomous mistakes need root-cause and prevention. |

## Are These New Agents?

Not necessarily.

Most candidate H flows should not become new "agents" immediately. They can be modeled as:

- CRM workflows;
- manager checklists;
- operation cases;
- tasks;
- approvals;
- reports;
- configuration/policy screens;
- later agent capabilities if usage proves frequent and automatable.

The current seven agents can still own many of them:

| Candidate Family | Likely Owner |
| --- | --- |
| Teacher/coverage | Agenda + Gestao |
| Equipment/maintenance | Gestao |
| Student onboarding | Agenda + Historico/Evolucao + Financeiro |
| Expenses/payroll/profit | Financeiro + Gestao |
| Complaints | Retencao + Atendimento + Gestao |
| Policy changes | Gestao + agent-specific flows |
| Multi-source leads | Vendas + Atendimento |
| Automation incident review | Gestao |

## Product Implication

If Taliya is sold as:

```text
agents that help with WhatsApp, agenda, sales, finance, retention and history
```

then the 91 flows may be close to enough for a first agent MVP.

If Taliya is sold as:

```text
a complete operational CRM for Pilates studios
```

then the 91 flows are not enough. They need a broader CRM/business-process layer around them.

## Recommended Reframing

Use three layers:

### Layer 1 - CRM Core

Contacts, students, leads, agenda, plans, payments, tasks, conversations, documents, history, roles, reports.

This layer must work in the Base plan with 0 agents.

### Layer 2 - Operational Workflows

Cases, checklists, approvals, policy changes, data quality, complaints, staff coverage, equipment/resource issues, month-end review.

Some workflows are manual-only in v1.

### Layer 3 - Agent Automation

The current 91 flows, plus future candidates promoted from Layer 2 when they prove repeated, rules-based and safe enough.

## Draft Conclusion

The right conclusion is:

```text
We have 91 validated agent-operation flows, not 91 final product use cases.
```

Before finalizing routes/screens or implementation scope, Taliya needs a second catalog:

```text
CRM/business workflow catalog from the studio manager perspective.
```

That catalog should decide which candidate H flows are:

- v1 required;
- v1 manual-only;
- v1 report/checklist only;
- later automation;
- out of scope.

## Suggested Next Document

Create:

```text
manager-workflow-catalog.md
```

with every manager workflow classified as:

- daily;
- weekly;
- monthly;
- event-driven;
- setup-only;
- compliance/safety;
- CRM-only;
- agent-assisted;
- autonomous candidate;
- out of scope.
