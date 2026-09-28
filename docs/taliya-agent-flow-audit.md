# Taliya Agent Flow Audit

> Historical document. This audit is superseded by `docs/taliya-agent-flow-deep-map.md`, `docs/taliya-agent-flow-validation-matrix.md`, `docs/taliya-agent-flow-configuration-matrix.md` and `docs/taliya-agent-flow-test-scenarios.md`.
>
> Do not use this file as the operational source of truth for channels, configuration or implementation. It is kept only as the initial audit/history of decisions.

## Purpose

This document audited and mapped the initial MVP operational flows for Taliya, a Pilates studio operating system with seven AI agents.

Terminology note: this audit was created before the final channel language was locked. In this document, `app` means the internal Taliya system surface, whether accessed on web or mobile app. The final documents use `sistema` for that surface and `hibrido` for flows that combine WhatsApp with the system.

The product model is:

- Taliya centralizes the studio operation.
- The seven agents work on top of that system.
- Each agent has mapped product flows.
- Studios configure how agents behave inside those mapped flows, not the flow design from zero.
- Flows can happen on WhatsApp, inside the app, or across both.
- Flows can lead to terminal states, human handoff, app tasks, or another agent flow.

## Sources Audited

- `specs/001-niche-landing-system/autonomous-whatsapp-flows.md`
- `specs/001-niche-landing-system/spec.md`
- `specs/002-floating-ai-sales-agent/agent-roles.md`
- `specs/002-floating-ai-sales-agent/agent-role-details.md`
- `specs/004-saas-onboarding/spec.md`
- `specs/004-saas-onboarding/data-model.md`
- `docs/landing-agentes-pilates/source/05_Agentes_Mockups.md`
- `docs/landing-agentes-pilates/source/06_Dinheiro_na_Mesa_Calculadora.md`
- `data/landing/niches/pilates.ts`

## Audit Findings

### What Is Already Strong

- The seven primary agents are stable: Atendimento, Agenda, Vendas, Financeiro, Retencao, Gestao and Historico/Evolucao.
- Five WhatsApp-first autonomous flows are already detailed: Atendimento, Agenda, Vendas, Financeiro and Retencao.
- The landing already describes the core business pains: WhatsApp overload, faltas, reposicoes, mensalidades, planos vencendo, alunos inativos, interessados, gestao clarity and historico/evolucao.
- The onboarding spec confirms all seven agents must be configurable by studio when included by plan.
- The product has a clear safety posture: pause or hand off for sensitive data, medical/health content, discounts/refunds/exceptions, angry tone, low confidence and conflicting data.

### Gaps To Close For MVP Product Spec

- Gestao and Historico/Evolucao need first-class flow maps, not only panel/mockup descriptions.
- Flow ownership must be explicit when multiple agents are involved. Example: absence can start in Agenda and continue through Retencao and Atendimento.
- Channel ownership must be explicit: WhatsApp-only, app-only or hybrid.
- Flow-to-flow transitions need to be defined so agents do not duplicate work.
- Configuration must be described as behavior configuration inside mapped flows: tone, message style, automation level, limits, escalation and responsible person.
- Terminal states must be standardized across agents.

## Core Concepts

### Channels

| Channel | Meaning |
| --- | --- |
| `whatsapp` | Flow happens primarily through WhatsApp messages with student/interested person. |
| `app` | Flow happens inside Taliya workspace/panel/task/history without sending external messages by default. |
| `hybrid` | Flow uses both WhatsApp and the Taliya app, often with app state plus WhatsApp communication. |

### Flow Runtime Modes

This audit only references modes at a high level. The full explanation belongs to the "Modos de operacao" product topic.

| Mode | Short Meaning |
| --- | --- |
| `copilot` | Agent prepares context/action and waits for team approval. |
| `autonomous` | Agent acts alone inside configured limits. |
| `custom_limit` | Studio defines how far the automatic behavior can go before handoff. |

### Standard Terminal States

| State | Meaning |
| --- | --- |
| `resolved_auto` | Flow completed without team action. |
| `suggested_for_approval` | Agent prepared action and waits for approval. |
| `waiting_student` | Waiting for student/interested person response. |
| `waiting_team` | Waiting for a responsible person. |
| `human_handoff_required` | Human must take over before continuing. |
| `task_created` | Internal task/pending action created. |
| `record_updated` | System record/history/status updated. |
| `next_flow_started` | Another flow starts from this outcome. |
| `paused_by_opt_out` | Contact asked not to receive messages. |
| `blocked_by_guardrail` | Safety/unsupported/sensitive boundary blocked action. |
| `no_action_missing_data` | Required context was unavailable. |
| `closed_no_response` | Flow ended after configured no-response window. |

