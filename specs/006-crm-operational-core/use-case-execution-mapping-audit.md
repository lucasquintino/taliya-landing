# Draft Audit - Are Use Case Execution Paths Fully Mapped?

> Status: exploratory draft. This audit was triggered by the "turma vaga -> Encontrar encaixe" example. It checks whether every manager use case is mapped not only by route and agent, but also by how the action is actually executed.

## Short Answer

No.

We have mapped:

- **96 candidate AI-agent flows**;
- **132 cataloged manager use cases**;
- **25 additional candidate manager gaps**;
- **157 total candidate manager use cases** under audit;
- routes and major surfaces;
- manual/copilot/autonomous concepts;
- agent invocation UX patterns.

But we have **not yet fully mapped every use case by execution path**.

The missing layer is:

```text
For each use case, what is programmatic, what uses AI, what the human can do manually, what can be copiloto, and what can become autonomous?
```

## Why This Matters

The "turma vaga" example proves the distinction:

The button **Encontrar encaixe** may involve the Agenda agent, but most of the useful work should be deterministic/programmatic:

- find open capacity;
- list make-up credits;
- check waitlist;
- filter by schedule preference;
- check restrictions;
- rank candidates;
- create invite/task/reservation records.

AI may help with:

- explaining why candidates were suggested;
- drafting a message;
- interpreting ambiguous replies;
- handling edge cases;
- summarizing the result.

The responsible person may still choose:

- solve manually;
- ask copiloto to prepare;
- allow autonomous execution.

This same pattern appears across hundreds of actions.

## New Required Dimension

Every use case needs an execution mapping with these fields:

| Field | Meaning |
| --- | --- |
| `primary_surface` | Where the user starts: route/screen/mobile/WhatsApp. |
| `business_object` | Student, class, payment, lead, conversation, case, policy, etc. |
| `trigger_type` | User click, system event, scheduled job, inbound message, integration event. |
| `invocation_type` | Contextual button, automatic trigger, assistant panel, approval, bulk action. |
| `deterministic_work` | Rules/data operations that should not require AI. |
| `ai_work` | Language, ambiguity, explanation, recommendation or summarization. |
| `manual_path` | How the human resolves it without active agent automation. |
| `copilot_path` | What the agent prepares and what requires approval. |
| `autonomous_path` | What can run alone, if configured and safe. |
| `gates` | Permissions, quota, opt-out, data quality, send window, risk, idempotency. |
| `outputs` | Record, task, case, approval, send, audit, flow run, usage ledger. |
| `fallback` | What happens when data/risk/quota/integration blocks execution. |

## Current Coverage Assessment

| Layer | Status | Notes |
| --- | --- | --- |
| Routes/screens | Mostly mapped | Good route map exists, but may need added routes from the 25 audit gaps. |
| Agent flow catalog | Mostly mapped | 96 candidates, 2 optional under validation. |
| Manager use cases | Strong baseline | 132 cataloged + 25 candidates = 157 working universe. |
| Manual/copilot/autonomous concepts | Mapped conceptually | Operating modes exist, but not per-use-case. |
| Agent invocation UX | Newly mapped | Contextual buttons, side panel, approvals and automatic triggers now defined. |
| Programmatic vs AI responsibility | Not fully mapped | Needs explicit classification per use case. |
| Human can resolve manually | Not fully mapped | Must be explicit because Base plan has 0 agents. |
| Buttons/actions per screen | Partially mapped | Invocation matrix maps route-level patterns, not every button per use case. |
| Autonomy gates per use case | Partially mapped | Global gates exist, but each use case needs local gates. |

## Product Rule

Every operational use case should be designed as:

```text
programmatic core
+ optional AI assistance
+ manual path
+ copilot path
+ autonomous path only when safe
```

Not:

```text
AI decides everything.
```

## Example: Turma Vaga / Encontrar Encaixe

| Field | Mapping |
| --- | --- |
| primary_surface | `/app/aulas/[id]`, `/app/agenda`, `/app/lista-espera`, mobile agenda |
| business_object | ClassSession, ClassGroup, MakeUpCredit, WaitlistEntry, Student |
| trigger_type | User click or automatic open-slot event |
| invocation_type | Contextual button: `Encontrar encaixe` |
| deterministic_work | Check capacity, credits, waitlist, preferences, restrictions, opt-out, attempts, cost |
| ai_work | Explain ranking, draft invitation, interpret ambiguous replies |
| manual_path | Show candidates; user chooses, contacts, records outcome |
| copilot_path | Agent suggests candidates/messages; user approves/edits/rejects |
| autonomous_path | Agent invites candidates by rule and reserves first accepted slot |
| gates | quota, WhatsApp permission, send window, opt-out, capacity, conflicts |
| outputs | invite send/task, reservation, audit, flow run, usage ledger |
| fallback | create task if no candidate, data missing, quota high or risk detected |

## Examples Of Other Cases Needing This Mapping

### Payment Overdue

Programmatic:

- identify overdue status;
- calculate days overdue;
- check previous attempts;
- check plan/policy;
- verify opt-out and channel eligibility.

AI:

- draft tone-sensitive message;
- explain why the case is risky;
- summarize payment history.

Manual:

- staff calls/messages manually and records result.

Copilot:

- agent prepares charge message and payment link, waits approval.

Autonomous:

- send configured low-risk reminder inside rules.

### Complaint Case

Programmatic:

- open case;
- assign SLA;
- pause automation;
- link conversation/student;
- track owner and status.

AI:

- summarize complaint;
- classify sentiment/severity;
- draft response;
- suggest recovery plan.

Manual:

- owner handles personally.

Copilot:

- agent prepares response/recovery steps.

Autonomous:

- only low-risk internal steps; not final resolution.

### Policy Change

Programmatic:

- version policy;
- compare old/new rule;
- find impacted students/classes/flows;
- schedule effective date.

AI:

- explain impact in plain language;
- draft rollout communication.

Manual:

- owner changes rule and communicates manually.

Copilot:

- system simulates and asks approval.

Autonomous:

- should be very limited; policy changes should not self-apply without owner approval.

## What Is Needed Next

Create a canonical matrix:

```text
use-case-execution-matrix.md
```

Recommended columns:

| Column | Example |
| --- | --- |
| ID | MUC-060 |
| Use case | Handle make-up request |
| Primary route | `/app/reposicoes` |
| Invocation | Button / inbound message / automatic |
| Deterministic core | validate credit and available slots |
| AI assist | draft options and interpret reply |
| Manual path | staff chooses slot and records |
| Copilot path | Taliya suggests and waits approval |
| Autonomous path | offer options if rules allow |
| Gates | quota, opt-out, capacity, restrictions |
| Outputs | reservation, message, audit, flow run |
| Priority | P0/P1/P2 |

## Scope Recommendation

Do not map all 157 in full prose first.

Use a spreadsheet-like matrix with compact rows:

1. Start with P0 use cases.
2. Add P1 safety-critical use cases.
3. Add remaining P1/P2.
4. Only then expand selected rows into detailed specs.

## Completeness Verdict

Current docs are enough to discuss product architecture.

They are **not yet enough** to implement every interaction safely, because each use case still needs execution mapping:

- button or trigger;
- programmatic core;
- AI role;
- manual path;
- copilot path;
- autonomous path;
- gates;
- outputs.

Until that matrix exists, we should not say:

```text
all cases are fully mapped
```

The accurate statement is:

```text
the product areas, routes, agent flows and manager use-case universe are mapped; detailed execution paths per use case are the next required artifact.
```
