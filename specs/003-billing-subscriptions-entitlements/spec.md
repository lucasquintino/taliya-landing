# Feature Specification: Billing, Subscriptions And Entitlements

**Feature Branch**: `codex/003-billing-subscriptions-entitlements`
**Created**: 2026-04-30
**Status**: Draft ready for planning
**Input**: Implement the paid subscription layer behind the vertical SaaS offer sold by the landing and Atendente IA. This feature turns a trusted checkout/payment confirmation into a tenant subscription and enforceable product access.

Commercial E2E launch readiness, checkout gate expectations and implementation order are defined in [../commercial-e2e-readiness-and-implementation-order.md](../commercial-e2e-readiness-and-implementation-order.md). Spec 3 owns server-side checkout, trusted payment confirmation, entitlement activation, payment failure denial and billing terms required by that cross-spec checklist.

## Product Goal

When a studio owner chooses a plan from the landing plans destination or Atendente IA, the system must route them through a trusted billing flow, confirm payment/subscription status through server-side provider events, create or update the correct customer/tenant billing record and grant only the entitlements included in the active plan.

This feature is the boundary between "visitor clicked a plan" and "studio has paid access".

## Trial Policy

The product does not offer a public free trial in v1.

Checkout must charge immediately according to the selected configured plan and billing period. No free trial, trialing subscription state, free workspace access, hidden trial entitlement, delayed first charge or "test for free" public offer is part of this release.

Any future trial, pilot, coupon, guarantee or delayed-billing experiment must be enabled by an explicit later product decision and reflected in trusted billing configuration, landing copy, entitlement rules and onboarding access rules before launch.

## Billing Provider Decision

The v1 billing provider is Asaas.

Rationale: the first commercial market is Brazil, and the SaaS needs BRL checkout with local payment methods, hosted/secure payment collection, recurring charges, server-side API usage, sandbox support and webhook-driven confirmation. Asaas is the default integration path for v1 because it supports Pix, boleto and credit card payments through its API/checkout surfaces, recurring charge scenarios, backend-only API credentials and sandbox testing.

The checkout experience must be created server-side from trusted plan configuration. Browser code, chat messages and query parameters must never generate prices, provider IDs, payment links or entitlement state.

Payment method policy for v1:

- Credit card recurring payment is the preferred automatic subscription path.
- Boleto is allowed as a slower confirmation path when configured.
- Pix can be offered only through the Asaas-supported path currently configured for the chosen checkout/subscription flow. If direct recurring Pix/Pix Automatico is not fully configured, public copy must not promise automatic Pix recurrence.
- Access starts only after the first trusted payment confirmation event is processed server-side.
- Annual billing stays hidden until Asaas price/configuration and renewal behavior are explicitly configured.

Checkout required fields for v1:

- full name;
- email;
- WhatsApp;
- CPF or CNPJ;
- selected plan.

Studio name and operational configuration are collected during onboarding, not required as checkout source of truth.

Webhook policy for Asaas:

- Billing state must be derived from trusted payment/webhook events, not only from checkout redirect success.
- Webhook handling must be idempotent by provider event ID.
- Subscription linkage must account for Asaas payment webhooks that reference the subscription/cobranca relationship.
- Failed, overdue, refunded, reversed, chargeback, canceled or unpaid payment states must not grant active paid access.
- Initial plan, upgrade and add-on activation happens only after trusted paid/received confirmation. Payment failure never activates the plan or onboarding.

## Launch Plan Entitlements

The public launch uses four configured plans organized by number of active AI agents: 0, 1, 3 and 7 agents. These values are launch defaults and must live in trusted plan configuration shared by Landing, Atendente IA, Billing and Onboarding.

| Plan | Monthly Price | Active AI Agents | Studio Scope | WhatsApp | Usage Cap | Onboarding | Support | Custom Agent |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Base | R$ 197/mes | 0 agents | 1 studio/unit, up to 1 user | No automated WhatsApp agent | No AI message automation included | Self-guided setup with AI | 24/7 AI support; human escalation when configured | Separate business |
| 1 Agente | R$ 497/mes | 1 selected primary agent | 1 studio/unit, up to 2 users | Studio's own WhatsApp connected for the selected agent | 1,500 AI messages/month hard cap | Self-guided setup with AI | 24/7 AI support; human escalation when configured | Separate business |
| 3 Agentes | R$ 897/mes | 3 selected primary agents | 1 studio/unit, up to 5 users | Studio's own WhatsApp connected for included agents | 5,000 AI messages/month hard cap | Self-guided setup with AI | 24/7 AI support; human escalation when configured | Separate business |
| 7 Agentes | R$ 1.497/mes | All seven primary agents: Atendimento, Agenda, Vendas, Financeiro, Retencao, Gestao and Historico/Evolucao | 1 studio/unit, up to 10 users | Studio's own WhatsApp connected for included agents | 15,000 AI messages/month hard cap | Self-guided setup with AI | 24/7 AI support; human escalation when configured | Separate business |

