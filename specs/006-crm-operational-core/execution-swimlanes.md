# Execution Swimlanes - Human, System, AI, WhatsApp And Audit

> Status: exploratory. These blueprints show how representative use cases should execute across manual, copilot and autonomous paths.

## Pattern A - Contextual Button With Copilot

Use for:

- MUC-062 Recover open slot;
- MUC-073 Send Pix/payment link;
- MUC-094 Recover trust;
- MUC-118 Change policy.

```mermaid
sequenceDiagram
  participant H as Human
  participant S as Programmatic CRM
  participant AI as AI Assist
  participant AP as Approval
  participant A as Audit/Usage
  H->>S: Click contextual action
  S->>S: Validate data, permission, quota, risk
  S->>S: Compute deterministic candidates/impact
  S->>AI: Ask for draft/explanation
  AI-->>S: Draft or explanation
  S->>AP: Create approval proposal
  H->>AP: Approve, edit or reject
  AP->>S: Decision
  S->>A: Audit decision and usage
```

## Pattern B - Autonomous Low-Risk Reminder

Use for:

- MUC-042 Trial reminder;
- MUC-057 Presence confirmation;
- MUC-071 Due reminder;
- MUC-092 Satisfaction check.

```mermaid
sequenceDiagram
  participant Job as Scheduled Trigger
  participant S as Programmatic CRM
  participant AI as AI Assist
  participant W as WhatsApp
  participant A as Audit/Usage
  Job->>S: Time window reached
  S->>S: Check eligibility, consent, quota, window, idempotency
  S->>AI: Optional draft/personalization
  AI-->>S: Message variant
  S->>W: Send message if allowed
  W-->>S: Provider status
  S->>A: Log send, usage and result
```

## Pattern C - Manual-First Sensitive Case

Use for:

- MUC-079 Financial exception;
- MUC-089 Cancellation risk;
- MUC-097 Sensitive health/personal event;
- AUD-013 Refund/dispute.

```mermaid
sequenceDiagram
  participant Signal as Signal
  participant S as CRM
  participant AI as AI Assist
  participant H as Human Owner
  participant A as Audit
  Signal->>S: Event/message/user report
  S->>S: Open operation case
  S->>AI: Summarize context only
  AI-->>S: Safe summary
  S->>H: Assign task/case
  H->>S: Decide and record outcome
  S->>A: Audit action
```

## Pattern D - Inbound WhatsApp To CRM Flow

Use for:

- MUC-024 New WhatsApp conversation;
- MUC-025 Existing student request;
- MUC-040 Price/plan question;
- MUC-060 Make-up request.

```mermaid
sequenceDiagram
  participant W as WhatsApp
  participant S as CRM
  participant AI as AI Assist
  participant H as Human
  participant A as Audit/Usage
  W->>S: Inbound message
  S->>S: Find contact/student/conversation
  S->>AI: Classify intent and risk
  AI-->>S: Intent, confidence, suggested flow
  alt safe autonomous
    S->>W: Send configured response/action
  else copilot
    S->>H: Create approval/task
  else manual/handoff
    S->>H: Assign case and pause AI
  end
  S->>A: Log result
```

## Pattern E - Policy Change

Use for:

- MUC-013 Operational policies;
- MUC-118 Change operational rule/policy;
- AUD-001 Holidays/recess;
- AUD-009 Holiday/recess class impact.

```mermaid
sequenceDiagram
  participant H as Owner
  participant S as CRM
  participant AI as AI Assist
  participant AP as Approval
  participant A as Audit
  H->>S: Change policy/rule
  S->>S: Version rule and find impacted objects
  S->>AI: Explain impact and draft rollout
  AI-->>S: Impact summary
  S->>AP: Require confirmation
  H->>AP: Approve effective date
  S->>S: Schedule/apply policy
  S->>A: Audit before/after
```

## Pattern F - Automation Incident

Use for:

- MUC-117 Investigate automation incident;
- F14;
- bad data after a successful run.

```mermaid
sequenceDiagram
  participant Detect as Detection
  participant S as CRM
  participant AI as AI Assist
  participant H as Owner
  participant A as Audit
  Detect->>S: Bad outcome suspected
  S->>S: Link flow run, objects and messages
  S->>S: Pause affected flow if risky
  S->>AI: Summarize likely cause
  AI-->>S: Explanation and correction draft
  S->>H: Incident case
  H->>S: Correct data/action and close incident
  S->>A: Audit root cause and prevention
```

## Design Rule

Every use case should use one of these patterns or explicitly justify a new pattern.
