# Paused Draft - MVP Scope All-In Hypothesis

> Status: paused/superseded draft. This was created when "everything enters the MVP" sounded like a final decision. The later correction is that fluxos and use cases are still being mapped. Treat this file as a hypothesis, not a product decision.

## Decision

Paused. Not final.

Current corrected framing:

```text
Everything currently mapped is being considered for the MVP, but final scope is not decided yet.
```

For this project, MVP means:

```text
the first complete commercial product version for a Pilates studio manager
```

Not:

```text
the smallest experimental prototype
```

## Candidate For MVP Consideration

The candidate universe currently includes:

- CRM web;
- mobile app;
- Base plan operation with 0 active agents;
- 96 candidate AI-agent flows;
- the 2 optional agent-flow candidates if validated during detailed design;
- 132 cataloged manager use cases;
- 25 candidate gap use cases from the complete audit;
- 157 current candidate manager use cases total;
- manual, copilot and autonomous execution paths;
- contextual agent buttons/actions;
- assistant side panel/command bar;
- approval queue;
- operation cases;
- tasks;
- audit;
- quotas and economy mode;
- data quality;
- integrations and logs;
- incident review;
- policy/rule governance.

## Product Implication

The MVP is not a lightweight CRM.

It is:

```text
CRM operacional completo para studios de Pilates com agentes de IA integrados ao sistema.
```

Therefore, the route and screen map must cover:

- daily manager command center;
- inbox and conversations;
- contacts and responsible parties;
- students and history;
- agenda, class groups, attendance, make-ups, waitlist and capacity;
- sales, interested people, trials, referrals and source attribution;
- finance, payments, charges, contracts, student plan changes and exceptions;
- retention, complaints, cancellation and reactivation;
- operation cases, tasks, approvals and incidents;
- agents, flows, simulation and execution history;
- usage, quotas, cost origin and economy mode;
- integrations, import, data quality and audit;
- settings, policies, templates, channels and permissions;
- mobile app for daily work, approvals, inbox, agenda, students, notes and alerts.

## Delivery Interpretation

Even though everything enters MVP, it should still be delivered in implementation slices.

The slices are not "future product phases"; they are internal build order.

Recommended language:

| Term | Meaning |
| --- | --- |
| MVP Scope | Everything required before first real launch. |
| Build Slice | Internal delivery order inside the MVP. |
| Beta Gate | A temporary readiness milestone, not reduced scope. |
| Deferred | Only items explicitly removed from MVP by product decision. |

## Current MVP Scope Counts

| Artifact | Count | Included |
| --- | ---: | --- |
| AI-agent flows accepted/current | 96 | Yes |
| Optional agent-flow candidates | 2 | Validate; include if kept as standalone flows |
| Manager use cases cataloged | 132 | Yes |
| Manager use case audit gaps | 25 | Yes |
| Total manager use cases under execution matrix | 157 | Yes |

## Execution Rule

Every MVP use case must support at least one valid execution path:

```text
manual OR copilot OR autonomous
```

But critical CRM use cases should generally support manual first, because:

- Base plan has 0 active agents;
- managers must be able to override automation;
- safety/risk cases require human control;
- agents should enhance the CRM, not replace the CRM.

## Agent Rule

Agents act in both:

- WhatsApp;
- CRM web/app.

WhatsApp is only one channel.

The CRM web/app is where agents:

- observe;
- analyze;
- suggest;
- prepare;
- ask for approval;
- execute configured actions;
- log results;
- explain failures;
- consume quota;
- create tasks/cases;
- update records.

## UI Rule

Agent invocation must be embedded in the CRM:

- contextual smart buttons;
- assistant side panel;
- approval drawer;
- automatic triggers;
- bulk actions;
- flow simulation and run history.

Avoid treating agents as a separate chatbot pasted onto the product.

## Risk

This MVP scope is large.

The main risks are:

- route/screen sprawl;
- implementation taking too long before first customer feedback;
- inconsistent depth across modules;
- agent runtime complexity;
- permission and audit complexity;
- quota/cost surprises;
- mobile app becoming too broad too early.

## Mitigation

Keep everything in MVP scope, but define launch readiness by depth:

1. Every route exists and supports the core workflow.
2. Every use case has manual path.
3. Copilot exists for high-value/high-risk cases.
4. Autonomous mode is enabled only where gates, quota and audit are ready.
5. Heavy configuration stays web-first.
6. Mobile focuses on execution and approvals, not full administration.

## Required Follow-Up

Round 1 has now updated the route/screen map with the main accepted audit gaps and created a complete review artifact:

- `rodada-1-auditoria-completa.pt-BR.md`
- `rodada-2-classificacao-157.pt-BR.md`
- `routes-and-surfaces.md`
- `flow-coverage-matrix.md`
- `data-model.md`

Next artifact should be:

```text
rodada-2-classificacao-157.pt-BR.md
```

with all 157 candidate cases grouped as:

- accepted;
- merged;
- deferred;
- out;
- route depth;
- autonomy boundary;
- mobile depth.