### Standard Escalation Reasons

- Health, pain, injury, restriction or medical advice.
- Discount, refund, exception, cancellation or negotiation.
- Angry, distressed or confused contact.
- Conflicting schedule, billing or CRM data.
- Contact asks for a human.
- Low confidence classification.
- Missing required data.
- Rule outside configured limit.
- WhatsApp opt-out.

## Configuration Model

### Studio Configuration

Studio configuration is the shared base all agents use:

- Units and location.
- Opening hours and attendance windows.
- Classes, schedules, teachers and capacity.
- Plans, prices, renewal windows and payment rules.
- Students, interested people, ex-students and statuses.
- Official channels and connected tools.
- Team roles and responsible people.
- General tone of voice.
- Consent and opt-out rules.
- Global escalation rules.

### Agent Flow Behavior Configuration

The studio does not design each flow from zero. Each agent has mapped flows. Configuration controls how the agent behaves inside each mapped flow:

- Enabled/disabled flow.
- Tone of voice.
- Message style and templates.
- Automation mode.
- How far automatic behavior can go.
- Allowed actions.
- Required approval points.
- Responsible person for handoff.
- Notification destination.
- Logging and history behavior.
- No-response timing.
- Edge-case limits.

## Flow Map By Agent

## 1. Atendimento

### Scope

Atendimento owns incoming conversation triage, common questions, routing, safe response preparation and handoff when the conversation needs a person or another agent.

### Flow A1: New Interested Person Triage

| Field | Detail |
| --- | --- |
| Channel | `whatsapp` or `hybrid` |
| Trigger | New message from unknown or interested contact. |
| Objective | Understand intent, answer basic questions and route toward trial class, plan info or human. |
| Uses | CRM contact, studio public info, plans, schedules, trial-class rules. |

Paths:

- Asked hours/availability -> start `Agenda B7: Trial Class Slot Search`.
- Asked price/plan -> start `Vendas C1: Price/Plan Interest`.
- Wants trial class -> start `Vendas C2: Trial Class Booking`.
- Existing student asking operational question -> route to Agenda, Financeiro, Retencao or Historico.
- Medical/sensitive question -> `human_handoff_required`.
- No clear intent -> ask one clarifying question.
- Opt-out -> `paused_by_opt_out`.

Terminal states:

- `next_flow_started`
- `waiting_student`
- `human_handoff_required`
- `blocked_by_guardrail`

### Flow A2: Common Question Answer

| Field | Detail |
| --- | --- |
| Channel | `whatsapp` |
| Trigger | Contact asks about address, hours, plans, trial class, class format or how studio works. |
| Objective | Answer from configured studio data only. |
| Uses | Studio profile, public plan data, FAQ, channel policy. |

Paths:

- Answer available in config -> send answer, offer next step.
- Answer missing -> create internal task or handoff.
- Question implies buying intent -> start Vendas flow.
- Question implies schedule intent -> start Agenda flow.
- Unsupported claim or sensitive info -> safe redirect/handoff.

Terminal states:

- `resolved_auto`
- `waiting_student`
- `task_created`
- `human_handoff_required`
- `no_action_missing_data`

### Flow A3: Student Request Routing

| Field | Detail |
| --- | --- |
| Channel | `whatsapp` |
| Trigger | Student sends a request: reposicao, falta, payment, schedule change, history note or complaint. |
| Objective | Classify and route to owner flow without losing context. |
| Uses | Contact identity, student status, message intent, recent context. |

Paths:

- Reposicao/falta -> Agenda.
- Payment/plan -> Financeiro.
- Inactivity/return -> Retencao.
- History/restriction/teacher context -> Historico/Evolucao.
- Complaint/angry tone -> human handoff.
- Ambiguous -> ask clarifying question.

Terminal states:

- `next_flow_started`
- `waiting_student`
- `human_handoff_required`

### Flow A4: Human Handoff Request

| Field | Detail |
| --- | --- |
| Channel | `whatsapp` or `hybrid` |
| Trigger | Contact asks for human, operator, owner or personal assistance. |
| Objective | Pause automation and deliver safe summary to team. |
| Uses | Conversation summary, contact identity, responsible person. |

