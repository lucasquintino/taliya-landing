# Operating Modes

Every flow can run in one of three modes when allowed by entitlement, risk and configuration.

## Manual

Manual mode means:

- Taliya organizes the case;
- Taliya records context;
- Taliya creates a task;
- the team executes the action.

Manual mode is required for:

- Base plan active work;
- health/clinical decisions;
- discounts, refunds, courtesies and blocks;
- high-risk privacy requests;
- financial exceptions;
- unclear or conflicting data;
- any flow where automation is disabled.

Manual lifecycle:

```text
signal
  -> operation case
  -> task
  -> user action
  -> record update
  -> audit
  -> resolved or next flow
```

Required routes:

- `/app/operacao/[caseId]`
- `/app/tarefas/[taskId]`
- object route such as student, class, payment or conversation
- `/app/auditoria/[eventId]` for sensitive actions

## Copilot

Copilot mode means:

- Taliya reads the context;
- Taliya prepares an action or message;
- Taliya waits for approval;
- a human approves, edits or rejects;
- only then does the system execute.

Copilot is required or recommended for:

- campaigns and batches;
- schedule changes that affect several students;
- financial reminders with risk;
- plan changes;
- history sharing;
- setup or configuration changes;
- low-confidence action proposals.

Copilot lifecycle:

```text
signal
  -> operation case
  -> flow execution
  -> proposed action
  -> approval
  -> approved/edited/rejected
  -> send or record update
  -> audit
  -> resolved or next flow
```

Required routes:

- `/app/fluxos/execucoes/[runId]`
- `/app/aprovacoes/[approvalId]`
- `/app/envios/[sendId]` when external message is sent
- object route
- audit route

## Autonomous

Autonomous mode means:

- Taliya executes inside the configured limits;
- Taliya checks data, permission, quota, opt-out, send window and risk;
- Taliya stops or downgrades when a gate fails.

Autonomous mode can be used for:

- simple public answers;
- classification and routing;
- presence confirmation;
- rule-clear make-up requests;
- configured Pix/link sends;
- low-risk reminders;
- internal summaries;
- routine logging.

Autonomous lifecycle:

```text
trigger
  -> preflight gates
  -> quota check
  -> flow execution
  -> action/send/update
  -> result
  -> audit/usage
  -> resolved or next flow
```

Autonomous downgrade paths:

| Blocker | Result |
| --- | --- |
| Missing data | setup/data-quality task |
| Sensitive risk | human task or approval |
| Low confidence | ask once or handoff |
| Opt-out | pause external messaging |
| Quota 90% | low-priority flow becomes copilot/task |
| Quota 100% | paid automation stops |
| Agent unavailable | task plus upsell context |
| Integration failure | retry-safe case and integration log |

## Mode By Plan

| Plan | Behavior |
| --- | --- |
| Base | CRM only. Flows may create records and tasks, but active agent automation is disabled. |
| 1 Agente | Selected agent can run allowed flows; dependent unavailable flows become tasks or upsell context. |
| 3 Agentes | Three selected agents can run; cross-agent transitions to blocked agents become tasks. |
| 7 Agentes | All primary agents can run, with sensitive flows still manual/copilot. |

## Required Gate Checks

Every flow run must check:

- tenant and entitlement;
- flow enabled state;
- operation mode;
- required data;
- contact consent and opt-out;
- send window;
- WhatsApp template/category when needed;
- quota and economy mode;
- user/agent permissions;
- risk/handoff rules;
- idempotency key;
- destination route for result.

## Standard Statuses

Operation case:

- open
- running
- waiting_contact
- waiting_team
- pending_approval
- blocked
- paused
- resolved
- canceled

Flow execution:

- started
- waiting_data
- pending_approval
- sent
- transitioned
- resolved
- blocked
- failed
- paused

Task:

- open
- in_progress
- done
- canceled

Approval:

- pending
- approved
- edited
- rejected
- expired

Send:

- queued
- sent
- delivered
- failed
- skipped
