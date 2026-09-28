# Routes And Product Surfaces

## Product Surfaces

Taliya operates on three surfaces:

1. Public web: landing, plans, checkout entry and privacy.
2. CRM web: full studio operation and configuration.
3. Mobile app: daily work, notifications, inbox, agenda, tasks and approvals.

The existing internal Sales Inbox is not the paying-studio CRM inbox. It is only for Taliya's own SaaS sales leads.

## Public Web

| Route | Purpose |
| --- | --- |
| `/` | Redirect or future home. |
| `/pilates` | Public Pilates landing. |
| `/pilates/planos` | Public plan comparison. |
| `/pilates/demonstracao` | Real guided demo when SaaS demo is ready. |
| `/privacidade` | Privacy notice. |
| `/checkout` or `/checkout/[planId]` | Server-side checkout entry. |
| `/assinatura/confirmando` | Waiting for trusted payment confirmation. |
| `/assinatura/falha` | Payment not confirmed or failed. |

## Internal Taliya Operator

| Route | Purpose |
| --- | --- |
| `/internal` | Taliya internal operating console. |
| `/internal/leads` | Taliya commercial lead control. |
| `/internal/leads/[leadId]` | Commercial lead detail. |
| `/internal/sales-inbox` | Legacy/alias surface for Taliya commercial leads. |
| `/internal/sales-inbox/[leadId]` | Legacy/alias commercial lead detail. |
| `/internal/commercial-metrics` | Funnel and operator metrics. |
| `/internal/tenants` | Customer studios, trials, active accounts, blocked accounts and cancelled accounts. |
| `/internal/tenants/[tenantId]` | 360 view of a customer studio. |
| `/internal/tenants/[tenantId]/users` | Tenant users, invites, roles and access status. |
| `/internal/tenants/[tenantId]/entitlements` | Plan, agent slots, quotas, add-ons and limits. |
| `/internal/support` | Internal Taliya queue for tickets opened by studios in `/app/suporte`. |
| `/internal/support/tickets/[ticketId]` | Internal ticket detail. |
| `/internal/support/grants` | Support access grants requested, active, expired, denied or revoked. |
| `/internal/support/grants/[grantId]` | Support grant detail and usage audit. |
| `/internal/incidents` | Taliya platform incidents. |
| `/internal/incidents/[incidentId]` | Incident detail, impact, cause, mitigation and postmortem. |
| `/internal/billing` | Taliya subscriptions, invoices, add-ons and entitlement operations. |
| `/internal/billing/[accountId]` | Billing detail for a customer studio. |
| `/internal/users` | Taliya internal users and permissions. |
| `/internal/audit` | Internal audit events. |
| `/internal/audit/[eventId]` | Internal audit event detail. |

## CRM Web: Core Routes

| Route | Purpose |
| --- | --- |
| `/login` | Magic link or OTP login. |
| `/onboarding/claim/[activationId]` | Claim paid workspace after billing confirmation. |
| `/onboarding/studio` | Initial studio profile. |
| `/onboarding/importacao` | Initial data import. |
| `/onboarding/agentes` | Entitlement-aware initial agent setup. |
| `/onboarding/revisao` | Review setup and open workspace. |
| `/app` | Today dashboard. |
| `/app/hoje` | Daily priorities and next actions. |
| `/app/operacao` | All operational cases. |
| `/app/operacao/[caseId]` | Case detail. |
| `/app/tarefas` | Task list. |
| `/app/tarefas/[taskId]` | Task detail. |
| `/app/aprovacoes` | Approval queue. |
| `/app/aprovacoes/[approvalId]` | Approval detail. |
| `/app/notificacoes` | Operational alerts. |

## CRM Web: Inbox And Contacts

| Route | Purpose |
| --- | --- |
| `/app/inbox` | Studio operational inbox. |
| `/app/conversas/[id]` | Conversation detail. |
| `/app/envios` | Outbound sends and failures. |
| `/app/envios/[sendId]` | Send attempt detail. |
| `/app/contatos` | Contacts, shared-phone identity issues and contact data quality. |
| `/app/contatos/[id]` | Contact detail. |

## CRM Web: Students And History

| Route | Purpose |
| --- | --- |
| `/app/alunos` | Student list. |
| `/app/alunos/[id]` | Student profile. |
| `/app/alunos/[id]/linha-do-tempo` | Unified student timeline. |
| `/app/historico` | History and evolution workspace. |
| `/app/historico/documentos` | Documents, attachments and anamnesis. |
| `/app/historico/permissoes` | History visibility rules. |
| `/app/professores` | Teacher-facing work and class context. |
| `/app/professores/[teacherId]` | Teacher detail, class context, notes and permitted workload. |