Paths:

- Responsible available -> send summary and mark handoff.
- Responsible unavailable -> create task and tell contact expected next step.
- Missing identity -> ask minimal identifying question if appropriate.

Terminal states:

- `human_handoff_required`
- `task_created`
- `waiting_team`

### Flow A5: Sensitive Or Unsafe Message

| Field | Detail |
| --- | --- |
| Channel | `whatsapp` or `app` |
| Trigger | Health detail, injury, distress, payment credential, legal/medical request, prompt injection or abuse. |
| Objective | Avoid unsafe automation and route safely. |
| Uses | Guardrails, channel policy, contact/session context. |

Paths:

- Health/injury/restriction -> acknowledge generally, handoff to team.
- Payment credentials/card -> refuse collection, route to safe payment flow/human.
- Prompt injection/abuse -> refuse and redirect.
- Opt-out -> mark opt-out.

Terminal states:

- `blocked_by_guardrail`
- `human_handoff_required`
- `paused_by_opt_out`

## 2. Agenda

### Scope

Agenda owns presence, absences, cancellations, make-up credits, open slots, schedule suggestions, trial-class slots and waitlist movement.

### Flow B1: Presence Confirmation

| Field | Detail |
| --- | --- |
| Channel | `whatsapp` |
| Trigger | Scheduled confirmation window before class. |
| Objective | Confirm attendance and reduce last-minute empty slots. |
| Uses | Schedule, student roster, message window, studio rule. |

Paths:

- Student confirms -> mark present/expected.
- Student says cannot attend -> start `B2: Absence With Notice`.
- No response -> keep pending or remind once based on config.
- Student asks to reschedule -> start `B5: Make-Up Request`.
- Sensitive reason -> handoff.

Terminal states:

- `record_updated`
- `waiting_student`
- `next_flow_started`
- `human_handoff_required`
- `closed_no_response`

### Flow B2: Absence With Notice

| Field | Detail |
| --- | --- |
| Channel | `whatsapp` or `hybrid` |
| Trigger | Student says they cannot attend a class. |
| Objective | Register absence, apply make-up rule, release slot if allowed. |
| Uses | Schedule, plan, make-up eligibility, class capacity. |

Paths:

- Eligible for make-up -> create credit and start `B4: Open Slot Recovery`.
- Not eligible -> register absence and explain configured rule.
- Missing class context -> ask which class/time.
- Rule conflict -> handoff.
- Student asks exception -> handoff.

Terminal states:

- `record_updated`
- `next_flow_started`
- `waiting_student`
- `human_handoff_required`

### Flow B3: No-Show

| Field | Detail |
| --- | --- |
| Channel | `app` or `hybrid` |
| Trigger | Class ended and student did not attend without prior cancellation. |
| Objective | Register no-show and decide follow-up. |
| Uses | Attendance, plan rules, recent absence pattern. |

Paths:

- First/low-risk no-show -> send gentle follow-up or app task.
- Repeated no-show -> start `Retencao E1: Low Frequency Risk`.
- Make-up not allowed -> register status.
- Needs team review -> task/handoff.

Terminal states:

- `record_updated`
- `next_flow_started`
- `task_created`
- `waiting_student`

### Flow B4: Open Slot Recovery

| Field | Detail |
| --- | --- |
| Channel | `hybrid` |
| Trigger | Slot opened by cancellation/absence. |
| Objective | Fill slot with compatible student. |
| Uses | Open slot, make-up credits, waitlist, preferences, restrictions, teacher/class fit. |

Paths:

- Candidate found -> invite candidate on WhatsApp.
- Candidate accepts -> reserve slot and notify team.
- Candidate declines -> invite next candidate if limit allows.
- No candidate -> mark slot open in app.
- Special restrictions -> handoff.

Terminal states:

- `resolved_auto`
- `waiting_student`
- `record_updated`
- `human_handoff_required`
- `closed_no_response`

Transitions:

- Acceptance -> `record_updated`.
- No candidate -> `Gestao F1: Daily Priorities`.
- Repeated open slots -> `Gestao F4: Recurring Bottleneck`.

### Flow B5: Make-Up Request

| Field | Detail |
| --- | --- |
| Channel | `whatsapp` |
| Trigger | Student asks to schedule a make-up class. |
| Objective | Check credit/eligibility and offer compatible options. |
| Uses | Student credits, schedule, preferences, class capacity. |

