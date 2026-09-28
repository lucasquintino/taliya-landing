# Data Model: Billing, Subscriptions And Entitlements

## PlanEntitlementConfig

Fields:

- `planId`
- `publicName`
- `monthlyPriceBRL`
- `recommended`
- `includedAgentIds`
- `studioUnitLimit`
- `userLimit`
- `whatsappChannelLimit`
- `monthlyAiMessageLimit`
- `onboardingLevel`
- `supportLevel`
- `customAgentPolicy`
- `providerPriceRefs`
- `createdAt`
- `updatedAt`

Validation:

- Must be the shared trusted source used by Landing, Atendente IA, Billing and Onboarding.
- Public visible plan claims must be derived from this config.
- Provider price references are server-trusted and never accepted from client input.

Launch defaults:

| Plan ID | Included agents | Unit limit | User limit | WhatsApp limit | AI message limit | Custom-agent policy |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `base` | 0 active AI agents, CRM only | 1 | 1 | 0 automated channels | 0/month | Separate business |
| `one_agent` | 1 selected primary agent | 1 | 2 | 1 studio-owned WhatsApp | 1,500/month hard cap | Separate business |
| `three_agents` | 3 selected primary agents | 1 | 5 | 1 studio-owned WhatsApp | 5,000/month hard cap | Separate business |
| `seven_agents` | All seven primary agents | 1 | 10 | 1 studio-owned WhatsApp | 15,000/month hard cap | Separate business |

## CheckoutIntent

Fields:

- `id`
- `provider`
- `providerCheckoutId`
- `providerPaymentId`
- `providerSubscriptionId`
- `planId`
- `billingPeriod`
- `billingEmail`
- `source`
- `sourcePage`
- `sourceSection`
- `sessionId`
- `status`
- `createdAt`
- `updatedAt`

Validation:

- Checkout intent is not proof of payment.
- Status can record started, redirected, abandoned, failed or confirmed, but entitlement is granted only by trusted webhook state.

## TenantBillingAccount

Fields:

- `tenantId`
- `billingProvider`
- `providerCustomerId`
- `billingEmail`
- `billingOwnerUserId`
- `status`
- `createdAt`
- `updatedAt`

Validation:

- One active billing account per tenant/provider.
- Billing owner must be a tenant owner/admin.

## BillingSubscription

Fields:

- `tenantId`
- `providerSubscriptionId`
- `providerCustomerId`
- `planId`
- `priceId`
- `billingPeriod`
- `status`
- `currentPeriodStart`
- `currentPeriodEnd`
- `cancelAtPeriodEnd`
- `createdAt`
- `updatedAt`

Validation:

- Status comes from trusted provider events.
- Client input never sets active status.
- Public v1 plans do not use trial periods.
- Provider `trialing` status, if received unexpectedly, must not grant active entitlement.
- Asaas-linked payment events must be mapped to the subscription using provider IDs stored here.

## EntitlementSet

Fields:

- `tenantId`
- `planId`
- `status`
- `features`
- `agentAccess`
- `usageLimits`
- `effectiveFrom`
- `effectiveUntil`

Validation:

- Entitlements are derived from subscription status and plan config.
- Server/API checks must use this record or a trusted derived view.
- Usage limits must include explicit counters for AI messages, WhatsApp channels, users and studio units.
- AI message caps are hard caps: after the cap is reached, automated usage stops until upgrade or quota purchase.

## TenantActivation

Fields:

- `id`
- `tenantId`
- `billingCustomerId`
- `billingSubscriptionId`
- `billingEmail`
- `activationTokenHash`
- `status`
- `expiresAt`
- `claimedByUserId`
- `createdAt`
- `claimedAt`

Validation:

- Created only after trusted first payment confirmation.
- Token must be single-use and stored hashed.
- Claiming requires authenticated identity through magic link/OTP or equivalent secure login.
- Claiming must verify the billing email/customer relationship before creating owner membership.

## BillingWebhookEvent

Fields:

- `provider`
- `providerEventId`
- `eventType`
- `signatureVerified`
- `processedAt`
- `processingStatus`
- `safeError`

Validation:

- `providerEventId` is unique.
- Failed signature events are not processed.

## BillingAuditLog

Fields:

- `actorUserId`
- `tenantId`
- `action`
- `before`
- `after`
- `reason`
- `createdAt`

Validation:

- Required for manual overrides, entitlement changes and billing ownership changes.
