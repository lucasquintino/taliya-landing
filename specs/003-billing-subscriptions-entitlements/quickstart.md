# Quickstart: Billing, Subscriptions And Entitlements

## Required Decisions

- Billing provider.
- Supported payment methods.
- Tax/invoice requirements.
- Monthly and annual billing availability.
- Coupon/guarantee policy.
- Past-due access policy.

## Required Environment

- Billing provider secret key.
- Billing webhook signing secret.
- Billing portal configuration if supported.
- Public success/cancel URLs.

## Manual Scenarios

1. Create checkout for 7 Agentes.
2. Complete payment in provider test mode.
3. Verify webhook activates subscription and entitlement.
4. Attempt access before webhook confirmation.
5. Replay duplicate webhook.
6. Cancel subscription and verify entitlement updates.
7. Open billing portal as tenant owner.
8. Attempt billing portal as non-owner.
9. Verify no plan is configured with free trial/trial period.
10. Simulate or inspect any `trialing` provider state and verify it does not grant active access in v1.

## Safety Checks

- No card data is collected by the app.
- No client query param grants active subscription.
- No public checkout creates a free trial.
- Webhook signature is required.
- Webhook events are idempotent.
- Entitlements are tenant-scoped.