Paths:

- Credit exists and options found -> offer options.
- Student chooses -> reserve make-up class.
- No credit -> explain rule or handoff.
- No compatible option -> create task/waitlist.
- Exception requested -> handoff.

Terminal states:

- `resolved_auto`
- `waiting_student`
- `task_created`
- `human_handoff_required`

### Flow B6: Waitlist To Slot

| Field | Detail |
| --- | --- |
| Channel | `hybrid` |
| Trigger | Slot opens in a class with waitlist. |
| Objective | Offer available slot to best waitlist candidate. |
| Uses | Waitlist, class fit, priority, student preferences. |

Paths:

- Candidate accepts -> reserve slot.
- Candidate declines/no response -> next candidate.
- No candidate -> open slot remains visible.
- Rule conflict -> handoff.

Terminal states:

- `resolved_auto`
- `waiting_student`
- `record_updated`
- `human_handoff_required`

### Flow B7: Trial Class Slot Search

| Field | Detail |
| --- | --- |
| Channel | `whatsapp` |
| Trigger | Interested person wants to try a class or asks for availability. |
| Objective | Offer compatible trial class options. |
| Uses | Trial rules, availability, plans, contact context. |

Paths:

- Options found -> offer two options.
- Option selected -> start `Vendas C2: Trial Class Booking`.
- No options -> create task or ask alternative window.
- Medical/restriction topic -> handoff.

Terminal states:

- `next_flow_started`
- `waiting_student`
- `task_created`
- `human_handoff_required`

## 3. Vendas

### Scope

Vendas owns interested-person progression from question to trial class, post-trial follow-up, plan interest, tentative schedule and subscription/enrollment handoff.

### Flow C1: Price Or Plan Interest

| Field | Detail |
| --- | --- |
| Channel | `whatsapp` or `hybrid` |
| Trigger | Interested person asks price, plans, packages or "how much". |
| Objective | Answer from configured plan info and move toward trial/subscription. |
| Uses | Public plan data, schedule preferences, CRM stage. |

Paths:

- Wants trial first -> start `B7: Trial Class Slot Search`.
- Wants to subscribe -> start `C6: Ready To Enroll`.
- Needs explanation -> answer and ask preference.
- Discount/negotiation -> handoff.

Terminal states:

- `waiting_student`
- `next_flow_started`
- `human_handoff_required`

### Flow C2: Trial Class Booking

| Field | Detail |
| --- | --- |
| Channel | `hybrid` |
| Trigger | Interested person chooses a trial class slot. |
| Objective | Book trial class and create interested-person record. |
| Uses | Contact, schedule, trial rules, source channel. |

Paths:

- Required info complete -> book and confirm.
- Missing name/contact -> ask minimal field.
- Slot no longer available -> offer alternatives.
- Restriction/special need -> handoff.

Terminal states:

- `resolved_auto`
- `record_updated`
- `waiting_student`
- `human_handoff_required`

Transitions:

- Trial booked -> later `C3: Trial Class Reminder`.

### Flow C3: Trial Class Reminder

| Field | Detail |
| --- | --- |
| Channel | `whatsapp` |
| Trigger | Trial class scheduled and reminder window arrives. |
| Objective | Confirm attendance and reduce no-show. |
| Uses | Trial booking, contact, attendance status. |

Paths:

- Confirms -> keep appointment.
- Needs reschedule -> return to `B7: Trial Class Slot Search`.
- No response -> optional reminder/task.
- Cancels -> mark lost/reschedule opportunity.

Terminal states:

- `record_updated`
- `waiting_student`
- `next_flow_started`
- `closed_no_response`

### Flow C4: Trial Completed Follow-Up

| Field | Detail |
| --- | --- |
| Channel | `whatsapp` |
| Trigger | Trial class marked completed. |
| Objective | Continue conversation while interest is warm. |
| Uses | Trial class, teacher note, plan options, schedule availability. |

Paths:

- Interested asks plans -> `C1`.
- Wants fixed schedule -> `C6`.
- Has objection -> answer or handoff if commercial exception.
- No response -> `C5: No Response After Trial`.

Terminal states:

- `waiting_student`
- `next_flow_started`
- `human_handoff_required`
- `closed_no_response`

### Flow C5: No Response After Trial Or Price