## CRM Web: Agenda

| Route | Purpose |
| --- | --- |
| `/app/agenda` | Calendar. |
| `/app/grade` | Weekly schedule structure. |
| `/app/turmas` | Class groups. |
| `/app/turmas/[id]` | Class group detail. |
| `/app/aulas/[id]` | Class session detail. |
| `/app/aulas/[id]/chamada` | Attendance and corrections. |
| `/app/reposicoes` | Make-up requests and reservations. |
| `/app/creditos-reposicao` | Make-up credit ledger. |
| `/app/lista-espera` | Waitlist. |
| `/app/eventos` | Workshops, special classes and events. |
| `/app/eventos/[eventId]` | Event detail, capacity, payments, attendance and communications. |

## CRM Web: Sales

| Route | Purpose |
| --- | --- |
| `/app/vendas` | Sales pipeline. |
| `/app/vendas/captura` | Multichannel lead capture and manual lead entry. |
| `/app/vendas/origens` | Source attribution, channels and source quality. |
| `/app/interessados` | Interested people. |
| `/app/interessados/novo` | Manual or assisted interested-person creation. |
| `/app/interessados/[id]` | Interested-person detail. |
| `/app/experimental` | Trial classes. |
| `/app/matriculas` | Pre-enrollment and conversion to student. |
| `/app/checkout-alunos` | Studio's own student checkout/link tracking. |
| `/app/indicacoes` | Referrals. |
| `/app/vendas/perdidos` | Lost opportunities. |
| `/app/segmentos` | Segments and bulk-action eligibility review. |
| `/app/segmentos/[segmentId]` | Segment detail, membership rules, eligible contacts and related actions. |

## CRM Web: Finance

| Route | Purpose |
| --- | --- |
| `/app/financeiro` | Finance overview. |
| `/app/financeiro/kanban` | Financial queue by stage. |
| `/app/financeiro/movimentacoes` | Unified list of monthly charges, one-off charges, payments, payment failures, reconciliation items, promises, adjustments and financial exceptions. |
| `/app/financeiro/movimentacoes/[id]` | Movement detail/drawer deep link. |
| `/app/financeiro/documentos` | Receipts, invoices and financial documents. |

Plan changes, agreements, refunds, discounts, blocks and courtesy credits are movement types or approval/task flows inside `/app/financeiro/movimentacoes` in the MVP, not separate topbar routes.

## CRM Web: Retention

| Route | Purpose |
| --- | --- |
| `/app/retencao` | Retention dashboard. |
| `/app/retencao/riscos` | Risk list and segments. |
| `/app/retencao/reativacoes` | Reactivation queue for ex-students, paused students and inactive students eligible to return. |
| `/app/cancelamentos` | Cancellation and pause cases. |
| `/app/reclamacoes` | Complaint cases and trust recovery follow-up. |
| `/app/reclamacoes/[caseId]` | Complaint detail, owner, SLA, resolution and recovery check. |

## CRM Web: Management And Reports

| Route | Purpose |
| --- | --- |
| `/app/dinheiro-na-mesa` | Operational opportunity summary. |
| `Gargalos` | MVP block/indicator inside reports and origin filters; no dedicated MVP route. |
| `Capacidade` | MVP occupancy/capacity indicators inside reports and agenda origins; no dedicated MVP route. |
| `/app/recursos` | Rooms, equipment and operational resources. |
| `/app/recursos/[resourceId]` | Resource detail, availability, capacity and outage history. |
| `/app/politicas` | Operational policies, rule versions and pending changes. |
| `/app/politicas/[policyId]` | Policy detail, effective dates and change history. |
| `/app/politicas/[policyId]/simular` | Policy impact simulation before rollout. |
| `/app/relatorios` | Reports hub. |
| `/app/relatorios/semana` | Weekly digest. |
| `/app/relatorios/financeiro` | Financial reports. |
| `/app/relatorios/vendas` | Sales reports. |
| `/app/relatorios/risco` | Retention risk reports. |
| `/app/relatorios/agentes` | Agent performance reports. |
| `/app/relatorios/ocupacao` | Capacity and occupancy reports. |
| `/app/checklists` | Daily opening, closing and setup checklist runs. |
| `/app/checklists/[runId]` | Checklist run detail, owner, missing items and completion history. |
| `/app/comunicados` | Broadcasts and audience-based announcements. |
| `/app/comunicados/[broadcastId]` | Broadcast detail, audience, approval, send status and audit. |

## CRM Web: Agents And Flow Runtime