Public copy may present usage as a plan limit/boundary instead of exposing every technical counter, but it must not imply unlimited or soft fair-use behavior. Entitlement enforcement must use explicit server-side hard caps.

Launch default add-on quota packs are defined in Spec 2 `commercial-sales-playbook.md` and must be copied into trusted billing configuration before being sold. These defaults may change, but the product must never silently allow over-limit usage or silently overcharge usage beyond the customer's active plan/quota.

Plan notes:

- 7 Agentes is the complete-system plan and the default commercial recommendation for broad operational pain, multi-agent needs or high buying intent unless configuration changes it.
- Base is a CRM-only plan with no active AI agent automation.
- 1 Agente is for a narrow first automation need.
- 3 Agentes is for studios that want meaningful automation but are not ready for the complete seven-agent system.
- 7 Agentes is the fit for the full SaaS promise and highest launch usage, but still for one studio/unit in v1.
- Multi-unit support is not included in v1 launch plans and belongs to a future Enterprise plan.
- Agente sob medida is never silently included as an eighth primary agent and is not included in any public launch plan. It is a separate business/opportunity.
- The sales AI uses the SaaS operator's own WhatsApp number. Paying studios connect and use their own WhatsApp number for their studio agents.
- When usage reaches the configured cap, additional automated AI usage must stop until the tenant upgrades or buys more quota.
- Public monthly plans include a 30-day guarantee on the first subscription, according to trusted cancellation/refund configuration.
- The 30-day guarantee must be represented in trusted billing/terms configuration and made available to landing and Atendente IA surfaces before checkout.
- Initial workspace activation and self-guided AI setup should take only a few minutes for all public plans after trusted payment confirmation. External setup dependencies such as WhatsApp connection, missing studio information or provider approval may still delay full agent operation.

## Private Operational-Cost Pilot

The product may include one internal, invite-only pilot plan for a specific Pilates studio to test the SaaS in real operation after the SaaS is ready.

This plan is not a public free trial and must not appear on `/pilates`, `/pilates/planos`, public checkout selection or the default Atendente IA sales path.

Rules:

- internal plan type: `private_operational_cost_pilot`;
- billing amount: no SaaS subscription/platform fee; operational costs may be passed through personally by the operator;
- entitlement: manually configured and audited for the pilot scope;
- duration/end date: defined personally by the operator at any time;
- operator handles the private pilot personally outside the public sales automation;
- access still requires trusted tenant, entitlement and activation records;
- usage and provider costs must still be logged;
- after pilot, the studio must move to a public paid plan or a separately approved commercial arrangement.

## Post-Payment Activation Decision

The buyer does not need to create an account before paying.

Default flow:

1. Visitor selects a plan from `/pilates/planos`, Atendente IA after recommendation/explicit buying intent, or Sales Inbox assisted close. `/pilates` itself should only pass consultor context unless the visitor has intentionally reached a checkout-eligible CTA.
2. Server creates an Asaas checkout/payment/subscription flow using trusted plan config.
3. Visitor pays with the configured payment method.
4. Asaas webhook confirms the first paid/received payment state.
5. Server creates or updates a billing customer, subscription and paid entitlement.
6. Server creates a pending tenant activation tied to the billing email/customer.
7. Owner receives an onboarding link by email and, when contact exists, WhatsApp.
8. Owner authenticates with magic link/OTP and claims or creates the studio workspace.
9. Onboarding configures the studio and included agents according to the active entitlement.

The product must not create paid workspace access from checkout-started, checkout-returned, query-string success, chat intent or unpaid subscription states.

If checkout or payment fails, the selected plan remains inactive. No onboarding link, paid entitlement, upgrade entitlement or add-on quota is granted until a trusted paid/received event is processed.

## User Scenarios & Testing

### User Story 1 - Studio Subscribes To A Plan (Priority: P1)

As a studio owner, I want to choose a plan and complete checkout securely, so my studio can start using the SaaS after payment confirmation.

**Acceptance Scenarios**:

1. **Given** a visitor selects Base, 1 Agente, 3 Agentes or 7 Agentes from `/pilates/planos`, Atendente IA after recommendation/explicit buying intent, or Sales Inbox assisted close, **When** checkout starts, **Then** the provider session is created server-side from trusted plan configuration.
2. **Given** checkout succeeds, **When** the trusted webhook confirms the subscription, **Then** the system creates/updates billing customer, subscription and tenant entitlement records.
3. **Given** checkout is abandoned or fails, **When** the visitor returns, **Then** the system does not mark the subscription active or grant access.

