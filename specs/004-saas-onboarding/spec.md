# Feature Specification: SaaS Onboarding And Studio Setup

**Feature Branch**: `codex/004-saas-onboarding`
**Created**: 2026-04-30
**Status**: Draft ready for planning
**Input**: After a studio subscribes, create the account/studio setup flow that activates the SaaS workspace, confirms plan entitlement and configures the operational agents for that studio.

## Product Goal

After a trusted subscription is active, the studio owner must be able to create or access their account, set up the studio profile, confirm plan access, configure the initial agents and reach a usable first workspace without manual engineering work.

This feature starts after billing confirmation and before full daily product usage.

Commercial E2E launch readiness, post-payment activation boundaries and implementation order are defined in [../commercial-e2e-readiness-and-implementation-order.md](../commercial-e2e-readiness-and-implementation-order.md). Spec 4 owns the post-payment workspace claim, entitlement-aware setup and safe commercial-context prefill required by that cross-spec checklist.

Activation speed target: after trusted payment confirmation, initial workspace activation and self-guided setup with the onboarding Agente IA should take only a few minutes for all public plans. Full operational readiness may still depend on customer-provided data, WhatsApp connection, provider approval or optional integrations.

## Paid Activation Decision

The owner pays before creating a SaaS workspace.

After the billing provider confirms the first paid payment, Spec 3 creates a pending tenant activation tied to the billing customer/email and active entitlement. The owner then authenticates with magic link/OTP or equivalent secure login and claims the studio workspace.

Onboarding must not start paid workspace access from checkout-started, checkout-returned, chat intent, lead status, external CRM/spreadsheet record or unpaid subscription state.

Spec 2 and Spec 3 may pass safe commercial context into onboarding, but only as prefill/setup assistance. This context can include entry path, selected pains, recommended agents, recommended plan, guided-demo scenario/completion, lead ID and safe summary. It must never create access, override entitlements or enable agents outside the paid plan.

Default post-payment flow:

1. Billing confirms first paid/received payment.
2. Billing creates pending tenant activation and active entitlement.
3. Owner receives onboarding link by email and, when contact exists, WhatsApp.
4. Owner authenticates with magic link/OTP.
5. System creates or links the tenant/studio.
6. System assigns owner membership.
7. Onboarding collects studio profile.
8. Onboarding shows only agents included by current entitlement.
9. When safe commercial context exists, onboarding can prefill or suggest setup steps for the purchased plan without trusting that context as proof of access.
10. Owner reaches the first usable workspace within a few minutes when required data is provided and no external provider step is blocking.

## User Scenarios & Testing

### User Story 1 - Owner Creates Account And Studio (Priority: P1)

As a studio owner who has subscribed, I want to create my account and studio workspace, so my team can start configuring the SaaS.

**Acceptance Scenarios**:

1. **Given** billing confirms an active subscription, **When** the owner opens onboarding, **Then** the system creates or links the user to the correct tenant/studio.
2. **Given** the owner enters studio name, location and contact details, **When** onboarding saves, **Then** the data is tenant-scoped.
3. **Given** an unauthenticated visitor without active entitlement tries to access onboarding, **When** they open the flow, **Then** access is denied or redirected to subscription.
4. **Given** billing activation includes safe commercial context from the consultor or guided demo, **When** onboarding starts, **Then** the owner may see prefilled/suggested pains, agents or setup checklist items while entitlement remains the source of truth.

### User Story 2 - Owner Configures Initial Studio Profile (Priority: P1)

As a studio owner, I want to enter my operational context, so the agents can be configured for my studio's real routine.

**Acceptance Scenarios**:

1. **Given** the onboarding asks for active students, schedule model and biggest pains, **When** the owner completes the step, **Then** the profile is stored for the tenant.
2. **Given** the owner skips optional fields, **When** onboarding continues, **Then** required setup remains clear and incomplete optional data does not block the whole flow.

### User Story 3 - Owner Configures Agents By Studio (Priority: P1)

As a studio owner, I want to configure how each included agent should behave for my studio, so the SaaS is not generic.

**Acceptance Scenarios**:

1. **Given** the tenant has 7 Agentes entitlement, **When** onboarding shows included agents, **Then** the seven primary agents can be configured according to plan access.
2. **Given** the tenant has Base, 1 Agente or 3 Agentes entitlement, **When** unavailable agents appear, **Then** they are locked or upsell-gated.
3. **Given** the owner configures Atendimento or Agenda, **When** they save rules, **Then** rules are stored tenant-scoped and do not affect other studios.

### User Story 4 - Owner Connects Channels And Tools (Priority: P2)

As a studio owner, I want to connect WhatsApp and basic operational tools when available, so agents can work with real channels.

**Acceptance Scenarios**:

1. **Given** WhatsApp connection is available, **When** the owner starts connection, **Then** the system guides them through authorized setup without exposing provider secrets.
2. **Given** a connection is not configured yet, **When** onboarding reaches that step, **Then** the system marks it as pending/manual setup instead of blocking everything.

### User Story 5 - Owner Reaches First Workspace (Priority: P1)

As a studio owner, I want to finish onboarding and land in the SaaS workspace, so I can see what is ready and what still needs setup.

**Acceptance Scenarios**:

1. **Given** required onboarding steps are complete, **When** the owner finishes, **Then** the system opens the workspace with setup status and next actions.
2. **Given** some optional setup remains incomplete, **When** the workspace opens, **Then** the system shows a clear checklist without hiding active access.