| Field | Detail |
| --- | --- |
| Channel | `whatsapp` or `app` |
| Trigger | Interested person stops responding after price/trial. |
| Objective | Send limited follow-up or create team task. |
| Uses | CRM stage, last message, no-response window, opt-out. |

Paths:

- Follow-up allowed -> send message.
- Responds -> route by intent.
- Still no response -> close or create task.
- Opt-out -> pause.

Terminal states:

- `waiting_student`
- `closed_no_response`
- `task_created`
- `paused_by_opt_out`

### Flow C6: Ready To Enroll

| Field | Detail |
| --- | --- |
| Channel | `hybrid` |
| Trigger | Interested person indicates readiness to enroll/subscribe. |
| Objective | Prepare enrollment/subscription handoff safely. |
| Uses | Plan selection, schedule, contact info, billing destination. |

Paths:

- Direct online subscription available -> route to configured checkout/plan destination.
- Studio finalizes manually -> create pre-enrollment and human task.
- Missing data -> ask minimal fields.
- Financial exception -> handoff.

Terminal states:

- `next_flow_started`
- `task_created`
- `human_handoff_required`
- `record_updated`

## 4. Financeiro

### Scope

Financeiro owns payment reminders, overdue follow-up, renewal reminders, payment confirmation status and financial exceptions.

### Flow D1: Upcoming Payment Reminder

| Field | Detail |
| --- | --- |
| Channel | `whatsapp` |
| Trigger | Monthly fee due soon according to studio rule. |
| Objective | Remind before payment becomes overdue. |
| Uses | Plan, due date, payment status, message rule. |

Paths:

- Student pays -> `D4: Payment Confirmation`.
- Student asks payment link/Pix -> `D3: Payment Link Or Pix`.
- Student asks exception -> handoff.
- No response -> wait or later `D2`.

Terminal states:

- `waiting_student`
- `next_flow_started`
- `human_handoff_required`
- `closed_no_response`

### Flow D2: Overdue Payment

| Field | Detail |
| --- | --- |
| Channel | `whatsapp` or `app` |
| Trigger | Payment overdue inside configured reminder window. |
| Objective | Send cordial reminder or alert team. |
| Uses | Due date, overdue days, contact status, previous reminders. |

Paths:

- Within automatic limit -> send reminder.
- Past custom limit -> team approval/handoff.
- Student pays -> `D4`.
- Student disputes/asks discount/refund -> handoff.
- No response after max attempts -> task for team.

Terminal states:

- `waiting_student`
- `suggested_for_approval`
- `task_created`
- `human_handoff_required`
- `closed_no_response`

### Flow D3: Payment Link Or Pix

| Field | Detail |
| --- | --- |
| Channel | `whatsapp` |
| Trigger | Student requests Pix/link or reminder rule sends configured payment destination. |
| Objective | Send safe configured payment info only. |
| Uses | Billing provider/configured payment link, student plan. |

Paths:

- Link exists -> send.
- Link missing -> create task/handoff.
- Student sends proof -> record proof pending or `D4`.
- Payment credentials/card sent -> refuse and redirect safely.

Terminal states:

- `resolved_auto`
- `task_created`
- `waiting_team`
- `blocked_by_guardrail`

### Flow D4: Payment Confirmation

| Field | Detail |
| --- | --- |
| Channel | `app` or `hybrid` |
| Trigger | Billing confirms payment or team marks payment received. |
| Objective | Update plan/payment status and notify student/team if needed. |
| Uses | Billing status, plan, renewal rules. |

Paths:

- Payment confirmed -> update status, optionally notify student.
- Proof received but not confirmed -> task for financial review.
- Mismatch/conflict -> handoff.
- Renewal needed -> `D5: Plan Renewal`.

Terminal states:

- `record_updated`
- `task_created`
- `human_handoff_required`
- `next_flow_started`

### Flow D5: Plan Renewal

| Field | Detail |
| --- | --- |
| Channel | `hybrid` |
| Trigger | Plan expires soon or payment confirmed for next cycle. |
| Objective | Renew/maintain plan and schedule continuity. |
| Uses | Plan, due date, payment, schedule, retention signals. |

Paths:

- Student wants same plan/schedule -> renew/update.
- Wants change -> task/handoff or sales/agenda flow.
- Payment missing -> D1/D2.
- Cancellation/pause/trancamento -> D6.

Terminal states:

- `resolved_auto`
- `record_updated`
- `next_flow_started`
- `human_handoff_required`

