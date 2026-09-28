# Data Model: SaaS Onboarding And Studio Setup

## UserAccount

Fields:

- `id`
- `email`
- `name`
- `phone`
- `createdAt`
- `updatedAt`

## Tenant

Fields:

- `id`
- `name`
- `billingCustomerId`
- `status`
- `createdAt`
- `updatedAt`

Validation:

- Tenant access must always be checked through membership and entitlement.
- Paid tenant creation starts from trusted billing activation, not from chat or lead status.

## TenantActivationClaim

Fields:

- `activationId`
- `billingCustomerId`
- `billingSubscriptionId`
- `billingEmail`
- `tenantId`
- `claimedByUserId`
- `status`: pending, claimed, expired, revoked
- `expiresAt`
- `createdAt`
- `claimedAt`

Validation:

- Must come from Spec 3 after trusted first payment confirmation.
- Claim requires authenticated user identity through magic link/OTP or equivalent secure login.
- Activation is single-use.
- Claim must create or link the owner membership for the correct tenant.

## Membership

Fields:

- `tenantId`
- `userId`
- `role`: owner, admin or member
- `createdAt`

Validation:

- Billing and onboarding owner actions require owner/admin role.

## StudioProfile

Fields:

- `tenantId`
- `studioName`
- `cityState`
- `contactWhatsApp`
- `activeStudentsRange`
- `scheduleModel`
- `currentSystem`
- `biggestPains`
- `createdAt`
- `updatedAt`

## AgentConfiguration

Fields:

- `tenantId`
- `agentId`
- `enabled`
- `rules`
- `tone`
- `handoffPreferences`
- `channelPermissions`
- `createdAt`
- `updatedAt`

Validation:

- `agentId` must be included by entitlement before enabling.
- Configuration is tenant-scoped.
- Launch entitlement defaults: Base configures CRM only and 0 active AI agents; 1 Agente configures one selected primary agent; 3 Agentes configures three selected primary agents; 7 Agentes configures all seven primary agents. Agente sob medida is a separate business and is not included in public launch entitlements.

## ChannelConnection

Fields:

- `tenantId`
- `channel`
- `status`: not_started, pending_manual_setup, connected, failed
- `providerAccountRef`
- `lastCheckedAt`

Validation:

- Provider secrets are never exposed to the browser.

## OnboardingProgress

Fields:

- `tenantId`
- `currentStep`
- `completedSteps`
- `requiredComplete`
- `optionalPending`
- `completedAt`

## FirstRunChecklistItem

Fields:

- `tenantId`
- `key`
- `label`
- `status`
- `required`
- `completedAt`
