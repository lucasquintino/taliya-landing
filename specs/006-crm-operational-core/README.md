# Taliya CRM Operational Core

This spec package defines the real Taliya SaaS product used by a paying Pilates studio.

It complements the existing commercial funnel specs:

- Spec 1: public niche landing and plans page.
- Spec 2: sales AI attendant, WhatsApp sales channel and internal Sales Inbox.
- Spec 3: billing, subscriptions and entitlements.
- Spec 4: post-payment onboarding.
- Spec 5: security, code and data governance.

Spec 6 defines the operational CRM that makes the product useful even when the plan has zero active agents.

## Core Decision

Taliya is a vertical operational CRM for Pilates studios with integrated AI agents.

The Base plan is CRM-only: it must let the studio run contacts, students, agenda, sales, finance, tasks, history and reports without active AI automation.

Plans with agents add automation, copilot and autonomous execution on top of the same CRM records, rules, tasks and audit trail.

## Documents

- [spec.md](./spec.md): product goal, scope, requirements and acceptance criteria.
- [mvp-scope-all-in.md](./mvp-scope-all-in.md): paused all-in MVP hypothesis; final scope is not decided while mapping continues.
- [data-model.md](./data-model.md): core entities needed by CRM, agents, cases and quotas.
- [routes-and-surfaces.md](./routes-and-surfaces.md): web and mobile routes required to operate the product.
- [routes-use-cases-v2.md](./routes-use-cases-v2.md): revised route, screen and use-case map after the 96-flow agent audit.
- [use-cases.md](./use-cases.md): user scenarios from setup to daily operation.
- [manager-use-case-catalog.md](./manager-use-case-catalog.md): broad catalog of 132 manager-followable CRM journeys.
- [complete-manager-use-case-audit.md](./complete-manager-use-case-audit.md): full audit of manager use cases across manual, copilot and autonomous actions, including 25 candidate gaps.
- [agent-invocation-ux-matrix.md](./agent-invocation-ux-matrix.md): UX matrix for contextual buttons, assistant panel, approvals and automatic triggers that invoke agents inside CRM web/app and WhatsApp.
- [use-case-execution-mapping-audit.md](./use-case-execution-mapping-audit.md): audit showing that each use case still needs execution-path mapping: programmatic core, AI role, manual path, copilot path, autonomous path, gates and outputs.
- [use-case-execution-matrix.md](./use-case-execution-matrix.md): compact execution-path matrix for all 157 current candidate manager use cases.
- [visual-mapping-toolkit.md](./visual-mapping-toolkit.md): collection of visual lenses and diagram types for understanding flows, use cases, screens, buttons, modes, objects and decisions.
- [product-master-map.md](./product-master-map.md): compact source-of-truth table for all 157 current candidate manager use cases.
- [product-master-map.csv](./product-master-map.csv): filterable CSV version of the product master map.
- [product-master-map-v2.md](./product-master-map-v2.md): decision-oriented master table with priority, decision, route type, risk, mobile depth, WhatsApp and agent-flow references.
- [product-master-map-v2.csv](./product-master-map-v2.csv): filterable CSV version of the decision-oriented master table.
- [README.pt-BR.md](./README.pt-BR.md): Portuguese index for the mapping package.
- [product-master-map-v2.pt-BR.md](./product-master-map-v2.pt-BR.md): Portuguese decision-oriented master table.
- [product-master-map-v2.pt-BR.csv](./product-master-map-v2.pt-BR.csv): Portuguese filterable CSV version.
- [glossario-produto.pt-BR.md](./glossario-produto.pt-BR.md): Portuguese product-language glossary for replacing technical terms in stakeholder-facing docs.
- [multi-view-product-audit.pt-BR.md](./multi-view-product-audit.pt-BR.md): Portuguese consolidated audit summary.
- [screen-inventory-tree.pt-BR.md](./screen-inventory-tree.pt-BR.md): Portuguese screen inventory.
- [coverage-heatmap.pt-BR.md](./coverage-heatmap.pt-BR.md): Portuguese coverage heatmap.
- [decision-kanban.pt-BR.md](./decision-kanban.pt-BR.md): Portuguese decision kanban.
- [journey-metro-map.md](./journey-metro-map.md): journey-line diagrams for sales, agenda, finance, retention, history, runtime and daily manager loops.
- [object-action-map.md](./object-action-map.md): business objects mapped to actions, buttons and related use cases.
- [execution-swimlanes.md](./execution-swimlanes.md): representative human/system/AI/WhatsApp/audit execution blueprints.
- [screen-inventory-tree.md](./screen-inventory-tree.md): exploratory CRM web and mobile route/screen tree.
- [coverage-heatmap.md](./coverage-heatmap.md): coverage and risk heatmap by product area.
- [decision-kanban.md](./decision-kanban.md): text kanban for accepted candidates, details needed, merge review and out-of-scope items.
- [multi-view-product-audit.md](./multi-view-product-audit.md): consolidated audit across master table, journeys, objects, swimlanes, screens, heatmap, kanban, mobile, data and agent boundaries.
- [rodada-1-auditoria-completa.pt-BR.md](./rodada-1-auditoria-completa.pt-BR.md): first full Portuguese product-review round across documents, flows, use cases, screens, data, quotas and mobile scope.
- [rodada-2-classificacao-157.pt-BR.md](./rodada-2-classificacao-157.pt-BR.md): Portuguese classification pass for all 157 candidate use cases.
- [rodada-2-classificacao-157.pt-BR.csv](./rodada-2-classificacao-157.pt-BR.csv): filterable CSV for the 157-case classification pass.
- [rodada-3-fechamento-consistencia.pt-BR.md](./rodada-3-fechamento-consistencia.pt-BR.md): Portuguese consistency closure after route, object, count, autonomy and PT-BR checks.
- [product-depth-audit.pt-BR.md](./product-depth-audit.pt-BR.md): Portuguese product-depth audit across navigation, screens, data, automation, mobile and MVP depth.
- [product-depth-matrix.pt-BR.md](./product-depth-matrix.pt-BR.md): Portuguese 157-case depth matrix.
- [product-depth-matrix.pt-BR.csv](./product-depth-matrix.pt-BR.csv): filterable CSV for the product-depth matrix.
- [page-requirements.pt-BR.md](./page-requirements.pt-BR.md): concrete Portuguese page list with what each page must contain.
- [page-requirements.pt-BR.csv](./page-requirements.pt-BR.csv): filterable page requirements table.
- [page-case-coverage.pt-BR.csv](./page-case-coverage.pt-BR.csv): filterable mapping from all 157 use cases to owner pages.
- [reference-aligned-ui-audit.pt-BR.md](./reference-aligned-ui-audit.pt-BR.md): audit against the provided CRM journey dashboard references.
- [page-layout-zones.pt-BR.md](./page-layout-zones.pt-BR.md): exact Portuguese map of what belongs in each page zone.
- [page-layout-zones.pt-BR.csv](./page-layout-zones.pt-BR.csv): filterable version of the page zone map.
- [end-to-end-product-audit.pt-BR.md](./end-to-end-product-audit.pt-BR.md): end-to-end Portuguese audit from initial flows through product direction, pages, quotas and mobile.
- [web-screen-map.pt-BR.md](./web-screen-map.pt-BR.md): consolidated Portuguese map of CRM web menus, screens and route groups.
- [mobile-screen-map.pt-BR.md](./mobile-screen-map.pt-BR.md): consolidated Portuguese map of mobile app screens, depth and mobile-only decisions.
- [mobile-coverage-audit.pt-BR.md](./mobile-coverage-audit.pt-BR.md): mobile coverage audit across all 38 CRM surfaces.
- [screen-depth-readiness-audit.pt-BR.md](./screen-depth-readiness-audit.pt-BR.md): Portuguese audit of whether each web/mobile screen is deep enough for design and implementation.
- [web-mobile-review-simulation.pt-BR.md](./web-mobile-review-simulation.pt-BR.md): consolidated web/mobile page list plus end-to-end user simulation.
- [complete-specification-plan.pt-BR.md](./complete-specification-plan.pt-BR.md): concrete round-by-round plan to reach complete screen/route/use-case specification.
- [operating-modes.md](./operating-modes.md): manual, copilot and autonomous behavior.
- [flow-coverage-matrix.md](./flow-coverage-matrix.md): historical 91-flow coverage map plus the 5 strong additions and 2 optional standalone-flow candidates.
- [quotas-and-economy.md](./quotas-and-economy.md): quota, cost origin, economy mode and blocking rules.
- [implementation-slices.md](./implementation-slices.md): recommended build sequence.
- [manager-flow-gap-audit.md](./manager-flow-gap-audit.md): draft audit testing whether the 91 agent flows are enough from a studio manager perspective.
- [agent-flow-cardinality-audit.md](./agent-flow-cardinality-audit.md): draft audit focused only on whether the AI-agent flow catalog should remain 91 or change.
- [crm-with-agents-readiness-audit.md](./crm-with-agents-readiness-audit.md): draft audit evaluating whether the agent flows are enough to produce a CRM with integrated AI agents.

## Source Documents

Primary inputs:

- `docs/taliya-agent-flow-deep-map.md`
- `docs/taliya-agent-flow-validation-matrix.md`
- `docs/taliya-agent-flow-configuration-matrix.md`
- `docs/taliya-agent-flow-test-scenarios.md`
- `specs/001-niche-landing-system/spec.md`
- `specs/003-billing-subscriptions-entitlements/spec.md`
- `specs/004-saas-onboarding/spec.md`
- `specs/005-security-code-data/spec.md`

## Conflict Resolution

Some older landing and attendant documents say the product should not be called CRM.

For the real SaaS product, Spec 3 and Spec 4 confirm that Base is CRM-only. Therefore this package treats CRM as the product core and treats agents as an optional integrated automation layer.

Public copy can still avoid looking like a generic CRM by using the stronger category:

```text
CRM operacional para studios de Pilates com agentes de IA integrados.
```