### User Story 2 - Tenant Access Follows Entitlements (Priority: P1)

As the SaaS system, I want every product boundary to check plan entitlements, so unpaid or downgraded studios cannot access features outside their plan.

**Acceptance Scenarios**:

1. **Given** a tenant has active 7 Agentes entitlement, **When** they access included agents, **Then** access is allowed.
2. **Given** a tenant has Base, 1 Agente or 3 Agentes entitlement, **When** they access an unavailable agent or feature, **Then** access is denied or upsell-gated.
3. **Given** subscription status becomes past due, canceled or unpaid, **When** protected SaaS routes or APIs are used, **Then** access is limited according to policy.

### User Story 3 - Billing Lifecycle Is Reliable (Priority: P1)

As the operator, I want webhook handling to be secure and idempotent, so retries, failures and plan changes do not corrupt subscription state.

**Acceptance Scenarios**:

1. **Given** the billing provider retries the same webhook event, **When** it is received twice, **Then** it is processed once.
2. **Given** webhook signature verification fails, **When** the event arrives, **Then** it is rejected and logged safely.
3. **Given** a plan is upgraded, downgraded, canceled or payment fails, **When** the provider sends the event, **Then** entitlement state updates server-side.

### User Story 4 - Customer Can Manage Billing (Priority: P2)

As a paying studio owner, I want to view invoices, update payment method and cancel or change my plan through a trusted billing portal, so I do not need support for basic billing actions.

**Acceptance Scenarios**:

1. **Given** an authenticated tenant owner opens billing settings, **When** they request billing management, **Then** the system creates a trusted provider portal/session.
2. **Given** a non-owner tries to manage billing, **When** they request the portal, **Then** access is denied.

## Functional Requirements

- **FR-001**: Billing provider sessions MUST be created server-side from trusted plan configuration.
- **FR-002**: The system MUST support the configured public plans from the landing: Base, 1 Agente, 3 Agentes and 7 Agentes.
- **FR-003**: Plan prices, billing periods and checkout mapping MUST come from trusted configuration, not client input.
- **FR-004**: The system MUST verify billing webhook signatures before processing events.
- **FR-005**: Webhook processing MUST be idempotent by provider event ID.
- **FR-006**: The system MUST store provider customer ID, subscription ID and price/plan ID scoped to the tenant.
- **FR-007**: The system MUST store subscription status server-side.
- **FR-008**: Product access MUST be granted only after trusted payment/subscription confirmation.
- **FR-009**: Entitlements MUST be tenant-scoped and enforced at server/API boundaries, not only in the UI.
- **FR-010**: The system MUST handle checkout success, checkout failure, abandoned checkout, active subscription, past due, unpaid, canceled, upgraded and downgraded states. If a provider unexpectedly sends `trialing`, the system MUST treat it as non-active for v1 access.
- **FR-011**: The system MUST not trust client-reported checkout status, query params or chat messages as proof of payment.
- **FR-012**: The system MUST provide a billing portal/session for authorized tenant owners when the provider supports it.
- **FR-013**: Manual admin billing changes MUST be audited.
- **FR-014**: Failed billing provider calls MUST return safe user-facing errors and log internal details server-side.
- **FR-015**: Billing events MUST not store full card numbers or sensitive payment credentials.
- **FR-016**: Billing state MUST integrate with onboarding so paid tenants can continue setup after activation.
- **FR-017**: Checkout creation MUST support plan selections coming from the `/pilates/planos` plans page, Atendente IA after recommendation/explicit buying intent and Sales Inbox assisted close without duplicating pricing logic.
- **FR-018**: Checkout requests SHOULD include source metadata such as `source`, `sourcePage`, `sourceSection`, `entryPath`, `sessionId`, `leadId`, `selectedPainIds`, `recommendedAgentIds`, `recommendedPlanId`, `selectedPlanId`, `guidedDemoCompleted` and `checkoutGateReason` for tracking, lead reconciliation and onboarding context, but these fields MUST NOT determine price or entitlement.
- **FR-018A**: Public checkout MUST collect full name, email, WhatsApp, CPF or CNPJ and selected plan before payment confirmation processing.
- **FR-019**: A visitor viewing plans or comparing plans MUST NOT create a checkout session until they explicitly choose a plan CTA.
- **FR-020**: Public v1 checkout MUST NOT create free trials, trialing subscriptions, delayed first charges or unpaid workspace access.
- **FR-021**: The billing provider configuration MUST NOT set `trial_period_days`, `trial_end` or equivalent trial settings for public v1 plans.
- **FR-022**: Entitlements MUST NOT treat `trialing`, unpaid, incomplete or checkout-started states as active paid access in v1.
- **FR-022A**: Failed payment MUST NOT activate an initial plan, upgrade, add-on quota or onboarding link.
- **FR-023**: Asaas MUST be the default v1 billing provider unless a later product decision replaces it before implementation.
- **FR-024**: The Asaas API key, webhook secret/token and provider identifiers MUST remain server-side.
- **FR-025**: Credit card recurring payment MUST be the preferred automatic subscription method for v1.
- **FR-026**: Boleto/Pix paths MUST grant access only after trusted payment confirmation, not after boleto generation, Pix QR generation or checkout redirect.
- **FR-027**: Public copy MUST NOT promise automatic Pix recurrence unless the configured Asaas Pix Automatico flow is implemented and enabled.
- **FR-028**: The system MUST create a pending tenant activation after trusted first payment confirmation.
- **FR-029**: The owner MUST authenticate through magic link/OTP or equivalent secure account flow before claiming the studio workspace.
- **FR-030**: Plan entitlements MUST match the Launch Plan Entitlements table unless trusted plan configuration changes it.
- **FR-031**: Usage limits MUST be enforced server-side as hard caps; tenants who hit the cap MUST upgrade or buy more quota before additional automated AI usage continues.
- **FR-032**: Agente sob medida MUST be treated as a separate business/opportunity and MUST NOT be included in any public launch plan entitlement.
- **FR-033**: All public launch plans MUST be scoped to one studio/unit; multi-unit behavior belongs to a future Enterprise plan.
- **FR-034**: Studio operational agents MUST use the paying studio's own connected WhatsApp, while the SaaS sales attendant uses the SaaS operator's own WhatsApp.
- **FR-035**: Checkout creation MUST reject or safely redirect requests that do not satisfy a trusted checkout gate: explicit buy intent, confirmed recommendation, intentional plans-page checkout action or operator-assisted close.
- **FR-036**: `/pilates` landing CTA context alone MUST NOT create checkout unless the request also includes a valid checkout gate.
- **FR-037**: The system MUST enforce AI-message usage caps as hard caps and require trusted upgrade or add-on quota purchase before additional automated AI usage continues.
- **FR-038**: The system MUST define fiscal/nota-fiscal behavior before paid launch and the Atendente IA MUST NOT promise automatic invoice issuance unless configured.
- **FR-038A**: V1 nota fiscal behavior is manual on request after trusted payment confirmation; automatic invoice issuance is future scope unless configured.
- **FR-039**: The system MAY support one private operational-cost pilot plan, but it MUST be internal-only, manually approved, audited, personally operator-controlled and excluded from public plan/checkout surfaces.
- **FR-040**: Public monthly plans MUST support the configured 30-day guarantee policy for the first subscription without implying guaranteed financial results.

