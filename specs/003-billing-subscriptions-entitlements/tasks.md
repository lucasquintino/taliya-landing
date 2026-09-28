# Tasks: Billing, Subscriptions And Entitlements

**Input**: Design documents from `/specs/003-billing-subscriptions-entitlements/`
**Prerequisites**: `spec.md`, `plan.md`, `data-model.md`, `contracts/billing-contract.md`

## Phase 1: Billing Foundation

- [ ] T001 Document Asaas v1 provider constraints, sandbox setup, required credentials and webhook secret/token handling
- [ ] T002 Define trusted plan/price config shared with landing and Atendente IA
- [ ] T003 Create billing provider abstraction in `lib/billing/provider.ts`
- [ ] T004 Create billing data models/migrations for customer, subscription, entitlement, webhook event and audit log
- [ ] T005 Add tenant-scoped billing ownership rules
- [ ] T033 Add launch entitlement config for Base, 1 Agente, 3 Agentes and 7 Agentes with agent access, user limits, WhatsApp limits, unit limits and AI message caps
- [ ] T034 Verify landing, Atendente IA, billing and onboarding read plan claims from the same trusted config

## Phase 2: Checkout

- [ ] T006 Implement server-side checkout route in `app/api/billing/checkout/route.ts`
- [ ] T007 Validate plan ID and billing period from trusted config
- [ ] T008 Create Asaas checkout/payment/subscription flow from server credentials
- [ ] T009 Ensure failed or abandoned checkout does not grant entitlement
- [ ] T010 Add tests for invalid plan, missing price and unauthorized checkout inputs
- [ ] T029 Support checkout source metadata from `/pilates/planos`, Atendente IA recommendation/explicit intent and Sales Inbox assisted close
- [ ] T030 Verify plan comparison/view-only actions do not create checkout sessions
- [ ] T031 Verify public checkout creates no free trial, no delayed first charge and no trialing entitlement
- [ ] T035 Hide or reject annual billing until Asaas annual price/renewal config exists
- [ ] T036 Verify boleto/Pix generation does not grant access before trusted payment confirmation
- [ ] T048 Add checkout gate validation for explicit buy intent, confirmed recommendation, intentional plans-page checkout action or operator-assisted close
- [ ] T049 Reject or safely redirect `/pilates` landing CTA context when no valid checkout gate is present
- [ ] T050 Persist safe checkout metadata for lead/onboarding context: entryPath, selectedPainIds, recommendedAgentIds, recommendedPlanId, guidedDemoCompleted, leadId and sessionId

## Phase 3: Webhooks

- [ ] T011 Implement billing webhook route in `app/api/billing/webhook/route.ts`
- [ ] T012 Verify provider webhook signatures
- [ ] T013 Deduplicate webhook processing by provider event ID
- [ ] T014 Persist subscription/customer updates
- [ ] T015 Update entitlement state from trusted provider events
- [ ] T016 Add tests for duplicate webhook, failed signature, success, failed payment, cancellation, upgrade and downgrade
- [ ] T037 Map Asaas payment events to internal checkout intent, customer and subscription records
- [ ] T038 Create pending tenant activation after the first trusted paid/received payment event
- [ ] T039 Verify overdue, refunded, reversed, chargeback, canceled and unpaid states do not grant active entitlement

## Phase 4: Entitlements

- [ ] T017 Implement entitlement helper in `lib/billing/entitlements.ts`
- [ ] T018 Gate protected SaaS server routes/APIs by tenant entitlement
- [ ] T019 Add cross-tenant denial tests
- [ ] T020 Add past-due/canceled access behavior
- [ ] T040 Enforce AI message, WhatsApp channel, user and studio-unit limits server-side as hard caps
- [ ] T041 Add usage near-limit warnings and cap-reached blocks with upgrade or quota-purchase path
- [ ] T051 Add trusted add-on quota configuration and checkout path for Cota Avulsa +2k (R$67) and Cota Mensal +5k (R$97/month) or approved replacements
- [ ] T052 Define fiscal/nota-fiscal operating model and block public copy/agent promises that are not configured
- [ ] T053 Add internal-only `private_operational_cost_pilot` entitlement path with manual operator approval/control, audit trail and operational cost logging
- [ ] T054 Add 30-day guarantee/cancellation/refund policy configuration for public monthly plans and ensure custom/private plans can use separate terms
- [ ] T055 Verify failed checkout/payment does not activate initial plan, upgrade, add-on quota or onboarding link
- [ ] T056 Add checkout field validation for full name, email, WhatsApp, CPF or CNPJ and selected plan

## Phase 5: Billing Portal And Admin

- [ ] T021 Implement billing portal route in `app/api/billing/portal/route.ts`
- [ ] T022 Restrict portal access to tenant owners/admins
- [ ] T023 Add audited admin override flow
- [ ] T024 Add safe error handling and internal billing logs

## Phase 6: Paid Activation

- [ ] T042 Implement pending tenant activation creation and single-use token persistence
- [ ] T043 Implement activation claim route requiring magic link/OTP authenticated owner
- [ ] T044 Link activation to tenant, owner membership and onboarding start state
- [ ] T045 Notify owner with onboarding link by email and, when contact exists, WhatsApp/n8n secondary alert
- [ ] T046 Verify checkout-return/query-string success cannot claim activation without trusted paid entitlement

## Final Verification

- [ ] T025 Verify checkout success grants access only after webhook
- [ ] T026 Verify no client-reported payment state grants access
- [ ] T027 Verify tenant A cannot access tenant B billing records
- [ ] T028 Verify onboarding can read active entitlement after payment
- [ ] T032 Verify unexpected provider `trialing` status does not grant paid access in v1
- [ ] T047 Verify Asaas sandbox checkout, webhook and activation flow end-to-end for each public plan
- [ ] T057 Verify 30-day guarantee/refund configuration is available to landing, Atendente IA and checkout terms before public checkout is enabled
- [ ] T058 Verify checkout creation rejects cold `/pilates` CTA context unless explicit checkout gate metadata is present
- [ ] T059 Verify checkout metadata includes `leadId`, `sessionId`, `entryPath`, selected pains, recommended plan, selected plan, guided-demo context and checkout gate reason without allowing those fields to determine price or entitlement