## Functional Requirements

- **FR-001**: Onboarding MUST require authenticated user identity.
- **FR-002**: Onboarding MUST require an active paid entitlement from Spec 3 before creating paid workspace access. Trial entitlement is not allowed in v1.
- **FR-003**: The system MUST create a tenant/studio workspace scoped to the subscribed customer.
- **FR-004**: Tenant membership and owner role MUST be established during onboarding.
- **FR-005**: Studio profile MUST capture studio name, city/state, contact WhatsApp, active student range, schedule model, current system and biggest pains.
- **FR-006**: Agent setup MUST be tenant-scoped.
- **FR-007**: Included agents MUST be determined by current plan entitlement.
- **FR-008**: Locked or unavailable agents MUST not be configurable without entitlement.
- **FR-009**: The seven primary agents MUST be configurable by studio when included by plan: Atendimento, Agenda, Vendas, Financeiro, Retencao, Gestao and Historico/Evolucao.
- **FR-010**: Agente sob medida MUST remain a separate request/follow-up path, not a hidden default agent.
- **FR-011**: Onboarding MUST show setup progress and incomplete steps.
- **FR-012**: Onboarding MUST not expose secrets for WhatsApp, billing provider or AI provider.
- **FR-013**: Cross-tenant access to onboarding data MUST be denied.
- **FR-014**: Sensitive changes such as owner assignment, agent channel connection and plan-derived access changes MUST be audited.
- **FR-015**: The workspace MUST show a first-run checklist after onboarding completion.
- **FR-016**: If billing entitlement changes later, onboarding/workspace access MUST reflect the new entitlement.
- **FR-017**: Onboarding MUST start from a trusted pending tenant activation created after first paid billing confirmation.
- **FR-018**: Owner authentication MUST use magic link/OTP or equivalent secure login before workspace claim.
- **FR-019**: A lead record, chat session, external CRM/spreadsheet status or checkout return URL MUST NOT create paid onboarding access.
- **FR-020**: Plan setup screens MUST use the same launch entitlement config as billing, including included agents, user limits, WhatsApp channel limits, studio-unit limits and usage caps.
- **FR-021**: Base onboarding MUST not enable active AI agents.
- **FR-022**: 1 Agente onboarding MUST let the owner configure one selected primary agent according to plan rules.
- **FR-023**: 3 Agentes onboarding MUST let the owner configure three selected primary agents according to plan rules.
- **FR-024**: 7 Agentes onboarding MUST let the owner configure all seven primary agents.
- **FR-025**: Base onboarding MUST behave as CRM-only setup.
- **FR-026**: Public launch onboarding MUST support one studio/unit only; multi-unit onboarding is deferred to a future Enterprise plan.
- **FR-027**: Studio agent WhatsApp setup MUST connect the studio's own WhatsApp, not the SaaS sales WhatsApp.
- **FR-028**: Agente sob medida setup MUST NOT appear as an included entitlement in any public launch plan.
- **FR-029**: Onboarding MAY consume safe commercial context from Spec 2/Spec 3 to prefill or suggest setup, including entry path, selected pains, recommended agents, recommended plan, guided-demo scenario/completion, lead ID and safe summary.
- **FR-030**: Commercial context MUST NOT grant access, override plan entitlement, enable unavailable agents or bypass tenant authorization.
- **FR-031**: When commercial context conflicts with active entitlement, onboarding MUST prefer billing entitlement and show locked/upsell-gated states.
- **FR-032**: Onboarding SHOULD complete initial workspace activation and self-guided AI setup within a few minutes for all public plans when payment is confirmed and required customer inputs are available.
- **FR-033**: Onboarding MUST clearly distinguish active workspace access from external/pending setup items such as WhatsApp connection, provider approval or missing studio data.

## Key Entities

- **User Account**: Authenticated person using the SaaS.
- **Tenant/Studio Workspace**: Customer organization representing one studio or studio group.
- **Membership**: User relationship to a tenant with role.
- **Studio Profile**: Business context and operational setup for a studio.
- **Agent Configuration**: Tenant-specific rules, tone, permissions and enabled flows for an included agent.
- **Channel Connection**: Tenant-scoped connection status for WhatsApp or future tools.
- **Onboarding Progress**: Required and optional setup state.
- **First-Run Checklist**: Workspace checklist shown after onboarding.
- **Commercial Context Prefill**: Safe sales/demo context attached after billing activation to help personalize onboarding without granting access.

## Success Criteria

- **SC-001**: A paid tenant can create an account/studio workspace and reach the first workspace without manual database edits.
- **SC-002**: A non-entitled visitor cannot access paid onboarding.
- **SC-003**: Agent configuration is scoped per tenant and does not leak across studios.
- **SC-004**: Plan entitlements determine which agents are configurable.
- **SC-005**: Onboarding completion produces a clear next-action checklist in the workspace.
- **SC-006**: Cross-tenant onboarding access tests fail safely.
- **SC-007**: A paid tenant arriving from consultor/demo sees relevant prefilled setup suggestions, but unavailable agents remain locked by entitlement.

## Out Of Scope

- Billing provider checkout/webhooks.
- Public landing design.
- Atendente IA sales conversation.
- Full operational agent runtime.
- Full CRM/calendar/payment integrations beyond setup status.

## Dependencies

- Spec 3 must provide trusted active paid entitlement state.
- Spec 2 and Spec 3 may pass assisted/demo/plan context into onboarding, but onboarding cannot trust chat-only subscription status.
