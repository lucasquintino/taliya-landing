# Journey Metro Map - Taliya CRM

> Status: exploratory visual map. This document turns the master use cases into journey lines. It does not finalize scope.

## How To Read

- Lines = business journeys.
- Stations = use cases/screens.
- Transfers = handoff between modules/agents.
- Gates = approval, quota, permission, data quality or risk checks.

## Line 1 - Lead To Student

```mermaid
flowchart LR
  Capture["C15 / MUC-036 Capture lead"] --> Qualify["MUC-039 Qualify"]
  Qualify --> Price["C1 / MUC-040 Price and plans"]
  Qualify --> Trial["C2+B7 / MUC-041 Schedule trial"]
  Trial --> Reminder["C3 / MUC-042 Trial reminder"]
  Reminder --> TrialDone["C4 / MUC-044 Post-trial follow-up"]
  TrialDone --> Objection["C7 / MUC-046 Objection"]
  TrialDone --> PreEnroll["C6 / MUC-047 Pre-enrollment"]
  PreEnroll --> Convert["C13 / MUC-051 Convert to student"]
  Convert --> FirstClass["B15 / MUC-067 First class checklist"]
  FirstClass --> Retention["E14 candidate / AUD-017 First-week journey"]
```

## Line 2 - Agenda Operation

```mermaid
flowchart LR
  Grade["B11 / MUC-052 Grade"] --> Class["MUC-055 Class session"]
  Class --> Confirm["B1 / MUC-057 Confirm presence"]
  Class --> Attendance["B3+B14 / MUC-056 Attendance"]
  Attendance --> Absence["B2 / MUC-058 Absence with notice"]
  Attendance --> NoShow["B3 / MUC-059 No-show"]
  Absence --> Credit["B13 / MUC-061 Make-up credit"]
  Credit --> Makeup["B5 / MUC-060 Make-up request"]
  Class --> OpenSlot["B4 / MUC-062 Recover open slot"]
  OpenSlot --> Waitlist["B6 / MUC-063 Waitlist"]
  Class --> Cancel["B9 / MUC-065 Studio cancellation"]
  Grade --> Capacity["B10 / MUC-066 Capacity conflict"]
```

## Line 3 - Student Finance

```mermaid
flowchart LR
  Plan["MUC-069 Student plan"] --> Due["D1 / MUC-071 Due reminder"]
  Due --> Overdue["D2 / MUC-072 Overdue"]
  Overdue --> Link["D3 / MUC-073 Pix/payment link"]
  Link --> Confirm["D4 / MUC-074 Payment confirmed"]
  Link --> Failed["D7 / MUC-076 Failed payment"]
  Confirm --> Renewal["D5 / Renewal"]
  Overdue --> Exception["D6 / MUC-079 Financial exception"]
  Exception --> Agreement["AUD-011 Partial payment"]
  Plan --> Change["D15 / MUC-083 Effective plan change"]
  Change --> Contract["D11 / MUC-078 Contract/terms"]
  Plan --> Close["D14 / MUC-084 Monthly close"]
```

## Line 4 - Retention And Trust

```mermaid
flowchart LR
  Risk["E8/E12 / MUC-096 Risk segmentation"] --> Frequency["E1 / MUC-086 Frequency drop"]
  Risk --> Inactive["E2 / MUC-087 Inactive student"]
  Frequency --> Action["E3 / MUC-088 Return action"]
  Inactive --> Reactivation["E5 / MUC-091 Reactivation"]
  Action --> Pause["E7 / MUC-095 Return after pause"]
  Risk --> Cancel["E4 / MUC-089 Cancellation risk"]
  Cancel --> PostCancel["E9 / MUC-090 Post-cancellation"]
  Risk --> Satisfaction["E6 / MUC-092 Satisfaction"]
  Satisfaction --> Complaint["E13 / MUC-093 Complaint case"]
  Complaint --> Recovery["E13 / MUC-094 Recover trust"]
```

## Line 5 - Student History And Teacher Work

```mermaid
flowchart LR
  Context["G1 / MUC-098 Class context"] --> Class["Class happens"]
  Class --> Note["G2 / MUC-099 Post-class note"]
  Note --> Restriction["G3 / MUC-100 Restriction/care"]
  Note --> Goal["G4 / MUC-101 Objective/evolution"]
  Restriction --> Handoff["G8 / MUC-104 Teacher handoff"]
  Goal --> Review["AUD-019 Periodic review"]
  Documents["G6 / MUC-102 Documents/anamnesis"] --> Gate["G13 candidate / AUD-018 Intake gate"]
  Timeline["G12 / MUC-108 Timeline"] --> AgentContext["G5 Context for agents"]
```

## Line 6 - Agent Runtime And Governance

```mermaid
flowchart LR
  Configure["MUC-109/110 Configure agent"] --> Flow["MUC-111 Configure flow"]
  Flow --> Simulate["F13 / MUC-112 Simulate"]
  Simulate --> Activate["MUC-113 Activate/pause"]
  Activate --> Run["MUC-114 Flow execution"]
  Run --> Approval["MUC-115 Approval"]
  Run --> Usage["F7 / MUC-120 Usage/quota"]
  Run --> Incident["F14 / MUC-117 Automation incident"]
  Flow --> Policy["F15 / MUC-118 Policy change"]
  Policy --> SimImpact["AUD-009 Closure/policy impact"]
```

## Line 7 - Daily Manager Loop

```mermaid
flowchart LR
  Today["F1 / MUC-014 Today"] --> Queue["F3 / MUC-016 Human queue"]
  Today --> Tasks["MUC-017 Tasks"]
  Today --> Alerts["MUC-020 Alerts"]
  Today --> Money["F2 / MUC-015 Money on table"]
  Queue --> Delegate["MUC-018 Delegate"]
  Tasks --> Close["MUC-019 Close case"]
  Money --> Bottlenecks["F4 / MUC-021 Bottlenecks"]
  Today --> Data["F6 / MUC-023 Data blockers"]
  Today --> Weekly["F5 / MUC-022 Weekly summary"]
```

## Cross-Line Transfers

| From | To | Examples |
| --- | --- | --- |
| Sales | Agenda | Trial scheduling, no available slot, first class. |
| Agenda | Retention | No-show, frequency drop, many make-up credits. |
| Finance | Retention | Payment risk, pause, cancellation, dispute. |
| Inbox | Any module | WhatsApp message routes to owner flow. |
| History | Retention | Sensitive event or restriction affects churn risk. |
| Agent Runtime | Operations | Approval, incident, blocked data or quota limit. |