| Route | Purpose |
| --- | --- |
| `/app/agentes` | Agent overview. |
| `/app/agentes/[agentId]` | Agent detail. |
| `/app/agentes/[agentId]/fluxos` | Agent flows. |
| `/app/fluxos` | All 96 candidate agent flows, with optional flows marked separately. |
| `/app/fluxos/[flowId]` | Flow configuration. |
| `/app/fluxos/[flowId]/simular` | Flow simulation before activation. |
| `/app/fluxos/execucoes/[runId]` | Simple operational receipt for a real flow execution; not a technical log or incident hub. |

## CRM Web: Usage, Billing And System

| Route | Purpose |
| --- | --- |
| `/app/uso` | Usage overview. |
| `/app/uso/extrato` | Usage ledger. |
| `/app/billing` | Taliya subscription. |
| `/app/billing/add-ons` | Extra quota and add-ons. |
| `/app/billing/invoices` | Billing history. |
| `/app/importacao` | Import jobs. |
| `/app/importacao/[jobId]` | Import job detail. |
| `/app/auditoria` | Audit events. |
| `/app/auditoria/[eventId]` | Audit detail. |
| `/app/dados/qualidade` | Missing and conflicting data. |
| `/app/dados/duplicidades` | Contact/student merge review. |
| `/app/exportacoes` | CRM, financial and backup export jobs. |
| `/app/exportacoes/[jobId]` | Export job detail, file availability, requester and audit trail. |
| `/app/privacidade/solicitacoes` | LGPD requests: export, correction, deletion and anonymization. |
| `/app/privacidade/solicitacoes/[requestId]` | Privacy request detail, identity validation, actions and audit. |
| `/app/suporte/acessos` | Taliya support access approvals. |
| `/app/suporte/acessos/[grantId]` | Scoped support access grant, expiration, purpose and audit. |

## Configuration Routes

| Route | Purpose |
| --- | --- |
| `/app/configuracoes` | Settings hub with the 8 post-go-live configuration cards. |
| `/app/configuracoes/studio` | Studio identity and institutional hours. |
| `/app/configuracoes/equipe` | Team users, invites, roles and access status. |
| `/app/configuracoes/permissoes` | Simple role permissions and sensitive limits. |
| `/app/configuracoes/canais` | Public contact channels, internal channel preferences, WhatsApp/e-mail technical status and compact logs when needed. |
| `/app/configuracoes/financeiro/modelos` | Student plans, lesson rights and simple make-up/consumption rules per plan. |
| `/app/configuracoes/financeiro/pagamentos` | Manual payment methods, simple finance rules, Pagamentos Taliya activation, provider status and compact logs when needed. |
| `/app/configuracoes/agenda` | Calendar exceptions, temporary blocks, simple agenda rules and calendar/import technical status when needed. |
| `/app/configuracoes/notificacoes` | Internal team alert preferences by role, frequency, internal channel and alert delivery status when needed. |

Removed from the post-go-live settings family:

- `/app/configuracoes/agenda/consumo-aulas`: absorbed into `/app/configuracoes/financeiro/modelos` per plan.
- `/app/configuracoes/financeiro`: absorbed into `/app/configuracoes/financeiro/pagamentos`.
- `/app/configuracoes/templates`, `/app/configuracoes/base-conhecimento`, `/app/configuracoes/vendas`, `/app/configuracoes/retencao`, `/app/configuracoes/politicas`, `/app/configuracoes/privacidade`, `/app/configuracoes/recursos` and `/app/configuracoes/campos`: not part of the MVP Configuracoes Pos-Go-Live surface. Their concerns live contextually in operational pages, Agentes/Fluxos, Billing, Auditoria, Privacidade requests or future product surfaces.

Technical integrations are not a separate owner-facing route family in the MVP. Their status, testing, reconnection and compact logs appear inside the specific configuration page that uses the connection.

## Route Consolidation Risks

These routes are candidates for grouped experiences rather than independent primary navigation items:

- finance exceptions, agreements, disputes and plan changes may become one finance cases workspace with tabs/filters;
- segments, broadcasts and campaigns may become one audience/actions workspace;
- setup checklist and data-quality blockers may share one readiness workspace;
- reports should avoid duplicating object detail pages;
- mobile should expose daily action surfaces, not every configuration route.

## Mobile App V1

Mobile should not duplicate every configuration surface.

Required tabs:

- Today
- Inbox
- Agenda
- Students
- Interested
- Tasks
- Approvals
- Finance essentials
- Complaints and sensitive cases
- Automation incidents
- Make-up requests
- Student history quick notes
- Notifications

Configuration-heavy routes should stay web-first.
