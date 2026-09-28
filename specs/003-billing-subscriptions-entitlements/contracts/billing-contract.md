# Billing API Contract

Provider for v1: Asaas.

## Create Checkout

Route:

```text
POST /api/billing/checkout
```

Input:

```json
{
  "planId": "seven_agents",
  "billingPeriod": "monthly",
  "source": "landing_plans",
  "sourcePage": "/pilates/planos",
  "sourceSection": "plans",
  "sessionId": "anon_123"
}
```

Rules:

- `planId` must exist in trusted config.
- `source` may be `landing_plans`, `landing_cta` or `ai_attendant`.
- Price, provider customer, provider subscription/payment and checkout details are resolved server-side.
- Source metadata is used for tracking/reconciliation only, never for pricing or entitlement.
- Plan comparison/view-only actions must not call this route.
- Response does not expose provider secrets.
- Credit card recurring is the preferred automatic path.
- Boleto/Pix paths may be created only when configured, and do not grant access until payment confirmation webhook is processed.
- Annual billing period is rejected or hidden unless provider price/configuration is enabled.

Output:

```json
{
  "checkoutUrl": "https://provider-checkout.example/session",
  "checkoutSessionId": "provider_session_id",
  "checkoutIntentId": "internal_checkout_intent_id"
}
```

## Billing Webhook

Route:

```text
POST /api/billing/webhook
```

Rules:

- Verify provider signature.
- Deduplicate by provider event ID.
- Update billing and entitlement state server-side.
- Map Asaas payment events to the internal customer/subscription/checkout intent using stored provider IDs.
- Create pending tenant activation only after trusted first paid/received payment confirmation.
- Do not activate access from boleto/Pix generation, checkout return URL or payment-pending states.
- Return success only after safe persistence or accepted idempotent duplicate.

## Tenant Activation

Internal route:

```text
POST /api/billing/activation/claim
```

Input:

```json
{
  "activationToken": "single_use_token",
  "authSessionId": "authenticated_owner_session"
}
```

Rules:

- Requires authenticated identity through magic link/OTP or equivalent secure login.
- Token must be single-use and unexpired.
- Activation must match a trusted paid entitlement.
- Creates or links tenant, owner membership and onboarding start state.
- Does not allow cross-email or cross-customer claiming without audited admin action.

## Billing Portal

Route:

```text
POST /api/billing/portal
```

Rules:

- Requires authenticated tenant owner/admin.
- Creates trusted provider portal session.
- Denies cross-tenant access.

## Entitlement Check

Internal API:

```ts
canUseFeature(tenantId, featureKey): Promise<boolean>
```

Rules:

- Tenant ID must be verified against authenticated membership.
- Entitlement state is server-side.
- UI may hide unavailable features but server remains authoritative.
