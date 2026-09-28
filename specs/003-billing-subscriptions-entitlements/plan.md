# Implementation Plan: Billing, Subscriptions And Entitlements

**Branch**: `codex/003-billing-subscriptions-entitlements` | **Date**: 2026-04-30 | **Spec**: [spec.md](./spec.md)

## Summary

Build the trusted paid-access layer for the vertical SaaS. Landing and Atendente IA can create subscription intent, but only this feature can create checkout sessions, process trusted billing events, update subscription state and grant tenant entitlements.

Public v1 has no free trial. Checkout charges immediately according to trusted plan configuration, and only confirmed active paid subscriptions grant entitlement.

## Technical Context

**Project Type**: Next.js SaaS web application
**Storage**: Durable database required for tenants, billing customers, subscriptions, entitlements, processed webhook events and audit logs
**Provider**: Asaas for v1, behind a billing provider adapter
**Security**: Webhook signature verification, idempotency, tenant scoping and server-only provider credentials are mandatory
**Dependencies**: Spec 1 provides public plan/pricing config; Spec 4 consumes active entitlements for onboarding/access

## Architecture Decisions

- Asaas is the v1 billing provider.
- Billing provider credentials stay server-side.
- Checkout/session creation happens through server routes/actions, never client-computed URLs unless the provider gives trusted preconfigured links.
- Webhooks are the source of truth for active subscription state.
- Entitlements are stored server-side and enforced by SaaS APIs/routes.
- Trial/trialing states are disabled for public v1 and must not grant access if received unexpectedly.
- Credit card recurring payment is the preferred automatic subscription path; boleto/Pix paths grant access only after trusted payment confirmation.
- Buyer account creation happens after payment confirmation through a pending tenant activation and magic link/OTP authentication.
- Tenant owner controls billing portal access.
- Admin overrides are possible only through audited internal actions.

## Planned Modules

```text
lib/billing/
  config.ts
  provider.ts
  checkout.ts
  webhooks.ts
  entitlements.ts
  portal.ts
  audit.ts
  activation.ts

app/api/billing/
  checkout/route.ts
  webhook/route.ts
  portal/route.ts
```

## Rollout Phases

### Phase 1: Billing Contract

- Define plan/price config contract shared with landing.
- Define internal billing entities.
- Implement provider adapter around Asaas.
- Define launch entitlements for Base, 1 Agente, 3 Agentes and 7 Agentes.

### Phase 2: Checkout

- Create server-side checkout/session route.
- Validate plan/price from trusted config.
- Redirect visitor safely to provider checkout.

### Phase 3: Webhooks

- Verify provider signatures.
- Deduplicate events by provider event ID.
- Update customer, subscription and entitlement state from trusted Asaas payment/subscription-linked events.
- Create pending tenant activation after first confirmed payment.

### Phase 4: Entitlement Enforcement

- Add server-side entitlement checks.
- Gate paid features by tenant plan.
- Add failed/canceled/past-due behavior.

### Phase 5: Billing Portal And Admin

- Create billing portal session for tenant owner.
- Add audited admin overrides where needed.

## Verification

- Webhook signature failure is rejected.
- Duplicate webhook event is processed once.
- Checkout success grants entitlement only after webhook.
- Failed checkout does not grant access.
- Canceled/past-due subscription updates access.
- Tenant A cannot access Tenant B billing state.