### Flow D6: Pause, Trancamento, Refund Or Exception

| Field | Detail |
| --- | --- |
| Channel | `whatsapp` or `app` |
| Trigger | Student asks pause, cancellation, refund, discount or exception. |
| Objective | Stop automatic financial handling and route safely. |
| Uses | Plan, student history, policy, responsible person. |

Paths:

- Policy answer allowed -> explain and create task.
- Any negotiation/refund/cancel decision -> human handoff.
- Retention risk detected -> start `Retencao E4: Cancellation Risk`.

Terminal states:

- `human_handoff_required`
- `task_created`
- `next_flow_started`

## 5. Retencao

### Scope

Retencao owns student inactivity, frequency drops, return paths, cancellation-risk signals and care-oriented reactivation.

### Flow E1: Low Frequency Risk

| Field | Detail |
| --- | --- |
| Channel | `app` or `hybrid` |
| Trigger | Frequency drops compared with expected pattern. |
| Objective | Detect risk early and choose next action. |
| Uses | Attendance, plan, historic schedule, recent messages. |

Paths:

- Low-risk -> create app priority or soft WhatsApp check-in.
- Repeated absences -> `E2: Inactive Student Check-In`.
- Payment/plan issue -> Financeiro.
- Health/sensitive context -> handoff.

Terminal states:

- `task_created`
- `waiting_student`
- `next_flow_started`
- `human_handoff_required`

### Flow E2: Inactive Student Check-In

| Field | Detail |
| --- | --- |
| Channel | `whatsapp` |
| Trigger | Student has not attended for configured days. |
| Objective | Start warm low-pressure reactivation. |
| Uses | Last attendance, preferred times, teacher, restrictions if any. |

Paths:

- Student wants return -> `E3: Return Class Booking`.
- Student says busy -> schedule gentle follow-up or close.
- Student mentions pain/health/personal issue -> handoff.
- No response -> close after limit or create task.

Terminal states:

- `next_flow_started`
- `waiting_student`
- `human_handoff_required`
- `closed_no_response`

### Flow E3: Return Class Booking

| Field | Detail |
| --- | --- |
| Channel | `hybrid` |
| Trigger | Inactive/low-frequency student agrees to return. |
| Objective | Offer low-friction return option. |
| Uses | Schedule, preferred times, class fit, teacher context. |

Paths:

- Compatible option found -> offer and reserve.
- No compatible option -> task/waitlist.
- Student needs adaptation -> Historico/Evolucao or human.
- Return booked -> notify teacher/team.

Terminal states:

- `resolved_auto`
- `record_updated`
- `task_created`
- `human_handoff_required`

### Flow E4: Cancellation Risk

| Field | Detail |
| --- | --- |
| Channel | `whatsapp` or `app` |
| Trigger | Student asks to cancel, pause or shows dissatisfaction. |
| Objective | Route to human with context, not automate persuasion blindly. |
| Uses | Attendance, plan, messages, reason if provided. |

Paths:

- Direct cancellation/refund/pause -> handoff.
- Dissatisfaction but open to conversation -> create high-priority task.
- Schedule friction -> Agenda flow.
- Financial reason -> Financeiro flow.

Terminal states:

- `human_handoff_required`
- `task_created`
- `next_flow_started`

### Flow E5: Student Recovered

| Field | Detail |
| --- | --- |
| Channel | `app` |
| Trigger | Student attends return class or resumes pattern. |
| Objective | Close retention loop and update status. |
| Uses | Attendance, previous risk status, teacher note. |

Paths:

- Returned successfully -> mark recovered.
- Returned with restrictions/context -> Historico/Evolucao.
- Still inconsistent -> keep monitoring.

Terminal states:

- `record_updated`
- `next_flow_started`
- `task_created`

## 6. Gestao

### Scope

Gestao owns app-first operational visibility: priorities, money on the table, bottlenecks, weekly digest, unresolved exceptions and recommendations.

### Flow F1: Daily Priorities

| Field | Detail |
| --- | --- |
| Channel | `app` |
| Trigger | Start of day or owner opens dashboard. |
| Objective | Show what needs action first today. |
| Uses | All agent statuses, schedule, billing, retention, sales, pending handoffs. |

Paths:

- High urgency item -> show priority and link to source flow.
- Action can be delegated -> create task or agent suggestion.
- No urgent item -> show healthy state.
- Missing data -> setup checklist.