## Key Entities

- **Billing Provider**: External payment/subscription provider selected for checkout, webhooks and billing portal.
- **Billing Customer**: Provider customer record linked to one tenant/studio.
- **Subscription**: Provider and internal subscription state for a tenant.
- **Plan**: Configured product tier such as Base, 1 Agente, 3 Agentes or 7 Agentes.
- **Price**: Configured billing amount and period for a plan.
- **Entitlement**: Tenant-scoped access rights derived from active subscription/plan.
- **Webhook Event**: Trusted provider event with signature, event ID and payload.
- **Billing Portal Session**: Trusted provider session for managing invoices, payment method and plan changes.
- **Audit Log**: Internal record of billing-sensitive changes.

## Success Criteria

- **SC-001**: Checkout completion grants access only after trusted server-side provider confirmation.
- **SC-002**: Duplicate provider webhooks produce one subscription/entitlement update.
- **SC-003**: Canceled, unpaid or past-due subscriptions do not retain unrestricted paid access.
- **SC-004**: Cross-tenant attempts to access billing or entitlement records are denied.
- **SC-005**: Landing plans destination and Atendente IA plan CTAs can route to billing without duplicating plan/pricing logic.
- **SC-006**: Manual QA verifies active, failed, canceled, upgraded and downgraded billing states.
- **SC-007**: Manual QA confirms checkout charges immediately in test mode and no public plan starts as a free trial.
- **SC-008**: Any `trialing` or unpaid provider status is denied paid onboarding/workspace access in v1.

## Out Of Scope

- Public landing pricing design.
- Atendente IA conversation behavior.
- Studio onboarding screens.
- Accounting/tax advisory decisions.
- Long-term revenue analytics.

## Open Decisions

- Tax/invoice requirements for Brazil must be confirmed before public paid launch.
- Coupon, guarantee and annual billing behavior must be explicitly enabled or hidden in configuration.
- Pix Automatico can be evaluated after launch; it must not be promised publicly until configured end-to-end.
