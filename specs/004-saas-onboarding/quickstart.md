# Quickstart: SaaS Onboarding And Studio Setup

## Required Preconditions

- Auth system exists or is selected.
- Billing entitlement state from Spec 3 exists.
- Plan-to-agent entitlement map exists.

## Manual Scenarios

1. Complete billing test subscription.
2. Open onboarding as tenant owner.
3. Enter studio profile.
4. Configure included agents.
5. Verify unavailable agents are locked.
6. Mark WhatsApp setup as pending/manual if not connected.
7. Finish onboarding.
8. Open workspace and review first-run checklist.
9. Try accessing onboarding as unpaid user.
10. Try accessing another tenant's onboarding data.

## Safety Checks

- Tenant IDs from the client are verified by membership.
- Plan entitlements come from billing state.
- Agent configs are tenant-scoped.
- Provider secrets are server-side only.
