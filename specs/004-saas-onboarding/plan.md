# Implementation Plan: SaaS Onboarding And Studio Setup

**Branch**: `codex/004-saas-onboarding` | **Date**: 2026-04-30 | **Spec**: [spec.md](./spec.md)

## Summary

Create the authenticated onboarding path that turns an active subscribed tenant into a usable studio workspace. This includes tenant creation/linking, owner membership, studio profile, plan-derived agent availability, initial per-studio agent configuration, setup progress and first-run workspace checklist.

## Technical Context

**Project Type**: Next.js SaaS web app  
**Storage**: Durable database for users, tenants, memberships, studio profile, agent configs and onboarding progress  
**Dependencies**: Billing entitlement from Spec 3; public offer/config from Spec 1; agent definitions from future operational agent specs  
**Security**: Tenant isolation, role checks and audited sensitive setup actions

## Architecture Decisions

- Onboarding is authenticated.
- Tenant ID is never trusted from client input without verifying membership/ownership.
- Active entitlement from Spec 3 gates paid workspace access.
- Agent setup data is tenant-scoped.
- Channel/provider secrets stay server-side.
- Incomplete optional setup does not block workspace access after required steps.

## Planned Modules

```text
app/onboarding/
  page.tsx

app/app/
  page.tsx

lib/onboarding/
  progress.ts
  studio-profile.ts
  agent-setup.ts
  checklist.ts

lib/tenancy/
  tenant.ts
  membership.ts
  authorization.ts
```

## Rollout Phases

### Phase 1: Tenant And Account Foundation

- Define tenant, user and membership model.
- Gate onboarding by entitlement.
- Create/link tenant after trusted billing activation.

### Phase 2: Studio Profile

- Capture core studio context.
- Save tenant-scoped profile.
- Track onboarding progress.

### Phase 3: Agent Setup

- Show plan-included agents.
- Configure initial rules per included agent.
- Lock unavailable agents.

### Phase 4: Channel/Tool Setup Status

- Show WhatsApp/tool setup status.
- Mark manual/pending setup clearly where needed.

### Phase 5: First Workspace

- Show first-run checklist.
- Route owner into workspace after required steps.

## Verification

- Paid tenant reaches onboarding.
- Unpaid visitor is denied.
- Tenant A cannot read Tenant B onboarding/profile/agent config.
- Agent availability follows entitlement.
- Workspace checklist reflects setup status.
