# Feature Specification: Taliya CRM Operational Core

**Feature Branch**: `codex/006-crm-operational-core`
**Created**: 2026-05-08
**Status**: Draft for product review

## Product Goal

After a studio pays and completes onboarding, Taliya must give the owner and team a usable operational CRM for running the studio day to day.

The CRM must work in the Base plan with zero active AI agents. When a plan includes agents, those agents operate on top of the same CRM records, cases, tasks, rules, permissions, quotas and audit events.

The product should answer the studio owner's daily questions:

- What needs attention today?
- Which conversations are open?
- Which interested people need follow-up?
- Which students missed class, need make-up, or are at risk?
- Which payments, plans, contracts or exceptions need action?
- Which tasks need the team or owner?
- Which automations are running, paused, blocked or waiting for approval?
- Which quotas are being consumed and why?

## Product Positioning

Taliya is not only a set of agents and not only WhatsApp automation.

Taliya is:

```text
A vertical operational CRM for Pilates studios, with AI agents integrated into the CRM.
```

The Base plan uses CRM features without active agent automation. Paid agent plans unlock one, three or seven active agents that can work in manual, copilot or autonomous mode according to entitlement and configuration.

## Scope

Included:

- tenant-scoped CRM workspace;
- contacts, students, interested people and responsible parties;
- inbox and conversation records;
- agenda, classes, attendance, make-up credits and waitlist;
- sales pipeline, trial classes, enrollment and losses;
- finance, payments, charges, contracts and financial exceptions;
- retention, risk, reactivation and cancellation work;
- history/evolution, notes, documents and permissions;
- operation cases, tasks, approvals, sends and flow executions;
- quota, usage, economy mode and hard-cap enforcement;
- agent configuration and flow simulation;
- audit trail and integration logs.

Excluded:

- public landing design;
- sales AI attendant implementation;
- billing provider checkout and webhook implementation;
- mobile native app implementation details;
- custom-agent delivery outside the seven mapped operational agents.

## User Roles

- **Owner**: pays for Taliya, manages settings, billing, users, quotas and sensitive decisions.
- **Admin**: manages CRM operations and configurations allowed by owner.
- **Reception/Operations**: handles inbox, agenda, sales, tasks and approved replies.
- **Finance**: handles payments, charges, contracts and financial exceptions.
- **Teacher**: sees class context, records observations and reads permitted student history.
- **Agent Runtime**: system actor that creates cases, tasks, approvals, sends and records.

## Core Concepts

### Operation Case

Every meaningful flow should create or update an operation case when it needs visibility, state, human decision, audit or quota tracking.

Examples:

- student asks for make-up class;
- payment is overdue;
- interested person wants trial class;
- teacher updates a sensitive restriction;
- WhatsApp send fails;
- automation is blocked by missing data.

### Task

A manual action assigned to a person or queue.

Manual mode always creates tasks instead of executing externally visible actions.

### Approval

A copilot decision checkpoint. The system prepares an action and waits for approval, edit or rejection.

### Flow Execution

One run of a mapped flow, whether it resolves, pauses, creates a task, requests approval, sends a message or transitions to another flow.

### Send

An external message attempt, usually WhatsApp, with provider result, template/cost class and retry state.

### Quota Event

A usage record for AI, WhatsApp, media processing, historical summarization, jobs or other metered work.

## Functional Requirements

- **FR-001**: The CRM MUST be tenant-scoped and require authenticated membership for all private routes.
- **FR-002**: The Base plan MUST allow CRM use with zero active AI agents.
- **FR-003**: Agent automation MUST be entitlement-gated and server-enforced.
- **FR-004**: Every flow execution MUST record tenant, flow, mode, status, origin, owner route and audit metadata.
- **FR-005**: Manual mode MUST create tasks and internal records, not send external messages automatically.
- **FR-006**: Copilot mode MUST create approvals before externally visible, costly or sensitive actions.
- **FR-007**: Autonomous mode MUST execute only inside configured limits, quotas, permissions, windows and guardrails.
- **FR-008**: Missing required data MUST create setup/data-quality tasks or ask for minimal safe data.
- **FR-009**: Sensitive health, financial, privacy, legal, reputation or conflicting-data cases MUST pause automation and require human handling.
- **FR-010**: All WhatsApp sends MUST use configured channels, windows, templates and opt-out state.
- **FR-011**: The system MUST expose an operational case detail page for all non-trivial cases.
- **FR-012**: The system MUST expose task and approval detail pages.
- **FR-013**: Attendance corrections, financial changes, permissions, history corrections, takeover, sends and entitlement-sensitive actions MUST be audited.
- **FR-014**: Quota usage MUST be tracked by flow, agent, channel, cost origin and tenant.
- **FR-015**: At 70%, 90% and 100% quota usage, the system MUST show alerts and adjust behavior according to economy rules.
- **FR-016**: At hard cap, paid automation MUST stop until upgrade or extra quota is active, while manual CRM work remains available.
- **FR-017**: Agent-locked flows MUST not pretend to run; they may create tasks and upsell context.
- **FR-018**: The mobile app MUST focus on daily operation, not full configuration.
- **FR-019**: The CRM MUST distinguish the studio's own operational inbox from the internal Taliya Sales Inbox.
- **FR-020**: The system MUST preserve cross-flow transitions so work does not duplicate or disappear.

## Acceptance Criteria

- **SC-001**: A Base-plan studio can manage contacts, students, agenda, sales, finance, tasks and history with no active agents.
- **SC-002**: A Base-plan flow request creates records/tasks instead of automated agent execution.
- **SC-003**: A 1-agent studio cannot enable unavailable agent flows.
- **SC-004**: A copilot flow creates an approval with enough context to approve, edit or reject.
- **SC-005**: An autonomous flow stops or downgrades when quota, data, opt-out, risk or permission blocks it.
- **SC-006**: Every strong candidate agent flow has a primary owner route and a case/task/approval path. The current working catalog is 96 strong candidate flows, with 2 optional standalone-flow candidates still under validation.
- **SC-007**: A user can open `/app/operacao` and see running, blocked, waiting and manual cases.
- **SC-008**: A user can open a student profile and see agenda, finance, retention, history and timeline context according to permissions.
- **SC-009**: A teacher can record post-class observation without seeing financial data.
- **SC-010**: A finance user can handle payment exceptions without seeing restricted health notes.
- **SC-011**: Quota and economy mode explain why an automation was paused or converted to task.
- **SC-012**: Audit logs show who/what changed sensitive data and why.

## Open Decisions

- Final CRM naming in public copy: "CRM operacional", "sistema operacional do studio" or both.
- Whether Base includes one user only or allows paid extra users before agent upgrade.
- Which payment provider is used for the studio's own student payments.
- Whether WhatsApp for Base is inbox-only or can include non-AI manual sends.
- Mobile app v1 scope: owner-only, team app, or teacher-first app.
- Whether E14 first-week new student and G13 intake/anamnesis gate remain use cases/gates or become standalone agent flows, which would move the catalog from 96 to 98.
- Which of the 157 candidate manager use cases are accepted, merged, deferred or explicitly out of scope.