Terminal states:

- `task_created`
- `record_updated`
- `no_action_missing_data`

Transitions:

- Open slot -> Agenda B4.
- Inactive student -> Retencao E2.
- Overdue payment -> Financeiro D2.
- Interested warm -> Vendas C4/C5.

### Flow F2: Dinheiro Na Mesa Summary

| Field | Detail |
| --- | --- |
| Channel | `app` |
| Trigger | Calculator/panel update, owner opens money view, weekly summary. |
| Objective | Estimate operational opportunity by agent/pain. |
| Uses | Absences, open slots, overdue payments, expiring plans, inactive students, trial conversion, manual hours. |

Paths:

- Biggest gap is agenda -> link Agenda flows.
- Biggest gap is finance -> link Financeiro flows.
- Biggest gap is retention -> link Retencao flows.
- Insufficient data -> ask setup/data import.

Terminal states:

- `record_updated`
- `next_flow_started`
- `no_action_missing_data`

### Flow F3: Weekly Digest

| Field | Detail |
| --- | --- |
| Channel | `app` or `whatsapp` internal notification |
| Trigger | Weekly scheduled summary. |
| Objective | Summarize what agents resolved and what needs owner decision. |
| Uses | Flow logs, metrics, pending tasks, recovered money estimate. |

Paths:

- Send internal summary to owner.
- Highlight pending approvals.
- Recommend configuration adjustment.
- Missing metrics -> setup prompt.

Terminal states:

- `resolved_auto`
- `task_created`
- `no_action_missing_data`

### Flow F4: Recurring Bottleneck Detection

| Field | Detail |
| --- | --- |
| Channel | `app` |
| Trigger | Repeated pattern across flows: same open slot, repeated no-shows, recurring overdue, repeated no-response. |
| Objective | Detect systemic issue and suggest operational adjustment. |
| Uses | Historical flow outcomes and metrics. |

Paths:

- Suggest rule/config adjustment.
- Create owner task.
- Link to affected agent flows.
- If outside product map -> custom-agent request.

Terminal states:

- `suggested_for_approval`
- `task_created`
- `next_flow_started`

### Flow F5: Human Queue And Exceptions

| Field | Detail |
| --- | --- |
| Channel | `app` |
| Trigger | Any flow creates human handoff or pending approval. |
| Objective | Keep human work visible and prioritized. |
| Uses | Handoffs from all agents. |

Paths:

- Owner approves -> resume source flow where allowed.
- Owner edits -> send/update and record.
- Owner rejects -> close with reason.
- Owner assigns -> waiting responsible.

Terminal states:

- `record_updated`
- `waiting_team`
- `next_flow_started`
- `closed_no_response`

## 7. Historico/Evolucao

### Scope

Historico/Evolucao owns student context: profile, goals, restrictions, observations, attendance pattern, teacher notes and useful summaries before/after class. It must avoid medical advice.

### Flow G1: Pre-Class Context Summary

| Field | Detail |
| --- | --- |
| Channel | `app` |
| Trigger | Teacher opens class view or scheduled pre-class preparation. |
| Objective | Show useful context before class. |
| Uses | Student history, restrictions, goals, last notes, attendance. |

Paths:

- Context complete -> show summary.
- Restriction/sensitive note exists -> highlight for teacher, no external message.
- Missing history -> prompt teacher to add note.
- Medical/clinical interpretation requested -> block/redirect.

Terminal states:

- `record_updated`
- `task_created`
- `blocked_by_guardrail`

### Flow G2: Post-Class Observation

| Field | Detail |
| --- | --- |
| Channel | `app` |
| Trigger | Class ends or teacher adds note. |
| Objective | Capture observation and update student history. |
| Uses | Teacher note, class, student profile, goals. |

Paths:

- Note saved -> update history.
- Note implies restriction/care -> flag for teacher/owner.
- Note suggests attendance risk -> Retencao.
- Missing detail -> ask teacher optional prompt.

Terminal states:

- `record_updated`
- `task_created`
- `next_flow_started`

### Flow G3: Restriction Or Important Context Updated

| Field | Detail |
| --- | --- |
| Channel | `app` |
| Trigger | Teacher/team updates restriction, preference or important observation. |
| Objective | Keep context visible to the right people. |
| Uses | Student profile, permission rules, class schedule. |

Paths:

- Save and surface before next class.
- Notify assigned teacher internally.
- If contact with student needed -> Atendimento handoff.
- If medical advice requested -> block/handoff.

Terminal states:

- `record_updated`
- `task_created`
- `blocked_by_guardrail`
- `next_flow_started`

### Flow G4: Goal Review

| Field | Detail |
| --- | --- |
| Channel | `app` |
| Trigger | Goal review interval or teacher update. |
| Objective | Keep student objective current and useful for classes. |
| Uses | Goals, attendance, teacher observations. |

Paths:

- Goal updated -> history updated.
- Goal stale -> teacher task.
- Goal ties to retention risk -> Retencao.

Terminal states:

- `record_updated`
- `task_created`
- `next_flow_started`

### Flow G5: History-Informed Response

| Field | Detail |
| --- | --- |
| Channel | `hybrid` |
| Trigger | Atendimento or another agent needs context to answer a student safely. |
| Objective | Provide safe context, not medical advice. |
| Uses | Student history and permissions. |

Paths:

- Safe context available -> return summary to source agent.
- Sensitive context -> source agent hands off.
- Missing history -> source agent asks or creates task.

Terminal states:

- `next_flow_started`
- `human_handoff_required`
- `no_action_missing_data`

## Cross-Agent Transition Matrix

| From | Condition | To |
| --- | --- | --- |
| Atendimento | Interested asks for trial/class availability | Agenda B7 / Vendas C2 |
| Atendimento | Student asks reposicao/falta | Agenda B2/B5 |
| Atendimento | Student asks payment/plan status | Financeiro D1-D6 |
| Atendimento | Message suggests inactivity/return | Retencao E2/E3 |
| Atendimento | Needs student context | Historico G5 |
| Agenda | Repeated absences/no-shows | Retencao E1 |
| Agenda | Open slot not filled | Gestao F1/F4 |
| Agenda | Trial slot selected | Vendas C2 |
| Vendas | Interested ready to enroll | Financeiro/onboarding/checkout handoff |
| Vendas | Trial no-show | Retencao-style soft recovery or Vendas C5 |
| Financeiro | Cancellation/pause/trancamento | Retencao E4 |
| Financeiro | Plan renewed | Agenda schedule continuity / Gestao summary |
| Retencao | Student returns | Agenda E3/B scheduling and Historico G2 |
| Retencao | Health/personal issue | Human handoff / Historico internal note |
| Gestao | Priority selected by owner | Source agent flow |
| Historico | Context indicates retention risk | Retencao E1/E2 |
| Historico | Context needed for response | Atendimento A3/A5 |

## MVP Completeness Check

| Agent | WhatsApp Flows | App Flows | Hybrid Flows | MVP Risk |
| --- | ---: | ---: | ---: | --- |
| Atendimento | Yes | Limited | Yes | Needs strong routing and safety classification. |
| Agenda | Yes | Yes | Yes | Needs reliable schedule/make-up data. |
| Vendas | Yes | Limited | Yes | Needs clean CRM stages and checkout/handoff boundary. |
| Financeiro | Yes | Yes | Yes | Needs strict payment safety and billing truth source. |
| Retencao | Yes | Yes | Yes | Needs careful tone and health/sensitive handoff. |
| Gestao | Internal only | Yes | Optional | Needs metrics and priority model. |
| Historico/Evolucao | Limited | Yes | Yes | Needs safety boundary around health/clinical claims. |

## Product Decisions Needed

1. Which external tools are real in MVP: WhatsApp only, or WhatsApp plus calendar/billing/CRM storage?
2. Is online checkout the final enrollment path, or does studio human finalize enrollment after pre-enrollment?
3. Which flows can be autonomous on day one versus copiloto by default?
4. Which flow outcomes create internal tasks, and where do these tasks live?
5. What is the source of truth for schedule, class capacity, plans and payments?
6. What data import/setup is required before each flow can be enabled?
7. How does the owner see and change behavior configuration per flow?

## Recommended Next Document

After this audit is approved, create a product spec for:

`specs/005-operational-agent-flows/`

Suggested artifacts:

- `spec.md`: user stories and requirements for MVP agent flows.
- `agent-flow-map.md`: this audit refined into source of truth.
- `data-model.md`: tenants, studio config, flow configs, flow runs, tasks, handoffs, logs.
- `contracts/flow-runtime.md`: flow state machine and channel contract.
- `eval-plan.md`: flow classification, transition and safety fixtures.
